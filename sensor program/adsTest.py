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

print("{:>5}\t{:>5}".format('raw', 'v'))

while True:
    print("{:>5}\t{:>5.3f}".format(chan.value, chan.voltage))
    # format格式化文字 value:取出字典中的所有值
    print('ph',chan.voltage*-5.8887 + 21.677)
    time.sleep(0.5)