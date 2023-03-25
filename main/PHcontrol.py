'''
用多執行序 執行ph ec ph調整 感測器壞掉 ec過低line警報
'''
import RPi.GPIO as GPIO
import time

adjustPH = 6    #從後端傳來的 要調整的數值
nowph = 5   #從感測器測到的 現在的數值
ec = 2
range = 0.5


if nowph > adjustPH + range:
    #調ph時， 開啟酸馬達，並開啟水泵

if nowph < adjustPH - range:
    #調ph時， 開啟鹼馬達，並開啟水泵
    
    