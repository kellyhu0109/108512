import pymysql

connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='bighitbts',
    db='bigdata',
    charset='utf8mb4'
)

cursor = connection.cursor()


def dbcnt():
    a = cursor.execute('SELECT * FROM user_message')
    b = cursor.fetchall()
    # return str(a)
    return b
