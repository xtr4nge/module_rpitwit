#!/usr/bin/python

import sys
import os
import time

from SOAPpy import SOAPProxy

url = 'http://localhost/FruityWifi/wsdl/FruityWifi.php?wsdl'

namespace = 'urn:FruityWifi'
server = SOAPProxy(url, namespace)

args=sys.argv[1:]

#twitter set FruityWifi Wireless Enabled!
#os.system("twitter set FruityWifi Wireless Enabled")

if len(args) > 0:
	if args[0] == "start":
		print server.serviceAction('s_wireless','start')
		msg = "Wireless Enabled"
	else:
		print server.serviceAction('s_wireless','stop')
		msg = "Wireless Disabled"

	mod_logs = "/usr/share/FruityWifi/logs/rpitwit.log"
	os.system("echo '" + time.strftime("%Y-%m-%d %X") + " - "+msg+"' >> " + mod_logs)
	os.system("twitter --oauth /usr/share/FruityWifi/conf/rpitwit_twitter_oauth set '" + msg + " (" + time.strftime("%Y-%m-%d %X") + ")'")
