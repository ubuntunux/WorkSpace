import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.factory import Factory
from kivy.graphics import Color, Rectangle, Point, GraphicException, Line, Quad, Ellipse
from kivy.graphics.opengl import glLineWidth
from kivy.logger import Logger
from kivy.vector import Vector
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.vector import Vector

import android
from cmath import polar, rect
from copy import deepcopy
from math import cos,sin,pi,sqrt,atan,atan2
from glob import glob
from os.path import join, dirname, basename, sep
import random
from random import choice, shuffle

from state import * 

def nRand(min, max):
	return random.randint(min, max)

def fRand(min, max):
	return random.uniform(min, max)

def getCenterPos():
	global cx, cy
	return (cx, cy)

def calcCenterPos(pos, size):
	return (pos[0]+size[0]/2.0, center_pos[1]+size[1]/2.0)
	 	
def calcPos(center_pos, size):
	return (center_pos[0]-size[0]/2.0, center_pos[1]-size[1]/2.0)

def calcSize(size, ratioX, ratioY):
		return (size[0]*ratioX, size[1]*ratioY)

class Music(Widget):
	sound = None
	def start(self):
		if self.sound is None:
			self.sound = SoundLoader.load("music.ogg")
			self.sound.volume = 0.8
			self.sound.play()
			self.sound.on_stop = self.sound.play
			
class NumButton(Scatter):
	isShow = True
	cellPos = [0, 0]
	targetPos = [0, 0]
	outline = None
	myNum = 0
	
	def hide(self):
		if self.isShow:
			self.isShow = False
			self.btn.text = ""
			self.btn.background_color = (0,0,0,1.0)
			#self.opacity=0
			
	def show(self):
		if self.isShow == False:
			self.isShow = True
			self.btn.text = str(self.myNum)
			self.btn.background_color = (0,0,0,0.0)
			#self.opacity=
			
	def toggleShow(self):
		if self.isShow:
			self.hide()
		else:
			self.show()
			
	def build(self, source, i, j, cols, rows, onpress):
		self.do_translation = False
		self.do_rotation = False
		self.do_Scale = False

		self.myNum = 1+i+j*cols
		self.cellPos = [i, j]
		self.btn=Button(text = "[color=000000]" + str(self.myNum) + "[/color]", size = self.size, font_size = 70, markup = True)
		self.btn.background_color = (10.0, 10.0, 10.0, 0.2)
		self.btn.bind(on_press=onpress)
		texture = Image(source = source).texture
		texture.uvpos=(float(i)/cols, float(j+1)/rows)
		texture.uvsize=(1.0/cols, -1.0/rows)
		with self.canvas:
			Rectangle(texture=texture, size=self.size)
			Color(0,0,0,0.5)
			self.outline = Line(points=[0, 0, self.size[0], 0, self.size[0], self.size[1], 0, self.size[1]], joint = 'round', width = self.size[0]/50.0, close = True)

		self.add_widget(self.btn)
	
	def onPress(self, bCorrect):
		if bCorrect:
			clickSnd.stop()
			clickSnd.play()
		else:
			wrongSnd.stop()
			wrongSnd.play()
		
class NumPuzzleGame(Widget, NumPuzzleGameBase):
	szDebug = StringProperty("Lable")
	fTime = NumericProperty(0.0)
	
	def start(self):
		#self.music = Music()
		#self.add_widget(self.music)
		#self.music.start()
		self.loadData()
		super(NumPuzzleGame, self).start()
		
	def loadData(self):
		#load images
		curdir = dirname(__file__)
		self.icons = glob(join(curdir, 'images', '*.png'))
		
		#load sounds
		self.sounds = {}
		for s in glob(join(curdir,"sounds", '*.wav')):
			name = basename(s[:-4]).split("_")[0]
			if self.sounds.has_key(name):
				self.sounds[name].append(s)
			else:
				self.sounds[name]=[s]
				
	def loadMySound(self, iconFile):
		key = iconFile.split(".png")[0].split(sep)[1]
		if self.sounds.has_key(key):
			self.mySound = SoundLoader.load(choice(self.sounds[key]))
		else:
			self.mySound = SoundLoader.load(choice(self.sounds['default']))
		if self.mySound:
			self.mySound.volume = 1.0

	def playMySound(self):
		if self.mySound:
			self.mySound.stop()
			self.mySound.play()
			
	def getIconFile(self):
		return choice(self.icons)
		
	def setReset(self):
		gameState.set_state(STATE_RESET)
	
	# buildNumeric
	def buildNumeric(self, cols=0, rows=0):
		self.curDir = -1
		self.oldDir = -1
		self.fTime = 0.0
		min = 3
		max = 5
		if cols < min : cols= nRand(min,max)
		#if rows < min : rows= nRand(min,max)
		rows = cols
		
		self.vMoveVel = 20.0*(self.numericWidget.size[0] / cols)
		
		self.numericCount = cols * rows
		self.numericCols = cols
		self.numericRows = rows
		self.buttonList = range(0, self.numericCount)
		self.numericWidget.clear_widgets()
		
		cellSize = (self.numericWidget.size[0] / cols, self.numericWidget.size[1] / rows)
	
		#set iconFile and load sound
		source = self.getIconFile()
		self.loadMySound(source)
		self.playMySound()
		
		for i in range(cols):
			for j in range(rows):
				btn = NumButton(size=cellSize, pos=(i*cellSize[0], self.numericWidget.size[1] - (j+1)*cellSize[1]))
				
				if (i+1) == cols and (j+1) == rows:
					self.lastButton = btn
					
				btn.build(source, i, j, cols, rows, self.pressButton)
				self.numericWidget.add_widget(btn)
				self.buttonList[i+j*cols] = btn
	
	# mixNumeric
	def mixNumeric(self):
		targetBtn = [self.lastButton.cellPos[0], self.lastButton.cellPos[1]]
		nextPos=[[2,3], [2,3], [0,1], [0,1]]
		self.oldDir = self.curDir
		self.curDir = nextPos[self.oldDir][nRand(0,1)]
		
		#left
		if self.curDir == 0:
			if self.lastButton.cellPos[0] == 0:
				targetBtn[0] += 1
				self.curDir = 1
			else:
				targetBtn[0] -= 1
		#right
		elif self.curDir == 1:
			if (1+self.lastButton.cellPos[0]) == self.numericCols:
				targetBtn[0] -= 1
				self.curDir = 0
			else:
				targetBtn[0] += 1
		#up
		elif self.curDir == 2:
			if self.lastButton.cellPos[1] == 0:
				targetBtn[1] += 1
				self.curDir = 3
			else:
				targetBtn[1] -= 1
		#down
		elif self.curDir == 3:
			if (1+self.lastButton.cellPos[1]) == self.numericRows:
				targetBtn[1] -= 1
				self.curDir = 2
			else:
				targetBtn[1] += 1
			
		btn = self.buttonList[targetBtn[0] + targetBtn[1]*self.numericCols]
		self.switchButton(btn, self.lastButton, True)
			
	# printButtonList
	def printButtonList(self):
		self.szDebug=""
		for i in self.buttonList:
			self.szDebug = self.szDebug + " " + str(i.myNum)
				
	# pressButton 		
	def pressButton(self, instance):
		if gameState.is_state(STATE_PLAY) != True or self.isMoveButton():
			return
		instance = instance.parent
		if instance == self.lastButton:
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
		
		#clickSnd	
		instance.onPress(bSwitched)
		
		if bSwitched:
			self.switchButton(instance, self.lastButton, True)
			
		if self.checkComplete() == True:
			gameState.set_state(STATE_COMPLETE)
			self.lastButton.show()
			
	def switchButton(self, btn1, btn2, bNow):
		oldCellPos = btn1.cellPos
		btn1.cellPos = btn2.cellPos
		btn2.cellPos = oldCellPos
		
		btn1.targetPos = btn2.pos
		btn2.targetPos = btn1.pos
		if bNow:
			btn1.pos = btn1.targetPos
			btn2.pos = btn2.targetPos
		else:
			self.setMoveButton(btn1, btn2)
		
		self.buttonList[btn1.cellPos[0] + btn1.cellPos[1]*self.numericCols] = btn1
		self.buttonList[btn2.cellPos[0] + btn2.cellPos[1]*self.numericCols] = btn2

	
	def setMoveButton(self, btn1, btn2):
		self.moveButton1 = btn1
		self.moveButton2 = btn2
		
	def isMoveButton(self):
		return self.moveButton1 or self.moveButton2
		
	def updateMoveButton(self):
		if self.moveButton1:
			moveDir = Vector(self.moveButton1.targetPos) - Vector(self.moveButton1.pos)
			moveDist 	= moveDir.length()
			moveVel = self.vMoveVel * self.fFrameTime
			if moveVel > moveDist:
				self.moveButton1.pos = self.moveButton1.targetPos
				self.moveButton1 = None
			else:
				moveDir = moveDir.normalize()
				moveDir *= moveVel
				self.moveButton1.pos = (self.moveButton1.pos[0] + moveDir[0], self.moveButton1.pos[1] + moveDir[1])
				
		if self.moveButton2:
			moveDir = Vector(self.moveButton2.targetPos) - Vector(self.moveButton2.pos)
			moveDist 	= moveDir.length()
			moveVel = self.vMoveVel * self.fFrameTime
			if moveVel > moveDist:
				self.moveButton2.pos = self.moveButton2.targetPos
				self.moveButton2 = None
			else:
				moveDir = moveDir.normalize()
				moveDir *= moveVel
				self.moveButton2.pos = (self.moveButton2.pos[0] + moveDir[0], self.moveButton2.pos[1] + moveDir[1])

				
	def checkComplete(self):
		for btn in self.buttonList:
			if (1+btn.cellPos[0]+btn.cellPos[1]*self.numericCols) != btn.myNum:
				return False
		return True
		
	def addSlider(self):
		popupSize = calcSize(Window.size, 0.5, 0.1)
		self.mixWidget = Popup(title = "Mix...", size = popupSize, pos = calcPos(getCenterPos(), popupSize))
		self.mixSlider = Slider(value = 0.0, min = 0, max = self.mixCount)
		self.mixWidget.add_widget(self.mixSlider)
		self.add_widget(self.mixWidget)
	
	def updateSlider(self):
		self.mixSlider.value = self.mixSlider.max - self.mixCount
		
	def removeSlider(self):
		self.remove_widget(self.mixWidget)
	
	def update(self, dt):
		self.fFrameTime = dt
		self.szDebug = str("%.2f" % (1.0/dt))

		gameState.update()

		
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
		global cx, cy
		global clickSnd, wrongSnd
		global fUpdateTime
		global bButtonLock
		
		fUpdateTime = 1.0/60.0
		bButtonLock = False

		clickSnd = SoundLoader.load("click.wav")
		clickSnd.volume = 1.0
		wrongSnd = SoundLoader.load("wrong.wav")
		wrongSnd.volume = 1.0

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