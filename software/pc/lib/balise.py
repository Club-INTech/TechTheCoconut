# -*- coding: utf-8 -*-

#import threading

from filtre_kalman import FiltreKalman
import outils_math.point as point
import numpy
from threading import Thread, Lock
import __builtin__
import lib.log
import time
import math

log =lib.log.Log(__name__)

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
        self.instances = __builtin__.instance
        if hasattr(self.instances, 'serieBaliseInstance'):
            self.serieBaliseInstance = self.instances.serieBaliseInstance
        else:
            log.logger.error("balise : ne peut importer instance.serieBaliseInstance")
        #self.serial = serial.Serial(peripherique.chemin_de_peripherique("balise"),"balise",9600,5)
        self.dt = 0.2
        self.timeout_serie = 0.25
        x = numpy.array([1500+687.90,1000-158.81,0.,0.])[:, numpy.newaxis] #Vecteur d'état au départ
        P =  numpy.matrix([[50.,0.,0.,0.],[0.,50.,0.,0.],[0.,0.,10.,0.],[0.,0.,0.,10.]])# initial uncertainty
        F =  numpy.matrix([[1.,0.,self.dt,0.],[0.,1.,0.,self.dt],[0.,0.,1.,0.],[0.,0.,0.,1.]])# next state function
        H =  numpy.matrix([[1.,0.,0.,0.],[0.,1.,0.,0.]])# measurement function
        R =   numpy.matrix([[10,0.],[0.,10]])# measurement uncertainty - 10mm
        Q = numpy.matrix([[self.dt**3/3., self.dt**2/2., 0, 0],[self.dt**2/2.,self.dt, 0, 0],[0,0,self.dt**3/3.,self.dt**2/2],[0,0,self.dt**2/2,self.dt]])
        Q *= 10;
        self.filtre_kalman = FiltreKalman(x,P,F,H,R,Q)
        self.mutex = Lock()
    
    def allumer(self):
        log.logger.info("balise : allumage")
        self.serieBaliseInstance.ecrire("allumer")
        
    def eteindre(self):
        log.logger.info("balise : eteindre")
        self.serieBaliseInstance.ecrire("eteindre")
        
        
    def getPosition(self):
        self.mutex.acquire()
        state = self.filtre_kalman.x;
        nouvelle_pos = point.Point(state[0], state[1])
        self.mutex.release()
        return nouvelle_pos
    
    def getVitesse(self):
        self.mutex.acquire()
        state = self.filtre_kalman.x;
        nouvelle_vitesse = [ state[2], state[3] ]
        self.mutex.release()
        return nouvelle_vitesse
                
    def tracker_robot_adverse(self):
        while(1):
            time.sleep(self.dt)
            log.logger.info("Balise : Communication avec la carte")
            #Z = self.serial.readline(30)
            self.serieBaliseInstance.ecrire("v")
            retour = self.serieBaliseInstance.lire()
            log.logger.info("Balise : Trame Reçue")
            
            #Prediction de Kalman.
            self.filtre_kalman.prediction()
            if(retour == "ERREUR_CANAL"):
               log.logger.error("balise : canal pourri.")
            elif(retour == "NON_VISIBLE"):
                log.logger.error("balise : non visible.")
            elif(retour == "timeout"):
                pass
            else:
                #La mesure est bonne, on peut ajouter la mesure au filtre de Kalman
                log.logger.info("Balise : Trame intègre")
                vals = retour.split('.')
                dist = vals[1]
                angle = vals[2]
                angle_rad = int(angle)*math.pi/180
                
                # x_adverse = x_robot + dist*cos(angle+angle_robot)
                # y_adverse = y_robot + dist*sin(angle+angle_robot)
                x = int(dist)*math.cos(angle_rad)
                y = int(dist)*math.sin(angle_rad)
                pos = point.Point(x,y) + self.instances.robotInstance.getPosition()
                log.logger.info("Balise : Mise à jour des coordonnées par Kalman : " + pos )
                self.mutex.acquire()
                self.filtre_kalman.measurement(numpy.array([pos.x,pos.y])[:, numpy.newaxis])
                self.mutex.release()
    
##robot = Robot()
#balise = Balise()
#balise.tracker_robot_adverse()
#balise.tracker_robot_adverse()
#balise.tracker_robot_adverse()
#balise.tracker_robot_adverse()
#print balise.filtre_kalman.x
