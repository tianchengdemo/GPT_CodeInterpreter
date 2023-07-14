import asyncio
import os
from tornado.escape import json_encode, json_decode, url_escape
from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from uuid import uuid4

ws = None  # Declare ws as a global variable

client = AsyncHTTPClient()

async def run_code(code):
    global ws  # Tell Python that we'll be using the global ws variable
    results = []
    msg_id = uuid4().hex
    await ws.write_message(json_encode({
        'header': {
            'username': '',
            'version': '5.0',
            'session': '',
            'msg_id': msg_id,
            'msg_type': 'execute_request'
        },
        'parent_header': {},
        'channel': 'shell',
        'content': {
            'code': code,
            'silent': False,
            'store_history': False,
            'user_expressions': {},
            'allow_stdin': False
        },
        'metadata': {},
        'buffers': {}
    }))

    while True:
        msg = await ws.read_message()
        msg = json_decode(msg)
        msg_type = msg['msg_type']
        if msg_type == 'error':
            print('ERROR')
            print(msg)
            break
        parent_msg_id = msg['parent_header']['msg_id']
        if msg_type == 'stream' and parent_msg_id == msg_id:
            results.append(msg['content']['text'])
            break

    return results

async def main(code):
    global ws  # Tell Python that we'll be using the global ws variable
    if not ws or ws.close:
        base_url = os.getenv('BASE_GATEWAY_HTTP_URL', 'http://localhost:8888')
        base_ws_url = os.getenv('BASE_GATEWAY_WS_URL', 'ws://localhost:8888')
        response = await client.fetch(
            '{}/api/kernels'.format(base_url),
            method='POST',
            auth_username='fakeuser',
            auth_password='fakepass',
            body=json_encode({'name': 'python3'})
        )
        kernel = json_decode(response.body)
        kernel_id = kernel['id']

        ws_req = HTTPRequest(url='{}/api/kernels/{}/channels'.format(
            base_ws_url,
            url_escape(kernel_id)
        ),
            auth_username='fakeuser',
            auth_password='fakepass'
        )
        ws = await websocket_connect(ws_req)

    result = await run_code(code)

    ws.close()  # Close the WebSocket connection

    return result

async def test_program():
    for i in range(5):
        print(f"Running iteration {i+1}")
        code = """
from PIL import Image
img = Image.new('RGB', (60, 30), color = 'red')
img_path = 'output.png'  # 更改为你想要保存的位置和文件名
img.save(img_path)
print('Image saved to {}'.format(img_path))
        """
        result = await main(code)
        print(f"Result: {result}")
        await asyncio.sleep(1)  # Wait for the WebSocket connection to close

# 运行测试程序
# loop = asyncio.get_event_loop()
# loop.run_until_complete(test_program())
# loop.close()