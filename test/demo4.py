import asyncio
import threading

from PyQt5.QtCore import QThread


class MyThread(QThread):
    def run(self):
        # 创建一个新的事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # 在新的事件循环中运行异步函数
        loop.run_until_complete(self.my_async_function())

        # 关闭事件循环
        loop.close()

    async def my_async_function(self):
        print("Start async function")
        await asyncio.sleep(2)
        print("End async function")


# 创建并启动线程
my_thread = MyThread()
my_thread.start()

# 等待线程结束
my_thread.wait()
