"""
run_hiapi.py – 通过 hiapi.online 调用最新 AI 模型的 Qwen-Agent Web UI 启动脚本

支持模型（2026年1-2月新出）：
  - gemini-2.0-flash / gemini-2.0-pro / gemini-2.5-pro
  - claude-sonnet-4-6 / claude-opus-4 / claude-3-7-sonnet
  - gpt-4.5-preview / gpt-4o / o3-mini
  - deepseek-r2 / deepseek-v3

用法：
    python run_hiapi.py
    python run_hiapi.py --model claude-sonnet-4-6
    python run_hiapi.py --model gemini-2.0-flash --port 7861
"""

import argparse
import os
import sys

# ── API 配置 ────────────────────────────────────────────────────────────────
HIAPI_BASE_URL = 'https://hiapi.online/v1'
HIAPI_API_KEY  = os.environ.get('QWEN_API_KEY', '')

# ── 可选模型列表（2026年1-2月最新）────────────────────────────────────────
AVAILABLE_MODELS = {
    # Google Gemini
    'gemini-2.5-pro':          'Google Gemini 2.5 Pro (2026.02)',
    'gemini-2.0-flash':        'Google Gemini 2.0 Flash (2026.01)',
    'gemini-2.0-flash-thinking':'Google Gemini 2.0 Flash Thinking (2026.01)',
    'gemini-2.0-pro':          'Google Gemini 2.0 Pro (2026.01)',
    # Anthropic Claude
    'claude-sonnet-4-6':       'Anthropic Claude Sonnet 4.6 (2026.02)',
    'claude-opus-4':           'Anthropic Claude Opus 4 (2026.01)',
    'claude-3-7-sonnet-20250219': 'Anthropic Claude 3.7 Sonnet (2025.02)',
    # OpenAI
    'gpt-4.5-preview':         'OpenAI GPT-4.5 Preview (2026.02)',
    'gpt-4o':                  'OpenAI GPT-4o',
    'o3-mini':                 'OpenAI o3-mini (2026.01)',
    'o3':                      'OpenAI o3 (2026.01)',
    # DeepSeek
    'deepseek-r2':             'DeepSeek R2 (2026.01)',
    'deepseek-v3':             'DeepSeek V3',
    # Qwen
    'qwen-max':                'Alibaba Qwen Max',
    'qwen-plus':               'Alibaba Qwen Plus',
}

DEFAULT_MODEL = 'claude-sonnet-4-6'


def _parse_args():
    p = argparse.ArgumentParser(
        description='hiapi.online 多模型 Qwen-Agent Web UI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='可用模型:\n' + '\n'.join(f'  {k:<40} {v}' for k, v in AVAILABLE_MODELS.items()),
    )
    p.add_argument('--model', default=DEFAULT_MODEL,
                   help=f'模型名称 (默认: {DEFAULT_MODEL})')
    p.add_argument('--list_models', action='store_true',
                   help='列出所有可用模型后退出')
    p.add_argument('--host', default='0.0.0.0', help='Web UI 监听地址')
    p.add_argument('--port', type=int, default=7860, help='Web UI 端口')
    p.add_argument('--share', action='store_true', help='创建 Gradio 公开分享链接')
    p.add_argument('--concurrency', type=int, default=10, help='并发请求数限制')
    p.add_argument('--system', default=None,
                   help='自定义系统提示词（默认：通用助手）')
    return p.parse_args()


def _build_system_prompt(model_name: str, custom: str = None) -> str:
    if custom:
        return custom
    model_display = AVAILABLE_MODELS.get(model_name, model_name)
    return (
        f'你是由 {model_display} 驱动的智能助手，通过 hiapi.online 接口接入。\n'
        '你具备强大的推理、编程、分析和创作能力。\n'
        '请用中文回复，除非用户使用其他语言。'
    )


def main():
    args = _parse_args()

    if args.list_models:
        print('\n可用模型列表：\n')
        for k, v in AVAILABLE_MODELS.items():
            print(f'  {k:<42} {v}')
        print()
        sys.exit(0)

    model_name = args.model
    model_display = AVAILABLE_MODELS.get(model_name, model_name)

    print('\n' + '='*60)
    print(f'  Qwen-Agent  ×  hiapi.online')
    print('='*60)
    print(f'  模型    : {model_display}')
    print(f'  API     : {HIAPI_BASE_URL}')
    print(f'  地址    : http://{args.host}:{args.port}')
    print('='*60 + '\n')

    # 设置项目路径
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    from qwen_agent.agents import Assistant
    from qwen_agent.gui import WebUI

    llm_cfg = {
        'model': model_name,
        'model_server': HIAPI_BASE_URL,
        'api_key': HIAPI_API_KEY,
        'generate_cfg': {
            'max_input_tokens': 32000,
        },
    }

    system_prompt = _build_system_prompt(model_name, args.system)

    agent = Assistant(
        llm=llm_cfg,
        name=f'AI 助手 ({model_display})',
        description=f'由 **{model_display}** 驱动，通过 hiapi.online 接入',
        system_message=system_prompt,
    )

    chatbot_cfg = {
        'prompt.suggestions': [
            '请介绍一下你自己以及你的能力',
            '帮我写一个 Python 快速排序算法并解释原理',
            '量子计算和经典计算有什么本质区别？',
            '请帮我分析以下代码存在的问题',
            '用简洁的语言解释 Transformer 注意力机制',
        ]
    }

    WebUI(agent, chatbot_config=chatbot_cfg).run(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        concurrency_limit=args.concurrency,
    )


if __name__ == '__main__':
    main()
