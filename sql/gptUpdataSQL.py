import mysql.connector
import time

# 格式化成2016-03-20 11:45:39形式





try:
    connection = mysql.connector.connect(host='localhost', port='3306', user='root', password='jonsoncC7', database='hydroponics')
    cursor = connection.cursor()
    time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ph = 7
    sql = "INSERT INTO hydroponics (time, ph) VALUES (%s, %s);"
    new_data = (time, ph)
    cursor.execute(sql, new_data)
    connection.commit()
    print("Insertion successful")
except mysql.connector.Error as error:
    print("Failed to insert into MySQL table {}".format(error))
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")