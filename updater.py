#!/usr/bin/python
import os, sys
os.chdir("/home/pi/airiana/")
os.system("sudo wget -q -O ./RAM/VERS http://lappy.asuscomm.com:443/current_version")
ver = os.popen("cat ./RAM/VERS").read()
ver = ver.split(" ")
tmp = os.popen("head airiana-core.py").readlines()
for each in tmp:
	if "vers" in each:
		temp = each.split("=")
		vers = temp[-1][2:-2]

if "debug" in sys.argv:
	print vers, "->", ver, "will update", vers not in ver[0]
if vers not in ver[0] and "Valid" in ver[1]:
	print "Updating Airiana system software to",ver[0]
        if "debug" not in sys.argv:
		os.system("./update&")  

