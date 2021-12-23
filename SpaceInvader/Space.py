import pygame
import random
class Main:
	def __init__(self):
		player_sprite = Player((screen_width/2,screen_height))
		self.player = pygame.sprite.GroupSingle(player_sprite)
		self.blocks = pygame.sprite.Group()
		self.size = 5
		self.score = 0
		self.enemies = pygame.sprite.Group()
		self.create_enemy(5,5,60,70)
		self.create_multiple_obstacle(screen_width/15,400)
		#self.enemy_shoot()
		self.speed = 1
		self.direction = self.speed
		self.enemy_laser = pygame.sprite.Group()
		self.boss = pygame.sprite.GroupSingle()
		self.boss_laser = pygame.sprite.Group()
		self.spwan_time = random.randint(300,400)
		self.random_time = random.randint(20,50)
	def spwan_boss(self):
		self.spwan_time -= 1
		if self.spwan_time == 0:
			self.boss_time_start = pygame.time.get_ticks()
			print(self.boss_time_start)
			self.boss.add(Boss(random.choice(["Left","Right"])))
			self.spwan_time = random.randint(300,400)
		
	def check_collide(self):
		if self.player.sprite.lasers:
			for laser in self.player.sprite.lasers:
				
				if pygame.sprite.spritecollide(laser,self.enemies,True):
					laser.kill()
					self.score += 1
					if len(self.enemies) == 0:
						self.create_enemy(5,5,60,70)
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()
				if pygame.sprite.spritecollide(laser,self.boss,True):
					laser.kill()
		print(self.score)
	def create_obstacle(self,x_start,y_start,offset):
		shape = [
			"   xxxx   ",
			" xxxxxxxx ",
			"xxxxxxxxxx",
			"xxxxxxxxxx",
			"xx      xx",
	]
		for row_index, row in enumerate(shape):
			for col_index, col in enumerate(row):
				if col == "x":
						x= x_start + col_index * self.size + offset
						y= y_start + row_index * self.size
						block = Block(x,y,self.size)
						self.blocks.add(block)
	def create_enemy(self,rows,cols,x_offset, y_offset):
		#enemy = Enemy(x,y,color)
		for row_index, row in enumerate(range(rows)):
			for col_index, col in enumerate(range(cols)):
				x = row_index *60 + x_offset
				y = col_index *48 + y_offset
				#print(row_index,col_index)
				if col_index == 0:
					enemy = Enemy(x,y,"red")
				elif 1<= col_index<=2:
					enemy = Enemy(x,y,"yellow")
				else:
					enemy = Enemy(x,y,"green")
				self.enemies.add(enemy)
	def enemy_movement(self):
		if self.enemies:
			for enemy in self.enemies.sprites():
				if enemy.rect.right >= screen_width:
					self.direction = -self.speed
				elif enemy.rect.left <= 0:
					self.direction = self.speed
	def boss_laser_shoot(self):
		if self.boss.sprite:
			self.random_time -=1
			if 20<self.boss.sprite.rect.x<screen_width-20 and self.random_time <=0:
				self.boss_laser.add(Laser(self.boss.sprite.rect.center,"red"))
				self.random_time = random.randint(20,50)
			#print(self.boss_laser)
	def boss_laser_movement(self):
		if self.boss_laser:
			#print(self.boss_laser)
			for laser in self.boss_laser:
				laser.rect.y += 5
	def enemy_shoot(self):
		if self.enemies:
			random_enemy = random.choice(self.enemies.sprites())
			self.enemy_laser.add(Laser(random_enemy.rect.center,"white"))
	def enemy_bullet_movement(self):
		if self.enemy_laser:
			#print(self.enemy_laser)
			for laser in self.enemy_laser:
				laser.rect.y += 5
				if laser.rect.y >= screen_height:
					laser.kill()
				
	def time_calculator(self):
		if self.boss:
			current_time = pygame.time.get_ticks()
			print(current_time - self.boss_time_start)
	def create_multiple_obstacle(self,x_start,y_start):
		obstacle_number = 4
		offsets = [num*(screen_width/obstacle_number) for num in range(obstacle_number)]
		for offset in offsets:
			self.create_obstacle(x_start,y_start,offset)

	def run(self):
		self.spwan_boss()
		self.enemy_movement()
		self.enemy_bullet_movement()
		self.enemy_laser.draw(screen)
		self.blocks.draw(screen)
		self.player.draw(screen)
		self.player.update()
		self.player.sprite.lasers.update()
		self.enemies.draw(screen)
		self.enemies.update(self.direction)
		self.boss.draw(screen)
		self.boss.update()
		self.boss_laser_shoot()
		self.boss_laser_movement()
		self.boss_laser.draw(screen)
		self.time_calculator()
		self.check_collide()
		#self.player.sprite.lasers.draw(screen)
class Enemy(pygame.sprite.Sprite):
	def __init__(self,x,y, color):
		super().__init__()
		file_path = f"graphics/{color}.png"
		self.image =pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(topleft =(x,y))
	
	def update(self, direction):
		self.rect.x += direction
class Block(pygame.sprite.Sprite):
	def __init__(self,x,y,size):
		super().__init__()
		self.size = size
		self.image = pygame.Surface((self.size,self.size))
		self.image.fill("white")
		self.rect = self.image.get_rect(topleft = (x,y))
	
class Boss(pygame.sprite.Sprite):
	def __init__(self,side):
		super().__init__()
		self.image = pygame.image.load("graphics/extra.png").convert_alpha()
		#self.speed = 4
		speed = 2
		if side == "Left":
			x = -50
			self.speed = speed
		else:
			x = screen_width + 50
			self.speed = -speed
		self.rect = self.image.get_rect(center = (x,40))
	def update(self):
		self.rect.x += self.speed
	
class Laser(pygame.sprite.Sprite):
	def __init__(self, pos,color):
		super().__init__()
		self.pos = pos
		self.image = pygame.Surface((5,20))
		self.image.fill(color)
		self.speed = 8
		self.rect = self.image.get_rect(midbottom = pos)
	def movement(self):
		self.rect.y -= self.speed
	def remove(self):
		if self.rect.y <= -30:
			self.kill()
	def update(self):
		self.movement()
		self.remove()

class Player(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.pos = pos
		self.image = pygame.image.load("graphics/player.png").convert_alpha()
		self.rect = self.image.get_rect(midbottom = self.pos)
		self.speed = 5
		self.lasers = pygame.sprite.Group()
		self.ready = True
		self.time_bullet_reload = 300
		self.time_shoot = 0

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.rect.x -=self.speed
		if keys[pygame.K_RIGHT]:
			self.rect.x +=self.speed
		if keys[pygame.K_SPACE] and self.ready:
			self.ready = False
			self.time_shoot = pygame.time.get_ticks()
			self.lasers.add(Laser(self.rect.center,"red"))
	def bullet_shoot(self):
		current_time = pygame.time.get_ticks()
		if current_time - self.time_shoot >self.time_bullet_reload:
			self.ready = True
	def constrain(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		elif self.rect.right >= screen_width:
			self.rect.right = screen_width
	def update(self):
		
		self.player_input()
		self.constrain()
		self.bullet_shoot()
		self.lasers.draw(screen)


pygame.init()
screen_width, screen_height = 400,600
screen = pygame.display.set_mode((screen_width,screen_height))
laser_time = pygame.USEREVENT + 1
pygame.time.set_timer(laser_time,500)
clock = pygame.time.Clock()
main = Main()
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == laser_time:
			main.enemy_shoot()
			main.boss_laser_shoot()
	screen.fill("black")
	main.run()
	pygame.display.update()
	clock.tick(60)