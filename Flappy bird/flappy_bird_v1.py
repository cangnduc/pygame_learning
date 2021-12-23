import pygame
import math
import random
pygame.init()
class PIPE:
	def __init__(self):
		self.pipe_x = 0
		self.pipe_height = [400,450,500]
		self.pip_image = pygame.transform.scale2x(pygame.image.load("Images/pipe-green.png").convert_alpha())
		self.add_pipe()
		self.pipe_list = [self.pipe_rect_bottom ,self.pipe_rect_top ]
	def pipe_animation(self):
		for pipe in self.pipe_list:
			pipe.centerx -= 5
	def add_pipe(self):
		random_height = random.choice(self.pipe_height)
		self.pipe_rect_bottom = self.pip_image.get_rect(midtop = (600,random_height))
		self.pipe_rect_top = self.pip_image.get_rect(midbottom= (600, random_height - 200))
		return self.pipe_rect_bottom, self.pipe_rect_top
	def draw_pipe(self):
		for pipe in self.pipe_list:
			if pipe.bottom > 800:
				screen.blit(self.pip_image,pipe)
			else:
				fliped_pipe = pygame.transform.flip(self.pip_image,False,True)
				screen.blit(fliped_pipe,pipe)
	def pip_update(self):
		self.pipe_animation()
		self.draw_pipe()

class FLOOR:
	def __init__(self):
		self.bg_image = pygame.transform.scale(pygame.image.load("Images/base.png"),(567,200))
		self.floor_x = 0
		
	def draw(self):
		self.bg_rect = self.bg_image.get_rect(topleft = (self.floor_x,650))
		self.bg_rect2 = self.bg_image.get_rect(topleft = (self.floor_x + 567,650))
		screen.blit(self.bg_image,self.bg_rect)
		screen.blit(self.bg_image,self.bg_rect2)
	def floor_animation(self):
		self.floor_x -= 1
		if self.floor_x < -567:
			self.floor_x = 0
	def update(self):
		self.draw()
		self.floor_animation()
class BIRD:
	def __init__(self):
		self.bird_frame1 = pygame.transform.scale2x(pygame.image.load("Images/bluebird-midflap.png").convert_alpha())
		self.bird_frame2 = pygame.transform.scale2x(pygame.image.load("Images/bluebird-upflap.png").convert_alpha())
		self.bird_frame3 = pygame.transform.scale2x(pygame.image.load("Images/bluebird-downflap.png").convert_alpha())
		self.bird_holder = [self.bird_frame1,self.bird_frame2, self.bird_frame3]
		self.index = 0
		self.bird_image = self.bird_holder[self.index]
		self.bird_rect = self.bird_image.get_rect(center= (100,350))
		self.bird_movement = 0
		self.bird_gravity = 0
	def bird_fly(self):
		self.bird_gravity += 0.8
		#self.bird_movement += self.bird_gravity
		self.bird_rect.centery += self.bird_gravity
	def bird_rotation(self):
		self.rotated_image = pygame.transform.rotate(self.bird_image,- self.bird_gravity*2)
		self.bird_rect = self.rotated_image.get_rect(center =(self.bird_rect.center)) 
	def draw(self):
		screen.blit(self.rotated_image,self.bird_rect)
	def bird_key_pressed(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE] and game_active == True:
			self.bird_gravity = 0
			self.bird_gravity -= 8
	
	def bird_animation(self):
		self.index += 0.1
		if self.index >len(self.bird_holder):
			self.index = 0
		self.bird_image = self.bird_holder[int(self.index)]

	def update(self):
		self.bird_animation()
		self.bird_rotation()
		self.draw()
		self.bird_key_pressed()
		self.bird_fly()
		
class Collide_manager:
	def check_collide_(self):
		if bird.bird_rect.bottom >650:
			return False
		for pipe in pipe_list:
			if bird.bird_rect.colliderect(pipe):
				return False
				print("collide")
		return True  
			
def remove_pipe(pipe_list):
	pipe_list = [a for a in pipe_list if a.centerx >-100]
	return pipe_list

game_active = True
screen = pygame.display.set_mode((567,800))
clock = pygame.time.Clock()
bg_image = pygame.transform.scale(pygame.image.load("Images/background-day.png"),(567,800))
pipe_timer = pygame.USEREVENT
pygame.time.set_timer(pipe_timer,1500)
floor = FLOOR()
bird = BIRD()
pipe = PIPE()

check_collide = Collide_manager()

while True:	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pipe_timer:
			pipe_top, pipe_bottom = pipe.add_pipe()
			pipe.pipe_list.append(pipe_top)
			pipe.pipe_list.append(pipe_bottom)
			print(pipe_list)
	screen.blit(bg_image,(0,0))
	if game_active:
		pipe.pip_update()
		pipe_list = remove_pipe(pipe.pipe_list)

		floor.update()
		bird.update()
		
		game_active = check_collide.check_collide_()
	else:
		pipe.pipe_list.clear()
		keys = pygame.key.get_pressed()
		bird.bird_rect.center = (100,350)
		bird.bird_gravity = 0
		if keys[pygame.K_SPACE] and game_active == False:
			game_active = True
			
	pygame.display.update()
	clock.tick(60)