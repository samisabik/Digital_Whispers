import socket,time,os

UDP_IP = ""
UDP_PORT = 2222
SERVER_IP = "192.168.2.194"

s = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
s.bind((UDP_IP, UDP_PORT))


os.system('clear')
print "## STARTING ON : " + socket.gethostname()

while True:
	data, addr = s.recvfrom(1024)

	if (data == "start_L"):
		print "START listen"
	if (data == "stop_L"):
		print "STOP listen"
		time.sleep(5)
		s.sendto('start_T', (SERVER_IP,UDP_PORT))
		print "START talk"
        time.sleep(15)
        s.sendto('stop_T', (SERVER_IP,UDP_PORT))
        print "STOP talk"

