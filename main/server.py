#!/usr/bin/env python
import socket, sys, time, datetime, os, json, utils
from termcolor import colored
from utils import *
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1
import zmq
from time import sleep

context = zmq.Context()
level = 200

class UnexpectedStateError(Exception):
	pass

class FailedRequestError(Exception):
	pass

## IBM Watson API
text_to_speech = TextToSpeechV1(
	username='96db6c7a-2595-491a-9a62-740dc31e0482',
	password='azDpe42DlQ5C')

speech_to_text = SpeechToTextV1(
	username='a1c7a39e-6618-4274-98f1-6ec5ef7237b8',
	password='pU5vkvlPIpmZ')

NUM_CLIENTS = 7

class Client:
	def __init__(self, addr):

		self.addr = addr
		self.connect()

	def connect(self):
		statesock = context.socket(zmq.SUB)
		statesock.setsockopt(zmq.LINGER, 0)
		statesock.connect("tcp://"+self.addr+":5560")
		statesock.setsockopt(zmq.SUBSCRIBE,'')
		statesock.SNDTIMEO = 2000
		self.statesock = statesock

		cmdsock = context.socket(zmq.REQ)
		cmdsock.setsockopt(zmq.LINGER, 0)
		cmdsock.connect("tcp://"+self.addr+":5561")
		cmdsock.SNDTIMEO = 2000
		cmdsock.RCVTIMEO = 2000
		self.cmdsock = cmdsock

	def reset(self):
		try:
			self.send("DIE")
		except zmq.ZMQError:
			pass

		self.cmdsock.disconnect("tcp://"+self.addr+":5561")
		self.cmdsock.close()
		self.statesock.disconnect("tcp://"+self.addr+":5560")
		self.statesock.close()
		self.connect()

	def send(self, cmd, msg=""):
		print self.addr, "->", cmd, msg
		self.cmdsock.send_string(cmd + ":" + msg)
		response = self.cmdsock.recv()
		print self.addr, "<-", response
		if response == "ERROR":
			raise FailedRequestError("client returned ERROR")

		return response

	def expect(self, expectedstate, timeout=2000):
		print self.addr, "[" + expectedstate + "]"
		self.statesock.RCVTIMEO = timeout
		[state, data] = self.statesock.recv().split(':')
		if state != expectedstate:
			raise UnexpectedStateError("unexpected state " + state)

		return data

clients = [Client('whisper_'+str(x)) for x in range(0,NUM_CLIENTS)]

threshold = audio_int(50) + level

while True:
	print "=== whisper_master ==="
	listen_for_speech(threshold,1)
	with open('output/record.wav', 'rb') as audio_file:
		result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
		parsed_json = json.loads(result)
	try:
		text = parsed_json['results'][0]['alternatives'][0]['transcript']
	except:
		print "Speech-to-text failed"
		continue

	with open('output/text.txt', 'a') as text_file:
		text_file.write(text + '\n')

	print "-"

	for i, client in enumerate(clients):
		if i+1 < len(clients):
			nextclient = clients[i+1]
		else:
			nextclient = None

		print "===", client.addr, "==="

		try:
			if nextclient:
				print "Listen:"
				nextclient.send("LISTEN")
				nextclient.expect("listening")
		except (zmq.ZMQError, UnexpectedStateError, FailedRequestError) as e:
			print nextclient.addr, "failed:", e
			nextclient.reset()
			nextclient = None

		try:
			# print "sending", text
			print "Talk:"
			client.send("TALK", text)
			client.expect("talking")
			client.expect("waiting", 20*1000)
		except (zmq.ZMQError, UnexpectedStateError, FailedRequestError) as e:
			print client.addr, "failed:", e
			client.reset()

		sleep(1)
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

		print "-"

	with open('output/text.txt', 'a') as text_file:
		text_file.write(text + '\n\n')
	print "-"
# sleep(10)

