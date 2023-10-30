from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import plotly
from plotly.graph_objs import Scatter
import json
import time

app = Flask(__name__)
socketio = SocketIO(app)

def get_database_data():
    # 这是一个模拟的数据库数据，格式为 (时间, pH) 的元组列表
    data = [
        (time.strftime("%H:%M:%S"), 7.0),
        (time.strftime("%H:%M:%S"), 7.2),
        (time.strftime("%H:%M:%S"), 7.5),
        # 添加更多数据
    ]
    return data


@app.route('/')
def index():
    data = get_database_data()  # 从数据库获取数据
    x_values = [entry[0] for entry in data]
    y_values = [entry[1] for entry in data]

    plotly_data = [Scatter(x=x_values, y=y_values, mode='lines+markers', name='pH Data')]
    layout = {'title': 'Real-Time pH Chart'}

    # 使用 .to_plotly_json() 将 Plotly 数据转换为 JSON 可序列化的格式
    plotly_data_json = [data.to_plotly_json() for data in plotly_data]

    return render_template('index.html', plotly_data=json.dumps(plotly_data_json), layout=json.dumps(layout))

@socketio.on('update_chart')
def handle_update():
    data = get_database_data()  # 从数据库获取最新数据
    x_values = [entry[0] for entry in data]
    y_values = [entry[1] for entry in data]

    updated_data = [Scatter(x=x_values, y=y_values, mode='lines+markers', name='pH Data')]
    emit('chart_updated', json.dumps(updated_data))

# run app
if __name__ == "__main__":      #如果以主程式運行
    # app.run(host='127.0.0.1', port=80)    #啟動伺服器
    app.run('127.0.0.1',debug=True) 

