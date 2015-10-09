import Tkinter
import tkMessageBox

class FileIO:
    global dataArray
    global paramArray
    global filNavn

    def __init__(self, filnavn ):
        self.filNavn = filnavn
        try:
            #Leser inn fila hvis den eksisterer
            configFile = open( str(filnavn) , 'r')
            pass
        except:
            #Oppretter filen hvis den mangler
            tkMessageBox.showinfo("Info","Opprettet ny fil med filnavn "+str(filnavn)+", fyll inn data")
            configFile = open( str(filnavn) , 'w')
            pass
        finally:
            #Leser inn parametre fra fil og legger i tabell(er)
            confDataLines = configFile.readlines()
            self.paramArray = [[] for i in range(len(confDataLines))]
            self.dataArray = [[[] for i in range(4)] for i in range(len(confDataLines))]
            for n in range(0 , len(confDataLines) ):
                strConfData = str( confDataLines[n] ).strip('[]')
                self.dataArray[n][:] = strConfData.split('\t')
                try:
                    if str(self.dataArray[n][2]) == "int":
                        #Behandler variabelen som en integer
                        self.paramArray[n] = int(str(self.dataArray[n][1]))
                    elif str(self.dataArray[n][2]) == "flt":
                        #Behandler variabelen som flyttall
                        self.paramArray[n] = float(str(self.dataArray[n][1]))
                    elif str(self.dataArray[n][2]) == "str":
                        #Behandler variabelen som en string
                        self.paramArray[n] = str(self.dataArray[n][1])
                    else:
                        tkMessageBox.showinfo("Info","Parameter type "+str(n)+" er ikke definert korrekt!")
                except:
                    tkMessageBox.showinfo("Info","Parameter "+str(n)+" er ikke definert korrekt")

           # print(self.dataArray)
            print(self.paramArray)
            configFile.close()
            pass
        pass

    def getParam( self, paramId ):
        return self.paramArray[ paramId ]
        pass

    def getParamName(self, paramId ):
        return str(self.dataArray[paramId][0])

    def settParam2(self, paramNavn, verdi):
        funnet = False
        for n in range(0 , len(self.paramArray) ):
            if str( self.dataArray[n][0]).find( paramNavn) == 0:
                self.settParam(n,verdi)
                funnet = True
                break
        if( funnet == False):
            tkMessageBox.showinfo("Info" , "Finner ikke "+str(paramNavn) + " i listen")
        return

    def settParam(self,paramId , verdi ):

        try:
            if str(self.dataArray[paramId][2]) == "int":
                #Behandler variabelen som en integer
                self.paramArray[paramId] = int(verdi)
                print( self.paramArray[paramId])
            elif str(self.dataArray[paramId][2]) == "flt":
                #Behandler variabelen som flyttall
                self.paramArray[paramId] = float(verdi)
                print(  self.paramArray[paramId])
            elif str(self.dataArray[paramId][2]) == "str":
                    #Behandler variabelen som en string
                    self.paramArray[paramId] = str(verdi)
                    print(self.paramArray[paramId])
            else:
                print("Fant ikke")
        except:
            tkMessageBox.showinfo("Info","Parameter "+str(paramId)+" ble ikke lagret korrekt")
            pass

    def saveConfig(self):

        for n in range(0 , len(self.paramArray) ):
            try:
                self.dataArray[n][1] = str(self.paramArray[n])
            except:
                tkMessageBox.showinfo("Info","Parameter: " + str(n) + " er ikke definert korrekt")
                print("Tull med element: ", n )

        file = open( self.filNavn , 'w+')

        for n in range(0 , len(self.dataArray) ):
            try:
                file.write(str(self.dataArray[n][0])+'\t'+str(self.dataArray[n][1])+'\t'+str(self.dataArray[n][2])+'\t'+str(self.dataArray[n][3]))
            except:
                tkMessageBox.showinfo("Info","Parameter: "+ str(n) + " er ikke definert korrekt")
                print("Tabellen har ikke korrekt antall elementer")

        file.close()
        self.loadConfig()
        pass

    def loadConfig(self):
        self.__init__(self.filNavn)
        pass



