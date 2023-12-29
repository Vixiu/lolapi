import asyncio

from win32api import Sleep

from Lcu import LcuRequest


async def ft(data):
    await asyncio.sleep(3)
    print(data)


async def main():
    await lcu.connect_websocket()
    print(await lcu.async_getdata('/lol-summoner/v1/current-summoner'))
    await lcu.subscribe('OnJsonApiEvent', ft)
    await lcu.run()
    await lcu.close_websocket()


if __name__ == '__main__':
    lcu = LcuRequest()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
