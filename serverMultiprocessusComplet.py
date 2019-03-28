# _*_ coding: utf-8 _*_

"""
clients array:
0 - Socket
1 - nickname
2 - active client or not (0 active , -1 disconnected)
3 - client ip
4 - en recherche (0 no ,1 yes)
5 - id of who invited/is connected
6 - is it in private chat?(0 - no , 1-yes)
7 - vient pas d'arriver (0 no, 1 yes)
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
def listClients():
	while 1:
		somethin = raw_input('see list?\n')
		#list all available connections
		if somethin == "list()":
			if len(clients) !=0:
				for i in range(0, len(clients)):
					#checks which clients are connected
					if clients[i][2]==0:
						print "name: %s ip: %s port: 12000"%(clients[i][1],clients[i][3])
			else: 
				print "no such clients logged" 
				
					
					
		elif somethin == "close()":
			for i in range(0, len(clients)):
				if clients[i][2]==0:
					try:
						clients[i][0].send("close")
					except:
						print "Logged out client"
			
			break
	serverSocket.close()	
	os._exit(0)
	sys.exit("Finished Execution")

#parallely manage clients
def clientManager(connectionSocket,t_id):
	#receive the nickname of the client
	good_name = "no"
	while good_name == "no":
		sentence = connectionSocket.recv(1024) 
		good_name = "yes"
		for i in range(0, len(clients)):
			if sentence == clients[i][1] and clients[i][2]==0:# si le nom est déjà utilisé et que l'utilisateur est actif
				good_name = "no"
				connectionSocket.send("Name already in use, choose another nickname:")
				break
	
	clients[t_id][1] = sentence
	clients[t_id][4] = 0
	clients[t_id][5] = 404
	clients[t_id][6] = 0
	clients[t_id][7] = 0

	identification = "Client %s has logged in." % (sentence)
	print identification
	for i in range(0, len(clients)):
		if clients[i][2]==0:
			clients[i][0].send(identification)
	while 1:	
		try:
			message = connectionSocket.recv(1024)
		except:
			os._exit(0)	
		serv_response = "%s sent: %s" % (clients[t_id][1],message)
		#stocke l'id du client qui a envoyé le message
		clientSender = t_id
		print serv_response

		if "start" in message and clients[t_id][7] == 0: 
			clients[t_id][7] = 1
			clients[clientSender][4]=1
			research.append(clients[clientSender])
			if len(research)>=2 and clients[clientSender][6]==0:
					#404 signifie que l'utilisateur cible n'existe pas
					idTarget = 404
					for i in range(0, len(clients)):
						clientTargetName = research[0][1]
						if clients[i][1]==clientTargetName:
							idTarget = i
					if idTarget == t_id:
						idTarget = 404
						for i in range(0, len(clients)):
							clientTargetName = research[1][1]
							if clients[i][1]==clientTargetName:
								idTarget = i
					if idTarget != 404 and clients[idTarget][6] == 0:
						clients[idTarget][4]=1
						clients[t_id][4]=1
						clients[clientSender][5] = idTarget
						clients[idTarget][5] = clientSender
						#stocke l'id des deux clients qui vont participer au chat privé
						client1 = clientSender
						client2 = clients[clientSender][5]
						privateChat.append([client1,client2])
						#change le statut pour garder une trace du chat privé
						clients[client1][6] = 1
						clients[client2][6] = 1
						clients[client1][0].send("You are in a private chat with %s" %(clients[client2][1]))
						clients[client2][0].send("You are in a private chat with %s" %(clients[client1][1]))
						for i in range(0,len(research)):
							if research[i][1] == clients[clientSender][1]:
								del research[i]
								break
						for i in range(0,len(research)):
							if research[i][1] == clientTargetName:
								del research[i]
								break

		elif clients[clientSender][6]==1:
			if message=="next":
				id1 = clientSender
				id2 = clients[clientSender][5]
				#retourne à un statut publique
				clients[id1][6] = 0
				clients[id2][6] = 0
				clients[id1][4] = 1
				clients[id2][4] = 1
				clients[id1][5] = 404
				clients[id2][5] = 404
				clients[id1][0].send("NextChat terminé")
				clients[id2][0].send("NextChat terminé")
				research.append(clients[id1])
				research.append(clients[id2])

				if len(research)>=3 and clients[clientSender][6]==0:
					#404 signifie que l'utilisateur cible n'existe pas
					idTarget = 404
					for i in range(0, len(clients)):
						clientTargetName = research[0][1]
						if clients[i][1]==clientTargetName:
							idTarget = i
					if idTarget == t_id:
						idTarget = 404
						for i in range(0, len(clients)):
							clientTargetName = research[1][1]
							if clients[i][1]==clientTargetName:
								idTarget = i
					if idTarget != 404 and clients[idTarget][6] == 0:
						clients[idTarget][4]=1
						clients[t_id][4]=1
						clients[clientSender][5] = idTarget
						clients[idTarget][5] = clientSender
						#stocke l'id des deux clients qui vont participer au chat privé
						client1 = clientSender
						client2 = clients[clientSender][5]
						privateChat.append([client1,client2])
						#change le statut pour garder une trace du chat privé
						clients[client1][6] = 1
						clients[client2][6] = 1
						clients[client1][0].send("You are in a private chat with %s" %(clients[client2][1]))
						clients[client2][0].send("You are in a private chat with %s" %(clients[client1][1]))
						for i in range(0,len(research)):
							if research[i][1] == clients[clientSender][1]:
								del research[i]
								break
						for i in range(0,len(research)):
							if research[i][1] == clientTargetName:
								del research[i]
								break


			else :
				#envoie les messages du private chat
				idToSendPrivateMessage = clients[clientSender][5]
				clients[idToSendPrivateMessage][0].send(serv_response)
		#envoie le message à tous les utilisateurs
		if message == "close":
			id1 = clientSender
			id2 = clients[clientSender][5]
			#retourne à un statut publique
			clients[id1][6] = 0
			clients[id2][6] = 0
			clients[id1][4] = 1
			clients[id2][4] = 1
			clients[id1][5] = 404
			clients[id2][5] = 404
			clients[id1][0].send("NextChat terminé")
			clients[id2][0].send("NextChat terminé")
			research.append(clients[id2])
			clients[t_id][2]=-1
			serv_response = "Client %s left the room."%clients[t_id][1]
			print "Client %s left the room."%clients[t_id][1]
			for i in range(0, len(clients)):
				if clients[i][2]==0 and i!= clientSender:
					clients[i][0].send(serv_response)	
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
	t = Thread(target=listClients, args=())
	t.start()
	serverSocket.listen(1) 
	print "TCP server waiting connections on port %d ..." % (serverPort)
	counter = 0
	while 1:
		#indique si il a été invité à un chat privé
		flagInvP=0
		#initialise celui qui a invité
		inviterID=0
		#initialise ceux qui sont dans le chat privé
		inPrivateChat = 0
		#initialise ceux qui viennent d'arriver
		arrival = 0
		try:
			connectionSocket, addr = serverSocket.accept() 
		except:
			serverSocket.close()
			os._exit(0)
		clients.append([connectionSocket,0,0,addr,flagInvP,inviterID,inPrivateChat,arrival])


		t = Thread(target=clientManager, args=(connectionSocket,counter,))
		t.start()
		counter += 1
	serverSocket.close() 

main()
