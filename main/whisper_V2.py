#!/usr/bin/env python
import socket, sys, time, datetime, os, json, utils
from termcolor import colored
from utils import *
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1

## IBM Watson API
text_to_speech = TextToSpeechV1(
    username='96db6c7a-2595-491a-9a62-740dc31e0482',
    password='azDpe42DlQ5C')

speech_to_text = SpeechToTextV1(
    username='a1c7a39e-6618-4274-98f1-6ec5ef7237b8',
    password='pU5vkvlPIpmZ')


## Whisper Server config
UDP_HOST = ''
UDP_PORT = 2222
NUM_CLIENT = 7
client = [None] * NUM_CLIENT

try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error, msg :
    print '##Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
try:
    s.bind((UDP_HOST, UDP_PORT))
except socket.error , msg:
    print '##Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

os.system('clear')
print colored('\t_______ CLIENT IP _______','magenta',attrs=['bold'])
print ""
for x in range(NUM_CLIENT):
    client[x] = socket.gethostbyname('whisper_'+str(x))
    print "\twhisper_" + str(x) + " at " + client[x]
print colored('\t_________________________','magenta',attrs=['bold'])
print ""

audio_int()

while True:
	listen_for_speech()
	with open(join(dirname(__file__), 'record.wav'), 'rb') as audio_file:
		result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
		parsed_json = json.loads(result)
		text = parsed_json['results'][0]['alternatives'][0]['transcript']
	print text
	with open("test.txt", "a") as myfile:
		myfile.write(text +'\n')
	s.sendto(text, (client[0],UDP_PORT))