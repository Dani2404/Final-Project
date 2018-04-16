import os 
import subprocess
import os.path
import json

# stuff
path = '/home/pi/Dani/jsonFiles'
finalJsonPath = '/home/pi/Dani/ALLJSON.json'
dataDir = '/home/pi/Dani/jsonFiles/';
blankjson = json.loads('{"data": []}')
timeout = 0
i = 0

# while forever
while True:

	# if these things are true
	if os.path.isfile(finalJsonPath) == False or os.path.getsize(finalJsonPath) == 0:
		
		# do this stuff
		print("Creating new file because it didn't exist")
		jsonfile = open(finalJsonPath,'w')
		jsonfile.write(json.dumps(blankjson))
		jsonfile.close()
		print("The file holds [" + json.dumps(blankjson) + "]")
		print("Created New File")

		# then stop doing stuff

	# until you get to here
	allJsonFile = open(finalJsonPath, 'r')
	allJsonObj = json.load(allJsonFile)

	# then for everything in there
 	for file in os.listdir(path):

 		# this
 		newJsonFile = open(dataDir + file, 'r')
		newJsonObj = json.load(newJsonFile)
		allJsonObj["data"].append(newJsonObj)
		print(file)
		print(i)
		os.remove(dataDir+file)
		newJsonFile.close()
		
		# remove this 
		i = i + 1

	# k wrapping things up now
	allJsonFile.close()
	allJsonFile = open(finalJsonPath, 'w')
	allJsonFile.write(json.dumps(allJsonObj))
	allJsonFile.flush()
	allJsonFile.close()

	# ignore that comment, that is just code I'm too lazy to remove
	# it really just does magic

	#Send Data to Raspberry Pi, if nothing to append
	#subprocess.call("bash /home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/Dani/ALLJSON.json BeagleBone/ALLJSON.json", shell=True)
	#print("Uploaded")	
	#Send Data to Raspberry Pi, if nothing to append
	subprocess.call("bash /home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/Dani/ALLJSON.json BeagleBone/ALLJSON.json", shell=True)
	print("Uploaded")
