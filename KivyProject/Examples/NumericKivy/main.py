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
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.vector import Vector

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

class Music():
	sound = None
	def start(self):
		if self.sound is None:
			self.sound = SoundLoader.load("bgm.wav")
			self.sound.volume = 0.8
			self.sound.play()
			self.sound.on_stop = self.sound.play
	def mute(self, mute_music):
		self.sound.volume = 0.0 if mute_music else 0.8
			
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

	def hide_font(self):
		self.btn.text = ""
		self.btn.background_color = (0,0,0,0.0)
			
	def show_font(self):
		if self.isShow:
			self.btn.text = str(self.myNum)
			self.btn.background_color = (10,10,10,0.2)
			 			
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

	# start - override states func
	def stateNone_onEnter(self):
		self.labelText.text = self.level_name[self.level]
		self.buildNumeric()
		self.hide_font()
		
	def stateReset_onEnter(self):
		if self.complete_picture:
			self.remove_widget(self.complete_picture)
		self.labelText.text = self.level_name[self.level]
		self.buildNumeric()
		gameState.set_state(STATE_MIX)

	def stateMix_onEnter(self):
		self.lastButton.hide()
		self.mixCount = (self.numericCols ** 3)

	def stateMix_onUpdate(self):
		if self.mixCount > 0:
			if self.isMoveButton():
				self.updateMoveButton()
			else:
				self.mixNumeric()
				self.mixCount -= 1
				if self.checkComplete():
					self.mixCount = self.numericCount ** 2
		else:
			gameState.set_state(STATE_READY)

	def stateReady_onEnter(self):
		self.countdown = Label(text=str(3), pos=(rootW*0.45, rootH*0.75), font_size=150)
		self.add_widget(self.countdown)
		self.fcountdown = 3.999999
		
	def stateReady_onUpdate(self):
		self.fcountdown -= self.fFrameTime
		if self.fcountdown < 0.0:
			self.remove_widget(self.countdown)
			gameState.set_state(STATE_PLAY)
		else:
			self.countdown.text = self.countdown_str[int(self.fcountdown)]
		
	def statePlay_onEnter(self):
		self.labelText.text = "Time : 0.0s"

	def statePlay_onUpdate(self):
		self.fTime += self.fFrameTime
		self.labelText.text = "Time : " + str("%.2f" % self.fTime) + "s"
		if self.isMoveButton():
				self.updateMoveButton()

	def stateComplete_onEnter(self):
		if self.sound_wow == None:
			self.sound_wow = SoundLoader.load("wow.wav")
		self.sound_wow.play()
		self.hide_font()
		
		'''
		# show complete image
		self.complete_picture = Scatter(pos = (self.size[0]*0.075, self.size[1]*0.075), size = (self.size[0]*0.85, self.size[1]*0.65))
		self.complete_picture.do_translation = False
		self.complete_picture.do_rotation = False
		self.complete_picture.do_scale = False
		texture = Image(source = choice(self.icons)).texture
		texture.wrap = 'repeat'
		texture.uvpos=(0.0, 0.0)
		texture.uvsize=(1.0, -1.0)
		with self.complete_picture.canvas:
			Rectangle(texture = texture, size=self.complete_picture.size)
		btn = Button(size=self.complete_picture.size)
		btn.background_color = (0,0,0,0)
		self.complete_picture.add_widget(btn)
		self.add_widget(self.complete_picture, 0)
		'''
		content = Widget()
		sizehintW = 0.8
		sizehintH = 0.3
		btnSizeW = rootW * sizehintW * 0.9
		btnSizeH = rootH * sizehintH * 0.2
		popup = Popup(title = " Complete!!", content=content, auto_dismiss=False, size_hint = (sizehintW, sizehintH))
		content.add_widget(Label(font_size = 35, text = "Time : " + str("%.2f" % self.fTime) + "s", pos = (cx - btnSizeW*0.5, rootH * 0.4 + btnSizeH * 2.4), size=(btnSizeW, btnSizeH), align = 'left'))
		content.add_widget(Label(font_size = 35, text = self.level_name[self.level] + " Complete!!", pos = (cx - btnSizeW*0.5, rootH * 0.4 + btnSizeH * 1.2), size=(btnSizeW, btnSizeH), align = 'left'))
		btn_close = Button(text='Close', pos = (cx - btnSizeW*0.5, rootH * 0.4), size=(btnSizeW, btnSizeH))
		content.add_widget(btn_close)
		def closePopup(instance):
			popup.dismiss()

		btn_close.bind(on_press=closePopup)
		popup.open()
	# end - override states

	def SetComplete(self):
		gameState.set_state(STATE_COMPLETE)

	def start(self):
		self.music = Music()
		self.music.start()
		self.loadData()
		super(NumPuzzleGame, self).start()
		
	def loadData(self):
		#load images
		curdir = dirname(__file__)
		self.icons = glob(join(curdir, 'images', '*.png')) + glob(join(curdir, 'images', '*.jpg'))

	def getIconFile(self):
		return choice(self.icons)
		
	def setReset(self, level = 1):
		self.level = level
		gameState.set_state(STATE_RESET)

	# buildNumeric
	def buildNumeric(self, cols=0, rows=0):
		self.curDir = -1
		self.oldDir = -1
		self.fTime = 0.0
		if cols < min : cols = self.level + 3
		if rows < min : rows = self.level + 3
		
		self.vMoveVel = 20.0*(self.numericWidget.size[0] / cols)
		
		self.numericCount = cols * rows
		self.numericCols = cols
		self.numericRows = rows
		self.buttonList = range(0, self.numericCount)
		self.numericWidget.clear_widgets()
		
		cellSize = (self.numericWidget.size[0] / cols, self.numericWidget.size[1] / rows)
	
		#set iconFile and load sound
		source = self.getIconFile()
		import copy
		self.current_source = copy.copy(source)

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
			self.lastButton.show()
			gameState.set_state(STATE_COMPLETE)
			
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
			moveDist	 = moveDir.length()
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
			moveDist	 = moveDir.length()
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
		
	def hide_font(self):
	 [i.hide_font() for i in self.buttonList]
	
	def update(self, dt):
		self.fFrameTime = dt
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
		try:
			import android
		except:
			pass
		else:
			android.map_key(android.KEYCODE_MENU, 1000)
			android.map_key(android.KEYCODE_BACK, 1001)
			android.map_key(android.KEYCODE_HOME, 1002)
			android.map_key(android.KEYCODE_SEARCH, 1003)
			win = self._app_window
			win.bind(on_keyboard=self._key_handler)

if __name__ in ('__android__', '__main__'):
	NumPuzzleApp().run()