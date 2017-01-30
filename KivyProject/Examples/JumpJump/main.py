import Utility as Util
from Utility import *

import MyGame

STATE_ENTER = 0
STATE_START = 1
STATE_PLAY = 2
STATE_EXIT = 3
szDebug = 'none'

#---------------------#
# CLASS : BlankScene
#---------------------#
class BlankScene(Widget):
	def __init__(self, startCallback):
		Widget.__init__(self)
		self.startCallback = startCallback
		self.btn_Start = Button(text='Start')
		self.add_widget(self.btn_Start)
		def run_game(inst):
			self.startCallback()
		self.btn_Start.bind(on_release = run_game)
	
	def preUpdate(self):
		getMyRoot().add_widget(self)
	
	def postUpdate(self):
		if self.parent:
			self.parent.remove_widget(self)

#---------------------#
# CLASS : StateMgr
#---------------------#
class State_Mgr(StateMachine):	
	def __init__(self):
		self.addState(State_Enter()) # STATE_ENTER
		self.addState(State_Start()) # STATE_START
		self.addState(State_Play()) # STATE_PLAY
		self.addState(State_Exit()) # STATE_EXIT
		self.setState(STATE_ENTER)
	
	def onTouchPrev(self):
		curItem = self.getStateItem()
		if curItem:
			return curItem.onTouchPrev()
	
# STATE_ENTER
class State_Enter(StateItem):
	def onUpdate(self):
		self.setState(STATE_START)

# STATE_START
class State_Start(StateItem):
	def __init__(self):
		self.Scene = BlankScene(self.next)

	def onEnter(self):
		self.Scene.preUpdate()
		
	def next(self):
		self.Scene.postUpdate()
		self.setNext()

# STATE_PLAY
class State_Play(StateItem):
	def __init__(self):
		self.MyGame = MyGame.MyGame()

	def onEnter(self):
		self.MyGame.preUpdate()
	
	def onUpdate(self):
		self.MyGame.onUpdate()
	
	def onTouchPrev(self):
		self.setPrev()
	
	def onExit(self):
		self.MyGame.postUpdate()

# STATE_EXIT
class State_Exit(StateItem):
	def onEnter(self):
		getMyApp().stop()

if __name__ in ('__android__', '__main__'):
	Util.MyApp().start( State_Mgr() )