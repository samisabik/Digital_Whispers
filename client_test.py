import socket,time               

PORT = 1234
SERVER_IP = "127.0.0.1"
BUFFER_SIZE = 1024

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

client.send('start')

message = client.recv(BUFFER_SIZE)
print "[" + time.strftime('%H:%M:%S') + "] " + SERVER_IP + " > " + str(message)

client.close()