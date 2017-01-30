import Utility as Util
from Utility import *

class FxMgr:
	inited = False
	images = {}
	sounds = {}
	emitters = []
	
	def __init__(self):
		self.inited = True
		for i in glob(os.path.join('effect', '*')):
			key = i.split(os.sep)[-1]
			ext = key[-3:].lower()
			key = key[:-4].lower()
			if ext in ['png','jpg']:
				self.images[key] = Image(source=i)
			elif ext == 'wav':
				self.sounds[key] = SoundLoader.load(i)

	def getTex(self, key):
		return self.images[key].texture
	
	def getImg(self, key):
		return self.images[key]
		
	def getSnd(self, key):
		return self.sounds[key]
		
	def clear_emitters(self):
		for i in self.emitters:
			i.clear_emitter()

	def add_emitters(self, emitter):
		self.emitters.append(emitter)
			
	def remove_emitters(self):
		self.emitters.remove_emitter()
	
	def onUpdate(self):
		for i in self.emitters:
			i.onUpdate()


class Var:
	def __init__(self, v1=None, v2=None):
		if v1 == None:
			return
			
		if v2 != None:
			self.v1 = v1
			self.v2 = v2
			if type(v1) == list or type(v1) == tuple:
				self.get = self.getRandList
			else:
				self.get = self.getRandScalar
		else:
			self.v1 = v1
			if type(v1) == list or type(v1) == tuple:
				self.get = self.getList
			else:
				self.get = self.getScalar
		
	def set(self, v1=None, v2=None):
		self.__init__(v1, v2)

	def get(self):
		pass

	def getList(self):
		return copy(self.v1)

	def getScalar(self):
		return self.v1

	def getRandList(self):
		return [random.uniform(self.v1[i],self.v2[i]) for i in range(len(self.v1))]

	def getRandScalar(self):
		return random.uniform(self.v1, self.v2)


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
		self.variables = {
		'lifeTime':Var(self.lifeTime),
		'gravity':Var(self.gravity),
		'vel':Var(self.vel),
		'rotateVel':Var(self.rotateVel),
		'rotation':Var(self.rotation),
		'scale':Var(self.scale),
		'opacity':Var(self.opacity)
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

		self.reset()
	
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
	def __init__(self, info, num):
		Scatter.__init__(self , size=[0,0])
		self.do_translation = False
		self.do_rotation = False
		self.do_scale = False
		self.particles = []
		self.add_particle(info, num)

	def clear_particle(self):
		for i in self.particles:
			i.setDead()
		if self.parent:
			self.parent.remove_widget(self)
			
	def add_particle(self, info, num):
		self.info = info
		for i in range(num):
			par = Particle()
			par.Create(**info)
			self.particles.append(par)
			self.add_widget(par)

	def reset(self):
		for i in self.particles:
			i.reset()

	def onUpdate(self):
		for i in self.particles:
			i.onUpdate()


class Emitters(Scatter):
	def __init__(self):
		Scatter.__init__(self, size=[0,0])
		self.do_translation = False
		self.do_rotation = False
		self.do_scale = False
		self.emitters=[]
	
	def clear_emitter(self):
		for i in self.emitters:
			i.clear_particle()
		if self.parent:
			self.parent.remove_widget(self)

	def add_emitter(self, emitter):
		self.emitters.append(emitter)
		self.add_widget(emitter)
	
	def reset(self):
		for i in self.emitters:
			i.reset()
			 	
	def onUpdate(self):
		for i in self.emitters:
			i.onUpdate()