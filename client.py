#!/usr/bin/python3.6
#shebang

#Nom            : Serveur concurrent
#Description    : Vous allez écrire un client et un serveur en python 3 sous Linux. Ce sera un simili-telnet.
#Ex)            : server.py 1234
#Param 1        : Script en lui même
#Param 2        : IP Server
#Param 3        : Port Server
#Version        : 0.1
#Auteur         : BEROL Saba & HUG Nicolas & RIOS Bastien
#Changelog      : Aucun

# IMPORT PART
# ----------------

from __future__ import print_function
import os
import sys
import socket

# FUNCTION PART
# ----------------

# S'il le manque ne serait-ce qu'un seule des arguements, sort du script.
if len(sys.argv)<4:
	print("Usage :",sys.argv[0],"IP_server port_server")
	sys.exit(-1)

if sys.argv[3]!="stdin": # la source de donnees est un fichier
	# on ouvre le fichier
	fd=os.open(sys.argv[3],os.O_RDONLY)
else:	# la source de donnees est le clavier
        fd=sys.stdin.fileno()

connectes=[fd] # on met le descripteur de l'entree de donnees dans les descripteurs a surveiller

end_data=0 	# si end_data=1, c'est qu'on n'a plus de donnees a envoyer
		# et qu'on a fait un shutdown sur la socket

# creation de la socket TCP/IPv4
sockfd=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# connexion au serveur dont l'adresse et le port sont passes en arguments
sockfd.connect((sys.argv[1],int(sys.argv[2])))
# on ajoute le descripteur de socket aux descripteurs a surveiller
connectes.append(sockfd)

while True:
	# on se met en attente d'un evenement en lecture
	# sur la socket ou l'entree de donnees
	# on recupere dans a_lire le(s) descripteur(s) prets a lire
	a_lire,[],[]=select.select(connectes,[],[])

	# on parcourt la liste des descripteurs sur lesquels un evenement s'est produit
	for desc in a_lire:
		if desc==sockfd: # evenement sur la socket
			recu=sockfd.recv(1024) # on lit sur la socket
			if len(recu)!=0: # on a recu quelque chose
				# affichage de ce qui a ete recu sur la socket
				recu=str(recu,'latin')
				print(recu,end='') # sans retour chariot
			else:	# si on n'a rien recu
				if end_data==0: # et qu'on n'a pas fait shutdown precedemment
					# alors c'est que le serveur a mis fin a la connexion
					print("Deconnexion du serveur")
					sys.exit(-1)
				else:	sys.exit(0) # sinon, fin normale

		if desc==fd: # evenement sur l'entree de donnees
			# on lit sur l'entree de donnees
			lu=os.read(fd,4096)
			if len(lu)==0: # si on n'a rien lu (EOF)
				sockfd.shutdown(socket.SHUT_WR) # on ferme la socket en ecriture
				end_data=1 # on marque la fin des donnees
				connectes=[sockfd] # on ne surveille plus que la socket
			else: # sinon on envoie dans la socket ce qu'on a lu
                       		sockfd.send(lu)
