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
        self.map.RenderToTexture() 
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
        node = self.doomengine.map.nodes[self.doomengine.map.currentNodeID]

        if is_key_pressed(KeyboardKey.KEY_LEFT):
            if node.rightchildID < 32768:  # not a leaf
                self.doomengine.map.nodestack.append(self.doomengine.map.currentNodeID)
                self.doomengine.map.currentNodeID = node.rightchildID
            self.doomengine.map.nodestack.append(self.doomengine.map.currentNodeID)
            self.doomengine.map.currentNodeID = node.rightchildID & 0x7FFF

        if is_key_pressed(KeyboardKey.KEY_RIGHT):
            if node.leftchildID < 32768:
                self.doomengine.map.nodestack.append(self.doomengine.map.currentNodeID)
                self.doomengine.map.currentNodeID = node.leftchildID
            self.doomengine.map.nodestack.append(self.doomengine.map.currentNodeID)
            self.doomengine.map.currentNodeID = node.leftchildID & 0x7FFF

        if is_key_pressed(KeyboardKey.KEY_UP):
            if self.doomengine.map.nodestack:
                self.doomengine.map.currentNodeID = self.doomengine.map.nodestack.pop()
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
        init_window(800, 450, "Hello")
        self.doomengine.Init()

    