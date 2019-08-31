## Class which gets parameters from GUI and formats them into filter

import requests
from datetime import date
from DataFile import DataFile
url    = "https://s5phub.copernicus.eu/dhus/odata/v1/Products"


class DataCollector:
    def __init__(self, gas, town, date, login):
        self.gas = gas
        self.coords = self.getCoordsFromTown(town)
        self.date = self.makeDate(date)
        self.user = login[0]
        self.passw = login[1]
        self.download()
        
        return

    def download(self):
        filterString = self.makeFilterString(self.gas, self.date)
        brojac = 0
        skip = 0
        while brojac != 1:
            
            req = requests.get(url, auth=(self.user, self.passw), params={'$format': 'json' , '$filter': filterString, '$skip': skip})
            print(req.status_code)
            js = req.json()
            #print(len(js['d']['results']))
            #print(js['d']['results'], file = open('ispis.txt', 'w'))
            res = js['d']['results']
            
            for i in range(len(res)):
                file = DataFile(res[i])
           
                if file.polygon.coordInsidePolygon(self.coords[0], self.coords[1]):
                    downloadLink = file.value
                    brojac += 1
                    print(file.id)
                    print(file.name)
                    print(file.polygon.polygonCoordinates)
                    break
                    
                    #print(i, file = open('ispis.txt', 'w'))
                #print("Idem dalje..")
            skip += 50
    
##        print(file.id)
##        print(file.name)
##        print(file.polygon.polygonCoordinates)
##        req = requests.get(url, auth=(user, passw), params={'$format': 'json' , '$filter': filterString, '$skip': 49})
##        print(req.status_code)
##        js = req.json()
##        print(len(js['d']['results']))
##        print(js['d']['results'][0], file = open('ispis2.txt', 'w'))
    
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
        
        return [45.815399, 15.966568]
