# -*- coding: utf-8 -*-

import log

import sys
import os
import serial
import serie_simple

log = log.Log(__name__)

liste = []

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# commande : '# ls -1 /dev/ttyUSB* 2> /dev/null'

def chemin_de_peripherique(periph):
    for p in liste:
        if p.nom == periph:
            return p.chemin
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
        
        Les numéros retournés par les AVR sont
        asservissement : 0
        capteur_actionneur : 1
        laser : 2
        
        :return: Succès ou échec de l'association du périphérique
        :rtype: bool
        """
        peripheriques_commande = 'ls -1 /dev/ttyUSB* 2> /dev/null'
        while 42:
            peripheriques = os.popen(peripheriques_commande)
            #print "Associer "+self.nom+" à "
            #print "0. Ne pas associer"
            i = 1
            #association = {}
            peripheriques = peripheriques.readlines()
            if not peripheriques:
                log.logger.error("Il n'y a plus de chemin pour le périphérique "+self.nom)
                return False
              
            # début Ancien système, on demande l'association à l'utilisateur
            #for chemin in peripheriques:
                #chemin_existant = False
                ## On veut enlever les \n finaux
                #chemin = chemin.split('\n')[0]
                ## Si le périphérique n'est pas déjà associé
                #chemins_existants = []
                #for p_existant in liste:
                    #if chemin == p_existant.chemin:
                        #chemin_existant = True
                    #chemins_existants.append(p_existant.chemin)
                ## On demande le chemin
                #if not chemin_existant:
                    #print str(i)+". "+chemin
                    #association[i] = chemin
                    #i+=1
            #numero = raw_input("numéro : ")
            #if numero == '':
                #log.logger.info("Périphérique "+self.nom+" ")
                #return False
            #try:
                #numero = int(numero)
            #except:
                #continue
            #if numero == '' or numero == 0:
                #log.logger.info("Périphérique "+self.nom+" volontairement non associé")
                #return False
            #elif numero in association.keys():
                #self.chemin = association[numero]
                #log.logger.info("Chemin "+self.chemin+" associé au périphérique "+self.nom)
                #return True
            #else:
                #log.logger.warning("Numéro "+str(numero)+" inconnu dans l'association du périphérique "+self.nom)
            # fin Ancien système
            
            # Association automatique
            # Doit correspondre à profil.prod.constantes et profil.develop.constantes
            association = []
            association.append('asservissement')
            association.append('capteur_actionneur')
            association.append('balise')
            chemin_existant = []
            for baudrate2 in [9600, 57600]:
                for chemin in peripheriques:
                    if chemin not in chemin_existant:
                        chemin = chemin.split('\n')[0]
                        serie = serie_simple.SerieSimple(chemin, baudrate2, 0.5)
                        # On envoie plusieurs fois au cas où
                        try:
                            serie.ecrire('?')
                        except:
                            pass
                        try:
                            serie.ecrire('?')
                        except:
                            pass
                        try:
                            serie.ecrire('?')
                        except:
                            pass
                        # Boucle pour gérer les exceptions
                        for i in xrange(3):
                            chemin_existant = []
                            for p in liste:
                                chemin_existant.append(p.nom)
                            try:
                                ping = serie.lire()
                                if association[int(ping)] == self.nom:
                                    self.chemin = chemin
                                    liste.append(self)
                                    serie.close()
                                    log.logger.info("Périphérique "+self.nom+" associé au chemin "+chemin)
                                    return True
                                serie.close()
                            except:
                                log.logger.error("Erreur de l'association sur "+self.nom+" avec le chemin "+chemin+", on recommence ...")

            log.logger.error("Périphérique "+self.nom+" non associé")
            return False