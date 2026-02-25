<!---
Copyright 2023 The Qwen team, Alibaba Group. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

<p align="center">
    <img src="https://qianwen-res.oss-accelerate-overseas.aliyuncs.com/logo_qwen_agent.png" width="400"/>
</p>

<h1 align="center">Qwen-Agent Desktop</h1>

<p align="center">
  <b>基于 <a href="https://github.com/QwenLM/Qwen-Agent">Qwen-Agent</a> 框架的原生桌面级 AI 助手</b><br>
  对话 · 发现 · 工具 · 文档解析 · 录音 · PPT · 音视频速读
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-Apache_2.0-green" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Platform">
</p>

<p align="center">
  💜 <a href="https://chat.qwen.ai/"><b>Qwen Chat</b></a>&nbsp;&nbsp;|&nbsp;&nbsp;🤗 <a href="https://huggingface.co/Qwen">Hugging Face</a>&nbsp;&nbsp;|&nbsp;&nbsp;🤖 <a href="https://modelscope.cn/organization/qwen">ModelScope</a>&nbsp;&nbsp;|&nbsp;&nbsp;📑 <a href="https://qwenlm.github.io/">Blog</a>&nbsp;&nbsp;|&nbsp;&nbsp;📖 <a href="https://qwenlm.github.io/Qwen-Agent/en/">Documentation</a>
</p>

---

> **致谢 · Acknowledgement**
>
> 本项目基于 [QwenLM/Qwen-Agent](https://github.com/QwenLM/Qwen-Agent)（通义千问 Agent 框架）进行二次开发。
> Qwen-Agent 由**阿里巴巴通义千问团队（The Qwen Team, Alibaba Group）**开源，采用 [Apache 2.0 许可证](LICENSE)。
> 我们对原团队在大模型 Agent 框架、工具调用、RAG、代码解释器、MCP 等方面的卓越贡献表示衷心感谢。
>
> This project is a derivative work based on [QwenLM/Qwen-Agent](https://github.com/QwenLM/Qwen-Agent),
> an open-source LLM agent framework by **The Qwen Team, Alibaba Group**, licensed under [Apache 2.0](LICENSE).
> We sincerely thank the original team for their outstanding contributions to LLM agent frameworks,
> tool calling, RAG, code interpreters, and MCP support.

---

## 📢 更新日志 / Changelog

### Desktop 版新增 (本仓库)

- **🖥 桌面级 SPA 前端** — 基于 aiohttp + 纯 HTML/CSS/JS 构建，无需 Node.js，支持 PyInstaller 打包为独立 EXE
- **💬 多模型流式对话** — 接入 OpenAI 兼容 API（Claude / GPT / Gemini / Grok 等），SSE 流式输出 + Markdown 渲染
- **🔍 发现页 + 20+ 工具卡片** — 绘图、实用、娱乐、学习、职场五大分类，搜索筛选，每个工具打开独立对话式子页面（Ephemeral 模式，不污染主对话）
- **📄 文档解析** — 上传 PDF / DOCX / PPTX / TXT / CSV，自动提取文本 + 文档问答
- **🎙 录音转写** — 浏览器内录音（暂停/继续），一键 AI 分析
- **� PPT 大纲生成** — 输入主题 → AI 生成大纲，5 种风格模板
- **🎬 音视频速读** — 上传音视频文件 → AI 生成摘要、文稿、时间线
- **🌙 深色模式 + 响应式** — 一键明/暗切换，全局响应式适配（移动端 ≤ 900px 侧边栏折叠）
- **🔒 安全** — API Key 通过环境变量 `QWEN_API_KEY` 配置，不再硬编码
- **⚡ 硬件自适应** — GPU / CPU / RAM 自动检测，BF16 + Flash Attention + TF32 优化（Blackwell 架构适配）

### 原始框架更新 (来自 QwenLM/Qwen-Agent)

- 🔥 Feb 16, 2026: 开源 Qwen3.5，参考 [Qwen3.5 Agent Demo](./examples/assistant_qwen3.5.py)
- Jan 27, 2026: 开源 Agent 评测基准 [DeepPlanning](https://qwenlm.github.io/Qwen-Agent/en/benchmarks/deepplanning/)，增加 [文档](https://qwenlm.github.io/Qwen-Agent/en/guide/)
- Sep 23, 2025: 新增 [Qwen3-VL Tool-call Demo](./examples/cookbook_think_with_images.ipynb)
- Jul 23, 2025: 新增 [Qwen3-Coder Tool-call Demo](./examples/assistant_qwen3_coder.py)；原生 API 工具调用接口支持
- May 1, 2025: 新增 [Qwen3 Tool-call Demo](./examples/assistant_qwen3.py)；新增 [MCP cookbooks](./examples/)
- Mar 18, 2025: 支持 `reasoning_content` 字段；调整默认 [Function Call 模版](./qwen_agent/llm/fncall_prompts/nous_fncall_prompt.py)
- Dec 3, 2024: GUI 升级为 Gradio 5（Python ≥ 3.10）

---

## ✨ 功能总览

### Desktop 桌面版功能

| 模块 | 说明 |
| ---- | ---- |
| 💬 **智能对话** | 多模型切换，SSE 流式输出，Markdown 渲染，对话管理（新建/切换/删除/重命名） |
| 🔍 **发现页** | 20+ 内置工具卡片（绘图/实用/娱乐/学习/职场），分类筛选 + 搜索 |
| 🛠 **工具子页** | 每个工具打开独立对话页面，对话式交互，Ephemeral 模式不污染主对话记录 |
| 📄 **文档解析** | 上传 PDF / DOCX / PPTX / TXT / CSV，自动提取文本 + 文档问答 |
| 🎙 **录音转写** | 浏览器内录音（暂停/继续），一键 AI 分析 |
| 📊 **PPT 生成** | 输入主题 → AI 生成大纲，5 种风格模板可选 |
| 🎬 **音视频速读** | 上传音视频 → AI 生成摘要、文稿、时间线 |
| 🌙 **深色模式** | 一键切换明/暗主题，全局响应式适配 |
| ⌨️ **快捷键** | `Ctrl+N` 新对话 · `Ctrl+B` 侧边栏 · `Ctrl+D` 主题切换 · `Esc` 取消流式 |

### 原始框架功能 (Qwen-Agent)

本项目完整保留了 Qwen-Agent 原始框架的所有功能：

- **Agent 开发框架** — 基于通义千问模型的指令遵循、工具使用、规划、记忆能力
- **Function Calling** — 支持并行工具调用、多步多轮工具调用
- **RAG** — 快速 RAG 解决方案 + 高精度长文档问答 Agent
- **代码解释器** — 基于 Docker 容器的安全沙箱代码执行
- **MCP 支持** — Model Context Protocol 工具集成
- **BrowserQwen** — 基于 Qwen-Agent 的浏览器助手（详见 [文档](./docs/browser_qwen_cn.md)）
- **Gradio GUI** — 基于 Gradio 5 的 Web UI 快速部署

---

## 🚀 快速开始

### 方式一：直接运行 Desktop 版（开发模式）

```bash
# 1. 克隆仓库
git clone https://github.com/sjkncs/Qwen-Agent-Desktop.git
cd Qwen-Agent-Desktop

# 2. 安装依赖
pip install -r requirements-desktop.txt

# 3. 设置环境变量
#    Windows PowerShell:
$env:QWEN_API_KEY="sk-your-api-key-here"
#    Linux / macOS:
export QWEN_API_KEY="sk-your-api-key-here"

# 4. 启动
python desktop_app.py
```

浏览器会自动打开 `http://localhost:9720`。

### 方式二：打包为 EXE 桌面版

```bash
pip install pyinstaller
python build_exe.py

# 运行
set QWEN_API_KEY=sk-your-key
dist\QwenAgent\QwenAgent.exe
```

### 方式三：使用原始 Qwen-Agent 框架

```bash
# 安装原始框架（完整依赖）
pip install -e ./"[gui,rag,code_interpreter,mcp]"

# 或从 PyPI 安装稳定版
pip install -U "qwen-agent[rag,code_interpreter,gui,mcp]"
```

详细用法请参阅 [原始框架文档](./docs/README_CN.md) 和 [官方文档](https://qwenlm.github.io/Qwen-Agent/en/guide/)。

---

## ⚙️ Desktop 版配置

| 环境变量 | 说明 | 默认值 |
| -------- | ---- | ------ |
| `QWEN_API_KEY` | OpenAI 兼容 API Key | *(必填)* |
| `QWEN_API_BASE` | API 基础 URL | `https://hiapi.online/v1` |
| `QWEN_MODEL` | 默认模型 ID | `claude-sonnet-4-5` |

也可通过命令行参数覆盖：

```bash
python desktop_app.py --api-key sk-xxx --api-base https://api.openai.com/v1 --model gpt-4o --port 8080
```

可复制 `.env.example` 为 `.env` 并填写配置，避免每次手动设置环境变量。

---

## 📁 项目结构

```text
Qwen-Agent-Desktop/
├── desktop_app.py                  # Desktop 版主入口（aiohttp 服务器 + SSE 流式 API）
├── build_exe.py                    # PyInstaller 打包脚本
├── requirements-desktop.txt        # Desktop 版依赖
├── .env.example                    # 环境变量模板
│
├── qwen_agent/                     # Qwen-Agent 原始框架（完整保留）
│   ├── agents/                     #   Agent 实现（Assistant, ReActChat, GroupChat 等）
│   ├── llm/                        #   LLM 接入（DashScope, OpenAI, vLLM, Ollama 等）
│   ├── tools/                      #   工具集（RAG, 代码解释器, 搜索, MCP 等）
│   ├── memory/                     #   记忆模块
│   ├── utils/                      #   工具函数 + hw_config 硬件检测
│   └── gui/
│       ├── desktop/                #   ★ Desktop 版前端 SPA
│       │   ├── index.html          #     主页面
│       │   ├── app.js              #     核心逻辑（路由/对话/工具/i18n）
│       │   ├── styles.css          #     全局样式（深色模式/响应式）
│       │   ├── api_bridge.py       #     Python API 桥接层
│       │   └── Qwen3.png           #     Logo
│       ├── assets/                 #   Gradio GUI 样式
│       ├── gradio_utils.py         #   Gradio 工具函数
│       └── web_ui.py               #   Gradio Web UI
│
├── docs/                           # 项目文档
│   ├── README_EN.md                #   原始英文文档
│   ├── README_CN.md                #   原始中文文档
│   ├── browser_qwen.md             #   BrowserQwen 英文文档
│   └── browser_qwen_cn.md          #   BrowserQwen 中文文档
│
├── examples/                       # 示例代码（原始框架）
├── benchmark/                      # 评测基准
├── setup.py                        # 原始框架安装脚本
└── LICENSE                         # Apache 2.0 许可证
```

---

## 🔧 原始框架快速开发

框架提供了 LLM（`BaseChatModel`，含 [Function Calling](./examples/function_calling.py)）、Tool（`BaseTool`）等原子组件，以及 Agent（`Agent`）等高级抽象。

```python
from qwen_agent.agents import Assistant
from qwen_agent.tools.base import BaseTool, register_tool

# 自定义工具
@register_tool('my_tool')
class MyTool(BaseTool):
    description = '工具描述'
    parameters = [{'name': 'param', 'type': 'string', 'description': '参数', 'required': True}]
    def call(self, params, **kwargs):
        return '结果'

# 创建 Agent
llm_cfg = {'model': 'qwen-max-latest', 'model_type': 'qwen_dashscope'}
bot = Assistant(llm=llm_cfg, function_list=['my_tool', 'code_interpreter'])

# 对话
messages = [{'role': 'user', 'content': '你好'}]
for response in bot.run(messages=messages):
    print(response)
```

更多示例请参阅 [examples/](./examples) 目录和 [原始文档](./docs/README_CN.md)。

---

## ❓ FAQ

**Q: 代码解释器如何使用？**
A: 基于本地 Docker 容器的沙箱环境。使用前请确保已安装并启动 Docker。详见 [Docker 官方文档](https://docs.docker.com/desktop/)。

**Q: 如何使用 MCP？**
A: 在 [MCP Server](https://github.com/modelcontextprotocol/servers) 选择工具并配置，参考 [MCP 使用例子](./examples/assistant_mcp_sqlite_bot.py)。

**Q: 支持函数调用（工具调用）吗？**
A: 支持，包括并行工具调用。参考 [function_calling.py](./examples/function_calling.py)。

**Q: 如何基于超长文档问答？**
A: 提供了 [快速 RAG 方案](./examples/assistant_rag.py) 和 [高精度 Agent](./examples/parallel_doc_qa.py)，在百万字级上下文中表现优异。

---

## 📜 License

[Apache License 2.0](LICENSE)

Copyright 2023 The Qwen team, Alibaba Group. All rights reserved.

本项目为基于 [QwenLM/Qwen-Agent](https://github.com/QwenLM/Qwen-Agent) 的衍生作品，遵循 Apache 2.0 许可证。
Desktop 版扩展部分同样采用 Apache 2.0 许可证发布。

---

## ⭐ 相关链接

- **原始仓库**: [QwenLM/Qwen-Agent](https://github.com/QwenLM/Qwen-Agent)
- **通义千问**: [Qwen Chat](https://chat.qwen.ai/)
- **模型下载**: [Hugging Face](https://huggingface.co/Qwen) · [ModelScope](https://modelscope.cn/organization/qwen)
- **官方文档**: [qwenlm.github.io/Qwen-Agent](https://qwenlm.github.io/Qwen-Agent/en/)
- **评测基准**: [DeepPlanning](https://qwenlm.github.io/Qwen-Agent/en/benchmarks/deepplanning/)
