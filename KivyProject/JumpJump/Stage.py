import math, time
import Utility
from Utility import *
from kivy.animation import Animation
from Sprite.Sprite import Sprite, SpriteMgr
from Particle.Particle import gFxMgr
from Character import gCharacterMgr, BaseCharacter
from Stuff import gStuffMgr
from ResourceMgr.ResourceMgr import gResMgr

from Constants import *
import GameFrame
import Character
import Weapon


class Block:
  cellCount = (16, 16)
  
  def __init__(self, parent, index_x, index_y, pos, scale):
    width = BLOCK_SIZE[0] * scale
    height = BLOCK_SIZE[1] * scale
    x = int(pos[0] / width) * width + width * 0.5
    y = int(pos[1] / height) * height + height * 0.5
    pos=(x, y)
    self.size = (width, height)
    texture = gResMgr.getTexture("terrain")
    cellWidth = texture.width / self.cellCount[0]
    cellHeight = texture.height / self.cellCount[1]
    cellX = min(index_x, self.cellCount[0]) * cellWidth
    cellY = min(self.cellCount[1] - index_y - 1, self.cellCount[1]) * cellHeight
    texture = texture.get_region(cellX, cellY, cellWidth, cellHeight)
    
    self.sprite = Sprite(pos=pos, size=self.size, touchable=False, gravity=0, \
      elastin=0, collision=False, texture=texture)
    parent.add_widget(self.sprite)
  
  def remove(self):
    if self.sprite.parent:
      self.sprite.parent.remove_widget(self.sprite)
      
      
class StageManager(Singleton):
  def __init__(self):
    self.inited = False
    self.acc_time = 0.0
    self.stageProps = None
    self.currentStage = None
    self.player = None
    self.parentLayer = None
    self.spriteMgr = None
    self.characterMgr = None
    self.weaponMgr = None
    self.stageEditor = None
  
  def setParentLayer(self, parentLayer):
    self.parentLayer = parentLayer
    
  def reset(self):
    self.acc_time = 0.0
    GameFrame.gGameFrame.board.reset()
    
    self.spriteMgr = SpriteMgr.instance()
    self.spriteMgr.reset()
    
    self.player = Character.Player.instance()
    
    self.stageProps = gResMgr.getProperty("stage")
    prop = self.stageProps.properties[0]
    stage = Stage(prop)
    stage.reset()
    self.parentLayer.add_widget(stage.layer_bg)
    self.currentStage = stage
    
    self.stageProps.addRowDatas(['bg01', 1.0, 1.0, 3, 1.0])
    self.stageProps.save()
    log("save")
    # init fx manager
    gFxMgr.setLayer(stage.layer_fx)
    gFxMgr.reset()
    gFxMgr.setActive(True)
    # create a hit fx particle
    particleInfo = dict(texture=gResMgr.getTexture('star'), scaling=Var(0.3, 0.7), rotateVel=Var(720.0), rotate=Var(0.0, 360), 
      lifeTime=Var(1.5,2.0), vel=Var([-200.0, 400.0], [200.0, 500.0]), gravity=Var(2000.0))
    gFxMgr.create_emitter(PARTICLE_HIT, particleInfo, 3)
    particleInfo = dict(texture=gResMgr.getTexture('explosion'), fade=1, scaling=Var(2.0, 3.0), rotateVel=Var(50.0), rotate=Var(0.0, 360), offset=Var((-20,20), (-20,20)),
      lifeTime=Var(0.5, 1.0), vel=Var([-500.0, 500.0], [500.0, 900.0]), gravity=Var(0.0), sequence=[4,4], delay=Var(0.0, 0.2))
    gFxMgr.create_emitter(PARTICLE_EXPLOSION, particleInfo, 5)
    # reset managers
    gStuffMgr.setParentLayer(stage.layer_bg)
    gStuffMgr.reset()
    self.characterMgr = gCharacterMgr
    self.characterMgr.setParentLayer(stage.layer_bg)
    self.characterMgr.reset(stage.getSpace())
    self.weaponMgr = Weapon.WeaponMgr.instance()
    self.weaponMgr.reset(stage.layer_bg, stage.getSpace())
  
  def isDone(self):
    return self.characterMgr.isDone()
    
  def setEnd(self):
    self.characterMgr.stop()
    self.weaponMgr.clear()
    
  def create_character(self, index):
    self.currentStage.create_character(index)
    
  def getCurrentStageSpace(self):
    return self.currentStage.getSpace()
  
  def getCurrentStageScale(self):
    return self.currentStage.getScale()
    
  def getEnemyCount(self):
    return self.currentStage.getEnemyCount()
  
  def getPosToIndex(self, pos):
    return self.currentStage.getPosToIndex(pos)
    
  def getIndexToPos(self, ipos):
    return self.currentStage.getIndexToPos(ipos)
  
  def isBlock(self, ipos):
    obj = self.currentStage.get_object(ipos)
    return isinstance(obj, Block)
  
  def isBlockByPos(self, pos):
    obj = self.currentStage.get_object_by_pos(pos)
    return isinstance(obj, Block)
    
  def togglePlay(self):
    if GameFrame.gGameFrame.isStatePlay():
      self.spriteMgr.play()
      gFxMgr.setActive(True)
    elif GameFrame.gGameFrame.isStatePause():
      self.spriteMgr.stop()
      gFxMgr.setActive(False)
      
  def update(self):
    if not GameFrame.gGameFrame.isStatePlay():
      return
      
    if self.currentStage:
      self.currentStage.update()
      gStuffMgr.update()
      gCharacterMgr.update()
      self.weaponMgr.update()
      
    
# manage character spawn, background
class Stage():
  def __init__(self, prop):
    self.i = 0
    self.prop = prop
    self.size = [W * prop["width"], H * prop["height"]]
    self.scale = self.prop["scale"]
    self.touch_time = 0.0
    self.grab = None
    self.grab_offset = (0.0, 0.0)
    self.layer_bg = Sprite(pos=[0,0], size=self.size, gravity=0, texture=prop["image"].texture)
    self.layer_bg.color.rgba = (1.0, 1.0, 1.0, 0.0)
    self.layer_fx = Sprite(pos=[0,0], size=[0,0])
    self.layer_bg.add_widget(self.layer_fx)
    self.layer_bg.setScale(self.scale)
    self.layer = None
    self.layer_bg.func_touch_down = self.func_touch_down
    self.layer_bg.func_touch_move = self.func_touch_move
    self.layer_bg.func_touch_up = self.func_touch_up
    self.blockCount = (int(self.size[0] / (self.scale * BLOCK_SIZE[0])), int(self.size[1] / (self.scale * BLOCK_SIZE[1])))
    self.blocks = []
    for iy in range(self.blockCount[1]):
      self.blocks.append([])
      for ix in range(self.blockCount[0]):
        self.blocks[iy].append(None)
    
  def reset(self):
    self.grab = None
    self.layer_bg.color.a = 0.0
    anim = Animation(a=1.0, duration=1.0)
    anim.start(self.layer_bg.color)
    self.player = Character.Player.instance()
  
  def screen_to_world(self, pos):
    return div(sub(pos, self.layer_bg.getPos()), self.scale)
  
  def func_touch_down(self, touch):
    self.layer_bg.dragable = True
    # screen pos to world pos
    touch_pos = self.screen_to_world(touch.pos)
    for character in gCharacterMgr.getCharacters():
      dist = getDist(touch_pos, character.getCenter())
      if dist < character.radius * 2.0:
        self.grab = character
        self.layer_bg.dragable = False
        self.grab_offset = sub(character.getPos(), touch_pos)
        break
    self.touch_time = getAccTime()
        
  def func_touch_move(self, touch):
    if self.grab:
      touch_pos = self.screen_to_world(touch.pos)
      self.grab.sprite.setPos(*add(touch_pos, self.grab_offset))
  
  def func_touch_up(self, touch):
    if getAccTime() - self.touch_time < TOUCH_TIME:
      self.touch_block(touch)
    self.grab = None
    self.layer_bg.dragable = True
    self.touch_time = 0.0
  
  def touch_block(self, touch):
    # remove character
    if self.grab and issubclass(self.grab.__class__, BaseCharacter) and \
      not self.grab.isPlayer:
        gCharacterMgr.remove_character(self.grab)
        self.grab = None
    else:
      # create or remove block
      pos = self.screen_to_world(touch.pos)
      ipos = self.getPosToIndex(pos)
      obj = self.get_object(ipos)
      if obj:
        self.remove_object(ipos) # remove character or block
      else:
        self.create_block(ipos)
    
  def getPosToIndex(self, pos):
    ix = max(0, min(int(pos[0] / (self.scale * BLOCK_SIZE[0])), self.blockCount[0] - 1))
    iy = max(0, min(int(pos[1] / (self.scale * BLOCK_SIZE[1])), self.blockCount[1] - 1))
    return (ix, iy)
  
  def getIndexToPos(self, ipos):
    return mul(mul(ipos, BLOCK_SIZE), self.scale)
  
  def get_object_by_pos(self, pos):
    return self.get_object(self.getPosToIndex(pos))
     
  def get_object(self, ipos):
    ipos = (int(max(0, min(ipos[0], self.blockCount[0] - 1)))
                , int(max(0, min(ipos[1], self.blockCount[1] - 1))))
    return self.blocks[ipos[1]][ipos[0]]
    
  def set_object(self, obj, ipos):
    ipos = (int(max(0, min(ipos[0], self.blockCount[0] - 1)))
            , int(max(0, min(ipos[1], self.blockCount[1] - 1))))
    self.blocks[ipos[1]][ipos[0]] = obj
      
  def remove_object(self, ipos):
    obj = self.get_object(ipos)
    if obj:
      obj.remove()
    self.set_object(None, ipos)
  
  def create_block(self, ipos):
    pos = self.getIndexToPos(ipos)
    block = Block(self.layer_bg, 3, 0, pos, self.scale)
    self.set_object(block, ipos)
    
  def create_character(self, index):
    pos = self.screen_to_world(cXY)
    gCharacterMgr.create_character(False, index, self.getSpace(), pos)
  
  def getScale(self):
    return self.scale
    
  def getSpace(self):
    return (0,0,self.size[0], self.size[1])
  
  def getEnemyCount(self):
    return self.prop["enemyCount"]
    
  def update(self):
    playerPos = self.player.getPos()
    x = max(min(0, cX - playerPos[0] * self.scale), min(W - self.size[0] * self.scale, (W - self.size[0] * self.scale) * 0.5))
    y = max(min(0, cY - playerPos[1] * self.scale), min(H - self.size[1] * self.scale, (H - self.size[1] * self.scale) * 0.5))
    self.layer_bg.setPos(x, y)
    

gStageMgr = StageManager.instance()
