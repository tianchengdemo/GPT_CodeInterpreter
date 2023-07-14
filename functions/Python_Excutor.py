import os
from uuid import uuid4
from tornado.escape import json_encode, json_decode, url_escape
from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


class PythonExecutor:
    def __init__(self):
        self.ws = None
        self.kernel_id = None
        self.client = AsyncHTTPClient()

    async def connect(self):
        if self.ws and not self.ws.closed:
            return

        base_url = os.getenv('BASE_GATEWAY_HTTP_URL', 'http://localhost:8888')
        base_ws_url = os.getenv('BASE_GATEWAY_WS_URL', 'ws://localhost:8888')
        response = await self.client.fetch(
            '{}/api/kernels'.format(base_url),
            method='POST',
            auth_username='fakeuser',
            auth_password='fakepass',
            body=json_encode({'name': 'python3'})
        )
        kernel = json_decode(response.body)
        self.kernel_id = kernel['id']

        ws_req = HTTPRequest(url='{}/api/kernels/{}/channels'.format(
            base_ws_url,
            url_escape(self.kernel_id)
        ),
            auth_username='fakeuser',
            auth_password='fakepass'
        )
        self.ws = await websocket_connect(ws_req)

    async def execute(self, code: str):
        await self.connect()

        results = []
        result = {}

        try:
            msg_id = uuid4().hex
            await self.ws.write_message(json_encode({
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
                msg = await self.ws.read_message()
                msg = json_decode(msg)
                msg_type = msg['msg_type']
                if msg_type == 'error':
                    print('ERROR')
                    print(msg['content'])
                    result['error'] = msg['content']['evalue']
                    break
                parent_msg_id = msg['parent_header']['msg_id']
                if msg_type == 'stream' and parent_msg_id == msg_id:
                    results.append(msg['content']['text'])
                    break
            result['results'] = results
        except Exception as e:
            result['error'] = str(e)

        return results