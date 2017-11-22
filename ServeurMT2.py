from Protocole import *
from Joueur import *
import time
import socket
import threading
import sys



#initialisation de la partie

nb_joueurs = int(sys.argv[1])
personages = ["Loup garou", "Villageois"]
players = [Joueur("no one", personages) for i in xrange(0,nb_joueurs)]
cptJoueurs = 0
threads = []

#ouverture de la communication
comSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
comSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
comSocket.bind(('',8000))
comSocket.listen(nb_joueurs)

print "En attente de connexion"

def partie():

	global cptJoueurs
	#ecoute des clients
	newSocket, address = comSocket.accept()
	p = Protocole(newSocket, '$')
	print "Connecte a ", address	
	
	#Envoie les informations relatives a la partie au joueur
	p.envoi("nb_Joueurs",str(nb_joueurs))	
	p.rec("val")
	p.envoiListe("persos",personages)
	
	#Recupere le nom du joueur
	nomJoueur = p.rec("nom")
	players[cptJoueurs].name = nomJoueur
	p.envoi("pers", players[cptJoueurs].perso)
	p.rec("merci")
	cptJoueurs += 1
	
	#Attent que tous les joueurs ait rejoint la partie
	if(cptJoueurs < nb_joueurs):
		while True:
			if(cptJoueurs == nb_joueurs):break
	
	newSocket.send("go")
	newSocket.recv(1024)
		
	#envoi de la liste complete des joueurs
	p.envoiListe("players", [player.name for player in players])
		
	#attend que des gens soient tues
	while True :	
		#try:
		d = p.rec("die")
		players.pop(int(d))
		#print "j'envoie", [player.name for player in players]
		p.envoiListe("players", [player.name for player in players])

		
	newSocket.close()
	print "Fin de connection avec ", address
			
	#finally:
	comSocket.close()


#Lancement de toutes les parties en parallele
for joueur in xrange(0,nb_joueurs):
	
	thread=threading.Thread(target=partie)
	thread.start()
	threads.append(thread)
		



