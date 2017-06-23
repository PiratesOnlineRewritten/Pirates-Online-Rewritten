from pandac.PandaModules import *
from direct.task import Task
from pirates.audio import SoundGlobals
from pirates.swamp.Swamp import Swamp
from pirates.effects import EnvironmentEffects
from pirates.piratesbase import TimeOfDayManager, TODGlobals, PiratesGlobals
from pirates.seapatch.Reflection import Reflection
from pirates.seapatch.Water import Water
from pirates.world.LocationConstants import LocationIds
from direct.interval.LerpInterval import LerpScaleInterval
from direct.interval.MetaInterval import Sequence

class CaveEffects(EnvironmentEffects.EnvironmentEffects):
    WaterCaves = [
     LocationIds.ANVIL_CAVE_BARBOSA]
    LavaCaves = []

    def __init__(self, parent, modelPath):
        EnvironmentEffects.EnvironmentEffects.__init__(self, parent, modelPath)
        self.modelPath = modelPath
        self.modelPrefix = ''
        self.animActor = None
        self.water = None
        self.reflection = None
        self.supports_sky_only = False
        self.startEffects()
        return

    def delete(self):
        del self.animActor
        self.stopEffects()
        EnvironmentEffects.EnvironmentEffects.delete(self)

    def startEffects(self):
        reflection = Reflection.getGlobalReflection()
        non_shader_water_color = Vec4(0.0, 1.0 / 255.0, 4.0 / 255.0, 1.0)
        shader_water_color = Vec4(0.0, 1.0, 4.0, 255.0)
        if self.parent.uniqueId in self.WaterCaves:
            if base.config.GetBool('want-shaders', 1) and base.win and base.win.getGsg() and base.win.getGsg().getShaderModel() >= GraphicsStateGuardian.SM20:
                self.water = Swamp('models/caves/cave_a_water', self.parent, reflection, None, None, shader_water_color)
                self.water.reflection_factor = 0.3
                self.water.set_reflection_parameters_np()
            else:
                water = loader.loadModel('models/caves/cave_a_water')
                water.reparentTo(self.parent)
                color = non_shader_water_color
                water.setColorScale(color)
                water.setTextureOff(1)
                mask = 4294967295L
                stencil = StencilAttrib.make(1, StencilAttrib.SCFAlways, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOReplace, 1, mask, mask)
                water.setAttrib(stencil)
                water.setBin('water', 0)
                self.reflection = reflection
                taskMgr.add(self.camTask, 'caveEffectsCamTask-' + str(id(self)), priority=49)
                water.setFogOff()
        elif self.parent.uniqueId in self.LavaCaves:
            if base.config.GetBool('want-shaders', 1) and base.win and base.win.getGsg() and base.win.getGsg().getShaderModel() >= GraphicsStateGuardian.SM20:
                self.water = Swamp(self.modelPrefix + 'lava', self.parent, reflection, None, None, shader_water_color)
                l1 = LerpScaleInterval(self.water.seamodel, 2, Vec3(1.006, 1.006, 1.0), Vec3(1.0, 1.0, 1.0), blendType='easeInOut')
                l2 = LerpScaleInterval(self.water.seamodel, 2, Vec3(1.0, 1.0, 1.0), Vec3(1.006, 1.006, 1.0), blendType='easeInOut')
                seq = Sequence(l1, l2)
                seq.loop()
                self.water.reflection_factor = 0.3
                self.water.set_reflection_parameters_np()
            else:
                water = loader.loadModel(self.modelPrefix + 'lava')
                water.reparentTo(self.parent)
                water.setFogOff()
        base.ambientMgr.requestFadeIn(SoundGlobals.AMBIENT_CAVE, duration=10, finalVolume=PiratesGlobals.DEFAULT_AMBIENT_VOLUME, priority=1)
        if self.water:
            self.water.supports_sky_only = self.supports_sky_only
        if reflection:
            if base.options.reflection >= 1:
                reflection.reflectShowThroughOnly(False)
                reflection.enable(True)
        return

    def camTask(self, task):
        if self.reflection:
            self.reflection.update_reflection(base.camLens, base.cam)
        return Task.cont

    def stopEffects(self):
        if hasattr(base, 'cr') and not hasattr(base.cr, 'isFake'):
            if base.options.reflection == 0:
                Water.all_reflections_off()
            elif base.options.reflection == 1:
                Water.all_reflections_show_through_only()
            elif base.options.reflection == 2:
                Water.all_reflections_on()
        if self.water:
            self.water.delete()
            self.water = None
        taskMgr.remove('caveEffectsCamTask-' + str(id(self)))
        base.ambientMgr.requestFadeOut(SoundGlobals.AMBIENT_CAVE, duration=5, priority=1)
        return