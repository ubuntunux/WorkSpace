import Utility as Util
from Utility import *

MYGAME_ENTER = 0
MYGAME_START = 1
MYGAME_EXIT = 2

#---------------------#
# CLASS : MyGameStateMgr
#---------------------#
class MyGame_Mgr(StateMachine):
	def __init__(self):
		self.inited = False
		self.addState(MyGame_Enter()) # MYGAME_ENTER
		self.addState(MyGame_Start()) # MYGAME_START
		self.addState(MyGame_Exit()) # MYGAME_EXIT
		self.run()
		Util.getMyApp().setTouchPrev(self.exit)

	def setInited(self, inited):
		self.inited = inited
		
	def run(self):
		if self.inited != True:
			self.setInited(True)
			self.setState(MYGAME_ENTER)
			Util.getMyRoot().regist(self)
	
	def exit(self):
		self.setInited(False)
		self.setState(MYGAME_EXIT)
		Util.getMyApp().resetTouchPrev()
		Util.getMyRoot().remove(self)

# MYGAME_ENTER
class MyGame_Enter(StateItem):		
	def onUpdate(self):
		self.setState(MYGAME_START)

# MYGAME_START
class MyGame_Start(Widget, StateItem):			
	def onEnter(self):
		Util.getMyRoot().add_widget(self)
		
	def onExit(self):
		Util.getMyRoot().remove_widget(self)

# MYGAME_EXIT
class MyGame_Exit(StateItem):
	pass