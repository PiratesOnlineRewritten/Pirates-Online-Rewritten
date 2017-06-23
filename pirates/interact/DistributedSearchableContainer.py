import math
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.showbase.PythonUtil import quickProfile
from pirates.distributed.DistributedInteractive import DistributedInteractive
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
containerCache = {}

class DistributedSearchableContainer(DistributedInteractive):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSearchableContainer')
    deferrable = True

    def __init__(self, cr):
        NodePath.__init__(self, 'DistributedSearchableContainer')
        DistributedInteractive.__init__(self, cr)
        self.searchTime = None
        self.type = None
        self.containerColorR = 1.0
        self.containerColorG = 1.0
        self.containerColorB = 1.0
        self.containerColorA = 1.0
        self.sphereScale = 10
        self.container = None
        self.startSearchTime = 0.0
        return

    def setSearchTime(self, t):
        self.searchTime = t

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def setSphereScale(self, sphereScale):
        self.sphereScale = sphereScale

    def getSphereScale(self):
        return self.sphereScale

    def setVisZone(self, zone):
        self.visZone = zone

    def getVisZone(self):
        return self.visZone

    def announceGenerate(self):
        self.setInteractOptions(proximityText=PLocalizer.InteractSearchableContainer, sphereScale=self.getSphereScale(), diskRadius=10, exclusive=0)
        DistributedInteractive.announceGenerate(self)
        self.loadContainer()
        self.getParentObj().builder.addSectionObj(self.container, self.visZone)

    def disable(self):
        DistributedInteractive.disable(self)
        self.getParentObj().builder.removeSectionObj(self.container, self.visZone)
        if self.container:
            self.container.removeNode()
            self.container = None
        return

    def loadContainer(self):
        if self.container:
            return
        modelPath = PiratesGlobals.SearchableModels.get(self.type, 'models/props/crate_04')
        container = self.getContainerModel(modelPath)
        containerColor = self.getContainerColor()
        container.setColorScale(containerColor[0], containerColor[1], containerColor[2], containerColor[3])
        container.reparentTo(self)
        self.container = container

    def getContainerModel(self, name):
        model = containerCache.get(name)
        if model:
            return model.copyTo(NodePath())
        else:
            model = loader.loadModel(name)
            model.flattenStrong()
            containerCache[name] = model
            return model.copyTo(NodePath())

    def requestInteraction(self, avId, interactType=0):
        localAvatar.motionFSM.off()
        DistributedInteractive.requestInteraction(self, avId, interactType)

    def rejectInteraction(self):
        localAvatar.guiMgr.createWarning(PLocalizer.AlreadySearched)
        localAvatar.motionFSM.on()
        DistributedInteractive.rejectInteraction(self)

    def startSearching(self):
        self.acceptInteraction()
        localAvatar.guiMgr.workMeter.updateText(PLocalizer.InteractSearching)
        localAvatar.guiMgr.workMeter.startTimer(self.searchTime)
        localAvatar.b_setGameState('Searching')
        pos = localAvatar.getPos(self)
        angle = math.atan2(pos[0], pos[1])
        radius = 4
        localAvatar.setPos(self, math.sin(angle) * radius, math.cos(angle) * radius, 0)
        localAvatar.headsUp(self)
        localAvatar.setH(localAvatar, 0)

    def stopSearching(self, questProgress):
        localAvatar.guiMgr.workMeter.stopTimer()
        localAvatar.guiMgr.showQuestProgress(questProgress)
        if localAvatar.getGameState() == 'Searching':
            localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
        self.refreshState()

    def requestExit(self):
        DistributedInteractive.requestExit(self)
        self.stopSearching(0)

    def setContainerColor(self, r, g, b, a):
        self.containerColorR = r
        self.containerColorG = g
        self.containerColorB = b
        self.containerColorA = a

    def getContainerColor(self):
        return (
         self.containerColorR, self.containerColorG, self.containerColorB, self.containerColorA)