import socket, sys, time, datetime

HOST = ''
PORT = 2222 
NUM_CLIENT = 3
client = [None] * NUM_CLIENT

try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print '## Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print '## Socket bind complete'

for x in range(NUM_CLIENT):
    client[x] = socket.gethostbyname('whisper_'+str(x))
    print "whisper_" + str(x) + " @ " + client[x]

while 1:
    for i in range(NUM_CLIENT):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        s.sendto(st + ': WHISPER_'+ str(i) + ' ', (client[i],PORT))
        time.sleep(5)

s.close()
