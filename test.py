import datetime


t1 = datetime.datetime(2000,1,1,0,0,0)
t2 = datetime.datetime(2300,1,1,0,0,0)
t3 = datetime.timedelta(0.5)
t4 = t3 * 0.1
print(max(t1, t2))
print(t3)
print(t4)
