# -*- coding: utf-8 -*-

import sys
import os

# Ajout de ../ au path python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lib.conf

class TestConf:
	"""
	Classe permettant de tester la gestion des profils de configuration
	"""

	def test_importer_profil(self):
		"""
		Teste le chargement d'un profil de configuration effectué avec lib.conf.importer_profil
		"""
		def importer_profil_aux(profil):
			obj = lib.conf.Conf(profil)
			return obj.importation
		
		assert not importer_profil_aux("azertyty")
		assert not importer_profil_aux("develope")
		assert not importer_profil_aux("pro")
		
		# On ne doit pas pouvoir non plus importer juste un sous-module
		# TODO: corriger le bug
		#assert not importer_profil_aux("develop.injection")
		assert not importer_profil_aux("develop.tests")
		# TODO: corriger le bug
		#assert not importer_profil_aux("prod.injection")
		assert not importer_profil_aux("prod.tests")
		# TODO: corriger le bug
		#assert not importer_profil_aux("developSimulUc.injection")
		assert not importer_profil_aux("developSimulUc.tests")
		
		assert importer_profil_aux("develop")
		assert importer_profil_aux("developSimulUc")
		assert importer_profil_aux("prod")
