import Utility as Util
from Utility import *
from kivy.animation import Animation

from Globals import *
from Particle import *
from ResourceMgr import *
from Character import *
from World import *

#---------------------#
# Global Instance
#---------------------#
def setGlobalInstance():
  global gMyGame, gGameScreen
  gGameScreen = MyGame_Screen.instance()
  gMyGame = MyGame_Mgr.instance()

#---------------------#
# Class
#---------------------#
# MYGAME_SCREEN
class MyGame_Screen(Screen, Singleton):      
  def __init__(self):
    Screen.__init__(self, name="MyGame")
  
  def build_ui(self):
    # add bg
    self.layer_bg = Widget()
    self.layer_bg.name="layer_bg"
    self.add_widget(self.layer_bg)

    # add fx layer
    self.layer_fx = Widget()
    self.layer_fx.name = "layer_fx"
    self.add_widget(self.layer_fx)
    
    # add ui layer
    self.layer_ui = Widget()
    self.layer_ui.name = "layer_ui"
    self.add_widget(self.layer_ui)
    
    # overlay
    self.layer_overlay = Widget()
    self.layer_overlay.name = "overlay"
    with self.layer_overlay.canvas:
      self.overlay_color = Color(0,0,0)
      Rectangle(pos=(0,0), size=WH)
      
  def screen_black(self):
    if not self.layer_overlay.parent:
      self.add_widget(self.layer_overlay)
    self.overlay_color.a = 1.0
    
  def screen_transition(self):
    def detach(inst):
      if self.layer_overlay.parent:
        self.remove_widget(self.layer_overlay)
        
    if not self.layer_overlay.parent:
      self.add_widget(self.layer_overlay)
    self.overlay_color.a = 1.0
    anim = Animation(a = 0.0, duration = 0.3)
    anim.start(self.overlay_color)
    Clock.schedule_once(detach, 0.4)

  def create_screen(self):
    self.build_ui()
    gMyRoot.add_screen(self)
    gMyRoot.current_screen(self)
    
  def remove_screen(self):
    gMyRoot.remove_screen(self)
    self.clear_screen()

  def clear_screen(self):
    self.clear_widgets()
    self.clear_bg()
    self.clear_fx()
    self.clear_ui()
  
  def clear_fx(self): self.layer_fx.clear_widgets() 
  def clear_ui(self): self.layer_ui.clear_widgets()
  def clear_bg(self): self.layer_bg.clear_widgets()
  def add_to_fx(self, widget): self.layer_fx.add_widget(widget)
  def add_to_ui(self, widget): self.layer_ui.add_widget(widget)   
  def add_to_bg(self, widget): self.layer_bg.add_widget(widget)
  def remove_from_fx(self, widget):
    if widget in self.layer_fx.children:
      self.layer_bg.remove_widget(widget)
  def remove_from_bg(self, widget):
    if widget in self.layer_bg.children:
      self.layer_bg.remove_widget(widget)
  def remove_from_ui(self, widget):
    if widget in self.layer_ui.children:
      self.layer_ui.remove_widget(widget)

#---------------------#
# CLASS : MyGameStateMgr
#---------------------#
class MyGame_Mgr(Singleton): 
  def __init__(self):
    self.running = False
    self.onExitFunc = None
    self.filename = ""
   
  def bind_OnExit(self, func):
    self.onExitFunc = func

  def callback_exit(self):
    '''call by gWorldEdit.onTouchPrev'''
    self.running = False
    gFxMgr.setActive(False)
    gFxMgr.remove_emitters()
    gGameScreen.remove_screen()
    gMyRoot.remove(self)
    if self.onExitFunc:
      self.onExitFunc()
    gMyRoot.setTouchPrev(None)
      
  def update(self, dt):
    pass
    
  def load(self, filename):
    if self.running:
      return
    self.running = True
    self.filename = filename
    # regist
    gMyRoot.regist(self)
    gGameScreen.create_screen()
    gWorldEdit.bind_OnExit(self.callback_exit)
    gWorldEdit.load(self.filename, gGameScreen)
   
#---------------------#
# set global instance
#---------------------#
setGlobalInstance()