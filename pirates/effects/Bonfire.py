from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.effects.Fire import Fire
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.piratesgui.GameOptions import Options

class Bonfire(NodePath):
    HackCount = 0

    def __init__(self, parent=None):
        NodePath.__init__(self, uniqueName('Bonfire'))
        self._fire = Fire.getEffect()
        self._smoke = BlackSmoke.getEffect()
        if self._fire:
            self._fire.reparentTo(self)
            self._fire.effectScale = 1.0
        if self._smoke:
            self._smoke.reparentTo(self)
        if parent is not None:
            self.reparentTo(parent)
        self._sound = None
        if Bonfire.HackCount == 0:
            Bonfire.HackCount += 1
            self._hasSound = True
            self._sound = None
        else:
            self._hasSound = False
        return

    def disableSound(self):
        if self._sound:
            self._sound.pause()
            self._sound = None
        return

    def startLoop(self, lod=Options.SpecialEffectsHigh):
        if self._fire:
            self._fire.startLoop(lod)
        if self._smoke and lod >= Options.SpecialEffectsHigh:
            self._smoke.startLoop(lod)
        if self._sound is not None:
            self._sound.loop()
        return

    def stop(self):
        if self._fire:
            self._fire.stop()
        if self._smoke:
            self._smoke.stop()
        if self._sound:
            self._sound.pause()

    def enableEffect(self):
        if not self._fire:
            self._fire = Fire.getEffect()
        if self._fire:
            self._fire.enableEffect()
            self._fire.reparentTo(self)
        if not self._smoke:
            self._smoke = BlackSmoke.getEffect()
        if self._smoke:
            self._smoke.enableEffect()
            self._smoke.reparentTo(self)

    def disableEffect(self):
        if self._fire:
            self._fire.disableEffect()
        if self._smoke:
            self._smoke.disableEffect()

    def cleanUpEffect(self):
        if self._fire:
            self._fire.cleanUpEffect()
            self._fire = None
        if self._smoke:
            self._smoke.cleanUpEffect()
            self._smoke = None
        if self._sound is not None:
            self._sound.pause()
            self._sound = None
        return

    def destroy(self):
        if self._hasSound:
            Bonfire.HackCount = 0
            self._hasSound = False
        if self._fire:
            self._fire.destroy()
            self._fire = None
        if self._smoke:
            self._smoke.destroy()
            self._smoke = None
        if self._sound is not None:
            self._sound.pause()
            self._sound = None
        return