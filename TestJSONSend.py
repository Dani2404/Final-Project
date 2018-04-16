import time
import datetime
import json
import os
import subprocess
import csv

i = 0
n = 0
isEmpty = False
fieldNames = ['Data File Number', 'Time']

while(1):

	if os.path.isfile('/home/debian/TimeToSend.csv') == False:
		with open('/home/debian/TimeToSend.csv', 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
			writer.writeheader()
			csvfile.close()
			print("New CSV file created")

	if os.path.exists("/home/debian/jsonFiles/JSON_DATA%s.json" %i):
		isEmpty = False
		t0 = time.time()			
		subprocess.call('sudo sshpass -p "drowssap76243" scp -o StrictHostKeyChecking=no  /home/debian/jsonFiles/JSON_DATA%s.json  pi@82.21.211.11:Dani/jsonFiles' %i, shell=True)
		print ("Sent")
		os.remove("/home/debian/jsonFiles/JSON_DATA%s.json" %i)
		print("Deleted")
		t1 = time.time()
		TotalTime = t1-t0
		print("Time to send and delete:  {0}".format(TotalTime))

		NewCSVData = [{'Data File Number' : str(i), 'Time' : str(TotalTime)}]

		with open('/home/debian/TimeToSend.csv', 'a') as csvfile: 
			writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
			writer.writerows(NewCSVData)
			csvfile.close()

	elif os.listdir("/home/debian/jsonFiles") == []:
			print("Folder Empty")
			exit()
	i = i + 1