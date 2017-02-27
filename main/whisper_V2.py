#!/usr/bin/env python
import json, os, sys, time, random
from utils import *
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1
import audioop
from collections import deque
import math
import pyaudio, wave
import RPi.GPIO as GPIO

## Watson Congitive API
text_to_speech = TextToSpeechV1(
    username='96db6c7a-2595-491a-9a62-740dc31e0482',
    password='azDpe42DlQ5C')

speech_to_text = SpeechToTextV1(
    username='a1c7a39e-6618-4274-98f1-6ec5ef7237b8',
    password='pU5vkvlPIpmZ')

## SETUP + TOOLS
audio_int()
rec = utils.Recorder(channels=1)
listen_for_speech()
with open(join(dirname(__file__), 'record.wav'), 'rb') as audio_file:
    result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
    parsed_json = json.loads(result)
    text = parsed_json['results'][0]['alternatives'][0]['transcript']
print text