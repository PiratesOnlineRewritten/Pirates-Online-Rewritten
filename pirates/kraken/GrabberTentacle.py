from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from otp.otpbase import OTPRender
from pirates.creature.DistributedCreature import DistributedCreature
from pirates.creature.Monstrous import Monstrous
from pirates.kraken.GrabberGameFSM import GrabberGameFSM
from pirates.piratesbase import PiratesGlobals
import math
import random

class GrabberTentacle(DistributedCreature, Monstrous):
    notify = DirectNotifyGlobal.directNotify.newCategory('GrabberTentacle')

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr)
        self.krakenId = 0
        self.krakenRequest = None
        self.avatarId = 0
        self.avRequest = None
        self.shipRequest = None
        self.moveTask = None
        self.rockingDampen = 0
        self.emerged = 0
        self.emergeIval = None
        self.locatorId = -1
        self.rangeCollisions = None
        self.collisionsSet = False
        return

    def setupCreature(self, avatarType):
        DistributedCreature.setupCreature(self, avatarType)
        self.slideBase = NodePath('slideBase')
        self.slider = self.slideBase.attachNewNode('slider')
        self.creature.reparentTo(self.slider)
        self.initializeMonstrousTags(self.creature)
        self.creature.getGeomNode().hide(OTPRender.ShadowCameraBitmask)

    def announceGenerate(self):
        DistributedCreature.announceGenerate(self)
        self.accept('f8', self.grabAvatar, extraArgs=[localAvatar])
        self.creature.hide()
        self.accept(self.uniqueName('enterRange'), self.withinRange)
        self.accept(self.uniqueName('exitRange'), self.withoutRange)
        self.creature.setPythonTag('tentacle', self)
        if not hasattr(base, 'tentacles'):
            getBase().tentacles = []
        getBase().tentacles.append(self)

    def disable(self):
        getBase().tentacles.remove(self)
        if self.krakenRequest:
            self.cr.relatedObjectMgr.abortRequest(self.krakenRequest)
            self.krakenRequest = None
        if self.avRequest:
            self.cr.relatedObjectMgr.abortRequest(self.avRequest)
            self.avRequest = None
        if self.shipRequest:
            self.cr.relatedObjectMgr.abortRequest(self.shipRequest)
            self.shipRequest = None
        self.avatarId = 0
        taskMgr.remove(self.uniqueName('grabDelay'))
        kraken = self.getKraken()
        if kraken:
            kraken.removeGrabberTentacle(self.doId)
        self.ignore('f8')
        self.ignore(self.uniqueName('enterRange'))
        self.ignore(self.uniqueName('exitRange'))
        self.creature.disable()
        self.slideBase.detachNode()
        if self.rangeCollisions:
            self.rangeCollisions.detachNode()
            self.rangeCollisions = None
        DistributedCreature.disable(self)
        return

    def delete(self):
        self.creature.delete()
        self.krakenId = 0
        self.locatorId = -1
        self.slider = None
        self.slideBase = None
        self.creature = None
        DistributedCreature.delete(self)
        return

    def wantsSmoothing(self):
        return 0

    def setKrakenId(self, krakenId):
        self.krakenId = krakenId

    def getKraken(self):
        return self.cr.doId2do.get(self.krakenId)

    def createGameFSM(self):
        self.gameFSM = GrabberGameFSM(self)

    def getShip(self):
        kraken = self.getKraken()
        return kraken and kraken.getTargetShip()

    def setLocatorId(self, locatorId):
        self.locatorId = locatorId

        def krakenArrived(kraken):
            self.krakenRequest = None
            kraken.addGrabberTentacle(self.locatorId, self)
            return

        self.krakenRequest = self.cr.relatedObjectMgr.requestObjects((self.krakenId,), eachCallback=krakenArrived)

    def setRockingDampen(self, val):
        self.rockingDampen = val

    def getRockingDampen(self):
        return self.rockingDampen

    def attachToShipLocator(self, time=0, pos=Point3(0), wrt=False):

        def shipArrived(ship):
            self.shipRequest = None
            locator = ship.getKrakenGrabberLocator(self.locatorId)
            if wrt:
                self.wrtSetBase(locator, scale=1)
            else:
                self.setBase(locator, scale=1)
            self.creature.setEffectsScale(2 * locator.getScale()[0])
            if not self.collisionsSet:
                self.creature.setupCollisions()
                self.collisionsSet = True
            return

        kraken = self.getKraken()
        if self.shipRequest:
            self.cr.relatedObjectMgr.abortRequest(self.shipRequest)
            self.shipRequest = None
        self.shipRequest = self.cr.relatedObjectMgr.requestObjects((kraken.getTargetShipId(),), eachCallback=shipArrived)
        return

    def attachToShipModel(self):

        def shipArrived(ship):
            self.shipRequest = None
            self.wrtSetBase(ship.getModelRoot())
            if not self.collisionsSet:
                self.creature.setupCollisions()
                self.collisionsSet = True
            return

        kraken = self.getKraken()
        if self.shipRequest:
            self.cr.relatedObjectMgr.abortRequest(self.shipRequest)
            self.shipRequest = None
        self.shipRequest = self.cr.relatedObjectMgr.requestObjects((kraken.getTargetShipId(),), eachCallback=shipArrived)
        return

    def setBase(self, node, scale=0):
        self.slideBase.reparentTo(node)
        if scale:
            self.slideBase.setScale(scale)

    def wrtSetBase(self, node, scale=0):
        self.slideBase.wrtReparentTo(node)
        if scale:
            self.slideBase.setScale(scale)

    def loop(self, *args, **kw):
        if args and args[0] == 'idle' or kw.get('animName') == 'idle' or kw.get('newAnim') == 'idle':
            kw['restart'] = 0
        DistributedCreature.loop(self, *args, **kw)

    def emerge(self, emerge):
        if emerge:
            if self.gameFSM.state in ['Off', 'Submerged']:
                self.requestGameState('Idle')
        else:
            self.requestGameState('Submerged')

    def grabAvatar(self, avId):
        taskMgr.remove(self.uniqueName('grabDelay'))
        self.stopMove()
        if avId:
            if self.avRequest:
                self.cr.relatedObjectMgr.abortRequest(self.avRequest)
                self.avRequest = None

            def avatarArrived(av):
                self.avRequest = None
                self.l_grabAvatar(av)
                return

            self.avRequest = self.cr.relatedObjectMgr.requestObjects((avId,), eachCallback=avatarArrived)
        elif self.avatarId:
            if self.avRequest:
                self.cr.relatedObjectMgr.abortRequest(self.avRequest)
                self.avRequest = None
            else:

                def avatarArrived(av):
                    self.avRequest = None
                    self.l_releaseAvatar(av)
                    return

                self.avRequest = self.cr.relatedObjectMgr.requestObjects((self.avatarId,), eachCallback=avatarArrived)
        return

    def l_grabAvatar(self, av):

        def moveComplete(completed):
            if completed:
                self.attachToShipModel()
                self.avatarId = av.doId
                self.reparentNodeToTip(av)
                av.setY(-4)
                av.loop('tentacle_struggle')
                taskMgr.doMethodLater(2, self.setAvatarToGrabbedState, self.uniqueName('grabDelay'), extraArgs=[av])
            else:
                self.notify.debug('move interrupted')

        time = 0.5
        blendDelay = 0
        self.creature.setPlayRate(4, 'grab_avatar')
        self.creature.play('grab_avatar')
        self.creature.loop('grab_avatar_idle', blendT=time - blendDelay, blendDelay=blendDelay)
        targetNode = av.find('grab_offset')
        if targetNode.isEmpty():
            targetNode = av.attachNewNode('grab_offset')
            targetNode.setZ(4)
        if av.isLocal():
            av.b_setGameState('TentacleTargeted', [self])
        else:
            av.setGameState('TentacleTargeted', [self], localChange=1)
        self.moveTask = self.moveToTarget(targetNode, time, True, moveComplete)

    def l_releaseAvatar(self, av):
        self.avatarId = 0
        time = self.creature.getDuration('grab_avatar')
        blendDelay = 0.5
        self.creature.setPlayRate(-1, 'grab_avatar')
        self.creature.play('grab_avatar')
        self.creature.loop('idle_d', blendT=time - blendDelay, blendDelay=blendDelay)
        self.attachToShipLocator(3, pos=self.getRandomPos(), wrt=True)
        av.wrtReparentTo(self.getShip().getModelRoot())
        if av.isLocal():
            av.b_setGameState('LandRoam')
        else:
            av.setGameState('LandRoam', localChange=1)

    def reparentNodeToTip(self, node):
        node.wrtReparentTo(self.creature.getGrabTipNode())
        node.setPosHpr(0, 0, 0, 0, -90, 0)
        node.setScale(render, 1)

    def setAvatarToGrabbedState(self, av):
        state = 'TentacleGrabbed'
        if av.isLocal():
            av.b_setGameState(state, [self])
        else:
            av.setGameState(state, localChange=1)

    def setGrabbedAvatar(self, avId):
        if self.isMoving():
            pass
        else:

            def avatarArrived(av):
                self.avRequest = None
                self.reparentNodeToTip(av)
                self.avatarId = avId
                self.loop('grab_avatar_idle', blendT=0)
                self.attachToShipModel()
                return

            if self.avRequest:
                self.cr.relatedObjectMgr.abortRequest(self.avRequest)
                self.avRequest = None
            self.avRequest = self.cr.relatedObjectMgr.requestObjects((avId,), eachCallback=avatarArrived)
        return

    def moveToTarget(self, targetNode, time, dampenRocking=False, callback=None):
        self.stopMove()
        task = taskMgr.add(self.targetMoveTask, self.uniqueName('move'))
        task.targetNode = targetNode
        task.tFinal = time
        task.dampenRocking = dampenRocking
        distance = self.creature.getGrabTargetNode().getPos(self.slideBase) - task.targetNode.getPos(self.slideBase)
        task.z0 = distance.getZ()
        distance.setZ(0)
        task.d0 = distance.length()
        reach = self.creature.getGrabTargetNode().getPos(self.creature)
        task.height = reach.getZ()
        reach.setZ(0)
        task.hypo = reach.length()
        task.hypo2 = task.hypo * task.hypo
        task.lam = math.asin(reach[0] / task.hypo)
        task.callback = callback
        return task

    def targetMoveTask(self, task):
        if task.dampenRocking:
            self.setRockingDampen(min(1, task.time / task.tFinal))
        distance = max(0, lerp(task.d0, 0, min(1, task.time / task.tFinal)))
        zDistance = lerp(task.z0, 0, min(1, task.time / task.tFinal))
        vTargetToTip = self.creature.getGrabTargetNode().getPos(self.slideBase) - task.targetNode.getPos(self.slideBase)
        flatTargetToTip = Point3(vTargetToTip)
        flatTargetToTip.setZ(0)
        flatTargetToTip.normalize()
        tipPos = flatTargetToTip * distance + task.targetNode.getPos(self.slideBase)
        creatureTipPos = self.creature.getRelativePoint(self.slideBase, tipPos)
        lam = math.atan2(creatureTipPos[0], -creatureTipPos[1])
        deltaTheta = lam - task.lam
        if abs(tipPos[0]) < abs(task.hypo):
            a = math.sqrt(task.hypo2 - tipPos[0] * tipPos[0])
        else:
            a = 0
        y = max(0, tipPos[1] + a)
        self.slider.setH(self.slider, deltaTheta / math.pi * 180)
        self.slider.setY(self.slideBase, y)
        zTargetToTip = vTargetToTip.getZ()
        zPos = zDistance + task.targetNode.getZ(self.slideBase)
        self.slider.setZ(self.slideBase, zPos - task.height)
        if task.time < task.tFinal:
            return task.cont
        if task.callback:
            task.callback(True)
        self.setRockingDampen(0)
        self.moveTask = None
        return task.done

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

    def setupCollisions(self):
        if not self.rangeCollisions:
            ship = self.getShip()
            rParent = ship.getKrakenRangeParent(self.locatorId)
            self.creature.pose('grab_avatar_idle', 0, blendT=0)
            self.creature.update()
            range = self.creature.getGrabTargetNode().getPos().length()
            from pirates.piratesbase import PiratesGlobals
            cNode = CollisionNode(self.uniqueName('Range'))
            cNode.setFromCollideMask(BitMask32.allOff())
            cNode.setIntoCollideMask(PiratesGlobals.WallBitmask)
            cSolid = CollisionTube(Point3(0), Point3(0, 0, 1), 1)
            cSolid.setTangible(0)
            cNode.addSolid(cSolid)
            cNodePath = NodePath(cNode)
            cNodePath.reparentTo(rParent)
            cNodePath.setScale(int(range * 0.9))
            self.rangeCollisions = cNodePath

    def withinRange(self, cEntry):
        self.notify.debug('withinRange-%s(%s)' % (self.doId, self.locatorId))

    def withoutRange(self, cEntry):
        self.notify.debug('withoutRange-%s(%s)' % (self.doId, self.locatorId))

    def showVis(self):
        self.rangeCollisions.show()

    def hideVis(self):
        self.rangeCollisions.hide()

    def getRandomPos(self):
        return Point3(0, lerp(0, 60, random.random()), lerp(-10, -40, random.random()))

    @staticmethod
    def showAllVis():
        for t in getBase().tentacles:
            t.showVis()

    @staticmethod
    def hideAllVis():
        for t in getBase().tentacles:
            t.hideVis()

    def initializeBattleCollisions(self):
        pass

    def isInteractiveMasked(self):
        return 1
