from Protocole import *
from Joueur import *
import time
import socket
import threading

#initialisation de la partie
nb_joueurs = 2
personages = ["Loup garou", "Villageois"]
players = [Joueur("no one", personages) for i in xrange(0,nb_joueurs)]
cptJoueurs = 0
threads = []
complet=open('complet.txt','w')

#ouverture de la communication
comSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
comSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
comSocket.bind(('',8000))
comSocket.listen(nb_joueurs)

def creation_partie():

	global cptJoueurs

	#ecoute des clients
	#try:
	newSocket, address = comSocket.accept()
	#newSocket.settimeout(10)
	global p
	p = Protocole(newSocket, '$')
	print "Connecte a ", address	
	p.envoi("nb_Joueurs",str(nb_joueurs))	
	p.rec("val")
	p.envoiListe("persos",personages)
	nomJoueur = p.rec("nom")
	
	players[cptJoueurs].name = nomJoueur
	print players[cptJoueurs].perso
	#p.envoi("valid", "OK")	
	#p.rec("merci")
	#permission de continuer si le nombre max de joueur n'est pas atteint
	p.envoi("pers", players[cptJoueurs].perso)
	p.rec("merci")
	cptJoueurs += 1
	
	
def partie():	
	
	#actualisation de la liste des joueurs
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

for joueur in xrange(0,nb_joueurs):
	thread=threading.Thread(target=creation_partie)
	thread.start()
	threads.append(thread)



for t in threads:
	t.join()

for t in threads:
	("complet","ok")

threads = []

for joueur in xrange(0,nb_joueurs):
	thread=threading.Thread(target=partie)
	thread.start()
	threads.append(thread)
	#time.sleep(2)

