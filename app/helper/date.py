import datetime

def get_day_num(date):
    if not date or type(date)!=str:
        return
    date = date.split("-")
    year, month, day= [int(date[0]),int(date[1]),int(date[2])]
    day_num = datetime.date(year,month,day).weekday()
    return day_num