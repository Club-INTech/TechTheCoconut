# -*- coding: utf-8 -*-

import os
import lib.log
import lib.conf
first = True
while first or not profil.importation:
	first = False
	conf = raw_input('Indiquer la configuration a importer (prod, develop, developSimulUc) : \n')
	profil = lib.conf.Conf(conf)


exec('from profils.'+conf+'.constantes import constantes')

log = lib.log.Log(constantes['Logs']['logs'], constantes['Logs']['logs_level'], constantes['Logs']['logs_format'], constantes['Logs']['stderr'], constantes['Logs']['stderr_level'], constantes['Logs']['stderr_format'], constantes['Logs']['dossier'])

log.logger.info('Profil de configuration chargé : ' + conf)

mode = raw_input('Indiquer le mode de lancement (autonome, console) : \n')
try:
	log.logger.info("Chargement du fichier de lancement " + mode)
	exec('import bin.'+ mode)
except:
	log.logger.warning("Le mode '" + mode + "' n'a pas pu etre charge")



