import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
from jupyter_client.manager import KernelManager
from queue import Empty
import re

# 定义移除ANSI转义序列的函数
def remove_ansi_escape_sequences(s):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', s)


class CodeExecutor:
    def __init__(self):
        # 创建一个新的内核管理器
        self.km = KernelManager()
        self.km.start_kernel()

        # 创建一个客户端并连接到新的内核
        self.kc = self.km.blocking_client()
        self.kc.start_channels()
        # 创建一个线程池执行器来运行阻塞操作
        self.executor = ThreadPoolExecutor(max_workers=1)

    async def execute(self, code):
        # 执行代码
        msg_id = self.kc.execute(code)

        # 用于保存所有收到的消息
        all_msgs = []

        # 等待执行结果
        while True:
            try:
                # 在新的线程中运行 get_iopub_msg 方法，并在异步函数中等待它的完成
                msg = await asyncio.get_event_loop().run_in_executor(self.executor, self.kc.get_iopub_msg, 60)
            except Empty:
                return None
            else:
                if msg["parent_header"].get("msg_id") == msg_id:
                    msg_type = msg["msg_type"]
                    content = msg["content"]
                    if msg_type == "execute_result" or msg_type == "display_data":
                        all_msgs.append(content["data"]["text/plain"])
                    elif msg_type == "stream":
                        all_msgs.append(content["text"])
                    elif msg_type == "error":
                        # 提取错误信息
                        traceback = content['traceback']
                        user_traceback = [remove_ansi_escape_sequences(line) for line in traceback]
                        # 我需要取0,1和-1行
                        indices_to_try = [2, 3, -1]  # Indices we are interested in
                        final_error = []

                        if len(user_traceback) >= 4:
                            for index in indices_to_try:
                                element = str(user_traceback[index])
                                if element not in final_error:  # Check for duplicates
                                    final_error.append(element)
                        else:  
                            # Keep all elements for lengths less than 4
                            final_error = [str(item) for item in user_traceback]
                        error_info = '\n'.join(final_error)
                        return f"Error info:\n{error_info}"
                    elif msg_type == "status" and content['execution_state'] == 'idle':
                        # 只保留all_msgs中的最后三个元素,不足三个元素则全部保留
                        if len(all_msgs) > 3:
                            all_msgs = all_msgs[-3:]
                        return '\n'.join(all_msgs)
                   
    def shutdown(self):
        # 关闭通道和内核
        time.sleep(2)
        self.kc.stop_channels()
        self.km.shutdown_kernel()
        # 关闭线程池执行器
        self.executor.shutdown()
        
        

if __name__ == "__main__":
    executor = CodeExecutor()
    res = executor.execute("""import matplotlib.pyplot as plt\n\nrandom_numbers = [42, 25, 69, 66, 42, 65, 73, 4, 74, 20]\n\nplt.plot(random_numbers)\nplt.xlabel('Index')\nplt.ylabel('Value')\nplt.title('Random Numbers')\nplt.savefig('./tmp/random_numbers.png')\nprint('path': './tmp/random_numbers.png')""")
    print("====================================")
    print(res)
    print("====================================")
    executor.shutdown()