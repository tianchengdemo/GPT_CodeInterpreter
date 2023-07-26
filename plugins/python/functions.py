import asyncio
import subprocess
import sys
import chainlit as cl
import os
from .executor import CodeExecutor

myexcutor = CodeExecutor()


# async def cmd_exec(command: str):
#     """
#     A shell. Use this to execute shell commands. Input should be a valid shell command.like ls -l,wget https://www.baidu.com...
#     Parameters: command: (str, required):The command to execute.
#     """
#     # 执行命令
#     proc = subprocess.Popen(command,
#                             stdout=subprocess.PIPE,
#                             stderr=subprocess.PIPE,
#                             shell=True)
#     out, err = proc.communicate()
#     if err:
#         return {"result": err.decode()}
#     return {"result": out.decode()} 


async def python_exec(code: str):
    """
    A Python shell. Use this to execute python commands in jupyter kernel. Input should be a valid python command.
    Parameters: code: (str, required):You can write python code here.
    """
    code_output = myexcutor.execute(code)
    print(f"REPL execution result: {code_output}")
    if code_output is None:
        return {'description': 'There is no output, Your code needs print something in the end.', 'code_output': code_output}
    if code_output.startswith("Error info:"):
        return {
            "error_info": code_output, 
            "description": """take it step by step. 
                Now you should analyze the cause of the error and provide feedback first
                Then, You can try to solve this problem yourself, unless you cannot solve it on your own, then please decide for yourself how to proceed.
                1. If the problem can be solved by fixing the code, please directly use the python_exec function to rerun the repaired code without returning any corresponding code.
                2. If there is a missing dependency, use dependency installation.
                3. If there is a file missing, consult on how to obtain the corresponding file instead of directly requesting to call the upload file function.""",
                "status": "error"
            }
    return {'code_output': code_output, 'status': 'success'}

async def need_install_package(package_name: str) -> dict:
    """
    If the user's question mentions installing packages, and the packages need to be installed, 
    you can call this function.
    Parameters: package_name: The name of the package.(required)
    """
    # check if package is already installed
    cmd_check = [sys.executable, '-m', 'pip', 'show', package_name]
    proc = subprocess.Popen(cmd_check,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, _ = proc.communicate()
    if out:
        return {'description': f"{package_name} is already installed"}

    # install package if it's not installed
    cmd_install = [sys.executable, '-m', 'pip', 'install', package_name]
    process = await asyncio.create_subprocess_exec(
        *cmd_install,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        await cl.Message(content=f"Failed to install {package_name}.").send()
        return {
            'description':
            f"Error installing {package_name}: {stderr.decode()}"
        }
    await cl.Message(content=f"Successfully installed {package_name}.").send()
    return {'description': f"{package_name} has been successfully installed"}
