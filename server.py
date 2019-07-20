#!/usr/bin/python3.6
#shebang

#Nom            : Serveur concurrent
#Description    : Vous allez écrire un client et un serveur en python 3 sous Linux. Ce sera un simili-telnet.
#Ex)            : server.py 1234
#Param 1        : Script en lui même
#Param 2        : port d'écoute
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

def serveur_fils():
	sockfd.close()
	while True:
		recu=connfd.recv(1024)
		if len(recu)==0:
			print("Deconnexion de",client)
			connfd.close()
			sys.exit(0)
		print(recu)
		connfd.send(recu)


# Création du père
def server_pere():

	# S'il le manque un argument ("port" ici), sort du script.
	if len(sys.argv)!=3:
		print("Usage : ",sys.argv[0],"name_file_user","n°_port")
		sys.exit(-1)
	try:
		fd=os.open(sys.argv[1],os.O_RDONLY) #Ouverture du fichier habilitation
	except OSError:
		print("erreur d'ouverture de",sys.argv[1])
	sys.exit(-1)

	

	# Initialisation du port d'écoute
	sockfd=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sockfd.bind(('',int(sys.argv[2])))
	# Autorise jusqu'a 10 connexions
	sockfd.listen(10)

	# Initialisation de la connexion
	while True:
		print("Attente d'un client")
		connfd,client=sockfd.accept()
		print("Connection de",client)
		child=os.fork()
		if child==0:
			serveur_fils()
		else:
			connfd.close()


# INSTRUCTION PART
# ----------------

    
    # Il faut créer une instruction qui lit dans le fichier habilitation les users et le mdp
    # CONNEXION

    message = "WHO : "
    conn.send(message.encode())
    login = conn.recv(1024).decode()
    login = str(login)

    if not login:
        conn.close()
    if login in fd:
        message = "PASSWD :"
        conn.send(message.encode())
        mdp = conn.recv(1024).decode()
        i=0
        if not mdp:
            conn.close()

        if i <= 3 :
            if mdp in fd:
                message = "WELC"
                conn.send(message.encode())
            else:
                message = "bad password try again"
                conn.send(message.encode())
        message = "Bad password BYE"
        conn.send(message.encode())
        conn.close()
    else:
        message = "Credential false ! BY"
        conn.send(message.encode())
        conn.close()


    # ACTION
    while True:
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        if data == "rls":
            files = []
            repo = []
            stop="stop"
            print("User asked my repo")
            for i in os.listdir(os.getcwd()):
                if os.path.isfile(i):
                    files.append(i)
                elif os.path.isdir(i):
                    repo.append(i)
            for x in files:
                print('Fil -', x)
                conn.send(x.encode())
            conn.send(stop.encode())
            for y in repo:
                print('Repo -', y)
                conn.send(y.encode())
            conn.send(stop.encode())

        if data == "rpwd":
            print("User asked whereiam")
            where = os.getcwd().encode()
            conn.send(where)

        if data == "rcd":
            files = []
            repo = []
            stop="stop"
            print("User asked me to go somewhere")
            for i in os.listdir(os.getcwd()):
                if os.path.isfile(i):
                    files.append(i)
                elif os.path.isdir(i):
                    repo.append(i)
            for x in files:
                print('Fil -', x)
                conn.send(x.encode())
            conn.send(stop.encode())
            for y in repo:
                print('Repo -', y)
                conn.send(y.encode())
            conn.send(stop.encode())

            where = conn.recv(1024).decode()
            print("ask to go there : " + where)
            cwd = os.getcwd()
            try: 
                os.chdir(where) 
                print("Now u r there:" + os.getcwd()) 
            except: 
                os.chdir(cwd)
                print("Not a repo ", sys.exc_info())    
            conn.send(os.getcwd().encode())

    conn.close()  # close the connection


if __name__ == '__main__':
    Server()