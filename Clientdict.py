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
			msgrecu = clientSocket.recv(1024) # reçoit une réponse du serveur
			if msgrecu == "close":
				print 'Fermeture du serveur'
				clientSocket.shutdown(socket.SHUT_RDWR) 
				clientSocket.close()
				os._exit(0)
				break
			else :
				print '%s' % (msgrecu)
			
	except:
		os._exit(0)	

serverName = 'localhost' # adresse ip du serveur
serverPort = 12000 # port de connexion
clientSocket = socket(AF_INET,SOCK_STREAM) # création de la socket TCP
clientSocket.connect((serverName, serverPort)) # connecte la socket au serveur
modifiedSentence = clientSocket.recv(1024) # reçoit une réponse du serveur
print 'Le serveur (\'%s\', %d) répond avec : %s' % (serverName, serverPort, modifiedSentence)
t = Thread(target=receiveMessage, args=(clientSocket,))
t.daemon = True
t.start()
while 1:
  try:
    sentence = raw_input('')
    if sentence == "close":
			clientSocket.send("lobby") # quitte le chat privé
			time.sleep(2)
			clientSocket.send("close") # quitte le chat global
			clientSocket.shutdown(socket.SHUT_RDWR) 
			clientSocket.close()
			os._exit(0)
    else :
      clientSocket.send(sentence) 
  except:
    os._exit(0)	

