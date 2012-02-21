# -*- coding: utf-8 -*-

import serie
import log

import os

log = log.Log()

liste = []

# commande : '# ls -1 /dev/ttyUSB* 2> /dev/null'

def chemin_de_peripherique(periph):
    for p in liste:
        if p.nom == periph:
            return periph
    log.logger.error(periph+" n'est pas relié à un chemin sur Linux")
    return None

class Peripherique():
    """
    Classe de gérer un périphérique, notamment permet d'associer un périphérique physique à son chemin sous Linux
    
    :param nom: Nom du périphérique
    :type nom: string
    """
    def __init__(self, nom):
        self.nom = nom
        self.chemin = None
        log.logger.info("Nouveau périphérique "+self.nom)
        self.association = self.associer()
    
    def associer(self):
        """
        Associer un périphérique USB physique à son chemin sur Linux
        
        :return: Succès ou échec de l'association du périphérique
        :rtype: bool
        """
        peripheriques_commande = 'ls -1 /dev/ttyUSB* 2> /dev/null'
        while 42:
            peripheriques = os.popen(peripheriques_commande)
            print "Associer "+self.nom+" à "
            print "0. Ne pas associer"
            i = 1
            association = {}
            peripheriques = peripheriques.readlines()
            if not peripheriques:
                log.logger.error("Il n'y a plus de chemin pour le périphérique "+self.nom)
                return False
            for chemin in peripheriques:
                chemin_existant = False
                # On veut enlever les \n finaux
                chemin = chemin.split('\n')[0]
                # Si le périphérique n'est pas déjà associé
                chemins_existants = []
                for p_existant in liste:
                    if chemin == p_existant.chemin:
                        chemin_existant = True
                    chemins_existants.append(p_existant.chemin)
                # On demande le chemin
                if not chemin_existant:
                    print str(i)+". "+chemin
                    association[i] = chemin
                    i+=1
            #log.logger.warning(association)
            numero = int(raw_input("numéro : "))
            if numero == 0:
                log.logger.info("Périphérique "+self.nom+" volontairement non associé")
                return False
            elif numero in association.keys() or numero:
                self.chemin = association[numero]
                log.logger.info("Chemin "+self.chemin+" associé au périphérique "+self.nom)
                return True
            else:
                log.logger.warning("Numéro "+numero+" inconnu dans l'association du périphérique "+self.nom)