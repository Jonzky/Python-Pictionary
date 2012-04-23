
import pygame, random, math, UDPTests, socket, socketserver, threading, sys
from time import clock as clocky
# image from http://www.frambozenbier.org/index.php/raspi-community-news/20167-antiloquax-on-getting-stuck-in-to-python


clients = []
arrow_dict = {}

global connected_clients

class Bullet(pygame.sprite.Sprite):

	def __init__(self, direction, x, y):

		super().__init__()

		self.image = pygame.image.load('shot.png').convert()
		self.lifetime = 10
		self.direction = direction
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.image = pygame.transform.rotate(self.image, self.direction)
		self.rect = self.image.get_rect(center=self.rect.center)					

	def update(self):

		self.move()
		self.timer()
		self.update_client()
				
	def timer(self):

		if self.lifetime < 0:
			bullets.remove(self)
			return False
		self.lifetime -= 0.3

	def move(self):
	
		radian_angle = math.radians(self.direction)
		self.rect.centerx += (10*(math.cos(radian_angle)))
		self.rect.centery -= (10*(math.sin(radian_angle)))
	
	def update_client(self):
	
		pass		

class Arrow(pygame.sprite.Sprite):
	
	def __init__(self, direction, x, y):
	
		super().__init__()
		self.clock = clocky()
		self.direction = direction
		self.gospeed = 0
		self.image = pygame.image.load('test.png').convert()
		background = self.image.get_at((0, 0))
		self.image.set_colorkey(background)
		
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.original = self.image
		self.olddirection = self.direction

	def update(self):	
		
		self.move()

	def update_pos(self, centerx, centery, gospeed, direction):
		
		self.rect.centerx, self.rect.centery, self.gospeed, self.direction = centerx, centery, gospeed, direction		
			
	def transform(self):
		pass

	def slowdown(self):
			
		self.gospeed -= 0.02
		self.move()
		
	def move(self):
		
		if self.gospeed <= 0:
			pass
		else:
				
			speeed = math.exp(self.gospeed)
			radian_angle = math.radians(self.direction)
			self.rect.centerx += (speeed*(math.cos(radian_angle)))
			self.rect.centery -= (speeed*(math.sin(radian_angle)))			
		if self.direction != self.olddirection:	
			self.image = pygame.transform.rotate(self.original, self.direction)
			self.rect = self.image.get_rect(center=self.rect.center)
		self.olddirection = self.direction									
class UDPHandler(socketserver.BaseRequestHandler):
	"""This handles the server for a multi-user chat client,
		it allows clients to connect to the server, it handles mainting the server"""


	def handle(self):
        

#		if not self.client_address in clients:
		
#			clients[self.client_address[1]] = False
		
		data = self.request[0].strip().decode('utf8')
		socket = self.request[1]
		
		self.proccess_data(data)
		
#		print("{} wrote:".format(self.client_address[0]))
#		print(data)

	def proccess_data(self, data):
		
		stripped_data = data.split('*')
#		stringa = "{}*{}*{}*{}*{}".format(type, x, y, speed, direction).encode('utf8')		
#		print(stripped_data[5])

		stripped_data[0] = str(stripped_data[0])
		stripped_data[5] = int(stripped_data[5])
		stripped_data[4] = float(stripped_data[4])
		stripped_data[3] = float(stripped_data[3])
		stripped_data[1] = int(stripped_data[1])
		stripped_data[2] = int(stripped_data[2])

		if stripped_data[5] == 3:
			a = Bullet(stripped_data[4], stripped_data[1], stripped_data[2])
			bullets.add(a)
		elif stripped_data[5] == 4:
			global arrows
			arrow_dict[stripped_data[0]] = Arrow(stripped_data[4], stripped_data[1], stripped_data[2])
			arrows.add(arrow_dict[stripped_data[0]])
			print("Added AEEEEOW")
		elif stripped_data[5] == 2:
			arrow_dict[stripped_data[0]].update_pos(stripped_data[1], stripped_data[2], stripped_data[3], stripped_data[4])
#			if clients[self.client_address] == False:
#				pass		
#			else:	
				#a.update_pos(stripped_data[3], stripped_data[4])


class ThreadedUDP(socketserver.ThreadingMixIn, socketserver.UDPServer):
	pass	
	

class start(threading.Thread):
#def start():		

	def __init__(self, address, port):
	
		super().__init__()
		self.daemon = False
		self.start()
		self.address, self.port = address, port
		

	def run(self):
		
		print("ASDASD2")
		pygame.init()	
		size = (700, 540)
		global screen
		screen = pygame.display.set_mode(size)
		pygame.display.set_caption('Shooting test')

		background = pygame.Surface(size).convert()
		background.fill((160, 160, 160))
		screen.blit(background, (0, 0))
	
		global bullets, arrows
		arrows = pygame.sprite.Group()
		bullets = pygame.sprite.Group()

		clock = pygame.time.Clock()
		running = True
		
		server_start(self.address, self.port)
		
		
		while running:		

			clock.tick(30)	

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			arrows.clear(screen, background)
			arrows.update()
			arrows.draw(screen)
			bullets.clear(screen, background)
			bullets.update()
			bullets.draw(screen)
			pygame.display.flip()
	


def server_start(host, port):
	"""This creates the server and then also functions as a prompt for the server operator to use
		the chat application"""

	try:
		udp_server = ThreadedUDP((host, port), UDPHandler)
		udp_server_thread = threading.Thread(target=udp_server.serve_forever)
		udp_server_thread.daemon = True
		udp_server_thread.start()
	except socket.error as error:
		sys.exit("There has been an error trying to create the server, please try again. - ERROR: {}".format(error))
	
	
	print('Running; type !quit to stop...')

#start()		
#start().daemon = True
#start().start()
