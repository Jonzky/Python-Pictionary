import socket, socketserver, threading, sys, time
from datetime import datetime
from getpass import getuser
global ghost, gport 




class UDPHandler(socketserver.BaseRequestHandler):
	"""This handles the server for a multi-user chat client,
		it allows clients to connect to the server, it handles mainting the server"""


	def handle(self):
        
		data = self.request[0].strip().decode('utf8')
		socket = self.request[1]
		
		self.proccess_data(data)
		
		print("{} wrote: /n".format(self.client_address[0]))
		print(data)

	def proccess_data(self, data):
		
		stripped_data = data.split('*')
#		stringa = "{}*{}*{}*{}*{}".format(type, x, y, speed, direction).encode('utf8')		
		if stripped_data[0] == 3:
			pass
			#ServerGUI.Bullet(stripped_data[4], stripped_data[1], stripped_data[2])

class ThreadedUDP(socketserver.ThreadingMixIn, socketserver.UDPServer):
	pass
	


	
#	connected = True
		
#	while True:	
		
#		server_input = input(">> ")
#			
#		time.sleep(0.2)	
						
