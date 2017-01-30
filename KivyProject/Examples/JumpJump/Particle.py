import Utility as Util
from Utility import *

class FxMgr:
	inited = False
	emitters = {}

	def __init__(self, parent_layer):
		self.parent_layer = parent_layer
		self.inited = True
		
	def clear_emitter(self):
		for i in self.emitters:
			self.emitters[i].clear_particle()

	def get_emitter(self, name):
		return self.emitters[name]
		
	def create_emitter(self, name, info, num):
		emitter = Emitter(self.parent_layer, info, num)
		self.emitters[name] = emitter
		return emitter
	
	def create_emitter_with(self, name, info, num, parent_layer):
		emitter = Emitter(parent_layer, info, num)
		self.emitters[name] = emitter
		return emitter
		
	def remove_emitter(self):
		for i in self.emitters:
			self.emitters[i].remove_particle()
		self.emitters = {}
				
	def stop_emitter(self):
		for i in self.emitters:
			self.emitters[i].stop_particle()

	def onUpdate(self):
		for i in self.emitters:
			self.emitters[i].onUpdate()

class Particle(Scatter):
	def __init__(self):
		Scatter.__init__(self)
		self.do_translation = False
		self.do_rotation = False
		self.do_scale = False
		self.isAlive = False
		self.elapseTime = 0.0
		self.accTime = 0.0
		self.texture = None
		self.curtexture = None
		#variation
		self.collision = False
		self.loop = 1
		self.loopleft = self.loop
		self.fade = 0.0
		self.sequence = [1,1]
		self.curseq = [0,0]
		self.cellsize = [1.0, 1.0]
		self.cellcount = 1
		self.playspeed = 1.0
		self.oldsequence = 0

		self.lifeTime = 1.0
		self.gravity = 1.0
		self.vel = [0.0, 0.0]
		self.rotateVel = 0.0
		self.rotation = 0.0
		self.scale = 1.0
		self.opacity = 1.0
		self.pos = (0.0, 0.0)
		self.variables = {
		'lifeTime':Var(self.lifeTime),
		'gravity':Var(self.gravity),
		'vel':Var(self.vel),
		'rotateVel':Var(self.rotateVel),
		'rotation':Var(self.rotation),
		'scale':Var(self.scale),
		'opacity':Var(self.opacity),
		'pos':Var(self.pos)
			}
			
	def Create(self, collision=False, size=[100,100], 
			source=None, texture=None, loop=1, fade=0.0,
			sequence=[1,1], playspeed=1.0, **args):
		self.collision = collision
		self.size = size
		self.loop = loop
		self.fade = fade
		self.sequence = sequence
		self.playspeed = playspeed
		if texture == None:
			if source != None:
				self.texture = Image(source=source).texture
		else:
			self.texture=texture
		if self.sequence[0]==1 and self.sequence[1]==1:
			self.playspeed = 0

		for key in args:
			self.variables[key] = args[key]
			
		if self.texture:
			self.cellcount = self.sequence[0] * self.sequence[1]
			self.cellsize = div(self.texture.size, self.sequence)
			curtexture = self.texture.get_region(0.0, 0.0, *self.cellsize)
			with self.canvas:
				Color(1,1,1,1)
				self.box = Rectangle(texture=curtexture, size=self.size)

	def reset(self):
		self.isAlive = True	
		self.elapseTime = 0.0
		self.loopleft = self.loop
		self.refresh()

	def refresh(self):
		for key in self.variables:
			setattr(self, key, self.variables[key].get())

	def updateSequence(self):
		if self.playspeed > 0 and self.cellcount > 1:
			ratio = self.elapseTime / self.lifeTime
			ratio *= self.playspeed
			ratio %= 1.0
			index = int(math.floor(self.cellcount * ratio))
			if index == self.oldsequence:
				return
			if index == self.cellcount:
				index = self.cellcount - 1
			self.oldsequence = index
			self.curseq = [index % self.sequence[0], self.sequence[1]-int(index / self.sequence[0])-1]
			self.curseq = mul(self.curseq, self.cellsize)
			self.box.texture = self.texture.get_region(*(self.curseq + self.cellsize))

	def onUpdate(self):
		if not self.isAlive:
			return
	
		fFrameTime = getFrameTime()
		self.accTime += fFrameTime
		self.elapseTime += fFrameTime
		
		if self.elapseTime > self.lifeTime:
			self.elapseTime -= self.lifeTime
			if self.loopleft > 0:
				self.loopleft -= 1
			if self.loopleft == 0:
				self.setDead()
				return
			self.refresh()
		lifeRatio = self.elapseTime / self.lifeTime
		
		self.updateSequence()
		self.vel[1] -= Util.gGravity * self.gravity * fFrameTime
		self.pos = add(self.pos, mul(self.vel, fFrameTime))
		#check collision
		if self.collision:
			if self.pos[0] < 0.0:
				self.pos = (-self.pos[0], self.pos[1])
				self.vel[0] = -self.vel[0]
			elif self.pos[0] > Util.W - self.size[0]:
				self.pos = ((Util.W - self.size[0])* 2.0 - self.pos[0], self.pos[1])
				self.vel[0] = -self.vel[0]
			if self.pos[1] < 0.0:
				self.pos = (self.pos[0], -self.pos[1])
				self.vel[1] = -self.vel[1]
			elif self.pos[1] > Util.H - self.size[1]:
				self.pos = (self.pos[0], (Util.H - self.size[1]) * 2.0 - self.pos[1])
				self.vel[1] = -self.vel[1]

		if self.rotateVel != 0.0:
			self.rotation += self.rotateVel * fFrameTime
		if self.fade:
			opacity = 1.0 - lifeRatio
			opacity = max(min(opacity,1.0), 0.0)
			self.opacity = pow(opacity, self.fade)
		
	def setDead(self):
		self.isAlive = False
		if self.parent:
			self.parent.remove_widget(self)


class Emitter(Scatter):
	def __init__(self, parent_layer, info, num):
		Scatter.__init__(self , size=[0,0])
		self.do_translation = False
		self.do_rotation = False
		self.do_scale = False
		self.particles = []
		self.create_particle(info, num)
		self.parent_layer = parent_layer

	def create_particle(self, info, num):
		self.info = info
		for i in range(num):
			par = Particle()
			par.Create(**info)
			self.particles.append(par)
	
	def remove_particle(self):
		self.stop_particle()
		self.particles = []
	
	def play_particle(self):
		for i in self.particles:
			if not i.parent:
				self.add_widget(i)
			i.reset()
		if not self.parent:
			self.parent_layer.add_widget(self)
			
	def stop_particle(self):
		for i in self.particles:
			i.setDead()
		if self.parent:
			self.parent.remove_widget(self)

	def onUpdate(self):
		for i in self.particles:
			i.onUpdate()