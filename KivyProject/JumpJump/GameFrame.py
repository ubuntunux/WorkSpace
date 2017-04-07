from Utility import *
from ResourceMgr.ResourceMgr import gResMgr
from Stage import gStageMgr
from Character import gCharacterMgr
from Constants import *


class Board(Singleton):
  def __init__(self):
    self.widget = Widget()
    self.font_size = "20dp"
    self.font_height = kivy.metrics.dp(20)
    self.score = 0
    self.score_label = Label(text="", center=(cX, H - self.font_height), font_size=self.font_size)
    self.high_jump = 0
    self.high_jump_label = Label(text="", center=(cX, H - self.font_height*2), font_size=self.font_size)
    self.combo = 0
    self.combo_label = Label(text="", center=(cX, H - self.font_height*3), font_size=self.font_size)
    self.widget.add_widget(self.score_label)
    self.widget.add_widget(self.high_jump_label)
    self.widget.add_widget(self.combo_label)
  
  def reset(self):
    self.setScore(0)
    self.setHighJump(0)
    self.setCombo(0)
    
  def addScore(self, score):
    self.setScore(self.score + score)
    
  def setScore(self, score):
    self.score = score
    self.score_label.text = "Score : " + str(self.score)
    
  def addHighJump(self):
    self.setHighJump(self.high_jump + 1)
    
  def setHighJump(self, value):
    self.high_jump = value
    self.high_jump_label.text = "HighJump : " + str(self.high_jump)
    
  def addCombo(self):
    self.setCombo(self.combo + 1)
    
  def setCombo(self, combo):
    self.combo = combo
    self.combo_label.text = "Combo : " + str(self.combo)
    

class StageEditor(Singleton):
  def __init__(self):
    self.count = 15
    self.props = gResMgr.getProperty("character")
    self.totalProps = len(self.props.properties)
    self.page = 0
    self.maxPage = int(self.totalProps / self.count)
    self.btn_size = W / float(self.count)
    self.buttons = []
    self.layout_edit = BoxLayout(orientation="horizontal", size_hint=(None,None), size=(W, self.btn_size))
  
  def clear(self):
    self.layout_edit.clear_widgets()
    self.buttons = []    
         
  def reset(self):
    self.build(0)
    
  def prevPage(self, inst):
   if self.page > 0:
     self.build(self.page - 1)
     
  def nextPage(self, inst):
    if self.page < self.maxPage:
      self.build(self.page + 1)
      
  def create_character(self, inst):
    gStageMgr.create_character(inst.index)
    
  def build(self, page):
    self.clear()
    self.page = page
    color = (1,1,1,0.5)
    # previous button
    btn = Button(text="<<", background_color=color)
    btn.bind(on_press=self.prevPage)
    self.buttons.append(btn)
    self.layout_edit.add_widget(btn)
    # create buttons  
    for i in range(self.count-2):
      index = i + self.page * (self.count-2)
      btn = Button(background_color=color)
      self.buttons.append(btn)
      if index < self.totalProps:
        prop = self.props.properties[index]
        btn.index = index
        with btn.canvas:
          Color(*color)
          Rectangle(texture=prop["image"].texture, pos=((i+1)*self.btn_size,0), size=(self.btn_size, self.btn_size))
        btn.bind(on_press=self.create_character)
      self.layout_edit.add_widget(btn)
    # next button
    btn = Button(text=">>", background_color=color)
    btn.bind(on_press=self.nextPage)
    self.buttons.append(btn)
    self.layout_edit.add_widget(btn)
      
      
class GameScreen(Singleton):
  MODE_PLAY = 1
  MODE_EDIT = 2
  def __init__(self):
    self.mode = self.MODE_PLAY
    self.screen = Screen(name="game screen")
    with self.screen.canvas:
      self.color = Color(0,0,0,1)
      Rectangle(pos=(0,0), size=WH)
    self.stageEditor = StageEditor.instance()
    self.layout_edit = self.stageEditor.layout_edit
     
    # add bg
    self.layer_bg = Widget()
    self.layer_bg.name="layer_bg"
    self.screen.add_widget(self.layer_bg)

    # add fx layer
    self.layer_fx = Widget()
    self.layer_fx.name = "layer_fx"
    self.screen.add_widget(self.layer_fx)
    
    # add ui layer
    self.layer_ui = Widget()
    self.layer_ui.name = "layer_ui"
    self.layer_ui = FloatLayout(size_hint=(1,1))
    self.screen.add_widget(self.layer_ui)
    
    # game button
    self.btn_left = Button(size_hint=(0.5, 1), background_color=(1,1,1,0))
    self.btn_right = Button(size_hint=(0.5, 1), background_color=(1,1,1,0), pos_hint={"right":1}) 
    
    # right menu
    self.rbtn_items = []
    self.rlayout_item = BoxLayout(orientation='vertical', size_hint=(None, None), size=(H * 0.2, H*0.8), pos_hint={"top":1.0, "right":1.0}) 
    self.screen.add_widget(self.rlayout_item)
  
  def set_layout_edit(self, layout_edit): 
    self.layout_edit = layout_edit
    
  def bind_btn_item(self, func, title, index):
    while index >= len(self.rbtn_items):
      btn = Button(background_color=(1,1,1,0.2))
      self.rbtn_items.append(btn)
      self.rlayout_item.add_widget(btn)   
    self.rbtn_items[index].text = title
    self.rbtn_items[index].bind(on_press=lambda inst:func())
      
  def bind_btn_left(self, func):
    self.btn_left.bind(on_press=lambda inst:func(True))
    self.btn_left.bind(on_release=lambda inst:func(False))
  
  def bind_btn_right(self, func):
    self.btn_right.bind(on_press=lambda inst:func(True))
    self.btn_right.bind(on_release=lambda inst:func(False))
  
  def recvResourceName(self, resName):
    log(resName)
  
  def setPlayMode(self):
    self.mode = self.MODE_PLAY
    if self.btn_left.parent is None:
      self.layer_ui.add_widget(self.btn_left)
    if self.btn_right.parent is None:
      self.layer_ui.add_widget(self.btn_right)
    if self.layout_edit.parent:
      self.screen.remove_widget(self.layout_edit)
    
  def setEditMode(self):
    self.mode = self.MODE_EDIT
    if self.btn_left.parent:
      self.layer_ui.remove_widget(self.btn_left)
    if self.btn_right.parent: 
      self.layer_ui.remove_widget(self.btn_right)
    if self.layout_edit.parent is None:
      self.screen.add_widget(self.layout_edit)
     
  def reset(self):
    self.clear_widgets()
    self.stageEditor.reset()
    self.setPlayMode()
    
  def show(self):
    gMyRoot.add_screen(self.screen)
    gMyRoot.current_screen(self.screen)
    
  def close(self):
    self.clear_widgets()
    gMyRoot.remove_screen(self.screen)
      
  def screen_black(self):
    self.color.a = 1.0
    
  def screen_transition(self, t=0.5):
    self.color.a = 1.0
    anim = Animation(a = 0.0, duration = t)
    anim.start(self.color)
    
  def clear_widgets(self):
    self.clear_bg()
    self.clear_fx()
    self.clear_ui()
  
  def clear_fx(self): self.layer_fx.clear_widgets() 
  def clear_ui(self):self.layer_ui.clear_widgets()  
  def clear_bg(self): self.layer_bg.clear_widgets()
  def add_to_fx(self, widget): self.layer_fx.add_widget(widget)
  def add_to_ui(self, widget): self.layer_ui.add_widget(widget)   
  def add_to_bg(self, widget): self.layer_bg.add_widget(widget)
  def remove_from_fx(self, widget):
    if widget in self.layer_fx.children:
      self.layer_bg.remove_widget(widget)
  def remove_from_bg(self, widget):
    if widget in self.layer_bg.children:
      self.layer_bg.remove_widget(widget)
  def remove_from_ui(self, widget):
    if widget in self.layer_ui.children:
      self.layer_ui.remove_widget(widget)


class GameFrame(Singleton):
  STATE_NONE = 0
  STATE_PLAY = 1
  STATE_PAUSE = 2
  STATE_END = 3
  
  def __init__(self):
    self.callback_on_closed = None
    self.ui = GameScreen()
    self.ui.bind_btn_item(self.togglePlay, "Play/Edit", 0)
    self.ui.bind_btn_item(self.reset, "Reset", 1)
    self.ui.bind_btn_item(self.togglePlay, "New", 2)
    self.ui.bind_btn_item(self.togglePlay, "Save", 3)
    self.ui.bind_btn_item(self.togglePlay, "Load", 4)
    self.board = Board()
    self.stageMgr = None
    self.state = self.STATE_NONE
    
  def togglePlay(self):
    if self.isStatePause():
      self.set_state_play()
      self.ui.setPlayMode()
    elif self.isStatePlay():
      self.set_state_pause()
      self.ui.setEditMode()
    if self.stageMgr:
      self.stageMgr.togglePlay()
      
  def reset(self, *args):
    gStageMgr.setEnd()
    self.set_state_end()
    self.start(self.callback_on_closed)
  
  def isStatePlay(self):
    return self.state == self.STATE_PLAY
  
  def set_state_play(self):
    self.state = self.STATE_PLAY
  
  def isStatePause(self):
    return self.state == self.STATE_PAUSE
      
  def set_state_pause(self):
    self.state = self.STATE_PAUSE
     
  def set_state_end(self):
    self.state = self.STATE_END
    
  def buttonBind(self, lfunc, rfunc):
    self.ui.bind_btn_left(lfunc)
    self.ui.bind_btn_right(rfunc)
    
  def start(self, callback_on_closed=None):
    self.callback_on_closed = callback_on_closed
    
    # clear ui
    self.ui.reset()
    self.ui.add_to_ui(self.board.widget)
    
    self.stageMgr = gStageMgr
    self.stageMgr.setParentLayer(self.ui.layer_bg)
    self.stageMgr.reset()
    
    gMyRoot.setTouchPrev(self.touchPrev)
    gMyRoot.regist(self)
    
    self.ui.screen_transition(1.0)
    self.ui.screen_black()
    self.ui.show()
    
    self.set_state_play()
    
  def touchPrev(self):
    self.ui.close()
    gMyRoot.remove(self)
    gMyRoot.setTouchPrev(None)
    if self.callback_on_closed:
      self.callback_on_closed()
    
  def update(self, dt):
    if self.state == self.STATE_PLAY:
      gStageMgr.update()
      if gStageMgr.isDone():
        gStageMgr.setEnd()
        self.set_state_end()

gGameFrame = GameFrame.instance()
