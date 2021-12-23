import pygame
import random
pygame.init()
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()

def score_calculate(obstacle_list, count):
	value = True
	if obstacle_list:
		
		for ostacle in obstacle_list:

			if ostacle.x <6:
				if value:
					count = count + 1
					value = False
	return count


def score_display(start_time, test_font,screen,score):
	current_time = int((pygame.time.get_ticks() /1000 - start_time))
	text_surf = test_font.render(f"Your Score: {score}, Time: {str(current_time)}", True,(64,64,64))
	text_rect = text_surf.get_rect(center = (400,30))
	screen.blit(text_surf,text_rect)

def obstacle_movement(obstacle_list):
	if obstacle_list:
		for obstacle_rect in obstacle_list:
			obstacle_rect.x -= random.randint(5,6)
			if obstacle_rect.bottom == 300:
				screen.blit(snail_surf,obstacle_rect)
			else:
				screen.blit(fly_surf,obstacle_rect)
		obstacle_list = [x for x in obstacle_list if x.x >0]
		return obstacle_list
		
	else:
		return []

def collide_check(obstacle_list, player):
	if obstacle_list:
		for obstacle_rect in obstacle_list:
			if player.colliderect(obstacle_rect): return False
				

			else: return True
	else:
		return True

def player_animation():
	global player_index,player_surf
	if player_rect.bottom < 300:
		player_surf = player_jump
	else:
		player_index += 0.1
		if player_index >= len(player_walk):
			player_index = 0
		player_surf = player_walk[int(player_index)]


test_font = pygame.font.Font("font/Pixeltype.ttf",50)
# text_surface = test_font.render("My Game: 000", False,"Green")
#text_rect = text_surface.get_rect(center = (400,30))
start_time = 0
ground_surface = pygame.image.load("graphics/ground.png").convert()
sky_surface = pygame.image.load("graphics/Sky.png").convert()
snail_frame1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_index = 0
snail_holder = [snail_frame1,snail_frame2]
snail_surf = snail_holder[snail_index]
#snail_rect = snail_surf.get_rect(bottomright = (700,300))

fly_frame1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
fly_frame2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
fly_holder = [fly_frame1,fly_frame2]
fly_index = 0
fly_surf =fly_holder[fly_index]
player_walk1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk1,player_walk2]
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
player_index = 0
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))


player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
Player_stand_rect = player_stand.get_rect(center = (400,140))
#-----------
text_play_again = test_font.render("Press Space to Play Again", False,"Green")
play_again_surf = text_play_again.get_rect(center = (400,270))
playagain = pygame.draw.rect(screen,"pink",play_again_surf)
text_play = test_font.render("Press Space to Play", False,"Green")
play_surf = text_play.get_rect(center = (400,270))
#-----------
obstacle_rect_list = []
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 300)
#--------------------
volocity = 0
score = 0
count = 0
game_active = False
while True:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		# CHECK for collision with the player_rect using event loop
		if game_active:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if player_rect.bottom == 300 and player_rect.collidepoint(event.pos):
				#if not handled and player_rect.collidepoint(pygame.mouse.get_pos()):
					volocity = -14
			
			    
			# 	print(event.pos)
			# 	if player_rect.collidepoint(event.pos): print("colli")
			#-------------------------
			# check for keyboard input using event loop
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s:
					if player_rect.bottom == 300:
					    volocity = -13
					    
		else:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					game_active = True
					
					start_time = pygame.time.get_ticks() /1000
		if game_active:
			if event.type == obstacle_timer:
				if random.randint(0,2):
					obstacle_rect_list.append(snail_surf.get_rect(bottomleft = (random.randint(800,1000),300)))
					
				else:
					obstacle_rect_list.append(fly_surf.get_rect(bottomleft=(random.randint(800,1000),210)))	
			if event.type == snail_animation_timer:
				if snail_index ==0: snail_index = 1
				else: snail_index = 0
				snail_surf = snail_holder[snail_index]
			if event.type == fly_animation_timer:
				if fly_index == 0: fly_index = 1
				else: fly_index = 0
				fly_surf = fly_holder[fly_index]
	#print(pygame.mouse.get_pressed())	
	if game_active:

		
		#draw a line from top left to mouse posion
		#pygame.draw.line(screen,"pink",(0,0),pygame.mouse.get_pos(), width=3)
		#pygame.draw.rect(screen,"#c0e8ec",(text_rect[0]-5,text_rect[1]-5,text_rect[2]+10,text_rect[3]+10))
		#pygame.draw.rect(screen,"#c0e8ec",(text_rect[0]-10,text_rect[1]-10,text_rect[2]+15,text_rect[3]+14),width =5, border_radius =5)
		#screen.blit(text_surface,text_rect)
		
		
		#print(snail_rect.bottomright, snail_rect.right)
		# if snail_rect.right <0:
		# 	score += 1
		# 	snail_rect.left = 800
		# 	print(score)
		#screen.blit(snail_surf,snail_rect)
		player_animation()
		screen.blit(player_surf,player_rect)
		volocity += 0.5
		player_rect.y += volocity
		if player_rect.bottom >300:
			player_rect.bottom = 300
		#print(volocity)

		obstacle_list = obstacle_movement(obstacle_rect_list)
		#print(collide_check(obstacle_list,player_rect))
		game_active = collide_check(obstacle_list,player_rect)
		count = score_calculate(obstacle_list,count)
		print(count)
		score_display(start_time, test_font,screen,count)
		#-------------------------
		# CHECK for collision with the player_rect using pygame.mouse function
		# mouse_pos = pygame.mouse.get_pos()
		# print(mouse_pos, [x for x in pygame.mouse.get_pos()])

		# if player_rect.collidepoint([x for x in pygame.mouse.get_pos()]):
		# 	print("collide")
		#-------------------------------


		#------------------------------

		# CHECK FOR BUTTON PRESS
		# keys = pygame.key.get_pressed()
		# if keys[pygame.K_SPACE]:
		# 	print("jump")
		#----------------------
	else:
		#playagain = pygame.draw.rect(screen,"pink",(400-40,200-40,80,80))
		screen.blit(player_stand,Player_stand_rect)
		start_time = pygame.time.get_ticks() / 1000
		obstacle_rect_list = []
		count = 0
		if score == 0:
			screen.blit(text_play,play_surf)
			
		else:
			screen.blit(text_play_again,play_again_surf)
			score = 0
		
		if playagain.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
			game_active = True
			
	pygame.display.update()
	screen.blit(sky_surface,(0,0))
	screen.blit(ground_surface,(0,300))
	clock.tick(60)
