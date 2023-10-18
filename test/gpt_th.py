# -*- coding: UTF-8 -*-
import json
import threading
import time

import requests

exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, chat, text):
        threading.Thread.__init__(self)
        self.chat = chat
        self.text = text
        api_key = "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"
        self.url = 'https://api.openai.com/v1/chat/completions'
        self.heards = {
            'Authorization': f'Bearer {api_key}',
            "Content-Type": "application/json"
        }

    def run(self):
        data = {

            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "messages":
                [
                    {"role": "system", "content": "翻译为中文"},
                    {"role": "user", "content": self.chat},
                ]

        }
        res = requests.post(self.url, headers=self.heards, data=json.dumps(data))
        r = res.json()['choices'][0]['message']['content'].split('\n')
        threadLock.acquire()
        with open("D:\\1.txt", "a") as f:
            for i in range(len(self.text)):
                f.write(f'"{self.text[i]}":"{r[i]}",')
        threadLock.release()


threadLock = threading.Lock()


def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1


# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# 开启新线程
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("退出主线程")
