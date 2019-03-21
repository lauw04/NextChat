# _*_ coding: utf-8 _*_

"""
clients array:
0 - Socket
1 - nickname
2 - active client or not (0 active , -1 disconnected)
3 - client ip
4 - invited to private chat with someone (0 no ,1 yes)
5 - id of who invited/is connected
6 - is it in private chat?(0 - no , 1-yes)
"""


from socket import * # sockets
from threading import Thread # thread
import sys
import os


#stocke les infos sur les clients
clients = []
#stocke les clients en recherche
research = []
#stocke les clients dans un chat privé
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
			if sentence == clients[i][1]:
				good_name = "no"
				connectionSocket.send("Name already in use, choose another nickname:")
				break
	
	clients[t_id][1] = sentence
	clients[t_id][4] = 0
	clients[t_id][5] = 404
	clients[t_id][6] = 0
	identification = "Cliente %s has logged in." % (sentence)
	print identification
	for i in range(0, len(clients)):
			if clients[i][2]==0:
				clients[i][0].send(identification)
	while 1:	
		try:
			message = connectionSocket.recv(1024) # 
		except:
			os._exit(0)	
		serv_response = "%s sent: %s" % (clients[t_id][1],message)
		#stocke l'id du client qui a envoyé le message
		clientSender = t_id
		print serv_response
		#changement de pseudo
		if "name(" in message:
			new_name = message.split('name(')
			new_name = new_name[1].split(')')
			new_name = new_name[0]	
			good_name = "yes"
			for i in range(0, len(clients)):
				if new_name == clients[i][1]:
					good_name = "no"
					break
			if good_name == "no":
				clients[t_id][0].send("Name already in use, choose another nickname:")
			else:
				nick_change = "%s changed to: %s"%(clients[t_id][1],new_name)
				clients[t_id][1] = new_name
				print "New nick is: %s"%new_name
				for i in range(0, len(clients)):
					if clients[i][2]==0:
						clients[i][0].send(nick_change)
		#envoie de la liste des utilisateurs connectés
		elif "list()" in message:
			for i in range(0, len(clients)):
				if clients[i][2]==0:
					send_list = "name: %s ip: %s port: 12000\n"%(clients[i][1],clients[i][3]) 
					clients[t_id][0].send(send_list)

		elif "private(" in message :
			#404 signifie que l'utilisateur cible n'existe pas
			idTarget = 404
			clientTargetName = message.split('private(')
			clientTargetName = clientTargetName[1].split(')')
			clientTargetName = clientTargetName[0]
			#stocke l'id de l'utilisateur qui a demandé un chat privé
			clientInviteSourceId = clientSender
			#privateInvitation = "%s invited you to a private chat. Accept(Y/N)? " %(clients[clientSender][1])
			#stocke l'id de l'utilisateur cible
			for i in range(0, len(clients)):
				if clients[i][1]==clientTargetName:
					idTarget = i
			#envoie le message à la cible (existante) si il est connecté
			if idTarget != 404:
				#indique que le client cible a reçu une demande de chat privé
				clients[idTarget][4]=1
				#stocke l'id de l'utilisateur qui a demandé un chat privé et celle de la cible
				clients[idTarget][5] = clientSender
				clients[clientSender][5] = idTarget
				#clients[idTarget][0].send(privateInvitation)
				print clientSender
			  #stocke l'id des deux clients qui vont participer au chat privé
				client1 = clientSender
				client2 = clients[clientSender][5]
				privateChat.append([client1,client2])
			  #change le statut pour garder une trace du chat privé
				clients[client1][6] = 1
				clients[client2][6] = 1
				clients[client1][0].send("You are in a private chat with %s" %(clients[client2][1]))
				clients[client2][0].send("You are in a private chat with %s" %(clients[client1][1]))

		elif clients[clientSender][6]==1:
			if message=="next":
				id1 = clientSender
				id2 = clients[clientSender][5]
				#retourne à un statut publique
				clients[id1][6] = 0
				clients[id2][6] = 0
				clients[id1][4] = 0
				clients[id2][4] = 0
				clients[id1][5] = 404
				clients[id2][5] = 404
				clients[id1][0].send("Private chat cancelled")
				clients[id2][0].send("Private chat cancelled")
			else :
				#envoie les messages du private chat
				idToSendPrivateMessage = clients[clientSender][5]
				clients[idToSendPrivateMessage][0].send(serv_response)
		#envoie le message à tous les utilisateurs
		else:

			if message == "close":
				clients[t_id][2]=-1
				serv_response = "Client %s left the room."%clients[t_id][1]
				print "Client %s left the room."%clients[t_id][1]
				for i in range(0, len(clients)):
					if clients[i][2]==0 and i!= clientSender:
						clients[i][0].send(serv_response)	
				break
			elif message != "next":
				for i in range(0, len(clients)):
					if clients[i][2]==0 and i!= clientSender and clients[i][6]!=1:
						clients[i][0].send(serv_response)

						
			
	connectionSocket.close()
	

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
	try:
		connectionSocket, addr = serverSocket.accept() 
	except:
		serverSocket.close()
		os._exit(0)
	clients.append([connectionSocket,0,0,addr,flagInvP,inviterID,inPrivateChat])

	t = Thread(target=clientManager, args=(connectionSocket,counter,))
	t.start()
	counter += 1
serverSocket.close() 

