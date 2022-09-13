import psutil


def CheckProcess():
    process = psutil.pids()
    for pid in process:
        if psutil.Process(pid).name() == 'LeagueClient.exe':
            return pid
    else:
        return None
