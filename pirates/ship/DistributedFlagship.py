from pandac.PandaModules import *
from direct.task import Task
from direct.gui.DirectGui import *
from direct.distributed.DistributedObject import DistributedObject
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer

class DistributedFlagship(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.currWave = 0
        self.maxWave = 0
        self.flagshipUIBaseNode = None
        self.baseFrame = None
        self.counter = None
        self.counterNode = None
        self.waveCount = None
        self.waveCountNode = None
        self.counterLabel = None
        self.counterLabelNode = None
        self.updateCounterTask = None
        return

    def startWave(self, countdown, currWave, maxWave):
        self.currWave = currWave
        self.maxWave = maxWave
        self.resetWavesUI()
        if not self.flagshipUIBaseNode:
            self.flagshipUIBaseNode = base.a2dTopLeft.attachNewNode('FlagshipUIBaseNode')
            self.flagshipUIBaseNode.setPos(1.15, 0, -0.42)
            self.flagshipUIBaseNode.setScale(0.75)
            globalGui = loader.loadModel('models/gui/toplevel_gui')
            if localAvatar.ship:
                self.baseFrame = DirectFrame(parent=localAvatar.ship.flagshipUIBaseNode, relief=None, state=DGG.DISABLED, image=globalGui.find('**/generic_box'), image_scale=0.12, image_pos=(0,
                                                                                                                                                                                               0,
                                                                                                                                                                                               0), pos=(0,
                                                                                                                                                                                                        0,
                                                                                                                                                                                                        0))
                self.baseFrame.reparentTo(self.flagshipUIBaseNode)
                self.baseFrame.setScale(16, 1, 8)
                self.baseFrame.setPos(0.3, 0, 0.075)
        if self.waveCount:
            pass
        else:
            self.waveCount = TextNode('BreakRemainingText')
            self.waveCount.setFont(PiratesGlobals.getInterfaceFont())
            self.waveCount.setTextColor(PiratesGuiGlobals.TextFG1)
            self.waveCount.setAlign(TextNode.ACenter)
            self.waveCount.setText(PLocalizer.FlagshipWaveCount % (str(currWave - 1), str(self.maxWave)))
            self.waveCountNode = self.flagshipUIBaseNode.attachNewNode(self.waveCount)
            self.waveCountNode.setPos(0.3, 0, 0.1)
            self.waveCountNode.setScale(0.075)
            if currWave <= 1:
                self.flagshipUIBaseNode.hide()
        if self.counter:
            pass
        else:
            self.counter = TextNode('BreakRemainingText')
            self.counter.setFont(PiratesGlobals.getInterfaceFont())
            self.counter.setTextColor(PiratesGuiGlobals.TextFG1)
            self.counter.setAlign(TextNode.ACenter)
            self.counter.setText(str(countdown))
            self.counterNode = self.flagshipUIBaseNode.attachNewNode(self.counter)
            self.counterNode.setPos(0.45, 0, 0)
            self.counterNode.setScale(0.1)
            self.counterLabel = TextNode('BreakRemainingTextLabel')
            self.counterLabel.setFont(PiratesGlobals.getInterfaceFont())
            self.counterLabel.setTextColor(PiratesGuiGlobals.TextFG1)
            self.counterLabel.setAlign(TextNode.ACenter)
            self.counterLabel.setText(PLocalizer.FlagshipWaveCountdown)
            self.counterLabelNode = self.flagshipUIBaseNode.attachNewNode(self.counterLabel)
            self.counterLabelNode.setPos(0.25, 0, 0)
            self.counterLabelNode.setScale(0.05)
        self.counterEndTime = globalClock.getRealTime() + countdown
        if self.updateCounterTask:
            taskMgr.remove(self.updateCounterTask)
        self.updateCounterTask = taskMgr.add(self.updateCounter, 'updateCounterTask')
        return

    def updateCounter(self, task=None):
        timeLeft = self.counterEndTime - globalClock.getRealTime()
        if timeLeft <= 0:
            self.counter = None
            self.counterNode.removeNode()
            self.counterNode = None
            self.counterLabel = None
            self.counterLabelNode.removeNode()
            self.counterLabelNode = None
            self.updateCounterTask = None
            self.waveCount.setText(PLocalizer.FlagshipWaveCount % (str(self.currWave), str(self.maxWave)))
            if self.currWave >= 1:
                self.flagshipUIBaseNode.show()
            return Task.done
        else:
            self.counter.setText(str(int(timeLeft)))
            return Task.cont
        return

    def resetWavesUI(self):
        if self.updateCounterTask:
            taskMgr.remove(self.updateCounterTask)
            self.updateCounterTask = None
        self.counter = None
        if self.counterNode:
            self.counterNode.removeNode()
            self.counterNode = None
        self.counterLabel = None
        if self.counterLabelNode:
            self.counterLabelNode.removeNode()
            self.counterLabelNode = None
        self.waveCount = None
        if self.waveCountNode:
            self.waveCountNode.removeNode()
            self.waveCountNode = None
        return

    def clearWaves(self):
        self.resetWavesUI()
        if self.flagshipUIBaseNode:
            self.flagshipUIBaseNode.removeNode()
            self.flagshipUIBaseNode = None
        if self.baseFrame:
            self.baseFrame.removeNode()
            self.baseFrame = None
        return

    def delete(self):
        self.clearWaves()

    def localAvatarExitShip(self, boardingFlagship=0):
        self.clearWaves()