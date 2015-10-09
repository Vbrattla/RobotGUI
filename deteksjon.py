import numpy
import cv2
from PIL import Image
from neuralNett import NeuraltNettverk
import fil_IO as IO

class AnsiktsDeteksjon():
    # Klasse for deteksjon av ansikt i videostroemmen

    def __init__(self, neuraltNett,confParametere):
        #Referanse til nauralNett klassen
        self.neuraltNett = neuraltNett
        #Referanse til fil_IO for aa hente konfigurasjonsparametre
        self.param = confParametere

        # Oppretter HoG objekt. Setter terskel for deteksjon av ansikt fra det neurale nettverket.
        self.NNHoG = cv2.HOGDescriptor((48, 64), (32,32), (16,16), (8,8), 6)
        self.klassifisering = numpy.zeros((1,2))
        self.terskel = self.param.getParam(4)
        self.iterasjonsvariabel = 0
        self.fjesDeteksjon = numpy.array((1,2))

        # Variabler til fjeslokalisering
        self.bredde = 160
        self.hoyde = 120
        self.iterasjonRad = (self.bredde - 48)/4 + 1
        self.iterasjonKol = (self.hoyde - 64)/4 + 1

    def behandlerData(self, videoFrame):
        self.klassifisering = numpy.zeros((1,2))

        # Endring av bildestorrelse til (bredde,hoyde) og konverterer til numpy array.
        self.bildeHalvert = videoFrame.resize((self.bredde,self.hoyde), Image.ANTIALIAS)
        self.bildeHalvertNump = numpy.asarray(self.bildeHalvert)

        # Finner features. Winstride gir forflytning av vindu i form av piksler. Padding anvendes ikke
        bildeFeatures = self.NNHoG.compute(self.bildeHalvertNump, winStride=(4,4), padding=(0,0)).T

        # Finner antall feature vektorer fra HoG
        antallFeatVektorer = (bildeFeatures.size)/576
        #print("AntFeatures: " + str(antallFeatVektorer))
        # Lokke for aa finne HoG features i bildet.
        for iterasjon in range(0,antallFeatVektorer):
            features= numpy.array([bildeFeatures[0,iterasjon*576:iterasjon*576+576]]).T

            # Kaller Neuralt Nettverk objektet.
            self.klassifisering = numpy.vstack([self.klassifisering,self.neuraltNett.FeedForward(features).T])

        # Fjerner forste tomme rad i matrise og endrer til heltallsvisning.
        self.klassifisering = numpy.delete(self.klassifisering, (0), axis=0)
        self.klassifisering = numpy.around(self.klassifisering * 100,5)

        return self.klassifisering

    def fjesLokalisering(self,klassifiseringsVektor):
        self.iterasjonsvariabel = 0
        self.fjesDeteksjon = numpy.array((1,2))
      # Itererer seg igjennom klassifiseringsvektor fra metoden behandlerData. Denne dataen er utgangen fra
      # det neurale nettverket.
        #print("Kol: " + str(self.iterasjonKol) + "Rad: " + str(self.iterasjonRad) + " IterasjonsVar: " + str(self.iterasjonsvariabel))
        for vertikal in range(0,self.iterasjonKol):
            for horisontal in range(0,self.iterasjonRad):

                # Sjekker hvert element mot terskel for aa lete etter ansikt.
                sjekkMotTerskel = klassifiseringsVektor[self.iterasjonsvariabel, 0]

                if sjekkMotTerskel >= self.terskel:
                    # Legger inn vinduets start posisjon i form av horisontal og vertikal pikselnummer.
                    ansiktsKoordinat = [horisontal*4,vertikal*4]

                    # Legger alle posisjonene i en vektor/matrise.
                    self.fjesDeteksjon = numpy.vstack([self.fjesDeteksjon,ansiktsKoordinat])

                # Itererer iterasjonsvariabel
                self.iterasjonsvariabel = self.iterasjonsvariabel + 1
            #print("IterasjonsVar: " + str(self.iterasjonsvariabel) + " Sjekk mot terskel: " + str(sjekkMotTerskel))

        # Fjerner forste rad av matrisen
        self.fjesDeteksjon = numpy.delete(self.fjesDeteksjon, (0), axis=0)

        # Returnerer pikselomraader hvor det er detektert fjes.
        return self.fjesDeteksjon
