from win32api import Sleep

from Lcu import LcuRequest

lcu = LcuRequest()

while True:
    res = lcu.getdata("/lol-champ-select/v1/session/timer").json()
    print(res['adjustedTimeLeftInPhase'] / 1000, res['phase'],res['internalNowInEpochMs'])
    Sleep(1000)
