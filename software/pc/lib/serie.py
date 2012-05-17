# -*- coding: utf-8 -*-

import serial
import threading
import Queue
import sys, os
import __builtin__
import instance
import log
log = log.Log(__name__)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import time
import threading
class TimeoutError(Exception): pass

def timelimit(timeout):
    def internal(function):
        def internal2(*args, **kw):
            class Calculator(threading.Thread):
                def __init__(self):
                    threading.Thread.__init__(self)
                    self.result = None
                    self.error = None
                
                def run(self):
                    try:
                        self.result = function(*args, **kw)
                    except:
                        self.error = sys.exc_info()[0]
            
            c = Calculator()
            c.start()
            c.join(timeout)
            if c.isAlive():
                raise TimeoutError
            if c.error:
                raise c.error
            return c.result
        return internal2
    return internal
    
    

class Serie(threading.Thread, serial.Serial):
    """
    Classe permettant de créer une liaison Série utilisant un thread (ie non bloquante)\n
    \n
    Pour la démarrer utiliser la méthode start()\n
    Les messages sont stockés dans l'attribut d'instance file_attente qui est un objet LifoQueue http://www.doughellmann.com/PyMOTW/Queue/index.html#lifo-queue \n
    Pour l'arrêter utiliser la méthode stop()\n
    \n
    :param peripherique: chemin du périphérique utilisant la liaison série
    :type peripherique: string
    :param nom: Nom à donner au thread
    :type nom: string
    :param debit: Débit de baud de la liaison
    :type debit: int
    :param timeout: Timeout de la liaison en secondes
    :type timeout: int
    :param parite: Type de parité
    :type parite: None|'PARITY_NONE'|'PARITY_EVEN'|'PARITY_ODD'|'PARITY_MARK'|'PARITY_SPACE'
    :TODO: Mettre le débit de Baud par défaut
    """
    def __init__(self, peripherique, debit, timeoutSerie):
        self.serie = serial.Serial(peripherique, debit, timeout = timeoutSerie)
        self.mutex = __builtin__.instance.mutex

    @timelimit(1)
    def decoLire(self):
        self.mutex.acquire()
        reponse = self.serie.readline()
        self.mutex.release()
        reponse = str(reponse).replace("\n","").replace("\r","").replace("\0", "")
        return reponse
        
    def lire(self,timeout = True):
        """
        Lire une information venant d'un périphérique jusqu'au retour à la ligne
        """
        if timeout :
            try:
                #print "lecture..."
                return self.decoLire()
            except:
                #print "sleep..."
                time.sleep(1)
                #print "recursion..."
                return self.lire()
        else:
            self.mutex.acquire()
            reponse = self.serie.readline()
            self.mutex.release()
            reponse = str(reponse).replace("\n","").replace("\r","").replace("\0", "")
            return reponse
    
    def ecrire(self, message):
        """
        Écrire une information vers un périphérique puis retourner à la ligne
        :param message: message à donner au périphérique
        :type message: string
        """
        self.mutex.acquire()
        self.serie.write(str(message) + '\r')
        self.mutex.release()
        
    def clean(self):
        """
        réinitialise le buffer d'envoi
        """
        self.ecrire("")
        self.lire()
        
    def stop(self):
        """
        Arrête la liaison série
        """
        log.logger.info("Suppression de la liaison série "+self.nom+" sur "+self.peripherique)
        self.active = False
        if self.active:
            self.join()
        # Pour gérer une mauvaise parité qui ne lance par la liaison
        if hasattr(self, "_isOpen"):
            self.close()
