import json, os, sys, time, utility
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1

## Watson Congitive API
text_to_speech = TextToSpeechV1(
    username='96db6c7a-2595-491a-9a62-740dc31e0482',
    password='azDpe42DlQ5C')

speech_to_text = SpeechToTextV1(
    username='a1c7a39e-6618-4274-98f1-6ec5ef7237b8',
    password='pU5vkvlPIpmZ')

## utils / debug / setup
STT = "You are running into the old problem with floating point numbers that all numbers cannot be represented."
voices = ["en-US_LisaVoice","en-US_AllisonVoice","en-GB_KateVoice","en-US_MichaelVoice"]

## TEXT TO SPEECH API CALL
with open(join(dirname(__file__), 'output/synthesize.wav'), 'wb') as audio_file:
    start = time.time()
    audio_file.write(text_to_speech.synthesize(STT,voices[1]))
    end = time.time()
    print "[OK] STT %.2f" % (end - start) + " s"

## SPEECH TO TEXT API CALL
with open(join(dirname(__file__), 'output/synthesize.wav'), 'rb') as audio_file:
    start = time.time()
    result = json.dumps(speech_to_text.recognize(audio_file, content_type='audio/wav'))
    end = time.time()
    parsed_json = json.loads(result)
    TTS = parsed_json['results'][0]['alternatives'][0]['transcript']
    print "[OK] TTS %.2f" % (end - start) + " s"
    print "[INPUT] " + STT
    print "[OUTPUT] " + TTS

# PLAY STT
#    os.system('omxplayer -o local output/synthesize.wav')

# RECORD for TTS
#    rec = utility.Recorder(channels=2)
#    with rec.open('output/record.wav', 'wb') as recfile:
#        recfile.start_recording()
#        recfile.stop_recording()
