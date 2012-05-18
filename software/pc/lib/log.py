# -*- coding: utf-8 -*-

import os
import sys
import datetime
import logging

# Couleurs pour le fun et surtout pour ... le fun
def add_coloring_to_emit_ansi(fn):
    # add methods we need to the class
    def new(*args):
        levelno = args[1].levelno
        if(levelno>=50): # CRITICAL
            color = '\x1b[31m' # red
        elif(levelno>=40): # ERROR
            color = '\x1b[33m' # yellow
        elif(levelno>=30): # WARNING
            color = '\x1b[35m' # magenta
        elif(levelno>=20): # INFO
            color = '\x1b[32m' # green 
        elif(levelno>=10): # DEBUG
            color = '\x1b[36m' # cyan
        else: # NOTSET
            color = '\x1b[0m' # normal
        args[1].msg = color + args[1].msg +  '\x1b[0m'  # normal
        return fn(*args)
    return new

# Ne fonctionne pas sur Windows mais de toute façon on s'en balance de Windaube
logging.StreamHandler.emit = add_coloring_to_emit_ansi(logging.StreamHandler.emit)

class Log:
    """
    Classe permettant de gérer les logs\n\n
    
    Pour utiliser les logs dans vos fichiers :\n
    Pour charger le système de log correctement, en début de fichier ajoutez :\n
    import lib.log\n
    log = lib.log.Log(__name__)
    \n
    Puis vous pouvez logguer des messages avec (dans ordre croissant de niveau) :\n
    log.logger.debug('mon message')\n
    log.logger.info('mon message')\n
    log.logger.warning('mon message')\n
    log.logger.error('mon message')\n
    log.logger.critical('mon message')\n
    \n
    L'arborescence des fichiers de logs est : [annee]-[mois]-[jour]/[revision].log\n\n

    :param logs: Enregistrer dans les fichiers de log ?
    :type logs: bool
    :param logs_level: Enregistrer à partir de quel niveau de log ?
    :type logs_level: string 'DEBUG'|'INFO'|'WARNING'|'ERROR'|'CRITICAL'
    :param logs_format: Format des logs (voir http://docs.python.org/library/logging.html#logrecord-attributes). Ex : '%(asctime)s:%(name)s:%(levelname)s:%(message)s'
    :type logs_format: string
    :param stderr: Afficher les erreur dans le stderr ? (ie à l'écran)
    :type stderr: bool
    :param stderr_level: Afficher sur l'écran à partir de quel niveau de log ?
    :type stderr_level: string 'DEBUG'|'INFO'|'WARNING'|'ERROR'|'CRITICAL'
    :param stderr_format: Format d'affiche à l'écran (voir http://docs.python.org/library/logging.html#logrecord-attributes). Ex : '%(asctime)s:%(name)s:%(levelname)s:%(message)s'
    :type stderr_format: string
    :param dossier: Dossier où mettre les logs (à partir de la racine du code, c'est-à-dire le dossier contenant lanceur.py). Ex : 'logs'
    :type dossier: string
    """
    def __init__(self, nom, logs=constantes['Logs']['logs'], logs_level=constantes['Logs']['logs_level'], logs_format=constantes['Logs']['logs_format'], stderr=constantes['Logs']['stderr'], stderr_level=constantes['Logs']['stderr_level'], stderr_format=constantes['Logs']['stderr_format'], dossier=constantes['Logs']['dossier']):
        self.nom = nom
        if (logs != None and stderr != None and dossier != None):
            self.initialisation(logs, logs_level, logs_format, stderr, stderr_level, stderr_format, dossier)
        elif str(self.__init__.im_class) != "tests.log.TestLog":
            print >> sys.stderr, "Erreur : Veuillez donner des paramètres pour créer un objet Log"
            self.logger = logging.getLogger(self.nom)
            self.logger.setLevel(logging.DEBUG)
            self.stderr_handler = logging.StreamHandler()
            self.stderr_handler.setLevel(logging.WARNING)
            formatter = logging.Formatter("%(asctime)s:"+self.nom+":%(levelname)s:%(message)s")
            self.stderr_handler.setFormatter(formatter)
            self.logger.addHandler(self.stderr_handler)

    def initialisation(self, logs, logs_level, logs_format, stderr, stderr_level, stderr_format, dossier):
        """
        Initialise le système de log
        
        :param logs: Enregistrer dans les fichiers de log ?
        :type logs: bool
        :param logs_level: Enregistrer à partir de quel niveau de log ?
        :type logs_level: string 'DEBUG'|'INFO'|'WARNING'|'ERROR'|'CRITICAL'
        :param logs_format: Format des logs (voir http://docs.python.org/library/logging.html#logrecord-attributes). Ex : '%(asctime)s:%(name)s:%(levelname)s:%(message)s'
        :type logs_format: string
        :param stderr: Afficher les erreur dans le stderr ? (ie à l'écran)
        :type stderr: bool
        :param stderr_level: Afficher sur l'écran à partir de quel niveau de log ?
        :type stderr_level: string 'DEBUG'|'INFO'|'WARNING'|'ERROR'|'CRITICAL'
        :param stderr_format: Format d'affiche à l'écran (voir http://docs.python.org/library/logging.html#logrecord-attributes). Ex : '%(asctime)s:%(name)s:%(levelname)s:%(message)s'
        :type stderr_format: string
        :param dossier: Dossier où mettre les logs (à partir de la racine du code, c'est-à-dire le dossier contenant lanceur.py). Ex : 'logs'
        :type dossier: string
        :return: Statut de l'initialisation. True si réussite, False si échec
        :rtype: bool
        """
        dossier_racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dossier_abs = dossier_racine+"/"+dossier
        Log.dossier_logs = dossier
        Log.dossier_date = str(datetime.date.today())
        Log.stderr = stderr
        Log.logs = logs
        Log.stderr_level = stderr_level
        Log.logs_level = logs_level
        # On ajoute le nom du module
        Log.logs_format = ':'.join(map(lambda x: x if x else self.nom, logs_format.split(":")))
        # On ajoute le nom du module
        Log.stderr_format = ':'.join(map(lambda x: x if x else self.nom, stderr_format.split(":")))
        Log.levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        
        if (stderr and (stderr_level not in Log.levels)):
            print >> sys.stderr, "Erreur : stderr_level incorrect lors de la création d'un objet lib.log.Log"
            return False
        if (logs and (logs_level not in Log.levels)):
            print >> sys.stderr, "Erreur : logs_level incorrect lors de la création d'un objet lib.log.Log"
            return False
        
        # Création du logger
        self.logger = logging.getLogger(self.nom)
        self.logger.setLevel(logging.DEBUG)
        if stderr:
            # Ajout du handler pour stderr
            self.configurer_stderr()
        if logs:
            self.creer_dossier(dossier_abs)
            if not hasattr(Log, 'revision'):
                Log.revision = self.revision_disponible(dossier, Log.dossier_date)
            # Ajout du handler pour logs
            self.configurer_logs()
        # Création de l'entête dans stderr et logs
        self.ecrire_entete()
        Log.initialise = True
        return True
    
    def creer_dossier(self, dossier):
        """
        Crée un dossier si il n'existe pas déjà
        
        :param dossier: chemin vers le dossier à créer
        :type dossier: string
        :return: True si on a eu besoin de créer le dossier, False si il existait déjà
        :rtype: bool
        """
        if not os.access(dossier, os.F_OK):
            os.makedirs(dossier)
            return True
        return False

    def revision_disponible(self, dossier):
        """
        Donne la prochaine révision à créer dans les logs
        
        :param dossier: dossier principal des logs
        :type dossier: string
        :return: révision à créer
        :rtype: int
        """
        i = 0
        self.creer_dossier(dossier)
        while os.path.exists(dossier+"/"+str(i)+".log"):
            i += 1
        return i

    def ecrire_entete(self):
        """
        Crée l'entête dans les logs au niveau INFO
        """
        #self.logger.info("Début des logs")
        pass
    
    def configurer_logs(self):
        """
        Configure les logs (handler)
        """
        if hasattr(Log, 'logs_handler'):
            self.logger.removeHandler(Log.logs_handler)
        Log.logs_handler = logging.FileHandler(Log.dossier_logs+"/"+Log.dossier_date+"/"+str(Log.revision)+".log")
        exec("Log.logs_handler.setLevel(logging."+Log.logs_level+")")
        formatter = logging.Formatter(Log.logs_format)
        Log.logs_handler.setFormatter(formatter)
        self.logger.addHandler(Log.logs_handler)
    
    def configurer_stderr(self):
        """
        Configure la sortie stderr (handler)
        """
        if hasattr(Log, 'stderr_handler'):
            self.logger.removeHandler(Log.stderr_handler)
        Log.stderr_handler = logging.StreamHandler()
        exec("Log.stderr_handler.setLevel(logging."+Log.stderr_level+")")
        formatter = logging.Formatter(Log.stderr_format)
        Log.stderr_handler.setFormatter(formatter)
        self.logger.addHandler(Log.stderr_handler)
