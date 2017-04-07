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
import Character


def check_collide(pos1, size1, pos2, size2):
  if pos1[0] > pos2[0] + size2[0] or \
    pos2[0] > pos1[0] + size1[0]:
      return False
  if pos1[1] > pos2[1] + size2[1] or \
    pos2[1] > pos1[1] + size1[1]:
      return False
  return True


class WeaponMgr(Singleton):
  def __init__(self):
    self.bullets = []
    self.parentLayer = None
    self.space = None
    
  def __del__(self):
    self.clear(None, None)
    
  def clear(self):
    for bullet in self.bullets:
      bullet.setDead()
    self.bullets = []
    
  def reset(self, parentLayer, space):
    self.clear()
    self.parentLayer = parentLayer
    self.space = space
  
  def regist(self, bullet):
    self.bullets.append(bullet)
  
  def update(self):
    dt = Utility.getFrameTime()
    for bullet in self.bullets:
      bullet.update(dt) 
    
    i = 0
    while i < len(self.bullets):
      if self.bullets[i].isDead:
        a = self.bullets.pop(i)
      else:
        i += 1
        

class WeaponBase:
  life_time = 1.0
  velocity = (BULLET_SPEED, 0.0)
  gravity = GRAVITY
  
  def __init__(self, owner):
    self.isDead = False
    self.fire = False
    self.damage = 1.0
    self.elapsed_time = 0.0
    self.owner = owner
    self.size = mul(CHARACTER_SIZE, 0.5)
  
  def __del__(self):
    self.setDead()
    
  def setFire(self, pos, isLeft):
    weaponMgr = WeaponMgr.instance()
    self.fire = True
    self.isDead = False
    self.elapsed_time = 0.0
    if isLeft:
      self.velocity = mul(self.velocity, -1.0)
    texture = gResMgr.getTexture('star')
    space = weaponMgr.space
    self.sprite = Sprite(pos=(0,0), size=self.size, gravity=self.gravity,
      elastin=1.0, collision=True, collisionSpace=(0, space[1], 0, space[3]), texture=texture)
    self.sprite.setPos(*pos)
    weaponMgr.parentLayer.add_widget(self.sprite)
    weaponMgr.regist(self)
  
  def setDead(self):
    self.isDead = True
    if self.sprite.parent:
      self.sprite.parent.remove_widget(self.sprite)
    
  def update(self, dt):
    if self.isDead:    
      return
      
    self.elapsed_time += dt
    
    if self.elapsed_time > self.life_time:
      self.setDead()
      
    if self.fire:
      pos = add(self.sprite.getPos(), mul(self.velocity, dt))
      self.sprite.setPos(*pos)
      characterMgr = Character.CharacterMgr.instance()
      if self.owner.isPlayer:
        for monster in characterMgr.getMonsters():
          if check_collide(self.sprite.getPos(), self.size, monster.getPos(), monster.getSize()):
            monster.setDamage(self.damage)
            self.setDead()
            break
      else:
        player = Character.Player.instance()
        if check_collide(self.sprite.getPos(), self.size, player.getPos(), player.getSize()):
          player.setDamage(self.damage)
          self.setDead()

     
class WeaponBow(WeaponBase):
  life_time = 1.0
  velocity = (BULLET_SPEED, 0.0)
  gravity = 0.0
