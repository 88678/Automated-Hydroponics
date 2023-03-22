import mysql.connector
import time

# 格式化成2016-03-20 11:45:39形式
time = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

ph=7

connection = mysql.connector.connect(host = 'localhost',port = '3306',user = 'root',password = 'jonsoncC7',database = 'hydroponics')   #database要使用的資料庫

cursor = connection.cursor()        #告訴他要開始使用了?#cursor光標

sql = "INSERT INTO hydroponics (time, ph) VALUES (%s, %s);"
new_data = (time, ph)

cursor.execute(sql, new_data)   #???

connection.commit() #有動到資料 都要寫這個 才會提交指令

connection.close()  #關閉connection連線