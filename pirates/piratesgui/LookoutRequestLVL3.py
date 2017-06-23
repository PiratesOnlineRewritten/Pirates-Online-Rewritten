from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.ListFrame import ListFrame
from pirates.piratesgui.OptionItemGui import OptionItemGui

class LookoutRequestLVL3(DirectFrame):

    def __init__(self, name, titleTextScale=None, itemList=None, optionsFor=None):
        self.width = PiratesGuiGlobals.LookoutRequestLVL3Width
        self.height = PiratesGuiGlobals.LookoutRequestLVL3Height
        DirectFrame.__init__(self, relief=DGG.RIDGE, state=DGG.NORMAL, frameColor=(0,
                                                                                   0,
                                                                                   0,
                                                                                   0), borderWidth=PiratesGuiGlobals.BorderWidth, frameSize=(0, self.width, 0, self.height))
        self.initialiseoptions(LookoutRequestLVL3)
        base.localAvatar.guiMgr.lookoutPage.title = name
        self.optionsFor = optionsFor
        self.name = name
        if itemList:
            self.itemList = itemList
        else:
            self.itemList = None
        self.activityListItems = ListFrame(0.8, None, 'blah', self, frameColor=(0,
                                                                                0,
                                                                                0,
                                                                                0))
        self.activityListItems.itemBuffer = 0.04
        self.activityListItems.setup()
        self.activityList = DirectScrolledFrame(parent=self, frameSize=(0, 0.9, 0,
                                                                        0.77), relief=DGG.GROOVE, state=DGG.NORMAL, frameColor=(0,
                                                                                                                                0,
                                                                                                                                0,
                                                                                                                                0), borderWidth=PiratesGuiGlobals.BorderWidth, canvasSize=(0, 0.7, 0, self.activityListItems['frameSize'][3]), verticalScroll_frameColor=PiratesGuiGlobals.ScrollbarColor, verticalScroll_borderWidth=(0.0075,
                                                                                                                                                                                                                                                                                                                                       0.0075), verticalScroll_frameSize=(0, PiratesGuiGlobals.ScrollbarSize, 0, self.height), verticalScroll_thumb_frameColor=PiratesGuiGlobals.ButtonColor2, verticalScroll_incButton_frameColor=PiratesGuiGlobals.ButtonColor2, verticalScroll_decButton_frameColor=PiratesGuiGlobals.ButtonColor2, sortOrder=5, pos=(0.115,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         0.2))
        self.activityListItems.reparentTo(self.activityList.getCanvas())
        self.selectedItem = None
        self.optionsPanel = None
        self.parentPanel = None
        self.acceptButton = None
        return

    def createDoneButton(self):
        lookoutUI = loader.loadModel('models/gui/lookout_gui')
        self.acceptButton, self.acceptButtonText = self.parentPanel.parentPanel.createButtonAndText(imageInfo={'textureCard': lookoutUI,'imageName': 'lookout_accept','buttonPos': (0.54, 0, 0.15),'buttonScale': 0.3,'clickCommand': self.confirmOptions}, textInfo=PLocalizer.LookoutConfirm)

    def confirmOptions(self):
        if self.optionsFor != None:
            currGameType = self.optionsFor
            options = []
            for currOption in self.activityListItems.items:
                optionPair = currOption.getOptionValuePair()
                options.append(optionPair)

            self.parentPanel.storedOptions[currGameType] = options
        self.parentPanel.optionsClose()
        return

    def getGameOptions(self, gameType, clear=False):
        options = self.parentPanel.storedOptions.get(gameType, [])
        if clear and len(options) > 0:
            del self.parentPanel.storedOptions[gameType]
        return options

    def setParentPanel(self, parentPanel):
        self.parentPanel = parentPanel
        if parentPanel:
            self.createDoneButton()
            self.activityList.wrtReparentTo(parentPanel.parentPanel)
            DirectFrame.hide(self)

    def destroy(self):
        self.selectedItem = None
        self.parentPanel = None
        if self.activityList:
            self.activityList.destroy()
            self.activityList = None
        if self.activityListItems:
            self.activityListItems.destroy()
            self.activityListItems = None
        if self.acceptButton:
            self.acceptButton.destroy()
            self.acceptButton = None
        DirectFrame.destroy(self)
        return

    def getItemChangeMsg(self):
        return self.taskName('gameTypeChanged')

    def getItemList(self):
        return self.itemList

    def createNewItem(self, item, parent, itemType=None, columnWidths=[], color=None):
        newItem = OptionItemGui(item, parent, frameColor=(0, 0, 0, 0), titleWrapLen=4)
        newItem.setup()
        return newItem

    def hide(self):
        self.activityList.hide()
        self.acceptButton.hide()

    def show(self, gameType, selectedItem):
        itemList = self.parentPanel.determineLvl3ItemList(selectedItem)
        if self.itemList != itemList:
            self.itemList = itemList
            self.activityListItems._handleItemChange()
            self.activityList['canvasSize'] = (
             0, 0.7, 0, self.activityListItems['frameSize'][3])
        self.activityList.show()
        self.acceptButton.show()
        self.title = self.name