import socket, socketserver, threading, sys, time
from datetime import datetime
from getpass import getuser
import pictsql

arrow_dict = {}
clients = []

class ClientUDP(threading.Thread):

	def __init__(self, host, port):
		
		super().__init__()
		self.daemon = True
		self.start()
		self.host = host
		self.port = port
				



	def run(self):
	
		print("ping")
	

		# SOCK_DGRAM is the socket type to use for UDP sockets
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		
		while True:
				
			incoming_data = self.sock.recv(1024)
	
			if len(incoming_data) == 0:
				pass
			elif incoming_data.decode("utf-8") == "***ShUtdOwn***":
				print("Server shutting down...")
				self.sock.close()
			else:
				
				print(incoming_data.decode('utf-8'))
				process_data(incoming_data.decode('utf-8'))

		# As you can see, there is no connect() call; UDP has no connections.
		# Instead, data is directly sent to the recipient via sendto().
#		sock.sendto(data + "\n", (HOST, PORT))
#		received = sock.recv(1024)

#		print "Sent:     {}".format(data)
#		print "Received: {}".format(received)


	def process_data(self, data):
	
		stripped_data = data.split('*')
#		stringa = "{}*{}*{}*{}*{}".format(type, x, y, speed, direction).encode('utf8')		
		print(stripped_data[0])


		stripped_data[0] = int(stripped_data[0])
		stripped_data[4] = float(stripped_data[4])
		stripped_data[3] = float(stripped_data[3])
		stripped_data[1] = int(stripped_data[1])
		stripped_data[2] = int(stripped_data[2])

		if stripped_data[0] == 3:
			a = Bullet(stripped_data[4], stripped_data[1], stripped_data[2])
			bullets.add(a)
		elif stripped_data[0] == 4:
			arrow_dict[stripped_data[0]] = Arrow(stripped_data[4], stripped_data[1], stripped_data[2])
			arrows.add(arrow_dict[stripped_data[0]])
#			clients[self.client_address] = True
		elif stripped_data[0] == 2:
			pass		

	def update_position(self, username, x, y, speed, direction, type):
		
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#		print(self.sock)
	

		stringa = "{}*{}*{}*{}*{}*{}".format(username, x, y, speed, direction, type).encode('utf8')
#		print('1')
	
		
#		stringa = "Type {} - Speed {} - Direction {}".format(type, speed, direction).encode('utf8')
		
		self.sock.sendto(stringa, (self.host, self.port))
		
