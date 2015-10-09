from Tkinter import *
from PIL import Image, ImageTk
from confGui import ConfGui
import trenBilder
import tkMessageBox
from trenBilder import ProgressBar
import time

class Gui():
    global running
    global CaptureVideo

    def __init__(self, mainGui, param, hogdb):
        self.master = mainGui
        self.running = True
        self.CaptureVideo = False
        self.konfigParam = param
        self.HoGDatabase = hogdb

        # Definerer knapper
        #self.knapp1 = Button(self.master, text="Toggle Video", command=self.ToggleVideoStream)
        #self.knapp1.config(height=4, width=20)
        #self.knapp1.grid(row=7, column=6, padx=2, pady=10, sticky=W)

        self.knapp1 = Button(self.master, text="Knapp3", bg="grey", command=self.KnappeTest1)
        self.knapp1.config(height=4, width=20)
        self.knapp1.grid(row=7, column=3, padx=2, pady=10, sticky=W)

        self.knapp2 = Button(self.master, text="Knapp2", bg="grey", command=self.KnappeTest2)
        self.knapp2.config(height=4, width=20)
        self.knapp2.grid(row=7, column=5, padx=2, pady=10, sticky=W)

        self.knapp3 = Button(self.master, text="Knapp3", bg="grey", command=self.KnappeTest3)
        self.knapp3.config(height=4, width=20)
        self.knapp3.grid(row=9, column=10, padx=2, pady=10, sticky=W)

        #Definerer menybar
        menubar = Menu(self.master)
        #Fil meny
        filemenu = Menu(menubar, tearoff = 0)
        filemenu.add_command(label="Konfigurer", command=self.konfigurer)
        filemenu.add_command(label="Oppdater Hog database", command=self.trenHoG)
        filemenu.add_command(label="Avslutt", command=self.Avslutt)
        menubar.add_cascade(label="File", menu=filemenu)

        #Video meny
        VideoMenu = Menu(menubar, tearoff = 0)
        VideoMenu.add_command(label="Start video", command=self.StartVideoStream)
        VideoMenu.add_command(label="Stopp video", command=self.StoppVideoStream)
        menubar.add_cascade(label="Video Stream", menu=VideoMenu)

        #Data meny
        self.master.config(menu = menubar)

        #Videorute
        self.VideoStream = Canvas( self.master, width=640,height=480,bg="white")
        self.VideoStream.grid(row=2,column=2,padx=2,pady=25,rowspan=5,columnspan=5,sticky=W)
        return

    def konfigurer(self):
        conf = Tk()
        conf.title("Konfigurasjon")
        cGui = ConfGui(conf,self.konfigParam )

    def KnappeTest3(self):
        self.knapp3.grid(row=7, column=10, padx=2, pady=10, sticky=W)
        print("Knapp 3 trykket")
        return

    def KnappeTest1(self):
        self.knapp3.grid(row=9, column=10, padx=2, pady=10, sticky=W)
        print("Knapp 3 trykket")
        return

    def KnappeTest2(self):
        print("Knapp 2 trykket")
        return

    def Avslutt(self):
        self.running = False
        self.CaptureVideo = False
        self.master.quit()
        return

    def StartVideoStream(self):
        self.CaptureVideo = True
        return

    def StoppVideoStream(self):
        self.CaptureVideo = False
        return

    def ToggleVideoStream(self):
        self.CaptureVideo = not self.CaptureVideo
        return

    def trenHoG(self):
        status = Tk()
        progressBar = ProgressBar("Fremdrift", status, 0, 0)
        status.lift()
        self.HoGDatabase.genererNyHoGDatabase(progressBar)
        return
