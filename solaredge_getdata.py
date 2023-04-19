import requests
import datetime
from openpyxl import Workbook, load_workbook

accesstoken_github = "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"

siteid = "2710924" #location
key = "1KP4K9CZOFOS9XZU3ZXHWM24RJTXCWAL"

def get_last_month():
    today = datetime.date.today()
    first = today.replace(day = 1)
    last_month = first - datetime.timedelta(days=1)
    last_month =  last_month.strftime("%m")
    return last_month

def get_timewindow(month):
    while True:
        month = input(f"Bitte gewüschten Monat angeben (default: letzter Monat - hier {month}): ") or month
        if month.isdigit():
            month = int(month)
            if 1 <= month <= 12:
                break
            else:
                print("You must enter a number from 1 - 12. ")
        else: 
            print("You must enter a number. ")
    startdate="2022-" + str(month) + "-01"
    enddate="2022-" + str(month) + "-20"    # any other day works as the unit is month anyway
    return startdate, enddate

def get_parameters():
    consumption_price_in_cent = input("Bitte Cent pro kWh angeben - Eigenverbrauch (default: 25.99): ")
    feedin_priceInCent = input("Bitte Cent pro kWh angeben - Einspeisung (default: 6.53): ")
    if type(consumption_price_in_cent) == str:
        if "," in consumption_price_in_cent: consumption_price_in_euro = (float(consumption_price_in_cent.replace(",", ".")))/100
        elif feedin_priceInCent == "": consumption_price_in_euro = 25.99 / 100
        else: consumption_price_in_euro = float(consumption_price_in_cent) / 100
    if type(feedin_priceInCent) == str:
        if "," in feedin_priceInCent: feedin_price_in_euro = (float(feedin_priceInCent.replace(",", ".")))/100
        elif feedin_priceInCent == "": feedin_price_in_euro = 6.53 / 100
        else: feedin_price_in_euro = float(feedin_priceInCent) / 100
    return feedin_price_in_euro, consumption_price_in_euro

# note: every time a new object of class api_calls is created, the information in the brackets is passed to the __init__ function - parameters have to be defined globally for python to put the into the init function
class apicalls:

    def __init__(self, siteid, key, startdate, enddate, feedin_price_in_euro, consumption_price_in_euro):
        self.siteid = siteid
        self.key = key
        self.startdate = startdate
        self.enddate = enddate
        self.feedin_price_in_euro = feedin_price_in_euro
        self.consumption_price_in_euro = consumption_price_in_euro

    def get_feedin(self):
        url_feedin = "https://monitoringapi.solaredge.com/site/" + self.siteid + "/energyDetails?meters=FEEDIN&timeUnit=MONTH&startTime=" + self.startdate + " 00:00:00&endTime=" + self.enddate + " 00:00:00&api_key=" + self.key #unit = MONTH, idea: import library to automatically switch to new month (with right number of days)
        feedin = requests.get(url_feedin)  
        assert feedin.status_code == 200
        feedin = feedin.json()
        feedin_list = feedin['energyDetails']['meters']
        feedin = (feedin_list[0]['values'][0]['value']) / 1000 # from Wh to kWh
        print(f"feedin: {feedin}")
        feedin_money = feedin * float(self.feedin_price_in_euro)
        print(f"feedin_money: {feedin_money}")
        print(f"Deine Einnahmen durch die Einspeisung für den abgelaufenen Monat betragen bei {round(self.feedin_price_in_euro * 100, 2)} ct/kWh {round(feedin_money, 2)} € netto")
        print(f"Du hast {round(feedin, 2)} kWh eingespeist!")

    def get_self_consumption(self):
        url_self_consumption = "https://monitoringapi.solaredge.com/site/" + self.siteid + "/energyDetails?meters=SELFCONSUMPTION&timeUnit=MONTH&startTime=" + self.startdate + " 00:00:00&endTime=" + self.enddate + " 00:00:00&api_key=" + self.key #unit = MONTH, idea: import library to automatically switch to new month (with right number of days)
        self_consumption = requests.get(url_self_consumption)
        print("status code:", self_consumption.status_code)
        assert self_consumption.status_code == 200
        self_consumption = self_consumption.json()
        # print(self_consumption)
        self_consumption_list = self_consumption['energyDetails']['meters']
        self_consumption = (self_consumption_list[0]['values'][0]['value']) / 1000 # consumption = self_consumption
        print(f"self_consumption: {self_consumption}")
        consumption_money = self_consumption * float(self.consumption_price_in_euro)
        print(f"consumption_money: {consumption_money}")
        print(f"Deine Kosten für den Eigenverbrauch für den abgelaufenen Monat betragen bei {round(self.consumption_price_in_euro*100, 2)} ct/kWh {round(consumption_money, 2)} € netto")
        print(f"Du hast {round(self_consumption, 2)} kWh selber verbraucht!")


def save_to_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Chart Export"

def main():
    month = get_last_month()
    startdate, enddate = get_timewindow(month)
    feedin_price_in_euro, consumption_price_in_euro = get_parameters()
    accounting = apicalls(siteid, key, startdate, enddate, feedin_price_in_euro, consumption_price_in_euro)
    self_consumption = accounting.get_self_consumption()
    # feedin = accounting.get_feedin()
    return self_consumption

main()