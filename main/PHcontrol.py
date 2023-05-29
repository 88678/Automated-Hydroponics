'''
用多執行序 執行ph ec ph調整 感測器壞掉 ec過高line警報
!!之後必須注意繼電器是高電壓開還是低電壓開
'''
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

adjustPH = 6    #從後端傳來的 要調整的數值
nowph = 5   #從感測器測到的 現在的數值
ec = 2
range = 0.5

acid = 18    #gpio18 為酸馬達的繼電器控制
alkali = 23     #gpio23 為鹼馬達的繼電器控制

GPIO.setup(acid, GPIO.OUT)  #將18和23腳位設為輸入?模式
GPIO.setup(alkali, GPIO.OUT)
while True:
    if nowph > (adjustPH + range):    #調ph時， 開啟酸馬達，並開啟水泵
        GPIO.output(acid,GPIO.HIGH) #控制繼電器高電位
        time.sleep(10)   #持續10秒
        GPIO.output(acid, GPIO.LOW) #控制繼電器低電位
        time.sleep(900)  #持續15分鐘

    elif nowph < (adjustPH - range):    #調ph時， 開啟鹼馬達，並開啟水泵
        GPIO.output(alkali,GPIO.HIGH)   
        time.sleep(10)   #持續10秒
        GPIO.output(alkali, GPIO.LOW)
        time.sleep(900)  #持續15分鐘
    
        
    
    