#!/usr/bin/python

import sys
import os
import time

from SOAPpy import SOAPProxy

url = 'http://localhost/FruityWifi/wsdl/FruityWifi.php?wsdl'

namespace = 'urn:FruityWifi'
server = SOAPProxy(url, namespace)

args=sys.argv[1:]

if len(args) > 0:
	if args[0] == "start":
		print server.moduleAction('mod_dnsspoof','start')
		msg = "DNSspoof Enabled"
	else:
		print server.moduleAction('mod_dnsspoof','stop')
		msg = "DNSspoof Disabled"

	mod_logs = "/usr/share/FruityWifi/logs/rpitwit.log"
	os.system("echo '" + time.strftime("%Y-%m-%d %X") + " - "+msg+"' >> " + mod_logs)
	os.system("twitter --oauth /usr/share/FruityWifi/conf/rpitwit_twitter_oauth set '" + msg + " (" + time.strftime("%Y-%m-%d %X") + ")'")
