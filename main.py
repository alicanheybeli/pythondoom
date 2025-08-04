# Example file showing a basic pygame "game loop"

 
from wad import *
from pyray import *
from doomengine import *


game = Game()

game.Init()

while not game.IsOver():
    game.ProcessInput()
    game.Update()   
    game.Render()
    game.Delay()
close_window()