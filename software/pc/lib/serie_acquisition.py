# -*- coding: utf-8 -*-

import __builtin__
import threading
from threading import Lock

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
        self.mutex = Lock()
        self.asserInstance = __builtin__.instance.asserInstance
        thread = threading.Thread(target = self.ecoute_thread)
        thread.start()

    def ecoute_thread(self):
        while self.run:
            try:
                reponse = self.serieAsserInstance.readline()
            except:
                pass
            if str(reponse) == 'FIN_GOTOA\r\n' or str(reponse) == 'FIN_GOTOA\r':
                if self.robotInstance.acqA == True:
                    pass
                else:
                    self.mutex.acquire()
                    print reponse
                    self.robotInstance.acquitemment = True
                    self.robotInstance.acqA = True
                    self.robotInstance.acqB = False
                    self.mutex.release()
            elif str(reponse) == 'FIN_GOTOB\r\n' or str(reponse) == 'FIN_GOTOB\r':
                if self.robotInstance.acqB == True:
                    pass
                else:
                    self.mutex.acquire()
                    print reponse
                    self.robotInstance.acquitemment = True
                    self.robotInstance.acqB = True
                    self.robotInstance.acqA = False
                    self.mutex.release()
            elif str(reponse) == 'STOPPE\r\n' or str(reponse) == 'STOPPE\r':
                self.mutex.acquire()
                self.robotInstance.est_arrete = True
                self.mutex.release()
                self.serieAsserInstance.write('TG\n')
            elif str(reponse) == 'FIN_TRA\r\n' or str(reponse) == 'FIN_TRA\r' or str(reponse) == 'FIN_TRA':
                self.mutex.acquire()
                self.robotInstance.fin_translation = True
                self.mutex.release()
                self.serieAsserInstance.write('TG\n')
            elif str(reponse) == 'FIN_TOU\r\n' or str(reponse) == 'FIN_TOU\r' or str(reponse) == 'FIN_TOU':
                self.mutex.acquire()
                self.robotInstance.fin_rotation = True
                self.mutex.release()
                print 'FIN TOURNER'
                self.serieAsserInstance.write('TG\n')
            elif str(reponse) == 'FIN_REC\r\n':
                self.mutex.acquire()
                self.robotInstance.fin_recalage = True
                self.mutex.release()
                self.serieAsserInstance.write('TG\n')
            try:
                if reponse[4] == '+':
                    reponse = reponse.split('+')
                    self.mutex.acquire()
                    self.robotInstance.position.x = int(reponse[1])
                    self.robotInstance.position.y = int(reponse[0])
                    self.mutex.release()
                elif reponse[4] == '-':
                    reponse = reponse.split('-')
                    self.mutex.acquire()
                    self.robotInstance.position.x = -int(reponse[1])
                    self.robotInstance.position.y = int(reponse[0])
                    self.mutex.release()
            except:
                pass
            
            else:
                self.mutex.acquire()
                self.robotInstance.new_message = True
                self.robotInstance.message = str(reponse)
                self.mutex.release()