import random
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
DYN_LIGHT_AMBIENT = 0
DYN_LIGHT_DIRECTIONAL = 1
DYN_LIGHT_POINT = 2
DYN_LIGHT_SPOT = 3

class DynamicLight(NodePath):

    def __init__(self, type=DYN_LIGHT_POINT, parent=None, pos=None, hpr=None, color=None, atten=None, exp=None, flicker=False, drawIcon=False, modular=False):
        self.light = None
        self.lightNodePath = None
        self.flickerIval = None
        self.attenIval = None
        self.type = None
        self.baseExp = 0.0
        self.intensity = 1.0
        self.baseIntensity = 1.0
        self.flickRate = 1.0
        self.drawIcon = drawIcon
        self.modular = modular
        self.flicker = flicker
        if color:
            self.color = color
        else:
            self.color = (1, 1, 1, 1)
        self.models = []
        if atten:
            self.baseAtten = atten
        else:
            self.baseAtten = (1, 0, 0)
        if exp:
            self.baseExp = exp
        light = self.setType(type, isInit=True)
        if parent == None:
            parent = render
        self.reparentTo(parent)
        if pos == None:
            pos = (0, 0, 0)
        self.setPos(pos)
        if hpr == None:
            hpr = (0, 0, 0)
        self.setHpr(hpr)
        if self.flicker:
            self.startFlickering()
        return

    def setType(self, type, isInit=False):
        if self.type == type:
            return None
        if type == DYN_LIGHT_AMBIENT:
            light = AmbientLight('AmbientLight')
        elif type == DYN_LIGHT_DIRECTIONAL:
            light = DirectionalLight('DirectionalLight')
            self.stopFlickering()
        elif type == DYN_LIGHT_POINT:
            light = PointLight('PointLight')
            if self.modular:
                light.setAttenuation(VBase3(*self.baseAtten))
        elif type == DYN_LIGHT_SPOT:
            light = Spotlight('Spotlight')
            if self.modular:
                light.setAttenuation(VBase3(*self.baseAtten))
                light.setExponent(self.baseExp)
            else:
                return None
        self.turnOff()
        self.type = type
        if isInit:
            if self.modular:
                NodePath.__init__(self, 'modularLight')
            else:
                NodePath.__init__(self, 'dynamicLight')
        if self.lightNodePath:
            self.lightNodePath.removeNode()
        self.lightNodePath = self.attachNewNode(light)
        if self.modular:
            self.setName('ModularLight')
        else:
            self.setName('DynamicLight')
        if base.config.GetBool('draw-light-icons', 0) or self.drawIcon:
            if isInit:
                if self.modular:
                    newModel = loader.loadModel('models/props/light_tool_bulb_modular')
                else:
                    newModel = loader.loadModel('models/props/light_tool_bulb')
                    newModel.setBillboardPointEye()
                    newModel.reparentTo(self)
                    newModel.flattenLight()
                    self.models.append(newModel)
                if hasattr(self, 'lightDirectionModel'):
                    self.lightDirectionModel.removeNode()
                    del self.lightDirectionModel
                if type == DYN_LIGHT_DIRECTIONAL or type == DYN_LIGHT_SPOT:
                    lightDirectionModel = loader.loadModel('models/props/light_tool_arrow')
                    lightDirectionModel.setScale(5.0)
                    lightDirectionModel.setY(2)
                    lightDirectionModel.setH(180)
                    lightDirectionModel.reparentTo(self)
                    self.lightDirectionModel = lightDirectionModel
        self.light = light
        if not self.modular:
            self.turnOn()
        if self.color:
            self.setColor(self.color)
        return light

    def unload(self):
        self.lightNodePath.removeNode()
        self.removeNode()

    def setAttenuation(self, atten):
        self.setQuadraticAttenuation(atten)

    def setQuadraticAttenuation(self, atten):
        if not self.modular:
            return
        atten = atten * atten / 100.0
        self.baseAtten = (
         self.baseAtten[0], self.baseAtten[1], atten)
        if hasattr(self.light, 'setAttenuation'):
            self.light.setAttenuation(VBase3(*self.baseAtten))

    def setConstantAttenuation(self, atten):
        if not self.modular:
            return
        self.baseAtten = (
         atten, self.baseAtten[1], self.baseAtten[2])
        if hasattr(self.light, 'setAttenuation'):
            self.light.setAttenuation(VBase3(*self.baseAtten))

    def setLinearAttenuation(self, atten):
        if not self.modular:
            return
        self.baseAtten = (
         self.baseAtten[0], atten, self.baseAtten[2])
        if hasattr(self.light, 'setAttenuation'):
            self.light.setAttenuation(VBase3(*self.baseAtten))

    def setTempIntensity(self, intensity):
        self.intensity = intensity
        self.setIntensityColor()

    def setIntensity(self, intensity):
        if self.modular:
            intensity = 1.0
        self.intensity = intensity
        self.baseIntensity = intensity
        self.setIntensityColor()

    def setConeAngle(self, angle):
        if hasattr(self.light, 'getLens'):
            self.light.getLens().setFov(angle)

    def setDropOff(self, angle):
        self.baseExp = angle
        if hasattr(self.light, 'setExponent'):
            self.light.setExponent(angle)

    def setIntensityColor(self):
        mup = self.intensity
        color = VBase4(self.color[0] * mup, self.color[1] * mup, self.color[2] * mup, self.color[3] * mup)
        for currModel in self.models:
            if currModel and not currModel.isEmpty():
                currModel.setColor(color)

        self.light.setColor(color)

    def setColor(self, color):
        self.color = color
        self.setIntensityColor()

    def getColor(self):
        return self.light.getColor()

    def setColorCustom(self, color):
        self.color = color
        self.setColor(color)

    def clearColorCustom(self):
        self.setColor((1, 1, 1, 1))

    def setFlickering(self, flickering):
        self.flicker = flickering
        if flickering:
            self.startFlickering()
        else:
            self.stopFlickering()

    def turnOn(self):
        if self.light:
            render.setLight(self.lightNodePath)
            return self
        else:
            return None
        return None

    def turnOff(self):
        if self.light:
            if self.canFlicker():
                self.stopFlickering()
            render.clearLight(self.lightNodePath)
            return self
        else:
            return None
        return None

    def canFlicker(self):
        return self.type != DYN_LIGHT_DIRECTIONAL and self.type != DYN_LIGHT_AMBIENT

    def startFlickering(self):
        self.stopFlickering()
        if not self.canFlicker():
            return
        if self.flicker:

            def flickerFunc():
                fromData = self.intensity
                originalA = self.baseIntensity
                offset = originalA * 0.1 * self.flickRate
                range = originalA * 0.4 * self.flickRate
                tgtA = originalA + (random.random() * range - offset)
                tgtA = max(0.0, tgtA)
                tgtA = min(3.0, tgtA)
                toData = tgtA
                duration = 0.05 + random.random() * 0.2
                if self.attenIval:
                    self.attenIval.finish()
                self.attenIval = LerpFunctionInterval(self.setTempIntensity, duration=duration, toData=toData, fromData=fromData, name='DynamicLightFlicker-%d' % id(self))
                self.attenIval.start()

            flickerIval = Sequence(Func(flickerFunc), Wait(0.25), name='DynamicLightHandle-%d' % id(self))
            flickerIval.loop()
            self.flickerIval = flickerIval

    def stopFlickering(self):
        if self.flickerIval:
            self.flickerIval.finish()
            self.flickerIval = None
        if self.attenIval:
            self.attenIval.finish()
            self.attenIval = None
        return

    def setFlickRate(self, flickRate):
        self.flickRate = flickRate