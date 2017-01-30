import Utility as Util
from Utility import *
from Resource import *
import ShowProp

STATE_NONE = 0
STATE_MENU = 1
STATE_RESET = 2
STATE_PLAY = 3
STATE_COMPLETE = 4
STATE_FAIL = 5
STATE_COUNT = 6

#---------------------#
# CLASS : GameStateMgr
#---------------------#
class GameStateMgr(StateMachine):	
	def __init__(self):
		self.addState(StateNone()) # STATE_NONE
		self.addState(StateMenu()) # STATE_MENU
		self.addState(StateItem()) # STATE_RESET
		self.addState(StatePlay()) # STATE_PLAY
		self.addState(StateItem()) # STATE_COMPLETE
		self.addState(StateItem()) # STATE_FAIL
		
		self.setState(STATE_NONE)

# STATE_NONE
class StateNone(StateItem):
	def onUpdate(self):
		self.stateMgr.setState(STATE_MENU)

# STATE_MENU
class StateMenu(Widget, StateItem):
	def __init__(self):
		super(StateMenu,self).__init__()
		with self.canvas:
			self.bgImage = Rectangle(source = szMenu_BG, size = (Util.W, Util.H))
		self.btn_start = getButton("Start", (0.5, 0.7), (0.3, 0.05))
		self.btn_exit = getButton('Exit', (0.5, 0.6), (0.3, 0.05))
		self.btn_start.bind(on_release = self.setPlay)
		self.btn_exit.bind(on_release = self.callback_Exit)
		self.add_widget(self.btn_start)
		self.add_widget(self.btn_exit)
		
	def callback_Exit(self, inst):
		getMyApp().popup_Exit()
		
	def setPlay(self, inst):
		self.stateMgr.setState(STATE_PLAY)
		
	def onEnter(self):
		getMyRoot().add_widget(self)
		getMyApp().resetTouchPrev()
	
	def onExit(self):
		getMyRoot().remove_widget(self)

# STATE_PLAY
class StatePlay(Widget, StateItem):
	def __init__(self):
		super(StatePlay,self).__init__()
		with self.canvas:
			Color(.5,.5,.5)
			Rectangle(size=Util.WH)
		def popup_prop(inst):
			ShowProp.ShowProp_Mgr()
		self.btn_popup = getButton('popup', (0.5, 0.5), (0.3, 0.05))
		self.btn_popup.bind(on_release = popup_prop)
			
		self.btn_exit = getButton('Exit', (0.5, 0.7), (0.3, 0.05))
		self.btn_exit.bind(on_release = self.callback_Exit)
		self.touchRegion = TouchRegion()
		self.enemy = Enemy()
		self.add_widget(self.touchRegion)
		self.add_widget(self.enemy)
		self.add_widget(self.btn_exit)
		self.add_widget(self.btn_popup)

	def callback_Exit(self, inst):
		self.stateMgr.setState(STATE_MENU)
	
	def callback_Prev(self):
		self.stateMgr.setState(STATE_MENU)
		
	def onEnter(self):		
		getMyRoot().add_widget(self)
		getMyApp().setTouchPrev(self.callback_Prev)
		
	def onUpdate(self):
		self.touchRegion.checkTouch()
		
	def onExit(self):
		self.touchRegion.clear_touch()
		getMyRoot().remove_widget(self)

#---------------------#
# CLASS : touchRegion
#---------------------#
class TouchRegion(Widget):
	touch1 = None
	touch2 = None
	
	def __init__(self):
		super(TouchRegion, self).__init__()
		self.size = (Util.W, Util.H*0.5)
		with self.canvas:
			Color(.5,.5,.0)
			Rectangle(size=self.size)
		self.clear_touch()
	
	def on_touch_down(self, touch):
		if self.touch1 == None:
			self.touch1 = touch
		elif self.touch2 == None:
			self.touch2 = touch
		else:
			return
		ud = touch.ud
		ud['label'] = Label(size_hint=(None, None))
		self.update_touch_label(ud['label'], touch)
		self.add_widget(ud['label'])
		touch.grab(self)

	def on_touch_move(self, touch):
		if touch.grab_current is not self:
			return
		self.update_touch_label(touch.ud['label'], touch)
    
	def on_touch_up(self, touch):
		if touch != None and touch.grab_current is not self:
			return
		if self.touch1 == touch:
			self.touch1 = None
		elif self.touch2 == touch:
			self.touch2 = None
			
		touch.ungrab(self)
		self.remove_widget(touch.ud['label'])
	
	def clear_touch(self):
		if self.touch1:
			self.touch1.ungrab(self)
			self.remove_widget(self.touch1.ud['label'])
			self.touch1 = None
		if self.touch2:
			self.touch2.ungrab(self)
			self.remove_widget(self.touch2.ud['label'])
			self.touch2 = None
		
	def update_touch_label(self, label, touch):
		label.text = 'ID: %s\nPos: (%d, %d)\nClass: %s' % (touch.id, touch.x, touch.y, touch.__class__.__name__)
		label.texture_update()
		label.pos = touch.pos
		label.size = label.texture_size[0] + 20, label.texture_size[1] + 20
		
	def checkTouch(self):
		if self.touch1 and self.touch2:
			vec = Vector(self.touch1.x, self.touch1.y) - Vector(self.touch2.x, self.touch2.y)
			dist = vec.length()
			vec = vec.normalize()
			if abs(vec.y) > abs(vec.x):
				getDebugPrint().Print('Scissors')
			elif dist > Util.W * 0.5:
				getDebugPrint().Print('Paper')
			else:
				getDebugPrint().Print('Rock')

#---------------------#
# CLASS : Enemy
#---------------------#
class Enemy(Widget):
	sprite = None
	def __init__(self):
		super(Enemy, self).__init__()
		self.tex = Image(source = szEnemy).texture
		with self.canvas:
			Color(1,1,1)
			self.sprite = Rectangle(texture = self.tex)
		
if __name__ in ('__android__', '__main__'):
	Util.startPoint = GameStateMgr()
	MyApp().run()