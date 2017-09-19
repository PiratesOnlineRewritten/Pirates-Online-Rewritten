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
from direct.showbase.PythonUtil import report
from otp.otpbase import OTPRender
from otp.otpbase import OTPGlobals
from pirates.leveleditor import CustomAnims
from pirates.world import AreaBuilderBase
from pirates.world.AreaBuilderBase import ModelDef
from pirates.effects import ObjectEffects
from pirates.effects import SoundFX
AREA_CHILD_TYPE_PROP = 1

class GridLODDef():

    def __init__(self, area, zoneId):
        self.gridNode = NodePath('Grid-' + str(zoneId) + 'Node')
        OTPRender.renderReflection(False, self.gridNode, 'p_grid', None)
        lod = LODNode.makeDefaultLod('LodNode')
        self.lodNode = self.gridNode.attachNewNode(lod)
        gridDetail = base.gridDetail
        if gridDetail == 'high':
            lod.addSwitch(500, 0)
            lod.addSwitch(1000, 500)
            lod.addSwitch(1500, 1000)
            lod.addSwitch(3000, 1500)
            high = self.lodNode.attachNewNode('High')
            med = self.lodNode.attachNewNode('Med')
            low = self.lodNode.attachNewNode('Low')
            superLow = self.lodNode.attachNewNode('superLow')
            self.highLodNode = high
        elif gridDetail == 'med':
            lod.addSwitch(750, 0)
            lod.addSwitch(1500, 750)
            lod.addSwitch(3000, 1500)
            high = None
            med = self.lodNode.attachNewNode('Med')
            low = self.lodNode.attachNewNode('Low')
            superLow = self.lodNode.attachNewNode('superLow')
            self.highLodNode = med
        elif gridDetail == 'low':
            lod.addSwitch(1500, 0)
            lod.addSwitch(3000, 1500)
            high = None
            med = None
            low = self.lodNode.attachNewNode('Low')
            superLow = self.lodNode.attachNewNode('Low')
            self.highLodNode = low
        else:
            raise StandardError, 'Invalid grid-detail: %s' % gridDetail
        low.setLightOff(base.cr.timeOfDayManager.sunLight)
        low.setLightOff(base.cr.timeOfDayManager.shadowLight)
        self.children = [high, med, low]
        if zoneId == PiratesGlobals.FakeZoneId:
            pos = area.master.getPos()
        pos = area.master.getZoneCellOriginCenter(zoneId)
        self.gridNode.setPos(pos[0], pos[1], pos[2])
        self.gridNode.reparentTo(area.staticGridRoot)
        return

    def cleanup(self):
        self.gridNode.removeNode()
        self.lodNode = None
        self.highLodNode = None
        self.children = None
        return


class GridAreaBuilder(AreaBuilderBase.AreaBuilderBase):
    notify = directNotify.newCategory('ClientArea')

    def __init__(self, master):
        AreaBuilderBase.AreaBuilderBase.__init__(self, master)
        self.GridLOD = {}

    def addChildObj(self, levelObj):
        transform = levelObj.transform
        objData = levelObj.data
        uid = levelObj.uniqueId
        if objData['Type'] == 'Animated Avatar - Skeleton' or objData['Type'] == 'Animated Avatar - Navy' or objData['Type'] == 'Animated Avatar - Townfolk' or objData['Type'] == 'Animated Avatar':
            propNp = self.getPropAvatarNode(objData, transform, uid)
            propNp.reparentTo(self.areaGeometry)
            return propNp
        objStolen = False
        flaggedToSkip = False
        highNode = None
        lowNode = None
        objModel = None
        loadObject = True
        self.notify.debug('ClientArea: loading %s' % uid)
        objectType = self.checkSanityOnType(objData)
        objectCat = base.worldCreator.findObjectCategory(objData['Type'])
        loadableType = objectCat == 'PROP_OBJ' or objectCat == 'BUILDING_OBJ' or objectType == 'Cell Portal Area' or objectType in ('Dinghy',
                                                                                                                                    'Holiday Object',
                                                                                                                                    'PotionTable')
        if not loadableType and not objData.has_key('Objects'):
            return
        if objData.has_key('Visual') and objData['Visual'].has_key('Model'):
            if objData.has_key('SubObjs'):
                objModel = self.loadTree(objData)
            else:
                objModel = self.getModel(objData)
            if not objModel:
                return
            self.checkForFootprint(levelObj)
            signLocator = objModel.root.find('**/sign_locator')
            if not signLocator.isEmpty():
                self.buildSign(objData, signLocator)
            if objData.get('DisableCollision', False):
                collisionNodes = objModel.collisions.findAllMatches('**/+CollisionNode')
                for collisionNode in collisionNodes:
                    collisionNode.removeNode()

            if objData['Type'] == 'Collision Barrier':
                geomNodes = objModel.root.findAllMatches('**/+GeomNode')
                for geomNode in geomNodes:
                    geomNode.removeNode()

                newBitmasks = objData.get('Bitmasks')
                if newBitmasks and newBitmasks != ['None']:
                    collNodes = objModel.root.findAllMatches('**/+CollisionNode')
                    for collNode in collNodes:
                        collNode.setTag('objType', str(PiratesGlobals.COLL_LAND))
                        currCollMask = collNode.node().getIntoCollideMask()
                        for currNewBitmask in newBitmasks:
                            collNode.setCollideMask(currCollMask | PiratesGlobals.TargetBitmask | eval('PiratesGlobals.' + currNewBitmask))

            if objData['Type'] == 'Invasion Barrier':
                geomNodes = objModel.root.findAllMatches('**/+GeomNode')
                for geomNode in geomNodes:
                    geomNode.removeNode()

            if objData['Type'] == 'Special':
                if objData.has_key('Visual') and objData['Visual'].has_key('Model') and objData['Visual']['Model'] == 'models/misc/smiley':
                    geomNodes = objModel.root.findAllMatches('**/+GeomNode')
                    for geomNode in geomNodes:
                        geomNode.removeNode()

            objModel.root.reparentTo(self.master)
            objModel.root.setTransform(transform)
            objModel.root.flattenLight()
            if objectType not in self.LARGE_OBJECTS:
                self.processSmallObject(objModel)
                objPos = objData.get('Pos', Vec3(0, 0, 0))
                if hasattr(self.master, 'fakeZoneId'):
                    zoneId = self.master.fakeZoneId
                else:
                    zoneId = self.master.getZoneFromXYZ(transform.getPos())
                if objectType == 'Light_Fixtures' or objectType == 'Tunnel Cap':
                    effects = objModel.root.findAllMatches('**/*_effect_*')
                    effects.wrtReparentTo(self.staticGridRoot)
                if not self.GridLOD.has_key(zoneId):
                    self.GridLOD[zoneId] = GridLODDef(self, zoneId)
                gldef = self.GridLOD[zoneId]
                gridNode = gldef.gridNode
                lodNode = gldef.lodNode
                highLODNode = gldef.highLodNode
                lodChildren = gldef.lodNode.getChildren()
                numGridLODs = len(lodChildren)
                numLODs = objModel.lod.getNumChildren()
                if numGridLODs > numLODs:
                    lowestModel = None
                    for i in range(numLODs):
                        if not lowestModel:
                            lowestModel = objModel.lod.getChild(numLODs - 1 - i)
                        objModel.lod.getChild(numLODs - 1 - i).wrtReparentTo(lodChildren[numLODs - 1 - i])

                    if lowestModel:
                        for i in range(numGridLODs - numLODs):
                            lowestModel.copyTo(lodChildren[numGridLODs - 1 - i])

                else:
                    for i in xrange(numGridLODs):
                        objModel.lod.getChild(numLODs - 1 - i).wrtReparentTo(lodChildren[numGridLODs - 1 - i])

                objModel.collisions.wrtReparentTo(gridNode)
                objModel.root.detachNode()
            else:
                objModel.root.setTag('uid', uid)
                objModel.root.wrtReparentTo(self.largeObjectsRoot)
                objModel.root.setName('large_object')
        if objectType in self.LOOKUP_TABLE_OBJECTS:
            objModel.root.setTag('uid', uid)
        return objModel.root

    def loadObjects(self):
        if not self.areaLoaded:
            AreaBuilderBase.AreaBuilderBase.loadObjects(self)
            self.parentGridNodes()
            for np in self.staticGridRoot.findAllMatches('**/+LODNode;+s'):
                np.setClipPlane(base.farCull)

            for np in self.areaGeometry.findAllMatches('**/door_left*;+s'):
                np.setClipPlane(base.farCull)

            for np in self.areaGeometry.findAllMatches('**/door_right*;+s'):
                np.setClipPlane(base.farCull)

    def unloadObjects(self):
        if self.areaLoaded:
            for currGrid in self.GridLOD:
                self.GridLOD[currGrid].cleanup()

            self.GridLOD = {}
            AreaBuilderBase.AreaBuilderBase.unloadObjects(self)

    def loadWholeModel(self, modelBaseName, altId=None):
        geom = loader.loadModel(modelBaseName)
        if altId:
            blocker = geom.find('**/blocker_*')
            blocker.setName('blocker_' + altId)
        return geom

    def loadPiecesModels(self, modelBaseName, altId=None):
        terrainModel = loader.loadModel(modelBaseName + '_terrain', okMissing=True)
        if terrainModel:
            geom = terrainModel.getChild(0)
            geom.setName(terrainModel.getName())
            caveModel = loader.loadModel(modelBaseName + '_caves', okMissing=True)
            if caveModel:
                caveModel.getChild(0).reparentTo(geom)
            vegModel = loader.loadModel(modelBaseName + '_veg', okMissing=True)
            if vegModel:
                vegModel.getChild(0).reparentTo(geom)
            rockModel = loader.loadModel(modelBaseName + '_rocks', okMissing=True)
            if rockModel:
                rockModel.getChild(0).reparentTo(geom)
        else:
            geom = loader.loadModel(modelBaseName)
        if altId:
            blocker = geom.find('**/blocker_*')
            blocker.setName('blocker_' + altId)
        return geom

    def parentGridNodes(self):
        for currGrid in self.GridLOD:
            self.flattenGridNode(currGrid)
            gridLOD = self.GridLOD[currGrid]
            gridNode = gridLOD.gridNode

    def flattenGridNode(self, currGrid):
        gridNode = self.GridLOD[currGrid].gridNode
        children = self.GridLOD[currGrid].children
        sgr = SceneGraphReducer()
        sgr.removeColumn(children[2].node(), InternalName.getNormal())
        for higher in children[0:1]:
            if higher:
                sgr.applyAttribs(higher.node(), sgr.TTCullFace)

        gridNode.flattenStrong()

    def stashGridNodes(self):
        if hasattr(self.master, 'GridLOD'):
            for currGrid in self.GridLOD:
                self.GridLOD[currGrid].gridNode.stash()

    def unstashGridNodes(self):
        for currGrid in self.GridLOD:
            self.GridLOD[currGrid].gridNode.unstash()

    def handleSpecial(self, objNP, objType, uid):
        objName = objNP.getName()
        forceRadius = None
        lodRadiusFactor = self.LOD_RADIUS_FACTOR_MOST
        if objName == 'PropSimple Fort':
            return
        forceLowLodSD = None
        if objType in self.LARGE_OBJECTS_LOW and self.minLowLodSD:
            forceLowLodSD = self.minLowLodSD
        for lod in objNP.findAllMatches('**/+LODNode'):
            bounds = lod.getBounds()
            if not bounds.isEmpty():
                center = bounds.getApproxCenter()
                if forceRadius:
                    radius = forceRadius
                else:
                    try:
                        radius = bounds.getRadius()
                    except:
                        radius = (bounds.getMax() - bounds.getMin()).length() / 2

                    node = lod.node()
                    node.clearSwitches()
                    for i in range(lod.getNumChildren()):
                        distance = radius * lodRadiusFactor[i + 1]
                        if forceLowLodSD:
                            if i == lod.getNumChildren() - 1 and forceLowLodSD > distance:
                                distance = forceLowLodSD
                        if i == lod.getNumChildren() - 1:
                            node.addSwitch(distance, radius * lodRadiusFactor[i])
                        else:
                            node.addSwitch(distance, radius * lodRadiusFactor[i])

        return

    def delete(self):
        for node in self.GridLOD.values():
            node.cleanup()

        self.GridLOD = {}
        AreaBuilderBase.AreaBuilderBase.delete(self)

    def addLocationSphere(self, uid, pos, radius, name):
        name = PLocalizer.LocationNames.get(uid, '')
        self.namedAreas[uid] = [
         pos, radius, name]

    def getLocationInfo(self, uid):
        return self.namedAreas.get(uid)

    def setupUniqueActor(self, actor, animName):
        data = self.anims.get(animName)
        if not data:
            anim = loader.loadModel(animName)
            anim.reparentTo(self.animNode)
            name = '%s%s' % (actor.getName(), self.uniqueNum)
            self.uniqueNum += 1
            self.anims[animName] = (
             anim, name)
            anim.find('**/+AnimBundleNode').node().getBundle().setName(name)
            anim.find('**/+AnimBundleNode').node().setName(name)
        else:
            anim, name = data
        actor.renamePartBundles('modelRoot', name)

    def playAnims(self):
        if not self.bound:
            self.animControls = AnimControlCollection()
            autoBind(self.master.node(), self.animControls, 3)
            self.bound = True
            for i in xrange(self.animControls.getNumAnims()):
                self.animControls.getAnim(i).setPlayRate(random.uniform(0.8, 1))

        self.animControls.loopAll(1)

    def stopAnims(self):
        if self.bound:
            self.animControls.stopAll()

    def clearAnims(self):
        if self.bound:
            self.bound = False
            self.animControls.stopAll()
            self.animControls = None
        return