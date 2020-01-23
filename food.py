from tkinter import *
from PIL import ImageTk, Image
import math

SF = 30 #Size of the food

class Point:
	def __init__(self, abscissa, ordinate):
		self.x, self.y = abscissa, ordinate	

class FOOD:
	def __init__(self, screen, a, b):	 
		self.cPoint = Point(a + 15, b + 15) #center Point
		self.screen = screen
		self.food = self.screen.create_rectangle(a, b, a + SF, b + SF, fill = "blue", outline = "white")
	def remove(self):
		self.screen.delete(self.food)
	

class SCORE:
	def __init__(self, default = None):
		self.cnt = StringVar(default, '0')
		self.max = StringVar(default, '0')
		
	def plus(self):
		score = int(self.cnt.get()) + 1
		maxScore = max(score, int(self.max.get()))
		self.cnt.set(str(score))
		self.max.set(str(maxScore))

	def reset(self):
		self.cnt.set('0')

