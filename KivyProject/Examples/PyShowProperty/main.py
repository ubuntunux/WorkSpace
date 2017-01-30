import Utility as Util
from Utility import *

import ShowProp

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
	Prop = None
	
	def callback_Exit(self, inst = None):
		getMyApp().popup_Exit()

	def onEnter(self):
		getMyRoot().add_widget(self)
		getMyApp().setTouchPrev(self.callback_Exit)
		self.btn_Prop = Button(text='Prop')
		self.add_widget(self.btn_Prop)
		def run_showProp(inst):
			if self.Prop == None:
				self.Prop = ShowProp.ShowProp_Mgr()
			else:
				self.Prop.run()
		self.btn_Prop.bind(on_release = run_showProp)

# STATE_EXIT
class State_Exit(StateItem):
	pass
				
if __name__ in ('__android__', '__main__'):
	Util.MyApp().start( State_Mgr() )