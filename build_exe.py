#!/usr/bin/env python3
"""
Build Qwen-Agent Desktop into a standalone EXE using PyInstaller.

Usage:
    python build_exe.py
    python build_exe.py --onefile    # single EXE (slower startup)
"""

import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT, 'qwen_agent', 'gui', 'desktop')
ICON_PATH = os.path.join(FRONTEND_DIR, 'Qwen3.png')


def build(onefile=False):
    # Collect frontend static files
    datas = [
        (os.path.join(FRONTEND_DIR, 'index.html'), 'qwen_agent/gui/desktop'),
        (os.path.join(FRONTEND_DIR, 'app.js'), 'qwen_agent/gui/desktop'),
        (os.path.join(FRONTEND_DIR, 'styles.css'), 'qwen_agent/gui/desktop'),
        (os.path.join(FRONTEND_DIR, 'Qwen3.png'), 'qwen_agent/gui/desktop'),
        (os.path.join(FRONTEND_DIR, 'api_bridge.py'), 'qwen_agent/gui/desktop'),
    ]

    # Build --add-data args
    sep = ';' if sys.platform == 'win32' else ':'
    add_data_args = []
    for src, dst in datas:
        if os.path.exists(src):
            add_data_args.extend(['--add-data', f'{src}{sep}{dst}'])

    hidden_imports = [
        'aiohttp',
        'aiohttp.web',
        'openai',
        'qwen_agent.gui.desktop.api_bridge',
    ]

    # Optional imports (don't fail if missing)
    optional = ['fitz', 'docx', 'pptx', 'PIL', 'psutil']
    for mod in optional:
        try:
            __import__(mod)
            hidden_imports.append(mod)
        except ImportError:
            print(f'  [skip] Optional module {mod} not installed')

    hidden_args = []
    for h in hidden_imports:
        hidden_args.extend(['--hidden-import', h])

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name', 'QwenAgent',
        '--noconfirm',
        '--clean',
        '--console',  # show console for debugging; change to --windowed for release
    ]

    if onefile:
        cmd.append('--onefile')
    else:
        cmd.append('--onedir')

    # Icon (convert PNG to ICO if possible, otherwise skip)
    ico_path = os.path.join(ROOT, 'QwenAgent.ico')
    if os.path.exists(ico_path):
        cmd.extend(['--icon', ico_path])
    elif os.path.exists(ICON_PATH):
        try:
            from PIL import Image
            img = Image.open(ICON_PATH)
            img.save(ico_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
            cmd.extend(['--icon', ico_path])
            print(f'  [icon] Converted {ICON_PATH} -> {ico_path}')
        except Exception as e:
            print(f'  [icon] Could not convert PNG to ICO: {e}')

    cmd.extend(add_data_args)
    cmd.extend(hidden_args)
    cmd.append(os.path.join(ROOT, 'desktop_app.py'))

    print('=' * 60)
    print('  Building Qwen-Agent Desktop EXE')
    print('=' * 60)
    print(f'  Mode: {"onefile" if onefile else "onedir"}')
    print(f'  Frontend: {FRONTEND_DIR}')
    print(f'  Hidden imports: {len(hidden_imports)}')
    print('=' * 60)
    print()
    print('  Command:')
    print('  ' + ' '.join(cmd))
    print()

    result = subprocess.run(cmd, cwd=ROOT)

    if result.returncode == 0:
        if onefile:
            exe = os.path.join(ROOT, 'dist', 'QwenAgent.exe')
        else:
            exe = os.path.join(ROOT, 'dist', 'QwenAgent', 'QwenAgent.exe')
        print()
        print('=' * 60)
        print('  ✅ Build successful!')
        print(f'  EXE: {exe}')
        print()
        print('  To run:')
        if onefile:
            print(f'    set QWEN_API_KEY=sk-your-key')
            print(f'    {exe}')
        else:
            print(f'    set QWEN_API_KEY=sk-your-key')
            print(f'    cd dist\\QwenAgent')
            print(f'    QwenAgent.exe')
        print('=' * 60)
    else:
        print()
        print('  ❌ Build failed! Check errors above.')
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build Qwen-Agent Desktop EXE')
    parser.add_argument('--onefile', action='store_true', help='Single EXE mode (slower startup)')
    args = parser.parse_args()
    build(onefile=args.onefile)
