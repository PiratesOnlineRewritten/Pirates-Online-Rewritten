from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.ListFrame import ListFrame
from pirates.world import GameTypeGlobals
from pirates.piratesgui.ButtonListItem import ButtonListItem
from pirates.piratesgui.LookoutListItem import LookoutListItem
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui import GuiButton

class OptionItemGui(DirectFrame):
    Width = PiratesGuiGlobals.OptionItemWidth
    Height = PiratesGuiGlobals.OptionItemHeight
    TOPLEVEL_GUI_FILE = 'models/gui/toplevel_gui'
    CHAR_GUI_FILE = 'models/gui/char_gui'

    def __init__(self, item, parent=None, textScale=None, itemHeight=None, frameColor=(0.1, 0.1, 1, 0.08), titleWrapLen=None, **kw):
        if itemHeight == None:
            itemHeight = OptionItemGui.Height
        optiondefs = (
         (
          'state', DGG.NORMAL, None), ('frameColor', frameColor, None), ('borderWidth', PiratesGuiGlobals.BorderWidth, None), ('frameSize', (0.0, OptionItemGui.Width, 0.0, itemHeight), None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.initialiseoptions(OptionItemGui)
        self.textScale = 0.04
        if textScale:
            self.textScale = textScale
        self.item = item
        self.value = ''
        self.optionUI = None
        self.selectedItem = None
        self.borderFrame = None
        self.optionType = None
        self.titleWrapLen = titleWrapLen
        return

    def setup(self):
        self.optionType = self.item['ValueType']
        self._createIface()

    def destroy(self):
        self._destroyIface()
        DirectFrame.destroy(self)
        self.ignoreAll()

    def _createIface(self):
        self._createLabel()
        self._createOptionEntry()

    def _createLabel(self):
        if self.optionType == PiratesGuiGlobals.UIItemType_Choice:
            self.titleWrapLen = None
        textFg = PiratesGuiGlobals.TextFG1
        self.descText = DirectLabel(parent=self, relief=None, text=self.item['Text'] + ':', text_align=TextNode.ALeft, text_scale=self.textScale, text_fg=textFg, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=self.titleWrapLen, textMayChange=1, pos=(0, 0, self.getHeight() / 2))
        return

    def _createOptionEntry(self):
        if self.optionType == PiratesGuiGlobals.UIItemType_Label:
            self.optionUI = DirectLabel(parent=self, relief=None, text=str(self.item['Value']), text_align=TextNode.ALeft, text_scale=self.textScale, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.3, 0, self.getHeight() / 2))
        elif self.optionType == PiratesGuiGlobals.UIItemType_Choice:
            lookoutUI = loader.loadModel('models/gui/lookout_gui')
            check_on = lookoutUI.find('**/lookout_submit')
            check_off = lookoutUI.find('**/lookout_submit_disabled')
            if self.value == '':
                self.value = 0
            self.optionItems = DirectCheckButton(parent=self, scale=0.05, indicatorValue=self.value, boxImageScale=4, command=self.itemChecked, pos=(0.78, 0, self.getHeight() / 2))
        elif self.optionType == PiratesGuiGlobals.UIItemType_ListItem:
            lookoutUI = loader.loadModel('models/gui/lookout_gui')
            charUI = loader.loadModel(self.CHAR_GUI_FILE)
            charGui_slider = charUI.find('**/chargui_slider_large')
            charGui_slider_thumb = charUI.find('**/chargui_slider_node')
            self.optionItems = ListFrame(0.4, None, 'blah', self, frameColor=(0, 0,
                                                                              0,
                                                                              0))
            self.optionItems.itemBuffer = 0.008
            self.optionItems.setup()
            self.optionUI = DirectScrolledFrame(parent=self, frameSize=(0, 0.45, 0,
                                                                        0.3), relief=DGG.GROOVE, state=DGG.NORMAL, frameColor=(0,
                                                                                                                               0,
                                                                                                                               0,
                                                                                                                               0), borderWidth=PiratesGuiGlobals.BorderWidth, canvasSize=(0, 0.38, 0, self.optionItems['frameSize'][3]), verticalScroll_frameColor=(0,
                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                    0), verticalScroll_thumb_frameColor=(0,
                                                                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                                                                         0), verticalScroll_incButton_frameColor=(0,
                                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                                  0), verticalScroll_decButton_frameColor=(0,
                                                                                                                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                                                                                                                           0), verticalScroll_image=charGui_slider, verticalScroll_image_scale=(0.12,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                0.28), verticalScroll_image_pos=(0.4195,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 0.15), verticalScroll_image_hpr=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  90), verticalScroll_frameSize=(0, PiratesGuiGlobals.ScrollbarSize, 0, OptionItemGui.Height * 3), verticalScroll_thumb_image=charGui_slider_thumb, verticalScroll_thumb_image_scale=(0.35,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      0.35,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      0.35), sortOrder=5, pos=(0.3, 0, self.getHeight() / 2 - 0.15))
            self.optionUI.guiItem.getVerticalSlider().clearLeftButton()
            self.optionUI.guiItem.getVerticalSlider().clearRightButton()
            self.optionUI.guiItem.getVerticalSlider().setRange(-1, 1)
            self.optionUI.guiItem.getHorizontalSlider().clearLeftButton()
            self.optionUI.guiItem.getHorizontalSlider().clearRightButton()
            self.optionUI.guiItem.getHorizontalSlider().setRange(-1, 1)
            self.createFrame()
            self.optionItems.reparentTo(self.optionUI.getCanvas())
        return

    def getItemChangeMsg(self):
        return self.taskName('gameTypeChanged')

    def getItemList(self):
        itemList = []
        for currValue in self.item['Values']:
            itemList.append({'Type': 'Literal','Text': str(currValue),'Value': currValue})

        return itemList

    def createNewItem(self, item, parent, itemType=None, columnWidths=[], color=None):
        newItem = ButtonListItem(item, 0.08, 0.38, parent, parentList=self, txtColor=color, pressEffect=False, image=GuiButton.GuiButton.genericButton, frameColor=(0,
                                                                                                                                                                    0,
                                                                                                                                                                    0,
                                                                                                                                                                    0), textScale=0.05)
        newItem.setup()
        return newItem

    def _destroyIface(self):
        self.removeFrame()
        self.descText.destroy()
        del self.descText
        if self.optionUI:
            self.optionUI.destroy()
            del self.optionUI

    def _handleItemChange(self):
        self._destroyIface()
        self._createIface()

    def itemSelect(self, item):
        for currItem in self.optionItems.items:
            currItem.setSelected(False)

        item.setSelected(True)
        self.selectedItem = item

    def itemChecked(self, status):
        self.value = status

    def getOptionValuePair(self):
        option = self.item['Option']
        value = self.value
        if self.selectedItem:
            value = self.selectedItem.value
        return [str(option), str(value)]

    def createFrame(self):
        self.removeFrame()
        self.borderFrame = BorderFrame(parent=self, pos=(0.5, 0, 0.15), scale=(0.57,
                                                                               1,
                                                                               0.33))
        self.borderFrame.setBackgroundVisible(False)

    def removeFrame(self):
        if self.borderFrame:
            self.borderFrame.removeNode()
            self.borderFrame = None
        return