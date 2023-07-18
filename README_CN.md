# Chainlit 项目

Chainlit 是一个由 AI 驱动，设计用于执行各种任务的项目。它基于插件架构，可以轻松扩展新功能。

## 项目特性

- **插件架构**：Chainlit 使用灵活且可扩展的插件架构。每个插件是一个包含 `functions.py` 和 `config.json` 文件的文件夹，定义了插件的功能和配置。

- **函数管理器**：函数管理器负责解析和调用每个插件的 `functions.py` 文件中定义的函数。

- **AI 驱动**：Chainlit 利用 AI 的力量理解和生成人类语言，使其能够处理各种任务。

## 当前插件

1. **通用插件**：此插件提供显示和上传图片的功能。

2. **Python 解释器插件**：此插件包括一个 Python 执行器，用于运行 Python 代码，非常适用于数据分析和表处理等任务。

3. **Vue 插件**：目前正在开发中，此插件设计用于与 Vue 项目一起工作，通过聊天界面自动化整个 Vue 项目的修改。

## 插件结构和使用

每个插件是 'plugins' 文件夹中的一个目录。目录名是插件的名称。每个插件目录至少包含两个文件：

1. `functions.py`：此文件包含插件提供的函数。每个函数应该是顶级函数（即，不是类的方法或内部函数），并应该以反映其功能的方式命名。函数可以是同步的或异步的。

2. `config.json`：此文件包含插件的配置。它是一个 JSON 文件，有一个必需的字段：`enabled`。如果 `enabled` 设置为 `true`，则将导入插件的函数并可供使用。如果 `enabled` 设置为 `false`，则不会导入插件的函数。

要使用插件，确保其在 `config.json` 文件中已启用。一旦启用，脚本运行时将自动导入插件提供的函数。AI 助手将能够在对话中调用这些函数。

## 创建插件

要创建插件，请按照以下步骤操作：

1. 在 'plugins' 文件夹中创建一个新目录。目录名将是插件的名称。

2. 在新目录中，创建一个名为 `functions.py` 的文件。在此文件中，定义你希望插件提供的函数。每个函数应该是顶级函数，并应该以反映其功能的方式命名。

3. 在同一目录中，创建一个名为 `config.json` 的文件。在此文件中，添加以下 JSON：

```json
{
    "enabled": true
}
```

这将默认启用插件。如果你想禁用插件，可以将 `true` 改为 `false`。

## 运行项目

要运行此项目，你需要按照以下步骤操作：

1. 首先，你需要在项目的根目录中创建一个 `.env` 文件。你可以通过复制 `.env.example` 文件来做到这一点。

2. 在 `.env` 文件中，你需要提供你的 OpenAI API 密钥。这应该是一个字符串，如 `OPENAI_API_KEY=your_api_key_here`。请将 `your_api_key_here` 替换为你实际的 OpenAI API 密钥。

3. 仍在 `.env` 文件中，你需要设置 OpenAI API 的基本 URL。这应该是一个字符串，如 `OPENAI_API_BASE=https://api.openai.com/v1`。

4. 保存 `.env` 文件后，你需要安装 Chainlit。你可以使用 pip 来做到这一点：`pip install chainlit`。

5. 一旦 Chainlit 安装完成，你可以使用以下命令运行项目：`chainlit run app.py -w`。

## 使用 Repl.it 部署

## 第一步：部署到 Repl.it

点击下面的按钮将此项目部署到 Repl.it：

[![在 Repl.it 上运行](https://replit.com/badge/github/boyueluzhipeng/GPT_CodeInterpreter)](https://replit.com/new/github/boyueluzhipeng/GPT_CodeInterpreter)

一旦你点击了按钮，项目仓库将被克隆到一个新的 Repl.it 工作区。

## 第二步：安装依赖项

项目克隆完成后，你需要安装必要的依赖项。要做到这一点，打开 Repl.it 中的 Shell 终端，并运行以下命令：

```bash
pip install -r requirements.txt
```

这将安装 `requirements.txt` 文件中列出的所有 Python 包。

## 第三步：配置环境变量

接下来，你需要设置环境变量。在 Shell 终端中，运行以下命令：

```bash
cp .env.example .env
```

此命令将 `.env.example` 文件的内容复制到一个名为 `.env` 的新文件中。

## 第四步：添加秘密

然后，转到 Repl.it 中的 'Secrets' 部分（通常在左侧边栏中），并选择 'Edit as JSON'。复制并粘贴以下 JSON 内容：

```json
{
  "OPENAI_API_KEY": "your_api_key",
  "OPENAI_API_BASE": "https://api.openai.com/v1"
}
```

将 `"your_api_key"` 替换为你实际的 OpenAI API 密钥。

## 第五步：运行项目

现在，你已经准备好运行项目了。点击 Repl.it 界面顶部的 'Run' 按钮。

## 第六步：访问网络界面

一旦项目运行起来，就可以在 'Webview' 部分找到你的公开 URL。你可以使用此 URL 在你的网络浏览器中访问 GPT Code Interpreter。

就这样！你已经成功地在 Repl.it 上部署了 GPT Code Interpreter。如果你遇到任何问题，请参考 Repl.it 的文档或在项目的 GitHub 页面上提出问题。

## 贡献

欢迎贡献！请阅读贡献指南，了解如何为此项目做出贡献。

## 许可

此项目根据 MIT 许可证的条款获得许可。