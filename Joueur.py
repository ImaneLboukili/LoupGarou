import random as rd 

class Joueur :
	
	def __init__(self, name, personages):
		
		self.name = name
		self.perso = rd.sample(personages,1)[0]
		self.state = "vivant"
