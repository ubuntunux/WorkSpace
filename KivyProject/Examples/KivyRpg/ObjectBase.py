from copy import copy
from xml.etree.ElementTree import Element, dump, parse, SubElement, ElementTree
import threading

import Utility as Util
from Utility import *
from kivy.animation import Animation
from ResourceMgr import gResMgr
import ObjectTransform
from Globals import *

#---------------------#
# Global Variable
#---------------------#
icon_size = WRect(0.1)

#---------------------#
# Global Instance
#---------------------#
def setGlobalInstance(WorldEdit, Bridge):
  global gWorldEdit
  global gBridge
  global gPlayer
  gWorldEdit = WorldEdit.instance()
  gBridge = Bridge.instance()
  gPlayer = Player.instance()
  ObjectTransform.setGlobalInstance(WorldEdit, Bridge, Player)
  
#---------------------#
# class : ObjectBase
#---------------------#
class BaseObject(Scatter, ObjectTransform.ObjectTransform, StateMachine):
  ID = -1
  xml_data = None
  namelistFile = ""
  namelist = []
  name = "No name"
  nameColor = [1,1,1,1]
  namePosHint = 0.35
  icon = ""
  body = None
  label = None
  bUniqueName = True
  bDrawTypeName = True
  parentObj = None
  childTypes = []
  childObj = []
  
  bHasDoor = False
  bFreeMoveType = False
  bEnterPoint = False # one of entry point on player enter the level
  bHasPath = False
  
  # editmode properties
  pTouch = None
  bTouchMoved = False
  nTouchPriority = 255
  touchRect = [1,1]
  touchRectHints = [1.0, 1.0]
  bCreatable = True
  bMovable = True
  bDeletable = True
  bEnableBridge = False
  bRedrawBridge = False
  bDrawAlways = False
  pDrawOnObj = None

  def __init__(self):
    # class method - load name library
    self.loadNamelist()
    
    # state machine init
    StateMachine.__init__(self)

    # init scatter
    Scatter.__init__(self, size=icon_size)
    self.setPos(cXY)
    self.do_translation = False
    self.do_rotation = False
    self.do_scale = False
    self.auto_bring_to_front = False
    
    # set box region
    self.body = Scatter(size=self.size, pos=(0,0))
    self.body.do_translation = False
    self.body.do_rotation = False
    self.body.do_scale = False
    self.body.auto_bring_to_front = False
    with self.body.canvas:
      self.boxColor = Color(0.7,0.7,1.0,0.0)
      Rectangle(size=self.size)
      self.objColor = Color(1,1,1)
      self.box = Rectangle(size=self.size)
    self.add_widget(self.body)
    
    # set touch rect
    self.touchRect = mul(mul(sub(self.touchRectHints, 1.0), self.size[:2]), 0.5)
    
    # attach name label
    self.label = Label(text=self.name, center=mul(self.size, (0.5, 1.0)))
    self.label.color = self.nameColor
    self.label.pos[1] += self.size[1] * self.namePosHint
    self.add_widget(self.label)
      
  def setPos(self, pos):
    self.pos = copy(pos)
    self.curPos = copy(pos)
    
  def getPos(self): return self.pos
  def getCurPos(self): return self.curPos
  def getTouchPriority(self): return self.nTouchPriority
  def setMovable(self, bMovable): self.bMovable = bMovable
  def isMove(self): return self.bMove
  def isJump(self): return self.bJump
  def hasPath(self): return self.bHasPath
  def enableBridge(self): return self.bEnableBridge
  
  def getType(self):
    return self.__class__.__name__
    
  def log(self, *args):
    text = [str(i) for i in args] + [str(self.getID())]
    text = " ".join(text)
    log(text)
    
  # reset data  
  def reset(self, parentObj, xml_data):
    if self == parentObj:
      return
    #init data
    self.xml_data = xml_data
    self.parentObj = parentObj
    self.childObj = []
    self.pTouch = None
    self.bTouchMoved = False
    self.bRedrawBridge = False
    self.bMove = False
    self.bJump = False
    self.fJump = 0.0
    self.vStartPos = [0,0]
    self.vTargetPos = [0,0]
    self.pTargetObj = None
    self.nTargetObjID = -1
    self.pOldTargetObj = None
    self.nOldTargetObjID = -1
    self.pPathList = []
    self.pStartFromObj = None
    self.nStartFromObjID = -1
    self.pCurArriveObj = None
    self.nCurArriveObjID = -1
    self.pDrawOnObj = None
    self.vMoveDir = [0,0]
    self.fMoveTime = 0.0
    self.fMoveTimeAcc = 0.0
    
    # set icon
    if self.icon:
      self.box.texture = gResMgr.getTex(self.icon)
        
    # create new data
    if xml_data == None:
      self.setNewName(self)
      self.setID(-1)
      self.setPos(cXY)
      # add door
      if self.bHasDoor:
        door = self.add_childObj("Door")
        door.center = mul(WH, (0.5, 0.15))
        door.setPos(door.pos)
    # adjust loading data
    else:
      self.setID(int(xml_data.get("id")))
      self.setName(xml_data.get("name"))
      # adjust screen ratio
      self.setPos(mul(eval(xml_data.get("pos")), (gWorldEdit.widthRatio, gWorldEdit.heightRatio)))
      self.setRotation(eval(xml_data.get("rotation")))
      
    # set floor pos
    self.fFloorPos = self.getCurPos()[1]
    # add to worldedit
    if self.bDrawAlways:
      gWorldEdit.addDrawAlwaysObj(self)
    # regist object
    gWorldEdit.registObjID(self)
  
  def remove(self):
    if not self.bDeletable and gWorldEdit.getCurrentLevel() == self.parentObj:
      return False
    # deleted log
    #log(" ".join(["Removed", self.getType(), ":", self.getTitle()]))
      
    # recursive
    childObj = copy(self.childObj)
    for child in childObj:
      child.remove()
    
    # movement stop 
    self.stop()
    
    # maybe.. I have gate. cause try to break link
    if gBridge.hasBridge(self):
      gBridge.breakLink(self)
      
    # pop my widget from parent 
    if self.parent:
      self.parent.remove_widget(self)
      
    # pop self from parent
    if self.parentObj:
      self.parentObj.pop_childObj(self)  
    self.parentObj = None
    
    # unregist
    gWorldEdit.unregistObjID(self)
    gWorldEdit.removeDrawAlwaysObj(self)
    gWorldEdit.removeDrawObj(self)
    return True
    
  @classmethod
  def loadNamelist(cls):
    if cls.namelistFile and not cls.namelist:
      filepath = os.path.join("data", cls.namelistFile)
      if os.path.isfile(filepath):
        f = open(filepath, "r")
        cls.namelist = map(lambda x:x.strip(), list(f))
        f.close()    
  
  @classmethod
  def setNewName(cls, obj):
    if cls.namelist and len(cls.namelist) > 0:
      name = random.choice(cls.namelist).strip()
      obj.setName(name)
    else:
      # set default name
      obj.setName(cls.name)
  
  @classmethod
  def checkName(cls, objName):
    '''if is there name then remove..'''
    if cls.bUniqueName and objName in cls.namelist:
      cls.namelist.remove(objName)
      
  def setName(self, name):
    self.name = name
    self.label.text = self.getTitle()
    self.checkName(self.name)
    
  def getName(self):
    return self.name
  
  def getNameWithID(self):
    return self.name + "[" + str(self.ID) + "]"
  
  def getTitle(self):
    if self.bDrawTypeName:
      return self.name + " " + self.__class__.__name__
    else:
      return self.name
  
  def getID(self):
    return self.ID 
    
  def setID(self, ID):
    self.ID = ID
    
  # Display ID 
  def showID(self, bShow):
    # toggle id label
    if bShow:
      self.label.text = "ID : " + str(self.ID) + "\n" + self.getTitle()
    else:
      self.label.text = self.getTitle()
  
  # show recursive parent obj name
  def showLocation(self):
    locate = ["%s(%d)" % (self.name, self.getID())]
    parentObj = self.parentObj
    while parentObj:
      locate.insert(0, parentObj.name.replace("\n", " "))
      parentObj = parentObj.parentObj
    log(", ".join(locate))
    
  def draw(self):
    # pop.from.old.parent
    if self.parent != None:
      self.parent.remove_widget(self)
    # calc pos
    self.pDrawOnObj = None
    if self.bDrawAlways:
      # draw to current position
      if self.parentObj == gWorldEdit.getCurrentLevel():
        self.pos = copy(self.curPos)
      # draw to parent position
      elif self.parentObj != None:
        prevParentObj = self.parentObj
        parentObj = self.parentObj.parentObj
        while parentObj:
          if gWorldEdit.getCurrentLevel() == parentObj:
            self.pos = prevParentObj.getCurPos()
            self.pDrawOnObj = prevParentObj
            break
          prevParentObj = parentObj
          parentObj = parentObj.parentObj
        else:
          # currentLevel not matched parent level, cause do not draw.
          return
    # add to parent
    gWorldEdit.gameScreen.add_to_bg(self)
    gWorldEdit.addDrawObj(self)
    # show id
    self.showID(gWorldEdit.isEditMode)
  
  # override
  def load_extend(self, xml_data):
    pass
      
  def load(self, currentTree):
    # load data
    if currentTree != None:   
      # loading progress
      gMyRoot.increaseProgress()
      for childType in self.childTypes:
        xml_tree = currentTree.findall(childType)
        if xml_tree != None:
          for xml_data in xml_tree:
            # child obj load xml data
            child = self.add_childObj(childType, xml_data)
            child.load_extend(xml_data)
            child.load(xml_data)
  
  def postLoadProcess(self):
    # clear xml data
    self.xml_data = None
  
  def save(self, parentTree, counter):
    counter.value += 1
    className = self.__class__.__name__
    if parentTree == None:
      xml_data = Element(className)
    else:
      xml_data = SubElement(parentTree, className)
    xml_data.set("id", str(self.getID()))
    xml_data.set("name", self.name)
    xml_data.set("pos", str(self.getCurPos()))
    xml_data.set("rotation", str(self.getRotation()))
    # override method
    self.save_extend(xml_data)
    
    # recursive
    for child in self.childObj:
      child.save(xml_data, counter)
    return xml_data
  
  # override
  def save_extend(self, xml_data):
    pass
    
  def append_childObj(self, childObj):
    self.childObj.append(childObj)
  
  # load and reset child object 
  def add_childObj(self, childType, xml_data = None):
    if childType in self.childTypes:
      childClass = eval(childType)
      child = None
      # check singleton - cannot add, but just only modify
      if hasattr(childClass, "instance"):
        # pop from parent
        child = childClass.instance()
        if child.parentObj:
          child.parentObj.pop_childObj(child)
        
        if child.getID() == -1:
          # when loaded...
          child.reset(self, xml_data)
        else:
          # set new parent
          child.set_parentObj(self)
      else:
        # add new child object or loaded
        child = childClass()
        child.reset(self, xml_data)
      self.append_childObj(child)
      
      # becareful, when loading dont attach obj.
      if not gWorldEdit.bLoading and gWorldEdit.getCurrentLevel() == self:
        child.draw()
      return child
  
  # clear    
  def clear(self):
    childObj = copy(self.childObj)
    for child in childObj:
      child.remove()
  
  # recursive check, is in parent list
  def isInParentList(self, obj):
    parentObj = self.parentObj
    while obj and parentObj:
      if obj == parentObj:
        return True
      parentObj = parentObj.parentObj
    return False
  
  # recursive check, is in child list
  def isInChildList(self, obj):
    for child in self.childObj:
      if child == obj:
        return True
      elif child.isInChildList(obj):
        return True
    return False
      
  def getChildTypes(self):
    return self.childTypes
  
  def get_childObj(self):
    return self.childObj
    
  def pop_childObj(self, obj):
    obj.parentObj = None
    if obj in self.childObj:
      # pop obj from childObj
      self.childObj.remove(obj)
    # pop from parent widget
    if obj.parent:
      obj.parent.remove_widget(obj)
    
  def draw_childObj(self):
    for child in self.childObj:
      child.draw()
  
  def get_parentObj(self):
    return self.parentObj
  
  def set_parentObj(self, parentObj):
    self.parentObj = parentObj
    
  def change_parentObj(self, newParentObj):
    if newParentObj != None and newParentObj != self.parentObj and \
      self.getType() in newParentObj.getChildTypes():
        if self.parentObj:
          self.parentObj.pop_childObj(self)
        self.set_parentObj(newParentObj)
        newParentObj.append_childObj(self)
        # set real position ( curPos )
        self.setPos(self.getPos())
        # draw
        if self.bDrawAlways or gWorldEdit.getCurrentLevel() == newParentObj:
          self.draw()
    
  def findGate(self, vMoveDir):
    #log("find gate")
    vMoveDir = normalize(mul(vMoveDir, (0.8,0.6)))
    #find best gate....
    maxDot = -1.0
    gateObj = None
    for child in self.childObj:
      if child.bEnterPoint:
        vDir = sub(mul(cXY, (1.0, 0.95)), child.center)
        vDir = normalize(vDir)
        curDot = dot(vDir, vMoveDir)
        if curDot > maxDot:
          maxDot = curDot
          gateObj = child
          #log(gateObj.getName() + " " + str(curDot))
    return gateObj
    
  # on enter or exit to other level
  def exitLevel(self, depth = 0):
    if depth == 0:
      for child in self.childObj:
        child.exitLevel(depth+1)
    self.pDrawOnObj = None
  
  def showPopup(self, *args):
    gWorldEdit.popupMenu.showPopup(self)
    
  def isTouched(self):
    return self.pTouch != None
    
  def check_touched(self, touchPos):
    vDiff = sub(touchPos, self.pos)
    if vDiff[0] >= -self.touchRect[0] and vDiff[1] >= -self.touchRect[1]\
     and vDiff[0] < (self.size[0] + self.touchRect[0]) and vDiff[1] < (self.size[1] + self.touchRect[1]):
      return True
    return False
   
  def touch_down(self, touch):
    self.pTouch = touch
    self.bTouchMoved = False
    # touch flag - check touch something? by gWorldEdit
    touch.bTouched = True

    # set selected color
    self.boxColor.a = 0.3
    
    # check edit
    if gWorldEdit.isEditMode:  
      self.bRedrawBridge = False
      # set schedule.prolerty popup
      self.setPopup(True)
      # double tap - enter the level
      if touch.is_double_tap:
        gWorldEdit.setCurrentLevel(self)
    
    # set select obj
    gWorldEdit.selectObj(self)
      
  def touch_move(self, touch):
    if gWorldEdit.isEditMode and self.pTouch == touch:
      # show property popup
      self.setPopup(False)
      
      if self.bMovable:
        self.bTouchMoved = True
        self.pos = add(self.pos, touch.dpos)
        self.curPos = self.pos
        self.bRedrawBridge = True
      
  def touch_up(self, touch):
    if self.isTouched():
      #log("touch up : " + str(self.getID()))
      self.pTouch = None
      self.boxColor.a = 0.0
      # unschedule prolerty popup
      self.setPopup(False)
      # edit mode
      if gWorldEdit.isEditMode and self.bMovable and self.bTouchMoved:
        # set pos
        self.bTouchMoved = False
         
        # snap character object
        if isinstance(self, Character):
          obj = gWorldEdit.findNearestObj(self)
          if obj:
            self.setPos(obj.getPos())
            self.setArriveObj(obj)
            self.clearPathList()
            
        # redraw bridge
        if self.bRedrawBridge:
          if gBridge.hasBridge(self):
            # redraw bridge and recalculate gate pos 
            job = gMyRoot.newJob("Generate Path")
            job.addJob(gBridge.refreshGatePos, args=(self,))
            job.addJob(gBridge.drawBridge)
            job.addJob(gBridge.doGeneratePathList)
            # regenerate path by moving...
            if self.parentObj.hasPath():
              job.addJob(gBridge.generatePath, args=(self.parentObj,))
          self.bRedrawBridge = False
        
  # set or unset showpopup schedule         
  def setPopup(self, bSet):
    if bSet:
      Clock.schedule_once(self.showPopup, 0.3)
    else:
      Clock.unschedule(self.showPopup)
 
  def checkInRegion(self):
    x, y = self.getPos()
    if x < W * 0.2:
      x = W * 0.2
    elif x + self.size[0] > W * 0.8:
      x = W * 0.8 - self.size[0]
    if y < H * 0.2:
      y = H * 0.2
    elif y + self.size[1] > H * 0.8:
      y = H * 0.8 - self.size[1]
    self.pos = (x,y)
    
  # update
  def update(self, dt):
    if self.bMove or self.bJump:
      self.updateMove(dt)
        
#---------------------#
# class : World
#---------------------#
class World(BaseObject, Singleton):
  childTypes = ["City", "Player"]
  name = "Kivy"
    
#---------------------#
# class : City
#---------------------#
class City(BaseObject):
  namelistFile = "city_names.txt"
  nameColor = [0.7,0.5,0.3,1]
  childTypes = ["Dungeon", "Town", "Road", "Gate", "Player"]
  icon = "city"
  bEnableBridge = True

#---------------------#
# class : Gate
#---------------------#
class Gate(BaseObject):
  icon = "arrow"
  name = "Gate"
  nameColor = [0.9,0.9,0.5,1]
  bDrawTypeName = False
  bEnableBridge = True
  bCreatable = False
  bMovable = False
  bDeletable = False
  bEnterPoint = True
  
#---------------------#
# class : Point
#---------------------#
class Point(BaseObject):
  icon = "point"
  name = ""
  bEnableBridge = True
  bDrawTypeName = False
  
#---------------------#
# class : Door
#---------------------#
class Door(BaseObject):
  icon = "point"
  name = ""
  bCreatable = False
  bDeletable = False
  bEnterPoint = True
  
#---------------------#
# class : Road
#---------------------#
class Road(BaseObject):
  namelistFile = "city_names.txt"
  nameColor = [0.8,0.8,1,1]
  childTypes = ["Building", "Gate", "Point", "Monster", "Npc", "Player"]
  icon = "road"
  bHasPath = True
  bCreatable = False
  bMovable = False
  bDeletable = False
  bFreeMoveType = False
  bEnableBridge = True
  
  def postLoadProcess(self):
    # clear xml data
    BaseObject.postLoadProcess(self)
  
#---------------------#
# class : Dungeon
#---------------------#
class Dungeon(BaseObject):
  namelistFile = "city_names.txt"
  nameColor = [0.4,0.4,0.4,1]
  childTypes = ["Gate", "Point", "Monster", "Npc", "Player"]
  icon = "dungeon"
  bHasPath = True
  bEnableBridge = True
  bFreeMoveType = False
  
#---------------------#
# class : Town
#---------------------#
class Town(BaseObject):
  namelistFile = "city_names.txt"
  nameColor = [1,0.85,0.6,1]
  childTypes = ["Building", "Point", "Gate", "Npc", "Monster", "Player"]
  icon = "town"
  bHasPath = True
  bEnableBridge = True
  bFreeMoveType = False
  
#---------------------#
# class : Building
#---------------------#
class Building(BaseObject):
  namelistFile = "building_names.txt"
  nameColor = [0.8,0.8,1.0,1]
  bUniqueName = False
  childTypes = ["Door", "Npc", "Monster", "Player"]
  icon = "building"
  bEnableBridge = True
  bDrawTypeName = False
  bHasDoor = True
  bFreeMoveType = True

#---------------------#
# class : Character
#---------------------#
class Character(BaseObject):
  bDrawTypeName = False
  namePosHint = 0.12
  nTouchPriority = 1
  touchRectHints = [2.0, 2.0]

#---------------------#
# class : Monster
#---------------------#
class Monster(Character):
  namelistFile = "monster_names.txt"
  icon = "monster"
  
#---------------------#
# class : Npc
#---------------------#
class Npc(Character):
  namelistFile = "npc_names.txt"
  icon = "npc"
 
#---------------------#
# class : Player ( Singleton )
#---------------------#
class Player(Character, Singleton):
  name = "Player"
  icon = "npc"
  bDrawAlways = True
  
  def load_extend(self, xml_data):
    if xml_data != None:
      transformData = xml_data.find("transformData")
      for data in transformData or []:
        value = eval(data.get("value"))
        if value != None:
          setattr(self, data.tag, value)
      
      # adjust screen size
      self.vStartPos = mul(self.vStartPos, (gWorldEdit.widthRatio, gWorldEdit.heightRatio))
      self.vTargetPos = mul(self.vTargetPos, (gWorldEdit.widthRatio, gWorldEdit.heightRatio))
      self.vMoveDir = normalize(mul(self.vMoveDir, (gWorldEdit.widthRatio, gWorldEdit.heightRatio)))
      self.fFloorPos *= gWorldEdit.heightRatio 
      
  def postLoadProcess(self):
    if self.xml_data != None:
      # load object data
      objectData = self.xml_data.find("objectData")
      for data in objectData or []:
        obj = gWorldEdit.getObj(int(data.get("value") or "-1"))
        setattr(self, data.tag, obj)     
    # clear xml data
    BaseObject.postLoadProcess(self)
  
  def save_extend(self, xml_data):
    if xml_data != None:
      # save objectData
      objectData = SubElement(xml_data, "objectData")
      saveEntry = ["pCurArriveObj", "pStartFromObj", "pTargetObj", "pOldTargetObj"]
      for entry in saveEntry:
        data = SubElement(objectData, entry)
        obj = getattr(self, entry)
        data.set("value", str(obj.getID() if obj else -1))
      
      # save transform data
      saveData = SubElement(xml_data, "transformData")
      saveEntry = ["bJump", "fJump", "bMove", "vStartPos", "vTargetPos",\
        "pPathList", "vMoveDir", "fMoveTime", "fMoveTimeAcc", "fFloorPos"]
      for entry in saveEntry:
        data = SubElement(saveData, entry)
        data.set("value", str(getattr(self, entry)))
        