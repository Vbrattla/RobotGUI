import threading
import time
from Tkinter import *
from klGui import *
import cv2
from PIL import Image, ImageTk, ImageStat
from trenBilder import HoGTrening
import tkMessageBox
import fil_IO as IO
from confGui import ConfGui
from neuralNett import NeuraltNettverk
from deteksjon import AnsiktsDeteksjon

# Henter inn konfigurasjonsparametre
konfigParam = IO.FileIO("lagre.txt")
root = Tk()
#root.geometry("1500x700")
root.title("Prosjekt")
HoGdB = HoGTrening(konfigParam)
program = Gui(root, konfigParam,HoGdB)
program.running = True
print(konfigParam.getParam(4))
try:
    posHoGVektor = HoGdB.hentPosHoGVektor()
    negHoGVektor = HoGdB.hentNegHoGVektor()
    print( type(posHoGVektor), posHoGVektor.shape )
except:
    tkMessageBox.showinfo("Info","Fikk ikke hentet inn HoG vektorer" )
    pass

neuralNett = NeuraltNettverk(60)
neuralNett.lageVekter()
neuralNett.TrenNauraltNett(299, posHoGVektor, negHoGVektor)

sti = "C:\Ansikt_Database"
bildeNavnPos = bildeNavnPos = "\pos\PosTrening (2).jpg"
bildeSti = str(sti+""+bildeNavnPos)
bildePos = Image.open(bildeSti)

#Faktisk deteksjon
klassifiserer = AnsiktsDeteksjon(neuralNett,konfigParam)
klassifisering = klassifiserer.behandlerData(bildePos)
test2 = klassifiserer.fjesLokalisering(klassifisering)


#klassifisering = klassifiserer.behandlerData(bildePos)
#test3 = klassifiserer.fjesLokalisering(klassifisering)


#print("Neuralt Nettverk")
#print(klassifisering)

print("Ansiktskoordinat retur")
print(test2)






def Thread_videoCapture():
    opptak = cv2.VideoCapture(0)
    opptak.set(3,640)
    opptak.set(4,480)
    while program.running:
        while program.CaptureVideo:
            #time.sleep( konfigParam.getParam(0))
            time.sleep( 1)
            try:
                ret, frame = opptak.read()


            except:
                opptak.release()
                cv2.destroyAllWindows()
                time.sleep( konfigParam.getParam(0))
                opptak = cv2.VideoCapture(0)
                pass

            else:
                if ret:
                    #print ("Frame default resolution: (" + str(opptak.get(cv2.CAP_PROP_FRAME_HEIGHT ))  + "; " + str(opptak.get(cv2.CAP_PROP_FRAME_WIDTH)) + ")" )
                    #frame = cv2.rectangle(frame,(384,0),(510,128),(0,255,0),3)
                    bildePre = Image.fromarray(frame)

                    bilde = ImageTk.PhotoImage(bildePre)
                    #klassifisering = klassifiserer.behandlerData(bildePre)
                    klassifisering = klassifiserer.behandlerData(bildePos)
                    #print(opptak)
                    #print(klassifisering )
                    test2 = klassifiserer.fjesLokalisering(klassifisering)
                    #print(len(test2.shape) )
                    if len(test2.shape) > 1:
                        frame = cv2.rectangle(frame,(test2[0,0],0),(test2[0,1],128),(0,255,0),3)
                        bildePre = Image.fromarray(frame)
                        bilde = ImageTk.PhotoImage(bildePre)
                        print( test2,test2 )
                    #program.VideoStream.create_image( 640,480, image=bilde)
                    program.VideoStream.create_image(322, 242, image=bilde)

    opptak.release()
    cv2.destroyAllWindows()
    return


def Worker():
    print("Worker")
    return


def t_print():
    while program.running:
        # program.KnappeTest1()
        time.sleep(1)
        print("StatusCapture", program.CaptureVideo)

    opptak.release()
    cv2.destroyAllWindows()
    return

b = threading.Thread(target=Thread_videoCapture)
b.start()
t = threading.Thread(target=Worker)
t.start()

# p = threading.Thread(target=t_print)
# p.start()

root.mainloop()
