## Class which gets parameters from GUI and formats them into filter

import requests
from datetime import date
from model.DataFile import DataFile



class DataCollector:
    def __init__(self, gas, date, login, url, selectedSentinel, lat, long):
        self.gas = gas
        self.date = self.makeDate(date)
        self.user = login[0]
        self.passw = login[1]
        self.url = url
        self.selectedSentinel = selectedSentinel
        self.lat = float(lat)
        self.long = float(long)
        self.download()
        
        return

    def download(self):
        filterString = self.makeFilterString(self.gas, self.date)
        brojac = 0
        skip = 0
        while brojac != 1:
            
            req = requests.get(self.url, auth=(self.user, self.passw), params={'$format': 'json' , '$filter': filterString, '$skip': skip})
            print(req.status_code)
            js = req.json()
            #print(len(js['d']['results']))
            #print(js['d']['results'], file = open('ispis.txt', 'w'))
            res = js['d']['results']
            
            for i in range(len(res)):
                file = DataFile(res[i])
           
                if file.polygon.coordInsidePolygon(self.lat, self.long):
                    downloadLink = file.value
                    brojac += 1
                    print(file.id)
                    print(file.name)
                    print(file.polygon.polygonCoordinates)
                    print(str(file.size) + 'MB')
                    break
                    
                    #print(i, file = open('ispis.txt', 'w'))
                #print("Idem dalje..")
            skip += 50

        downloadreq = requests.get(downloadLink, auth = (self.user, self.passw))
        if self.selectedSentinel == 'S5P':
            fileType = '.nc'
        else:
            fileType = '.zip'
            
        if file.size > 200:
            print("Prevelik file")
        else:    
            with open(f"../downloaded_data/{file.name}{fileType}", "wb") as fout:
                print("Zapocinjem skidanje")
                fout.write(downloadreq.content)
                print("Skinuto!")
    
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

