
import pygame, random, math
# image from http://www.frambozenbier.org/index.php/raspi-community-news/20167-antiloquax-on-getting-stuck-in-to-python

class Arrow(pygame.sprite.Sprite):
	
	def __init__(self):
	
		super().__init__()
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
		self.rect.centerx = random.randint(10, width-10)
		self.rect.centery = random.randint(10, hieght-10)
		self.vx = self.vy = 5
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
	pygame.display.flip()
