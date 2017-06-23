from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.movement.DistributedMovingObject import DistributedMovingObject
from pirates.creature.DistributedCreature import DistributedCreature
from pirates.creature.Monstrous import Monstrous
from pirates.kraken.KrakenGameFSM import KrakenGameFSM
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from pirates.ship import ShipGlobals
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PiratesGlobals
import math
import time
import random
from otp.otpbase import OTPRender

class bp():
    startup = bpdb.bpPreset(cfg='kraken', grp='startup', static=1)
    startupCall = bpdb.bpPreset(cfg='kraken', grp='startup', static=1, call=1)
    shutdown = bpdb.bpPreset(cfg='kraken', grp='shutdown', static=1)
    shutdownCall = bpdb.bpPreset(cfg='kraken', grp='shutdown', static=1, call=1)
    targeting = bpdb.bpPreset(cfg='kraken', grp='targeting', static=1)
    targetingCall = bpdb.bpPreset(cfg='kraken', grp='targeting', call=1, static=1)
    update = bpdb.bpPreset(cfg='kraken', grp='update', static=1)
    updateCall = bpdb.bpPreset(cfg='kraken', grp='update', call=1, static=1)


class Kraken(DistributedCreature, Monstrous):
    notify = DirectNotifyGlobal.directNotify.newCategory('Kraken')

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr)
        self.body = loader.loadModel('models/char/live_kraken_zero')
        self.body.find('**/kraken_high_tentacles').hide()
        self.body.reparentTo(self)
        self.body.setZ(-140)
        self.body.setH(90)
        self.targetShipId = None
        self.grabberTentacles = {}
        self.holderTentacles = {}
        self.doomTentacles = {}
        self.shipRomRequest = None
        self.dampen = [0, 0]
        self.rTask = None
        self.sinkCutsceneIval = None
        self.sinkShipIval = None
        self.sinkEffectsNode = None
        self.submergeInterval = self.body.posInterval(1, (0, 0, -140), (0, 0, -110))
        self.emergeInterval = self.body.posInterval(4, (0, 0, -110), (0, 0, -140))
        getBase().kraken = self
        self.createGameFSM()
        return

    def setupCreature(self, avatarType):
        DistributedCreature.setupCreature(self, avatarType)
        self.initializeMonstrousTags(self.creature)
        self.creature.getGeomNode().hide(OTPRender.ShadowCameraBitmask)
        self.creature.setupCollisions()

    def announceGenerate(self):
        DistributedMovingObject.announceGenerate(self)
        self.setupSmoothing()

    def disable(self):
        self.submergeInterval.pause()
        self.submergeInterval = None
        self.emergeInterval.pause()
        self.emergeInterval = None
        self.stopSmooth()
        self.stopRangeTask()
        if self.shipRomRequest:
            self.cr.relatedObjectMgr.abortRequest(self.shipRomRequest)
            self.shipRomRequest = None
        if self.sinkCutsceneIval:
            self.sinkCutsceneIval.finish()
            self.sinkCutsceneIval = None
        if self.sinkShipIval:
            self.sinkShipIval.finish()
            self.sinkShipIval = None
        targetShip = self.getTargetShip()
        if targetShip:
            targetShip.setKraken(None)
        DistributedMovingObject.disable(self)
        return

    def createGameFSM(self):
        self.gameFSM = KrakenGameFSM(self)

    def getNameText(self):
        return None

    @bp.targetingCall()
    def setTargetShipId(self, targetShipId):
        self.notify.debug('setTargetShipId: was %s, now %s' % (self.targetShipId, targetShipId))
        targetShip = self.getTargetShip()
        if targetShip:
            targetShip.setKraken(None)
        self.targetShipId = targetShipId
        if self.targetShipId == 0:
            self.submergeInterval.start()
            self.emergeInterval.pause()
        else:
            self.submergeInterval.pause()
            self.emergeInterval.start()
        if self.shipRomRequest:
            self.cr.relatedObjectMgr.abortRequest(self.shipRomRequest)
            self.shipRomRequest = None

        @bp.targetingCall()
        def targetArrived(targetShip):
            self.notify.debug('setTargetShipId:targetArrived: attaching %d grabbers' % len(self.grabberTentacles))
            self.targetRomRequest = None
            targetShip.setKraken(self)
            for grabber in self.grabberTentacles.itervalues():
                grabber.attachToShipLocator()
                grabber.setupCollisions()

            return

        self.targetRomRequest = self.cr.relatedObjectMgr.requestObjects((targetShipId,), eachCallback=targetArrived)
        return

    def getTargetShipId(self):
        return self.targetShipId

    def getTargetShip(self):
        return self.cr.getDo(self.targetShipId)

    def addGrabberTentacle(self, locId, grabber):
        self.grabberTentacles[locId] = grabber
        ship = self.getTargetShip()
        if ship:
            startPos = grabber.getRandomPos()
            grabber.attachToShipLocator(pos=startPos)
            grabber.setupCollisions()

    def addHolderTentacle(self, locId, holder):
        self.holderTentacles[locId] = holder
        ship = self.getTargetShip()
        if ship:
            startPos = holder.getRandomPos()
            holder.attachToShipLocator(pos=startPos)
            holder.setupCollisions()

    def removeGrabberTentacle(self, grabber):
        for locId in self.grabberTentacles:
            if self.grabberTentacles[locId]:
                self.grabberTentacles.pop(locId)
                return

    def getRollAngle(self):
        dampen = 0
        dampenAmounts = [ grabber.getRockingDampen() for grabber in self.grabberTentacles.itervalues() ]
        if dampenAmounts:
            dampen = max(dampenAmounts)
        if dampen:
            frameTime = globalClock.getFrameTime()
            self.dampen[1] = frameTime
        elif self.dampen[0]:
            frameTime = globalClock.getFrameTime()
            dt = globalClock.getFrameTime() - self.dampen[1]
            self.dampen[1] = frameTime
            dampen = max(0, self.dampen[0] - dt * 0.333)
        self.dampen[0] = dampen
        period = 5
        return (1 - dampen) * 25 * max(math.sin(time.time() % period / period * 2 * math.pi), -1)

    def getDampenAmount(self):
        return self.dampen[0]

    def startRangeTask(self):
        self.rTask = taskMgr.add(self.rangeTask, self.uniqueName('rangeTask'))

    def stopRangeTask(self):
        if self.rTask:
            taskMgr.remove(self.rTask)
            self.rTask = None
        return

    def rangeTask(self, task):
        t = task.time
        t = task.frame
        t /= 15
        t %= len(self.grabberTentacles)
        t = int(t)
        for grabber in self.grabberTentacles.itervalues():
            grabber.rangeCollisions.hide()

        self.grabberTentacles[t].rangeCollisions.show()
        return task.cont

    def spawnDoomTentacle(self):
        targetShip = self.getTargetShip()
        if targetShip and not self.doomTentacle:
            self.doomTentacle = DoomTentacle(self.uniqueName)
            self.doomTentacle.reparentTo(self)
            self.doomTentacle.setScale(targetShip.dimensions[1] / 400)
            self.doomTentacle.setEffectsScale(targetShip.dimensions[1] / 100)
            self.doomTentacle.setPos(targetShip, -targetShip.dimensions[0] / 1.3, -1 * ShipGlobals.getShipSplitOffset(targetShip.shipClass) + 2, -15)
            self.doomTentacle.setHpr(targetShip, 90, 0, 0)
        self.doomTentacle.setPlayRate(1.2, 'emerge')
        self.doomTentacle.play('emerge')

    def hideSideTentacles(self, side):
        numTent = len(self.grabberTentacles) / 2
        for i in range(numTent):
            self.grabberTentacles[i + numTent * side].emerge(0)

    def setupSmoothing(self):
        self.activateSmoothing(1, 0)
        self.smoother.setDelay(OTPGlobals.NetworkLatency * 1.5)
        broadcastPeriod = 0.2
        self.smoother.setMaxPositionAge(broadcastPeriod * 1.25 * 10)
        self.smoother.setExpectedBroadcastPeriod(broadcastPeriod)
        self.smoother.setDefaultToStandingStill(False)
        self.startSmooth()

    def setGameState(self, stateName, timeStamp):
        print '!!'
        self.gameFSM.request(stateName)