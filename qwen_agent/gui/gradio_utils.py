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

import base64


def covert_image_to_base64(image_path):
    ext = image_path.split('.')[-1]
    if ext not in ['gif', 'jpeg', 'png']:
        ext = 'jpeg'

    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read())
        base64_data = encoded_string.decode('utf-8')
        base64_url = f'data:image/{ext};base64,{base64_data}'
        return base64_url


def _get_hw_badge_html() -> str:
    """Return a small GPU/CPU status badge for the agent card."""
    try:
        from qwen_agent.utils.hw_config import get_hw_profile
        hw = get_hw_profile()
        if hw.cuda_available:
            label = hw.gpu_name.replace('NVIDIA ', '').replace('GeForce ', '')
            vram = f'{hw.gpu_vram_gb:.0f}GB'
            dtype = hw.recommended_dtype.upper()
            quant = f' · {hw.recommended_quantization.upper()}' if hw.recommended_quantization else ''
            text = f'{label} · {vram} · {dtype}{quant}'
        else:
            text = f'CPU · {hw.cpu_cores}C/{hw.cpu_threads}T'
    except Exception:
        text = 'Hardware info unavailable'

    return (
        f'<div class="hw_badge">'
        f'<span class="dot"></span>'
        f'{text}'
        f'</div>'
    )


def format_cover_html(bot_name, bot_description, bot_avatar):
    if bot_avatar:
        image_src = covert_image_to_base64(bot_avatar)
    else:
        image_src = '//img.alicdn.com/imgextra/i3/O1CN01YPqZFO1YNZerQfSBk_!!6000000003047-0-tps-225-225.jpg'

    hw_badge = _get_hw_badge_html()

    return f"""
<div class="bot_cover">
    <div class="bot_avatar">
        <img src="{image_src}" alt="{bot_name}" />
    </div>
    <div class="bot_name">{bot_name}</div>
    <div class="bot_desp">{bot_description}</div>
    {hw_badge}
    <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;justify-content:center;">
        <span style="display:inline-flex;align-items:center;gap:4px;padding:3px 10px;background:rgba(99,102,241,0.06);border:1px solid rgba(99,102,241,0.12);border-radius:14px;font-size:11px;color:#6366f1;">💬 对话</span>
        <span style="display:inline-flex;align-items:center;gap:4px;padding:3px 10px;background:rgba(16,185,129,0.06);border:1px solid rgba(16,185,129,0.12);border-radius:14px;font-size:11px;color:#10b981;">🔧 工具</span>
        <span style="display:inline-flex;align-items:center;gap:4px;padding:3px 10px;background:rgba(245,158,11,0.06);border:1px solid rgba(245,158,11,0.12);border-radius:14px;font-size:11px;color:#f59e0b;">📄 RAG</span>
    </div>
</div>
"""
