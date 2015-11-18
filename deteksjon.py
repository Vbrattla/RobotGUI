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

        # Variabler til nonmax og ansiktsLokalisjon
        self.originalHoyde = 480
        self.originalBredde = 640
        self.originalVinduBredde = 48
        self.originalVinduHoyde = 64

    def behandlerData(self, videoFrame):
        self.klassifisering = numpy.zeros((1,2))

        # Endring av bildestorrelse til (bredde,hoyde) og konverterer til numpy array.
        self.bildeHalvert = videoFrame.resize((self.bredde,self.hoyde), Image.ANTIALIAS)
        self.bildeHalvertNump = numpy.asarray(self.bildeHalvert)

        # Finner features. Winstride gir forflytning av vindu i form av piksler. Padding anvendes ikke
        bildeFeatures = self.NNHoG.compute(self.bildeHalvertNump, winStride=(4,4), padding=(0,0)).T

        # Finner antall feature vektorer fra HoG
        antallFeatVektorer = (bildeFeatures.size)/576

        # Lokke for aa finne HoG features i bildet.
        for iterasjon in range(0,antallFeatVektorer):
            features= numpy.array([bildeFeatures[0,iterasjon*576:iterasjon*576+576]]).T

            # Kaller Neuralt Nettverk objektet.
            self.klassifisering = numpy.vstack([self.klassifisering,self.neuraltNett.FeedForward(features).T])

        # Fjerner forste tomme rad i matrise og endrer til heltallsvisning.
        self.klassifisering = numpy.delete(self.klassifisering, (0), axis=0)
        self.klassifisering = numpy.around(self.klassifisering * 100,5)

        return self.klassifisering

    def fjesDetektering(self,klassifiseringsVektor):

        self.fjesKoordinat = numpy.array([self.bredde,self.hoyde])
        self.iterasjonsvariabel = 0
        # Itererer seg igjennom klassifiseringsvektor fra metoden behandlerData. Denne dataen er utgangen fra
        # det neurale nettverket.

        for vertikal in range(0,self.iterasjonKol):
            for horisontal in range(0,self.iterasjonRad):

                # Sjekker hvert element mot terskel for aa lete etter ansikt.
                sjekkMotTerskel = klassifiseringsVektor[self.iterasjonsvariabel, 0]

                if sjekkMotTerskel >= self.terskel:
                    # Legger inn vinduets start posisjon i form av horisontal og vertikal pikselnummer.
                    ansiktsKoordinat = [horisontal*4,vertikal*4]

                    # Legger alle posisjonene i en vektor/matrise.
                    self.fjesKoordinat = numpy.vstack([self.fjesKoordinat,ansiktsKoordinat])

                # Itererer iterasjonsvariabel
                self.iterasjonsvariabel = self.iterasjonsvariabel + 1

        # Returnerer pikselomraader hvor det er detektert fjes.
        return self.fjesKoordinat


    def transformerKoordinat(self,fjesdeteksjon):
        # vektor fjesdeteksjon inneholder koordinater med detekterte fjes.

        # Finner nedskaleringsfaktoren til bilde
        self.skaleringBredde = self.originalBredde/fjesdeteksjon[0,0]
        self.skaleringHoyde = self.originalHoyde/fjesdeteksjon[0,1]

        # Lagrer deteksjonsmatrise og fjerner forste rad med skalering
        self.fjesDeteksjon = numpy.delete(fjesdeteksjon,(0), axis=0)

        # Multipliserer inn skaleringsfaktor for bredde og hoyde
        self.fjesLokalisjon = numpy.array([self.fjesDeteksjon[0:,0]*self.skaleringBredde,self.fjesDeteksjon[0:,1]*self.skaleringHoyde,
                                           (self.fjesDeteksjon[0:,0]+self.originalVinduBredde)*self.skaleringBredde,
                                           (self.fjesDeteksjon[0:,1]+self.originalVinduHoyde)*self.skaleringHoyde]).T

        # Returnerer lokalisering for fjes i originalt bilde.
        return self.fjesLokalisjon

    def nonMaximumSuppression(self,detekterteAnsikt, terskel):
        # Metode fra http://www.pyimagesearch.com/2015/02/16/faster-non-maximum-suppression-python/

        # Finner storrelse paa skalert vindu
        self.skalertVinduBredde = self.skaleringBredde * self.originalVinduBredde
        self.skalertVinduHoyde = self.skaleringHoyde * self.originalVinduHoyde

        # Sjekker at elementer er av type float.
        if detekterteAnsikt.dtype.kind == "i":
            detekterteAnsikt = detekterteAnsikt.astype("float")

        # Lager en tom liste
        pick = []

        # Henter ut koordinatene til vinduene
        x1 = detekterteAnsikt[:,0]
        y1 = detekterteAnsikt[:,1]
        x2 = detekterteAnsikt[:,2]
        y2 = detekterteAnsikt[:,3]

        # Finner arealet i vinduene.
        areal = (x2 - x1 + 1) * (y2 - y1 + 1)

        idxs = numpy.argsort(y2)

        while len(idxs) > 0:

            last = len(idxs) - 1
            i = idxs[last]
            pick.append(i)

            xx1 = numpy.maximum(x1[i], x1[idxs[:last]])
            yy1 = numpy.maximum(y1[i], y1[idxs[:last]])
            xx2 = numpy.minimum(x2[i], x2[idxs[:last]])
            yy2 = numpy.minimum(y2[i], y2[idxs[:last]])

            w = numpy.maximum(0, xx2 - xx1 + 1)
            h = numpy.maximum(0, yy2 - yy1 + 1)

            overlap = (w * h) / areal[idxs[:last]]

            idxs = numpy.delete(idxs, numpy.concatenate(([last],
                                                         numpy.where(overlap > terskel)[0])))

        return detekterteAnsikt[pick].astype("int")
