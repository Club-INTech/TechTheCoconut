# -*- coding: utf-8 -*-

import sys
import os

# Ajout de ../ au path python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Conf:
	"""
	Classe permettant de gérer les profils de configuration
	
	:param profil: Profil de configuration
	:type profil: string
	"""
	def __init__(self, profil):
		self.importation = self.importer_profil(profil)

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