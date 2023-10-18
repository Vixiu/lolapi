import asyncio
import json
import time
from base64 import b64encode

import aiohttp
import requests
from win32api import Sleep

from Lcu import LcuRequest


async def post_queue(queue_id):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10, ssl=False), trust_env=True) as session:
        async with  session.request(
                "post",


                f"https://127.0.0.1:{lcu.port}/lol-loot/v1/recipes/CHEST_3330162_OPEN/craft?repeat=200",

                headers={
                    "User-Agent": "LeagueOfLegendsClient",
                    'Authorization': 'Basic ' + b64encode(f'riot:{lcu.pw}'.encode()).decode(),
                },
                json=["CHEST_3330162"],

        ) as resp:
            return await resp.text(), queue_id


def result(res):
    print(1)

lcu = LcuRequest()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

task = []

start = time.perf_counter()

for i in range(10):

    _ = loop.create_task(post_queue(i))
    _.add_done_callback(result)
    task.append(_)

    loop.run_until_complete(asyncio.wait(task))

end = time.perf_counter()

# 计算运行时间，单位为秒
print('运行时间为：{}秒'.format(end - start))