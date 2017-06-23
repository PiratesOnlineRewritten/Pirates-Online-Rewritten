from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals

class StatRowGui(DirectFrame):
    Width = PiratesGuiGlobals.TMCompletePanelWidth - PiratesGuiGlobals.GridSize
    Height = PiratesGuiGlobals.TMCompletePageHeight / 7

    def __init__(self, item, columnHeadings, parent=None, textScale=None, itemHeight=None, itemWidth=None, itemWidths=[], txtColor=None, frameColor=(1, 1, 1, 0.05), **kw):
        if itemHeight == None:
            itemHeight = self.Height
        if itemWidth == None:
            itemWidth = self.Width
        self.columnHeadings = columnHeadings
        self.columnWidths = itemWidths
        optiondefs = (('state', DGG.NORMAL, None), ('frameColor', frameColor, None), ('borderWidth', PiratesGuiGlobals.BorderWidth, None), ('frameSize', (0.0, itemWidth, 0.0, itemHeight), None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.initialiseoptions(StatRowGui)
        self.textScale = 0.045
        if textScale:
            self.textScale = textScale
        self.item = item
        self.descText = None
        self.valueTexts = []
        self.textColor = txtColor
        return

    def setup(self):
        self._createIface()

    def destroy(self):
        self._destroyIface()
        DirectFrame.destroy(self)
        self.ignoreAll()

    def _createIface(self):
        textFg = PiratesGuiGlobals.TextFG1
        self.valueTexts = []
        currColWidth = 0.5
        if len(self.columnWidths) > 0:
            currColWidth = self.columnWidths.pop(0)
        currValueX = currColWidth / 2.0
        rowHeading = str(self.item[0])
        if self.textColor:
            textFg = self.textColor
        self.descText = DirectLabel(parent=self, relief=None, text=rowHeading, text_align=TextNode.ACenter, text_scale=self.textScale, text_fg=textFg, text_wordwrap=14, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(currValueX, 0, self.getHeight() / 2))
        for currValueItem in self.item[1]:
            if currValueItem[0] in self.columnHeadings:
                currValueX += currColWidth / 2.0
                if len(self.columnWidths) > 0:
                    currColWidth = self.columnWidths.pop(0)
                currValueX += currColWidth / 2.0
                self.valueTexts.append(DirectLabel(parent=self, relief=None, text=str(currValueItem[1]), text_align=TextNode.ACenter, text_scale=self.textScale, text_fg=textFg, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(currValueX, 0, self.getHeight() / 2)))

        return

    def _destroyIface(self):
        if self.descText:
            self.descText.destroy()
            self.descText = None
        for currValueText in self.valueTexts:
            currValueText.destroy()

        self.valueTexts = []
        return

    def _handleItemChange(self):
        self._destroyIface()
        self._createIface()