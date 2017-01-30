import Utility as Util
from Utility import *

from Globals import *
from MyGame import gMyGame

#---------------------#
# Global instance
#---------------------#
def setGlobalInstance():
  global gMenuScreen, gMainMenu
  gMenuScreen = MyGame_Screen.instance()
  gMainMenu = MainMenu_Mgr.instance()

#---------------------#
# CLASS : MainMenu
#---------------------#
class MyGame_Screen(Screen, Singleton):      
  def __init__(self):
    Screen.__init__(self, name="MainMenu")
    
    self.callback_btnload = None
    
    layout = BoxLayout(orientation="vertical", pos=mul(WH, 0.25),  size_hint=(0.5, 0.5))
    self.add_widget(layout)
    
    # start button
    self.btn_load = []
    for i in range(gSaveCount):
      btn = Button(text='New')
      self.btn_load.append(btn)
      layout.add_widget(btn)
    
    # exit button 
    self.btn_Exit = Button(text="Exit")
    layout.add_widget(self.btn_Exit)
    
  def refreshFilename(self):
    for i, btn in enumerate(self.btn_load):
      btn.text = gSaveFile[i] if os.path.isfile(gSaveFile[i]) else 'New'
    
  def getButtonIndex(self, btn):
    return self.btn_load.index(btn)
 
  def bind_LoadButton(self, func):
   for btn in self.btn_load:
     btn.bind(on_release=func)
  
  def bind_ExitButton(self, func):
    self.btn_Exit.bind(on_release=func)
   
  def create_screen(self):
    gMyRoot.add_screen(self)
    gMyRoot.current_screen(self)
    self.refreshFilename()
    
  def remove_screen(self):
    gMyRoot.remove_screen(self)

#---------------------#
# CLASS : MainMenu
#---------------------#
class MainMenu_Mgr(Singleton): 
  def __init__(self):
    gMyGame.bind_OnExit(self.init)
    gMenuScreen.bind_LoadButton(self.load_game)
    gMenuScreen.bind_ExitButton(self.exit)
    self.init()
    
  def init(self, *args):
    gMyRoot.regist(self)
    gMenuScreen.create_screen()
    
  def load_game(self, inst):
    gMenuScreen.remove_screen()
    gMyRoot.remove(self)
    index = gMenuScreen.getButtonIndex(inst)
    gMyGame.load(gSaveFile[index])
    
  def update(self, dt):
    pass
    
  def exit(self, *args):
    gMyRoot.exit()

#---------------------#
# set global instance
#---------------------#
setGlobalInstance()

if __name__ in ('__android__', '__main__'):
  gMyRoot.run( gMainMenu )