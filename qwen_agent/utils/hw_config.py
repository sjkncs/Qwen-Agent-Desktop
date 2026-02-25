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

"""
Hardware-adaptive configuration module.
Automatically detects GPU/CPU capabilities and recommends optimal inference settings.
Designed for RTX 5060 Ti (Blackwell GB206) + AMD Ryzen 7 9700X + 32GB DDR5.
"""

import os
import platform
from dataclasses import dataclass, field
from typing import Optional

from qwen_agent.log import logger


@dataclass
class HardwareProfile:
    """Detected hardware profile and recommended inference settings."""
    # GPU info
    gpu_name: str = 'cpu'
    gpu_vram_gb: float = 0.0
    gpu_compute_capability: str = ''
    gpu_count: int = 0
    cuda_available: bool = False
    # CPU info
    cpu_name: str = ''
    cpu_cores: int = 1
    cpu_threads: int = 1
    # RAM info
    system_ram_gb: float = 0.0
    # Recommended inference settings
    recommended_device: str = 'cpu'
    recommended_dtype: str = 'float32'
    recommended_max_new_tokens: int = 2048
    recommended_batch_size: int = 1
    # Flash Attention support (Ampere+)
    flash_attn_available: bool = False
    # Quantization recommendation
    recommended_quantization: Optional[str] = None   # None | 'int8' | 'int4'
    # torch.compile support
    compile_available: bool = False
    # Context window tuned
    recommended_max_input_tokens: int = 58000
    # Parallelism
    recommended_num_workers: int = 4


def detect_hardware() -> HardwareProfile:
    """Detect available hardware and return an optimised HardwareProfile."""
    profile = HardwareProfile()

    # ---------- CPU ----------
    profile.cpu_name = platform.processor()
    try:
        import psutil
        profile.system_ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 1)
        profile.cpu_cores = psutil.cpu_count(logical=False) or 1
        profile.cpu_threads = psutil.cpu_count(logical=True) or 1
    except ImportError:
        import os
        profile.cpu_threads = os.cpu_count() or 1
        profile.cpu_cores = max(1, profile.cpu_threads // 2)

    # ---------- GPU ----------
    try:
        import torch
        if torch.cuda.is_available():
            profile.cuda_available = True
            profile.gpu_count = torch.cuda.device_count()
            props = torch.cuda.get_device_properties(0)
            profile.gpu_name = props.name
            profile.gpu_vram_gb = round(props.total_memory / (1024 ** 3), 1)
            major, minor = props.major, props.minor
            profile.gpu_compute_capability = f'{major}.{minor}'

            # Ampere (8.x) and later support BF16 + Flash Attention 2
            if major >= 8:
                profile.flash_attn_available = _check_flash_attn()
                profile.recommended_dtype = 'bfloat16'
            elif major >= 7:
                # Turing / Volta – good FP16 support
                profile.recommended_dtype = 'float16'
            else:
                profile.recommended_dtype = 'float16'

            # Blackwell (RTX 50xx) = compute 10.x
            # Ampere (RTX 30xx)    = compute 8.x
            # Ada Lovelace (RTX 40xx) = compute 8.9
            is_blackwell = major >= 10
            is_ada_or_ampere = major == 8

            profile.recommended_device = 'cuda'

            # VRAM-based quantization recommendation
            if profile.gpu_vram_gb >= 24:
                profile.recommended_quantization = None           # Full precision fine-tune OK
                profile.recommended_max_new_tokens = 4096
                profile.recommended_max_input_tokens = 131072
            elif profile.gpu_vram_gb >= 16:
                profile.recommended_quantization = None           # BF16 7B/14B models fit
                profile.recommended_max_new_tokens = 4096
                profile.recommended_max_input_tokens = 65536
            elif profile.gpu_vram_gb >= 10:
                profile.recommended_quantization = 'int8'
                profile.recommended_max_new_tokens = 2048
                profile.recommended_max_input_tokens = 32768
            elif profile.gpu_vram_gb >= 6:
                profile.recommended_quantization = 'int4'
                profile.recommended_max_new_tokens = 2048
                profile.recommended_max_input_tokens = 16384
            else:
                profile.recommended_quantization = 'int4'
                profile.recommended_max_new_tokens = 1024
                profile.recommended_max_input_tokens = 8192

            # torch.compile available in PyTorch >= 2.0
            torch_version = tuple(int(x) for x in torch.__version__.split('.')[:2])
            profile.compile_available = torch_version >= (2, 0)

            # Worker threads – leave headroom for the GPU dispatch thread
            profile.recommended_num_workers = min(8, max(2, profile.cpu_threads // 2))

            logger.info(
                f'[HW] GPU: {profile.gpu_name} | VRAM: {profile.gpu_vram_gb}GB '
                f'| CC: {profile.gpu_compute_capability} | dtype: {profile.recommended_dtype} '
                f'| quant: {profile.recommended_quantization} '
                f'| flash_attn: {profile.flash_attn_available}'
            )
        else:
            _set_cpu_profile(profile)
    except ImportError:
        _set_cpu_profile(profile)

    return profile


def _set_cpu_profile(profile: HardwareProfile):
    """Fallback: CPU-only settings."""
    profile.recommended_device = 'cpu'
    profile.recommended_dtype = 'float32'
    profile.recommended_quantization = 'int4'    # Needed to fit large models on CPU
    profile.recommended_max_new_tokens = 512
    profile.recommended_max_input_tokens = 8192
    profile.recommended_num_workers = max(1, profile.cpu_threads // 4)
    logger.info('[HW] No CUDA GPU detected – falling back to CPU inference.')


def _check_flash_attn() -> bool:
    """Return True if flash_attn package is importable."""
    try:
        import flash_attn  # noqa: F401
        return True
    except ImportError:
        return False


def apply_torch_optimizations(profile: HardwareProfile):
    """Apply global PyTorch performance tweaks based on the detected profile."""
    if not profile.cuda_available:
        return
    try:
        import torch
        # Enable TF32 on Ampere+ for ~2-3x matmul throughput with minimal precision loss
        major = int(profile.gpu_compute_capability.split('.')[0])
        if major >= 8:
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            logger.info('[HW] TF32 matmul enabled (Ampere/Blackwell).')

        # Efficient SDPA for attention
        if hasattr(torch.backends.cuda, 'enable_flash_sdp'):
            torch.backends.cuda.enable_flash_sdp(profile.flash_attn_available)
        if hasattr(torch.backends.cuda, 'enable_mem_efficient_sdp'):
            torch.backends.cuda.enable_mem_efficient_sdp(True)
        if hasattr(torch.backends.cuda, 'enable_math_sdp'):
            torch.backends.cuda.enable_math_sdp(not profile.flash_attn_available)

        # Set inter-op threads for CPU side work
        torch.set_num_interop_threads(max(1, profile.cpu_threads // 4))
        torch.set_num_threads(max(1, profile.cpu_threads // 2))

        logger.info('[HW] PyTorch CUDA optimizations applied.')
    except Exception as e:
        logger.warning(f'[HW] Could not apply torch optimizations: {e}')


def get_optimized_load_kwargs(profile: HardwareProfile) -> dict:
    """
    Return kwargs suitable for `AutoModelForCausalLM.from_pretrained(..., **kwargs)`
    based on the hardware profile.
    """
    import torch

    kwargs = {}

    if profile.recommended_dtype == 'bfloat16':
        kwargs['torch_dtype'] = torch.bfloat16
    elif profile.recommended_dtype == 'float16':
        kwargs['torch_dtype'] = torch.float16
    else:
        kwargs['torch_dtype'] = torch.float32

    if profile.flash_attn_available:
        kwargs['attn_implementation'] = 'flash_attention_2'
    elif profile.cuda_available:
        kwargs['attn_implementation'] = 'sdpa'

    if profile.recommended_quantization == 'int8':
        try:
            from transformers import BitsAndBytesConfig
            kwargs['quantization_config'] = BitsAndBytesConfig(load_in_8bit=True)
            logger.info('[HW] INT8 quantization enabled via bitsandbytes.')
        except ImportError:
            logger.warning('[HW] bitsandbytes not found – INT8 quantization skipped.')

    elif profile.recommended_quantization == 'int4':
        try:
            from transformers import BitsAndBytesConfig
            kwargs['quantization_config'] = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.bfloat16 if profile.recommended_dtype == 'bfloat16' else torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type='nf4',
            )
            logger.info('[HW] NF4 double-quant enabled via bitsandbytes.')
        except ImportError:
            logger.warning('[HW] bitsandbytes not found – INT4 quantization skipped.')

    return kwargs


def get_generation_performance_kwargs(profile: HardwareProfile) -> dict:
    """Return extra kwargs to pass to model.generate() for speed."""
    kwargs = {}
    if profile.cuda_available:
        kwargs['use_cache'] = True
    return kwargs


# Module-level singleton – computed once on first import
_profile: Optional[HardwareProfile] = None


def get_hw_profile() -> HardwareProfile:
    """Return the (cached) hardware profile for this machine."""
    global _profile
    if _profile is None:
        _profile = detect_hardware()
        apply_torch_optimizations(_profile)
    return _profile
