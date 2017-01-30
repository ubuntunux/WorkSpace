import Utility as Util
from Utility import *

class Race:
  Human = 0
  Orc = 1
  Devil = 2
  Ogre = 3
  
class CharacterInfo(Singleton):
  def __init__(self, name, male, age, race):
    self.name = name
    self.male = male
    self.age = age
    self.race = race
    
class Player(Singleton):
  def __init__(self):
    self.myInfo = CharacterInfo("Julian", True, 25, Race.Human)