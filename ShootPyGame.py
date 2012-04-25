
import pygame, random, math, threading, socket, time, sys
from time import clock as clocky
# image from http://www.frambozenbier.org/index.php/raspi-community-news/20167-antiloquax-on-getting-stuck-in-to-python

arrow_dict = {}
bullet_dict = {}

class Bullet(pygame.sprite.Sprite):

	def __init__(self, master):

		super().__init__()
		width, hieght = screen.get_size()
		self.image = pygame.image.load('shot.png').convert()
		self.orginal_image = self.image
		self.master = master
		self.lifetime = 10
		self.direction = self.master.direction
		self.rect = self.image.get_rect()
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
		self.lifetime -= 0.3

	def move(self):
	
		radian_angle = math.radians(self.direction)
		self.rect.centerx += (10*(math.cos(radian_angle)))
		self.rect.centery -= (10*(math.sin(radian_angle)))			


#################################

class Arrow(pygame.sprite.Sprite):
	
	def __init__(self):
	
		super().__init__()
		self.clock = clocky()

		width, hieght = screen.get_size()
		self.direction = 0
		self.gospeed = 0

		self.image = pygame.image.load('test.png').convert()
		background = self.image.get_at((0, 0))
		self.image.set_colorkey(background)		
		self.original = self.image
	
		self.rect = self.image.get_rect()
		self.rect.centerx = width-10
		self.rect.centery = hieght-10

		self.udp_client = client_udp
		self.server_update(True)

	def update(self):

		keys = pygame.key.get_pressed()
		if not keys[pygame.K_UP]:	
			self.image = pygame.transform.rotate(self.original, self.direction)
			self.rect = self.image.get_rect(center=self.rect.center)						
			if self.gospeed > 0:
				self.slowdown()
				
		if keys[pygame.K_LEFT]:
			self.direction += 10
			self.image = pygame.transform.rotate(self.original, self.direction)
			self.rect = self.image.get_rect(center=self.rect.center)			
		if keys[pygame.K_RIGHT]:
			self.direction -= 10
			self.image = pygame.transform.rotate(self.original, self.direction)
			self.rect = self.image.get_rect(center=self.rect.center)			
		if keys[pygame.K_UP]:
			self.gospeed += 0.05
			self.image = pygame.transform.rotate(self.original, self.direction)
			self.rect = self.image.get_rect(center=self.rect.center)						
			self.move()
		if keys[pygame.K_SPACE]:
			if clocky() - self.clock > 0.01:
				self.clock = clocky()
				time = str(clocky())
				time = Bullet(self)
				bullets.add(time)
				
		self.server_update()		
	
	def server_update(self, new=False):
		
		if new == True:
			self.udp_client.update_position(randomint, self.rect.centerx, self.rect.centery, self.gospeed, self.direction, 4)
		else:
			self.udp_client.update_position(randomint, self.rect.centerx, self.rect.centery, self.gospeed, self.direction, 2)	

	def slowdown(self):
			
		self.gospeed -= 0.02
		self.move()
		
	def move(self):

		speeed = math.exp(self.gospeed)
		radian_angle = math.radians(self.direction)
		self.rect.centerx += (speeed*(math.cos(radian_angle)))
		self.rect.centery -= (speeed*(math.sin(radian_angle)))			
	

####################################

class OtherBullet(pygame.sprite.Sprite):

	def __init__(self, direction, x, y):

		super().__init__()

		self.image = pygame.image.load('shot.png').convert()
		self.orginal_image = self.image
		self.lifetime = 10
		
		self.direction = direction

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
			return False
		self.lifetime -= 0.3

	def move(self):
	
		radian_angle = math.radians(self.direction)
		self.rect.centerx += (10*(math.cos(radian_angle)))
		self.rect.centery -= (10*(math.sin(radian_angle)))
	
	
###########################################



class OtherArrow(pygame.sprite.Sprite):
	
	def __init__(self, direction, x, y):
	
		super().__init__()

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
		self.arrows = arrows
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
		
#		print(stripped_data[1], self.randomint)

		
		stripped_data[6] = int(stripped_data[6])
		stripped_data[5] = float(stripped_data[5])
		stripped_data[4] = float(stripped_data[4])
		stripped_data[2] = int(stripped_data[2])
		stripped_data[3] = int(stripped_data[3])


		if stripped_data[1] == self.randomint:
#			print('aww')
			pass
		elif stripped_data[6] == 3:

			global other_bullets

			print("!!2222333!")
			
			print(" Direction -{}- X -{}- Y -{}-".format(stripped_data[5], stripped_data[2], stripped_data[3]))
			randomnumber = random.randint(50,1000)
				
			bullet_dict[randomnumber] = OtherBullet(stripped_data[5], stripped_data[2], stripped_data[3])

			other_bullets.add(bullet_dict[randomnumber])


		elif stripped_data[6] == 2:
			
			if stripped_data[1] in arrow_dict:
				
				arrow_dict[stripped_data[1]].update_pos(stripped_data[2], stripped_data[3], stripped_data[4], stripped_data[5])

			else:
			
				arrow_dict[stripped_data[1]] = OtherArrow(stripped_data[5], stripped_data[2], stripped_data[3])
				self.arrows.add(arrow_dict[stripped_data[1]])				
					
			
	def update_position(self, username, x, y, speed, direction, type):
		
		stringa = "SERVER*{}*{}*{}*{}*{}*{}".format(username, x, y, speed, direction, type).encode('utf8')
		
		self.sock.sendto(stringa, (self.host, self.port))
		





#####################################

class start(threading.Thread):	

	def __init__(self, address1, port1, randomint1):


		global address, port, randomint		
		address, port, randomint = address1, port1, randomint1		
		super().__init__()
		self.daemon = False
		self.start()
		self.running = True
	
	def run(self):
	
		pygame.init()
		global screen
		size = (700, 540)
		screen = pygame.display.set_mode(size)
		pygame.display.set_caption('Shooting test')
	
		background = pygame.Surface(size).convert()
		background.fill((160, 160, 160))
		screen.blit(background, (0, 0))
		print("!")
		global bullets, arrows, other_bullets
		arrows = pygame.sprite.Group()
		other_bullets = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
				
		global client_udp
		client_udp = ClientUDP()
	
		arrows.add(Arrow())

		other_bullets = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
	
	
		clock = pygame.time.Clock()
		
	
		while self.running:
			clock.tick(30)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					
					print('ping')
#					self.destroy()
					sys.exit("UEUUE")
					self.running = False
	
			arrows.clear(screen, background)
			arrows.update()
			arrows.draw(screen)
			
			bullets.clear(screen, background)
			bullets.update()
			bullets.draw(screen)
			
			other_bullets.clear(screen, background)
			other_bullets.update()
			other_bullets.draw(screen)
			
			pygame.display.flip()	
