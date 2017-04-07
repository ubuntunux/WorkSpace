import math, time
import Utility
from Utility import *
from kivy.animation import Animation
from Sprite.Sprite import Sprite
from Particle.Particle import gFxMgr
from ResourceMgr.ResourceMgr import gResMgr

from Constants import *
import GameFrame
import Stage
from Weapon import *


class CharacterMgr(Singleton):
  def __init__(self):
    self.characters = []
    self.monsters = []
    self.player = None
    self.stageMgr = None
    self.parentLayer = None
  
  def setParentLayer(self, parentLayer):
    self.parentLayer = parentLayer
  
  def isDone(self):
    return self.player.isDead or gCharacterMgr.getMonsterCount() == 0
    
  def clear(self):
    for character in self.characters:
      character.setDead()
    self.monsters = []
    self.characters = []
  
  def reset(self, space):
    self.monsters = []
    self.characters = []
    self.stageMgr = Stage.gStageMgr
    self.props = props = gResMgr.getProperty("character")
    # add player
    self.player = Player.instance()
    playerIndex = 4 # A bee
    pos = (CHARACTER_SIZE[0], CHARACTER_SIZE[1] * 0.5)
    self.create_character(True, playerIndex, space, pos)
    self.player.binding_key() 
     
    # add monster
    count = self.stageMgr.getEnemyCount()
    for i in range(count): 
      n = random.randrange(0, len(props.properties))
      # TestCode
      n = 5
      pos = (random.uniform(SEARCH_RANGE * 2.0, W), CHARACTER_SIZE[1] * 0.5) 
      self.create_character(False, n, space, pos)
        
  def create_character(self, isPlayer, prop_index, space, pos):
    prop = self.props.properties[prop_index]
    character = None
    if isPlayer:
      character = Player.instance()
    else:
      try:
        if prop["type"]:
          character = eval(prop["type"] + "()")
      except:
        pass
      if character is None:
        character = Monster()
    character.init(pos, prop)
    character.reset(space)
    self.parentLayer.add_widget(character.getSprite())
    if not isPlayer:
      self.monsters.append(character)
    self.characters.append(character)
  
  def remove_character(self, character):
    if character:
      character.remove()
      if character in self.characters:
        self.characters.remove(character)
      if character in self.monsters:
        self.monsters.remove(character)
    
  def getMonsters(self):
    return self.monsters
  
  def getMonsterCount(self):
    return len(self.monsters)
    
  def getCharacters(self):
    return self.characters
  
  def update(self):
    for character in self.characters:
      character.update()
    
    # check collide
    hitList = set()
    collideOnlyPlayer = True
    for i, A in enumerate(self.characters):
      if A.isDead:
        continue
      posA = add(A.getPos(), mul(A.size, 0.5))
      vA = A.getVelocity()
      lA = getDist(vA)
      nA = normalize(vA)
      for B in [gPlayer,] if collideOnlyPlayer else self.characters[i+1:]:
        if A == B or B.isDead:
          continue
        posB = add(B.getPos(), mul(B.size, 0.5))
        dist = getDist(posA, posB)
        if dist < (A.size[0] + B.size[0]) * 0.5:
          v = normalize(sub(posA, posB))
          vB = B.getVelocity()
          lB = getDist(vB)
          nB = normalize(vB)
          d = -dot(v, nA)
          isHit = False
          if d > 0.0:
            isHit = True
            A.setVelocity(*sub(A.getVelocity(), vA))
            B.setVelocity(*add(B.getVelocity(), mul(vA, d)))
            rV = mul(v, dot(v, mul(nA, -1.0)))
            rV = sub(mul(rV, 2.0), mul(nA, -1.0))
            rV = mul(normalize(rV), lA * (1.0-d))
            A.setVelocity(*add(A.getVelocity(), rV))
            B.setHitForce(A.getForce())
          d = dot(v, nB)
          if d > 0.0:
            isHit = True
            A.setVelocity(*add(A.getVelocity(), mul(vB, d)))
            B.setVelocity(*sub(B.getVelocity(), vB))
            v = mul(v, -1.0)
            rV = mul(v, dot(v, mul(nB, -1.0)))
            rV = sub(mul(rV, 2.0), mul(nB, -1.0)) 
            rV = mul(normalize(rV), lB * (1.0-d))
            B.setVelocity(*add(B.getVelocity(), rV))
            A.setHitForce(B.getForce())
          # check damage
          if isHit and (gPlayer == A or gPlayer == B):
            if abs(v[0]) < DAMAGE_ANGLE:
              if posA[1] > posB[1]:
                hitList.add(B)
                A.setJump()
                B.setVelocity(0, 0)
              else:
                hitList.add(A)
                A.setVelocity(0, 0)
                B.setJump()
          # set damage and set score
          for hitted in hitList:
            self.process_hit(hitted)
            
  def push(self, A, B, force):
    vector = mul(normalize(sub(A.getPos(), B.getPos())), force)
    A.setVelocity(*vector)
        
  def process_hit(self, hitted):
    if not hitted.isDead:
      hitted.setDamage()
      if hitted is not self.player:
        GameFrame.gGameFrame.board.addCombo()
        GameFrame.gGameFrame.board.addScore(SCORE_HIT)
              
  def stop(self):
    for character in self.characters:
      character.stop()
  
  
class BaseCharacter():
  jumpable = True
  search_range = SEARCH_RANGE
  maxHp = MAXHP
  isPlayer = False
  fireTime = 1.0
  scale = 1.0
  force = 1.0
  weaponClass = None
  confuse_time = 1.0
  
  def __init__(self):
    self.prop = None
    self.pos = (0, 0)
    self.old_pos = (0, 0)
    self.hp = self.maxHp
    self.size = None 
    self.radius = 0.0
    self.frameTime = 0.0
    self.flickerTime = 0.0
    self.idleTime = 0.0
    self.patrolTime = 0.0
    self.confuseElapseTime = 0.0
    self.fire = False
    self.fireElapsedTime = 0.0
    self.isHittedFly = False
    self.isDead = False
    self.isLeft = False
    self.isMoveLeft = False
    self.isMoveRight = False
    self.target = None
    self.sprite = None
    self.state = StateMachine()
    self.STATE_IDLE = StateItem()
    self.STATE_PATROL = StateItem()
    self.STATE_TRACE = StateItem()
    self.STATE_CONFUSE = StateItem()
    self.STATE_BOMB = StateItem()
    self.STATE_DEAD = StateItem()
    self.state.addState(self.STATE_IDLE)
    self.state.addState(self.STATE_PATROL)
    self.state.addState(self.STATE_TRACE)
    self.state.addState(self.STATE_CONFUSE)
    self.state.addState(self.STATE_BOMB)
    self.state.addState(self.STATE_DEAD)
  
  def __del__(self):
    self.remove()
  
  def remove(self):
    self.isDead = True
    if self.sprite.parent:
      self.sprite.parent.remove_widget(self.sprite)
  
  def setDead(self):
    self.remove()
    gCharacterMgr.remove_character(self)
      
  def init(self, pos, prop):
    self.prop = prop
    self.size = mul(CHARACTER_SIZE, self.scale)
    self.radius = getDist(self.size) * 0.5
    self.sprite = Sprite(pos=pos, size=self.size, gravity=GRAVITY, friction=FRICTION,\
      elastin=ELASTIN, collision=True, collisionSpace=WORLD_REGION, texture=prop["image"].texture)
    self.registStates()
    
  def reset(self, space):
    self.hp = self.maxHp
    self.target = None
    self.hitForce = 0.0
    self.frameTime = 0.0
    self.flickerTime = 0.0
    self.idleTime = 0.0
    self.patrolTime = 0.0
    self.confuseElapseTime = 0.0
    self.isDead = False
    self.isLeft = False
    self.isMoveLeft = False
    self.isMoveRight = False
    self.sprite.color.rgba = (1,1,1,1)
    self.sprite.collisionSpace = space
    self.state.setState(self.STATE_IDLE) 
    self.pos = self.getPos()
    self.old_pos = copy(self.pos)
    
  def getForce(self):
    return self.force
    
  def setHitForce(self, force):
    self.hitForce = force
    
  def setWeaponClass(self, weaponClass):
    self.weaponClass = weaponClass
     
  def stop(self):
    self.setVelocity(0, self.sprite.getVelocity()[1])
    
  def getCenter(self):
    return add(self.sprite.getPos(), mul(self.size, 0.5))
  
  def setPos(self, x, y):
    self.sprite.setPos(x, y)
    self.old_pos = self.pos
    self.pos = self.getPos()
  
  def getPos(self):
    return self.sprite.getPos()
    
  def getSize(self):
    return self.size
    
  def getVelocity(self):
    return self.sprite.getVelocity()
  
  def setVelocity(self, vx, vy):
    self.sprite.setVelocity(vx, vy)
    
  def setMoveLeft(self, isMove):
    self.isMoveLeft = isMove
    if isMove:
      self.isLeft = True
    
  def setMoveRight(self, isMove):
    self.isMoveRight = isMove
    if isMove:
      self.isLeft = False
  
  def toggleFire(self):
    self.fire = not self.fire
   
  def setFire(self):
    if GameFrame.gGameFrame.isStatePlay():
      if self.weaponClass and self.fireElapsedTime == 0.0:
        self.fireElapsedTime = self.fireTime
        weapon = self.weaponClass(self)
        weapon.setFire(self.getPos(), self.isLeft)
    
  def getSprite(self):
    return self.sprite
  
  def update(self):
    self.frameTime = Utility.getFrameTime()
    
    if self.weaponClass:
      if self.fireElapsedTime > 0.0:
        self.fireElapsedTime -= self.frameTime
        if self.fireElapsedTime < 0.0:
          self.fireElapsedTime = 0.0
      if self.fire and self.fireElapsedTime == 0.0:
        self.setFire()
      
    self.state.updateState()
    
    if self.isDead:
      return
      
    if self == gPlayer or self.state.isState(self.STATE_TRACE):
      self.updateTrace()
      
    if self.flickerTime > 0.0:
      self.updateFlicker()
    
    self.old_pos = self.pos
    self.pos = self.getPos()
    
    velocity = self.getVelocity()
    if self.old_pos[1] > self.pos[1]:
      if Stage.gStageMgr.isBlockByPos(add(self.getPos(), (self.size[0] * 0.5, 0.0))):
        if self.jumpable and (self.state.isState(self.STATE_TRACE) or self.isPlayer):
          self.setJump(1.0)
        else:
          # on ground
          scale = Stage.gStageMgr.getCurrentStageScale()
          y = int(self.pos[1] / (BLOCK_SIZE[1] * scale) + 1) * BLOCK_SIZE[1] * scale
          self.setPos(self.pos[0], y)
          self.sprite.setOnGround(True)
    elif self.sprite.isOnGround():
      # fall
      ipos = Stage.gStageMgr.getPosToIndex(add(self.getPos(), (self.size[0] * 0.5, 0.0)))
      if not Stage.gStageMgr.isBlock(add(ipos, (0, -1))):
        self.sprite.setOnGround(False)
    elif self.old_pos[1] < self.pos[1]:
      if Stage.gStageMgr.isBlockByPos(add(self.getPos(), (self.size[0] * 0.5, self.size[1]))):
        velocity = self.getVelocity()
        self.setVelocity(velocity[0], -velocity[1])
    if self.old_pos[0] > self.pos[0]:
      if Stage.gStageMgr.isBlockByPos(add(self.getPos(), (0, self.size[1] * 0.5))):
        velocity = self.getVelocity()
        self.setVelocity(-velocity[0], velocity[1])
    elif self.old_pos[0] < self.pos[0]:
      if Stage.gStageMgr.isBlockByPos(add(self.getPos(), (self.size[0], self.size[1] * 0.5))):
        velocity = self.getVelocity()
        self.setVelocity(-velocity[0], velocity[1])
      
  def isGround(self):
    return self.sprite.isGround
      
  def setJump(self, force=1.0):
    if self.jumpable:
      ratio = self.scale * abs(self.sprite.getVelocity()[0] / MAX_MOVE_SPEED)
      self.sprite.setVelocity(self.sprite.getVelocity()[0], \
        JUMP * random.uniform(0.95, 1.05) * force + JUMP * ratio * 0.05)
      
  def updateTrace(self):     
      # set jump
      if self.sprite.isGround:
        # reset combo
        if self == gPlayer:
          GameFrame.gGameFrame.board.setCombo(0)
        self.setJump()
        self.setHitForce(0.0)
        
      if self.isMoveLeft:
        vx, vy = self.getVelocity()
        if vy < 0.0:
          vy -= MOVE_ACCELERATE * self.frameTime
        if vx > -MAX_MOVE_SPEED:
          vx -= MOVE_ACCELERATE * self.frameTime
          if vx < -MAX_MOVE_SPEED:
            vx = -MAX_MOVE_SPEED
        self.setVelocity(vx, vy)
      elif self.isMoveRight:
        vx, vy = self.getVelocity()
        if vy < 0.0:
          vy -= MOVE_ACCELERATE * self.frameTime
        if vx < MAX_MOVE_SPEED:
          vx += MOVE_ACCELERATE * self.frameTime
          if vx > MAX_MOVE_SPEED:
            vx = MAX_MOVE_SPEED
        self.setVelocity(vx, vy)
      # decay velocity
      if not self.isMoveLeft and not self.isMoveRight:
          vx, vy = self.getVelocity()
          if vx != 0.0:
            if vx > 0.0:
              vx -= self.frameTime * MOVE_ACCELERATE / max(self.hitForce, 1.0)
              if vx < 0.0:
                vx = 0.0
            else:
              vx += self.frameTime * MOVE_ACCELERATE / max(self.hitForce, 1.0)
              if vx > 0.0:
                vx = 0.0
            self.setVelocity(vx, vy)
  
  def updateFlicker(self):
    self.flickerTime -= Utility.getFrameTime()
    if self.flickerTime < 0.0:
      self.sprite.color.rgba = (1,1,1,1)
    else:
      bright = 1.0 + FLICKER_BRIGHT * abs(math.sin(self.flickerTime * FLICKER_SPEED))
      self.sprite.color.rgba = (bright, bright, bright, bright - 0.7)
  
  def setFlicker(self, flickerTime):
    if self.flickerTime < flickerTime:
      self.flickerTime = flickerTime
      
  def setDamage(self, n=1):
    self.state.setState(self.STATE_CONFUSE)
    gFxMgr.get_emitter(PARTICLE_HIT).play_particle_with(self.sprite, True)
    self.setFlicker(self.confuse_time)
    self.hp -= n
    if self.hp <= 0:
      self.hp = 0
      self.state.setState(self.STATE_DEAD)
      if not self.isPlayer:
        GameFrame.gGameFrame.board.addScore(SCORE_KILL)
    elif not self.isPlayer:
      self.target = gPlayer
        
  def registStates(self):
    self.STATE_DEAD.onEnter = self.stateDeadOnEnter
    
  def stateDeadOnEnter(self):
    self.setDead()
    

class Player(BaseCharacter, Singleton):  
  isPlayer = True
  key_binded = False
  fireTime = 0.5
  maxHp = 500
  weaponClass = WeaponBow
  
  def reset(self, space):
    BaseCharacter.reset(self, space)
    self.fire = False
    self.state.setState(self.STATE_TRACE)
  
  def binding_key(self):
    if not self.key_binded:
      GameFrame.gGameFrame.buttonBind(
            self.setMoveLeft,
            self.setMoveRight)
      self.key_binded = True


class Monster(BaseCharacter):
  def reset(self, space):
    BaseCharacter.reset(self, space)
    self.state.setState(self.STATE_PATROL)
  
  def registStates(self):
    BaseCharacter.registStates(self)
    self.STATE_IDLE.onEnter = self.stateIdleOnEnter  
    self.STATE_IDLE.onUpdate = self.stateIdleOnUpdate
    self.STATE_PATROL.onEnter = self.statePatrolOnEnter  
    self.STATE_PATROL.onUpdate = self.statePatrolOnUpdate  
    self.STATE_TRACE.onEnter = self.stateTraceOnEnter
    self.STATE_TRACE.onUpdate = self.stateTraceOnUpdate 
    self.STATE_TRACE.onExit = self.stateTraceOnExit
    self.STATE_CONFUSE.onEnter = self.stateConfuseOnEnter
    self.STATE_CONFUSE.onUpdate = self.stateConfuseOnUpdate
    
  def stateIdleOnEnter(self):
    self.idleTime = random.uniform(*IDLE_TIME)
    self.setVelocity(0, 0)
    
  def stateIdleOnUpdate(self):
    self.idleTime -= self.frameTime
    if self.idleTime < 0.0:
      self.state.setState(self.STATE_PATROL)
      if self.target and not self.target.isDead:
        self.state.setState(self.STATE_TRACE)
    
  def statePatrolOnEnter(self):
    speed = PATROL_MOVE_SPEED
    if random.uniform(0.0, 1.0) > 0.5:
      speed = -speed
    self.setVelocity(speed, 0)
    self.patrolTime = random.uniform(*PATROL_TIME)
      
  def statePatrolOnUpdate(self):
    self.patrolTime -= self.frameTime
    if self.patrolTime < 0.0:
      self.state.setState(self.STATE_IDLE)
         
    # search target
    target = Player.instance()
    if target and not target.isDead:
      dx = self.getPos()[0] - target.getPos()[0]
      if abs(dx) < self.search_range:
        self.target = target
        self.state.setState(self.STATE_TRACE)
      
  def stateTraceOnEnter(self):
    pass
  
  def stateTraceOnExit(self):
    pass
      
  def stateTraceOnUpdate(self):
    if self.target and not self.target.isDead:
      # update trace
      dx = self.getPos()[0] - self.target.getPos()[0]  
      dy = self.getPos()[1] - self.target.getPos()[1]
      # attack
      if ATTACK_RANGE < abs(dx):
        self.setMoveLeft(dx > 0.0)
        self.setMoveRight(not self.isMoveLeft)
      # evade
      '''
      elif abs(dx) < EVADE_RANGE and dy < 0.0:
        self.setMoveLeft(dx < 0.0)
        self.setMoveRight(not self.isMoveLeft)
      '''
    elif self.sprite.isGround:
      self.target = None
      self.setMoveLeft(False)
      self.setMoveRight(False)
      self.state.setState(self.STATE_PATROL)
  
  def stateConfuseOnEnter(self):
    self.confuseElapseTime = self.confuse_time
  
  def stateConfuseOnUpdate(self):
    self.confuseElapseTime -= self.frameTime
    if self.confuseElapseTime < 0.0:
      if self.target and not self.target.isDead:
        self.state.setState(self.STATE_TRACE)
      else:
        self.state.setState(self.STATE_PATROL) 


class Slime(Monster):
  jumpable = False
  search_range = 0.0
  maxHp = 2
  

class BombSlime(Monster):
  jumpable = False
  search_range = 0.0
  bombTime = BOMB_TIME
  bomb_range = BOMB_RANGE
  bomb_force = BOMB_FORCE
  maxHp = 2
  
  def registStates(self):
    Monster.registStates(self)
    self.STATE_BOMB.onEnter = self.stateBombOnEnter
    self.STATE_BOMB.onUpdate = self.stateBombOnUpdate
  
  def stateBombOnEnter(self):
    self.bombAccTime = self.bombTime
    self.setFlicker(self.bombTime)
    
  def stateBombOnUpdate(self):
    self.bombAccTime -= self.frameTime
    if self.bombAccTime < 0.0:
      self.setExplosion()   
      
  def setExplosion(self):
    if self.bomb_range > getDist(gPlayer.getPos(), self.getPos()):
      gCharacterMgr.process_hit(gPlayer)
      gCharacterMgr.push(gPlayer, self, self.bomb_force)
    gFxMgr.get_emitter(PARTICLE_EXPLOSION).play_particle_with(self.sprite, True)
    self.state.setState(self.STATE_DEAD)
  
  def setDamage(self, n=1):
    BaseCharacter.setDamage(self, n)
    self.state.setState(self.STATE_BOMB)
    

class Archer(Monster):
  jumpable = True
  maxHp = 2
  fireTime = 1.0
  weaponClass = WeaponBow
  
  def reset(self, space):
    BaseCharacter.reset(self, space)
    self.state.setState(self.STATE_TRACE)
    
  def stateTraceOnEnter(self):
    self.fire = True
  
  def stateTraceOnExit(self):
    self.fire = False
  
  def stateTraceOnUpdate(self):
    Monster.stateTraceOnUpdate(self)  
  
  
gCharacterMgr = CharacterMgr.instance()
gPlayer = Player.instance()
