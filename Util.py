from datetime import datetime


def minutes_to_hhmmss(decimal_minutes):
    hours = int(decimal_minutes // 60)
    minutes = int(decimal_minutes % 60)
    seconds = int((decimal_minutes % 1) * 60)
    return '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)


def hhmmss_to_minutes(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))

    # 计算总分钟数
    total_minutes = hours * 60 + minutes + seconds / 60

    return total_minutes


def minutes_to_timestamp(decimal_minutes):
    hours = int((decimal_minutes % (24 * 60)) // 60)
    minutes = int(decimal_minutes % 60)
    seconds = int((decimal_minutes % 1) * 60)

    # 构建时间戳格式字符串，精确到秒
    timestamp = datetime(2024, 3, 1, hours, minutes, seconds).strftime('%Y-%m-%d %H:%M:%S')

    return timestamp


# 将时间戳字符串转换回分钟数
def timestamp_to_minutes(timestamp_str):
    timestamp_obj = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    total_seconds = (timestamp_obj - datetime(2024, 3, 1)).total_seconds()
    minutes = total_seconds / 60
    return minutes
