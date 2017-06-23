from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import Task
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.battle import WeaponGlobals
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.battle import CannonGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.uberdog import UberDogGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.reputation import ReputationGlobals
from pirates.piratesgui.StowawayListItem import StowawayListItem
from pirates.world.LocationConstants import LocationIds

class StowawayItemGui(StowawayListItem):
    width = PiratesGuiGlobals.InventoryItemGuiWidth
    height = PiratesGuiGlobals.InventoryItemGuiHeight
    available = True
    islandModelLookup = {LocationIds.PORT_ROYAL_ISLAND: 'models/islands/pir_m_are_isl_portRoyal_worldmap',LocationIds.TORTUGA_ISLAND: 'models/islands/pir_m_are_isl_tortuga_worldmap',LocationIds.CUBA_ISLAND: 'models/islands/pir_m_are_isl_cuba_worldmap',LocationIds.DEL_FUEGO_ISLAND: 'models/islands/pir_m_are_isl_delFuego_worldmap'}
    islandHprLookup = {LocationIds.PORT_ROYAL_ISLAND: (0, -90, 180),LocationIds.TORTUGA_ISLAND: (0, -90, 180),LocationIds.CUBA_ISLAND: (0, 90, 0),LocationIds.DEL_FUEGO_ISLAND: (0, 90, 0)}
    islandScaleLookup = {LocationIds.PORT_ROYAL_ISLAND: 0.15,LocationIds.TORTUGA_ISLAND: 0.18,LocationIds.CUBA_ISLAND: 0.4,LocationIds.DEL_FUEGO_ISLAND: 0.275}
    islandPosLookup = {LocationIds.PORT_ROYAL_ISLAND: (0.07, 0, 0.07),LocationIds.TORTUGA_ISLAND: (0.06, 0, 0.05),LocationIds.CUBA_ISLAND: (0.1, 0, 0.07),LocationIds.DEL_FUEGO_ISLAND: (0.07, 0, 0.07)}
    islandColorScaleLookup = {LocationIds.PORT_ROYAL_ISLAND: (1, 1, 1, 1),LocationIds.TORTUGA_ISLAND: (1, 1, 1, 1),LocationIds.CUBA_ISLAND: (0.6, 1.0, 0.9, 1),LocationIds.DEL_FUEGO_ISLAND: (1, 1, 1, 1)}

    def __init__(self, data, trade=0, buy=0, sell=0, use=0, weapon=0, isDisabled=0, **kw):
        if (trade or buy or sell or use or weapon) and not isDisabled:
            buttonRelief = DGG.RAISED
            buttonState = DGG.NORMAL
        else:
            buttonRelief = DGG.RIDGE
            buttonState = DGG.DISABLED
        self.loadGui()
        optiondefs = (
         ('relief', None, None), ('state', buttonState, None), ('frameSize', (0, self.width, 0, self.height), None), ('image', StowawayItemGui.genericButton, None), ('image_scale', (0.54, 1, 0.42), None), ('image_pos', (0.26, 0, 0.08), None), ('pressEffect', 0, None), ('command', self.sendEvents, None))
        self.defineoptions(kw, optiondefs)
        StowawayListItem.__init__(self, data, trade=trade, buy=buy, sell=sell, use=use, weapon=weapon, isDisabled=isDisabled, width=self.width, height=self.height)
        self.initialiseoptions(StowawayItemGui)
        self.createGui()
        self.helpBox = None
        return

    def loadGui(self):
        if StowawayItemGui.guiLoaded:
            return
        StowawayListItem.loadGui(self)
        StowawayItemGui.genericButton = (
         StowawayListItem.topGui.find('**/generic_button'), StowawayListItem.topGui.find('**/generic_button_down'), StowawayListItem.topGui.find('**/generic_button_over'), StowawayListItem.topGui.find('**/generic_button_disabled'))

    def createGui(self):
        itemId = self.data[0]
        self.picture = DirectFrame(parent=self, relief=None, state=DGG.DISABLED, pos=(0.01,
                                                                                      0,
                                                                                      0.01))
        self.nameTag = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=self.name, text_scale=PiratesGuiGlobals.TextScaleSmall * PLocalizer.getHeadingScale(2), text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.05,
                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                           0.09), text_font=PiratesGlobals.getInterfaceFont())
        itemTypeFormatted = ''
        self.itemTypeName = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=itemTypeFormatted, text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getInterfaceFont(), pos=(0.05,
                                                                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                                                                     0.065))
        self.miscText = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text='', text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.05,
                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                       0.025))
        self.costText = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, image=StowawayListItem.coinImage, image_scale=0.12, image_pos=Vec3(-0.01, 0, 0.01), text=str(self.price), text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ARight, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, text_pos=(-0.03, 0, 0), pos=(self.width - 0.035, 0, 0.09), text_font=PiratesGlobals.getInterfaceFont())
        self.picture['geom'] = loader.loadModel(StowawayItemGui.islandModelLookup[itemId])
        self.picture['geom_scale'] = StowawayItemGui.islandScaleLookup[itemId]
        self.picture['geom_pos'] = StowawayItemGui.islandPosLookup[itemId]
        self.picture['geom_hpr'] = StowawayItemGui.islandHprLookup[itemId]
        self.picture['geom_color'] = StowawayItemGui.islandColorScaleLookup[itemId]
        self.flattenStrong()
        return

    def highlightRed(self, text=''):
        self['state'] = DGG.DISABLED
        self['image_color'] = Vec4(0.55, 0.55, 0.5, 1)
        self.available = False
        self.highlightBox(text, Vec4(0.75, 0.5, 0.5, 1), PiratesGuiGlobals.TextFG6)

    def highlightGreen(self, text=''):
        self.highlightBox(text, Vec4(0.5, 0.75, 0.5, 1), PiratesGuiGlobals.TextFG4)

    def highlightBox(self, text, image_color, text_fg):
        self.miscText['text_fg'] = text_fg
        if text != '':
            self.miscText['text'] = text

    def enable(self):
        if self.available:
            self['state'] = DGG.NORMAL

    def disable(self):
        if self.available:
            self['state'] = DGG.DISABLED

    def destroy(self):
        taskMgr.remove('helpInfoTask')
        taskMgr.remove(self.taskName('dragTask'))
        if self.helpBox:
            self.helpBox.destroy()
            self.helpBox = None
        del self.picture
        if self.weapon:
            taskMgr.remove(DGG.B1PRESS)
            taskMgr.remove(DGG.B2PRESS)
            taskMgr.remove(DGG.B3PRESS)
        StowawayListItem.destroy(self)
        return

    def setDraggable(self, d):
        self.draggable = d

    def dragStart(self, event):
        self.origionalPos = self.getPos(render2d)
        self.origionalParent = self.getParent()
        self.bringToFront()
        self.setColorScale(1, 1, 1, 0.5)
        if self.draggable:
            self.wrtReparentTo(aspect2d)
            taskMgr.remove(self.taskName('dragTask'))
            vWidget2render2d = self.getPos(render2d)
            vMouse2render2d = Point3(event.getMouse()[0], 0, event.getMouse()[1])
            editVec = Vec3(vWidget2render2d - vMouse2render2d)
            task = taskMgr.add(self.dragTask, self.taskName('dragTask'))
            task.editVec = editVec

    def dragTask(self, task):
        if task.time < PiratesGuiGlobals.DragStartDelayTime:
            return Task.cont
        else:
            mwn = base.mouseWatcherNode
            if mwn.hasMouse():
                vMouse2render2d = Point3(mwn.getMouse()[0], 0, mwn.getMouse()[1])
                newPos = vMouse2render2d + task.editVec
                self.setPos(render2d, newPos)
                newPos = self.getPos(aspect2d)
                x = newPos[0]
                z = newPos[2]
                x = x - x % 0.05
                z = z - z % 0.05
                x = min(1.3 - self.width, max(-1.3, x))
                z = min(1 - self.height, max(-1, z))
                self.setPos(aspect2d, x, 0.0, z)
            return Task.cont

    def dragStop(self, event):
        self.clearColorScale()
        self.wrtReparentTo(self.origionalParent)
        self.setPos(render2d, self.origionalPos)
        if self.draggable:
            taskMgr.remove(self.taskName('dragTask'))

    def showDetails(self, event):
        taskMgr.doMethodLater(PiratesGuiGlobals.HelpPopupTime, self.createHelpbox, 'helpInfoTask')
        self.createHelpbox()

    def hideDetails(self, event):
        taskMgr.remove('helpInfoTask')
        if self.helpBox:
            self.helpBox.destroy()
            self.helpBox = None
        return