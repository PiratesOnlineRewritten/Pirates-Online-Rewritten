from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesgui import PiratesGuiGlobals
from direct.showbase.DirectObject import DirectObject
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import Freebooter

class ListFrame(DirectFrame, DirectObject):
    revealSpeed = PiratesGuiGlobals.ItemRevealTime
    pageFinishWait = PiratesGuiGlobals.PageFinishWaitTime
    maxTotalWait = PiratesGuiGlobals.MaxTotalRevealTime

    def __init__(self, w, h, title, holder=None, hideAll=True, delayedReveal=None, frameColor=PiratesGuiGlobals.FrameColor, **kw):
        self.adjustHeight = False
        if h == None:
            h = 1
            self.adjustHeight = True
        DirectFrame.__init__(self, relief=None, state=DGG.NORMAL, frameColor=frameColor, borderWidth=PiratesGuiGlobals.BorderWidth, frameSize=(0.0, w, 0.0, h), pos=(PiratesGuiGlobals.BorderWidth[0], 0, PiratesGuiGlobals.BorderWidth[0]), **kw)
        self.initialiseoptions(ListFrame)
        self.delayedReveal = delayedReveal
        self.items = []
        self.hideAll = hideAll
        if holder is None:
            holder = localAvatar
        self.holder = holder
        self.accept(self.getItemChangeMessage(), self._handleItemChange)
        self.myHeight = h
        self.resizeItemHeights = False
        self.pendingObjRequests = []
        self.itemBuffer = 0
        self.topBuffer = 0.015
        gui = loader.loadModel('models/gui/toplevel_gui')
        self.lockArt = gui.find('**/pir_t_gui_gen_key_subscriber')
        return

    def setup(self):
        self._createIface()

    def getItemChangeMessage(self):
        if self.holder:
            return self.holder.getItemChangeMsg()
        else:
            return ''

    def getShowNextItemMessage(self):
        return 'showNext'

    def getListFinishedMessage(self):
        return 'listFinished'

    def getItemList(self):
        return self.holder.getItemList()

    def createNewItem(self, item, itemType=None, columnWidths=[], color=None):
        return self.holder.createNewItem(item, self, itemType, columnWidths, color)

    def setResizeItemHeights(self, resize):
        self.resizeItemHeights = resize

    def destroy(self):
        self.ignoreAll()
        for entry in self.items:
            entry.destroy()

        self.items = []
        self._destroyIface()
        DirectFrame.destroy(self)
        for request in self.pendingObjRequests:
            base.cr.relatedObjectMgr.abortRequest(request)

        self.pendingObjRequests = []
        self.holder = None
        return

    def getItemHeight(self):
        if self.resizeItemHeights:
            numItems = len(self.items)
            return (self.myHeight - 0.02) / numItems
        else:
            return -1

    def createListItem(self, currItem, revealTime=0, itemType=None, columnWidths=[], color=None):
        newItem = self.createNewItem(currItem, itemType, columnWidths, color)
        self.items.insert(0, newItem)
        itemHeight = self.getItemHeight()
        totalY = 0
        if self.adjustHeight:
            y = 0
        else:
            y = 0
        for gui in self.items:
            if self.hideAll == False:
                gui.descText.wrtReparentTo(gui)
            gui.setZ(y)
            if itemHeight == -1:
                currHeight = gui.getHeight()
            else:
                gui['frameSize'] = (
                 0, gui.getWidth(), 0, itemHeight)
                currHeight = itemHeight
            currHeight += self.itemBuffer
            y += currHeight
            totalY += currHeight
            if self.hideAll == False:
                gui.descText.wrtReparentTo(self.getParent().getParent())

        if self.adjustHeight:
            newSize = self['frameSize']
            self['frameSize'] = (
             newSize[0], newSize[1], newSize[2], totalY + self.topBuffer)
        if hasattr(currItem, 'getChangeEvent'):
            self.accept(currItem.getChangeEvent(), self._handleItemChange)
        if revealTime:
            unwrapMode = currItem.get('UnwrapMode', 0)
            newItem.setRevealTimer(revealTime, unwrapMode)
        return newItem

    def _createIface(self):
        itemList = self.getItemList()
        revealTime = self.revealSpeed
        if base.config.GetBool('fast-gui', 0) is 1:
            self.revealSpeed = 0
        numItems = len(itemList)
        if numItems > 0:
            min(self.revealSpeed, self.maxTotalWait / numItems)
        revealTime = 0
        for currItem in itemList:
            if currItem is not None:
                if isinstance(currItem, tuple) or isinstance(currItem, list):
                    self.createListItem(currItem, revealTime)
                else:
                    itemType = currItem.get('Type')
                    if itemType == 'ObjectId':
                        objId = currItem.get('Value')
                        request = base.cr.relatedObjectMgr.requestObjects([objId], eachCallback=lambda param1=None, param2=revealTime: self.createListItem(param1, param2))
                        self.pendingObjRequests.append(request)
                    else:
                        itmPtr = self.createListItem(currItem, revealTime)
                        itemText = currItem.get('Text')
                        if itemText:
                            if itemText[0] == PLocalizer.TBTGame or itemText[0] == PLocalizer.CTLGame or itemText[0] == PLocalizer.SBTGame or itemText[0] == PLocalizer.PokerGame:
                                if 0:
                                    itmPtr.setColorScale(0.3, 0.3, 0.3, 1)
                                    lock = DirectFrame(parent=itmPtr, relief=None, image=self.lockArt, image_scale=0.2, image_pos=(0.55,
                                                                                                                                   0,
                                                                                                                                   0.09))
                                    itmPtr.locked = True
                                    itmPtr['command'] = base.localAvatar.guiMgr.showNonPayer
                                    itmPtr['extraArgs'] = ['Restricted_ListFrame', 4]
                    if (itemType == None or itemType != 'Space') and self.delayedReveal:
                        revealTime += self.revealSpeed

        return

    def sendFinished(args=None):
        messenger.send(self.getListFinishedMessage())
        taskMgr.doMethodLater(self.pageFinishWait + revealTime, sendFinished, 'scoreboardWait')

    def _destroyIface(self):
        for gui in self.items:
            gui.destroy()

        self.items = []

    def removeItem(self, item):
        item.detachNode()
        self.items.remove(item)

    def redraw(self):
        self._destroyIface()
        self.items = []
        self._createIface()

    def _handleItemChange(self):
        self.redraw()
        if self.holder and hasattr(self.holder, 'handleChildChange'):
            self.holder.handleChildChange()

    def cleanup(self):
        for currItem in self.items:
            currItem.descText.wrtReparentTo(currItem)