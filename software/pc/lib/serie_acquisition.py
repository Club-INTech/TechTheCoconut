# -*- coding: utf-8 -*-

import robot
import __builtin__
import math
import instance

class Serie_acquisition:
    
    __init__(self, huk):
        self.run = True
        self.serieAsserInstance = __builtin__.instance.serieAsserInstance
        self.serieCaptInstance = __builtin__.instance.serieCaptInstance
        self.robotInstance = __builtin__.instance.robotInstance
        thread = threading.Thread(target = self.ecoute_thread(huk))
        thread.start()
        
    def ecoute_thread(self, huk):
        reponse = 'HUK'
        while self.run:
            #reponse = self.serieAsserInstance.readline()
            reponse = huk
            if str(reponse) == 'FIN_GOTO\r\n' or str(reponse) == 'FIN_GOTO\r':
                self.robotInstance.acquitemment = True
            elif str(reponse) == 'FIN_TRA\r\n' or str(reponse) == 'FIN_TRA\r':
                self.robotInstance.translation = True
            elif str(reponse) == 'FIN_TOU\r\n' or str(reponse) == 'FIN_TOU\r':
                self.robotInstance.rotation = True
            elif str(reponse) == 'FIN_REC\r\n':
                self.robotInstance.recalage = True
            else:
                signe = math.copysign(1,int(reponse))
                if reponse[0] == 1:
                    x = int(reponse) + 10000*signe 
                    self.robotInstance.position.x = x
                else:
                    y = int(reponse) + 20000*signe
                    self.robotInstance.position.y = y
                
            
            print 'acquitemment :'
            print self.robotInstance.acquitemment
            print 'translation :'
            print self.robotInstance.translation
            print 'rotation'
            print self.robotInstance.rotation
            print 'recalage'
            print self.robotInstance.recalage
            print x
            print y