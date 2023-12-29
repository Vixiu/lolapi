import asyncio
import ssl

import aiohttp
import websockets
import json

from Lcu import LcuRequest


#        self.ws_session = aiohttp.ClientSession(auth=aiohttp.BasicAuth('riot', self._auth_key), headers=self._headers)
#       self.ws_client = await self.ws_session.ws_connect(f'wss://127.0.0.1:{self._port}', ssl=False)

# mHhI4u-HvZJQyB_R-7CBfg 14888
async def main():
    ws_session = aiohttp.ClientSession(auth=aiohttp.BasicAuth('riot', lcu.token), headers={
        "User-Agent": "LeagueOfLegendsClient"
    })
    ws_client = await ws_session.ws_connect(f'wss://127.0.0.1:{lcu.port}', ssl=False)
    res = await ws_session.request('GET', f'https://127.0.0.1:{lcu.port}/lol-summoner/v1/current-summoner', ssl=False)
    print(await res.text())
    await ws_client.send_json([5, 'OnJsonApiEvent_lol-kr-playtime-reminder_v1_message'])
    '''
    async for msg in ws_client:
        if msg.type == aiohttp.WSMsgType.TEXT:
            print(f'Received message: {msg.data}')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print(f'WebSocket connection closed with exception {ws_client.exception()}')
    await ws_session.close()
    '''

if __name__ == '__main__':
    lcu = LcuRequest()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
