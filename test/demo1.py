import asyncio


async def main():
    await asyncio.sleep(2)
    print("Task completed")


if __name__ == '__main__':
    asyncio.create_task(main())

    # 下面的代码会继续执行而不会等待main()任务完成
    print("Continuing to other operations...")

    # 可以继续进行其他操作，而不会被main()任务阻塞
