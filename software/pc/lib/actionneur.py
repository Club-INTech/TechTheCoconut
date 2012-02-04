# -*- coding: utf-8 -*-

import serial
import serie
import log
log = log.Log()

class Actionneur:
    """
    Classe permettant de gérer un actionneur
    """
    def __init__(self, peripherique, nom, latence, timeout):
	peripherique = "/dev/usbmon0"
	#actionneur = Serie(peripherique, actionneur, 11000, 5000)
	actionneur.start()
	print 'LOL'
	
	
	
	
    