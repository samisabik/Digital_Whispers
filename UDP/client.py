import socket,time

UDP_IP = ""
UDP_PORT = 2222
SERVER_IP = "192.168.2.194"

s = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
s.bind((UDP_IP, UDP_PORT))

while True:
	data, addr = s.recvfrom(1024)

	if (data == "start_L"):
		print "i'm starting to listen"
	if (data == "stop_L"):
		print "i'm stopping to listen"
		s.sendto('start_T', (SERVER_IP,UDP_PORT))
		print "i'm starting to talk"
        time.sleep(10)
        s.sendto('stop_T', (SERVER_IP,UDP_PORT))
        print "i'm stopping to talk"

