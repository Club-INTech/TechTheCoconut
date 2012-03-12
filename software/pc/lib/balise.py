# -*- coding: utf-8 -*-

import threading
import peripherique
from filtre_kalman
from numpy import array
from numpy import matrix

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
	
    def __init__(self, robot):
	self.serial = lib.serie.Serie(peripherique.chemin_de_peripherique("balise"),"balise",9600,5)
	dt_init = 0.1
	x = numpy.array([0.,0.,0.,0.])[:, numpy.newaxis] #Vecteur d'état au départ
	P =  numpy.matrix([[0.,0.,0.,0.],[0.,0.,0.,0.],[0.,0.,1000.,0.],[0.,0.,0.,1000.]])# initial uncertainty
	F =  numpy.matrix([[1.,0.,dt_init,0.],[0.,1.,0.,dt_init],[0.,0.,1.,0.],[0.,0.,0.,1.]])# next state function
	H =  numpy.matrix([[1.,0.,0.,0.],[0.,1.,0.,0.]])# measurement function
	R =   numpy.matrix([[0.1,0.],[0.,0.1]])# measurement uncertainty
	self.filtre_kalman = FiltreKalman(x,P,F,H,R)
    
    def tracker_robot_adverse(self):
	Z = self.serial.readline(30)
	self.filtre_kalman.filtrer(Z)
	
	
	
	