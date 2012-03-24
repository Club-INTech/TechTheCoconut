# -*- coding: utf-8 -*-

import robot
import __builtin__
import instance

class Serie_acquisition:
    
    __init__(self):
        self.run = True
        self.serieAsserInstance = __builtin__.instance.serieAsserInstance
        self.serieCaptInstance = __builtin__.instance.serieCaptInstance
        self.robotInstance = __builtin__.instance.robotInstance
        thread = threading.Thread(target = self.ecoute_thread)
        thread.start()
        
    def ecoute_thread(self):
        reponse = 'HUK'
        while self.run:
            reponse = self.serieAsserInstance.readline()
            if str(reponse) == 'FIN_GOTO\r\n' or str(reponse) == 'FIN_GOTO\r':
                self.robotInstance.acquitemment = True
            elif str(reponse) == 'FIN_TRA\r\n' or str(reponse) == 'FIN_TRA\r':
                self.robotInstance.translation = True
            elif str(reponse) == 'FIN_TOU\r\n' or str(reponse) == 'FIN_TOU\r':
                self.robotInstance.rotation = True
            elif str(reponse) == 'FIN_REC\r\n':
                self.robotInstance.recalage = True
            else:
                rep = str(reponse).split('.')
                self.robotInstance.position.x = rep[0]
                self.robotInstance.position.y = rep[1]