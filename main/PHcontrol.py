'''
用多執行序 執行ph ec ph調整 感測器壞掉 ec過低line警報
'''
adjustPH = 6    #從後端傳來的 要調整的數值
nowph = 5   #從感測器測到的 現在的數值
ec = 2
range = 0.5


if nowph > adjustPH + range:
    #開啟酸馬達

if nowph < adjustPH - range:
    #開啟鹼馬達
    