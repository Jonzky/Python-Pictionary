###This file will handle all of the required (master) server 
###
###

import socket, socketserver, threading, sys, time, ServerGui, random
from datetime import datetime
from getpass import getuser
import pictsql


address = '127.0.0.1'
port = 2500

connected_clients = {}
connected_clients_test = {}

class TCPHandler(socketserver.BaseRequestHandler):
	"""This handles the server for a multi-user chat client,
		it allows clients to connect to the server, it handles mainting the server"""


	def handle(self):

#		while True:
#		
#			print(self.request)
#			print(self.client_key)
#			print(self)
#			time.sleep(3)
	
#		self.request.loggedin = False
		print("user connected")		

		while True:
			
			try:
			
				data = self.request.recv(1024)
				data = data.decode("utf-8")

			except socket.error as error:
				print("Errrrror")
				return

			if len(data) < 5:
				pass
				
			else:
				print(data)
				self.check_header(data)
				


	def check_header(self, data):
		
		splitted_data = data.split("^")
		
		header = splitted_data[0]
		
		if header == 'Registration':
			field_data =splitted_data[1].split("|")
			
			print(field_data[0])

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
			
				randomint = random.randint(1, 100000)
				print("Raaaaaaandomint - {}".format(randomint))
				connected_clients[randomint] = self.username
				loggedin = "*loggEdin*^{}".format(randomint).encode("utf8")
				self.request.send(loggedin)

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
	
	
	print('Running; type !quit to stop...')
	
#	try:
	gui_server = ServerGui.start(address, port)
#	gui_server.daemon = False
#	gui_server.start()			
	
#	except KeyboardInterrupt:
#		server.shutdown()
#		sys.exit("Client closed.")

if __name__ == "__main__":
	b = pictsql.SQLManager()
	b.path = './data'
	b.main()
	server_start(address, port)			

