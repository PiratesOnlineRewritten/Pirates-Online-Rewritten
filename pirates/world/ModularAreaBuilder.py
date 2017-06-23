from pandac.PandaModules import *
from otp.otpbase import OTPRender
from pirates.world.SectionAreaBuilder import SectionAreaBuilder
from pirates.leveleditor import EditorGlobals

class ModularAreaBuilder(SectionAreaBuilder):

    def __init__(self, master):
        SectionAreaBuilder.__init__(self, master)
        self.subLights = {}
        self.adjTable = {}
        self.subLights = {}
        self.areaLights = {}

    def _postLoadStep(self):
        SectionAreaBuilder._postLoadStep(self)
        adjTable = base.worldCreator.uidAdjTables.get(self.master.uniqueId, {})
        for light in self.areaGeometry.findAllMatches('**/=SubLight;+s'):
            zone = self.sectionsToParent.get(light.getTag('SubLight'))
            if zone:
                self.addSubLight(zone, light.find('**/+Light').node())

        self.lightObjects()

    def addChildObj(self, levelObj):
        root = SectionAreaBuilder.addChildObj(self, levelObj)
        if levelObj['Type'] == 'Cave_Pieces':
            root.setTag('modular', '1')
            if levelObj.get('OverrideFog', False):
                root.setTag('fog-onset', str(levelObj.get('FogOnSet', 0)))
                root.setTag('fog-peak', str(levelObj.get('FogPeak', 100)))

    def lightObjects(self):
        self.generateAdjLightSets()
        for zone in self.sections:
            parent = self.sectionsToParent[zone]
            lightAttrib = self.areaLights.get(parent)
            if not lightAttrib:
                continue
            self.sections[zone].setAttrib(lightAttrib)

        for uid, obj in self.largeObjects.iteritems():
            visZone = obj.getTag('visZone')
            modular = obj.getTag('modular')
            if modular:
                self.largeObjects[uid].setAttrib(self.areaLights[uid])
            elif visZone:
                self.largeObjects[uid].setAttrib(self.areaLights[self.sectionsToParent[visZone]])

        for node in self.areaGeometry.findAllMatches('**/=PortalVis'):
            visZone = node.getTag('PortalVis')
            node.setAttrib(self.areaLights[self.sectionsToParent[visZone]])

    def generateAdjLightSets(self):
        for zone in self.adjTable:
            lightAttrib = LightAttrib.make()
            group = self.subLights.get(zone, [])
            for light in group:
                lightAttrib = lightAttrib.addLight(light)

            for adjZone in self.adjTable[zone]:
                adjGroup = self.subLights.get(adjZone, [])
                for light in adjGroup:
                    lightAttrib = lightAttrib.addLight(light)

            self.areaLights[zone] = lightAttrib

    def addSubLight(self, zone, light):
        subLightGroup = self.subLights.get(zone)
        if not subLightGroup:
            subLightGroup = self.subLights[zone] = []
        subLightGroup.append(light)

    def makeLight(self, levelObj):
        light = EditorGlobals.LightModular(levelObj, self.areaGeometry, drawIcon=False)
        if levelObj.get('VisZone'):
            if light:
                light.setTag('SubLight', levelObj.get('VisZone'))
                OTPRender.renderReflection(False, light, 'p_light', None)
        return light

    def handleLighting(self, obj, visZone):
        parent = self.sectionsToParent.get(visZone)
        if parent and self.areaLights.has_key(parent):
            obj.setAttrib(self.areaLights[parent])
        SectionAreaBuilder.handleLighting(self, obj, visZone)

    def localAvLeaving(self):
        localAvatar.clearAttrib(LightAttrib.getClassType())

    def disableDynamicLights(self):
        pass

    def addSectionObj(self, obj, visZone, logError=0):
        SectionAreaBuilder.addSectionObj(self, obj, visZone)
        parent = self.sectionsToParent.get(visZone)
        if parent and self.areaLights.has_key(parent):
            obj.setAttrib(self.areaLights[parent])
        elif logError:
            errorMessage = 'Chest missing parent visZone %s location %s position %s' % (visZone, localAvatar.getLocation(), localAvatar.getPos())
            localAvatar.sendAILog(errorMessage)
        elif __dev__:
            set_trace()

    def arrived(self):
        render.setClipPlane(base.farCull)

    def left(self):
        render.clearClipPlane()

    def triggerEffects(self, visZone):
        SectionAreaBuilder.triggerEffects(self, visZone)
        parent = self.sectionsToParent.get(visZone)
        if parent:
            module = self.largeObjects.get(parent)
            if module and module.getTag('modular'):
                onset = module.getTag('fog-onset')
                peak = module.getTag('fog-peak')
                if onset:
                    onset = float(onset)
                    peak = float(peak)
                    base.cr.timeOfDayManager.lerpLinearFog(onset, peak)
                else:
                    base.cr.timeOfDayManager.restoreLinearFog()

    def unloadObjects(self):
        self.areaLights = {}
        self.subLights = {}
        self.adjTable = {}
        SectionAreaBuilder.unloadObjects(self)