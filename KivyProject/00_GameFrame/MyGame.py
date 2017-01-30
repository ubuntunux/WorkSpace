import Utility as Util
from Utility import *

from Sprite import Sprite, gSpriteMgr
from Particle import *
from ResourceMgr import *

#---------------------#
# Global Instance
#---------------------#
def setGlobalInstance():
  global gMyGame, gGameScreen
  gGameScreen = MyGame_Screen.instance()
  gMyGame = MyGame_Mgr.instance()
  
#---------------------#
# Global variable
#---------------------#
gPlayer = None
gCheckAngle = 0.707
gFriction = 10.0
gMaxSpeed = 60.0
gGround = Util.H * 0.05
gJump = Util.H * 1.8
gVel = Util.W * 0.8
gWalk = Util.W * 0.3
gIncVel = Util.W * 1.6
gDecVel = Util.W * 2.5
gRange = Util.W * 0.3
gUnitSize = [Util.H*.18]*2
gCenter = mul(Util.WH, 0.5)
gWorldSize = mul(Util.WH, (1.0, 1.0))
gGravity = H * 5.5

# MYGAME_SCREEN
class MyGame_Screen(Screen, Singleton):      
  def __init__(self):
    Screen.__init__(self, name="MyGame")
    self.popup_widget = None

    # add bg
    self.layer_bg = Widget()
    with self.layer_bg.canvas:
      Rectangle(texture=gResMgr.getTexture('bg01'), size=gWorldSize)
    self.add_widget(self.layer_bg)

    # add fx layer
    self.layer_fx = Widget()
    self.add_widget(self.layer_fx)
    
    # add ui layer
    self.layer_ui = Widget()
    self.btn_exit = Button(text='exit', center=Util.cXY)
    self.layer_ui.add_widget(self.btn_exit)
    self.add_widget(self.layer_ui)
    
  def bind_OnExit(self, func):
    self.btn_exit.bind(on_release=func)
    
  def create_screen(self):
    gMyRoot.add_screen(self)
    gMyRoot.current_screen(self)
    self.popup_create()
    
  def remove_screen(self):
    gMyRoot.remove_screen(self)
    self.layer_bg.clear_widgets()
    self.layer_fx.clear_widgets()
    
  def add_to_bg(self, widget):
    self.layer_bg.add_widget(widget)
    
  def popup_create(self):
    if self.popup_widget:
      return
    content = Widget(size=mul(WH,0.5))
    self.popup_widget = Popup(title = "Name", content=content, auto_dismiss=False,  size_hint=(0.5,0.5))
    btn_Yes = Button(text='Yes', size=(200,100))
    btn_No = Button(text='No', size=(200,100))
    content.add_widget(btn_Yes)
    content.add_widget(btn_No)
    btn_Yes.center=(cX, cY+50)
    btn_No.center=(cX, cY-50)
    btn_Yes.bind(on_pres=self.remove_popup)
    btn_No.bind(on_press=self.remove_popup)
    self.popup_widget.open()
 
  def remove_popup(self, *args):
    if self.popup_widget:
      self.popup_widget.dismiss()
      self.popup_widget = None
      return True
    else:
      return False

#---------------------#
# CLASS : MyGameStateMgr
#---------------------#
class MyGame_Mgr(StateMachine, Singleton): 
  def __init__(self):
    self.running = False
    self.onExitFunc = None
    self.addState(MyGame_Start)
    self.addState(MyGame_Exit)
    gGameScreen.bind_OnExit(self.onTouchPrev)
  
  def bind_OnExit(self, func):
    self.onExitFunc = func

  def run(self):
    if self.running:
      return
    self.running = True
    gMyRoot.regist(self)
    gMyRoot.setTouchPrev(self.onTouchPrev)
    self.setState(MyGame_Start)

  def onTouchPrev(self, *args):
    if gGameScreen.remove_popup():
      return
    self.running = False
    gMyRoot.remove(self)
    self.setState(MyGame_Exit)
    if self.onExitFunc:
      self.onExitFunc()
    gMyRoot.setTouchPrev(None)

# MYGAME_START
class MyGame_Start(StateItem):
  def onEnter(self):
    # create screen
    gGameScreen.create_screen() 
    # init fx manager
    gFxMgr.setLayer(gGameScreen.layer_fx)
    gFxMgr.setActive(True)
    # sprite manager
    gSpriteMgr.reset()
    
    # add star
    sprite1 = Sprite(size=(500,500), vel=[500,500], rotateVel=360, scaling=0.5, texture=gResMgr.getTexture('star'), gravity=980, collision=True)
    sprite2 = Sprite(pos=(200,200), size=(500,500), vel=[500,500], rotateVel=180, scaling=0.5, texture=gResMgr.getTexture('star'), gravity=80, collision=True)
    gGameScreen.add_to_bg(sprite1)
    gGameScreen.add_to_bg(sprite2)
    
    # create a particle
    particleInfo = dict(loop=-1,texture=gResMgr.getTexture('explosion'), fade=1, delay=Var(0.0,1.0), rotateVel=Var(360.0), rotate=Var(0.0, 360), offset=Var((-20,20), (-20,20)),
      lifeTime=Var(0.5,1.5), sequence=[4,4], vel=Var([gVel*0.1, gJump*0.1], [-gVel*0.1, gJump*0.25]), scaling=Var(1.0, 2.5), gravity=Var(0.0))
    gFxMgr.create_emitter('explosion1', particleInfo, 20)
    gFxMgr.create_emitter('explosion2', particleInfo, 20)
    
    gFxMgr.get_emitter('explosion1').play_particle_with(sprite1, True)
    gFxMgr.get_emitter('explosion2').play_particle_with(sprite2, True)  
    
  def onExit(self):
    gSpriteMgr.reset()
    gFxMgr.setActive(False)
    gFxMgr.remove_emitters()
    gGameScreen.remove_screen()

# MYGAME_EXIT
class MyGame_Exit(StateItem):
  pass
  
#---------------------#
# set global instance
#---------------------#
setGlobalInstance()