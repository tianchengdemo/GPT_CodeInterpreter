# robot_functions.py
import asyncio
import base64
import time
import aiohttp
import chainlit as cl
import subprocess
import sys
from sqlalchemy import Column, create_engine, MetaData, Table, inspect, String
import pandas as pd
import os
import datetime, json
import openai
import requests
from .executor import PythonExecutor
kernel_id = None

import global_value as gv

context = {}

sql_query_result = None


async def python_exec(code: str, language: str = "python"):
    """
    Exexute code. \nNote: This endpoint current supports a REPL-like environment for Python only.\n\nArgs:\n    request (CodeExecutionRequest): The request object containing the code to execute.\n\nReturns:\n    CodeExecutionResponse: The result of the code execution.
    Parameters: code:
    """
  
    myexcutor = PythonExecutor()
    code_output = myexcutor.execute(code)
    print(f"REPL execution result: {code_output}")
    response = {"result": code_output.strip()}
    return response
    


async def need_file_upload():
    """
    When the user's question mentions handling files, you need to upload files, you can call this function.
    Parameters: None
    """
    files = await cl.AskFileMessage(
        content="Please upload a text file to begin!",
        accept=[
            "text/plain",
            "image/png",
            "image/jpeg",
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # for .xlsx files
            "application/vnd.ms-excel",  # for .xls files
            "text/csv",  # for .csv files
            # More MIME types here as needed.
        ]).send()
    file = files[0]

    # 保存文件到/tmp目录
    file_path = "/tmp/" + file.name
    # 保存文件
    content = file.content
    file_name = file.name
    file_type = file.type
    # 保存文件
    # content是bytes类型
    with open(file_path, "wb") as f:
        f.write(content)
    return {
        'type': 'file',
        'path': file_path,
        'name': file_name,
        'file_type': file_type
    }


async def show_images(paths: str):
    """
    If your return contains images in png or jpg format, you can call this function to display the images.
    Parameters: paths: The paths of the images as a comma-separated string.(required)
    """
    path_list = paths.split(',')
    elements = [
        cl.Image(name=f"image{i}", display="inline", path=path.strip())
        for i, path in enumerate(path_list)
    ]

    await cl.Message(content="Look at these local images!",
                     elements=elements).send()  # type: ignore

    return {'description': '图片显示成功'}


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


async def csv_to_db(csv_path: str) -> dict:
    """
    If the user's question mentions the need to save the csv file to the database, you can call this func
    Parameters: 
    csv_path: The path of the csv file.(required)
    """
    # 从csv文件路径中获取文件名作为表名
    try:
        user = os.environ['MYSQL_USER']
        password = os.environ['MYSQL_PASSWORD']
        host = os.environ['MYSQL_HOST']
        database = os.environ['MYSQL_DATABASE']
        table_name = os.path.splitext(os.path.basename(csv_path))[0]
        # 创建数据库连接
        engine = create_engine(
            f'mysql+pymysql://{user}:{password}@{host}/{database}')
        # 读取csv文件
        df = pd.read_csv(csv_path)
        # 检查表是否存在
        insp = inspect(engine)
        if not insp.has_table(table_name):
            # 创建表结构
            metadata = MetaData()
            table = Table(
                table_name, metadata,
                *(Column(column_name, String(255))
                  for column_name in df.columns))
            # 创建表
            metadata.create_all(engine)
        # 将数据写入数据库
        df.to_sql(table_name, engine, if_exists='append', index=False)
        return {
            'description': f"Successfully saved csv to database.",
            'askuser': '是否需要我自己根据自己的见解帮您进行统计分析'
        }
    except Exception as e:
        return {'description': f"Error saving csv to database: {e}"}


async def query_data_by_sql(sql: str):
    """
    If the user's question mentions the need to select data the database, you can call this function.
    Parameters:
    sql: The sql statement.(required)
    """
    global sql_query_result
    try:
        user = os.environ['MYSQL_USER']
        password = os.environ['MYSQL_PASSWORD']
        host = os.environ['MYSQL_HOST']
        database = os.environ['MYSQL_DATABASE']
        # Create a connection to the database
        engine = create_engine(
            f'mysql+pymysql://{user}:{password}@{host}/{database}')
        # Execute the SQL statement
        df = pd.read_sql(sql, engine)
        # Convert the results to a list of dictionaries
        sql_query_result = df.to_dict('records')
        # Check if sql_query_result is empty
        if not sql_query_result:
            return {
                'description':
                "No data to save. The sql_query_result is empty."
            }

        # Generate a timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # Create a filename with the timestamp
        filename = f'results_{timestamp}.json'

        try:
            # Write the results to the file
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(sql_query_result, jsonfile)
            elements = [cl.Text(name=filename, path=filename, display="page")]
            await cl.Message(content=f"查看{filename}",
                             elements=elements).send()  # type: ignore
        except Exception as e:
            return {'description': f"Error writing to JSON file: {e}"}

        # Return the file path
        return {
            'type': 'file',
            'filename': filename,
            "description": "为了节省token,已经帮您存文件了不用"
        }
    except Exception as e:
        return {'description': f"Error querying database: {e}"}


async def sql_get_tables(sql: object = None):
    """
    If the user's question mentions the need to get all table names in the database, you can call this function.
    Parameters: 
    sql: The sql statement.(optional)
    """
    try:
        user = os.environ['MYSQL_USER']
        password = os.environ['MYSQL_PASSWORD']
        host = os.environ['MYSQL_HOST']
        database = os.environ['MYSQL_DATABASE']
        # Create a connection to the database
        engine = create_engine(
            f'mysql+pymysql://{user}:{password}@{host}/{database}')
        # If an SQL statement is provided, execute it and return the result
        if sql:
            result = engine.execute(text(sql))
            return {
                'type': 'content',
                'content': f"Result of the SQL statement: {result}",
                'status': 'true'
            }
        # If no SQL statement is provided, return all table names
        else:
            # Use the inspect module
            inspector = inspect(engine)
            # Get all table names
            table_names = inspector.get_table_names()
            return {
                'type': 'content',
                'content': f"All tables in the database: {table_names}",
                'status': 'true'
            }
    except Exception as e:
        return {
            'type': 'error',
            'content': f"Error getting table names: {e}",
            'status': 'false'
        }


async def generate_and_process_dalle_images(dalle_prompt: str):
    """
    This function generates DALL-E images based on the given prompts and processes these images. This method is invoked when the user talks about needing to draw.
    Parameters: 
        dalle_prompt: The prompt to generate the DALL-E images. This should be a vivid description based on your analysis of the natural language input. it must be english (required)
    """
    # Define the filename and the image directory
    filename = datetime.datetime.now().strftime(
        '%Y%m%d%H%M%S')  # use the current date and time as the filename
    image_dir = "/tmp"  # replace with your actual image directory

    # Generate your images
    generation_response = await openai.Image.acreate(
        prompt=dalle_prompt,
        n=1,
        size="512x512",
        response_format="url",
    )

    # save the images
    urls = [datum["url"]
            for datum in generation_response["data"]]  # extract URLs
    images = [requests.get(url).content for url in urls]  # download images
    image_names = [f"{filename}_{i + 1}.png"
                   for i in range(len(images))]  # create names
    filepaths = [os.path.join(image_dir, name)
                 for name in image_names]  # create filepaths
    # elements = [cl.Image(name="image1", display="inline", path=path)]

    # await cl.Message(content="Look at this local image!",
    #                  elements=elements).send()
    # Return a JSON object containing the filepaths
    for image, filepath in zip(images,
                               filepaths):  # loop through the variations
        with open(filepath, "wb") as image_file:  # open the file
            image_file.write(image)  # write the image to the fil

    return json.dumps({
        "filepaths": filepaths,
        "status": "true",
    })


async def generate_and_process_stable_diffusion_images(
        stable_diffusion_prompt: str):
    global style_preset
    """
    This function generates stable diffusion images based on the given prompts and processes these images. This method is invoked when the user talks about needing to draw.
    Parameters: 
        stable_diffusion_prompt: The prompt to generate the stable diffusion images. This should be a vivid description based on your analysis of the natural language input. it must be english (required)
    """
    try:
        engine_id = gv.model_id
        api_host = os.getenv('API_HOST', 'https://api.stability.ai')
        api_key = os.environ['SD_API_KEY']

        if api_key is None:
            raise Exception("Missing Stability API key.")

        json_body = {
            "text_prompts": [{
                "text": stable_diffusion_prompt
            }],
            "height": 512,
            "width": 512,
            "cfg_scale": 7,
            "samples": 4,
            "clip_guidance_preset": "FAST_BLUE",
        }
        json_body["style_preset"] = gv.style_preset
        print(json_body)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    f"{api_host}/v1/generation/{engine_id}/text-to-image",
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "Authorization": f"Bearer {api_key}"
                    },
                    json=json_body,
            ) as response:
                if response.status != 200:
                    raise Exception("Non-200 response: " +
                                    str(await response.text()))

                data = await response.json()

        filepaths = []
        for i, image in enumerate(data["artifacts"]):
            filename = f"./images/v1_txt2img_{i}{str(int(time.time()))}.png"
            with open(filename, "wb") as f:
                f.write(base64.b64decode(image["base64"]))
            filepaths.append(filename)

        return {
            "filepaths": filepaths,
            "status": "true",
        }
    except Exception as e:
        return {"status": "false", "error": str(e)}


async def get_style_descriptions():
    """
    This function returns a JSON object containing descriptions of various preset .
    
    Returns:
        str: A JSON object in string format. The JSON object keys are the style model names and the values are their descriptions.
    """
    model = {
        "3d-model":
        "This style is best for creating 3D model-like images.",
        "analog-film":
        "This style is ideal for creating images that look like they were shot on analog film.",
        "anime":
        "This style is recommended for creating anime-style images.",
        "cinematic":
        "This style is suitable for creating images with a cinematic feel.",
        "comic-book":
        "This style is best for creating comic-book-style images.",
        "digital-art":
        "This style is ideal for creating digital art-style images.",
        "enhance":
        "This style is best for enhancing the quality of images.",
        "fantasy-art":
        "This style is recommended for creating fantasy art-style images.",
        "isometric":
        "This style is suitable for creating isometric images.",
        "line-art":
        "This style is best for creating line art-style images.",
        "low-poly":
        "This style is ideal for creating low-poly images.",
        "modeling-compound":
        "This style is recommended for creating images that look like they were made from modeling compound.",
        "neon-punk":
        "This style is suitable for creating neon punk-style images.",
        "origami":
        "This style is best for creating images that look like they were made from origami.",
        "photographic":
        "This style is ideal for creating photographic images.",
        "pixel-art":
        "This style is recommended for creating pixel art-style images.",
    }

    actions = []
    elements = []
    for index, (key, value) in enumerate(model.items()):
        action = cl.Action(name='action_button',
                           value=key,
                           label=key,
                           description=value)
        image = cl.Image(name='action_image',
                         path=f"model_images/{key}.png",
                         display="inline")
        image.size = "small"
        actions.append(action)
        elements.append(image)

    await cl.Message(content="点击图片下面按钮选择模型:",
                     actions=actions,
                     elements=elements,
                     author="action").send()
    actions = []
    elements = []

    return {"status": "true", "description": "Please select a model."}


async def image_2_image_stable_diffusion_images(stable_diffusion_prompt: str,
                                                init_image_path: str):
    """
    This function generates stable diffusion images based on the given prompts and processes these images. 
    This method is invoked when the user talks about needing to draw.
    Parameters: 
        stable_diffusion_prompt: The prompt to generate the stable diffusion images. 
        This should be a vivid description based on your analysis of the natural language input. it must be english (required)
        init_image_path: The path to the initial image file.
    """
    try:
        engine_id = gv.model_id
        api_host = os.getenv("API_HOST", "https://api.stability.ai")
        api_key = os.environ['SD_API_KEY']

        if api_key is None:
            raise Exception("Missing Stability API key.")

        data = {
            "image_strength": 0.35,
            "init_image_mode": "IMAGE_STRENGTH",
            "text_prompts[0][text]": stable_diffusion_prompt,
            "cfg_scale": 7,
            "clip_guidance_preset": "FAST_BLUE",
            "samples": 4,
            "steps": 30,
        }
        data["style_preset"] = gv.style_preset

        with open(init_image_path, "rb") as img_file:
            response = requests.post(
                f"{api_host}/v1/generation/{engine_id}/image-to-image",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {api_key}"
                },
                files={"init_image": img_file},
                data=data)

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        response_data = response.json()

        if "artifacts" not in response_data:
            raise Exception("Unexpected response data: " + str(response_data))

        filepaths = []
        for i, image in enumerate(response_data["artifacts"]):
            filename = f"./images/v1_img2img_{i}.png"
            with open(filename, "wb") as f:
                f.write(base64.b64decode(image["base64"]))
            filepaths.append(filename)

        return {
            "filepaths": filepaths,
            "status": "true",
        }
    except Exception as e:
        return {"status": "false", "error": str(e)}


async def change_sd_model():
    """
    This function is used to switch the model of the Stability Diffusion API.
    """
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    url = f"{api_host}/v1/engines/list"
    api_key = os.environ['SD_API_KEY']
    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.get(url,
                            headers={"Authorization": f"Bearer {api_key}"})

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    # Do something with the payload...
    payload = response.json()
    model_descriptions = {
        engine['id']: engine['description']
        for engine in payload
    }

    actions = []
    for id, description in model_descriptions.items():
        action = cl.Action(name='action_model', # type: ignore
                           value=id,
                           label=id,
                           description=description)
        actions.append(action)

    await cl.Message(content="Please select a model:",
                     actions=actions,
                     author="action").send()

    return {"status": "choose", "description": "请选择上方的一个模型进行切换"}
