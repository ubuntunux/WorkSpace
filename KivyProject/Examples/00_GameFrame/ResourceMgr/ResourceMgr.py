import Utility as Util
from Utility import *

#---------------------#
# Global instance
#---------------------#
def setGlobalInstance():
  global gResMgr
  gResMgr = ResourceMgr.instance()
  
class Resource:
 def __init__(self, key):
  self.key = key
  self.tag = []
  self.img = []
  self.snd = []
  
 def addTag(self, tag):
   if not self.isTag(tag):
     self.tag.append(tag)
 
 def isTag(self, tag):
    if type(tag) == tuple or type(tag) == list:
      for i in tag:
        if i in self.tag:
          return True
      return False
    else:
      return tag in self.tag

 def addImg(self, img):
  self.img.append(img)

 def addSnd(self, snd):
  self.snd.append(snd)

 def getName(self):
  return self.key
  
 def getImg(self, index = 0):
  if len(self.img) > index:
   return self.img[index]
    
 def getTex(self, index = 0):
  if len(self.img) > index:
   return self.img[index].texture

 def getSnd(self, index = 0):
  if len(self.snd) > index:
   return self.snd[index]

 def getSnd_Rnd(self):
  if len(self.snd) > index:
   return random.choice(self.snd)
 
 def playSnd(self, index = 0):
  if len(self.snd) > index:
   self.snd[index].play()

 def playSnd_Rnd(self):
  if len(self.snd) > 0:
   random.choice(self.snd).play()

class ResourceMgr(Singleton):
 inited = False
 resources = {}
 images = {}
 sounds = {}
 def __init__(self):
  if self.inited:
   return
  self.inited = True
  ignoredir = os.path.join(os.path.abspath('.'), '.kivy')
  
  # write resource list
  f=open('resources_log.txt','w')
  for dirname, dirnames, filenames in os.walk('.'):
   if os.path.abspath(dirname)[:len(ignoredir)] == ignoredir:
    continue
   for filename in filenames:
    ext = os.path.splitext(filename)[1].lower()
    key = os.path.splitext(filename)[0].lower()
    # extract key from number indexed filename
    if key.rfind('_') > 0:
     try:num = int(key[key.rfind('_')+1:])
     except:pass
     else:key = key[:key.rfind('_')]
    filepath = os.path.join(dirname, filename)
    res = self.resources[key] if key in self.resources else Resource(key)
    if ext in ['.png','.jpg']:
     res.addImg(Image(source = filepath))
     res.addTag('image')
     self.images[key] = res
    elif ext in ['.wav', '.ogg']:
     res.addSnd(SoundLoader.load(filepath))
     res.addTag('sound')
     self.sounds[key] = res
    else:
     continue
    [res.addTag(tag) for tag in filepath.split(os.sep)[1:-1]]
    self.resources[key] = res
    # write resource list
    f.write(filepath+'\n')
  
  # write resource list
  f.close()

 def getCount(self):
  return len(self.resources)
 
 def getResourceNames(self):
   return self.resources.keys()
    
 def getResourceList(self):
   return self.resources.values()
 
 def getImageNames(self):
   return self.images.keys()
   
 def getImageList(self):
   return self.images.values()
 
 def getSoundNames(self):
   return self.sounds.keys()
   
 def getSoundList(self):
   return self.sounds.values()
   
 def getResource(self, name = ''):
   return self.resources[name]
  
 def getResource_Rnd(self):
  return random.choice(self.resources.values())

 def getImg(self, name='', index=0):
  return self.images[name].getImg(index)

 def getImg_Rnd(self):
  return random.choice(self.images.values()).getImg()

 def getTex(self , name='', index=0):
  return self.images[name].getTex(index)

 def getTex_Rnd(self):
  return random.choice(self.images.values()).getTex()

 def getSnd(self , name='', index=0):
  return self.sounds[name].getSnd(index)

 def getSnd_Rnd(self):
  return random.choice(self.sounds.values()).getSnd_Rnd()
 
 def playSnd(self, name='', index = 0):
  self.sounds[name].getSnd(index)

 def playSnd_Rnd(self):
  random.choice(self.sounds.values()).playSnd_Rnd()
  
#---------------------#
# set global instance
#---------------------#
setGlobalInstance()