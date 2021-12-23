import pygame
pygame.init()
from os import walk
def import_folder(path):
		f = []
		for (dirpath, dirnames, filenames) in walk(path):
		    for file in filenames:
			    full_path = f"{path}/{file}"
			    image_surface = pygame.image.load(full_path).convert_alpha()
			    f.append(image_surface)
		return f
class Level:
	def __init__(self,level_map,Surface):
		self.Surface = Surface
		self.level_map  = level_map
		self.player = pygame.sprite.GroupSingle()
		self.blocks = pygame.sprite.Group()
		self.map_shift = 0
		self.draw_map()
		
		self.big_dust =pygame.sprite.GroupSingle()
		self.player_on_ground = False
		self.current_x = 0
	def draw_map(self):
		
		for row_index, row in enumerate(self.level_map):
			for col_index, col in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if col == "X":
					block = Block(x,y)
					self.blocks.add(block)
				if col == "P":
					self.player.add(Player(x,y,self.Surface,self.create_jump_particle))
	def create_jump_particle(self,pos):
		if self.player.sprite.face_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		big_dust = Particle_effect(pos,"jump")
		self.big_dust.add(big_dust)


	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False
	def create_landing_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.big_dust:
			if self.player.sprite.face_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)
			fall_dust_particle = Particle_effect(self.player.sprite.rect.midbottom-offset,"land")
			self.big_dust.add(fall_dust_particle)
	def scroll_x(self):
		player = self.player.sprite
		player_x = self.player.sprite.rect.centerx
		player_direction = self.player.sprite.direction.x
		if player_x >=(screen_width/4)*3 and player_direction>0:
			self.map_shift = -8
			player.speed = 0
		elif player_x <screen_width/4 and player_direction<0:
			self.map_shift = 8
			player.speed = 0
		else:
			self.map_shift = 0
			player.speed =8
	def check_horizental_collide(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed
		for block in self.blocks:
			if block.rect.colliderect(player.rect):
				if player.direction.x <0:
					player.rect.left = block.rect.right
					player.on_left = True
					
					self.current_x = player.rect.left
				elif player.direction.x >0:
					player.rect.right = block.rect.left
					player.on_right = True
					self.current_x = player.rect.right
		if player.on_right and (self.current_x >player.rect.right or player.direction.x <=0):
			player.on_right = False
		if player.on_left and (self.current_x<player.rect.left or player.direction.x >= 0):
			player.on_left = False
		
	def check_vertical_collide(self):
		player = self.player.sprite
		#print(player.direction.y)
		player.player_gravity()
		for block in self.blocks:
			if block.rect.colliderect(player.rect):
				if player.direction.y >0:
					player.rect.bottom = block.rect.top
					player.direction.y = 0
					player.on_ground = True

				elif player.direction.y <0:
					player.direction.y = 0
					player.rect.top = block.rect.bottom
					player.on_ceiling = True
		if player.on_ground and player.direction.y <0 or player.direction.y >1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y >0:
			player.on_ceiling = False

		
	def run(self):
		#draw the map
		
			
		self.big_dust.update(self.map_shift)
		self.big_dust.draw(self.Surface)
		self.blocks.update(self.map_shift)
		self.scroll_x()
		self.blocks.draw(self.Surface)
	
		#draw the player
		self.player.update()
		self.get_player_on_ground()
		self.check_horizental_collide()
		self.check_vertical_collide()
		self.create_landing_dust()
		self.player.draw(self.Surface)
		

class Block(pygame.sprite.Sprite):
	def __init__(self, x,y):
		super().__init__()
		self.image = pygame.Surface((tile_size,tile_size))
		self.image.fill("grey")
		self.rect = self.image.get_rect(topleft = (x,y))
		
	def update(self, x_shift):
		self.rect.x += x_shift
	
class Particle_effect(pygame.sprite.Sprite):
	def __init__(self,pos,type):
		super().__init__()
		self.frame_index = 0
		self.frame_speed = 0.5
		if type == "jump":
			self.frames = import_folder("graphics/character/dust_particles/jump")
		if type == "land":
			self.frames = import_folder("graphics/character/dust_particles/jump") 
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)
	def animation(self):
		self.frame_index += self.frame_speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]
	def update(self,x_shift):
		self.rect.x += x_shift
		self.animation()
class Player(pygame.sprite.Sprite):
	def __init__(self,x,y,display_surface,create_jump_particle):
		super().__init__()
		self.import_character_assets()
		self.create_jump_particle = create_jump_particle
		self.display_surface = display_surface
		#player
		self.character_animation_state = "idle"
		self.animation_index = 0
		self.image = self.animations[self.character_animation_state][self.animation_index]
		self.rect = self.image.get_rect(topleft =(x,y))
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 6
		self.gravity = 0.8
		self.jump = -16
		self.face_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False

		#dusparticles
		self.big_dust = pygame.sprite.GroupSingle()
		self.import_dust_particle()
		self.dus_index = 0
		self.dus_speed = 0.1
		#print(self.dust_particles)
	def import_character_assets(self):
		character_path = "graphics/character/"
		self.animations = {"idle": [],"run": [],"jump": [],"fall": []}
		for animation in self.animations:
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)
	def import_dust_particle(self):
		self.dust_particles = import_folder("graphics/character/dust_particles/run")
	
	def dust_animation(self):
		if self.character_animation_state == "run":
			self.dus_index += self.dus_speed
			if self.dus_index >= len(self.dust_particles):
				self.dus_index = 0
			dust_particles = self.dust_particles[int(self.dus_index)]
			if self.face_right:
				x,y = self.rect.bottomleft
				self.display_surface.blit(dust_particles,(x-7,y-10))
			if not self.face_right:
				x,y = self.rect.bottomright
				fliped = pygame.transform.flip(dust_particles,True,False)
				self.display_surface.blit(fliped,(x+7,y-10))
	
		
	def character_animation(self):
		self.animation_index += 0.1
		if self.animation_index >= len(self.animations[self.character_animation_state]):
			self.animation_index = 0
		#self.image = pygame.image.load(f"graphics/character/{self.character_animation_state}/{self.animations['idle'][int(self.animation_index)]}")
		if self.face_right:
			self.image = self.animations[self.character_animation_state][int(self.animation_index)]
		else:
			flip = pygame.transform.flip(self.animations[self.character_animation_state][int(self.animation_index)],True,False)
			self.image = flip
		#set the origin of the player rect
		if self.on_ground and self.on_right:
			self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		elif self.on_ground and self.on_left:
			self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		elif self.on_ground:
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		elif self.on_ceiling and self.on_left:
			self.rect = self.image.get_rect(topleft = self.rect.topleft)
		elif self.on_ceiling and self.on_right:
			self.rect = self.image.get_rect(topright = self.rect.topright)
		else:
			self.rect = self.image.get_rect(midtop = self.rect.midtop)
	# def import_folder(self, path):
	# 	f = []
	# 	for (dirpath, dirnames, filenames) in walk(path):
	# 	    for file in filenames:
	# 		    full_path = f"{path}/{file}"
	# 		    image_surface = pygame.image.load(full_path).convert_alpha()
	# 		    f.append(image_surface)
	# 	return f
	def animation_status(self):
		
		if self.direction.y >1:
			self.character_animation_state = "fall"
		elif self.direction.y <0:
			self.character_animation_state = "jump"
		else:
			if self.direction.x != 0:
				self.character_animation_state = "run"
			else:
				self.character_animation_state ="idle"
			
	def key_input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.face_right = False
		elif keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.face_right = True
		else:
			self.direction.x = 0
		if keys[pygame.K_SPACE] and self.on_ground:
			self.direction.y = self.jump
			self.create_jump_particle(self.rect.midbottom - pygame.math.Vector2(0,18))
			
	def player_gravity(self):
		self.key_input()
		self.direction.y += self.gravity
		self.rect.y += self.direction.y
	def update(self):

		self.animation_status()
		self.character_animation()
		self.dust_animation()
		
level_map = [
'                            ',
'                            ',
'                            ',
' XX    XXX            XX    ',
' XX P                       ',
' XXXX         XX         XX ',
' XXXX       XX              ',
' XX    X  XXXX    XX  XX    ',
'       X  XXXX    XX  XXX   ',
'    XXXX  XXXXXX  XX  XXXX  ',
'XXXXXXXX  XXXXXX  XX  XXXX  ']

tile_size = 64
screen_width = 1200
screen_height = len(level_map) * tile_size
print(screen_height)
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
level = Level(level_map,screen)
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	screen.fill("black")
	level.run()
	pygame.display.update()
	clock.tick(60)
