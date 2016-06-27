#!/usr/bin/env python
import json, os, sys, time, utility, socket, random
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1

## Watson Congitive API
text_to_speech = TextToSpeechV1(
    username='96db6c7a-2595-491a-9a62-740dc31e0482',
    password='azDpe42DlQ5C')

speech_to_text = SpeechToTextV1(
    username='a1c7a39e-6618-4274-98f1-6ec5ef7237b8',
    password='pU5vkvlPIpmZ')

## SETUP + TOOLS
TTSvoices = ["en-US_AllisonVoice","en-US_LisaVoice","en-GB_KateVoice","en-US_MichaelVoice"]
rec = utility.Recorder(channels=2, rate=44100, frames_per_buffer=1024)
text = "This is only a test, please ignore !"
loopid = 0

## MAIN
if __name__ == "__main__":

    while True:

        ## TEXT TO SPEECH API CALL
        with open(join(dirname(__file__), 'output/synthesize.wav'), 'wb') as audio_file:
            
            startTTS = time.time()
            audio_file.write(text_to_speech.synthesize(text,TTSvoices[random.randrange(0, 4)],"audio/wav"))
            endTTS = time.time()

        # PLAY + RECORD TTS
        with rec.open('output/record.wav', 'wb') as recfile:
            
            recfile.start_recording()
            ##PLAY STT Linux/Mac
            #os.system('omxplayer -o local output/synthesize.wav')
            os.system('aplay output/synthesize.wav')
            recfile.stop_recording()

        ## SPEECH TO TEXT API CALL
        with open(join(dirname(__file__), 'output/record.wav'), 'rb') as audio_file:
            
            startSTT = time.time()
            result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
            parsed_json = json.loads(result)
            STT = parsed_json['results'][0]['alternatives'][0]['transcript']
            endSTT = time.time()
        
        print "[*] RUN LOOP : " + str(loopid)
        print "[*] INPUT : " + text
        print "[*] STT delay :  %.2f" % (endTTS - startTTS) + "s"
        print "[*] TTS delay :  %.2f" % (endSTT - startSTT) + "s"
        print "[*] OUTPUT : " + STT
        #MAC LOOP
        text = STT
        loopid = loopid + 1