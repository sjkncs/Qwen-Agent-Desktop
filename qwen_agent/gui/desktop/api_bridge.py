"""
Qwen-Agent Desktop App - Python API Bridge
Handles communication between the web frontend and Qwen-Agent backend.
All public methods are callable from JavaScript via pywebview's js_api.
"""

import json
import os
import threading
import uuid
from datetime import datetime
from pathlib import Path

DATA_DIR = Path.home() / '.qwen-agent-desktop'
CONVERSATIONS_DIR = DATA_DIR / 'conversations'


class ApiBridge:
    """pywebview JS API bridge — every public method is callable from JS."""

    def __init__(self, window=None, api_key='', api_base='', default_model=''):
        self._window = window
        self._api_key = api_key
        self._api_base = api_base
        self._default_model = default_model
        self._conversations = {}
        self._current_conv_id = None
        self._streaming = False
        self._cancel_flag = False

        CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)
        self._load_conversations()

    def set_window(self, window):
        self._window = window

    # ═══════════════════════════════════════════
    #  Conversation Management
    # ═══════════════════════════════════════════

    def new_conversation(self):
        conv_id = str(uuid.uuid4())[:8]
        self._conversations[conv_id] = {
            'title': '新对话',
            'messages': [],
            'created_at': datetime.now().isoformat(),
            'model': self._default_model,
        }
        self._current_conv_id = conv_id
        self._save_conversations()
        return json.dumps({'id': conv_id, 'title': '新对话'})

    def get_conversations(self):
        result = []
        for cid, conv in sorted(
            self._conversations.items(),
            key=lambda x: x[1].get('created_at', ''),
            reverse=True,
        ):
            result.append({
                'id': cid,
                'title': conv['title'],
                'created_at': conv.get('created_at', ''),
                'message_count': len(conv.get('messages', [])),
            })
        return json.dumps(result)

    def switch_conversation(self, conv_id):
        if conv_id in self._conversations:
            self._current_conv_id = conv_id
            return json.dumps(self._conversations[conv_id].get('messages', []))
        return json.dumps([])

    def delete_conversation(self, conv_id):
        if conv_id in self._conversations:
            del self._conversations[conv_id]
            self._save_conversations()
            if self._current_conv_id == conv_id:
                self._current_conv_id = None
        return json.dumps({'ok': True})

    def rename_conversation(self, conv_id, new_title):
        if conv_id in self._conversations:
            self._conversations[conv_id]['title'] = new_title
            self._save_conversations()
        return json.dumps({'ok': True})

    def get_current_conv_id(self):
        return json.dumps(self._current_conv_id)

    # ═══════════════════════════════════════════
    #  Chat / Streaming
    # ═══════════════════════════════════════════

    def send_message(self, text, mode='chat', model=None):
        """Send a user message and start streaming the response."""
        if not text or not text.strip():
            return json.dumps({'ok': False, 'error': 'empty'})

        if not self._current_conv_id:
            self.new_conversation()

        conv = self._conversations[self._current_conv_id]
        conv['messages'].append({'role': 'user', 'content': text})

        # Auto-title from first user message
        if sum(1 for m in conv['messages'] if m['role'] == 'user') == 1:
            conv['title'] = text[:30] + ('…' if len(text) > 30 else '')
            self._push_js(
                f"onConversationTitleUpdate({json.dumps(self._current_conv_id)},{json.dumps(conv['title'])})"
            )

        use_model = model or conv.get('model', self._default_model)

        system_prompt = self._get_system_prompt(mode)

        self._streaming = True
        self._cancel_flag = False
        t = threading.Thread(
            target=self._stream_response,
            args=(conv, system_prompt, use_model),
            daemon=True,
        )
        t.start()
        self._save_conversations()
        return json.dumps({'ok': True})

    def cancel_stream(self):
        self._cancel_flag = True
        return json.dumps({'ok': True})

    def is_streaming(self):
        return json.dumps(self._streaming)

    def _stream_response(self, conv, system_prompt, model):
        try:
            import openai
            client = openai.OpenAI(api_key=self._api_key, base_url=self._api_base)

            api_messages = []
            if system_prompt:
                api_messages.append({'role': 'system', 'content': system_prompt})
            api_messages.extend([
                {'role': m['role'], 'content': m['content']}
                for m in conv['messages']
            ])

            stream = client.chat.completions.create(
                model=model,
                messages=api_messages,
                stream=True,
                max_tokens=4096,
            )

            full_response = ''
            for chunk in stream:
                if self._cancel_flag:
                    break
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    full_response += delta.content
                    self._push_js(f"onStreamToken({json.dumps(delta.content)})")

            conv['messages'].append({'role': 'assistant', 'content': full_response})
            self._save_conversations()

        except Exception as e:
            self._push_js(f"onStreamError({json.dumps(str(e))})")
        finally:
            self._streaming = False
            self._push_js("onStreamDone()")

    def _get_system_prompt(self, mode):
        prompts = {
            'chat': '你是Qwen-Agent，一个强大的AI助手。请用简洁清晰的语言回复用户。',
            'think': (
                '你是Qwen-Agent，一个擅长深度思考和分析的AI助手。'
                '请对用户的问题进行深入、多角度的分析，展示你的思考过程和推理链。'
            ),
            'code': (
                '你是Qwen-Agent，一个专业的编程助手。'
                '请提供高质量、可运行的代码解决方案，包含适当的注释。'
            ),
            'analyze': (
                '你是Qwen-Agent，一个专业的文本分析助手。'
                '请对用户提供的文本进行全面分析，包括主题提取、情感分析、关键信息识别、'
                '结构分析等维度。输出结构化的分析报告。'
            ),
            'translate': (
                '你是Qwen-Agent，一个专业的翻译助手。'
                '请准确翻译用户提供的文本，保持原文的语气和风格。'
                '如果是中文则翻译为英文，如果是其他语言则翻译为中文。'
            ),
            'write': (
                '你是Qwen-Agent，一个专业的写作助手。'
                '请帮助用户完成高质量的文本创作，注意文笔流畅、逻辑清晰。'
            ),
            'research': (
                '你是Qwen-Agent，一个擅长深度研究和调查分析的AI助手。'
                '请对用户的问题进行全面深入的研究，从多个信息来源和角度进行分析，'
                '给出详尽的研究报告，包含背景、现状、数据、趋势和结论。'
            ),
            'image': (
                '你是Qwen-Agent，一个专业的图像理解和生成助手。'
                '请根据用户的需求描述、分析或创意生成相关的图像内容描述。'
            ),
        }
        return prompts.get(mode, prompts['chat'])

    # ═══════════════════════════════════════════
    #  Model Management
    # ═══════════════════════════════════════════

    def get_models(self):
        models = [
            {'id': 'claude-sonnet-4-5', 'name': 'Claude Sonnet 4.5', 'provider': 'Anthropic'},
            {'id': 'claude-opus-4-6', 'name': 'Claude Opus 4.6', 'provider': 'Anthropic'},
            {'id': 'gpt-5', 'name': 'GPT-5', 'provider': 'OpenAI'},
            {'id': 'gpt-5-mini', 'name': 'GPT-5 Mini', 'provider': 'OpenAI'},
            {'id': 'gemini-3-pro', 'name': 'Gemini 3 Pro', 'provider': 'Google'},
            {'id': 'gemini-2.5-pro', 'name': 'Gemini 2.5 Pro', 'provider': 'Google'},
            {'id': 'grok-4', 'name': 'Grok 4', 'provider': 'xAI'},
            {'id': 'gpt-4o', 'name': 'GPT-4o', 'provider': 'OpenAI'},
        ]
        return json.dumps(models)

    def get_current_model(self):
        if self._current_conv_id and self._current_conv_id in self._conversations:
            return json.dumps(self._conversations[self._current_conv_id].get('model', self._default_model))
        return json.dumps(self._default_model)

    def set_model(self, model_id):
        if self._current_conv_id and self._current_conv_id in self._conversations:
            self._conversations[self._current_conv_id]['model'] = model_id
            self._save_conversations()
        self._default_model = model_id
        return json.dumps({'ok': True})

    # ═══════════════════════════════════════════
    #  System Info
    # ═══════════════════════════════════════════

    def get_system_info(self):
        info = {'cpu': '', 'ram': '', 'gpu': '', 'os': ''}
        try:
            import platform
            info['os'] = platform.system() + ' ' + platform.release()
            info['cpu'] = platform.processor() or ''
        except Exception:
            pass
        try:
            import psutil
            info['ram'] = f'{psutil.virtual_memory().total / (1024 ** 3):.1f} GB'
        except Exception:
            pass
        try:
            from qwen_agent.utils.hw_config import get_hw_profile
            hw = get_hw_profile()
            if hw.cuda_available:
                info['gpu'] = f'{hw.gpu_name} ({hw.gpu_vram_gb:.0f}GB)'
            info['cpu'] = f'{hw.cpu_cores}C/{hw.cpu_threads}T'
            info['ram'] = f'{hw.system_ram_gb:.1f} GB'
        except Exception:
            pass
        return json.dumps(info)

    # ═══════════════════════════════════════════
    #  Preferences
    # ═══════════════════════════════════════════

    def get_preference(self, key):
        prefs = self._load_prefs()
        return json.dumps(prefs.get(key))

    def set_preference(self, key, value):
        prefs = self._load_prefs()
        prefs[key] = value
        self._save_prefs(prefs)
        return json.dumps({'ok': True})

    def _load_prefs(self):
        pref_file = DATA_DIR / 'preferences.json'
        if pref_file.exists():
            try:
                return json.loads(pref_file.read_text(encoding='utf-8'))
            except Exception:
                pass
        return {}

    def _save_prefs(self, prefs):
        pref_file = DATA_DIR / 'preferences.json'
        try:
            pref_file.write_text(json.dumps(prefs, ensure_ascii=False, indent=2), encoding='utf-8')
        except Exception:
            pass

    # ═══════════════════════════════════════════
    #  File Handling
    # ═══════════════════════════════════════════

    def read_file_content(self, file_path):
        """Read a file and return its text content (up to 50KB)."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read(50000)
            return json.dumps({
                'name': os.path.basename(file_path),
                'content': content,
                'size': os.path.getsize(file_path),
            })
        except Exception as e:
            return json.dumps({'error': str(e)})

    # ═══════════════════════════════════════════
    #  Persistence Helpers
    # ═══════════════════════════════════════════

    def _save_conversations(self):
        try:
            data_file = CONVERSATIONS_DIR / 'conversations.json'
            data_file.write_text(
                json.dumps(self._conversations, ensure_ascii=False, indent=2),
                encoding='utf-8',
            )
        except Exception:
            pass

    def _load_conversations(self):
        try:
            data_file = CONVERSATIONS_DIR / 'conversations.json'
            if data_file.exists():
                self._conversations = json.loads(data_file.read_text(encoding='utf-8'))
        except Exception:
            self._conversations = {}

    def _push_js(self, js_code):
        """Safely evaluate JS in the frontend window."""
        if self._window:
            try:
                self._window.evaluate_js(js_code)
            except Exception:
                pass
