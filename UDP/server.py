import socket, sys, time, datetime

UDP_HOST = ''
UDP_PORT = 2222 
NUM_CLIENT = 3
client = [None] * NUM_CLIENT

try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print '## Socket created'
except socket.error, msg :
    print '##Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
try:
    s.bind((UDP_HOST, UDP_PORT))
except socket.error , msg:
    print '##Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print '## Socket bind complete'
print "## CLIENT LIST"
for x in range(NUM_CLIENT):
    client[x] = socket.gethostbyname('whisper_'+str(x))
    print "whisper_" + str(x) + " @ " + client[x]
print "## START SERVER LISTEN"
while 1:

    data, addr = s.recvfrom(1024)

    print "[+] RECEIVED " + data + " FROM " + str(socket.gethostbyaddr(addr[0])[0])

    if (data == 'start_T'):
        s.sendto('start_L', (client[client.index(addr[0]) + 1],PORT))
        print "[+] SEND start_L TO " + str(socket.gethostbyaddr(client[client.index(addr[0]) + 1])[0])
    if (data == 'stop_T'):
        s.sendto('stop_L', (client[client.index(addr[0]) + 1],PORT))
        print "[+] SEND stop_L TO " + str(socket.gethostbyaddr(client[client.index(addr[0]) + 1])[0])

s.close()
