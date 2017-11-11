class Protocole:
	#this class provides methods to send and receive data avoiding buffer issues
	#we format our data flow as follows : 
	#ID:data$ID:data$.....	
	
	def __init__(self, socket, fin):
		self.fin = fin
		self.s = socket
		
	def envoi(self, ID, data):
		envoi = ID +":" + str(data) + self.fin
		self.s.sendall(envoi)
	
	def envoiListe(self, ID, data):
		self.envoi(ID, ','.join(data))
		
	def envoiGroupe(self, ID, data):
		res = str()
		for iD, d in ID, data:
			res += iD +":" + str(d) + self.fin
		self.sendall(res)

	def rec(self, ID):
		data = self.s.recv(1024)
		print "recu : ",data
		data = data.split(':')
		data = data[data.index(ID)+1]
		data = data.split(self.fin)[0]
		return data

	def recListe(self, ID):	
		d = self.rec(ID)
		print d
		return d.split(',')
		
	def recGroupe(self, ID):
		data = self.rec(ID)
		res = []
		for iD in ID:
			data = data.split(':')
			data = data[data.index(ID)+1]
			data = data.split(self.fin)[0]
			res.append(res)
		return res
			
