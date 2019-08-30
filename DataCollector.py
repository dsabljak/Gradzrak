import requests
from datetime import date
url    = "https://s5phub.copernicus.eu/dhus/odata/v1/Products"
user    = "s5pguest"
passw = "s5pguest"

class DataCollector:
    def __init__(self, gas, town, date):
        self.gas = gas
        self.coords = self.getCoordsFromTown(town)
        self.date = self.makeDate(date)
        self.download()
        return

    def download(self):
        filterString = self.makeFilterString(self.gas, self.date)
        req = requests.get(url, auth=(user, passw), params={'$format': 'json' , '$filter': filterString})
        print(req.status_code)
        js = req.json()
        
        print(js, file = open('ispis.txt', 'w'))
    
    def makeFilterString(self, gas, date):
        print(gas)
        productName = f"substringof('{gas}', Name)"
        startDate = f"year(ContentDate/Start) eq {date.year} and month(ContentDate/Start) eq {date.month} and day(ContentDate/Start) eq {date.day}"
        endDate = f"year(ContentDate/Start) eq {date.year} and month(ContentDate/Start) eq {date.month} and day(ContentDate/Start) eq {date.day}"
        
        return f"{productName} and {startDate} and {endDate}"
    
    def makeDate(self, datetime):
        tempList = datetime.split('.')
        print("evo me")
        year = int(tempList[2])
        month = int(tempList[1])
        day = int(tempList[0])
        return date(year, month, day)

    def getCoordsFromTown(self, town):
        return
