from pirates.piratesgui import ListFrame
from pirates.piratesgui import PiratesGuiGlobals

class SheetFrame(ListFrame.ListFrame):

    def __init__(self, w, h, title, holder=None, hideAll=True, delayedReveal=None, **kw):
        ListFrame.ListFrame.__init__(self, w, h, title, holder, hideAll, delayedReveal, frameColor=(1,
                                                                                                    1,
                                                                                                    1,
                                                                                                    0.5), **kw)
        self.initialiseoptions(SheetFrame)
        self.rowColors = {}

    def createListItem(self, currItem, revealTime=0, itemType=None, columnWidths=[], color=None):
        newItem = self.createNewItem(currItem, itemType, columnWidths, color)
        self.items.insert(0, newItem)
        itemHeight = self.getItemHeight()
        y = self.getHeight() - 0.01
        for guiitem in self.items:
            y -= guiitem.getHeight()

        print 'y = %s' % y
        for gui in self.items:
            if self.hideAll == False:
                gui.descText.wrtReparentTo(gui)
            gui.setZ(y)
            gui.setX(0.01)
            y += gui.getHeight()
            if self.hideAll == False:
                gui.descText.wrtReparentTo(self.getParent().getParent())

        if hasattr(currItem, 'getChangeEvent'):
            self.accept(currItem.getChangeEvent(), self._handleItemChange)
        return newItem

    def _createIface(self):
        itemList = self.getItemList()
        numRows = len(itemList)
        if numRows > 0:
            numColumns = len(itemList[0])
            column1Width = 0.55
            columnWidth = (self.getWidth() - column1Width) / (numColumns - 1)
            revealTime = 0
            self.createListItem(itemList[0], itemType=PiratesGuiGlobals.UIListItemType_ColumHeadings, columnWidths=[column1Width, columnWidth])
            for currItemIdx in range(1, numRows):
                currItem = itemList[currItemIdx]
                if currItem is not None and len(currItem) > 0:
                    if currItem[-1][0] == 'color':
                        customColor = currItem[-1][1]
                    else:
                        customColor = None
                    self.createListItem(currItem, revealTime, columnWidths=[column1Width, columnWidth], color=customColor)

        return

    def _destroyIface(self):
        for gui in self.items:
            gui.destroy()

        self.items = []

    def getItemHeight(self):
        return -1