# LangGraph 学习笔记

这个仓库记录我从基础状态图到工具调用智能体的 LangGraph 学习过程。每个示例都是一个独立的图，并在 [`langgraph.json`](langgraph.json) 中注册，方便用 `langgraph dev` 逐个观察和调试。

目前的重点是理解 **状态如何在节点之间传递、边如何决定下一步，以及模型提出工具调用后图如何真正执行工具**。这些文件是练习示例，不是完整的生产应用。

## 学习路线

| 图 ID | 文件 | 学习内容 |
| --- | --- | --- |
| `0_graph` | [`0_graph_state_str.py`](module1/0_graph_state_str.py) | 用字符串作为状态，认识 `StateGraph`、节点、`START` 和 `END`。 |
| `1_graph` | [`1_graph_state_dict.py`](module1/1_graph_state_dict.py) | 用 `TypedDict` 定义结构化状态，让节点返回状态更新。 |
| `2_graph` | [`2_graph_conditional_edge.py`](module1/2_graph_conditional_edge.py) | 用条件边根据状态选择 `node2` 或 `node3`。 |
| `3_graph` | [`3_graph_introduction_model.py`](module1/3_graph_introduction_model.py) | 在节点中调用聊天模型，并根据模型输出选择分支。 |
| `4_graph` | [`4_graph_messages_state.py`](module1/4_graph_messages_state.py) | 使用 `MessagesState` 保存和追加对话消息。 |
| `5_graph` | [`5_graph_model_tool.py`](module1/5_graph_model_tool.py) | 用 `@tool` 定义乘法工具，并通过 `bind_tools` 告诉模型可用的工具。此图尚未执行工具。 |
| `6_graph` | [`6_graph_tool_call.py`](module1/6_graph_tool_call.py) | 加入 `ToolNode` 和 `tools_condition`，按模型输出执行工具；执行后直接结束。 |
| `8_graph` | [`8_graph_agent.py`](module1/8_graph_agent.py) | 提供加、减、乘三个工具，并让工具节点返回模型节点，形成可反复调用工具的循环。 |

编号 `7` 目前没有对应示例。根目录的 [`main.py`](main.py) 是另一个工具调用实验，没有在 `langgraph.json` 中注册。

## 环境准备

- Python 3.12 或更高版本（项目的 [`.python-version`](.python-version) 指定 3.12）。
- [uv](https://docs.astral.sh/uv/) 用于安装依赖和运行命令。
- 运行 `3_graph` 及之后的模型示例时，需要一个可用的聊天模型 API。工具相关示例还要求所选模型支持工具调用。

在项目根目录执行：

```powershell
uv sync
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

`uv sync` 会按照 [`pyproject.toml`](pyproject.toml) 和 `uv.lock` 准备 `.venv`。使用 `uv run` 时，uv 也会自动检查并同步环境；添加依赖后通常不需要再手动执行一次 `uv lock` 和 `uv sync`。[uv 锁定与同步说明](https://docs.astral.sh/uv/concepts/projects/sync/)

### 配置模型

编辑本地 `.env`，重点设置以下三个变量：

```dotenv
LLM_API_KEY="你的 API Key"
LLM_MODEL_ID="你的模型名称"
LLM_BASE_URL="你的 OpenAI 兼容接口地址"
```

当前各模型示例读取的是 `LLM_API_KEY`、`LLM_MODEL_ID` 和 `LLM_BASE_URL`；仅填写 `.env.example` 中的 `OPENAI_API_KEY` 不会替这些示例完成配置。`langgraph.json` 也指定了 `.env` 作为开发服务的环境文件。

如果使用本机 Ollama 的 OpenAI 兼容接口，可参考：

```dotenv
LLM_API_KEY="ollama"
LLM_MODEL_ID="你已下载的模型名称"
LLM_BASE_URL="http://localhost:11434/v1"
```

先确保 Ollama 正在运行，并用 `ollama list` 核对本地模型名称。Ollama 本地接口要求客户端提供一个 API Key 值，但会忽略其内容；其 OpenAI 兼容接口只覆盖部分 OpenAI API 功能。运行工具示例前，还应确认具体模型支持工具调用。[Ollama OpenAI 兼容接口](https://docs.ollama.com/api/openai-compatibility) · [Ollama 工具调用](https://docs.ollama.com/capabilities/tool-calling)

`.env` 已加入 `.gitignore`，不要把真实密钥写进 `.env.example` 或提交到 GitHub。如果不使用 LangSmith 追踪，可在 `.env` 中将 `LANGSMITH_TRACING_V2` 改为 `false`；若使用 Studio，请按启动提示配置所需的 LangSmith 账号和密钥。

## 运行示例

### 先运行不依赖模型的图

例如，在 PowerShell 中运行 `0_graph`：

```powershell
uv run python -c "import runpy; graph = runpy.run_path('module1/0_graph_state_str.py')['graph']; print(graph.invoke('Hello'))"
```

这个示例会在输入字符串后追加欢迎语。其余示例文件主要导出名为 `graph` 的已编译图，直接运行 `.py` 文件通常不会打印结果。

### 在 LangGraph 开发服务中查看所有图

```powershell
uv run langgraph dev
```

启动后，按终端给出的地址打开 API 文档或 Studio，并选择 `langgraph.json` 注册的图。`langgraph dev` 是本地开发服务，支持修改代码后重新加载。[LangGraph 本地开发文档](https://docs.langchain.com/langsmith/local-dev-testing)

输入需与图的状态结构对应：

| 图 | 示例输入 |
| --- | --- |
| `0_graph` | `"Hello"` |
| `1_graph`、`2_graph` | `{"graph_str": "Hello"}` |
| `3_graph` | `{"graph_str": "Hello"}` |
| `4_graph`、`5_graph`、`6_graph`、`8_graph` | `{"messages": [{"role": "user", "content": "2 乘以 3 是多少？"}]}` |

Windows 下如果启动时遇到编码问题，可在当前 PowerShell 终端先执行 `$env:PYTHONUTF8 = "1"`。仓库的 [`.vscode/settings.json`](.vscode/settings.json) 已为 **新建的 VS Code 集成终端**设置此变量。

## 当前示例的边界

- `5_graph` 只让模型知道乘法工具，模型可能返回工具调用请求，但图中没有 `ToolNode` 来执行它。
- `6_graph` 能执行工具，但工具节点连接到 `END`，不会再把结果交给模型生成最终回答；`8_graph` 才展示工具执行后的模型循环。
- `3_graph` 直接用 `int()` 解析模型回复。若模型没有返回整数，运行会报错；这是一个适合继续练习输出校验的地方。
- `8_graph` 当前写成了 `load_dotenv`，缺少调用括号。通过 `langgraph dev` 时可以由 `langgraph.json` 加载 `.env`；如果单独运行该文件，可能需要先修正为 `load_dotenv()` 或提前设置环境变量。
- 当前示例没有在代码中显式配置检查点保存器；[`main.py`](main.py) 中的 `thread_id` 本身不等于已经实现跨次调用的对话记忆。

## 参考资料

- [LangGraph 文档](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph 本地开发与测试](https://docs.langchain.com/langsmith/local-dev-testing)
- [uv 项目与依赖管理](https://docs.astral.sh/uv/guides/projects/)
- [Ollama OpenAI 兼容接口](https://docs.ollama.com/api/openai-compatibility)
