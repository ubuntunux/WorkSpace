import Utility as Util
from Utility import *
import ObjectBase
from Globals import *

#---------------------#
# Global Instance
#---------------------#
def setGlobalInstance(WorldEdit, Bridge, Player):
  global gWorldEdit
  global gBridge
  global gPlayer
  gWorldEdit = WorldEdit.instance()
  gBridge = Bridge.instance()
  gPlayer = Player.instance()

#---------------------#
# class : ObjectTransform
#---------------------#
class ObjectTransform:
  # transform method
  curPos = None # real position, pos is relative position
  bJump = False
  fJump = False
  bMove = False
  vStartPos = (0,0)
  vTargetPos = (0,0)
  pTargetObj = None
  pOldTargetObj = None
  pStartFromObj = None
  pCurArriveObj = None
  pPathList = []
  vMoveDir = (0,0)
  fMoveTime = 0.0
  fMoveTimeAcc = 0.0
  fFloorPos = 0.0
  
  # move method 
  def updateMove(self, dt):
    pos = self.getPos()
    # move
    if self.bMove:
      pos = add(pos, mul(self.vMoveDir, gWalk * dt))
      self.fMoveTimeAcc += dt
      if self.fMoveTimeAcc >= self.fMoveTime:
        self.bMove = False
        self.fMoveTime = 0.0
        self.fMoveTimeAcc = 0.0
        if self.bJump:
          pos = (self.vTargetPos[0], pos[1])
        else:
          pos = copy(self.vTargetPos)
      ratio = self.fMoveTimeAcc / self.fMoveTime if self.fMoveTime > 0.0 else 1.0
      ratio = min(1.0, max(0.0, ratio))
      self.fFloorPos = self.vStartPos[1] * (1.0-ratio) + self.vTargetPos[1]*ratio
      self.setJump()
      
    # jump
    if self.bJump:
      self.fJump -= gGravity * dt
      pos = add(pos, (0.0, self.fJump * dt))
      if self.fJump <= 0.0 and self.getPos()[1] <= self.fFloorPos:
        pos = (pos[0], self.fFloorPos)
        self.bJump = False
        
    # set position
    self.setPos(pos)
    
    # check arrived to the target - 
    if not self.bMove and (not self.bJump or self.hasPathList()):
      self.arrivedAt()
  
  def getRotation(self):
    return self.body.rotation

  def setRotation(self, degree):
    self.body.rotation = degree
      
  def getTargetObj(self):
    return self.pTargetObj
    
  def hasPathList(self):
    return len(self.pPathList) > 0
    
  def clearPathList(self):
    self.pPathList = []
    
  def setArriveObj(self, arriveObj):
    self.pCurArriveObj = arriveObj
    self.pTargetObj = None
    self.pStartFromObj = None
    self.stop()
     
  def arrivedAt(self):
    # check move end
    if self == gPlayer:
      if self.pTargetObj != None and not self.hasPathList():
        # arrived at city - this is only for animation..
        if isinstance(self.pTargetObj, ObjectBase.City):
          linkedGate = gBridge.getLinkedGate(self.pStartFromObj)
          if linkedGate:
            # maybe arrivedObj is Road Object
            arrivedObj = linkedGate.parentObj
            if arrivedObj:
              gWorldEdit.setCurrentLevel(arrivedObj)
              self.change_parentObj(arrivedObj)
              # set pos at outside
              vDir = normalize(sub(linkedGate.getPos(), cXY))
              self.setPos(add(linkedGate.getPos(), mul(vDir, gOutsideDist)))
              self.pCurArriveObj = None
              self.pStartFromObj = None
              self.move(linkedGate.getPos(), linkedGate)
              # it's not arrived.. return
              return
        # up to level
        elif isinstance(self.pTargetObj, ObjectBase.Door):
          gWorldEdit.upToTheLevel()
        # move to the parent of linked gate
        elif isinstance(self.pTargetObj, ObjectBase.Gate):
          if self.pStartFromObj:
            # move to the outside of gate direction
            self.move_to_gateDir(self.pTargetObj)
            # it's not arrived.. return
            return
          else:
            # arrive from outside
            pass
        # enter the level - check player can enter the level
        elif self.getType() in self.pTargetObj.getChildTypes():
          # change parent
          self.change_parentObj(self.pTargetObj)
          gWorldEdit.setCurrentLevel(self.pTargetObj)
          # find gate by close angle
          self.pTargetObj = self.pTargetObj.findGate(self.vMoveDir)
          if self.pTargetObj:
            self.setPos(self.pTargetObj.getPos())
      elif self.pTargetObj == None and isinstance(self.pStartFromObj, ObjectBase.Gate):
        self.move_to_ParentOfLinkedGate(self.pStartFromObj)
        # it's not arrived.. return
        return
      # end of check arrive
    # end of check gPlayer
    self.setArriveObj(self.pTargetObj)
    
    # move continue...
    if self.hasPathList():
      targetObj = gWorldEdit.getObj(self.pPathList.pop(0))
      if targetObj:
        self.move(targetObj.getPos(), targetObj)
  
  def setJump(self, force = gJump):
    if not self.bJump:
      self.bJump = True
      self.fJump = force
      if not self.bMove:
        self.fFloorPos = self.getPos()[1]
  
  def move(self, targetPos, targetObj = None):
    self.pOldTargetObj = self.pTargetObj
    self.pTargetObj = targetObj
    dist = getDist(targetPos, self.pos)
    # check, can move?
    if dist > 0.001:
      self.bMove = True
      self.fMoveTime = dist / gWalk
      self.fMoveTimeAcc = 0.0
      self.pStartFromObj = self.pStartFromObj or self.pDrawOnObj or self.pCurArriveObj
      self.vStartPos = copy(self.getPos())
      self.vTargetPos = copy(targetPos)
      self.pCurArriveObj = None
      self.vMoveDir = normalize(sub(targetPos, self.pos))
      # set parent the current level
      self.change_parentObj(gWorldEdit.getCurrentLevel())
    else:
      self.arrivedAt()
   
  def move_to(self, targetObj):
    if targetObj in (self, None):
      return
    
    # move to current arrive at object
    if targetObj == self.pDrawOnObj or targetObj == self.pCurArriveObj:
      # up to the level
      if isinstance(targetObj, ObjectBase.Door):
        gWorldEdit.upToTheLevel()
      # move to the outside of gate direction
      elif isinstance(targetObj, ObjectBase.Gate):
        self.move_to_gateDir(targetObj)
      # enter the level
      elif targetObj:
        gWorldEdit.setCurrentLevel(targetObj)
    # move to the target
    else:
      startObj = self.pStartFromObj or self.pDrawOnObj or self.pCurArriveObj
      if startObj:
        self.pPathList = gBridge.getPath(startObj, targetObj)
        if self.pPathList:
          # case : when moving touch other target..
          if self.pStartFromObj and self.pTargetObj.getID() != self.pPathList[0]:
            if self.pOldTargetObj == targetObj:
              # when moving, go back to the OldTargetObj...
              self.pPathList = [targetObj.getID()]
            else:
              # when moving, touch other target exclude pStartFromObj and pTargetObj
              self.pPathList.insert(0, self.pStartFromObj.getID())     
          # case : general case, player stop and touch target
          targetObj = gWorldEdit.getObj(self.pPathList.pop(0))
        # when moving go back to the startObj
        elif startObj == targetObj:
          targetObj = self.pStartFromObj
        else:
          #log("cannot move")
          return
      # case : when moving.. touch same target. that's startObj is none..
      elif not gWorldEdit.getCurrentLevel().bFreeMoveType:
        return
      # case : when moving touch door
      else:
        pass
      # move to lower position of target, little offset
      self.move(targetObj.getPos(), targetObj)
  
  # move to outside of gate direction
  def move_to_gateDir(self, pTargetGate):
    self.pStartFromObj = pTargetGate
    vDir = normalize(sub(pTargetGate.getPos(), cXY))
    self.move(add(pTargetGate.getPos(), mul(vDir, gOutsideDist)), None)
    
  # move to parent of linked gate
  def move_to_ParentOfLinkedGate(self, pTargetGate):
    linkedGate = gBridge.getLinkedGate(pTargetGate)    
    # move to the linkedGate
    bShowMoveAnimation = False
    if linkedGate and not bShowMoveAnimation:
      # immediately move
      # change parent and move to the targetPos
      self.change_parentObj(linkedGate.parentObj)
      gWorldEdit.setCurrentLevel(linkedGate.parentObj)
      # set pos at outside
      vDir = normalize(sub(linkedGate.getPos(), cXY))
      self.setPos(add(linkedGate.getPos(), mul(vDir, gOutsideDist)))
      self.pCurArriveObj = None
      self.pStartFromObj = None
      self.move(linkedGate.getPos(), linkedGate)
    else:
      # if not found linked gate then Find linked Obj with parent of gate
      linkedObj = gBridge.getLinkedObjWithGate(pTargetGate)
      gWorldEdit.upToTheLevel()
      # up to level once again
      if isinstance(linkedObj, ObjectBase.City):
        gWorldEdit.upToTheLevel()
      # move to the City
      if linkedObj:
        self.pStartFromObj = pTargetGate
        self.move(linkedObj.getPos(), linkedObj)
  
  def stop(self):
    self.bMove = False
    self.bJump = False