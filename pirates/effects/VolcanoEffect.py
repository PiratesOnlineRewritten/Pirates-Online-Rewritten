from pandac.PandaModules import *
from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait, SoundInterval
from pirates.effects.VolcanoSmoke import VolcanoSmoke
from pirates.effects.EruptionSmoke import EruptionSmoke
from pirates.effects.LavaEruption import LavaEruption
from pirates.effects.LavaSplats import LavaSplats
from pirates.effects.CameraShaker import CameraShaker
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import random

class VolcanoEffect(NodePath):
    eruptionSfx = None

    def __init__(self):
        NodePath.__init__(self, 'VolcanoEffect')
        self.smoke = VolcanoSmoke()
        self.smoke.setEffectScale(1.0)
        self.smoke.reparentTo(self)
        self.eruptionSmoke = None
        self.eruption = None
        self.splats = None
        self.cameraShaker = None
        if not self.eruptionSfx:
            self.eruptionSfx = (
             loadSfx(SoundGlobals.SFX_FX_VOLCANO_ERUPT),)
        self.inEditor = hasattr(base, 'pe')
        return

    def startLavaEruption(self):
        self.stopLavaEruption()
        duration = random.randint(10, 20)
        base.playSfx(self.eruptionSfx[0], node=self, cutoff=5000)
        self.eruption = LavaEruption()
        self.eruption.duration = duration
        self.eruption.setEffectScale(1.0)
        self.eruption.reparentTo(self)
        self.eruption.play()
        if self.inEditor or base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
            self.cameraShaker = CameraShaker()
            self.cameraShaker.reparentTo(self)
            self.cameraShaker.shakeSpeed = 0.05
            self.cameraShaker.shakePower = 0.2
            self.cameraShaker.scalePower = True
            self.cameraShaker.numShakes = duration * 10
            self.cameraShaker.play(2200.0)
        if self.inEditor or base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
            self.eruptionSmoke = EruptionSmoke()
            self.eruptionSmoke.duration = duration
            self.eruptionSmoke.reparentTo(self)
            self.eruptionSmoke.setEffectScale(1.0)
            self.eruptionSmoke.play()
            self.splats = LavaSplats()
            self.splats.duration = duration
            self.splats.setEffectScale(1.0)
            self.splats.reparentTo(self)
            self.splats.play()
        taskMgr.doMethodLater(duration + 10.0, self.stopLavaEruption, 'stopLavaEruptionTask')

    def stopLavaEruption(self, task=None):
        if self.eruption:
            self.eruption.destroy()
            self.eruption = None
        if self.splats:
            self.splats.destroy()
            self.splats = None
        if self.eruptionSmoke:
            self.eruptionSmoke.destroy()
            self.eruptionSmoke = None
        return

    def enable(self):
        self.smoke.enableEffect()

    def disable(self):
        self.smoke.disableEffect()

    def destroy(self):
        self.disable()
        taskMgr.remove('stopLavataEruptionTask')
        if self.smoke:
            self.smoke.cleanUpEffect()
            self.smoke = None
        self.stopLavaEruption()
        return