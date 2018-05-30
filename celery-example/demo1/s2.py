# 立即执行任务
"""
# result = xxxxxx.delay(4, 4)
# print(result.id)
"""


# 定时任务
"""
import datetime
# 当前本地时间
# ctime = datetime.datetime.now()
# print(ctime)
#
ctime = datetime.datetime(year=2019,month=5,day=19,hour=18,minute=55)
# 把当前本地时间转换成UTC时间
utc_ctime = datetime.datetime.utcfromtimestamp(ctime.timestamp())

# s10 = datetime.timedelta(seconds=10)
# ctime_x = utc_ctime + s10

# 使用apply_async并设定时间
result = xxxxxx.apply_async(args=[99, 3], eta=utc_ctime)
print(result)
"""
