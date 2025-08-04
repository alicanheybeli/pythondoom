
class Player():
    ID = 0
    xPos = 0
    yPos = 0
    angle = 0

    def __init__(self,ID) -> None:
        self.ID = ID    
    def GetId(self):
        return self.ID
    def SetPos(self, x,y):
        self.xPos = x
        self.yPos = y
    def SetAngle(self,angle):
        self.angle = angle

Players = [None,Player(1),Player(2),Player(3),Player(4)]

class Thing():
    xPos = 0
    yPos = 0
    angle = 0
    type = None
    flags = None
