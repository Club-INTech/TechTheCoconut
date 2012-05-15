import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lib.balise
import lib.visualisation
from threading import Thread
import __builtin__

vTable = lib.visualisation.Visu_table(__builtin__.instance)
balise = __builtin__.instance.baliseInstance
balise.allumer()
#t = Thread(target=balise.tracker_robot_adverse)
#t.start();