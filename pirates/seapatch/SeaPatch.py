import os
import math
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from libpirates import SeaPatchRoot, SeaPatchNode
from direct.task import Task
from pirates.seapatch.LerpSeaPatchInterval import LerpSeaPatchInterval
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.DirectObject import DirectObject
from pirates.piratesbase import PiratesGlobals
from direct.showbase.DirectObject import DirectObject
from otp.otpbase import OTPRender
from pirates.seapatch.Reflection import Reflection
from pirates.seapatch.Water import Water
from direct.motiontrail.MotionTrail import MotionTrail
from direct.showbase import AppRunnerGlobal
from pirates.piratesgui.GameOptions import *

class SeaPatch(Water):
    notify = directNotify.newCategory('SeaPatch')

    def __init__(self, parentNP=render, reflection=None, todMgr=None):
        Water.__init__(self, 'Sea')
        if base.win.getFbProperties().getStencilBits() == 0:
            self.use_water_bin = False
        self.p3 = Point3()
        self.parentNP = parentNP
        self.followWater = base.config.GetBool('ships-follow-water', 1)
        self.damper = 0.2 * 180.0 / math.pi
        self.floats = {}
        self.floatmasses = {}
        self.patch = SeaPatchRoot()
        self.patch.setSeaLevel(0)
        self.hidden = False
        self.usingFlatWater = False
        if base.camera:
            self.setCenter(base.camera)
            self.setAnchor(render)
        patchNode = SeaPatchNode('seapatch', self.patch)
        patchNode.setWantReflect(0)
        self.patchNP = NodePath(patchNode)
        self.patchNP.setColorScale(0.15, 0.4, 0.5, 1.0)
        self.patchNP.setTwoSided(True)
        self.patchNP.hide()
        shader_file_path = None
        if base.config.GetBool('want-shaders', 1) and base.win and base.win.getGsg() and base.win.getGsg().getShaderModel() >= GraphicsStateGuardian.SM20:
            patchNode.setWantColor(0)
            shader_directory = 'models/sea/'
            shader_file_name_array = [
             '', 'water008_11.cg', 'water008_20.cg', 'water008_2X.cg']
            shader_model = base.win.getGsg().getShaderModel()
            maximum_shader_model = len(shader_file_name_array) - 1
            if shader_model > maximum_shader_model:
                shader_model = maximum_shader_model
            file_name = shader_file_name_array[shader_model]
            shader_file_path = shader_directory + file_name
            self.shader = loader.loadShader(shader_file_path)
            if self.shader:
                pass
        if self.shader:
            if base.win.getGsg().getShaderModel() == GraphicsStateGuardian.SM20:
                self.seamodel = loader.loadModel('models/sea/SeaPatch34')
            else:
                self.seamodel = loader.loadModel('models/sea/SeaPatch31')
        else:
            if base.options.getTerrainDetailSetting() == 0:
                self.seamodel = loader.loadModel('models/sea/pir_m_are_wld_seaPatch_low')
            else:
                self.seamodel = loader.loadModel('models/sea/SeaPatch31')
            self.seamodel.setScale(2, 1, 1)
            self.seamodel.flattenMedium()
            mask = 4294967295L
            if self.use_water_bin:
                self.seamodel.setBin('water', 0)
                stencil = StencilAttrib.makeWithClear(1, StencilAttrib.SCFAlways, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOReplace, 1, mask, mask, 1, 0)
                self.seamodel.setAttrib(stencil)
            else:
                self.seamodel.setBin('background', 200)
            self.seamodel.hide(OTPRender.MainCameraBitmask)
            self.seamodel.showThrough(OTPRender.EnviroCameraBitmask)
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
            self.flatSea = self.seamodel.find('**/flatsea')
            flat2 = self.flatSea.copyTo(self.flatSea)
            flat2.setScale(2, 2, 1)
            flat2.setZ(-4)
            flat4 = self.flatSea.copyTo(self.flatSea)
            flat4.setScale(4, 4, 1)
            flat4.setZ(-8)
            if not self.flatSea.isEmpty():
                self.flatSea.setTag('flat_sea', 'true')
                self.flatSea.setPos(0, 0, -1)
                if False:
                    self.flatSea.setScale(1.3)
                if self.use_water_bin:
                    self.flatSea.setDepthWrite(0)
            self.flatSea.flattenStrong()
            if self.use_water_bin:
                self.patchNP.setBin('water', 10)
            else:
                self.patchNP.setBin('ground', -10)
            self.todMgr = todMgr
            if self.getTodMgr():
                self.patchNP.setLightOff()
                self.patchNP.setLight(self.getTodMgr().alight)
            seaMin, seaMax = self.seamodel.getTightBounds()
            seaDelta = seaMax - seaMin
            cp = CollisionPolygon(Point3(-1.0, -1.0, 0), Point3(1.0, -1.0, 0), Point3(1.0, 1.0, 0), Point3(-1.0, 1.0, 0))
            cNode = CollisionNode('seaCollision')
            cNode.setCollideMask(PiratesGlobals.TargetBitmask)
            cNode.addSolid(cp)
            cNodePath = NodePath(cNode)
            cNodePath.reparentTo(self.seamodel)
            cNodePath.setScale(Vec3(seaDelta).length())
            cNodePath.setZ(-3)
            cNodePath.setTag('objType', str(PiratesGlobals.COLL_SEA))
            cNodePath.reparentTo(self.parentNP)
            self.cNodePath = cNodePath
            ccPlane = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
            ccNode = CollisionNode('seaCamCollision')
            ccNode.setCollideMask(PiratesGlobals.CameraBitmask)
            ccNode.addSolid(ccPlane)
            ccNodePath = NodePath(ccNode)
            ccNodePath.reparentTo(self.seamodel)
            self.ccNodePath = ccNodePath
            self.seamodel.reparentTo(self.patchNP)
            self.patchNP.flattenLight()
            patchNode.collectGeometry()
            self.enabled = False
            self.enable()
            if self.use_alpha_map:
                if self.enable_alpha_map:
                    self.patchNP.setTransparency(1)
                    alpha_test_attrib = AlphaTestAttrib.make(RenderAttrib.MAlways, 0)
                    self.patchNP.setAttrib(alpha_test_attrib, 100)
            if self.water_panel != None:
                self.water_panel.setSeaPatch(self)
            if self.enable_parameter_keys:

                def showSeaPatchPanel():
                    from pirates.seapatch import SeaPatchPanel
                    self.spp = SeaPatchPanel.SeaPatchPanel()
                    self.spp.setPatch(self)

                self.accept('shift-5', showSeaPatchPanel)
            self.setting_0()
            self.patchNP.setTransparency(0)
            buffer_width = 512
            buffer_height = 512
            self.texture_extension = '.jpg'
            if self.shader:
                self.seamodel.setShader(self.shader)
                self.seamodel.setFogOff()
                if self.use_alpha_map:
                    self.patchNP.setTransparency(1)
                self.base_texture = loader.loadTexture('maps/oceanWater2' + self.texture_extension)
                self.texture_d = self.base_texture.loadRelated(InternalName.make('-d'))
                self.texture_n = self.base_texture.loadRelated(InternalName.make('-n'))
                self.texture_bb = self.base_texture.loadRelated(InternalName.make('-bb'))
                self.setting_0()
                self.water_r = 77
                self.water_g = 128
                self.water_b = 179
                self.water_a = 255
                self.set_water_color()
                default_water_color_texture_filename = 'maps/ocean_color_1' + self.texture_extension
                default_water_alpha_texture_filename = 'maps/default_inv_alpha' + self.texture_extension
                self.set_water_color_texture(default_water_color_texture_filename)
                self.set_water_alpha_texture(default_water_alpha_texture_filename)
                if self.enable_water_panel:
                    self.water_panel.set_texture(default_water_color_texture_filename)
                    self.water_panel.set_shader(shader_file_path)
            if True:
                if reflection:
                    self.reflection = reflection
                else:
                    self.reflection = Reflection('seapatch', buffer_width, buffer_height, render, Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
                if self.reflection_enabled():
                    self.reflection_on()
                else:
                    self.reflection_off()
                self.reflection.reflectShowThroughOnly(self.reflect_show_through_only)
                self.seamodel.setShaderInput(self.reflectiontexture_name, self.reflection.reflection_texture)
                OTPRender.renderReflection(False, self.patchNP, 'p_ocean_water', None)
            else:
                self.reflection_factor = 0.0
                self.set_reflection_parameters_np()
            if not self.shader:
                self.accept('timeOfDayChange', self._timeChange)
                if self.reflection:
                    self.reflection.createCard('water', 6)
                self.setting_0()
                self.reflection_factor = 0.2
                self.set_reflection_parameters_np()
                if False:
                    default_water_color_texture_filename = 'maps/ocean_color_1' + self.texture_extension
                    self.set_water_color_texture(default_water_color_texture_filename)
                    self.setup_color_map()
        self.create_interface()
        self.patchNP.reparentTo(self.parentNP)
        self.accept('grid-detail-changed', self.updateWater)
        return

    def updateWater(self, level):
        if level == 0:
            self.patch.animateHeight(False)
            self.patch.animateUv(False)
        else:
            self.patch.animateHeight(True)
            self.patch.animateUv(True)

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

    def getTodMgr(self):
        if self.todMgr:
            return self.todMgr
        try:
            return base.cr.timeOfDayManager
        except:
            return None

        return None

    def delete(self):
        self.ccNodePath.removeNode()
        self.cNodePath.removeNode()
        self.seamodel.removeNode()
        self.patchNP.removeNode()
        self.parentNP = None
        self.todMgr = None
        taskMgr.remove('seaFloatTask-' + str(id(self)))
        taskMgr.remove('seaPatchCamTask-' + str(id(self)))
        self.delete_water()
        if len(self.floats):
            self.notify.error('All floating objects not removed from seapatch. You must call removeFloatable')
            self.floats.clear()
            self.floatmasses.clear()
        self.ignoreAll()
        return

    def disable(self):
        if self.enabled:
            self.enabled = False
            self.patch.disable()
            self.patchNP.hide()
            taskMgr.remove('seaPatchCamTask-' + str(id(self)))
            taskMgr.remove('seaFloatTask-' + str(id(self)))

    def enable(self):
        if not self.enabled:
            self.enabled = True
            self.patch.enable()
            self.patchNP.show()
            taskMgr.add(self.camTask, 'seaPatchCamTask-' + str(id(self)), priority=49)
            if self.followWater:
                taskMgr.add(self.floatTask, 'seaFloatTask-' + str(id(self)), priority=35)

    def setAnchor(self, anchor):
        self.anchor = anchor
        self.patch.setAnchor(anchor)

    def setCenter(self, center):
        self.center = center
        self.patch.setCenter(center)

    def camTask(self, task):
        refNode = base.cam
        if not refNode:
            return Task.cont
        p = refNode.getPos(render)
        r = refNode.getHpr(render)
        if not self.usingFlatWater:
            self.patchNP.setPos(p.getX(), p.getY(), 0.0)
            self.patchNP.setH(r.getX())
        todMgr = self.getTodMgr()
        if self.shader and todMgr:
            self.clear_color = todMgr.fog.getColor()
            fog_color = todMgr.fog.getColor()
            self.fog_r = fog_color.getX()
            self.fog_g = fog_color.getY()
            self.fog_b = fog_color.getZ()
            self.fog_exp_density = todMgr.fog.getExpDensity()
            ambient_color = todMgr.alight.node().getColor()
            if todMgr.dlight is None:
                diffuse_color = VBase3(1.0, 1.0, 1.0)
            else:
                diffuse_color = todMgr.dlight.node().getColor()
            self.ar = ambient_color.getX() * 255.0
            self.ag = ambient_color.getY() * 255.0
            self.ab = ambient_color.getZ() * 255.0
            self.dr = diffuse_color.getX() * 255.0
            self.dg = diffuse_color.getY() * 255.0
            self.db = diffuse_color.getZ() * 255.0
            self.r = diffuse_color.getX() * 255.0
            self.g = diffuse_color.getY() * 255.0
            self.b = diffuse_color.getZ() * 255.0
            camera_position = p
            self.camera_x = camera_position.getX()
            self.camera_y = camera_position.getY()
            self.camera_z = camera_position.getZ()
            fakeDistance = 10000.0
            heading = 360.0 - todMgr.skyGroup.sunWheelRoll.getR()
            camera_heading = r.getX()
            adjusted_camera_heading = -camera_heading
            sunPos = todMgr.skyGroup.sunLight.getPos(todMgr.skyGroup)
            trueDistance = todMgr.skyGroup.sunLight.getDistance(todMgr.skyGroup)
            light_distance = fakeDistance
            distanceScalar = fakeDistance / trueDistance
            x1 = sunPos[0] * distanceScalar
            y1 = x1 - sunPos[1] * distanceScalar
            z1 = sunPos[2] * distanceScalar
            x2 = math.cos(math.radians(heading)) * fakeDistance
            y2 = math.cos(math.radians(heading)) * fakeDistance
            z2 = math.sin(math.radians(heading)) * fakeDistance
            x = x1
            y = y1
            z = z1
            self.x = math.cos(math.radians(adjusted_camera_heading)) * x
            self.y = math.sin(math.radians(adjusted_camera_heading)) * y
            self.z = z
            if z > 0.0:
                x = z / light_distance * 3.0 + 0.05
                mu = 0.0
                sigma = 0.5
                a = math.log(x) - mu
                a = a * a
                self.s = 2.0 * (1.0 / (x * sigma * math.sqrt(2.0 * math.pi))) * math.exp(-a / (2 * sigma * sigma))
                if self.s < 0.0:
                    self.s = 0.0
                self.p = 80.0
            else:
                self.s = 0.0
                self.p = 80.0
            self.d = 1.0
        self.update_water(task.time)
        return Task.cont

    def addFloatable(self, name, transNode, rotNode=None, mass=1):
        if rotNode == None:
            rotNode = transNode
        self.floats[name] = [
         transNode, rotNode]
        self.floatmasses[name] = mass
        return

    def removeFloatable(self, name):
        if self.floats.has_key(name):
            del self.floats[name]
            del self.floatmasses[name]

    def showFrustum(self):
        base.cam.node().setCullCenter(base.camera)
        base.graphicsEngine.setPortalCull(1)

    def toggleRes(self):
        if self.seamodel == self.lowres:
            self.seamodel = self.highres
        elif self.seamodel == self.highres:
            self.seamodel = self.lowres

    def floatTask(self, task):
        mass = -6.0
        area = 1
        k = self.damper
        for name, floater in self.floats.items():
            transNode = floater[0]
            rotNode = floater[1]
            height, normal = self.calcHeightAndNormalForMass(node=transNode, mass=mass, area=area)
            height = height - self.floatmasses[name]
            transNode.setZ(render, height)
            r = -k * normal[0]
            p = -k * normal[1]
            rotNode.setR(r)
            rotNode.setP(p)

        return Task.cont

    def setReflection(self, tex, factor):
        if self.reflectStage == None:
            self.reflectStage = TextureStage('reflect')
            self.reflectStage.setTexcoordName('reflect')
            self.reflectStage.setSort(10)
        if factor == None:
            self.reflectStage.setCombineRgb(TextureStage.CMAdd, TextureStage.CSTexture, TextureStage.COSrcColor, TextureStage.CSPrevious, TextureStage.COSrcColor)
        else:
            self.reflectStage.setCombineRgb(TextureStage.CMInterpolate, TextureStage.CSTexture, TextureStage.COSrcColor, TextureStage.CSPrevious, TextureStage.COSrcColor, TextureStage.CSConstant, TextureStage.COSrcAlpha)
            self.reflectStage.setColor(VBase4(1, 1, 1, factor))
        self.seamodel.setTexture(self.reflectStage, tex)
        return

    def clearReflection(self):
        if self.reflectStage != None:
            self.seamodel.clearTexture(self.reflectStage)
        return

    def saveSeaPatchFile(self, filename):
        if not isinstance(filename, Filename):
            filename = Filename.fromOsSpecific(filename)
        speed = self.patch.getOverallSpeed()
        radius = self.patch.getRadius()
        threshold = self.patch.getThreshold()
        hcolor = self.patch.getHighColor()
        lcolor = self.patch.getLowColor()
        uvscale = self.patch.getUvScale()
        pas = self.patch.getUvSpeed()
        mamplitude = []
        mlength = []
        mspeed = []
        mdir = []
        mchoppy = []
        for i in range(self.patch.getNumWaves()):
            mamplitude.append(self.patch.getWaveAmplitude(i))
            mlength.append(self.patch.getWaveLength(i))
            mspeed.append(self.patch.getWaveSpeed(i))
            mdir.append(self.patch.getWaveDirection(i))
            mchoppy.append(self.patch.getChoppyK(i))

        i1 = '    '
        i2 = i1 + i1
        i3 = i2 + i1
        out_file = open(filename.toOsSpecific(), 'wb')
        i2 = ''
        out_file.write(i2 + 'patch.setOverallSpeed(%.4f)\n' % speed)
        out_file.write(i2 + 'patch.setUvSpeed(Vec2(%.5f, %.5f))\n' % (pas[0], pas[1]))
        out_file.write(i2 + 'patch.setThreshold(%.2f)\n' % threshold)
        out_file.write(i2 + 'patch.setRadius(%.2f)\n' % radius)
        out_file.write(i2 + 'patch.setUvScale(VBase2(%.4f, %.4f))\n' % (uvscale[0], uvscale[1]))
        out_file.write(i2 + 'patch.setHighColor(Vec4(%.4f, %.4f, %.4f, %.4f))\n' % (hcolor[0], hcolor[1], hcolor[2], hcolor[3]))
        out_file.write(i2 + 'patch.setLowColor(Vec4(%.4f, %.4f, %.4f, %.4f))\n' % (lcolor[0], lcolor[1], lcolor[2], lcolor[3]))
        for i in range(self.patch.getNumWaves()):
            if self.patch.isWaveEnabled(i):
                out_file.write(i2 + 'patch.enableWave(' + str(i) + ')\n')
            else:
                out_file.write(i2 + 'patch.disableWave(' + str(i) + ')\n')
            out_file.write(i2 + 'patch.setWaveTarget(%s, %s)\n' % (i, self.__formatWaveTarget(self.patch.getWaveTarget(i))))
            out_file.write(i2 + 'patch.setWaveFunc(%s, %s)\n' % (i, self.__formatWaveFunc(self.patch.getWaveFunc(i))))
            if self.patch.getWaveFunc(i) == SeaPatchRoot.WFSin:
                out_file.write(i2 + 'patch.setWaveDirection(' + str(i) + ', Vec2(%.4f, %.4f))\n' % (mdir[i][0], mdir[i][1]))
            out_file.write(i2 + 'patch.setChoppyK(' + str(i) + ', %d)\n' % mchoppy[i])
            out_file.write(i2 + 'patch.setWaveAmplitude(%s, %.4f)\n' % (i, mamplitude[i]))
            out_file.write(i2 + 'patch.setWaveLength(%s, %.4f)\n' % (i, mlength[i]))
            out_file.write(i2 + 'patch.setWaveSpeed(%s, %.4f)\n' % (i, mspeed[i]))

    def __formatWaveTarget(self, target):
        if target == SeaPatchRoot.WTZ:
            return 'SeaPatchRoot.WTZ'
        elif target == SeaPatchRoot.WTU:
            return 'SeaPatchRoot.WTU'
        elif target == SeaPatchRoot.WTV:
            return 'SeaPatchRoot.WTV'

    def __formatWaveFunc(self, func):
        if func == SeaPatchRoot.WFSin:
            return 'SeaPatchRoot.WFSin'
        elif func == SeaPatchRoot.WFNoise:
            return 'SeaPatchRoot.WFNoise'

    def loadSeaPatchFileExt(self, filename, patch=None):
        if patch == None:
            patch = SeaPatchRoot()
            patch.assignEnvironmentFrom(self.patch)
        patch.resetProperties()
        if not isinstance(filename, Filename):
            filename = Filename.fromOsSpecific(filename)
        searchPath = DSearchPath()
        if AppRunnerGlobal.appRunner:
            searchPath.appendDirectory(Filename.expandFrom('$POTCO_2_ROOT/etc'))
        else:
            searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$PIRATES/src/seapatch')))
            searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('pirates/src/seapatch')))
            searchPath.appendDirectory(Filename('etc'))
            searchPath.appendDirectory(Filename('.'))
        found = vfs.resolveFilename(filename, searchPath)
        if not found:
            print 'seapatch file not found: %s' % filename
        else:
            data = vfs.readFile(filename, 1)
            data = data.replace('\r', '')
            exec data
        return patch

    def loadSeaPatchFile(self, filename):
        self.loadSeaPatchFileExt(filename, patch=self.patch)
        self.updateWater(base.options.getTerrainDetailSetting())

    def lerpToSeaPatchFile(self, filename, duration, name=None, blendType='easeInOut'):
        newpatch = self.loadSeaPatchFileExt(filename)
        newpatch.setCenter(self.center)
        newpatch.setAnchor(self.anchor)
        sealerp = LerpSeaPatchInterval(name, duration, blendType, self.patch, self.patch, newpatch)
        return sealerp

    def calcFlatWellScale(self, x=0, y=0, node=None):
        p3 = self.p3
        p3.set(x, y, 0)
        if node == None:
            node = self.anchor
        ap = self.anchor.getRelativePoint(node, p3)
        return self.patch.calcFlatWellScale(ap.getX(), ap.getY())

    def calcHeight(self, x=0, y=0, z=0, node=None):
        p3 = self.p3
        p3.set(x, y, z)
        if node == None:
            node = self.anchor
        ap = self.anchor.getRelativePoint(node, p3)
        cp = self.center.getRelativePoint(node, p3)
        x = cp.getX()
        y = cp.getY()
        dist2 = x * x + y * y
        return self.patch.calcHeight(ap.getX(), ap.getY(), dist2)

    def calcFilteredHeight(self, x=0, y=0, z=0, minWaveLength=0, node=None):
        p3 = self.p3
        p3.set(x, y, z)
        if node == None:
            node = self.anchor
        ap = self.anchor.getRelativePoint(node, p3)
        cp = self.center.getRelativePoint(node, p3)
        x = cp.getX()
        y = cp.getY()
        dist2 = x * x + y * y
        return self.patch.calcFilteredHeight(ap.getX(), ap.getY(), minWaveLength, dist2)

    def calcHeightForMass(self, x=0, y=0, z=0, node=None, mass=1, area=1):
        p3 = self.p3
        p3.set(x, y, z)
        if node == None:
            node = self.anchor
        ap = self.anchor.getRelativePoint(node, p3)
        cp = self.center.getRelativePoint(node, p3)
        x = cp.getX()
        y = cp.getY()
        dist2 = x * x + y * y
        return self.patch.calcHeightForMass(ap.getX(), ap.getY(), dist2, mass, area)

    def calcHeightAndNormal(self, x=0, y=0, z=0, node=None):
        p3 = self.p3
        p3.set(x, y, z)
        if node == None:
            node = self.anchor
        ap = self.anchor.getRelativePoint(node, p3)
        ax = ap.getX()
        ay = ap.getY()
        cp = self.center.getRelativePoint(node, p3)
        x = cp.getX()
        y = cp.getY()
        dist2 = x * x + y * y
        height = self.patch.calcHeight(ax, ay, dist2)
        normal = self.patch.calcNormal(height, ax, ay, dist2)
        normal = node.getRelativeVector(self.anchor, normal)
        return (
         height, normal)

    def calcHeightAndNormalForMass(self, x=0, y=0, z=0, node=None, mass=1, area=1):
        p3 = self.p3
        p3.set(x, y, z)
        if node == None:
            node = self.anchor
        ap = self.anchor.getRelativePoint(node, p3)
        ax = ap.getX()
        ay = ap.getY()
        cp = self.center.getRelativePoint(node, p3)
        x = cp.getX()
        y = cp.getY()
        dist2 = x * x + y * y
        height = self.patch.calcHeightForMass(ax, ay, dist2, mass, area)
        normal = self.patch.calcNormalForMass(height, ax, ay, dist2, mass, area)
        normal = node.getRelativeVector(self.anchor, normal)
        return (
         height, normal)

    def setSeaWeights(self, weight_map):
        pass

    def _timeChange(self, stateId, stateDuration, elapsedTime, transitionTime):
        transTime = 2.0
        if stateId == PiratesGlobals.TOD_DAWN:
            highColor = Vec4(1.0, 1.0, 1.0, 0.5)
            lowColor = Vec4(0.5, 0.3, 0.3, 0.8)
        elif stateId == PiratesGlobals.TOD_DAY:
            highColor = Vec4(1.0, 1.0, 1.0, 0.5)
            lowColor = Vec4(0.2, 0.2, 0.2, 0.8)
        elif stateId == PiratesGlobals.TOD_DUSK:
            highColor = Vec4(1.0, 1.0, 1.0, 0.5)
            lowColor = Vec4(0.7, 0.2, 0.2, 0.8)
        elif stateId == PiratesGlobals.TOD_NIGHT:
            highColor = Vec4(1.0, 1.0, 1.0, 0.5)
            lowColor = Vec4(0.2, 0.2, 0.8, 0.8)
        elif stateId == PiratesGlobals.TOD_STARS:
            highColor = Vec4(1.0, 1.0, 1.0, 0.5)
            lowColor = Vec4(0.2, 0.2, 0.4, 0.8)
        elif stateId in [PiratesGlobals.TOD_HALLOWEEN, PiratesGlobals.TOD_FULLMOON, PiratesGlobals.TOD_HALFMOON2, PiratesGlobals.TOD_HALFMOON]:
            highColor = Vec4(1.0, 1.0, 1.0, 0.5)
            lowColor = Vec4(0.5, 0.25, 0.6, 0.8)
        else:
            highColor = Vec4(1.0, 1.0, 1.0, 0.5)
            lowColor = Vec4(0.2, 0.2, 0.2, 0.8)
        self.patch.setHighColor(highColor)
        self.patch.setLowColor(lowColor)

    maintenanceTaskName = 'maintenanceTask'

    def initialize(self):
        self.time = 0.0
        self.cacheTime = 0.0
        self.updateTimeInSeconds = 10.0
        self.cacheUpdateTimeInSeconds = 60.0 * 5.0

    def cleanup(self):
        taskMgr.remove(self.maintenanceTaskName)

    def setup(self, updateTimeInSeconds, cacheUpdateTimeInSeconds, taskPriority):
        self.updateTimeInSeconds = updateTimeInSeconds
        self.cacheUpdateTimeInSeconds = cacheUpdateTimeInSeconds
        taskMgr.add(self.maintenanceTask, self.maintenanceTaskName, priority=taskPriority)

    def maintenanceFunction(self):
        models_freed = 1
        textures_freed = 1
        while models_freed > 0 or textures_freed > 0:
            models_freed = ModelPool.garbageCollect()
            textures_freed = TexturePool.garbageCollect()
            if models_freed > 0 or textures_freed > 0:
                pass

    def clearCachesFunction(self):
        RenderState.clearCache()
        TransformState.clearCache()

    def maintenanceTask(self, task):
        if task.time - self.time >= self.updateTimeInSeconds:
            self.maintenanceFunction()
            self.time = task.time
        if task.time - self.cacheTime >= self.cacheUpdateTimeInSeconds:
            self.clearCachesFunction()
            self.cacheTime = task.time
        return Task.cont

    def getSpecialEffectsLevel(self):
        try:
            level = base.options.getSpecialEffectsSetting()
        except:
            level = Options.SpecialEffectsHigh

        return level

    def addMotionTrail(self, parent):
        if self.motion_trail == None:
            motion_trail = MotionTrail('sword_motion_trail', parent)
            if False:
                axis = loader.loadModel('models/misc/xyzAxis')
                axis.reparentTo(parent)
            test_vertex_list = [Vec4(0.0, 0.4, 0.0, 1.0), Vec4(0.0, 2.0, 0.0, 1.0), Vec4(-0.55, 2.95, 0.0, 1.0)]

            def test_vertex_function(motion_trail_vertex, vertex_id, context):
                return test_vertex_list[vertex_id]

            index = 0
            total_test_vertices = len(test_vertex_list)
            while index < total_test_vertices:
                motion_trail_vertex = motion_trail.add_vertex(index, test_vertex_function, None)
                if True:
                    if index == 0:
                        motion_trail_vertex.start_color = Vec4(0.0, 0.25, 0.0, 1.0)
                        motion_trail_vertex.end_color = Vec4(0.0, 0.0, 0.0, 1.0)
                    if index == 1:
                        motion_trail_vertex.start_color = Vec4(0.25, 0.0, 0.0, 1.0)
                        motion_trail_vertex.end_color = Vec4(0.0, 0.0, 0.0, 1.0)
                    if index == 2:
                        motion_trail_vertex.start_color = Vec4(0.0, 0.0, 1.0, 1.0)
                        motion_trail_vertex.end_color = Vec4(0.0, 0.0, 0.0, 1.0)
                    if index == 3:
                        motion_trail_vertex.start_color = Vec4(0.0, 1.0, 1.0, 1.0)
                        motion_trail_vertex.end_color = Vec4(0.0, 0.0, 0.0, 1.0)
                    if index == 4:
                        motion_trail_vertex.start_color = Vec4(1.0, 1.0, 0.0, 1.0)
                        motion_trail_vertex.end_color = Vec4(0.0, 0.0, 0.0, 1.0)
                    if index == 0:
                        motion_trail_vertex.start_color = Vec4(0.0, 0.1, 0.0, 1.0)
                        motion_trail_vertex.end_color = Vec4(0.0, 0.0, 0.0, 1.0)
                    if index == 1:
                        motion_trail_vertex.start_color = Vec4(0.25, 0.0, 0.0, 1.0)
                        motion_trail_vertex.end_color = Vec4(0.0, 0.0, 0.0, 1.0)
                index += 1

            motion_trail.update_vertices()
            motion_trail.register_motion_trail()
            motion_trail.calculate_relative_matrix = True
            motion_trail.root_node_path = parent
            motion_trail.time_window = 0.25
            motion_trail.continuous_motion_trail = False
            motion_trail.end_motion_trail()
            self.motion_trail = motion_trail
            if not False:
                print 'ADD MOTION TRAIL'
                axis = Vec3(0.0, 0.0, 1.0)
                time = 0.0
                angle = (1.0 - time) * 90.0
                matrix = Mat4.rotateMat(angle, axis)
                self.motion_trail.update_motion_trail(time, matrix)
                time = 0.2
                angle = (1.0 - time) * 90.0
                matrix = Mat4.rotateMat(angle, axis)
                self.motion_trail.update_motion_trail(time, matrix)
                time = 0.4
                angle = (1.0 - time) * 90.0
                matrix = Mat4.rotateMat(angle, axis)
                self.motion_trail.update_motion_trail(time, matrix)
                time = 0.6
                angle = (1.0 - time) * 90.0
                matrix = Mat4.rotateMat(angle, axis)
                self.motion_trail.update_motion_trail(time, matrix)
                time = 0.8
                angle = (1.0 - time) * 90.0
                matrix = Mat4.rotateMat(angle, axis)
                self.motion_trail.update_motion_trail(time, matrix)
                time = 1.0
                angle = (1.0 - time) * 90.0
                matrix = Mat4.rotateMat(angle, axis)
                self.motion_trail.update_motion_trail(time, matrix)
        return