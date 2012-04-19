# -*- coding: utf-8 -*-

#import threading

from filtre_kalman import FiltreKalman
import numpy

class Balise:
    """
    Classe permettant de gérer la balise
    """
    aliases = {
        'etat_robot_adverse': 'self.filtre_kalman.x',
    }

        
    def update_dt(self, new_dt):
	self.filtre_kalman.F[1,3] = new_dt
	self.filtre_kalman.F[2,4] = new_dt
	
    def __init__(self):
	#self.serial = serial.Serial(peripherique.chemin_de_peripherique("balise"),"balise",9600,5)
	dt_init = 0.1
	x = numpy.array([0.,0.,0.,0.])[:, numpy.newaxis] #Vecteur d'état au départ
	P =  numpy.matrix([[0.,0.,0.,0.],[0.,0.,0.,0.],[0.,0.,1000.,0.],[0.,0.,0.,1000.]])# initial uncertainty
	F =  numpy.matrix([[1.,0.,dt_init,0.],[0.,1.,0.,dt_init],[0.,0.,1.,0.],[0.,0.,0.,1.]])# next state function
	H =  numpy.matrix([[1.,0.,0.,0.],[0.,1.,0.,0.]])# measurement function
	R =   numpy.matrix([[0.1,0.],[0.,0.1]])# measurement uncertainty
	self.filtre_kalman = FiltreKalman(x,P,F,H,R)
    
    def tracker_robot_adverse(self,x,y):
	#Z = self.serial.readline(30)
	self.filtre_kalman.filtrer(numpy.array([x,y]))

#robot = Robot()
balise = Balise()
balise.tracker_robot_adverse(0,0)
balise.tracker_robot_adverse(1,2)
balise.tracker_robot_adverse(3,4)
balise.tracker_robot_adverse(8,30)
print balise.filtre_kalman.x
	
	