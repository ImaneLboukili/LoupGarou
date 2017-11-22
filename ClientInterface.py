from Tkinter import *
import random as rd 
from socket import *
import time
import sys

from Protocole import *
from Joueur import *

adresse_serveur = str(sys.argv[1])
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
		self.N = Label(text ="Nouvelle partie de Loup Garou\n \nVeuillez entrer votre nom")
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
		self.N['text'] = "Nous attendons les autres participants"
		self.p.envoi("nom", self.e.get())
		pe = self.p.rec("pers")
		self.perso = pe
		self.p.envoi("merci", "ok")
		
		#Attent que le serveur indique que tous les joueurs ont rejoint la
		#partie
		go = ''
		while True:
			go = self.socket.recv(1024)
			print go
			if(go=="go"):break
		self.socket.send("go!")
		
		#Interface de la partie
		top=Toplevel()
		top.title("La partie est lancee.")		
		notiLabel = Label(top, text ="Vous etes un "+self.perso+".", font=('Times', 20))
		notiLabel.grid(row=0,column=0, sticky=W)
		self.joueursLabel = Label(top, text = "", font=('Times', 20))
		self.joueursLabel.grid(row=1,column=0, sticky=W)
		self.MAJplayers()
		vote = Button(top, text="Vote", width =50, command = self.Vote)
		vote.grid(row=6, column=0)


	#Met a jour la liste des joueurs de la fenetre de partie
	#En demandant une actualisation au serveur
	def MAJplayers(self):
		
		per = self.p.recListe("players")
		self.playersNames = per
		txt = "Vous jouez actuellement avec : "
		for player in self.playersNames:
			txt += "\n"+ player
		self.joueursLabel.config(text=txt)
		
	#Ouvre une fenetre de deliberation chez les clients pour 
	#designer le mort du jour	
	def Vote(self):
		
		#Interface de la fenetre de vote
		self.topvote=Toplevel()
		self.topvote.title("Let's vote...")
		notiLabel = Label(self.topvote, text ="Qui souhaitez vous tuer, "+self.perso+" ? \nDeliberez en utilisant le chat ci dessous", font=('Times', 20))
		notiLabel.grid(row=0,column=0, sticky=W)
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
		self.chat += "\n" +self.players[0].name+" : " + self.field.get()
		self.chatLabel.config(text=self.chat)
		self.field.delete(0, 'end')
		
	#Tue un joueur et efface son nom de la liste des joueurs de la fenetre de partie
	#supprime le joueur de la liste dans le serveur
	def die(self):
		self.p.envoi("die", self.listusers.curselection()[0])
		self.MAJplayers()
		self.topvote.destroy()
	
			
	
game = Partie(socket)

