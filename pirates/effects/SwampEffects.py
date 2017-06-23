from pandac.PandaModules import *
from direct.task import Task
from pirates.audio import SoundGlobals
from pirates.swamp.Swamp import Swamp
from pirates.effects import EnvironmentEffects
from pirates.effects.Fireflies import Fireflies
from pirates.effects.GroundFog import GroundFog
from pirates.piratesbase import TimeOfDayManager, TODGlobals, PiratesGlobals
from pirates.seapatch.Reflection import Reflection
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import random

class SwampEffects(EnvironmentEffects.EnvironmentEffects):
    GROUND_FOG_Z = 2.0
    FIREFLIES_Z = 6.0
    RANDOM_SOUND_PERIOD = 6
    RANDOM_SOUND_CHANCE = 12

    def __init__(self, parent, modelPath):
        EnvironmentEffects.EnvironmentEffects.__init__(self, parent, modelPath)
        self.fireflies = None
        self.groundFog = None
        self.swamp_water = None
        self.water = None
        self.randomAnimalSoundFiles = [SoundGlobals.SFX_FX_SWAMP_FROG_01, SoundGlobals.SFX_FX_SWAMP_OWL_01, SoundGlobals.SFX_FX_SWAMP_OWL_02]
        self.randomSfx = []
        self.startEffects()
        return

    def delete(self):
        self.stopEffects()
        EnvironmentEffects.EnvironmentEffects.delete(self)

    def startEffects(self):
        self.swamp_water = None
        if base.config.GetBool('want-shaders', 1) and base.win and base.win.getGsg() and base.win.getGsg().getShaderModel() >= GraphicsStateGuardian.SM20:
            reflection = Reflection.getGlobalReflection()
            self.swamp_water = Swamp(self.modelPath + '_water', self.parent, reflection)
        else:
            self.water = loader.loadModel(self.modelPath + '_water')
            self.water.reparentTo(self.parent)
            self.water.setTransparency(TransparencyAttrib.MNone, 100)
            alpha_test_attrib = AlphaTestAttrib.make(RenderAttrib.MAlways, 0)
            self.water.setAttrib(alpha_test_attrib, 100)
        if not self.fireflies:
            self.fireflies = Fireflies()
        if self.fireflies and hasattr(base, 'cr'):
            self.fireflies.reparentTo(base.localAvatar)
            self.fireflies.startLoop()
        if not self.groundFog:
            self.groundFog = GroundFog()
        if self.groundFog and hasattr(base, 'options'):
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                self.groundFog.reparentTo(base.localAvatar)
                self.groundFog.startLoop(base.options.getSpecialEffectsSetting())
        if hasattr(base, 'cr') and not hasattr(base.cr, 'isFake'):
            taskMgr.add(self.adjustGroundFogZ, self.parent.uniqueName('groundFogZTask'))
        base.ambientMgr.requestFadeIn(SoundGlobals.AMBIENT_SWAMP, duration=10, finalVolume=PiratesGlobals.DEFAULT_AMBIENT_VOLUME, priority=1)
        for file in self.randomAnimalSoundFiles:
            sfx = loadSfx(file)
            self.randomSfx.append(sfx)

        taskMgr.doMethodLater(self.RANDOM_SOUND_PERIOD, self.checkForRandomSound, name='checkForRandomSound-' + str(id(self)))
        return

    def stopEffects(self):
        if hasattr(base, 'cr') and not hasattr(base.cr, 'isFake'):
            taskMgr.remove(self.parent.uniqueName('groundFogZTask'))
        taskMgr.remove('checkForRandomSound-' + str(id(self)))
        if self.swamp_water:
            self.swamp_water.delete()
            self.water = None
        if self.fireflies:
            self.fireflies.destroy()
            self.fireflies = None
        if self.groundFog:
            self.groundFog.destroy()
            self.groundFog = None
        base.ambientMgr.requestFadeOut(SoundGlobals.AMBIENT_SWAMP, duration=5, priority=1)
        for sfx in self.randomSfx:
            sfx.stop()

        return

    def adjustGroundFogZ(self, task):
        if self.fireflies:
            self.fireflies.setZ(render, self.FIREFLIES_Z)
        if self.groundFog:
            self.groundFog.setZ(render, self.GROUND_FOG_Z)
        if self.fireflies or self.groundFog:
            return Task.cont
        return Task.done

    def checkForRandomSound(self, task):
        randomSoundPlaying = False
        for sfx in self.randomSfx:
            if sfx.status() == 2:
                randomSoundPlaying = True
                break

        if not randomSoundPlaying:
            roll = random.randint(0, 100)
            if roll < self.RANDOM_SOUND_CHANCE:
                sfxToPlay = random.choice(self.randomSfx)
                sfxToPlay.play()
        taskMgr.doMethodLater(self.RANDOM_SOUND_PERIOD, self.checkForRandomSound, name='checkForRandomSound-' + str(id(self)))
        return Task.done