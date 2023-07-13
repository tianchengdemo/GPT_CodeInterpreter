# GPT_CodeInterpreter

## 先决条件

在开始之前，请确保你已经满足以下要求：

- 你已经安装了最新版本的Python（推荐3.8+版本）。
- 你已经安装了Chainlit。

## 安装Chainlit

按照以下步骤安装Chainlit：

```bash
pip install chainlit
```

## 环境变量

在运行项目之前，你需要设置以下环境变量。你可以在你的shell中设置这些，或者将它们添加到项目根目录的`.env`文件中。

将`<your_value>`替换为你实际的值。

```bash
export OPENAI_API_KEY=<your_value>
export OPENAI_API_BASE=<your_value>
export SD_API_KEY=<your_value>
export MYSQL_USER=<your_value>
export MYSQL_PASSWORD=<your_value>
export MYSQL_HOST=<your_value>
export MYSQL_DATABASE=<your_value>
```

## 使用环境变量运行项目

如果你在`.env`文件中设置环境变量，你需要使用一个Python包，如`python-dotenv`，在运行你的脚本时加载变量。

要安装`python-dotenv`，运行：

```bash
pip install python-dotenv
```

然后，在你的`main.py`脚本中，你需要在脚本开始时加载环境变量：

```python
from dotenv import load_dotenv
load_dotenv()
```

## 使用GPT_CodeInterpreter

要使用GPT_CodeInterpreter，按照以下步骤操作：

1. 克隆仓库：

```bash
git clone https://github.com/boyueluzhipeng/GPT_CodeInterpreter.git
```

2. 导航到项目目录：

```bash
cd GPT_CodeInterpreter
```

3. 运行主脚本：

```bash
python main.py
```

## 联系

如果你想联系我，你可以通过402087139@qq.com找到我。