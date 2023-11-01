from flask import Flask,render_template,request,g,redirect    #render_template連分頁   #request拿前端數據 #g上下文變數 #redirect重定向

import mysql.connector  #需要先pip install mysql-connector-python #sql #圖表

import matplotlib.pyplot as plt  # 匯入 Matplotlib 套件   #圖表

import time #ADS#sql
import board #ADS
import busio #ADS
import adafruit_ads1x15.ads1115 as ADS #ADS
from adafruit_ads1x15.analog_in import AnalogIn #ADS

from flask_apscheduler import APScheduler   #定時任務



app = Flask(__name__)   #__name__代表目前執行的模組

scheduler = APScheduler()   

##sql write
nowTime = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) #sql# 格式化成2016-03-20 11:45:39形式
connection = mysql.connector.connect(host = 'localhost',port = '3306',user = 'jonsoncc7',password = 'jonsoncC7',database = 'hydroponics')   #database要使用的資料庫 #sql
cursor = connection.cursor()        #告訴他要開始使用了?#cursor光標 #sql
sql = "INSERT INTO hydroponics (time, ph) VALUES (%s, %s);" #sql

##sql write
    ###ph read
ph = 0
#即使有未處理的異常拋出，也每一次请求之后都会调用，会接受一个参数，参数是服务器出现的错误信息 #要在debug為true情況下
# @app.teardown_request
# def teardown_request(error):
def update_data():

    # Create the I2C bus #創建 I2C 總線
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create the ADC object using the I2C bus #使用I2C總線創建ADC對象
    ads = ADS.ADS1115(i2c)
    # Create single-ended input on channel 0 #在通道0上創建單端輸入
    chan = AnalogIn(ads, ADS.P0)
    print("{:>5}\t{:>5}".format('raw', 'v'))
    
    print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    # format格式化文字 value:取出字典中的所有值
    global ph   #使用全域的ph
    ph = chan.voltage*-5.8887 + 21.677  #套用用戶手冊的公式
    print('ph in teardown_request',ph)
    nowTime = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) #sql# 格式化成2016-03-20 11:45:39形式
    new_data = (nowTime, ph) #sql
    cursor.execute(sql, new_data)   #在sql中的時間和ph位置 新增時間和ph #sql
    print('數據庫寫入','new_data',new_data)
    connection.commit() #有動到資料 都要寫這個 才會提交指令 #sql
scheduler.add_job(id='update_job', func=update_data, trigger='interval', seconds=10)
scheduler.start()
    ###ph read
    # ####圖表
    # # cursor = mydb.cursor()  # 創建 MySQL 游標物件，用於執行 SQL 查詢

    # # 從 MySQL 中擷取資料到 Python 程式中
    # cursor.execute("select time, ph from hydroponics;")  # 執行 SQL 查詢，選擇 hydroponics 表格中的 time 和 ph 欄位
    # result = cursor.fetchall  # 擷取查詢結果

    # time_list = []  # 用來儲存time_list的清單
    # ph_list = []  # 用來儲存ph_list的清單

    # # 迭代處理查詢結果，將姓名和成績分別加入清單
    # for i in cursor:
    #     time_list.append(i[0])  # 將姓名加入 Names 清單
    #     ph_list.append(i[1])  # 將成績加入 Marks 清單

    # # 輸出學生姓名和成績
    # print("Name of Students = ", time_list)  # 顯示學生姓名
    # print("Marks of Students = ", ph_list)  # 顯示學生成績

    # # 使用 Matplotlib 進行資料視覺化
    # # plt.bar(time_list, ph_list)  # 創建長條圖，擺放學生姓名和成績
    # # 繪製折線圖
    # plt.plot(time_list, ph_list, label='折線圖', marker='', linestyle='-', color='b')
    # plt.ylim(0, 14)  # 設定 Y 軸範圍
    # plt.xlabel("time_list")  # 設定 X 軸標籤
    # plt.ylabel("ph_list")  # 設定 Y 軸標籤
    # plt.title("ph_list table")  # 設定圖表標題
    # plt.show()  # 顯示圖表
    #     ####圖表
print('global ph',ph)   
   
###

# student = [                                         #一邊來說這裡是數據庫，這裡用列表示範   #給admin資料
#     {'name': '張三','chinese':'65','math':65,'english':'66'},
#     {'name': '李四','chinese':'65','math':65,'english':'65'},
#     {'name': '王武','chinese':'65','math':65,'english':'65'},
#     {'name': '造六','chinese':'65','math':65,'english':'65'},


# ph = 0##未來要從別的檔案import ph ec
ec = 2.4

i = 1
#test
#0不懂0
#test2526


@app.route('/')     #@裝飾器(路由)      #('/')根目錄   訪問路徑
def hello():
    # return 'hi 這裡是主頁'
    return render_template('main.html') #連到


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',ph=ph)    #連結到dashboard.html

@app.route('/adjust',methods=['GET','POST']) 
def adjust():
    global AdjustPh
    if request.method == 'GET':
        print(request.method)   #表單傳送方法
        AdjustPh = request.values.get('numAdjustPh')    #要調整的ph
        AdjustTemp = request.values.get('numAdjustTemp')  #要調整的溫度
        AdjustRH = request.values.get('numAdjustRH')    #要調整的濕度
        numInterval = request.values.get('numInterval') #打水間隔
        numPump = request.values.get('numPump')

        
        print('ph要調整為:',AdjustPh)
        print('溫度要調整為:',AdjustTemp,'°C')
        print('濕度要調整為:',AdjustRH,'%')
        print('間隔',numInterval,'分鐘，打水',numPump,'分鐘')
        
        # return redirect('/dashboard')   #重定向回dashboard
    return render_template('adjust.html',AdjustPh=AdjustPh,numInterval=numInterval,numPump=numPump,AdjustTemp=AdjustTemp,AdjustRH=AdjustRH)    #連結到adjust.html



# run app
if __name__ == "__main__":      #如果以主程式運行
    # app.run(host='127.0.0.1', port=80)    #啟動伺服器
    app.run('127.0.0.1',debug=True) 