import datetime


values = [0]
values[0] = "06/26/2024 00:00:00 AM"
def datetime_str(string:str):
    date,time = string.split(" ")
    month,day,year = date.split("/")
    hour,minute,second = time.split(":")
    month = int(month)
    day = int(day)
    year = int(year) 
    hour = int(hour)
    minute = int(minute)
    second = int(second)

    t = datetime.datetime(day=day,month=month,year=year,hour=hour,minute=minute,second=second)
    return t