import socket, sys, time, datetime, os
from random import randint
from termcolor import colored

UDP_HOST = ''
UDP_PORT = 2222 
NUM_CLIENT = 4
client = [None] * NUM_CLIENT
run_id = 0
MAX_LOOP = 5

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

## DEBUG SEED
while 1:

    s.sendto('start_L', (client[0],UDP_PORT))
    text = raw_input("Please enter your name: ")
    s.sendto('stop_L', (client[0],UDP_PORT))

    while (run_id < MAX_LOOP):

        data, addr = s.recvfrom(1024)

        ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S] ')
        print ts + data + colored('\t<<<', 'red', attrs=['bold']) + "\t" + str(socket.gethostbyaddr(addr[0])[0])
        
        if (client.index(addr[0]) + 1 >= len(client)):
            client_id = 0
        else :
            client_id = client.index(addr[0]) + 1

        if (data == 'start_T'):
            run_id = run_id + 1
            s.sendto('start_L', (client[client_id],UDP_PORT))
            ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S] ')
            print ts +"start_L " + colored('\t>>>', 'green', attrs=['bold']) + "\t" + str(socket.gethostbyaddr(client[client_id])[0])
        
        if (data == 'stop_T'):
            ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S] ')
            s.sendto('stop_L', (client[client_id],UDP_PORT))
            print ts +"stop_L " + colored('\t>>>', 'green', attrs=['bold']) + "\t" + str(socket.gethostbyaddr(client[client_id])[0])
            print colored('['+ str(run_id) + ']','magenta',attrs=['bold'])

s.close()
