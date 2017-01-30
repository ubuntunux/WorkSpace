import Utility as Util
from Utility import *

from Animal import *
from Particle import *
from Shaders import *

class Resource:
	def __init__(self, key, img, snd):
		self.key = key
		self.img = img
		self.snd = snd

	def getName(self):
		return self.key

	def getImg(self):
		return self.img
				
	def getTex(self):
		return self.img.texture

	def getSnd(self):
		return random.choice(self.snd)


class Resources:
	inited = False
	resources = []
	def __init__(self):
		if self.inited:
			return
		self.inited = True
		for i in glob(os.path.join('images', '*.png')):
			key = i.split(os.sep)[-1]
			key = key[:-4]
			snd = []
			for n in range(3):
				filename = 'sounds'+ os.sep + key + '_' + str(n) + '.wav'
				if os.path.isfile(filename):
					snd.append(SoundLoader.load(filename))
			img = Image(source = i)
			self.resources.append(Resource(key, img, snd))
		self.count = len(self.resources)

	def getCount(self):
		return self.count
	
	def getResource(self, index = -1):
		if index == -1:
			return random.choice(self.resources)
		return self.resources[index]
		
	
class Music():
	def __init__(self):
		self.sound = None
		
	def start(self):
		return
		if self.sound is None:
			self.sound = SoundLoader.load("music.ogg")
			self.sound.volume = 0.8
			self.sound.play()
			self.sound.on_stop = self.sound.play


class MyGame(Widget):
	def __init__(self):
		self.FxMgr = FxMgr()
		self.resources = Resources()
		self.music = Music()
		self.music.start()
		Widget.__init__(self, size=Util.WH, orientation='vertical')
		self.background = ShaderScatter(shader=fs_panning, uv_panning=[.5,0], source='Jungle_Background_-_by-vectorjungle.jpg', size=Util.WH)
		self.add_widget(self.background)
		res = self.resources.getResource()
		self.target = MoveAnimal(res)
		self.add_widget(self.target)

	def preload_Fx(self):
		particleInfo = dict(loop=-1, source='star.png', #texture=self.FxMgr.getTex('star'),
			pos=Var([0,0],[300,300]), vel=Var([gVel, gJump*0.7], [-gVel, gJump*0.5] ),
			rotateVel=Var(0.0), lifeTime=Var(10.0),
			scale=Var(1.0,0.5), collision=True
			)
		emitter=Emitter(particleInfo, 1)
		emitters=Emitters()
		emitters.add_emitter(emitter)
		particleInfo = dict(loop=-1, texture=self.FxMgr.getTex('explosion'),
			pos=Var([500,500],[300,300]), vel=Var([gVel*.1, gJump*0.1], [-gVel*.1, gJump*0.2] ),
			rotateVel=Var(0.0), lifeTime=Var(0.1,0.3), collision=True,
			scale=Var(2.0,3.5), sequence=[4,4], gravity=Var(0.0), playspeed=0.0, fade=1.5
			)
		emitter = Emitter(particleInfo, 3)
		emitters.add_emitter(emitter)
		getMyRoot().add_widget(emitters)
		self.FxMgr.add_emitters(emitters)

	def preUpdate(self):
		getMyRoot().add_widget(self)
		self.preload_Fx()
	
	def postUpdate(self):
		self.FxMgr.clear_emitters()
		if self.parent:
			self.parent.remove_widget(self)

	def onUpdate(self):
		self.FxMgr.onUpdate()
		if self.target:
			if not self.target.bDead:
				self.target.onUpdate()
