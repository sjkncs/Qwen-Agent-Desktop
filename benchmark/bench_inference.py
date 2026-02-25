"""
bench_inference.py – Measure raw tokens/s throughput for the Transformers LLM backend.

Usage:
    python benchmark/bench_inference.py --model Qwen/Qwen2.5-7B-Instruct
    python benchmark/bench_inference.py --model /path/to/local --warmup --torch_compile
    python benchmark/bench_inference.py --help
"""

import argparse
import time
import statistics
import sys
import os

# Make sure the project root is on the path when run directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _parse_args():
    p = argparse.ArgumentParser(description='Qwen-Agent inference benchmark (tokens/s)')
    p.add_argument('--model', required=True, help='Model id or local path')
    p.add_argument('--prompt', default='请介绍一下量子计算的基本原理，并举例说明其应用场景。', help='Benchmark prompt')
    p.add_argument('--max_new_tokens', type=int, default=256, help='Tokens to generate per run')
    p.add_argument('--runs', type=int, default=5, help='Number of timed runs')
    p.add_argument('--warmup_runs', type=int, default=2, help='Untimed warmup runs')
    p.add_argument('--warmup', action='store_true', help='Enable model KV-cache warmup pass')
    p.add_argument('--torch_compile', action='store_true', help='Enable torch.compile (reduce-overhead)')
    p.add_argument('--static_cache', action='store_true', help='Enable StaticCache / CUDA Graph')
    p.add_argument('--device', default=None, help='Force device (cuda/cpu). Auto-detected if omitted.')
    p.add_argument('--dtype', default=None, help='Force dtype (bfloat16/float16/float32).')
    p.add_argument('--stream', action='store_true', help='Benchmark streaming mode')
    return p.parse_args()


def _build_llm(args):
    from qwen_agent.llm import get_chat_model
    cfg = {
        'model': args.model,
        'model_type': 'transformers',
        'generate_cfg': {'max_new_tokens': args.max_new_tokens},
        'warmup': args.warmup,
        'torch_compile': args.torch_compile,
        'use_static_cache': args.static_cache,
    }
    if args.device:
        cfg['device'] = args.device
    if args.dtype:
        cfg['torch_dtype'] = args.dtype
    return get_chat_model(cfg)


def _count_tokens(text: str, tokenizer) -> int:
    try:
        return len(tokenizer.encode(text, add_special_tokens=False))
    except Exception:
        return len(text.split())


def _run_once(llm, messages: list, stream: bool) -> tuple[str, float]:
    t0 = time.perf_counter()
    full_text = ''
    if stream:
        for chunks in llm.chat(messages=messages, stream=True):
            if chunks:
                full_text = chunks[-1].content
    else:
        result = llm.chat(messages=messages, stream=False)
        full_text = result[-1].content if result else ''
    elapsed = time.perf_counter() - t0
    return full_text, elapsed


def main():
    args = _parse_args()

    print(f'\n{"="*60}')
    print(f'  Qwen-Agent Inference Benchmark')
    print(f'{"="*60}')
    print(f'  Model         : {args.model}')
    print(f'  Max new tokens: {args.max_new_tokens}')
    print(f'  Timed runs    : {args.runs}  (+ {args.warmup_runs} warmup)')
    print(f'  torch.compile : {args.torch_compile}')
    print(f'  static_cache  : {args.static_cache}')
    print(f'  stream mode   : {args.stream}')
    print(f'{"="*60}\n')

    # Print hardware info
    try:
        from qwen_agent.utils.hw_config import get_hw_profile
        hw = get_hw_profile()
        if hw.cuda_available:
            print(f'  GPU  : {hw.gpu_name}  ({hw.gpu_vram_gb:.1f} GB VRAM, CC {hw.gpu_compute_capability})')
            print(f'  Dtype: {hw.recommended_dtype}  |  Flash Attn: {hw.flash_attn_available}')
        else:
            print(f'  Device: CPU  |  {hw.cpu_cores}C/{hw.cpu_threads}T')
        print(f'  RAM  : {hw.system_ram_gb:.1f} GB')
        print()
    except Exception:
        pass

    print('Loading model...')
    llm = _build_llm(args)
    tokenizer = getattr(llm, 'tokenizer', None)
    print('Model loaded.\n')

    messages = [{'role': 'user', 'content': args.prompt}]

    # Untimed warmup
    if args.warmup_runs > 0:
        print(f'Running {args.warmup_runs} warmup pass(es)...')
        for _ in range(args.warmup_runs):
            _run_once(llm, messages, args.stream)
        print('Warmup done.\n')

    # Timed runs
    latencies = []
    token_counts = []
    print(f'Running {args.runs} timed pass(es)...')
    for i in range(args.runs):
        text, elapsed = _run_once(llm, messages, args.stream)
        n_tokens = _count_tokens(text, tokenizer) if tokenizer else args.max_new_tokens
        tps = n_tokens / elapsed if elapsed > 0 else 0
        latencies.append(elapsed)
        token_counts.append(n_tokens)
        print(f'  Run {i+1:2d}: {elapsed:.2f}s  |  {n_tokens} tokens  |  {tps:.1f} tok/s')

    # Summary
    avg_lat = statistics.mean(latencies)
    med_lat = statistics.median(latencies)
    min_lat = min(latencies)
    avg_tok = statistics.mean(token_counts)
    avg_tps = avg_tok / avg_lat if avg_lat > 0 else 0
    peak_tps = max(t / l for t, l in zip(token_counts, latencies))

    print(f'\n{"="*60}')
    print(f'  Results (avg of {args.runs} runs)')
    print(f'{"="*60}')
    print(f'  Avg latency   : {avg_lat:.2f} s')
    print(f'  Median latency: {med_lat:.2f} s')
    print(f'  Best latency  : {min_lat:.2f} s')
    print(f'  Avg tokens    : {avg_tok:.0f}')
    print(f'  Avg throughput: {avg_tps:.1f} tok/s')
    print(f'  Peak throughput: {peak_tps:.1f} tok/s')
    print(f'{"="*60}\n')

    # VRAM after inference
    try:
        import torch
        if torch.cuda.is_available():
            alloc = torch.cuda.memory_allocated(0) / (1024**3)
            reserved = torch.cuda.memory_reserved(0) / (1024**3)
            print(f'  VRAM allocated : {alloc:.2f} GB')
            print(f'  VRAM reserved  : {reserved:.2f} GB')
            print()
    except Exception:
        pass


if __name__ == '__main__':
    main()
