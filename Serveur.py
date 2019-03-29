# _*_ coding: utf-8 _*_

"""
clients array:
0 - Socket
1 - Pseudo
2 - Client connecté au serveur (0 - déconnecté , 1 - connecté)
3 - Adresse IP client
4 - En recherche (0 - no ,1 - yes)
5 - Id interlocuteur (404 s'il n'y en a pas)
6 - Client en chat privé (0 - no , 1 - yes)
7 - Client connecté au chat (0 - no, 1 - yes)
"""


from socket import * # sockets
from threading import Thread # thread
import sys
import os


#stocke les infos sur les clients
clients = []
#stocke les clients en recherche
research = []
#stocke les clients qui sont ou ont été dans un chat privé
privateChat = []
#thread that receives inputs at the server terminal 
def serverManager():
	while 1:
		sentence = raw_input('see list?\n')
		#liste les clients connectés
		if sentence == "list()":
			if len(clients) !=0:
				for i in range(0, len(clients)):
					
					if clients[i][2]==1:
						print "name: %s ip: %s port: 12000"%(clients[i][1],clients[i][3])
			else: 
				print "no such clients logged" 
					
		elif sentence == "close()":
			for i in range(0, len(clients)):
				if clients[i][2]==1:
					try:
						clients[i][0].send("close")
					except:
						print "Logged out client"
			
			break
	serverSocket.close()	
	os._exit(0)
	sys.exit("Finished Execution")

#parallely manage clients
def clientManager(connectionSocket,c_id): #c_id est le client id
	#initialisation du pseudo
	good_name = "no"
	while good_name == "no":
		sentence = connectionSocket.recv(1024) 
		good_name = "yes"
		for i in range(0, len(clients)):
			if sentence == clients[i][1] and clients[i][2]==1:# si le nom est déjà utilisé et que l'utilisateur est actif
				good_name = "no"
				connectionSocket.send("Name already in use, choose another nickname:")
				break
	
	clients[c_id][1] = sentence
	clients[c_id][4] = 0
	clients[c_id][5] = 404
	clients[c_id][6] = 0
	clients[c_id][7] = 0

	identification = "Client %s has logged in." % (sentence)
	print identification
	for i in range(0, len(clients)):
		if clients[i][2]==1:
			clients[i][0].send(identification)
	while 1:	
		try:
			message = connectionSocket.recv(1024)
		except:
			os._exit(0)	
		serv_response = "%s sent: %s" % (clients[c_id][1],message)
		print serv_response

		if message=="start" and clients[c_id][7] == 0: 
			clients[c_id][7] = 1
			clients[c_id][4]=1
			research.append(clients[c_id])
			if len(research)>=2 and clients[c_id][6]==0:
					#404 signifie que l'utilisateur cible n'existe pas
					t_id = 404 #target id
					for i in range(0, len(clients)):
						t_name = research[0][1]
						if clients[i][1]==t_name:
							t_id = i #on récupère l'id de la cible
					if t_id == c_id: #si le client s'auto-invite
						t_id = 404
						for i in range(0, len(clients)):
							t_name = research[1][1]
							if clients[i][1]==t_name:
								t_id = i
					if t_id != 404 and clients[t_id][6] == 0:
						clients[t_id][4]=1
						clients[c_id][4]=1
						clients[c_id][5] = t_id #interlocuteur du client
						clients[t_id][5] = c_id #interlocuteur de la cible
						#stocke l'id des deux clients qui vont participer au chat privé
						privateChat.append([c_id,t_id])
						#change le statut pour garder une trace du chat privé
						clients[c_id][6] = 1
						clients[t_id][6] = 1
						clients[c_id][0].send("You are in a private chat with %s" %(clients[t_id][1]))
						clients[t_id][0].send("You are in a private chat with %s" %(clients[c_id][1]))
						for i in range(0,len(research)):
							if research[i][1] == clients[c_id][1]:
								del research[i]
								break
						for i in range(0,len(research)):
							if research[i][1] == t_name:
								del research[i]
								break

		elif clients[c_id][6]==1: #si le client est dans un chat privé
			if message=="next":
				t_id = clients[c_id][5] #récupère l'id de l'interlocuteur
				#retour à un statut publique dans la file d'attente research
				clients[c_id][6] = 0
				clients[t_id][6] = 0
				clients[c_id][4] = 1
				clients[t_id][4] = 1
				clients[c_id][5] = 404
				clients[t_id][5] = 404
				clients[c_id][0].send("\nNextChat terminé")
				clients[t_id][0].send("\nNextChat terminé")
				research.append(clients[c_id])
				research.append(clients[t_id])

				#reconnection à un autre interlocuteur
				if len(research)>=3 and clients[c_id][6]==0:
					#404 signifie que l'utilisateur cible n'existe pas
					t_id = 404
					for i in range(0, len(clients)):
						t_name = research[0][1]
						if clients[i][1]==t_name:
							t_id = i
					if t_id == c_id:
						t_id = 404
						for i in range(0, len(clients)):
							t_name = research[1][1]
							if clients[i][1]==t_name:
								t_id = i
					if t_id != 404 and clients[t_id][6] == 0:
						clients[t_id][4]=1
						clients[c_id][4]=1
						clients[c_id][5] = t_id
						clients[t_id][5] = c_id
						#stocke l'id des deux clients qui vont participer au chat privé
						privateChat.append([c_id,t_id])
						#change le statut pour garder une trace du chat privé
						clients[c_id][6] = 1
						clients[t_id][6] = 1
						clients[c_id][0].send("You are in a private chat with %s" %(clients[t_id][1]))
						clients[t_id][0].send("You are in a private chat with %s" %(clients[c_id][1]))
						for i in range(0,len(research)):
							if research[i][1] == clients[c_id][1]:
								del research[i]
								break
						for i in range(0,len(research)):
							if research[i][1] == t_name:
								del research[i]
								break


			else :
				#envoie les messages du private chat
				t_id = clients[c_id][5]
				clients[t_id][0].send(serv_response)

		
		if message == "close":
			#envoie le message à tous les utilisateurs
			serv_response = "\nClient %s left the room."%clients[c_id][1]
			print "\nClient %s left the room."%clients[c_id][1]
			for i in range(0, len(clients)):
				if clients[i][2]==1 and i!= c_id:
					clients[i][0].send(serv_response)
					
			#retour à un statut publique pour l'interlocuteur s'il existe
			if clients[c_id][6]==1:
				t_id = clients[c_id][5]
				clients[t_id][6] = 0
				clients[t_id][4] = 1
				clients[t_id][5] = 404
				clients[t_id][0].send("\nNextChat terminé")
				research.append(clients[t_id])
				#tentative de reconnection de l'interlocuteur à quelqu'un d'autre s'il y a assez de clients en recherche
				if len(research)>=3:
					#404 signifie que l'utilisateur cible n'existe pas
					t_id2 = 404 #id du prochain interlocuteur de t_id
					for i in range(0, len(clients)):
						t_name2 = research[0][1]
						if clients[i][1]==t_name2:
							t_id2 = i
					if t_id2 == t_id:
						t_id2 = 404
						for i in range(0, len(clients)):
							t_name2 = research[1][1]
							if clients[i][1]==t_name2:
								t_id2 = i
					if t_id2 != 404 and clients[t_id2][6] == 0:
						clients[t_id2][4]=1
						clients[t_id][4]=1
						clients[t_id][5] = t_id2
						clients[t_id2][5] = t_id
						#stocke l'id des deux clients qui vont participer au chat privé
						privateChat.append([t_id,t_id2])
						#change le statut pour garder une trace du chat privé
						clients[t_id][6] = 1
						clients[t_id2][6] = 1
						clients[t_id][0].send("\nYou are in a private chat with %s" %(clients[t_id2][1]))
						clients[t_id2][0].send("\nYou are in a private chat with %s" %(clients[t_id][1]))
						for i in range(0,len(research)):
							if research[i][1] == clients[t_id][1]:
								del research[i]
								break
						for i in range(0,len(research)):
							if research[i][1] == t_name2:
								del research[i]
								break

			#déconnecte le client
			clients[c_id][6] = 0
			clients[c_id][4] = 0
			clients[c_id][5] = 404
			clients[c_id][0].send("\nNextChat terminé")
			clients[c_id][2]=0
	
			break


						
			
	connectionSocket.close()
	
def main():

	serverName = '' # server ip
	serverPort = 12000 # port
	global serverSocket
	serverSocket = socket(AF_INET,SOCK_STREAM) # TCP socket
	try:
		serverSocket.bind((serverName,serverPort))
	except:
		print "Port already in use"
		serverSocket.close()
		os._exit(0)
	t = Thread(target=serverManager, args=())
	t.start()
	serverSocket.listen(1) 
	print "TCP server waiting connections on port %d ..." % (serverPort)
	counter = 0
	while 1:
		try:
			connectionSocket, addr = serverSocket.accept() 
		except:
			serverSocket.close()
			os._exit(0)
		clients.append([connectionSocket,0,1,addr,0,0,0,0]) #voir docstring en haut du code pour savoir à quoi correspond chaque éléments


		t = Thread(target=clientManager, args=(connectionSocket,counter,))
		t.start()
		counter += 1
	serverSocket.close() 

main()
