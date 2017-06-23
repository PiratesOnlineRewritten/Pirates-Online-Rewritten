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

class ForestEffects(EnvironmentEffects.EnvironmentEffects):
    FIREFLIES_Z = 6.0
    RANDOM_SOUND_PERIOD = 6
    RANDOM_SOUND_CHANCE = 12

    def __init__(self, parent, modelPath):
        EnvironmentEffects.EnvironmentEffects.__init__(self, parent, modelPath)
        self.fireflies = None
        self.modelPrefix = modelPath[:-4]
        self.animActor = self.setupAnimActor()
        self.water = None
        self.randomAnimalSoundFiles = [SoundGlobals.SFX_FX_JUNGLE_BIRDS_01, SoundGlobals.SFX_FX_JUNGLE_BIRDS_02]
        self.randomSfx = []
        self.startEffects()
        return

    def delete(self):
        del self.animActor
        self.stopEffects()
        EnvironmentEffects.EnvironmentEffects.delete(self)

    def startEffects(self):
        if not self.fireflies:
            self.fireflies = Fireflies()
        if self.fireflies and hasattr(base, 'cr'):
            self.fireflies.reparentTo(base.localAvatar)
            self.fireflies.startLoop()
        base.ambientMgr.requestFadeIn(SoundGlobals.AMBIENT_JUNGLE, duration=10, finalVolume=PiratesGlobals.DEFAULT_AMBIENT_VOLUME, priority=1)
        self.swamp_water = None
        reflection = Reflection.getGlobalReflection()
        if 'jungle_a' in self.modelPrefix:
            if base.config.GetBool('want-shaders', 1) and base.win and base.win.getGsg() and base.win.getGsg().getShaderModel() >= GraphicsStateGuardian.SM20:
                water_color = Vec4(13, 15, 21, 255.0)
                self.water = Swamp(self.modelPrefix + 'water', self.parent, reflection, None, None, water_color)
                self.water.reflection_factor = 0.3
                self.water.set_reflection_parameters_np()
            else:
                water = loader.loadModel(self.modelPrefix + 'water')
                water.reparentTo(self.parent)
                color = Vec4(0)
                water.setColorScale(color)
                mask = 4294967295L
                stencil = StencilAttrib.make(1, StencilAttrib.SCFAlways, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOReplace, 1, mask, mask)
                water.setAttrib(stencil)
                water.setBin('water', 0)
                self.reflection = reflection
                taskMgr.add(self.camTask, 'jungleEffectsCamTask-' + str(id(self)), priority=49)
                water.setFogOff()
        for file in self.randomAnimalSoundFiles:
            sfx = loadSfx(file)
            self.randomSfx.append(sfx)

        taskMgr.doMethodLater(self.RANDOM_SOUND_PERIOD, self.checkForRandomSound, name='checkForRandomSound-' + str(id(self)))
        return

    def stopEffects(self):
        if hasattr(base, 'cr') and not hasattr(base.cr, 'isFake'):
            taskMgr.remove(self.parent.uniqueName('groundFogZTask'))
        if self.water:
            self.water.delete()
            self.water = None
        if self.fireflies:
            self.fireflies.destroy()
            self.fireflies = None
        taskMgr.remove('jungleEffectsCamTask-' + str(id(self)))
        taskMgr.remove('checkForRandomSound-' + str(id(self)))
        for sfx in self.randomSfx:
            sfx.stop()

        base.ambientMgr.requestFadeOut(SoundGlobals.AMBIENT_JUNGLE, duration=5, priority=1)
        return

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

    def camTask(self, task):
        if self.reflection:
            self.reflection.update_reflection(base.camLens, base.cam)
        return Task.cont

    def adjustGroundFogZ(self, task):
        if self.fireflies:
            self.fireflies.setZ(render, self.FIREFLIES_Z)
        if self.fireflies:
            return Task.cont
        return Task.done