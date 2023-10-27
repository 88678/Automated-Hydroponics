from flask import Flask,render_template,request,g,redirect    #render_template連分頁   #request拿前端數據 #g上下文變數 #redirect重定向

import mysql.connector  #需要先pip install mysql-connector-python #sql

import time #ADS#sql
import board #ADS
import busio #ADS
import adafruit_ads1x15.ads1115 as ADS #ADS
from adafruit_ads1x15.analog_in import AnalogIn #ADS


app = Flask(__name__)   #__name__代表目前執行的模組

##sql write
nowTime = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) #sql# 格式化成2016-03-20 11:45:39形式
connection = mysql.connector.connect(host = 'localhost',port = '3306',user = 'jonsoncc7',password = 'jonsoncC7',database = 'hydroponics')   #database要使用的資料庫 #sql
cursor = connection.cursor()        #告訴他要開始使用了?#cursor光標 #sql
sql = "INSERT INTO hydroponics (time, ph) VALUES (%s, %s);" #sql

##sql write
    ###ph read
ph = 0
#即使有未處理的異常拋出，也每一次请求之后都会调用，会接受一个参数，参数是服务器出现的错误信息 #要在debug為true情況下
@app.teardown_request
def teardown_request(error):

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
    ###ph
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


# @app.route('/login',methods=['GET','POST']) #因為要使用post方法?
# def login():
#     #登入的功能
#     #request對象可以拿到瀏覽器(前端)傳給服務器的所有數據
#     if request.method == 'POST':
#         username = request.form.get('txtAct')
#         password = request.form.get('txtPas')
#         #應該要登入後 連接數據庫 校驗帳密   這裡先省略
#         print('從服務器接收到的數據:',username,password)
#         return redirect('/admin')
#     return render_template('login.html')

# @app.route('/admin')
# def admin():
#     return render_template('admin.html',student=student)    #把上面列表(數據庫)傳給admin

# @app.route('/add',methods=['GET','POST'])
# def add():                             #添加學生信息
#     if request.method == 'POST':
#         username = request.form.get('txtName')
#         chinese = request.form.get('chinese')
#         math = request.form.get('math')
#         english = request.form.get('english')
#         print('獲取的學員信息',username,chinese,math,english)
#         student.append({'name':username, 'chinese':chinese, 'math':math, 'english':english})
#         return redirect('/admin')       #重定向回admin
        
#     return render_template('add.html')    #返回add.html

# @app.route('/delete')
# def delete_student():       #刪除學生信息   #在後台需要拿到學員的信息(名子)，才能刪除
#     print(request.method)
#     username = request.args.get('name')     #取出後端的值 看是否和前端要刪除的東西一樣 ，若一樣就刪除
#     for stu in student:    
#         if stu['name'] == username:     
#                student.remove(stu)      #刪除student列表中的 那個和 前端傳過來要刪除的name 一樣的name #??不是只刪除name嗎?

#     return redirect('/admin')   #重定向回admin

# @app.route('/change',methods=['GET','POST'])
# def change_student():       #修改學生信息
#     #先顯示學員的數據，然後在瀏覽器修改，提交到服務器保存
#     username = request.args.get('name')     #取出後端的值 

#     if request.method == 'POST':        #如果請求方法為post 用變數去存回傳的值
#         username = request.form.get('txtName')
#         chinese = request.form.get('chinese')
#         math = request.form.get('math')
#         english = request.form.get('english')

#         for stu in student:             #將列表裡的東西取出
#             if stu['name'] == username:     #如果列表中的名子等於回傳的名子 就修改列表內的其他資料
#                 stu['chinese'] = chinese
#                 stu['math'] = math
#                 stu['english'] = english
#         return redirect('/admin')   #重定向回admin

#     for stu in student:    
#         if stu['name'] == username:   
#             #需要在頁面中渲染學生的成績數據
#             return render_template('change.html',student=stu)       #把學員數據顯示到前端
#     return redirect('/admin')   #重定向回admin
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