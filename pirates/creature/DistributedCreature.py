from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.battle.DistributedBattleNPC import DistributedBattleNPC
from pirates.piratesbase import PLocalizer
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals
from pirates.creature.Alligator import Alligator
from pirates.creature.Bat import Bat
from pirates.creature.Chicken import Chicken
from pirates.creature.Crab import Crab
from pirates.creature.Dog import Dog
from pirates.creature.FlyTrap import FlyTrap
from pirates.creature.Monkey import Monkey
from pirates.creature.Pig import Pig
from pirates.creature.Rooster import Rooster
from pirates.creature.Scorpion import Scorpion
from pirates.creature.Seagull import Seagull
from pirates.creature.Raven import Raven
from pirates.creature.Stump import Stump
from pirates.creature.Wasp import Wasp
from pirates.kraken.Grabber import Grabber
from pirates.kraken.Holder import Holder
from pirates.kraken.KrakenBody import KrakenBody
from pirates.kraken.Head import Head as KrakenHead
from pirates.pirate import AvatarTypes
from pirates.battle import EnemyGlobals
from pirates.effects.Immolate import Immolate
from pirates.effects.JRDeathBlast import JRDeathBlast
from pirates.effects.JRDeath import JRDeath
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import random
CreatureTypes = {AvatarTypes.Crab: Crab,AvatarTypes.RockCrab: Crab,AvatarTypes.StoneCrab: Crab,AvatarTypes.GiantCrab: Crab,AvatarTypes.CrusherCrab: Crab,AvatarTypes.Chicken: Chicken,AvatarTypes.Rooster: Rooster,AvatarTypes.Pig: Pig,AvatarTypes.Dog: Dog,AvatarTypes.Seagull: Seagull,AvatarTypes.Raven: Raven,AvatarTypes.Stump: Stump,AvatarTypes.TwistedStump: Stump,AvatarTypes.FlyTrap: FlyTrap,AvatarTypes.RancidFlyTrap: FlyTrap,AvatarTypes.AncientFlyTrap: FlyTrap,AvatarTypes.Scorpion: Scorpion,AvatarTypes.DireScorpion: Scorpion,AvatarTypes.DreadScorpion: Scorpion,AvatarTypes.Alligator: Alligator,AvatarTypes.BayouGator: Alligator,AvatarTypes.BigGator: Alligator,AvatarTypes.HugeGator: Alligator,AvatarTypes.Bat: Bat,AvatarTypes.RabidBat: Bat,AvatarTypes.VampireBat: Bat,AvatarTypes.FireBat: Bat,AvatarTypes.Wasp: Wasp,AvatarTypes.KillerWasp: Wasp,AvatarTypes.AngryWasp: Wasp,AvatarTypes.SoldierWasp: Wasp,AvatarTypes.Monkey: Monkey,AvatarTypes.GrabberTentacle: Grabber,AvatarTypes.HolderTentacle: Holder,AvatarTypes.Kraken: KrakenBody,AvatarTypes.KrakenHead: KrakenHead}

class DistributedCreature(DistributedBattleNPC):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCreature')

    def __init__(self, cr):
        DistributedBattleNPC.__init__(self, cr)
        self.creature = None
        self.creatureTypeEffect = None
        self.needNoticeGroundTracking = 1
        self.sfxList = []
        return

    def generate(self):
        DistributedBattleNPC.generate(self)
        self.customInteractOptions()

    def announceGenerate(self):
        DistributedBattleNPC.announceGenerate(self)
        self.addActive()

    def disable(self):
        self.removeActive()
        DistributedBattleNPC.disable(self)

    def delete(self):
        if self.creature and self.creatureTypeEffect:
            self.creatureTypeEffect.stopLoop()
        if self.creature:
            self.creature.detachNode()
            self.creature.delete()
            self.creature = None
        self.sfxList = []
        DistributedBattleNPC.delete(self)
        return

    def setupCreature(self, avatarType):
        if not self.creature:
            self.creature = CreatureTypes[avatarType.getNonBossType()]()
            self.creature.setAvatarType(avatarType)
            self.creature.reparentTo(self.getGeomNode())
            self.motionFSM.setAnimInfo(self.getAnimInfo('LandRoam'))
            self.nametag3d.setName('empty_use_self_dot_creature_dot_nametag3d_instead')
            self.creature.nametag3d.reparentTo(self.nametag3d)
            if base.options.getCharacterDetailSetting() == 0:
                if self.creature.hasLOD():
                    self.creature.getLODNode().forceSwitch(2)
            if self.avatarType.isA(AvatarTypes.FireBat):
                geom = self.creature.getGeomNode()
                geom.setTransparency(1)
                geom.setBin('pre-additive', 4)
                geom.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                geom.setColorScale(VBase4(1.0, 0.3, 0.3, 1))
                from pirates.effects.FireBat import FireBat
                self.creatureTypeEffect = FireBat.getEffect()
                if self.creatureTypeEffect:
                    self.creatureTypeEffect.reparentTo(geom)
                    self.creatureTypeEffect.setPos(0, 0.0, 4.5)
                    self.creatureTypeEffect.startLoop()
                self.creature.nametagOffset = 5.0
                self.adjustNametag3d()

    def loop(self, *args, **kw):
        return self.creature and self.creature.loop(*args, **kw)

    def play(self, *args, **kw):
        return self.creature and self.creature.play(*args, **kw)

    def pingpong(self, *args, **kw):
        return self.creature and self.creature.pingpong(*args, **kw)

    def pose(self, *args, **kw):
        return self.creature and self.creature.pose(*args, **kw)

    def stop(self, *args, **kw):
        return self.creature and self.creature.stop(*args, **kw)

    def setPlayRate(self, *args, **kw):
        return self.creature and self.creature.setPlayRate(*args, **kw)

    def getPlayRate(self, *args, **kw):
        return self.creature and self.creature.getPlayRate(*args, **kw)

    def getDuration(self, *args, **kw):
        return self.creature and self.creature.getDuration(*args, **kw)

    def actorInterval(self, *args, **kw):
        return self.creature and self.creature.actorInterval(*args, **kw)

    def getAnimControl(self, *args, **kw):
        return self.creature and self.creature.getAnimControl(*args, **kw)

    def getOuchSfx(self):
        return self.creature and self.creature.sfx.get('pain')

    def getSfx(self, *args, **kw):
        return self.creature and self.creature.getSfx(*args, **kw)

    @report(types=['module', 'args'], dConfigParam='nametag')
    def initializeNametag3d(self):
        return self.creature and self.creature.initializeNametag3d()

    @report(types=['module', 'args'], dConfigParam='nametag')
    def getNameText(self):
        return self.creature and self.creature.getNameText()

    @report(types=['module', 'args'], dConfigParam='nametag')
    def setName(self, name):
        DistributedBattleNPC.setName(self, name)
        self.refreshStatusTray()
        self.creature.nametag.setDisplayName('        ')
        nameText = self.getNameText()
        if nameText:
            if self.isNpc:
                self.accept('weaponChange', self.setMonsterNameTag)
                self.setMonsterNameTag()
                from pirates.battle import EnemyGlobals
                color2 = EnemyGlobals.getNametagColor(self.avatarType)
                if self.isBoss():
                    color2 = (0.95, 0.1, 0.1, 1)
                nameText['fg'] = color2

    @report(types=['module', 'args'], dConfigParam='nametag')
    def setMonsterNameTag(self):
        from pirates.piratesbase import PLocalizer
        if self.isInInvasion():
            name = self.name
        elif self.level:
            color = self.cr.battleMgr.getExperienceColor(base.localAvatar, self)
            name = '%s  %s\x01smallCaps\x01%s%s\x02\x02' % (self.name, color, PLocalizer.Lv, self.level)
        else:
            name = self.name
        self.getNameText()['text'] = name

    @report(types=['module', 'args'], dConfigParam='nametag')
    def addActive(self):
        if self.creature:
            self.creature.addActive()
            self.creature.nametag.setName(' ')

    def removeActive(self):
        if self.creature:
            self.creature.removeActive()

    def customInteractOptions(self):
        self.setInteractOptions(isTarget=False, allowInteract=False)

    @report(types=['module', 'args'], dConfigParam='nametag')
    def setAvatarType(self, avatarType):
        DistributedBattleNPC.setAvatarType(self, avatarType)
        self.setupCreature(avatarType)

    def setLevel(self, level):
        DistributedBattleNPC.setLevel(self, level)
        self.creature.setLevel(level)

    def getAnimInfo(self, *args, **kw):
        return self.creature and self.creature.getAnimInfo(*args, **kw)

    def freezeShadow(self, *args, **kw):
        self.creature.shadowPlacer.off()
        self.freezeTask = None
        return

    def setHeight(self, height):
        self.height = height
        self.creature.adjustNametag3d(self.scale)
        if self.collTube:
            self.collTube.setPointB(0, 0, height)
            if self.collNodePath:
                self.collNodePath.forceRecomputeBounds()
        if self.battleTube:
            self.battleTube.setPointB(0, 0, max(5.0, height))

    def shouldNotice(self):
        return self.creature.shouldNotice()

    def endShuffle(self):
        self.creature.endShuffle()

    def disableMixing(self):
        self.creature.disableMixing()

    def enableReducedMixing(self):
        self.creature.enableReducedMixing()

    def enableMixing(self):
        self.creature.enableMixing()

    def getDeathTrack(self):
        if self.avatarType.isA(AvatarTypes.FireBat):
            av = self.creature
            animName = av.getDeathAnimName()
            duration = av.getDuration(animName)
            frames = av.getNumFrames(animName)
            delay = 0.0

            def startSFX():
                sfx = loadSfx(SoundGlobals.SFX_SKILL_HELLFIRE_HIT)
                pitchRate = 0.8 + random.random() * 0.4
                sfx.setPlayRate(pitchRate)
                si = SoundInterval(sfx, node=self, volume=1.0, seamlessLoop=False, cutOff=150.0)
                self.sfxList.append(si)
                si.start()

            def stopSmooth():
                if self.smoothStarted:
                    taskName = self.taskName('smooth')
                    taskMgr.remove(taskName)
                self.smoothStarted = 0

            def startVFX():
                offset = Vec3(0.0, 2.0, 5.0)
                root = av
                explosionEffect = ExplosionFlip.getEffect()
                if explosionEffect:
                    explosionEffect.reparentTo(render)
                    explosionEffect.setPos(root, offset)
                    explosionEffect.setScale(0.5)
                    explosionEffect.play()
                if self.creatureTypeEffect:
                    self.creatureTypeEffect.stopLoop()
                    self.creatureTypeEffect = None
                return

            def startVFX2():
                effectScale = EnemyGlobals.getEffectScale(self)
                offset = Vec3(0.0, 2.0, 5.0)
                root = av
                deathBlast = Immolate.getEffect()
                if deathBlast:
                    deathBlast.reparentTo(render)
                    deathBlast.setPos(root, offset)
                    deathBlast.setScale(effectScale)
                    deathBlast.play()

            deathIval = Parallel(Func(stopSmooth), Func(self.setTransparency, 1), Sequence(Func(startVFX), Wait(0.2), Func(startVFX2)), Sequence(Func(startSFX), Wait(0.25), Func(startSFX)), av.actorInterval(animName, blendOutT=0.0), Sequence(Wait(duration / 2.0), LerpColorScaleInterval(av, duration / 2.0, Vec4(1, 1, 1, 0), startColorScale=Vec4(1)), Func(self.hide, 0, PiratesGlobals.INVIS_DEATH), Func(self.clearColorScale), Func(self.clearTransparency)))
            return deathIval
        else:
            return DistributedBattleNPC.getDeathTrack(self)

    def getSpawnTrack(self):
        if self.avatarType.isA(AvatarTypes.FireBat):
            if self.getAnimControl('intro'):
                introIval = self.actorInterval('intro')
            else:
                fadeIn = LerpFunctionInterval(self.setAlphaScale, 2.0, fromData=0.0, toData=1.0)
                introIval = Sequence(Func(self.setTransparency, 1), fadeIn, Func(self.clearTransparency), Func(self.clearColorScale))
                introIval.append(Func(self.ambushIntroDone))
                return introIval
        else:
            DistributedBattleNPC.getSpawnTrack(self)