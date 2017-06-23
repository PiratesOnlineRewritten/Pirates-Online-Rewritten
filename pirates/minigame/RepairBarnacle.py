import random
from pandac.PandaModules import Point3
from direct.gui.DirectGui import DirectFrame, DirectLabel
from direct.fsm import FSM
from direct.interval.IntervalGlobal import *
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import RepairGlobals
MIN_SCALE = 1.5
MAX_SCALE_ADD = 1.0
MAX_SCRUB_AMT = 20.0

class RepairBarnacle(DirectFrame, FSM.FSM):
    barnacleFallSounds = None

    def __init__(self, name, barnacleGeom):
        self.config = RepairGlobals.Careening
        DirectFrame.__init__(self, parent=None, relief=None)
        self.barnacleGeom = barnacleGeom
        FSM.FSM.__init__(self, 'Barnacle_%sFSM' % name)
        self._initAudio()
        self._initVars()
        self._initGUI()
        return

    def _initVars(self):
        self.heat = 0.0
        self.hp = 100
        self.maxHP = 100
        self.currentShake = None
        self.fallingAnim = None
        return

    def _initAudio(self):
        if not self.barnacleFallSounds:
            RepairBarnacle.barnacleFallSounds = (
             loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_CAREEN_COMPLETE1), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_CAREEN_COMPLETE2), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_CAREEN_COMPLETE3), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_CAREEN_COMPLETE4), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_CAREEN_COMPLETE5))

    def _initGUI(self):
        self.barnacleGeom.reparentTo(self)
        self.barnacleGeom.setScale(0.6)
        self.barnacleGeom.setR(random.random() * 360)
        if self.config.showBarnacleHP:
            self.hpLabel = DirectLabel(text='', scale=(0.025, 0.025, 0.025), pos=(0.0, 0.0, -0.01), textMayChange=1, parent=self)

    def destroy(self):
        if self.currentShake is not None:
            self.currentShake.clearToInitial()
            self.currentShake = None
        del self.currentShake
        if self.fallingAnim is not None:
            self.fallingAnim.clearToInitial()
            self.fallingAnim = None
        del self.fallingAnim
        self.cleanup()
        if self.config.showBarnacleHP:
            self.hpLabel.destroy()
            del self.hpLabel
        DirectFrame.destroy(self)
        self.barnacleGeom.removeNode()
        del self.barnacleGeom
        return

    def setMaxHP(self, newMaxHP, globalMaxHP):
        self.maxHP = newMaxHP
        self.globalMaxHP = globalMaxHP

    def setHP(self, newHP):
        self.hp = newHP
        if self.config.showBarnacleHP:
            self.hpLabel['text'] = '%i' % self.hp
            self.hpLabel.setText()
        if self.hp <= 0.0:
            self.hp = 0.0
            self.request('Falling')
        self.setScale(self.hp * MAX_SCALE_ADD / self.globalMaxHP + MIN_SCALE)

    def reduceHP(self, pushDir, powerScale):
        amount = pushDir.length()
        pushDir.normalize()
        self.heat = min(1.0, self.heat + amount)
        amount *= 50
        if amount > MAX_SCRUB_AMT:
            amount = MAX_SCRUB_AMT
        amount *= powerScale
        newHP = self.hp - amount
        self.setHP(newHP)
        if self.currentShake is None:
            self.currentShake = Sequence(LerpPosInterval(self, duration=0.03, pos=(self.getX() - pushDir[0] * (0.01 + amount / 1000.0), self.getY(), self.getZ() - pushDir[1] * (0.01 + amount / 1000.0)), blendType='easeIn'), LerpPosInterval(self, duration=0.06, pos=(self.getX(), self.getY(), self.getZ()), blendType='easeOut'), LerpPosInterval(self, duration=0.04, pos=(self.getX() + pushDir[0] * (0.0075 + amount / 2000.0), self.getY(), self.getZ() + pushDir[1] * (0.005 + amount / 2000.0)), blendType='easeIn'), LerpPosInterval(self, duration=0.08, pos=(self.getX(), self.getY(), self.getZ()), blendType='easeOut'), Func(self.clearCurrentShake))
            self.currentShake.start()
        return

    def checkCollision(self, mousePosition):
        sld = Point3(mousePosition.getX(), 0.0, mousePosition.getY()) - self.getPos(render2d)
        return self.getCurrentOrNextState() == 'Idle' and sld.length() < self.config.barnacleRadius * self.getScale().getX()

    def clearCurrentShake(self):
        self.currentShake = None
        return

    def enterIdle(self):
        visibleIndex = random.uniform(0, self.barnacleGeom.getNumChildren() - 1)
        for i in range(self.barnacleGeom.getNumChildren() - 1):
            self.barnacleGeom.getChild(i).unstash()

        newHP = self.maxHP
        self.heat = 0.0
        self.setHP(newHP)
        self.unstash()

    def exitIdle(self):
        pass

    def enterFalling(self):
        if self.currentShake is not None:
            self.currentShake.finish()
        sound = random.choice(self.barnacleFallSounds)
        sound.play()
        self.fallingAnim = Sequence(LerpPosInterval(self, duration=2.0, pos=(self.getX(), self.getY(), self.getZ() - 2.0), blendType='easeIn'), Func(self.request, 'Clean'))
        self.fallingAnim.start()
        return

    def exitFalling(self):
        self.stash()

    def enterClean(self):
        pass

    def exitClean(self):
        pass