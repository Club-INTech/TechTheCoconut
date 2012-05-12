# -*- coding : utf-8 -*-

ok = False

print "Nombre de bits du timer (8, 16, etc...)      : "
# Boucle de gestion d'erreur
while not ok :
    try :
        bits = input()
        ok = True
    except :
        pass
    
ok = False

print "Prescaler (1, 8, 64, 1024, etc...)           : "
while not ok :
    try :
        prescaler = input()
        ok = True
    except :
        pass

ok = False
print "Frequence du quartz (16000000, 20000000, ...): "
while not ok :
    try :
        quartz = input()
        ok = True
    except :
        pass

prescaler = float(prescaler)
quartz    = float(quartz)

print "Duree maximale d'un timer avant overflow : " + str(prescaler/quartz*2**int(bits))