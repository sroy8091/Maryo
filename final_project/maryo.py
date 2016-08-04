import pygame, random, sys
from pygame.locals import *
pygame.init()

window_height = 750
window_width = 1300

black = (0,0,0)
blue = (0,0,255)
white = (255, 255, 255)

fps = 25
level = 0
addnewflamerate=20

class dragon:
	global fire_rect, image_rect, Canvas
	up = False
	down = True
	velocity = 15
	def __init__(self):
		self.image = pygame.image.load('dragon.png')
		self.image_rect = self.image.get_rect()
		self.image_rect.right = window_width
		self.image_rect.top = window_height/2
	def update(self):
		if (self.image_rect.top < cactus_rect.bottom):
			self.up = False
			self.down = True
		if (self.image_rect.bottom > fire_rect.top):
			self.up = True
			self.down = False
		if (self.down):
			self.image_rect.top+=self.velocity
		if (self.up):
			self.image_rect.top-=self.velocity
		Canvas.blit(self.image, self.image_rect)
	def return_height(self):
		return(self.image_rect.top)

class flames:
	flamespeed = 20
	def __init__(self):
		self.image = pygame.image.load('fireball.png')
		self.height = dragon.return_height()+20
		self.surface = pygame.transform.smoothscale(self.image, (20,20))
		self.image_rect = pygame.Rect(window_width - 106, self.height, 20, 20)
	def update(self):
		self.image_rect.left -= self.flamespeed
	def collision(self):
		if self.image_rect.left == 0:
			return True
		else:
			return False

class maryo:
	global moveup, movedown, gravity, cactus_rect, fire_rect
	speed = 10
	downspeed = 20
	def __init__(self):
		self.image = pygame.image.load('maryo.png')
		self.image_rect = self.image.get_rect()
		self.image_rect.top = window_height/2
		self.image_rect.left = 50
		self.score = 0

	def update(self):
		if (moveup and (self.image_rect.top > cactus_rect.bottom)):
			self.image_rect.top -= self.speed
			self.score += 1
		if (movedown and (self.image_rect.bottom < fire_rect.top)):
			self.image_rect.bottom += self.downspeed
			self.score += 1
		if (gravity and (self.image_rect.bottom < fire_rect.top)):
			self.image_rect.bottom += self.speed

def terminate():
	pygame.quit()
	sys.exit()

def waitforkey():
	while True :
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					terminate()
				return


def flamehitsmario(player_rect, flames):
	for f in flame_list:
		if (player_rect.colliderect(f.image_rect)):
			return True
		return False

def scoreboard(text, font, surface, x, y):
	text_obj = font.render(text, 1, white)
	text_rect = text_obj.get_rect()
	text_rect.topleft = (x,y)
	surface.blit(text_obj, text_rect)

def check_level(score):
	global window_height, level, cactus_rect, fire_rect
	if score in range(0,250):
		fire_rect.top = window_height-50
		cactus_rect.bottom = 50
		level=1
	elif score in range(250, 500):
		fire_rect.top = window_height-100
		cactus_rect.bottom = 100
		level = 2
	elif score in range(500,750):
		fire_rect.top = window_height-150
		cactus_rect.bottom = 150
		level = 3
	elif score in range(750,1000):
		fire_rect.top = window_height-200
		cactus_rect.bottom = 200
		level = 4

mainClock = pygame.time.Clock()
Canvas = pygame.display.set_mode((window_width, window_height), FULLSCREEN)
pygame.display.set_caption('Maryo')

font = pygame.font.SysFont('Arial', 48)
scorefont = pygame.font.SysFont('Arial', 30)
fire_image = pygame.image.load('fire_bricks.png')
fire_rect = fire_image.get_rect()
cactus_image = pygame.image.load('cactus_bricks.png')
cactus_rect = cactus_image.get_rect()
start_image = pygame.image.load('start.png')
start_rect = start_image.get_rect()
start_rect.centerx = window_width/2
start_rect.centery = window_height/2
end_image = pygame.image.load('end.png')
end_rect = end_image.get_rect()
end_rect.centerx = window_width/2
end_rect.centery = window_height/2

pygame.mixer.music.load('mario_theme.wav')
die = pygame.mixer.Sound('mario_dies.wav')

Canvas.blit(start_image, start_rect)
pygame.display.update()

waitforkey()
topscore = 0
dragon = dragon()

while True:

	flame_list = []
	player = maryo()
	moveup = movedown = gravity = False
	flameaddcounter = 0
	die.stop()
	pygame.mixer.music.play(-1, 0.0)

	while True:

		for e in pygame.event.get():
			if e.type==QUIT:
				terminate()
			if e.type==KEYDOWN:
				if e.key==K_UP:
					moveup=True
					movedown=False
					gravity=False
				if e.key==K_DOWN:
					movedown=True
					moveup=False
					gravity=False
			if e.type==KEYUP:
				if e.key==K_UP:
					moveup=False
					gravity=True
				if e.key==K_DOWN:
					movedown=False
					gravity=True

		flameaddcounter+=1
		check_level(player.score)

		if flameaddcounter==addnewflamerate:
			flameaddcounter=0
			newFlame = flames()
			flame_list.append(newFlame)

		for f in flame_list:
			flames.update(f)

		for f in flame_list:
			if (f.image_rect.left<=0):
				flame_list.remove(f)

		player.update()
		dragon.update()

		Canvas.fill(black)
		Canvas.blit(fire_image, fire_rect)
		Canvas.blit(cactus_image, cactus_rect)
		Canvas.blit(player.image, player.image_rect)
		Canvas.blit(dragon.image, dragon.image_rect)

		scoreboard('Score : %s | Top score : %s | Level : %s' %(player.score, topscore, level),scorefont, Canvas, 350, cactus_rect.bottom + 10)

		for f in flame_list:
			Canvas.blit(f.surface, f.image_rect)

		if flamehitsmario(player.image_rect, flame_list):
			if player.score>topscore:
				topscore=player.score
			break
		if ((player.image_rect.top <= cactus_rect.bottom) or (player.image_rect.bottom >= fire_rect.top)):
			if player.score > topscore:
				topscore = player.score
			break

		pygame.display.update()
		mainClock.tick(fps)
	pygame.mixer.music.stop()
	die.play()
	Canvas.blit(end_image, end_rect)
	pygame.display.update()
	waitforkey()