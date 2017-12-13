import random as rd 

class Joueur :
	
	def __init__(self, name, personage):
		
		self.name = name
		self.perso = personage
		self.state = "vivant"
