"""
run_optimized.py – RTX 5060 Ti (Blackwell) optimised launcher for Qwen-Agent.

Sets all environment variables and pre-configures PyTorch before starting
the web UI or the API server, maximising throughput on the RTX 5060 Ti.

Usage:
    # Interactive Web UI (local model)
    python run_optimized.py --model Qwen/Qwen2.5-7B-Instruct

    # Interactive Web UI (API backend)
    python run_optimized.py --model_server http://localhost:8000/v1 --api_key EMPTY

    # With torch.compile + warmup for best steady-state throughput
    python run_optimized.py --model Qwen/Qwen2.5-7B-Instruct --torch_compile --warmup

    # Run benchmark instead of UI
    python run_optimized.py --model Qwen/Qwen2.5-7B-Instruct --bench
"""

import argparse
import os
import sys


# ─── Environment optimisations (must be set before any torch/transformers import) ──

# CUDA allocator: expandable segments reduce fragmentation on 16 GB VRAM
os.environ.setdefault('PYTORCH_CUDA_ALLOC_CONF', 'expandable_segments:True,max_split_size_mb:512')

# Suppress slow tokenizer warning (we use fast tokenizers)
os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false')

# Use C++ backend for transformer attention kernels
os.environ.setdefault('TRANSFORMERS_NO_ADVISORY_WARNINGS', '1')

# Avoid unnecessary triton recompilation messages
os.environ.setdefault('TORCHINDUCTOR_DISABLE_PROGRESS', '1')

# Keep HuggingFace hub cache on the fastest drive (edit if needed)
os.environ.setdefault('HF_HOME', os.path.join(os.path.expanduser('~'), '.cache', 'huggingface'))

# RTX 5060 Ti: enable cuDNN benchmark mode for fixed input sizes
os.environ.setdefault('CUDNN_BENCHMARK', '1')


def _apply_torch_globals():
    """Apply PyTorch globals after env vars are set."""
    try:
        import torch
        if torch.cuda.is_available():
            # Blackwell (CC 10.x) and Ampere (CC 8.x): enable TF32
            props = torch.cuda.get_device_properties(0)
            if props.major >= 8:
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.allow_tf32 = True

            # Memory-efficient attention via SDPA
            if hasattr(torch.backends.cuda, 'enable_mem_efficient_sdp'):
                torch.backends.cuda.enable_mem_efficient_sdp(True)

            torch.backends.cudnn.benchmark = True
            print(f'[run_optimized] GPU: {props.name}  |  VRAM: {props.total_memory / 1024**3:.1f} GB  |  CC {props.major}.{props.minor}')
            print(f'[run_optimized] TF32={torch.backends.cuda.matmul.allow_tf32}  cuDNN benchmark=True')
        else:
            print('[run_optimized] No CUDA GPU detected – running on CPU.')
    except ImportError:
        print('[run_optimized] torch not installed – skipping GPU setup.')


def _parse_args():
    p = argparse.ArgumentParser(
        description='RTX 5060 Ti optimised Qwen-Agent launcher',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Backend selection
    backend = p.add_mutually_exclusive_group()
    backend.add_argument('--model', default=None,
                         help='Local transformers model id or path (e.g. Qwen/Qwen2.5-7B-Instruct)')
    backend.add_argument('--model_server', default=None,
                         help='OpenAI-compatible API base URL (e.g. http://localhost:8000/v1)')

    p.add_argument('--api_key', default='EMPTY', help='API key for model_server mode')
    p.add_argument('--model_name', default=None,
                   help='Model name when using model_server (default: auto-detected)')

    # Inference optimisations
    p.add_argument('--torch_compile', action='store_true',
                   help='Enable torch.compile(reduce-overhead) – adds ~60s first-run JIT cost')
    p.add_argument('--warmup', action='store_true',
                   help='Run a KV-cache warmup pass before serving the UI')
    p.add_argument('--static_cache', action='store_true',
                   help='Enable StaticCache / CUDA Graph (text-only models, transformers>=4.45)')
    p.add_argument('--dtype', default=None,
                   help='Override dtype (bfloat16/float16/float32). Auto-detected if omitted.')
    p.add_argument('--device', default=None,
                   help='Override device (cuda/cpu). Auto-detected if omitted.')

    # Server options
    p.add_argument('--host', default='0.0.0.0', help='Web UI host address')
    p.add_argument('--port', type=int, default=7860, help='Web UI port')
    p.add_argument('--share', action='store_true', help='Create a public Gradio share link')
    p.add_argument('--concurrency', type=int, default=4,
                   help='Gradio concurrency limit (lower = less VRAM pressure)')

    # Utilities
    p.add_argument('--bench', action='store_true',
                   help='Run benchmark instead of starting the UI')
    p.add_argument('--bench_tokens', type=int, default=256, help='Max new tokens for benchmark')
    p.add_argument('--bench_runs', type=int, default=5, help='Number of timed benchmark runs')
    p.add_argument('--info', action='store_true',
                   help='Print hardware info and exit')

    return p.parse_args()


def _print_hw_info():
    try:
        from qwen_agent.utils.hw_config import get_hw_profile
        hw = get_hw_profile()
        print('\n─── Hardware Profile ──────────────────────────────')
        if hw.cuda_available:
            print(f'  GPU           : {hw.gpu_name}')
            print(f'  VRAM          : {hw.gpu_vram_gb:.1f} GB')
            print(f'  Compute cap.  : {hw.gpu_compute_capability}')
            print(f'  Recommended   : dtype={hw.recommended_dtype}  quant={hw.recommended_quantization}')
            print(f'  Flash Attn    : {hw.flash_attn_available}')
            print(f'  torch.compile : {hw.compile_available}')
            print(f'  Max input tok : {hw.recommended_max_input_tokens:,}')
            print(f'  Max new tokens: {hw.recommended_max_new_tokens}')
        else:
            print(f'  Device        : CPU  ({hw.cpu_cores}C / {hw.cpu_threads}T)')
        print(f'  System RAM    : {hw.system_ram_gb:.1f} GB')
        print('───────────────────────────────────────────────────\n')
    except Exception as e:
        print(f'[run_optimized] Could not read hardware profile: {e}')


def _build_llm_cfg(args) -> dict:
    if args.model_server:
        model_name = args.model_name or 'default'
        return {
            'model': model_name,
            'model_server': args.model_server,
            'api_key': args.api_key,
            'generate_cfg': {'max_new_tokens': 2048},
        }
    else:
        cfg = {
            'model': args.model,
            'model_type': 'transformers',
            'torch_compile': args.torch_compile,
            'warmup': args.warmup,
            'use_static_cache': args.static_cache,
            'generate_cfg': {'max_new_tokens': 2048},
        }
        if args.dtype:
            cfg['torch_dtype'] = args.dtype
        if args.device:
            cfg['device'] = args.device
        return cfg


def _run_bench(args):
    bench_script = os.path.join(os.path.dirname(__file__), 'benchmark', 'bench_inference.py')
    bench_args = [
        sys.executable, bench_script,
        '--model', args.model,
        '--max_new_tokens', str(args.bench_tokens),
        '--runs', str(args.bench_runs),
    ]
    if args.warmup:
        bench_args.append('--warmup')
    if args.torch_compile:
        bench_args.append('--torch_compile')
    if args.static_cache:
        bench_args.append('--static_cache')
    if args.dtype:
        bench_args += ['--dtype', args.dtype]
    if args.device:
        bench_args += ['--device', args.device]

    import subprocess
    result = subprocess.run(bench_args)
    sys.exit(result.returncode)


def _run_webui(args):
    from qwen_agent.agents import Assistant
    from qwen_agent.gui import WebUI

    llm_cfg = _build_llm_cfg(args)
    model_label = args.model or args.model_server or 'Qwen-Agent'

    agent = Assistant(
        llm=llm_cfg,
        name='Qwen Assistant',
        description=f'由 {model_label} 驱动，针对 RTX 5060 Ti 硬件加速优化',
    )

    chatbot_cfg = {
        'prompt.suggestions': [
            '请介绍量子计算的基本原理',
            '帮我写一个快速排序的 Python 实现',
            '分析这段代码有什么问题',
            '用中文总结：The Attention Is All You Need paper',
        ]
    }

    print(f'\n[run_optimized] Starting Qwen-Agent Web UI on http://{args.host}:{args.port}')
    print(f'[run_optimized] Model: {model_label}')
    print(f'[run_optimized] torch.compile={args.torch_compile}  warmup={args.warmup}  static_cache={args.static_cache}\n')

    WebUI(agent, chatbot_config=chatbot_cfg).run(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        concurrency_limit=args.concurrency,
    )


def main():
    args = _parse_args()

    if args.info:
        _print_hw_info()
        sys.exit(0)

    _apply_torch_globals()

    if args.bench:
        if not args.model:
            print('[run_optimized] --bench requires --model')
            sys.exit(1)
        _run_bench(args)
    else:
        if not args.model and not args.model_server:
            print('[run_optimized] Please provide --model or --model_server')
            sys.exit(1)
        _run_webui(args)


if __name__ == '__main__':
    main()
