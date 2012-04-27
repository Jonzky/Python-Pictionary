
import pygame, random, math, threading, socket, time, sys, builtins, os
from PictClient import ClientPinger
from PictClient import TCPConnection
from time import clock as clocky
# image from http://www.frambozenbier.org/index.php/raspi-community-news/20167-antiloquax-on-getting-stuck-in-to-python
#Explosion sprites from David Howe http://homepage.ntlworld.com/david.howe50/page16a.html


builtins.arrow_dict = {}
bullet_dict = {}

class Bullet(pygame.sprite.Sprite):

	def __init__(self, master):

		super().__init__()
		width, hieght = screen.get_size()
		self.image = pygame.image.load(os.path.join('Sprites', 'shot.png')).convert()
		self.orginal_image = self.image
		self.master = master
		self.lifetime = 10
		self.direction = self.master.direction
		self.rect = self.image.get_rect()
		
		self.rect.centerx += (20*(math.cos(self.master.radian_angle)))
		self.rect.centery -= (20*(math.sin(self.master.radian_angle)))			

		self.rect.centerx = self.master.rect.centerx+5
		self.rect.centery = self.master.rect.centery+5


		self.udp_client = client_udp		
		self.image = pygame.transform.rotate(self.orginal_image, self.direction)
		self.rect = self.image.get_rect(center=self.rect.center)					

		self.server_update(True)

	def update(self):

		self.move()
		self.timer()

	def server_update(self, new=False):
		
		if new == True:
			self.udp_client.update_position(randomint, self.rect.centerx, self.rect.centery, 0, self.direction, 3)
		else:
			pass

	def timer(self):

		if self.lifetime < 0:
		
			bullets.remove(self)
			self.kill()
		self.lifetime -= 0.3

	def move(self):
	
		self.radian_angle = math.radians(self.direction)
		self.rect.centerx += (10*(math.cos(self.radian_angle)))
		self.rect.centery -= (10*(math.sin(self.radian_angle)))			


#################################

class Arrow(pygame.sprite.Sprite):
	
	def __init__(self):
	
		super().__init__()
		self.clock = clocky()

		width, hieght = screen.get_size()
		self.direction = 0
		self.gospeed = 0
		self.radian_angle = 0

		self.image = pygame.image.load(os.path.join('Sprites', 'test.png')).convert()
		background = self.image.get_at((0, 0))
		self.image.set_colorkey(background)		
		self.original = self.image
	
		self.rect = self.image.get_rect()
		self.rect.centerx = width-10
		self.rect.centery = hieght-10
		self.not_space = True

		self.udp_client = client_udp
		self.server_update(True)

	def update(self):

		keys = pygame.key.get_pressed()
		if not keys[pygame.K_UP]:	
			self.image = pygame.transform.rotate(self.original, self.direction)
			self.rect = self.image.get_rect(center=self.rect.center)						
			if self.gospeed > 0:
				self.slowdown()
		if not keys[pygame.K_SPACE]:
			self.not_space = True 		
		if keys[pygame.K_LEFT]:
			self.direction += 10
			self.image = pygame.transform.rotate(self.original, self.direction)
			self.rect = self.image.get_rect(center=self.rect.center)			
		if keys[pygame.K_RIGHT]:
			self.direction -= 10
			self.image = pygame.transform.rotate(self.original, self.direction)
			self.rect = self.image.get_rect(center=self.rect.center)			
		if keys[pygame.K_UP]:
			if self.gospeed >= 2:
				pass
			else:	
				self.gospeed += 0.05
			self.image = pygame.transform.rotate(self.original, self.direction)
			self.rect = self.image.get_rect(center=self.rect.center)						
			self.move()
		if keys[pygame.K_SPACE]:
			if self.not_space:
				if clocky() - self.clock > 0.02:
					self.clock = clocky()
					time = str(clocky())
					time = Bullet(self)
					bullets.add(time)
					self.not_space = False
				
		self.server_update()		
	
	def server_update(self, new=False):
		
		if new == True:
			self.udp_client.update_position(randomint, self.rect.centerx, self.rect.centery, self.gospeed, self.direction, 4)
		else:
			self.udp_client.update_position(randomint, self.rect.centerx, self.rect.centery, self.gospeed, self.direction, 2)	

	def slowdown(self):
			
		self.gospeed -= 0.02
		self.move()

	def update_pos(self, centerx, centery, gospeed, direction):
		
		self.rect.centerx, self.rect.centery, self.gospeed, self.direction = centerx, centery, gospeed, direction
		
	def move(self):

		speeed = math.exp(self.gospeed)
		self.radian_angle = math.radians(self.direction)
		self.rect.centerx += (speeed*(math.cos(self.radian_angle)))
		self.rect.centery -= (speeed*(math.sin(self.radian_angle)))			

####################################	

class Explosion(pygame.sprite.Sprite):

	def __init__(self, master, x, y):

		super().__init__()
		
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

				
		
	def update(self):

		self.cur_image += 1
		if self.cur_image >= self.num_images:
			explosion.remove(self)
			if self.master != '':			
				self.master.kill()
			self.kill()
		else:
			
			self.image = self.explosion_images[self.cur_image]
			background = self.image.get_at((0, 0))		
			self.image.set_colorkey(background)		
		

####################################

class OtherBullet(pygame.sprite.Sprite):

	def __init__(self, direction, x, y, key):

		super().__init__()

		self.image = pygame.image.load(os.path.join('Sprites', 'shot.png')).convert()
		self.orginal_image = self.image
		self.lifetime = 10
		
		self.direction = direction
		self.key = key
		self.rect = self.image.get_rect()

		self.rect.centerx = x
		self.rect.centery = y


		self.image = pygame.transform.rotate(self.orginal_image, self.direction)
		self.rect = self.image.get_rect(center=self.rect.center)					
				
		
	def update(self):

		self.move()
		self.timer()
		
	def timer(self):

		if self.lifetime < 0:
			bullets.remove(self)
			self.kill()
			return False
		self.lifetime -= 0.3

	def move(self):
	
		radian_angle = math.radians(self.direction)
		self.rect.centerx += (10*(math.cos(radian_angle)))
		self.rect.centery -= (10*(math.sin(radian_angle)))
		
	def remove(self):
		
		try:
			other_bullets.remove(bullet_dict[self.key])
			del bullet_dict[self.key]
		except:
			pass
		self.kill()			
	
	
###########################################



class OtherArrow(pygame.sprite.Sprite):
	
	def __init__(self, direction, x, y):
	
		super().__init__()

		self.direction = direction
		self.gospeed = 0

		self.image = pygame.image.load(os.path.join('Sprites', 'test.png')).convert()
		background = self.image.get_at((0, 0))
		self.image.set_colorkey(background)

		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.original = self.image
		self.olddirection = self.direction
		self.lastupdate = 0

	def update(self):	
		
		self.move()
		self.check()

	def update_pos(self, centerx, centery, gospeed, direction):
		
		self.rect.centerx, self.rect.centery, self.gospeed, self.direction = centerx, centery, gospeed, direction
		self.lastupdate = time.clock()
			
	def check(self):
		
		cur_time = time.clock()

		if (cur_time - self.lastupdate) > 8:
			
			print("User DC'ed")
			
			builtins.arrows.remove(self)
			
		
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




####################################


class ClientUDP(threading.Thread):

	def __init__(self):
		
		time.sleep(2.0)			
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		super().__init__()
		self.daemon = True
		self.host = address
		self.port = port
		self.randomint = int(randomint)
		self.arrows = builtins.arrows
		self.bullets = bullets
		self.start()

	def run(self):		
		
		while True:
				
			incoming_data = self.sock.recv(1024)

			data = incoming_data.strip().decode('utf8') 

			if len(data) == 0:
				pass
			elif data == "***ShUtdOwn***":
				print("Server shutting down...")

			else:
				
				if data.startswith("CLIENT"):
					self.process_data(data)


	def process_data(self, data):
	
		stripped_data = data.split('*')
		stripped_data[1] = int(stripped_data[1])

		stripped_data[6] = int(stripped_data[6])
		stripped_data[5] = float(stripped_data[5])
		stripped_data[4] = float(stripped_data[4])
		stripped_data[2] = int(stripped_data[2])
		stripped_data[3] = int(stripped_data[3])
		stripped_data[7] = bool(stripped_data[7])

		if stripped_data[1] == self.randomint:
			
			if stripped_data[7] == True:

				my_arrow.update_pos(stripped_data[2], stripped_data[3], stripped_data[4], stripped_data[5])
	
		elif stripped_data[6] == 3:

			global other_bullets

			print("bullet")

			randomnumber = random.randint(50,1000)
				
			bullet_dict[randomnumber] = OtherBullet(stripped_data[5], stripped_data[2], stripped_data[3], randomnumber)

			other_bullets.add(bullet_dict[randomnumber])

		elif stripped_data[6] == 7:
			
			a = Explosion('', stripped_data[2], stripped_data[3])
			explosion.add(a)

		elif stripped_data[6] == 2:
			
			if stripped_data[1] in builtins.arrow_dict:
				
				builtins.arrow_dict[stripped_data[1]].update_pos(stripped_data[2], stripped_data[3], stripped_data[4], stripped_data[5])

			else:
			
				builtins.arrow_dict[stripped_data[1]] = OtherArrow(stripped_data[5], stripped_data[2], stripped_data[3])
				self.arrows.add(arrow_dict[stripped_data[1]])				
					
	def update_position(self, username, x, y, speed, direction, type):
		
		stringa = "SERVER*{}*{}*{}*{}*{}*{}".format(username, x, y, speed, direction, type).encode('utf8')
		
		self.sock.sendto(stringa, (self.host, self.port))
		

######################################
def mega_test():
	explosion_images = []
	for i in range(0, 10):
		for j in range(0, 10):

			explosion_images.append(pygame.image.load(os.path.join('Sprites', 'boom-1-00{}{}.png'.format(i,j))).convert())
	
	

	print(explosion_images)

#####################################

class start(threading.Thread):	

	def __init__(self, address1, port1, randomint1):


		global address, port, randomint		
		
		address, port, randomint = str(address1), int(port1), int(randomint1)		
		self.pinger = ClientPinger(address, port, randomint)
		self.TCP = TCPConnection(self, randomint, address, port)
		super().__init__()
		self.daemon = False
		self.start()
		self.running = True

	
	def run(self):
	
		
		pygame.init()
		global screen
		global width, height
		width, height = 800, 800
		size = (width, height)	
		screen = pygame.display.set_mode(size)
		pygame.display.set_caption('Pygame Space Shooter')


		background = pygame.image.load(os.path.join('Sprites', 'nebula-reflection.jpg'))
		background = background.convert()
	
#		background = pygame.Surface(size).convert()
#		background.fill((160, 160, 160))
		screen.blit(background, (0, 0))
		print("!")
		global bullets, arrows, other_bullets, explosion
		explosion = pygame.sprite.Group()
		builtins.arrows = pygame.sprite.Group()
		other_bullets = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
				
		global client_udp
		client_udp = ClientUDP()
		global my_arrow
		my_arrow = Arrow()
		builtins.arrows.add(my_arrow)

		other_bullets = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
	
	
		clock = pygame.time.Clock()


		while self.running:
			clock.tick(30)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:

					self.running = False

			
#			try:
			
			for item in builtins.arrow_dict:
			
				_arrow = builtins.arrow_dict[item]
				
				for bull in bullet_dict:
					
					_bullet = bullet_dict[bull]
				
					if pygame.sprite.collide_rect(_arrow, _bullet):
				
							_bullet.remove()	
	

#			except:
				
#				print("Error in collision detection. Skipping it.")
			
			builtins.arrows.clear(screen, background)
			builtins.arrows.update()
			builtins.arrows.draw(screen)
			
			bullets.clear(screen, background)
			bullets.update()
			bullets.draw(screen)
			
			other_bullets.clear(screen, background)
			other_bullets.update()
			other_bullets.draw(screen)

			explosion.clear(screen, background)
			explosion.update()
			explosion.draw(screen)
			
			pygame.display.flip()

