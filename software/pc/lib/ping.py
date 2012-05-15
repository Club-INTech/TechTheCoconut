# -*- coding: utf-8 -*-

import __builtin__
import instance
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
    """
    asser.serieAsserInstance.ecrire("d")
    asser.serieAsserInstance.ecrire("200")
    while True:
        asser.serieAsserInstance.ecrire("acq")
        print ">"+str(asser.serieAsserInstance.lire())+"<"
    """
    while True:
        asser.serieAsserInstance.ecrire("pos")
        print "x : >"+str(asser.serieAsserInstance.lire())+"<"
        print "y : >"+str(asser.serieAsserInstance.lire())+"<"