import Utility as Util
from Utility import *
		
#---------------------#
# CLASS : GameRoot
#---------------------#
class GameRoot(FloatLayout):	
	def __init__(self):
		super(GameRoot, self).__init__()
		self.size = Window.size
		Util.gGameRoot = self
		Clock.schedule_interval(self.update, Util.fUpdateTime)
		
	def update(self, frameTime):
		Util.fFrameTime = frameTime
		Util.fGameTime += frameTime
		getDebugPrint().Reset()
		if Util.startPoint:
			Util.startPoint.update()
		
#---------------------#
# CLASS : GameApp
#---------------------#
class GameApp(App):
	bPopup = False
	touchPrev = None
	
	def __init__(self):
		super(GameApp, self).__init__()
		Util.gGameApp = self
	
	def on_pause(self):
		return True
		
	def build(self):		
		Util.fUpdateTime = 1.0/60.0
		Util.bButtonLock = False

		self.bPopup = False
		self.root = FloatLayout()
		self.gameRoot = GameRoot()
		self.root.add_widget(self.gameRoot)
		
		self.debugPrint = DebugPrint()
		Util.gDebugPrint = self.debugPrint
		self.root.add_widget(self.debugPrint)
		self.resetTouchPrev()
		self.bind(on_start = self.post_build_init)
		return self.root
		
	def setTouchPrev(self, func):
		self.touchPrev = func
	
	def resetTouchPrev(self):
		self.touchPrev = None
		
	def onTouchPrev(self):
		if self.touchPrev:
			self.touchPrev()
		else:
			self.popup_Exit()
	
	def popup_Exit(self):
		if self.bPopup:
			return
		self.bPopup = True
		content = Widget()
		sizehintW = 0.9
		sizehintH = 0.2
		btnSizeW = Util.W * sizehintW * 0.5
		btnSizeH = Util.H * sizehintH * 0.5
		popup = Popup(title = "Exit?", content=content, auto_dismiss=False, size_hint = (sizehintW, sizehintH))
		content.pos=popup.pos
		btn_Yes = Button(text='Yes', pos = (Util.cX-btnSizeW*0.1- btnSizeW*0.75, Util.cY - btnSizeH*0.5), size=(btnSizeW*0.75, btnSizeH*0.75))
		btn_No = Button(text='No', pos = (Util.cX+btnSizeW*0.1, Util.cY - btnSizeH*0.5), size=(btnSizeW*0.75, btnSizeH*0.75))
		content.add_widget(btn_Yes)
		content.add_widget(btn_No)
		def closePopup(instance):
			popup.dismiss()
			self.bPopup=False
		btn_Yes.bind(on_press=self.stop)
		btn_No.bind(on_press=closePopup)
		popup.open()

		
	def _key_handler(self, a,b,c,d,e):
		if b == 1001:
			self.onTouchPrev()
					
	def post_build_init(self,ev): 
		android.map_key(android.KEYCODE_MENU, 1000) 
		android.map_key(android.KEYCODE_BACK, 1001) 
		android.map_key(android.KEYCODE_HOME, 1002) 
		android.map_key(android.KEYCODE_SEARCH, 1003) 

		win = self._app_window 
		win.bind(on_keyboard=self._key_handler)