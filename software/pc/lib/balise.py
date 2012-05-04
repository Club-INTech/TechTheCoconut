# -*- coding: utf-8 -*-

#import threading

from filtre_kalman import FiltreKalman
import numpy
from threading import Thread, Lock

class Balise:
    """
    Classe permettant de gérer la balise
    """
    def etat_robot_adverse(self):
        return self.filtre_kalman.x
        
    def update_dt(self, new_dt):
        self.filtre_kalman.F[1,3] = new_dt
        self.filtre_kalman.F[2,4] = new_dt
	
    def __init__(self):
        self.robotInstance = __builtin__.instance.robotInstance
        
        if hasattr(__builtin__.instance, 'serieBaliseInstance'):
            self.serieBaliseInstance = __builtin__.instance.serieBaliseInstance
        else:
            log.logger.error("balise : ne peut importer instance.serieBaliseInstance")
        
        #self.serial = serial.Serial(peripherique.chemin_de_peripherique("balise"),"balise",9600,5)
        self.dt_init = 0.1
        x = numpy.array([0.,0.,0.,0.])[:, numpy.newaxis] #Vecteur d'état au départ
        P =  numpy.matrix([[0.,0.,0.,0.],[0.,0.,0.,0.],[0.,0.,1000.,0.],[0.,0.,0.,1000.]])# initial uncertainty
        F =  numpy.matrix([[1.,0.,dt_init,0.],[0.,1.,0.,dt_init],[0.,0.,1.,0.],[0.,0.,0.,1.]])# next state function
        H =  numpy.matrix([[1.,0.,0.,0.],[0.,1.,0.,0.]])# measurement function
        R =   numpy.matrix([[0.1,0.],[0.,0.1]])# measurement uncertainty
        self.filtre_kalman = FiltreKalman(x,P,F,H,R)
        self.mutex = Lock()
    
    def tracker_robot_adverse(self):
        while(1):
            time.sleep(0.1)
            log.logger.info("Balise : Communication avec la carte")
            #Z = self.serial.readline(30)
            self.serieBaliseInstance.ecrire("v")
            retour = self.serieBaliseInstance.lire()
            log.logger.info("Balise : Trame Reçue")
            if(retour == "ERREUR_CANAL"):
               log.logger.error("balise : canal pourri.")
            elif(retour == "NON_VISIBLE"):
                log.logger.error("balise : non visible.")
            else:
                log.logger.info("Balise : Trame intègre")
                vals = retour.split('.')
                dist = vals[1]
                angle = vals[2]
                angle_rad = angle*math.pi/180
                x = dist*math.cos(angle_rad)
                y = dist*math.sin(angle_rad)
                log.logger.info("Balise : Mise à jour des coordonnées par Kalman")
                self.filtre_kalman.filtrer(numpy.array([x,y]))

    
#robot = Robot()
balise = Balise()
balise.tracker_robot_adverse()
balise.tracker_robot_adverse()
balise.tracker_robot_adverse()
balise.tracker_robot_adverse()
print balise.filtre_kalman.x
	
	