import asyncio
from base64 import b64encode

import json

import aiohttp
import requests
from psutil import process_iter

from urllib3 import disable_warnings
from requests import request
import logging


class LcuRequest:
    disable_warnings()

    def __init__(self):
        self.logger = logging.getLogger('my_logger')
        self.ws_session = None
        self.ws_client = None
        self.event_call_back = {}
        self.port, self.token, self.url = '', '', ''
        self.headers = {}
        lcu_args = self.get_lcu_args()
        if lcu_args:
            self.port, self.token = lcu_args.get('app-port', '0000'), lcu_args.get("remoting-auth-token", 'None')
            self.url = 'https://127.0.0.1:' + self.port
            self.headers = {
                "User-Agent": "LeagueOfLegendsClient",
                'Authorization': 'Basic ' + b64encode(('riot' + ':' + self.token).encode()).decode(),

            }

        else:
            self.logger.warning('未找到Lcu进程.')

    async def start(self, wait_lcu_thread=2):
        while True:
            lcu_args = self.get_lcu_args()
            if lcu_args:
                self.port, self.token = lcu_args.get('app-port', '0000'), lcu_args.get("remoting-auth-token", 'None')
                self.url = 'https://127.0.0.1:' + self.port
                self.headers = {
                    "User-Agent": "LeagueOfLegendsClient",
                    'Authorization': 'Basic ' + b64encode(('riot' + ':' + self.token).encode()).decode(),

                }
                while True:
                    try:
                        res = self.getdata('/lol-summoner/v1/current-summoner').json()
                        if "errorCode" not in res:
                            await self.connect_websocket()
                            break
                    except requests.exceptions.ConnectionError:
                        print('等待客户端加载完毕')
                break
            elif wait_lcu_thread > -1:
                self.logger.warning(f'未找到Lcu进程,将在{wait_lcu_thread}秒后重试...')
                await asyncio.sleep(wait_lcu_thread)
            else:
                self.logger.warning('未找到Lcu进程.')

    def get_lcu_args(self):
        cmd_line = []
        for prs in process_iter():
            if prs.name() in ['LeagueClient', 'LeagueClientUx.exe']:
                cmd_line = prs.cmdline()
                break
        return {
            line[2:].split('=', 1)[0]: line[2:].split('=', 1)[1]
            for line in cmd_line
            if '=' in line
        }

    def getdata(self, path, method='get', data=None) -> requests.Response:
        """
        :param path:路径
        :param method:方式,默认get
        :param headers:参数
        :param data:内容body
        :return:数据
        """
        return request(method, self.url + path, headers=self.headers, data=json.dumps(data), verify=False)

    async def connect_websocket(self):
        self.ws_session = aiohttp.ClientSession(auth=aiohttp.BasicAuth('riot', self.token), headers={
            "User-Agent": "LeagueOfLegendsClient",
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.ws_client = await self.ws_session.ws_connect(f'wss://127.0.0.1:{self.port}', ssl=False)
        '''
     
        '''

    async def async_getdata(self, path, method='GET', data=None):
        async with await self.ws_session.request(method, f'{self.url}{path}', data=json.dumps(data), ssl=False) as resp:
            data = await resp.text()
            if data:
                data = json.loads(data)
                return data
            return {}

    async def subscribe(self, event: str, call_back):
        if event in self.event_call_back:
            pass
        else:
            await self.ws_client.send_json([5, event])
            self.event_call_back[event] = call_back

    async def unsubscribe(self, event: str):
        if event in self.event_call_back:
            del self.event_call_back[event]
        else:
            pass

    async def run(self):
        loop = asyncio.get_running_loop()
        async for msg in self.ws_client:
            if msg.type == aiohttp.WSMsgType.TEXT and msg.data:
                resp = json.loads(msg.data)
                data = {} if resp[2]['data'] is None else resp[2]['data']
                loop.create_task(self.event_call_back[resp[1]](data))
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print(f'WebSocket connection closed with exception {self.ws_client.exception()}')
        await self.ws_session.close()

    async def close_websocket(self):
        await self.ws_client.close()
        await self.ws_session.close()

    def reset(self):
        self.__init__()


lcu = LcuRequest()
