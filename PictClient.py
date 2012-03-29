### This is a very basic implementation to ensure the User/SQL queries are handled correctly
### Prior to incorparating the GUI in PyGame

import socket, socketserver, threading, sys, time
from datetime import datetime
from getpass import getuser


easy_host = "127.0.0.1"
max_size = 1024
socket_connected = True
global connected
connected = False

##############################################################################################################

class ClientConnection(threading.Thread):
	"""This creates a thread off which a client can recieve data from the server"""
	
	def run(self):
		
		global sock 
		
		try:
			
			
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((self.easy_host, self.host_port))		
			

		except socket.error as error:
			print("An error has occured and you have been unable to connect to the host, please try again. ERROR: {}".format(error))
			global socket_connected
			socket_connected = False
			sock.close()

		except (OverflowError, ValueError):
		
			print("The chosen port must be between 0-65535, please try again")
			main()
		
		#Now the client can recieve chat messages
		while True:
			try:	
			
				incoming_data = sock.recv(max_size)
				if len(incoming_data) == 0:
					pass
				elif incoming_data.decode("utf-8") == "***ShUtdOwn***":
					print("Server shutting down...")
					sock.close()
					socket_connected = False
				else:
					print(incoming_data.decode('utf-8'))
			
			except socket.error as error:
				sys.exit("An error has occured, please try to connect to the host again, ERROR: {}".format(error))

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
		



def client_input(host, port):
	"""This creates the socket on the client and also prompts the client to input messages to be sent"""

	client_socket = ClientConnection()
	client_socket.easy_host = host
	client_socket.host_port = port
	
	# After hours of issues it came down to the thread not being daemon and it would restict the
	# program from terminating...
	client_socket.daemon = True
	client_socket.start()

	time.sleep(1)
	connected = True
	print("Teg")

def main():
	"""The main function which allows the user to choose what the application should be used for
		(client/server)"""

	while not connected:

		if not socket_connected:
			sys.exit("The server has been shutdown")
		
		try:		
	
			server_port = int(input("Please input the server's port to join >> "))
			client_input(easy_host, server_port)
			
		except (OverflowError, ValueError):
			print("The chosen port must be between 0-65535, please try again")

		print(connected)

#Adds some reusability to the code above
if __name__ == "__main__":

	main()
		
		
		

