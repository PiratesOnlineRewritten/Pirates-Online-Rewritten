from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.interval.ProjectileInterval import *
from direct.directnotify import DirectNotifyGlobal
from direct.task.Task import Task
from direct.distributed.GridChild import GridChild
from pirates.piratesbase import PLocalizer
from pirates.battle.CannonballProjectile import CannonballProjectile
from pirates.piratesbase import PiratesGlobals
from pirates.minigame import CannonDefenseGlobals, DistributedDefendWorld
from pirates.effects.SimpleSmokeCloud import SimpleSmokeCloud
from pirates.effects.FireTrail import FireTrail
from pirates.effects.FireballHit import FireballHit
from pirates.audio.SoundGlobals import loadSfx
from pirates.audio import SoundGlobals
import random
from direct.distributed.DistributedObject import DistributedObject

class DistributedFlamingBarrel(DistributedObject, GridChild):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        GridChild.__init__(self)
        self.collNode = None
        self.destroyed = False
        self.smokeVfx = None
        self.barrelModel = None
        self.trailEffect = None
        self._initAudio()
        return

    def _initAudio(self):
        self.launchSound = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_BARREL_LAUNCH)
        self.hitSound = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_BARREL_HIT)
        self.shotDownSound = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_BARREL_SHOTDOWN)
        self.closeSound = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_BARREL_CLOSE)

    def setShipDoId(self, shipDoId):
        self.ship = self.cr.getDo(shipDoId)

    def setTargetDoId(self, targetDoId):
        self.pirateTarget = self.cr.getDo(targetDoId)

    def setFlightDuration(self, duration):
        self.flightDuration = duration

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        if self.ship is None or self.pirateTarget is None or self.ship.isEmpty() or self.pirateTarget.isEmpty():
            self.sendUpdate('shotDown')
            return
        self.barrelModel = loader.loadModel('models/ammunition/pir_m_gam_can_powderKeg')
        self.barrelModel.setScale(2.0)
        base.playSfx(self.launchSound, node=self.barrelModel, cutoff=2000)
        self.barrelModel.reparentTo(self.ship)
        self.barrelModel.setPos(0, 0, 10)
        self.barrelModel.wrtReparentTo(self.pirateTarget)
        self.makeCollNode()
        self.barrelModel.setTag('objType', str(PiratesGlobals.COLL_FLAMING_BARREL))
        self.collNode.setPythonTag('barrel', self)
        self.projectileInterval = Parallel(ProjectileInterval(self.barrelModel, endPos=Point3(0.0, 0.0, 4.5), duration=self.flightDuration, gravityMult=CannonDefenseGlobals.BARREL_GRAVITY), self.barrelModel.hprInterval(self.flightDuration, Vec3(720, 640, 440)), Sequence(Wait(self.flightDuration - 1.2), Func(base.playSfx, self.closeSound, node=self.barrelModel, cutoff=2000), Wait(1.2), Func(self.hitTarget)), name=self.uniqueName('FlamingBarrelFlying'))
        self.collNode.reparentTo(self.barrelModel)
        self.projectileInterval.start()
        base.cTrav.addCollider(self.collNode, self.collHandler)
        base.cr.activeWorld.flamingBarrels.append(self)
        self.trailEffect = FireTrail.getEffect()
        if self.trailEffect:
            self.trailEffect.reparentTo(self.barrelModel)
            self.trailEffect.wantGlow = base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium
            self.trailEffect.wantBlur = base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh
            self.trailEffect.startLoop()
        return

    def shotDown(self, s=None):
        base.playSfx(self.shotDownSound, node=self.barrelModel, cutoff=2000)
        self.destroyed = True
        if self in base.cr.activeWorld.flamingBarrels:
            base.cr.activeWorld.flamingBarrels.remove(self)
        self.startSmoke()
        self.projectileInterval.pause()
        self.projectileInterval.clearToInitial()
        self.barrelModel.removeNode()
        base.cTrav.removeCollider(self.collNode)
        self.collNode.removeNode()
        taskMgr.doMethodLater(0.4, self.sendUpdate, name=self.uniqueName('SendShotDown'), extraArgs=['shotDown'])

    def startSmoke(self):
        self.smokeVfx = SimpleSmokeCloud.getEffect(unlimited=True)
        if self.smokeVfx:
            self.smokeVfx.reparentTo(self.pirateTarget)
            self.smokeVfx.setPos(self.barrelModel.getPos())
            self.smokeVfx.setEffectScale(0.6)
            self.smokeVfx.play()

    def hitTarget(self):
        base.playSfx(self.hitSound, node=self.barrelModel, cutoff=2000)
        if not self.destroyed:
            base.talkAssistant.receiveGameMessage(PLocalizer.CannonDefense['DizzyChatNotification'] % self.pirateTarget.name)
            if CannonDefenseGlobals.DAZED_ENABLED and isinstance(base.cr.activeWorld, DistributedDefendWorld.DistributedDefendWorld) and base.cr.activeWorld.fsm.getCurrentOrNextState() not in ('ResultScreen',
                                                                                                                                                                                                 'Defeat',
                                                                                                                                                                                                 'Victory'):
                self.pirateTarget.setPirateDazed(True)
            self.barrelModel.removeNode()
            self.barrelModel = None
            base.cTrav.removeCollider(self.collNode)
            self.collNode.removeNode()
            self.projectileInterval.pause()
            self.projectileInterval.clearToInitial()
        effect = SimpleSmokeCloud.getEffect(unlimited=True)
        if effect:
            effect.reparentTo(self.pirateTarget)
            effect.setEffectScale(0.6)
            effect.play()
        effect = FireballHit.getEffect()
        if effect:
            effect.reparentTo(self.pirateTarget)
            effect.setScale(2.0)
            effect.play()
        return

    def delete(self):
        taskMgr.remove(self.uniqueName('SendShotDown'))
        if not self.destroyed:
            if isinstance(base.cr.activeWorld, DistributedDefendWorld.DistributedDefendWorld) and self in base.cr.activeWorld.flamingBarrels:
                base.cr.activeWorld.flamingBarrels.remove(self)
            self.destroyed = True
            if self.barrelModel is not None:
                self.barrelModel.removeNode()
                base.cTrav.removeCollider(self.collNode)
                self.collNode.removeNode()
                self.projectileInterval.pause()
                self.projectileInterval.clearToInitial()
        if self.smokeVfx:
            self.smokeVfx.cleanUpEffect()
            self.smokeVfx = None
        if self.trailEffect:
            self.trailEffect.stopLoop()
            self.trailEffect = None
        GridChild.delete(self)
        DistributedObject.delete(self)
        return

    def makeCollNode(self):
        if self.collNode == None:
            node = CollisionNode('flamingBarrelCollNode')
            node.setFromCollideMask(BitMask32.allOff())
            node.setIntoCollideMask(PiratesGlobals.TargetBitmask)
            weaponSphere = CollisionSphere(0.0, 0.0, 0.0, 2.0)
            weaponSphere.setTangible(1)
            node.clearSolids()
            node.addSolid(weaponSphere)
            self.collNode = NodePath(node)
            self.collHandler = CollisionHandlerEvent()
        return