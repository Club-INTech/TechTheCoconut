# -*- coding: utf-8 -*-

"""
* constantes["Coconut"]["largeur"] Largeur en mm
* constantes["Coconut"]["longueur"] Longueur en mm
"""
constantes = \
{
    "Coconut":
    {
        #: Largeur en mm
        "largeur": 3000,
        #: Longueur en mm
        "longueur": 2000,
        
        #longueur du coté du robot, en mm
        "coteRobot" : 350.,        
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
        #   %(processName)s pour ajouter nom du processus
        "logs_format": "%(asctime)s:%(name)s:%(levelname)s:%(threadName)s:l%(lineno)d:%(message)s",
        "stderr": True,
        "stderr_level": "WARNING",
        "stderr_format": "%(asctime)s:%(name)s:%(levelname)s:%(message)s",
        "dossier": "logs"
    },
    "Recherche_Chemin":
    {
        #rayon maximal du cercle circonscrit aux robots adverses, en mm
        "rayonRobotsA" : 350.,
        #approximation hexagonale des robots adverses
        "nCotesRobotsA" : 6
    },
        "Serie":
        {
            "peripheriques": ["actionneur", "asservissement", "capteur"]
        }
}