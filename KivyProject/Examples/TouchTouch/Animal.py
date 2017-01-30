import Utility as Util
from Utility import *

from Particle import *

gFriction = 10.0
gMaxSpeed = 60.0
gGround = Util.H * 0.1
gJump = Util.H * 2.0
gVel = Util.W * .3
gAnimalSize = getHint(.15, .27)

class AnimalBase(Widget):
	def __init__(self, res, size):
		Widget.__init__(self)
		self.img = Scatter(size = size)
		self.img.do_translation = False
		self.img.do_rotation = False
		self.img.do_scale = False
		self.res = res

		with self.img.canvas:
			Color(1,1,1)
			Rectangle(size = self.img.size, texture=self.res.getTex())

		self.add_widget(self.img)			
		self.radius = getDist(mul(self.img.size, 0.5))

class TargetAnimal(AnimalBase):
	def __init__(self, res):
		AnimalBase.__init__(self, res, getHint(.1, .2))

class MoveAnimal(Scatter):
	def __init__(self, res):
		Scatter.__init__(self, size=self.size)
		self.do_translation = False
		self.do_rotation = False
		self.do_scale = False
		self.res = res
		self.size = gAnimalSize
		self.btn = Button(size=self.size, background_color=[1,1,1,.5])
		self.btn.bind(on_press=self.onTouch)
		with self.btn.canvas:
			Color(1,1,1)
			Rectangle(size=self.size, texture=self.res.getTex())
		self.add_widget(self.btn)
		
		self.bDead = False
		self.vel = gVel
		self.jump = 0.0
		self.bJump = False
			
	def onTouch(self, instance):
		self.setJump()

	def setJump(self):
		if self.bJump:
			return
		self.bJump = True
		self.jump = gJump
	
	def setDead(self):
		if self.bDead:
			return
		self.bDead = True
		#self.res.getSnd().play()
		if self.parent:
			self.parent.remove_widget(self)
		
	def onUpdate(self):
		self.updateMove()
	
	def updateMove(self):
		vel = mul((self.vel, self.jump), getFrameTime())
		self.pos = add(self.pos, vel)
		if self.pos[1] < gGround:
			self.pos = (self.pos[0], gGround)
			if self.bJump:
				self.bJump = False
				self.jump = 0.0
		if self.bJump:
			self.jump -= Util.gGravity * getFrameTime()
		if self.pos[0] > Util.W - self.size[0]:
			self.pos=mul(self.pos, (0,1.0))
		

class GrabAnimal(Widget):
	def __init__(self, res):
		Widget.__init__(self)
		self.img = Scatter(size = (300,300))
		#self.img.do_translation = False
		self.img.do_rotation = False
		self.img.do_scale = False
		self.res = res

		with self.img.canvas:
			Color(1,1,1)
			Rectangle(size = self.img.size, texture=self.res.getTex())

		self.add_widget(self.img)	
		
		self.vel = [0.0, 0.0]
		self.minXY = [0.0, 0.0]
		self.maxXY = sub(Util.WH, self.img.size)
		self.radius = getDist(mul(self.img.size, 0.5))
			
	def on_touch_move(self, touch):
		self.check_collide()
	
	def on_touch_up(self, touch):
		self.vel = [touch.dx, touch.dy]

	def check_collide(self):
		r = self.radius
		x,y = self.img.pos
		vx = vy = 1.0

		if x < self.minXY[0]:
			x = self.minXY[0]
			if self.vel[0] < 0.0:
				vx = -1.0				
		elif x > self.maxXY[0]:
			x = self.maxXY[0]
			if self.vel[0] > 0.0:
				vx = -1.0
		if y < self.minXY[1] :
			y = self.minXY[1]
			if self.vel[1] < 0.0:
				vy = -1.0
		elif y > self.maxXY[1]:
			y = self.maxXY[1]
			if self.vel[1] > 0.0:
				vy = -1.0
		
		self.vel = mul(self.vel, (vx,vy))
		self.img.pos = (x,y)
				
	def update_vel(self):
		speed = getDist(self.vel)
		newSpeed = speed - gFriction * getFrameTime()
		if newSpeed < 0.0:
			self.vel = [0.0, 0.0]
		elif newSpeed > gMaxSpeed:
			newSpeed = gMaxSpeed
		self.vel = mul(normalize(self.vel, speed), newSpeed)
		
	def onUpdate(self):
		self.img.pos = add(self.img.pos, self.vel)
		self.check_collide()
		self.update_vel()