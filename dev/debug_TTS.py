#!/usr/bin/env python
import json, os, sys, time, random, utils
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1

## Watson Congitive API
text_to_speech = TextToSpeechV1(
    username='YOUR_WATSON_USERNAME',
    password='YOUR_WATSON_PASSWORD')

speech_to_text = SpeechToTextV1(
    username='YOUR_WATSON_USERNAME',
    password='YOUR_WATSON_PASSWORD')

## SETUP + TOOLS
TTSvoices = ["en-US_AllisonVoice","en-US_LisaVoice","en-GB_KateVoice","en-US_MichaelVoice"]
text = raw_input("Enter the seed: ")

## MAIN
if __name__ == "__main__":

    ## TEXT TO SPEECH API CALL
    with open(join(dirname(__file__), 'output/synthesize.wav'), 'wb') as audio_file:
        
        startTTS = time.time()
        audio_file.write(text_to_speech.synthesize(text,TTSvoices[random.randrange(0, 4)],"audio/wav"))
        endTTS = time.time()

    #os.system('play -q --ignore-length output/synthesize.wav')
    os.system('aplay output/synthesize.wav')

