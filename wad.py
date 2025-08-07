
from logging import *
from BSP import *
from map import *

LOL = None

class Header:
    wadtype = None
    directorycount = 0
    directoryoffset = 0

class Directory:
    lumpoffset = 0
    lumpsize = 0
    lumpname = None

class WADLoader:
    
    header = None
    filename:str = None
    filestream = None
    data = None
    directories:list[Directory] = []

    def __init__(self, filepath:str):
        self.filestream = open(filepath,"rb")
        self.filename = self.filestream.name
        self.data = bytearray(self.filestream.read())
        self.ReadDirectories()

    def Read2Bytes_UShort(self,dataindex):
        val = int.from_bytes(self.data[dataindex:dataindex+2],'little')
        
        
        return val
    
    def Read4Bytes_Uint(self,dataindex):
        val = int.from_bytes(self.data[dataindex:dataindex+4],'little')
        return val
    
    def Read2Bytes_SShort(self,dataindex):
        val = int.from_bytes(self.data[dataindex:dataindex+2],'little',signed=True)
        
        
        return val
    
    def Read4Bytes_Sint(self,dataindex):
        val = int.from_bytes(self.data[dataindex:dataindex+4],'little',signed=True)
        return val
    
    def ReadHeaderData(self,offset):
        header = Header()
        header.wadtype = self.data[offset:offset+4].decode("ascii")
        header.directorycount = self.Read4Bytes_Uint(offset+4)
        header.directoryoffset = self.Read4Bytes_Uint(offset+8)
        self.header = header

    def ReadDirectoryData(self,offset):
        directory = Directory()
        directory.lumpoffset = self.Read4Bytes_Uint(offset)
        directory.lumpsize = self.Read4Bytes_Uint(offset + 4)
        directory.lumpname = self.data[offset + 8:offset + 16].replace(b'\x00',b'').decode("ascii")
        
        return directory

    def ReadVertexData(self,offset):
        vertex = Vertex()
        vertex.x = self.Read2Bytes_SShort(offset)
        vertex.y = self.Read2Bytes_SShort(offset + 2)
        return vertex
    def ReadNodesData(self,offset):
        node = BTreeNode()
        
        node.xPartition = self.Read2Bytes_SShort(offset)
        node.yPartition = self.Read2Bytes_SShort(offset+2)
        node.changeXPartition = self.Read2Bytes_SShort(offset+4)
        node.changeYPartition = self.Read2Bytes_SShort(offset+6)

        node.rightboxtop = self.Read2Bytes_SShort(offset+8)
        node.rightboxbottom = self.Read2Bytes_SShort(offset+10)
        node.rightboxleft = self.Read2Bytes_SShort(offset+12)
        node.rightboxright = self.Read2Bytes_SShort(offset+14)

        node.leftboxtop = self.Read2Bytes_SShort(offset+16)
        node.leftboxbottom = self.Read2Bytes_SShort(offset+18)
        node.leftboxleft = self.Read2Bytes_SShort(offset+20)
        node.leftboxright = self.Read2Bytes_SShort(offset+22)
        
        node.rightchildID = self.Read2Bytes_UShort(offset+24)
        node.leftchildID = self.Read2Bytes_UShort(offset+26)

        return node
    def ReadThingData(self,offset):
        thing = Thing()
        thing.xPos = self.Read2Bytes_SShort(offset)
        thing.yPos = self.Read2Bytes_SShort(offset+2)
        thing.angle = self.Read2Bytes_UShort(offset+4)
        thing.type = self.Read2Bytes_UShort(offset+6)
        thing.flags = self.Read2Bytes_UShort(offset+8)
        return thing

    
    def ReadLinedefData(self,offset):
        linedef = Linedef()
        linedef.startvertex = self.Read2Bytes_UShort(offset)
        linedef.endvertex = self.Read2Bytes_UShort(offset+2)
        linedef.flags = self.Read2Bytes_UShort(offset+4)
        linedef.linetype = self.Read2Bytes_UShort(offset+6)
        linedef.sectortag = self.Read2Bytes_UShort(offset+8)
        linedef.rightsidedef = self.Read2Bytes_UShort(offset+10)
        linedef.leftsidedef = self.Read2Bytes_UShort(offset+12)
        return linedef
    def FindMapIndex(self,map:Map):
        for i in range(0,len(self.directories)):
            if(self.directories[i].lumpname == map.mapname):
                return i
        return -1
    
    
    def ReadMapVertex(self,map:Map) -> Map:
        mapindex = self.FindMapIndex(map)
        if(mapindex == -1):
            return False
        mapindex += EMAPLUMPSINDEX.eVERTEXES
        if(self.directories[mapindex].lumpname != "VERTEXES"):
            return False
        vertexsize = 4 # short x,y;
        vertexcount = int(self.directories[mapindex].lumpsize / vertexsize)
        
        
        for i in range(0,vertexcount):
            vertex = self.ReadVertexData(self.directories[mapindex].lumpoffset + i * vertexsize )
            map.AddVertex(vertex)

            log('(',vertex.x ,',', vertex.y , ')\n')
        
        return map
    def ReadMapLinedef(self,map:Map) -> Map:
        mapindex = self.FindMapIndex(map)
        if(mapindex == -1):
            return False
        mapindex += EMAPLUMPSINDEX.eLINEDEFS
        if(self.directories[mapindex].lumpname != "LINEDEFS"):
            return False
        linedefsize = 14 
        linedefcount = self.directories[mapindex].lumpsize / linedefsize
        
        
        for i in range(0,int(linedefcount)):
            linedef = self.ReadLinedefData(self.directories[mapindex].lumpoffset + i * linedefsize)
            map.AddLinedef(linedef)

            #log(linedef.xposition , " " , linedef.yposition , "\n")
        
        return map


    def LoadMapData(self,map:Map)->map:
        
        map = self.ReadMapVertex(map)
        if(not map):
           log("Error: Failed to load map vertex data for MAP: " + map.mapname)
           return False
        
        map = self.ReadMapLinedef(map)
        if(not map):
           log("Error: Failed to load map linedef data for MAP: " + map.mapname)
           return False
        
        map = self.ReadMapThings(map)
        if(not map):
           log("Error: Failed to load map things data for MAP: " + map.mapname)
           return False
        map = self.ReadMapNodes(map)
        if(not map):
           log("Error: Failed to load map nodes data for MAP: " + map.mapname)
           return False
        return map

    def ReadDirectories(self):
        self.ReadHeaderData(0)
        log(self.header.wadtype)
        log(self.header.directorycount)
        log(self.header.directoryoffset)
        directory = Directory()
        for i in range(0,self.header.directorycount):
            directory = self.ReadDirectoryData(self.header.directoryoffset + i * 16)
            self.directories.append(directory)
            log([directory.lumpoffset,directory.lumpsize,directory.lumpname],"\n")
    
    
    def ReadMapThings(self,map:Map):
        mapindex = self.FindMapIndex(map)
        if (mapindex == -1):
            return False
        mapindex = mapindex + EMAPLUMPSINDEX.eTHINGS
        if(self.directories[mapindex].lumpname != "THINGS"):
            return False
        thingsize = 10
        thingscount = self.directories[mapindex].lumpsize / thingsize
                
        for i in range(0,int(thingscount)):
            thing = self.ReadThingData(self.directories[mapindex].lumpoffset + i * thingsize)
            map.AddThing(thing)
            log(vars(thing))
            log("\n")
        return map
        
    def ReadMapNodes(self,map:Map) -> Map:
        mapindex = self.FindMapIndex(map)
        if(mapindex == -1):
            return False
        mapindex += EMAPLUMPSINDEX.eNODES
        if(self.directories[mapindex].lumpname != "NODES"):
            return False
        nodesize = 28
        nodecount = self.directories[mapindex].lumpsize / nodesize
        
        
        for i in range(0,int(nodecount)):
            node = self.ReadNodesData(self.directories[mapindex].lumpoffset + i * nodesize)
            map.AddNode(node)
            log(vars(node))
            log("\n")
            #log(linedef.xposition , " " , linedef.yposition , "\n")
        
        return map