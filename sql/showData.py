import mysql.connector

connection = mysql.connector.connect(host = 'localhost',port = '3306',user = 'root',password = 'jonsoncC7',database = 'hydroponics')   #database要使用的資料庫

cursor = connection.cursor()        #告訴他要開始使用了?#cursor光標

cursor.execute('SELECT * FROM `hydroponics`;')   #執行SQL指令   #回傳hydroponics表格中的所有資料

records = cursor.fetchall()  #取出資料(列表狀態)
for r in records:           #把列表取出 印出
    print(r)
print('running')
#執行完後都要關閉
cursor.close()  #關閉cursor
connection.close()  #關閉connection連線