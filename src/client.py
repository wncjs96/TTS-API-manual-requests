# Typecast Typer with Sound 
# Note about typecast.ai: uses bearer token for authentication
 
# 1. post request to typecast.ai, make sure it's not a batch request, only consisting of 1 request.
# TODO: actor_id setup with at least 3 actors
# get text data from GUI

# 2. post request to typecast.ai, use the URL from the response to the first request.
# 3. GET batch request to typecast.ai, get the first object's audio data and play it using python third party library

import requests
import sys
import os
import json
# regex for string processing
import re
import logging
from dotenv import load_dotenv, find_dotenv
import pathlib

#TODO: speech_recognition for other commands?
import threading
import pygame 

def audio_play(filename):
	# Basically adding synchronization to the method.
	# thread-safe, multi thread (without worker) solution
	lock.acquire()
	pygame.mixer.music.load(filename)
	pygame.mixer.music.play()
	pygame.time.Clock().tick(10)
	lock.release()

# Global Variables
pygame.mixer.init()
lock = threading.Lock()

# Audio is generated using the two fields: Text and Selected index of voice actors
def generate_audio(text, count, voice):
	#voice = 'MIO'
	logging.info("Text received")
	# Testing - post post get
	url2 = 'https://typecast.ai/api/speak/batch/post'
	url3 = 'https://typecast.ai/api/speak/batch/get'

	# Bearer token - user specific store in env file 
	load_dotenv()
	bearer = os.getenv('BEARER_TOKEN')

	# Voice Actors GUID, Hashmap for performance
	actors = {"MIO":"5c3c52caea9791000747155c", "CHANGU": "5c547544fcfee90007fed455", "DUCKGU": "5c3c52c95827e00008dd7f34", "JAMMIN": "5ffda49bcba8f6d3d46fc447", "AHRI": "6047863af12456064b35354e", "DUCKHOO": "618203826672d21ebf37748e", "BORA": "618203f635ea62f8574c7d8a", "JIAN": "615c6a4e369566b08b8a7a71"}

	# Expected object from GUI.py
	# TODO: Change actors indexing and substitute text into the field.
	obj1 = [
		{"actor_id": actors[voice], 
		"text": text,
		"lang": "auto",
		"max_seconds":30,
		"naturalness": 0.8, 
		"speed_x":1,
		"gid":"qqttl-h-uqhGDaXYGMLe4", 
		"tempo":1, 
		"pitch":0,
		"mode":"one-vocoder", 
		"style_label":0, 
		"style_label_version":"v2"}]
	# Header includes authorization that expires for certain time ~ 30min
	# The token is USER SPECIFIC
	headers = {"Authorization": bearer, "content-type": "application/json"}
	response1 = None
	response2 = None
	response3 = None

	response1 = requests.post(url2, json=obj1, headers=headers)
	print(response1.text)

	# Start the second request with the returned URL
	response2 = requests.post(url3, json=json.loads(response1.text)["result"]["speak_urls"], headers=headers)

	# if response2 is not done, get request again
	progress = json.loads(response2.text)["result"][0]["status"]
	
	while (progress != "done") :
		response2 = requests.post(url3, json=json.loads(response1.text)["result"]["speak_urls"], headers=headers)
		progress = json.loads(response2.text)["result"][0]["status"]
		
	# Start the third request but with a parsed object
	temp = requests.get(json.loads(response2.text)["result"][0]["audio"]["url"], headers=headers)
	with open('assets\\temp'+str(count)+'.wav', 'wb') as f:
		f.write(temp.content)
	return 'assets\\temp' + str(count) + '.wav'

# After playing like a few audio files, the files generated must be deleted.
def clearfiles():
	# pygame.mixer.music to be resetted
	pygame.mixer.music.load("assets/reset.wav")
	# curr node for navigating through file system, matches temp files
	curr = str(pathlib.Path().absolute()) + '\\assets'

	regex = re.compile("temp(\d)*\.(.)*")

	for root,dirs,files in os.walk(curr):
		for file in files:
			if regex.match(file) : 
				os.unlink('assets\\' + file)

def main():
	logging.basicConfig(filename='client.log', level=logging.INFO)
	logging.info("Started")
	generate_audio("안녕하세요 테스트입니다. 헬로우 월드!",100, 1)
	clearfiles()

if __name__ ==  "__main__": main()


