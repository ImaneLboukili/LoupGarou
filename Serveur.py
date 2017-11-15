from Protocole import *
import socket
from Joueur import *
import pickle


#initialisation de la partie
nb_joueurs = 4
personages = ["Loup garou", "Villageois"]
players = [Joueur("no one", personages) for i in xrange(0,nb_joueurs)]
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
	p = Protocole(newSocket, '$')
	print "Connecte a ", address
	#while True:
		
	p.envoi("nb_Joueurs",str(nb_joueurs))
	
	p.rec("val")
	
	p.envoiListe("persos",personages)
	
	
	nomJoueur1 = p.rec("nom")

	if(cptJoueurs <nb_joueurs):

		players[cptJoueurs].name = nomJoueur1
		p.envoi("valid", "OK")		

	
		p.rec("merci")

		#permission de continuer si le nombre max de joueur n'est pas atteint
		p.envoi("pers", players[cptJoueurs].perso)
		p.rec("merci2")

		p.envoiListe("players", [player.name for player in players])
		#actualisation de la liste des joueurs
		cptJoueurs += 1

		#################Maintenant la partie est lancee
		
		#attend que des gens soient tues
		while True :
		
			#try:
			d = p.rec("die")
			print "on me dit de tuer",d
			#print players[int(d)]
			
			players.pop(int(d))
			print "j'envoie", [player.name for player in players]
			p.envoiListe("players", [player.name for player in players])
		#except:
			#	message = p.rec("chat")
		
		
	newSocket.close()
	print "Fin de connection avec ", address
		
finally:
    comSocket.close()

