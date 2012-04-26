### This is a very basic implementation to ensure the User/SQL queries are handled correctly
### Prior to incorparating the GUI in PyGame

import socket, socketserver, threading, sys, time, ShootPyGame, builtins
from getpass import getuser


max_size = 1024
#connected.loggedin = False
#connected.failed = False

##############################################################################################################

class ClientConnection(threading.Thread):
	"""This creates a thread off which a client can recieve data from the server"""
	
	def __init__(self, handler, host, port):
		
		super().__init__()
		self.daemon = True
		self.host = host
		self.port = port
		self.handler = handler
		self.running = True

	def run(self):
		
		global sock 
		
		try:
		
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)			
			sock.connect((self.host, self.port))
			self.handler.connected = True
			
		except socket.error as error:
			
			sock.close()
			self.handler.connected = False
			return
				
		while self.running:
			try:	
			
				incoming_data = sock.recv(max_size)
				print("Recieved")
				if self.handler.loggedin == False:

					decoded_data = incoming_data.decode('utf-8').split("^")

					if decoded_data[0] == "*loggEdin*":
						self.randomint = decoded_data[1]
						self.handler.loggedin = True
						break
	
					elif decoded_data[0] == "*faiLed*":
						self.handler.failed = True
						print("Sad Face")
					elif decoded_data[0] == "***UsernAmeuSed***":
						print("username used")
					elif decoded_data[0] == "***EmailtAken***":
						print("email used...")
			
			except socket.error as error:
				self.handler.warn_exit()
				
				
		print("Done")
		return
		
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



class TCPConnection(threading.Thread):
	"""This creates a thread off which a client can recieve data from the server"""
	
	def __init__(self, master, randomint, host, port):
		
		super().__init__()
		self.daemon = True
		self.host = host
		self.port = port
		self.randomint = randomint
		self.start()
		self.zero_count = 0
		self.master = master

	def run(self):
		
		global sock 
		
		try:
			
			
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)			
			sock.connect((self.host, self.port))

			recon_pack = "RECON^{}".format(self.randomint).encode('utf8')
			
			sock.send(recon_pack)
			
		except socket.error as error:
			
			sock.close()
			sys.exit("An error has occured, please try to connect to the host again, ERROR: {}".format(error))
			return
				
		while True:
			try:	
				print("Trying")
				incoming_data = sock.recv(max_size)
				print(len(incoming_data))

				decoded_data = incoming_data.decode('utf-8')

				if len(decoded_data) == 0:
					self.zero_count += 1
					if self.zero_count >=30:
						self.master.running = False
				elif decoded_data == "***ShUtdOwn***":
					print("Shut this shit DOWWWWWN!")
				elif decoded_data.startswith("DC"):
				
					split_data = decoded_data.split("^")
					randomint = int(split_data[1])
					builtins.arrows.remove(builtins.arrow_dict[randomint])
					print("Fuck yeh?")

				else:
					print(incoming_data.decode('utf-8'))
			
			except socket.error as error:
				sys.exit("An error has occured, please try to connect to the host again, ERROR: {}".format(error))


class ClientPinger(threading.Thread):
	
	def __init__(self, host, port, randomint):

		super().__init__()
		self.daemon = True
		self.host = host
		self.port = port
		self.randomint = randomint
		self.start()


	def run(self):
				
		try:
			
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.connect((self.host, self.port))		
			
			
		except socket.error as error:
			
			sock.close()
			sys.exit("An error has occured, please try to connect to the host again, ERROR: {}".format(error))			
			return
				
		
		ping_packet = "PING^{}".format(self.randomint).encode("utf8")
				
		while True:
			
			try:
			
				time.sleep(2)
				self.socket.send(ping_packet)
				
			except socket.error as error:
				sys.exit("An error has occured, please try to connect to the host again, ERROR: {}".format(error))


