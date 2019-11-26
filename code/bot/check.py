import pymysql

connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='admin',
    password='bighitbts',
    db='mydb',
)

cursor = connection.cursor()


def dbcnt():
    a = cursor.execute('SELECT * FROM user_message')
    b = cursor.fetchall()
    # return str(a)
    return b
