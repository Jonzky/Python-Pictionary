### This is a very basic implementation to ensure the User/SQL queries are handled correctly
### Prior to incorparating the GUI in PyGame

import socket, socketserver, threading, sys, time, ShootPyGame
from getpass import getuser


max_size = 1024
#connected.loggedin = False
#connected.failed = False

##############################################################################################################

class ClientConnection(threading.Thread):
	"""This creates a thread off which a client can recieve data from the server"""
	
	def __init__(self, handler):
		
		
		threading.Thread.__init__(self)
		self.handler = handler

	def run(self):
		
		global sock 
		
		try:
			
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((self.easy_host, self.host_port))		
			self.handler.connected = True
			
		except socket.error as error:
			
			sock.close()
			self.handler.connected = False
			return
				
		while True:
			try:	
			
				incoming_data = sock.recv(max_size)
				if self.handler.loggedin == False:

					decoded_data = incoming_data.decode('utf-8').split("^")

					if decoded_data[0] == "*loggEdin*":

						randomint = decoded_data[1]
					
						self.handler.loggedin = True
						a = ShootPyGame.start(self.easy_host, self.host_port, randomint)
						self.handler.parent.destroy()
						
					elif decoded_data[0] == "*faiLed*":
						self.handler.failed = True
						print("Sad Face")
					elif decoded_data[0] == "***UsernAmeuSed***":
						print("username used")
					elif decoded_data[0] == "***EmailtAken***":
						print("email used...")

					continue

				decoded_data = incoming_data.decode('utf-8')

				if len(incoming_data) == 0:
					pass
				else:
					print(incoming_data.decode('utf-8'))
			
			except socket.error as error:
				self.handler.warn_exit()


	#Sending data, 
	def send_data(self, data):
		"""Function that sends the clients data"""
		try:
			if len(data) == 0:
				print("You need to type something to send!")
			elif len(data) >= 1000:
				print("You have exceeded the maximum message size")	
			else:	
				encoded_data = data.encode("utf-8")
				sock.send(encoded_data)
		except socket.error as error:			
			sys.exit("An error has occured, please try to connect to the host again, ERROR: {}".format(error))


		
		
		

