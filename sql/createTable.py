#應該一開始執行一次就好
#測試時一開始執行沒有結果，用偵錯就可以跑了
#1.創建資料庫 和3.創建表格 要分開來執行

import mysql.connector  #需要先pip install mysql-connector-python

connection = mysql.connector.connect(host = 'localhost',port = '3306',user = 'jonsoncc7',password = 'jonsoncC7') #連線    #因為在本機，所以是locahost   #port會寫在mySQL workbench  #user和password是workbench的使用者名稱和密碼

cursor = connection.cursor()        #告訴他要開始使用了?#cursor光標

#1.創建資料庫
cursor.execute('CREATE DATABASE `hydroponics`;') #execute執行SQL指令    #在()內輸入SQL指令  #創建一個叫hydroponics的資料庫

#刪除資料庫(有需要再用)
# cursor.execute('drop database `hydroponics`;	')

#取得資料庫名稱
# cursor.execute('SHOW DATABASES;')   #回傳資料
# records = cursor.fetchall()  #取出資料(列表狀態)  #fetchall()：取出全部資料
# for r in records:           #把列表取出 印出
#     print(r)

#2.選擇資料庫
cursor.execute('USE `hydroponics`;')  #使用hydroponics資料庫

#3.創建表格
cursor.execute('CREATE TABLE `hydroponics`(`time` TIMESTAMP,`ph` DECIMAL(4,2));')  #創建名為hydroponics的表格有time和ph兩個屬性 資料型態分別為TIMESTAMP和decimal(總共有幾位數,小數點後面有幾位)

#刪除表格(有需要再用)
# cursor.execute('DROP TABLE `hydroponics`;')

#4.顯示表格
cursor.execute('describe `hydroponics`;	')
records = cursor.fetchall()   #fetchall()：取出全部資料(列表狀態)
for r in records:           #把列表取出 印出
    print(r)

print('running')

#執行完後都要關閉
cursor.close()  #關閉cursor
connection.close()  #關閉connection連線