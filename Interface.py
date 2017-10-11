from Tkinter import *
import random as rd 
from Joueur import *

class Partie:

	def __init__(self, root, personages, nbJoueurs):
		self.user = ""
		self.chat = ""
		self.nbJoueurs = nbJoueurs
		self.players = [Joueur("no one", personages) for i in xrange(0,nbJoueurs)]
		self.perso = ""
		self.root = root
		self.personages = personages
		self.cptJoueurs = 0
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
		
	def getchat(self):
		self.chat += "\n" +self.player[0].name+" : " + self.field.get()
		self.chatLabel.config(text=self.chat)
		self.field.delete(0, 'end')
		
		
	def die(self):
		print "****************", self.listusers.curselection()[0]
		self.players.pop(self.listusers.curselection()[0])
		self.MAJplayers()
		self.topvote.destroy()
		
	def MAJplayers(self):
		txt = "Vous jouez actuellement avec : "
		for player in self.players:
			txt += "\n"+ player.name
		self.joueursLabel.config(text=txt)
		
	def Play(self):
		print "nombre de joueurs : ", self.cptJoueurs
		if(self.cptJoueurs <self.nbJoueurs):
			self.players[self.cptJoueurs].name = self.e.get()
			if(self.cptJoueurs == 0):
				top=Toplevel()
				top.title("La partie est lancee.")
				notiLabel = Label(top, text ="Vous etes un "+self.players[0].perso+".", font=('Times', 20))
				notiLabel.grid(row=0,column=0, sticky=W)
					
				self.joueursLabel = Label(top, text = "", font=('Times', 20))
				self.MAJplayers()
				self.joueursLabel.grid(row=1,column=0, sticky=W)
				
				vote = Button(top, text="Vote", width =50, command = self.Vote)
				vote.grid(row=6, column=0)
			else:
				self.MAJplayers()
				
			self.cptJoueurs +=1
		
		
		
	def Vote(self):
		self.topvote=Toplevel()
		self.topvote.title("Let's vote...")
		notiLabel = Label(self.topvote, text ="Qui souhaitez vous tuer, "+self.players[0].name+" ? \nDeliberez en utilisant le chat ci dessous", font=('Times', 20))
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

		for item in self.players:
			self.listusers.insert(END, item.name)
			
	
root=Tk()
root.title("Loup Garou")

game = Partie(root, ["Loup garou", "Villageois"], 4)
