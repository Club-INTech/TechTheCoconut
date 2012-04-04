# -*- coding: utf-8 -*-

import __builtin__
import threading
from threading import Lock

class Serie_acquisition:
    
    def __init__(self):
        self.run = True
        self.acqA = False
        self.acqB = False
        self.touA = False
        self.touB = False
        self.traA = False
        self.traB = False
        
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
            if str(reponse) == 'FIN_GOTOA\r\n' or str(reponse) == 'FIN_GOTOA\r' or str(reponse) == 'FIN_GOTOA\n' or str(reponse) == 'FIN_GOTOA':
                if self.acqA == True:
                    pass
                else:
                    self.mutex.acquire()
                    print reponse
                    self.robotInstance.acquitemment = True
                    self.acqA = True
                    self.acqB = False
                    self.mutex.release()
            elif str(reponse) == 'FIN_GOTOB\r\n' or str(reponse) == 'FIN_GOTOB\r' or str(reponse) == 'FIN_GOTOB\n' or str(reponse) == 'FIN_GOTOB':
                if self.acqB == True:
                    pass
                else:
                    self.mutex.acquire()
                    print reponse
                    self.robotInstance.acquitemment = True
                    self.acqB = True
                    self.acqA = False
                    self.mutex.release()
            elif str(reponse) == 'STOPPE\r\n' or str(reponse) == 'STOPPE\r' or str(reponse) == 'STOPPE' or str(reponse) == 'STOPPE\n':
                self.mutex.acquire()
                self.robotInstance.est_arrete = True
                self.mutex.release()
                self.serieAsserInstance.write('TG\n')
            elif (str(reponse) == 'FIN_TRAA\r\n' or str(reponse) == 'FIN_TRAA\r' or str(reponse) == 'FIN_TRAB\n' or str(reponse) == 'FIN_TRAA') and self.robotInstance.fin_translation == False:
                print reponse
                if self.traA == True:
                    pass
                else:
                    self.mutex.acquire()
                    self.robotInstance.fin_translation = True
                    self.traA = True
                    self.traB = False
                    self.mutex.release()
            elif str(reponse) == ('FIN_TRAB\r\n' or str(reponse) == 'FIN_TRAB\r' or str(reponse) == 'FIN_TRAB\n' or str(reponse) == 'FIN_TRAB') and self.robotInstance.fin_translation == False:
                print reponse
                if self.traB == True:
                    pass
                else:
                    self.mutex.acquire()
                    self.robotInstance.fin_translation = True
                    self.traB = True
                    self.traA = False
                    self.mutex.release()
            elif str(reponse) == ('FIN_TOUA\r\n' or str(reponse) == 'FIN_TOUA\r'or str(reponse) == 'FIN_TOUA\n' or str(reponse) == 'FIN_TOUA') and self.robotInstance.fin_rotation == False:
                print reponse
                if self.touA == True:
                    pass
                else:
                    self.mutex.acquire()
                    self.robotInstance.fin_rotation = True
                    self.touA = True
                    self.touB = False
                    self.mutex.release()
            elif str(reponse) == ('FIN_TOUB\r\n' or str(reponse) == 'FIN_TOUB\r' or str(reponse) == 'FIN_TOUB\n' or str(reponse) == 'FIN_TOUB') and self.robotInstance.fin_rotation == False:
                print reponse
                if self.touB == True:
                    pass
                else:
                    self.mutex.acquire()
                    self.robotInstance.fin_rotation = True
                    self.touB = True
                    self.touA = False
                    self.mutex.release()
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
            print reponse