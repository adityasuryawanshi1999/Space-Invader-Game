import pygame
import random
import math
import time
from pygame import mixer
#initialize pygame
pygame.init()

#create window
screen=pygame.display.set_mode((800,600))

#score
score=0
font=pygame.font.Font("freesansbold.ttf",32)

def scorePrint(x,y):
	display=font.render("SCORE:"+str(score),True,(255,255,255))#this renders the string into an image that can be drawn with blit
	screen.blit(display,(x,y))

#sound effects
mixer.music.load("background.wav")
mixer.music.play(-1)

#bullet
bulletImg=pygame.image.load("bullet.png")
bulletX=0
bulletY=480
bulletXchange=0
bulletYchange=3
bulletState="ready"

def fire(x,y):
	global bulletState
	bulletState="fire"
	screen.blit(bulletImg,(x+16,y+10))

#Title and icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

#player
playerImg=pygame.image.load("player2.png")
playerX=370
playerY=480
change=0

def player(x,y):
	screen.blit(playerImg,(x,y)) #blit draws over the screen callec

#enemy
enemyCount=5
enemyImg=[]
enemyX=[]
enemyY=[]
enemyChangeX=[]
enemyChangeY=[]
for i in range(enemyCount):
	enemyImg.append(pygame.image.load("enemy.png"))
	enemyX.append(random.randint(0,736))
	enemyY.append(random.randint(0,150))
	enemyChangeX.append(0.5)
	enemyChangeY.append(0)

def enemy(x,y,i):
	screen.blit(enemyImg[i],(x,y))

#for collision
def isCollision(enemyX,enemyY,bulletX,bulletY):
	distance=math.sqrt((pow(enemyX-bulletX,2))+(pow(enemyY-bulletY,2)))
	if distance<27:
		return True
	else:
		return False


#game loop
running=True
while running:
	screen.fill((0,0,0))
	for event in pygame.event.get():
		if(event.type==pygame.QUIT):
			running=False
		if(event.type==pygame.KEYDOWN):
			if(event.key==pygame.K_LEFT):
				change=-2
			elif(event.key==pygame.K_RIGHT):
				change=2
			elif(event.key==pygame.K_SPACE):
				if(bulletState is "ready"):
					bulletSound=mixer.Sound("laser.wav")
					bulletSound.play()
					bulletX=playerX
					fire(bulletX,bulletY)
		if(event.type==pygame.KEYUP):
			if((event.key==pygame.K_LEFT) or (event.key==pygame.K_RIGHT)):
				change=0

	#player movement 
	playerX+=change
	if(playerX>736):
		playerX=736
	if(playerX<0):
		playerX=0
	#enemy movement and collision detection
	for i in range(enemyCount):
		#collision detection
		collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
		if collision:
			explosionSound=mixer.Sound("explosion.wav")
			explosionSound.play()
			bulletY=480
			bulletState="ready"
			enemyX[i]=random.randint(0,736)
			enemyY[i]=random.randint(0,150)
			score+=1
		#enemy movement
		enemyX[i]+=enemyChangeX[i]
		enemyY[i]+=enemyChangeY[i]
		enemyChangeY[i]=0
		if(enemyX[i]>736):
			enemyX[i]=736
			enemyChangeX[i]=-0.5
			enemyChangeY[i]=50
		if(enemyX[i]<0):
			enemyX[i]=0
			enemyChangeX[i]=0.5
			enemyChangeY[i]=50
		if(enemyY[i]>420): #hereeeee 480 , orignal value(420 works)
			gameOver=font.render("GAME OVER! SCORE:"+str(score),True,(255,255,255))#this renders the string into an image that can be drawn with blit
			screen.blit(gameOver,(220,250))
			pygame.display.update()
			time.sleep(4)
			running=False
		enemy(enemyX[i],enemyY[i],i)
	#bullet movement
	if(bulletY<=0):
		bulletY=480
		bulletState="ready"
	if(bulletState is "fire"):
		bulletY-=bulletYchange
		fire(bulletX,bulletY)

	scorePrint(10,10)
	player(playerX,playerY)
	pygame.display.update()

#if loop exited means screen 1 is destroyed create 2nd screen