# -*- coding: utf-8 -*-

import sys
import os

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class Conf:
    """
    Classe permettant de gérer les profils de configuration
    \n\n
    Pour charger les constantes :\n
    import __builtin__\n
    on a accès à la variable constante qui contient la variable constante des profils
    
    :param profil: Profil de configuration
    :type profil: string
    """
    def __init__(self, profil):
        self.importation = self.importer_profil(profil)
        if (self.importation):
            exec("import profils."+profil+".constantes")
            exec("self.constantes = profils.prod.constantes.constantes")

    def importer_profil(self, profil):
        """
        Charge un profil de configuration
        
        :param profil: Profil de configuration
        :type profil: string
        """
        try:
            exec("import profils."+profil)
            return True
        except:
            print "Erreur : profil de configuration "+profil+" inconnu"
            return False
