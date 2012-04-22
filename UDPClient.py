import socket, socketserver, threading, sys, time
from datetime import datetime
from getpass import getuser
import pictsql


clients = []

class ClientUDP(threading.Thread):

#	def __init__(self):
#		
#		super().__init__()
		
		

	def run(self):
	
		print("ping")
	
		HOST, PORT = "localhost", 9999

		self.host = '127.0.0.1'
		self.port = 2500

		# SOCK_DGRAM is the socket type to use for UDP sockets
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		

		# As you can see, there is no connect() call; UDP has no connections.
		# Instead, data is directly sent to the recipient via sendto().
#		sock.sendto(data + "\n", (HOST, PORT))
#		received = sock.recv(1024)

#		print "Sent:     {}".format(data)
#		print "Received: {}".format(received)
		

	def update_position(self, type, x, y, speed, direction):
		

		self.host = '127.0.0.1'
		self.port = 2600
		
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#		print(self.sock)
	

		stringa = "{}*{}*{}*{}*{}".format(type, x, y, speed, direction).encode('utf8')
#		print('1')
	
		
#		stringa = "Type {} - Speed {} - Direction {}".format(type, speed, direction).encode('utf8')
		
		self.sock.sendto(stringa, (self.host, self.port))
		
