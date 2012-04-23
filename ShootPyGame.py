
import pygame, random, math, UDPClient, threading
from time import clock as clocky
# image from http://www.frambozenbier.org/index.php/raspi-community-news/20167-antiloquax-on-getting-stuck-in-to-python

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

		self.udp_client = UDPClient.ClientUDP(address, port)
		self.udp_client.master = self
		
		self.image = pygame.transform.rotate(self.orginal_image, self.direction)
		self.rect = self.image.get_rect(center=self.rect.center)					

		self.server_update(True)

	def update(self):

		self.move()
		self.timer()
		keys = pygame.key.get_pressed()
#		if not keys[pygame.K_SPACE]:	
#			self.image = self.not_moving_image
#			self.image = pygame.transform.rotate(self.not_moving_image, self.direction)
#			self.rect = self.image.get_rect(center=self.rect.center)						
#			if self.gospeed > 0:
#				self.slowdown()
		#self.server_update()


	def server_update(self, new=False):
		
		if new == True:
			self.udp_client.update_position(randomint, self.rect.centerx, self.rect.centery, 0, self.direction, 3)
		else:
			pass
#			self.udp_client.update_position(1, 0, self.direction)	
				
	def timer(self):

		if self.lifetime < 0:
			bullets.remove(self)
		self.lifetime -= 0.3

			

	def move(self):
	

		radian_angle = math.radians(self.direction)
		self.rect.centerx += (10*(math.cos(radian_angle)))
		self.rect.centery -= (10*(math.sin(radian_angle)))			

class Arrow(pygame.sprite.Sprite):
	
	def __init__(self):
	
		super().__init__()
		self.clock = clocky()
		print(self.clock)
		width, hieght = screen.get_size()
		self.direction = 0
		self.gospeed = 0
		self.image = pygame.image.load('test.png').convert()
		background = self.image.get_at((0, 0))
		self.image.set_colorkey(background)		
		self.rect = self.image.get_rect()
		self.rect.centerx = width-10
		self.rect.centery = hieght-10
		self.original = self.image

		self.udp_client = UDPClient.ClientUDP(address, port)
		self.udp_client.master = self
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
				print("Shoot")
				self.clock = clocky()
				time = str(clocky())
				time = Bullet(self)
				bullets.add(time)
				
		self.server_update()		
	
	def server_update(self, new=False):
		
		if new == True:
			self.udp_client.update_position(randomint, self.rect.centerx, self.rect.centery, 0, self.direction, 4)
		else:
			self.udp_client.update_position(randomint, self.rect.centerx, self.rect.centery, self.gospeed, self.direction, 2)	
			

	def transform(self):
		pass

	def slowdown(self):
			
		self.gospeed -= 0.02
		self.move()
		
	def move(self):

		speeed = math.exp(self.gospeed)
		radian_angle = math.radians(self.direction)
		self.rect.centerx += (speeed*(math.cos(radian_angle)))
		self.rect.centery -= (speeed*(math.sin(radian_angle)))			
	

class start(threading.Thread):	

	def __init__(self, address1, port1, randomint1):
		
		super().__init__()
		self.daemon = False
		self.start()
		global address, port, randomint		
		address, port, randomint = address1, port1, randomint1
	
	def run(self):
	
		pygame.init()
		global screen, bullets
		size = (700, 540)
		screen = pygame.display.set_mode(size)
		pygame.display.set_caption('Shooting test')
	
		background = pygame.Surface(size).convert()
		background.fill((160, 160, 160))
		screen.blit(background, (0, 0))
	
		
		arrows = pygame.sprite.Group(Arrow())
		bullets = pygame.sprite.Group()
	
	
		clock = pygame.time.Clock()
		running = True
	
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
