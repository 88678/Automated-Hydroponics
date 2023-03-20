import RPi.GPIO as GPIO
import time

pinRelay = 21#繼電器訊號腳
#pinBn = 7 #微動開關接腳
GPIO.setmode(GPIO.BCM)#将GPIO模式设置为BCM，这是指定树莓派GPIO引脚的两种模式之一（另一种是BOARD模式）。
GPIO.setup(pinRelay, GPIO.OUT) #gpio21輸出
#GPIO.setup(pinBn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        GPIO.output(pinRelay, 1)
        time.sleep(1)
#         GPIO.output(pinRelay, 0)
#         time.sleep(1)
        
except:
    pass
GPIO.cleanup()
