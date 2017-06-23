from pandac.PandaModules import Point3, Vec3, Vec4, VBase3, CompassEffect, ModelNode, TransformState, NodePath, NodePathCollection
from direct.showbase import DirectObject
from pirates.piratesbase import PiratesGlobals
from direct.interval.AnimControlInterval import AnimControlInterval
from direct.interval.IntervalGlobal import Sequence, Func
from pirates.audio.SoundGlobals import loadSfx
from pirates.audio import SoundGlobals
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PLocalizer
from pirates.effects.ShipPowerRecharge import ShipPowerRecharge
from pirates.effects.ProtectionDome import ProtectionDome
from pirates.effects.WindBlurCone import WindBlurCone
from pirates.effects.FadingCard import FadingCard
from pirates.effects.DarkMaelstrom import DarkMaelstrom
from pirates.effects.Wind import Wind
from pirates.effects.Wake import Wake
from pirates.effects.WaterWakes import WaterWakes
from pirates.effects.WaterMist import WaterMist
from pirates.effects.ShipFire import ShipFire
from pirates.effects.ShipSmoke import ShipSmoke
from pirates.effects.DarkShipFog import DarkShipFog
from pirates.ship import ShipGlobals
from pirates.battle import Cannon
from pirates.shipparts import CannonPort
from direct.showutil.Rope import Rope
from pandac.PandaModules import RopeNode
import random

class Ship(DirectObject.DirectObject):
    notify = directNotify.newCategory('Ship')
    WantWake = config.GetBool('want-wake', 1)
    breakSfx1 = None
    breakSfx3 = None
    sinkingSfx1 = None
    sinkingSfx2 = None

    def __init__(self, shipClass, root, breakAnims, hitAnims, metaAnims, collisions, locators):
        self.modelRoot = root
        self.transRoot = NodePath('transRoot')
        self.modelRoot.reparentTo(self.transRoot)
        self.shipRoot = None
        self.shipClass = shipClass
        self.sailing = False
        self.sfxAlternativeStyle = False
        self.landedGrapples = []
        self.landedGrappleNodes = []
        self.breakAnims = breakAnims
        self.hitAnims = hitAnims
        self.metaAnims = metaAnims
        self.char = self.modelRoot.find('**/+Character')
        self.riggingControls = {}
        numBundles = self.char.node().getNumBundles()
        masts = self.breakAnims.keys()
        masts.sort()
        self.sinkTimeScale = 1.0
        if self.breakSfx1 is None:
            Ship.breakSfx1 = loadSfx(SoundGlobals.SFX_SHIP_MAST_BREAK_01)
        if self.breakSfx3 == None:
            Ship.breakSfx3 = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_MAST_BREAK)
        for i, j in enumerate(masts):
            bundle = self.char.node().getBundle(i + 1)
            ladderJoint = bundle.findChild('def_ladder_base')
            if ladderJoint:
                self.riggingControls[j] = ladderJoint

        self.__breakIvals = {}
        for i in self.breakAnims:
            self.__breakIvals[i] = Sequence(AnimControlInterval(self.breakAnims[i][0]), AnimControlInterval(self.breakAnims[i][1]))

        self.__hitSailingIvals = {}
        for i in self.breakAnims:
            self.__hitSailingIvals[i] = Sequence(AnimControlInterval(self.hitAnims[i][1]), Func(self.metaAnims['idle'].playAll))

        self.lod = self.modelRoot.find('**/+LODNode')
        self.modelCollisions = collisions
        self.mastStates = [
         1, 1, 1, 1, 1]
        self.mastsHidden = False
        self.__targetableCollisions = []
        self.locators = locators
        self.center = None
        self.stern = None
        self.bow = None
        self.starboard = None
        self.port = None
        if self.sinkingSfx1 is None:
            Ship.sinkingSfx1 = loadSfx(SoundGlobals.SFX_SHIP_SINKING)
            Ship.sinkingSfx2 = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_SHIP_SINK)
        self.sinkEffectsRoot = None
        self.sinkEffects = []
        self.sinkTrack = None
        self.isSplit = False
        self.owner = None
        self.mastCollisions = dict([ (int(x.getTag('Mast Code')), x) for x in self.modelCollisions.findAllMatches('**/collision_masts') ])
        self.sailCollisions = self.modelCollisions.findAllMatches('**/collision_sails')
        self.disableSails()
        if self.metaAnims['rolldown'].getNumAnims():
            self.__rollDownIval = AnimControlInterval(self.metaAnims['rolldown'])
            self.metaAnims['rolldown'].poseAll(0)
        else:
            self.__rollDownIval = Interval('dummy', 0, 0)
        if self.metaAnims['rollup'].getNumAnims():
            self.__rollUpIval = AnimControlInterval(self.metaAnims['rollup'])
        else:
            self.__rollUpIval = Interval('dummy', 0, 0)
        self.sailStartIval = Sequence(Func(self.stopIvals), Func(self.enableSails), self.__rollDownIval, Func(self.metaAnims['idle'].loopAll, 1))
        self.sailStopIval = Sequence(Func(self.stopIvals), self.__rollUpIval, Func(self.disableSails), Func(self.metaAnims['tiedup'].playAll))
        self.windTunnelEffect1 = None
        self.windTunnelEffect2 = None
        self.windConeEffect = None
        self.powerRechargeEffect = None
        self.protectionEffect = None
        self.takeCoverEffect = None
        self.openFireEffect = None
        self.stormEffect = None
        self.wake = None
        self.fogEffect = None
        self.leftSideFire = None
        self.leftSideSmoke = None
        self.leftSideFire2 = None
        self.leftSideSmoke2 = None
        self.rightSideFire = None
        self.rightSideSmoke = None
        self.rightSideFire2 = None
        self.rightSideSmoke2 = None
        self.rearSideFire = None
        self.rearSideSmoke = None
        self.fader = None
        self.idleBounds = self.modelRoot.getTightBounds()
        self.setupCollisions()
        return

    def setOwner(self, owner, ownerIsModelRoot=False):
        self.owner = owner
        if self.owner:
            if ownerIsModelRoot:
                self.shipRoot = self.owner.getParent()
                self.owner.reparentTo(self.shipRoot)
                self.transRoot.reparentTo(self.owner)
            else:
                self.shipRoot = self.owner.attachNewNode('ShipRoot')
                self.transRoot.reparentTo(self.shipRoot)
            self.modelRoot.setPythonTag('ship', owner)

    def setupCollisions(self):
        self.modelCollisions.setTag('objType', str(PiratesGlobals.COLL_NEWSHIP))
        self.floors = self.modelCollisions.find('**/collision_floors')
        self.deck = self.modelCollisions.find('**/collision_deck')
        self.planeBarriers = self.modelCollisions.find('**/collision_planes')
        self.planeBarriers.stash()
        self.walls = self.modelCollisions.find('**/collision_walls')
        self.shipCollWall = self.modelCollisions.find('**/collision_shiptoship')
        self.shipCollWall.setTag('objType', str(PiratesGlobals.COLL_NEWSHIP))
        if self.owner:
            self.shipCollWall.setTag('shipId', str(self.owner.doId))
        self.panels = self.modelCollisions.find('**/collision_panels')
        self.stashPlaneCollisions()

    def stashPlaneCollisions(self):
        self.planeBarriers.stash()

    def unstashPlaneCollisions(self):
        self.planeBarriers.unstash()

    def computeDimensions(self):
        if not self.center:
            self.center = self.modelRoot.attachNewNode('center')
        tb = self.idleBounds
        self.center.setPos((tb[0] + tb[1]) / 2.0)
        self.dimensions = tb[1] - tb[0]
        self.hullDimensions = tb[1] - tb[0]
        if not self.bow:
            self.bow = self.modelRoot.attachNewNode('bowPos')
        if not self.port:
            self.port = self.modelRoot.attachNewNode('portPos')
        if not self.starboard:
            self.starboard = self.modelRoot.attachNewNode('starboardPos')
        if not self.stern:
            self.stern = self.modelRoot.attachNewNode('sternPos')
        self.stern.setPos(Point3(0, tb[1][1], 0))
        self.bow.setPos(Point3(0, tb[0][1], 0))
        self.starboard.setPos(Point3(tb[1][0], 0, 0))
        self.port.setPos(Point3(tb[0][0], 0, 0))

    def getBoardingLocators(self):
        return self.locators.findAllMatches('**/boarding_spot_*;+s')

    def getPartNodes(self):
        if not self.center:
            self.computeDimensions()
        return (self.bow, self.port, self.starboard, self.stern)

    def disableOnDeckInteractions(self):
        pass

    def uniqueName(self, name):
        return name + '-%s' % id(self)

    def isInCrew(self, avId):
        if self.owner:
            return self.owner.isInCrew(avId)
        return False

    def dropMast(self, index):
        if index in self.breakAnims:
            self.breakAnims[index][1].playAll()
            self.dropRigging(index)
            self.mastCollisions[index].stash()
        self.mastStates[index] = 0

    def dropRigging(self, index):
        if index in self.riggingControls:
            self.riggingControls[index].applyFreeze(TransformState.makeScale((0, 0,
                                                                              0)))
            self.char.node().forceUpdate()

    def restoreRigging(self, index):
        if index in self.riggingControls:
            self.riggingControls[index].applyFreeze(TransformState.makeMat(self.riggingControls[index].getDefaultValue()))
            self.char.node().forceUpdate()

    def hideMasts(self):
        self.mastsHidden = True
        for i in range(5):
            if i in self.breakAnims:
                if self.mastStates[i]:
                    self.breakAnims[i][1].playAll()
                    self.dropRigging(i)

    def showMasts(self):
        self.mastsHidden = False
        for i in range(5):
            if i in self.breakAnims:
                if self.mastStates[i]:
                    self.breakAnims[i][0].poseAll(0)
                    self.restoreRigging(i)

    def breakMast(self, index):
        breakSfx = self.breakSfx1
        if self.sfxAlternativeStyle:
            breakSfx = self.breakSfx3
        base.playSfx(breakSfx, node=self.modelRoot, cutoff=3000)
        if index in self.breakAnims:
            self.__hitSailingIvals[index].pause()
            self.__breakIvals[index].pause()
            self.__breakIvals[index].start()
            self.dropRigging(index)
            self.mastCollisions[index].stash()
        self.mastStates[index] = 0

    def restoreMast(self, index):
        if index in self.breakAnims:
            self.__breakIvals[index].pause()
            self.breakAnims[index][0].poseAll(0)
            self.restoreRigging(index)
            self.mastCollisions[index].unstash()
        self.mastStates[index] = 1

    def mastHit(self, index):
        if index in self.hitAnims:
            if self.mastStates[index]:
                if not self.mastsHidden:
                    self.sailing or self.hitAnims[index][0].playAll()
                else:
                    self.__hitSailingIvals[index].start()

    def stopIvals(self):
        self.__rollDownIval.pause()
        self.__rollUpIval.pause()
        for ival in self.__hitSailingIvals.values():
            ival.pause()

    def playIdle(self):
        self.stopIvals()
        self.metaAnims['idle'].loopAll(1)

    def instantSailing(self):
        self.sailing = True
        self.enableSails()
        self.sailStopIval.pause()
        self.sailStartIval.pause()
        self.metaAnims['idle'].loopAll(1)

    def startSailing(self):
        self.stopIvals()
        if not self.sailing:
            self.sailing = True
            self.sailStopIval.pause()
            self.sailStartIval.pause()
            self.sailStartIval.start()

    def instantDocked(self):
        self.sailing = False
        self.disableSails()
        self.stopIvals()
        self.sailStopIval.pause()
        self.sailStartIval.pause()
        self.metaAnims['tiedup'].playAll()

    def stopSailing(self):
        if self.sailing:
            self.sailing = False
            self.sailStartIval.pause()
            self.sailStopIval.pause()
            self.sailStopIval.start()

    def playFullSailEffect(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            if not self.windTunnelEffect1:
                self.windTunnelEffect1 = Wind.getEffect()
            if self.windTunnelEffect1:
                self.windTunnelEffect1.reparentTo(self.center)
                self.windTunnelEffect1.fadeColor = Vec4(0.8, 0.8, 0.8, 0.5)
                self.windTunnelEffect1.setScale(self.dimensions / 6.0)
                self.windTunnelEffect1.fadeTime = 2.0
                self.windTunnelEffect1.setH(180)
                self.windTunnelEffect1.play()

    def playComeAboutEffect(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            if not self.windTunnelEffect2:
                self.windTunnelEffect2 = Wind.getEffect()
            if self.windTunnelEffect2:
                self.windTunnelEffect2.reparentTo(self.center)
                self.windTunnelEffect2.fadeColor = Vec4(0.8, 0.8, 0.8, 0.4)
                self.windTunnelEffect2.setScale(self.dimensions / 10.0)
                self.windTunnelEffect2.fadeTime = 2.0
                self.windTunnelEffect2.setH(0)
                self.windTunnelEffect2.play()

    def playRamEffect(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            if not self.windConeEffect:
                self.windConeEffect = WindBlurCone.getEffect()
            if self.windConeEffect:
                self.windConeEffect.reparentTo(self.bow)
                self.windConeEffect.fadeColor = Vec4(0.8, 0.8, 0.8, 0.5)
                self.windConeEffect.setScale(self.dimensions / 3.0)
                self.windConeEffect.setPos(0, self.dimensions[1] / 18.0, self.dimensions[2] / 4.0)
                self.windConeEffect.fadeTime = 2.0
                self.windConeEffect.startLoop()

    def playRechargeEffect(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            if not self.powerRechargeEffect:
                self.powerRechargeEffect = ShipPowerRecharge.getEffect()
            if self.powerRechargeEffect:
                self.powerRechargeEffect.reparentTo(self.char)
                self.powerRechargeEffect.setEffectColor(Vec4(0.5, 0.5, 1, 1))
                self.powerRechargeEffect.setScale(self.dimensions / 4.0)
                self.powerRechargeEffect.startLoop()

    def playSpawnEffect(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            self.protectionEffect = ProtectionDome.getEffect()
            if self.protectionEffect:
                self.protectionEffect.reparentTo(self.shipRoot)
                self.protectionEffect.setScale(self.dimensions[1] / 15.0)
                self.protectionEffect.startLoop()

    def playTakeCoverEffect(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            self.takeCoverEffect = FadingCard(loader.loadModel('models/textureCards/skillIcons').find('**/sail_take_cover'), color=Vec4(1, 1, 1, 1), fadeTime=0.01, waitTime=2.5, startScale=0.95, endScale=1.0)
            if self.takeCoverEffect:
                self.takeCoverEffect.reparentTo(self.shipRoot)
                self.takeCoverEffect.setPos(0, 0, self.dimensions[2] * 1.25)
                self.takeCoverEffect.setScale(self.dimensions[1] / 4.0)
                self.takeCoverEffect.play()
                self.owner.playTextEffect(PLocalizer.CrewBuffTakeCoverString)

    def playOpenFireEffect(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            self.openFireEffect = FadingCard(loader.loadModel('models/textureCards/skillIcons').find('**/sail_openfire2'), color=Vec4(1, 1, 1, 1), fadeTime=0.01, waitTime=2.5, startScale=0.95, endScale=1.0)
            if self.openFireEffect:
                self.openFireEffect.reparentTo(self.shipRoot)
                self.openFireEffect.setPos(0, 0, self.dimensions[2] * 1.25)
                self.openFireEffect.setScale(self.dimensions[1] / 4.0)
                self.openFireEffect.play()
                self.owner.playTextEffect(PLocalizer.CrewBuffOpenFireString)

    def stopRamEffect(self):
        if self.windConeEffect:
            self.windConeEffect.stopLoop()

    def stopRechargeEffect(self):
        if self.powerRechargeEffect:
            self.powerRechargeEffect.stopLoop()

    def stopSpawnEffect(self):
        if self.protectionEffect:
            self.protectionEffect.stopLoop()

    def stopTakeCoverEffect(self):
        if self.takeCoverEffect:
            self.takeCoverEffect.stop()

    def stopOpenFireEffect(self):
        if self.openFireEffect:
            self.openFireEffect.stop()

    def playStormEffect(self):
        if not self.stormEffect:
            self.stormEffect = DarkMaelstrom(self.shipRoot)
            self.stormEffect.setZ(50)
            self.stormEffect.loop()
            compassFX = CompassEffect.make(render)
            self.stormEffect.setEffect(compassFX)

    def stopStormEffect(self):
        if self.stormEffect:
            self.stormEffect.destroy()
            self.stormEffect = None
        return

    def createWake(self):
        if self.owner:
            ownerId = self.owner.doId
        else:
            ownerId = None
        if not base.cr.activeWorld:
            self.notify.warning('Ship %s is trying to create a wake without an active world.' % (ownerId,))
            return
        if not base.cr.activeWorld.getWater():
            self.notify.warning('Ship %s is trying to create a wake without an ocean. (world: %s)' % (ownerId, base.cr.activeWorld))
            return
        if self.WantWake and base.cr.wantSpecialEffects and self.owner:
            self.removeWake()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                if not hasattr(base.cr.activeWorld.getWater(), 'patch'):
                    self.notify.error("Ship %s is in location %s,%s (%s[%s]).\nThis causes Attribute Error: 'NoneType' object has no attribute 'patch'\n" % (ownerId, self.getLocation()[0], self.getLocation()[1], type(self.getParentObj()), safeRepr(self.getParentObj())))
                self.wake = Wake.getEffect()
                if self.wake:
                    self.wake.attachToShip(self.owner)
                    compassFX = CompassEffect.make(render)
                    self.wake.setEffect(compassFX)
                    self.wake.startAnimate(self.owner)
        return

    def removeWake(self):
        if self.wake:
            self.wake.cleanUpEffect()
            self.wake = None
        return

    def hasWake(self):
        return self.wake != None

    def cleanup(self):
        self.sinkingEnd()
        self.modelRoot.clearPythonTag('ship')
        self.breakAnims = {}
        self.metaAnims = {}
        self.lod = None
        self.modelRoot.detachNode()
        self.modelRoot = None
        self.locators = None
        self.center = None
        self.stern = None
        self.bow = None
        self.starboard = None
        self.port = None
        self.removeLandedGrapples()
        self.cleanupCollisions()
        self.char = None
        loader.unloadSfx(self.sinkingSfx1)
        loader.unloadSfx(self.sinkingSfx2)
        self.sinkingSfx1 = None
        self.sinkingSfx2 = None
        self.sinkEffectsRoot = None
        self.sinkEffects = []
        self.owner = None
        self.__rollDownIval.pause()
        self.__rollDownIval = None
        self.__rollUpIval.pause()
        self.__rollUpIval = None
        self.sailStartIval.pause()
        self.sailStartIval = None
        self.sailStopIval.pause()
        self.sailStopIval = None
        for ival in self.__breakIvals.values():
            ival.pause()

        self.__breakIvals = {}
        self.windTunneldEffect1 = None
        self.windTunnelEffect2 = None
        self.windConeEffect = None
        self.powerRechargeEffect = None
        self.protectionEffect = None
        self.takeCoverEffect = None
        self.openFireEffect = None
        self.stopStormEffect()
        self.removeWake()
        self.cleanupDarkFog()
        if self.fader:
            self.fader.pause()
            self.fader = None
        return

    def cleanupCollisions(self):
        self.mastCollisions = None
        self.__targetableCollisions = []
        self.modelCollisions = None
        self.floors = None
        self.deck = None
        self.planeBarriers = None
        self.walls = None
        self.shipCollWall = None
        self.panels = None
        return

    def demandMastStates(self, mastStates, maxHealth):
        for i in range(5):
            if maxHealth[i]:
                if mastStates[i]:
                    self.restoreMast(i)
                else:
                    self.dropMast(i)

    def sinkingBegin(self):
        self.computeDimensions()
        self.disableOnDeckInteractions()
        self.removeWake()
        soundTrack = Sequence()
        sinkingSfx = self.sinkingSfx1
        if self.sfxAlternativeStyle:
            sinkingSfx = self.sinkingSfx2
        if sinkingSfx:
            soundTrack = Sequence(Func(base.playSfx, sinkingSfx, node=self.modelRoot, cutoff=1000))
        self.sinkTrack = Sequence()
        sinkParallel = Parallel()
        if self.isInCrew(localAvatar.doId):
            sinkParallel.append(Func(base.localAvatar.b_setGameState, 'Cutscene', localArgs=[self.owner]))
            sinkParallel.append(self.getSinkCamIval())
        sinkParallel.append(Sequence(Func(self.startSinkEffects), soundTrack, self.getSinkShipIval()))
        self.sinkTrack.append(sinkParallel)
        self.sinkTrack.append(Func(self.endSinkEffects))
        if self.owner.isInCrew(localAvatar.doId):
            self.sinkTrack.append(Func(self.cleanupLocalSinking))
        self.sinkTrack.start()

    def sinkingEnd(self):
        if self.sinkTrack:
            self.sinkTrack.finish()
            self.sinkTrack = None
            self.endSinkEffects()
        return

    def getSinkShipIval(self):
        return Parallel(LerpPosInterval(self.modelRoot, 18.0 * self.sinkTimeScale, Vec3(0, 0, -1.5 * self.dimensions[2])), LerpHprInterval(self.modelRoot, 12.0 * self.sinkTimeScale, VBase3(self.modelRoot.getH(), self.modelRoot.getP() + 75, self.modelRoot.getR())))

    def getSinkCamIval(self):
        camStartPos = Vec3(-4.0 * self.dimensions[0], -1.25 * self.dimensions[1], 40)
        camEndPos = Vec3(-4.0 * self.dimensions[0], self.dimensions[1], self.dimensions[2] / 2.0)
        if self.owner:
            self.owner.lookAtDummy.setPos(0, 0, self.center.getZ())

            def camLookAtDummy(t):
                camera.lookAt(self.owner.lookAtDummy)

            return Parallel(Func(camera.reparentTo, self.owner.attachNewNode('cameraDummy')), LerpPosInterval(camera, 16.0 * self.sinkTimeScale, camEndPos, startPos=camStartPos, blendType='easeInOut'), LerpPosInterval(self.owner.lookAtDummy, 18.0 * self.sinkTimeScale, Vec3(0, 80, 0)), LerpFunc(camLookAtDummy, 18.0 * self.sinkTimeScale))

    def startSinkEffects(self):
        if not self.sinkEffectsRoot:
            self.sinkEffectsRoot = self.shipRoot.attachNewNode('sinkEffectsRoot')
        self.sinkEffectsRoot.setY(self.center.getY())
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
            ripples = WaterWakes.getEffect()
            if ripples:
                scale = self.hullDimensions
                ripples.duration = ripples.duration * self.sinkTimeScale
                ripples.reparentTo(self.sinkEffectsRoot)
                ripples.setScale(scale[0] / 6, scale[1] / 10, scale[2] / 5)
                ripples.play()
                self.sinkEffects.append(ripples)
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
            mist = WaterMist.getEffect()
            if mist:
                mist.sinkTimeScale = self.sinkTimeScale
                mist.reparentTo(self.sinkEffectsRoot)
                mist.setScale(self.hullDimensions / 50.0)
                mist.setEffectScale(1.0)
                mist.setZ(-5.0)
                mist.play()
                self.sinkEffects.append(mist)
        taskMgr.add(self.updateSinkEffects, self.uniqueName('updateSinkEffects'))

    def endSinkEffects(self):
        taskMgr.remove(self.uniqueName('updateSinkEffects'))
        for effect in self.sinkEffects:
            effect.stopLoop()

        self.sinkEffects = []

    def updateSinkEffects(self, task):
        pos = self.modelRoot.getPos(render)
        if base.cr.activeWorld:
            if base.cr.activeWorld.getWater():
                waterHeight = base.cr.activeWorld.getWater().calcHeight(pos[0], pos[1], 0, render)
                self.sinkEffectsRoot.setZ(render, waterHeight)
                self.sinkEffectsRoot.setY(self.sinkEffectsRoot.getY() - 0.15)
            return task.cont
        return task.done

    def cleanupLocalSinking(self):
        base.transitions.fadeOut()
        base.transitions.letterboxOff()
        base.cr.interactionMgr.unlock()
        base.cr.interactionMgr.start()
        base.musicMgr.requestCurMusicFadeOut()

    def undoSinking(self):
        self.modelRoot.setPosHpr(0, 0, 0, 0, 0, 0)
        if self.isSplit:
            self.clipParent1.setPosHpr(0, 0, 0, 0, 0, 0)
            self.clipParent2.setPosHpr(0, 0, 0, 0, 0, 0)

    def splitShip(self):
        if not self.isSplit:
            self.isSplit = True
            self.modelGeom.instanceTo(self.clipParent2)
            planeNode1 = NodePath(PlaneNode('planeNode1', Plane(Vec4(0, 1, 0, 0))))
            planeNode1.reparentTo(self.clipParent1)
            planeNode1.setY(ShipGlobals.getShipSplitOffset(self.shipClass))
            self.clipParent1.setClipPlane(planeNode1)
            planeNode2 = NodePath(PlaneNode('planeNode2', Plane(Vec4(0, -1, 0, 0))))
            planeNode2.reparentTo(self.clipParent2)
            planeNode2.setY(ShipGlobals.getShipSplitOffset(self.shipClass))
            self.clipParent2.setClipPlane(planeNode2)

    def destroy(self):
        self.cleanup()

    def manufactureCannons(self, detailLevel=2):
        stats = ShipGlobals.getShipConfig(self.shipClass)
        cannonConfig = stats['cannons']
        leftConfig = stats['leftBroadsides']
        rightConfig = stats['rightBroadsides']
        cannons = {}
        for i in range(len(cannonConfig)):
            cannonType = cannonConfig[i]
            cannon = Cannon.Cannon(None)
            cannon.loadModel(None, cannonType)
            cannons[i] = [cannon, 0]

        broadsides = [[[], []], None]
        for i in range(len(leftConfig)):
            if leftConfig[i] > 0:
                cannon = CannonPort.CannonPort(leftConfig[i], 0, i)
                broadsides[0][0].append(cannon)
            else:
                broadsides[0][0].append(None)

        for i in range(len(rightConfig)):
            if rightConfig[i] > 0:
                cannon = CannonPort.CannonPort(rightConfig[i], 1, i)
                broadsides[0][1].append(cannon)
            else:
                broadsides[0][1].append(None)

        self.setupCannons(cannons, broadsides, detailLevel)
        return

    def setupCannons(self, cannons, broadsides, detailLevel=2):
        self.cannons = {}
        if detailLevel in (1, 2):
            self.cannonsHigh = self.lod.getChild(0).attachNewNode(ModelNode('cannons'))
            self.cannonsMed = self.lod.getChild(1).attachNewNode(ModelNode('cannons'))
            self.cannonsLow = self.lod.getChild(2).attachNewNode(ModelNode('cannons'))
        else:
            self.cannonsHigh = self.lod.getChild(0).attachNewNode(ModelNode('cannons'))
            self.cannonsMed = self.lod.getChild(1).attachNewNode(ModelNode('cannons'))
        self.cannonColl = self.modelCollisions.attachNewNode('cannons')
        for i in cannons:
            transform = self.locators.find('**/cannon_%s;+s' % i).getTransform(self.locators)
            cannon = cannons[i][0]
            cannon.root.setTransform(transform)
            cannon.root.flattenLight()
            char = cannon.root.node()
            bundle = char.getBundle(0)
            if detailLevel in (1, 2):
                high = cannon.lod.getChild(0)
                med = cannon.lod.getChild(1)
                low = cannon.lod.getChild(2)
                self.char.node().combineWith(char)
                high.reparentTo(self.cannonsHigh)
                med.reparentTo(self.cannonsMed)
                low.reparentTo(self.cannonsLow)
            else:
                low = cannon.lod.getChild(2)
                superlow = cannon.lod.getChild(3)
                self.char.node().combineWith(char)
                low.reparentTo(self.cannonsHigh)
                superlow.reparentTo(self.cannonsMed)
            cannon.propCollisions.setTransform(transform)
            cannon.propCollisions.reparentTo(self.cannonColl)
            cannon.hNode.reparentTo(self.locators.find('**/cannon_%s;+s' % i))
            self.cannons[i] = cannon

        if broadsides:
            broadsideLeft = broadsides[0][0]
            broadsideRight = broadsides[0][1]
            self.broadsides = [broadsideLeft, broadsideRight]
            leftRoot = self.locators.find('**/broadsides_left')
            rightRoot = self.locators.find('**/broadsides_right')
            for broadsideSet, side in zip(broadsides[0], ((leftRoot, 'left'), (rightRoot, 'right'))):
                for i in range(len(broadsideSet)):
                    port = broadsideSet[i]
                    if not port:
                        continue
                    locator = side[0].find('broadside_%s_%s;+s' % (side[1], i))
                    transform = locator.getTransform(self.locators)
                    port.locator = locator
                    port.root.setTransform(transform)
                    port.root.flattenLight()
                    char = port.root.node()
                    bundle = char.getBundle(0)
                    if detailLevel in (1, 2):
                        high = port.lod.getChild(0)
                        med = port.lod.getChild(1)
                        low = port.lod.getChild(2)
                        self.char.node().combineWith(char)
                        high.reparentTo(self.cannonsHigh)
                        med.reparentTo(self.cannonsMed)
                        low.reparentTo(self.cannonsLow)
                    else:
                        geom = port.lod.getChild(2)
                        self.char.node().combineWith(char)
                        geom.copyTo(self.cannonsHigh)
                        geom.copyTo(self.cannonsMed)

        else:
            self.broadsides = []
        self.cannonsHigh.flattenStrong()
        self.cannonsMed.flattenStrong()
        if detailLevel != 0:
            self.cannonsLow.flattenStrong()
        for cannon in self.cannons.values():
            cannon.finalize()

        for side in self.broadsides:
            for port in side:
                if port:
                    port.finalize()

    def updateDamageEffects(self, health, rear, left, right):
        effectSettings = base.options.getSpecialEffectsSetting()
        if left <= 30.0:
            locator = self.locators.find('**/location_fire_1')
            scale = locator.getScale()[0] / 1.75 + locator.getScale()[0] / 2.0 * (1.0 - health / 100.0)
            if not self.leftSideFire:
                self.leftSideFire = ShipFire.getEffect()
                if self.leftSideFire:
                    self.leftSideFire.reparentTo(self.modelRoot)
                    self.leftSideFire.setPos(locator.getPos())
                    self.leftSideFire.setHpr(80, -15, 0)
                    self.leftSideFire.startLoop()
            if self.leftSideFire:
                self.leftSideFire.setEffectScale(scale)
            if not self.leftSideSmoke and effectSettings >= base.options.SpecialEffectsMedium:
                self.leftSideSmoke = ShipSmoke.getEffect()
                if self.leftSideSmoke:
                    self.leftSideSmoke.reparentTo(self.modelRoot)
                    self.leftSideSmoke.setPos(locator.getPos())
                    self.leftSideSmoke.setHpr(90, -15, 0)
                    self.leftSideSmoke.startLoop()
            if self.leftSideSmoke:
                self.leftSideSmoke.setEffectScale(scale)
        else:
            if self.leftSideFire:
                self.leftSideFire.stopLoop()
                self.leftSideFire = None
            if self.leftSideSmoke:
                self.leftSideSmoke.stopLoop()
                self.leftSideSmoke = None
        if left <= 0.0 and effectSettings >= base.options.SpecialEffectsMedium:
            locator = self.locators.find('**/location_fire_3')
            if locator:
                scale = locator.getScale()[0] / 1.75 + locator.getScale()[0] / 2.0 * (1.0 - health / 100.0)
            if locator and not self.leftSideFire2:
                self.leftSideFire2 = ShipFire.getEffect()
                if self.leftSideFire2:
                    self.leftSideFire2.reparentTo(self.modelRoot)
                    self.leftSideFire2.setPos(locator.getPos())
                    self.leftSideFire2.setHpr(90, -10, 10)
                    self.leftSideFire2.startLoop()
            if self.leftSideFire2:
                self.leftSideFire2.setEffectScale(scale)
            if locator and not self.leftSideSmoke2:
                self.leftSideSmoke2 = ShipSmoke.getEffect()
                if self.leftSideSmoke2:
                    self.leftSideSmoke2.reparentTo(self.modelRoot)
                    self.leftSideSmoke2.setPos(locator.getPos())
                    self.leftSideSmoke2.setHpr(90, -15, 0)
                    self.leftSideSmoke2.startLoop()
            if self.leftSideSmoke2:
                self.leftSideSmoke2.setEffectScale(scale)
        else:
            if self.leftSideFire2:
                self.leftSideFire2.stopLoop()
                self.leftSideFire2 = None
            if self.leftSideSmoke2:
                self.leftSideSmoke2.stopLoop()
                self.leftSideSmoke2 = None
        if right <= 30.0:
            locator = self.locators.find('**/location_fire_2')
            scale = locator.getScale()[0] / 1.75 + locator.getScale()[0] / 2.0 * (1.0 - health / 100.0)
            if not self.rightSideFire:
                self.rightSideFire = ShipFire.getEffect()
                if self.rightSideFire:
                    self.rightSideFire.reparentTo(self.modelRoot)
                    self.rightSideFire.setPos(locator.getPos())
                    self.rightSideFire.setHpr(100, 15, 0)
                    self.rightSideFire.startLoop()
            if self.rightSideFire:
                self.rightSideFire.setEffectScale(scale)
            if not self.rightSideSmoke and effectSettings >= base.options.SpecialEffectsMedium:
                self.rightSideSmoke = ShipSmoke.getEffect()
                if self.rightSideSmoke:
                    self.rightSideSmoke.reparentTo(self.modelRoot)
                    self.rightSideSmoke.setPos(locator.getPos())
                    self.rightSideSmoke.setHpr(90, 15, 0)
                    self.rightSideSmoke.startLoop()
            if self.rightSideSmoke:
                self.rightSideSmoke.setEffectScale(scale)
        else:
            if self.rightSideFire:
                self.rightSideFire.stopLoop()
                self.rightSideFire = None
            if self.rightSideSmoke:
                self.rightSideSmoke.stopLoop()
                self.rightSideSmoke = None
        if right <= 0.0 and effectSettings >= base.options.SpecialEffectsMedium:
            locator = self.locators.find('**/location_fire_4')
            if locator:
                scale = locator.getScale()[0] / 1.75 + locator.getScale()[0] / 2.0 * (1.0 - health / 100.0)
            if locator and not self.rightSideFire2:
                self.rightSideFire2 = ShipFire.getEffect()
                if self.rightSideFire2:
                    self.rightSideFire2.reparentTo(self.modelRoot)
                    self.rightSideFire2.setPos(locator.getPos())
                    self.rightSideFire2.setHpr(90, 10, 10)
                    self.rightSideFire2.startLoop()
            if self.rightSideFire2:
                self.rightSideFire2.setEffectScale(scale)
            if locator and not self.rightSideSmoke2:
                self.rightSideSmoke2 = ShipSmoke.getEffect()
                if self.rightSideSmoke2:
                    self.rightSideSmoke2.reparentTo(self.modelRoot)
                    self.rightSideSmoke2.setPos(locator.getPos())
                    self.rightSideSmoke2.setHpr(90, 15, 0)
                    self.rightSideSmoke2.startLoop()
            if self.rightSideSmoke2:
                self.rightSideSmoke2.setEffectScale(scale)
        else:
            if self.rightSideFire2:
                self.rightSideFire2.stopLoop()
                self.rightSideFire2 = None
            if self.rightSideSmoke2:
                self.rightSideSmoke2.stopLoop()
                self.rightSideSmoke2 = None
        if rear <= 30.0:
            locator = self.locators.findAllMatches('**/location_fire_0')[0]
            scale = locator.getScale()[0] / 1.75 + locator.getScale()[0] / 2.0 * (1.0 - health / 100.0)
            if not self.rearSideFire:
                self.rearSideFire = ShipFire.getEffect()
                if self.rearSideFire:
                    self.rearSideFire.reparentTo(self.modelRoot)
                    self.rearSideFire.setPos(locator.getPos())
                    self.rearSideFire.setHpr(0, 20, 0)
                    self.rearSideFire.startLoop()
            if self.rearSideFire:
                self.rearSideFire.setEffectScale(scale)
            if not self.rearSideSmoke and effectSettings >= base.options.SpecialEffectsMedium:
                self.rearSideSmoke = ShipSmoke.getEffect()
                if self.rearSideSmoke:
                    self.rearSideSmoke.reparentTo(self.modelRoot)
                    self.rearSideSmoke.setPos(locator.getPos())
                    self.rearSideSmoke.setHpr(0, 20, 0)
                    self.rearSideSmoke.startLoop()
            if self.rearSideSmoke:
                self.rearSideSmoke.setEffectScale(scale)
        else:
            if self.rearSideFire:
                self.rearSideFire.stopLoop()
                self.rearSideFire = None
            if self.rearSideSmoke:
                self.rearSideSmoke.stopLoop()
                self.rearSideSmoke = None
        return

    def cleanUpDamageEffects(self):
        if self.leftSideFire:
            self.leftSideFire.cleanUpEffect()
            self.leftSideFire = None
        if self.leftSideSmoke:
            self.leftSideSmoke.cleanUpEffect()
            self.leftSideSmoke = None
        if self.leftSideFire2:
            self.leftSideFire2.cleanUpEffect()
            self.leftSideFire2 = None
        if self.leftSideSmoke2:
            self.leftSideSmoke2.cleanUpEffect()
            self.leftSideSmoke2 = None
        if self.rightSideFire:
            self.rightSideFire.cleanUpEffect()
            self.rightSideFire = None
        if self.rightSideSmoke:
            self.rightSideSmoke.cleanUpEffect()
            self.rightSideSmoke = None
        if self.rightSideFire2:
            self.rightSideFire2.cleanUpEffect()
            self.rightSideFire2 = None
        if self.rightSideSmoke2:
            self.rightSideSmoke2.cleanUpEffect()
            self.rightSideSmoke2 = None
        if self.rearSideFire:
            self.rearSideFire.cleanUpEffect()
            self.rearSideFire = None
        if self.rearSideSmoke:
            self.rearSideSmoke.cleanUpEffect()
            self.rearSideSmoke = None
        return

    def startDarkFog(self, offset=None):
        self.fogEffect = DarkShipFog.getEffect()
        if self.fogEffect:
            self.fogEffect.reparentTo(self.shipRoot)
            if offset:
                self.fogEffect.setY(self.fogEffect, offset)
            self.fogEffect.setZ(self.fogEffect, 50)
            self.fogEffect.startLoop()

    def stopDarkFog(self):
        if self.fogEffect:
            self.fogEffect.stopLoop()
            self.fogEffect = None
        return

    def cleanupDarkFog(self):
        if self.fogEffect:
            self.fogEffect.destroy()
            self.fogEffect = None
        return

    def fadeIn(self, duration=2.0):
        if self.fader:
            self.fader.finish()
            self.fader = None
        self.modelRoot.setTransparency(1)
        self.fader = Sequence(self.modelRoot.colorScaleInterval(duration, Vec4(1, 1, 1, 1), startColorScale=Vec4(0, 0, 0, 0)), Func(self.modelRoot.clearTransparency))
        self.fader.start()
        return

    def fadeOut(self, duration=2.0):
        if self.fader:
            self.fader.finish()
            self.fader = None
        self.modelRoot.setTransparency(1)
        self.fader = Sequence(self.modelRoot.colorScaleInterval(duration / 2.0, Vec4(0, 0, 0, 0), startColorScale=Vec4(1, 1, 1, 1)), Func(self.modelRoot.clearTransparency))
        self.fader.start()
        return

    def enableSails(self):
        self.sailCollisions.unstash()

    def disableSails(self):
        self.sailCollisions.stash()

    def forceLOD(self, index):
        self.lod.node().forceSwitch(index)

    def clearForceLOD(self):
        self.lod.node().clearForceSwitch()

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='shipboard')
    def getRope(self, thickness=0.15):
        rope = Rope()
        rope.ropeNode.setRenderMode(RopeNode.RMTube)
        rope.ropeNode.setNumSlices(10)
        rope.ropeNode.setUvMode(RopeNode.UVDistance)
        rope.ropeNode.setUvDirection(1)
        rope.ropeNode.setUvScale(0.25)
        rope.ropeNode.setThickness(thickness)
        ropePile = loader.loadModel('models/char/rope_high')
        ropeTex = ropePile.findTexture('rope_single_omit')
        ropePile.removeNode()
        rope.setTexture(ropeTex)
        rope.setLightOff()
        rope.setColorScale(0.5, 0.5, 0.5, 1)
        return rope

    def setLandedGrapples(self, ship, landedGrapples):
        for grapple in landedGrapples:
            if grapple not in self.landedGrapples:
                self.createLandedGrapple(ship, grapple[1])

        self.landedGrapples = landedGrapples
        self.startAnimateLandedGrappleTask()

    def createLandedGrapple(self, otherShip, targetId):
        self.accept(otherShip.getDisableEvent(), self.removeLandedGrapples)
        otherShipRelX = otherShip.model.modelRoot.getX(self.modelRoot)
        grappleStr = '**/grapple_right*'
        anchorOffset = Vec3(0, 0, -1)
        if otherShipRelX < 0:
            grappleStr = '**/grapple_left*'
        anchorNode = random.choice(self.locators.findAllMatches(grappleStr))
        anchorPos = anchorNode.getPos(self.modelRoot) + anchorOffset
        side = 'right'
        if self.modelRoot.getX(otherShip.model.modelRoot) < 0:
            side = 'left'
        targetStr = '**/grapple_%s_%s' % (side, targetId)
        if targetId >= 0:
            grappleLocator = otherShip.findLocator(targetStr)
        else:
            grappleLocator = random.choice(otherShip.findLocators('**/grapple_%s_*' % (side,)))
        rope = self.getRope(thickness=0.5)
        grapplePos = grappleLocator.getPos(self.modelRoot)
        sagNode = self.modelRoot.attachNewNode('sagNode')
        sagNode.setPos((grapplePos + anchorPos) * 0.5)
        grapple = loader.loadModel('models/ammunition/GrapplingHook')
        grapple.reparentTo(otherShip.model.modelRoot)
        posHpr = (
         grappleLocator, 2, 0, -2.5, -270, -350, 80)
        if targetStr.find('right') > 0:
            posHpr = (
             grappleLocator, 1, 0, -1.5, 90, -40, -180)
        grapple.setPosHpr(*posHpr)
        rope.reparentTo(grapple)
        rope.setup(3, ((None, Point3(0)), (sagNode, Point3(0)), (self.modelRoot, anchorPos)))
        self.landedGrappleNodes.append([otherShip, grapple, anchorNode, sagNode, grappleLocator, rope])
        return

    def removeLandedGrapples(self):
        self.stopAnimateLandedGrappleTask()
        for ship, grapple, anchorNode, sagNode, grappleLocator, rope in self.landedGrappleNodes:
            self.ignore(ship.getDisableEvent())
            grapple.removeNode()
            sagNode.removeNode()
            rope.removeNode()

        self.landedGrappleNodes = []
        self.landedGrapples = []

    def startAnimateLandedGrappleTask(self):
        self.stopAnimateLandedGrappleTask()
        taskMgr.add(self.animateLandedGrappleTask, self.uniqueName('animateGrapple'))

    def animateLandedGrappleTask(self, task):
        ship = None
        for ship, grapple, anchorNode, sagNode, grappleLocator, rope in self.landedGrappleNodes:
            grapplePos = grappleLocator.getPos(self.modelRoot)
            anchorPos = anchorNode.getPos(self.modelRoot)
            sagPos = (grapplePos + anchorPos) * 0.5
            sagNode.setPos(sagPos)

        return task.cont

    def stopAnimateLandedGrappleTask(self):
        taskMgr.remove(self.uniqueName('animateGrapple'))