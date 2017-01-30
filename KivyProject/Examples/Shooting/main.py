import Utility as Util
from Utility import *

import MyGame

STATE_ENTER = 0
STATE_START = 1
STATE_EXIT = 2
szDebug = 'none'

#---------------------#
# CLASS : StateMgr
#---------------------#
class State_Mgr(StateMachine):	
	def __init__(self):
		self.addState(State_Enter()) # STATE_ENTER
		self.addState(State_Start()) # STATE_START
		self.addState(State_Exit()) # STATE_EXIT
		self.setState(STATE_ENTER)
	
# STATE_ENTER
class State_Enter(StateItem):
	def onUpdate(self):
		self.setState(STATE_START)

# STATE_START
class State_Start(Widget, StateItem):
	def __init__(self):
		Widget.__init__(self)
		self.myGame = None
		
	def callback_Exit(self, inst = None):
		getMyApp().popup_Exit()

	def onEnter(self):
		getMyRoot().add_widget(self)
		getMyApp().setTouchPrev(self.callback_Exit)
		
		self.btn_Start = Button(text='Start')
		self.add_widget(self.btn_Start)
		def run_game(inst):
			if self.myGame == None:
				self.myGame = MyGame.MyGame_Mgr()
			else:
				self.myGame.run()
		self.btn_Start.bind(on_release = run_game)

# STATE_EXIT
class State_Exit(StateItem):
	def onEnter(self):
		getMyApp().stop()

if __name__ in ('__android__', '__main__'):
	Util.MyApp().start( State_Mgr() )