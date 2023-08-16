import json
import os
import uuid
import chainlit as cl
from functions.FunctionManager import FunctionManager
print(cl.__version__ ,type(cl.__version__))
from codebot_server.ChatGPT.ChatGPT import Chatbot
from codebot_server.FunctionManager import FunctionManager
import json
from codebot_server.plugins.python.functions import python_exec, need_install_package
from fastapi.responses import  StreamingResponse
if cl.__version__ == "0.6.2":
    from chainlit.input_widget import Select, Switch, Slider, TextInput

if cl.__version__ == "0.6.2":
    from chainlit.server import app
    from fastapi import Request
    from fastapi.responses import (
        FileResponse,
    )

    # fastapi 静态文件 ./tmp 
    from fastapi.staticfiles import StaticFiles

    @app.get("/tmp/{file_path:path}")
    async def read_file(file_path: str):
        return FileResponse(f"./tmp/{file_path}")
    
chatbot_dit = {}

function_manager = FunctionManager(functions=[python_exec, need_install_package])

base_host = "http://localhost:8000"

sys_prompt = '''1.You are now a code interpreter in the Jupyter Notebook environment. When you encounter code that needs to be processed, please use Python code to analyze and solve the corresponding problems. You can solve problems step by step and can also use variables generated from previous code at any time.
2.to show images or files, you should respond like ![image](./tmp/xxx.png), download the file like [file](./tmp/xxx.png)
example:
```json
{
    "code": "import matplotlib.pyplot as plt\\nimport numpy as np\\n\\n# Generate 10 random numbers\\nrandom_numbers = np.random.rand(10)\\n\\n# Draw a graph\\nplt.plot(random_numbers)\\nplt.title('Graph of 10 random numbers')\\nplt.xlabel('Index')\\nplt.ylabel('Random Number')\\nplt.grid(True)\\n\\n# Save the figure\\nplt.savefig('./tmp/random_numbers.png')\\n\\n"
}
```
function response is {"code_output": "show image: ./tmp/1690679381.220762.png", "status": "success"}
the base_host is BASE_HOST, so you need to respond like ![image](BASE_HOST/tmp/1690679381.220762.png)
3.After encountering an error, please try to utilize existing functions as much as possible to attempt problem-solving instead of providing direct feedback.
4.[IMPORTANT] LOOP UNTIL YOU SOLVE THE PROBLEM. DO NOT GIVE UP.Prohibited to repeatedly make the same mistake more than 3 times.
5.[IMPORTANT] In the process of problem-solving, you have an absolute dominant role. Please try not to consult user opinions and proceed directly according to your own ideas.
6.Try to avoid printing terminal data with more than 2000 characters. Before considering using operations like print, make sure to first check if the content to be printed is too large. If it is, please store it in a file for later use by subsequent programs.'''

sys_prompt = sys_prompt.replace("BASE_HOST", base_host)

def my_print(text):
    function_name = ""
    if 'choices' in text:
        choices = text['choices']
        if len(choices) > 0 and 'delta' in choices[0]:
            delta = choices[0]['delta']
            if 'content' in delta:
                if delta['content'] != None:
                    print(delta['content'], end="", flush=True)
            if "function_call" in delta:
                if "name" in delta["function_call"]:
                    function_name = delta["function_call"]["name"]
                    print(function_name + ": " + "function_args\n", end="", flush=True)
                if "arguments" in delta["function_call"]:
                    print(delta["function_call"]["arguments"], end="", flush=True)
            if "tool" in delta and 'output' in delta:
                print(delta['output'], end="", flush=True)
            if choices[0]['finish_reason'] != None:
                print()       
   
async def my_chainlit_pirnt(response):
    message_ui_arr = {}
    async for text in response:
        function_name = ""
        if 'choices' in text:
            choices = text['choices']
            if len(choices) > 0 and 'delta' in choices[0]:
                delta = choices[0]['delta']
                if 'content' in delta:
                    if message_ui_arr.get('content') == None:
                        message_ui_arr['content'] = cl.Message(content="")
                    if delta['content'] != None:
                        await message_ui_arr['content'].stream_token(delta['content'])
                if "function_call" in delta:
                    if "name" in delta["function_call"]:
                        function_name = delta["function_call"]["name"]
                        if message_ui_arr.get('function_name') == None:
                            message_ui_arr['function_name'] = cl.Message(content="", indent=1, author=function_name, language="python")
                    if "arguments" in delta["function_call"]:
                        # print(delta["function_call"]["arguments"], end="", flush=True)
                        await message_ui_arr['function_name'].stream_token(delta["function_call"]["arguments"])
                if "tool" in delta and 'output' in delta:
                    if message_ui_arr.get('output') == None:
                        message_ui_arr['output'] = cl.Message(content="", indent=1, author="output", language="json")
                    await message_ui_arr['output'].stream_token(delta['output'])
                if choices[0]['finish_reason'] != None:
                    for key in message_ui_arr:
                        if message_ui_arr[key] != None:
                            await message_ui_arr[key].send() 
                            message_ui_arr[key] = None   
    
        
@app.post("/agent")
async def agent_endpoint(request_data: dict):
    global chatbot_dit
    input_text = request_data.get('input_text')
    session_id = request_data.get('session_id', uuid.uuid4().hex)
    chatbot = create_chatbot(session_id)
    async def chatbot_responses():
        async for response in chatbot.ask_stream(input_text):
            yield f"data: {json.dumps(response)}\n\n".encode('utf-8')

    return StreamingResponse(chatbot_responses(), media_type="text/event-stream")


def create_chatbot(session_id):
    global chatbot_dit
    if session_id not in chatbot_dit:
        chatbot = Chatbot(function_manager=function_manager, 
                      api_key=cl.user_session.get('settings')['OPENAI_API_KEY'],
                      base_url=cl.user_session.get('settings')['OPENAI_API_BASE'],
                      system_prompt=cl.user_session.get('settings')['SYSTEM_PROMPT'],
                      engine=cl.user_session.get('settings')['OPENAI_MODEL'],
                      max_tokens=int(cl.user_session.get('settings')['MAX_TOKENS']),
                      session_id=session_id,
        )
        
        chatbot.add_to_conversation(role="assistant", message="![image](http://localhost:8000/tmp/1692077412.7676768.png)")
        chatbot_dit[session_id] = chatbot
    else:
        print("session_id already exists")
        chatbot = chatbot_dit[session_id]
        settings = cl.user_session.get('settings')
        chatbot.system_prompt = settings['SYSTEM_PROMPT']
        chatbot.engine = settings['OPENAI_MODEL']
        chatbot.max_tokens = int(settings['MAX_TOKENS'])
        chatbot.api_key = settings['OPENAI_API_KEY']
        chatbot.base_url = settings['OPENAI_API_BASE']
        chatbot.session_id = session_id
        chatbot_dit[session_id] = chatbot
    return chatbot_dit[session_id]

def create_chatbot_endpoint(settings):
    global chatbot_dit
    chatbot = None
    session_id = settings['SESSION_ID']
    if session_id not in chatbot_dit:
        chatbot = Chatbot(function_manager=function_manager, 
                      api_key=settings['OPENAI_API_KEY'],
                      base_url=settings['OPENAI_API_BASE'],
                      system_prompt=settings['SYSTEM_PROMPT'],
                      engine=settings['OPENAI_MODEL'],
                      max_tokens=int(settings['MAX_TOKENS']),
                      session_id=session_id,
        )
        
        chatbot.add_to_conversation(role="assistant", message="![image](http://localhost:8000/tmp/1692077412.7676768.png)")
        chatbot_dit[session_id] = chatbot
    else:
        chatbot = chatbot_dit[session_id]
    
    return chatbot


async def agent(input_text):
    session_id = cl.user_session.get('settings')['SESSION_ID']
    chatbot = create_chatbot(session_id)
    return chatbot.ask_stream(input_text)


valid_models = ["gpt-3.5-turbo", "gpt-4", "gpt-3.5-turbo-16k"]

@app.post("/v1/chat/completions")
async def create_conversation(request_data: dict):
    settings = {}
    session_id = request_data.get('session_id', uuid.uuid4().hex)
    messages = request_data.get('messages')
    content = messages[0].get('content')
    model = request_data.get('model', 'gpt-3.5-turbo')
    model = model.replace("-codeinterpreter", "")
    settings['OPENAI_MODEL'] = model
    # headers中获取Authorization bearer token
    settings['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')
    settings['OPENAI_API_BASE'] = os.environ.get('OPENAI_API_BASE')
    settings['SYSTEM_PROMPT'] = sys_prompt
    settings['MAX_TOKENS'] = int(os.environ.get('MAX_TOKENS'))
    settings['SESSION_ID'] = session_id
    chatbot = create_chatbot_endpoint(settings)
    if model not in valid_models:
        return {"error": "model not found"}
    chatbot.engine = model
    async def chatbot_responses():
        async for response in chatbot.ask_stream(content):
            yield f"data: {json.dumps(response)}\n\n".encode('utf-8')
    return StreamingResponse(chatbot_responses(), media_type="text/event-stream")


@cl.on_chat_start
async def on_chat_start():
    if cl.__version__ == "0.6.2":
        settings = await cl.ChatSettings(
            [
                Select(
                    id="OPENAI_MODEL",
                    label="OPENAI_MODEL",
                    values=["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4"],
                    initial_index=0,
                ),
                TextInput(
                    id="OPENAI_API_KEY",
                    label="OPENAI_API_KEY",
                    initial=os.environ.get("OPENAI_API_KEY"),
                ),
                TextInput(
                    id="OPENAI_API_BASE",
                    label="OPENAI_API_BASE",
                    initial=os.environ.get("OPENAI_API_BASE"),
                ),
                TextInput(
                    id="SYSTEM_PROMPT",
                    label="SYSTEM_PROMPT",
                    initial=sys_prompt,
                ),
                TextInput(
                    id="MAX_TOKENS",
                    label="MAX_TOKENS",
                    initial=os.environ.get("MAX_TOKENS"),
                ),
                TextInput(
                    id="SESSION_ID",
                    label="SESSION_ID",
                    initial=os.environ.get("SESSION_ID", uuid.uuid4().hex),
                ),
            ]
        ).send()
        cl.user_session.set("settings", settings)
    else:
        settings = {
            'OPENAI_MODEL': os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo'), 
            'OPENAI_API_KEY': os.environ.get('OPENAI_API_KEY'), 
            'SYSTEM_PROMPT': sys_prompt,
            'MAX_TOKENS': os.environ.get('MAX_TOKENS', 3000),
            'OPENAI_API_BASE': os.environ.get('OPENAI_API_BASE', 'https://api.openai.com'),
            'SESSION_ID': os.environ.get('SESSION_ID', uuid.uuid4().hex)
        }
        cl.user_session.set("settings", settings)

if cl.__version__ == "0.6.2":
    @cl.on_settings_update
    async def setup_agent(settings):
        global chatbot_dit
        print("on_settings_update", settings)
        cl.user_session.set("settings", settings)
        create_chatbot(settings['SESSION_ID'])


    
    
async def pre_user_message(user_message: object):
    
    if '/upload' == str(user_message):
        if not os.path.exists('./tmp'):
            os.mkdir('./tmp')
        files = await cl.AskFileMessage(
            content="Please upload a file.",
            max_size_mb=10,
            accept=[
                "*"
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
        chatbot = create_chatbot(cl.user_session.get('settings')['SESSION_ID'])
        chatbot.add_to_conversation(role="user", message=f"i have upload a file {file_path}")
        elements = [
            cl.Image(name="image", display="inline", path=file_path),
        ]
        await cl.Message(content="Look at this local image!", elements=elements).send()
        return False
    return True

@cl.on_message
async def on_message(user_message: object):
    if await pre_user_message(user_message):
        resp = await agent(str(user_message))
        await my_chainlit_pirnt(resp)
        