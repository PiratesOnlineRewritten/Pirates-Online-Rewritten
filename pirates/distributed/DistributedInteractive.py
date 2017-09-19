from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedNode import DistributedNode
from direct.distributed.GridChild import GridChild
from pirates.piratesgui import InteractGUI
from pirates.interact.InteractiveBase import InteractiveBase
from pirates.world.DistributedLocatableObject import DistributedLocatableObject
from direct.showbase.PythonUtil import report

class DistributedInteractive(DistributedNode, InteractiveBase, DistributedLocatableObject, GridChild):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteractive')

    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        InteractiveBase.__init__(self)
        DistributedLocatableObject.__init__(self, cr)
        GridChild.__init__(self)
        self.interactGUI = None
        self.hideHpMeterFlag = 0
        self.userId = 0
        self.uniqueId = None
        return

    def delete(self):
        DistributedNode.delete(self)
        InteractiveBase.delete(self)
        DistributedLocatableObject.delete(self)
        GridChild.delete(self)

    def generate(self):
        DistributedNode.generate(self)
        InteractiveBase.generate(self)
        DistributedLocatableObject.generate(self)

    def disable(self):
        DistributedNode.disable(self)
        InteractiveBase.disable(self)
        DistributedLocatableObject.disable(self)

    def announceGenerate(self):
        DistributedNode.announceGenerate(self)
        DistributedLocatableObject.announceGenerate(self)

    def isBattleable(self):
        return 0

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='shipboard')
    def requestInteraction(self, avId, interactType=0, instant=0):
        if self.cr:
            self.sendUpdate('requestInteraction', [base.localAvatar.doId, interactType, instant])
            self.cr.interactionMgr.stop()
            self.request('Waiting')

    def setLocation(self, parentId, zoneId):
        DistributedNode.setLocation(self, parentId, zoneId)
        self.reparentTo(self.getParentObj())

    def requestExit(self):
        self.sendUpdate('requestExit')
        self.refreshState()

    def demandExit(self):
        self.sendUpdate('demandExit')
        self.refreshState()

    def refreshState(self):
        if self.hasProximityCollision and self.allowInteract and not self.ignoreProximity and not self.proximityCollisionNodePath.isEmpty():
            distance = self.proximityCollisionNodePath.getDistance(localAvatar)
            proxSphereRadius = self.proximityCollisionNodePath.getScale()[0]
            avRadius = 1.4
            if distance <= proxSphereRadius + avRadius:
                self.request('Proximity')
            else:
                self.request('Idle')
        else:
            self.request('Idle')

    def acceptInteraction(self):
        self.request('Use')

    def rejectInteraction(self):
        self.cr.interactionMgr.start()
        self.refreshState()

    def rejectExit(self):
        pass

    def offerOptions(self, optionIds, statusCodes):
        if self.interactGUI:
            self.notify.warning('offerOptions: old interact GUI still around')
            self.interactGUI.destroy()
            self.interactGUI = None
        self.interactGUI = InteractGUI.InteractGUI()
        title = self.getMenuTitle()
        self.interactGUI.setOptions(title, optionIds, statusCodes, self.b_selectOption)
        return

    def b_selectOption(self, optionId):
        self.d_selectOption(optionId)
        self.selectOption(optionId)

    def d_selectOption(self, optionId):
        self.sendUpdate('selectOption', [optionId])

    def selectOption(self, optionId):
        if self.interactGUI:
            self.interactGUI.destroy()
            self.interactGUI = None
        return

    def getMenuTitle(self):
        return ''

    def setUserId(self, avId):
        self.userId = avId

    def getUserId(self):
        return self.userId

    def setUniqueId(self, uid):
        if self.uniqueId != '' and uid != self.uniqueId:
            base.cr.uidMgr.removeUid(self.uniqueId)
        self.uniqueId = uid
        base.cr.uidMgr.addUid(self.uniqueId, self.getDoId())

    def getUniqueId(self):
        return self.uniqueId

    def getWorld(self):
        return base.cr.activeWorld

    def isInvisibleGhost(self):
        return 0
