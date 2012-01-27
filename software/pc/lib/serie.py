# -*- coding: utf-8 -*-

import serial
import threading
import Queue

import log
log = log.Log()

class SerieThread(threading.Thread, serial.Serial):
    """
    Classe de créer une liaison Série utilisant un thread (ie non bloquante)
    
    :param peripherique: chemin du périphérique utilisant la liaison série
    :type peripherique: string
    :param nom: Nom à donner au thread
    :type nom: string
    :param debit: Débit de baud de la liaison
    :type debit: int
    :param timeout: Timeout de la liaison en secondes
    :type timeout: int
    :param parite: Type de parité
    :type parite: None|PARITY_NONE|PARITY_EVEN|PARITY_ODD|PARITY_MARK|PARITY_SPACE
    :TODO: Mettre le débit de Baud par défaut
    """
    def __init__(self, peripherique, nom, debit, timeout, parite=None):
        self.peripherique = peripherique
        self.file_attente = Queue.LifoQueue()
        log.logger.info("Initialisation de la liaison série threadée sur "+peripherique+" avec un débit de baud de "+str(debit)+" et un timeout de "+str(timeout))
        try:
            threading.Thread.__init__(self, name=nom, target=self.lire)
            if parite == None:
                serial.Serial.__init__(self, peripherique, debit, timeout=timeout)
            else:
                serial.Serial.__init__(self, peripherique, debit, name=nom, target=self.lire, timeout=timeout, parity=parite)
        except:
            log.logger.error("Erreur d'initialisation de la liaison série threadée sur "+peripherique+" avec un débit de baud de "+str(debit)+" et un timeout de "+str(timeout))

    def ecrire(self, msg):
        """
        Écrire une information vers un périphérique puis retourner à la ligne
        
        :param msg: message à donner au périphérique
        :type msg: string
        :return: Nombre de caractères envoyés
        :rtype: int
        """
        log.logger.debug("Écrire sur la liaison série "+self.peripherique+" : "+msg)
        return self.write(msg+"\r\n")
    
    def lire(self):
        """
        Lire une information venant d'un périphérique jusqu'au retour à la ligne
        
        :return: Chaîne lue
        :rtype: string
        """
        while 42:
            lu = self.readline()
            lu = lu.split("\r\n")[0]
            if lu != '':
                log.logger.debug("Lecture sur la liaison série "+self.peripherique+" : "+lu)
                self.file_attente.put(lu)

    def __del__(self):
        """
        Destructeur qui ferme proprement la liaison série
        """
        log.logger.info("Suppression de la liaison série sur "+self.peripherique)
        self.join()
        self.close()

def ipbreak():
    import IPython.Shell
    if IPython.Shell.KBINT:
        IPython.Shell.KBINT = False
        raise SystemExit

class SerieSimple(serial.Serial):
    """
    Classe de créer une liaison Série sans Thread (ie bloquante)
    
    :param peripherique: chemin du périphérique utilisant la liaison série
    :type peripherique: string
    :param debit: Débit de baud de la liaison
    :type debit: int
    :param timeout: Timeout de la liaison en secondes
    :type timeout: int
    :TODO: Mettre le débit de Baud par défaut
    """
    def __init__(self, peripherique, debit, timeout):
        self.peripherique = peripherique
        log.logger.info("Initialisation de la liaison série simple sur "+peripherique+" avec un débit de baud de "+str(debit)+" et un timeout de "+str(timeout))
        try:
            serial.Serial.__init__(self, peripherique, debit, timeout=timeout)
        except:
            log.logger.error("Erreur d'initialisation de la liaison série simple sur "+peripherique+" avec un débit de baud de "+str(debit)+" et un timeout de "+str(timeout))

    def ecrire(self, msg):
        """
        Écrire une information vers un périphérique puis retourner à la ligne
        
        :param msg: message à donner au périphérique
        :type msg: string
        :return: Nombre de caractères envoyés
        :rtype: int
        """
        log.logger.debug("Écrire sur la liaison série "+self.peripherique+" : "+msg)
        return self.write(msg+"\r\n")
    
    def lire(self):
        """
        Lire une information venant d'un périphérique jusqu'au retour à la ligne
        
        :return: Chaîne lue
        :rtype: string
        """
        lu = self.readline()
        lu = lu.split("\r\n")[0]
        log.logger.debug("Lecture sur la liaison série "+self.peripherique+" : "+lu)
        return lu;

    def __del__(self):
        """
        Destructeur qui ferme proprement la liaison série
        """
        log.logger.info("Suppression de la liaison série sur "+self.peripherique)
        self.close()