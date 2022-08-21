import requests
import datetime as dt

class api_calls():

    siteid = "2710924" #location
    key = "1KP4K9CZOFOS9XZU3ZXHWM24RJTXCWAL"

    def getpowerflow(self, siteid = siteid, key = key):
        urlpowerflow = "https://monitoringapi.solaredge.com/site/" + siteid + "/currentPowerFlow?api_key=" + key
        pf = requests.get(urlpowerflow)
        if pf.status_code == 200:
            print(pf.json())


    def getconsumption(self, siteid = siteid, key = key, starttime="2022-06-01%2000:00:00", endtime="2022-06-30%2023:59:59"):
        urlconsumption = "https://monitoringapi.solaredge.com/site/" + siteid + "/energyDetails?meters=CONSUMPTION&timeUnit=MONTH&startTime=" + starttime + "&endTime=" + endtime + "&api_key=" + key #unit = MONTH, idea: import library to automatically switch to new month (with right number of days)
        consumption = requests.get(urlconsumption)
        print(consumption.status_code)
        if consumption.status_code == 200:
            print(consumption.json())




testobject = api_calls()
testobject.getconsumption()



