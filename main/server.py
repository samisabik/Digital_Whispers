#!/usr/bin/env python
import datetime, time, os, json, zmq
from utils import *
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1
import RPi.GPIO as GPIO

## Input / Output log file
ts = time.time()
filename = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M')

## Setup GPIOs
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)
for x in range(2, 9):
	GPIO.setup(x, GPIO.OUT)

## MAKE A FOR LOOP !

## IBM Watson API Call
text_to_speech = TextToSpeechV1(
	username='c62c972e-727b-4ee3-9436-b808cbbca69a',
	password='BkSjWMgbDopX')
speech_to_text = SpeechToTextV1(
	username='22d00128-ea8c-4d10-a0e8-7059450c7de7',
	password='x8OOTkHv0vXz')

LEVEL = 200
NUM_CLIENTS = 7
clients = [Client('whisper_'+str(x)) for x in range(0,NUM_CLIENTS)]

os.system('clear')
print "# starting whisper_master"

THRESHOLD = audio_int(50) + LEVEL

while True:
	listen_for_speech(THRESHOLD,1)
	with open('output/record.wav', 'rb') as audio_file:
		result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
		parsed_json = json.loads(result)
	try:
		text = parsed_json['results'][0]['alternatives'][0]['transcript']
		print "# starting with phrase : " + text
	except:
		print "# STT failed!"
		continue
	with open('output/'+filename+'.txt', 'a') as text_file:
		text_file.write(text + '\n')
	for i, client in enumerate(clients):
		print "\n"
		if i+1 < len(clients):
			nextclient = clients[i+1]
		else:
			nextclient = None
		try:
			if nextclient:
				nextclient.send("LISTEN")
				nextclient.expect("listening")
		except (zmq.ZMQError, UnexpectedStateError, FailedRequestError) as e:
			print nextclient.addr, "failed:", e
			nextclient.reset()
			nextclient = None
		GPIO.output(i+2, 1)
		time.sleep(1)
		try:
			client.send("TALK", text)
			client.expect("talking")
			client.expect("waiting", 20*1000)
		except (zmq.ZMQError, UnexpectedStateError, FailedRequestError) as e:
			print client.addr, "failed:", e
			client.reset()
			GPIO.output(i+2, 0)
		time.sleep(1) ## addin extra time to add some fucking up
		GPIO.output(i+2, 0)
		try:
			if nextclient:
				nextclient.send("STOP_LISTEN")

				clienttext = nextclient.expect("waiting", 20*1000)
				if clienttext:
					print "TTS result:", '"' + clienttext + '"'
					text = clienttext
				else:
					print "TTS result: (no text)"
		except (zmq.ZMQError, UnexpectedStateError, FailedRequestError) as e:
			print nextclient.addr, "failed:", e
			nextclient.reset()
	with open('output/'+filename+'.txt', 'a') as text_file:
		text_file.write(text + '\n\n')
