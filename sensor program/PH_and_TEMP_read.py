import time     #temp
from w1thermsensor import W1ThermSensor #temp
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus #創建 I2C 總線
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus #使用I2C總線創建ADC對象
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0 #在通道0上創建單端輸入
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1 #在通道0和1之間創建差分輸入
#chan = AnalogIn(ads, ADS.P0, ADS.P1)   #AnalogIn(模擬輸入) 接口用於讀取施加到模擬輸入引腳的電壓。

sensor = W1ThermSensor()    #temp





while True:
    print('PH raw',chan.value, 'PH v',chan.voltage,'ph',chan.voltage*-5.8887 + 21.677)
    temperature = sensor.get_temperature()  #temp
    print("The temperature is %s celsius" % temperature)    #temp
    time.sleep(1)