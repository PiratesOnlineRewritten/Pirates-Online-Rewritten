import os
import math
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task import Task
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.DirectObject import DirectObject
from pirates.piratesbase import PiratesGlobals
from otp.otpbase import OTPRender
from pirates.seapatch.Reflection import Reflection
from pirates.seapatch.Water import Water
if base.config.GetBool('want-water-panel', False):
    from pirates.seapatch.WaterPanel import *

class Swamp(Water):
    notify = directNotify.newCategory('Swamp')

    def __init__(self, swamp_model_file_path, parentNP=render, reflection=None, input_swamp_model=None, input_shader_file_path=None, input_water_color=None):
        if input_swamp_model:
            swamp_name = 'Swamp I'
        else:
            swamp_name = 'Swamp'
        Water.__init__(self, swamp_name)
        self.parentNP = parentNP
        self.swamp_model = input_swamp_model
        if input_swamp_model:
            self.seamodel = input_swamp_model
            self.parentNP = input_swamp_model.getParent()
            self.patchNP = NodePath(self.seamodel)
        else:
            if swamp_model_file_path:
                self.seamodel = loader.loadModel(swamp_model_file_path)
            else:
                self.swampmodel = loader.loadModel('models/swamp/SwampA')
                self.swampmodel.reparentTo(self.parentNP)
                self.swampmodel.setPos(0.0, 0.0, -1.0)
                self.seamodel = loader.loadModel('models/swamp/swampA_water')
            self.patchNP = NodePath(self.seamodel)
            self.patchNP.reparentTo(self.parentNP)
        self.hidden = False
        mask = 4294967295L
        if self.use_water_bin:
            self.seamodel.setBin('water', 1)
            stencil = StencilAttrib.make(1, StencilAttrib.SCFAlways, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOReplace, 1, mask, mask)
            self.seamodel.setAttrib(stencil)
        else:
            self.seamodel.setBin('background', 200)
        self.reflectStage = None
        if False:
            self.model = loader.loadModel('models/misc/smiley')
            self.model.reparentTo(render)
            self.model.setPos(0.0, 50.0, 10.0)
            self.model.setHpr(0.0, 180.0, 0.0)
            self.model.setBin('water', 100)
            self.model2 = loader.loadModel('models/misc/smiley')
            self.model2.reparentTo(render)
            self.model2.setPos(10.0, 50.0, 15.0)
            self.model2.setHpr(180.0, 0.0, 0.0)
            self.model2.setBin('water', 50)
            self.model3 = loader.loadModel('models/misc/smiley')
            self.model3.reparentTo(render)
            self.model3.setPos(-10.0, 50.0, 15.0)
            self.model3.setHpr(0.0, 0.0, 0.0)
            self.model3.setBin('water', 50)
            stencil = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 1, mask, mask)
            self.model.setAttrib(stencil)
            stencil = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 0, mask, mask)
            self.model3.setAttrib(stencil)
        if self.use_water_bin:
            self.patchNP.setBin('water', 10)
        else:
            self.patchNP.setBin('ground', -10)
        try:
            self.todMgr = base.cr.timeOfDayManager
        except:
            self.todMgr = None

        if self.todMgr:
            self.patchNP.setLightOff()
            self.patchNP.setLight(self.todMgr.alight)
        seaMin, seaMax = self.seamodel.getTightBounds()
        seaDelta = seaMax - seaMin
        cp = CollisionPolygon(Point3(-1.0, -1.0, 0), Point3(1.0, -1.0, 0), Point3(1.0, 1.0, 0), Point3(-1.0, 1.0, 0))
        cNode = CollisionNode('seaCollision')
        cNode.setCollideMask(PiratesGlobals.TargetBitmask)
        cNode.addSolid(cp)
        cNodePath = self.parentNP.attachNewNode(cNode)
        cNodePath.reparentTo(self.seamodel)
        cNodePath.setScale(Vec3(seaDelta).length())
        cNodePath.setZ(3)
        cNodePath.setTag('objType', str(PiratesGlobals.COLL_SEA))
        self.cNodePath = cNodePath
        ccPlane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
        ccNode = CollisionNode('seaCamCollision')
        ccNode.setCollideMask(PiratesGlobals.CameraBitmask)
        ccNode.addSolid(ccPlane)
        ccNodePath = self.parentNP.attachNewNode(ccNode)
        ccNodePath.reparentTo(self.seamodel)
        self.ccNodePath = ccNodePath
        self.enabled = False
        self.enable()
        self.setting_0()
        if input_water_color:
            self.water_r = input_water_color[0]
            self.water_g = input_water_color[1]
            self.water_b = input_water_color[2]
            self.water_a = input_water_color[3]
        else:
            self.water_r = 33
            self.water_g = 43
            self.water_b = 38
            self.water_a = 255
        self.set_water_color()
        self.reflection_factor = 0.34
        self.set_reflection_parameters_np()
        if self.use_alpha_map:
            if self.enable_alpha_map:
                self.patchNP.setTransparency(1)
        if self.water_panel != None:
            self.water_panel.setSeaPatch(self)
        if input_shader_file_path == None:
            shader_file_path = 'models/swamps/swamp002_2X.cg'
        else:
            shader_file_path = input_shader_file_path
        if base.config.GetBool('want-shaders', 1) and base.win and base.win.getGsg() and base.win.getGsg().getShaderModel() >= GraphicsStateGuardian.SM20:
            self.shader = loader.loadShader(shader_file_path)
            if self.shader != None:
                self.seamodel.setShader(self.shader)
                self.seamodel.setFogOff()
                self.setting_0()
                if input_water_color:
                    self.water_r = input_water_color[0]
                    self.water_g = input_water_color[1]
                    self.water_b = input_water_color[2]
                    self.water_a = input_water_color[3]
                else:
                    self.water_r = 33
                    self.water_g = 43
                    self.water_b = 38
                    self.water_a = 255
                self.set_water_color()
                self.reflection_factor = 0.34
                self.set_reflection_parameters_np()
                if self.use_alpha_map:
                    self.patchNP.setTransparency(1)
                self.texture_extension = '.jpg'
                default_water_color_texture_filename = 'maps/ocean_color_1' + self.texture_extension
                default_water_alpha_texture_filename = 'maps/default_inv_alpha' + self.texture_extension
                if swamp_model_file_path:
                    if False:
                        self.base_texture = loader.loadTexture('maps/oceanWater2' + self.texture_extension)
                        self.texture_d = self.base_texture.loadRelated(InternalName.make('-d'))
                        self.texture_n = self.base_texture.loadRelated(InternalName.make('-n'))
                        self.texture_bb = self.base_texture.loadRelated(InternalName.make('-bb'))
                    else:
                        swamp_texture = self.seamodel.findTexture('*')
                        self.set_water_color_texture(default_water_color_texture_filename, True, swamp_texture)
                        if False:
                            card_x_size = 0.5
                            card_y_size = 0.5
                            card = CardMaker('test_texture_card')
                            card.setFrame(-card_x_size, card_x_size, -card_y_size, card_y_size)
                            card_node_path = NodePath(card.generate())
                            card_node_path.setTexture(swamp_texture, 1)
                            card_node_path.node().setBounds(OmniBoundingVolume())
                            card_node_path.node().setFinal(1)
                            card_node_path.reparentTo(render2d)
                        self.texture_d = loader.loadTexture('maps/oceanWater2-d' + self.texture_extension)
                        self.texture_n = loader.loadTexture('maps/oceanWater2-n' + self.texture_extension)
                        self.texture_bb = loader.loadTexture('maps/oceanWater2-bb' + self.texture_extension)
                        self.texture_low2 = loader.loadTexture('maps/oceanWater2-low2' + self.texture_extension)
                        self.seamodel.setShaderInput('d', self.texture_d)
                        self.seamodel.setShaderInput('n', self.texture_n)
                        self.seamodel.setShaderInput('bb', self.texture_bb)
                        self.seamodel.setShaderInput('low2', self.texture_low2)
                    self.set_water_alpha_texture(default_water_alpha_texture_filename)
                else:
                    self.texture_d = loader.loadTexture('maps/oceanWater2-d' + self.texture_extension)
                    self.texture_n = loader.loadTexture('maps/oceanWater2-n' + self.texture_extension)
                    self.texture_bb = loader.loadTexture('maps/oceanWater2-bb' + self.texture_extension)
                    self.texture_low2 = loader.loadTexture('maps/oceanWater2-low2' + self.texture_extension)
                    self.seamodel.setShaderInput('d', self.texture_d)
                    self.seamodel.setShaderInput('n', self.texture_n)
                    self.seamodel.setShaderInput('bb', self.texture_bb)
                    self.seamodel.setShaderInput('low2', self.texture_low2)
                    self.set_water_color_texture(default_water_color_texture_filename)
                    self.set_water_alpha_texture(default_water_alpha_texture_filename)
                if self.enable_water_panel:
                    self.water_panel.set_texture(default_water_color_texture_filename)
                    self.water_panel.set_shader(shader_file_path)
        buffer_width = 512
        buffer_height = 512
        if True:
            if reflection:
                self.reflection = reflection
            else:
                self.reflection = Reflection('swamp', buffer_width, buffer_height, render, Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
            if self.reflection_enabled():
                self.reflection_on()
            else:
                self.reflection_off()
            self.seamodel.setShaderInput('reflectiontexture', self.reflection.reflection_texture)
            OTPRender.renderReflection(False, self.patchNP, 'p_swamp_water', None)
        else:
            self.reflection_factor = 0.0
            self.set_reflection_parameters()
        if not self.shader:
            if True:
                self.reflection.createCard('water', 6)
            self.setting_0()
            self.reflection_factor = 0.34
            self.set_reflection_parameters_np()
        self.create_interface()
        return

    def hide(self):
        self.patchNP.hide()
        self.hidden = True

    def show(self):
        self.patchNP.show()
        self.hidden = False

    def toggle_display(self):
        if self.hidden:
            self.show()
        else:
            self.hide()

    def delete(self):
        self.ccNodePath.removeNode()
        self.cNodePath.removeNode()
        if self.swamp_model == None:
            self.seamodel.removeNode()
        self.patchNP.removeNode()
        self.parentNP = None
        self.todMgr = None
        taskMgr.remove('swampCamTask-' + str(id(self)))
        self.ignoreAll()
        self.delete_water()
        return

    def disable(self):
        if self.enabled:
            self.enabled = False
            if self.patchNP.getParent().isEmpty() == False:
                self.patchNP.stash()
            taskMgr.remove('swampCamTask-' + str(id(self)))

    def enable(self):
        if not self.enabled:
            self.enabled = True
            if self.patchNP.getParent().isEmpty() == False:
                self.patchNP.unstash()
            taskMgr.add(self.camTask, 'swampCamTask-' + str(id(self)), priority=49)

    def camTask(self, task):
        self.s = 0.0
        self.p = 80.0
        self.d = 1.0
        self.update_water(task.time)
        return Task.cont