import requests
import json
import time
import datetime
from tkinter import *

#rewrite to classes

def calculate_hours(cr1, cr2):
    #config
    login_page = 'https://helios.krakow.comarch/app/Mop2/Account/Index?ReturnUrl=%2fapp%2fMop2%2f'

    # starting session
    s = requests.Session()

    # for django page
    #test = s.get(link)
    #csrftoken = s.cookies['csrftoken']

    #credentials
    payload = {'action': '/app/Mop2/Account/Index?ReturnUrl=%2fapp%2fMop2%2f', 'Login': '%s' % cr1, 'password': '%s' % cr2}

    req = s.post(login_page, data=payload, verify=False)

    #getting user details
    req_user_details = s.post('https://helios.krakow.comarch/app/Mop2/Home/GetLoggedEmployee')
    json_data = json.loads(req_user_details.text)

    user_name = json_data['fullName']
    user_id = json_data['id']
    companyId = json_data['companyId']
    now_month = datetime.datetime.now().month
    now_year = datetime.datetime.now().year

    #get current report

    report_page = "https://helios.krakow.comarch/app/Mop2/Reports/GetEmployeeReport?companyId=%s&month=%s&userId=%s&year=%s" % (companyId, now_month, user_id, now_year)
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
    all_text = "Welcome %s \n" % user_name
    all_text += "Total time in company - %i working days: %d:%02d:%02d\n" % (days, hr, min, sec)

    shouldBeDay = 8.5*60*60
    timeCalc = (len(timeList)*shouldBeDay) - totalSecs

    if timeCalc <= 0:
        timeCalc = timeCalc*(-1)
        timeCalcNew, timeCalcSec = divmod(timeCalc, 60)
        timeCalcH, timeCalcMin = divmod(timeCalcNew, 60)
        all_text += "You have: %d hours %d minutes overtime. Good stuff!\n" % (timeCalcH, timeCalcMin)
    else:
        timeCalcNew, timeCalcSec = divmod(timeCalc, 60)
        timeCalcH, timeCalcMin = divmod(timeCalcNew, 60)
        all_text += "You have: %d hours %d minutes under the limit. What a pity...:(\n" % (timeCalcH, timeCalcMin)

    return all_text

root = Tk()
root.title("MOP Reporter")


frame_left = Frame(root)
frame_right = Frame(root)

logo = PhotoImage(file="logo.png")
label_logo = Label(root, image=logo, bg="blue")
label_name = Label(frame_left, text="Login: ")
label_pass = Label(frame_left, text="Password: ")
entry_name = Entry(frame_left, width=20)
entry_pass = Entry(frame_left, width=20, show="*")
text_field = Text(frame_right)


def insert_text():
    e1 = entry_name.get()
    e2 = entry_pass.get()
    text = calculate_hours(e1, e2)
    text_field.insert(INSERT, text)

report_button = Button(frame_left, text="Generate Report", command=insert_text)

label_logo.pack(fill=X)

frame_left.pack(side=LEFT)

label_name.grid(row=0)
entry_name.grid(row=0, column=1)
label_pass.grid(row=1)
entry_pass.grid(row=1, column=1)
report_button.grid(columnspan=2)

frame_right.pack(side=RIGHT)
text_field.grid(row=0)

root.mainloop()