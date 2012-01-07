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
		"largeur": 150,
		#: Longueur en mm
		"longueur": 350
	},
	"Anna": {},
	"Objets_Table": {
        "rayon_disque"      = 150,       #:TODO: Changer la valeur numérique
        "longueur_totem"    = 150,       #:TODO: Changer la valeur numérique
        "largeur_totem"     = 150,       #:TODO: Changer la valeur numérique
        "hauteur_totem"     = 150,       #:TODO: Changer la valeur numérique
        "longueur_lingot"   = 150,       #:TODO: Changer la valeur numérique
        "largeur_lingot"    = 150,       #:TODO: Changer la valeur numérique
        "regletteEnBois_largeur" = 200,  #:TODO: Changer la valeur numérique
        "regletteEnBois_longueur"= 200   #:TODO: Changer la valeur numérique
        
        },
	"Logs":
	{
		"logs": True,
		"logs_level": "DEBUG",
		"logs_format": "%(asctime)s:%(name)s:%(levelname)s:%(threadName)s:l%(lineno)d:%(message)s",
		"stderr": True,
		"stderr_level": "INFO",
		"stderr_format": "%(asctime)s:%(name)s:%(levelname)s:%(threadName)s:l%(lineno)d:%(message)s",
		"dossier": "logs"
	}
}