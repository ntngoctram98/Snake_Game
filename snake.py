from tkinter import *
from PIL import ImageTk, Image
import math
from time import sleep
from food import *
import random


SN = 40 #Size of face snake
SB = 20 #Size of 1 block of body snake
CB1 = SN - SB
CB = CB1/2
SF = 30
#when snake changes direction: 8 case. ------ because the size of Face Snake != sz of Blocks of Snake

				#(x_FaceSnake > x_BodySnake)                     								#y_FaceSnake > y_BodySnake
DIRECTIONS_FACE = {'Up':[[-CB, -SN + CB], [CB, -SN + CB]], 'Down':[[-CB, SN - CB], [CB, SN - CB]], 'Left':[[-SN + CB, -CB], [-SN + CB, CB]], 'Right': [[SN - CB, -CB ], [SN - CB, CB]]}
DIRECTIONS_BODY = {'Up':[[SB, 0],[-SB, 0]], 'Down':[[SB, 0 ],[-SB, 0]], 'Left': [[0, -SB], [0, SB]], 'Right':[[0, -SB], [0, SB]]} 

#4 case for straight move 
DIRECTIONS_Straight = {'Up':[0, -SB], 'Down':[0, SB], 'Left':[-SB, 0], 'Right':[SB, 0]} 
AXES = {'Up': 'Vertical', 'Down':'Vertical', 'Right':'Horizontal', 'Left':'Horizontal'} #, 'space': None
WAIT = 0.1

class GAME(Canvas):
	def __init__(self, default = None):
		#Read Image
		normal_img = Image.open("Photos/nomalFace.png")
		#Resize Image
		self.img = ImageTk.PhotoImage(normal_img.resize((SN, SN), Image.ANTIALIAS)) 

		super().__init__(default)
		self.configure(width = 500, height = 500, bg = "cyan")
		#screen = Canvas(width = 500, height = 500, background = "cyan")
		# white black red green blue cyan yellow magenta 
		self.run = 0
		self.snake = None
		self.food = None	
		self.direction = None
		self.cur = None
		self.score = SCORE(default)

	#Start game: Snake runs to the right
	def play(self):
		self.delete("all") 
		if self.run == 0:			
			self.snake = SNAKE(self, 150, 420, self.img)
			self.food = FOOD(self, random.randint(50,450), random.randint(50,450))
			self.direction = 'Right'
			self.cur = Movement(self, 'Right')
			self.cur.begin() #only move straight
			self.run = 1
	
	def redirect(self, event):
		if event.keysym in AXES.keys() and self.run == 1 and AXES[event.keysym] != AXES[self.direction]:
			self.cur.flag = 0 #Mark change keypress
			self.direction = event.keysym
			self.cur = Movement(self, event.keysym)
			self.cur.change_direction() #switch direction and move straight untill switch direction again
		
	def Stop(self):
		self.snake.delete_Snake()
		self.run = 0
		self.cur.stop()
		self.score.reset()
		self.food.remove()
		self.delete("all")

	def In4(self):
		self.delete("all")
		self.create_text(250, 250, text = "MAKE BY Bé TRÂM. A HUY HUY", fill = "blue", font = ("Times", 20))
		

class Movement:
	def __init__(self, game, direction):
		self.flag = 1
		self.game = game
		self.direction = direction

	def begin(self):
		if self.flag > 0:
			self.game.snake.move_straight(self.direction)
			self.game.after(100, self.begin)
	
	def change_direction(self):
		self.game.snake.move(self.direction)
		self.game.snake.move_straight(self.direction)
		self.game.after(100, self.begin)

	def stop(self):
		self.flag = 0


class BODY_SNAKE:
	def __init__(self, canvas, a, b):
		self.screen = canvas
		self.x, self.y = a, b
		self.bodyS = self.screen.create_oval(a, b, a + SB, b + SB, fill = "orange", outline = "orange")

	def remove(self):
		self.screen.delete(self.bodyS)

	def reset_Body0(self, a, b):
		self.x, self.y = a, b
		self.screen.coords(self.bodyS, a, b, a + SB, b + SB, fill = "orange", outline = "orange")
		

class SNAKE:
	def __init__(self, game, abscissa, ordinate, img):	 
	#(abscissa, ordinate): coordinate of TOP LEFT point img face Snake
		self.screen = game
		self.x, self.y = abscissa, ordinate	
		self.img = img	 
		self.faceS = self.screen.create_image(self.x, self.y, anchor = NW, image = img)
		self.mainS = [0, 0, 0]
		self.xC, self.yC = self.x + SN/2, self.y + SN/2 #coordinate of center point
		for i in range (3):
			self.mainS[i] = BODY_SNAKE(self.screen, self.x - SB - SB*i, self.y + (SN - SB)/2)

	#Check Snake eat food?
	def checkEat(self, food):
		xF = food.cPoint.x 
		yF = food.cPoint.y
		d = math.sqrt(math.pow(self.xC - xF, 2) + math.pow(self.yC - yF, 2))		
		if (d < SN - SB): 
			return True
		else:
			return False

	#If face Snake touch block in Body or touch edges => Lose
	def snakeDie(self):
		#touch edges
		if self.x > 480 or self.y > 480 or self.x < -10 or self.y < -10:	
			return True
		#touch blocks 
		for i in range(len(self.mainS)):
			xC_B, yC_B = self.mainS[i].x + SB/2, self.mainS[i].y + SB/2
			d_S2B = math.sqrt(math.pow(self.xC - xC_B, 2) + math.pow(self.yC - yC_B, 2))	
			if d_S2B < (SN + SB)*0.5 - 10:
				return True
		
		return False

	def move_straight(self, direction):
		#create a new face Snake and delete old face Snake 
		self.x += DIRECTIONS_Straight[direction][0]
		self.y += DIRECTIONS_Straight[direction][1]
		self.xC, self.yC = self.x + SN/2, self.y + SN/2
		self.screen.delete(self.faceS)
		self.faceS = self.screen.create_image(self.x, self.y, anchor = NW, image = self.img)
		#create a first block: mainS[0]
		a = self.mainS[0].x + DIRECTIONS_Straight[direction][0]
		b = self.mainS[0].y + DIRECTIONS_Straight[direction][1]
		bodyN = BODY_SNAKE(self.screen, a, b)
		tmp = [bodyN]
		self.mainS = tmp + self.mainS
		
		#Snake don't eat food
		if self.checkEat(self.screen.food) == False: 
			self.mainS[-1].remove()	
			self.mainS.remove(self.mainS[-1])
		else:
			self.screen.score.plus()
			self.screen.food.remove()
			self.screen.food = FOOD(self.screen, random.randint(50,450), random.randint(50,450))
		
		#End Game
		if self.snakeDie() == True:
			self.screen.Stop()
		
		sleep(WAIT)
		self.screen.update()

	def move(self, direction):
		def moveFnB(i, j):
			self.x += (DIRECTIONS_FACE[direction][i])[0]
			self.y += (DIRECTIONS_FACE[direction][i])[1]
			self.xC, self.yC = self.x + SN/2, self.y + SN/2

			self.screen.delete(self.faceS)
			self.faceS = self.screen.create_image(self.x, self.y, anchor = NW, image = self.img)
			
			a = self.mainS[0].x + (DIRECTIONS_BODY[direction][j])[0]
			b = self.mainS[0].y + (DIRECTIONS_BODY[direction][j])[1]
			bodyN = BODY_SNAKE(self.screen, a, b)
			tmp = [bodyN]
			self.mainS = tmp + self.mainS

			if self.checkEat(self.screen.food) == False: #Snake don't eat food
				self.mainS[-1].remove()	
				self.mainS.remove(self.mainS[-1])
			else:
				self.screen.score.plus()
				self.screen.food.remove()
				self.screen.food = FOOD(self.screen, random.randint(50,450), random.randint(50,450))
			#End game		
			if self.snakeDie() == True:
				self.screen.Stop()

		if (AXES[direction] == 'Vertical' and self.x > self.mainS[0].x): 
			moveFnB(0,0)
		elif (AXES[direction] == 'Horizontal' and self.y > self.mainS[0].y):
			moveFnB(0,1)
		elif (AXES[direction] == 'Horizontal' and self.y < self.mainS[0].y):  
			moveFnB(1,0)		
		elif (AXES[direction] == 'Vertical' and self.x < self.mainS[0].x):
			moveFnB(1,1)

		sleep(WAIT)
		self.screen.update()
			
	def delete_Snake(self):
		self.screen.delete(self.faceS)
		for i in range(len(self.mainS)):
			self.mainS[i].remove()
				
