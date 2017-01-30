import Utility as Util
from Utility import *

from Particle import *
import MyGame

gPlayer = None
gWorldSize = Util.WH
gCheckAngle = 0.707
gFriction = 10.0
gMaxSpeed = 60.0
gGround = Util.H * 0.05
gJump = Util.H * 1.8
gVel = Util.W * 0.8
gWalk = Util.W * 0.3
gIncVel = Util.W * 1.6
gDecVel = Util.W * 2.5
gRange = Util.W * 0.3
gAnimalSize = [Util.H*.18]*2
gGravity = Util.gGravity*0.8

class AnimalBase(Scatter):
	isPlayer = False
	def __init__(self, res):
		Scatter.__init__(self, size=self.size)
		self.do_translation = False
		self.do_rotation = False
		self.do_scale = False
		self.res = res
		self.size = mul(gAnimalSize, fRand(0.5,1.0))
		self.radius = Util.getDist(self.size) * 0.707
		with self.canvas:
			Color(1,1,1)
			Rectangle(size=self.size, texture=self.res.getTex())
		# debug button
		'''
		self.btn = Button(size=self.size, background_color=[1,1,1,.5])
		self.btn.bind(on_press=self.onTouch)
		self.add_widget(self.btn)
		'''
		# check this out!!!!!
		self.pos = (fRand(0.0, gWorldSize[0]), fRand(0.0, gWorldSize[1]))
		self.life = 5
		self.collide = False
		self.bDead = False
		self.vel = 0.0
		self.jump = 0.0
		self.bJump = False
		self.wallJump = False
		self.inc_vel = gIncVel
		self.dec_vel = gDecVel
		self.maxVel = gVel
		self.dir_left = False
		self.dir_right = False
			
	def onTouch(self, instance):
		self.setJump()

	def setJump(self, bIgnore=False, ratio=1.0):
		if self.bJump and not bIgnore:
			return
		self.bJump = True
		self.jump = gJump * ratio

	def set_wallJump(self):
			if not self.wallJump:
				self.jump += gJump * 0.1
				self.wallJump = True

	def setFx(self):
		if MyGame.gMyGame:
			emitter = MyGame.gMyGame.FxMgr.get_emitter('star')
			emitter.pos = add(self.pos, mul(self.size, (0.5, 1.0)))
			emitter.play_particle()
			
	def setDamage(self, damage=1):
		if self.bDead:
			return
		self.life -= damage
		#self.res.playSnd()
		self.setFx()
		if self.life <= 0:
			self.life = 0
			self.setDead()
	
	def setDead(self):
		if self.bDead:
			return
		self.bDead = True
		if self.parent:
			self.parent.remove_widget(self)
			
	def set_turn(self):
		if self.dir_left:
			self.set_right()
		elif self.dir_right:
			self.set_left()
		
	def set_left(self, *args):
		self.vel = 0.0
		self.dir_left = True
		self.dir_right = False

	def set_right(self, *args):
		self.vel = 0.0
		self.dir_left = False
		self.dir_right = True
		
	def release_all(self):
		self.dir_left = False
		self.dir_right = False

	def release_left(self, *args):
		self.dir_left = False

	def release_right(self, *args):
		self.dir_right = False
	
	def inc_velocity(self):
		vel = self.inc_vel * getFrameTime()
		if self.jump < 0.0:
			self.jump -= gGravity * 1.5 * getFrameTime()
			vel*=1.75

		if self.dir_left:
			vel = -vel
		self.vel += vel
		if abs(self.vel) > self.maxVel:
			self.vel = self.maxVel if self.vel > 0.0 else -self.maxVel
		
	def dec_velocity(self):
		vel = abs(self.vel)
		if vel == 0.0:
			return
		vel -= self.dec_vel * getFrameTime()
		if vel < 0.0:
			self.vel = 0.0
			return
		self.vel = vel if self.vel > 0.0 else -vel

	def onUpdate(self):
		if not self.bJump:
			self.setJump()		
		if self.dir_left or self.dir_right:
			self.inc_velocity()
		else:
			self.dec_velocity()	
		self.updateMove()
		 	
	def updateMove(self):
		self.collide = False
		vel = mul((self.vel, self.jump), getFrameTime())
		self.pos = add(self.pos, vel)
		if self.pos[1] < gGround:
			self.pos = (self.pos[0], gGround)
			self.wallJump = False
			self.jump = 0.0
			if self.bJump:
				self.bJump = False
		elif self.pos[1] > gWorldSize[1] - self.size[1]:
			self.pos = (self.pos[0], (gWorldSize[1]-self.size[1])*2-self.pos[1])
			self.jump = -self.jump

		if self.pos[1] > gGround :
			self.jump -= gGravity * getFrameTime()
		if self.pos[0] < 0:
			self.pos = (-self.pos[0], self.pos[1])
			self.vel = -self.vel
			self.collide=True
			self.set_wallJump()
		elif self.pos[0] > gWorldSize[0] - self.size[0]:
			self.pos = ((gWorldSize[0]-self.size[0])*2-self.pos[0], self.pos[1])
			self.vel = -self.vel
			self.collide=True
			self.set_wallJump()

class AnimalEnemy(AnimalBase, StateMachine):
	STATE_NONE = 0
	STATE_IDLE = 1
	STATE_WALK = 2
	STATE_STUN = 3
	STATE_ATTACKREADY = 4
	STATE_ATTACK = 5
	
	class State_Idle(StateItem):
		def __init__(self, actor):
			self.actor = actor
		def onEnter(self):
			self.actor.release_all()
			self.idle_time =fRand(0.5,1.5)
		def onUpdate(self):
			self.idle_time -= getFrameTime()*1.0
			if self.idle_time < 0.0:
				self.setState(self.actor.STATE_WALK)
			self.actor.checkPlayer()
				
	class State_Walk(StateItem):
		def __init__(self, actor):
			self.actor = actor
		def onEnter(self):
			self.walk_time = fRand(1.0,3.0)
			self.actor.set_left() if nRand(0,1) else self.actor.set_right()
			self.actor.maxVel = gWalk
		def onUpdate(self):
			if self.actor.collide:
				self.actor.set_turn()
				self.actor.setJump(ratio=0.7)
			self.walk_time -= getFrameTime()
			if self.walk_time < 0.0:
				self.setState(self.actor.STATE_IDLE)
			self.actor.checkPlayer()

	class State_Stun(StateItem):
		def __init__(self, actor):
			self.actor = actor
		def onEnter(self):
			self.actor.release_all()
			self.stun_time = 1.0
		def onUpdate(self):
			self.stun_time -= getFrameTime()*1.0
			if self.stun_time < 0.0:
				self.setState(self.actor.STATE_ATTACK)				

	class State_AttackReady(StateItem):
		def __init__(self, actor):
			self.actor = actor
		def onEnter(self):
			self.actor.release_all()
			self.time = 1.0
		def onUpdate(self):
			self.time -= getFrameTime()*1.0
			if self.time < 0.0:
				if self.actor.playerInRange():
					self.setState(self.actor.STATE_ATTACK)
				else:
					self.setState(self.actor.STATE_WALK)
				
	class State_Attack(StateItem):
		def __init__(self, actor):
			self.actor = actor
		def onEnter(self):
			self.actor.maxVel = gVel
		def onUpdate(self):
			if not self.actor.bJump:
				self.actor.setJump()		
				if gPlayer.pos[0] > self.actor.pos[0]:
					self.actor.set_right()
				else:
					self.actor.set_left()
					
	def __init__(self, res):
		AnimalBase.__init__(self, res)
		StateMachine.__init__(self)
		self.addState(StateItem())
		self.addState(self.State_Idle(self))
		self.addState(self.State_Walk(self))
		self.addState(self.State_Stun(self))
		self.addState(self.State_AttackReady(self)) 		
		self.addState(self.State_Attack(self))
		self.setState(self.STATE_IDLE)
		self.preAttack = nRand(0,1)
		self.preAttackRange = gRange
	
	def playerInRange(self):
		return True if abs(gPlayer.pos[0] - self.pos[0]) < self.preAttackRange else False
 	
	def checkPlayer(self):
		if self.preAttack and self.playerInRange():
			self.setState(self.STATE_ATTACKREADY)
			return True
		return False
		
	def setDamage(self, damage=1):
		AnimalBase.setDamage(self, damage)
		if not self.bDead:
			self.setState(self.STATE_STUN, True)
	
	def onUpdate(self):
		StateMachine.update(self)
		if self.dir_left or self.dir_right:
			self.inc_velocity()
		else:
			self.dec_velocity()	
		self.updateMove()

class AnimalPlayer(AnimalBase):
	isPlayer = True
	def __init__(self, res):
		AnimalBase.__init__(self, res)
		global gPlayer
		gPlayer = self
		self.life=100

class AIMgr:
	def __init__(self, parent_layer):
		self.ai_list = []
		self.player = None
		self.parent_layer = parent_layer
	
	def setPlayer(self, player)	:
		self.player = player
		
	def add_ai(self, res, num=1):
		for i in range(num):
			self.ai_list.append(AnimalEnemy(res))
			self.parent_layer.add_widget(self.ai_list[-1])

	def remove_ai(self):
		for i in self.ai_list:
			i.setDead()
		self.ai_list = []
				
	def check_collide(self, a, b):
		dist = getDist(a.pos, b.pos)
		radius = (a.radius + b.radius) * 0.5
		if dist < radius:
			v1 = (a.vel, a.jump)
			v2 = (b.vel, b.jump)
			vVel = sub(v1, v2)
			vDir = normalize(sub(b.pos, a.pos))
			dot = sum(mul(vVel, vDir))
			if dot > 0.0:
				vVel = mul(vDir, dot)
				b.vel = b.vel + vVel[0]
				b.jump = b.jump + vVel[1]
				a.vel = a.vel - vVel[0]
				a.jump = a.jump - vVel[1]
				a.collide = True
				b.collide = True
				
				if vDir[1] < -gCheckAngle:
					a.setJump(True, 0.8)
					if a.isPlayer or b.isPlayer:
						b.setDamage()
				elif vDir[1] > gCheckAngle:
					b.setJump(True, 0.8)
					if a.isPlayer or b.isPlayer:
						a.setDamage()
								
	def onUpdate(self):
		deadList = []
		animals = copy(self.ai_list)
		animals.append(self.player)
		for i in self.ai_list:
			i.onUpdate()
			if i.bDead:
				deadList.append(i)
			for j in animals:
				if i is not j:
					self.check_collide(i,j)	
			animals.remove(i)
			
		for i in deadList:
			self.ai_list.remove(i)
			