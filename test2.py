
result = 2
ee=11

try:
    ee=10
    result = 10 / 0  # 除以零会引发 ZeroDivisionError 异常
    print(result)
except:
    print("除零错误发生:")

print(result)
print(ee)