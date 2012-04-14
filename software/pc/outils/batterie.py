import os
import sys
import re

cmd = 'acpi'
p = os.popen(cmd)
string = p.readline().replace('\n', '')

# Battery 0: Discharging, 24%, 00:28:54 remaining\n
pourcentage = re.findall('[0-9]+%', string)[0]
pourcentage = pourcentage.replace('%', '')
temps_restant = re.findall('[0-9]{2}:[0-9]{2}:[0-9]{2}', string)

print pourcentage
print temps_restant

if temps_restant:
    temps_restant = temps_restant[0]
    temps_restant = temps_restant.split(':')

    if int(pourcentage) <= 900:
        print "Pourcentage"
        f = file('/tmp/acpi', 'w')
        f.write(string)
        f.close()
        os.popen('wall < /tmp/acpi')
    if int(temps_restant[0]) == 0 and int(temps_restant[1]) <= 15:
        print "temps restant"
        f.write(string)
        f.close()
        os.popen('wall < /tmp/acpi')
    if temps_restant[0] == 0 and temps_restant[1] <= 15:
        print "temps restant"
