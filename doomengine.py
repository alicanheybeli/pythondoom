from wad import *
from map import *
from pyray import *


class DoomEngine():

    renderheight = 0
    renderwidth = 0

    isover = False

    wadloader = None
    map = None
    def __init__(self) -> None:
        self.map = Map("E1M1")
    
    def Render(self):
        begin_drawing()
        clear_background(WHITE)
        draw_text("Hello world", 400, 200, 20, VIOLET)
        end_drawing()
    def KeyPressed():
        pass
    def KeyRelease():
        pass
    def Quit():
        pass
    def Update():
        pass
    
    
    def IsOver():
        pass
    def Init(self):
        self.wadloader = WADLoader(self.GetWADFileName())
        self.map = self.wadloader.LoadMapData(self.map)
        return True

    def GetRenderWidth():
        pass
    def GetRenderHeight():
        pass
    def GetTimePerFrame():
        pass

    def GetName():
        pass
    def GetWADFileName(self):
        return "data/DOOM.WAD"
    
class Game:
    windowheight = 0
    windowwidth = 0

    doomengine = None

    def __init__(self) -> None:
        pass
    def ProcessInput(self):
        pass
    def Render(self):
        begin_drawing()
        clear_background(WHITE)
        #draw_text("lol",190,50,12,BLACK)
        self.doomengine.map.RenderAutoMap()
        end_drawing()

    def Update(self):
        pass
    def Delay(self):
        pass
    
    def IsOver(self):
        return window_should_close()
    def Init(self):
        self.doomengine = DoomEngine()
        
        if(not self.doomengine.Init()):
            print("could not initialize engine")
            exit(-1)

        init_window(800, 450, "Hello")    



    