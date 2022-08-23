import json

from requests import request

from Fuwendemo import FuWen
from Lcu import LcuRequest

lolpath = 'F:\\1\\英雄联盟-\\LeagueClient'

lcures = LcuRequest(lolpath)
a = FuWen(lcures)
a.show()
a.exec()