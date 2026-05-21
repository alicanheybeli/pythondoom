from enum import IntEnum
from pyray import *
from things import *
from BSP import * 
from logging import log
from random import randrange
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
    eCOUNT = 11
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
    vertexes:list[Vertex] = []
    linedefs:list[Linedef] = []
    things:list[Thing] = []
    nodes:list[BTreeNode] = []
    segs:list[Seg] = []
    subsectors = []
    xmax = 0
    xmin = 0
    ymax = 0
    ymin = 0
    automapscalefactor = 10
    def __init__(self,mapname:str) -> None:
        self.mapname = mapname
        self.rendertexture = None
        self.currentNodeID = len(self.nodes) - 1  # start at root
        self.nodestack = []

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
    def RenderSubSector(self,subsectorID):
        #self.RenderNode(self.nodes[_NodeID])
        #rl_draw_render_batch_active()
        #swap_screen_buffer()
        #wait_time(1)
        #swap_screen_buffer()
        ssector = self.subsectors[subsectorID]
        for i in self.segs[ssector.firstsegID:(ssector.firstsegID+ssector.segcount+1)]:
            draw_line_ex([self.xtoscreen(self.vertexes[i.startvertexID].x),
                         self.ytoscreen(self.vertexes[i.startvertexID].y)],
                         [self.xtoscreen(self.vertexes[i.endvertexID].x),
                         self.ytoscreen(self.vertexes[i.endvertexID].y)],
                         2,
                         [randrange(0,255,1),randrange(0,255,1),randrange(0,255,1),255])
        rl_draw_render_batch_active()
        swap_screen_buffer()
        #wait_time(0.2)
        swap_screen_buffer()
            
            
        
    def AddSubSector(self,ssector):
        self.subsectors.append(ssector)

    def AddSegs(self,segs):
        self.segs.append(segs)

    def RenderBSPNodes(self, NodeID:int):

        bID = format(NodeID, '016b')
        

        if(NodeID >= 32768):
            self.RenderSubSector(NodeID - 32768)
            return
        
        
        
        self.RenderBSPNodes(self.nodes[NodeID].leftchildID)
        self.RenderBSPNodes(self.nodes[NodeID].rightchildID)
        #isonleftside = self.CheckPointSubSectorSide(Players[1].xPos,Players[1].yPos,NodeID)
        
        #if(isonleftside):
        #    self.RenderBSPNodes(self.nodes[NodeID].leftchildID)
        #    self.RenderBSPNodes(self.nodes[NodeID].rightchildID)
        #else:
        #    self.RenderBSPNodes(self.nodes[NodeID].rightchildID)
        #    self.RenderBSPNodes(self.nodes[NodeID].leftchildID)
            

        
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

        
    #def RenderAutoMap(self):
    #    
    #    clear_background(WHITE)
    #    self.RenderAutoMapPlayer()
    #    self.RenderAutoMapWalls()
    #    #self.RenderAutoMapNodes()
    #    #log("\n\n\n\n\n\n")
    #    #for i in self.nodes:
    #    #    log(i)
    #    #    log("\n")
    #    #log("\n\n\n\n\n\n")
    #    self.RenderBSPNodes(self.nodes.__len__() - 1)
    def RenderAutoMap(self):
        draw_texture_rec(self.rendertexture.texture, 
                     [0, 0, self.rendertexture.texture.width, -self.rendertexture.texture.height],
                     [0, 0], 
                     WHITE)
        self.RenderAutoMapPlayer()  # player still draws every frame

        self.RenderNode(self.nodes[self.currentNodeID])

    def RenderToTexture(self):
        self.rendertexture = load_render_texture(800, 450)
        begin_texture_mode(self.rendertexture)
        clear_background(WHITE)
        self.RenderAutoMapWalls()
        self.RenderBSPNodes(self.nodes.__len__() - 1)
        end_texture_mode()


        
        
    
