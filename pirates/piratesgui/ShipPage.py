from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.InventoryPage import InventoryPage
from pirates.piratesgui.ShipPanel import ShipPanel
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryCategory, InventoryType
from pirates.uberdog import UberDogGlobals

class ShipPage(InventoryPage):
    BottleFrame = None

    def __init__(self):
        if not ShipPage.BottleFrame:
            gui = loader.loadModel('models/gui/gui_ship_window')
            ShipPage.BottleFrame = gui.find('**/ship_bottle').copyTo(NodePath(''))
            ShipPage.BottleFrame.flattenStrong()
        InventoryPage.__init__(self)
        self.initialiseoptions(ShipPage)
        self.panels = {}
        self.pendingRequestInventory = None
        self.currentPanel = 0
        self.tabBar = None
        self.accept('DistributedShipOV-announceGenerate', self.shipOVArrived)
        self.accept('DistributedShipOV-delete', self.shipOVRemoved)
        return

    def destroy(self):
        self.ignoreAll()
        taskMgr.remove('ShipPage-refresh')
        if self.tabBar:
            self.tabBar.destroy()
            self.tabBar = None
        for panel in self.panels.itervalues():
            panel.destroy()

        self.panels = None
        if self.pendingRequestInventory:
            base.cr.relatedObjectMgr.abortRequest(self.pendingRequestInventory)
            self.pendingRequestInventory = None
        DirectFrame.destroy(self)
        return

    def show(self):
        InventoryPage.show(self)
        if not self.tabBar:
            self.clearTabs()
            for id in range(3):
                self.addPanel(id)

        self.refreshList()
        self.tabBar.unstash()
        activeShipId = localAvatar.getActiveShipId()
        if activeShipId:
            self.tabBar.selectTab(activeShipId)
            self.showPanel(activeShipId)

    def hide(self):
        InventoryPage.hide(self)
        if self.tabBar:
            self.tabBar.stash()

    def addPanel(self, shipId):
        self.removePanel(shipId)
        panel = ShipPanel(self, shipId, parent=NodePath(), state=DGG.DISABLED)
        panel.hide()
        panel.reparentTo(self)
        self.panels[shipId] = panel

    def removePanel(self, shipId):
        panel = self.panels.pop(shipId, None)
        if panel:
            panel.destroy()
        return

    def shipOVArrived(self, shipId):
        self.addPanel(shipId)
        self.refreshList()
        taskMgr.remove('ShipPage-refresh')
        taskMgr.doMethodLater(5, self.refreshList, 'ShipPage-refresh', extraArgs=[])

    def shipOVRemoved(self, shipId):
        self.removePanel(shipId)
        self.refreshList()

    def clearBlankPanels(self):
        for id in self.panels.keys():
            if id <= 2:
                self.removePanel(id)

    def clearTabs(self):
        if self.tabBar:
            self.tabBar.destroy()
        self.tabBar = localAvatar.guiMgr.chestPanel.makeTabBar()

    def makeTab(self, shipId):
        tab = self.tabBar.addTab(shipId, frameSize=(-0.125, 0.125, -0.125, 0.125), unfocusSize=(-0.125, 0.125, -0.125, 0.125), focusSize=(-0.125, 0.125, -0.135, 0.135), command=self.showPanel, extraArgs=[shipId])
        tab.shipModel = tab.attachNewNode('modelInstance')
        if shipId > 2:
            self.panels[shipId].bottleFrame.shipMeter.modelRoot.instanceTo(tab.shipModel)
            tab.shipModel.setHpr(-70, 12, 15)
            tab.shipModel.setDepthTest(1, 100)
            tab.shipModel.setDepthWrite(1, 100)

            def mouseOver(tab=tab):
                tab.shipModel.setPos(0.01, 0, -0.05)
                tab.shipModel.setScale(0.3)
                tab.shipModel.setColorScale(1, 1, 1, 1)

            def mouseOff(tab=tab):
                if not tab['selected']:
                    tab.shipModel.setPos(0.01, 0, -0.035)
                    tab.shipModel.setScale(0.25)
                    tab.shipModel.setColorScale(0.8, 0.8, 0.8, 1.0)
                else:
                    mouseOver(tab)

        else:
            self.BottleFrame.instanceTo(tab.shipModel)

            def mouseOver(tab=tab):
                tab.shipModel.setPos(0.01, 0, -0.055)
                tab.shipModel.setScale(0.06, 0.071, 0.071)
                tab.shipModel.setColorScale(1, 1, 1, 1)

            def mouseOff(tab=tab):
                if not tab['selected']:
                    tab.shipModel.setPos(0.01, 0, -0.05)
                    tab.shipModel.setScale(0.055, 0.065, 0.065)
                    tab.shipModel.setColorScale(0.9, 0.9, 0.9, 1.0)
                else:
                    mouseOver(tab)

        tab['mouseEntered'] = mouseOver
        tab['mouseLeft'] = mouseOff
        mouseOff(tab)

    def needRefresh(self):
        if not self.tabBar:
            return True
        if set(self.tabBar.getOrder()) == set(self.panels):
            return False
        return True

    def refreshList(self):
        if not self.needRefresh():
            return

        def doRefresh(inventory):
            shipIds = localAvatar.getInventory().getShipDoIdList()
            self.clearBlankPanels()
            self.clearTabs()
            for id in range(len(shipIds), 3):
                self.addPanel(id)

            validShips = [ shipId for shipId in shipIds if shipId in self.panels ]
            for shipId in validShips:
                self.makeTab(shipId)

            for x in range(len(validShips), 3):
                self.makeTab(x)

            activeShipId = localAvatar.getActiveShipId()
            if activeShipId:
                self.tabBar.selectTab(activeShipId)
                self.showPanel(activeShipId)
            else:
                self.tabBar.selectTab(self.getCurrentPanel())
                self.showPanel(self.getCurrentPanel())
            if self.isHidden():
                self.tabBar.stash()

        def doReadyCheck(inventory):
            if inventory.isReady():
                doRefresh(inventory)
            else:
                self.acceptOnce('inventoryReady-%s' % inventory.getDoId(), doRefresh)

        if self.pendingRequestInventory:
            base.cr.relatedObjectMgr.abortRequest(self.pendingRequestInventory)
            self.pendingRequestInventory = None
        self.pendingRequestInventory = base.cr.relatedObjectMgr.requestObjects([localAvatar.getInventoryId()], eachCallback=doReadyCheck)
        return

    def showPanel(self, shipId):
        for panel in self.panels.itervalues():
            panel.hide()

        if shipId in self.panels:
            self.currentPanel = shipId
            self.panels[self.currentPanel].show()

    def getCurrentPanel(self):
        shipIds = localAvatar.getInventory().getShipDoIdList()
        if shipIds:
            if self.currentPanel not in self.panels:
                if self.panels:
                    self.currentPanel = shipIds[0]
                else:
                    self.currentPanel = 0
        else:
            self.currentPanel = 0
        return self.currentPanel

    def slideOpenPrecall(self):
        self.show()