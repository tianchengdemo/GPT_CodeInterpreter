import openai
import json
import ast
import os
import chainlit as cl
from functions.FunctionManager import FunctionManager
import inspect
import tiktoken
import importlib
import asyncio
from functions.MakeRequest import make_request, make_request_chatgpt_plugin
import globale_values as gv


openai.api_key = os.environ.get("OPENAI_API_KEY")
openai.api_base = os.environ.get("OPENAI_API_BASE")

plugin_dirs = [
    d for d in os.listdir('plugins')
    if os.path.isdir(os.path.join('plugins', d)) and d != '__pycache__'
]

functions = []
for dir in plugin_dirs:
    try:
        with open(f'plugins/{dir}/config.json', 'r') as f:
            config = json.load(f)
        enabled = config.get('enabled', True)
    except FileNotFoundError:
        enabled = True

    if not enabled:
        continue

    module = importlib.import_module(f'plugins.{dir}.functions')
    functions.extend([
        obj for name, obj in inspect.getmembers(module) if inspect.isfunction(obj)
    ])

function_manager = FunctionManager(functions=functions)
print("functions:", function_manager.generate_functions_array())

env_max_tokens = os.environ.get("MAX_TOKENS", None)
if env_max_tokens is not None:
    max_tokens = int(env_max_tokens)
else:
    max_tokens = 5000
is_stop = False


def __truncate_conversation(conversation):
    system_con = conversation[0]
    conversation = conversation[1:]
    while True:
        if (get_token_count(conversation) > max_tokens and len(conversation) > 1):
            conversation.pop(1)
        else:
            break
    conversation.insert(0, system_con)
    return conversation


def get_token_count(conversation):
    encoding = tiktoken.encoding_for_model(os.environ.get("OPENAI_MODEL") or "gpt-4")

    num_tokens = 0
    for message in conversation:
        num_tokens += 4
        for key, value in message.items():
            num_tokens += len(encoding.encode(str(value)))
            if key == "name":
                num_tokens += -1
    num_tokens += 2
    return num_tokens


MAX_ITER = 100


async def on_message(user_message: object):
    global is_stop
    is_stop = False
    print("==================================")
    print(user_message)
    print("==================================")
    user_message = str(user_message)
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": user_message})
    cur_iter = 0
    while cur_iter < MAX_ITER and not is_stop:

        openai_message = {"role": "", "content": ""}
        function_ui_message = None
        content_ui_message = cl.Message(content="")
        stream_resp = None
        send_message = __truncate_conversation(message_history)
        try:
            functions = function_manager.generate_functions_array()
            user_plugin_api_info = cl.user_session.get('user_plugin_api_info')
            if user_plugin_api_info is not None:
                for item in user_plugin_api_info:
                    for i in item['api_info']:
                        functions.append(i)
            print("functions:", functions)
            async for stream_resp in await openai.ChatCompletion.acreate(
                    model=os.environ.get("OPENAI_MODEL") or "gpt-4",
                    messages=send_message,
                    stream=True,
                    function_call="auto",
                    functions=functions,
                    temperature=0):  # type: ignore
                new_delta = stream_resp.choices[0]["delta"]
                if is_stop:
                    is_stop = True
                    cur_iter = MAX_ITER
                    break
                openai_message, content_ui_message, function_ui_message = await process_new_delta(
                    new_delta, openai_message, content_ui_message, function_ui_message)
        except Exception as e:
            print(e)
            cur_iter += 1
            await asyncio.sleep(1)
            continue

        if stream_resp is None:
            await asyncio.sleep(2)
            continue

        if function_ui_message is not None:
            await function_ui_message.send()

        if stream_resp.choices[0]["finish_reason"] == "stop":
            break
        elif stream_resp.choices[0]["finish_reason"] != "function_call":
            raise ValueError(stream_resp.choices[0]["finish_reason"])

        function_name = openai_message.get("function_call").get("name")
        print(openai_message.get("function_call"))
        function_response = ""
        try:
            arguments = json.loads(
                openai_message.get("function_call").get("arguments"))
        except:
            try:
              arguments = ast.literal_eval(
                  openai_message.get("function_call").get("arguments"))
            except:
              if function_name == 'python' or function_name == 'python_exec':
                if function_name == 'python':
                  function_name = 'python_exec'
                arguments = {"code": openai_message.get("function_call").get("arguments")}
                openai_message["function_call"]["arguments"] = json.dumps(arguments)
        try:
            function_response = await function_manager.call_function(
                function_name, arguments)
        except Exception as e:
            print(e)
            raise e 
        print("==================================")
        print(function_response)
        if type(function_response) != str:
            function_response = str(function_response)
        
        message_history.append(openai_message)
        
        if function_name == 'python_exec' and 'status' in function_response and 'error_info' in function_response and 'error' in function_response:
            # function_response 中取出 description 并从中 去掉这个key
            print("🚀" * 20)
            function_response = json.loads(function_response)
            description = function_response['description']
            del function_response['description']
            message_history.append({
                "role": "function",
                "name": function_name,
                "content": json.dumps(function_response),
            })
            language = os.environ.get("LANGUAGE") or "chinese"
            message_history.append({
                "role": "user",
                "content": str(description) + "\n\n" + "Please answer me in " + language
            })
            print("🚀" * 20)
        else:
            message_history.append({
                "role": "function",
                "name": function_name,
                "content": function_response,
            })
            
        print("==================================")
        print(message_history)
        print("==================================")

        await cl.Message(
            author=function_name,
            content=str(function_response),
            language="json",
            indent=1,
        ).send()
        cur_iter += 1


async def process_new_delta(new_delta, openai_message, content_ui_message,
                            function_ui_message):
    if "role" in new_delta:
        openai_message["role"] = new_delta["role"]
    if "content" in new_delta:
        new_content = new_delta.get("content") or ""
        openai_message["content"] += new_content
        await content_ui_message.stream_token(new_content)
    if "function_call" in new_delta:
        if "name" in new_delta["function_call"]:
            function_name = new_delta["function_call"]["name"]
            if function_name == "python":
                function_name = "python_exec"
            openai_message["function_call"] = {
                "name": function_name,
            }
            await content_ui_message.send()
            function_ui_message = cl.Message(
                author=function_name,
                content="",
                indent=1,
                language="json")
            await function_ui_message.stream_token(function_name)

        if "arguments" in new_delta["function_call"]:
            if "arguments" not in openai_message["function_call"]:
                openai_message["function_call"]["arguments"] = ""
            openai_message["function_call"]["arguments"] += new_delta[
                "function_call"]["arguments"]
            await function_ui_message.stream_token(
                new_delta["function_call"]["arguments"])
    return openai_message, content_ui_message, function_ui_message


async def analyze_error(error_info: str):
    """
    Analyze the cause of the error and provide feedback.
    Parameters:
        origin_code: The original code.(required)
        error_info: The error info.(required)
    """
    llm_chain = cl.user_session.get("llm_chain")
    res = await llm_chain.acall(error_info, callbacks=[cl.AsyncLangchainCallbackHandler()])
    return res


@cl.on_chat_start
async def start_chat():
    content = '''\
      1、you are a helper bot, you can generate python code to analyze the data,
      2、If the code needs to show images or files, you should save them to the ./tmp folder.
      3、[IMPORTANT] you should save the images or files to the ./tmp folder, and `print('path', './tmp/xxx.png')` at the end of the code.
      4、if you want to show images or files, you should respond like ![image](./tmp/xxx.png), download the file like [file](./tmp/xxx.png)
      5、[IMPORTANT] Do not use any graphical interface to display the code.
      example:
      ```json
      {
        "code":"import matplotlib.pyplot as plt\\nrandom_data = [1,2,3,4,5,6,7,8,9,10]\\nplt.hist(random_numbers)\\nplt.ylabel('Frequency')\\nplt.title('Random numbers')\\nplt.savefig('./tmp/xxx.png')\\nprint('path','./tmp/xxx.png')"
        "language":"python"
      }
      ```
      [IMPORTANT] Do not use plt.show() or cv2.imshow() or any graphical interface to display in the code.\
    '''
    language = os.environ.get("LANGUAGE") or "chinese"
    cl.user_session.set(
        "message_history",
        [{
            "role":
            "system",
            "content": content + "\n\n" + "Please answer me in " + language
        }],
    )
    await cl.Avatar(
        name="Chatbot",
        url="https://avatars.githubusercontent.com/u/128686189?s=400&u=a1d1553023f8ea0921fba0debbe92a8c5f840dd9&v=4",
    ).send()
    await cl.Message(
        author="Chatbot",
        content="""
## 📁 文件上传指南
你好！如果你需要上传文件，你可以使用 `/upload` 指令。这个指令会帮助你将文件上传到我们的系统。🚀
## 🐾 步骤
1. 在聊天框中输入 `/upload` 指令 🖥️
2. 按下回车键 ➡️
3. 在弹出的窗口中，选择你需要上传的文件 📂
4. 点击 "上传" 按钮，等待文件上传完成 ⏳
💡 提示：请确保你的文件不包含任何敏感信息，因为我们的系统会保存你上传的文件。
## 🎉 上传完成
一旦文件上传成功，你会在聊天窗口中看到一个确认消息，证明你的文件已经成功上传。🏁
如果你在上传过程中遇到任何问题，或者需要更多帮助，随时向我们提问。我们会尽快回答你的问题。📬
祝你一切顺利！🍀""",
    ).send()


@cl.on_message
async def run_conversation(user_message: object):
    if '/upload' == str(user_message):
        if not os.path.exists('./tmp'):
            os.mkdir('./tmp')
        files = await cl.AskFileMessage(
            content="Please upload a file.",
            max_size_mb=10,
            accept=[
                "text/plain",
                "image/png",
                "image/jpeg",
                "application/pdf",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # for .xlsx files
                "application/vnd.ms-excel",  # for .xls files
                "text/csv",  # for .csv files
                "application/json",  # for .json files
                "application/zip",  # for .zip files
                "application/x-tar",  # for .tar files
                "application/gzip",  # for .gz files
                "application/x-bzip2",  # for .bz2 files
                "application/x-7z-compressed",  # for .7z files
                "application/yaml",  # for .yaml files
                "application/x-yaml",  # for .yml files
                "text/markdown",  # for .md files
                "text/html",  # for .html files
                "text/css",  # for .css files
                "text/javascript",  # for .js files
                "text/x-python",  # for .py files
                "text/x-c",  # for .c files
                "text/x-c++",  # for .cpp files
                "text/x-java",  # for .java files
                "text/x-go",  # for .go files
                "text/x-php",  # for .php files
                "text/x-ruby",  # for .rb files
                "text/x-rust",  # for .rs files
                "text/x-sql",  # for .sql files
                "text/x-swift",  # for .swift files
                "text/x-typescript",  # for .ts files
                "text/x-kotlin",  # for .kt files
                "text/yaml",  # for .yaml files
                "text/x-yaml",  # for .yml files
                "text/xml",  # for .xml files
            ]).send()
        file = files[0]
        save_path = ""
        # 保存文件到paths目录下
        # 判断paths目录是否存在
        if save_path == "":
            save_path = file.name
        file_path = f"./tmp/{save_path}"
        # 保存文件
        content = file.content
        # 保存文件
        # content是bytes类型
        with open(file_path, "wb") as f:
            f.write(content)
        message_history = cl.user_session.get("message_history")
        message_history.append({
            "role": "assistant",
            "content": f"upload file ./tmp/{save_path} success"
        })
        await cl.Message(
            author="Chatbot",
            content=f"🚀 文件 `./tmp/{save_path}` 已成功上传 🎉",
        ).send()
        return
    
    await on_message(user_message)


@cl.on_stop
async def stop_chat():
    global is_stop
    print("stop chat")
    is_stop = True
