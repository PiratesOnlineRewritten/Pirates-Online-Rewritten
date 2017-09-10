import random
import re
import types
import copy
import marshal
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.showbase import DirectObject
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
from pirates.leveleditor import EditorGlobals
from pirates.ai import HolidayGlobals
from pirates.map.MinimapObject import MinimapShop
from pirates.effects import ObjectEffects
from pirates.world.LocationConstants import LocationIds
from pirates.effects import SoundFX
from pirates.effects import AmbientSoundFX
AREA_CHILD_TYPE_PROP = 1
staticLODs = [
 0, 40, 100, 200]

class ModelDef():
    root = None
    geomRoot = None
    high = None
    med = None
    low = None
    superLow = None
    collisions = None
    lod = None
    effects = None

    def copy(self):
        newModel = ModelDef()
        newModel.root = self.root.copyTo(NodePath())
        newModel.geomRoot = newModel.root.find('geomRoot')
        newModel.lod = newModel.geomRoot.find('+LODNode')
        newModel.high = newModel.lod.getChild(0)
        if self.med:
            newModel.med = newModel.lod.getChild(1)
            if self.low:
                newModel.low = newModel.lod.getChild(2)
                if self.superLow:
                    newModel.superLow = newModel.lod.getChild(3)
        newModel.collisions = newModel.root.find('collisions')
        newModel.effects = newModel.root.find('effects')
        return newModel


class AreaBuilderBase(DirectObject.DirectObject):
    LARGE_OBJECTS = [
     'Arch', 'Tavern', 'Building Exterior', 'Ship Wreck', 'Jungle_Props_large', 'Simple Fort', 'Pier', 'Tunnel Cap', 'Wall', 'Dinghy', 'Crane']
    LARGE_OBJECTS_HIGH = ['Arch', 'Tavern', 'Building Exterior', 'Ship Wreck', 'Jungle_Props_large', 'Simple Fort', 'Pier', 'Tunnel Cap', 'Wall']
    LARGE_OBJECTS_LOW = ['Arch', 'Tavern', 'Building Exterior', 'Ship Wreck', 'Jungle_Props_large', 'Simple Fort', 'Pier', 'Tunnel Cap', 'Wall']
    MED_OBJECTS_HIGH = [
     'Tree', 'Tree - Animated', 'Swamp_props', 'Military_props']
    MED_OBJECTS_LOW = ['Tree', 'Tree - Animated', 'Swamp_props', 'Military_props']
    LOOKUP_TABLE_OBJECTS = [
     'Building Exterior', 'Simple Fort', 'Ship Wreck']
    FOOTPRINT_OBJECTS = [
     'Arch', 'Building Exterior', 'Dinghy', 'Simple Fort', 'Wall', 'Shanty Gypsywagon', 'Shanty Tents', 'Burnt_Props', 'Cemetary', 'Stairs', 'Spanish Walls', 'Holiday Object', 'Invasion Barricade', 'Switch Prop']
    LOD_RADIUS_FACTOR_MOST = [
     0, 3.0, 6.0, 20.0, 100.0]
    LOD_RADIUS_FACTOR_TALL = [0, 6.0, 12.0, 20.0, 100.0]
    AREA_NOT_LOADED = 999
    notify = directNotify.newCategory('ClientArea')

    def __init__(self, master):
        DirectObject.DirectObject.__init__(self)
        self.doneParenting = False
        self.master = master
        self.propAvs = []
        self.treeCache = {}
        self.modelCache = {}
        self.doors = {}
        self.areaGeometry = self.master.attachNewNode('areaGeometry')
        self.dummyLight = AmbientLight('a')
        self.dummyLight.setColor(Vec4(0, 0, 0, 1))
        self.largeObjects = {}
        self.largeObjectsRoot = self.areaGeometry.attachNewNode('largeObjects')
        self.staticGridRoot = self.areaGeometry.attachNewNode('staticGrid')
        self.collisions = self.areaGeometry.attachNewNode('collisions')
        self.animNode = self.areaGeometry.attachNewNode('animations')
        self.uniqueNum = 0
        self.areaGeometry.hide(OTPRender.MainCameraBitmask)
        self.areaGeometry.showThrough(OTPRender.EnviroCameraBitmask)
        self.anims = {}
        self.bound = False
        self.footprintObjects = NodePath('footprint')
        self.interactives = []
        self.haveLODs = False
        self.areaLoaded = False
        self.globalLights = set()
        self.namedAreas = {}
        self.minLowLodSD = None
        self.sfxNodes = []
        self.minimapPrefix = None
        self.cleanUpList = []
        self.visZoneLock = False
        return

    def addToCleanUp(self, obj):
        self.cleanUpList.append(obj)

    def setVisZoneLock(self, lock=True):
        self.visZoneLock = lock

    def makeNPCNavy(self, dna):
        dna.makeNPCNavySailor()
        dna.gender = 'n'
        dna.body.color = 0
        dna.body.shape = 3
        dna.body.height = random.choice([0.8, 0.9, 1, 1.1, 1.2])
        dna.clothes.shirt = 0
        dna.clothes.vest = 0
        dna.clothes.coat = 3
        dna.clothes.pant = 4
        dna.clothes.sock = 0
        dna.clothes.shoe = 3
        dna.clothes.belt = 0
        dna.head.hair.hair = 1
        dna.head.hair.beard = 0
        dna.head.hair.mustache = 0
        dna.head.hair.color = 0

    def getPropAvatarNode(self, object, transform, uid):
        object = copy.copy(object)
        nodePath = NodePath(ModelNode('propAv'))
        nodePath.node().setPreserveTransform(ModelNode.PTLocal)
        nodePath.setTag('objectType', 'propAv')
        del object['Pos']
        del object['Hpr']
        del object['Scale']
        nodePath.setTransform(transform)
        nodePath.setTag('data', marshal.dumps(object))
        nodePath.setTag('uid', uid)
        return nodePath

    def setupPropAv(self, root):
        object = marshal.loads(root.getTag('data'))
        objType = object['Type']
        uid = root.getTag('uid')

        def playPropAvAnim(task, propAv, object, createDefault=True):
            anim = object['Animation Track']
            createDefSword = createDefault
            if anim == 'Track 1':
                ivals = []
                randWait = random.random() * 4.0
                ival = Sequence(ActorInterval(propAv, 'sword_slash'), ActorInterval(propAv, 'sword_thrust', duration=1), ActorInterval(propAv, 'sword_idle'), ActorInterval(propAv, 'sword_slash'), ActorInterval(propAv, 'sword_idle', duration=randWait))
                ival.loop()
                ivals.append(ival)
                propAv.swordIvals = ivals
            else:
                if anim == 'Track 2':
                    ivals = []
                    ival = Sequence(ActorInterval(propAv, 'sword_slash'), ActorInterval(propAv, 'sword_thrust', duration=1), ActorInterval(propAv, 'sword_idle'), ActorInterval(propAv, 'boxing_kick'), ActorInterval(propAv, 'sword_idle'))
                    ival.loop()
                    ivals.append(ival)
                    propAv.swordIvals = ivals
                else:
                    allAnims = CustomAnims.INTERACT_ANIMS.get(anim)
                    if allAnims:
                        allIdles = allAnims.get('idles')
                        allProps = allAnims.get('props')
                        currChoice = random.choice(allIdles)
                        anim = currChoice
                        createDefSword = False
                        if allProps:
                            propInfo = random.choice(allProps)
                            if type(propInfo) == types.ListType:
                                propInfo = propInfo[0]
                            prop = loader.loadModel(propInfo)
                            prop.reparentTo(propAv.rightHandNode)
                    propAv.loop(anim)
                if createDefSword:
                    s = Sword.Sword(10103)
                    s.attachTo(propAv)
            return Task.done

        propAv = None
        createDefaultProp = True
        if objType == 'Animated Avatar - Skeleton':
            propAv = Skeleton.Skeleton()
            propAv.setAvatarType()
            propAv.setName('Extra')
        else:
            if objType == 'Animated Avatar - Navy':
                propAv = NavySailor.NavySailor()
                dna = HumanDNA()
                self.makeNPCNavy(dna)
                propAv.setDNAString(dna)
                propAv.generateHuman(propAv.style.gender, base.cr.human)
                propAv.setName('Extra')
            elif objType == 'Animated Avatar - Townfolk':
                propAv = Townfolk.Townfolk()
                dna = HumanDNA()
                dna.makeNPCPirate()
                dna.gender = object['Visual']['Gender']
                dna.body.shape = object['Visual']['Shape']
                dna.head.hair.hair = object['Visual']['Hair']
                dna.head.hair.beard = object['Visual']['Beard']
                dna.head.hair.mustache = object['Visual']['Mustache']
                dna.head.hair.color = object['Visual']['HairColor']
                dna.body.color = object['Visual']['Skin']
                dna.clothes.coat = object['Visual']['Coat']
                dna.clothes.coatColor = object['Visual']['CoatColor']
                dna.clothes.shirt = object['Visual']['Shirt']
                dna.clothes.shirtColor = object['Visual']['ShirtColor']
                dna.clothes.pant = object['Visual']['Pants']
                dna.clothes.pantColor = object['Visual']['PantsColor']
                dna.clothes.sock = object['Visual']['Sock']
                dna.clothes.shoe = object['Visual']['Shoe']
                dna.clothes.belt = object['Visual']['Belt']
                dna.clothes.beltColor = object['Visual']['BeltColor']
                dna.head.hat = object['Visual']['Hat']
                propAv.setDNAString(dna)
                propAv.generateHuman(propAv.style.gender, base.cr.human)
                propAv.setName('Extra')
            else:
                propAv = Townfolk.Townfolk()
                subCat = object.get('SubCategory')
                if subCat:
                    propAv.loadCast(subCat)
                    propAv.loop('idle')
                    __builtins__['propAv'] = propAv
                createDefaultProp = False
                if object.has_key('Effect Type') and object['Effect Type'] != None and ObjectEffects.OBJECT_EFFECTS.has_key(object['Effect Type']):
                    ObjectEffects.OBJECT_EFFECTS[object['Effect Type']](propAv)
            if propAv:
                propAv.swordIvals = []
                propAv.moveIvals = []
                propAv.reparentTo(root)
                playPropAvAnim(None, propAv, object, createDefaultProp)
                if object.has_key('Visual') and object['Visual'].has_key('Color'):
                    propAv.setColorScale(*object['Visual']['Color'])
                if object['Animation Track'] == 'walk' or object['Animation Track'] == 'run':
                    self.createPropAvatarMovement(uid, propAv, object['Animation Track'])
        self.propAvs.append(propAv)
        return propAv

    def createPropAvatarMovement(self, uid, propAv, anim):
        for currData in base.worldCreator.fileDicts:
            if currData['Objects'].has_key(self.uniqueId):
                for currLink in currData['Node Links']:
                    amNode1 = currLink[0] == uid
                    amNode2 = currLink[1] == uid
                    if amNode1 or amNode2:
                        if amNode1:
                            path = currData['ObjectIds'][currLink[1]]
                        else:
                            path = currData['ObjectIds'][currLink[0]]
                        getDstPos = 'dstPos = currData' + path + '["Pos"]'
                        exec getDstPos
                        h0 = propAv.getH()
                        h1 = propAv.getH() + 180
                        p = propAv.getP()
                        r = propAv.getR()
                        srcPos = propAv.getPos()
                        tgtLoc = propAv.getParent().attachNewNode('dummy')
                        tgtLoc.setPos(dstPos)
                        moveDist = propAv.getDistance(tgtLoc)
                        if anim == 'run':
                            moveTime = moveDist / 16
                        else:
                            moveTime = moveDist / 4
                        moveIval = Sequence(LerpPosInterval(propAv, moveTime, dstPos), LerpHprInterval(propAv, 0, Vec3(h1, p, r)), LerpPosInterval(propAv, moveTime, srcPos), LerpHprInterval(propAv, 0, Vec3(h0, p, r)))
                        tgtLoc.removeNode()
                        moveIval.loop()
                        propAv.moveIval = moveIval
                        return

    def checkSanityOnType(self, objData):
        objectType = objData['Type']
        if objectType != 'Building Exterior':
            return objectType
        return objectType
        file = None
        try:
            file = objData['File']
            bTrueBuilding = file != ''
        except:
            return objectType

        if not bTrueBuilding:
            return 'PropBuildingExterior'
        else:
            return objectType
        return

    def checkForFootprint(self, levelObj):
        objData = levelObj.data
        if objData['Type'] not in self.FOOTPRINT_OBJECTS:
            return
        visual = objData.get('Visual')
        if not visual:
            return
        model = visual.get('Model') or visual.get(0, {}).get('Model')
        if not model:
            return
        name = model + '_footprint'
        footprint = loader.loadModel(name, okMissing=True)
        if not footprint:
            return
        footprint.reparentTo(self.footprintObjects)
        footprint.setTransform(levelObj.transform)
        for field in ('Holiday', ):
            value = objData.get(field)
            if value:
                footprint.setTag(field, objData[field])

        return footprint

    def buildFootprintNode(self):
        footprintRoot = NodePath('footprint')
        footprintNodes = {}
        for child in self.footprintObjects.getChildren():
            geoms = child.findAllMatches('**/+GeomNode')
            for geom in geoms:
                geom.setTransform(child.getTransform(footprintRoot))
                geom.node().copyTags(child.node())
                tag = geom.getNetTag('Footprint')
                sort = 0
                if tag == 'FortColumn':
                    sort = -1
                else:
                    if tag == 'FortWall':
                        sort = -2
                    elif tag == 'Column':
                        sort = -3
                    elif tag == 'Wall':
                        sort = -4
                    minimapId = child.getTag('VisZone Minimap') or '0'
                    footprintNode = footprintNodes.get(minimapId)
                    if not footprintNode:
                        footprintNode = footprintRoot.attachNewNode('footprint_' + minimapId)
                        footprintNodes[minimapId] = footprintNode
                geom.reparentTo(footprintNode, sort=sort)

        self.footprintObjects.get_children().detach()
        for node in footprintNodes.values():
            node.flattenStrong()

        return footprintRoot

    def flattenObjNode(self, objNode):
        lodnode = objNode.find('**/+LODNode')
        if not lodnode.isEmpty():
            sgr = SceneGraphReducer()
            if base.gridDetail == 'low':
                lodnode.setLightOff(base.cr.timeOfDayManager.dlight)
                sgr.removeColumn(lodnode.node(), InternalName.getNormal())
            else:
                lowNP = lodnode.find('low;+i')
                if not lowNP.isEmpty():
                    lowNP.setLightOff(base.cr.timeOfDayManager.dlight)
                    sgr.removeColumn(lowNP.node(), InternalName.getNormal())
                for higherName in ['med*', 'hi*']:
                    higher = lodnode.find(higherName + ';+i')
                    if not higher.isEmpty():
                        sgr.applyAttribs(higher.node(), sgr.TTCullFace)

        objNode.flattenStrong()

    def setupLODs(self):
        self.haveLODs = True
        detailNode = LODNode.makeDefaultLod('largeObjects')
        sdHigh = 1000
        sdLow = 2000
        if hasattr(self.master, 'sphereRadii'):
            sdHigh = self.master.sphereRadii[0]
            sdLow = self.master.sphereRadii[2]
        detailNode.addSwitch(sdHigh, 0)
        detailNode.addSwitch(sdLow, sdHigh)
        self.minLowLodSD = sdHigh
        self.largeObjectsHigh = self.allDetails.attachNewNode('BigStuff')
        self.largeObjectsLow = NodePath('low details throwaway')
        self.largeObjects = []
        self.medObjectsHigh = self.allDetails.attachNewNode('MedStuff')
        self.medObjectsLow = NodePath('lowDetail')
        self.mediumObjects = []
        self.smallObjectsHigh = self.allDetails.attachNewNode('smallStuff')
        self.smallObjects = []

    def loadAnimatedTree(self, obj, modelName, animName, partName):
        syls = modelName.split('trunk_')
        newModelName = syls[0]
        syls = animName.split('_')
        numDelms = len(syls)
        aName = syls[numDelms - 1]
        newAnimName = newModelName + aName
        newModelName += 'hi'
        newPartName = 'modelRoot'
        bLODLoaded = not obj.hasLOD()
        if bLODLoaded:
            obj.setLODNode()
        if loader.loadModel(newModelName) != None:
            if bLODLoaded:
                obj.addLOD(1, 200, 0)
            obj.loadModel(newModelName, newPartName, '1')
        newModelName = re.sub('_hi', '_med', newModelName)
        if loader.loadModel(newModelName) != None:
            if bLODLoaded:
                obj.addLOD(2, 400, 200)
            obj.loadModel(newModelName, newPartName, '2')
        newModelName = re.sub('_med', '_low', newModelName)
        if loader.loadModel(newModelName) != None:
            if bLODLoaded:
                obj.addLOD(3, 1000, 400)
            if base.options.getTerrainDetailSetting() == PiratesGlobals.TD_LOW:
                model = loader.loadModel(newModelName)
                model.findAllMatches('**/+GeomNode').reparentTo(obj.getLOD('3'))
            else:
                obj.loadModel(newModelName, newPartName, '3')
        self.setupUniqueActor(obj, newAnimName)
        newModelName = re.sub('_low', '_zero_coll', newModelName)
        coll = loader.loadModel(newModelName)
        if coll:
            coll.reparentTo(obj)
        return

    def makeAnimatedTree(self, obj, trunk, leaf):
        tname = ''
        tparts = trunk.split('_')
        numDelms = len(tparts)
        i = 0
        for syl in tparts:
            if syl == 'trunk':
                tname = syl + '_' + tparts[i + 1]
                break
            i += 1

        lname = ''
        lparts = leaf.split('_')
        numDelms = len(lparts)
        i = 0
        for syl in lparts:
            if syl == 'leaf':
                lname = syl + '_' + lparts[i + 1]
                break
            i += 1

        trunkNodes = obj.findAllMatches('**/*' + tname + '*')
        leafNodes = obj.findAllMatches('**/*' + lname + '*')
        obj.findAllMatches('**/+GeomNode').stash()
        trunkNodes.unstash()
        leafNodes.unstash()

    def loadSubModelLODs(self, obj, modelName, animName, partName):
        if not obj.hasLOD():
            obj.setLODNode()
            obj.addLOD(1, 120, 0)
            obj.addLOD(2, 300, 120)
            obj.addLOD(3, 750, 300)
        obj.loadModel(modelName, partName, '1')
        modelName = re.sub('_hi', '_med', modelName)
        obj.loadModel(modelName, partName, '2')
        modelName = re.sub('_med', '_low', modelName)
        obj.loadModel(modelName, partName, '3')
        self.setupUniqueActor(obj, animName)

    def loadSubModels(self, propData):
        bAnimatedTree = propData['Type'] == 'Tree - Animated'
        obj = Actor.Actor()
        name = propData['Visual']['PartName']
        modelName = propData['Visual']['Model']
        animName = propData['Visual']['Animate']
        if bAnimatedTree:
            trunkName = modelName
            self.loadAnimatedTree(obj, modelName, animName, name)
        else:
            self.loadSubModelLODs(obj, modelName, animName, name)
        subObjs = obj.findAllMatches('**/*' + name + '*')
        if propData['Visual'].has_key('Scale'):
            for i in range(len(subObjs)):
                currSubObj = subObjs[i]
                currSubObj.setScale(propData['Visual']['Scale'])

        if propData['Visual'].has_key('Color'):
            for i in range(len(subObjs)):
                currSubObj = subObjs[i]
                currSubObj.setColorScale(*propData['Visual']['Color'])

        animRateRange = [
         1.0, 1.0]
        if propData.has_key('SubObjs'):
            if type(propData['SubObjs']) == types.DictType:
                subObjsInfo = propData['SubObjs'].values()
            else:
                subObjsInfo = propData['SubObjs']
            for currSubObj in subObjsInfo:
                attachInfo = currSubObj['Visual']['Attach']
                name = currSubObj['Visual']['PartName']
                modelName = currSubObj['Visual']['Model']
                animName = currSubObj['Visual']['Animate']
                if bAnimatedTree:
                    leafName = modelName
                else:
                    self.loadSubModelLODs(obj, modelName, animName, name)
                subObjs = obj.findAllMatches('**/*' + name + '*')
                if currSubObj['Visual'].has_key('Scale'):
                    if bAnimatedTree:
                        transform = TransformState.makeMat(Mat4(obj.getJointTransform('modelRoot', attachInfo[1], '1')))
                        obj.freezeJoint('modelRoot', attachInfo[1], pos=Vec3(transform.getPos()), hpr=Vec3(transform.getHpr()), scale=currSubObj['Visual']['Scale'])
                    else:
                        for i in range(len(subObjs)):
                            currLOD = subObjs[i]
                            currLOD.setScale(currSubObj['Visual']['Scale'])

                if currSubObj['Visual'].has_key('Color'):
                    for i in range(len(subObjs)):
                        currLOD = subObjs[i]
                        currLOD.setColorScale(*currSubObj['Visual']['Color'])

                if propData['Type'] != 'Tree - Animated':
                    for lodName in obj.getLODNames():
                        obj.attach(name, attachInfo[0], attachInfo[1], lodName)

                animRateRange = WorldGlobals.ObjectAnimRates.get(animName)
                if animRateRange == None:
                    animRateRange = WorldGlobals.ObjectAnimRates.get('Default')

            if bAnimatedTree:
                self.makeAnimatedTree(obj, trunkName, leafName)
        return obj

    def pauseSFX(self):
        for sfxNode in self.sfxNodes:
            sfxNode.stopPlaying()

    def resumeSFX(self):
        for sfxNode in self.sfxNodes:
            sfxNode.startPlaying()

    def loadSFXNode(self, objData, parent, uid):
        sfxNode = SoundFX.SoundFX(sfxFile=objData['SoundFX'], volume=float(objData['Volume']), looping=True, delayMin=float(objData['DelayMin']), delayMax=float(objData['DelayMax']), pos=objData['Pos'], hpr=objData['Hpr'], parent=parent, listenerNode=base.localAvatar, drawIcon=False)
        sfxNode.startPlaying('playSfx_%s' % uid)
        self.sfxNodes.append(sfxNode)
        return sfxNode

    def loadAnimatedProp(self, propData, parent):

        def playAnim(propAv, anim):
            __builtins__['bird'] = propAv
            propAv.loadAnims({'idle': anim})
            propAv.loop('idle')

        propAv = Actor.Actor()
        visInfo = propData.get('Visual')
        if visInfo:
            modelName = visInfo.get('Model')
            anim = visInfo.get('Animate')
        if modelName == None:
            return
        propAv.loadModel(modelName)
        if anim:
            playAnim(propAv, anim)
        propAv.reparentTo(self.areaGeometry)
        propAv.setPos(propData['Pos'])
        propAv.setHpr(propData['Hpr'])
        if propData.has_key('Scale'):
            propAv.setScale(propData['Scale'])
        if propData.has_key('Visual') and propData['Visual'].has_key('Color'):
            propAv.setColorScale(*propData['Visual']['Color'])
        self.smallObjects.append(propAv)
        propAv.wrtReparentTo(self.areaGeometry)
        return propAv

    def reparentLODCollisions(self, sourceNode, targetNode, collName):
        sourceNode.findAllMatches('**/+' + collName).wrtReparentTo(targetNode)
        targetNode.flattenLight()

    def loadLights(self):
        self.polyLights = self.areaGeometry.findAllMatches('**/+PolylightNode')
        self.fires = []
        self.discs = []
        self.lights = []
        lightCol = [VBase4(0, 0, 0, 1), VBase4(1, 0, 0, 1), VBase4(0, 1, 0, 1), VBase4(0, 0, 1, 1)]
        for i in range(len(self.polyLights)):
            light = self.polyLights[i]
            plNode = light.node()
            plNode.flickerOff()
            plNode.setAttenuation(PolylightNode.AQUADRATIC)
            plNode.setRadius(20)
            effect = base.localAvatar.node().getEffect(PolylightEffect.getClassType()).addLight(light)
            base.localAvatar.node().setEffect(effect)
            self.lights.append(light)
            fire = loader.loadModel('models/misc/fire')
            fire.setBillboardPointEye()
            fire.setPos(plNode.getPos())
            fire.setScale(0.1)
            fire.setColorScaleOff()
            fire.reparentTo(light)
            self.fires.append(fire)
            LanternGlowEffect = LanternGlow(light, 2)
            pos = plNode.getPos()
            LanternGlowEffect.setPos(pos)
            LanternGlowEffect.loop()
            self.discs.append(LanternGlowEffect)

    def unloadLights(self):
        for light in self.lights:
            effect = base.localAvatar.node().getEffect(PolylightEffect.getClassType())
            if effect.hasLight(light):
                base.localAvatar.node().setEffect(effect.removeLight(light))

        for disc in self.discs:
            disc.removeNode()

        del self.discs

    def attachCannon(self, cannon):
        self.interactives.append(cannon)

    def setupCannonballBldgColl(self, collNode, mask):
        if collNode == None or collNode.isEmpty():
            return
        collNode.setCollideMask(mask)
        collNode.setTag('objType', str(PiratesGlobals.COLL_BLDG))
        return

    @report(types=['args'], dConfigParam='minimap')
    def loadObjects(self):
        if not self.areaLoaded:
            self._preLoadStep()
            self._loadObjects()
            self._postLoadStep()
            self.areaLoaded = True

    @report(types=['args'], dConfigParam='minimap')
    def _preLoadStep(self):
        pass

    @report(types=['args'], dConfigParam='minimap')
    def _loadObjects(self):
        self.uniqueId = self.master.uniqueId
        areaGeometry = base.bamCache.lookup(Filename('/%s_area_%s_%s.bam' % (self.uniqueId, base.launcher.getServerVersion(), base.gridDetail)), 'bam')
        if base.config.GetBool('want-disk-cache', 0) and areaGeometry.hasData():
            base.cr.loadingScreen.beginStep('CachedObjects', 3, 70)
            if not areaGeometry.hasData():
                self.notify.error('nonexistant geometry file for %s' % self.uniqueId)
            self.staticGridRoot.detachNode()
            self.largeObjectsRoot.detachNode()
            self.collisions.detachNode()
            self.animNode.detachNode()
            data = areaGeometry.getData()
            base.cr.loadingScreen.tick()
            newData = data.copySubgraph()
            base.cr.loadingScreen.tick()
            self.areaGeometry.node().stealChildren(newData)
            self.areaGeometry.node().copyTags(newData)
            base.cr.loadingScreen.tick()
            self.collisions = self.areaGeometry.find('collisions')
            self.largeObjectsRoot = self.areaGeometry.find('largeObjects')
            self.staticGridRoot = self.areaGeometry.find('staticGrid')
            self.animNode = self.areaGeometry.find('animations')
            base.cr.loadingScreen.endStep('CachedObjects')
        else:
            base.loadingScreen.beginStep('PreLoad', 1, 5)
            self._preSubObjectsStep()
            base.cr.loadingScreen.tick()
            base.loadingScreen.endStep('PreLoad')
            base.worldCreator.loadFileObjFromUid(self.uniqueId, self.master, self.master)
            base.loadingScreen.beginStep('PostLoad', 3, 7)
            base.cr.loadingScreen.tick()
            self._postSubObjectsStep()
            base.cr.loadingScreen.tick()
            areaGeometry.setData(self.areaGeometry.node(), 0)
            base.bamCache.store(areaGeometry)
            base.cr.loadingScreen.tick()
            base.cr.loadingScreen.endStep('PostLoad')

    @report(types=['args'], dConfigParam='minimap')
    def _preSubObjectsStep(self):
        pass

    @report(types=['args'], dConfigParam='minimap')
    def _postSubObjectsStep(self):
        minimapPrefix = base.worldCreator.uidMinimapPrefix.get(self.master.uniqueId, '')
        if minimapPrefix:
            self.areaGeometry.setTag('Minimap Prefix', minimapPrefix)
        footstepSound = base.worldCreator.footstepTable.get(self.master.uniqueId, '')
        if footstepSound:
            self.areaGeometry.setTag('Footstep Sound', footstepSound)
        environment = base.worldCreator.environmentTable.get(self.master.uniqueId, '')
        if environment:
            self.areaGeometry.setTag('Environment', environment)
        self.staticGridRoot.flattenLight()
        self.largeObjectsRoot.flattenLight()
        self.collisions.flattenLight()

    @report(types=['args'], dConfigParam='minimap')
    def _postLoadStep(self):
        base.loadingScreen.tick()
        self.setupLights()
        base.loadingScreen.tick()
        base.worldCreator.processPostLoadCalls()
        base.loadingScreen.tick()
        self.playAnims()
        for object in self.areaGeometry.findAllMatches('**/=Object_Cutscene'):
            base.cr.activeWorld.addCutsceneOriginNode(object, object.getName())

        for object in self.areaGeometry.findAllMatches('**/Entity_Node'):
            entity = base.cr.activeWorld.addEntityObject(object)
            self.addToCleanUp(entity)

        self.setupFloors(self.master.geom)
        self.setupFloors(self.areaGeometry)
        base.loadingScreen.tick()
        for obj in self.areaGeometry.findAllMatches('**/=objectType=propAv'):
            self.setupPropAv(obj)

        for obj in self.largeObjectsRoot.findAllMatches('large_object;+s'):
            base.loadingScreen.tick()
            uid = obj.getTag('uid')
            self.largeObjects[uid] = obj
            geomRoots = obj.findAllMatches('geomRoot')
            doorList = {'left': [],'right': [],'locator': []}
            if not geomRoots:
                geomRoots = obj.findAllMatches('*/*/geomRoot')
            for geomRoot in geomRoots:
                for doorStr in doorList:
                    nodeList = []
                    nodes = geomRoot.findAllMatches('door_%s*;+s' % doorStr)
                    for i in range(nodes.getNumPaths()):
                        if i < 1:
                            door = geomRoot.find('door_%s;+s' % doorStr)
                        else:
                            door = geomRoot.find('door_%s_%d;+s' % (doorStr, i + 1))
                        if not door.isEmpty():
                            doorList[doorStr].append(door)

                lod = geomRoot.find('+LODNode')
                if lod:
                    for door in doorList['left'] + doorList['right']:
                        door.wrtReparentTo(lod.getChild(0))
                        for i in range(1, lod.getNumChildren() - 1):
                            door.instanceTo(lod.getChild(i))

            self.doors[uid] = doorList

        holidayObjects = self.areaGeometry.findAllMatches('**/=Holiday;+s')
        if holidayObjects:
            self.accept('HolidayStarted', self.handleHolidayStarted)
            self.accept('HolidayEnded', self.handleHolidayEnded)
        holidayObjects.stash()
        minimapPrefix = self.areaGeometry.getTag('Minimap Prefix')
        if minimapPrefix:
            self.master.setMinimapPrefix(minimapPrefix)
        self.master.hideMapNodes()
        footstepSound = self.areaGeometry.getTag('Footstep Sound')
        if footstepSound:
            self.master.setFootstepSound(footstepSound)
        environment = self.areaGeometry.getTag('Environment')
        if environment:
            self.master.setEnvironment(environment)
        base.cr.npcManager.clearNpcData()
        npcDataNode = self.areaGeometry.find('npcData')
        if npcDataNode:
            offsetInfoStr = npcDataNode.getTag('npcData')
            if offsetInfoStr:
                offsetInfo = eval(offsetInfoStr)
                base.cr.npcManager.addNpcData(offsetInfo)

    def setupLights(self):
        for light in self.areaGeometry.findAllMatches('**/=Global Light'):
            self.addLight(light)
            OTPRender.renderReflection(False, light, 'p_light', None)

        self.turnOnLights()
        return

    def unloadObjects(self):
        if not self.areaLoaded:
            return
        self.areaLoaded = False
        self.clearAnims()
        for av in self.propAvs:
            for ival in av.swordIvals:
                ival.pause()

            for ival in av.moveIvals:
                ival.pause()

            av.swordIvals = []
            av.moveIvals = []
            av.delete()

        self.propAvs = []
        for light in self.globalLights:
            render.clearLight(light)

        self.largeObjects = {}
        self.modelCache = {}
        self.treeCache = {}
        for sfxNode in self.sfxNodes:
            sfxNode.stopPlaying()
            sfxNode.removeNode()

        self.sfxNodes = []
        if base.config.GetBool('want-model-texture-cleanup', 1):
            ModelPool.garbageCollect()
            TexturePool.garbageCollect()

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
        pass

    def flattenGridNode(self, currGrid):
        pass

    def stashGridNodes(self):
        pass

    def unstashGridNodes(self):
        pass

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
                    node.setCenter(center)
                    for i in range(lod.getNumChildren()):
                        distance = radius * lodRadiusFactor[i + 1]
                        if forceLowLodSD:
                            if i == lod.getNumChildren() - 1 and forceLowLodSD > distance:
                                distance = forceLowLodSD
                        node.addSwitch(distance, radius * lodRadiusFactor[i])

        return

    def addLight(self, light):
        self.globalLights.add(light)

    def delete(self):
        self.cleanupData()
        del self.globalLights
        self.ignore('HolidayStarted')
        self.ignore('HolidayEnded')
        del self.footprintObjects
        self.master.ignore('localAvatarQuestComplete')
        self.master = None
        return

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

    def addObject(self, object, gameArea, transformParent):
        pass

    def addLargeObj(self, geometry, uniqueId):
        pass

    def removeLargeObj(self, geometry, uniqueId):
        pass

    def addSectionObj(self, geometry, visZone, logError=0):
        pass

    def removeSectionObj(self, geometry, visZone):
        pass

    def loadTerrain(self):
        pass

    def getModel(self, objData):
        base.loadingScreen.tick()
        if objData.get('Type') == 'Tree - Animated':
            obj = self.loadTree(objData)
            color = objData['Visual'].get('Color')
            if color:
                rs = RenderState.makeEmpty().addAttrib(ColorScaleAttrib.make(color))
                for np in obj.root.findAllMatches('**/+GeomNode'):
                    node = np.node()
                    for i in range(node.getNumGeoms()):
                        node.setGeomState(i, node.getGeomState(i).compose(rs))

            return obj
        else:
            if objData['Type'] == 'Switch Prop':
                model, subDefs = self.buildSwitchModel(objData)
                if not objData.get('UseMayaLOD', False):
                    for subDef in subDefs:
                        self.setupSwitchDistances(subDef.lod.node(), subDef.root)

            else:
                modelName = objData['Visual']['Model']
                model = self.modelCache.get(modelName)
                if not model:
                    model = self.buildModel(modelName)
                model = model.copy()
                if not objData.get('UseMayaLOD', False):
                    self.setupSwitchDistances(model.lod.node(), model.root)
            holiday = objData.get('Holiday')
            if holiday:
                self._applyTagToModel(objData, model, 'Holiday', holiday)
                if objData['Type'] == 'Invasion Barricade' or objData['Type'] == 'Invasion Barrier':
                    self._applyTagToModel(objData, model, 'Zone', objData.get('Zone'))
            color = objData['Visual'].get('Color')
            if color:
                rs = RenderState.makeEmpty().addAttrib(ColorScaleAttrib.make(color))
                for np in model.root.findAllMatches('**/+GeomNode'):
                    node = np.node()
                    for i in range(node.getNumGeoms()):
                        node.setGeomState(i, node.getGeomState(i).compose(rs))

            return model

    def processSmallObject(self, model):
        model.lod.detachNode()
        extraData = model.geomRoot.findAllMatches('*')
        node = model.geomRoot.attachNewNode('extraData')
        extraData.wrtReparentTo(node)
        for child in model.lod.getChildren():
            node.copyTo(child)

        node.detachNode()
        model.lod.reparentTo(model.geomRoot)

    def _applyTagToModel(self, objData, model, tag, value):
        if 'VisSize' in objData:
            if objData['VisSize'] == 'Large':
                model.root.setTag(tag, value)
            else:
                model.collisions.setTag(tag, value)
                model.high.setTag(tag, value)
                if model.med:
                    model.med.setTag(tag, value)
                if model.low:
                    model.low.setTag(tag, value)
                if model.superLow:
                    model.superLow.setTag(tag, value)
        else:
            if objData['Type'] in self.LARGE_OBJECTS:
                model.root.setTag(tag, value)
            else:
                model.collisions.setTag(tag, value)
                model.high.setTag(tag, value)
                model.med.setTag(tag, value)
                model.low.setTag(tag, value)
                model.superLow.setTag(tag, value)
            for effect in model.root.findAllMatches('**/*_effect_*'):
                effect.setTag(tag, value)

    def buildModel(self, name):
        data = loader.loadModel(name)
        if not data:
            return NodePath('Error!')
        modelDef = self.makeModelDef(data)
        self.modelCache[name] = modelDef
        return modelDef

    def buildSwitchModel(self, objData):
        modelDef = ModelDef()
        modelDef.root = NodePath(ModelNode('large_object'))
        modelDef.collisions = NodePath('collisions')
        modelDef.root.node().setPreserveTransform(True)
        switchRoot = modelDef.root.attachNewNode(SwitchNode('Switch Prop'))
        switchRoot.setTag('Switch Class', objData['Switch Class'])
        subDefs = [ (key, self.makeModelDef(loader.loadModel(visualData['Model']))) for key, visualData in objData['Visual'].iteritems() ]
        subDefs.sort()
        for key, subDef in subDefs:
            x = switchRoot.getNumChildren()
            while x < key:
                switchRoot.attachNewNode('blank-%d' % x)
                x += 1

            subDef.root.reparentTo(switchRoot)

        return (
         modelDef, [ subDef[1] for subDef in subDefs ])

    def makeModelDef(self, data):
        model = ModelDef()
        PandaNode(data.getName()).replaceNode(data.node())
        lod = data.find('**/+LODNode')
        if lod and lod.getNumChildren() == 4:
            holes = lod.getChild(0).findAllMatches('**/door_hole*')
            holes.addPathsFrom(lod.getChild(1).findAllMatches('**/door_hole*'))
            holes.addPathsFrom(lod.getChild(2).findAllMatches('**/door_hole*'))
            for hole in lod.getChild(3).findAllMatches('**/door_hole*'):
                hole.findAllMatches('**/+GeomNode').wrtReparentTo(hole.getParent())
                hole.detachNode()

        else:
            holes = data.findAllMatches('**/door_hole*')
        for hole in holes:
            geoms = hole.findAllMatches('**/+GeomNode')
            geoms.setColorScale(0, 0, 0, 1)
            geoms.wrtReparentTo(hole.getParent())
            hole.detachNode()

        lowendHighNP = data.find('**/lowend*')
        if not lowendHighNP.isEmpty():
            lowendHighNP.detachNode()
            lowendHighNP.flattenStrong()
        model.root = NodePath('model')
        model.root.setTag('ModelName', data.getName())
        model.geomRoot = model.root.attachNewNode('geomRoot')
        data.reparentTo(model.geomRoot)
        data.findAllMatches('**/door_locator*').wrtReparentTo(model.geomRoot)
        data.findAllMatches('**/door_left*').wrtReparentTo(model.geomRoot)
        data.findAllMatches('**/door_right*').wrtReparentTo(model.geomRoot)
        for obj in data.findAllMatches('**/=ignore-lighting'):
            obj.setLightOff(1000)

        model.collisions = model.root.attachNewNode('collisions')
        cols = data.findAllMatches('**/+CollisionNode')
        for i in xrange(cols.getNumPaths()):
            cols[i].wrtReparentTo(model.collisions)

        model.geomRoot.findAllMatches('**/collisions').detach()
        effects = data.findAllMatches('**/*_effect*;+s')
        if effects:
            model.effects = model.root.attachNewNode('effects')
            effects.wrtReparentTo(model.effects)
        self.flattenObj(data)
        model.lod = data.find('**/+LODNode')
        if model.lod.isEmpty():
            model.lod = model.geomRoot.attachNewNode(LODNode('lod'))
            model.lod.node().addSwitch(100000, 0)
            model.high = model.lod.attachNewNode('high')
            model.med = None
            model.low = None
            data.reparentTo(model.high)
        else:
            model.lod.wrtReparentTo(model.geomRoot)
            data.reparentTo(model.geomRoot)
        if model.lod.node().getNumSwitches() != model.lod.getNumChildren():
            self.setupSwitchDistances(model.lod.node(), model.root)
        if base.options.getTerrainDetailSetting() > PiratesGlobals.TD_LOW:
            model.high = model.lod.getChild(0)
            if model.lod.getNumChildren() > 1:
                model.med = model.lod.getChild(1)
                if model.lod.getNumChildren() > 2:
                    model.low = model.lod.getChild(2)
                    if model.lod.getNumChildren() > 3:
                        model.superLow = model.lod.getChild(3)
                    else:
                        model.superLow = None
                else:
                    model.low = None
                    model.superLow = None
            else:
                model.med = None
                model.low = None
                model.superLow = None
        elif base.options.getTerrainDetailSetting() == PiratesGlobals.TD_LOW:
            if model.lod.getNumChildren() >= 4:
                model.lod.node().removeChild(0)
                model.lod.node().removeChild(0)
                model.high = model.lod.getChild(0)
                model.med = model.lod.getChild(1)
                model.low = None
                model.superLow = None
            elif model.lod.getNumChildren() == 3:
                model.lod.node().removeChild(0)
                model.lod.node().removeChild(0)
                model.high = model.lod.getChild(0)
                model.med = None
                model.low = None
                model.superLow = None
            elif model.lod.getNumChildren() == 2:
                model.lod.node().removeChild(0)
                model.high = model.lod.getChild(0)
                model.med = None
                model.low = None
                model.superLow = None
            elif model.lod.getNumChildren() == 1:
                model.high = model.lod.getChild(0)
                model.med = None
                model.low = None
                model.superLow = None
        if base.gridDetail != 'high' and not lowendHighNP.isEmpty():
            model.high.get_children().detach()
            lowendHighNP.node().replaceNode(model.high.node())
        numChildren = model.lod.getNumChildren()
        numSwitches = model.lod.node().getNumSwitches()
        switches = []
        for i in range(numSwitches):
            switches.append((model.lod.node().getIn(i), model.lod.node().getOut(i)))

        for i in range(numChildren - 1):
            model.lod.node().addSwitch(switches[i][0], switches[i][1])

        #model.lod.node().addSwitch(1000000, switches[numChildren - 1][1])
        return model

    def setupSwitchDistances(self, lodNode, root):
        bounds = root.getBounds()
        if bounds.isEmpty():
            return
        if bounds.isOfType(BoundingSphere.getClassType()):
            radius = bounds.getRadius()
        else:
            if bounds.isOfType(BoundingBox.getClassType()):
                radius = (bounds.getMax() - bounds.getMin()).length() / 2
            else:
                return
            lodNode.clearSwitches()
            lodNode.setCenter(Point3(0, 0, 0))
            numChildren = NodePath(lodNode).getNumChildren()
            if config.GetBool('static-large-lods', 0):
                for i in range(numChildren - 1):
                    lodNode.addSwitch(staticLODs[i + 1], staticLODs[i])

                lodNode.addSwitch(1000000, staticLODs[numChildren - 1])
            else:
                for i in xrange(numChildren - 1):
                    lodNode.addSwitch(radius * self.LOD_RADIUS_FACTOR_MOST[i + 1], radius * self.LOD_RADIUS_FACTOR_MOST[i])

            lodNode.addSwitch(100000, radius * self.LOD_RADIUS_FACTOR_MOST[numChildren - 1])

    def _applyRenderEffects(self, data):
        for node in data.findAllMatches('**/=Render=dual'):
            node.setAttrib(TransparencyAttrib.make(TransparencyAttrib.MMultisample), 1)

    def buildSign(self, objData, locator):
        signFrameName = objData['Visual'].get('SignFrame', '')
        if signFrameName:
            signFramePaletteName = signFrameName.split('frame')[0]
            signFrame = loader.loadModel(signFrameName)
            signIconModel = objData['Visual'].get('SignImage')
            if signIconModel:
                signIconName = objData['Visual']['SignImage'].split('icon')[1]
                signIcon = loader.loadModel(signFramePaletteName + 'icon' + signIconName)
                signIcon.reparentTo(signFrame)
                signFrame.reparentTo(locator)
                signFrame.flattenStrong()

    def getTreeInfo(self, data):
        match = re.match('(.*)_trunk_([a-z])_.*', data['Visual']['Model'])
        leafType = re.match('.*leaf_([a-z]).*', data['SubObjs']['Top Model']['Visual']['Model'])
        if match and leafType:
            modelRoot, trunkType = match.groups()
            return (
             modelRoot, trunkType, leafType.groups()[0])
        else:
            return None
        return None

    def loadTree(self, data):
        result = self.getTreeInfo(data)
        if result:
            if result in self.treeCache:
                return self.treeCache[result].copy()
            else:
                modelRoot, trunkType, leafType = result
                obj = ModelDef()
                modelHi = loader.loadModel('%s_hi' % modelRoot)
                modelMed = loader.loadModel('%s_med' % modelRoot)
                modelLow = loader.loadModel('%s_low' % modelRoot)
                modelAnim = loader.loadModel('%s_idle' % modelRoot)
                modelAnim.reparentTo(self.animNode)
                root = NodePath('Tree Root')
                geomRoot = root.attachNewNode('geomRoot')
                lod = FadeLODNode('tree lod')
                lodNP = geomRoot.attachNewNode(lod)
                modelHi.reparentTo(lodNP)
                modelMed.reparentTo(lodNP)
                modelLow.reparentTo(lodNP)
                self.setupSwitchDistances(lod, root)
                coll = loader.loadModel('%s_zero_coll' % modelRoot)
                obj.root = root
                obj.geomRoot = geomRoot
                obj.lod = lodNP
                obj.high = modelHi
                obj.med = modelMed
                obj.low = modelLow
                obj.collisions = obj.root.attachNewNode('collisions')
                coll.reparentTo(obj.collisions)
                trunk = obj.root.findAllMatches('**/*trunk_%s*' % trunkType)
                leaf = obj.root.findAllMatches('**/*leaf_%s' % leafType)
                obj.root.findAllMatches('**/+GeomNode').stash()
                trunk.unstash()
                leaf.unstash()
                self.treeCache[result] = obj
                return obj.copy()

    def makeLight(self, levelObj):
        light = EditorGlobals.LightDynamic(levelObj, self.areaGeometry, drawIcon=False)
        if light:
            light.lightNodePath.setTag('Global Light', '')
            OTPRender.renderReflection(False, light, 'p_light', None)
        return light

    def handleHolidayStarted(self, holidayName):
        self.unstashHolidayObjects(holidayName)
        self.master.handleHolidayStarted(holidayName)

    def handleHolidayEnded(self, holidayName):
        self.stashHolidayObjects(holidayName)
        self.master.handleHolidayEnded(holidayName)

    def checkForHolidayObjects(self):
        for holidayId in HolidayGlobals.getAllHolidayIds():
            if base.cr.newsManager and base.cr.newsManager.getHoliday(holidayId):
                self.unstashHolidayObjects(HolidayGlobals.getHolidayName(holidayId))
            else:
                self.stashHolidayObjects(HolidayGlobals.getHolidayName(holidayId))

    def stashHolidayObjects(self, holidayName):
        self.master.findAllMatches('**/=Holiday=%s;+s' % (holidayName,)).stash()

    def unstashHolidayObjects(self, holidayName):
        self.master.findAllMatches('**/=Holiday=%s;+s' % (holidayName,)).unstash()

    def arrived(self):
        pass

    def left(self):
        pass

    def cleanupData(self):
        for obj in self.cleanUpList:
            obj.cleanUp()

        self.cleanUpList = []
        self.unloadObjects()
        self.areaGeometry.get_children().detach()
        self.collisions.detachNode()
        self.collisions = self.areaGeometry.attachNewNode('collisions')
        self.staticGridRoot.detachNode()
        self.staticGridRoot = self.areaGeometry.attachNewNode('staticGrid')
        self.largeObjectsRoot.detachNode()
        self.largeObjectsRoot = self.areaGeometry.attachNewNode('largeObjects')
        self.animNode.detachNode()
        self.animNode = self.areaGeometry.attachNewNode('animations')
        self.ignoreAll()

    def flattenObj(self, obj):
        node = obj.node()
        gr = SceneGraphReducer()
        gr.applyAttribs(node, SceneGraphReducer.TTOther | SceneGraphReducer.TTCullFace | SceneGraphReducer.TTTransform | SceneGraphReducer.TTColor | SceneGraphReducer.TTColorScale)
        num_removed = gr.flatten(node, -1)
        gr.makeCompatibleState(node)
        gr.collectVertexData(node, ~(SceneGraphReducer.CVDFormat | SceneGraphReducer.CVDName | SceneGraphReducer.CVDAnimationType))
        gr.unify(node, 0)

    def setupFloors(self, data):
        for collision in data.findAllMatches('**/+CollisionNode;+s'):
            curMask = collision.node().getIntoCollideMask()
            if curMask.hasBitsInCommon(OTPGlobals.FloorBitmask):
                collision.node().setIntoCollideMask(collision.node().getIntoCollideMask() | PiratesGlobals.TargetBitmask)
                collision.setTag('objType', str(PiratesGlobals.COLL_LAND))
                collision.setTag('groundId', str(self.master.doId))

    def disableDynamicLights(self):
        attrib = render.getAttrib(LightAttrib.getClassType())
        if attrib:
            for i in range(attrib.getNumLights()):
                light = attrib.getLight(i).asNode()
                if light.getClassType() != AmbientLight.getClassType():
                    self.staticGridRoot.setLightOff(NodePath(light), 10)

    def addClassObj(self, parentObj, levelObj, myClass):
        newObj = myClass()
        objData = levelObj.data
        model = self.getModel(objData)
        newObj.setup(objData, 0, parent=parentObj, transform=levelObj.transform)
        return newObj

    def addEntityNode(self, entityCatName, entityTypeName, properties, levelObj):
        transform = levelObj.transform
        objData = levelObj.data
        uid = levelObj.uniqueId
        node = self.areaGeometry.attachNewNode(ModelNode('Entity_Node'))
        node.node().setPreserveTransform(ModelNode.PTLocal)
        node.setTransform(transform)
        node.setTag('EntityCat', entityCatName)
        node.setTag('EntityType', entityTypeName)
        dataDict = levelObj.data
        for propertyName in properties:
            propertyValue = dataDict.get(propertyName)
            if propertyValue:
                node.setTag(propertyName, propertyValue)

        return node

    def registerMinimapObject(self, levelObj):
        transform = levelObj.transform
        objData = levelObj.data
        uid = levelObj.uniqueId
        shopType = None
        if objData['Type'] == 'Building Exterior':
            visual = objData['Visual']
            imageString = visual.get('SignImage')
            if imageString and visual.get('SignFrame'):
                shopType = MinimapShop.getShopType(imageString)
        elif objData['Type'] == 'Townsperson':
            category = objData['Category'].lower()
            shopType = MinimapShop.getShopType(category)
        if shopType:
            node = self.areaGeometry.attachNewNode(ModelNode('MinimapShopNode'))
            node.node().setPreserveTransform(ModelNode.PTLocal)
            node.setTransform(transform)
            node.setTag('Uid', uid)
            node.setTag('ShopType', shopType)
            return node
        if objData['Type'] == 'Invasion Barricade':
            holiday = objData['Holiday']
            zone = objData['Zone']
            node = self.areaGeometry.attachNewNode(ModelNode('MinimapCapturePointNode'))
            node.node().setPreserveTransform(ModelNode.PTLocal)
            node.setTransform(transform)
            node.setTag('Holiday', holiday)
            node.setTag('Zone', zone)
            return node
        return

    def getMinimapShopNodes(self):
        return self.areaGeometry.findAllMatches('MinimapShopNode;+s')

    def getMinimapCapturePointNodes(self, holidayName):
        nodes = self.areaGeometry.findAllMatches('MinimapCapturePointNode;+s')
        nodes = [ node for node in nodes if node.getTag('Holiday') == holidayName ]
        return nodes

    def isVisible(self, data):
        return True

    def addSFXObject(self, levelObj):
        name = levelObj.data.get('SoundFX', '')
        node = self.areaGeometry.attachNewNode(ModelNode(name))
        node.node().setPreserveTransform(ModelNode.PTLocal)
        node.setTransform(levelObj.transform)
        return node

    def addEffectObject(self, levelObj):
        name = levelObj.data.get('EffectName', '')
        node = self.areaGeometry.attachNewNode(ModelNode(name))
        node.node().setPreserveTransform(ModelNode.PTLocal)
        node.setTransform(levelObj.transform)
        return node

    def handleLighting(self, obj, visZone):
        pass

    def registerEffect(self, effect):
        pass

    def unregisterEffect(self, effect):
        pass

    def initEffects(self):
        pass

    def turnOnLights(self):
        for light in self.globalLights:
            render.setLight(light)

    def turnOffLights(self):
        for light in self.globalLights:
            render.clearLight(light)

    def getTunnelMinimap(self, tunnelUid):
        return 0

    def localAvLeaving(self):
        pass

    def addCutsceneOriginNode(self):
        for object in self.areaGeometry.findAllMatches('**/=Object_Cutscene'):
            base.cr.activeWorld.addCutsceneOriginNode(object, object.getName())
