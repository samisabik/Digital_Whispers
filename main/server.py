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
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)

## IBM Watson API Call
text_to_speech = TextToSpeechV1(
	username='YOUR_WATSON_USERNAME',
	password='YOUR_WATSON_PASSWORD')
speech_to_text = SpeechToTextV1(
	username='YOUR_WATSON_USERNAME',
	password='YOUR_WATSON_PASSWORD')

LEVEL = 200
NUM_CLIENTS = 7
clients = [Client('whisper_'+str(x)) for x in range(0,NUM_CLIENTS)]

os.system('clear')
print "# starting whisper_master"

THRESHOLD = audio_int(50) + LEVEL

while True:
	print "\n\twhisper_master\n"
	listen_for_speech(THRESHOLD,1)
	with open('output/record.wav', 'rb') as audio_file:
		result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
		parsed_json = json.loads(result)
	try:
		text = parsed_json['results'][0]['alternatives'][0]['transcript']
		print "# seed : " + text
	except:
		print "# STT failed!"
		continue
	with open('output/'+filename+'.txt', 'a') as text_file:
		text_file.write(text + '\n')
	for i, client in enumerate(clients):
		if i+1 < len(clients):
			nextclient = clients[i+1]
		else:
			nextclient = None
		print "\n\t", client.addr, "\n"
		try:
			if nextclient:
				print "Listen:"
				nextclient.send("LISTEN")
				nextclient.expect("listening")
		except (zmq.ZMQError, UnexpectedStateError, FailedRequestError) as e:
			print nextclient.addr, "failed:", e
			nextclient.reset()
			nextclient = None
		GPIO.output(client+2, 1)
		time.sleep(1)
		try:
			print "Talk:"
			client.send("TALK", text)
			client.expect("talking")
			client.expect("waiting", 20*1000)
		except (zmq.ZMQError, UnexpectedStateError, FailedRequestError) as e:
			print client.addr, "failed:", e
			client.reset()
			GPIO.output(client+2, 0)
		time.sleep(1) ## addin extra time to add some fucking up
	    GPIO.output(client+2, 0)
		try:
			if nextclient:
				print "TTS:"
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
