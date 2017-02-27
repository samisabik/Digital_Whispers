#!/usr/bin/env python
import json, os, sys, time, random, utils
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1
import audioop
from collections import deque
import math
import pyaudio, wave
import RPi.GPIO as GPIO

## Watson Congitive API
text_to_speech = TextToSpeechV1(
    username='YOUR_WATSON_USERNAME',
    password='YOUR_WATSON_PASSWORD')

speech_to_text = SpeechToTextV1(
    username='YOUR_WATSON_USERNAME',
    password='YOUR_WATSON_PASSWORD')

## SETUP + TOOLS
audio_int()
rec = utils.Recorder(channels=1)
listen_for_speech()
with open(join(dirname(__file__), 'record.wav'), 'rb') as audio_file:
    result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
    parsed_json = json.loads(result)
    text = parsed_json['results'][0]['alternatives'][0]['transcript']
print text