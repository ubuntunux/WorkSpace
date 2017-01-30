#---------------------#
# Import kivy
#---------------------#
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.factory import Factory
from kivy.graphics import Color, Rectangle, Point, GraphicException, Line, Quad, Ellipse, Fbo, RenderContext
from kivy.graphics.opengl import glLineWidth
from kivy.logger import Logger
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.vector import Vector

#---------------------#
# Import library
#---------------------#
import android
from cmath import polar, rect
from copy import deepcopy
from glob import glob
import math
from math import cos,sin,pi,sqrt,atan,atan2
import os
import random
import sys

#---------------------#
# Global variable
#---------------------#
startPoint = None
W = Window.size[0]
H = Window.size[1]
WH = (W, H)
cX = W * 0.5
cY = H * 0.5
cXY = (W * 0.5, H * 0.5)
fUpdateTime = 1.0 / 60.0
fFrameTime = 1.0
fAccTime = 0.0
bButtonLock = False
gMyApp = None
gMyRoot = None
gDebugPrint = None

def getFrameTime():
	return fFrameTime
	
def getAccTime():
	return fAccTime

def getDebugPrint():
	return gDebugPrint
	
def getMyRoot():
	return gMyRoot

def getMyApp():
	return gMyApp

def sizeHint(ratioX, ratioY):
	return (W * ratioX, H * ratioY)
	
def getCenter(size = (W,H)):
	return (size[0]*.5, size[1]*.5)

def getLT(center, size):
	return (center_pos[0]-size[0]/2.0, center_pos[1]+size[1]/2.0)

def getRT(center, size):
	return (center_pos[0]+size[0]/2.0, center_pos[1]+size[1]/2.0)

def getLB(center, size):
	return (center_pos[0]-size[0]/2.0, center_pos[1]-size[1]/2.0)

def getRB(center, size):
	return (center_pos[0]+size[0]/2.0, center_pos[1]-size[1]/2.0)
#---------------------#
# Utility
#---------------------#
def nRand(min, max):
	return random.randint(min, max)

def fRand(min, max):
	return random.uniform(min, max)

def calcCenterPos(pos, size):
	return (pos[0]+size[0]/2.0, center_pos[1]+size[1]/2.0)
	 	
def calcPos(center_pos, size):
	return (center_pos[0]-size[0]/2.0, center_pos[1]-size[1]/2.0)

def calcSize(size, ratioX, ratioY):
	return (size[0]*ratioX, size[1]*ratioY)

def getButton(text, center, size):
	widget = Button()
	widget.text = text
	widget.size = sizeHint( size[0], size[1] )
	widget.center = sizeHint( center[0], center[1] )
	return widget

#---------------------#
# CLASS : DebugPrint
#---------------------#
class DebugPrint(Widget):
	nLine = 0
	nLineLimit = 85
	bRefresh = True
	bShowFrame = True
	debugLabel = Label(text = "debug print text", halign = 'left', valign = 'top')
	
	def __init__(self):
		gDebugPrint = self
		super(DebugPrint, self).__init__()
		self.nLine = 0
		self.size = (W,H)
		self.debugLabel.x = W - self.debugLabel.width
		self.debugLabel.y = H - self.debugLabel.height
		self.add_widget(self.debugLabel)

	def refresh(self, bRefresh):
		sslf.bRefresh = bRefresh
		
	def showFrame(self, bShow):
		self.bShowFrame = bShow
	
	def Print(self, szString):
		if self.nLine > self.nLineLimit:
			return False
		self.nLine += 1
		if self.debugLabel.text:
			self.debugLabel.text += "\n"
		self.debugLabel.text += szString
		return True
		
	def Printf(self, fNum):
		if self.nLine > self.nLineLimit:
			return False
		self.nLine += 1
		if self.debugLabel.text:
			self.debugLabel.text += "\n"
		self.debugLabel.text += str(fNum)
		return True
	
	def showProp(self, obj, start = 0):
		for x,i in enumerate(dir(obj)[start:-1]):
			if self.Print(str(x+start)+'.'+i) == False:
				return
	
	def Reset(self):
		self.nLine = 0
		if self.bShowFrame:
			self.debugLabel.text = "%.2f" % (1.0/fFrameTime)
		else:
			self.debugLabel.text = ""

#---------------------#
# CLASS : MyRoot
#---------------------#
class MyRoot(FloatLayout):
	def __init__(self):
		super(MyRoot, self).__init__()
		self.size = Window.size
		self.appList = []

		global gMyRoot
		gMyRoot = self
		Clock.schedule_interval(self.update, fUpdateTime)
	
	def regist(self, app):
		if app in self.appList:
			return
		self.appList.append(app)
	
	def remove(self, app):
		if app in self.appList:
			self.appList.remove(app)
		
	def update(self, frameTime):
		global fFrameTime, fAccTime
		fFrameTime = frameTime
		fAccTime += frameTime
		getDebugPrint().Reset()
		if startPoint:
			startPoint.update()
		for app in self.appList:
			app.update()
		
#---------------------#
# CLASS : MyApp
#---------------------#
class MyApp(App):
	bPopup = False
	touchPrev = None
	
	def __init__(self):
		super(MyApp, self).__init__()
		global gMyApp
		gMyApp = self
		
	def start(self, app):
		global startPoint
		startPoint = app
		super(MyApp, self).run()
	
	def on_pause(self):
		return True
		
	def build(self):
		global bButtonLock
		bButtonLock = False

		self.bPopup = False
		self.root = FloatLayout()
		self.gameRoot = MyRoot()
		self.root.add_widget(self.gameRoot)
		
		global gDebugPrint
		self.debugPrint = DebugPrint()
		gDebugPrint = self.debugPrint
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
		btnSizeW = W * sizehintW * 0.5
		btnSizeH = H * sizehintH * 0.5
		popup = Popup(title = "Exit?", content=content, auto_dismiss=False, size_hint = (sizehintW, sizehintH))
		content.pos=popup.pos
		btn_Yes = Button(text='Yes', pos = (cX-btnSizeW*0.1- btnSizeW*0.75, cY - btnSizeH*0.5), size=(btnSizeW*0.75, btnSizeH*0.75))
		btn_No = Button(text='No', pos = (cX+btnSizeW*0.1, cY - btnSizeH*0.5), size=(btnSizeW*0.75, btnSizeH*0.75))
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
		#android.map_key(android.KEYCODE_MENU, 1000) 
		android.map_key(android.KEYCODE_BACK, 1001) 
		android.map_key(android.KEYCODE_HOME, 1002) 
		android.map_key(android.KEYCODE_SEARCH, 1003) 

		win = self._app_window 
		win.bind(on_keyboard=self._key_handler)

#---------------------#
# CLASS : StateItem
#---------------------#
class StateItem():	
	stateMgr = None
	
	def onEnter(self):
		pass
		
	def onUpdate(self):
		pass
		
	def onExit(self):
		pass
	
	def setState(self, state):
		if self.stateMgr:
			self.stateMgr.setState(state)
	
#---------------------#
# CLASS : StateMachine
#---------------------#
class StateMachine(object):
	stateCount = 0
	stateList = None
	curState = -1
	oldState = -1
		
	def addState(self, stateItem):
		self.stateCount += 1
		if self.stateList:
			self.stateList.append(stateItem)
		else:
			self.stateList = [stateItem]
		stateItem.stateMgr = self
	
	def getCount(self):
		return self.stateCount
		
	def isState(self, index):
		return index == self.curState
		
	def getState(self):
		return self.curState
	
	def setState(self, index):
		if index < self.stateCount and index != self.curState:
			self.oldState = self.curState
			self.curState = index
			if self.oldState > 0:
				self.stateList[self.oldState].onExit()
			if index > 0:
				self.stateList[index].onEnter()

	def update(self):
		if self.stateList:
			self.stateList[self.curState].onUpdate()
			
#---------------------#
# MultiMethod
#---------------------#
registry = {}

class MultiMethod(object):
    def __init__(self, name):
        self.name = name
        self.typemap = {}
    def __call__(self, *args):
        types = tuple(arg.__class__ for arg in args) # a generator expression!
        function = self.typemap.get(types)
        if function is None:
            raise TypeError("no match")
        return function(*args)
    def register(self, types, function):
        if types in self.typemap:
            raise TypeError("duplicate registration")
        self.typemap[types] = function

def multimethod(*types):
    def register(function):
        name = function.__name__
        mm = registry.get(name)
        if mm is None:
            mm = registry[name] = MultiMethod(name)
        mm.register(types, function)
        return mm
    return register
    
overload = multimethod

@overload()	
def getX():
	return cX
	
@overload(int)	
def getX(a):
	return cX*a

@overload(int, int)
def getX(a,b):
	return cX*b

