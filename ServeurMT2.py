from Protocole import *
from Joueur import *
import time
import socket
import threading
import sys
import random as rd 

#initialisation de la partie

nb_joueurs = int(sys.argv[1])
personages = ["Loup garou", "Villageois"]
players = []

#On a ttribue le bon nombre de loups garous (et autres personages)
for i in xrange(0,nb_joueurs):
	perso = "Villageois"
	if(i<int(nb_joueurs/2)):
		perso = personages[0]
	players.append(Joueur("no one", perso))

#on melange aleatoirement les joueurs
rd.shuffle(players)
cptJoueurs = 0
threads = []

#ouverture de la communication
comSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
comSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
comSocket.bind(('',8000))
comSocket.listen(nb_joueurs)

global nomMort 

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
	perso = players[cptJoueurs].perso
	p.rec("merci")
	cptJoueurs += 1
	
	#Attent que tous les joueurs aient rejoint la partie
	if(cptJoueurs < nb_joueurs):
		while True:
			if(cptJoueurs == nb_joueurs):break
	
	newSocket.send("go")
	newSocket.recv(1024)
		
	#envoi de la liste complete des joueurs
	p.envoiListe("players", [player.name for player in players])
	
	#############################################"
	
	#debut de la partie. Chaque client fait ce qu'il doit faire la nuit
	p.rec("nuit?")
	newSocket.sendall("nuit")
	nomMort = ''
	#envoie la liste des gens tuables aux loups garous
	if(perso == "Loup garou"):
		tuables = []
		for pl in players:
			if(pl.perso != "Loup garou"):
				tuables.append(pl)
		p.envoiListe("tuables", [player.name for player in tuables])	
		d = int(p.rec("die"))
		#faire ici la majorite des d quand il y aura plusieurs loups
		
		nomMort = tuables[d].name
		print "les loups vont tuer ", nomMort
		
		for pl in players:
			if(pl.name == nomMort):
				players.pop(players.index(pl))
		
			
		#p.envoiListe("players", [player.name for player in tuables])
		
	#Passe a la suite une fois qu'un mort a ete designe
	#Si le joueur est un villageois, il attendra en dormant que
	#les loups aient tue qqn
	else:
		while True:
			if(nomMort != ''): break
			
			
	print "fini!"
	p.envoi("jour?", "jour")
	p.rec("reveil")
	
	p.envoi("mort",nomMort)

		
	newSocket.close()
	print "Fin de connection avec ", address
			
	#finally:
	comSocket.close()


#Lancement de toutes les parties en parallele
for joueur in xrange(0,nb_joueurs):
	
	thread=threading.Thread(target=partie)
	thread.start()
	threads.append(thread)
		



