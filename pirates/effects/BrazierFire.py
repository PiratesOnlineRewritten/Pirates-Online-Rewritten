from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesgui.GameOptions import Options
from pirates.effects.LightFire import LightFire
from pirates.effects.GentleSmoke import GentleSmoke
from pirates.effects.LightSparks import LightSparks
from EffectController import EffectController
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class BrazierFire(NodePath, EffectController):

    def __init__(self, effectParent=None):
        NodePath.__init__(self, uniqueName('BrazierFire'))
        EffectController.__init__(self)
        if effectParent:
            self.reparentTo(effectParent)
        self._fire = None
        self._smoke = None
        self._sparks = None
        self.fireSfx = loadSfx(SoundGlobals.SFX_FX_FIRE_LOOP)
        self.fireSfxIval = None
        return

    def createTrack(self, lod=0):
        self.startEffect = Sequence(Func(self.enableEffect))
        self.endEffect = Sequence(Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(10.0), self.endEffect)

    def enableEffect(self):
        if hasattr(base, 'pe'):
            effectSetting = Options.SpecialEffectsHigh
        else:
            effectSetting = base.options.getSpecialEffectsSetting()
        if not self._fire:
            self._fire = LightFire.getEffect()
        if self._fire:
            self._fire.enableEffect()
            self._fire.reparentTo(self)
        if not self._smoke and effectSetting >= Options.SpecialEffectsMedium:
            self._smoke = GentleSmoke.getEffect()
        if self._smoke:
            self._smoke.enableEffect()
            self._smoke.reparentTo(self)
            self._smoke.setPos(0, 0, 1)
        if not self._sparks and effectSetting >= Options.SpecialEffectsHigh:
            self._sparks = LightSparks.getEffect()
        if self._sparks:
            self._sparks.enableEffect()
            self._sparks.reparentTo(self)
        if self.fireSfx:
            self.fireSfxIval = SoundInterval(self.fireSfx, node=self, volume=0.25, seamlessLoop=False)
            self.fireSfxIval.loop()

    def disableEffect(self):
        if self._fire:
            self._fire.disableEffect()
        if self._smoke:
            self._smoke.disableEffect()
        if self._sparks:
            self._sparks.disableEffect()
        if self.fireSfxIval:
            self.fireSfxIval.finish()
            self.fireSfxIval = None
        return

    def setScale(self, scale=VBase3(1, 1, 1)):
        self.setEffectScale(scale[0])

    def setEffectScale(self, scale):
        if self._fire:
            self._fire.setEffectScale(scale)
        if self._smoke:
            self._smoke.setEffectScale(scale)
        if self._sparks:
            self._sparks.setEffectScale(scale)

    def cleanUpEffect(self):
        if self._fire:
            self._fire.cleanUpEffect()
            self._fire = None
        if self._smoke:
            self._smoke.cleanUpEffect()
            self._smoke = None
        if self._sparks:
            self._sparks.cleanUpEffect()
            self._sparks = None
        if self.fireSfxIval:
            self.fireSfxIval.finish()
            self.fireSfxIval = None
        EffectController.cleanUpEffect(self)
        return

    def destroy(self):
        if self._fire:
            self._fire.destroy()
        if self._smoke:
            self._smoke.destroy()
        if self._sparks:
            self._sparks.destroy()
        if self.fireSfxIval:
            self.fireSfxIval.finish()
            self.fireSfxIval = None
        del self._fire
        del self._smoke
        del self._sparks
        del self.fireSfx
        EffectController.destroy(self)
        return