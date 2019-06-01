#!/usr/bin/python
import json
import time
import sys
import graphyte
import statsd
import socket
import syslog

start = time.time()
hostname =(socket.gethostname())
graphyte.init('192.168.1.136', prefix='acurite')
c = statsd.StatsClient('192.168.1.136', 8125, prefix='acu')

DEBUG = True
#DEBUG = False
data = []

with open('acu.json') as f:
    lines = f.readlines()
    for line in lines[-40:]:
	data.append(json.loads(line))


    for item in data:
        try:
	    syslog.syslog(str(item))
            pass
            if DEBUG:
		 print ('id.' + str(item["id"]))
            id = str(item["id"])
            if item['id'] != -149:
		if DEBUG:
                	print ( id + ':temperature_C: ' + str(item["temperature_C"]))
                temperature_H = 9.0/5.0 * item["temperature_C"] + 32
                graphyte.send(id + '.temperature_C',item["temperature_C"])
		if DEBUG:
                	print ( id + ':temperature_H: ' + str(temperature_H))
                graphyte.send(id + '.temperature_H', temperature_H)
		try:
			if DEBUG:
                		print ( id + ':humidity: ' + str(item["humidity"]))
                	graphyte.send(id + '.humidity',item["humidity"])
			if DEBUG:
                		print ( id + ':battery_low: ' + str(item["battery_low"]))
                	graphyte.send(id + '.battery_low',item["battery_low"])
		except:
			pass
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
# You must convert to milliseconds:
dt = int((time.time() - start) * 1000)
c.timing(hostname + '.runtime', dt)
c.incr(hostname + '.loglines' , len(lines))
