#!/usr/bin/python
import json
import time
import sys
import socket
import requests
from requests.structures import CaseInsensitiveDict
hostname =(socket.gethostname())

start = time.time()

auth_token = '161384:eyJrIjoiMTI4MDViMjJhMjM1NmVkMzk3NzMxNmE3NjJjNDFhM2Y2N2ZlYTI0ZSIsIm4iOiJncmFwaGl0ZSIsImlkIjoyMzkxMDJ9'
header = {'Authorization': 'Bearer ' + auth_token,  'Content-Type': 'application/json'}
data = []
payload = []
id = "0"

with open('acu.json') as f:
    lines = f.readlines()
    for line in lines[-20:]:
	data.append(json.loads(line))

    for item in data:
	try:
		id = str(item["sid"])
	except:
		id = str(item["id"])

	if (id != ""):
                temperature_H = 9.0/5.0 * item["temperature_C"] + 32
		temperature_C = item["temperature_C"]
		try:
			humidity = item["humidity"]
		except:
			pass
                try:
			battery_low = item["battery_low"]
		except:
			battery_low = 0
			pass
		try:
			battery_low = item["battery"]
                except:
			battery_low = 0
			pass
		try:
			moisture = item["moisture"]
		except:
			moisture = 0
			pass
		payload.append (
			 {
				'hostname' : hostname,
				'id': id,
				'temperature_H': temperature_H,
				'temperature_C': temperature_C,
				'moisture' : moisture,
				'battery_low' : battery_low,
			 }
		)
		print(payload)
		r = requests.post("https://graphite-us-central1.grafana.net/metrics", json=payload, headers=header)
		print r
		if r.status_code != 200:
			raise Exception(r.text)
    			print('%s: %s' % (r.status_code, r.text))

		payload=[]
