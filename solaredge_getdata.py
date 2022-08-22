import requests
import datetime as dt

siteid = "2710924" #location
key = "1KP4K9CZOFOS9XZU3ZXHWM24RJTXCWAL"
startdate="2022-06-01"
enddate="2022-06-30"

#note: every time a new object of class api_calls is created, the information in the brackets is passed to the __init__ function - parameters have to be defined globally for python to put the into the init function

class apicalls:
   
    def __init__(self, siteid, key, startdate, enddate):
        self.siteid = siteid
        self.key = key
        self.startdate = startdate
        self.enddate = enddate

    def getdata(self):
        urldata = "https://monitoringapi.solaredge.com/site/" + self.siteid + "/energyDetails?meters=CONSUMPTION,FEEDIN&timeUnit=MONTH&startTime=" + self.startdate + " 00:00:00&endTime=" + self.enddate + " 00:00:00&api_key=" + self.key #unit = MONTH, idea: import library to automatically switch to new month (with right number of days)
        data = requests.get(urldata)
        if data.status_code == 200:
            data = data.json()
            data_list = data['energyDetails']['meters']
            feedin = data_list[0]['values'][0]['value']
            data = data_list[1]['values'][0]['value']
            print(feedin,data)

testobject = apicalls(siteid,key,startdate,enddate)
testobject.getdata()



