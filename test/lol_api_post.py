import asyncio

from win32api import Sleep

from Lcu import LcuRequest


async def ft(data):
    print(data)


async def main():
    await lcu.start()
    await lcu.subscribe('OnJsonApiEvent_lol-champ-select_v1_session', ft)
    await lcu.run()


if __name__ == '__main__':
    lcu = LcuRequest()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
