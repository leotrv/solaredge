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

    def getconsumption(self, siteid = siteid, key = key, startdate="2022-06-01", enddate="2022-06-30"):
        urlconsumption = "https://monitoringapi.solaredge.com/site/" + siteid + "/energyDetails?meters=CONSUMPTION,FEEDIN&timeUnit=MONTH&startTime=" + startdate + " 00:00:00&endTime=" + enddate + " 00:00:00&api_key=" + key #unit = MONTH, idea: import library to automatically switch to new month (with right number of days)
        consumption = requests.get(urlconsumption)
        #print(consumption.status_code)
        if consumption.status_code == 200:
            consumption = consumption.json()
            consumption_list = consumption['energyDetails']['meters']
            consumption = consumption_list[1]['values'][0]['value']
            print(consumption)
    
    def getfeedin(self, siteid = siteid, key = key, startdate="2022-06-01", enddate="2022-06-30"):
        urlfeed = 'https://monitoringapi.solaredge.com/site/' + siteid + '/energyDetails?meters=FEEDIN&timeUnit=MONTH&startTime=' + startdate + ' 00:00:00&endTime=' + enddate + ' 00:00:00&api_key=' + key
        feedin = requests.get(urlfeed)
        if feedin.status_code == 200:
            feedin = feedin.json()
            feedin_list = feedin['energyDetails']['meters']
            feedin = feedin_list[0]['values'][0]['value'] #FeedIn value in Wh for full month starting from startdate
            print(feedin)




testobject = api_calls()
testobject.getfeedin()
testobject.getconsumption()



