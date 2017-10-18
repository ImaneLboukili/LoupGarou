
import socket

comSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
comSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
comSocket.bind(('',8000))

nb_joueurs = 4


comSocket.listen(nb_joueurs)

try:
   while True:
		newSocket, address = comSocket.accept()
		print "Connecte a ", address
		while True:
			receivedData = newSocket.recv(1024)
			if not receivedData: break
			tosend = str(time.ctime())
			newSocket.sendall(tosend)
		newSocket.close()
		print "Fin de connection avec ", address
		
finally:
    comSocket.close()

