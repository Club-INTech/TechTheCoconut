# -*- coding: utf-8 -*-

import sys
import os
import robot
import __builtin__
import math
import instance
import asservissement
import threading

class Serie_acquisition:
    
    def __init__(self):
        self.run = True
        
        if hasattr(__builtin__.instance, 'robotInstance'):
            self.robotInstance = __builtin__.instance.robotInstance
        else:
            log.logger.error("l'instance de instance.robotInstance n'est pas chargée")
        if hasattr(__builtin__.instance, 'serieAsserInstance'):
            self.serieAsserInstance = __builtin__.instance.serieAsserInstance
        else:
            log.logger.error("l'instance de instance.serieAsserInstance n'est pas chargée")
        self.serieAsserInstance.write('TG\n')
        self.asserInstance = __builtin__.instance.asserInstance
        thread = threading.Thread(target = self.ecoute_thread)
        thread.start()

    def ecoute_thread(self):
        while self.run:
            reponse = self.serieAsserInstance.readline()
            if str(reponse) == 'FIN_GOTO\r\n' or str(reponse) == 'FIN_GOTO\r':
                if self.asserInstance.mutex:
                    pass
                else:
                    self.robotInstance.acquitemment = True
                    self.serieAsserInstance.write('TG\n')
            elif str(reponse) == 'STOPPE\r\n' or str(reponse) == 'STOPPE\r':
                self.robotInstance.est_arrete = True
                self.serieAsserInstance.write('TG\n')
            elif str(reponse) == 'FIN_TRA\r\n' or str(reponse) == 'FIN_TRA\r' or str(reponse) == 'FIN_TRA':
                self.robotInstance.fin_translation = True
                self.serieAsserInstance.write('TG\n')
            elif str(reponse) == 'FIN_TOU\r\n' or str(reponse) == 'FIN_TOU\r' or str(reponse) == 'FIN_TOU':
                self.robotInstance.fin_rotation = True
                self.serieAsserInstance.write('TG\n')
            elif str(reponse) == 'FIN_REC\r\n':
                self.robotInstance.fin_recalage = True
                self.serieAsserInstance.write('TG\n')
            try:
                if reponse[4]== '+':
                    reponse = reponse.split('+')
                    self.robotInstance.position.x = int(reponse[1])
                    self.robotInstance.position.y = int(reponse[0])
                elif reponse[4] == '-':
                    reponse = reponse.split('-')
                    self.robotInstance.position.x = -int(reponse[1])
                    self.robotInstance.position.y = int(reponse[0])
            except:
                pass
            
            else:
                self.robotInstance.new_message = True
                self.robotInstance.message = str(reponse)