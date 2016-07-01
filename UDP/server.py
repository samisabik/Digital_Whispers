import socket, sys, time

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 2222  # Arbitrary non-privileged port

# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

A = socket.gethostbyname('whisper03')
B = socket.gethostbyname('whisper01')
print A
print B

while 1:
    s.sendto('test', (A,PORT))
    s.sendto('test', (B,PORT))
    time.sleep(10)
s.close()
