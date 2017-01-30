import Utility as Util
from Utility import *
import math
from kivy.graphics import Scale, Rotate, PushMatrix, PopMatrix, Translate, \
                          UpdateNormalMatrix

class Sprite(Widget):
  def __init__(self, *args, **kargs):
    Widget.__init__(self)
    self.box = None
    self.boxPos = None
    self.boxRot = None
    self.boxScale = None
    self.texture = None
    self.collision = False
    self.elastin = 0.8
    self.gravity = 980.0
    self.vel = [0.0, 0.0]
    self.rotateVel = 0.0
    self.rotate = 0.0
    self.scaling = 1.0
    self.opacity = 1.0
    self.offset = (0.0, 0.0)
    # clamp
    self.elastin = max(min(self.elastin, 1.0), 0.0)
    
    if texture == None:
      if source != None:
        self.texture = Image(source = source).texture
    else:
      self.texture = texture
      
    if self.texture:
      with self.canvas:
        Color(1,1,1,1)
        self.box = Rectangle(texture=self.texture, pos=(0,0), size=self.size)
      with self.canvas.before:
        PushMatrix()
        self.boxPos = Translate(0,0)
        self.boxRot = Rotate(angle=0, axis=(0,0,1), origin=mul(mul(self.size, 0.5), self.scaling))
        self.boxScale = Scale(1,1,1)
      with self.canvas.after:
        PopMatrix()
        
    self.vel = div(self.vel, self.scaling)
    self.boxPos.x = -self.size[0] * 0.5 + self.offset[0]
    self.boxPos.y = -self.size[1] * 0.5 + self.offset[1]
    self.boxRot.origin = origin = mul(mul(self.size, 0.5), self.scaling)
    self.boxRot.angle = self.rotate
    self.boxScale.xyz = (self.scaling, self.scaling, self.scaling)

  def update(self, fFrameTime):
    if self.gravity != 0:
      self.vel[1] -= self.gravity * fFrameTime
    
    # adjust velocity, move
    if self.collision:
      self.boxPos.x += self.vel[0] * fFrameTime
      self.boxPos.y += self.vel[1] * fFrameTime
      if self.boxPos.x < 0.0:
        self.boxPos.x = -self.boxPos.x
        self.vel[0] = -self.vel[0] * self.elastin
      elif self.boxPos.x > Util.W - self.size[0]:
        self.boxPos.x = (Util.W - self.size[0])* 2.0 - self.boxPos.x
        self.vel[0] = -self.vel[0] * self.elastin
      if self.boxPos.y < 0.0:
        self.boxPos.y = -self.boxPos.y
        self.vel[1] = -self.vel[1] * self.elastin
      elif self.boxPos.y > Util.H - self.size[1]:
        self.boxPos.y = (Util.H - self.size[1]) * 2.0 - self.boxPos.y
        self.vel[1] = -self.vel[1] * self.elastin
    else:
      if self.vel[0] != 0:
        self.boxPos.x += self.vel[0] * fFrameTime
      if self.vel[1] != 0:
        self.boxPos.y += self.vel[1] * fFrameTime

    if self.rotateVel != 0.0:
      self.boxRot.angle += self.rotateVel * fFrameTime