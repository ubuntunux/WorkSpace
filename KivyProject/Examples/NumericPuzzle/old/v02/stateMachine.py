class eventMachine():

	def updateNone(self, pol):
		pol.state=99
		
	onEnter = updateNone
	onUpdate = updateNone
	onExit = updateNone
		
class stateMachine():
	state = 0
	aaa=eventMachine()

	def __init__(self):
		self.state = 99
		self.aaa.onUpdate(self)