from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor.Actor import Actor
from direct.gui.DirectGui import DirectWaitBar, DirectLabel, DGG
from otp.otpbase import OTPRender
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.battle import WeaponGlobals
from pirates.effects.ShipFire import ShipFire
from pirates.effects.CannonSplash import CannonSplash
from pirates.effects.BulletEffect import BulletEffect
from pirates.minigame import CannonDefenseGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.ship.DistributedNPCSimpleShip import DistributedNPCSimpleShip
from pirates.uberdog.UberDogGlobals import InventoryType
import random

class DistributedCannonDefenseShip(DistributedNPCSimpleShip):
    specialHitSfx = {}
    coldShotHitSfx = None
    sharkChompSfx = {}

    def __init__(self, cr):
        DistributedNPCSimpleShip.__init__(self, cr)
        self.goldStolenlbl = None
        self.hasGoldlbl = None
        self.hasBNote = None
        self.textureCard = None
        self.goldIcon = None
        self.flameEffects = []
        self.isSinkingWhileOnFire = False
        self.healthModifier = 0
        self.modifierSet = False
        self.shipStatsSet = False
        self.shipStatIndex = None
        self.initHealthBar()
        self.initIndicatorIcons()
        self.sinkTimeScale = CannonDefenseGlobals.SHIP_SINK_DURATION_SCALE
        self.sharkActor = Actor('models/char/pir_r_gam_fsh_lgComTshark.bam', {'attack': 'models/char/pir_a_gam_fsh_lgComTshark_attack.bam'})
        self.sharkParallel = None
        self.fader = None
        if not self.coldShotHitSfx:
            DistributedCannonDefenseShip.specialHitSfx = {InventoryType.DefenseCannonMineInWater: loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_MINE_HIT),InventoryType.DefenseCannonBomb: loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_BOMB_HIT),InventoryType.DefenseCannonHotShot: loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_HOTSHOT_HIT),InventoryType.DefenseCannonFireStorm: loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_FIRESTORM_HIT),InventoryType.DefenseCannonChumShot: loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_SHARK)}
            DistributedCannonDefenseShip.coldShotHitSfx = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_ICE_HIT)
            DistributedCannonDefenseShip.sharkChompSfxs = [loadSfx(SoundGlobals.SFX_MONSTER_SMASH_01), loadSfx(SoundGlobals.SFX_MONSTER_SMASH_02), loadSfx(SoundGlobals.SFX_MONSTER_SMASH_03)]
        return

    def buildShip(self):
        DistributedNPCSimpleShip.buildShip(self)
        self.model.sfxAlternativeStyle = True

    def setupLocalStats(self):
        DistributedNPCSimpleShip.setupLocalStats(self)

    def setShipStatIndex(self, statIndex):
        self.shipStatsSet = True
        self.shipStatIndex = statIndex
        self.maxHp = CannonDefenseGlobals.shipStats[self.shipStatIndex]['shipHp']
        self.maxMastHealth = CannonDefenseGlobals.shipStats[self.shipStatIndex]['mastHp']
        self.healthBar.setPos(0.0, 0.0, CannonDefenseGlobals.shipStats[self.shipStatIndex]['healthBarHeight'])
        if self.modifierSet:
            self.calcModifiedHealth()

    def setHealthModifier(self, modifier):
        self.modifierSet = True
        self.healthModifier = modifier
        if self.shipStatsSet:
            self.calcModifiedHealth()

    def calcModifiedHealth(self):
        if self.healthModifier == 0:
            return
        self.maxHp += self.healthModifier * (self.maxHp * CannonDefenseGlobals.ENEMY_DIFFICULTY_INCREASE)
        mastList = CannonDefenseGlobals.shipStats[self.shipStatIndex]['mastHp']
        mastFinalHp = []
        for mastHealth in mastList:
            hp = mastHealth
            hp += self.healthModifier * (mastHealth * CannonDefenseGlobals.ENEMY_DIFFICULTY_INCREASE)
            mastFinalHp.append(hp)

        self.maxMastHealth = mastFinalHp

    def setLogo(self, logo):
        self.logo = logo

    def setStyle(self, style):
        self.style = style

    def announceGenerate(self):
        DistributedNPCSimpleShip.announceGenerate(self)
        rad = (self.model.dimensions / 2.0).length()
        cn = NodePath(CollisionNode('c'))
        cs = CollisionSphere(0, 0, 0, rad)
        cn.node().addSolid(cs)
        cn.reparentTo(self.model.modelCollisions)
        cn.setTransform(self.model.center.getTransform(self))
        cn.node().setIntoCollideMask(PiratesGlobals.GenericShipBitmask)
        self.model.defendSphere = cn
        self.model.modelRoot.setScale(CannonDefenseGlobals.SHIP_SCALE)
        self.fadeIn(CannonDefenseGlobals.SHIP_FADEIN)
        self.smoother.setExpectedBroadcastPeriod(0.3)
        self.smoother.setDelay(2)
        self.healthBar.reparentTo(self.model.modelRoot)

    def initHealthBar(self):
        self.healthBar = DirectWaitBar(frameSize=(-0.35, 0.35, -0.04, 0.04), relief=DGG.FLAT, frameColor=(0.0,
                                                                                                          0.0,
                                                                                                          0.0,
                                                                                                          0.0), borderWidth=(0.0,
                                                                                                                             0.0), barColor=(0.0,
                                                                                                                                             1.0,
                                                                                                                                             0.0,
                                                                                                                                             1.0), scale=100)
        self.healthBar.setBillboardPointEye()
        self.healthBar['value'] = 100
        self.healthBar.hide(OTPRender.ReflectionCameraBitmask)
        self.healthBar.setLightOff()

    def initIndicatorIcons(self):
        self.textureCard = loader.loadModel('models/textureCards/pir_m_gam_can_ship_icons')
        if self.textureCard:
            self.goldIcon = self.textureCard.find('**/pir_t_shp_can_gold*')
        self.goldStolenlbl = DirectLabel(parent=self.healthBar, relief=None, pos=(0,
                                                                                  0,
                                                                                  0.2), text_align=TextNode.ACenter, text_scale=0.5, textMayChange=0, text='!', text_fg=PiratesGuiGlobals.TextFG23, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateBoldOutlineFont(), sortOrder=2)
        self.goldStolenlbl.setTransparency(1)
        self.goldStolenlbl.hide()
        self.hasGoldlbl = DirectLabel(parent=self.healthBar, relief=None, pos=(0, 0,
                                                                               0.35), image=self.goldIcon, image_scale=0.5, image_pos=(0,
                                                                                                                                       0,
                                                                                                                                       0), sortOrder=2)
        self.hasGoldlbl.setTransparency(1)
        self.hasGoldlbl.hide()
        self.hasBNote = self.healthBar.attachNewNode('noteIndicator')
        self.bnoteBack = loader.loadModel('models/textureCards/skillIcons').find('**/pir_t_gui_can_moneyIcon').copyTo(self.hasBNote)
        self.hasBNote.setZ(0.35)
        self.hasBNote.setScale(0.6)
        self.hasBNote.hide()
        return

    def getHealthBarColor(self, health):
        return CannonDefenseGlobals.SHIP_HEALTH_COLORS[int(health / 100.0 * (len(CannonDefenseGlobals.SHIP_HEALTH_COLORS) - 1))]

    def setHealthState(self, health):
        DistributedNPCSimpleShip.setHealthState(self, health)
        self.healthBar['value'] = health
        self.healthBar['barColor'] = self.getHealthBarColor(health)

    def setCurrentState(self, state):
        if state == CannonDefenseGlobals.SHIP_STATE_STEALING:
            self.goldStolenlbl.show()
        elif state == CannonDefenseGlobals.SHIP_STATE_HASTREASURE:
            self.hasGoldlbl.show()
            self.goldStolenlbl.hide()
        elif state == CannonDefenseGlobals.SHIP_STATE_HASBNOTES:
            self.hasBNote.show()
            self.goldStolenlbl.hide()
        else:
            self.hasGoldlbl.hide()
            self.hasBNote.hide()
            self.goldStolenlbl.hide()
        rad = (self.model.dimensions / 2.0).length()
        cn = NodePath(CollisionNode('c'))
        cs = CollisionSphere(0, 0, 0, rad)
        cn.node().addSolid(cs)
        cn.reparentTo(self.model.modelCollisions)
        cn.setTransform(self.model.center.getTransform(self))
        cn.node().setIntoCollideMask(PiratesGlobals.GenericShipBitmask)
        self.model.defendSphere = cn
        self.model.modelRoot.setScale(CannonDefenseGlobals.SHIP_SCALE)
        self.fadeIn(CannonDefenseGlobals.SHIP_FADEIN)
        self.smoother.setExpectedBroadcastPeriod(0.3)
        self.smoother.setDelay(2)
        self.healthBar.reparentTo(self.model.modelRoot)

    def initHealthBar(self):
        self.healthBar = DirectWaitBar(frameSize=(-0.35, 0.35, -0.04, 0.04), relief=DGG.FLAT, frameColor=(0.0,
                                                                                                          0.0,
                                                                                                          0.0,
                                                                                                          0.0), borderWidth=(0.0,
                                                                                                                             0.0), barColor=(0.0,
                                                                                                                                             1.0,
                                                                                                                                             0.0,
                                                                                                                                             1.0), scale=100)
        self.healthBar.setBillboardPointEye()
        self.healthBar['value'] = 100
        self.healthBar.hide(OTPRender.ReflectionCameraBitmask)
        self.healthBar.setLightOff()

    def initIndicatorIcons(self):
        self.textureCard = loader.loadModel('models/textureCards/pir_m_gam_can_ship_icons')
        if self.textureCard:
            self.goldIcon = self.textureCard.find('**/pir_t_shp_can_gold*')
        self.goldStolenlbl = DirectLabel(parent=self.healthBar, relief=None, pos=(0,
                                                                                  0,
                                                                                  0.2), text_align=TextNode.ACenter, text_scale=0.5, textMayChange=0, text='!', text_fg=PiratesGuiGlobals.TextFG23, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateBoldOutlineFont(), sortOrder=2)
        self.goldStolenlbl.setTransparency(1)
        self.goldStolenlbl.hide()
        self.hasGoldlbl = DirectLabel(parent=self.healthBar, relief=None, pos=(0, 0,
                                                                               0.35), image=self.goldIcon, image_scale=0.5, image_pos=(0,
                                                                                                                                       0,
                                                                                                                                       0), sortOrder=2)
        self.hasGoldlbl.setTransparency(1)
        self.hasGoldlbl.hide()
        self.hasBNote = self.healthBar.attachNewNode('noteIndicator')
        self.bnoteBack = loader.loadModel('models/textureCards/skillIcons').find('**/pir_t_gui_can_moneyIcon').copyTo(self.hasBNote)
        self.hasBNote.setZ(0.35)
        self.hasBNote.setScale(0.6)
        self.hasBNote.hide()
        return

    def getHealthBarColor(self, health):
        return CannonDefenseGlobals.SHIP_HEALTH_COLORS[int(health / 100.0 * (len(CannonDefenseGlobals.SHIP_HEALTH_COLORS) - 1))]

    def setHealthState(self, health):
        DistributedNPCSimpleShip.setHealthState(self, health)
        self.healthBar['value'] = health
        self.healthBar['barColor'] = self.getHealthBarColor(health)

    def setCurrentState(self, state):
        if state == CannonDefenseGlobals.SHIP_STATE_STEALING:
            self.goldStolenlbl.show()
        elif state == CannonDefenseGlobals.SHIP_STATE_HASTREASURE:
            self.hasGoldlbl.show()
            self.goldStolenlbl.hide()
        elif state == CannonDefenseGlobals.SHIP_STATE_HASBNOTES:
            self.hasBNote.show()
            self.goldStolenlbl.hide()
        else:
            self.hasGoldlbl.hide()
            self.hasBNote.hide()
            self.goldStolenlbl.hide()

    def calculateLook(self):
        pass

    def playProjectileHitSfx(self, ammoSkillId, hitSail):
        if ammoSkillId in [InventoryType.DefenseCannonColdShotInWater, InventoryType.DefenseCannonSmokePowder]:
            return
        if ammoSkillId in self.specialHitSfx:
            sfx = self.specialHitSfx[ammoSkillId]
            base.playSfx(sfx, node=self, cutoff=2000)
            return
        DistributedNPCSimpleShip.playProjectileHitSfx(self, ammoSkillId, hitSail)

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker, itemEffects=[]):
        DistributedNPCSimpleShip.projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker, itemEffects)

    def sinkingBegin(self):
        self.healthBar.reparentTo(hidden)
        if len(self.flameEffects) > 0:
            self.isSinkingWhileOnFire = True
        DistributedNPCSimpleShip.sinkingBegin(self)

    def sinkingEnd(self):
        while len(self.flameEffects) > 0:
            effect = self.flameEffects.pop()
            effect.stopLoop()

        DistributedNPCSimpleShip.sinkingEnd(self)

    def addStatusEffect(self, effectId, attackerId, duration=0, timeLeft=0, timestamp=0, buffData=[0]):
        if effectId == WeaponGlobals.C_CANNON_DEFENSE_FIRE:
            self.addFireEffect(self.getModelRoot().getPos())
        if effectId == WeaponGlobals.C_CANNON_DEFENSE_ICE:
            base.playSfx(self.coldShotHitSfx, node=self, cutoff=2000)
        DistributedNPCSimpleShip.addStatusEffect(self, effectId, attackerId, duration, timeLeft, timestamp, buffData)

    def removeStatusEffect(self, effectId, attackerId):
        DistributedNPCSimpleShip.removeStatusEffect(self, effectId, attackerId)
        if effectId == WeaponGlobals.C_CANNON_DEFENSE_FIRE:
            if not self.isSinkingWhileOnFire:
                while len(self.flameEffects) > 0:
                    effect = self.flameEffects.pop()
                    effect.stopLoop()

    def addFireEffect(self, pos):
        fireEffect = ShipFire.getEffect()
        if fireEffect:
            fireEffect.reparentTo(self.getModelRoot())
            fireEffect.setPos(pos)
            fireEffect.setHpr(90, -15, 0)
            fireEffect.startLoop()
            fireEffect.setEffectScale(20.0)
            self.flameEffects.append(fireEffect)

    def playSharkAttack(self, pos):
        if self.sharkActor.getCurrentAnim() == None:
            self.sharkActor.wrtReparentTo(self.getModelRoot())
            self.sharkActor.setPos(self, pos)
            self.sharkActor.setScale(20)
            self.sharkActor.play('attack')
            sharkAttackEffect = None
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                effect = CannonSplash.getEffect()
                if effect:
                    effect.reparentTo(base.effectsRoot)
                    effect.setPos(self, pos)
                    effect.setZ(1)
                    effect.play()
                sharkAttackEffect = Func(self.playAttackEffect, pos)
            hprIvalShip = LerpHprInterval(self.getModelRoot(), duration=3, hpr=(0,
                                                                                0,
                                                                                -180))
            s1 = Sequence(Wait(0.75), hprIvalShip, Func(self.getModelRoot().stash))
            s2 = Sequence(Wait(0.75), sharkAttackEffect, Wait(0.5), sharkAttackEffect)
            self.sharkParallel = Parallel(s1, s2)
            self.sharkParallel.start()
            taskMgr.doMethodLater(self.sharkActor.getDuration('attack'), self.detachShark, self.uniqueName('playSharkAttack'), extraArgs=[])
        return

    def playAttackEffect(self, pos):
        effect = BulletEffect.getEffect()
        if effect:
            effect.reparentTo(base.effectsRoot)
            effect.setPos(self, pos)
            effect.loadObjects(6)
            effect.play()
        sfx = random.choice(self.sharkChompSfxs)
        base.playSfx(sfx, node=self.getModelRoot(), cutoff=2000)

    def detachShark(self):
        self.sharkActor.detachNode()

    def delete(self):
        if self.fader:
            self.fader.pause()
            self.fader = None
        DistributedNPCSimpleShip.delete(self)
        return

    def destroy(self):
        if self.goldStolenlbl:
            self.goldStolenlbl.destroy()
            self.goldStolenlbl = None
        if self.hasGoldlbl:
            self.hasGoldlbl.destroy()
            self.hasGoldlbl = None
        if self.textureCard:
            self.textureCard.removeNode()
            self.textureCard = None
            self.goldIcon = None
        if self.healthBar:
            self.healthBar.destroy()
        if self.sharkActor:
            self.sharkActor.cleanUp()
            self.sharkActor.removeNode()
        if self.sharkParallel:
            self.sharkParallel.pause()
            self.sharkParallel = None
        DistributedNPCSimpleShip.destroy(self)
        return

    def fadeIn(self, length):
        if self.fader:
            self.fader.finish()
            self.fader = None
        self.setTransparency(1)
        self.fader = Sequence(self.colorScaleInterval(length, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0)), Func(self.clearTransparency))
        self.fader.start()
        return

    def fadeOut(self, length):
        if self.fader:
            self.fader.finish()
            self.fader = None
        self.setTransparency(1)
        self.fader = Sequence(self.colorScaleInterval(length, Vec4(1, 1, 1, 0), Vec4(1, 1, 1, 1)), Func(self.hide), Func(self.clearTransparency))
        self.fader.start()
        return