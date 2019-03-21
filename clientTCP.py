# _*_ coding: utf-8 _*_

from socket import *
from threading import Thread # thread
import sys
import os
import time

sentence = ""
#affiche les messages parallèlement depuis le serveur
def receiveMessage(clientSocket):
	try:
		while 1:
			msgRecebida = clientSocket.recv(1024) # reçoit une réponse du serveur
			print '%s' % (msgRecebida)
			if msgRecebida == "close":
				clientSocket.shutdown(socket.SHUT_RDWR) 
				clientSocket.close()
				os._exit(0)
				break
			
	except:
		os._exit(0)	

serverName = 'localhost' # adresse ip du serveur
serverPort = 12000 # port de connexion
clientSocket = socket(AF_INET,SOCK_STREAM) # création de la socket TCP
clientSocket.connect((serverName, serverPort)) # connecte la socket au serveur
sentence = raw_input('Type your nickname: ')
clientSocket.send(sentence) # envoie le pseudo au serveur 
modifiedSentence = clientSocket.recv(1024) # reçoit une réponse du serveur
print 'The server (\'%s\', %d) responded with: %s' % (serverName, serverPort, modifiedSentence)
t = Thread(target=receiveMessage, args=(clientSocket,))
t.daemon = True
t.start()
while 1:
	try:
		sentence = raw_input('')
		if sentence == "close":
<<<<<<< HEAD
=======
			clientSocket.send("next") # quitte le chat privé
			time.sleep(2)
>>>>>>> b8cd91d0393d8d2fc284b5762030a3d655f2656d
			clientSocket.send("close") # quitte le chat global
			clientSocket.shutdown(socket.SHUT_RDWR) 
			clientSocket.close()
			os._exit(0)
		if sentence == "closepchat":
			clientSocker.send("closepchat")

		clientSocket.send(sentence) 
	except:
		os._exit(0)	

