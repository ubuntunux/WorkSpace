import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Point, GraphicException, Line, Quad, Ellipse
from kivy.graphics.opengl import glLineWidth
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

import android
from copy import deepcopy
from cmath import polar, rect
from math import cos,sin,pi,sqrt,atan,atan2
import random
from stateMachine import stateMachine

cx = 0
cy = 0
rootW = rootH = 0
unitW = unitH = 0
global fUpdateTime
fUpdateTime = 1.0/60.0

def nRand(min, max):
	return random.randint(min, max)

def fRand(min, max):
	return random.uniform(min, max)

class Music(Widget):
	sound = None
	def start(self):
		if self.sound is None:
			self.sound = SoundLoader.load("music.ogg")
			self.sound.volume = 0.8
			self.sound.play()
			self.sound.on_stop = self.sound.play
			
class NumButton(Widget):
	isShow = True
	cellPos = [0, 0]
	myNum = 0	
	
	def hide(self):
		if self.isShow:
			self.isShow = False
			
	def show(self):
		if self.isShow == False:
			self.isShow = True
			
	def toggleShow(self):
		if self.isShow:
			self.hide()
		else:
			self.show()
	
	def build_child(self):
		with self.canvas:
			self.image = Rectangle(size=self.size, pos=self.pos, source = "drone.png")
		self.button = Button(text=str(self.myNum), size=self.size, pos=self.pos)
		self.add_widget(self.button)
		
	def update(self):
		self.button.text = str(self.myNum)
		
	def onPress(self, instance, dt):
		instance.button.text="x"

class NumPuzzleGame(Widget):
	szDebug = StringProperty("Lable")
	fTime = NumericProperty(0.0)
	
	STATE_NONE = 0
	STATE_RESET = 1
	STATE_MIX = 2
	STATE_PLAY = 3
	STATE_COMPLETE = 4
	STATE_FAIL = 5
	
	gameState = STATE_NONE
	buttonList = []
	lastButton = None
	numericCount = 0
	numericCols = 0
	numericRows = 0
	oldDir = -1
	curDir = -1
	
	def start(self):
		self.setState(self.STATE_NONE)
		self.music = Music()
		self.add_widget (self.music)
		self.music.start()
		self.buildNumeric()
		
	def buildNumeric(self, cols=0, rows=0):
		self.setState(self.STATE_PLAY)
		self.szDebug=str(stateMachine().state)
		self.curDir = -1
		self.oldDir = -1
		self.fTime = 0.0
		min = 3
		max = 5
		if cols < min : cols= nRand(min,max)
		#if rows < min : rows= nRand(min,max)
		rows = cols
		self.numericCount = cols * rows
		self.numericCols = cols
		self.numericRows = rows
		self.buttonList = range(0, self.numericCount)
		self.numericWidget.clear_widgets()
		
		cellSize = (self.numericWidget.size[0] / cols, self.numericWidget.size[1] / rows)

		for i in range(cols):
			for j in range(rows):
				btn = NumButton(size=cellSize, pos=(i*cellSize[0], self.numericWidget.size[1] - (j+1)*cellSize[1]))
				
				if (i+1) == cols and (j+1) == rows:
					self.lastButton = btn
					
				btn.myNum = 1+i+j*cols
				btn.cellPos = [i, j]
				btn.build_child()
				btn.bind(on_touch_down=btn.onPress)
				self.numericWidget.add_widget(btn)
				self.buttonList[i+j*cols] = btn

	def mixNumeric(self):
		self.szDebug="Mix"
		self.lastButton.hide()
		nRandomCount = self.numericCount ** 2
		checkPos=[[0,1], [1,0], [2,3], [3,2]]
		while nRandomCount:
			targetBtn = [self.lastButton.cellPos[0], self.lastButton.cellPos[1]]
			self.oldDir = self.curDir
			self.curDir = nRand(0,3)
			#check samedir
			for i in range(4):
				if checkPos[i] == [self.oldDir, self.curDir]:
					self.curDir = (self.curDir+nRand(1,3))%4
					break
			
			#left
			if self.curDir == 0:
				if self.lastButton.cellPos[0] == 0:
					targetBtn[0] += 1
				else:
					targetBtn[0] -= 1
			#right
			elif self.curDir == 1:
				if (1+self.lastButton.cellPos[0]) == self.numericCols:
					targetBtn[0] -= 1
				else:
					targetBtn[0] += 1
			#up
			elif self.curDir == 2:
				if self.lastButton.cellPos[1] == 0:
					targetBtn[1] += 1
				else:
					targetBtn[1] -= 1
			#down
			elif self.curDir == 3:
				if (1+self.lastButton.cellPos[1]) == self.numericRows:
					targetBtn[1] -= 1
				else:
					targetBtn[1] += 1
			
			btn = self.buttonList[targetBtn[0] + targetBtn[1]*self.numericCols]
			self.switchButton(btn, self.lastButton)
			#self.printButtonList()
			nRandomCount -= 1
			
		#remix
		if self.checkComplete() == True:
			self.mixNumeric()
			
	def printButtonList(self):
		self.szDebug=""
		for i in self.buttonList:
			self.szDebug = self.szDebug + " " + str(i.myNum)
				
	def pressButton(self, instance, touch):
		if instance == self.lastButton:
			return

		self.szDebug = str(touch.x)+" "+str(touch.y)
		return
		
		bSwitched = 0
		#left
		if instance.cellPos[0] > 0 and [instance.cellPos[0]-1, instance.cellPos[1]] == self.lastButton.cellPos:
			bSwitched = 1
		#right
		elif instance.cellPos[0] < self.numericCols and  [instance.cellPos[0]+1, instance.cellPos[1]] == self.lastButton.cellPos:
			bSwitched = 2
		#up
		elif instance.cellPos[1] > 0 and [instance.cellPos[0], instance.cellPos[1]-1] == self.lastButton.cellPos:
			bSwitched = 3
		#down
		elif instance.cellPos[1] < self.numericRows and [instance.cellPos[0], instance.cellPos[1]+1] == self.lastButton.cellPos:
			bSwitched = 4
		
		if bSwitched:
			self.switchButton(instance, self.lastButton)
			
		if self.checkComplete() == True:
			self.setState(self.STATE_COMPLETE)
			self.lastButton.show()
			
	def switchButton(self, btn1, btn2):
		oldCellPos = btn1.cellPos
		oldPos = btn1.pos
		btn1.cellPos = btn2.cellPos
		btn1.pos = btn2.pos
		btn2.cellPos = oldCellPos
		btn2.pos = oldPos
		self.buttonList[btn1.cellPos[0] + btn1.cellPos[1]*self.numericCols] = btn1
		self.buttonList[btn2.cellPos[0] + btn2.cellPos[1]*self.numericCols] = btn2
		btn1.update()
		btn2.update()
				
	def checkComplete(self):
		for btn in self.buttonList:
			if (1+btn.cellPos[0]+btn.cellPos[1]*self.numericCols) != btn.myNum:
				return False
		self.szDebug="complete"
		return True
		
	def setState(self, state):
		self.gameState = state
	
	def update(self, dt):
		#self.szDebug = str("%.2f" % (1.0/dt))
		self.fTime += dt
		
class NumPuzzleRoot(Widget):
	def start(self):
		self.game = NumPuzzleGame()
		self.game.size = self.size
		self.add_widget (self.game)
		self.game.start()
		Clock.schedule_interval(self.game.update, fUpdateTime )

class NumPuzzleApp(App):
	bPopup = False
	def build(self):
		global rootW, rootH
		global unitW, unitH
		global cx
		global cy
		rootW = Window.size[0]
		rootH = Window.size[1]
		unitW = rootW / 10.0
		unitH = rootH / 10.0
		cx = rootW / 2
		cy = rootH / 2
		self.bPopup = False
		
		self.root = NumPuzzleRoot()
		self.root.size = (rootW, rootH)
		self.root.start()
		self.bind(on_start = self.post_build_init)
		return self.root
		
	def _key_handler(self, a,b,c,d,e):
		if b == 1001 and self.bPopup == False:
			self.bPopup = True
			content = Widget()
			sizehintW = 0.9
			sizehintH = 0.2
			btnSizeW = rootW * sizehintW * 0.5
			btnSizeH = rootH * sizehintH * 0.5
			popup = Popup(title = "Exit?", content=content, auto_dismiss=False, size_hint = (sizehintW, sizehintH))
			content.pos=popup.pos
			btn_Yes = Button(text='Yes', pos = (cx-btnSizeW*0.1- btnSizeW*0.75, cy - btnSizeH*0.5), size=(btnSizeW*0.75, btnSizeH*0.75))
			btn_No = Button(text='No', pos = (cx+btnSizeW*0.1, cy - btnSizeH*0.5), size=(btnSizeW*0.75, btnSizeH*0.75))
			content.add_widget(btn_Yes)
			content.add_widget(btn_No)
			def closePopup(instance):
				popup.dismiss()
				self.bPopup=False
			btn_Yes.bind(on_press=self.stop)
			btn_No.bind(on_press=closePopup)
			popup.open()
		
	def post_build_init(self,ev): 
		android.map_key(android.KEYCODE_MENU, 1000) 
		android.map_key(android.KEYCODE_BACK, 1001) 
		android.map_key(android.KEYCODE_HOME, 1002) 
		android.map_key(android.KEYCODE_SEARCH, 1003) 

		win = self._app_window 
		win.bind(on_keyboard=self._key_handler)

if __name__ in ('__android__', '__main__'):
	NumPuzzleApp().run()