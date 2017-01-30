import Utility as Util
from Utility import *

SHOWPROP_ENTER = 0
SHOWPROP_START = 1
SHOWPROP_EXIT = 2

#---------------------#
# CLASS : ShowPropStateMgr
#---------------------#
class ShowProp_Mgr(StateMachine):
	def __init__(self):
		self.inited = False
		self.addState(ShowProp_Enter()) # SHOWPROP_ENTER
		self.addState(ShowProp_Start()) # SHOWPROP_START
		self.addState(ShowProp_Exit()) # SHOWPROP_EXIT
		self.run()
	
	def setInited(self, inited):
		self.inited = inited
		
	def run(self):
		if self.inited != True:
			self.setInited(True)
			self.setState(SHOWPROP_ENTER)
			Util.getMyRoot().regist(self)
	
	def exit(self):
		Util.getMyRoot().remove(self)

# SHOWPROP_ENTER
class ShowProp_Enter(StateItem):		
	def onUpdate(self):
		self.setState(SHOWPROP_START)

# SHOWPROP_START
class ShowProp_Start(Widget, StateItem):
	pageItemCount = 10
	szItem = ''
			
	def __init__(self):
		super(ShowProp_Start, self).__init__()
		self.size = (500, 500)
		self.main = Scatter()
		self.main.size = self.size
		Util.getCenter(Util.WH)
		self.main.do_rotation = False
		with self.main.canvas:
			Color(0.5,0.5,0.5)
			Rectangle(size=self.size)

		self.add_widget(self.main)
			
		self.frame = BoxLayout(orientation='vertical')
		self.frame.size = Util.calcSize(self.size, .8, .8)
		self.frame.center = Util.getCenter(self.size)
		self.main.add_widget(self.frame)
		 
		# Head
		self.myHead = BoxLayout(orientation='horizontal')
		self.itemName = TextInput(text='input', size_hint_x=.5)
		self.itemName.multiline = False
		def cleartext(instance, bFocus):
			if bFocus:
				instance.text=''
		self.btn_ok = Button(text='Ok', size_hint_x=.25)
		self.btn_close = Button(text='Close', size_hint_x=.25)
		self.itemName.bind(focus=cleartext)
		self.btn_ok.bind(on_release = self.press_Ok)
		self.btn_close.bind(on_release = self.press_Close)
		self.myHead.add_widget(self.itemName)
		self.myHead.add_widget(self.btn_ok)
		self.myHead.add_widget(self.btn_close)
		self.frame.add_widget(self.myHead)

		# Property
		self.btn_parent = Button(text='..')
		self.btn_parent.bind(on_release = self.goParent)
		self.frame.add_widget(self.btn_parent)
		
		self.propItem = []
		for i in range(self.pageItemCount):
			self.propItem.append(Button())
			self.propItem[i].bind(on_release = self.viewItem)
			self.frame.add_widget(self.propItem[i])
		
		# End	
		self.myEnd = BoxLayout()
		self.pageLabel = Label(text='0/0')
		self.itemInfo = Button(text='Info')
		self.prevBtn = Button(text='<<')
		self.nextBtn = Button(text='>>')
		self.itemInfo.bind(on_release=self.viewSelfInfo)
		self.prevBtn.bind(on_release=self.setPrevPage)
		self.nextBtn.bind(on_release=self.setNextPage)
		self.myEnd.add_widget(self.pageLabel)
		self.myEnd.add_widget(self.itemInfo)
		self.myEnd.add_widget(self.prevBtn)
		self.myEnd.add_widget(self.nextBtn)
		self.frame.add_widget(self.myEnd)
				
		self.init()

	def init(self):
		self.oldPage = 0
		self.curPage = 0
		self.numPage = 0
		self.numProp = 0
		self.listProp = []
		self.btn_parent.text = ''
		self.itemName.text = ''
		self.szItem = ''
		self.updatePropList()
			
	def press_Ok(self, inst):
		self.oldPage = 0
		self.szItem = self.itemName.text
		self.showProp()
	
	def press_Close(self, inst):
		self.setState(SHOWPROP_EXIT)
		
	def showProp(self, curPage = 1):
		if self.szItem == '':
			self.init()
			return
		try:
			exec 'self.listProp = dir(' + self.szItem + ')'
			self.numProp = len(self.listProp)
			self.numPage = int(math.ceil(float(self.numProp) / float(self.pageItemCount)))
			self.curPage = curPage
			self.updatePropList()
		except:
			self.init()
			return
		#self.itemName.text = self.szItem
		#self.itemName.scroll_x = 0

	def updatePropList(self):
		index = self.szItem.rfind('.')
		if index >-1:
			self.btn_parent.text = self.szItem[index+1:] + os.sep
		else:
			self.btn_parent.text = ('None' if self.szItem == '' else self.szItem+os.sep)

		n1 = (self.curPage-1) * self.pageItemCount
		n2 = self.pageItemCount
		if self.curPage >= self.numPage:
			n2 = self.numProp % self.pageItemCount
			if n2 == 0 and self.numProp > 0:
				n2 = self.pageItemCount
		for i in range(self.pageItemCount):
			if i < n2:
				self.propItem[i].text = str(n1+i+1)+'.'+self.listProp[n1+i]
			else:
				self.propItem[i].text = ''
				
		# updatePageLabel
		self.pageLabel.text = str(self.curPage) + '/' + str(self.numPage) + '(' + str(self.numProp) + ')'

	def setNextPage(self, inst):
		if self.curPage < self.numPage:
			self.curPage += 1
			self.updatePropList()

	def setPrevPage(self, inst):
		if self.curPage > 1:
			self.curPage -= 1
			self.updatePropList()
	
	def goParent(self, inst):
		index = self.szItem.rfind('.')
		if index > -1:
			self.szItem = self.szItem[:index]
			self.showProp(self.oldPage)

	def viewSelfInfo(self, inst):
		if self.szItem == '':
			return
		else:
			doc = ''
			exec 'doc = ' + self.szItem + '.__doc__'
			if doc:
				try:
					docModal = ModalView(size_hint = (1,1), center= Util.getCenter(Util.WH), auto_dismiss=True)
					btn = Button()
					btn.bind(on_release = docModal.dismiss)
					label = Label(text=self.szItem +'\n'+doc)
					docModal.add_widget(btn)
					docModal.add_widget(label)
					self.fDebug = label.size[0]
					docModal.open()
				except:
					return		

	def viewItemInfo(self, inst):
		if self.szItem == '':
			return
		else:
			doc = ''
			exec 'doc = ' + self.szItem + '.__doc__'
			if doc:
				try:
					docModal = ModalView(size_hint = (1,1), center= Util.getCenter(Util.WH), auto_dismiss=True)
					btn = Button()
					btn.bind(on_release = docModal.dismiss)
					label = Label(text=self.szItem +'\n'+doc)
					docModal.add_widget(btn)
					docModal.add_widget(label)
					self.fDebug = label.size[0]
					docModal.open()
				except:
					return
				
	def viewItem(self, inst):
		index = inst.text.find('.')
		if index > -1:
			self.oldPage = self.curPage
			self.szItem += inst.text[index:]
			self.showProp()
		
	def onEnter(self):
		Util.getMyRoot().add_widget(self)
		
	def onExit(self):
		self.stateMgr.setInited(False)
		Util.getMyRoot().remove_widget(self)

# SHOWPROP_EXIT
class ShowProp_Exit(StateItem):
	def onExit(self):
		self.stateMgr.exit()