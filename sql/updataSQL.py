import mysql.connector

ph=7

connection = mysql.connector.connect(host = 'localhost',port = '3306',user = 'root',password = 'jonsoncC7',database = 'hydroponics')   #database要使用的資料庫

cursor = connection.cursor()        #告訴他要開始使用了?#cursor光標

sql = "INSERT INTO hydroponics (time, ph) VALUES (%s, %s);"
new_data = (null, ph)
cursor = connection.cursor()
cursor.execute(sql, new_data)