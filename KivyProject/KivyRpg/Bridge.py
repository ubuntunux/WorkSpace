from copy import copy
from xml.etree.ElementTree import Element, dump, parse, SubElement, ElementTree
import math, sys

import Utility as Util
from Utility import *

from Globals import *
from ResourceMgr import gResMgr
from ObjectBase import Gate, City, Road

#---------------------#
# Global Variable
#---------------------#
bridge_size = W * 0.03

#---------------------#
# Global Instance
#---------------------#
def setGlobalInstance(WorldEdit):
  global gWorldEdit
  gWorldEdit = WorldEdit.instance()

#---------------------#
# class : Bridge
#---------------------#
class Bridge(Singleton, Widget):
  bridgeMap = {}
  gateMap = {}
  pathMap = {}
  generatePathList = set()
  
  def __init__(self):
    Widget.__init__(self, size=WH)
    self.bridgeMap = {} # ex)bridgeMap[id1] = {id2:[gate1ID, gate2ID], ...}
    self.gateMap = {} # ex)gateMap[gate1id] = [gate2id, (obj1ID, obj2ID)]
    self.pathMap = {} # ex)pathMap[id1] = {targetID:nextObjID, ...}
    self.generatePathList = set()
    self.bridge_texture = gResMgr.getTex("bridge")
    self.bridge_texture.wrap =  "repeat"
  
  def load(self, parentTree):
    self.generatePathList = set()
   
    if parentTree != None:
      # load bridgeMap
      xml_tree = parentTree.find("Bridge")
      if xml_tree != None:
        self.bridgeMap = eval(xml_tree.get("data") or "{}")
        for id1 in self.bridgeMap.keys():
          _toList = self.bridgeMap[id1]
          # generate gateMap
          for id2 in _toList:
            gate1ID, gate2ID = _toList[id2]
            self.gateMap[gate1ID] = [gate2ID, (id1, id2)]
      # load pathMap
      xml_tree = parentTree.find("PathMap")
      if xml_tree != None:
        gMyRoot.increaseProgress()
        self.pathMap = eval(xml_tree.get("data") or "{}")
        
  def save(self, parentTree, counter):
    # save bridge
    xml_data = SubElement(parentTree, "Bridge")
    counter.value += 1
    if self.bridgeMap:
      xml_data.set("data", str(self.bridgeMap) or {})
    
    # save pathMap
    xml_data = SubElement(parentTree, "PathMap")
    counter.value += 1
    if self.pathMap:
      xml_data.set("data", str(self.pathMap) or {})
    
  def remove(self):
    # clear
    self.generatePathList = []
    self.canvas.clear()
    for child in self.canvas.children:
      self.canvas.remove(child)
    
    self.bridgeMap = {}   
    # detach self
    if self.parent:
      self.parent.remove_widget(self)
      
  def update(self):
    if self.generatePathList:
      job = gMyRoot.newJob("Generate Path")
      job.addJob(self.doGeneratePathList)
  
  def draw(self):
    gWorldEdit.gameScreen.add_to_bg(self)
  
  def drawLine(self, pos1, pos2):
    # set texture
    vDir = sub(pos1, pos2)
    dist = getDist(vDir)
    ratio = dist / bridge_size
    tex = self.bridge_texture.get_region(0, 0, self.bridge_texture.size[0], self.bridge_texture.size[1] * ratio)
    
    # make bridge
    bridge = Scatter(size=(bridge_size, getDist(pos1, pos2)))
    bridge.do_translation = False
    bridge.do_rotation = False
    bridge.do_scale = False
    bridge.auto_bring_to_front = False
    bridge.rotation = atan2(-vDir[0], vDir[1]) * gRadian2Degree
    bridge.center = mul(add(pos1, pos2), 0.5)
    with bridge.canvas:
      Rectangle(texture=tex, size=bridge.size)
    self.add_widget(bridge)
    
  def refreshGatePos(self, obj1, _ignoreGateIDList=None):
    _roadObjList = set()
    _ignoreGateIDList = _ignoreGateIDList or set()
    # recalculate gate pos function
    def recalcGatePos(gateID1, obj1, obj2):
     gate1 = gWorldEdit.getObj(gateID1)
     if gate1 and gateID1 not in _ignoreGateIDList:
       # recalculate gate1 pos
       self.calcGatePos(gate1, obj1, obj2)
       # add generate path level
       if gate1.parentObj.hasPath():
         self.generatePathList.add(gate1.parentObj)
       # recalc Road Obj pos
       if isinstance(gate1.parentObj, Road) and isinstance(obj1, City) and isinstance(obj2, City):
         self.calcGatePos(gate1.parentObj, obj1, obj2)
         _ignoreGateIDList.add(gateID1)
         _roadObjList.add(gate1.parentObj)
    # do recalculate gate pos    
    id1 = obj1.getID() 
    if id1 in self.bridgeMap:
      for id2 in self.bridgeMap[id1]:
        obj2 = gWorldEdit.getObj(id2)
        gateID1, gateID2 = self.bridgeMap[id1][id2]
        if obj1 and obj2:
          recalcGatePos(gateID1, obj1, obj2)
          recalcGatePos(gateID2, obj2, obj1)
    # road object refresh gate pos
    for roadObj in _roadObjList:
      self.refreshGatePos(roadObj, _ignoreGateIDList)
        
  def drawBridge(self):
    # clear drawn bridge
    self.clear_widgets()
    
    # make draw bridge list
    redrawObjIDList = [obj.getID() for obj in gWorldEdit.getCurrentLevel().get_childObj()]
    # start draw linked bridges
    while redrawObjIDList:
      id1 = redrawObjIDList.pop()
      if id1 in self.bridgeMap:
        # check linked obj2 with obj1
        for id2 in self.bridgeMap[id1]:
          obj1 = gWorldEdit.getObj(id1)
          obj2 = gWorldEdit.getObj(id2)
          if obj1 and obj2:
            if id2 in redrawObjIDList:
              # draw bridge line
              self.drawLine(obj1.center, obj2.center)
        # end of For statement
    # end of draw linked bridges
    
    # draw single path bridge
    for obj in gWorldEdit.getCurrentLevel().get_childObj():
      if isinstance(obj, Gate):
        self.drawLine(obj.center, add(obj.center, sub(obj.center, cXY)) )
      # direction of Road obj
      # draw single bridge when gate in childObj has City type parentOfGate.
      elif isinstance(obj, Road):
        for child in obj.get_childObj():
          if child.getID() in self.gateMap:
            gateData = self.gateMap[child.getID()]
            parentOfGateID = gateData[1][0] if len(gateData)>1 else -1
            parentOfGate = gWorldEdit.getObj( parentOfGateID )
            if isinstance(parentOfGate, City):
              self.drawLine(obj.center, add(obj.center, sub(obj.center, cXY)))
               
  def getParentOfGate(self, gate):
    if gate.getID() in self.gateMap:
      linkedObjs = self.gateMap[gate.getID()][1]
      parentOfGate = linkedObjs[0]
      return gWorldEdit.getObj(parentOfGate)
    return None
    
  def getLinkedGate(self, gate):
    if gate.getID() in self.gateMap:
      otherGateID = self.gateMap[gate.getID()][0]
      return gWorldEdit.getObj(otherGateID)
    return None
  
  def getLinkedObjWithGate(self, gateObj):
    gateID = gateObj.getID()
    if gateID in self.gateMap:
      linkedObjs = self.gateMap[gateID][1]
      obj2ID = linkedObjs[1]
      return gWorldEdit.getObj(obj2ID)
    return None
    
  def hasBridge(self, obj):
    return obj and (obj.getID() in self.bridgeMap)
                      
  def isLinked(self, obj1, obj2):
    if obj1 and obj2 and obj1 is not obj2:
      id1 = obj1.getID()
      id2 = obj2.getID()
      if id1 in self.bridgeMap and id2 in self.bridgeMap and \
        id1 in self.bridgeMap[id2] and id2 in self.bridgeMap[id1]:
        return True
    return False
    
  def breakLink(self, obj1):
    if obj1:
      id1 = obj1.getID()
      if id1 in self.bridgeMap:
        linkedIDList = copy(self.bridgeMap[id1])
        for id2 in linkedIDList:
          self.removeBridge(obj1, gWorldEdit.getObj(id2))
  
  def recalcGatePos(self, gate):
    if gate:
      obj1 = self.getParentOfGate(gate)
      obj2 = self.getLinkedObjWithGate(gate)
      self.calcGatePos(gate, obj1, obj2)
      
  def calcGatePos(self, gate, obj1, obj2):
    wRatio = 0.4
    hRatio = 0.3
    offset = (1.0, 0.9)
    if gate and obj1 and obj2:
      vDir = normalize(sub(obj2.center, obj1.center))
      if vDir[1] == 0.0 or abs(vDir[0]/vDir[1]) > (W*wRatio)/(H*hRatio):
        # left or right direction
        if vDir[0] != 0.0:
          vDir = mul(vDir, abs(W * wRatio / vDir[0]))
      else:
        # top or bottom.direction
        if vDir[1] != 0.0:
          vDir = mul(vDir, abs(H * hRatio / vDir[1]))
      gate.setPos(sub(add(mul(cXY, offset), vDir), mul(gate.size, 0.5)))
      # do rotation
      if isinstance(gate, Gate):
        gate.setRotation(math.atan2(-vDir[0], vDir[1]) * gRadian2Degree)
  
  def linkToCloseObj(self, obj):
    # find closed object
    if obj and obj.parentObj:
      minDist = 99999.0
      findObj = None
      for child in obj.parentObj.get_childObj():
        if not child.enableBridge() or obj == child:
          continue
        dist = getDist(obj.getPos(), child.getPos())
        if dist < minDist:
          findObj = child
          minDist = dist
      # add a bridge
      if findObj and not self.isLinked(obj, findObj):
        self.addBridge(obj, findObj)
            
  def addBridge(self, obj1, obj2):
    if obj1 and obj2 and obj1 is not obj2:
      def addGate(obj1, obj2):
        id1 = obj1.getID()
        id2 = obj2.getID()
        
        gate = None
        gateID = -1
        road = None
        
        if isinstance(obj1, City):
          # first, add road and add gate
          road = obj1.add_childObj("Road")
          self.calcGatePos(road, obj1, obj2)
          gate = road.add_childObj("Gate")
        else:
          # add new gate
          gate = obj1.add_childObj("Gate")
          
        if gate:
          gateID = gate.getID()
          gate.setName(obj2.getTitle())
          self.calcGatePos(gate, obj1, obj2)
        return road, gate, gateID
        
      # create gates
      road1, gate1, gate1ID = addGate(obj1, obj2)
      road2, gate2, gate2ID = addGate(obj2, obj1)
      
      # if parent of gate is road, rename gate.
      if road1 and road2:
        gate1.setName("\n".join([obj2.getTitle(), road2.getTitle(), ""]))
        gate2.setName("\n".join([obj1.getTitle(), road1.getTitle(), ""]))
      
      # add new bridge item - { id2:[gate1id, gate2id],... }
      id1 = obj1.getID()
      id2 = obj2.getID()
      
      # bridgeMap
      if id1 in self.bridgeMap:
        self.bridgeMap[id1][id2] = [gate1ID, gate2ID]
      else:
        self.bridgeMap[id1] = { id2:[gate1ID, gate2ID] }
        
      if id2 in self.bridgeMap:
        self.bridgeMap[id2][id1] = [gate2ID, gate1ID]
      else:
        self.bridgeMap[id2] = { id1:[gate2ID, gate1ID] }
        
      # gateMap
      self.gateMap[gate1ID] = [gate2ID, (id1, id2)] #if not isinstance(obj2, Gate) else obj2.getID()
      self.gateMap[gate2ID] = [gate1ID, (id2, id1)] #if not isinstance(obj1, Gate) else obj1.getID()
         
      # add line
      if gWorldEdit.getCurrentLevel() == obj1.parentObj:
        self.drawLine(obj1.center, obj2.center)
      
      self.generatePathList.add(obj1)
      self.generatePathList.add(obj2)
      self.generatePathList.add(obj1.parentObj)
      self.generatePathList.add(obj2.parentObj)
      
      # link to close obj
      for obj in [road1, road2, gate1, gate2]:
        obj and self.linkToCloseObj(obj)
        
  def removeBridge(self, obj1, obj2):
    if obj1 and obj2 and obj1 is not obj2:
      if self.isLinked(obj1, obj2):
        id1 = obj1.getID()
        id2 = obj2.getID()
        # remove gate and pop bridge
        def removeGate_popBridge(id1, id2):
          # remove gate
          if id1 in self.bridgeMap and id2 in self.bridgeMap[id1]:
            gate1ID = self.bridgeMap[id1].pop(id2)[0]
            gate1 = gWorldEdit.getObj(gate1ID)
            if gate1:
              # pop gate id from gateMap
              if gate1ID in self.gateMap:
                self.gateMap.pop( gate1ID )
             
              # if parent of gate is Road, remove Road
              # remove gate and road
              if isinstance(gate1.parentObj, Road):
                obj1 = gWorldEdit.getObj(id1)
                obj2 = gWorldEdit.getObj(id2)
                # if Road made by City, remove road
                if isinstance(obj1, City) and isinstance(obj2, City):
                  gate1.parentObj.remove()
                else:
                  # remove gate
                  gate1.remove()
              else:
                # remove only gate
                gate1.remove()
              
          # pop empty map item
          if id1 in self.bridgeMap and not self.bridgeMap[id1]:
            self.bridgeMap.pop(id1)
        # do it...
        removeGate_popBridge(id1, id2)
        removeGate_popBridge(id2, id1)
        # add generate path list
        self.generatePathList.add(obj1)
        self.generatePathList.add(obj2)
        self.generatePathList.add(obj1.parentObj)
        self.generatePathList.add(obj2.parentObj)
      # redraw bridge
      self.drawBridge()
      
  # Bridge method
  def checkBridge(self, obj1, obj2):
    if obj1 and obj2 and obj1 is not obj2 and obj1.enableBridge() and obj2.enableBridge():
      if self.isLinked(obj1, obj2):
        self.removeBridge(obj1, obj2)
      else:
        self.addBridge(obj1, obj2)
      
  def doGeneratePathList(self):
    for obj in self.generatePathList:
      self.generatePath(obj)
    self.generatePathList = set()
     
  # generate shortest path
  def generatePath(self, parentObj, bLog = False):
    if not parentObj.hasPath():
      return
    parentObj.log("generatePatth")
    # initialize, clear children of current level
    for obj in parentObj.get_childObj():
      objID = obj.getID()
      self.pathMap[objID] = {}
    #log("child %s" % (str([i.getID() for i in parentObj.get_childObj()])))
    # build shortest path map to the target
    for obj in parentObj.get_childObj():
      objID = obj.getID()
      for targetObj in parentObj.get_childObj():
        targetID = targetObj.getID()
        # check same obj
        if objID == targetID or targetID in self.pathMap[objID]:
          continue
          
        bLog and log(">> Start %d => %d" % (objID, targetID))
        pMinDist = Pointer(99999.0)
        pResult = Pointer([])
        self.buildPath(bLog, pResult, objID, targetID, objID, pMinDist, 0.0, [])
        bLog and log(pResult.get())
        
        # result - optimized code. generate all path by one path
        # ex) [1,2,3] generate 1->2=2, 1->3=2, 2->1=1, 2->3=3, 3->1=2, 3->2=2
        result = pResult.get()
        for i, startID in enumerate(result[:-1:]):
          for j, targetID in enumerate(result[i+1::]):
            if startID != targetID:
              self.pathMap[startID][targetID] = result[i+1]
              self.pathMap[targetID][startID] = result[j+i]
              bLog and log("%d->%d=%d, %d->%d=%d" % (startID, targetID, result[i+1], targetID, startID, result[j+i]))
        bLog and log("-"*40)
            
  # find shortest path 
  def buildPath(self, bLog, pResult, startObjID, targetID, curObjID, pMinDist, accDist, searchIDList):
    # start and target is same.
    if startObjID == targetID:
      bLog and log("start same target : %d" % startObjID)
      #linkInfo.targetDist = 0.0
      #linkInfo.nextObjID = targetID
      return
      
    # get current check Obj
    curObj = gWorldEdit.getObj(curObjID)
    if curObj == None:
      return
      
    # insert curObjID into the checked list
    searchIDList.append(curObjID)

    # continue check...
    linkIDs = self.bridgeMap[curObjID].keys() if curObjID in self.bridgeMap else []
    
    # check target is neighborhood of startObj?
    if startObjID == curObjID and targetID in linkIDs:
      targetObj = gWorldEdit.getObj(targetID)
      curDist = getDist(curObj.pos, targetObj.pos)
      pResult.set(searchIDList + [targetID])
      bLog and log(">> Find %d->%d cur:%d dist:%d path:%s" % (startObjID, targetID, curObjID, curDist, str(pResult.get())))
    else:
      # find path loop
      for linkID in linkIDs:
        # check infinite loop
        if linkID in searchIDList:
          continue
        # start find shortest path
        linkObj = gWorldEdit.getObj(linkID)
        if linkObj:
          curDist = accDist + getDist(curObj.pos, linkObj.pos)
          # find the target!!!
          if linkID == targetID:
            # check shortest dist
            #bLog and log("checkDist: pMinDist:%d curDist:%d path:%s" % (linkInfo.targetDist, dist, str(searchIDList+[linkID])))
            if curDist < pMinDist.get():
              pMinDist.set(curDist)
              pResult.set(searchIDList + [linkID])
              bLog and log(">> Find %d->%d cur:%d dist:%d path:%s" % (startObjID, targetID, curObjID, curDist, str(pResult.get())))
            else:
              # this is not best path.
              break
          # not found target, check continue...
          else:
            self.buildPath(bLog, pResult, startObjID, targetID, linkID, pMinDist, curDist, searchIDList)
    # pop from.checked list
    searchIDList.remove(curObjID)
  
  # get nextobj for reach to target
  def getNextObj(self, curObj, targetObj):
    if curObj and targetObj and curObj is not targetObj:
      curObjID = curObj.getID()
      targetObjID = targetObj.getID()
      # check is in pathMap
      if curObjID in self.pathMap and targetObjID in self.pathMap[curObjID]:
        return gWorldEdit.getObj(self.pathMap[curObjID][targetObjID])
    return None
      
  # return shortest path obj list
  def getPath(self, startObj, targetObj):
    if startObj and targetObj and startObj is not targetObj:
      startObjID = startObj.getID()
      targetID = targetObj.getID()
      # path generator
      def pathGenerator(curObjID, targetID):
        while curObjID in self.pathMap and targetID in self.pathMap[curObjID]:
          nextObjID = self.pathMap[curObjID][targetID]
          curObjID = nextObjID
          yield nextObjID
      # return pathMap
      return [i for i in pathGenerator(startObjID, targetID)]
    return []
