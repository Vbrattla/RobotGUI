import math, random
import cv2
from PIL import Image
import numpy

class NeuraltNettverk():
    # Opprettet et neuralt nettverk

    def __init__(self,nh):
        # Variabler
        # nh = antall gjemte noder, initVekt = initialverdi til vektene.
        self.nh = nh
        self.initVekt = 1/math.sqrt(self.nh)
        self.antallKlasser = 2
        self.antallInput = 576

        # Kan implementeres i fremtiden.
        self.larerate = 0.01

        # Lager utgangsvektor fra den gjemte noden og utgangen
        self.fnetHidden = numpy.zeros((self.nh,1))
        self.fnetUtgang = numpy.zeros((self.antallKlasser,1))

        # Lager tomme matriser for vektene
        self.vektItH = numpy.empty((self.nh, self.antallInput))
        self.vektHtO = numpy.empty((self.antallKlasser,self.nh))

        # Lager tomme vektorer for ItH, HtO Bias og bias vekt
        self.ItHBias = numpy.ones((self.nh,1))
        self.vektBiasItH = numpy.empty((self.nh,1))
        self.HtOBias = numpy.ones((self.antallKlasser,1))
        self.vektBiasHtO = numpy.empty((self.antallKlasser,1))

    def lageVekter(self):
    # Denne metoden initerer verdiene til vekter og bias til det neurale nettverket.

        # Fyller inn verdier i nodevekt og bias.
        for rad in range(0, self.nh):

            # Lager biasvekt for Input to Hidden
            self.vektBiasItH[rad,0] = 0.5*math.pow(-1,rad)

            # Lager biasvekt for Hidden to Output
            if rad <= self.antallKlasser-1:
                self.vektBiasHtO[rad,0] = 0.5*math.pow(-1,rad)

            # Lager Input to Hidden nodevekt i omraadet -1/sqrt(nh)<noder<1/sqrt(nh).
            for kol in range(0,self.antallInput):
                self.vektItH[rad, kol] = (random.randrange(-100,100) * self.initVekt)/100

                # Lager Hidden to Output nodevekt i omraadet -1/sqrt(nh)<noder<1/sqrt(nh).
                if kol <= self.antallKlasser-1:
                    self.vektHtO[kol, rad] = (random.randrange(-100,100) * self.initVekt)/100


    def FeedForward(self,inngangsVektor):
        # Regner metoden utforer FeedForward for det neurale nettverket.

        # Finner "net_j" for Input to Hidden
        netHidden = (self.vektItH).dot(inngangsVektor) + self.ItHBias*self.vektBiasItH

        # Finner utgangen til den gjemte noden. Bruker aktiveringsfunkjson paa formen 1/(1+e^(-net))
        # Har tanh aktiveringsfunksjon som mulighet i fremtiden.
        for node in range(0,self.nh):
            #self.fnetHidden[node,0] = 1.716*math.tanh(netHidden[node,0]*2/3)
            self.fnetHidden[node,0] = 1/(1 + math.exp((-1)*netHidden[node,0]))

        # Finner "net" for Hidden to Output.
        netUtgang = (self.vektHtO).dot(self.fnetHidden) + self.HtOBias*self.vektBiasHtO

        # Regner ut utgangsverdiene z. Bruker aktiveringsfunkjson paa formen 1/(1+e^(-net))
        # Har tanh aktiveringsfunksjon som mulighet i fremtiden.
        for node in range(0,self.antallKlasser):
            #self.fnetUtgang[node,0] = 1.716*math.tanh(netUtgang[node,0]*2/3)
            self.fnetUtgang[node,0] = 1/(1 + math.exp((-1)*netUtgang[node,0]))

        # Returnerer utgangsvektor, der hver element beskrive en klasse.
        return self.fnetUtgang

    def Backward(self,target,inngangsVektor):

        # Finner f(net_1) og f(net_2) derivert
        fnetHiddenDerivert = self.fnetHidden.T*(numpy.ones((1,self.nh)) - self.fnetHidden.T)
        fnetUtgangDerivert = self.fnetUtgang.T*(numpy.ones((1,self.antallKlasser)) - self.fnetUtgang.T)

        # Finner sensitiviteten til Hidden to Output og Input to Hidden
        sensitivitetHtO = (((target - self.fnetUtgang.T))*fnetUtgangDerivert).T
        sensitivitetItH = fnetHiddenDerivert.T*self.vektHtO.T.dot(sensitivitetHtO)

        # Finner delta vekt HtO og ItH
        deltaVektHtO = sensitivitetHtO.dot(self.fnetHidden.T)
        deltaVektItH = sensitivitetItH.dot(inngangsVektor.T)

        # Finner delta vekt bias HtO og ItH
        deltaVektBiasHtO = sensitivitetHtO
        deltaVektBiasItH = sensitivitetItH

        # Oppdaterer Input to Hidden vektene
        self.vektItH = (self.vektItH + deltaVektItH)
        self.vektBiasItH = (self.vektBiasItH + deltaVektBiasItH)

        # Oppdaterer Hidden to Output vektene
        self.vektHtO = (self.vektHtO + deltaVektHtO)
        self.vektBiasHtO = (self.vektBiasHtO + deltaVektBiasHtO)

        return self.vektHtO

    def TrenNauraltNett(self, iterasjoner, posHoGVektor, negHoGVektor):
        for iterasjon in range(1,iterasjoner):
            targetPos = numpy.array([1, 0])
            targetNeg = numpy.array([0, 1])

            vektorPos =  numpy.array([posHoGVektor[iterasjon,0:]]).T
            test = self.FeedForward(vektorPos)
            test6= self.Backward(targetPos,vektorPos)

            vektorNeg =  numpy.array([negHoGVektor[iterasjon,0:]]).T
            test = self.FeedForward(vektorNeg)
            test6= self.Backward(targetNeg,vektorNeg)

    pass
