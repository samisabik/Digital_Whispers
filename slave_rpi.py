import json
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
import utility
import time
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys

PORT_NUMBER = 5000
SIZE = 1024

hostName = gethostbyname( '0.0.0.0' )

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )

speech_to_text = SpeechToTextV1(
    username='a1c7a39e-6618-4274-98f1-6ec5ef7237b8',
    password='pU5vkvlPIpmZ')

# RECORD SAMPLE 
rec = utility.Recorder(channels=2)
with rec.open('output/record.wav', 'wb') as recfile2:
    while True:
        (data,addr) = mySocket.recvfrom(SIZE)

        if data == 'start':
        	print("START RECORD")
        	recfile2.start_recording()
        
        if data == 'stop':
        	print("STOPING RECORD")
        	recfile2.stop_recording()
        	with open(join(dirname(__file__), 'output/record.wav'), 'rb') as audio_file:
       			result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
    			parsed_json = json.loads(result)
    			print parsed_json['results'][0]['alternatives'][0]['transcript']
    			sys.exit()