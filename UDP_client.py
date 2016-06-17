import socket

HOST = '127.0.0.1'
PORT = 9000
DATA = 'AAAAAAAAAA'

def udp_client():
	while True:
    	client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM)
    	client.sendto(DATA, ( HOST, PORT ))
    	data, addr = client.recvfrom(4096)
    print data, adr

if __name__ == '__main__':
    udp_client()
    time(1)
    udp_client()