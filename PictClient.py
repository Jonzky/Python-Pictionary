### This is a very basic implementation to ensure the User/SQL queries are handled correctly
### Prior to incorparating the GUI in PyGame

import socket, socketserver, threading, sys, time
from datetime import datetime
from getpass import getuser


easy_host = "127.0.0.1"
max_size = 1024
socket_connected = True
global connecte
#connected.loggedin = False
#connected.failed = False

##############################################################################################################

class ClientConnection(threading.Thread):
	"""This creates a thread off which a client can recieve data from the server"""
	
	def __init__(self, handler):
		
		threading.Thread.__init__(self)
		self.handler = handler
		print(handler)	

	def run(self):
		
		global sock 
		
		try:
			
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((self.easy_host, self.host_port))		
			self.handler.connected = True			
			
		except socket.error as error:
			
			print("Error?")
			sock.close()
			self.handler.connected = False
			return
				
		#Now the client can recieve chat messages
		while True:
			try:	
			
				incoming_data = sock.recv(max_size)
				decoded_data = incoming_data.decode('utf-8')

				if self.handler.loggedin == False:

					if decoded_data == "*loggEdin*":
						print("Fuck yeh")
						self.handler.loggedin = True						
						break
					elif decoded_data == "*faiLed*":
						self.handler.failed = True
						print("Sad Face")
					elif decoded_data == "***ShUtdOwn***":
						print("Server shutting down...")
						sock.close()
						socket_connected = False

					continue

				if len(incoming_data) == 0:
					pass
				elif decoded_data == "***ShUtdOwn***":
					print("Server shutting down...")
					sock.close()
					socket_connected = False
				else:
					print(incoming_data.decode('utf-8'))
			
			except socket.error as error:
				self.handler.warn_exit()


	#Sending data, 
	def send_data(self, data):
		"""Function that sends the clients data"""
	
		try:
			if not socket_connected:
				pass
			elif len(data) == 0:
				print("You need to type something to send!")
			elif len(data) >= 1000:
				print("You have exceeded the maximum message size")	
			else:	
				encoded_data = data.encode("utf-8")
				sock.send(encoded_data)
			
			
					
		except socket.error as error:
			
			sys.exit("An error has occured, please try to connect to the host again, ERROR: {}".format(error))
		


#Adds some reusability to the code above
if __name__ == "__main__":

	pass
		
		
		

