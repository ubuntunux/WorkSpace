import Utility as Util
from Utility import *

import Animal
from Animal import *
from Particle import *
from Shaders import *

from ResourceMgr import ResourceMgr as ResMgr

global gMyGame
gMyGame = None

gCenter = mul(Util.WH, 0.5)
gWorldSize = mul(Util.WH, (3.0, 2.0))
Animal.gWorldSize = gWorldSize 
 
class Music():
 def __init__(self):
  self.sound = None
  
 def start(self):
  return
  if self.sound is None:
   self.sound = SoundLoader.load("music.ogg")
   self.sound.volume = 0.8
   self.sound.play()
   self.sound.on_stop = self.sound.play

class SceneButtons():
 def __init__(self, parent_layer):
  btnsize = [Util.H*0.3]*2
  self.btn_left=Button(text='Left', size=btnsize, pos=(0,0), opacity = .5)
  self.btn_right=Button(text='Right', size=btnsize, pos=(Util.W-btnsize[0],0), opacity=.5)
  parent_layer.add_widget(self.btn_left)
  parent_layer.add_widget(self.btn_right)

class MyGame(Widget):
 def __init__(self):
  Widget.__init__(self, size=Util.WH, orientation='vertical')
  global gMyGame
  gMyGame=self
  # create layers
  self.layer_background = RelativeLayout ()
  self.layer_fx = RelativeLayout ()
  self.layer_buttons = Widget()
  #create managers
  self.ResMgr = ResMgr()
  self.FxMgr = FxMgr(self.layer_fx)
  self.AIMgr = AIMgr(self.layer_background)
  # add widgets
  self.add_widget(self.layer_background)
  self.background = Widget()
  with self.layer_background.canvas:
   Rectangle(texture=self.ResMgr.getTex('bg01'), size=gWorldSize)
  self.add_widget(self.layer_fx)
  self.add_widget(self.layer_buttons)
  
  self.buttons = SceneButtons(self.layer_buttons)
  self.music = Music()
  self.music.start()

 def preload_Fx(self):
  particleInfo = dict(loop=1, texture=self.ResMgr.getTex('star'), 
   vel=Var([gVel*2.0, gJump*0.5], [gVel*-2.0, gJump*1.5]), scale=Var(.5, 1.5))
  self.FxMgr.create_emitter('star', particleInfo, 3)
   
 def preUpdate(self):
  getMyRoot().add_widget(self)
  #load fx
  self.preload_Fx()
  #create player
  res = self.ResMgr.getResource('bee')
  self.player = AnimalPlayer(res)
  self.layer_background.add_widget(self.player)
  self.buttons.btn_left.bind(on_press=self.player.set_left)
  self.buttons.btn_left.bind(on_release=self.player.release_left)
  self.buttons.btn_right.bind(on_press=self.player.set_right)
  self.buttons.btn_right.bind(on_release=self.player.release_right)
  #create ai
  for i in range(5):
   res = self.ResMgr.getResource_Rnd()
   self.AIMgr.add_ai(res, 1)
  self.AIMgr.setPlayer(self.player)
  
 def postUpdate(self):
  self.parent.remove_widget(self)
  #remove fx
  self.FxMgr.remove_emitter()
  #remove player
  self.player.setDead()
  self.player = None
  #remove ai
  self.AIMgr.remove_ai()

 def onUpdate(self):
  self.FxMgr.onUpdate()
  self.player.onUpdate()
  self.AIMgr.onUpdate()
  offset_x = 0.0
  offset_y = 0.0  
  if self.player.pos[0] < gCenter[0]:
   offset_x = 0.0
  elif self.player.pos[0] > gWorldSize[0] - gCenter[0]:
   offset_x = gWorldSize[0] - Util.W
  else:
   offset_x = self.player.pos[0] - gCenter[0] 
  if self.player.pos[1] < gCenter[1]:
   offset_y = 0.0
  elif self.player.pos[1] > gWorldSize[1] - gCenter[1]:
   offset_y = gWorldSize[1] - Util.H
  else:
   offset_y = self.player.pos[1] - gCenter[1] 
  self.layer_background.pos = (-offset_x,-offset_y)
  self.layer_fx.pos = (-offset_x,-offset_y)