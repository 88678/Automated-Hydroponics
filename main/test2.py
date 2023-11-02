from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import mysql.connector
import time
import busio
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

# 创建一个后台任务调度器
scheduler = BackgroundScheduler()
scheduler.start()

# 创建Flask应用和SocketIO对象
app = Flask(__name__)
socketio = SocketIO(app)

# 创建MySQL数据库连接和游标
db = mysql.connector.connect(host='localhost', port='3306', user='jonsoncc7', password='jonsoncC7', database='hydroponics')
cursor = db.cursor()

#创建一个根路径路由，渲染HTML模板
@app.route('/')
def index2():
    return render_template('index2.html')

#处理SocketIO连接和断开连接的事件
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# 获取传感器数据的函数
def get_sensor_data():
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    chan = AnalogIn(ads, ADS.P0)

    ph = chan.voltage * -5.8887 + 21.677

    nowTime = datetime.now()  # 获取当前日期时间
    iso_time = nowTime.isoformat()  # 将时间戳转换为ISO 8601日期时间格式
    new_data = (iso_time, ph)

    # 定义SQL查询语句
    sql = "INSERT INTO hydroponics (time, ph) VALUES (%s, %s)"

    # 执行数据库查询
    cursor.execute(sql, new_data)
    db.commit()

    # 发送数据到客户端
    socketio.emit('sensor_data', {'time': nowTime.timestamp() * 1000, 'ph': ph})

#这个路由查询数据库以获取最新的pH数据，并将其作为JSON数据返回给客户端。
@app.route('/data')
def get_latest_sensor_data():
    #执行了一个SQL查询，从名为 hydroponics 的数据库表中选择最新的时间戳和pH值，按时间降序排序，然后限制结果只返回一行数据（即最新的数据）。
    cursor.execute("SELECT time, ph FROM hydroponics ORDER BY time DESC LIMIT 1")
    #获取SQL查询的结果，将其存储在 result 变量中。cursor.fetchone() 用于获取查询结果的下一行数据。
    result = cursor.fetchone()

    #检查是否查询结果非空（即是否有最新的数据）。如果有数据，进入条件块。
    if result:
        time, ph = result
        # 如果有最新数据，这行代码创建一个JSON响应，其中包含时间戳和pH值，并将其返回给客户端。
        return jsonify({'time': time, 'ph': ph})
    else:
        return jsonify({'error': 'No data available'})

if __name__ == '__main__':
    # 设置后台任务，每秒获取一次传感器数据
    scheduler.add_job(get_sensor_data, 'interval', seconds=3)
    socketio.run(app, host='127.0.0.1', port=5000)
