from Tkinter import *
import random as rd 
from Joueur import *
from socket import *
import pickle
from Protocole import *

complet = open("complet.txt", 'r')

class Partie:

	def __init__(self):
	
		#recuperation des donnes de la partie depuis le serveur
		#Nombre de joueurs, persos disponibles...
		
		self.socket = socket(AF_INET, SOCK_STREAM)
		self.socket.connect(('127.0.0.1',8000))
		print "Connexion au serveur"
		
		self.p = Protocole(self.socket, '$')
		self.nbJoueurs = self.p.rec("nb_Joueurs")
		print "nombre de joueurs : ", self.nbJoueurs
		
		self.p.envoi("val", "OK")
		
		self.personages = self.p.recListe("persos")
		print "personages : ", self.personages 
		
		#Creation de l'interface
		self.root = Tk()
		self.chat = ""
		self.root.title("Loup Garou")
		s = Label(text ="Bienvenue", font=(('Times'),20))
		s.grid(row=2,column=0)

		N = Label(text ="Nouvelle partie de Loup Garou\n \nVeuillez entrer votre nom")
		N.grid(row=3,column=0)

		self.e = Entry(self.root)
		self.e.focus_set()
		self.e.grid(row=4, column=0)
		
		play = Button(text="Play", width =50, command = self.Play)
		play.grid(row=6, column=0)
		
		self.root.mainloop()
	
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
	
	#Met a jour la liste des joueurs de la fenetre de partie
	def MAJplayers(self):
		self.playersNames = self.p.recListe("players")
		print self.playersNames
		txt = "Vous jouez actuellement avec : "
		for player in self.playersNames:
			txt += "\n"+ player
		self.joueursLabel.config(text=txt)
	
	#Lance la fenetre de la partie
	def Play(self):
		self.p.envoi("nom", self.e.get())
		valid = self.p.rec("valid")
		#si le serveur dit que le client peut joueur
		if(valid=="OK"):
			
			
			'''complet = 0
			while (complet ==0):
				complet = int(rec("feuvert"))'''
				
			wait=Toplevel()
			wait.title("La partie est lancee.")
			notiLabel = Label(wait, text ="Nous attendons les autres participants", font=('Times', 20))
			notiLabel.grid(row=0,column=0, sticky=W)
			comp = 0
			while ('1' not in complet.read()):
				comp = 0
				
			wait.destroy()
			
			top=Toplevel()
			top.title("La partie est lancee.")
			self.p.envoi("merci", "ok")
			#le serveur envoie au client la liste des autres persos
			self.perso = self.p.rec("pers")
			self.p.envoi("merci2", "ok")
			notiLabel = Label(top, text ="Vous etes un "+self.perso+".", font=('Times', 20))
			notiLabel.grid(row=0,column=0, sticky=W)
			self.joueursLabel = Label(top, text = "", font=('Times', 20))
			self.joueursLabel.grid(row=1,column=0, sticky=W)
			self.MAJplayers()
			vote = Button(top, text="Vote", width =50, command = self.Vote)
			vote.grid(row=6, column=0)
			
	#ouvre une fenetre de deliberation chez les clients pour designer le mort du jour	
	def Vote(self):
		self.topvote=Toplevel()
		self.topvote.title("Let's vote...")
		notiLabel = Label(self.topvote, text ="Qui souhaitez vous tuer, "+self.playersNames[0]+" ? \nDeliberez en utilisant le chat ci dessous", font=('Times', 20))
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

game = Partie()

