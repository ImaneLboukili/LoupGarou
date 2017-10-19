
import socket
from Joueur import *
import pickle


#initialisation de la partie
nb_joueurs = 4
personages = ["Loup garou", "Villageois"]
players = [Joueur("", personages) for i in xrange(0,nb_joueurs)]
cptJoueurs = 0


#ouverture de la communication
comSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
comSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
comSocket.bind(('',8000))
comSocket.listen(nb_joueurs)


#ecoute des clients
try:
   #while True:
	newSocket, address = comSocket.accept()
	print "Connecte a ", address
	while True:
		
		
		newSocket.sendall(str(nb_joueurs))
		print "envoye"
		#newSocket.sendall(str(players))
		newSocket.sendall(pickle.dumps(personages))
		#print pickle.dumps(personages)
		
		nomJoueur1 = newSocket.recv(1024)
		if not nomJoueur1: break
		if(cptJoueurs <nb_joueurs):
			players[cptJoueurs].name = nomJoueur1			
			newSocket.sendall("OK")
			#permission de continuer si le nombre max de joueur n'est pas atteint
			
			newSocket.sendall(players[cptJoueurs].perso)
			
			newSocket.sendall(pickle.dumps([player.name for player in players]))
			#actualisation de la liste des joueurs
			cptJoueurs += 1
			
				
			
		newSocket.close()
		print "Fin de connection avec ", address
		
finally:
    comSocket.close()

