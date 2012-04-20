
import pygame, random, math
from time import clock as clocky
# image from http://www.frambozenbier.org/index.php/raspi-community-news/20167-antiloquax-on-getting-stuck-in-to-python

class Bullet(pygame.sprite.Sprite):

	def __init__(self, master):

		super().__init__()
		width, hieght = screen.get_size()
		self.image = pygame.image.load('shot.png').convert()
		self.master = master
		self.lifetime = 10
		self.direction = self.master.direction
		self.rect = self.image.get_rect()
		self.rect.centerx = self.master.rect.centerx+5
		self.rect.centery = self.master.rect.centery+5
	
		self.image = pygame.transform.rotate(self.image, self.direction)
		self.rect = self.image.get_rect(center=self.rect.center)					

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
		self.moving_image = pygame.image.load('test.png').convert()
		self.not_moving_image = pygame.image.load('test.png').convert()
		self.image = self.not_moving_image

		background = self.image.get_at((0, 0))
		self.image.set_colorkey(background)
		self.moving_image.set_colorkey(background)
		self.not_moving_image.set_colorkey(background)		
		
		self.rect = self.image.get_rect()
		self.rect.centerx = width-10
		self.rect.centery = hieght-10
		self.original = self.image

	def update(self):

		keys = pygame.key.get_pressed()
		if not keys[pygame.K_UP]:	
			self.image = self.not_moving_image
			self.image = pygame.transform.rotate(self.not_moving_image, self.direction)
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
			self.image = pygame.transform.rotate(self.moving_image, self.direction)
			self.rect = self.image.get_rect(center=self.rect.center)						
			self.move()
		if keys[pygame.K_SPACE]:
			if clocky() - self.clock > 0.01:
				print("Shoot")
				self.clock = clocky()
				time = str(clocky())
				time = Bullet(self)
				bullets.add(time)
			
			
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
	
pygame.init()

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
