from direct.task import Task
from pirates.piratesgui.NewTutorialPanel import NewTutorialPanel
from pirates.interact import InteractiveBase
from DistributedShipCannon import DistributedShipCannon

class DistributedTutorialShipCannon(DistributedShipCannon):

    def __init__(self, cr):
        DistributedShipCannon.__init__(self, cr)
        self.tutorial = 1
        self.cannonMoved = 0
        self.cannonExitShown = 0
        self.moveCannonPanel = None
        self.fireCannonPanel = None
        self.exitCannonPanel = None
        self.setIgnoreProximity(True)
        return

    def disable(self):
        taskMgr.remove(self.uniqueName('moveCannonPanelPause'))
        taskMgr.remove(self.uniqueName('cannonMoveWatchTask'))
        DistributedShipCannon.disable(self)

    def startWeapon(self, av):
        DistributedShipCannon.startWeapon(self, av)
        if av == base.localAvatar:
            base.localAvatar.guiMgr.combatTray.hide()

    def selectAmmo(self, atype):
        pass

    def changeAmmo(self, amt=1):
        pass

    def enterFireCannon(self):
        DistributedShipCannon.enterFireCannon(self)
        self.power = 0.8
        messenger.send('usedCannon')
        base.localAvatar.guiMgr.setIgnoreEscapeHotKey(True)
        self.cgui.exitCannon.hide()
        self.ignore(InteractiveBase.END_INTERACT_EVENT)
        if self.cannonMoved == 0:
            self.moveCannonPanel = NewTutorialPanel(['moveCannon'])
            self.moveCannonPanel.hide()
            taskMgr.add(self.watchForCannonMovementTask, self.uniqueName('cannonMoveWatchTask'))
            taskMgr.doMethodLater(2.0, self.moveCannonPanel.activate, self.uniqueName('moveCannonPanelPause'), extraArgs=[])
        self.fireCannonPanel = NewTutorialPanel(['fireCannon', '\n', 'shipCombatInstruction', 1])
        self.fireCannonPanel.hide()

    def exitFireCannon(self):
        DistributedShipCannon.exitFireCannon(self)
        taskMgr.remove(self.uniqueName('moveCannonPanelPause'))
        taskMgr.remove(self.uniqueName('fireCannonPanelPause'))
        if self.moveCannonPanel:
            self.moveCannonPanel.hide()
            self.moveCannonPanel.destroy()
            self.moveCannonPanel = None
        if self.fireCannonPanel:
            self.fireCannonPanel.hide()
            self.fireCannonPanel.destroy()
            self.fireCannonPanel = None
        if self.exitCannonPanel:
            self.exitCannonPanel.hide()
            self.exitCannonPanel.destroy()
            self.exitCannonPanel = None
        messenger.send('exitedCannon')
        return

    def fireCannon(self):
        DistributedShipCannon.fireCannon(self)
        messenger.send('firedCannon')

    def playerMovedCannonFirstTime(self):
        self.cannonMoved = 1
        if self.moveCannonPanel:
            self.moveCannonPanel.hide()
        taskMgr.remove(self.uniqueName('moveCannonPanelPause'))
        taskMgr.remove(self.uniqueName('cannonMoveWatchTask'))
        taskMgr.doMethodLater(2.0, self.fireCannonPanel.activate, self.uniqueName('fireCannonPanelPause'), extraArgs=[])

    def watchForCannonMovementTask(self, task):
        dx, dy = localAvatar.cameraFSM.cannonCamera.mouseDelta
        kdx, kdy = localAvatar.cameraFSM.cannonCamera.keyboardDelta
        if dx or dy or kdx or kdy:
            self.playerMovedCannonFirstTime()
        return Task.cont

    def showExitCannonPanel(self):
        if self.cannonExitShown == 0:
            if self.fireCannonPanel and not self.fireCannonPanel.isEmpty():
                self.fireCannonPanel.hide()
            self.cannonExitShown = 1
            self.exitCannonPanel = NewTutorialPanel(['exitCannon'], False)
            self.exitCannonPanel.activate()
            base.localAvatar.guiMgr.setIgnoreEscapeHotKey(False)
            self.cgui.exitCannon.show()
            self.accept(InteractiveBase.END_INTERACT_EVENT, self.handleEndInteractKey)