import win32gui

hwnd = win32gui.FindWindow(None,'League of Legends')

print(hwnd)
