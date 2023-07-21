# GPT_CodeInterpreter 项目 🤖

GPT_CodeInterpreter 是一个由 AI 驱动的项目，旨在执行与代码解释相关的各种任务。它构建在一个插件架构上，可以轻松扩展新功能。

## 视频演示 🎥

为了更好地了解 GPT_CodeInterpreter 的功能，您可以观看以下演示视频：
https://github.com/boyueluzhipeng/GPT_CodeInterpreter/releases/download/v1.0.0/0718.mp4" controls title="https://szby.oss-cn-beijing.aliyuncs.com/07133.mp4
<video src="https://github.com/boyueluzhipeng/GPT_CodeInterpreter/releases/download/v1.0.0/07134.mp4" controls title="https://szby.oss-cn-beijing.aliyuncs.com/0718.mp4"></video>

## 项目特点

- **插件架构**：GPT_CodeInterpreter 使用灵活且可扩展的插件架构。每个插件是一个包含 `functions.py` 和 `config.json` 文件的文件夹，定义插件的功能和配置。

### 🌟 即将推出的功能：

- **Official Plugin Integration🔌**: 通过处理提供的标准 `openapi.yaml` 来自官方源，我们可以自动获取相应的请求 URL 和方法名称。这些将与本地功能组合，并像调用本地功能一样发送给 GPT。在用户调用时，我们将对相应的 API 进行分类和请求，以确保实时和精确的反馈。

- **Role Masking🎭**: 我们在本地插件中集成了许多基于角色的功能。例如，新增加的 `Vue` 插件可以轻松修改本地 Vue 项目。

- **Join the Movement🤝**: 我们正在积极邀请热情的个人与我们合作！让我们走向"metaGPT"的未来，并共同开发一系列迷人的角色插件。

### 🌈 未来计划：

- **多客户端交互🔗**: 在运行多个客户端时，我们希望这些客户端可以交换消息，便于在不同角色之间传输数据。

  **初步概念💡**:

  - **服务器端⚙️**: 由 GPT-4 的 "管理员" 预设角色操作，其主要职责包括根据用户的"角色掩码"和预设目标分配任务，然后评估任务完成率。
  
  - **客户端🖥️**: 用户可以自主注册服务器，然后能够接收派遣的任务并得到任务完成率的反馈。它可以自主执行某些任务，同时也支持通过网络聊天界面进行交互以完成相关任务。

让我们期待这些新功能带来的无限可能性！ 🚀🎉

- **功能管理器**: 功能管理器负责解析和调用每个插件的 `functions.py` 文件中定义的功能。

- **AI 驱动**: GPT_CodeInterpreter 利用 AI 的力量来理解和生成人类语言，从而处理与代码解释相关的各种任务。

## 当前插件

1. **通用插件**: 该插件提供显示和上传图像的功能.

2. **Python 解释器插件**: 该插件包含一个 Python 执行器，用于运行 Python 代码，非常适用于数据分析和表格处理等任务.

3. **Vue 插件**: 目前正在开发中，该插件旨在与 Vue 项目配合使用，通过聊天界面自动化整个 Vue 项目修改过程.

## 文档

要开始使用 GPT_CodeInterpreter，请参阅以下文档：

- 📚 [如何安装和使用 GPT_CodeInterpreter](docs/install.md): 了解如何在您的项目中安装和使用 GPT_CodeInterpreter.

- 🚀 [通过 Replit 发布 GPT_CodeInterpreter](docs/replit.md): 逐步指南，教您如何在 Replit 平台上发布 GPT_CodeInterpreter.

- 📝 [了解环境变量](docs/env.md) - 🔑 配置 GPT_CodeInterpreter 的重要环境变量。

## 贡献

欢迎贡献！请阅读贡献指南，了解如何为该项目做出贡献。

## 联系方式

如有任何问题或合作机会，请通过电子邮件 `402087139@qq.com` 联系我. 📧

## 许可证

该项目根据 MIT 许可证条款许可. 📜

此版本将视频演示放在了开头，并添加了可点击的视频链接，以便吸引观看者的注意力。同时，保留了之前的表情符号和其他内容，使得整个文档看起来更加生动和有趣。如果您还有其他需求或想要进一步修改，请随时告诉我！
