import socket, sys, time, datetime, os
from random import randint
from termcolor import colored


UDP_HOST = ''
UDP_PORT = int(raw_input('Enter UDP_PORT: '))
NUM_CLIENT = int(raw_input('Enter NUM_CLIENT: '))
MAX_LOOP = int(raw_input('Enter MAX_LOOP: '))
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
print colored('\t_______ CLIENT IP _______','magenta',attrs=['bold'])
print ""
for x in range(NUM_CLIENT):
    client[x] = socket.gethostbyname('whisper_'+str(x))
    print "\twhisper_" + str(x) + " at " + client[x]
print colored('\t_________________________','magenta',attrs=['bold'])
print ""

## DEBUG SEED
while True:
    
    run_id = 0
    print ""
    text = raw_input(" Enter some text : ")
    print ""
    s.sendto('start_L', (client[0],UDP_PORT))
    time.sleep(10)
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
            s.sendto('start_L', (client[client_id],UDP_PORT))
            ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S] ')
            print ts +"start_L " + colored('\t>>>', 'green', attrs=['bold']) + "\t" + str(socket.gethostbyaddr(client[client_id])[0])
        
        if (data == 'stop_T'):
            ts = datetime.datetime.fromtimestamp(time.time()).strftime('[%H:%M:%S] ')
            s.sendto('stop_L', (client[client_id],UDP_PORT))
            print ts +"stop_L " + colored('\t>>>', 'green', attrs=['bold']) + "\t" + str(socket.gethostbyaddr(client[client_id])[0])
            print colored('['+ str(run_id) + ']','magenta',attrs=['bold'])
            run_id = run_id + 1


s.close()
