# -*- coding: utf-8 -*-

"""
Gère l'association automatique des périphériques
"""

import sys
import os
import serial
import serie_simple
import re


sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lib.peripherique
log = lib.log.Log(__name__)



class Detection_peripheriques():
    """
    Classe qui gère l'association automatique des périphériques
    """
    def __init__(self):
        self.associer()
    
    def associer(self):
        """
        Associer un périphérique USB physique à son chemin sur Linux
        """
        commande = 'ls -1 /dev/ttyUSB* 2> /dev/null'
        chemins = os.popen(commande)
        chemins = chemins.readlines()
        
        chemin_existant = []
        for peripherique in constantes["Serie"]["peripheriques"].keys():
            for chemin in chemins:
                chemin_existant = []
                for p in lib.peripherique.liste:
                    chemin_existant.append(p.chemin)
                if chemin not in chemin_existant:
                    chemin = chemin.split('\n')[0]
                    serie = serie_simple.SerieSimple(chemin, constantes["Serie"]["peripheriques"][peripherique], 0.1)
                    # On envoie plusieurs fois au cas où
                    for i in xrange(3):
                        try:
                            serie.ecrire('?')
                        except:
                            pass
                    # Boucle pour gérer les exceptions
                    for i in xrange(3):
                        chemin_existant = []
                        for p in lib.peripherique.liste:
                            chemin_existant.append(p.chemin)
                        try:
                            ping = -1
                            for i in xrange(10):
                                ping = serie.lire()
                                #print "p"+ping+"p", constantes["Serie"]["peripheriques_association"][peripherique]
                                if re.match(constantes["Serie"]["peripheriques_association"][peripherique], ping):
                                    p_obj = lib.peripherique.Peripherique(peripherique)
                                    p_obj.chemin = chemin
                                    lib.peripherique.liste.append(p_obj)
                                    log.logger.info("Périphérique "+peripherique+" associé au chemin "+chemin)
                                    break
                            serie.close()
                        except:
                            log.logger.error("Erreur de l'association sur "+peripherique+" avec le chemin "+chemin+", on recommence ...")