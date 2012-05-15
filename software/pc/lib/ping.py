# -*- coding: utf-8 -*-

import __builtin__
import instance
import time
asser = __builtin__.instance.asserInstance
"""
while True :
    a = raw_input(":")
    if (a=="q"):
        print asser.serialInstance.readline()
    elif (a== "n"):
        asser.serialInstance.write("\n")
    elif (a== "r"):
        asser.serialInstance.write("\r")
    elif (a== "z"):
        asser.serialInstance.write("\0")
    else:
        asser.serialInstance.write(a)
"""

def ping():
    
    while True:
        
        com = raw_input("?")
        if com == "q":
            break
        if com == "d":
            asser.serieAsserInstance.ecrire("d")
            asser.serieAsserInstance.ecrire("200")
            for i in range(50):
                asser.serieAsserInstance.ecrire("acq")
                print str(i)+">"+str(asser.serieAsserInstance.lire())+"<"
        if com == "":
            for i in range(50):
                asser.serieAsserInstance.ecrire("acq")
                print str(i)+">"+str(asser.serieAsserInstance.lire())+"<"
                    
    
    """
    while True:
        asser.serieAsserInstance.ecrire("pos")
        print "x : >"+str(asser.serieAsserInstance.lire())+"<"
        print "y : >"+str(asser.serieAsserInstance.lire())+"<"
        #time.sleep(0.03)
    """
    """
    while True:
        com = raw_input("?")
        if com == "p":
            while True:
                print asser.getPosition()
        if com == "o":
            while True:
                print asser.getOrientation()
        if com == "q":
            break
    """