import asyncio
import time

import requests
from win32api import Sleep

from Lcu import LcuRequest

LOL_PATH = 'F:\\1\\英雄联盟-\\LeagueClient'

lcu = LcuRequest(LOL_PATH)
try:

    print(lcu.getdata('/lol-gameflow/v1/session').text)

# utility
except requests.exceptions.ConnectionError:
    print(1)
except Exception as e:
    print(e)
    print(2)
