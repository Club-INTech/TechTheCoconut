# -*- coding: utf-8 -*-

import os
import shutil
import glob
import lib.conf
import __builtin__


# Chargement de la couleur du robot
first = True
while first or couleur not in ['', 'R', 'V']:
    first = False
    couleur = raw_input('Couleur de notre robot rouge ou violet ([V], R) : ')
    if couleur == '' :
        couleur = 'V'
    
# Chargement du profil de configuration
first = True
while first or not profil.importation:
	first = False
	conf = raw_input('Indiquer la configuration a importer (prod, [develop], developSimulUc) : \n')
	
	#tronque la string conf pour éviter les bugs à l'import
	conf = conf.split('.')
	for i in conf:
            if i == 'prod':
                conf = 'prod'
            elif i == 'develop':
                conf = 'develop'
            elif i == 'developSimulUc':
                conf = 'developSimulUc'
            elif i == '':
                conf = 'develop'
    
        profil = lib.conf.Conf(conf)
	
	
# Chargement des constantes en variable globale
exec('import profils.'+conf+'.constantes')
exec('__builtin__.constantes = profils.'+conf+'.constantes.constantes')

__builtin__.constantes['couleur'] = couleur

# Initialisatoin des logs
import lib.log
log = lib.log.Log(__name__)

log.logger.info('Profil de configuration chargé : ' + conf)

log.logger.info('Injection des données de la carte')
exec('import profils.'+conf+'.injection.elements_jeu')

if conf == 'develop':
    exec('import profils.'+conf+'.injection.robot')
else:
    exec('import profils.'+conf+'.injection')

import lib.peripherique

# Association des périphériques
for p in constantes['Serie']['peripheriques']:
    p_obj = lib.peripherique.Peripherique(p)
    if p_obj.association:
        lib.peripherique.liste.append(p_obj)
# Fin association des périphériques

first = True
erreur = False
while first or erreur:
    mode = raw_input('Indiquer le mode de lancement (autonome, [console], visualisation_table, e (etalonnage_constantes)) : \n')
    first = False
    #try:
    if mode == '':
        mode = 'console'
    if mode == 'e':
        mode = 'etalonnage_constantes'
    log.logger.info("Chargement du fichier de lancement " + mode)
    exec('import bin.'+ mode)
    if mode == "visualisation_table":
        first = True
    #except:
        #log.logger.warning("Le mode '" + mode + "' n'a pas pu etre charge")
        #erreur = True
