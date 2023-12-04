import time

import pygetwindow

# 获取所有窗口
windows = pygetwindow.getAllWindows()
time.sleep(2)
# 循环遍历所有窗口
for window in windows:
    print(window)
    if "League" in window.title:
        print(f"窗口标题：{window.title}, 位置：{window.topleft}, 大小：{window.size}")

        # 检查窗口是否最小化
        if window.isMinimized:
            print(f"窗口 '{window.title}' 已最小化")
        if not window.isActive:
            print(f"窗口 '{window.title}' 被遮挡")
# 通过标题获取特定窗口
# specific_window = gw.getWindowsWithTitle("Your Window Title")[0]
# print(f"Specific Window - 位置：{specific_window.topleft}, 大小：{specific_window.size}")
