import pygame
from os import walk
from csv import reader
import random
from levels import *
pygame.init()
def import_csv_layout(path):
	terrain_map = []
	with open(path) as map:
		level = reader(map, delimiter = ",")
		for row in level:
			terrain_map.append(list(row))
	return terrain_map
def import_cut_graphic(path):
	surface = pygame.image.load(path).convert_alpha()
	tile_num_x = int(surface.get_size()[0]/tile_size)
	tile_num_y = int(surface.get_size()[1]/tile_size)
	cut_tiles = []
	for row in range(tile_num_y):
		for col in range(tile_num_x):
			x = col * tile_size
			y = row * tile_size
			new_surface = pygame.Surface((tile_size,tile_size),flags = pygame.SRCALPHA)
			new_surface.blit(surface,(0,0),pygame.Rect(x,y,tile_size,tile_size))
			cut_tiles.append(new_surface)
	return cut_tiles
def import_folder(path):
	f = []
	for (dirpath, dirnames, filenames) in walk(path):
	    for file in filenames:
		    full_path = f"{path}/{file}"
		    image_surface = pygame.image.load(full_path).convert_alpha()
		    f.append(image_surface)
	return f

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
class Tile(pygame.sprite.Sprite):
	def __init__(self, size,x,y):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.image.fill("grey")
		self.rect = self.image.get_rect(topleft = (x,y))
	def update(self,x_shift):
		self.rect.x += x_shift
class StaticTile(Tile):
	def __init__(self,size,x,y,surface):
		super().__init__(size,x,y)
		self.image = surface
class Crate(StaticTile):
	def __init__(self,size,x,y):
		super().__init__(size,x,y,pygame.image.load("graphics/terrain/crate.png").convert_alpha())
		offset_y = y + size *3
		
		self.rect = self.image.get_rect(bottomleft = (x,offset_y))
		
class AnimatedTile(Tile):
	def __init__(self,size,x,y,path):
		super().__init__(size,x,y)
		self.frames = import_folder(path)
		self.frames_index = 0
		self.image = self.frames[self.frames_index]
		# self.rect = self.image.get_rect(topleft=(x,y)) inherited from Tile class
	def tile_animate(self):
		self.frames_index += 0.15
		if self.frames_index >= len(self.frames):
			self.frames_index = 0
		self.image = self.frames[int(self.frames_index)]
	def update(self,x_shift):
		self.rect.x += x_shift
		self.tile_animate()

class Coins(AnimatedTile):
	def __init__(self,size,x,y,path):
		super().__init__(size,x,y,path)
		center_x = x + int((size/2))
		center_y = y + int(size/2)
		self.rect = self.image.get_rect(center = (center_x,center_y))

class Palm(AnimatedTile):
	def __init__(self,size,x,y,path):
		super().__init__(size,x,y,path)
		new_y = y - self.rect.width
		self.rect = self.image.get_rect(topleft =(x,new_y))
class Enemies(AnimatedTile):
	def __init__(self,size,x,y):
		super().__init__(size,x,y,"graphics/enemy/run/")
		y_offset = y + 20
		self.speed = random.choice([3,-3,5,-5])
		self.rect.y = y_offset
	def move(self):
		self.rect.x += self.speed
	def reverse_speed(self):
		self.speed *= -1
	def facing(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image, True, False)

	def update(self,x_shift):
		self.rect.x += x_shift
		self.move()
		self.tile_animate()
		self.facing()

class Sky:
	def __init__(self,horizon):
		self.top = pygame.image.load("graphics/decoration/sky/sky_top.png").convert_alpha()
		self.middle = pygame.image.load("graphics/decoration/sky/sky_middle.png").convert_alpha()
		self.bottom = pygame.image.load("graphics/decoration/sky/sky_bottom.png").convert_alpha()
		self.horizon = horizon
	def strech(self):
		self.top = pygame.transform.scale(self.top,(screen_width,tile_size))
		self.middle = pygame.transform.scale(self.middle,(screen_width,tile_size))
		self.bottom = pygame.transform.scale(self.bottom,(screen_width,tile_size))
	def draw(self,screen):
		self.strech()
		for i in range(vertical_tile_number):
			y = i * tile_size
			if i<self.horizon: 
				screen.blit(self.top,(0,y))
			elif self.horizon<i<11:
				screen.blit(self.middle,(0,y))
			else:
				screen.blit(self.bottom,(0,y))
class Cloud:
	def __init__(self,horizon,cloud_width,cloud_number):
		self.horizon = horizon
		cloud_list  = import_folder("graphics/decoration/clouds/")
		min_x = - screen_width/2
		max_x = cloud_width + screen_width/2
		min_y = 20
		max_y = self.horizon
		self.cloud_sprites = pygame.sprite.Group()
		for cloud in range(cloud_number):
			cloud = random.choice(cloud_list)
			x = random.randint(min_x,max_x)
			y = random.randint(min_y,max_y)
			sprite = StaticTile(0,x,y,cloud)
			self.cloud_sprites.add(sprite)
	def draw(self,surface,x_shift):
		for cloud in self.cloud_sprites.sprites():
			if x_shift <0:
				cloud.rect.x -=1
			else:
				cloud.rect.x +=1
		self.cloud_sprites.update(x_shift)
		self.cloud_sprites.draw(surface)

class Water:
	def __init__(self,water_y,water_width):
		water_start = - screen_width/2
		water_tile_width = 192
		tile_x_amount = int((water_width+screen_width)/water_tile_width)
		self.water_sprites = pygame.sprite.Group()
		for tile in range(tile_x_amount+3):
			x = tile * water_tile_width + water_start
			y = water_y
			sprite = AnimatedTile(192,x,y,"graphics/decoration/water/")
			self.water_sprites.add(sprite)
	def draw(self,surface,x_shift):
		
		self.water_sprites.update(x_shift)
		self.water_sprites.draw(surface)
class Level:
	def __init__(self, Level_data, surface):
		self.display_surface = surface
		self.world_shift = 0
		self.Level_data = Level_data
		#Sky decoration
		self.sky = Sky(5)
		self.big_dust =pygame.sprite.GroupSingle()

		#player set up
		player_csv = import_csv_layout(self.Level_data["player"])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_csv)
		self.player_on_ground = False
		self.current_x = 0
		#terrain set up
		terrain_csv = import_csv_layout(self.Level_data["terrain"])
		self.terrain_sprites = self.create_tile_group(terrain_csv,"terrain")
		# grass setup
		grass_csv = import_csv_layout(self.Level_data["grass"])
		self.grass_sprites = self.create_tile_group(grass_csv,"grass")
		#print(self.Level_data.keys())
		#crate
		crate_csv = import_csv_layout(self.Level_data["crate"])
		self.crate_sprites = self.create_tile_group(crate_csv,"crate")
		#coins
		coin_csv = import_csv_layout(self.Level_data["coin"])
		self.coins_sprites = self.create_tile_group(coin_csv,"coins")
		#fg_palm_tree
		fg_plam_tree_csv = import_csv_layout(self.Level_data["fg_palms"])
		self.fg_plam_tree_sprites = self.create_tile_group(fg_plam_tree_csv,"fg_plam_tree")
		#bg_palm_tree
		bg_palm_tree_csv = import_csv_layout(self.Level_data["bg_palms"])
		self.bg_palm_sprites = self.create_tile_group(bg_palm_tree_csv,"bg_palm_tree")
		#Enemy
		enemy_csv = import_csv_layout(self.Level_data["enemy"])
		self.enemy_sprites = self.create_tile_group(enemy_csv,"enemies")

		#constrain
		constrain_csv = import_csv_layout(self.Level_data["Contrains"])
		self.constrain_sprites = self.create_tile_group(constrain_csv,"Contrains")
		# Water
		water_width = int(len(terrain_csv[0]) * tile_size)
		
		self.water = Water(screen_height-50,water_width)
		# Cloud
		self.cloud = Cloud(200,water_width,12)
		
	def create_tile_group(self,playout,type):
		sprite_group = pygame.sprite.Group()
		for row_index, row in enumerate(playout):
			for col_index, col in enumerate(row):
				if col != "-1":
					x = col_index * tile_size
					y = row_index * tile_size
					if type == "terrain":
						terrain_tile_list = import_cut_graphic("graphics/terrain/terrain_tiles.png")
						tile_surface = terrain_tile_list[int(col)]
						sprite = StaticTile(tile_size,x,y,tile_surface)
						
					if type == "grass":
						grass_tile_list = import_cut_graphic("graphics/decoration/grass/grass.png")
						tile_surface = grass_tile_list[int(col)]
						sprite = StaticTile(tile_size,x,y,tile_surface)
					if type == "crate":
						sprite = Crate(tile_size,x,y)
					if type =="coins":
						if col == "0":
							sprite = Coins(tile_size,x,y,"graphics/coins/gold/")
						elif col == "1":
							sprite = Coins(tile_size,x,y,"graphics/coins/silver/")
					if type == "fg_plam_tree":
						sprite = Palm(tile_size,x,y,"graphics/terrain/palm_large/")
					if type == "bg_palm_tree":
						sprite = Palm(tile_size,x,y,"graphics/terrain/palm_bg/")
					if type == "enemies":
						sprite = Enemies(tile_size,x,y)
					if type == "Contrains":
						sprite = Tile(tile_size,x,y)
					sprite_group.add(sprite)
		return sprite_group

	def create_jump_particle(self,pos):
		if self.player.sprite.face_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		big_dust = Particle_effect(pos,"jump")
		self.big_dust.add(big_dust)

	def player_setup(self,playout):
		for row_index, row in enumerate(playout):
			for col_index, col in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if col == "0":
					player = Player(x+20,y,self.display_surface,self.create_jump_particle)
					self.player.add(player)
				if col =="1":
					goal_sur = pygame.image.load("graphics/character/hat.png").convert_alpha()
					sprite = StaticTile(tile_size,x+8,y,goal_sur)
					self.goal.add(sprite)
	def check_horizental_collide(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed
		self.blocks = self.terrain_sprites.sprites() + self.fg_plam_tree_sprites.sprites() + self.crate_sprites.sprites()
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
			self.world_shift = -8
			player.speed = 0
		elif player_x <screen_width/4 and player_direction<0:
			self.world_shift = 8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed =8
	def check_vertical_collide(self):
		player = self.player.sprite
		#print(player.direction.y)
		player.player_gravity()
		self.blocks = self.terrain_sprites.sprites() + self.fg_plam_tree_sprites.sprites() + self.crate_sprites.sprites()
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

		
	def enemy_collidesion(self):
		for enemy in self.enemy_sprites.sprites():
			if pygame.sprite.spritecollide(enemy, self.constrain_sprites, False):
				enemy.reverse_speed()
	def run(self):
		# sky
		self.sky.draw(self.display_surface)
		self.cloud.draw(self.display_surface,self.world_shift)
		#water
		self.water.draw(self.display_surface,self.world_shift)
		#grass

		self.grass_sprites.draw(self.display_surface)
		self.grass_sprites.update(self.world_shift)
		#palm fg tree
		self.bg_palm_sprites.draw(self.display_surface)
		self.bg_palm_sprites.update(self.world_shift)
		
		#bg palm tree


		

		
		#crate
		self.crate_sprites.draw(self.display_surface)
		self.crate_sprites.update(self.world_shift)
		#Enemies

		self.enemy_sprites.draw(self.display_surface)
		self.enemy_sprites.update(self.world_shift)
		self.enemy_collidesion()
		self.constrain_sprites.update(self.world_shift)
		
		#palm fg tree
		self.fg_plam_tree_sprites.draw(self.display_surface)
		self.fg_plam_tree_sprites.update(self.world_shift)
		#terrain
		self.terrain_sprites.draw(self.display_surface)
		self.terrain_sprites.update(self.world_shift)
		#coins
		self.coins_sprites.update(self.world_shift)
		self.coins_sprites.draw(self.display_surface)
		#player
		
		
		self.scroll_x()
		self.big_dust.draw(self.display_surface)
		self.big_dust.update(self.world_shift)
		self.player.update()
		self.check_horizental_collide()
		self.get_player_on_ground()
		
		self.check_vertical_collide()
		self.create_landing_dust()
		self.player.draw(self.display_surface)
		#goal
		self.goal.draw(self.display_surface)
		self.goal.update(self.world_shift)
		
# level_0 = {'bg_palms': 'Levels/0/level_0._bg_palms.csv',
# 		 'coin': 'Levels/0/level_0._coin.csv',
# 		 'Contrains': 'Levels/0/level_0._Contrains.csv',
# 		 'crate': 'Levels/0/level_0._crate.csv',
# 		 'enemy': 'Levels/0/level_0._enemy.csv',
# 		 'fg_palms': 'Levels/0/level_0._fg_palms.csv',
# 		 'grass': 'Levels/0/level_0._grass.csv',
# 		 'player': 'Levels/0/level_0._player.csv',
# 		 'terrain': 'Levels/0/level_0._terrain.csv'}
# function for return dictionary in folder

vertical_tile_number = 12
tile_size = 64
screen_height = vertical_tile_number * tile_size
screen_width = 1200
screen = pygame.display.set_mode((screen_width,screen_height))
level = Level(level_0,screen)
clock = pygame.time.Clock()

while True:
	screen.fill("grey")
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	
	level.run()
	pygame.display.update()
	clock.tick(60)
