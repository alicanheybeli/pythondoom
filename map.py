from enum import IntEnum


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

class Vertex:
    xposition = 0
    yposition = 0
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
    def __init__(self,mapname:str) -> None:
        self.mapname = mapname
        
    def AddVertex(self,vertex):
        self.vertexes.append(vertex)
        
    def AddLinedef(self,linedef):
        self.linedefs.append(linedef)
        
    
