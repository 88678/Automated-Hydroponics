#/coding=utf-8
# 用ads讀ph值出來 再把ph存到SQL
import mysql.connector  #需要先pip install mysql-connector-python #sql

import time #ADS#sql
import board #ADS
import busio #ADS
import adafruit_ads1x15.ads1115 as ADS #ADS
from adafruit_ads1x15.analog_in import AnalogIn #ADS

nowTime = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) #sql# 格式化成2016-03-20 11:45:39形式

connection = mysql.connector.connect(host = 'localhost',port = '3306',user = 'jonsoncc7',password = 'jonsoncC7',database = 'hydroponics')   #database要使用的資料庫 #sql

cursor = connection.cursor()        #告訴他要開始使用了?#cursor光標 #sql

sql = "INSERT INTO hydroponics (time, ph) VALUES (%s, %s);" #sql

'''
sql上面
ads(PH)下面
'''


# Create the I2C bus #創建 I2C 總線
i2c = busio.I2C(board.SCL, board.SDA) #ADS

# Create the ADC object using the I2C bus #使用I2C總線創建ADC對象
ads = ADS.ADS1115(i2c) #ADS

# Create single-ended input on channel 0 #在通道0上創建單端輸入
chan = AnalogIn(ads, ADS.P0) #ADS

# Create differential input between channel 0 and 1 #在通道0和1之間創建差分輸入
#chan = AnalogIn(ads, ADS.P0, ADS.P1)   #AnalogIn(模擬輸入) 接口用於讀取施加到模擬輸入引腳的電壓。
ph = chan.voltage*-5.8887 + 21.677  #套用用戶手冊的公式 #ADS

print("{:>5}\t{:>5}\t{:>5}".format('raw', 'v','PH')) #ADS

try:
    while True:
        print("{:>5}\t{:>5.3f}\t{:>5}".format(chan.value, chan.voltage,ph)) #ADS
        # format格式化文字 value:取出字典中的所有值
        time.sleep(10) #ADS

        new_data = (nowTime, ph) #sql
        cursor.execute(sql, new_data)   #在sql中的時間和ph位置新增時間和ph #sql
        print('sql',sql,'new_data',new_data)
        connection.commit() #有動到資料 都要寫這個 才會提交指令 #sql
except:
    print('  關閉連線')
    connection.close()  #關閉connection連線 #sql    
