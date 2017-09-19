from pandac.PandaModules import *
from direct.gui.DirectOptionMenu import *
from direct.gui.DirectFrame import *
from direct.gui.DirectButton import *
from direct.gui import DirectGuiGlobals as DGG

class OptionMenu(DirectOptionMenu):
    normal_fg_color = (0.2, 0.8, 0.6, 1.0)
    disabled_fg_color = (0.2, 0.2, 0.2, 1.0)

    def __init__(self, parent=None, **kw):
        gui_main = loader.loadModel('models/gui/gui_main')
        titleImage = gui_main.find('**/game_options_panel/top/titlebox')
        gui_main.removeNode()
        char_gui = loader.loadModel('models/gui/char_gui')
        popupMarkerImage = char_gui.find('**/chargui_forward')
        popupMarkerImageOver = char_gui.find('**/chargui_forward_over')
        char_gui.removeNode()
        optiondefs = (('image', titleImage, None), ('image_pos', (0, 0, -6), None), ('image_scale', (6, 3, 3), None), ('popupMarkerImage', (popupMarkerImage, popupMarkerImage, popupMarkerImageOver, popupMarkerImage), None), ('popupMarkerImageScale', 5, None), ('popupMarkerHpr', (0, 0, 90), None), ('text_fg', self.normal_fg_color, None), ('text_align', TextNode.ACenter, None), ('popupBgColor', (0.0745, 0.0627, 0.0501, 1.0), None), ('popupTextColor', (0.831, 0.745, 0.58, 1.0), None), ('popupHalfWidth', 3.8, None), ('highlightColor', (0.212, 0.192, 0.169, 1), None), ('frameSize', (0, 3.4, 0, 0.6), None), ('relief', None, None))
        self.defineoptions(kw, optiondefs)
        DirectOptionMenu.__init__(self, parent)
        self.popupMarker.removeNode()
        self.popupMarker = self.createcomponent('popupMarker', (), None, DirectButton, (self,), image=self['popupMarkerImage'], image_scale=self['popupMarkerImageScale'], hpr=self['popupMarkerHpr'], relief=None, frameSize=(-0.5, 0.5, -0.2, 0.2))
        self.popupMarker.bind(DGG.B1PRESS, self.showPopupMenu)
        self.popupMarker.bind(DGG.B1RELEASE, self.selectHighlightedIndex)
        self.popupMarker.guiItem.setSound(DGG.B1PRESS + self.popupMarker.guiId, self['clickSound'])
        self.initialiseoptions(OptionMenu)
        return None

    def setItems(self):
        if self.popupMenu != None:
            self.destroycomponent('popupMenu')
        self.popupMenu = self.createcomponent('popupMenu', (), None, DirectFrame, (
         self,), relief=None)
        self.popupMenu.setBin('gui-popup', 0)
        if not self['items']:
            return
        itemIndex = 0
        self.minX = self.maxX = self.minZ = self.maxZ = None
        self.maxX = self['popupHalfWidth']
        self.minX = -1 * self.maxX
        for item in self['items']:
            c = self.createcomponent('item%d' % itemIndex, (), 'item', DirectButton, (self.popupMenu,), text=item, text_align=TextNode.ACenter, frameColor=self['popupBgColor'], text_fg=self['popupTextColor'], command=lambda i=itemIndex: self.set(i))
            bounds = c.getBounds()
            if self.minX == None:
                self.minX = bounds[0]
            elif bounds[0] < self.minX:
                self.minX = bounds[0]
            if self.maxX == None:
                self.maxX = bounds[1]
            elif bounds[1] > self.maxX:
                self.maxX = bounds[1]
            if self.minZ == None:
                self.minZ = bounds[2]
            elif bounds[2] < self.minZ:
                self.minZ = bounds[2]
            if self.maxZ == None:
                self.maxZ = bounds[3]
            elif bounds[3] > self.maxZ:
                self.maxZ = bounds[3]
            itemIndex += 1

        self.maxWidth = self.maxX - self.minX
        self.maxHeight = self.maxZ - self.minZ
        for i in range(itemIndex):
            item = self.component('item%d' % i)
            item['frameSize'] = (
             self.minX, self.maxX, self.minZ, self.maxZ)
            item.setPos(0, 0, -self.maxZ - i * self.maxHeight)
            item.bind(DGG.B1RELEASE, self.hidePopupMenu)
            item.bind(DGG.WITHIN, lambda x, i=i, item=item: self._highlightItem(item, i))
            fc = item['frameColor']
            item.bind(DGG.WITHOUT, lambda x, item=item, fc=fc: self._unhighlightItem(item, fc))

        f = self.component('popupMenu')
        f['frameSize'] = (0, self.maxWidth, -self.maxHeight * itemIndex, 0)
        if self['initialitem']:
            self.set(self['initialitem'], fCommand=0)
        else:
            self.set(0, fCommand=0)
        pm = self.popupMarker
        pmw = pm.getWidth() * pm.getScale()[0] + 2 * self['popupMarkerBorder'][0]
        if self.initFrameSize:
            bounds = list(self.initFrameSize)
        else:
            bounds = [
             self.minX, self.maxX, self.minZ, self.maxZ]
        pm.setPos(bounds[1] + pmw / 2.0, 0, bounds[2] + (bounds[3] - bounds[2]) / 2.0)
        bounds[1] += pmw
        self['frameSize'] = (bounds[0], bounds[1], bounds[2], bounds[3])
        self.hidePopupMenu()
        return

    def showPopupMenu(self, event=None):
        self.popupMenu.show()
        self.popupMenu.setScale(self, VBase3(1))
        b = self.getBounds()
        fb = self.popupMenu.getBounds()
        xPos = (b[1] - b[0]) / 2.0 - fb[0]
        self.popupMenu.setZ(self, -0.2)
        pos = self.popupMenu.getPos(render2d)
        scale = self.popupMenu.getScale(render2d)
        maxX = pos[0] + fb[1] * scale[0]
        if maxX > 1.0:
            self.popupMenu.setX(render2d, pos[0] + (1.0 - maxX))
        minZ = pos[2] + fb[2] * scale[2]
        maxZ = pos[2] + fb[3] * scale[2]
        if minZ < -1.0:
            self.popupMenu.setZ(render2d, pos[2] + (-1.0 - minZ))
        elif maxZ > 1.0:
            self.popupMenu.setZ(render2d, pos[2] + (1.0 - maxZ))
        self.cancelFrame.show()
        self.cancelFrame.setPos(render2d, 0, 0, 0)
        self.cancelFrame.setScale(render2d, 1, 1, 1)

    def updateState(self, state):
        self['state'] = state
        self.setState()
        if state == DGG.DISABLED:
            self['text_fg'] = self.disabled_fg_color
        else:
            self['text_fg'] = self.normal_fg_color
        self.popupMarker['state'] = state
        self.popupMarker.setState()

    def set(self, index, fCommand=1):
        newIndex = self.index(index)
        if newIndex is not None:
            self.selectedIndex = newIndex
            item = self['items'][self.selectedIndex]
            self['text'] = item
            if fCommand and self['command']:
                apply(self['command'], [item, index] + self['extraArgs'])
        return

    def setByValue(self, val, fCommand=True):
        i = 0
        for item in self['items']:
            if item == val:
                break
            i += 1

        if i < len(self['items']):
            self.set(i, fCommand=fCommand)