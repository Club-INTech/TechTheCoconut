# -*- coding: utf-8 -*-

import __builtin__
import instance
asser = __builtin__.instance.asserInstance

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