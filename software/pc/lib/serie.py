# -*- coding: utf-8 -*-

import serial
import threading
import Queue

import log
log = log.Log()

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
    def __init__(self, peripherique, nom, debit, timeout, parite=None):
        self.peripherique = peripherique
        self.nom = nom
        # File d'attente LIFO des messages venant de cette liaison
        self.file_attente = Queue.LifoQueue()
        log.logger.info("Initialisation de la liaison série threadée "+nom+" sur "+peripherique+" avec un débit de baud de "+str(debit)+" et un timeout de "+str(timeout))
        if parite != None:
            exec("parite = serial."+parite)
        try:
            threading.Thread.__init__(self, name=nom, target=self.lire)
            self.active = True
            if parite == None:
                serial.Serial.__init__(self, peripherique, debit, timeout=timeout)
            else:
                serial.Serial.__init__(self, peripherique, debit, target=self.lire, timeout=timeout, parity=parite)
        except:
            self.active = False
            log.logger.error("Erreur d'initialisation de la liaison série threadée "+nom+" sur "+peripherique+" avec un débit de baud de "+str(debit)+" et un timeout de "+str(timeout))
            self.stop()

    def ecrire(self, msg):
        """
        Écrire une information vers un périphérique puis retourner à la ligne
        
        :param msg: message à donner au périphérique
        :type msg: string
        :return: Nombre de caractères envoyés
        :rtype: int
        """
        msg = msg.split()
        liste_number = []
        for i in msg:
            if i.isdigit(): 
                liste_number.append(i) # on place les nombres dans une liste
            else:
                log.logger.debug("Écrire sur la liaison série "+self.nom+" : "+i)
                return self.write(i+"\r\n") # on écrit la chaine
        for i in liste_number: # écriture des nombres, mais ça reste des strings
            log.logger.debug("Écrire sur la liaison série "+self.nom+" : "+i)
            return self.write(i+"\r\n")
    
    def lire(self):
        """
        Lire une information venant d'un périphérique jusqu'au retour à la ligne
        
        :return: Chaîne lue
        :rtype: string
        """
        while self.active:
            lu = self.readline()
            lu = lu.split("\r\n")[0]
            if lu != '':
                log.logger.debug("Lecture sur la liaison série "+self.nom+" : "+lu)
                self.file_attente.put(lu)
    
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
