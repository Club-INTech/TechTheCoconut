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
            recu = True
            reponse = self.serieAsserInstance.readline()
            if str(reponse) == 'FIN_GOTO\r\n' or str(reponse) == 'FIN_GOTO\r':
                self.robotInstance.segment_en_cours = False
                self.serieAsserInstance.write('TG\n')
            elif str(reponse) == 'STOPPE\r\n' or str(reponse) == 'STOPPE\r':
                self.robotInstance.est_arrete = True
                self.serieAsserInstance.write('TG\n')
            elif str(reponse) == 'FIN_TRA\r\n' or str(reponse) == 'FIN_TRA\r':
                self.robotInstance.translation_en_cours = False
                self.serieAsserInstance.write('TG\n')
            elif str(reponse) == 'FIN_TOU\r\n' or str(reponse) == 'FIN_TOU\r':
                self.robotInstance.rotation_en_cours = False
                self.serieAsserInstance.write('TG\n')
            elif str(reponse) == 'FIN_REC\r\n':
                self.robotInstance.recalage_en_cours = False
                self.serieAsserInstance.write('TG\n')
            else:
                recu = False
                
            try:
                if reponse[4]== '+':
                    recu = True
                    reponse = reponse.split('+')
                    self.robotInstance.position.x = int(reponse[1])
                    self.robotInstance.position.y = int(reponse[0])
                elif reponse[4] == '-':
                    recu = True
                    reponse = reponse.split('-')
                    self.robotInstance.position.x = -int(reponse[1])
                    self.robotInstance.position.y = int(reponse[0])
            except:
                pass
            
            if not recu and len(reponse) > 3 :
                self.robotInstance.message = str(reponse).replace("\r","")
                self.robotInstance.new_message = True