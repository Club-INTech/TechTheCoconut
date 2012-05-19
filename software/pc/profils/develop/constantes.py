# -*- coding: utf-8 -*-

"""
* constantes["Coconut"]["largeur"] Largeur en mm
* constantes["Coconut"]["longueur"] Longueur en mm
"""
constantes = \
{
	"Coconut":
	{
		#: Largeur de la table en mm
		"largeur": 3000,
		#: Longueur de la table en mm
		"longueur": 2000,
		
		#longueur d'un bras
		"longueurBras" : 180.,
		
		#sans compter les bras
		"largeurRobot" : 200.,
		"longueurRobot" : 360.,
	},
	"Anna": {},
    "Objets_Table": {
        "rayon_disque":             60,
        "longueur_totem":           250,
        "largeur_totem":            250,
        "hauteur_totem":            163,
        "longueur_lingot":          150,
        "largeur_lingot":           70,
        "largeur_regletteEnBois":   18,
        "rayon_palmier":            20
    },
	"Logs":
	{
		"logs": True,
		"logs_level": "DEBUG",
		# 	%(processName)s pour ajouter nom du processus
		# le :: est volontaire, le nom du module sera inséré par la suite du programme
		"logs_format": "%(asctime)s::%(levelname)s:l%(lineno)d:%(threadName)s:%(message)s",
		"stderr": True,
		"stderr_level": "INFO",
                # le :: est volontaire, le nom du module sera inséré par la suite du programme
		"stderr_format": "%(asctime)s::%(levelname)s:l%(lineno)d:%(threadName)s:%(message)s",
		"dossier": "logs"
	},
	"Recherche_Chemin":
    {
        #rayon maximal du cercle circonscrit aux robots adverses, en mm
        "rayonRobotsA" : 200.,
        #approximation hexagonale des robots adverses
        "nCotesRobotsA" : 6
    },
    "Serie":
    {
        "peripheriques": {
            "asservissement": 9600,
            "capteur_actionneur": 57600,
            "balise": 9600,
        },
        "peripheriques_association": {
            "asservissement": "^([0-9]{4}(\+|-)[0-9]{4}|0)$",
            "capteur_actionneur": "^1$",
            "balise": "^2$",
            "actionneur": "^4$",
        },
    },
    "DureeJeu": 89,
    "Strategie": 1, # profil de stratégie    
    "Actionneurs":
    {
        "angleMax": 160,
        "angleMin": 0,
        
    },
    "Tests_mecha":
    {
        "batterie_test": True,
        "batterie_contraintes":
        {
            "pourcentage_min": 10,
            "minutes_min": 20,
        },
        "actionneurs_test": True,
        "deplacement_test": True,
        "recalage_test": True,
        "capteurs_test": True,
    },
    "Lolilol":
    {
        "musique_active": True,
        "musique_dossier": "/home/netantho/intech/multimedia_lolilol/",
    },
}
