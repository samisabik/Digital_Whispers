#!/usr/bin/env python
import json, os, sys, time, utility, socket
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1
# tts playback mac import/lib (to be removed)
from pydub import AudioSegment, playback
import random


## Watson Congitive API
text_to_speech = TextToSpeechV1(
    username='YOUR_WATSON_USERNAME',
    password='YOUR_WATSON_PASSWORD')

speech_to_text = SpeechToTextV1(
    username='YOUR_WATSON_USERNAME',
    password='YOUR_WATSON_PASSWORD')

## utils / debug / setup
text = "I am the number one, i are bestest in the world"
voices = ["en-US_AllisonVoice","en-US_LisaVoice","en-GB_KateVoice","en-US_MichaelVoice"]

if __name__ == "__main__":

    while True:
        ## TEXT TO SPEECH API CALL
        with open(join(dirname(__file__), 'output/synthesize.wav'), 'wb') as audio_file:
            start = time.time()
            audio_file.write(text_to_speech.synthesize(text,voices[random.randrange(0, 4)]))
            end = time.time()
            print "[OK] STT %.2f" % (end - start) + "s"
    
        ## RECORD TTS   
        rec = utility.Recorder(channels=2)
        with rec.open('output/record.wav', 'wb') as recfile:
            recfile.start_recording()
            
            ## PLAY TTS Mac
            TTS_output = AudioSegment.from_wav("output/synthesize.wav")
            playback.play(TTS_output)

            # PLAY STT Linux
			#os.system('omxplayer -o local output/synthesize.wav')
           
            recfile.stop_recording()

    ## SPEECH TO TEXT API CALL
        with open(join(dirname(__file__), 'output/record.wav'), 'rb') as audio_file:
            start = time.time()
            result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
            parsed_json = json.loads(result)
            TTS = parsed_json['results'][0]['alternatives'][0]['transcript']
            end = time.time()
            print "[OK] TTS %.2f" % (end - start) + "s"
            print "[INPUT] " + text
            print "[OUTPUT] " + TTS
            text = TTS

# RECORD for TTS
#    rec = utility.Recorder(channels=2)
#    with rec.open('output/record.wav', 'wb') as recfile:
#        recfile.start_recording()
#        recfile.stop_recording()
