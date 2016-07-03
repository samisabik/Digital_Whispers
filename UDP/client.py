import socket,time,os

UDP_IP = ""
UDP_PORT = 2222
SERVER_IP = "192.168.2.194"

s = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
s.bind((UDP_IP, UDP_PORT))

os.system('clear')
print "## STARTING ON : " + socket.gethostname()
print ""

while True:

	data, addr = s.recvfrom(1024)

	if (data == "start_L"):
		ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S]')
		print ts + " START listen"
	
	if (data == "stop_L"):
		ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S]')
		print ts + " STOP listen"

