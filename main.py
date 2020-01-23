'''
Name: NGUYEN THI NGOC TRAM
Gmail: ntngoctram98@gmail.com
'''
from snake import *
from tkinter import *
from time import sleep
import random

game = Tk()
game.title("HAPPY SNAKE GAME")

SnakeGame = GAME(game)
SnakeGame.grid(column=1, row=0, rowspan=3)
game.bind("<Key>", SnakeGame.redirect)
	
menuBar = Menu(game)
game.config(menu=menuBar)
fileMenu = Menu(menuBar)

fileMenu.add_command(label="Play", command=SnakeGame.play)
fileMenu.add_command(label="Stop", command=SnakeGame.Stop)
fileMenu.add_command(label="Exit", command=game.destroy)#.quit
menuBar.add_cascade(label="File", menu=fileMenu)

In4Menu = Menu(menuBar, tearoff=0)  
In4Menu.add_separator()  
In4Menu.add_command(label="Click", command = SnakeGame.In4)  

menuBar.add_cascade(label="Help", menu=None) 
menuBar.add_cascade(label="Information", menu=In4Menu) 

scoreboard = Frame(game, width=500, height=10)
Label(scoreboard, text='Game Score:').grid()
Label(scoreboard, textvariable=SnakeGame.score.cnt).grid()

Label(scoreboard, text='High Score:').grid()
Label(scoreboard, textvariable=SnakeGame.score.max).grid()
scoreboard.grid(column=0, row=2)
  
game.mainloop()


