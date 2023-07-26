import json
import os
import chainlit as cl


async def need_file_upload():
    """
    When the user's question refers to managing files and requires file uploads, you can invoke this function.
    Parameters: None
    """
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
            # More MIME types here as needed.
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
    return {
        'description': f"upload file ./tmp/{save_path} success",
    }
    
async def need_rename_file(old_path: str, new_path: str):
    """
    When the user's question refers to managing files and requires file rename, you can invoke this function.
    Parameters: old_path: The old path of the file.(required)
    new_path: The new path of the file.(required)
    """
    # 判断old_path是否存在
    if not os.path.exists(old_path):
        return {'description': f"{old_path} is not exist"}
    # 判断new_path是否存在
    if os.path.exists(new_path):
        return {'description': f"{new_path} is already exist"}
    # 重命名文件
    os.rename(old_path, new_path)
    return {'description': f"rename file {old_path} to {new_path} success"}


# async def show_images(title: str,paths: str):
#     """
#     If your return contains images in png or jpg format, you can call this function to display the images.
#     Parameters: title: The title of the image. paths: The path of the image.(required)
#     paths: The paths of the images as a comma-separated string.(required)
#     """
#     path_list = paths.split(',')
#     elments = []
#     for i, path in enumerate(path_list):
#         tmp_image = cl.Image(name=f"image{i}",
#                              path=path.strip(),
#                              display="inline")
#         tmp_image.size = "large"
#         elments.append(tmp_image)

#     await cl.Message(content=title,
#                      elements=elments).send()  # type: ignore

#     return {'description': '图片已经显示成功了，下面的回复中不再需要展示它了'}