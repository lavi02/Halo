from datetime import datetime
import pytz

def time_builder_logger():
    korea_tz = pytz.timezone('Asia/Seoul')
    now = datetime.now()
    korea_time = now.astimezone(korea_tz)

    year = korea_time.year
    month = korea_time.month
    day = korea_time.day
    hour = korea_time.hour
    minute = korea_time.minute
    second = korea_time.second


    return f"{year}_{month}_{day}_{hour}_{minute}_{second}"