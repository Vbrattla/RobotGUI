import fil_IO
from Tkinter import *

class ConfGui():
    global params

    def __init__(self, maingui,confData):
        self.master = maingui
        self.params = confData
        self.tblEntries = {}

        for n in range(0 , len(confData.dataArray) ):
            self.label = Label( self.master, text= confData.getParamName( n ) )
            self.label.grid( row = n, column = 1)
            self.boxVar = Entry(self.master, bd =5 )
            self.boxVar.grid(row = n, column = 3)
            self.boxVar.insert(1,str(confData.getParam(n)) )
            self.tblEntries[n] = self.boxVar

        self.btnSave = Button(self.master, text = "Lagre data", command = self.LagreData )
        self.btnSave.grid(row = (len(confData.dataArray)+1), column = 2,padx = 5, pady = 20 )
        self.btnQuit = Button(self.master, text = "Avslutt", command = self.Avslutt )
        self.btnQuit.grid(row = (len(confData.dataArray)+1), column = 3,padx = 5, pady = 20 )
        return

    def Avslutt(self):
        self.master.destroy()
        return

    def LagreData(self):

        for n in range(0 , len( self.params.dataArray) ):
            self.params.settParam(n, self.tblEntries[n].get() )
            #print("ConfGui: " + self.tblEntries[n].get() )

        self.params.saveConfig()
        return


