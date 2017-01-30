from copy import copy
from xml.etree.ElementTree import Element, dump, parse, SubElement, ElementTree, tostring
from xml.dom import minidom
import threading
import traceback
import time
import random

import Utility as Util
from Utility import *
from ResourceMgr import gResMgr

from Globals import *

import ObjectBase
import Bridge

#---------------------#
# Global Instance
#---------------------#
def setGlobalInstance():
  global gWorldEdit, gBridge, gWorld, gPlayer
  gWorldEdit = WorldEdit.instance()
  gBridge = Bridge.Bridge.instance()
  gWorld = ObjectBase.World.instance()
  gPlayer = ObjectBase.Player.instance()
  # set global variable
  ObjectBase.setGlobalInstance(WorldEdit, Bridge.Bridge)
  Bridge.setGlobalInstance(WorldEdit)

#---------------------#
# class : WorldEdit
#---------------------#    
class WorldEdit(Singleton, Widget):
  city = []
  bLoading = False
  gameScreen = None
  currentLevel = None
  currentDrawObj = []
  selectedObj = None
  touchObjList = {} # {touchObject:touched obj list, ...}
  isEditMode = True
  bPause = False
  bTouchEditBtn = False
  lastCheckTime = 0.0
  popupMenu = None
  widgets = ScrollView(size=(W*0.15, H), size_hint=(None,None))
  widgets.name = "WorldEditUI"
  layout = GridLayout(cols=1, size_hint_y=None)
  layout.name = "WorldEditUI_Layout"
  onExitFunc = None
  IDs = set(range(gMaxObj))
  objMap = {}
  drawAlwaysObj = []
  widthRatio = 1.0
  heightRatio = 1.0 
  
  def init(self, screen):
    self.gameScreen = screen
    # set touch prev callback
    gMyRoot.setTouchPrev(self.onTouchPrev)
    self.IDs = set(range(gMaxObj))
    self.popupMenu = popupMenu.instance()
    self.gameScreen.add_to_ui(self)
    self.gameScreen.add_to_ui(self.popupMenu)
    self.bind(on_touch_up = self.onTouchUp,
      on_touch_move = self.onTouchMove,
      on_touch_down = self.onTouchDown)
    self.setCurrentLevel(None)
    gMyRoot.regist(self)
      
  def bind_OnExit(self, func):
    self.onExitFunc = func

  # init
  def build_ui(self):
      # level name
      if not hasattr(self, "currentLevelName"):
        self.currentLevelName = Label(text="World", font_size="25dp", pos=(0,H-100), size=(W,100))
        with self.currentLevelName.canvas.before:
          Color(0.6, 0.2, 0.4, 0.5)
          Rectangle(size=self.currentLevelName.size, pos=self.currentLevelName.pos)
      if not self.currentLevelName.parent:
        self.gameScreen.add_to_ui(self.currentLevelName)
      if self.currentLevel:
        self.currentLevelName.text = self.currentLevel.getTitle()
        # show id
        if self.isEditMode: 
          self.currentLevelName.text += "(ID:%d)" % self.currentLevel.getID()
      else:
        self.currentLevelName.text = ""
    
      btn_size = mul(WH, (0.15, 0.08))
      # toggle edit mode button
      if not hasattr(self, "btn_edit"):
        self.btn_edit = Button(text="Edit Mode", pos=(W-btn_size[0], H-btn_size[1]), size=btn_size)
        self.btn_edit.bind(on_release = lambda inst:self.setEditMode(inst, not self.isEditMode))
      # attach
      if not self.btn_edit.parent:
        self.gameScreen.add_to_ui(self.btn_edit)
      
      # toggle ui button
      if not hasattr(self, "btn_toggle"):
        self.btn_toggle = Button(text="Toggle UI", pos=(W-btn_size[0], H-btn_size[1]*2), size=btn_size)
        self.btn_toggle.bind(on_release = lambda inst:self.toggleUI())  
      # attach
      if self.isEditMode and not self.btn_toggle.parent:
        self.gameScreen.add_to_ui(self.btn_toggle)
      
      # toggle able widgets
      self.layout.clear_widgets()
      if not self.layout.parent:
        self.widgets.add_widget(self.layout)
      # function - add button
      def add_button(text, func, userData = None):
        btn = Button(text=text, width=btn_size[0], size_hint_y=None, height=btn_size[1])
        btn.userData = userData
        btn.bind(on_release = func)
        self.layout.add_widget(btn)
      add_button("Clear", self.clearCurrentLevel)
      if self.currentLevel:
        for childType in self.currentLevel.childTypes:
          childClass = eval("ObjectBase." + childType)
          if childClass.bCreatable:
            add_button("Add " + childType, self.add_object, childType)
      add_button("Exit", self.exit)
      if self.currentLevel:
        self.layout.height = btn_size[1] * (2+len(self.currentLevel.childTypes))
      self.widgets.pos = (W-btn_size[0], 0)
      self.widgets.size = (btn_size[0], self.btn_toggle.pos[1])
      
  def setPause(self, bPause):
    self.bPause = bPause
  
  def setEditMode(self, inst, bEdit):
    if inst and self.bLoading:
      return
    # set pause
    self.setPause(bEdit)
    # touched flag - for check something?
    self.bTouchEditBtn = True
    self.isEditMode = bEdit
    # toggle - toggle ui button
    if bEdit and self.btn_toggle.parent == None:
      self.gameScreen.add_to_ui(self.btn_toggle)
    elif not bEdit and self.btn_toggle.parent:
      self.btn_toggle.parent.remove_widget( self.btn_toggle)
        
    self.showID(bEdit)
    self.showUI(bEdit)
    
  def showUI(self, bShow):
    if bShow and self.widgets.parent == None:
      self.gameScreen.add_to_ui(self.widgets)
    elif not bShow and self.widgets.parent:
      self.widgets.parent.remove_widget(self.widgets)
  
  def toggleUI(self):
    self.showUI(not self.widgets.parent)
  
  def postLoadProcess(self):
    for obj in self.objMap.values():
      obj.postLoadProcess()
  
  def load(self, filename, screen):
    bUseLoadThread = False
    if bUseLoadThread:
      t = threading.Thread(target=self.load_thread, args=(filename, screen, bUseLoadThread))
      t.start()
    else:
      # redraw bridge and recalculate gate pos 
      job = gMyRoot.newJob("Loading...")     
      job.addJob(self.load_thread, args=(filename, screen, bUseLoadThread))
 
  def load_thread(self, filename, screen, bThread):
    try:
      self.bLoading = True
      # init
      self.init(screen)
      # black screen
      screen.screen_black()
      
      # load file
      tree = root = None
      itemCount = 0
      self.filename = filename
      if os.path.isfile(filename):
        try:
          tree = parse(filename)
          root = tree.getroot()
          itemCount = int(root.get("count") or 0)
          # get device window size
          self.widthRatio = W / float(root.get("width") or W)
          self.heightRatio = H / float(root.get("height") or H)
        except:
          log("load error : %s" % filename)
      else:
        log("no file : %s" % filename)
        
      # load data
      # build loading bar
      if bThread:
        gMyRoot.createProgressPopup("loading...", itemCount)
      gWorld.reset(None, root)
      gWorld.load(root)
      gBridge.load(root)
      if bThread:
        gMyRoot.destroyProgressPopup()
    except:
      log("loading error..." + traceback.format_exc())
      gMyRoot.exit() 
    # process after load done
    self.postLoadProcess()  
    # set current level
    if gPlayer and gPlayer.parentObj:
      self.setCurrentLevel(gPlayer.parentObj)
    else:
      self.setCurrentLevel(gWorld)
    # set edit mode
    self.setEditMode(None, True)
    # screen transition
    screen.screen_transition()
    self.bLoading = False
    
  def save(self):
    # check save directory
    if self.filename:
      if not os.path.isdir(gSaveDir):
        os.mkdir(gSaveDir)
       
    class Counter:
      value = 0
        
    # save tree data
    root = gWorld.save(None, Counter)
    gBridge.save(root, Counter)
    root.set("count", str(Counter.value))
    # save window size
    root.set("width", str(W))
    root.set("height", str(H))
    
    # xml save - good to view
    data = tostring(root)
    data = minidom.parseString(data)
    f = open(self.filename, "w")
    f.writelines(data.toprettyxml(indent="    "))
    f.close()
      
  def exit(self, *args):
    # save and clear
    self.save()
    self.clearDrawAlwaysObj()
    # remove order is very important
    gBridge.remove()
    gWorld.remove() 
    self.setCurrentLevel(None)
    # set touch prev callback
    gMyRoot.setTouchPrev(None)
    # unregist
    gMyRoot.remove(self)
    # call exit
    if self.onExitFunc:
      self.onExitFunc()
      
  def update(self, dt):
    if self.bLoading:
      return
    
    # find really touched object
    for touch in self.touchObjList:
      touchedList = self.touchObjList[touch]
      minDist = 99999.9
      maxPriority = -1
      touchedObj = None
      for obj in touchedList:
        # check priority
        dist = getDist(obj.center, touch.pos)
        if obj.getTouchPriority() > maxPriority or (obj.getTouchPriority() >= maxPriority and dist < minDist):
          touchedObj = obj
          minDist = dist
          maxPriority = obj.getTouchPriority()
      if touchedObj:
        #log("touch : " + str(touchedObj.getID()))
        touchedObj.touch_down(touch)
    # clear
    self.touchObjList.clear()
    
    # update bridge
    gBridge.update()
    
    # check game paused
    if not self.bPause:
      # update object
      for obj in self.objMap.values():
        obj.update(dt)
      
  def clearDrawAlwaysObj(self):
    self.drawAlwaysObj = []
  
  def addDrawAlwaysObj(self, obj):
    if obj not in self.drawAlwaysObj:
      self.drawAlwaysObj.append(obj)
    
  def removeDrawAlwaysObj(self, obj):
    if obj in self.drawAlwaysObj:
      self.drawAlwaysObj.remove(obj)
  
  def addDrawObj(self, obj):
    self.currentDrawObj.append(obj)
    
  def removeDrawObj(self, obj):
    if obj in self.currentDrawObj:
      self.currentDrawObj.remove(obj)
  
  def getObj(self, ID):
    return self.objMap[ID] if ID in self.objMap else None
  
  # regist object and set id
  def registObjID(self, obj):
    # check maxobj count limit
    if len(self.IDs) == 0:
      raise Exception('setObjId error', 'Too many object...')
    if obj.getID() not in self.IDs:
      # set new id
      newID = self.IDs.pop()
      obj.setID( newID )
    else:
      # set exist id
      self.IDs.remove(obj.getID())
    # slice for log, because too big list.. too slow
    # obj add to map
    self.objMap[obj.getID()] = obj
      
  # unregist object id
  def unregistObjID(self, obj):
    if obj.getID() > -1:
      ID = obj.getID()
      if ID in self.objMap:
        self.objMap.pop(ID)
      self.IDs.add(ID)
      obj.setID(-1)
      
  def showID(self, bShow):
    # show current level id
    self.currentLevelName.text = self.currentLevel.getTitle() if self.currentLevel else ""
    if self.isEditMode: 
      self.currentLevelName.text += "(ID:%d)" % self.currentLevel.getID()    
    # show player id
    gPlayer.showID(bShow)
    # show object id
    for childLevel in self.currentLevel.get_childObj():
      childLevel.showID(bShow)
      
  def checkCanMove(self, obj):  
    if obj.parentObj and obj.parentObj is not self.getCurrentLevel() and\
      (not obj.parentObj.bHasDoor or obj.parentObj.parentObj is not self.getCurrentLevel()):
      return False
    return True
    
  # find nearest object        
  def findNearestObj(self, fromObj, ignoreTypes = []):    
    if fromObj and self.getCurrentLevel():
      checkList = []
      # filtering ignore list
      for obj in self.getCurrentLevel().get_childObj():
        if fromObj == obj:
          continue
        for ignore in ignoreTypes:
          if isinstance(obj, ignore):
            break
        else:
          checkList.append(obj)
      # find nearest object
      minDist = fromObj.size[0]
      nearestObj = None
      
      for obj in checkList:
        dist = getDist(fromObj.getPos(), obj.getPos())
        if dist < minDist:
          minDist = dist
          nearestObj = obj  
      return nearestObj
    return None # found nothing...
  
  def onTouchPrev(self, *args):
    # check loading
    if self.bLoading or gPlayer.isMove() or gPlayer.isJump():
      return

    if self.getParentLevel():
      self.gotoParentLevel()
    else:
      self.exit()
      
  def onTouchDown(self, inst, touch):
    added = 0
    for obj in self.currentDrawObj:
      if obj.check_touched(touch.pos):
        self.addTouchObj(obj, touch)
        added += 1
    # touch nothing
    if added == 0:
      self.selectObj(None)
    
  def onTouchMove(self, inst, touch):
    if self.selectedObj and self.selectedObj.isTouched():
      self.selectedObj.touch_move(touch)
      
  def onTouchUp(self, inst, touch):
    if self.selectedObj and self.selectedObj.isTouched():
      self.selectedObj.touch_up(touch)
      
    if not self.isEditMode and touch.pos[1] < (H - self.btn_edit.size[1]):
      # check touch nothing?
      if self.getCurrentLevel() != None and self.getCurrentLevel().bFreeMoveType \
        and touch != None and (not hasattr(touch, "bTouched") or not touch.bTouched) \
        and self.checkCanMove(gPlayer):
        # player move to touch point
        gPlayer.move(sub(touch.pos, mul(gPlayer.size, 0.5)))
    self.bTouchEditBtn = False
  
  def addTouchObj(self, obj, touch):
    if touch in self.touchObjList:
      self.touchObjList[touch].append(obj)
    else:
      self.touchObjList[touch] = [obj]
      
  # call by Object's touch event  
  def selectObj(self, obj):  
    # add or remove bridge
    if self.isEditMode:
      if obj and obj != self.selectedObj and self.selectedObj\
        and self.selectedObj.isTouched():
          gBridge.checkBridge(self.selectedObj, obj)
          # unset object property popup
          self.selectedObj.setPopup(False)
          obj.setPopup(False)
          #self.selectedObj.touch_up(None)
          obj.touch_up(None)
    # play mode
    elif obj != None:
      # move to the target
      if self.checkCanMove(gPlayer):
        gPlayer.move_to(obj)
      # enter the level
      elif gPlayer.isInParentList(obj):
        self.setCurrentLevel(obj)
        
    if self.selectedObj and self.selectedObj != obj and self.selectedObj.isTouched():
      self.selectedObj.touch_up(None)
      
    self.selectedObj = obj
  
  def getSelected(self):
    return self.selectedObj
     
  def isSelected(self, obj):
    return self.selectedObj is obj
    
  def add_object(self, inst):
    if self.isEditMode:
      self.currentLevel.add_childObj(inst.userData)
    
  def notifyRemoveObj(self, obj):
    if self.selectedObj == obj:
      self.selectObj(None)
    
  def clearCurrentLevel(self, *args):
    if self.isEditMode and self.currentLevel != None:
      gMyRoot.popup("Clear all?", self.currentLevel.clear, None)
        
  def getCurrentLevel(self):
    return self.currentLevel
    
  def upToTheLevel(self):
    if self.getCurrentLevel().parentObj:
      self.setCurrentLevel(self.getCurrentLevel().parentObj)
      
  def drawBgTile(self):
    tile_count = (20, 10)
    widget_size = div(WH, tile_count)
    for x in range(tile_count[0]):
      for y in range(tile_count[1]):
        tile = Widget(pos=mul((x,y), widget_size), size=widget_size)
        tex = gResMgr.getTex("ground_8x6")
        tex_count = (8, 6)
        tex_size = div(tex.size, tex_count)
        i, j = mul(tex_size, (random.randint(0, tex_count[0]), random.randint(0, tex_count[1])))
        tex = tex.get_region(i, j, tex_size[0], tex_size[1])  
        with tile.canvas:
          Rectangle(texture=tex, size=tile.size, pos=tile.pos)
        self.gameScreen.add_to_bg(tile)
  
  def setCurrentLevel(self, currentLevel):
    # check level has childtype, then enterable
    if currentLevel != None and not currentLevel.getChildTypes():
      return
    
    # screen transition
    self.gameScreen.screen_transition()
    self.gameScreen.clear_bg()
    
    # set bg
    bg = Widget(size=WH)
    with bg.canvas:
      Rectangle(size=WH, texture=gResMgr.getTex("bg01"))
    self.gameScreen.add_to_bg(bg)
    
    oldLevel = self.currentLevel
    # level change..
    if oldLevel:
      oldLevel.exitLevel()
      
    # set new level
    self.currentLevel = currentLevel
    self.build_ui()
    if currentLevel != None:
      # attach objects and draw - important order
      gBridge.draw()
      self.currentDrawObj = []
      self.currentLevel.draw_childObj()
      gBridge.drawBridge()
      
    # draw always object
    for obj in self.drawAlwaysObj:
      # check draw twice...
      if obj.parentObj != currentLevel:
        obj.draw()
    self.selectObj(None)
    self.popupMenu.removePopup()
    
  def getParentLevel(self):
    return self.currentLevel.parentObj if self.currentLevel else None
  
  def gotoParentLevel(self):
    parentObj = self.getParentLevel()
    if parentObj:
      self.setCurrentLevel(parentObj)

#---------------------#
# decorator
#---------------------#
def popupTouch(func):
  def decorator(self, *args):
    func(self, *args)
    self.removePopup()
  return decorator

#---------------------#
# Popup Menu
#---------------------#
class popupMenu(RelativeLayout, Singleton):
  popupRect = [0,0,0,0]
  bShowPopup = False
  widgetSize = mul(WH, (0.2,0.07))
  widgets = None
  nameTag = None
  obj = None
  
  def __init__(self):
    RelativeLayout.__init__(self)
    self.bind(on_touch_down=self.onTouchDown)
    self.bind(on_touch_move=self.movePopup)
    self.bind(on_touch_up=self.movePopup)
  
  def onTouchDown(self, inst, touch):
    # check popup widgets region and clear
    if touch.pos[0] < self.popupRect[0] or touch.pos[0] > self.popupRect[2] \
      or touch.pos[1] < self.popupRect[1] or touch.pos[1] > self.popupRect[3]:
        self.removePopup()
        
  def movePopup(self, inst, touch):
    if self.bShowPopup:
      self.calcPopupPos()
  
  @popupTouch
  def rename(self, obj, inst):
    obj.setName(inst.text)
  
  @popupTouch
  def removeDialog(self, obj):
    def funcRemove():
      obj.remove()
      gWorldEdit.notifyRemoveObj(obj)
    gMyRoot.popup("Remove?", funcRemove, None)
    
  @popupTouch
  def test(self):
    pass
    
  def showPopup(self, obj):
    self.removePopup()
    if self.bShowPopup != True:
      self.bShowPopup = True
      self.obj = obj
      self.widgets = []
      # name
      self.nameTag = TextInput(text = self.obj.getName(), multiline=False, size=self.widgetSize,
          background_color=(1,1,1,0.2), foreground_color=(1,1,1,1))
      self.nameTag.bind(on_text_validate = lambda inst:self.rename(obj, inst))
      self.widgets.append(self.nameTag)
      
      # etc button
      btn = Button(text = "test", size=self.widgetSize)
      btn.bind(on_release = lambda inst:self.test())
      self.widgets.append(btn)
      
      # remove button - check deletable flag
      if obj and obj.bDeletable:
        btn = Button(text = "Remove", size=self.widgetSize)
        btn.bind(on_release = lambda inst:self.removeDialog(obj))
        self.widgets.append(btn)
        
      # close button
      btn = Button(text = "Close", size=self.widgetSize)
      btn.bind(on_release = lambda inst:self.removePopup())
      self.widgets.append(btn)
      # attach all widget
      for i, widget in enumerate(self.widgets):  
        widget.pos = (0, i * -self.widgetSize[1])
        self.add_widget(widget)
      # popup position
      self.calcPopupPos()
 
  def calcPopupPos(self):
      # right-top
      pos = sub(add(self.obj.pos[:2], self.obj.size[:2]), (0, self.widgetSize[1]))
      width = self.widgetSize[0]
      height = self.widgetSize[1] * len(self.widgets)
      # check popup pos
      if (pos[1] + self.widgetSize[1]) - height < 0.0:
        pos[1] = height - self.widgetSize[1]
      if pos[0] + width > W:
        pos[0] = self.obj.pos[0] - width
      # set popup rect
      self.popupRect = [pos[0], (pos[1]+self.widgetSize[1])-height, pos[0]+width, pos[1] + self.widgetSize[1]]
      # set pos
      self.pos = pos
      
  def removePopup(self):
    if self.bShowPopup:
      self.bShowPopup = False
      #gWorldEdit.gameScreen.remove_from_bg(self)
      for btn in self.widgets:
        self.remove_widget(btn)
    self.widgets = []
    self.nameTag = None
    self.obj = None
        
  def togglePopup(self):
    if self.bShowPopup:
      self.clearPopup()
    else:
      self.showPopup()
  
#---------------------#
# set global instance
#---------------------#
setGlobalInstance()