from stateMachine import *

STATE_NONE = 0
STATE_RESET = 1
STATE_MIX = 2
STATE_PLAY = 3
STATE_COMPLETE = 4
STATE_FAIL = 5
STATE_COUNT = 6

gameState = stateMachine(STATE_COUNT)


class NumPuzzleGameBase():
	szDebug = None
	fTime = None	
	buttonList = []
	lastButton = None
	moveButton1 = None
	moveButton2 = None
	icons = []
	sounds = {}
	mySound = None
	mixCount = 0
	numericCount = 0
	numericCols = 0
	numericRows = 0
	fFrameTime = 0.0
	vMoveVel = 100.0
	mixWidget = None
	mixSlider = None
	oldDir = -1
	curDir = -1
	
	def start(self):
		gameState.stateList[STATE_RESET].onEnter =\
		 self.stateReset_onEnter
		gameState.stateList[STATE_MIX].onEnter =\
		 self.stateMix_onEnter
		gameState.stateList[STATE_MIX].onUpdate =\
		 self.stateMix_onUpdate
		gameState.stateList[STATE_MIX].onExit =\
		 self.stateMix_onExit
		gameState.stateList[STATE_PLAY].onEnter =\
		 self.statePlay_onEnter
		gameState.stateList[STATE_PLAY].onUpdate =\
		 self.statePlay_onUpdate
		 
		gameState.set_state(STATE_RESET)
	
	def buildNumeric(self, cols=0, rows=0):
		pass
		
	def mixNumeric(self):
		pass
		
	def switchButton(self, btn1, btn2, bNow):
		pass
	
	def setMoveButton(self, btn1, btn2):
		pass
		
	def updateMoveButton(self):
		pass
				
	def checkComplete(self):
		pass
		
	def stateReset_onEnter(self):
		self.buildNumeric()
		gameState.set_state(STATE_MIX)
		
	def stateMix_onEnter(self):
		self.lastButton.hide()
		self.mixCount = (self.numericCols ** 3)
		self.addSlider()
		
	def stateMix_onUpdate(self):
		if self.mixCount > 0:
			if self.isMoveButton():
				self.updateMoveButton()
			else:
				self.updateSlider()
				self.mixNumeric()
				self.mixCount -= 1
				if self.checkComplete():
					self.mixCount = self.numericCount ** 2
		else:
			gameState.set_state(STATE_PLAY)
			
	def stateMix_onExit(self):
		self.removeSlider()
	
	def statePlay_onEnter(self):
		self.fTime = 0.0
		
	def statePlay_onUpdate(self):
		self.fTime += self.fFrameTime
		if self.isMoveButton():
				self.updateMoveButton()