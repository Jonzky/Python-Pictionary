import socket, socketserver, threading, sys, time
from datetime import datetime
from getpass import getuser
import pictsql

arrow_dict = {}
clients = []

class ClientUDP(threading.Thread):

	def __init__(self, host, port, randomint, bullets, arrows):
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		super().__init__()
		self.daemon = True
		self.start()
		self.host = host
		self.port = port
		self.randomint = str(randomint)
		self.arrows = arrows
		self.bullets = bullets

	def run(self):		
		
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


	def process_data(self, data):
	
		stripped_data = data.split('*')
		
		
		stripped_data[0] = str(stripped_data[0])
		
		if stripped_data[0] == self.randomint:
			return
		
		stripped_data[5] = int(stripped_data[5])
		stripped_data[4] = float(stripped_data[4])
		stripped_data[3] = float(stripped_data[3])
		stripped_data[1] = int(stripped_data[1])
		stripped_data[2] = int(stripped_data[2])

		if stripped_data[5] == 3:
			a = ShootPyGame.OtherBullet(stripped_data[4], stripped_data[1], stripped_data[2])
			self.bullets.add(a)
		elif stripped_data[5] == 4:
			global arrows
			arrow_dict[stripped_data[0]] = ShootPyGame.OtherArrow(stripped_data[4], stripped_data[1], stripped_data[2])
			self.arrows.add(arrow_dict[stripped_data[0]])
		elif stripped_data[5] == 2:
			arrow_dict[stripped_data[0]].update_pos(stripped_data[1], stripped_data[2], stripped_data[3], stripped_data[4])

	def update_position(self, username, x, y, speed, direction, type):
		
		stringa = "{}*{}*{}*{}*{}*{}".format(username, x, y, speed, direction, type).encode('utf8')
		
		self.sock.sendto(stringa, (self.host, self.port))
		
