## Class which gets parameters from GUI and formats them into filter

import time
from zipfile import ZipFile

from netCDF4 import Dataset
import requests
from datetime import date
from model.DataFile import DataFile
from model.DataAnalizer import *
import os



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
                    print(str(file.size) + ' MB')
                    break
                    
                    #print(i, file = open('ispis.txt', 'w'))
                #print("Idem dalje..")
            skip += 50

        if self.selectedSentinel == 'S5P':
            fileType = '.nc'
        else:
            fileType = '.zip'

        if os.path.exists(f"/home/filip/git/Copernicus/Gradzrak/model/downloaded_data/{file.name}{fileType}") == True:
            print("File exists")

            if fileType == ".nc":
                rootgrp = Dataset(f"/home/filip/git/Copernicus/Gradzrak/model/downloaded_data/{file.name}{fileType}", "r")
                DataAnalizer(rootgrp)
            elif fileType == ".zip":
                with ZipFile(f"/home/filip/git/Copernicus/Gradzrak/model/downloaded_data/{file.name}{fileType}", "r") as zipObj:
                    print("unzipping")
                    zipObj.extractall("/home/filip/git/Copernicus/Gradzrak/model/downloaded_data")
                    print("unzipped")
            else:
                print("Not a supported file type")

        else:

            if file.size > 200:
                print("Prevelik file")
            else:
                print("Zapocinjem skidanje")
                initial = time.time()
                downloadreq = requests.get(downloadLink, auth = (self.user, self.passw))
                final = time.time() - initial
                print("Elapsed time: " + str(final) + " s")

                with open(f"/home/filip/git/Copernicus/Gradzrak/model/downloaded_data/{file.name}{fileType}", "wb") as fout:
                    fout.write(downloadreq.content)
                    print("Skinuto!")
                    if fileType == ".nc":
                        rootgrp = Dataset(f"/home/filip/git/Copernicus/Gradzrak/model/downloaded_data/{file.name}{fileType}", "r")
                        DataAnalizer(rootgrp)
                    elif fileType == ".zip":
                        with ZipFile(f"/home/filip/git/Copernicus/Gradzrak/model/downloaded_data/{file.name}{fileType}", "r") as zipObj:
                            print("unzipping")
                            zipObj.extractall("/home/filip/git/Copernicus/Gradzrak/model/downloaded_data")
                            print("unzipped")
                    else:
                        print("Not a supported file type")

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

