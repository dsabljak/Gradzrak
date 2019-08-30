from tkinter import *
from tkinter import ttk
from DataCollector import DataCollector

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
gasList = ["CO2", "CO"] 
townList = ["Zagreb", "Split", "Osijek", "Rijeka"]

class App(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.R = root
        self.R.title("Graf")
        self.grid()
        self.makeGUI()

    def makeGUI(self):
        Label(text = "Select gas").grid(row = 0, column = 0)

        self.gas = StringVar()
        self.town = StringVar()
        self.date = StringVar(value = "dd.mm.yyyy")
        
        self.gasCombobox = ttk.Combobox(self.R, textvariable = self.gas, values = gasList, state = "readonly")
        self.gasCombobox.grid(row = 1, column = 0)
        self.gas.set(gasList[1])

        Label(text = "Select town").grid(row = 3, column = 0)

        self.townCombobox = ttk.Combobox(self.R, textvariable = self.town, values = townList, state = "readonly")
        self.townCombobox.grid(row = 4, column = 0)
        self.town.set(townList[0])

        Label(text = "Select date").grid(row = 5, column = 0)
        self.dateEntry = Entry(self.R, textvariable = self.date)
        self.dateEntry.grid(row = 6, column = 0)
        
        self.okayButton = Button(self.R, text = "Done", command = self.getData)
        self.okayButton.grid(row = 7, column = 0)
        
        
    def getData(self, e = None):
        if not self.checkDate():
            print("Wrong format")
            exit()

        print(self.gas.get())
        download = DataCollector(self.gas.get(), self.town.get(), self.date.get())
        
        #print(self.town.get())
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
root = Tk()
app = App(root)
