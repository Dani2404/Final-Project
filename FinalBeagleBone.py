import os 
import subprocess
import time
import serial
import Adafruit_DHT
import datetime
import json
import sys

led0_off = 'echo 0 > /sys/class/leds/beaglebone:green:usr0/brightness'
led0_on = 'echo 1 > /sys/class/leds/beaglebone:green:usr0/brightness'
led1_off = 'echo 0 > /sys/class/leds/beaglebone:green:usr1/brightness'
led2_off = 'echo 0 > /sys/class/leds/beaglebone:green:usr2/brightness'
led3_off = 'echo 0 > /sys/class/leds/beaglebone:green:usr3/brightness'

os.system(led1_off)
os.system(led0_off)
os.system(led2_off)
os.system(led3_off)

path = '/home/debian/jsonFiles'
CheckConnection = 'ping -q -w 1 -c 1 `ip r | grep default | cut -d \ ' ' -f 3` > /dev/null && echo ok || echo error'
i=0
isData = 0
Connection = True
TimeDateUpdate = False
FirstInteration = True

ser = serial.Serial(
	port = "/dev/ttyUSB0",
	baudrate = 9600,
	bytesize = serial.EIGHTBITS, 
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE, 
	timeout = 1,
	xonxoff = False,
	rtscts = False,
	dsrdtr = False,
	writeTimeout = 2
)

ser.isOpen()

def GetTempAndHumidity():

	sensor = Adafruit_DHT.DHT22
	pin = 'P8_11'
	i = 0
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	while humidity is None and temperature is None:
		pass

	return(humidity, temperature)

while True:

	os.system(led0_on)
	TimeDateSt = time.strftime("%Y%m%d-%H%M%S")
	TimeSt = time.strftime("%H%M%S")
	DateSt = time.strftime("%Y%m%d")

	if os.path.exists('/home/debian/FullSystemLog.txt') == False:
		with open('/home/debian/FullSystemLog.txt', 'w') as log:
			log.sclose()

	with open('/home/debian/FullSystemLog', 'a') as log:
		if FirstInteration == True:
			log.write("FileManagement.py started at: {0}\n".format(TimeDateSt))
			FirstInteration = False
		else:
			log.write("{0}\n".format(TimeDateSt))


	# while TimeDateUpdate == False:		
	# 	result = subprocess.check_output(CheckConnection, shell=True)
	# 	print("Connection:{0}".format(result))
	# 	if result == "ok\n":
	# 		subprocess.call('sudo service ntp stop', shell=True)
	# 		subprocess.call('sudo ntpd -q', shell=True)
	# 		subprocess.call('sudo service ntp start', shell=True)
	# 		TimeDateUpdate = True
	# 		print("Time and Date Updated")


	Input = "RAT"
	ser.write(Input +'\r\n')
	output = ''

	time.sleep(1)

	while ser.inWaiting() > 0:
		x = ser.read(1)
		if x == '\r':
			break
		output += x

	ser.flushOutput()

	if len(output) == 32: 
		print "success [" + output + "]"
		print output[0:3]
		print output[4:1]

		CountryCode = output[0:3]
		TagID = output[4:15]
		print("Country Code: {0}".format(CountryCode))
		print("Tag ID: {0}\n".format(TagID))
		isData = 1
		humid, temp = GetTempAndHumidity()

		data = {
				'Time' : TimeSt,
				'Date' : DateSt,
				'Temp' : temp,
				'Humidity' : humid,
				'Country Code' : CountryCode,
				'RFID TAG' : TagID
				}

		if os.listdir("/home/debian/jsonFiles") == []:
			i = 0


		while os.path.exists("/home/debian/jsonFiles/JSON_DATA%s.json" % i):
			i = i + 1

		with open("/home/debian/jsonFiles/JSON_DATA%s.json" % i, 'w') as f: 
		#with open("/home/debian/jsonFiles/JSON_DATA%s.json" %timeSt, 'a') as f:
			json.dump(data, f, indent = 2)
			#print("/home/debian/jsonFiles/JSON_DATA%s.json" % i)
	else:
		print "searching"

	while len(os.listdir(path)) != 0 and Connection == True:
		FilePath = "/home/debian/jsonFiles/JSON_DATA{0}.json".format(i)
		if os.path.isfile(FilePath):
			#print("Here");
			#subprocess--> ssh to pi using bash as more simpleS
			exit_Code = subprocess.call('sudo sshpass -p "drowssap76243" scp -o StrictHostKeyChecking=no  %s  pi@82.21.211.11:Dani/jsonFiles' %FilePath, shell=True)
			#subprocess.check_call("sshpass -p \"drowssap76243\" scp -o StrictHostKeyChecking=no  /home/debian/jsonFiles/JSON_DATA0.json pi@82.21.211.11:/home/pi/Dani/jsonFiles", shell=True)
			if exit_Code == 0:
				print ("Sent")
				os.remove(FilePath)
				print("Deleted")
				Connection = True
			else:
				print("unable to send")
				Connection = False				
		i =  i + 1

	i = 0

	result = subprocess.check_output(CheckConnection, shell=True)
	if result == "ok\n":
		Connection = True
	else:
		Connection = False


	os.system(led0_off)
		  
