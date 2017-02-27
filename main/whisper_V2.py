#!/usr/bin/env python
import json, os, sys, time, utils
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
import audioop
from collections import deque
import pyaudio, wave

speech_to_text = SpeechToTextV1(
    username='a1c7a39e-6618-4274-98f1-6ec5ef7237b8',
    password='pU5vkvlPIpmZ')

## Microphone stream config.
CHUNK = 4096 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 1500  
SILENCE_LIMIT = 2 
PREV_AUDIO = 0.5  

def listen_for_speech(threshold=THRESHOLD, num_phrases=1):

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print "* Listening mic. "
    audio2send = []
    cur_data = ''  # current chunk  of audio data
    rel = RATE/CHUNK
    slid_win = deque(maxlen=SILENCE_LIMIT * rel)
    #Prepend audio from 0.5 seconds before noise was detected
    prev_audio = deque(maxlen=PREV_AUDIO * rel) 
    started = False
    n = num_phrases
    response = []

    while (num_phrases == -1 or n > 0):
        cur_data = stream.read(CHUNK)
        slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
        #print slid_win[-1]
        if(sum([x > THRESHOLD for x in slid_win]) > 0):
            if(not started):
                print "Starting record of phrase"
                started = True
            audio2send.append(cur_data)
        elif (started is True):
            print "Finished"
            # The limit was reached, finish capture and deliver.
            filename = save_speech(list(prev_audio) + audio2send, p)
            # Reset all
            started = False
            slid_win = deque(maxlen=SILENCE_LIMIT * rel)
            prev_audio = deque(maxlen=0.5 * rel) 
            audio2send = []
            n -= 1
            print "Listening ..."
        else:
            prev_audio.append(cur_data)

    print "* Done recording"
    stream.close()
    p.terminate()

    return response

def save_speech(data, p):

    data = ''.join(data)
    wf = wave.open('record.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100) 
    wf.writeframes(data)
    wf.close()
    return 'record.wav'

## SETUP + TOOLS
rec = utils.Recorder(channels=1)
listen_for_speech()
with open(join(dirname(__file__), 'record.wav'), 'rb') as audio_file:
    result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
    parsed_json = json.loads(result)
    text = parsed_json['results'][0]['alternatives'][0]['transcript']
print text