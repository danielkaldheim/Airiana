#!/usr/bin/python
#################################################################
#								#
#	Installation script for airiana system			#
#								#
#								#
#								#
#################################################################
#
#
# INSTALL BY CLONING#
# git clone https://github.com/beamctrl/airiana/
#
#################################################################
import os, sys
print "Installing the AirianaCores"
os.system("apt-get update")
dir = os.getcwd()
#MAKE RAM DRIVE IN FSTAB#
fstab_comment = "#temp filesystem only in RAM for use on Airiana tempfiles.\n"
fstab_cmd = "tmpfs "+dir+"/RAM tmpfs defaults,noatime,nosuid,mode=0755,size=50m 0 0\n"
# MAKE RAM DRIve for linux logs var/logs
fstab_cmd += "tmpfs /var/log tmpfs defaults,noatime,mode=0755,size=75m 0 0/n" 
# INSTALL DEPS#
os.system("apt-get -y install python-matplotlib")
os.system("pip install  minimalmodbus")
os.system("pip install  progressbar")
os.system("pip install requests")
os.system("pip install pyModbusTCP")
os.system("apt-get -y install ntp")
# NEED TO SET LOCALE
os.system("cp ./systemfiles/timezone /etc/")

boot_cmd="enable_uart=1\n"
boot_file = open("/boot/config.txt","rw+")
lines=boot_file.readlines()
if boot_cmd in lines: print "uart_enabled" 
else: 
	print "Enabling uart"
	boot_file.write(boot_cmd)
	boot_file.close()

fstab_file = open("/etc/fstab","rw+")
lines=fstab_file.readlines()
if fstab_comment in lines: print "fstab installed" 
else:
	 print "Setting up Ram drive"
	 fstab_file.write(fstab_comment)
	 fstab_file.write(fstab_cmd)
	 fstab_file.close()
#install system services for airaina and controller
if not os.path.lexist("/etc/systemd/system/airiana.service"):
	os.system("cp ./systemfiles/airiana.service /etc/systemd/system/")
if not os.path.lexist("/etc/systemd/system/controller.service"):
	os.system("cp ./systemfiles/controller.service /etc/systemd/system/")

os.system("systemctl enable airiana.service")
os.system("systemctl enable controller.service")
# redir console from uart
boot_cmd= "dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait"
os.system("echo " +boot_cmd+"> /boot/cmdline.txt" )
##
## setup airiana as host#
os.system ("cp ./systemfiles/hosts /etc/")
#Touch a data log file
os.system ("touch data.log.1")

os.chdir("./public/")
# link files to RAM-disk
os.system("ln -s ../RAM/out out.txt")
os.system("ln -s ../RAM/history.png history.png")
os.system("ln -s ../RAM/status.html status.html")
os.system("echo airiana > /etc/hostname")
os.system("chown pi:pi ../RAM/")
os.system("chown pi:pi ../RAM/*")
# setup updater.py for auto update
tmp  =os.popen("crontab -u pi -l").read()
os.system("echo \"" + tmp+ "0 */4 * * * sudo /usr/bin/python "+dir+"/updater.py\"|crontab -u pi -")

print "Installation completed, reboot in 15 sec"
os.system("sleep 15")
os.system("reboot")
