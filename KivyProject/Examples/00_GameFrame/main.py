import Utility as Util
from Utility import *

from MyGame import gMyGame

szDebug = 'none'

#---------------------#
# CLASS : MainMenu
#---------------------#
class MainMenu_Mgr(StateMachine, Singleton): 
  def __init__(self):
    self.addState(State_Start)
    self.addState(State_Exit)
    self.setState(State_Start)
  
  def run_MyGame(self):
    gMyRoot.remove(self)
    gMyGame.bind_OnExit(self.callback_OnExit)
    gMyGame.run()
    
  def callback_OnExit(self):
    gMyRoot.regist(self)
    self.setState(State_Start)
    
# STATE_START
class State_Start(Screen, StateItem):
  def __init__(self):
    Screen.__init__(self, name="MainMenu")
    # start button
    self.btn_Start = Button(text='Start', size_hint=(.1,.1), center=[Util.W*0.5, Util.H*0.5])
    self.btn_Start.bind(on_release = lambda x:self.stateMgr.run_MyGame())
    self.add_widget(self.btn_Start)
    
    # exit button 
    self.btn_Exit = Button(text="Exit", size_hint=(.1,.1), center=(Util.W*0.5, Util.H*0.5-100))
    def exit(inst):
      gMyRoot.remove_screen(self)
      self.setState(State_Exit)
    self.btn_Exit.bind(on_release = exit)
    self.add_widget(self.btn_Exit)
    
    # add screen
    gMyRoot.add_screen(self)
  
  def onEnter(self):
    gMyRoot.current_screen(self)

# STATE_EXIT
class State_Exit(StateItem):
  def onEnter(self):
    gMyRoot.exit()

if __name__ in ('__android__', '__main__'):
  gMyRoot.run( MainMenu_Mgr.instance() )