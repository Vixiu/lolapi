from mpmath import mp

# 设置 mp 中的浮点数精度（位数）
mp.dps = 1000000000000000000  # 设置为1万零1位

# 计算 π
pi = mp.pi

# 输出 π 的后1万位
print(str(pi)[2:])  # 去掉小数点，输出后1万位
