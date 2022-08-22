import requests
import datetime as dt


siteid = "2710924" #location
key = "1KP4K9CZOFOS9XZU3ZXHWM24RJTXCWAL"
startdate="2022-06-01"
enddate="2022-06-30"

feedin_priceInCent = input("Bitte Cent pro kWh angeben - Einspeisung (default: 6.53): ") or 6.53

consumption_priceInCent = input("Bitte Cent pro kWh angeben - Eigenverbrauch (default: 25.99): ") or 25.99


#note: every time a new object of class api_calls is created, the information in the brackets is passed to the __init__ function - parameters have to be defined globally for python to put the into the init function

class apicalls:


    def __init__(self, siteid, key, startdate, enddate, feedin_priceInCent, consumption_priceInCent):
        self.siteid = siteid
        self.key = key
        self.startdate = startdate
        self.enddate = enddate
        self.feedin_priceInCent = feedin_priceInCent
        self.consumption_priceInCent = consumption_priceInCent

    def getdata(self):
        urldata = "https://monitoringapi.solaredge.com/site/" + self.siteid + "/energyDetails?meters=SELFCONSUMPTION,FEEDIN&timeUnit=MONTH&startTime=" + self.startdate + " 00:00:00&endTime=" + self.enddate + " 00:00:00&api_key=" + self.key #unit = MONTH, idea: import library to automatically switch to new month (with right number of days)
        data = requests.get(urldata)
        if data.status_code == 200:
            data = data.json()
            data_list = data['energyDetails']['meters']
            feedin = data_list[0]['values'][0]['value']
            consumption = data_list[1]['values'][0]['value'] #consumption = selfconsumption
            feedin_money = feedin/1000 * float(feedin_priceInCent)/100 #from Wh to kWh, from euro to ct
            consumption_money = consumption/1000 * float(consumption_priceInCent/100) 
            print("Deine Einnahmen durch die Einspeisung für den angegebenen Monat betragen: ", round(feedin_money,2), "€")
            print("Deine Kosten für den Eigenverbrauch für den angegebenen Monat betragen: ", round(consumption_money,2), "€")
            


testobject = apicalls(siteid,key,startdate,enddate,feedin_priceInCent, consumption_priceInCent)
testobject.getdata()



