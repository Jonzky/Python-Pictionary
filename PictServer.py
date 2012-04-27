import socket, socketserver, threading, sys, time, ServerGui, random, builtins
from datetime import datetime
from getpass import getuser
import pictsql

address = '127.0.0.1'
port = 2600
ping_dict = {}
ping_dict_buff = {}
connected_dict = {}
builtins.connected_clients = {}

class TCPHandler(socketserver.BaseRequestHandler):
	"""This handles the server for a multi-user chat client,
		it allows clients to connect to the server, it handles mainting the server"""


	def handle(self):



		while True:
			
			
			try:
			
				data = self.request.recv(1024)
				data = data.decode("utf-8")

			except socket.error as error:
				print("Errr************************************************************************************************rror")
				return

			if len(data) < 5:
				pass
				
			else:
				self.check_header(data)
				


	def check_header(self, data):
		
		splitted_data = data.split("^")
		header = splitted_data[0]

		
		if header == 'Registration':
			field_data =splitted_data[1].split("|")

			if b.check_field('username', field_data[0]):

				username_used = "***UsernAmeuSed***".encode("utf8")
				self.request.send(username_used)
				print("Used Already")

			elif b.check_field('email', field_data[2]):

				email_used = "***EmailtAken***".encode("utf8")
				self.request.send(email_used)		
				print("Email used")

			else:

				print("Addd Free")
				b.add_user(field_data[0], field_data[1], field_data[2])

		elif header == 'Login':
		
			field_data = splitted_data[1].split("|")
			self.username, self.password = field_data
			if not b.user_login(self.username, self.password):

				failedloggedin = "*faiLed*".encode("utf8")
				self.request.send(failedloggedin)

			else:
							
				randomint = int(random.randint(1, 100000))
				ping_dict[randomint] = time.clock()

				builtins.connected_clients[randomint] = self.username
				loggedin = "*loggEdin*^{}".format(randomint).encode("utf8")
				
				self.request.send(loggedin)
				
		elif header == 'PING':
			
			ping_data = int(splitted_data[1])
		
			if ping_data in ping_dict:
#				print("Ping recieved")
				ping_dict[ping_data] = time.clock()
		
			else:
				
				print("Error: Ping recieved from {} - Randint - {} - User is not in the dictionary".format(self.client_address, ping_data))
				ping_dict[ping_data] = time.clock()				
				
				
		elif header == 'RECON':
			
			ping_data = int(splitted_data[1])

		
			if self.request in connected_dict:
				print("Error: RECON recieved from {} - Req - {} - User is not in the dictionary".format(self.client_address, self.request))								
			else:
				connected_dict[ping_data] = self.request
		
	def send(self, packet):
	
		for a, b in list(connected_dict.items()):
		#The various sleep times are to try to ensure the text is formatted nicely.
							
#			encoded_v = "DC^{}".format(k).encode("utf8")
			print("Sending DC message")

			try:
				b.send(encoded_v)
			except socket.error as error:
				print("BOOOORRRRKED PIPE - {}".format(error))
				del connected_dict[a]					
		

class ClientPinger(threading.Thread):
	
	def __init__(self):

		super().__init__()
		self.daemon = True
		self.start()
 
	def run(self):
		
		
		while True:
			
			time.sleep(2)
			cur_time = time.clock() 		

			
			
		
			for _k, v in list(ping_dict.items()):

		
#				print("K - {} V - {}".format(k, v))
		

				if (cur_time - v) > 8:
					
					k = int(_k)
					
#					print(ping_dict)
#					print(connected_dict)
#					print(builtins.arrow_dict[k])				

					try:
						del connected_dict[k]
						del ping_dict[k]
						
						if k in builtins.arrow_dict:						
							builtins.arrows.remove(builtins.arrow_dict[k])					
							print("Yey, a client has DC'ed - Shitstorms a brewing. Client - {} Time - {}".format(k, v))
							del builtins.arrow_dict[k]							
					except:
						del ping_dict[k]
					
						print("Errrrors")	

					for a, b in list(connected_dict.items()):
						#The various sleep times are to try to ensure the text is formatted nicely.
							
						encoded_v = "DC^{}".format(k).encode("utf8")
						print("Sending DC message")
						print(b)
						print(connected_dict)
						try:
							b.send(encoded_v)
						except socket.error as error:
							print("BOOOORRRRKED PIPE - {}".format(error))
							del connected_dict[a]					
		
				else:
					pass
#					print("Time - {}, Client-time {}".format(cur_time, v))
				


								
class ThreadedTCP(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass

class ThreadedUDP(socketserver.ThreadingMixIn, socketserver.UDPServer):
	pass
	
	
def server_start(host, port):
	"""This creates the server and then also functions as a prompt for the server operator to use
		the chat application"""

	try:
		server = ThreadedTCP((host, port), TCPHandler)
		server_thread = threading.Thread(target=server.serve_forever)
		server_thread.daemon = True
		server_thread.start()
	except socket.error as error:
		sys.exit("There has been an error trying to create the server, please try again. - ERROR: {}".format(error))
	
	pinger = ClientPinger()
	gui_server = ServerGui.start(address, port)


if __name__ == "__main__":
	b = pictsql.SQLManager()
	b.path = './data'
	b.main()
	server_start(address, port)			

