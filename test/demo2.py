import ctypes

import wmi

command = 'WMIC PROCESS WHERE name="LeagueClientUx.exe" GET commandline'

import ctypes, sys
import os


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    os.system(command)
 
    pass
else:
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
