# Copyright 2023 The Qwen team, Alibaba Group. All rights reserved.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pprint
import re
from typing import List, Optional, Union

from qwen_agent import Agent, MultiAgentHub
from qwen_agent.agents.user_agent import PENDING_USER_INPUT
from qwen_agent.gui.gradio_utils import format_cover_html
from qwen_agent.gui.utils import convert_fncall_to_text, convert_history_to_chatbot, get_avatar_image
from qwen_agent.llm.schema import AUDIO, CONTENT, FILE, IMAGE, NAME, ROLE, USER, VIDEO, Message
from qwen_agent.log import logger
from qwen_agent.utils.utils import print_traceback


_QWEN_LOGO_SVG = '''<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
  <defs><linearGradient id="qg" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" style="stop-color:#6366f1"/><stop offset="100%" style="stop-color:#06b6d4"/>
  </linearGradient></defs>
  <circle cx="60" cy="60" r="56" fill="url(#qg)" opacity="0.12"/>
  <circle cx="60" cy="60" r="42" fill="url(#qg)" opacity="0.20"/>
  <text x="60" y="72" text-anchor="middle" font-size="42" font-weight="800"
        font-family="Inter,system-ui,sans-serif" fill="url(#qg)">Q</text>
</svg>'''


def _build_splash_html() -> str:
    """Build the startup splash screen overlay."""
    return f'''
<div id="qa-splash">
  <div class="splash-logo">{_QWEN_LOGO_SVG}</div>
  <div class="splash-title">Qwen-Agent</div>
  <div class="splash-sub">POWERED BY QWEN</div>
  <div class="splash-bar"><div class="splash-bar-fill"></div></div>
</div>
'''


def _build_fab_html() -> str:
    """Build the floating action button with expandable menu."""
    return '''
<div id="qa-fab">
  <button class="fab-main" onclick="document.getElementById('qa-fab').classList.toggle('expanded');this.classList.toggle('open')" title="菜单">
    ✦
  </button>
  <div class="fab-menu">
    <button class="fab-item" onclick="document.body.classList.toggle('dark-mode');localStorage.setItem('qa-dark',document.body.classList.contains('dark-mode'))" title="切换主题">
      <span class="fab-tooltip">深色/浅色</span>🌓
    </button>
    <button class="fab-item" onclick="window.scrollTo({top:0,behavior:'smooth'})" title="回到顶部">
      <span class="fab-tooltip">回到顶部</span>↑
    </button>
    <button class="fab-item" onclick="let c=document.querySelector('[data-testid=chatbot]');if(c)c.scrollTo({top:c.scrollHeight,behavior:'smooth'})" title="滚到底部">
      <span class="fab-tooltip">滚到底部</span>↓
    </button>
    <button class="fab-item" onclick="if(document.fullscreenElement)document.exitFullscreen();else document.documentElement.requestFullscreen()" title="全屏">
      <span class="fab-tooltip">全屏切换</span>⛶
    </button>
  </div>
</div>
<script>
// Restore dark mode preference
if(localStorage.getItem('qa-dark')==='true') document.body.classList.add('dark-mode');
// Auto-remove splash after animation completes
setTimeout(function(){var s=document.getElementById('qa-splash');if(s)s.remove();},3200);
</script>
'''


def _build_hw_info_html() -> str:
    """Build static hardware config panel (shown once at startup)."""
    try:
        from qwen_agent.utils.hw_config import get_hw_profile
        hw = get_hw_profile()
        rows = []
        if hw.cuda_available:
            rows.append(('GPU', hw.gpu_name))
            rows.append(('VRAM', f'{hw.gpu_vram_gb:.1f} GB'))
            rows.append(('Compute', hw.gpu_compute_capability))
            rows.append(('Dtype', hw.recommended_dtype))
            if hw.recommended_quantization:
                rows.append(('Quant', hw.recommended_quantization.upper()))
            rows.append(('Flash Attn', '✓' if hw.flash_attn_available else '✗'))
            rows.append(('Ctx Tokens', f'{hw.recommended_max_input_tokens:,}'))
        else:
            rows.append(('Device', 'CPU'))
            rows.append(('Cores', f'{hw.cpu_cores}C / {hw.cpu_threads}T'))
        rows.append(('RAM', f'{hw.system_ram_gb:.1f} GB'))

        table_rows = ''.join(
            f'<tr><td class="hw-key">{k}</td><td class="hw-val">{v}</td></tr>'
            for k, v in rows
        )
        return f'<div class="hw-panel"><div class="hw-title">⚡ 硬件加速状态</div><table class="hw-table">{table_rows}</table></div>'
    except Exception:
        return ''


def _build_gpu_stats_html() -> str:
    """Build live GPU utilization / VRAM usage panel (called every ~3s)."""
    try:
        import torch
        if not torch.cuda.is_available():
            return ''
        # Memory stats
        mem_alloc = torch.cuda.memory_allocated(0) / (1024 ** 3)
        mem_total_bytes = torch.cuda.get_device_properties(0).total_memory
        mem_total = mem_total_bytes / (1024 ** 3)
        mem_pct = mem_alloc / mem_total * 100 if mem_total > 0 else 0
        mem_bar_cls = 'bar-green' if mem_pct < 60 else ('bar-yellow' if mem_pct < 85 else 'bar-red')

        # GPU utilization via pynvml (optional)
        util_pct = None
        try:
            import pynvml
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            util_pct = util.gpu
        except Exception:
            pass

        util_row = ''
        if util_pct is not None:
            u_cls = 'bar-green' if util_pct < 60 else ('bar-yellow' if util_pct < 85 else 'bar-red')
            util_row = (
                f'<tr><td class="hw-key">GPU利用率</td>'
                f'<td class="hw-val">{util_pct}%'
                f'<span class="bar-wrap"><span class="bar-fill {u_cls}" style="width:{util_pct}%"></span></span>'
                f'</td></tr>'
            )

        mem_row = (
            f'<tr><td class="hw-key">显存占用</td>'
            f'<td class="hw-val">{mem_alloc:.1f}/{mem_total:.1f}GB'
            f'<span class="bar-wrap"><span class="bar-fill {mem_bar_cls}" style="width:{mem_pct:.0f}%"></span></span>'
            f'</td></tr>'
        )

        table = f'<table class="hw-table">{util_row}{mem_row}</table>'
        return f'<div class="hw-panel"><div class="hw-title">📊 实时显存监控</div>{table}</div>'
    except Exception:
        return ''


class WebUI:
    """A Common chatbot application for agent."""

    def __init__(self, agent: Union[Agent, MultiAgentHub, List[Agent]], chatbot_config: Optional[dict] = None):
        """
        Initialization the chatbot.

        Args:
            agent: The agent or a list of agents,
                supports various types of agents such as Assistant, GroupChat, Router, etc.
            chatbot_config: The chatbot configuration.
                Set the configuration as {'user.name': '', 'user.avatar': '', 'agent.avatar': '', 'input.placeholder': '', 'prompt.suggestions': []}.
        """
        chatbot_config = chatbot_config or {}

        if isinstance(agent, MultiAgentHub):
            self.agent_list = [agent for agent in agent.nonuser_agents]
            self.agent_hub = agent
        elif isinstance(agent, list):
            self.agent_list = agent
            self.agent_hub = None
        else:
            self.agent_list = [agent]
            self.agent_hub = None

        user_name = chatbot_config.get('user.name', 'user')
        self.user_config = {
            'name': user_name,
            'avatar': chatbot_config.get(
                'user.avatar',
                get_avatar_image(user_name),
            ),
        }

        self.agent_config_list = [{
            'name': agent.name,
            'avatar': chatbot_config.get(
                'agent.avatar',
                get_avatar_image(agent.name),
            ),
            'description': agent.description or "I'm a helpful assistant.",
        } for agent in self.agent_list]

        self.input_placeholder = chatbot_config.get('input.placeholder', '跟我聊聊吧～')
        self.prompt_suggestions = chatbot_config.get('prompt.suggestions', [])
        self.verbose = chatbot_config.get('verbose', False)

    """
    Run the chatbot.

    Args:
        messages: The chat history.
    """

    def run(self,
            messages: List[Message] = None,
            share: bool = False,
            server_name: str = None,
            server_port: int = None,
            concurrency_limit: int = 10,
            enable_mention: bool = False,
            **kwargs):
        self.run_kwargs = kwargs

        from qwen_agent.gui.gradio_dep import gr, mgr, ms

        customTheme = gr.themes.Default(
            primary_hue=gr.themes.utils.colors.indigo,
            secondary_hue=gr.themes.utils.colors.slate,
            neutral_hue=gr.themes.utils.colors.gray,
            radius_size=gr.themes.utils.sizes.radius_md,
            font=[gr.themes.GoogleFont('Inter'), gr.themes.GoogleFont('Noto Sans SC')],
        ).set(
            body_background_fill='#f7f8fa',
            block_background_fill='#ffffff',
            block_border_color='#e5e7eb',
            block_label_text_color='#6b7280',
            body_text_color='#1a1a2e',
            body_text_color_subdued='#9ca3af',
            input_background_fill='#ffffff',
            input_border_color='#e5e7eb',
            button_primary_background_fill='#6366f1',
            button_primary_text_color='#ffffff',
            button_secondary_background_fill='#ffffff',
            button_secondary_border_color='#e5e7eb',
        )

        _latex_delimiters = [
            {'left': '\\(', 'right': '\\)', 'display': True},
            {'left': '\\begin{equation}', 'right': '\\end{equation}', 'display': True},
            {'left': '\\begin{align}', 'right': '\\end{align}', 'display': True},
            {'left': '\\begin{alignat}', 'right': '\\end{alignat}', 'display': True},
            {'left': '\\begin{gather}', 'right': '\\end{gather}', 'display': True},
            {'left': '\\begin{CD}', 'right': '\\end{CD}', 'display': True},
            {'left': '\\[', 'right': '\\]', 'display': True},
        ]

        with gr.Blocks(
                css=os.path.join(os.path.dirname(__file__), 'assets/appBot.css'),
                theme=customTheme,
                title='Qwen-Agent',
        ) as demo:
            # ── Splash screen + FAB overlay ──────────────────────
            gr.HTML(value=_build_splash_html())
            gr.HTML(value=_build_fab_html())

            history = gr.State([])
            with ms.Application():
                with gr.Row(elem_classes='container'):
                    # ── Left: chat panel ──────────────────────────────────
                    with gr.Column(scale=4):
                        chatbot = mgr.Chatbot(
                            value=convert_history_to_chatbot(messages=messages),
                            avatar_images=[self.user_config, self.agent_config_list],
                            height=750,
                            avatar_image_width=64,
                            flushing=False,
                            show_copy_button=True,
                            latex_delimiters=_latex_delimiters,
                        )

                        with gr.Row():
                            input = mgr.MultimodalInput(
                                placeholder=self.input_placeholder,
                                scale=9,
                            )
                            clear_btn = gr.Button(
                                '🗑️ 清空',
                                variant='secondary',
                                scale=1,
                                min_width=72,
                            )

                        audio_input = gr.Audio(
                            label='🎙️ 语音输入',
                            sources=['microphone'],
                            type='filepath',
                        )

                    # ── Right: sidebar ────────────────────────────────────
                    with gr.Column(scale=1, elem_classes='qa-sidebar'):
                        if len(self.agent_list) > 1:
                            agent_selector = gr.Dropdown(
                                [(agent.name, i) for i, agent in enumerate(self.agent_list)],
                                label='🤖 Agents',
                                info='选择一个 Agent',
                                value=0,
                                interactive=True,
                            )

                        agent_info_block = self._create_agent_info_block()
                        agent_plugins_block = self._create_agent_plugins_block()

                        hw_info_block = gr.HTML(value=_build_hw_info_html())
                        gpu_stats_block = gr.HTML(value=_build_gpu_stats_html())

                        if self.prompt_suggestions:
                            gr.Examples(
                                label='💡 推荐对话',
                                examples=self.prompt_suggestions,
                                inputs=[input],
                            )

                    # ── Event wiring ──────────────────────────────────────
                    if len(self.agent_list) > 1:
                        agent_selector.change(
                            fn=self.change_agent,
                            inputs=[agent_selector],
                            outputs=[agent_selector, agent_info_block, agent_plugins_block],
                            queue=False,
                        )

                    clear_btn.click(
                        fn=self.clear_history,
                        inputs=None,
                        outputs=[chatbot, history],
                        queue=False,
                    )

                    input_promise = input.submit(
                        fn=self.add_text,
                        inputs=[input, audio_input, chatbot, history],
                        outputs=[input, audio_input, chatbot, history],
                        queue=False,
                    )

                    if len(self.agent_list) > 1 and enable_mention:
                        input_promise = input_promise.then(
                            self.add_mention,
                            [chatbot, agent_selector],
                            [chatbot, agent_selector],
                        ).then(
                            self.agent_run,
                            [chatbot, history, agent_selector],
                            [chatbot, history, agent_selector],
                        )
                    else:
                        input_promise = input_promise.then(
                            self.agent_run,
                            [chatbot, history],
                            [chatbot, history],
                        )

                    input_promise.then(self.flushed, None, [input])

                    # Live GPU stats refresh every 3 seconds
                    try:
                        gpu_timer = gr.Timer(value=3)
                        gpu_timer.tick(fn=_build_gpu_stats_html, outputs=[gpu_stats_block])
                    except Exception:
                        pass

            demo.load(None)

        demo.queue(default_concurrency_limit=concurrency_limit).launch(
            share=share,
            server_name=server_name,
            server_port=server_port,
        )

    def change_agent(self, agent_selector):
        yield agent_selector, self._create_agent_info_block(agent_selector), self._create_agent_plugins_block(
            agent_selector)

    def add_text(self, _input, _audio_input, _chatbot, _history):
        _history.append({
            ROLE: USER,
            CONTENT: [{
                'text': _input.text
            }],
        })

        if self.user_config[NAME]:
            _history[-1][NAME] = self.user_config[NAME]
        
        # if got audio from microphone, append it to the multimodal inputs
        if _audio_input:
            from qwen_agent.gui.gradio_dep import gr, mgr, ms
            audio_input_file = gr.data_classes.FileData(path=_audio_input, mime_type="audio/wav")
            _input.files.append(audio_input_file)

        if _input.files:
            for file in _input.files:
                if file.mime_type.startswith('image/'):
                    _history[-1][CONTENT].append({IMAGE: 'file://' + file.path})
                elif file.mime_type.startswith('audio/'):
                    _history[-1][CONTENT].append({AUDIO: 'file://' + file.path})
                elif file.mime_type.startswith('video/'):
                    _history[-1][CONTENT].append({VIDEO: 'file://' + file.path})
                else:
                    _history[-1][CONTENT].append({FILE: file.path})

        _chatbot.append([_input, None])

        from qwen_agent.gui.gradio_dep import gr

        yield gr.update(interactive=False, value=None), None, _chatbot, _history

    def add_mention(self, _chatbot, _agent_selector):
        if len(self.agent_list) == 1:
            yield _chatbot, _agent_selector

        query = _chatbot[-1][0].text
        match = re.search(r'@\w+\b', query)
        if match:
            _agent_selector = self._get_agent_index_by_name(match.group()[1:])

        agent_name = self.agent_list[_agent_selector].name

        if ('@' + agent_name) not in query and self.agent_hub is None:
            _chatbot[-1][0].text = '@' + agent_name + ' ' + query

        yield _chatbot, _agent_selector

    def agent_run(self, _chatbot, _history, _agent_selector=None):
        if self.verbose:
            logger.info('agent_run input:\n' + pprint.pformat(_history, indent=2))

        num_input_bubbles = len(_chatbot) - 1
        num_output_bubbles = 1
        _chatbot[-1][1] = [None for _ in range(len(self.agent_list))]

        agent_runner = self.agent_list[_agent_selector or 0]
        if self.agent_hub:
            agent_runner = self.agent_hub
        responses = []
        for responses in agent_runner.run(_history, **self.run_kwargs):
            if not responses:
                continue
            if responses[-1][CONTENT] == PENDING_USER_INPUT:
                logger.info('Interrupted. Waiting for user input!')
                break

            display_responses = convert_fncall_to_text(responses)
            if not display_responses:
                continue
            if display_responses[-1][CONTENT] is None:
                continue

            while len(display_responses) > num_output_bubbles:
                # Create a new chat bubble
                _chatbot.append([None, None])
                _chatbot[-1][1] = [None for _ in range(len(self.agent_list))]
                num_output_bubbles += 1

            assert num_output_bubbles == len(display_responses)
            assert num_input_bubbles + num_output_bubbles == len(_chatbot)

            for i, rsp in enumerate(display_responses):
                agent_index = self._get_agent_index_by_name(rsp[NAME])
                _chatbot[num_input_bubbles + i][1][agent_index] = rsp[CONTENT]

            if len(self.agent_list) > 1:
                _agent_selector = agent_index

            if _agent_selector is not None:
                yield _chatbot, _history, _agent_selector
            else:
                yield _chatbot, _history

        if responses:
            _history.extend([res for res in responses if res[CONTENT] != PENDING_USER_INPUT])

        if _agent_selector is not None:
            yield _chatbot, _history, _agent_selector
        else:
            yield _chatbot, _history

        if self.verbose:
            logger.info('agent_run response:\n' + pprint.pformat(responses, indent=2))

    def flushed(self):
        from qwen_agent.gui.gradio_dep import gr

        return gr.update(interactive=True)

    def clear_history(self):
        return [], []

    def _get_agent_index_by_name(self, agent_name):
        if agent_name is None:
            return 0

        try:
            agent_name = agent_name.strip()
            for i, agent in enumerate(self.agent_list):
                if agent.name == agent_name:
                    return i
            return 0
        except Exception:
            print_traceback()
            return 0

    def _create_agent_info_block(self, agent_index=0):
        from qwen_agent.gui.gradio_dep import gr

        agent_config_interactive = self.agent_config_list[agent_index]

        return gr.HTML(
            format_cover_html(
                bot_name=agent_config_interactive['name'],
                bot_description=agent_config_interactive['description'],
                bot_avatar=agent_config_interactive['avatar'],
            ))

    def _create_agent_plugins_block(self, agent_index=0):
        from qwen_agent.gui.gradio_dep import gr

        agent_interactive = self.agent_list[agent_index]

        if agent_interactive.function_map:
            capabilities = [key for key in agent_interactive.function_map.keys()]
            return gr.CheckboxGroup(
                label='插件',
                value=capabilities,
                choices=capabilities,
                interactive=False,
            )

        else:
            return gr.CheckboxGroup(
                label='插件',
                value=[],
                choices=[],
                interactive=False,
            )
