import socket,time,os,datetime,sys,random
from watson_developer_cloud import TextToSpeechV1,SpeechToTextV1

## IBM Watson API
text_to_speech = TextToSpeechV1(
    username='YOUR_WATSON_USERNAME',
    password='YOUR_WATSON_PASSWORD')

speech_to_text = SpeechToTextV1(
    username='YOUR_WATSON_USERNAME',
    password='YOUR_WATSON_PASSWORD')

TTSvoices = ["en-US_AllisonVoice","en-US_LisaVoice","en-GB_KateVoice","en-US_MichaelVoice"]

UDP_HOST = ""
UDP_PORT = 2222

try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error, msg :
    print '##Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((UDP_HOST, UDP_PORT))
except socket.error , msg:
    print '##Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

SERVER_IP = socket.gethostbyname('whisper_master')

os.system('clear')
print "## STARTING ON : " + socket.gethostname()
print ""

while True:
	data, addr = s.recvfrom(1024)
	print data
	with open(join(dirname(__file__), 'output/synthesize.wav'), 'wb') as audio_file: 
		audio_file.write(text_to_speech.synthesize(data,TTSvoices[random.randrange(0, 4)],"audio/wav"))
	os.system('play -q --ignore-length output/synthesize.wav')
	# if (data == "start_L"):
	# 	ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S] ')
	# 	print ts + "START LISTEN"
	# if (data == "stop_L"):
	# 	ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S] ')
	# 	print ts + "STOP LISTEN"		
	# 	time.sleep(5)
	# 	s.sendto('start_T', (SERVER_IP,UDP_PORT))
	# 	ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S] ')
	# 	print ts + "START TALK"
	# 	time.sleep(5)
	# 	s.sendto('stop_T', (SERVER_IP,UDP_PORT))
	# 	ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S] ')
	# 	print ts + "STOP TALK"