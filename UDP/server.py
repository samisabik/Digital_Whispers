import socket, sys, time, datetime, os
from termcolor import colored

UDP_HOST = ''
UDP_PORT = 2222 
NUM_CLIENT = 3
client = [None] * NUM_CLIENT

try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error, msg :
    print '##Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
try:
    s.bind((UDP_HOST, UDP_PORT))
except socket.error , msg:
    print '##Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

os.system('clear')
print colored('_______ CLIENT IP _______','magenta',attrs=['bold'])
print ""
for x in range(NUM_CLIENT):
    client[x] = socket.gethostbyname('whisper_'+str(x))
    print "whisper_" + str(x) + " at " + client[x]
print colored('_________________________','magenta',attrs=['bold'])
print ""
while 1:

    data, addr = s.recvfrom(1024)

    ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S]')
    print ts + " " + data + " " + colored('\t<', 'red', attrs=['bold']) + "\t" + str(socket.gethostbyaddr(addr[0])[0])
    
    if (client.index(addr[0]) + 1 > len(client)):
        client_id = 0
    else :
        client_id = client.index(addr[0]) + 1

    if (data == 'start_T'):
        s.sendto('start_L', (client[client_id],UDP_PORT))
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S]')
        print ts +" start_L " + colored('\t>', 'green', attrs=['bold']) + "\t" + str(socket.gethostbyaddr(client[client.index(addr[0]) + 1])[0])
    
    if (data == 'stop_T'):
        ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S]')
        s.sendto('stop_L', (client[client_id],UDP_PORT))
        print ts +" stop_L " + colored('\t>', 'green', attrs=['bold']) + "\t" + str(socket.gethostbyaddr(client[client.index(addr[0]) + 1])[0])

s.close()
