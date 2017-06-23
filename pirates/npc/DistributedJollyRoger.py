from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from pirates.battle import DistributedBattleNPC
from pirates.npc import JollyRoger
from pirates.npc.Boss import Boss
from pirates.pirate import AvatarTypes
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.effects.JRTeleportEffect import JRTeleportEffect
import NPCSkeletonGameFSM
import random

class DistributedJollyRoger(DistributedBattleNPC.DistributedBattleNPC, JollyRoger.JollyRoger, Boss):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedJollyRoger')

    def __init__(self, cr):
        DistributedBattleNPC.DistributedBattleNPC.__init__(self, cr)
        Boss.__init__(self, cr)
        JollyRoger.JollyRoger.__init__(self)
        self.canPlaySfx = False
        self.recentlyPlayedDamage = False
        self.recentlyPlayedAttack = False

    def announceGenerate(self):
        DistributedBattleNPC.DistributedBattleNPC.announceGenerate(self)
        self.setupBoss(True, True)
        self.addBossEffect(AvatarTypes.Undead)
        if base.launcher.getPhaseComplete(5):
            self.canPlaySfx = True
            self.attackSounds = [loadSfx(SoundGlobals.SFX_MONSTER_JR_ATTACK_01), loadSfx(SoundGlobals.SFX_MONSTER_JR_ATTACK_03), loadSfx(SoundGlobals.SFX_MONSTER_JR_ATTACK_06), loadSfx(SoundGlobals.SFX_MONSTER_JR_ATTACK_07)]
            self.damageSounds = [
             loadSfx(SoundGlobals.SFX_MONSTER_JR_DAMAGE_01), loadSfx(SoundGlobals.SFX_MONSTER_JR_DAMAGE_03), loadSfx(SoundGlobals.SFX_MONSTER_JR_DAMAGE_06), loadSfx(SoundGlobals.SFX_MONSTER_JR_DAMAGE_07), loadSfx(SoundGlobals.SFX_MONSTER_JR_DAMAGE_10), loadSfx(SoundGlobals.SFX_MONSTER_JR_DAMAGE_13), loadSfx(SoundGlobals.SFX_MONSTER_JR_DAMAGE_14)]
            self.taunts = [
             loadSfx(SoundGlobals.SFX_MONSTER_JR_SMELL), loadSfx(SoundGlobals.SFX_MONSTER_JR_REALLY_IS_A_LAUGH), loadSfx(SoundGlobals.SFX_MONSTER_JR_FEAR_ME), loadSfx(SoundGlobals.SFX_MONSTER_JR_NEED_TO_FIND_SOMEONE_ELSE), loadSfx(SoundGlobals.SFX_MONSTER_JR_SUBMIT), loadSfx(SoundGlobals.SFX_MONSTER_JR_CHILDS_PLAY), loadSfx(SoundGlobals.SFX_MONSTER_JR_SUBMIT_TO_ME), loadSfx(SoundGlobals.SFX_MONSTER_JR_SO_MUCH_FUN), loadSfx(SoundGlobals.SFX_MONSTER_JR_FIGHT_BEFORE_MEAL), loadSfx(SoundGlobals.SFX_MONSTER_JR_WEAPON_NUISANCE), loadSfx(SoundGlobals.SFX_MONSTER_JR_BRING_OPPONENT), loadSfx(SoundGlobals.SFX_MONSTER_JR_DEAD), loadSfx(SoundGlobals.SFX_MONSTER_JR_ALL_YOU_GOT), loadSfx(SoundGlobals.SFX_MONSTER_JR_LAUGH_01), loadSfx(SoundGlobals.SFX_MONSTER_JR_MEET_YOUR_MAKER), loadSfx(SoundGlobals.SFX_MONSTER_JR_HOW_ITS_DONE), loadSfx(SoundGlobals.SFX_MONSTER_JR_SOULS_TO_DEVOUR), loadSfx(SoundGlobals.SFX_MONSTER_JR_EVERYONE_WILL_PAY), loadSfx(SoundGlobals.SFX_MONSTER_JR_QUIP_03), loadSfx(SoundGlobals.SFX_MONSTER_JR_QUIP_04), loadSfx(SoundGlobals.SFX_MONSTER_JR_LAUGH_02), loadSfx(SoundGlobals.SFX_MONSTER_JR_YOU_CALL), loadSfx(SoundGlobals.SFX_MONSTER_JR_ENJOYING), loadSfx(SoundGlobals.SFX_MONSTER_JR_IS_THAT_THE_BEST)]
        else:
            self.canPlaySfx = False

    def generate(self):
        DistributedBattleNPC.DistributedBattleNPC.generate(self)
        self.setInteractOptions(isTarget=False, allowInteract=False)

    def disable(self):
        self.removeBossEffect()
        taskMgr.remove(self.uniqueName('restoreDamageSounds'))
        taskMgr.remove(self.uniqueName('restoreAttackSounds'))
        DistributedBattleNPC.DistributedBattleNPC.disable(self)
        JollyRoger.JollyRoger.disable(self)

    def delete(self):
        DistributedBattleNPC.DistributedBattleNPC.delete(self)
        JollyRoger.JollyRoger.delete(self)

    def getNameText(self):
        return JollyRoger.JollyRoger.getNameText(self)

    def setAvatarType(self, avatarType):
        JollyRoger.JollyRoger.setAvatarType(self, avatarType)
        DistributedBattleNPC.DistributedBattleNPC.setAvatarType(self, avatarType)
        self.loadBossData(self.getUniqueId(), avatarType)

    def createGameFSM(self):
        self.gameFSM = NPCSkeletonGameFSM.NPCSkeletonGameFSM(self)

    def initializeDropShadow(self):
        JollyRoger.JollyRoger.initializeDropShadow(self)

    def setSpeed(self, forwardSpeed, rotateSpeed):
        if self.gameFSM.state == 'Jump':
            return
        JollyRoger.JollyRoger.setSpeed(self, forwardSpeed, rotateSpeed)

    def setHp(self, hp, quietly=0):
        DistributedBattleNPC.DistributedBattleNPC.setHp(self, hp, quietly)
        if self.glow:
            self.glow.adjustHeartColor(float(self.hp) / float(self.maxHp))

    def playOuch(self, skillId, ammoSkillId, targetEffects, attacker, pos, itemEffects=[], multihit=0, targetBonus=0, skillResult=0):
        if not self.recentlyPlayedDamage and self.canPlaySfx:
            self.recentlyPlayedDamage = True
            sfx = random.choice(self.damageSounds)
            base.playSfx(sfx, node=self, cutoff=60)
            taskMgr.doMethodLater(1.0, self.restoreDamageSounds, self.uniqueName('restoreDamageSounds'))
        DistributedBattleNPC.DistributedBattleNPC.playOuch(self, skillId, ammoSkillId, targetEffects, attacker, pos, itemEffects=itemEffects, multihit=multihit, targetBonus=targetBonus)

    def restoreDamageSounds(self, task):
        self.recentlyPlayedDamage = False

    def useTargetedSkill(self, skillId, ammoSkillId, skillResult, targetId, areaIdList, attackerEffects, targetEffects, areaIdEffects, itemEffects, timestamp, pos, charge=0, localSignal=0):
        if not self.recentlyPlayedAttack and self.canPlaySfx:
            self.recentlyPlayedAttack = True
            sfx = random.choice(self.attackSounds)
            base.playSfx(sfx, node=self, cutoff=60)
            taskMgr.doMethodLater(1.0, self.restoreAttackSounds, self.uniqueName('restoreAttackSounds'))
        DistributedBattleNPC.DistributedBattleNPC.useTargetedSkill(self, skillId, ammoSkillId, skillResult, targetId, areaIdList, attackerEffects, targetEffects, areaIdEffects, itemEffects, timestamp, pos, charge, localSignal)

    def restoreAttackSounds(self, task):
        self.recentlyPlayedAttack = False

    def play(self, *args, **kwArgs):
        JollyRoger.JollyRoger.play(self, *args, **kwArgs)

    def loop(self, *args, **kwArgs):
        JollyRoger.JollyRoger.loop(self, *args, **kwArgs)

    def pose(self, *args, **kwArgs):
        JollyRoger.JollyRoger.pose(self, *args, **kwArgs)

    def pingpong(self, *args, **kwArgs):
        JollyRoger.JollyRoger.pingpong(self, *args, **kwArgs)

    def stop(self, *args, **kwArgs):
        JollyRoger.JollyRoger.stop(self, *args, **kwArgs)

    def shouldNotice(self):
        return 0

    def getEnemyScale(self):
        return Boss.getEnemyScale(self)

    def getBossEffect(self):
        return Boss.getBossEffect(self)

    def getBossHighlightColor(self):
        return Boss.getBossHighlightColor(self)

    def _handleEnterAggroSphere(self, collEntry):
        pass

    def sendInvasionTaunt(self, number):
        if self.canPlaySfx:
            sfx = self.taunts[number]
            base.playSfx(sfx, node=self, cutoff=250)

    def setMonsterNameTag(self):
        color = '\x01red\x01'
        name = '%s  %s\x01smallCaps\x01%s%s\x02\x02' % (self.name, color, PLocalizer.Lv, PLocalizer.InvasionLv)
        self.getNameText()['text'] = name

    def getVictoryTrack(self):
        av = self
        animName = 'victory'
        duration = av.getDuration(animName)
        frames = av.getNumFrames(animName)

        def startSFX():
            sfx = self.getSfx('victory')
            if sfx:
                base.playSfx(sfx, node=self, cutoff=60)

        def stopSmooth():
            if self.smoothStarted:
                taskName = self.taskName('smooth')
                taskMgr.remove(taskName)
                self.smoothStarted = 0

        def startVFX():
            joint = av.find('**/def_root')
            if not joint.isEmpty():
                self.effectDummy = joint.attachNewNode('effectDummy')
            effect = JRTeleportEffect.getEffect()
            if effect:
                effect.reparentTo(self.effectDummy)
                posIval = LerpPosInterval(self.effectDummy, 3.5, Vec3(self.effectDummy.getX(), self.effectDummy.getY(), self.effectDummy.getZ()), startPos=Vec3(self.effectDummy.getX(), self.effectDummy.getY(), self.effectDummy.getZ() - 6.0))
                effect.setPos(Point3(0, 0, 3.5))
                effect.duration = 3.0
                effect.setScale(1, 1, 2)
                effect.setEffectScale(1.5)
                Sequence(Func(effect.play), posIval).start()

        victoryIval = Parallel(Sequence(Wait(3.0), Func(startVFX), Func(startSFX)), Sequence(Func(stopSmooth), Func(av.disableMixing), av.actorInterval(animName, startFrame=0.0, endFrame=frames - 1.0, blendOutT=0.0, blendInT=0.0), Func(av.pose, animName, frames - 2, blendT=0.0), Func(av.setTransparency, 1), LerpColorScaleInterval(self, 1.0, Vec4(0, 0, 0, 0), startColorScale=Vec4(1.0, 1.0, 1.0, 1.0)), Func(av.nametag3d.reparentTo, av), Func(self.hide, 0, PiratesGlobals.INVIS_DEATH), Func(av.clearColorScale), Func(av.clearTransparency)))
        return victoryIval

    def getDeathTrack(self):
        self.refreshStatusTray()
        if self.getHp() > 0:
            return self.getVictoryTrack()
        av = self
        animName = av.getDeathAnimName()
        duration = av.getDuration(animName)
        frames = av.getNumFrames(animName)

        def startSFX():
            sfx = self.getSfx('death')
            if sfx:
                base.playSfx(sfx, node=self, cutoff=60)

        def stopSmooth():
            if self.smoothStarted:
                taskName = self.taskName('smooth')
                taskMgr.remove(taskName)
                self.smoothStarted = 0

        def startVFX():
            from pirates.effects.MysticFire import MysticFire
            effect = MysticFire.getEffect()
            if effect:
                effect.reparentTo(render)
                effect.setPos(av, Point3(0, 0, -1))
                effect.setEffectScale(0.5)
                effect.play()

        def startGlow():
            geom = av.getGeomNode()
            model = loader.loadModel('models/effects/particleMaps')
            tex = model.find('**/effectWindBlur').findAllTextures()[0]
            geom.setTransparency(1)
            geom.setTexture(tex, 100)
            geom.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
            geom.setColorScale(VBase4(0.8, 1, 0.1, 1))
            self.animNode = NodePath('animNode')
            anim = LerpPosInterval(self.animNode, startPos=VBase3(0, 0, 0), pos=VBase3(0.0, -5.0, 0.0), duration=5.0)
            geom.setTexProjector(geom.findAllTextureStages()[0], self.animNode, NodePath())
            anim.start()

        deathIval = Parallel(Sequence(Func(startVFX), Wait(1.0), Func(startSFX), Func(startGlow)), Sequence(Func(stopSmooth), Func(av.disableMixing), av.actorInterval(animName, startFrame=0.0, endFrame=frames - 1.0, blendOutT=0.0, blendInT=0.0), Func(av.pose, animName, frames - 2, blendT=0.0), Func(av.setTransparency, 1), LerpColorScaleInterval(self, 1.0, Vec4(0, 0, 0, 0), startColorScale=Vec4(1.0, 1.0, 1.0, 1.0)), Func(av.nametag3d.reparentTo, av), Func(self.hide, 0, PiratesGlobals.INVIS_DEATH), Func(av.clearColorScale), Func(av.clearTransparency)))
        return deathIval

    def setInInvasion(self, value):
        self.inInvasion = value
        if value:
            taskMgr.doMethodLater(5, self.removeCollisions, self.uniqueName('removeCollisions'))
            self.setClipPlane(base.farCull)
            self.setMonsterNameTag()
            if base.config.GetBool('want-invasion-npc-minimap', 1):
                self.destroyMinimapObject()

    def _addInterruptedEffect(self, attackerId, duration):
        pass