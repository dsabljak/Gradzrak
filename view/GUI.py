##App for pulling Copernicus data from the Hub using parameters which the user
##puts. Currently working for Sentinel5P

from tkinter import *
from tkinter import ttk
from Gradzrak.model.DataCollector import DataCollector
from functools import partial

url1    = "https://s5phub.copernicus.eu/dhus/odata/v1/Products"
url2    = "https://scihub.copernicus.eu/apihub/odata/v1/Products"

s5pLogin = ("s5pguest", "s5pguest")
s123Login = ("dsabljak", "Jabuka!=42")
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
cx
gasList = ["CO2", "CO"]

s1productList = ["SLC", "GRD", "OCN"]

s2productList = ["S2MSI1C", "S2MSI2A", "S2MSI2Ap"]

s3productList = ["OL_1_EFR___", "OL_1_ERR___", "OL_2_LFR___", "OL_2_LRR___", "SR_1_SRA___", "SR_1_SRA_A_", "SR_1_SRA_BS", "SR_2_LAN___"
                 "SL_1_RBT___", "SL_2_LST___", "SY_2_SYN___", "SY_2_V10___", "SY_2_VG1___", "SY_2_VGP___"]

s5pproductList = ["L1B_IR_SIR", "L1B_IR_UVN", "L1B_RA_BD1", "L1B_RA_BD2", "L1B_RA_BD3", "L1B_RA_BD4", "L1B_RA_BD5", "L1B_RA_BD6", "L1B_RA_BD7",
                  "L1B_RA_BD8", "L2__AER_AI", "L2__CH4___", "L2__CLOUD_", "L2__CO____", "L2__HCHO__", "L2__NO2___", "L2__NP_BD3", "L2__NP_BD6",
                  "L2__NP_BD7", "L2__O3_TCL", "L2__O3____", "L2__SO2___"]

townList = ["Zagreb", "Split", "Osijek", "Rijeka"]


class App(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.R = root
        self.selectedSentinel = ''
        self.R.title("Graf")
        self.grid()
     
        self.makeGUI()

    
    def makeGUI(self):
        self.S1Button = Button(self.R, text = "Sentinel_1", command = partial(self.setForm, 'S1'))
        self.S1Button.grid(row = 0, column = 0)

        self.S2Button = Button(self.R, text = "Sentinel_2", command = partial(self.setForm, 'S2'))
        self.S2Button.grid(row = 0, column = 1)

        self.S3Button = Button(self.R, text = "Sentinel_3", command = partial(self.setForm, 'S3'))
        self.S3Button.grid(row = 1, column = 0)

        self.S5Button = Button(self.R, text = "Sentinel_5P", command = partial(self.setForm, 'S5P'))
        self.S5Button.grid(row = 1, column = 1)
        

        Label(text = "Select product").grid(row = 2, column = 0, columnspan = 5)

        self.product = StringVar()
        self.town = StringVar()
        self.date = StringVar(value = "dd.mm.yyyy")
        
        self.productCombobox = ttk.Combobox(self.R, textvariable = self.product, values = s5pproductList, state = "readonly")
        self.productCombobox.grid(row = 3, column = 0, columnspan = 5)
        self.product.set(s5pproductList[0])

        Label(text = "Select town").grid(row = 4, column = 0, columnspan = 5)

        self.townCombobox = ttk.Combobox(self.R, textvariable = self.town, values = townList, state = "readonly")
        self.townCombobox.grid(row = 5, column = 0, columnspan = 5)
        self.town.set(townList[0])

        Label(text = "Select date").grid(row = 6, column = 0, columnspan = 5)
        self.dateEntry = Entry(self.R, textvariable = self.date)
        self.dateEntry.grid(row = 7, column = 0, columnspan = 5)
        
        self.okayButton = Button(self.R, text = "Done", command = self.getData)
        self.okayButton.grid(row = 8, column = 0, columnspan = 5)

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
        self.productCombobox['values'] = s1productList
        self.product.set(s1productList[0])
        return

    def setS2(self):
        self.productCombobox['values'] = s2productList
        self.product.set(s2productList[0])
        return

    def setS3(self):
        self.productCombobox['values'] = s3productList
        self.product.set(s3productList[0])
        return

    def setS5P(self):
        self.productCombobox['values'] = s5pproductList
        self.product.set(s5pproductList[0])
        return
        
    def getData(self, e = None):
        if not self.checkDate():
            print("Wrong format")
            exit()

        print(self.product.get())
        if self.selectedSentinel in ['S1', 'S2', 'S3']:
            auth = s123Login
            url = url2
        else:
            auth = s5pLogin
            url = url1
            
        download = DataCollector(self.product.get(), self.town.get(), self.date.get(), auth, url)
        
        #print(self.town.get())>
        #print(self.date.get())
        return

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
        for i in day:
                if i not in numbers:
                    return False
                
        for j in month:
            if j not in numbers:
                return False
                
        for j in year:
            if j not in numbers:
                return False
            
        if int(month) > 12 or int(month) < 1:
            return False
        return True

    def postoji(self):
        return
    
root = Tk()
app = App(root)
root.mainloop()
