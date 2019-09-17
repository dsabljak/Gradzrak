##App for pulling Copernicus data from the Hub using parameters which the user
##puts. 
import threading
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Gradzrak.model.DataCollector import DataCollector
from functools import partial
from Gradzrak.model.Constants import Constants


class App(Frame):
    
    def __init__(self, root):
        super().__init__(root)
        self.R = root
        self.selectedSentinel = 'S1'
        self.selectedLocationOption = 'town'
        self.R.title("Graf")
        self.grid()
        self.makeGUI()

    
    def makeGUI(self):
        Label(text = 'Choose Sentinel').grid(row = 0, column = 0, columnspan = 5)
        
        self.S1Button = Button(self.R, text = "Sentinel_1", command = partial(self.setForm, 'S1'))
        self.S1Button.grid(row = 1, column = 0)

        self.S2Button = Button(self.R, text = "Sentinel_2", command = partial(self.setForm, 'S2'))
        self.S2Button.grid(row = 1, column = 1)

        self.S3Button = Button(self.R, text = "Sentinel_3", command = partial(self.setForm, 'S3'))
        self.S3Button.grid(row = 2, column = 0)

        self.S5Button = Button(self.R, text = "Sentinel_5P", command = partial(self.setForm, 'S5P'))
        self.S5Button.grid(row = 2, column = 1)
        

        Label(text = "Select product").grid(row = 3, column = 0, columnspan = 5)

        self.product = StringVar()
        self.town = StringVar()
        self.date = StringVar(value = "dd.mm.yyyy")
        self.lat = StringVar()
        self.long = StringVar()
        
        self.productCombobox = ttk.Combobox(self.R, textvariable = self.product, values = Constants.s1productList, state = "readonly")
        self.productCombobox.grid(row = 4, column = 0, columnspan = 5)
        self.product.set(Constants.s1productList[0])

        Label(text = "Choose town or coordinate entry").grid(row = 5, column = 0, columnspan = 5)
        self.coordButton = Button(self.R, text = "Coordinate", command = partial(self.setLocationOption, 'entry'))
        self.coordButton.grid(row = 6, column = 0)

        self.townButton = Button(self.R, text = "Town", command = partial(self.setLocationOption, 'town'))
        self.townButton.grid(row = 6, column = 1)
        
        Label(text = "Select town").grid(row = 7, column = 0, columnspan = 5)

        self.townCombobox = ttk.Combobox(self.R, textvariable = self.town, values = Constants.townList, state = "readonly")
        self.townCombobox.grid(row = 8, column = 0, columnspan = 5)
        self.town.set(Constants.townList[0])

        Label(text = "Select date").grid(row = 9, column = 0, columnspan = 5)
        self.dateEntry = Entry(self.R, textvariable = self.date)
        self.dateEntry.grid(row = 10, column = 0, columnspan = 5)

        Label(text = "Select latitude and longitude").grid(row = 11, column = 0, columnspan = 5)
        
        self.latEntry = Entry(self.R, textvariable = self.lat, state = 'disabled')
        self.latEntry.grid(row = 12, column = 0)

        self.longEntry = Entry(self.R, textvariable = self.long, state = 'disabled')
        self.longEntry.grid(row = 12, column = 1)
        
        self.okayButton = Button(self.R, text = "Done", command = partial(self.createThread, ''))
        self.okayButton.grid(row = 13, column = 0, columnspan = 5)

    def createThread(self, e):
        newThread = threading.Thread(target = self.getData)
        newThread.start()
        return
    
    def setLocationOption(self, e):
        self.selectedLocationOption = e
        
        if e == 'entry':
            self.townCombobox['state'] = 'disabled'
            self.latEntry['state'] = 'normal'
            self.longEntry['state'] = 'normal'
        else:
            self.townCombobox['state'] = 'normal'
            self.latEntry['state'] = 'disabled'
            self.longEntry['state'] = 'disabled'
        
        return
    
    def setForm(self, e):
        self.selectedSentinel = e
        
        if e == 'S1':
            self.setS1()
        elif e == 'S2':
            self.setS2()
        elif e == 'S3':
            self.setS3()
        else:
            self.setS5P()
            
        return

    def setS1(self):
        self.productCombobox['values'] = Constants.s1productList
        self.product.set(Constants.s1productList[0])
        
        return

    def setS2(self):
        self.productCombobox['values'] = Constants.s2productList
        self.product.set(Constants.s2productList[0])
        
        return

    def setS3(self):
        self.productCombobox['values'] = Constants.s3productList
        self.product.set(Constants.s3productList[0])
        
        return

    def setS5P(self):
        self.productCombobox['values'] = Constants.s5pproductList
        self.product.set(Constants.s5pproductList[0])
        
        return
        
    def getData(self, e = None):
        if not self.checkDate():
            messagebox.showinfo("Error", "Date format must be dd.mm.yyyy \nMonth must be between 1 and 12")
            print("Wrong format")
        
            return

        print(self.product.get())
        if self.selectedSentinel in ['S1', 'S2', 'S3']:
            auth = Constants.s123Login
            url = Constants.url2
        else:
            auth = Constants.s5pLogin
            url = Constants.url1
            
        try:
            lat, long = self.getLocation()
        except:
            return

        print(lat, long)
        download = DataCollector(self.product.get(), self.date.get(), auth, url, self.selectedSentinel, lat, long)
        
        return
    
    def checkLocation(self, lat, long):
        if lat == '' or long == '':
            print("slovo il prazno a minus")
            return False
        if lat[0] == '-' :
            if not(lat[1::].isdigit()) or not(long.isdigit()):
                print("slovo il prazno a minus")
                return False
            
        elif long[0] == '-' :
            if not(lat.isdigit()) or not(long[1::].isdigit()):
                print("slovo il prazno a minus")
                return False
            
        elif not(lat.isdigit()) or not(long.isdigit()):
                print("slovo il prazno")
                return False
            
        if lat == None or long == None:
            print(None)
            return False
        
        lat = float(lat)
        long = float(long)
        if long <= -180 or long >= 180:
            print("Long cudan")
            return False
        
        if lat <= -90 or lat >= 90:
            print("Lat cudan")
            return False
        
        return True
        
    def getLocation(self):
        if self.selectedLocationOption  == 'entry':
            if not self.checkLocation(self.lat.get(), self.long.get()):
                messagebox.showinfo("Error", "Latitude must be between -90 and 90.\n Longitude must be between -180 and 180.\n Both must be float or integer. ")
                print("Wrong format")
            else:
                return float(self.lat.get()), float(self.long.get())
        else:
            return Constants.townCoords[self.town.get()][0], Constants.townCoords[self.town.get()][1]

    def checkDate(self):
        date = self.date.get()
        
        if date[2] != '.' or date[5] != '.':
            return False
        
        if len(date) != 10:
            return False
        
        date = date.split('.')
        print(date)
        day = date[0]
        month = date[1]
        year = date[2]

        if len(day) != 2 or len(month) != 2 or len(year) != 4:
            return false
        
        if not day.isdigit() or not month.isdigit() or not year.isdigit():
                    return False
            
        if int(month) > 12 or int(month) < 1:
            return False
        
        return True


    
root = Tk()
app = App(root)
root.mainloop()
