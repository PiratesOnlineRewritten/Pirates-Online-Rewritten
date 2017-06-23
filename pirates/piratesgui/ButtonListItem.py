from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
import types

class ButtonListItem(DirectButton):

    def __init__(self, item, itemHeight, itemWidth, parent=None, parentList=None, textScale=None, txtColor=None, **kw):
        optiondefs = (
         (
          'state', DGG.NORMAL, None), ('image', None, None), ('image_scale', (0.24, 0.22, 0.22), None), ('image_pos', (0.185, 0, 0.043), None), ('frameColor', (0.1, 0.1, 1, 0.08), None), ('borderWidth', PiratesGuiGlobals.BorderWidth, None), ('frameSize', (0.0, itemWidth, 0.0, itemHeight), None))
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent)
        self.initialiseoptions(ButtonListItem)
        self.textScale = textScale
        if not self.textScale:
            self.textScale = PiratesGuiGlobals.TextScaleLarge
        self.item = item.get('Text')
        self.descText = None
        self.valueTexts = []
        self.textColor = txtColor
        if not self.textColor:
            self.textColor = PiratesGuiGlobals.TextFG1
        self.parentList = parentList
        self.value = item.get('Value')
        self.defaultColorScale = (0.75, 0.75, 0.75, 1)
        self.setColorScale(*self.defaultColorScale)
        self.prevImageScale = None
        self.locked = False
        return

    def setup(self):
        self._createIface()

    def destroy(self):
        self._destroyIface()
        self.parentList = None
        DirectButton.destroy(self)
        self.ignoreAll()
        return

    def _createIface(self):
        if type(self.item) is types.ListType:
            itemText = self.item[0]
        else:
            itemText = self.item
        self['text'] = itemText
        self['text_scale'] = self.textScale
        self['text_fg'] = self.textColor
        self['text_pos'] = (self.getWidth() / 2, 0.025)
        self.prevImageScale = self['image_scale']

    def _destroyIface(self):
        pass

    def _handleItemChange(self):
        self._destroyIface()
        self._createIface()

    def commandFunc(self, event):
        DirectButton.commandFunc(self, event)
        if not self.locked:
            self.parentList.itemSelect(self)

    def setSelected(self, selected):
        self.selected = selected
        if selected:
            self.setColorScale(1, 1, 1, 1)
            self.prevImageScale = self['image_scale']
            self['image_scale'] = (0.25, 0.23, 0.23)
        else:
            self.setColorScale(*self.defaultColorScale)
            self['image_scale'] = self.prevImageScale