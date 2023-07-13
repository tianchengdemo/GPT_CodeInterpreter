import time
import openai
import json
import ast
import os
import chainlit as cl
from functions.FunctionManager import FunctionManager
from functions import robot_functions
import inspect
import asyncio
import threading
import os
import tiktoken
import global_value as gv

max_tokens = 5000


def __truncate_conversation(conversation) -> None:
    """
    Truncate the conversation
    """
    # 第一条取出来
    system_con = conversation[0]
    # 去掉第一条
    conversation = conversation[1:]
    while True:
        if (get_token_count(conversation) > max_tokens
                and len(conversation) > 1):
            # Don't remove the first message
            conversation.pop(1)
        else:
            break
    # 再把第一条加回来
    conversation.insert(0, system_con)
    return conversation


# https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
def get_token_count(conversation) -> int:
    """
    Get token count
    """
    encoding = tiktoken.encoding_for_model('gpt-4')

    num_tokens = 0
    for message in conversation:
        # every message follows <im_start>{role/name}\n{content}<im_end>\n
        num_tokens += 4
        for key, value in message.items():
            num_tokens += len(encoding.encode(str(value)))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens


functions = [
    obj for name, obj in inspect.getmembers(robot_functions)
    if inspect.isfunction(obj)
]
function_manager = FunctionManager(functions=functions)

print("functions:", function_manager.generate_functions_array())

openai.api_key = 'catto_key_P33rJ7zKlu79FXj8mdWxkiu9'
openai.api_base = 'https://api.catto.codes/v1'

MAX_ITER = 10


async def on_message(user_message: object):
    print("==================================")
    print(user_message)
    print("==================================")
    user_message = str(user_message)
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": user_message})

    cur_iter = 0

    while cur_iter < MAX_ITER:

        # OpenAI call
        openai_message = {"role": "", "content": ""}
        function_ui_message = None
        content_ui_message = cl.Message(content="")
        stream_resp = None
        send_message = __truncate_conversation(message_history)
        try:
            async for stream_resp in await openai.ChatCompletion.acreate(
                    model="gpt-4",
                    messages=send_message,
                    stream=True,
                    function_call="auto",
                    functions=function_manager.generate_functions_array(),
                    temperature=0):  # type: ignore
                new_delta = stream_resp.choices[0]["delta"]
                openai_message, content_ui_message, function_ui_message = await process_new_delta(
                    new_delta, openai_message, content_ui_message,
                    function_ui_message)
        except Exception as e:
            print(e)
            cur_iter += 1
            continue

        if stream_resp is None:
            break

        message_history.append(openai_message)
        if function_ui_message is not None:
            await function_ui_message.send()

        if stream_resp.choices[0]["finish_reason"] == "stop":
            break
        elif stream_resp.choices[0]["finish_reason"] != "function_call":
            raise ValueError(stream_resp.choices[0]["finish_reason"])
        # if code arrives here, it means there is a function call
        function_name = openai_message.get("function_call").get("name")
        print(openai_message.get("function_call"))
        try:
            arguments = json.loads(
                openai_message.get("function_call").get("arguments"))
        except:
            arguments = ast.literal_eval(
                openai_message.get("function_call").get("arguments"))

        function_response = await function_manager.call_function(
            function_name, arguments)
        # print(function_response)

        message_history.append({
            "role": "function",
            "name": function_name,
            "content": function_response,
        })

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
            openai_message["function_call"] = {
                "name": new_delta["function_call"]["name"]
            }
            await content_ui_message.send()
            function_ui_message = cl.Message(
                author=new_delta["function_call"]["name"],
                content="",
                indent=1,
                language="json")
            await function_ui_message.stream_token(
                new_delta["function_call"]["name"])

        if "arguments" in new_delta["function_call"]:
            if "arguments" not in openai_message["function_call"]:
                openai_message["function_call"]["arguments"] = ""
            openai_message["function_call"]["arguments"] += new_delta[
                "function_call"]["arguments"]
            await function_ui_message.stream_token(
                new_delta["function_call"]["arguments"])
    return openai_message, content_ui_message, function_ui_message


@cl.action_callback("action_button")
async def on_action(action):
    await cl.Message(content=f"选择了 {action.value}",
                     author="action_style").send()
    # Optionally remove the action button from the chatbot user interface
    gv.style_preset = action.value


@cl.action_callback("action_model")
async def on_action_model(action):
    await cl.Message(content=f"选择了 {action.value}",
                     author="action_model").send()
    # Optionally remove the action button from the chatbot user interface
    gv.model_id = action.value


@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{
            "role": "system",
            "content": "You are a helpful assistant.请尽量使用中文来回复"
        }],
    )


@cl.on_message
async def run_conversation(user_message: object):
    await on_message(user_message)
