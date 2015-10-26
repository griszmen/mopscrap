import requests
import json
import time
import datetime

#config
login_page = 'https://helios.krakow.comarch/app/Mop2/Account/Index?ReturnUrl=%2fapp%2fMop2%2f'

# starting session
s = requests.Session()

# for django page
#test = s.get(link)
#csrftoken = s.cookies['csrftoken']

#credentials
payload = {'action': '/app/Mop2/Account/Index?ReturnUrl=%2fapp%2fMop2%2f', 'Login': 'WATROBAG', 'password': 'Tonymontana!3'}

req = s.post(login_page, data=payload, verify=False)

#getting user details
req_user_details = s.post('https://helios.krakow.comarch/app/Mop2/Home/GetLoggedEmployee')
json_data = json.loads(req_user_details.text)

user_name = json_data['fullName']
user_id = json_data['id']
companyId = json_data['companyId']

print(req_user_details.text)
print(user_name)
print(user_id)
print(companyId)

#get current report

report_page = "https://helios.krakow.comarch/app/Mop2/Reports/GetEmployeeReport?companyId=%s&month=%s&userId=%s&year=2015" % (companyId, '10', user_id)
print(report_page)
resp = s.get(report_page)

resp_json = json.loads(resp.text)

timeList = []

for day in resp_json:
    if day['IsWorkingDay'] == 1 and day['IsHoliday'] == 0:
        if day['InTime'] != '00:00:00':

            inTime = time.strptime(day['InTime'], '%H:%M:%S')
            outTime = time.strptime(day['OutTime'], '%H:%M:%S')
            combineOutTime = datetime.datetime.combine(datetime.date(1, 1, 1), datetime.time(outTime.tm_hour, outTime.tm_min, outTime.tm_sec))
            timeInWork = (combineOutTime - datetime.timedelta(hours=inTime.tm_hour, minutes=inTime.tm_min, seconds=inTime.tm_sec)).time()
            if timeInWork.second > 0:
                timeInWork = datetime.time(hour=timeInWork.hour, minute=timeInWork.minute+1)
                timeList.append(timeInWork)
            else:
                timeList.append(timeInWork)

totalSecs = 0
for times in timeList:
    totalSecs += (times.hour * 60 + times.minute) * 60 + times.second

days = len(timeList)

totalSecsNew, sec = divmod(totalSecs, 60)
hr, min = divmod(totalSecsNew, 60)
print("Time in company in %i working days: %d:%02d:%02d" % (days, hr, min, sec))

shouldBeDay = 8.5*60*60
timeCalc = (len(timeList)*shouldBeDay) - totalSecs

if timeCalc <= 0:
    timeCalc = timeCalc*(-1)
    timeCalcNew, timeCalcSec = divmod(timeCalc, 60)
    timeCalcH, timeCalcMin = divmod(timeCalcNew, 60)
    print("You have: %d:%d:%d overtime" % (timeCalcH, timeCalcMin, timeCalcSec))
else:
    timeCalcNew, timeCalcSec = divmod(timeCalc, 60)
    timeCalcH, timeCalcMin = divmod(timeCalcNew, 60)
    print("You have: %d:%d:%d under the limit" % (timeCalcH, timeCalcMin, timeCalcSec))


#print(resp.status_code)
#print(resp.url)
#print(resp.text)
