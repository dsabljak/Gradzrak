from tkinter import *
from tkinter import ttk

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
        self.label1 = Label(text = "Select gas").grid(row = 0, column = 0)

        self.gas = StringVar()
        self.town = StringVar()
        
        self.gasCombobox = ttk.Combobox(self.R, textvariable = self.gas, values = gasList, state = "readonly")
        self.gasCombobox.grid(row = 1, column = 0)
        self.gas.set(gasList[0])

        Label(text = "Select town").grid(row = 3, column = 0)

        self.townCombobox = ttk.Combobox(self.R, textvariable = self.town, values = townList, state = "readonly")
        self.townCombobox.grid(row = 4, column = 0)
        self.town.set(townList[0])

        self.okayButton = Button(self.R, text = "Done", command = self.getData)
        self.okayButton.grid(row = 5, column = 0)
        
        
    def getData(self, e = None):
        print(self.gas.get())
        print(self.town.get())
        return
root = Tk()
app = App(root)
