import pygame
pygame.init()
import math
import random
class SNAKE:
	def __init__(self,row_size):
		self.row_size = row_size
		self.pos_list = [pygame.math.Vector2(5,5),pygame.math.Vector2(4,5),pygame.math.Vector2(3,5)]
		#self.image = pygame.Surface(row_size, row_size)
		self.direction = pygame.math.Vector2(1,0)

	def draw(self):
		for pos in self.pos_list:
			pygame.draw.rect(screen,"pink",(self.row_size*pos.x,pos.y *self.row_size,row_size,row_size))
			#print(pos.x)

	def animation(self):
		self.pos_copy = self.pos_list[:-1]
		self.pos_copy.insert(0,self.pos_list[0]+ self.direction)
		self.pos_list = self.pos_copy
	
	def check_key_pressed(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]:
			if self.direction.y != 1:
				self.direction = pygame.math.Vector2(0,-1)
		elif keys[pygame.K_DOWN]:
			if self.direction.y != -1:
				self.direction = pygame.math.Vector2(0,1)
		elif keys[pygame.K_LEFT]:
			if self.direction.x != 1:
				self.direction = pygame.math.Vector2(-1,0)
		elif keys[pygame.K_RIGHT]:
			if self.direction.x != -1:
				self.direction = pygame.math.Vector2(1,0)

	def update(self):
		self.draw()
		#self.animation()
		self.check_key_pressed()
class FRUIT(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.pos_randomize()

	def pos_randomize(self):
		self.pos_x = random.randint(0,row_size - 1)
		self.pos_y = random.randint(0,row_size - 1)
		for block in snake.pos_list:
			if pygame.math.Vector2(self.pos_x,self.pos_y) == block:
				self.pos_randomize()
		self.image = pygame.Surface((row_size,row_size))
		self.rect = self.image.get_rect(topleft = (collum_size*self.pos_x,collum_size*self.pos_y))
	def update(self):
		pygame.draw.rect(screen,"pink", self.rect)
class Manager:
	def eat_fruit(self):
		if snake.pos_list[0] == [fruit.pos_x,fruit.pos_y]:
			fruit.pos_randomize()
			snake.pos_copy = snake.pos_list[:]
			snake.pos_copy.insert(0,snake.pos_list[0]+ snake.direction)
			snake.pos_list = snake.pos_copy
	def check_collide_(self):
		if not 0<= snake.pos_list[0].x <row_size:
			print("collide")
		if not 0<= snake.pos_list[0].y <row_size:
			print("collideyyyy")
		for block in snake.pos_list[1:]:
			if block == snake.pos_list[0]:
				print("collide itself")
	def update(self):
		self.eat_fruit()
		self.check_collide_()
clock = pygame.time.Clock()


row_size = 20
collum_size = 20
screen = pygame.display.set_mode((row_size*collum_size,row_size*collum_size))
snake = SNAKE(row_size)
fruit = FRUIT()
manager = Manager()
#print(fruit.pos)
time = pygame.USEREVENT
pygame.time.set_timer(time, 200)
while True:
	screen.fill("black")
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == time:
			snake.animation()
	snake.update()
	fruit.update()
	manager.update()
	#screen.fill("black")
	pygame.display.update()
	clock.tick(60)
