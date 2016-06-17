import socket,time               

s = socket.socket()         
port = 7777               
s.bind(('', port))        
s.listen(5)     

while True:
   c, addr = s.accept()
   message = c.recv(1024)
   hostname = socket.gethostbyaddr(str(addr[0]))
   print "[" + time.strftime('%H:%M:%S') + "] " + str(hostname[0]) + " > " + str(message)
   c.send("OK")
   c.close()                