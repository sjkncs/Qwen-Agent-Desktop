<p align="center">
  <img src="qwen_agent/gui/desktop/Qwen3.png" width="80" alt="Qwen-Agent">
</p>

<h1 align="center">Qwen-Agent Desktop</h1>

<p align="center">
  <b>原生桌面级 AI 助手 — 对话 · 发现 · 工具 · 文档解析</b><br>
  基于 aiohttp + SPA 前端 + SSE 流式输出，支持 PyInstaller 打包为 EXE
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-Apache_2.0-green" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Platform">
</p>

---

## ✨ 功能特性

| 模块 | 说明 |
|------|------|
| 💬 **智能对话** | 多模型切换（Claude / GPT / Gemini / Grok），SSE 流式输出，Markdown 渲染 |
| 🔍 **发现页** | 20+ 内置工具卡片（绘图/实用/娱乐/学习/职场），分类筛选 + 搜索 |
| 🛠 **工具子页** | 每个工具打开独立对话页面，对话式交互，不污染主对话记录 |
| 📄 **文档解析** | 上传 PDF / DOCX / PPTX / TXT / CSV，自动提取文本 + 文档问答 |
| 🎙 **录音转写** | 浏览器内录音，支持暂停/继续，一键 AI 分析 |
| 📊 **PPT 生成** | 输入主题 → AI 生成大纲，5 种风格模板 |
| 🎬 **音视频速读** | 上传音视频 → AI 生成摘要、文稿、时间线 |
| 🌙 **深色模式** | 一键切换明/暗主题，全局响应式适配 |
| 🌐 **双语 i18n** | 中文 / English 界面切换 |

## 🚀 快速开始

### 方式一：直接运行（开发模式）

```bash
# 1. 安装依赖
pip install aiohttp openai

# 2. 设置环境变量
#    Windows PowerShell:
$env:QWEN_API_KEY="sk-your-api-key-here"
#    Linux/macOS:
export QWEN_API_KEY="sk-your-api-key-here"

# 3. 启动
python desktop_app.py
```

浏览器会自动打开 `http://localhost:9720`。

### 方式二：EXE 桌面版

```bash
# 打包
pip install pyinstaller
python build_exe.py

# 运行（dist/QwenAgent/ 目录下）
dist\QwenAgent\QwenAgent.exe
```

## ⚙️ 配置

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `QWEN_API_KEY` | OpenAI 兼容 API Key | *(必填)* |
| `QWEN_API_BASE` | API 基础 URL | `https://hiapi.online/v1` |
| `QWEN_MODEL` | 默认模型 ID | `claude-sonnet-4-5` |

也可通过命令行参数覆盖：

```bash
python desktop_app.py --api-key sk-xxx --api-base https://api.openai.com/v1 --model gpt-4o --port 8080
```

## 📁 项目结构

```
Qwen-Agent/
├── desktop_app.py              # 主入口（aiohttp 服务器）
├── build_exe.py                # PyInstaller 打包脚本
├── qwen_agent/gui/desktop/     # 前端 SPA
│   ├── index.html              # 主页面
│   ├── app.js                  # 核心逻辑（路由/对话/工具/i18n）
│   ├── styles.css              # 全局样式
│   ├── api_bridge.py           # Python API 桥接层
│   └── Qwen3.png               # Logo
├── docs/                       # 项目文档
│   ├── README_EN.md
│   ├── README_CN.md
│   ├── browser_qwen.md
│   └── browser_qwen_cn.md
├── .env.example                # 环境变量模板
└── requirements-desktop.txt    # 桌面版依赖
```

## 📜 License

[Apache 2.0](LICENSE)
