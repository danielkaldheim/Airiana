#!/usr/bin/python

import os, time
import mail
mailer = mail.Smtp()
if  not os.path.lexists("/home/pi/airiana/RAM/status.html"):
	os.system("touch /home/pi/airiana/RAM/status.html" )
def init():
	from users import users
	global users
	global status
	global mail_sent
	status = {}
	mail_sent = {}

	for each in users.keys():
		status[each]= 0

	for each in users.keys():
		mail_sent[each] = False
init()
os.chdir("/home/pi/airiana")
os.system("./alive_logger.py &")
files = os.listdir("./public/local_links/")

#for each in users.keys():
#	print each, ": ",users[each]
while True:
    try:
		users_prev = users
		from users import users
		if users_prev <> users:
			init()
		html = "<html>STATUS VIEW AIRIANA SYSTEMS<br><table><tr><th>Name</th><th>Ping</th><th>Status</th></tr>"
		flag = "unknown"
		files = os.listdir("./public/local_links/")
		for each in files:
			try:
				mod = os.stat(str("./public/local_links/"+each)).st_mtime
				content = os.popen("cat ./public/local_links/"+each).read()
				stat_field = content.split("status:")[-1]
				print stat_field
				if content.find("status")!=-1 :exec  ("lis ="+stat_field)
				else: lis =[]
				#print status[str(each.split(".")[0])], each
				if (time.time()-mod)/3600>status[str(each.split(".")[0])]:
					status[str(each.split(".")[0])] = round((time.time()-mod)/3600,2)
				status[str(each.split(".")[0])] =status[str(each.split(".")[0])]*0.99
				if (time.time()-mod)/3600<3:
					flag = "<font color=\"green\"> Alive </font>"
					if  mail_sent[each.split(".")[0]]:
                                                mail_sent[each.split(".")[0]] = False
                                                mailer.setup ("daniel.halling@outlook.com","airiana@abiding.se","Airiana user: "+str(users[str(each.split(".")[0])])+" has checked in and is now alive.")
                                                mailer.send()
				else: 
					flag = "<font color=\"red\"> Inactive </font>"
					if not mail_sent[each.split(".")[0]]:
						mail_sent[each.split(".")[0]] = True
						mailer.setup ("daniel.halling@outlook.com","airiana@abiding.se","Airiana user: "+str(users[str(each.split(".")[0])])+" has changed status to inactive.")
						mailer.send()
				html += "<tr><td><a href=\"/local_links/"+each+"\">"+users[str(each.split(".")[0])]+"</a></td><td>"+time.ctime(mod)+"</td><td>"+flag+" "+str(round(status[str(each.split(".")[0])],2))+" "+str(lis)+" </td></tr>\n" 
			except KeyError:
 				html += "<tr><td><a href=\"/local_links/"+each+"\">"+each+"</a></td><td>"+time.ctime(mod)+"</td><td>"+flag+" </td></tr>\n" 

		html +="<br></table></html>"
		file = open("/home/pi/airiana/RAM/status.html","w+")
		file.write(html)
		file.close()
		time.sleep(60)
    except KeyboardInterrupt: break 
