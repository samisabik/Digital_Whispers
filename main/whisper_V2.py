#!/usr/bin/env python
import json, os, sys, time, random, utils
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1
import audioop
from collections import deque
import math
import pyaudio, wave
import RPi.GPIO as GPIO

## set GPIO relay
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)

## Microphone stream config.
CHUNK = 4096 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 1500  
SILENCE_LIMIT = 2 
PREV_AUDIO = 0.5  

def audio_int(num_samples=50):

    print "Getting intensity values from mic."
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4))) 
              for x in range(num_samples)] 
    values = sorted(values, reverse=True)
    r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
    print " Finished "
    print " Average audio intensity is ", r
    stream.close()
    p.terminate()
    return r


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

## Watson Congitive API
text_to_speech = TextToSpeechV1(
    username='96db6c7a-2595-491a-9a62-740dc31e0482',
    password='azDpe42DlQ5C')

speech_to_text = SpeechToTextV1(
    username='a1c7a39e-6618-4274-98f1-6ec5ef7237b8',
    password='pU5vkvlPIpmZ')

## SETUP + TOOLS
TTSvoices = ["en-US_AllisonVoice","en-US_LisaVoice","en-GB_KateVoice","en-US_MichaelVoice"]
rec = utils.Recorder(channels=1)
listen_for_speech()
with open(join(dirname(__file__), 'record.wav'), 'rb') as audio_file:
    result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
    parsed_json = json.loads(result)
    text = parsed_json['results'][0]['alternatives'][0]['transcript']
##text = raw_input("Enter the seed: ")
loopid = 0

## MAIN
if __name__ == "__main__":

    while True:

        ## TEXT TO SPEECH API CALL
        with open(join(dirname(__file__), 'output/synthesize.wav'), 'wb') as audio_file:
            
            startTTS = time.time()
            audio_file.write(text_to_speech.synthesize(text,TTSvoices[random.randrange(0, 4)],"audio/wav"))
            endTTS = time.time()

        ## PLAY + REC
        GPIO.output(40, GPIO.HIGH)
  
        with rec.open('output/record.wav', 'wb') as recfile2:
            recfile2.start_recording()
            os.system('play tempo 0.5 -q --ignore-length output/synthesize.wav')
            recfile2.stop_recording()
        GPIO.output(40, GPIO.LOW)

        ## SPEECH TO TEXT API CALL
        with open(join(dirname(__file__), 'output/record.wav'), 'rb') as audio_file:
            
            startSTT = time.time()
            result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
            parsed_json = json.loads(result)
            STT = parsed_json['results'][0]['alternatives'][0]['transcript']
            endSTT = time.time()

        print "-------------------------------------------"
        print "[+] RUN : " + str(loopid)
        print "[+] STT : %.2f" % (endTTS - startTTS) + "s"
        print "[+] TTS : %.2f" % (endSTT - startSTT) + "s"
        print "[+] OUT : " + STT
     
        #single client debug loop
        text = STT
        loopid = loopid + 1
