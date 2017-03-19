#!/usr/bin/env python
import os,sys,random,json,zmq,utils
from utils import *
from os.path import join, dirname
from sys import exit
from time import sleep
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1

## IBM Watson API (Germany LOC)
text_to_speech = TextToSpeechV1(
	username='b2cb07cb-14f8-4262-9a57-331747a50639',
	password='xKy1K6fSOvU0')
speech_to_text = SpeechToTextV1(
	username='4ad77d91-b0ab-4a70-bf37-6af867f83599',
	password='s32ny3e1eOTW')

TTSvoices = ["en-US_AllisonVoice","en-US_LisaVoice","en-GB_KateVoice","en-US_MichaelVoice"]
voice = TTSvoices[random.randrange(0, 4)]

context = zmq.Context()
statesock = context.socket(zmq.PUB)
statesock.setsockopt(zmq.LINGER, 0)
statesock.bind("tcp://*:5560")

cmdsock = context.socket(zmq.REP)
cmdsock.setsockopt(zmq.LINGER, 0)
cmdsock.bind("tcp://*:5561")

state = "waiting"

def changestate(newstate, data=""):
	global state
	state = newstate
	statesock.send_string(state + ":" + data)
	print "state", state

def ok():
	cmdsock.send_string("OK")

def error():
	cmdsock.send_string("ERROR")
	exit()

def expect(expectedstate):
	if (state == expectedstate):
		ok()
		sleep(0.1)
	else:
		print("Expected state", expectedstate, "not", state)
		error()

rec = utils.Recorder(channels=1)

changestate("waiting")

recfile = None
while True:
	[cmd, data] = cmdsock.recv().split(':')
	print "received", cmd, data

	if cmd == "LISTEN":
		expect("waiting")

		recfile2 = rec.open('output/record.wav', 'wb')
		recfile2.start_recording()
		changestate("listening")

	elif cmd == "STOP_LISTEN":
		expect("listening")

		recfile2.stop_recording()
		recfile2.close()
		with open('output/record.wav', 'rb') as audio_file:
			result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
			parsed_json = json.loads(result)
		try:
			text = parsed_json['results'][0]['alternatives'][0]['transcript']
		except:
			print "STT failed !"
			text = ""
		changestate("waiting", text)

	elif cmd == "TALK":
		expect("waiting")

		changestate("talking")
		with open('output/synthesize.wav', 'wb') as audio_file:
			audio_file.write(text_to_speech.synthesize(data,voice,"audio/wav"))
		os.system('play -q --ignore-length output/synthesize.wav')
		changestate("waiting")

	elif cmd == "DIE":
		ok()
		exit()

	else:
		error()
		exit()

