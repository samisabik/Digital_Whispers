import json
from os.path import join, dirname
import os, sys
from watson_developer_cloud import TextToSpeechV1
import pyaudio
import wave
import time
from socket import socket, AF_INET, SOCK_DGRAM

## test
SERVER_IP   = '192.168.2.174'
PORT_NUMBER = 5000
SIZE = 1024

mySocket = socket( AF_INET, SOCK_DGRAM )

CHUNK = 1024

text_to_speech = TextToSpeechV1(
    username='YOUR_WATSON_USERNAME',
    password='YOUR_WATSON_PASSWORD')

print "Enter some text:",
text = raw_input()

with open(join(dirname(__file__), 'output/synthesize.wav'), 'wb') as audio_file:
    audio_file.write(text_to_speech.synthesize(text))

mySocket.sendto('start',(SERVER_IP,PORT_NUMBER))
time.sleep(0.5)
print("starting sound")
os.system('omxplayer -o local output/synthesize.wav')
print("stop sound")
mySocket.sendto('stop',(SERVER_IP,PORT_NUMBER))
time.sleep(0.5)
