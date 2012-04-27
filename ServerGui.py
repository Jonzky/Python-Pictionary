
import pygame, random, math, socket, socketserver, threading, sys, builtins, os
from time import clock as clocky
# image from http://www.frambozenbier.org/index.php/raspi-community-news/20167-antiloquax-on-getting-stuck-in-to-python


clients = []
builtins.arrow_dict = {}
bullets_dict = {}
explosion_dict = {}

#########################################


class Explosion(pygame.sprite.Sprite):

	def __init__(self, master, x, y):

		super().__init__()
		
		
		
		self.randint = random.randint(1, 100)
		explosion_dict[self.randint] = self
		
		self.num_images = 89
		self.cur_image = 0
		self.master = master

		self.explosion_images = []

		for i in range(0, 9):
			for j in range(0, 10):

				self.explosion_images.append(pygame.image.load(os.path.join('Sprites', 'boom-1-00{}{}.png'.format(i,j))).convert())

		self.image = self.explosion_images[0]
		self.rect = self.image.get_rect()

		self.rect.centerx = x
		self.rect.centery = y
		self.update_client()

				
		
	def update(self):

		self.cur_image += 1
		if self.cur_image >= self.num_images:
			explosion.remove(self)
			try:
				del explosion_dict[self.randint]
			except:
				pass
			if self.master != '':
				self.master.kill()
			self.kill()
		else:
			
			self.image = self.explosion_images[self.cur_image]
			background = self.image.get_at((0, 0))		
			self.image.set_colorkey(background)	

	def update_client(self):
	
		packet = "CLIENT*1*{}*{}*1*1*7*False".format(self.rect.centerx, self.rect.centery).encode('utf8')

		for address in clients:

			outgoing_udp.sendto(packet, address)


#########################################

class Bullet(pygame.sprite.Sprite):

	def __init__(self, master, direction, x, y, user, key):

		super().__init__()

		self.image = pygame.image.load(os.path.join('Sprites', 'shot.png')).convert()
		self.lifetime = 10
		self.direction = direction
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.image = pygame.transform.rotate(self.image, self.direction)
		self.rect = self.image.get_rect(center=self.rect.center)					
		self.master = master
		self.user = user
		self.key = key
		

	def update(self):

		self.move()
		self.timer()
				
	def timer(self):

		if self.lifetime < 0:
			bullets.remove(self)
			del bullets_dict[self.key]
			self.explosion = Explosion(self, self.rect.centerx, self.rect.centery)			
			explosion.add(self.explosion)
			
		self.lifetime -= 0.3
		
	def remove(self):
		
		bullets.remove(self)
		del bullets_dict[self.key]
		self.kill()	

	def move(self):
	
		radian_angle = math.radians(self.direction)
		self.rect.centerx += (10*(math.cos(radian_angle)))
		self.rect.centery -= (10*(math.sin(radian_angle)))
	
class Arrow(pygame.sprite.Sprite):
	
	def __init__(self, master, direction, x, y, user):
	
		super().__init__()
		self.clock = clocky()
		self.direction = direction
		self.gospeed = 0
		self.image = pygame.image.load(os.path.join('Sprites', 'test.png')).convert()
		background = self.image.get_at((0, 0))
		self.image.set_colorkey(background)
		self.recenthit = True
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.original = self.image
		self.olddirection = self.direction
		self.master = master
		self.user = user
		self.lasthit = clocky()

	def update(self):	
		
		self.move()
		self.update_client()
		
		if clocky() - self.lasthit > 2:
			self.recenthit = False

	def update_pos(self, centerx, centery, gospeed, direction):
		
		self.rect.centerx, self.rect.centery, self.gospeed, self.direction = centerx, centery, gospeed, direction		
			
	def transform(self):
		pass

	def slowdown(self):
			
		self.gospeed -= 0.02
		self.move()
		
	def hit(self):
		
		self.explosion = Explosion('', self.rect.centerx, self.rect.centery)			
		explosion.add(self.explosion)
		self.recenthit = True
		self.gospeed = 0
		self.rect.centerx = random.randint(0, width)
		self.rect.centery = random.randint(0, height)
		self.update_client()
		
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


		if self.rect.centerx > width:
			self.rect.centerx = 0
		if self.rect.centerx < 0:
			self.rect.centerx = width
		if self.rect.centery > height:
			self.rect.centery = 0
		if self.rect.centery < 0:
			self.rect.centery = height

	        


	def update_client(self):
	
		packet = "CLIENT*{}*{}*{}*{}*{}*2*False".format(self.user, self.rect.centerx, self.rect.centery, self.gospeed, self.direction).encode('utf8')
	
		for address in clients:
			
			outgoing_udp.sendto(packet, address)
			


class UDPHandler(socketserver.BaseRequestHandler):
	"""This handles the server for a multi-user chat client,
		it allows clients to connect to the server, it handles mainting the server"""


	def handle(self):
        
		clients_first = []

		if not self.client_address[0] in clients_first:
			clients_first.append(self.client_address[0])
				
			if not self.client_address in clients:
				clients.append(self.client_address)		
			
		data = self.request[0].strip().decode('utf8')
		
		if data.startswith("SERVER"):
			self.proccess_data(data)
		else:
			print("No --  ", data)
	def proccess_data(self, data):
		
		stripped_data = data.split('*')
		
		stripped_data[1] = int(stripped_data[1])
		stripped_data[6] = int(stripped_data[6])
		stripped_data[5] = float(stripped_data[5])
		stripped_data[4] = float(stripped_data[4])
		stripped_data[2] = int(stripped_data[2])
		stripped_data[3] = int(stripped_data[3])

		if stripped_data[6] == 3:
		
			global bullets_dict
			_ran = random.randint(0,10000)
			a = Bullet(self, stripped_data[5], stripped_data[2], stripped_data[3], stripped_data[1], _ran)
			bullets_dict[_ran] = a
	
			bullets.add(a)
			
			packet = "CLIENT*{}*{}*{}*0*{}*3*False".format(stripped_data[1], stripped_data[2], stripped_data[3], stripped_data[5]).encode('utf8')
	
			for address in clients:
			
				outgoing_udp.sendto(packet, address)
			
		elif stripped_data[6] == 4:
			global arrows

			if not stripped_data[1] in builtins.arrow_dict:
				builtins.arrow_dict[stripped_data[1]] = Arrow(self, stripped_data[5], stripped_data[2], stripped_data[3], stripped_data[1])
				arrows.add(builtins.arrow_dict[stripped_data[1]])

		elif stripped_data[6] == 2:

			if stripped_data[1] in builtins.arrow_dict:
		
				builtins.arrow_dict[stripped_data[1]].update_pos(stripped_data[2], stripped_data[3], stripped_data[4], stripped_data[5])
			
			else:

				builtins.arrow_dict[stripped_data[1]] = Arrow(self, stripped_data[5], stripped_data[2], stripped_data[3], stripped_data[1])
				builtins.arrows.add(builtins.arrow_dict[stripped_data[1]])
			

class ThreadedUDP(socketserver.ThreadingMixIn, socketserver.UDPServer):
	pass	
	

class start(threading.Thread):


	def __init__(self, address, port):
	
		super().__init__()
		self.daemon = False
		self.start()
		self.address, self.port = address, port
		

	def run(self):
		

		pygame.init()
		global width, height
		width, height = 800, 800	
		size = (width, height)
		global screen
		screen = pygame.display.set_mode(size)
		pygame.display.set_caption('Shooting Server!')

		background = pygame.image.load(os.path.join('Sprites', 'nebula-reflection.jpg'))
		background = background.convert()

#		background = pygame.Surface(size).convert()
#		background.fill((160, 160, 160))
		screen.blit(background, (0, 0))
	
		global bullets, explosion
		builtins.arrows = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		explosion = pygame.sprite.Group()

		clock = pygame.time.Clock()
		running = True
		
		server_start(self.address, self.port)
		
		
		while running:		

			clock.tick(30)	


			try:
			
				for item in builtins.arrow_dict:
			
					_arrow = builtins.arrow_dict[item]
				
					for bull in bullets_dict:
					
						_bullet = bullets_dict[bull]
				
					
						if pygame.sprite.collide_rect(_arrow, _bullet):
				
					
							if _arrow.recenthit == True:
								pass
							elif _bullet.user == item:
								pass				
							else:	
								_arrow.hit()
								_bullet.remove()	
	
					for explo in explosion_dict:
				
						_explosion = explosion_dict[explo]
						
						
						if pygame.sprite.collide_rect(_arrow, _explosion):
						
							if _arrow.recenthit == True:
								pass
							else:	
								_arrow.hit()
						
					for obj in builtins.arrow_dict:
						
						_arrow2 = builtins.arrow_dict[obj]

					
						if _arrow2 == _arrow:						
						
							continue
						
						elif pygame.sprite.collide_rect(_arrow, _arrow2):
					
							_arrow.hit()
							_arrow2.hit()	
			except:
				
				print("Error in collision detection. Skipping it.")

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			builtins.arrows.clear(screen, background)
			builtins.arrows.update()
			builtins.arrows.draw(screen)
			
			bullets.clear(screen, background)
			bullets.update()
			bullets.draw(screen)
			
			explosion.clear(screen, background)
			explosion.update()
			explosion.draw(screen)

			pygame.display.flip()


def server_start(host, port):
	"""This creates the server and then also functions as a prompt for the server operator to use
		the chat application"""

	try:
		udp_server = ThreadedUDP((host, port), UDPHandler)
		udp_server_thread = threading.Thread(target=udp_server.serve_forever)
		udp_server_thread.daemon = True
		udp_server_thread.start()
		global outgoing_udp
		outgoing_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	except socket.error as error:
		sys.exit("There has been an error trying to create the server, please try again. - ERROR: {}".format(error))
	
	
	print('Running; type !quit to stop...')

#start()		
#start().daemon = True
#start().start()
