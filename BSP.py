class BTreeNode():
    xPartition = None
    yPartition = None
    changeXPartition = None
    changeYPartition = None

    rightboxtop = None
    rightboxbottom = None
    rightboxleft = None
    rightboxright = None

    leftboxtop = None
    leftboxbottom = None
    leftboxleft = None
    leftboxright = None

    rightchildID = None
    leftchildID = None
class Subsector():
    segcount = None
    firstsegID= None
class Seg():
    startvertexID = None
    endvertexID = None
    angle = None
    linedefID = None
    direction = None
    offset = None