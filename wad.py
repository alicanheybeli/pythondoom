
from map import *



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

    def Read2Bytes(self,dataindex):
        val = int.from_bytes(self.data[dataindex:dataindex+1],'little')
        return val
    
    def Read4Bytes(self,dataindex):
        val = int.from_bytes(self.data[dataindex:dataindex+3],'little')
        return val
    
    def ReadHeaderData(self,offset):
        header = Header()
        header.wadtype = self.data[offset:offset+4].decode("ascii")
        header.directorycount = self.Read4Bytes(offset+4)
        header.directoryoffset = self.Read4Bytes(offset+8)
        self.header = header

    def ReadDirectoryData(self,offset):
        directory = Directory()
        directory.lumpoffset = self.Read4Bytes(offset)
        directory.lumpsize = self.Read4Bytes(offset + 4)
        directory.lumpname = self.data[offset + 8:offset + 15].decode("ascii")
        return directory

    def ReadVertexData(self,offset):
        vertex = Vertex()
        vertex.xposition = self.Read2Bytes(offset)
        vertex.yposition = self.Read2Bytes(offset + 2)
        return vertex

    def ReadLinedefData(self,offset):
        linedef = Linedef()
        linedef.startvertex = self.Read2Bytes(offset)
        linedef.endvertex = self.Read2Bytes(offset+2)
        linedef.flags = self.Read2Bytes(offset+4)
        linedef.linetype = self.Read2Bytes(offset+6)
        linedef.sectortag = self.Read2Bytes(offset+8)
        linedef.rightsidedef = self.Read2Bytes(offset+10)
        linedef.leftsidedef = self.Read2Bytes(offset+12)
        return linedef
    def FindMapIndex(self,map:Map):
        for i in self.directories:
            if(i.lumpname == map.mapname):
                return i
        return -1

    def ReadDirectories(self):
        self.ReadHeaderData(0)
        print(self.header.wadtype)
        print(self.header.directorycount)
        print(self.header.directoryoffset)
        directory = Directory()
        for i in range(0,self.header.directorycount):
            directory = self.ReadDirectoryData(self.header.directoryoffset + i * 16)
            self.directories.append(directory)
            print([directory.lumpoffset,directory.lumpsize,directory.lumpname],"\n")
