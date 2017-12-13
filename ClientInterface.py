from Tkinter import *
import random as rd 
from socket import *
import time
import sys

from Protocole import *
from Joueur import *

adresse_serveur = str(sys.argv[1])
print "Demande de connexion"
socket = socket(AF_INET, SOCK_STREAM)
socket.connect((adresse_serveur,8000))
print "Connecte au serveur"


class Partie:

	def __init__(self, socket):
			
		self.socket = socket
		self.p = Protocole(self.socket, '$')
		
		#recuperation des donnes de la partie depuis le serveur
		#Nombre de joueurs, persos disponibles...
		self.nbJoueurs = self.p.rec("nb_Joueurs")
		self.p.envoi("val", "OK")
		self.personages = self.p.recListe("persos")

		#Creation de l'interface pour l'identification des joueurs
		self.root = Tk()
		self.chat = ""
		self.root.title("Loup Garou")
		s = Label(text ="Bienvenue", font=(('Times'),20))
		s.grid(row=2,column=0)
		self.N = Label(self.root, text ="Nouvelle partie de Loup Garou\n \nVeuillez entrer votre nom")
		self.N.grid(row=3,column=0)
		self.e = Entry(self.root)
		self.e.focus_set()
		self.e.grid(row=4, column=0)	
		play = Button(text="Play", width =50, command = self.Play)
		play.grid(row=6, column=0)
		self.root.mainloop()

	
	#Lance la fenetre de la partie
	def Play(self):
		
		#Envoi du nom et recuperation du personnage associe par le serveur
		self.N = Label(self.root, text ="Nous attendons les autres participants")
		self.N.grid(row=3,column=0)
		#self.N = "Nous attendons les autres participants"
		self.nom = self.e.get()
		#self.root.mainloop()
		self.p.envoi("nom", self.nom)
		pe = self.p.rec("pers")
		self.perso = pe
		self.p.envoi("merci", "ok")
		
		self.top=Toplevel()
		self.top.title("La partie est lancee.")		
		self.noti = Label(self.top, text ="Vous etes un "+self.perso+".", font=('Times', 20))
		self.noti.grid(row=0,column=0, sticky=W)
		#self.joueursLabel = Label(self.top, text = "", font=('Times', 20))
		#self.joueursLabel.grid(row=1,column=0, sticky=W)
		#self.MAJplayers()
		vote = Button(self.top, text="OK", width =50, command = self.suite)
		vote.grid(row=6, column=0)
		self.top.mainloop()
		#Attent que le serveur indique que tous les joueurs ont rejoint la
		#partie
	def suite (self):
		go = ''
		while True:
			go = self.socket.recv(1024)
			if(go=="go"):break
		self.socket.send("go!")
		
		#Interface de la partie
		'''self.top=Toplevel()
		self.top.title("La partie est lancee.")		
		self.notiLabel = Label(self.top, text ="Vous etes un "+self.perso+".", font=('Times', 20))
		self.notiLabel.grid(row=0,column=0, sticky=W)'''
		self.joueursLabel = Label(self.top, text = "", font=('Times', 20))
		self.joueursLabel.grid(row=1,column=0, sticky=W)
		self.MAJplayers()
		#vote = Button(self.top, text="Vote", width =50, command = self.VoteVillage)
		#vote.grid(row=6, column=0)
		
		self.p.envoi("nuit?","ok")
		nuit = "jour"
		#les joueurs attendent le signal pour s'endormir
		while True:
			nuit = self.socket.recv(1024)
			if(nuit=="nuit"):
				print "avant nuit"
				self.Nuit()
				break
		#self.top.mainloop()
		
	#def reveil(self):
		while True:
			print "avant nuit recue"
			nuit = self.p.rec("jour?")
			#print "apres nuit recue"
			#print "nuit recue" ,nuit
			if(nuit=="jour"):
				break
		self.p.envoi("reveil","ok")
		nomMort = self.p.rec("mort")
		self.notiLabel['text'] =  ("Vous etes un "+self.perso+".\n Le jour se leve. \n"+ nomMort+" a ete tue par les loups.")
		#self.VoteVillage()
				
				
	def Nuit(self):
		
		if(self.perso == "Villageois"):
			self.noti = Label(self.top, text ="Vous etes un "+self.perso+". \nLa nuit est tombee. Faites le dodo.", font=('Times', 20))
			self.noti.grid(row=0,column=0, sticky=W)
			#self.top.mainloop()
			
		if(self.perso == "Loup garou"):
			self.notiLabel = Label(self.top, text ="Vous etes un "+self.perso+". \nLa nuit est tombee.\n Decidez de votre victime dans la nouvelle fenetre.", font=('Times', 20))
			self.notiLabel.grid(row=0,column=0, sticky=W)
			print "avant voteloups"
			self.VoteLoups()
			
	#Met a jour la liste des joueurs de la fenetre de partie
	#En demandant une actualisation au serveur
	def MAJplayers(self):
		
		per = self.p.recListe("players")
		self.playersNames = per
		txt = "Vous jouez actuellement avec : "
		for player in self.playersNames:
			txt += "\n"+ player
		self.joueursLabel.config(text=txt)
		
			
	def VoteLoups(self):
		#Interface de la fenetre de vote
		self.voteLoups=Toplevel()
		self.voteLoups.title("Let's vote...")
		notiLab = Label(self.voteLoups, text ="Qui souhaitez vous tuer dans son sommeil ? \nDeliberez en utilisant le chat ci dessous. \n Si vous ne trouvez pas de compromis, la majorite l'emportera.", font=('Times', 20))
		notiLab.grid(row=0,column=0, sticky=W)
		chatLabel = Label(self.voteLoups, text ="", font=('Times', 14), height = 20, width = 40, background="white")
		chatLabel.grid(row=1,column=0, sticky=W)	
		field = Entry(self.voteLoups)
		field.focus_set()
		field.grid(row=2, column=0)
		self.listtuables = Listbox(self.voteLoups)
		self.listtuables.grid(row=1,column=1, sticky=W)	
		b = Button(self.voteLoups, text="You die", command = self.dieLoups)
		b.grid(row=2, column=1)
		ok = Button(self.voteLoups, text="Ok", width =50, command=self.getchat)
		ok.grid(row=7, column=0)
		#le serveur envoie la liste des persos non loups garous pouvant 
		#etre tues
		tuables = self.p.recListe("tuables")
		for item in tuables:
			self.listtuables.insert(END, item)
		self.voteLoups.mainloop()
		
	#Ouvre une fenetre de deliberation chez les joueurs pour 
	#designer la personne choisie par tout le village pour mourrir
	def VoteVillage(self):
		
		#Interface de la fenetre de vote
		self.topvote=Toplevel()
		self.topvote.title("Let's vote...")
		notiLab = Label(self.topvote, text ="Qui souhaitez vous tuer, "+self.perso+" ? \nDeliberez en utilisant le chat ci dessous", font=('Times', 20))
		notiLab.grid(row=0,column=0, sticky=W)
		self.chatLabel = Label(self.topvote, text ="", font=('Times', 14), height = 20, width = 40, background="white")
		self.chatLabel.grid(row=1,column=0, sticky=W)	
		self.field = Entry(self.topvote)
		self.field.focus_set()
		self.field.grid(row=2, column=0)
		self.listusers = Listbox(self.topvote)
		self.listusers.grid(row=1,column=1, sticky=W)	
		b = Button(self.topvote, text="You die", command = self.die)
		b.grid(row=2, column=1)
		ok = Button(self.topvote, text="Ok", width =50, command=self.getchat)
		ok.grid(row=7, column=0)
	
		for item in self.playersNames:
			self.listusers.insert(END, item)


	#recupere la valeur d'un message dans le chat, et l'affiche a la suite des autres
	def getchat(self):
		self.chat += "\n" +self.nom+" : " + self.field.get()
		self.chatLabel.config(text=self.chat)
		self.field.delete(0, 'end')
	
	def dieLoups(self):
		self.p.envoi("die", self.listtuables.curselection()[0])
		#self.MAJplayers()
		self.voteLoups.destroy()
	
		
		
	#Tue un joueur et efface son nom de la liste des joueurs de la fenetre de partie
	#supprime le joueur de la liste dans le serveur
	def die(self):
		self.p.envoi("die", self.listusers.curselection()[0])
		self.MAJplayers()
		self.topvote.destroy()
	
			
	
game = Partie(socket)

