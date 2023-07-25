import sys
import ast
from io import StringIO
from pprint import pformat
from typing import Dict, Optional, Any

def is_module_installed(module_name: str) -> bool:
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def disable_graphics_displays():
    # 对于matplotlib
    if is_module_installed("matplotlib"):
        import matplotlib
        matplotlib.use('Agg')

    # 对于PIL/Pillow
    if is_module_installed("PIL"):
        from PIL import Image
        def disable_show(*args, **kwargs):
            print("Image display is disabled.")
        Image.Image.show = disable_show

    # 对于cv2 (OpenCV)
    if is_module_installed("cv2"):
        import cv2
        def disable_imshow(*args, **kwargs):
            print("cv2 imshow is disabled.")
        cv2.imshow = disable_imshow

    # 对于plotly
    if is_module_installed("plotly"):
        import plotly.io as pio
        pio.renderers.default = "json"

    # 对于bokeh
    if is_module_installed("bokeh"):
        from bokeh.io import output_notebook
        output_notebook()

    # 对于pygame
    if is_module_installed("pygame"):
        import pygame
        pygame.init()
        pygame.display.set_mode((1, 1))
        pygame.display.iconify()

    # 对于tkinter
    if is_module_installed("tkinter"):
        import tkinter
        def disable_mainloop(*args, **kwargs):
            print("Tkinter mainloop is disabled.")
        tkinter.Tk.mainloop = disable_mainloop

class PythonExecutor:
    
    def __init__(self):
        self._context = {}

    def execute(self, code: str) -> Dict[str, Optional[str]]:
        """
        执行传入的Python代码，并返回执行结果和任何打印输出。
        返回值是一个字典，其中:
        'result' - 是执行的结果（如果有的话）
        'output' - 是任何打印输出
        """
        # 禁用图形显示功能
        disable_graphics_displays()

        # 设置捕获标准输出
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        response = {
            'result': '',
            'output': ''
        }

        try:
            # 尝试使用 eval 来评估代码
            result = eval(code, self._context, self._context)
            response['result'] = pformat(result)
        except SyntaxError:
            # 如果是语句，则使用 exec
            try:
                exec(code, self._context, self._context)
                # 试图得到代码的最后一个表达式的值
                lines = [line.strip() for line in code.split('\n') if line.strip()]
                if lines:
                    try:
                        last_result = eval(lines[-1], self._context, self._context)
                        response['result'] = last_result
                    except:
                        pass
            except Exception as e:
                response['result'] = repr(e)
        except Exception as e:
            response['result'] = repr(e)

        response['result'] = str(response['result'])
        # 获取标准输出内容
        sys.stdout = old_stdout
        output = mystdout.getvalue()
        response['output'] = output.strip() if output else None

        return response
   
    def get_context(self):
        """返回当前的上下文（包括所有变量和函数）"""
        return self._context
    
    

if __name__ == "__main__":
    executor = PythonExecutor()
    res = executor.execute("""import dlib\nimport cv2\n\n# Load the image\nimage_path = '../../tmp/1.png'\nimage = cv2.imread(image_path)\n\n# Initialize the face detector\ndetector = dlib.get_frontal_face_detector()\n\n# Convert the image to grayscale\ngray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n\n# Detect faces in the grayscale image\nfaces = detector(gray)\n\n# Draw rectangles around the detected faces\nfor face in faces:\n    x, y, w, h = face.left(), face.top(), face.width(), face.height()\n    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)\n\n# Save the image with the rectangles\noutput_path = './tmp/1_face_detected.png'\ncv2.imwrite(output_path, image)\n\noutput_path""")

    print(res)