import requests
import datetime
import json
from openpyxl import Workbook, load_workbook

ACCESSTOKEN_GITHUB = "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"

SITEID = "2710924" #location
KEY = "1KP4K9CZOFOS9XZU3ZXHWM24RJTXCWAL"

def get_last_month():
    today = datetime.date.today()
    first = today.replace(day = 1)
    last_month = first - datetime.timedelta(days=1)
    last_month =  last_month.strftime("%m")
    return last_month

def get_timewindow(month):
    year = datetime.datetime.today().year
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
    startdate = f"{year}-{str(month)}-01" # year variable -> datetime object
    enddate = f"{year}-{str(month)}-04"    # any other day works as the unit is month anyway
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

    def __init__(self, SITEID, KEY, startdate, enddate, feedin_price_in_euro, consumption_price_in_euro):
        self.SITEID = SITEID
        self.KEY = KEY
        self.startdate = startdate
        self.enddate = enddate
        self.feedin_price_in_euro = feedin_price_in_euro
        self.consumption_price_in_euro = consumption_price_in_euro

    def get_feedin_with_unit_month(self):
        url_feedin = f"https://monitoringapi.solaredge.com/site/{self.SITEID}/energyDetails?meters=FEEDIN&timeUnit=MONTH&startTime={self.startdate}%2011:00:00&endTime={self.enddate}%2013:00:00&api_key={self.KEY}"
        feedin = requests.get(url_feedin)
        assert feedin.status_code == 200
        feedin = feedin.json()
        feedin_list = feedin['energyDetails']['meters']
        feedin = (feedin_list[0]['values'][0]['value']) / 1000 # from Wh to kWh
        feedin_money = feedin * float(self.feedin_price_in_euro)
        print(f"Einspeisung: {round(feedin, 2)} kWh")
        print(f"Einnahmen Einspeisung: {round(feedin_money, 2)} € netto")
        return feedin, self.feedin_price_in_euro, feedin_money

    def get_self_consumption_with_unit_month(self):
        url_self_consumption = f"https://monitoringapi.solaredge.com/site/{self.SITEID}/energyDetails?meters=SELFCONSUMPTION&timeUnit=MONTH&startTime={self.startdate}%2011:00:00&endTime={self.enddate}%2013:00:00&api_key={self.KEY}"
        self_consumption = requests.get(url_self_consumption)
        assert self_consumption.status_code == 200
        self_consumption = self_consumption.json()
        self_consumption_list = self_consumption['energyDetails']['meters']
        self_consumption = (self_consumption_list[0]['values'][0]['value']) / 1000
        print(f"Eigenverbrauch: {round(self_consumption, 2)} kWh")
        consumption_money = self_consumption * float(self.consumption_price_in_euro)
        print(f"Kosten Eigenverbrauch: {round(consumption_money, 2)} € netto")
        return self_consumption, self.consumption_price_in_euro, consumption_money
    
    def get_parameters_for_excel_file_with_unit_day(self):
        url_parameters = f"https://monitoringapi.solaredge.com/site/{self.SITEID}/energyDetails?meters=SELFCONSUMPTION,CONSUMPTION,PRODUCTION,FEEDIN,PURCHASED&timeUnit=DAY&startTime={self.startdate}%2011:00:00&endTime={self.enddate}%2013:00:00&api_key={self.KEY}"
        parameters = requests.get(url_parameters).json()
        values_production, values_consumption, values_purchased, values_feedin, values_self_consumption = [], [], [], [], []
        meters = parameters['energyDetails']['meters']
        for i in range(len(meters)):
            if meters[i]["type"] == "Production":
                values_production = [meters[i]["values"][day]["value"] for day in range(len(meters[i]["values"]))]
                continue
            if meters[i]["type"] == "Consumption":
                values_consumption = [meters[i]["values"][day]["value"] for day in range(len(meters[i]["values"]))]
                continue
            if meters[i]["type"] == "Purchased":
                values_purchased = [meters[i]["values"][day]["value"] for day in range(len(meters[i]["values"]))]
                continue
            if meters[i]["type"] == "FeedIn":
                values_feedin = [meters[i]["values"][day]["value"] for day in range(len(meters[i]["values"]))]
                continue
            if meters[i]["type"] == "SelfConsumption":
                values_self_consumption = [meters[i]["values"][day]["value"] for day in range(len(meters[i]["values"]))]
                continue
        # print(json.dumps(parameters, indent = 4))
        # create dataframe

def save_to_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "Chart Export"

def main():
    month = get_last_month()
    startdate, enddate = get_timewindow(month)
    feedin_price_in_euro, consumption_price_in_euro = get_parameters()
    accounting = apicalls(SITEID, KEY, startdate, enddate, feedin_price_in_euro, consumption_price_in_euro)
    # accounting.get_feedin_with_unit_month()
    # accounting.get_self_consumption_with_unit_month()
    accounting.get_parameters_for_excel_file_with_unit_day()
    return

main()