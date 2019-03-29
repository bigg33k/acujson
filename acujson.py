#!/usr/bin/python
import json
import sys
import graphyte
graphyte.init('192.168.1.136', prefix='acurite')


data = []

with open('acu.json') as f:
    lines = f.readlines()
    for line in lines[-10:]:
	data.append(json.loads(line))
    #line = (list(f)[-1])

    #data.append(json.loads(line))

    for item in data:
        #print item
        try:
            pass
            print ('id.' + str(item["id"]))
            id = str(item["id"])
            if item['id'] != -149:
                print ( id + ':temperature_C: ' + str(item["temperature_C"]))
                temperature_H = 9.0/5.0 * item["temperature_C"] + 32
                graphyte.send(id + '.temperature_C',item["temperature_C"])
                print ( id + ':temperature_H: ' + str(temperature_H))
                graphyte.send(id + '.temperature_H', temperature_H)
		try:
                	print ( id + ':humidity: ' + str(item["humidity"]))
                	graphyte.send(id + '.humidity',item["humidity"])
                	print ( id + ':battery_low: ' + str(item["battery_low"]))
                	graphyte.send(id + '.battery_low',item["battery_low"])
		except:
			pass
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
