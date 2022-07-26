import pymysql


def savadata(data):
    sql = "INSERT INTO lols VALUES(%s,%s,%s)"
    try:
        cur.executemany(sql, data)
        connect.commit()
    except Exception as e:
        print("失败:", e)


def dxxxxx():
    read_len = 10240
    with open(r'F:\1\lllllollllll\3.txt', 'r', encoding='utf-8') as f:
        lineList = []
        for line in f:
            lineList.append(tuple(line.strip().split("\t", 3)))
            if (len(lineList) >= read_len):
                savadata(lineList)
                lineList = []
        savadata(lineList)


# ---------连接--------------
connect = pymysql.connect(host='localhost',  # 本地数据库
                          user='root',
                          password='123456',
                          db='16e',
                          charset='utf8')  # 服务器名,账户,密码，数据库名称

cur = connect.cursor()

cur.execute("SELECT * FROM lols WHERE lolname='愉快的4小二货'")
shuJu=cur.fetchall()

for i in shuJu:
    print(i)




