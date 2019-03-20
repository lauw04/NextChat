from socket import *
s = socket(AF_INET, SOCK_STREAM)
s.connect(("127.0.0.1",8888))
print("Connexion au serveur")
data = "Mon Cul c'est du Poulet"
for line in data.splitlines():
	s.sendall(line)
	print("Sent:", line)
	response = s.recv(1024)
	print("Received", response)
#s.shutdown(SHUT_RDWR)
