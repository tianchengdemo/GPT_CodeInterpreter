from ChatGPT.ChatGPT import Chatbot
from FunctionManager import FunctionManager
import json
from plugins.python.functions import python_exec, need_install_package
from fastapi import FastAPI, HTTPException
from fastapi.responses import  StreamingResponse
# from Dxr_mqtt.dxr_log import *

import os

app = FastAPI()

chatbot = None

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
print(sys_prompt)

@app.on_event("startup")
async def startup_event():
    global chatbot
    function_manager = FunctionManager(functions=[python_exec, need_install_package])
    chatbot = Chatbot(function_manager=function_manager, 
                      api_key="sk-YLhISXYYmthDgwR027B889343a3248Dd80B6Cc59Eb83946f", 
                      base_url="https://api.analogai.in/v1", 
                      system_prompt=sys_prompt,
                      engine="gpt-3.5-turbo-16k"
    )
    chatbot.add_to_conversation(role="assistant", message="![image](http://localhost:8000/tmp/1692077412.7676768.png)")


def my_print(text):
    function_name = ""
    function_args = ""
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
        
        
@app.post("/agent")
async def agent(request_data: dict):
    input_text = request_data.get('input_text')
    def chatbot_responses():
        for response in chatbot.ask_stream(input_text):
            my_print(response)
            yield f"data: {json.dumps(response)}\n\n".encode('utf-8')
    return StreamingResponse(chatbot_responses(), media_type="text/event-stream")

if __name__ == "__main__":
   import uvicorn
   uvicorn.run(app, host="0.0.0.0", port=8000)

