from direct.directnotify import DirectNotifyGlobal
from pirates.creature import DistributedCreature
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals
from otp.otpbase import OTPRender
from direct.showbase import PythonUtil
from pirates.uberdog.UberDogGlobals import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
import random

class DistributedSeagull(DistributedCreature.DistributedCreature):

    def __init__(self, cr):
        DistributedCreature.DistributedCreature.__init__(self, cr)
        self.battleCollisionBitmask = PiratesGlobals.WallBitmask | PiratesGlobals.TargetBitmask
        OTPRender.renderReflection(False, self, 'p_animal', None)
        self.isFlying = 0
        self.flyIval = None
        self.maxSwingX = 35.0
        self.swingCycles = 7
        self.stepSwingX = 7.0
        self.maxHeight = 50.0
        self.heightCycles = 5
        self.stepHeight = 10.0
        self.stepVelocity = 0.0
        self.stepVelStep = 1.0
        self.flightCount = 0
        self.minFlightCount = 7
        self.flightData = (6.0, 20.0)
        self.flightForward = 20.0
        self.flapLoopIval = None
        self.cawLoopIval = None
        return

    def customInteractOptions(self):
        self.setInteractOptions(proximityText=None, allowInteract=False)
        return

    def showHpMeter(self):
        pass

    def isBattleable(self):
        return 0

    def initializeBattleCollisions(self):
        pass

    def announceGenerate(self):
        DistributedCreature.DistributedCreature(self)
        self.firstCaw = 1
        self.doCawSoundLoop()
        self.stopFly()
        self.setH(0)

    def disable(self):
        if self.flapLoopIval:
            self.flapLoopIval.pause()
            self.flapLoopIval = None
        if self.cawLoopIval:
            self.cawLoopIval.pause()
            self.cawLoopIval = None
        DistributedCreature.DistributedCreature.disable(self)
        return

    def getMinimapObject(self):
        return None

    def firstNoticeLocalAvatar(self):
        base.nav = self
        if self.isMovingDontNotice:
            return
        self.hasTurnedToNotice = 0
        self.localAvatarHasBeenNoticed = 1

    def startFlying(self):
        self.isFlying = 1
        self.doFly()
        self.doFlapSoundLoop()

    def doFlapSoundLoop(self):
        if self.flapLoopIval:
            self.flapLoopIval.pause()
            self.flapLoopIval = None
        self.flapLoopIval = Sequence()
        sound = loader.loadSfx('audio/sfx_bird_wings.mp3')
        sound.setPlayRate(0.9 + random.random() * 0.2)
        soundIval = SoundInterval(sound, node=self.creature, volume=0.5, seamlessLoop=False, cutOff=150.0)
        self.flapLoopIval.append(soundIval)
        self.flapLoopIval.start()
        return

    def doCawSoundLoop(self):
        if self.cawLoopIval:
            self.cawLoopIval.pause()
            self.cawLoopIval = None
        self.cawLoopIval = Sequence()
        soundFile = random.choice(['audio/seagull_1_fix.mp3', 'audio/seagull_2_fix.mp3', 'audio/seagull_3_fix.mp3'])
        sound = loader.loadSfx(soundFile)
        pitchRate = 0.9 + random.random() * 0.2
        volumeCaw = 0.5 + random.random() * 0.5
        sound.setPlayRate(pitchRate)
        numCaws = random.choice([0.0, 0.5, 1.0, 1.5])
        if self.firstCaw:
            self.firstCaw = 0
            self.cawLoopIval.append(Wait(random.random() * 10.0 + 10.0))
        else:
            soundIval = SoundInterval(sound, node=self.creature, volume=volumeCaw, seamlessLoop=False, cutOff=250.0)
            self.cawLoopIval.append(soundIval)
            self.cawLoopIval.append(Wait(random.random() * 60.0 + 10.0))
        self.cawLoopIval.append(Func(self.doCawSoundLoop))
        self.cawLoopIval.start(numCaws * pitchRate)
        return

    def stopFly(self):
        if self.flyIval:
            self.flyIval.finish()
        if self.creature == None:
            return
        self.loop('groom_idle', blendDelay=0.15)
        self.isFlying = 0
        self.flightCount = 0
        self.setH(self.getH() % 360)
        self.flyIval = LerpHprInterval(self.creature, duration=1.0, hpr=Vec3(0, 0, 0))
        self.flyIval.start()
        return

    def doFly(self):
        if self.creature == None:
            return
        self.flyIval = Sequence()
        flightMotion = Parallel()
        swingXOld = self.creature.getX()
        if self.localAvatarHasBeenNoticed or self.flightCount < self.minFlightCount:
            loopAnim = random.choice(('flying', 'run', 'flying'))
            self.loop(loopAnim, blendDelay=0.15)
            swingX = min(swingXOld + self.stepSwingX, self.maxSwingX)
            heightOld = self.creature.getZ()
            self.stepVelocity = max(self.stepHeight, self.stepVelocity + self.stepVelStep)
            heightC = min(heightOld + self.stepVelocity, self.maxHeight)
            durationMove = max(2.0, 2.0 + abs(swingX * 0.2))
            goingUp = 1
        else:
            loopAnim = random.choice(('flying', 'run', 'run'))
            self.loop(loopAnim, blendDelay=0.15)
            self.loop('run', blendDelay=0.15)
            self.stepVelocity = max(self.stepVelStep, self.stepVelocity - self.stepVelStep)
            heightOld = self.creature.getZ()
            heightC = max(heightOld - self.stepVelocity, 0.0)
            heightProp = heightC / self.maxHeight
            swingX = heightProp * self.maxHeight
            durationMove = max(2.0, 2.0 + abs(swingXOld * 0.2))
            goingUp = 0
        out = 0.0
        clipH = self.getH() % 1080
        self.setH(clipH)
        oldHpr = Vec3(clipH, 0.0, 0.0)
        newHpr = Vec3(clipH + 360.0, 0.0, 0.0)
        if heightC <= self.flightData[0]:
            newHpr = Vec3(clipH + 180.0, 0.0, 0.0)
        if heightC <= self.flightData[1]:
            if goingUp:
                self.loop('flying', blendDelay=0.15, rate=1.5)
            else:
                self.loop('flying', blendDelay=0.15, rate=1.0)
        if heightC <= 1.0 or goingUp == 0:
            out = 0.0
        else:
            if heightC <= self.flightData[0]:
                out = -5.0
            else:
                out = 5.0
            turnAround = LerpHprInterval(self, duration=durationMove, startHpr=oldHpr, hpr=newHpr)
            newPos = Vec3(swingX, out, heightC)
            moveOut = LerpPosInterval(self.creature, duration=durationMove, pos=newPos)
            pitchAmount = 1.0 - min(heightC / (self.stepHeight * 3.0), 1.0)
            pitchHpr = (90 * pitchAmount, 70.0 * pitchAmount, -45 * pitchAmount)
            pitchUp = LerpHprInterval(self.creature, duration=durationMove, hpr=pitchHpr)
            flightMotion.append(turnAround)
            flightMotion.append(moveOut)
            flightMotion.append(pitchUp)
            self.flyIval.append(flightMotion)
            if self.localAvatarHasBeenNoticed or heightC > 0.0:
                self.flyIval.append(Func(self.doFly))
            self.flyIval.append(Func(self.stopFly))
        self.flyIval.start()
        self.flightCount += 1
        return

    def endNotice(self):
        self.doneThreat = 0
        self.localAvatarHasBeenNoticed = 0

    def abortNotice(self):
        if self.noticeIval:
            self.noticeFlag = 1
            self.noticeIval.pause()
            self.noticeFlag = 0
            self.doneThreat = 0
        if self.flyIval:
            self.flyIval.pause()
        self.noticeIval = None
        self.flyIval = None
        self.localAvatarHasBeenNoticed = 0
        return

    def noticeLocalAvatar(self):
        if self.isInInvasion():
            return
        if not self.shouldNotice() or self.isMovingDontNotice or self.noticeFlag:
            return
        if self.getDistance(localAvatar) > self.getEffectiveNoticeDistance() + 2.0 or not self.stateOkayForNotice():
            if self.gameFSM:
                pass
            self.endNotice()
            return
        heading = self.getHpr()
        self.headsUp(localAvatar)
        if self.needNoticeGroundTracking:
            self.trackTerrain()
        noticeHeading = self.getHpr()
        self.setHpr(heading)
        angle = PythonUtil.fitDestAngle2Src(heading[0], noticeHeading[0])
        if self.needNoticeGroundTracking:
            newHpr = Vec3(angle, noticeHeading[1], noticeHeading[2])
        else:
            newHpr = Vec3(angle, heading[1], heading[2])
        noticeDif = abs(angle - heading[0])
        turnAnim = self.getTurnAnim(noticeDif)
        if self.noticeIval:
            self.noticeFlag = 1
            self.noticeIval.finish()
            self.noticeFlag = 0
            self.noticeIval = None
        self.noticeIval = Sequence(Wait(self.noticeSpeed), Func(self.noticeLocalAvatar))
        self.noticeIval.start()
        if not self.isFlying:
            self.startFlying()
        return
        if self.getDistance(localAvatar) > self.closeNoticeDistance + 2.0:
            if self.hasTurnedToNotice:
                self.endNotice()
            else:
                self.noticeIval = Sequence(Wait(self.noticeSpeed), Func(self.noticeLocalAvatar))
                self.noticeIval.start()
        elif abs(noticeDif) > 15.0 and self.shouldTurnToNotice:
            if turnAnim:
                self.noticeIval = Sequence(Func(self.startShuffle, turnAnim), LerpHprInterval(self, duration=self.noticeSpeed, hpr=newHpr), Func(self.midShuffle), Wait(self.noticeSpeed), Func(self.endShuffle), Func(self.noticeLocalAvatar))
                self.noticeIval.start()
            else:
                self.noticeIval = Sequence(LerpHprInterval(self, duration=self.noticeSpeed, hpr=newHpr), Wait(self.noticeSpeed), Func(self.noticeLocalAvatar))
                self.noticeIval.start()
            self.doNoticeFX()
            self.hasTurnedToNotice = 1
        elif abs(noticeDif) < 45.0:
            duration = self.presetNoticeAnimation()
            if duration == None or self.doneThreat == 1:
                duration = self.noticeSpeed
            self.noticeIval = Sequence(Func(self.startNoticeLoop), Func(self.playNoticeAnim), Wait(duration), Func(self.endNoticeLoop), Func(self.noticeLocalAvatar))
            self.noticeIval.start()
            self.doNoticeFX()
        return