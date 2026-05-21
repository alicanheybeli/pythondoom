# Example file showing a basic pygame "game loop"

 
from wad import *
from pyray import *
from doomengine import *

game = Game()

game.Init()

while not game.IsOver():
    set_target_fps(120)
    game.ProcessInput()
    game.Update()   
    game.Render()
    game.Delay()
close_window()