import numpy as np
import pygame
import random
import time
import cv2
import mediapipe as mp
import numpy
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
screen_width, screen_height = 800, 600


cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpdraw = mp.solutions.drawing_utils

def findxy():
	if results.multi_hand_landmarks:
		# print(len(results.multi_hand_landmarks)) // number of hands
		for handlms in results.multi_hand_landmarks:

			for id, lm in enumerate(handlms.landmark):
				h, w, c, = img.shape
				cx, cy = int(lm.x * w), int(lm.y * h)
				if id == 8:
					cv2.circle(img, (cx, cy), 15, (255, 0, 0), 4)
			mpdraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)
		return cx, cy
def Player():
	player_rect = pygame.draw.rect(screen,"white",player)
	# player.y += player_speed
	player.y = vol
	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_height:
		player.bottom = screen_height
	return player_rect
def Enemy(ball_rect):
	enemy_rect = pygame.draw.rect(screen,"white",enemy)
	#enemy.y = ball_rect.y
	# if enemy.top < ball_rect.y:
	# 	enemy.top  += enemy_speed
	# if enemy.bottom > ball_rect.y:
	# 	enemy.bottom -= enemy_speed
	enemy.y = ball_rect.y
	if enemy.bottom >= screen_height:
		enemy.bottom = screen_height
	if enemy.top <= 0:
		enemy.top = 0
	return enemy_rect
class Ball():
	def __init__(self):
		self.ball = pygame.Rect(screen_width/2-10,screen_height/2-10,20,20)
		self.ball_speed_x = ball_speed_x
		self.ball_speed_y = ball_speed_y
		self.score_time = True
		self.player_score = 0
		self.enemy_score = 0
	def draw_ball(self):
		balll = pygame.draw.ellipse(screen,"white",self.ball)
		return balll
	
	def ball_restart(self):
		current_time = pygame.time.get_ticks()
		self.ball.center =(screen_width/2,screen_height/2)
		times =  int(current_time) -int(self.score_time)
		

		if times < 700:
			number_three = basic_font.render("3",False,light_grey)
			number_three_rect = number_three.get_rect(center = (screen_width/2, screen_height/2-30))
			screen.blit(number_three,number_three_rect)
		if 700 < times < 1400:
			number_two = basic_font.render("2",False,light_grey)
			number_two_rect = number_two.get_rect(center = (screen_width/2, screen_height/2-30))
			screen.blit(number_two,number_two_rect)
		if 1400 < times < 2100:
			number_one = basic_font.render("1",False,light_grey)
			number_one_rect = number_one.get_rect(center = (screen_width/2, screen_height/2-30))
			screen.blit(number_one,number_one_rect)

		if  times < 2000:
			ball_speed_x, ball_speed_y = 0,0
		else:
			self.ball_speed_x *= random.choice((1,-1))
			self.ball_speed_y *= random.choice((1,-1))
			self.score_time = 0
			
		
	def ball_animation(self, player_score, enemy_score):
		self.ball.y += self.ball_speed_y
		self.ball.x += self.ball_speed_x
		if self.ball.right >= screen_width:
			self.player_score += 1
			score_sound.play()
			self.score_time = pygame.time.get_ticks()
		if self.ball.left <= 0:
			self.enemy_score += 1
			score_sound.play()
			self.score_time = pygame.time.get_ticks()
		if self.ball.bottom >= screen_height or self.ball.top <= 0:
			self.ball_speed_y *= -1
		
		
	def check_collide_(self, player_rect,enemy_rect):
		if self.ball.colliderect(player_rect) and self.ball_speed_x <0:
			if abs(self.ball.left - player_rect.right) <10:
				self.ball_speed_x *= -1
				sounds.play()
			elif abs(self.ball.top - player_rect.bottom)<10 and self.ball_speed_x <0:
				self.ball_speed_y *= -1
			elif abs(self.ball.bottom - player_rect.top)<10 and self.ball_speed_x>0:
				self.ball_speed_y *= -1
		if self.ball.colliderect(enemy_rect) and self.ball_speed_x >0:
			if abs(self.ball.right - enemy_rect.left) <10:
				self.ball_speed_x *= -1
				sounds.play()
			elif abs(self.ball.top - enemy_rect.bottom)<10 and self.ball_speed_x <0:
				self.ball_speed_y *= -1
			elif abs(self.ball.bottom - enemy_rect.top)<10 and self.ball_speed_x>0:
				self.ball_speed_y *= -1

	def update(self):
		self.draw_ball()
		self.check_collide_(player_rect,enemy_rect)
		self.ball_animation(player_score, enemy_score)
def text_display():
	player_score = test_font.render(f"Player Score: {ball.player_score}", False,"Green")
	enemy_score = test_font.render(f"Computer Score: {ball.enemy_score}", False,"Green")
	enemy_rect = enemy_score.get_rect(top= 50, right = screen_width-50)
	screen.blit(player_score,(50,50))
	screen.blit(enemy_score,enemy_rect)

screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
player = pygame.Rect(0,screen_height/2-40,20,100)
enemy = pygame.Rect(screen_width-20,screen_height/2 - 40, 20,100)
#ball = pygame.Rect(screen_width/2-10,screen_height/2-10,20,20)
bg = pygame.Rect(0,0,screen_width,screen_height)
score_time = None
ball_speed = [4,-4]
ball_speed_x = random.choice(ball_speed)
ball_speed_y = random.choice(ball_speed)
ball = Ball()
player_speed = 0
enemy_speed = 12
player_score = 0
enemy_score = 0
test_font = pygame.font.Font("font/Pixeltype.ttf",20)
basic_font =pygame.font.Font("font/Pixeltype.ttf",30)
sounds = pygame.mixer.Sound("pong.ogg")
sounds.set_volume(0.3)
score_sound = pygame.mixer.Sound("score.ogg")
score_sound.set_volume(0.3)
light_grey = (200,200,200)
while True:
	success, old_img = cap.read()
	img = cv2.flip(old_img, 1)
	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	results = hands.process(imgRGB)
	if findxy():
		cx, cy = findxy()

	else: cy = 0
	vol = np.interp(cy,[100,400], [0,600])
	print(vol)
	cv2.imshow("Image", img)
	if cv2.waitKey(1) == ord("q"):
		break
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				player_speed += 5
				print("keydown")
			if event.key == pygame.K_UP:
				player_speed -= 5
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				player_speed -= 5
				print("keydown")
			if event.key == pygame.K_UP:
				player_speed += 5

	screen.fill("black")

	
	
	#Ball()
	
	ball_rect = ball.draw_ball()
	enemy_rect = Enemy(ball_rect)
	player_rect = Player()
	#ball_speed_x = check_collide(ball_speed_x)
	#
	ball.update()
	if ball.score_time:
		ball.ball_restart()
	text_display()
	pygame.draw.line(screen,"white",(screen_width/2,0),(screen_width/2,screen_height))
	pygame.display.update()
	clock.tick(30)

cv2.destroyAllWindows()