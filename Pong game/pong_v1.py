import pygame
import random
pygame.init()
screen_width, screen_height = 800, 500

def Player():
	player_rect = pygame.draw.rect(screen,"white",player)
	#player.y = ball_rect.y
	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_height:
		player.bottom = screen_height
	return player_rect
def Enemy(ball_rect):
	enemy_rect = pygame.draw.rect(screen,"white",enemy)
	#enemy.y = ball_rect.y
	if enemy.top < ball_rect.y:
		enemy.top += enemy_speed
	if enemy.bottom > ball_rect.y:
		enemy.bottom -= enemy_speed
	if enemy.bottom >= screen_height:
		enemy.bottom = screen_height
	if enemy.top <= 0:
		enemy.top = 0
	return enemy_rect
def Ball():
	pygame.draw.ellipse(screen,"white",ball)

def check_collide(ball_speed_x):
	if ball.ball.colliderect(player_rect) or ball.ball.colliderect(enemy_rect):
		#ball_rect.x += ball_speed_x
		ball_speed_x *= -1
		
	return ball_speed_x
	
	
			
	
class Ball():
	def __init__(self):
		self.ball = pygame.Rect(screen_width/2-10,screen_height/2-10,20,20)
		#self.ball_speed_x = ball_speed_x
		self.ball_speed_y = ball_speed_y
	def draw_ball(self):
		balll = pygame.draw.ellipse(screen,"white",self.ball)
		return balll
	def ball_animation(self, ball_speed_x):
		#print(self.ball_speed_x)
		
		
		print(self.ball.x)
		self.ball.y += self.ball_speed_y

		if self.ball.right >= screen_width or self.ball.left <= 0:
			self.ball.center =(screen_width/2,screen_height/2)
			ball_speed_x *= random.choice((1,-1))
			self.ball_speed_y *= random.choice((1,-1))
		self.ball.x += ball_speed_x
		#ball_speed_x *= -1
		if self.ball.bottom >= screen_height or self.ball.top <= 0:
			self.ball_speed_y *= -1
	def update(self):
		self.draw_ball()
		self.ball_animation(ball_speed_x)


screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
player = pygame.Rect(0,screen_height/2-40,20,80)
enemy = pygame.Rect(screen_width-20,screen_height/2 - 40, 20,80)
#ball = pygame.Rect(screen_width/2-10,screen_height/2-10,20,20)
bg = pygame.Rect(0,0,screen_width,screen_height)

ball_speed = [4,-4]
ball_speed_x = random.choice(ball_speed)
ball_speed_y = 5
ball = Ball()
player_speed = 0
enemy_speed = 10
while True:
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
	ball.update()
	ball_rect = ball.draw_ball()
	enemy_rect = Enemy(ball_rect)
	player_rect = Player()
	ball_speed_x = check_collide(ball_speed_x)

	pygame.draw.line(screen,"white",(screen_width/2,0),(screen_width/2,screen_height))
	pygame.display.update()
	clock.tick(60)