from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesgui.GameOptions import Options
from pirates.effects.Fire import Fire
from pirates.effects.FireSparks import FireSparks
from pirates.effects.FireSplats import FireSplats
from pirates.effects.HeavySmoke import HeavySmoke
from pirates.effects.FeastSmoke import FeastSmoke
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class FeastFire(NodePath):

    def __init__(self, effectParent=None):
        NodePath.__init__(self, uniqueName('FeastFire'))
        self._fire = Fire()
        self._splats = FireSplats()
        self._sparks = FireSparks()
        self._smoke = HeavySmoke()
        self._feastSmoke = FeastSmoke()
        self.fireSfx = loadSfx(SoundGlobals.SFX_FX_FIRE_LOOP)
        self.fireSfxIval = None
        if self._fire:
            self._fire.reparentTo(self)
            self._fire.effectScale = 1.0
        if self._splats:
            self._splats.reparentTo(self)
            self._splats.effectScale = 1.0
        if self._sparks:
            self._sparks.reparentTo(self)
            self._sparks.setPos(0, 0, 3)
        if self._smoke:
            self._smoke.reparentTo(self)
        if self._feastSmoke:
            self._feastSmoke.reparentTo(self)
        return

    def setCustomSettings(self):
        if self._fire:
            self._fire.setScale(VBase3(1.5, 1, 1))
            self._fire.p0.factory.setLifespanBase(1.25)
            self._fire.p0.factory.setLifespanSpread(0.5)
            self._fire.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 15.0))
            self._fire.p0.emitter.setRadius(4.0)
        if self._splats:
            self._splats.setScale(VBase3(1.5, 1, 1))
            self._splats.p0.factory.setLifespanBase(1.3)
            self._splats.p0.factory.setLifespanSpread(0.5)
            self._splats.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 18.0))
            self._splats.p0.emitter.setRadius(4.0)
        if self._sparks:
            self._sparks.setScale(VBase3(1.25, 1, 1))
            self._sparks.p0.factory.setLifespanBase(1.5)
            self._sparks.p0.factory.setLifespanSpread(0.5)
            self._sparks.p0.emitter.setOffsetForce(Vec3(2.0, 2.0, 24.0))
            self._sparks.p0.emitter.setRadius(6.0)
        if self._smoke:
            self._smoke.setScale(VBase3(1.25, 1, 1))
            self._smoke.p0.emitter.setOffsetForce(Vec3(2.0, 2.0, 30.0))
            self._smoke.p0.emitter.setRadius(5.0)

    def startMainEffects(self):
        effectSetting = base.options.getSpecialEffectsSetting()
        if self._fire:
            self._fire.enable()
        if self._splats and effectSetting >= base.options.SpecialEffectsHigh:
            self._splats.enable()
        if self._sparks and effectSetting >= base.options.SpecialEffectsMedium:
            self._sparks.enable()
        if self._smoke:
            self._smoke.enable()
        if self.fireSfx:
            self.fireSfxIval = SoundInterval(self.fireSfx, node=self, seamlessLoop=False)
            self.fireSfxIval.loop()

    def stopMainEffects(self):
        if self._fire:
            self._fire.disable()
        if self._splats:
            self._splats.disable()
        if self._sparks:
            self._sparks.disable()
        if self._smoke:
            self._smoke.disable()
        if self.fireSfxIval:
            self.fireSfxIval.finish()
            self.fireSfxIval = None
        return

    def startFarEffects(self):
        if self._feastSmoke:
            self._feastSmoke.enable()
            self._feastSmoke.accelerate()

    def stopFarEffects(self):
        if self._feastSmoke:
            self._feastSmoke.disable()

    def stopLoop(self):
        if self._fire:
            self._fire.disable()
        if self._splats:
            self._splats.disable()
        if self._sparks:
            self._sparks.disable()
        if self._smoke:
            self._smoke.disable()
        if self._feastSmoke:
            self._feastSmoke.disable()
        if self.fireSfxIval:
            self.fireSfxIval.finish()
            self.fireSfxIval = None
        return

    def destroy(self):
        if self._fire:
            self._fire.destroy()
        if self._splats:
            self._splats.destroy()
        if self._sparks:
            self._sparks.destroy()
        if self._smoke:
            self._smoke.destroy()
        if self._feastSmoke:
            self._feastSmoke.destroy()
        if self.fireSfxIval:
            self.fireSfxIval.finish()
            self.fireSfxIval = None
        del self._fire
        del self._splats
        del self._sparks
        del self._smoke
        del self._feastSmoke
        del self.fireSfx
        return