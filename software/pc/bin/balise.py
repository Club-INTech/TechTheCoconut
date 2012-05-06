import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import lib.balise
import lib.visualisation
from threading import Thread

vTable = lib.visualisation.Visu_table()
vTable.start()
balise = lib.balise.Balise(vTable)
t = Thread(target=balise.tracker_robot_adverse)
t.start();