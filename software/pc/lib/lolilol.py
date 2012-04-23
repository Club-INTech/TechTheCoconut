# -*- coding: utf-8 -*-

import sys, os
import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import log
log = log.Log(__name__)

def son(fichier):
    s = Son(fichier)
    s.play()

class Son(object):
    def __init__(self, fichier, dossier=constantes['Lolilol']['musique_dossier']):
        self.actif = constantes['Lolilol']['musique_active']
        if not os.access(dossier+fichier, os.F_OK):
            self.actif = False
            #log.logger.error("Fichier de son "+dossier+fichier+" non trouvé")
        self.fichier = fichier
        self.dossier = dossier
        if self.actif:
            pygame.init()
            pygame.mixer.music.load(self.dossier+self.fichier)

    def play(self):
        if self.actif:
            pygame.mixer.music.play()

    def pause(self):
        if self.actif:
            pygame.mixer.music.pause()

    def stop(self):
        if self.actif:
            pygame.mixer.music.stop()