# 連接到 MySQL 資料庫
import mysql.connector  # 匯入 mysql.connector 套件
import matplotlib.pyplot as plt  # 匯入 Matplotlib 套件

# 建立 MySQL 連線
mydb = mysql.connector.connect(
    host = 'localhost',# 主機名稱，這裡是本地主機
    port = '3306',
    user = 'jonsoncc7',# 使用者名稱
    password = 'jonsoncC7',# 使用者密碼
    database = 'hydroponics')   #database要使用的資料庫

mycursor = mydb.cursor()  # 創建 MySQL 游標物件，用於執行 SQL 查詢

# 從 MySQL 中擷取資料到 Python 程式中
mycursor.execute("select time, ph from hydroponics;")  # 執行 SQL 查詢，選擇 hydroponics 表格中的 time 和 ph 欄位
result = mycursor.fetchall  # 擷取查詢結果

time = []  # 用來儲存time的清單
ph = []  # 用來儲存ph的清單

# 迭代處理查詢結果，將姓名和成績分別加入清單
for i in mycursor:
    time.append(i[0])  # 將姓名加入 Names 清單
    ph.append(i[1])  # 將成績加入 Marks 清單

# 輸出學生姓名和成績
print("Name of Students = ", time)  # 顯示學生姓名
print("Marks of Students = ", ph)  # 顯示學生成績

# 使用 Matplotlib 進行資料視覺化
# plt.bar(time, ph)  # 創建長條圖，擺放學生姓名和成績
# 繪製折線圖
plt.plot(time, ph, label='折線圖', marker='', linestyle='-', color='b')
plt.ylim(0, 14)  # 設定 Y 軸範圍
plt.xlabel("time")  # 設定 X 軸標籤
plt.ylabel("ph")  # 設定 Y 軸標籤
plt.title("ph table")  # 設定圖表標題
plt.show()  # 顯示圖表
