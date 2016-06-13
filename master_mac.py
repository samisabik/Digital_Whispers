import json
from os.path import join, dirname
import os, sys
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1
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
WAV_CHUNK = 256

## Watson Congitive API
text_to_speech = TextToSpeechV1(
    username='YOUR_WATSON_USERNAME',
    password='YOUR_WATSON_PASSWORD'
)

speech_to_text = SpeechToTextV1(
    username='YOUR_WATSON_USERNAME',
    password='YOUR_WATSON_PASSWORD'
)

if __name__ == "__main__":
    print "Enter some text:",
    text = raw_input()

## TEXT TO SPEECH API CALL
    with open(join(dirname(__file__), 'output/synthesize.wav'), 'wb') as audio_file:
        audio_file.write(text_to_speech.synthesize(text))

## SPEECH TO TEXT API CALL
    with open(join(dirname(__file__), 'output/record.wav'), 'rb') as audio_file:
        result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
        parsed_json = json.loads(result)
    	print parsed_json['results'][0]['alternatives'][0]['transcript']
    	sys.exit()  

# PLAY SYNTHESIZE
    mySocket.sendto('start',(SERVER_IP,PORT_NUMBER))
    os.system('omxplayer -o local output/synthesize.wav')
    mySocket.sendto('end',(SERVER_IP,PORT_NUMBER))

# RECORD MICROPHONE
    rec = utility.Recorder(channels=2)

    with rec.open('output/record.wav', 'wb') as recfile:
        while True:
            (data,addr) = mySocket.recvfrom(SIZE)

            if data == 'start':
        	   print("START RECORD")
        	   recfile.start_recording()
            if data == 'stop':
        	   print("STOPING RECORD")
        	   recfile.stop_recording()
