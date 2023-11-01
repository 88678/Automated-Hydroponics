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

app = Flask(__name__)
socketio = SocketIO(app)

# 创建MySQL连接
db = mysql.connector.connect(host='localhost', port='3306', user='jonsoncc7', password='jonsoncC7', database='hydroponics')
cursor = db.cursor()

@app.route('/')
def index2():
    return render_template('index2.html')

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
    # 将时间戳转换为ISO 8601日期时间格式
    iso_time = nowTime.isoformat()
    new_data = (iso_time, ph)

    # 定义SQL查询语句
    sql = "INSERT INTO hydroponics (time, ph) VALUES (%s, %s)"

    # 执行数据库查询
    cursor.execute(sql, new_data)
    db.commit()

    # 发送数据到客户端
    socketio.emit('sensor_data', {'time': nowTime.timestamp() * 1000, 'ph': ph})

@app.route('/data')
def get_latest_sensor_data():
    cursor.execute("SELECT time, ph FROM hydroponics ORDER BY time DESC LIMIT 1")
    result = cursor.fetchone()

    if result:
        time, ph = result
        return jsonify({'time': time, 'ph': ph})
    else:
        return jsonify({'error': 'No data available'})

if __name__ == '__main__':
    # 设置后台任务，每秒获取一次传感器数据
    scheduler.add_job(get_sensor_data, 'interval', seconds=3)
    socketio.run(app, host='0.0.0.0', port=5000)
