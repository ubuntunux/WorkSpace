class stateItem():
	def updateNone(self):
		pass
		
	onEnter = updateNone
	onUpdate = updateNone
	onExit = updateNone
	
		
class stateMachine():
	stateCount = 0
	stateList = []
	curState = -1
	oldState = -1
	
	def __init__(self, stateCount):
		self.stateCount = stateCount
		for i in range(stateCount):
			self.stateList.append(stateItem())
			
	def is_state(self,index):
		return index == self.curState
		
	def get_state(self):
		#return str(self.stateCount) +" "+str(self.oldState) +" "+str(self.curState)
		return self.curState
	
	def set_state(self, index):
		if index < self.stateCount and index != self.curState:
			self.oldState = self.curState
			self.curState = index
			if self.oldState > -1:
				self.stateList[self.oldState].onExit()
			if index > -1:
				self.stateList[index].onEnter()
	
	def update(self):
		if self.stateList:
			self.stateList[self.curState].onUpdate()