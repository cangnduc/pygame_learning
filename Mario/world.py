import pygame
from os import walk
from csv import reader
import random

import math

#dawdawdw
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

def level_data():
	final_dic = {}
	for (dirpaths, dirnamess, filenamess) in walk("Levels/"):
		
		
		for level in dirnamess[:-2]:
			#print(level)
			dics = {}
			for (a, b, c) in walk(f"Levels/{level}"):
				 new_list = [f"Levels/{level}/{i}" for i in c]
				 #dics[int(level)] = new_list
			
			for item in new_list:
				dics[item.split("_",2)[2][:-4]] = item
			
			dics["node_pos"] = pos_list[int(level)]
			dics["node_graphics"] = f"graphics/overworld/{level}"
			if int(level) < len(dirnamess[:-2])-1:
				dics["unclock"] = int(level) + 1
			else:
				dics["unclock"] = int(level)
			final_dic[int(level)] = dics
			
	return final_dic

class Node(pygame.sprite.Sprite):
	def __init__(self,pos,status,icon_speed,path):
		super().__init__()
		self.frames = import_folder(path)
		self.frame_index = 0

		self.image = self.frames[self.frame_index]

		if status == "available":
			self.status = 'available'
		if status == "blocked":
			self.status = 'blocked'
		self.rect = self.image.get_rect(center = pos)
		self.detection_zone = pygame.Rect(self.rect.centerx -(icon_speed//2),self.rect.centery -(icon_speed//2),icon_speed,icon_speed)
	def animated(self):
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]
	def update(self):
		if self.status == "available":
			self.animated()
		else:
			tint_surf = self.image.copy()
			tint_surf.fill("black", None, pygame.BLEND_RGBA_MULT)
			self.image.blit(tint_surf,(0,0))
class Icon(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.pos = pos
		self.frames = import_folder("graphics/character/idle")
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)
	def animated(self):
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]
		
	def update(self):
		self.animated()
		self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		self.rect.center = self.pos
		
class UI:
	def __init__(self, surface):
		self.display_surface = surface

		#health
		self.health_bar = pygame.image.load("graphics/ui/health_bar.png").convert_alpha()
		self.health_bar_topleft = (54,50)

		self.bar_max_width = 152
		self.bar_height =4
		#coin
		self.coin = pygame.image.load("graphics/ui/coin.png").convert_alpha()
		self.coin_rect = self.coin.get_rect(center = (40,100))
		self.font = pygame.font.SysFont(None,30)
	def show_health(self,current, full):
		self.display_surface.blit(self.health_bar,(20,20))
		current_ratio = current / full
		current_bar_width = self.bar_max_width * current_ratio
		health_bar_rect = pygame.Rect(self.health_bar_topleft,(current_bar_width,self.bar_height))
		pygame.draw.rect(self.display_surface,"red",health_bar_rect)

	def show_coin(self,coin_num):
		self.display_surface.blit(self.coin,self.coin_rect)
		
		self.coin_surf = self.font.render(str(coin_num),True,"White")
		self.coin_text_rect = self.coin_surf.get_rect(center = ((self.coin_rect.right + 25),self.coin_rect.centery))
		self.display_surface.blit(self.coin_surf,self.coin_text_rect)

class Game:
	def __init__(self):
		self.bg_music = pygame.mixer.Sound('audio/level_music.wav')
		self.world_music = pygame.mixer.Sound('audio/overworld_music.wav')
		self.bg_music.set_volume(0.1)
		self.world_music.set_volume(0.1)
		self.max_health = 100
		self.current_health = 100
		self.coin = 0
		self.ui = UI(screen)
		self.max_level = 0
		self.world = World(0,self.max_level,screen,self.create_level)
		self.status = "overworld"
		self.world_music.play(-1)

		#self.level = Level(1,screen)

	def create_level(self,current_level):
		self.level = Level(current_level,screen,self.create_world,self.change_coin,self.change_health)
		self.status = "level"
		self.bg_music.play(-1)
		self.world_music.stop()
		
	
	def create_world(self,current_level,new_max_level):
		if new_max_level >self.max_level:
			self.max_level = new_max_level
		self.world = World(current_level,self.max_level,screen,self.create_level)
		self.status ="overworld"
		self.world_music.play(-1)
		self.bg_music.stop()
	def change_coin(self,amount):
		self.coin += amount
		if self.coin >=20:
			self.current_health += 10
			self.coin = 0
	def change_health(self,amount):
		self.current_health += amount
	def game_over(self):
		if self.current_health <=0:
			self.current_health = 100
			self.coin = 0
			self.max_level = 0
			self.status = "overworld"
			self.world = World(0,self.max_level,screen,self.create_level)
			
	def run(self):
		
		if self.status == "overworld":
			self.world.run()
		else:

			self.level.run()
			# self.coin = self.level.eating_coin(self.coin)

			self.ui.show_health(self.current_health,self.max_health)
			self.ui.show_coin(self.coin)
			self.game_over()
			

class World:
	def __init__(self,start_level,max_level,surface,create_level):
		# setup
		self.display_surface = surface
		self.max_level = max_level
		self.current_level = start_level
		self.create_level = create_level
		self.move_direction = pygame.math.Vector2(0,0)
		self.speed = 5
		self.moving = False
		self.setup_node()
		self.setup_icon()
		self.sky = Sky(8,'overworld')
		#time
		self.start_time = pygame.time.get_ticks()
		self.allow_input = False
		self.timer_length = 600
	def setup_node(self):
		self.nodes = pygame.sprite.Group()
		for index, node_data in levels.items():
			if index <= self.max_level:
				node_sprite = Node(node_data["node_pos"],"available",self.speed,node_data['node_graphics'])
			elif index >self.max_level:
				node_sprite = Node(node_data["node_pos"],"blocked",self.speed,node_data['node_graphics'])
			self.nodes.add(node_sprite)
	def setup_icon(self):
		self.icon = pygame.sprite.GroupSingle()
		icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
		self.icon.add(icon_sprite)

	def draw_path(self):
		if self.max_level >0:
			lists = [value["node_pos"] for index, value in levels.items() if index<= self.max_level]
			pygame.draw.lines(self.display_surface,"red",False,lists,5)
	def input(self):
		keys = pygame.key.get_pressed()
		if not self.moving and self.allow_input:
			if keys[pygame.K_RIGHT] and self.current_level<self.max_level:
				self.move_direction = self.get_movement_data("forward")
				self.current_level += 1
				self.moving = True
				
			elif keys[pygame.K_LEFT] and self.current_level >0:
				self.move_direction = self.get_movement_data("backward")
				self.current_level -= 1
				self.moving = True
			elif keys[pygame.K_SPACE]:
				self.create_level(self.current_level)
	def get_movement_data(self,direction):
		start =  pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
		if direction == "forward":
			end =  pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
		else:
			end =  pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)
		result = (end - start).normalize()
		
		return result
	def update_icon_pos(self):
		if self.moving and self.move_direction:
			self.icon.sprite.pos += self.move_direction * self.speed
			target_node = self.nodes.sprites()[self.current_level]
			if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
				
				self.moving = False
				self.move_direction = pygame.math.Vector2(0,0)
	def input_timer(self):
		if not self.allow_input:
			current_time = pygame.time.get_ticks()
			if current_time - self.start_time >= self.timer_length:
				self.allow_input = True
	def run(self):
		self.sky.draw(self.display_surface)
		self.draw_path()
		self.nodes.draw(self.display_surface)
		self.nodes.update()
		self.icon.draw(self.display_surface)
		self.input()
		self.update_icon_pos()
		self.icon.update()
		self.input_timer()
class Level1:
	def __init__(self, current_level, display_surface,create_world):
		self.create_world = create_world
		self.display_surface = display_surface
		self.current_level = current_level
		level_data = levels[current_level]
		level_content = level_data["content"]
		self.next_max_level = level_data['unclock']
		#display
		self.font = pygame.font.Font(None,40)
		self.text_surf = self.font.render(level_content,True,"White")
		self.text_rect = self.text_surf.get_rect(center =(screen_width//2,screen_height//2))

	def run(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RETURN]:
			self.create_world(self.current_level,self.next_max_level)
		if keys[pygame.K_ESCAPE]:
			self.create_world(self.current_level,0)
		self.display_surface.blit(self.text_surf,self.text_rect)

class Particle_effect(pygame.sprite.Sprite):
	def __init__(self,pos,type):
		super().__init__()
		self.frame_index = 0
		self.frame_speed = 0.5
		if type == "jump":
			self.frames = import_folder("graphics/character/dust_particles/jump")
		if type == "land":
			self.frames = import_folder("graphics/character/dust_particles/jump")
		if type =="explosion":
			self.frames = import_folder("graphics/enemy/explosion")
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
	def __init__(self,x,y,display_surface,create_jump_particle,change_health):
		super().__init__()
		self.change_health = change_health
		self.import_character_assets()
		self.create_jump_particle = create_jump_particle
		self.display_surface = display_surface
		#player
		self.character_animation_state = "idle"
		self.animation_index = 0
		self.image = self.animations[self.character_animation_state][self.animation_index]
		self.rect = self.image.get_rect(topleft =(x,y))
		self.coliision_rect = pygame.Rect(self.rect.topleft,(50,self.rect.height))
		
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 6
		self.gravity = 0.8
		self.jump = -16
		self.face_right = True
		self.on_ground = False
		self.on_ceiling = False
		self.on_left = False
		self.on_right = False
		self.invincible = False
		self.invincible_duration = 700
		#dusparticles
		self.big_dust = pygame.sprite.GroupSingle()
		self.import_dust_particle()
		self.dus_index = 0
		self.dus_speed = 0.1
		self.hurt_time = 0

		#Player sound
		self.jump_sound = pygame.mixer.Sound('audio/effects/jump.wav')
		self.jump_sound.set_volume(0.5)
		self.hit_sound = pygame.mixer.Sound('audio/effects/hit.wav')
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
	
	def get_damage(self,type ="walking"):

		if not self.invincible:
			self.invincible = True
			self.hit_sound.play()
			self.hurt_time = pygame.time.get_ticks()
			self.change_health(-10)
		if type == "falling":
			self.change_health(-30)
	def character_animation(self):
		self.animation_index += 0.1
		if self.animation_index >= len(self.animations[self.character_animation_state]):
			self.animation_index = 0
		#self.image = pygame.image.load(f"graphics/character/{self.character_animation_state}/{self.animations['idle'][int(self.animation_index)]}")
		if self.face_right:
			self.image = self.animations[self.character_animation_state][int(self.animation_index)]
			self.rect.bottomleft = self.coliision_rect.bottomleft
		else:
			flip = pygame.transform.flip(self.animations[self.character_animation_state][int(self.animation_index)],True,False)
			self.image = flip
			self.rect.bottomright = self.coliision_rect.bottomright
		
		if self.invincible:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else: self.image.set_alpha(255)
		self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		#set the origin of the player rect
		# if self.on_ground and self.on_right:
		# 	self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		# elif self.on_ground and self.on_left:
		# 	self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		# elif self.on_ground:
		# 	self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		# elif self.on_ceiling and self.on_left:
		# 	self.rect = self.image.get_rect(topleft = self.rect.topleft)
		# elif self.on_ceiling and self.on_right:
		# 	self.rect = self.image.get_rect(topright = self.rect.topright)
		# else:
		# 	self.rect = self.image.get_rect(midtop = self.rect.midtop)
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
	def wave_value(self):
		value = math.sin(pygame.time.get_ticks())
		if value >0: return 255
		else: return 0	
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
			self.jump_sound.play()
			self.create_jump_particle(self.rect.midbottom - pygame.math.Vector2(0,18))
	
	def player_gravity(self):
		self.key_input()
		self.direction.y += self.gravity
		self.coliision_rect.y += self.direction.y
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
	def __init__(self,size,x,y,path,value):
		super().__init__(size,x,y,path)
		center_x = x + int((size/2))
		center_y = y + int(size/2)
		self.rect = self.image.get_rect(center = (center_x,center_y))
		self.value = value
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
	def __init__(self,horizon, style = "level"):
		self.top = pygame.image.load("graphics/decoration/sky/sky_top.png").convert_alpha()
		self.middle = pygame.image.load("graphics/decoration/sky/sky_middle.png").convert_alpha()
		self.bottom = pygame.image.load("graphics/decoration/sky/sky_bottom.png").convert_alpha()
		self.horizon = horizon
		self.style = style
		if self.style == "overworld":
			palm_surfaces = import_folder("graphics/overworld/palms")
			self.palms = []
			for surface in [random.choice(palm_surfaces) for _ in range(15)]:
				x = random.randint(0,screen_width)
				y = (self.horizon * tile_size) +   random.randint(00,75)
				rect = surface.get_rect(midbottom = (x,y))
				self.palms.append((surface,rect))

			cloud_surfaces = import_folder("graphics/overworld/clouds")
			self.clouds = []
			for surface in [random.choice(cloud_surfaces) for _ in range(7)]:
				x = random.randint(0,screen_width)
				y = random.randint(0,tile_size * self.horizon) -100
				rect = surface.get_rect(midbottom = (x,y))
				self.clouds.append((surface,rect))

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
		if self.style == 'overworld':
			for cloud in self.clouds:
				screen.blit(cloud[0],cloud[1])
			for palm in self.palms:
				screen.blit(palm[0],palm[1])
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
	def __init__(self, current_level,surface,create_world,change_coin,change_health):
		self.display_surface = surface
		self.world_shift = 0
		self.change_coin = change_coin
		#Sky decoration
		self.sky = Sky(5)
		self.big_dust =pygame.sprite.GroupSingle()
		self.explosion_sprite = pygame.sprite.GroupSingle()

		#overworld connection
		self.create_world = create_world
		self.current_level = current_level
		self.Level_data = levels[self.current_level]
		self.new_max_level = self.Level_data["unclock"]
		#audio
		self.coin_sound = pygame.mixer.Sound("audio/effects/Mario-coin-sound.mp3")
		self.stomp_sound = pygame.mixer.Sound("audio/effects/stomp.wav")

		#player set up
		player_csv = import_csv_layout(self.Level_data["player"])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_csv,change_health)
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
							sprite = Coins(tile_size,x,y,"graphics/coins/gold/",2)
						elif col == "1":
							sprite = Coins(tile_size,x,y,"graphics/coins/silver/",1)
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

	def player_setup(self,playout,change_health):
		for row_index, row in enumerate(playout):
			for col_index, col in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if col == "0":
					player = Player(x+20,y,self.display_surface,self.create_jump_particle,change_health)
					self.player.add(player)
				if col =="1":
					goal_sur = pygame.image.load("graphics/character/hat.png").convert_alpha()
					sprite = StaticTile(tile_size,x+8,y,goal_sur)
					self.goal.add(sprite)
	def check_horizental_collide(self):
		player = self.player.sprite
		player.coliision_rect.x += player.direction.x * player.speed
		self.blocks = self.terrain_sprites.sprites() + self.fg_plam_tree_sprites.sprites() + self.crate_sprites.sprites()
		for block in self.blocks:
			if block.rect.colliderect(player.coliision_rect):
				if player.direction.x <0:
					player.coliision_rect.left = block.rect.right
					player.on_left = True
					
					self.current_x = player.coliision_rect.left
				elif player.direction.x >0:
					player.coliision_rect.right = block.rect.left
					player.on_right = True
					self.current_x = player.coliision_rect.right
	def check_vertical_collide(self):
		player = self.player.sprite
		#print(player.direction.y)
		player.player_gravity()
		self.blocks = self.terrain_sprites.sprites() + self.fg_plam_tree_sprites.sprites() + self.crate_sprites.sprites()
		for block in self.blocks:
			if block.rect.colliderect(player.coliision_rect):
				if player.direction.y >0:
					player.coliision_rect.bottom = block.rect.top
					player.direction.y = 0
					player.on_ground = True

				elif player.direction.y <0:
					player.direction.y = 0
					player.coliision_rect.top = block.rect.bottom
					player.on_ceiling = True
		if player.on_ground and player.direction.y <0 or player.direction.y >1:
			player.on_ground = False
		
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

		
	def enemy_collidesion(self):
		for enemy in self.enemy_sprites.sprites():
			if pygame.sprite.spritecollide(enemy, self.constrain_sprites, False):
				enemy.reverse_speed()
	def eating_coin(self,coin_num):
		#print(self.player.sprite.rect)
		blocks_hit_list = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True)
		for block in blocks_hit_list:
			coin_num += 1
		return coin_num
		# for coin in self.coins_sprites.sprites():
		# 	if pygame.sprite.spritecollide(self.player.sprite,coin,True):
		# 		print("collide")#another way of counting coin number ( calling from Game class)
	def check_coin_collide(self):
		blocks_hit_list = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True)
		if blocks_hit_list:
			self.coin_sound.play()
			for block in blocks_hit_list:
				self.change_coin(block.value)
	def check_enemy_collidesion(self):
		enemy_collision = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)
		current_time = pygame.time.get_ticks()
		if enemy_collision:

			for enemy in enemy_collision:
				enemy_centery = enemy.rect.centery
				enemy_top = enemy.rect.top
				player_bottom = self.player.sprite.rect.bottom
				
				if enemy_top < player_bottom < enemy_centery and self.player.sprite.direction.y >= 0:
					self.stomp_sound.play()
					self.player.sprite.invincible = True
					self.player.sprite.direction.y = -15
					explosion_particle = Particle_effect(enemy.rect.center,"explosion")
					self.explosion_sprite.add(explosion_particle)
					enemy.kill()
					#explosion_particle.draw(self.display_surface)
				else:
					self.player.sprite.get_damage()
		if self.player.sprite.invincible:
			if current_time - self.player.sprite.hurt_time >self.player.sprite.invincible_duration:
				self.player.sprite.invincible = False
	
	def after_death(self):
		if self.player.sprite.rect.top > screen_height:
			time_death = pygame.time.get_ticks()
	def check_death(self):
		

		if self.player.sprite.rect.top > screen_height:
			self.player.sprite.get_damage("falling")
			self.create_world(self.current_level,0)
			

	def check_win(self):
		if pygame.sprite.spritecollide(self.player.sprite,self.goal,False):
			self.create_world(self.current_level,self.new_max_level)
	def run(self):
		self.check_coin_collide()
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
		#self.eating_coin()
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
		self.check_win()
		self.check_death()
		self.check_enemy_collidesion()
		self.explosion_sprite.update(self.world_shift)
		self.explosion_sprite.draw(self.display_surface)
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
pos_list = [(110,400),(300,220),(480,610),(610,350),(880,210),(1050,400)]
levels = level_data()

tile_size = 64
screen_width = 1200
screen_height = 12 * tile_size
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	screen.fill("grey")
	game.run()
	pygame.display.update()
	clock.tick(60)
