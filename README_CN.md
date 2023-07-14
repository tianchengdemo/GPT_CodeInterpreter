# GPT_CodeInterpreter


## 计划添加的功能

- [ ] 添加IPython和Jupyter的功能,以便可以在robot_functions中创建交互式widgets
- [ ] 支持直接在robot_functions中编写和调试HTML代码
- [ ] 利用IPython/Jupyter的功能使代码编写和执行更加智能方便  
- [ ] 自动迭代HTML项目,完成整个项目的开发流程
- [ ] 支持更好的页面展示,而不仅仅是图片,比如可以直接在Jupyter中显示页面

## 先决条件

在开始前，请确保你已经满足以下要求：

- 你已经安装了最新版本的 Python（推荐使用 3.8+ 版本）。
- 你已经安装了 Chainlit。

## 安装 Chainlit

按照以下步骤来安装 Chainlit：

```bash
pip install chainlit
```

## 环境变量

在运行项目之前，你需要设置以下环境变量。你可以在你的 shell 中设置这些变量，或者将它们添加到项目根目录下的 `.env` 文件中。

将 `<your_value>` 替换为你实际的值。

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

如果你在 `.env` 文件中设置环境变量，你需要使用一个像 `python-dotenv` 这样的 Python 包在运行脚本时加载变量。

安装 `python-dotenv`，运行：

```bash
pip install python-dotenv
```

然后，在你的 `main.py` 脚本中，你需要在脚本开始时加载环境变量：

```python
from dotenv import load_dotenv
load_dotenv()
```

## 使用 GPT_CodeInterpreter

要使用 GPT_CodeInterpreter，按照以下步骤操作：

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

`robot_functions.py` 是一个包含一系列用于特定场景的实用函数的 Python 模块。这些函数以异步的方式编写，允许它们在你的应用程序中以非阻塞的方式使用。

## 如何添加你的函数

你可以在 `functions` 目录下的 `robot_functions.py` 文件中添加你自己的自定义函数。你添加的每个函数都应编写为异步函数，并包含详细的 docstring，描述函数的目的、参数和返回值。

以下是如何添加你自己的函数的示例：

```python
async def your_function_name(your_parameters):
    """
    这是函数描述，描述函数的作用。

    参数:
    your_parameters: 这是参数描述，描述参数的用途。
    
    返回:
    这是返回描述，描述函数的返回值。
    """
    # 你的函数实现在这里
```

你为函数提供的 docstrings 很重要，因为它们会被自动解析并传递给 GPT 模型。这有助于模型理解你的函数的目的和用法。

## 函数描述

以下是 `robot_functions.py` 文件中提供的函数的简要描述：

- `python(code: str)`：执行提供的 Python 代码。
- `need_file_upload()`：请求用户上传文件。
- `show_images(paths: str)`：显示给定文件路径的图片。
- `need_install_package(package_name: str)`：检查并安装指定的 Python 包。
- `csv_to_db(csv_path: str)`：将 CSV 文件保存到数据库。
- `query_data_by_sql(sql: str)`：使用 SQL 查询数据库中的数据。
- `sql_get_tables(sql: str)`：获取数据库中的所有表名。
- `generate_and_process_dalle_images(dalle_prompt: str)`：基于提供的提示生成 DALL-E 图片。
- `generate_and_process_stable_diffusion_images(stable_diffusion_prompt: str)`：基于提供的提示生成稳定扩散图片。
- `get_style_descriptions()`：返回各种风格预设的描述。
- `image_2_image_stable_diffusion_images(stable_diffusion_prompt: str, init_image_path: str)`：基于提供的提示和初始图像生成稳定扩散图像。
- `change_sd_model()`：切换稳定扩散 API 的模型。

请参考 `robot_functions.py` 文件中的 docstrings，以获取这些函数及其参数的更详细描述。



## 联系方式

如果你想联系我，可以通过 402087139@qq.com 向我发送邮件。