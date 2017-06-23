import random
from pandac.PandaModules import *
from pirates.creature.DistributedCreature import DistributedCreature
from pirates.creature.Monstrous import Monstrous
from pirates.kraken.HolderGameFSM import HolderGameFSM
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from otp.otpbase import OTPRender

class HolderTentacle(DistributedCreature, Monstrous):

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr)
        self.shipRequest = None
        self.emergeIval = None
        self.moveTask = None
        self.rockingDampen = 0
        self.emerged = 0
        self.emergeIval = None
        return

    def delete(self):
        DistributedCreature.delete(self)

    def setKrakenId(self, krackenId):
        self.krakenId = krackenId

    def getKrakenId(self):
        return self.krakenId

    def getKraken(self):
        return self.cr.getDo(self.krakenId)

    def createGameFSM(self):
        self.gameFSM = HolderGameFSM(self)

    def emerge(self, emerge):
        if self.emergeIval:
            self.emergeIval.finish()
            self.emergeIval = None
        if emerge:
            self.setPlayRate(0.75, 'emerge')
            self.emergeIval = Sequence(Wait(random.random()), Func(self.creature.show), Func(self.play, 'emerge', blendInT=0))
        else:
            self.setPlayRate(-1, 'emerge')
            self.emergeIval = Sequence(Wait(random.random()), Func(self.play, 'emerge', blendOutT=0), Wait(self.creature.getDuration('emerge') / abs(self.creature.getPlayRate('emerge')) - 0.1), Func(self.creature.hide))
        self.emergeIval.start()
        return

    def setLocatorId(self, locatorId):
        self.locatorId = locatorId

        def krakenArrived(kraken):
            self.krakenRequest = None
            kraken.addHolderTentacle(self.locatorId, self)
            return

        self.krakenRequest = self.cr.relatedObjectMgr.requestObjects((self.krakenId,), eachCallback=krakenArrived)

    def attachToShipLocator(self, time=0, pos=Point3(0), wrt=False):

        def shipArrived(ship):
            self.shipRequest = None
            locator = ship.getKrakenHolderLocator(self.locatorId)
            if wrt:
                self.wrtSetBase(locator, scale=1)
            else:
                self.setBase(locator, scale=1)
            self.creature.setEffectsScale(2 * locator.getScale()[0])
            self.creature.setupCollisions()
            return

        kraken = self.getKraken()
        if self.shipRequest:
            self.cr.relatedObjectMgr.abortRequest(self.shipRequest)
            self.shipRequest = None
        self.shipRequest = self.cr.relatedObjectMgr.requestObjects((kraken.getTargetShipId(),), eachCallback=shipArrived)
        return

    def setupCollisions(self):
        pass

    def getRandomPos(self):
        return Point3(0, 0, 0)

    def setBase(self, node, scale=0):
        ship = node.getNetPythonTag('ship')
        transform = node.getTransform(ship.model.modelRoot)
        self.slideBase.reparentTo(ship.model.modelRoot)
        self.slideBase.setTransform(transform)
        if scale:
            self.slideBase.setScale(scale)

    def wrtSetBase(self, node, scale=0):
        self.slideBase.wrtReparentTo(node)
        if scale:
            self.slideBase.setScale(scale)

    def setupCreature(self, avatarType):
        DistributedCreature.setupCreature(self, avatarType)
        self.slideBase = NodePath('slideBase')
        self.slider = self.slideBase.attachNewNode('slider')
        self.slider.setPos(-5, 0, 47)
        self.creature.reparentTo(self.slider)
        self.creature.getGeomNode().hide(OTPRender.ShadowCameraBitmask)
        self.creature.generateCreature()
        self.creature.loop('idle')
        self.initializeMonstrousTags(self.creature)

    def resetSlider(self, time=0, pos=Point3(0), callback=None):
        self.stopMove()
        if time:
            task = taskMgr.add(self.resetSliderTask, self.uniqueName('move'))
            task.tFinal = time
            task.callback = callback
            task.sBPos = self.slideBase.getPos()
            task.sBHpr = self.slideBase.getHpr()
            task.sPos = self.slider.getPos()
            task.sHpr = self.slider.getHpr()
            task.sPosFinal = pos
            self.moveTask = task
            return task
        else:
            self.slideBase.setPosHpr(0, 0, 0, 0, 0, 0)
            self.slider.setPos(pos)
            if callback:
                callback(True)

    def resetSliderTask(self, task):
        t = min(1, task.time / task.tFinal)
        sBPos = lerp(task.sBPos, Point3(0), t)
        sBHpr = lerp(task.sBHpr, VBase3(0), t)
        sPos = lerp(task.sPos, task.sPosFinal, t)
        self.slideBase.setPos(sBPos)
        self.slideBase.setHpr(sBHpr)
        self.slider.setPos(sPos)
        if task.time < task.tFinal:
            return task.cont
        if task.callback:
            task.callback(True)
        self.moveTask = None
        return task.done

    def stopMove(self):
        if self.moveTask:
            taskMgr.remove(self.moveTask)
            self.setRockingDampen(0)
            if self.moveTask.callback:
                self.moveTask.callback(False)
            self.moveTask = None
        return

    def isMoving(self):
        return bool(self.moveTask)

    def initializeBattleCollisions(self):
        pass

    def isInteractiveMasked(self):
        return 1
