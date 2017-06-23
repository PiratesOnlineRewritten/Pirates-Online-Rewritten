from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
import re
import random
import types
from pirates.holiday import DistributedHolidayObject
from pirates.movement import DistributedMovingObject
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.pirate import BattleNPCGameFSM
from pirates.pirate import AvatarType
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle import WeaponGlobals
from pirates.piratesgui import HpMeter
from pirates.invasion import InvasionGlobals
from pirates.ai import HolidayGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.effects.SmokeBlast import SmokeBlast
from pirates.effects.ExplosionFlip import ExplosionFlip

class DistributedCapturePoint(DistributedHolidayObject.DistributedHolidayObject, DistributedMovingObject.DistributedMovingObject):
    DiskUseColor = (0, 0, 0, 1)
    DiskWaitingColor = (1, 0, 0, 1)
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCapturePoint')
    WantHpCheck = base.config.GetBool('want-hp-check', 1)

    def __init__(self, cr):
        NodePath.__init__(self, 'DistributedCapturePoint')
        DistributedHolidayObject.DistributedHolidayObject.__init__(self, cr, '')
        DistributedMovingObject.DistributedMovingObject.__init__(self, cr)
        self.__geomLoaded = 0
        self.anims = None
        self.uniqueId = ''
        self.parentObjId = None
        self.pendingPlacement = None
        self.name = 'Capture Point'
        self.isNpc = 1
        self.locationId = ''
        self.holidayId = None
        self.currentTarget = None
        self.skillEffects = []
        self.belongsToTeam = PiratesGlobals.PLAYER_TEAM
        self.avatarType = AvatarType.AvatarType()
        self.level = 1
        if self.WantHpCheck:
            self.__hp = 0
            self.__maxHp = 0
        else:
            self.hp = 0
            self.maxHp = 0
        self.hpMeter = None
        self.visible = False
        self.cHp = None
        self.cHpNode = None
        self.cHpNodePath = None
        self.enteredSphere = False
        self.damageSfxs = []
        self.destroyedSfxs = []
        self.blinker = None
        self.initialHp = True
        self.noIntervals = True
        self.destroySmoke = None
        self.destroyExplosionLeft = None
        self.destroyExplosionRight = None
        return

    if WantHpCheck:

        def get_hp(self):
            return self.__hp

        def set_hp(self, hp):
            if type(hp) in [types.IntType, types.FloatType]:
                self.__hp = hp
            else:
                self.__hp = 0

        hp = property(get_hp, set_hp)

        def get_maxHp(self):
            return self.__maxHp

        def set_maxHp(self, maxHp):
            if type(maxHp) in [types.IntType, types.FloatType]:
                self.__maxHp = maxHp
            else:
                self.__maxHp = 1

        maxHp = property(get_maxHp, set_maxHp)

    def generate(self):
        DistributedHolidayObject.DistributedHolidayObject.generate(self)
        DistributedMovingObject.DistributedMovingObject.generate(self)

    def announceGenerate(self):
        DistributedHolidayObject.DistributedHolidayObject.announceGenerate(self)
        DistributedMovingObject.DistributedMovingObject.announceGenerate(self)
        myParentId = self.getLocation()[0]
        myParent = self.cr.doId2do[myParentId]
        self.gameFSM = BattleNPCGameFSM.BattleNPCGameFSM(self)
        self.motionFSM = None
        self.cr.uidMgr.addUid(self.uniqueId, self.getDoId())
        self.setClipPlane(base.farCull)
        self.damageSfxs = [
         loadSfx(SoundGlobals.SFX_FX_WOOD_SHATTER_02), loadSfx(SoundGlobals.SFX_FX_WOOD_SHATTER_03)]
        self.destroyedSfxs = [
         loadSfx(SoundGlobals.SFX_FX_EXPLODE_WOOD_01), loadSfx(SoundGlobals.SFX_FX_EXPLODE_WOOD_02)]
        whiteColor = PiratesGuiGlobals.TextFG2
        self.blinker = Sequence(Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor), Wait(0.2), Func(self.setBarColor, whiteColor), Wait(0.2), Func(self.setBarColor))
        return

    def setParentObjId(self, parentObjId):
        self.parentObjId = parentObjId

        def putObjOnParent(parentObj, self=self):
            self.notify.debug('putObj %s on parent %s' % (self.doId, parentObj))
            self.parentObj = parentObj
            self.pendingPlacement = None
            return

        if parentObjId > 0:
            self.pendingPlacement = base.cr.relatedObjectMgr.requestObjects([self.parentObjId], eachCallback=putObjOnParent)

    def disable(self):
        taskMgr.remove(self.taskName('playHitSoundTask'))
        taskMgr.remove(self.taskName('playOuchTask'))
        taskMgr.remove(self.taskName('playBonusOuchTask'))
        if self.hpMeter:
            self.hpMeter.destroy()
        if self.cHpNodePath:
            self.cTrav.removeCollider(self.cHpNodePath)
            self.cHpNodePath.removeNode()
            self.cHpNodePath = None
        if self.cHpNode:
            self.cHpNode = None
        if self.cHp:
            self.cHp = None
        if self.blinker:
            self.blinker.pause()
        self.damageSfxs = []
        self.destroyedSfxs = []
        self.blinker = None
        self.ignoreAll()
        self.cTrav = None
        DistributedHolidayObject.DistributedHolidayObject.disable(self)
        DistributedMovingObject.DistributedMovingObject.disable(self)
        self.gameFSM.cleanup()
        return

    def delete(self):
        DistributedHolidayObject.DistributedHolidayObject.delete(self)
        DistributedMovingObject.DistributedMovingObject.delete(self)
        if self.destroySmoke:
            self.destroySmoke.stop()
            self.destroySmoke.cleanUpEffect()
            self.destroySmoke = None
        if self.destroyExplosionLeft:
            self.destroyExplosionLeft.stop()
            self.destroyExplosionLeft.cleanUpEffect()
            self.destroyExplosionLeft = None
        if self.destroyExplosionRight:
            self.destroyExplosionRight.stop()
            self.destroyExplosionRight.cleanUpEffect()
            self.destroyExplosionRight = None
        return

    def setZone(self, zone):
        self.notify.debug('setZone %s' % zone)
        self.zone = zone

    def setLocationId(self, locationId):
        self.notify.debug('setLocationId %s' % locationId)
        self.locationId = locationId

    def setHp(self, hp):
        self.hp = hp
        if self.hpMeter and self.maxHp:
            self.hpMeter.update(self.hp, self.maxHp)
            if self.hp != self.maxHp:
                if self.blinker:
                    self.blinker.finish()
                    self.blinker.start()
            if not self.enteredSphere:
                self.hpMeter.hideMeter()

    def setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def setVisible(self, visible):
        self.visible = visible
        if visible:
            self.createHpMeter()

    def setBarColor(self, color=None):
        if self.hpMeter:
            if not color:
                hpFraction = float(self.hp) / float(self.maxHp)
                if hpFraction >= 0.5:
                    color = (0.1, 0.7, 0.1, 1)
                elif hpFraction >= 0.25:
                    color = (1.0, 1.0, 0.1, 1)
                else:
                    color = (1.0, 0.0, 0.0, 1)
            self.hpMeter.meter['barColor'] = color
            if color == PiratesGuiGlobals.TextFG2:
                self.hpMeter.categoryLabel['text_fg'] = color
            else:
                self.hpMeter.categoryLabel['text_fg'] = PiratesGuiGlobals.TextFG1

    def setHolidayId(self, holidayId):
        self.holidayId = holidayId
        self.name = PLocalizer.CapturePointNames[HolidayGlobals.getHolidayName(self.holidayId)][self.zone]
        if self.hpMeter:
            self.hpMeter.categoryLabel['text'] = self.name
        self.createCollisions()

    def createHpMeter(self):
        self.hpMeter = HpMeter.HpMeter(name='', height=0.035, width=0.45, parent=base.a2dBottomRight)
        self.hpMeter.setPos(-0.5, 0, 0.65)
        self.hpMeter.update(1, 1)
        self.hpMeter.hide()
        self.accept('enteringMinigame', self.hpMeter.hide)
        self.accept('exitingMinigame', self.hpMeter.show)

    def getTeam(self):
        return self.belongsToTeam

    def getLevel(self):
        return self.level

    def targetedWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, attacker, pos, charge=0, delay=None, multihit=0, itemEffects=[]):
        DistributedMovingObject.DistributedMovingObject.targetedWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, attacker, pos, charge, delay, multihit)
        if self.damageSfxs:
            base.playSfx(random.choice(self.damageSfxs), volume=0.6, node=self, cutoff=100)

    def getSkillEffects(self):
        return []

    def setInteractMode(self, mode):
        pass

    def getShortName(self):
        return self.getName()

    def isBoss(self):
        return False

    def isInInvasion(self):
        return False

    def getArmorScale(self):
        return 1.0

    def getMinimapObject(self):
        return None

    def destroyMinimapObject(self):
        pass

    def createCollisions(self):
        self.cTrav = base.localAvatar.cTrav
        if self.cHp == None:
            self.cHp = CollisionSphere(0, 0, 0, InvasionGlobals.getCapturePointHpSphereSize(self.holidayId))
            self.cHp.setTangible(0)
            self.cHpNode = CollisionNode(self.uniqueName('HpSphere'))
            self.cHpNode.setFromCollideMask(BitMask32.allOff())
            self.cHpNode.setIntoCollideMask(PiratesGlobals.WallBitmask)
            self.cHpNode.addSolid(self.cHp)
            self.cHpNodePath = self.attachNewNode(self.cHpNode)
            enterCollEvent = self.uniqueName('enter' + 'HpSphere')
            exitCollEvent = self.uniqueName('exit' + 'HpSphere')
            self.accept(enterCollEvent, self._handleEnterHpSphere)
            self.accept(exitCollEvent, self._handleExitHpSphere)
        return

    def _handleEnterHpSphere(self, collEntry):
        self.enteredSphere = True
        if self.hpMeter:
            self.hpMeter.showMeter()

    def _handleExitHpSphere(self, collEntry):
        self.enteredSphere = False
        if self.hpMeter:
            self.hpMeter.hideMeter()

    def playDestroyEffects(self):
        if self.destroyedSfxs:
            base.playSfx(random.choice(self.destroyedSfxs), node=self, cutoff=200)
        self.destroySmoke = SmokeBlast.getEffect(unlimited=True)
        if self.destroySmoke:
            self.destroySmoke.reparentTo(self)
            self.destroySmoke.play()
        self.destroyExplosionLeft = ExplosionFlip.getEffect(unlimited=True)
        if self.destroyExplosionLeft:
            self.destroyExplosionLeft.reparentTo(self)
            self.destroyExplosionLeft.setPos(random.randint(-10, 0), 0, 2.5)
            self.destroyExplosionLeft.play()
        self.destroyExplosionRight = ExplosionFlip.getEffect(unlimited=True)
        if self.destroyExplosionRight:
            self.destroyExplosionRight.reparentTo(self)
            self.destroyExplosionRight.setPos(random.randint(0, 10), 0, 2.5)
            self.destroyExplosionRight.play()

    def isInvisible(self):
        return 0