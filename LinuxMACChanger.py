#!/usr/bin/env python

import subprocess
import optparse

parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="Interface",
                  help="name the interface to change its MAC address")
parser.add_option("-m", "--mac", dest="Custom_MAC",
                  help="new custom MAC address")

(options, args) = parser.parse_args()

Interface = options.Interface
Custom_MAC = options.Custom_MAC

print("""
             [+] Linux Mac Changer [+]
          
        ======================================= 
        [+] Programmed By : Falcon Clutch     |+
        [+] Instagram: falcon71181            |+
        [+] Youtube: Falcon Clutch            |+
        [+] Github : falcon71181              |+
        =======================================
        """)

subprocess.call("ifconfig " + Interface + " down", shell=True )
subprocess.call("ifconfig " + Interface + " hw ether " + Custom_MAC, shell=True )
subprocess.call("ifconfig " + Interface + " up " , shell=True )
