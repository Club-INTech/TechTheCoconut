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
	"Table": {
        "rayon_disque" = 150 #:TODO: Changer la valeur numérique
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