###This file will handle all of the required (master) server 
###
###

import socket, socketserver, threading, sys, time
from datetime import datetime
from getpass import getuser
import pictsql

connected_clients = {}
connected_clients_test = {}

class TCPHandler(socketserver.BaseRequestHandler):
	"""This handles the server for a multi-user chat client,
		it allows clients to connect to the server, it handles mainting the server"""
			

	def handle(self):
	
		print("user connected")		
		self.loggedin = False
		while not self.loggedin:
			
			data = self.request.recv(1024).decode("utf-8")
			if len(data) < 5:
				pass
			else:
				print(data)
				self.check_header(data)
		
		
		self.client_join(self.client_username)
		self.client_key = self.request
		
		if not self.client_username in connected_clients:
		
			connected_clients[self.request] = self.client_username

			self.request.send(welcome_message.encode("utf-8"))
			
						
			while True:
		
				#Ready to recieve chat messages now (from a specific client)						
				try:
					self.data = self.request.recv(1024)
#				print("Recieved data - {} length".format(len(self.data)))
				except socket.error as error:
					self.client_leave(self.client_username)
					return
			
#				if (len(self.data.decode("utf-8"))) != 0:
			
					#Strip any spaces trailing any any sides and prepare the message all users will
					#see
				decoded_data = self.data.strip().decode("utf-8")
					
				self.check_data(decoded_data)
#				else:
#					self.client_leave(self.client_username)

	def check_header(self, data):
		
		splitted_data = data.split("^")
		
		header = splitted_data[0]
		
		if header == 'Registration':
			field_data =splitted_data[1].split("|")
			
		elif header == 'Login':
			field_data = splitted_data[1].split("|")
			self.Username, self.Password = field_data
			print("User {} Password {}".format(self.Username, self.Password))
			if not b.user_login(self.Username, self.Password):

				failedloggedin = "*faiLed*".encode("utf8")
				self.request.send(failedloggedin)

			else:
				loggedin = "*loggEdin*".encode("utf8")
				self.request.send(loggedin)

#		elif header = 'Guess':
#			pass
#		elif header = 'Message':		
#			check_data(splitted_data[1])


	def client_join(self, client_name):
		"""Lets other clients know when someone joins the server, you need to specify the name of
			the client in client_name"""
		pass			


	def client_leave(self, client_name):
		"""Lets other clients know when someone leaves the server, you need to specify the name of
			the client in client_name"""

		pass

	def check_data(self, data):
		"""Prepares the data for a check for specific commands, its basically just checks for an
			! at the start of text"""
	
		if data.startswith("!"):
		
			print("Admin command entered")
			stripped = data.strip("!").lower()
			print(data, stripped)
			self.admin_command_check(stripped)
				
		else:
		
			pass
	
	
	def admin_command_check(self, command):	
		"""Checks if a client is trying to run a special command such as !who, the text from the
			client needs to be specified in data"""

		#This has been implemented (Very) badly but I am short of time...		
		if command == "who":
			online_users = ("There is {} users currently online!".format(len(connected_clients))).encode("utf-8")
#			encoded_users = 
			self.request.send(online_users)
			
			for k, v in connected_clients.items():
				#The various sleep times are to try to ensure the text is formatted nicely.			
				time.sleep(0.2)
				encoded_v = v.encode("utf-8")
				self.request.send(encoded_v)
								
class ThreadedTCP(socketserver.ThreadingMixIn, socketserver.TCPServer):
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
	
	print('Running; type !quit to stop...')
	
	try:
		
		connected = True
		while True:	
		
			server_input = input(">> ")
			
			time.sleep(0.2)

			if len(server_input) == 0:
				print("You need to type something to send!")
			#The max size of a packet is 1024, I assume encoding may add something to its length.
			#1000 is long enough anyway.
			elif len(server_input) >= 1000:
				print("You have exceeded the maximum message size")
			elif server_input.lower() == "!quit":
				shutting_down = ("The server is shutting down, sorry for troubles.").encode("utf-8")
				shutting_down_signal = ("***ShUtdOwn***").encode("utf-8")
				send_message(shutting_down)
				time.sleep(2)	
				send_message(shutting_down_signal)
				sys.exit("Goodbye...")
			#Here for debugging reasons.
			elif server_input == "!dict":
				print(connected_clients)
				
			else:			
				server_data = ("[CONSOLE] - {}".format( server_input))
				send_message(server_data.encode("utf-8"))
			
			
	except KeyboardInterrupt:
		server.shutdown()
		sys.exit("Client closed.")

b = pictsql.SQLManager()
b.path = './data'
b.main()
server_start('127.0.0.1', 2600)			

