import datetime
import time

str1 = '09:14:01'
str2 = '20:07:23'

str1list = str1.split(':')

date1 = time.strptime(str1, '%H:%M:%S')
date2 = time.strptime(str2, '%H:%M:%S')

datetime1 = datetime.time(date1.tm_hour, date1.tm_min, date1.tm_sec)
datetime2 = datetime.time(date2.tm_hour, date2.tm_min, date2.tm_sec)

print(datetime1.second)

if datetime1.second > 0:
    datetime1 = datetime.time(hour=date1.tm_hour, minute=date1.tm_min+1)
    print(datetime1)

# s = (timeSum + datetime.timedelta(seconds=datetime1.second)).time()
#
# timeList = []
# timeList[0] = 2
#
# print(datetime1)
# print(datetime2)
# print(timeList)



#combine_datetime2 = datetime.datetime.combine(datetime.date(1, 1, 1), date2)
#print(combine_datetime2)

# timeInWork = (combine_datetime2 - datetime.timedelta(hours=date1.tm_hour, minutes=date1.tm_min, seconds=date1.tm_sec)).time()
# print(timeInWork)
# datetime.timedelta()

#result = (time.mktime(date2) - time.mktime(date1))/60
#print(result)