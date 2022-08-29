import requests
import datetime


siteid = "2710924" #location
key = "1KP4K9CZOFOS9XZU3ZXHWM24RJTXCWAL"


today = datetime.date.today()
first = today.replace(day=1)
last_month = first - datetime.timedelta(days=1)
month =  last_month.strftime("%m")


consumption_priceInEuro = input("Bitte Cent pro kWh angeben - Eigenverbrauch (default: 25.99): ")
feedin_priceInEuro = input("Bitte Cent pro kWh angeben - Einspeisung (default: 6.53): ")
consumption_priceInEuro = (float(consumption_priceInEuro.replace(",",".")) if type(consumption_priceInEuro) == str and "," in consumption_priceInEuro else 25.99)/100
feedin_priceInEuro = (float(feedin_priceInEuro.replace(",",".")) if type(feedin_priceInEuro) == str and "," in feedin_priceInEuro else 6.53)/100


month = input("Bitte gewüschten Monat angeben (default: letzter Monat): ") or month
startdate="2022-" + str(month) + "-01"
enddate="2022-" + str(month) + "-20" #any other day works as the unit is month anyway


#note: every time a new object of class api_calls is created, the information in the brackets is passed to the __init__ function - parameters have to be defined globally for python to put the into the init function

class apicalls:

    def __init__(self, siteid, key, startdate, enddate, feedin_priceInEuro, consumption_priceInEuro):
        self.siteid = siteid
        self.key = key
        self.startdate = startdate
        self.enddate = enddate
        self.feedin_priceInCent = feedin_priceInEuro
        self.consumption_priceInCent = consumption_priceInEuro


    def getfeedin(self):
        urlfeedin = "https://monitoringapi.solaredge.com/site/" + self.siteid + "/energyDetails?meters=FEEDIN&timeUnit=MONTH&startTime=" + self.startdate + " 00:00:00&endTime=" + self.enddate + " 00:00:00&api_key=" + self.key #unit = MONTH, idea: import library to automatically switch to new month (with right number of days)
        feedin = requests.get(urlfeedin)  
        if feedin.status_code == 200:
            feedin = feedin.json()
            feedin_list = feedin['energyDetails']['meters']
            feedin = (feedin_list[0]['values'][0]['value'])/1000 #from Wh to kWh 
            feedin_money = feedin * float(feedin_priceInEuro) #from euro to ct
            print("Deine Einnahmen durch die Einspeisung für den abgelaufenen Monat betragen: ", round(feedin_money,2), "€")
            print("Du hast ",round(feedin,2)," kWh eingespeist!")

    def getselfcon(self):
        urlselfcon = "https://monitoringapi.solaredge.com/site/" + self.siteid + "/energyDetails?meters=SELFCONSUMPTION&timeUnit=MONTH&startTime=" + self.startdate + " 00:00:00&endTime=" + self.enddate + " 00:00:00&api_key=" + self.key #unit = MONTH, idea: import library to automatically switch to new month (with right number of days)
        selfcon = requests.get(urlselfcon)
        if selfcon.status_code == 200:
            selfcon = selfcon.json()
            selfcon_list = selfcon['energyDetails']['meters']
            selfcon = (selfcon_list[0]['values'][0]['value'])/1000 #consumption = selfconsumption
            consumption_money = selfcon * float(consumption_priceInEuro)
            print("Deine Kosten für den Eigenverbrauch für den abgelaufenen Monat betragen: ", round(consumption_money,2), "€")
            print("Du hast ",round(selfcon,2)," kWh selber verbraucht!")



accounting = apicalls(siteid,key,startdate,enddate,feedin_priceInEuro, consumption_priceInEuro)
accounting.getselfcon()
accounting.getfeedin()



