from enum import IntEnum
from pyray import *
from things import *
from BSP import * 

SUBSECTORIDENTIFIER = 0
class EMAPLUMPSINDEX(IntEnum):

    eTHINGS = 1
    eLINEDEFS = 2
    eSIDEDDEFS = 3
    eVERTEXES = 4
    eSEAGS = 5
    eSSECTORS = 6
    eNODES = 7
    eSECTORS = 8
    eREJECT = 9
    eBLOCKMAP = 10
    eCOUN = 11
class ELINEDEFFLAGS(IntEnum):

    eBLOCKING      = 0
    eBLOCKMONSTERS = 1
    eTWOSIDED      = 2
    eDONTPEGTOP    = 4
    eDONTPEGBOTTOM = 8
    eSECRET        = 16
    eSOUNDBLOCK    = 32
    eDONTDRAW      = 64
    eDRAW          = 128


class Vertex:
    x = 0
    y = 0
class Linedef:
    startvertex = None
    endvertex = None
    flags = None
    linetype = None
    sectortag = None
    rightsidedef = None
    leftsidedef = None


class Map:


    mapname = None
    vertexes = []
    linedefs = []
    things = []
    nodes = [BTreeNode]
    xmax = 0
    xmin = 0
    ymax = 0
    ymin = 0
    automapscalefactor = 10
    def __init__(self,mapname:str) -> None:
        self.mapname = mapname
    

    def AddVertex(self,vertex:Vertex):
        self.vertexes.append(vertex)
        self.xmax = max(vertex.x,self.xmax)
        self.xmin = min(vertex.x,self.xmin)
        self.ymax = max(vertex.y,self.ymax)
        self.ymin = min(vertex.y,self.ymin)

    def CheckPointSubSectorSide(self,pointX,pointY,nodeID):
        dx = pointX - self.nodes[nodeID].xPartition
        dy = pointY - self.nodes[nodeID].yPartition

        return (((dx * self.nodes[nodeID].changeXPartition) -(dy*self.nodes[nodeID].changeYPartition)) >= 0)
    def RenderBSPNodes(self, NodeID:int):
        def RenderSubSector(_NodeID):
            self.RenderNode(self.nodes[_NodeID])
        #bID = format(NodeID, '016b')
        #
        #if(bID[SUBSECTORIDENTIFIER] == "-"): #I have to do It this because python is fucking dumb
        #    bID = "0" + bID[1:15] 
        #    bID = int(bID,2)
        #    RenderSubSector(0,bID)
        #    return
        if(NodeID >= 32768):
            RenderSubSector(NodeID - 32768)
            return
        
        isonleftside = self.CheckPointSubSectorSide(Players[1].xPos,Players[1].yPos,NodeID)
        if(isonleftside):
            self.RenderBSPNodes(self.nodes[NodeID].leftchildID)
        else:
            self.RenderBSPNodes(self.nodes[NodeID].rightchildID)
            

        
    def AddLinedef(self,linedef):
        self.linedefs.append(linedef)
    
    def AddNode(self,Node):
        self.nodes.append(Node)

    def AddThing(self,thing:Thing):
        if(thing.type == 1):
            Players[1].xPos = thing.xPos
            Players[1].yPos = thing.yPos
            Players[1].angle = thing.angle
        self.things.append(thing)
    def xtoscreen(self,x):
        return int((x - self.xmin) / self.automapscalefactor)
    def ytoscreen(self,y):
        ysize = get_render_height() - 1
        return int(ysize - ((y -self.ymin) / self.automapscalefactor))
    def RenderAutoMapWalls(self):
        
        for linedef in self.linedefs:
            vstart = self.vertexes[linedef.startvertex]
            vend =  self.vertexes[linedef.endvertex] 



            draw_line(self.xtoscreen(vstart.x),
                      self.ytoscreen(vstart.y),
                      self.xtoscreen(vend.x),
                      self.ytoscreen(vend.y),
                      BLACK)
            
    def RenderAutoMapPlayer(self):

        
        draw_circle(self.xtoscreen(Players[1].xPos),
                    self.ytoscreen(Players[1].yPos),
                    5,RED)
    
    def RenderNode(self, node:BTreeNode):
        draw_rectangle_lines_ex([self.xtoscreen(node.rightboxleft),
                             self.ytoscreen(node.rightboxtop),
                             self.xtoscreen(node.rightboxright)- self.xtoscreen(node.rightboxleft)+1,
                             self.ytoscreen(node.rightboxbottom)- self.ytoscreen(node.rightboxtop)+1],
                             3,
                             RED)
        draw_rectangle_lines_ex([self.xtoscreen(node.leftboxleft),
                             self.ytoscreen(node.leftboxtop),
                             self.xtoscreen(node.leftboxright) - self.xtoscreen(node.leftboxleft)+1,
                             self.ytoscreen(node.leftboxbottom) - self.ytoscreen(node.leftboxtop)+1],
                             3,
                             GREEN)
        draw_line(self.xtoscreen(node.xPartition),
                  self.ytoscreen(node.yPartition),
                  self.xtoscreen(node.xPartition+ node.changeXPartition),
                  self.ytoscreen(node.yPartition+node.changeYPartition),
                  BLUE)
    def RenderAutoMapNodes(self):
        for i in self.nodes:
            self.RenderNode(i)

        
    def RenderAutoMap(self):
        
        clear_background(WHITE)
        self.RenderAutoMapPlayer()
        self.RenderAutoMapWalls()
        #self.RenderAutoMapNodes()
        self.RenderBSPNodes(self.nodes.__len__() - 1)



        
        
    
