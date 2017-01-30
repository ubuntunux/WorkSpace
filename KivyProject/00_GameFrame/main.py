import Utility as Util
from Utility import *

from MyGame import gMyGame
from ResourceMgr import resourceViewer
from toast import toast

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
    layout = BoxLayout(orientation="vertical", size_hint=(0.2, 0.3), center=cXY)
    self.add_widget(layout)
    
    # start button
    self.btn_Start = Button(text='Start')
    self.btn_Start.bind(on_release = lambda x:self.stateMgr.run_MyGame())
    layout.add_widget(self.btn_Start)
    
    # resource viewer button
    self.btn_Resource = Button(text='Resource Viewer')
    self.btn_Resource.bind(on_release = lambda x:resourceViewer.openWidget(callbackOnClose=toast))
    layout.add_widget(self.btn_Resource)
    
    # exit button 
    self.btn_Exit = Button(text="Exit")  
    def exit(inst):
      gMyRoot.remove_screen(self)
      self.setState(State_Exit)
    self.btn_Exit.bind(on_release = exit)
    layout.add_widget(self.btn_Exit)
    
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