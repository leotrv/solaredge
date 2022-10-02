import requests
import datetime



accesstoken_github = "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"

siteid = "2710924" #location
key = "1KP4K9CZOFOS9XZU3ZXHWM24RJTXCWAL"



def get_last_month():
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    last_month =  last_month.strftime("%m")

    return last_month


def get_timewindow(month):
    while True:
        month = input(f"Bitte gewüschten Monat angeben (default: letzter Monat - hier {month}): ") or month
        if month.isdigit():                 #check if string month is a number
            month = int(month)              #cant compare strings to integers
            if 1 <= month <= 12:
                break
            else:
                print("You must enter a number from 1 - 12. ")
        else: 
            print("You must enter a number. ")

    startdate="2022-" + str(month) + "-01"
    enddate="2022-" + str(month) + "-20"    #any other day works as the unit is month anyway
    
    return startdate, enddate


def get_parameters():
    consumption_priceInEuro = input("Bitte Cent pro kWh angeben - Eigenverbrauch (default: 25.99): ")
    feedin_priceInEuro = input("Bitte Cent pro kWh angeben - Einspeisung (default: 6.53): ")
    if type(consumption_priceInEuro) == str:
        if "," in consumption_priceInEuro: consumption_priceInEuro = (float(consumption_priceInEuro.replace(",",".")))/100
        elif feedin_priceInEuro == "": consumption_priceInEuro = 25.99/100
        else: consumption_priceInEuro = float(consumption_priceInEuro)/100
    if type(feedin_priceInEuro) == str:
        if "," in feedin_priceInEuro: feedin_priceInEuro = (float(feedin_priceInEuro.replace(",",".")))/100
        elif feedin_priceInEuro == "": feedin_priceInEuro = 6.53/100
        else: feedin_priceInEuro = float(feedin_priceInEuro)/100
    
    return feedin_priceInEuro, consumption_priceInEuro



#note: every time a new object of class api_calls is created, the information in the brackets is passed to the __init__ function - parameters have to be defined globally for python to put the into the init function
class apicalls:


    def __init__(self, siteid, key, startdate, enddate, feedin_priceInEuro, consumption_priceInEuro):
        self.siteid = siteid
        self.key = key
        self.startdate = startdate
        self.enddate = enddate
        self.feedin_priceInEuro = feedin_priceInEuro
        self.consumption_priceInEuro = consumption_priceInEuro


    def getfeedin(self):
        urlfeedin = "https://monitoringapi.solaredge.com/site/" + self.siteid + "/energyDetails?meters=FEEDIN&timeUnit=MONTH&startTime=" + self.startdate + " 00:00:00&endTime=" + self.enddate + " 00:00:00&api_key=" + self.key #unit = MONTH, idea: import library to automatically switch to new month (with right number of days)
        feedin = requests.get(urlfeedin)  
        if feedin.status_code == 200:
            feedin = feedin.json()
            feedin_list = feedin['energyDetails']['meters']
            feedin = (feedin_list[0]['values'][0]['value'])/1000 #from Wh to kWh 
            feedin_money = feedin * float(self.feedin_priceInEuro)
            print(f"Deine Einnahmen durch die Einspeisung für den abgelaufenen Monat betragen bei {round(self.feedin_priceInEuro*100,2)} ct/kWh: ", round(feedin_money,2), "€")
            print("Du hast ",round(feedin,2)," kWh eingespeist!")


    def getselfcon(self):
        urlselfcon = "https://monitoringapi.solaredge.com/site/" + self.siteid + "/energyDetails?meters=SELFCONSUMPTION&timeUnit=MONTH&startTime=" + self.startdate + " 00:00:00&endTime=" + self.enddate + " 00:00:00&api_key=" + self.key #unit = MONTH, idea: import library to automatically switch to new month (with right number of days)
        selfcon = requests.get(urlselfcon)
        if selfcon.status_code == 200:
            selfcon = selfcon.json()
            selfcon_list = selfcon['energyDetails']['meters']
            selfcon = (selfcon_list[0]['values'][0]['value'])/1000 #consumption = selfconsumption
            consumption_money = selfcon * float(self.consumption_priceInEuro)
            print(f"Deine Kosten für den Eigenverbrauch für den abgelaufenen Monat betragen bei {round(self.consumption_priceInEuro*100,2)} ct/kWh: ", round(consumption_money,2), "€")
            print("Du hast ",round(selfcon,2)," kWh selber verbraucht!")


def main():
    month = get_last_month()
    timewindow = get_timewindow(month)
    parameters = get_parameters()

    accounting = apicalls(siteid, key, timewindow[0], timewindow[1], parameters[0], parameters[1])
    accounting.getselfcon()
    accounting.getfeedin()
    return accounting

main()

