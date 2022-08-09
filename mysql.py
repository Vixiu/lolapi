import sys

import pymysql

#sys.setrecursionlimit(10240)  # 设置最大递归次数


def savadata(data):
    sql = "INSERT INTO se VALUES(%s,%s)"
    try:
        cur.executemany(sql, data)
        connect.commit()
    except Exception as e:
        with open(r'F:\1\裤子\err_e.txt', 'a+', encoding='utf-8') as f:
            f.write(str(data) + '\n')
        '''
        strl = str(e).split('\'')
        if len(strl) == 5:
            strl = strl[1]
            # print(strl,data)
            for i in data:
                if strl in i:
                    data.remove(i)
                    with open(r'F:\1\裤子\err_cf.txt', 'a+', encoding='utf-8') as f:
                        f.write(str(i) + '\n')
                    break
            savadata(data)
        else:
            with open(r'F:\1\裤子\err_e.txt', 'a+', encoding='utf-8') as f:
                f.write(str(e) + '\n')
                f.write(str(data) + '\n')
        '''


def dxxxxx():
    read_len = 20480
    with open(r'F:\1\裤子\1.txt', 'r', encoding='utf-8') as f:
        lineList = []
        for line in f:
            line = line.strip().split("----", 2)
            if len(line) != 2:
                with open(r'F:\1\裤子\err_line.txt', 'a+', encoding='utf-8') as f:
                    f.write(str(line) + '\n')
                continue
            lineList.append(line)
            if len(lineList) >= read_len:
                savadata(lineList)
                lineList = []
        savadata(lineList)


# ---------连接--------------
connect = pymysql.connect(host='localhost',  # 本地数据库
                          user='root',
                          password='123456',
                          db='se_data',
                          charset='utf8')  # 服务器名,账户,密码，数据库名称

cur = connect.cursor()
dxxxxx()
