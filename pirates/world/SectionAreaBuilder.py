import random
import re
import types
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.actor import *
from pirates.world import WorldGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.npc import NavySailor
from pirates.pirate.HumanDNA import *
from pirates.npc import Skeleton
from pirates.npc import Townfolk
from pirates.battle import Sword
from direct.interval.IntervalGlobal import *
from otp.otpbase import OTPRender
from otp.otpbase import OTPGlobals
from pirates.leveleditor import CustomAnims
from pirates.world.AreaBuilderBase import AreaBuilderBase, ModelDef
from pirates.effects import DynamicLight
from pirates.effects import ObjectEffects
from pirates.effects import SoundFX
AREA_CHILD_TYPE_PROP = 1

class Section(NodePath):

    def __init__(self, name):
        NodePath.__init__(self, ModelNode('Section-%s' % name))
        node = FadeLODNode('sectionLOD')
        self.lodRoot = self.attachNewNode(node)
        self.high = self.lodRoot.attachNewNode(PandaNode('high'))
        self.med = self.lodRoot.attachNewNode(PandaNode('med'))
        self.low = self.lodRoot.attachNewNode(PandaNode('low'))
        self.superLow = self.lodRoot.attachNewNode(PandaNode('superLow'))
        self.effectsRoot = self.attachNewNode(PandaNode('effectsRoot'))
        node.addSwitch(1000, 0)
        node.addSwitch(10000, 1000)
        node.addSwitch(100000, 10000)
        node.addSwitch(1000000, 100000)
        self.collisions = self.attachNewNode('collisions')


class SectionAreaBuilder(AreaBuilderBase):
    notify = directNotify.newCategory('SectionAreaBuilder')

    def __init__(self, master):
        AreaBuilderBase.__init__(self, master)
        self.doneParenting = False
        self.oldVis = NodePathCollection()
        self.visZone = ''
        self.potentialVisHeight = -10000
        self.potentialVisZone = ''
        self.visSets = {}
        self.visTable = {}
        self.terrainDict = {}
        self.tempSections = {}
        self.sections = {}
        self.objectSets = {}
        self.effectsSets = {}
        self.currEffectSet = set()
        self.sectionObjs = set()
        self.sectionsToParent = {}
        self.visZoneMinimaps = {}
        self.visZoneTunnels = {}

    def addChildObj(self, levelObj):
        transform = levelObj.transform
        objData = levelObj.data
        uid = levelObj.uniqueId
        visZone = objData.get('VisZone')
        size = objData.get('VisSize')
        if objData['Type'] == 'Animated Avatar - Skeleton' or objData['Type'] == 'Animated Avatar - Navy' or objData['Type'] == 'Animated Avatar - Townfolk' or objData['Type'] == 'Animated Avatar':
            propNp = self.getPropAvatarNode(objData, transform, uid)
            if visZone:
                if size != 'Large':
                    section = self.tempSections.get(visZone)
                    if section:
                        propNp.wrtReparentTo(section)
                else:
                    propNp.setName('large_object')
                    propNp.wrtReparentTo(self.largeObjectsRoot)
            return propNp
        model = self.getModel(objData)
        if objData.get('DisableCollision', False):
            collisionNodes = model.collisions.findAllMatches('**/+CollisionNode')
            for collisionNode in collisionNodes:
                collisionNode.removeNode()

        if objData['Type'] == 'Collision Barrier':
            model.root.findAllMatches('**/+GeomNode').detach()
        if objData['Type'] == 'Invasion Barrier':
            model.root.findAllMatches('**/+GeomNode').detach()
            collisionNodes = model.collisions.findAllMatches('**/+CollisionNode')
            for collisionNode in collisionNodes:
                collisionNode.node().setIntoCollideMask(collisionNode.node().getIntoCollideMask() | OTPGlobals.CameraBitmask)

        if not objData.get('Visible', True):
            model.root.findAllMatches('**/+GeomNode').detach()
            collisionNodes = model.collisions.findAllMatches('**/+CollisionNode')
            for collisionNode in collisionNodes:
                collisionNode.removeNode()

        self.checkForFootprint(levelObj, visZone)
        signLocator = model.root.find('**/sign_locator')
        if signLocator:
            self.buildSign(objData, signLocator)
        model.root.reparentTo(self.master)
        model.root.setTransform(transform)
        zones = model.collisions.findAllMatches('**/collision_zone*;+s')
        for zone in zones:
            name = zone.getName()
            name = '%s_%s' % (name, uid)
            zone.setName(name)
            zone.setTag('parentUid', uid)
            self.tempSections[name[15:]] = self.createSection(name[15:], zone)

        if size != 'Large':
            self.processSmallObject(model)
            if visZone:
                section = self.tempSections.get(visZone)
                if section:
                    if model.effects:
                        model.effects.wrtReparentTo(section.effectsRoot)
                    model.high.wrtReparentTo(section.high)
                    if model.med:
                        model.med.wrtReparentTo(section.med)
                    if model.low:
                        model.low.wrtReparentTo(section.low)
                    if model.superLow:
                        model.superLow.wrtReparentTo(section.superLow)
                    if model.collisions.findAllMatches('**/+CollisionNode').getNumPaths() > 0:
                        model.collisions.wrtReparentTo(section.collisions)
                    model.root.detachNode()
                    model.root = model.high
                else:
                    model.root.wrtReparentTo(self.staticGridRoot)
            else:
                model.root.wrtReparentTo(self.staticGridRoot)
        else:
            if visZone:
                model.root.setTag('visZone', visZone)
            model.root.wrtReparentTo(self.largeObjectsRoot)
            model.root.setName('large_object')
            model.root.setTag('uid', uid)
        return model.root

    def checkForFootprint(self, levelObj, visZone):
        footprint = AreaBuilderBase.checkForFootprint(self, levelObj)
        if footprint:
            if visZone:
                footprint.setTag('VisZone Minimap', str(self.visZoneMinimaps.get(visZone, 0)))
                return footprint
            elif levelObj.get('VisSize') == 'Large':
                footprint.setTag('VisZone Minimap', '0')
                return footprint
            else:
                footprint.stash()
                return None
        return None

    def cleanupData(self):
        AreaBuilderBase.cleanupData(self)
        self.oldVis = NodePathCollection()
        self.visZone = ''
        self.visSets = {}
        self.visHelper = {}
        self.visTable = {}
        self.terrainDict = {}
        self.tempSections = {}
        self.sections = {}
        self.objectSets = {}
        self.effectsSets = {}
        self.currEffectSet = set()
        self.sectionObjs = set()
        self.sectionsToParent = {}
        self.ignore('collisionLoopFinished')

    @report(types=['args'], dConfigParam='minimap')
    def createSection(self, name, collision):
        section = Section(name)
        centerTrans = TransformState.makePos(collision.getBounds().getCenter())
        baseTrans = collision.getTransform(self.master).compose(centerTrans)
        section.setPos(baseTrans.getPos())
        section.reparentTo(self.staticGridRoot)
        self.tempSections[name] = section
        return section

    def unloadObjects(self):
        self.tempSections = {}
        self.sections = {}
        self.sectionObjs = set()
        self.visTable = {}
        self.largeObjectsVis = {}
        self.oldVis = NodePathCollection()
        AreaBuilderBase.unloadObjects(self)

    @report(types=['args'], dConfigParam='minimap')
    def _preSubObjectsStep(self):
        AreaBuilderBase._preSubObjectsStep(self)
        collisionSet = self.master.geom.findAllMatches('**/collision_zone_*;+s')
        for collision in collisionSet:
            name = collision.getName()[15:]
            section = self.createSection(name, collision)
            self.tempSections[name] = section
            self.setupSwitchDistances(section.lodRoot.node(), collision)

        self.visZoneMinimaps = base.worldCreator.uidVisZoneMinimaps.get(self.master.uniqueId, {})
        self.visZoneTunnels = base.worldCreator.uidVisZoneTunnels.get(self.master.uniqueId, {})

    @report(types=['args'], dConfigParam='minimap')
    def _postSubObjectsStep(self):
        self.largeObjectsRoot.findAllMatches('**/collision_zone_*;+s').wrtReparentTo(self.collisions)
        for zone in self.tempSections.values():
            zone.lodRoot.flattenStrong()
            if base.options.getTerrainDetailSetting() == 0:
                zone.lodRoot.getChild(0).reparentTo(zone)
                zone.lodRoot.detachNode()

        self.areaGeometry.setTag('VisZoneMinimaps', repr(self.visZoneMinimaps))
        self.areaGeometry.setTag('VisZoneTunnels', repr(self.visZoneTunnels))
        AreaBuilderBase._postSubObjectsStep(self)

    @report(types=['args'], dConfigParam='minimap')
    def _postLoadStep(self):
        AreaBuilderBase._postLoadStep(self)
        self.accept('collisionLoopFinished', self.processCollisions)
        self.visTable = base.worldCreator.uidVisTables.get(self.master.uniqueId, {})
        for section in self.master.geom.findAllMatches('**/collision_zone_*') + self.areaGeometry.findAllMatches('**/collision_zone_*'):
            uid = section.getTag('parentUid')
            if uid:
                self.sectionsToParent[section.getName()[15:]] = uid
            else:
                uid = section.getName()[15:]
                self.sectionsToParent[uid] = uid

        for uid, obj in self.largeObjects.iteritems():
            visZone = obj.getTag('visZone')
            if visZone:
                visData = self.visTable.get(visZone)
                if visData:
                    if uid not in visData[1]:
                        visData[1].append(uid)

        adjTable = base.worldCreator.uidAdjTables.get(self.master.uniqueId)
        if adjTable:
            self.adjTable = adjTable
        for zone in self.visTable:
            self.effectsSets[zone] = set()

        self.setupCollisionSections()
        self.setupVisibleData()
        visZoneMaps = self.areaGeometry.getTag('VisZoneMinimaps')
        visZoneTunnels = self.areaGeometry.getTag('VisZoneTunnels')
        try:
            self.visZoneMinimaps = eval(visZoneMaps)
        except:
            base.cr.centralLogger.writeClientEvent('failed to load minimap zones for area %s, (%s)' % (self.master.uniqueId, visZoneMaps))
            self.visZoneMinimaps = {}

        try:
            self.visZoneTunnels = eval(visZoneTunnels)
        except:
            base.cr.centralLogger.writeClientEvent('failed to load tunnel zones for area %s, (%s)' % (self.master.uniqueId, visZoneTunnels))
            self.visZoneTunnels = {}

        self.areaGeometry.clearTag('VisZoneMinimaps')
        self.areaGeometry.clearTag('VisZoneTunnels')

    @report(types=['args'], dConfigParam='minimap')
    def setupCollisionSections(self):
        self.visHelper = {}
        for zoneName in self.visTable:
            self.visHelper[zoneName] = set()
            section = self.areaGeometry.find('**/Section-%s' % zoneName)
            if section:
                section.setTag('visZone', zoneName)
                self.sections[zoneName] = section
                self.accept('againcollision_zone_%s' % zoneName, self.handleNewSection)
                self.accept('entercollision_zone_%s' % zoneName, self.handleNewSection)
                self.sections[zoneName].stash()

    def setupVisibleData(self):
        for zoneName in self.visTable:
            zones = self.visTable[zoneName][0]
            for zone in zones:
                self.visHelper[zone].add(zoneName)

        for obj in self.largeObjects.values():
            obj.stash()

        self.terrainDict = {}
        for x in self.master.geom.findAllMatches('**/naturalBarrier_*;+s') + self.master.geom.findAllMatches('**/treeBackground_*;+s') + self.master.geom.findAllMatches('**/rockFormation_*;+s') + self.master.geom.findAllMatches('**/fortVis_*;+s'):
            self.terrainDict[x.getName()] = x
            x.stash()

        for zone in self.visTable:
            visZone = self.visTable[zone]
            paths = NodePathCollection()
            effectsList = set()
            if self.sections.get(zone):
                paths.addPath(self.sections[zone])
            for cs in visZone[0]:
                section = self.sections.get(cs)
                if section:
                    paths.addPath(section)

            for uid in visZone[1]:
                largeObj = self.largeObjects.get(uid)
                if largeObj:
                    paths.addPath(largeObj)

            if len(visZone) > 2:
                for terrain in visZone[2]:
                    obj = self.terrainDict.get(terrain)
                    if obj:
                        paths.addPath(obj)

            self.visSets[zone] = paths

    def processCollisions(self):
        self.potentialVisHeight = -10000
        if not self.potentialVisZone:
            return
        if self.potentialVisZone == self.visZone:
            return
        if self.potentialVisZone not in self.visTable:
            return
        if self.visZoneLock:
            return
        oldZone = self.visZone
        self.visZone = self.potentialVisZone
        newVis = self.visSets.get(self.visZone, NodePathCollection())
        self.updateCurrEffectSet()
        self.oldVis.stash()
        newVis.unstash()
        self.oldVis = newVis
        messenger.send('localAvatarVisZoneChanged')
        parent = self.sectionsToParent.get(self.visZone)
        self.handleLighting(localAvatar, self.visZone)
        self.triggerEffects(self.visZone)
        localAvatar.d_setVisZone(self.visZone)
        self.master.setMinimapArea(self.visZoneMinimaps.get(self.visZone, 0))

    def handleNewSection(self, entry):
        name = entry.getIntoNode().getName()[15:]
        z = entry.getSurfacePoint(render).getZ()
        if z > self.potentialVisHeight:
            self.potentialVisHeight = z
            self.potentialVisZone = name

    def removeCollisionSections(self):
        for zoneName in self.sections:
            self.ignore('entercollision_zone%s' % zoneName)

        self.visTable = {}
        self.largeObjects = {}

    @report(types=['args'], dConfigParam='minimap')
    def addLargeObj(self, geometry, uniqueId):
        AreaBuilderBase.addLargeObj(self, geometry, uniqueId)
        if not self.visSets:
            return
        if uniqueId not in self.largeObjects:
            for zone in self.visTable:
                if uniqueId in self.visTable[zone][1]:
                    self.visSets[zone].addPath(geometry)

            self.largeObjects[uniqueId] = geometry
        geometry.stash()
        self.oldVis.stash()
        self.oldVis.unstash()

    def removeLargeObj(self, geometry, uniqueId):
        AreaBuilderBase.removeLargeObj(self, geometry, uniqueId)
        if uniqueId not in self.largeObjects:
            return
        for zone in self.visTable:
            if uniqueId in self.visTable[zone][1]:
                self.visSets[zone].removePath(geometry)

        del self.largeObjects[uniqueId]

    @report(types=['args'], dConfigParam='minimap')
    def addSectionObj(self, geometry, visZone, logError=0):
        if not visZone or not self.visHelper:
            return
        if geometry in self.sectionObjs:
            return
        if not self.visHelper.has_key(visZone):
            self.notify.warning('object %s tried to be placed in visZone %s, which does not exist in %s' % (str(geometry), str(visZone), str(self.master.uniqueId)))
            return
        AreaBuilderBase.addSectionObj(self, geometry, visZone)
        self.sectionObjs.add(geometry)
        for zone in self.visHelper[visZone]:
            self.visSets[zone].addPath(geometry)

        self.visSets[visZone].addPath(geometry)
        if not self.visZone or visZone in self.visHelper[self.visZone] or visZone == self.visZone:
            geometry.unstash()
        else:
            geometry.stash()

    def removeSectionObj(self, geometry, visZone):
        if not visZone:
            return
        if geometry not in self.sectionObjs:
            return
        self.sectionObjs.remove(geometry)
        AreaBuilderBase.removeSectionObj(self, geometry, visZone)
        for zone in self.visHelper[visZone]:
            self.visSets[zone].removePath(geometry)

        self.visSets[visZone].removePath(geometry)

    def arrived(self):
        base.disableFarCull()

    def left(self):
        base.positionFarCull()

    def isVisible(self, data):
        if not self.visZone or not data or not self.visTable:
            return True
        if data in self.visTable[self.visZone][0] or data == self.visZone:
            return True
        else:
            return False

    @report(types=['args'], dConfigParam='minimap')
    def addEffectObject(self, levelObj):
        visZone = levelObj.data.get('VisZone')
        visSize = levelObj.data.get('VisSize')
        if visZone:
            effectObj = NodePath(ModelNode(levelObj.data.get('EffectName')))
            effectObj.node().setPreserveTransform(effectObj.node().PTLocal)
            section = self.tempSections.get(visZone)
            if visSize == 'Large' or section == None:
                effectObj.reparentTo(self.largeObjectsRoot)
                effectObj.setTag('uid', levelObj.uniqueId)
                self.largeObjects[levelObj.uniqueId] = effectObj
            else:
                effectObj.reparentTo(self.tempSections[visZone].effectsRoot)
            effectObj.setTransform(self.areaGeometry, levelObj.transform)
        else:
            return AreaBuilderBase.addEffectObject(self, levelObj)
        return

    def registerEffect(self, effect):
        visZone = effect.getNetTag('visZone')
        uid = effect.getNetTag('uid')
        if uid:
            for zone in self.visTable:
                if uid in self.visTable[zone][1]:
                    self.effectsSets[zone].add(effect)

        if visZone:
            self.effectsSets[visZone].add(effect)
            for zone in self.visHelper[visZone]:
                self.effectsSets[zone].add(effect)

    def unregisterEffect(self, effect):
        effect.cleanUpEffect()
        self.currEffectSet -= set([effect])
        for zone in self.visTable:
            self.effectsSets[zone] -= set([effect])

    def enableEffects(self, effectSet):
        for effect in effectSet:
            effect.enableEffect()

    def disableEffects(self, effectSet):
        for effect in effectSet:
            effect.disableEffect()

    def initEffects(self):
        self.enableEffects(self.currEffectSet)

    def updateCurrEffectSet(self):
        newEffectSet = self.effectsSets.get(self.visZone)
        if not newEffectSet:
            newEffectSet = set()
        self.disableEffects(self.currEffectSet - newEffectSet)
        self.enableEffects(newEffectSet - self.currEffectSet)
        self.currEffectSet = newEffectSet

    def validateEffectSet(self, effectSet=set()):
        toEnable = self.currEffectSet & effectSet
        self.enableEffects(toEnable)

    def getTunnelMinimap(self, tunnelUid):
        return self.visZoneTunnels.get(tunnelUid, 0)

    def registerMinimapObject(self, levelObj):
        node = AreaBuilderBase.registerMinimapObject(self, levelObj)
        if node:
            objData = levelObj.data
            visZone = objData.get('VisZone', '')
            if visZone:
                node.setTag('MinimapArea', str(self.visZoneMinimaps.get(visZone, 0)))
                return node
            elif levelObj.get('VisSize') == 'Large':
                node.setTag('MinimapArea', '0')
                return node
        return None

    def triggerEffects(self, visZone):
        pass