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


## MAIN
if __name__ == "__main__":

    with open(join(dirname(__file__), 'output/record.wav'), 'rb') as audio_file:
        result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
        parsed_json = json.loads(result)
        STT = parsed_json['results'][0]['alternatives'][0]['transcript']
        print STT