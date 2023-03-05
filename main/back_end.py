from flask import Flask,render_template,request,redirect    #render_template連分頁   #request拿前端數據  #redirect重定向

app = Flask(__name__)   #__name__代表目前執行的模組

student = [                                         #一邊來說這裡是數據庫，這裡用列表示範   #給admin資料
    {'name': '張三','chinese':'65','math':65,'english':'66'},
    {'name': '李四','chinese':'65','math':65,'english':'65'},
    {'name': '王武','chinese':'65','math':65,'english':'65'},
    {'name': '造六','chinese':'65','math':65,'english':'65'},

]
ph = 5.33##未來要從別的檔案import ph ec
ec = 2.4

i = 1
#test
#0不懂
#test2526


@app.route('/')     #@裝飾器(路由)      #('/')根目錄   訪問路徑
def hello():
    # return 'hi 這裡是主頁'
    return render_template('main.html') #連到


@app.route('/login',methods=['GET','POST']) #因為要使用post方法?
def login():
    #登入的功能
    #request對象可以拿到瀏覽器(前端)傳給服務器的所有數據
    if request.method == 'POST':
        username = request.form.get('txtAct')
        password = request.form.get('txtPas')
        #應該要登入後 連接數據庫 校驗帳密   這裡先省略
        print('從服務器接收到的數據:',username,password)
        return redirect('/admin')
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin.html',student=student)    #把上面列表(數據庫)傳給admin

@app.route('/add',methods=['GET','POST'])
def add():                             #添加學生信息
    if request.method == 'POST':
        username = request.form.get('txtName')
        chinese = request.form.get('chinese')
        math = request.form.get('math')
        english = request.form.get('english')
        print('獲取的學員信息',username,chinese,math,english)
        student.append({'name':username, 'chinese':chinese, 'math':math, 'english':english})
        return redirect('/admin')       #重定向回admin
        
    return render_template('add.html')    #返回add.html

@app.route('/delete')
def delete_student():       #刪除學生信息   #在後台需要拿到學員的信息(名子)，才能刪除
    print(request.method)
    username = request.args.get('name')     #取出後端的值 看是否和前端要刪除的東西一樣 ，若一樣就刪除
    for stu in student:    
        if stu['name'] == username:     
               student.remove(stu)      #刪除student列表中的 那個和 前端傳過來要刪除的name 一樣的name #??不是只刪除name嗎?

    return redirect('/admin')   #重定向回admin

@app.route('/change',methods=['GET','POST'])
def change_student():       #修改學生信息
    #先顯示學員的數據，然後在瀏覽器修改，提交到服務器保存
    username = request.args.get('name')     #取出後端的值 

    if request.method == 'POST':        #如果請求方法為post 用變數去存回傳的值
        username = request.form.get('txtName')
        chinese = request.form.get('chinese')
        math = request.form.get('math')
        english = request.form.get('english')

        for stu in student:             #將列表裡的東西取出
            if stu['name'] == username:     #如果列表中的名子等於回傳的名子 就修改列表內的其他資料
                stu['chinese'] = chinese
                stu['math'] = math
                stu['english'] = english
        return redirect('/admin')   #重定向回admin

    for stu in student:    
        if stu['name'] == username:   
            #需要在頁面中渲染學生的成績數據
            return render_template('change.html',student=stu)       #把學員數據顯示到前端
    return redirect('/admin')   #重定向回admin
@app.route('/autoControl')
def autoControl():
    return render_template('autoControl.html')    #連結到autoControl.html

@app.route('/adjust',methods=['GET','POST']) 
def adjust():
    global AdjustPh
    if request.method == 'GET':
        print(request.method)   #表單傳送方法
        AdjustPh = request.values.get('numAdjustPh')    #要調整的ph
        AdjustTemp = request.values.get('numAdjustTemp')  #要調整的溫度
        AdjustRH = request.values.get('numAdjustRH')    #要調整的濕度
        
        print('ph要調整為:',AdjustPh)
        print('溫度要調整為:',AdjustTemp,'°C')
        print('濕度要調整為:',AdjustRH,'%')
        
        # return redirect('/autoControl')   #重定向回autoControl
    return render_template('adjust.html',AdjustPh=AdjustPh,AdjustTemp=AdjustTemp,AdjustRH=AdjustRH)    #連結到adjust.html



# run app
if __name__ == "__main__":      #如果以主程式運行
    # app.run(host='127.0.0.1', port=80)    #啟動伺服器
    app.run('127.0.0.1',debug=True) 