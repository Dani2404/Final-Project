import Adafruit_DHT
import time
import datetime
import json
import os
import subprocess
import csv

sensor = Adafruit_DHT.DHT22
pin = 'P8_11'
i = 0
fieldNames = ['humidity','temperature']

while(1):
# Example using a Raspberry Pi with DHT sensor
# connected to GPIO23.
#pin = 23
# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	if os.path.isfile('/home/debian/sensorData.csv') == False:
		with open('/home/debian/sensorData.csv', 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
			writer.writeheader()
			csvfile.close()

	while humidity is None and temperature is None:
		pass

	print(humidity)
	print(temperature)

	NewCSVData = [{'humidity' : str(humidity), 'temperature' : str(temperature)}]

	with open('/home/debian/sensorData.csv', 'a') as csvfile: 
		writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
		writer.writerows(NewCSVData)

		
