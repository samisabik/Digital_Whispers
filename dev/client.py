import socket,time,os,datetime,sys

UDP_HOST = ""
UDP_PORT = 2222
SERVER_IP = raw_input("Server IP : ")

print SERVER_IP

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

SERVER_IP = socket.gethostbyname('whisper_server')

os.system('clear')
print "## STARTING ON : " + socket.gethostname()
print ""

while True:

	data, addr = s.recvfrom(1024)

	if (data == "start_L"):
		ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S] ')
		print ts + "START LISTEN"
	
	if (data == "stop_L"):
		ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S] ')
		print ts + "STOP LISTEN"		
		time.sleep(5)
		s.sendto('start_T', (SERVER_IP,UDP_PORT))
		ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S] ')
		print ts + "START TALK"
		time.sleep(5)
		s.sendto('stop_T', (SERVER_IP,UDP_PORT))
		ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S] ')
		print ts + "STOP TALK"


