import socket,time

UDP_IP = ""
UDP_PORT = 2222
UDP_SERVER = "192.168.2.194"

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
        sock.sendto('start_T', (UDP_SERVER,UDP_PORT))
        time.sleep(10)
        sock.sendto('stop_T', (UDP_SERVER,UDP_PORT))
        time.sleep(10)