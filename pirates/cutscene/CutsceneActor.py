from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor.Actor import Actor
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import ScratchPad
from direct.task import Task
from pirates.leveleditor import NPCList
from pirates.pirate.Human import Human
from pirates.pirate.Pirate import Pirate
from pirates.pirate.HumanDNA import HumanDNA
from pirates.npc.Cast import JollyRoger
from pirates.npc.Cast import JackSparrow
from pirates.npc.Cast import WillTurner
from pirates.npc.Cast import ElizabethSwan
from pirates.npc.Cast import CaptBarbossa
from pirates.npc.Cast import TiaDalma
from pirates.npc.Cast import JoshGibbs
from pirates.npc.Skeleton import Skeleton
from pirates.shipparts import CannonDNA
from pirates.ship import ShipGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.effects.SpectralSmoke import SpectralSmoke
from pirates.effects.VoodooAura import VoodooAura
from pirates.effects.JollySoulDrain import JollySoulDrain
from pirates.effects.VoodooFire import VoodooFire
from pirates.effects.JRTeleportEffect import JRTeleportEffect
from pirates.effects.ShipSinkSplashes import ShipSinkSplashes
from pirates.effects.Explosion import Explosion
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle import Cannon
from pirates.effects.JRSpawn import JRSpawn
from pirates.effects.DarkPortal import DarkPortal
from pirates.effects.WaterSplashes import WaterSplashes
from pirates.effects.WaterWakes import WaterWakes
from pirates.effects.WaterMist import WaterMist
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import random

class CutsceneActor():
    notify = directNotify.newCategory('CutsceneActor')

    def __init__(self, cutsceneDesc):
        self._cutsceneName = cutsceneDesc.filename
        self._csComponents = cutsceneDesc.components
        self.animFileNames = []
        self.effect = None
        self.fader = None
        self.effectDummy = None
        if self.Uid:
            self.handleModelHiding()
        return

    def handleModelHiding(self):
        self.modelLoaded = None
        if 'localAvatar' in __builtins__:
            base.cr.uidMgr.addUidCallback(self.Uid, self.foundIt, timeout=0)
        if self.modelLoaded:
            self.modelLoaded.stash()
        return

    def foundIt(self, npc):
        if npc == None:
            self.notify.debug('Movie cast not created yet')
        elif not base.cr.doId2do.has_key(npc):
            self.notify.debug('Movie cast not in doId2do')
        else:
            self.modelLoaded = base.cr.doId2do[npc]
            if self.modelLoaded.isDeleted():
                self.notify.debug('Warning:Cast Deleted Already')
                self.modelLoaded = None
        return

    def destroy(self):
        if self.fader:
            self.fader.finish()
            self.fader = None
        for animName in self.animFileNames:
            self.notify.debug('unloading cs anim file: %s' % animName)
            loader.unloadModel(animName)

        del self._cutsceneName
        del self._csComponents
        if self.Uid and self.modelLoaded and not self.modelLoaded.isEmpty():
            self.modelLoaded.unstash()
        return

    @staticmethod
    def getActorKey(actorName):
        self.notify.error('derived must implement')

    def getThisActorKey(self):
        return self.getActorKey()

    def getCSAnimNames(self):
        names = []
        for component in self._csComponents:
            names.append(self._cutsceneName + component)

        return names

    def getInterval(self, duration=None):
        ival = Sequence()
        for animName in self.getCSAnimNames():
            if animName == self.getCSAnimNames()[len(self.getCSAnimNames()) - 1]:
                ival.append(self.actorInterval(animName, duration=duration))
            else:
                ival.append(self.actorInterval(animName))

        return ival

    def startCutscene(self, locators):
        self.reparentTo(locators.origin)
        self.clearMat()
        if 'localAvatar' in __builtins__:
            characterDetailLevel = base.options.getCharacterDetailSetting()
        else:
            characterDetailLevel = 2
        if characterDetailLevel != 2:
            characterDetailLevel = 1
        if self.node() != NotImplemented:
            self.node().setBounds(OmniBoundingVolume())
            self.node().setFinal(1)
            lodNode = self.find('**/+LODNode')
            LODMapping = {2: 0,1: 1,0: 2}
            if not lodNode.isEmpty():
                lodNode.node().forceSwitch(LODMapping[characterDetailLevel])

    def finishCutscene(self):
        if self.node() != NotImplemented:
            self.node().clearBounds()
            self.node().setFinal(0)
            lodNode = self.find('**/+LODNode')
            if not lodNode.isEmpty():
                lodNode.node().clearForceSwitch()
        self.detachNode()

    def fadeIn(self, time):
        if self.fader:
            self.fader.finish()
            self.fader = None
        self.setTransparency(1, 1)
        self.setAlphaScale(0.0)
        self.show()
        self.fader = Sequence(LerpFunctionInterval(self.setAlphaScale, time, fromData=0.0, toData=1.0), Func(self.clearTransparency))
        self.fader.start()
        return

    def fadeOut(self, time):
        if self.fader:
            self.fader.finish()
            self.fader = None
        self.setTransparency(1, 1)
        self.fader = Sequence(LerpFunctionInterval(self.setAlphaScale, time, fromData=1.0, toData=0.0), Func(self.hide), Func(self.clearTransparency))
        self.fader.start()
        return

    def fadeInBlack(self, time):
        if self.fader:
            self.fader.finish()
            self.fader = None
        self.setTransparency(1)
        self.show()
        self.fader = Sequence(self.colorScaleInterval(time / 2.0, Vec4(0, 0, 0, 1), startColorScale=Vec4(0, 0, 0, 0)), self.colorScaleInterval(time / 2.0, Vec4(1, 1, 1, 1), startColorScale=Vec4(0, 0, 0, 1)), Func(self.clearTransparency))
        self.fader.start()
        return

    def fadeOutBlack(self, time):
        if self.fader:
            self.fader.finish()
            self.fader = None
        self.setTransparency(1)
        self.fader = Sequence(self.colorScaleInterval(time / 2.0, Vec4(0, 0, 0, 1), startColorScale=Vec4(1, 1, 1, 1)), self.colorScaleInterval(time / 2.0, Vec4(0, 0, 0, 0), startColorScale=Vec4(0, 0, 0, 1)), Func(self.clearTransparency), Func(self.hide))
        self.fader.start()
        return


class CutsceneShadowCaster(CutsceneActor):

    def initShadow(self):
        self.initializeDropShadow()
        self.setActiveShadow(1)

    def cleanupShadow(self):
        self.deleteDropShadow()


class CutCam(CutsceneActor, Actor):

    def __init__(self, cutsceneDesc):
        self.Uid = None
        Actor.__init__(self, allowAsyncBind=False)
        CutsceneActor.__init__(self, cutsceneDesc)
        self.filmSizeHorizontal = cutsceneDesc.filmSizeHorizontal
        self.focalLength = cutsceneDesc.focalLength
        self.loadModel('models/char/cutcam_dummy')
        for animName in self.getCSAnimNames():
            animFileName = 'models/char/cutcam_%s' % animName
            self.animFileNames.append(animFileName)
            self.loadAnims({animName: animFileName})
            self.getAnimControls(animName, allowAsyncBind=False)

        geomNode = self.find('**/+GeomNode')
        if geomNode.isEmpty():
            self.notify.error('could not find cutcam geom node')
        geomNode.stash()
        return

    def destroy(self):
        CutsceneActor.destroy(self)
        Actor.delete(self)

    @staticmethod
    def getActorKey():
        return 'CutCam'

    def _getCutCamTaskName(self):
        return '%s-cutCam-update' % self._cutsceneName

    def startCutscene(self, locators):
        CutsceneActor.startCutscene(self, locators)
        self.oldParams = ScratchPad()
        self.oldParams.nearPlaneDist = base.camLens.getNear()
        self.oldParams.camParent = camera.getParent()
        self.oldParams.FOV = base.camLens.getFov()
        self.oldParams.filmSizeHorizontal = base.camLens.getFilmSize()[0]
        self.oldParams.focalLength = base.camLens.getFocalLength()
        base.camLens.setNear(0.3)
        base.camLens.setFilmSize(self.filmSizeHorizontal)
        base.camLens.setFocalLength(self.focalLength)
        parentNode = self.find('**/cutcam')
        if parentNode.isEmpty():
            self.notify.error('could not find cutcam node')
        self._parentNode = parentNode
        if 'localAvatar' in __builtins__:
            self.oldParams.state = base.localAvatar.cameraFSM.state
            base.localAvatar.cameraFSM.request('Control')
        base.camLens.setNear(0.3)
        base.camLens.setFilmSize(self.filmSizeHorizontal)
        base.camLens.setFocalLength(self.focalLength)
        camera.reparentTo(self._parentNode)
        camera.setPosHprScale(0, 0, 0, 0, 0, 0, 1, 1, 1)
        taskMgr.add(self._updateCamTask, self._getCutCamTaskName())

    def _updateCamTask(self, task):
        self.update()
        return Task.cont

    def finishCutscene(self):
        globalClock.setMode(ClockObject.MNormal)
        taskMgr.remove(self._getCutCamTaskName())
        if hasattr(self, '_parentNode'):
            del self._parentNode
        if 'localAvatar' not in __builtins__:
            camera.reparentTo(self.oldParams.camParent)
        elif self.oldParams.state == 'Cannon':
            base.localAvatar.cameraFSM.request('FPS')
        else:
            base.localAvatar.cameraFSM.request(self.oldParams.state)
        base.camLens.setNear(self.oldParams.nearPlaneDist)
        base.camLens.setFilmSize(self.oldParams.filmSizeHorizontal)
        base.camLens.setFocalLength(self.oldParams.focalLength)
        del self.oldParams
        CutsceneActor.finishCutscene(self)
        camera.setScale(1)

    def changeCameraParams(self, filmSize, focalLength):
        if filmSize:
            base.camLens.setFilmSize(filmSize)
        if focalLength:
            base.camLens.setFocalLength(focalLength)


class CutGenericActor(CutsceneActor, Actor):

    def __init__(self, actorName, modelName, path, cutsceneDesc):
        self.Uid = None
        CutsceneActor.__init__(self, cutsceneDesc)
        Actor.__init__(self, allowAsyncBind=False)
        self.actorName = actorName
        self.loadModel('%s%s' % (path, modelName))
        for animName in self.getCSAnimNames():
            animFileName = '%s%s_%s' % (path, actorName, animName)
            self.animFileNames.append(animFileName)
            self.loadAnims({animName: animFileName})
            self.getAnimControls(animName, allowAsyncBind=False)

        return

    def destroy(self):
        CutsceneActor.destroy(self)
        Actor.delete(self)

    @staticmethod
    def getActorKey(actorName):
        return 'GenericActor-%s' % actorName

    def getThisActorKey(self):
        return CutGenericActor.getActorKey(self.actorName)

    def loadEffects(self, cutscene):
        self.effect = None
        if cutscene.envEffects:
            effect = cutscene.envEffects.loadSingleEffect(self)
            if effect:
                effect.startLoop()
                effect.reparentTo(self.find('**/candle_effect_01'))
                self.effect = effect
        return

    def unloadEffects(self):
        if self.effect:
            self.effect.destroy()
            self.effect = None
        return


class CutLocators(CutGenericActor):

    def __init__(self, cutsceneDesc):
        CutGenericActor.__init__(self, 'cs', 'cs_dummy', 'models/char/', cutsceneDesc)
        self._locators = {'ghostShip': self.find('**/locator_ship_ghostship'),'interceptor': self.find('**/locator_ship_interceptor'),'warship': self.find('**/locator_ship_interceptor'),'blackpearl': self.find('**/locator_ship_ghostship')}
        for name, node in self._locators.items():
            pass

        geomNode = self.find('**/+GeomNode')
        if geomNode.isEmpty():
            self.notify.error('could not find cut locator geom node')
        geomNode.stash()

    def setOrigin(self, origin):
        self.origin = origin

    def __getitem__(self, name):
        return self._locators[name]

    def destroy(self):
        for name, node in self._locators.items():
            node.removeNode()

        del self._locators
        del self.origin
        CutGenericActor.destroy(self)

    @staticmethod
    def getActorKey():
        return 'Locators'


class CutShip(CutsceneActor):
    Class2Locator = {ShipGlobals.STUMPY_SHIP: 'interceptor',ShipGlobals.SKEL_DEATH_OMEN: 'ghostShip',ShipGlobals.GOLIATH: 'warship',ShipGlobals.BLACK_PEARL: 'blackpearl'}

    def __init__(self, shipClass, style, cutsceneDesc):
        self.Uid = None
        self._shipClass = shipClass
        CutsceneActor.__init__(self, cutsceneDesc)
        self.ship = base.shipFactory.getShip(shipClass, style, 0, wantWheel=shipClass != ShipGlobals.STUMPY_SHIP)
        self.ship.modelRoot.setH(180)
        self.cannons = {}
        self.masts = {}
        for bundle in self.ship.char.node().getBundles():
            mast = bundle.findChild('def_mast_base')
            if mast:
                self.masts[mast] = TransformState.makeMat(mast.getDefaultValue())

        self.cannonSfx = (
         loadSfx(SoundGlobals.SFX_WEAPON_CANNON_FIRE_01), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_FIRE_02), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_FIRE_03), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_FIRE_04))
        return

    def destroy(self):
        self.ship.destroy()
        CutsceneActor.destroy(self)

    @classmethod
    def getActorKey(cls, shipClass):
        return 'CutShip-%s' % cls.Class2Locator[shipClass]

    def getThisActorKey(self):
        return CutShip.getActorKey(self._shipClass)

    def startCutscene(self, locators):
        locatorName = self.Class2Locator[self._shipClass]
        locator = locators[locatorName]
        self.ship.setOwner(locator, ownerIsModelRoot=True)

    def finishCutscene(self):
        pass

    def getInterval(self, duration=None):
        return WaitInterval(0.001)

    def hideMasts(self):
        ts = TransformState.makeScale(Vec3(0.0001, 0.0001, 0.0001))
        for mast in self.masts:
            mast.applyFreeze(ts)

        self.ship.char.node().forceUpdate()

    def showMasts(self):
        for mast in self.masts:
            mast.applyFreeze(self.masts.get(mast))

        self.ship.char.node().forceUpdate()

    def explosionVFX(self, node=None, offset=Vec3(0, 0, 0)):
        explosion = None
        if 'localAvatar' in __builtins__:
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                explosion = Explosion.getEffect()
        if explosion:
            pos = node.getPos(render) + offset
            explosion.reparentTo(render)
            explosion.setEffectScale(0.2)
            explosion.setEffectRadius(4.0)
            explosion.setPos(pos)
            explosion.play()
        return

    def buildCannons(self):
        cannonLocators = self.ship.locators.findAllMatches('**/cannon_*;+s')
        for i in xrange(len(cannonLocators)):
            cannon = Cannon.Cannon(base.cr)
            cannon.loadModel(CannonDNA.CannonDNA())
            self.cannons[i] = [cannon, None]

        self.ship.setupCannons(self.cannons, None)
        return

    def fireCannon(self, index, ammo=InventoryType.CannonRoundShot, targetPos=None, targetNode=None, wantCollisions=0, flightTime=None, preciseHit=False, offset=Vec3(0, 0, 0)):
        if targetNode:
            targetPos = targetNode.getPos(render)
        targetPos = targetPos + offset
        if len(self.cannons):
            self.cannons[index][0].playAttack(InventoryType.CannonShoot, ammo, 'localShipHit', targetPos, wantCollisions, flightTime, preciseHit)
        sfx = random.choice(self.cannonSfx)
        base.playSfx(sfx)


class CutJackSparrow(CutsceneActor, JackSparrow):

    def __init__(self, cutsceneDesc):
        self.Uid = None
        JackSparrow.__init__(self)
        CutsceneActor.__init__(self, cutsceneDesc)
        for animName in self.getCSAnimNames():
            animFileName = 'models/char/js_%s' % animName
            self.animFileNames.append(animFileName)
            self.loadAnims({animName: animFileName})
            self.getAnimControls(animName, allowAsyncBind=False)

        return

    def destroy(self):
        if self.effect:
            self.effect.finish()
            self.effect = None
        if self.fader:
            self.fader.finish()
            self.fader = None
        CutsceneActor.destroy(self)
        JackSparrow.delete(self)
        return

    @staticmethod
    def getActorKey():
        return 'JackSparrow'

    def attachHandheld(self, handheld, bRightHand):
        if handheld.isEmpty():
            return
        if bRightHand:
            handNode = self.find('**/*weapon_right')
        else:
            handNode = self.find('**/*weapon_left')
        handheld.reparentTo(handNode)

    def detachHandheld(self, handheld, remove=False):
        if handheld.isEmpty():
            return
        handheld.detachNode()
        if remove:
            handheld.removeNode()

    def keepDOHidden(self):
        self.Uid = None
        return


class CutJollyRoger(CutsceneActor, JollyRoger):

    def __init__(self, cutsceneDesc):
        self.Uid = None
        JollyRoger.__init__(self)
        CutsceneActor.__init__(self, cutsceneDesc)
        for animName in self.getCSAnimNames():
            animFileName = 'models/char/jr_%s' % animName
            self.animFileNames.append(animFileName)
            self.loadAnims({animName: animFileName})
            self.getAnimControls(animName, allowAsyncBind=False)

        self.attuneEffect = None
        self.darkEffects = []
        self.setTransparency(1)
        return

    def destroy(self):
        if self.effect:
            self.effect.finish()
            self.effect = None
        if self.attuneEffect:
            self.attuneEffect.finish()
            self.attuneEffect = None
        for effect in self.darkEffects:
            if effect:
                effect.finish()

        self.darkEffects = []
        CutsceneActor.destroy(self)
        JollyRoger.delete(self)
        return

    def startTeleportEffect(self, offset=None):
        joint = self.find('**/def_root')
        if not joint.isEmpty():
            self.effectDummy = joint.attachNewNode('effectDummy')
        self.effect = JRTeleportEffect.getEffect()
        if self.effect and self.effectDummy:
            if not offset:
                offset = 0.0
            posIval = LerpPosInterval(self.effectDummy, 2.0, Vec3(self.effectDummy.getX(), self.effectDummy.getY() + offset / 3.0, self.effectDummy.getZ() + 5.5), startPos=Vec3(self.effectDummy.getX() + offset, self.effectDummy.getY() + offset, self.effectDummy.getZ() - 3.0))
            self.effect.reparentTo(self.effectDummy)
            self.effect.duration = 1.5
            self.effect.effectScale = 1.0
            self.effect.radius = 1.25
            Sequence(Func(self.effect.play), posIval).start()

    def spawnSkeletons(self, cutscene):
        jr1 = cutscene.getActor('Skeleton-2')
        jr1.unstash()
        jr1.fadeIn(1.5)
        jr2 = cutscene.getActor('Skeleton-3')
        jr2.unstash()
        jr2.fadeIn(1.5)
        spawnEffect = JRSpawn.getEffect()
        if spawnEffect:
            spawnEffect.reparentTo(render)
            spawnEffect.setPos(jr1.find('**/dx_root').getPos(render))
            spawnEffect.setZ(spawnEffect.getZ(render) - 1.2)
            spawnEffect.setScale(0.75)
            spawnEffect.play()
        spawnEffect = JRSpawn.getEffect()
        if spawnEffect:
            spawnEffect.reparentTo(render)
            spawnEffect.setPos(jr2.find('**/dx_root').getPos(render))
            spawnEffect.setZ(spawnEffect.getZ(render) - 1.2)
            spawnEffect.setScale(0.75)
            spawnEffect.play()

    def startAttuneEffect(self):
        joint = self.find('**/weapon_left')
        self.leftHandNode = NodePath('leftHand')
        self.leftHandNode.reparentTo(joint)
        self.attuneEffect = VoodooAura.getEffect()
        if self.attuneEffect:
            self.attuneEffect.reparentTo(self.leftHandNode)
            self.attuneEffect.setEffectColor(Vec4(0.2, 0.1, 0.4, 1))
            self.attuneEffect.setPos(0, 0, 0)
            self.attuneEffect.particleDummy.reparentTo(self.leftHandNode)
            self.attuneEffect.startLoop()

    def startSoulSuckEffect(self):
        joint2 = self.find('**/p_1_2')
        joint3 = self.find('**/p_1_3')
        joint4 = self.find('**/p_1_4')
        joint5 = self.find('**/p_1_5')
        joint6 = self.find('**/p_1_6')
        joint7 = self.find('**/p_1_7')
        joint8 = self.find('**/p_1_8')
        joint9 = self.find('**/p_1_9')
        joint11 = self.find('**/p_1_11')
        effect = JollySoulDrain.getEffect()
        if effect:
            effect.reparentTo(joint3)
            effect.setPos(0, 0, 0)
            effect.particleDummy.reparentTo(render)
            effect.startLoop()
            self.darkEffects.append(effect)
        effect = JollySoulDrain.getEffect()
        if effect:
            effect.reparentTo(joint5)
            effect.setPos(0, 0, 0)
            effect.particleDummy.reparentTo(render)
            effect.startLoop()
            self.darkEffects.append(effect)
        effect = JollySoulDrain.getEffect()
        if effect:
            effect.reparentTo(joint7)
            effect.setPos(0, 0, 0)
            effect.particleDummy.reparentTo(render)
            effect.startLoop()
            self.darkEffects.append(effect)
        effect = JollySoulDrain.getEffect()
        if effect:
            effect.reparentTo(joint9)
            effect.setPos(0, 0, 0)
            effect.particleDummy.reparentTo(render)
            effect.startLoop()
            self.darkEffects.append(effect)
        effect = JollySoulDrain.getEffect()
        if effect:
            effect.reparentTo(joint11)
            effect.setPos(0, 0, 0)
            effect.particleDummy.reparentTo(render)
            effect.startLoop()
            self.darkEffects.append(effect)

    def stopSoulSuckEffect(self):
        if self.attuneEffect:
            self.attuneEffect.stopLoop()
            self.attuneEffect = None
        for effect in self.darkEffects:
            if effect:
                effect.stopLoop()

        self.darkEffects = []
        self.leftHandNode.removeNode()
        return

    @staticmethod
    def getActorKey():
        return 'JollyRoger'


class CutWillTurner(CutsceneActor, WillTurner):

    def __init__(self, Uid, cutsceneDesc):
        self.Uid = Uid
        WillTurner.__init__(self)
        CutsceneActor.__init__(self, cutsceneDesc)
        for animName in self.getCSAnimNames():
            animFileName = 'models/char/wt_%s' % animName
            self.animFileNames.append(animFileName)
            self.loadAnims({animName: animFileName})
            self.getAnimControls(animName, allowAsyncBind=False)

    def destroy(self):
        if self.effect:
            self.effect.finish()
            self.effect = None
        if self.fader:
            self.fader.finish()
            self.fader = None
        CutsceneActor.destroy(self)
        WillTurner.delete(self)
        if self.modelLoaded:
            self.modelLoaded.tutorialCharacter = 0
        return

    @staticmethod
    def getActorKey():
        return 'WillTurner'

    def attachHandheld(self, handheld, bRightHand):
        if handheld.isEmpty():
            return
        if bRightHand:
            handNode = self.find('**/*weapon_right')
        else:
            handNode = self.find('**/*weapon_left')
        handheld.reparentTo(handNode)

    def detachHandheld(self, handheld, remove=False):
        if handheld.isEmpty():
            return
        handheld.detachNode()
        if remove:
            handheld.removeNode()

    def recordTransAtCutscene(self, frame):
        animName = self.getCSAnimNames()[0]
        self.pose(animName, frame)
        rootNode = self.find('**/dx_root')
        self.posFromPose = Vec3(rootNode.getX(render), rootNode.getY(render), 0)
        self.hprFromPose = rootNode.getHpr(render)
        if self.modelLoaded:
            self.modelLoaded.setPos(render, self.posFromPose)
            self.modelLoaded.setH(render, self.hprFromPose[0] - 180)

    def spawnSkeletons(self, cutscene):
        jr1 = cutscene.getActor('Skeleton-2')
        jr1.unstash()
        jr1.fadeIn(1.5)
        jr2 = cutscene.getActor('Skeleton-3')
        jr2.unstash()
        jr2.fadeIn(1.5)
        spawnEffect = JRSpawn.getEffect()
        if spawnEffect:
            spawnEffect.reparentTo(render)
            spawnEffect.setPos(jr1.find('**/dx_root').getPos(render))
            spawnEffect.setZ(1.75)
            spawnEffect.setScale(0.8)
            spawnEffect.play()
        spawnEffect = JRSpawn.getEffect()
        if spawnEffect:
            spawnEffect.reparentTo(render)
            spawnEffect.setPos(jr2.find('**/dx_root').getPos(render))
            spawnEffect.setZ(1.75)
            spawnEffect.setScale(0.8)
            spawnEffect.play()


class CutElizabethSwan(CutsceneActor, ElizabethSwan):

    def __init__(self, Uid, cutsceneDesc):
        self.Uid = Uid
        ElizabethSwan.__init__(self)
        CutsceneActor.__init__(self, cutsceneDesc)
        for animName in self.getCSAnimNames():
            animFileName = 'models/char/es_%s' % animName
            self.animFileNames.append(animFileName)
            self.loadAnims({animName: animFileName})
            self.getAnimControls(animName, allowAsyncBind=False)

    def destroy(self):
        if self.effect:
            self.effect.finish()
            self.effect = None
        if self.fader:
            self.fader.finish()
            self.fader = None
        if self.modelLoaded:
            self.modelLoaded.tutorialCharacter = 0
        CutsceneActor.destroy(self)
        ElizabethSwan.delete(self)
        return

    @staticmethod
    def getActorKey():
        return 'ElizabethSwan'


class CutCaptBarbossa(CutsceneActor, CaptBarbossa):

    def __init__(self, Uid, cutsceneDesc):
        self.Uid = Uid
        CaptBarbossa.__init__(self)
        CutsceneActor.__init__(self, cutsceneDesc)
        for animName in self.getCSAnimNames():
            animFileName = 'models/char/cb_%s' % animName
            self.animFileNames.append(animFileName)
            self.loadAnims({animName: animFileName})
            self.getAnimControls(animName, allowAsyncBind=False)

    def destroy(self):
        if self.effect:
            self.effect.finish()
            self.effect = None
        if self.fader:
            self.fader.finish()
            self.fader = None
        if self.modelLoaded:
            self.modelLoaded.tutorialCharacter = 0
        CutsceneActor.destroy(self)
        CaptBarbossa.delete(self)
        return

    @staticmethod
    def getActorKey():
        return 'CaptBarbossa'

    def attachHandheld(self, handheld, bRightHand):
        if handheld.isEmpty():
            return
        if bRightHand:
            handNode = self.find('**/*weapon_right')
        else:
            handNode = self.find('**/*weapon_left')
        handheld.reparentTo(handNode)

    def detachHandheld(self, handheld, remove=False):
        if handheld.isEmpty():
            return
        handheld.detachNode()
        if remove:
            handheld.removeNode()


class CutTiaDalma(CutsceneActor, TiaDalma):

    def __init__(self, Uid, cutsceneDesc):
        self.Uid = Uid
        TiaDalma.__init__(self)
        CutsceneActor.__init__(self, cutsceneDesc)
        self.loadBG = False
        if '2.2' in cutsceneDesc.id:
            self.loadBG = True
        for animName in self.getCSAnimNames():
            animFileName = 'models/char/td_%s' % animName
            self.animFileNames.append(animFileName)
            self.loadAnims({animName: animFileName})
            self.getAnimControls(animName, allowAsyncBind=False)
            if self.loadBG:
                self.loadBGItems('models/jungles/jungle_set')

    def destroy(self):
        if self.effect:
            self.effect.finish()
            self.effect = None
        if self.fader:
            self.fader.finish()
            self.fader = None
        CutsceneActor.destroy(self)
        TiaDalma.delete(self)
        return

    def loadBGItems(self, path):
        self.bg = loader.loadModel(path)
        self.bg.reparentTo(self.getParent())

    def unloadBGItems(self):
        self.bg.removeNode()

    def showVisionBG(self, cutscene):
        bg1 = cutscene.getActor('Pirate-n-1')
        bg1.setTransparency(1)
        bg1.setAlphaScale(0.0)
        bg1.unstash()
        handNode = bg1.rightHandNode
        self.cutlassDict[0].reparentTo(handNode)
        bg2 = cutscene.getActor('Pirate-n-2')
        bg2.setTransparency(1)
        bg2.setAlphaScale(0.0)
        bg2.unstash()
        handNode = bg2.rightHandNode
        self.cutlassDict[1].reparentTo(handNode)
        bg3 = cutscene.getActor('Pirate-n-3')
        bg3.setTransparency(1)
        bg3.setAlphaScale(0.0)
        bg3.unstash()
        handNode = bg3.rightHandNode
        self.cutlassDict[2].reparentTo(handNode)
        self.fader = Parallel(LerpFunctionInterval(bg1.setAlphaScale, 2.0, fromData=0.0, toData=0.6), LerpFunctionInterval(bg2.setAlphaScale, 2.5, fromData=0.0, toData=0.6), LerpFunctionInterval(bg3.setAlphaScale, 2.0, fromData=0.0, toData=0.6))
        self.fader.start()

    def hideVisionBG(self, cutscene, cleanup):
        bg1 = cutscene.getActor('Pirate-n-1')
        bg1.stash()
        self.cutlassDict[0].detachNode()
        if cleanup:
            self.cutlassDict[0].removeNode()
        bg2 = cutscene.getActor('Pirate-n-2')
        bg2.stash()
        self.cutlassDict[1].detachNode()
        if cleanup:
            self.cutlassDict[1].removeNode()
        bg3 = cutscene.getActor('Pirate-n-3')
        bg3.stash()
        self.cutlassDict[2].detachNode()
        if cleanup:
            self.cutlassDict[2].removeNode()

    def showVisionJR(self, cutscene):
        self.hideVisionBG(cutscene, False)
        jr1 = cutscene.getActor('JollyRoger')
        jr1.unstash()
        jr1.setTransparency(1)
        jr1.setAlphaScale(0.5)
        jr2 = cutscene.getActor('Skeleton-4')
        jr2.unstash()
        jr2.setTransparency(1)
        jr2.setAlphaScale(0.7)
        jr3 = cutscene.getActor('Skeleton-5')
        jr3.unstash()
        jr3.setTransparency(1)
        jr3.setAlphaScale(0.7)

    def spawnSkeleton1(self, cutscene):
        rootNode = cutscene.getActor('JollyRoger').find('**/def_root')
        effectPos = Vec3(rootNode.getX(self) + 2.5, rootNode.getY(self) + 2, rootNode.getZ(self) - 4.5)
        spawnEffect = JRSpawn.getEffect()
        if spawnEffect:
            spawnEffect.reparentTo(self)
            spawnEffect.setPos(effectPos)
            spawnEffect.play()

    def spawnSkeleton2(self, cutscene):
        rootNode = cutscene.getActor('JollyRoger').find('**/def_root')
        effectPos = Vec3(rootNode.getX(self) - 4.0, rootNode.getY(self) + 2, rootNode.getZ(self) - 4.5)
        spawnEffect = JRSpawn.getEffect()
        if spawnEffect:
            spawnEffect.reparentTo(self)
            spawnEffect.setPos(effectPos)
            spawnEffect.play()

    def hideVisionJR(self, cutscene, cleanup):
        cutscene.getActor('JollyRoger').stash()
        cutscene.getActor('Skeleton-4').stash()
        cutscene.getActor('Skeleton-5').stash()

    def hideVision(self, cutscene, cutlassDict, cleanup):
        if cutlassDict:
            self.cutlassDict = cutlassDict
        self.hideVisionBG(cutscene, cleanup)
        self.hideVisionJR(cutscene, cleanup)

    @staticmethod
    def getActorKey():
        return 'TiaDalma'

    def startCutscene(self, locators):
        CutsceneActor.startCutscene(self, locators)
        if self.loadBG:
            self.bg.reparentTo(self.getParent())

    def finishCutscene(self):
        CutsceneActor.finishCutscene(self)
        if self.loadBG:
            self.unloadBGItems()

    def attachHandheld(self, handheld, bRightHand):
        if handheld.isEmpty():
            return
        if bRightHand:
            handNode = self.find('**/*weapon_right')
        else:
            handNode = self.find('**/*weapon_left')
        handheld.reparentTo(handNode)

    def detachHandheld(self, handheld, remove=False):
        if handheld.isEmpty():
            return
        handheld.detachNode()
        if remove:
            handheld.removeNode()


class CutJoshGibbs(CutsceneActor, JoshGibbs):

    def __init__(self, Uid, cutsceneDesc):
        self.Uid = Uid
        JoshGibbs.__init__(self)
        CutsceneActor.__init__(self, cutsceneDesc)
        for animName in self.getCSAnimNames():
            animFileName = 'models/char/jg_%s' % animName
            self.animFileNames.append(animFileName)
            self.loadAnims({animName: animFileName})
            self.getAnimControls(animName, allowAsyncBind=False)

    def destroy(self):
        if self.effect:
            self.effect.finish()
            self.effect = None
        if self.fader:
            self.fader.finish()
            self.fader = None
        CutsceneActor.destroy(self)
        JoshGibbs.delete(self)
        return

    @staticmethod
    def getActorKey():
        return 'JoshGibbs'


class CutPirate(CutsceneActor, Pirate):

    def __init__(self, Uid, npcIndex, cutsceneDesc):
        self.Uid = Uid
        Pirate.__init__(self)
        CutsceneActor.__init__(self, cutsceneDesc)
        dna = HumanDNA()
        dna.loadFromNPCDict(NPCList.NPC_LIST[Uid])
        self.setDNA(dna)
        self.makeAnimDict(dna.gender, npcIndex)
        if 'localAvatar' in __builtins__:
            self.generateHuman(dna.gender, base.cr.humanHigh)
        else:
            self.generateHuman(dna.gender, base.pe.human)
        if cutsceneDesc.id == '2.2: Tia Dalma Compass':
            self.useLOD(500)
        self.setGlobalScale(1.0)
        self._npcIndex = npcIndex
        self.faceTowardsViewer()
        for animName in self.getCSAnimNames():
            self.getAnimControls(str(npcIndex) + '_' + animName, allowAsyncBind=False)

    def destroy(self):
        CutsceneActor.destroy(self)
        Pirate.delete(self)

    def getInterval(self, duration=None):
        ival = Sequence()
        for animName in self.getCSAnimNames():
            if animName == self.getCSAnimNames()[len(self.getCSAnimNames()) - 1]:
                ival.append(self.actorInterval('%s_%s' % (self._npcIndex, animName), duration=duration))
            else:
                ival.append(self.actorInterval('%s_%s' % (self._npcIndex, animName)))

        return ival

    def makeAnimDict(self, gender, npcIndex):
        animDict = []
        for animName in self.getCSAnimNames():
            queryName = '%s_%s' % (npcIndex, animName)
            if gender == 'f':
                animFileName = 'models/char/fp_%s' % queryName
            else:
                animFileName = 'models/char/mp_%s' % queryName
            self.animFileNames.append(animFileName)
            entryDict = [queryName, queryName]
            animDict.append(entryDict)

        self.createAnimDict(animDict)

    @staticmethod
    def getActorKey(self, npcIndex):
        return 'Pirate-%s-%s' % (self.style.gender, npcIndex)

    def getThisActorKey(self):
        return CutPirate.getActorKey(self, self._npcIndex)

    def attachHandheld(self, handheld, bRightHand):
        if handheld == None or handheld.isEmpty():
            return
        if bRightHand:
            handNode = self.rightHandNode
        else:
            handNode = self.leftHandNode
        handheld.reparentTo(handNode)
        return

    def detachHandheld(self, handheld, remove=False):
        if handheld == None or handheld.isEmpty():
            return
        handheld.detachNode()
        if remove:
            handheld.removeNode()
        return


class CutSkeleton(CutsceneActor, Skeleton):

    def __init__(self, skeletonType, npcIndex, cutsceneDesc):
        self.Uid = None
        Skeleton.__init__(self)
        CutsceneActor.__init__(self, cutsceneDesc)
        self.setAvatarType(skeletonType)
        self._npcIndex = npcIndex
        self.faceTowardsViewer()
        if cutsceneDesc.id == '2.2: Tia Dalma Compass':
            self.useLOD(500)
        for animName in self.getCSAnimNames():
            animFileName = 'models/char/mp_%s_%s' % (npcIndex, animName)
            self.animFileNames.append(animFileName)
            self.getAnimControls(str(npcIndex) + '_' + animName, allowAsyncBind=False)

        return

    def destroy(self):
        CutsceneActor.destroy(self)
        Skeleton.delete(self)

    def getInterval(self, duration=None):
        ival = Sequence()
        for animName in self.getCSAnimNames():
            if animName == self.getCSAnimNames()[len(self.getCSAnimNames()) - 1]:
                ival.append(self.actorInterval('%s_%s' % (self._npcIndex, animName), duration=duration))
            else:
                ival.append(self.actorInterval('%s_%s' % (self._npcIndex, animName)))

        return ival

    @staticmethod
    def getActorKey(npcIndex):
        return 'Skeleton-%s' % npcIndex

    def getThisActorKey(self):
        return CutSkeleton.getActorKey(self._npcIndex)


class CutLocalPirate(CutsceneActor):

    def __init__(self, wantZombie, cutsceneDesc):
        self.Uid = None
        CutsceneActor.__init__(self, cutsceneDesc)
        self.posFromPose = None
        self.eventName = None
        if 'localAvatar' in __builtins__:
            self.localAvatar = localAvatar
            dna = localAvatar.style
            masterHuman = base.cr.humanHigh
        else:
            masterHuman = base.pe.human
            self.localAvatar = Human()
            if not hasattr(base, 'pe'):
                gender = 'm'
                shape = 2
                dna = HumanDNA(gender)
                dna.setBodyShape(shape)
            else:
                gender = base.pe.cutLocalPirateGender
                shape = base.pe.cutLocalPirateShape
                dna = HumanDNA(gender)
                dna.setBodyShape(shape)
                if base.pe.panel.useNPCinCutscene.get():
                    currNpcList = base.pe.getNPCList()
                    if currNpcList.NPC_LIST.has_key(base.pe.cutLocalPirateId):
                        dnaDict = currNpcList.NPC_LIST[base.pe.cutLocalPirateId]
                        dna = HumanDNA()
                        dna.loadFromNPCDict(dnaDict)
            self.localAvatar.setDNA(dna)
            self.localAvatar.generateHuman(dna.gender, masterHuman)
        self.wantZombie = wantZombie
        if self.wantZombie:
            self.zombieAvatar = Human()
            self.zombieAvatar.style = HumanDNA(self.localAvatar.style.gender)
            self.zombieAvatar.zombie = True
            self.zombieAvatar.style.copy(self.localAvatar.style)
            self.zombieAvatar.generateHuman(self.zombieAvatar.style.gender, masterHuman)
            self.zombieAvatar.faceTowardsViewer()
        for animName in self.getCSAnimNames():
            if dna.gender == 'f':
                animFileName = 'models/char/fp_0_%s' % animName
            else:
                animFileName = 'models/char/mp_0_%s' % animName
            self.animFileNames.append(animFileName)
            self.localAvatar.getAnimControls('0_' + animName, allowAsyncBind=False)
            if self.wantZombie:
                self.zombieAvatar.getAnimControls('0_' + animName, allowAsyncBind=False)

        if 'localAvatar' in __builtins__:
            if self._cutsceneName == 'tut_act_1_1_2_jail':
                self.preloadFemale()
        self.oldAvState = None
        return

    def destroy(self):
        if 'localAvatar' not in __builtins__:
            self.localAvatar.delete()
        del self.localAvatar
        if self.wantZombie:
            del self.zombieAvatar
        CutsceneActor.destroy(self)
        if self.fader:
            self.fader.finish()
            self.fader = None
        return

    def fadeIn(self):
        if self.fader:
            self.fader.finish()
            self.fader = None
        self.localAvatar.setTransparency(1)
        self.fader = Sequence(self.localAvatar.colorScaleInterval(1.0, Vec4(0, 0, 0, 1), startColorScale=Vec4(0, 0, 0, 0)), self.localAvatar.colorScaleInterval(1.0, Vec4(1, 1, 1, 1), startColorScale=Vec4(0, 0, 0, 1)))
        self.fader.start()
        return

    def fadeOut(self):
        if self.fader:
            self.fader.finish()
            self.fader = None
        self.localAvatar.setTransparency(1)
        self.fader = Sequence(self.localAvatar.colorScaleInterval(1.0, Vec4(0, 0, 0, 1), startColorScale=Vec4(1, 1, 1, 1)), self.localAvatar.colorScaleInterval(1.0, Vec4(0, 0, 0, 0), startColorScale=Vec4(0, 0, 0, 1)))
        self.fader.start()
        return

    def openJailDoor(self):
        if 'localAvatar' in __builtins__:
            localAvatar.openJailDoor()
            return
        self.jail = render.find('**/navy_jail_interior*')
        if self.jail.isEmpty():
            return
        self.jail_door = self.jail.find('**/jail_door01')
        self.jail_lock = self.jail.find('**/lock01')
        self.jail_door_collision = self.jail.find('**/door_collision_01')
        seq = Sequence(LerpHprInterval(self.jail_door, 1, VBase3(120, self.jail_door.getP(), self.jail_door.getR()), blendType='easeInOut'), duration=1.0)
        seq.start()
        self.jail_door_collision.setR(30)
        if not self.jail_lock.isEmpty():
            self.jail_lock.stash()

    def closeJailDoor(self):
        if 'localAvatar' in __builtins__:
            return
        if self.jail.isEmpty():
            return
        self.jail_door.setH(0)
        self.jail_door_collision.setR(0)
        self.jail_lock.unstash()

    def attachHandheld(self, handheld, bRightHand, zombie=False):
        if handheld.isEmpty():
            return
        if zombie:
            avatar = self.zombieAvatar
        else:
            avatar = self.localAvatar
        if bRightHand:
            handNode = avatar.rightHandNode
        else:
            handNode = avatar.leftHandNode
        handheld.reparentTo(handNode)

    def detachHandheld(self, handheld, remove=False, zombie=False):
        if handheld.isEmpty():
            return
        if zombie:
            avatar = self.zombieAvatar
        else:
            avatar = self.localAvatar
        handheld.detachNode()
        if remove:
            handheld.removeNode()

    def preloadFemale(self):
        for animName in self.getCSAnimNames():
            animFileName = 'models/char/fp_0_%s' % animName
            self.animFileNames.append(animFileName)
            loader.loadModel(animFileName)

    def hideZombie(self):
        if self.wantZombie:
            self.zombieAvatar.hide()
        self.localAvatar.show()

    def showZombie(self):
        if self.wantZombie:
            self.zombieAvatar.show()
        self.localAvatar.hide()

    def syncZombieAnimation(self):
        if self.wantZombie:
            self.zombieAvatar.play('0_' + self.getCSAnimNames()[1])

    @staticmethod
    def getActorKey():
        return 'LocalPirate'

    def getInterval(self, duration=None):
        ival = Sequence()
        for animName in self.getCSAnimNames():
            if animName == self.getCSAnimNames()[len(self.getCSAnimNames()) - 1]:
                actorIval = self.localAvatar.actorInterval('0_%s' % animName, duration=duration, blendInT=0, blendOutT=0)
            else:
                actorIval = self.localAvatar.actorInterval('0_%s' % animName, blendInT=0, blendOutT=0)
            ival.append(actorIval)

        return ival

    def recordTransAtCutscene(self, frame):
        animName = '0_' + self.getCSAnimNames()[0]
        self.localAvatar.pose(animName, frame)
        rootNode = self.localAvatar.getLOD('2000').find('**/dx_root')
        self.posFromPose = Vec3(rootNode.getX(render), rootNode.getY(render), 0)
        self.hprFromPose = rootNode.getHpr(render)

    def adjustPos(self, x, y, z, h=-90):
        self.posFromPose = Vec3(x, y, z)
        self.hprFromPose = Vec3(h, 0, 0)

    def recordEvent(self, eventName):
        self.eventName = eventName

    def setOldAvState(self, avState):
        self.oldAvState = avState

    def startCutscene(self, locators):
        self.oldParams = ScratchPad()
        self.oldParams.parent = self.localAvatar.getParent()
        self.oldParams.trans = self.localAvatar.getTransform()
        self.oldParams.bodyScale = self.localAvatar.getGlobalScale()
        if hasattr(self.localAvatar, 'gameFSM'):
            if self.oldAvState:
                self.oldParams.gameState = self.oldAvState
            else:
                self.oldParams.gameState = self.localAvatar.gameFSM.state
            self.oldParams.gameStateLock = self.localAvatar.gameFSM.lockFSM
            self.localAvatar.gameFSM.lockFSM = True
            self.localAvatar.b_setGameState('Cutscene')
        self.localAvatar.reparentTo(locators.origin)
        self.localAvatar.clearTransform()
        self.localAvatar.node().setBounds(OmniBoundingVolume())
        self.localAvatar.node().setFinal(1)
        self.localAvatar.stopBlink()
        if 'localAvatar' in __builtins__:
            self.localAvatar.stopLookAroundTask()
        self.localAvatar.headNode.setHpr(0, 0, 0)
        self.localAvatar.nametag3d.hide()
        self.localAvatar.faceTowardsViewer()
        LODLevels = {2: 2000,1: 1000,0: 500}
        if 'localAvatar' in __builtins__:
            characterDetailLevel = base.options.getCharacterDetailSetting()
            if characterDetailLevel != 2:
                characterDetailLevel = 1
            characterDetail = LODLevels[characterDetailLevel]
        else:
            characterDetail = 2000
        self.localAvatar.useLOD(characterDetail)
        self.localAvatar.setGlobalScale(1.0)
        if self.wantZombie:
            self.zombieAvatar.reparentTo(locators.origin)
            self.zombieAvatar.clearTransform()
            self.zombieAvatar.node().setBounds(OmniBoundingVolume())
            self.zombieAvatar.node().setFinal(1)
            self.zombieAvatar.stopBlink()
            if self.localAvatar and hasattr(self.zombieAvatar, 'lookAroundTaskName'):
                self.zombieAvatar.stopLookAroundTask()
            self.zombieAvatar.headNode.setHpr(0, 0, 0)
            self.zombieAvatar.nametag3d.hide()
            self.zombieAvatar.faceTowardsViewer()
            self.zombieAvatar.useLOD(characterDetail)
            self.zombieAvatar.setGlobalScale(1.0)

    def finishCutscene(self):
        self.localAvatar.faceAwayFromViewer()
        self.localAvatar.wrtReparentTo(self.oldParams.parent)
        self.localAvatar.setTransform(self.oldParams.trans)
        self.localAvatar.setPrevTransform(self.oldParams.trans)
        if self.posFromPose:
            self.localAvatar.setPos(render, self.posFromPose)
            self.localAvatar.setH(render, self.hprFromPose[0])
        self.localAvatar.node().clearBounds()
        self.localAvatar.node().setFinal(0)
        self.localAvatar.startBlink()
        self.localAvatar.nametag3d.show()
        self.localAvatar.resetLOD()
        if self.wantZombie:
            self.zombieAvatar.hide()
            self.localAvatar.show()
        if hasattr(self.localAvatar, 'gameFSM'):
            self.localAvatar.enableMixing()
            self.localAvatar.gameFSM.lockFSM = False
            if self.oldParams.gameState == 'EnterTunnel' or self.oldParams.gameState == 'DoorInteract' or self.oldParams.gameState == 'TeleportOut':
                self.localAvatar.b_setGameState('LandRoam')
            else:
                self.localAvatar.b_setGameState(self.oldParams.gameState)
            self.localAvatar.gameFSM.lockFSM = self.oldParams.gameStateLock
        self.localAvatar.setGlobalScale(self.oldParams.bodyScale)
        del self.oldParams
        if self.eventName:
            messenger.send(self.eventName)


CutBartenderMmsDoggerel = Functor(CutPirate, '1154731709.64jubutler')
CutBartenderFmiNell = Functor(CutPirate, '1171238953.92MAsaduzz')
CutCaptainBeckShort = Functor(CutPirate, '1153439632.21darren')
CutBlackGuard1 = Functor(CutPirate, '1175282688.00MAsaduzz')
CutBlackGuard2 = Functor(CutPirate, '1175283200.00MAsaduzz')
CutBlackGuard3 = Functor(CutPirate, '1175283328.00MAsaduzz')
CutBartenderPear = Functor(CutPirate, '1168022348.66Shochet')
CutNavyMtpPeter = Functor(CutPirate, '1171321221.87MAsaduzz')
CutNavyMtpJeff = Functor(CutPirate, '1171321509.23MAsaduzz')