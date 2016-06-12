import json
from os.path import join, dirname
import os, sys
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1
import pyaudio,wave
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import utility,time

## Socket setup
SERVER_IP   = '127.0.0.1'
PORT_NUMBER = 5000
SIZE = 1024
hostName = gethostbyname( '0.0.0.0' )
mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )

## Audio setup
WAV_CHUNK = 1024

## Watson Congitive API
text_to_speech = TextToSpeechV1
(
    username='96db6c7a-2595-491a-9a62-740dc31e0482',
    password='azDpe42DlQ5C'
)

speech_to_text = SpeechToTextV1
(
    username='a1c7a39e-6618-4274-98f1-6ec5ef7237b8',
    password='pU5vkvlPIpmZ'
)

## MAIN
print "Enter some text:",
text = raw_input()

with open(join(dirname(__file__), 'output/synthesize.wav'), 'wb') as audio_file:
    audio_file.write(text_to_speech.synthesize(text))

mySocket.sendto('start',(SERVER_IP,PORT_NUMBER))
print("START TTS")

wf = wave.open('output/synthesize.wav', 'rb')
p = pyaudio.PyAudio()

stream = p.open(
    format = p.get_format_from_width(wf.getsampwidth()),
    channels = wf.getnchannels(),
    rate = wf.getframerate(),
    output = True)
data = wf.readframes(WAV_CHUNK)

while data != '':
    stream.write(data)
    data = wf.readframes(WAV_CHUNK)

stream.close()
p.terminate()

print("END TTS")
mySocket.sendto('stop',(SERVER_IP,PORT_NUMBER))
time.sleep(0.5)
