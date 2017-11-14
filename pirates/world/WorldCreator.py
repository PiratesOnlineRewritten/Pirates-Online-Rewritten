from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase import DirectObject
from pirates.world import WorldCreatorBase
from pirates.leveleditor import ObjectList
from pirates.piratesbase import PiratesGlobals
from pirates.leveleditor import EditorGlobals
from pirates.leveleditor import WorldDataGlobals
from pirates.effects import DynamicLight
from direct.actor import Actor
from otp.otpbase import OTPRender
from pirates.world import SectionAreaBuilder, GridAreaBuilder, ModularAreaBuilder

class WorldCreator(WorldCreatorBase.WorldCreatorBase, DirectObject.DirectObject):
    notify = directNotify.newCategory('WorldCreator')
    animPartsDict = {'Crane': [('Hpr', 2, Point3(10, 10, 0), Point3(-10, -10, 0), '')]}

    def __init__(self, cr, worldFile, district):
        self.propNum = 0
        self.cr = cr
        self.district = district
        WorldCreatorBase.WorldCreatorBase.__init__(self, cr, worldFile)
        self.portalAreas = []
        self.postLoadCalls = []
        self.oceanAreas = {}
        self.waypoints = {}
        self.links = {}
        self.allowFishingGame = config.GetBool('want-fishing-game', 0)
        self.allowRepairGame = config.GetBool('want-repair-game', 0)
        self.allowPotionGame = config.GetBool('want-potion-game', 0)
        self.allowCannonGame = config.GetBool('want-cannondefense-game', 0)

    def destroy(self):
        self.district = None
        return

    def cleanupAllAreas(self):
        self.portalAreas = []

    def loadObjectsFromFile(self, filename, parent, parentUid=None, dynamic=0, merge=False):
        fileData = self.openFile(filename)
        if parentUid:
            fileDict = {filename: fileData}
            if merge:
                subUid = fileData['Objects'].keys()[0]
                self.loadAdditionalObjectsByUid(subUid, parent, parentUid, dynamic=dynamic, fileDict=fileDict)
            else:
                self.loadObjectsByUid(parent, parentUid, dynamic=dynamic, fileDict=fileDict)
        elif parent == self.cr:
            self.loadOceanData(filename, fileData)
            self.loadWaypointData(filename, fileData)
        self.storeNecessaryAreaData(parentUid, fileData)
        return self.fileDicts

    def loadWaypointData(self, filename, fileData):
        filename = None
        self.waypoints[filename] = {}
        self.loadWaypointDataFromDict(filename, fileData)
        links = fileData.get(WorldDataGlobals.LINK_TYPE_AI_NODE, [])
        for link in links:
            if not self.waypoints[filename].has_key(link[0]):
                continue
            if not self.waypoints[filename].has_key(link[1]):
                continue
            if link[2] in ['Direction 1', 'Bi-directional']:
                self.waypoints[filename][link[1]]['Links'].append(link[0])
            if link[2] in ['Direction 2', 'Bi-directional']:
                self.waypoints[filename][link[0]]['Links'].append(link[1])

        return

    def loadWaypointDataFromDict(self, filename, fileDict):
        for key in fileDict.iterkeys():
            if isinstance(fileDict[key], type({})):
                if fileDict[key].get('Type') in WorldDataGlobals.WAYPOINT_TYPES:
                    self.waypoints[filename][key] = {'Pos': fileDict[key].get('Pos'),'Links': []}
                self.loadWaypointDataFromDict(filename, fileDict[key])

    def getWaypointPos(self, waypointId, filename=None):
        waypoint = self.waypoints[filename].get(waypointId)
        if waypoint:
            return waypoint.get('Pos')
        return None

    def getWaypointLinks(self, waypointId, filename=None):
        waypoint = self.waypoints[filename].get(waypointId)
        if waypoint:
            return waypoint.get('Links')
        return []

    def loadOceanData(self, filename, fileData):
        oceanAreas = fileData.get(WorldDataGlobals.OCEAN_AREAS)
        if oceanAreas:
            self.oceanAreas[filename] = oceanAreas

    def getOceanData(self, filename):
        return self.oceanAreas.get(filename)

    def loadObjectsByUid(self, parent, parentUid, dynamic=0, fileDict=None):
        objectInfo = self.getObjectDataByUid(parentUid, fileDict)
        if not objectInfo:
            if len(parent.master.links):
                tunnel = base.cr.doId2do.get(parent.master.links[0][0])
                self.notify.error('Data file not found for area. connecting tunnel uid = %s' % tunnel.uniqueId)
            self.notify.error('Data file not found for area being loaded: %s, make sure worldCreator.loadObjectsFromFile is being called.' % parentUid)
        objDict = objectInfo.get('Objects')
        if objDict != None:
            self.loadObjectDict(objDict, parent, parentUid, dynamic)
        if objectInfo.has_key('AdditionalData'):
            additionalFiles = objectInfo['AdditionalData']
            for currFile in additionalFiles:
                self.loadObjectsFromFile(currFile + '.py', parent, parentUid, dynamic, merge=True)

            if objectInfo.has_key('AdditionalData'):
                additionalFiles = objectInfo['AdditionalData']
                for currFile in additionalFiles:
                    if self.fileDicts.has_key(currFile + '.py'):
                        altParentUid = self.fileDicts[currFile + '.py']['Objects'].keys()[0]
                        addObjDict = self.fileDicts[currFile + '.py']['Objects'][altParentUid]['Objects']
                        self.loadObjectDict(addObjDict, parent, parentUid, dynamic)
                        yieldThread('load object')

        fileRef = objectInfo.get('File')
        if fileRef:
            self.loadObjectsFromFile(fileRef + '.py', parent, parentUid, dynamic)
        return

    def loadAdditionalObjectsByUid(self, subUid, parent, parentUid, dynamic=0, fileDict=None):
        objectInfo = self.getObjectDataByUid(subUid, fileDict)
        if not objectInfo:
            if len(parent.master.links):
                tunnel = base.cr.doId2do.get(parent.master.links[0][0])
                self.notify.error('Data file not found for area. connecting tunnel uid = %s' % tunnel.uniqueId)
            self.notify.error('Data file not found for area being loaded: %s, make sure worldCreator.loadObjectsFromFile is being called.' % parentUid)
        objDict = objectInfo.get('Objects')
        if objDict != None:
            self.loadObjectDict(objDict, parent, parentUid, dynamic)
        if objectInfo.has_key('AdditionalData'):
            additionalFiles = objectInfo['AdditionalData']
            for currFile in additionalFiles:
                self.loadObjectsFromFile(currFile + '.py', parent, parentUid, dynamic)

        fileRef = objectInfo.get('File')
        if fileRef:
            self.loadObjectsFromFile(fileRef + '.py', parent, parentUid, dynamic)
        return

    def findObjectCategory(self, objectType):
        cats = ObjectList.AVAIL_OBJ_LIST.keys()
        for currCat in cats:
            types = ObjectList.AVAIL_OBJ_LIST[currCat].keys()
            if objectType in types:
                return currCat

        return None

    def createObject(self, object, parent, parentUid, objKey, dynamic, fileName=None, actualParentObj=None):
        objType = WorldCreatorBase.WorldCreatorBase.createObject(self, object, parent, parentUid, objKey, dynamic, fileName=fileName)
        if not objType:
            return (None, None)
        newObj = None
        objParent = None
        parentDoId = base.cr.uidMgr.getDoId(parentUid)
        if parentDoId:
            objParent = base.cr.getDo(parentDoId)
            if not objParent:
                pass
        if dynamic:
            objectCat = self.findObjectCategory(objType)
            if objType == 'Jack Sparrow Standin' and base.config.GetBool('want-npcs', 1) is 1:
                newObj = self.createJackSparrowStandin(object, objKey, objParent)
            elif objectCat == 'PROP_OBJ' or objectCat == 'BUILDING_OBJ':
                if objType == 'Light - Dynamic':
                    light = objParent.builder.createDynamicLight(object, objParent)
                    if light:
                        base.cr.uidMgr.uid2obj[objKey] = light
                        objParent.builder.addLight(light)
                    OTPRender.renderReflection(False, light, 'p_light', None)
                elif objParent:
                    if object.has_key('Color'):
                        if not object.has_key('Visual'):
                            object['Visual'] = {}
                        if not object['Visual'].has_key('Color'):
                            object['Visual']['Color'] = object['Color']
                    self.propNum += 1
                    newObj = objParent.builder.addChildObj(object, objKey, altParent=actualParentObj, actualParentObj=actualParentObj)
                    if newObj:
                        base.cr.uidMgr.uid2obj[objKey] = newObj
                        if objType in ('Pier', 'Dinghy'):
                            OTPRender.renderReflection(True, newObj, 'p_pier', None)
            elif objType == 'Cell Portal Area':
                newObj = objParent.builder.addChildObj(object, objKey)
            elif objType == 'Event Sphere':
                newObj = self.addEventSphere(object, objParent)
            elif objType == 'Port Collision Sphere':
                pos = object.get('Pos', Point3(0, 0, 0))
                radius = object.get('Scale', VBase3(500))[0]
            elif objType == 'Location Sphere':
                if objParent:
                    newObj = self.addLocationSphere(objKey, object, objParent, parentUid)
        if objType == 'Cutscene Origin Node':
            if objParent:
                pos = object['Pos']
                hpr = object['Hpr']
                name = object['CutsceneId']
                node = objParent.attachNewNode(ModelNode(name))
                node.node().setPreserveTransform(ModelNode.PTLocal)
                node.setPosHpr(pos, hpr)
                self.cr.activeWorld.addCutsceneOriginNode(node, name)
                newObj = node
        elif objType == 'Effect Node':
            if objParent:
                pos = object['Pos']
                hpr = object['Hpr']
                if object.has_key('Scale'):
                    scale = object['Scale']
                else:
                    scale = Point3(1.0, 1.0, 1.0)
                name = object['EffectName']
                node = objParent.attachNewNode(ModelNode(name))
                node.node().setPreserveTransform(ModelNode.PTLocal)
                node.setPosHprScale(pos, hpr, scale)
                newObj = node
        elif objType == 'Dinghy':
            newObj = objParent.builder.addChildObj(object, objKey)
        return (
         newObj, None)

    def loadObject(self, object, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        newObj, actualParentObj = self.createObject(object, parent, parentUid, objKey, dynamic, fileName=fileName, actualParentObj=actualParentObj)
        objDict = object.get('Objects')
        if objDict:
            if newObj:
                parentObj = newObj
                newParentUid = objKey
                self.loadObjectDict(objDict, parentObj, newParentUid, dynamic, actualParentObj=newObj)
        return newObj

    def addEventSphere(self, levelObj, objParent):
        objPos = levelObj.transform.getPos()
        radius = levelObj.transform.getHpr()[0]
        category = levelObj.data['Event Type']
        extraParam = levelObj.data['Extra Param']
        collideType = PiratesGlobals.WallBitmask
        collType = levelObj.data['Collide Type']
        if collType == 'Ship':
            collideType = PiratesGlobals.ShipCollideBitmask
        elif collType == 'Object':
            collideType = PiratesGlobals.ShipCollideBitmask
        newEventSphere = CollisionSphere(objPos[0], objPos[1], objPos[2], radius)
        newEventSphere.setTangible(0)
        newEventSphereName = self.cr.activeWorld.uniqueName(extraParam) + str(id(newEventSphere))
        newEventSphereNode = CollisionNode(newEventSphereName)
        msgName = None
        if category == 'Port':
            msgName = PiratesGlobals.EVENT_SPHERE_PORT
            newEventSphereNode.setFromCollideMask(BitMask32.allOff())
            newEventSphereNode.setIntoCollideMask(collideType)
        elif category == 'Capture':
            msgName = PiratesGlobals.EVENT_SPHERE_CAPTURE
            newEventSphereNode.setFromCollideMask(BitMask32.allOff())
            newEventSphereNode.setIntoCollideMask(collideType)
        elif category == 'Sneak':
            newEventSphere.setTangible(1)
            msgName = PiratesGlobals.EVENT_SPHERE_SNEAK
            newEventSphereNode.setFromCollideMask(BitMask32.allOff())
            newEventSphereNode.setIntoCollideMask(collideType)
        elif category == 'Dock':
            pass
        elif category == 'DockWall':
            pass
        elif category in ['Spawning', 'Staging']:
            return
        newEventSphereNode.addSolid(newEventSphere)
        newEventSphereNodePath = objParent.builder.collisions.attachNewNode(newEventSphereNode)
        self.cr.activeWorld.accept('enter' + newEventSphereName, self.cr.activeWorld.enteredSphere, extraArgs=[[msgName, extraParam]])
        self.cr.activeWorld.accept('exit' + newEventSphereName, self.cr.activeWorld.exitedSphere, extraArgs=[[msgName, extraParam]])
        return newEventSphereNodePath

    def addLocationSphere(self, levelObj, objParent, parentUid=None):
        uid = levelObj.uniqueId
        objPos = levelObj.transform.getPos()
        radius = levelObj.transform.getScale()[0]
        locName = levelObj.data.get('Area Name', '')
        collideType = PiratesGlobals.WallBitmask | PiratesGlobals.ShipCollideBitmask
        newSphere = CollisionSphere(objPos[0], objPos[1], objPos[2], radius)
        newSphere.setTangible(0)
        newSphereName = 'locSphere-%s' % objParent.uniqueId
        newSphereNode = CollisionNode(newSphereName)
        newSphereNode.setTag('uid', uid)
        newSphereNode.setTag('parentUid', objParent.uniqueId)
        msgName = None
        msgName = PiratesGlobals.LOCATION_SPHERE
        newSphereNode.setFromCollideMask(BitMask32.allOff())
        newSphereNode.setIntoCollideMask(collideType)
        newSphereNode.addSolid(newSphere)
        newSphereNodePath = objParent.builder.collisions.attachNewNode(newSphereNode)
        objParent.builder.addLocationSphere(uid, objPos, radius, locName)
        return newSphereNodePath

    def createDynamicLight(self, objData, objParent):
        light = EditorGlobals.LightDynamic(objData, objParent, drawIcon=False)
        return light

    def createJackSparrowStandin(self, object, uid, parent):
        self.notify.debug('creating Jack')
        jack = Actor.Actor(object['Visual']['Model'], {'idle': 'models/char/js_idle','walk': 'models/char/js_walk','run': 'models/char/js_run'})
        jack.loop('idle')
        __builtins__['js'] = jack
        return parent.builder.addChildObj(object, uid, objRef=jack)

    def loadAnimParts(self, object, objParent):
        effects = self.animPartsDict.get(object)
        intervals = Parallel()
        for effect in effects:
            myPart = effect[4]
            if effect[0] == 'Hpr':
                randomness = random.random() / 10
                rotate1 = myPart.hprInterval(effect[1] + randomness, effect[3], startHpr=effect[2], blendType='easeInOut')
                rotate2 = myPart.hprInterval(effect[1] + randomness, effect[2], startHpr=effect[3], blendType='easeInOut')
                anim = Sequence(rotate1, rotate2)
                anim.loop()
                intervals.append(anim)
            elif effect[0] == 'ColorFade':
                randomness = random.random() / 10
                fadeIn = myPart.colorInterval(effect[1] + randomness, effect[3], startColor=effect[2])
                fadeOut = myPart.colorInterval(effect[1] + randomness, effect[2], startColor=effect[3])
                anim = Sequence(fadeIn, fadeOut)
                anim.loop()
                intervals.append(anim)
            elif effect[0] == 'DelayColorFade':
                randomness = random.random() / 10
                fadeIn = myPart.colorInterval(effect[1] + randomness, effect[3], startColor=effect[2])
                fadeOut = myPart.colorInterval(effect[1] + randomness, effect[2], startColor=effect[3])
                anim = Sequence(fadeIn, Wait(effect[4]), fadeOut, Wait(effect[4]))
                anim.loop()
                intervals.append(anim)
            elif effect[0] == 'UVScroll':
                t = myPart.findAllTextureStages()[0]
                randomness = random.random() / 10
                anim = LerpFunctionInterval(self.setNewUVs, fromData=0.0, toData=10.0, duration=effect[1] + randomness, extraArgs=[myPart, t, effect], name='UVScroll-%d')
                anim.loop()
                intervals.append(anim)
            elif effect[0] == 'UVOverlayScroll':
                t = TextureStage('t')
                t.setMode(TextureStage.MBlend)
                t.setSort(60)
                card = loader.loadModel(effect[4])
                tex = card.findTexture('*')
                myPart.setTexture(t, tex)
                myPart.setTexScale(t, 2, 2)
                randomness = random.random() / 10
                anim = LerpFunctionInterval(self.setNewUVs, fromData=0.0, toData=10.0, duration=effect[1] + randomness, extraArgs=[myPart, t, effect], name='UVOverlayScroll-%d')
                anim.loop()
                intervals.append(anim)
            elif effect[0] == 'Unlit':
                myPart.setDepthWrite(0)
                myPart.setColorScaleOff()
                myPart.setFogOff()

        return intervals

    def registerPostLoadCall(self, funcCall):
        self.postLoadCalls.append(funcCall)

    def processPostLoadCalls(self):
        functionsCalled = []
        for currObj in self.postLoadCalls:
            if currObj not in functionsCalled:
                functionsCalled.append(currObj)
                currObj()

        self.postLoadCalls = []

    def registerSpecialNodes(self, parent, uniqueId):
        self.registerSpawnNodes(parent, uniqueId)
        self.registerCutsceneNodes(parent, uniqueId)

    def registerSpawnNodes(self, parent, uniqueId):
        spawnNodes = base.worldCreator.getObjectsOfType(uniqueId, 'Player Spawn Node')
        for object in spawnNodes:
            pos = object.transform.getPos()
            hpr = object.transform.getHpr()
            index = object.data.get('Index', -1)
            posHpr = (pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2])
            parent.getParentObj().addPlayerSpawnPt(parent, posHpr, index)

    def registerCutsceneNodes(self, parent, uniqueId):
        cutsceneNodes = base.worldCreator.getObjectsOfType(uniqueId, 'Cutscene Origin Node')
        for object in cutsceneNodes:
            pos = object.transform.getPos()
            hpr = object.transform.getHpr()
            name = object.data['CutsceneId']
            node = parent.attachNewNode(ModelNode(name))
            node.node().setPreserveTransform(ModelNode.PTLocal)
            node.setPosHpr(pos, hpr)
            parent.getParentObj().addCutsceneOriginNode(node, name)

    def createObj(self, levelObj, gameArea):
        objType = levelObj.data.get('Type')
        objectCat = self.findObjectCategory(objType)
        newObj = None
        if ObjectList.AVAIL_OBJ_LIST[objectCat][objType].has_key('Entity'):
            properties = ObjectList.AVAIL_OBJ_LIST[objectCat][objType]['Properties']
            newObj = gameArea.builder.addEntityNode(objectCat, objType, properties, levelObj)
        elif objType == 'Cutscene Origin Node':
            name = levelObj.data.get('CutsceneId')
            node = gameArea.builder.areaGeometry.attachNewNode(ModelNode(name))
            node.node().setPreserveTransform(ModelNode.PTLocal)
            node.setTransform(levelObj.transform)
            node.setTag('Object_Cutscene', '1')
            newObj = node
        elif objType == 'Light - Dynamic' or objType == 'Light - Modular':
            newObj = gameArea.builder.makeLight(levelObj)
        elif objType == 'Event Sphere':
            newObj = self.addEventSphere(levelObj, gameArea)
        elif objType == 'Location Sphere':
            newObj = self.addLocationSphere(levelObj, gameArea)
        elif objType == 'Effect Node':
            newObj = gameArea.builder.addEffectObject(levelObj)
        elif objType == 'SFX Node':
            newObj = gameArea.builder.addChildObj(levelObj)
            base.theSFX = newObj
            print "Before it's #*$ up %s" % newObj.getPos(render)
        elif objType == 'Portal Node':
            node = gameArea.builder.areaGeometry.attachNewNode(ModelNode(levelObj.data.get('Name', '')))
            node.node().setPreserveTransform(ModelNode.PTLocal)
            node.setTransform(levelObj.transform)
            visZone = levelObj.get('VisZone')
            if visZone:
                node.setTag('PortalVis', visZone)
        elif objectCat == 'PROP_OBJ' or objectCat == 'BUILDING_OBJ' or objType in ('Dinghy', 'Holiday Object') or objType == 'Cave_Pieces':
            newObj = gameArea.builder.addChildObj(levelObj)
        elif objType == 'RepairBench' and self.allowRepairGame:
            newObj = gameArea.builder.addChildObj(levelObj)
        elif objType == 'PotionTable' and self.allowPotionGame:
            newObj = gameArea.builder.addChildObj(levelObj)
        elif objType == 'FishingSpot' and self.allowFishingGame:
            newObj = gameArea.builder.addChildObj(levelObj)
        elif objType == 'Cannon Defense Game' and self.allowCannonGame:
            newObj = gameArea.builder.addChildObj(levelObj)
        elif objType == 'Switch Prop':
            newObj = gameArea.builder.addChildObj(levelObj)
        elif objType == 'Townsperson':
            rolOffset = levelObj.data.get('rolOffset')
            if rolOffset:
                uid = levelObj.uniqueId
                node = gameArea.builder.areaGeometry.find('npcData')
                if not node:
                    node = gameArea.builder.areaGeometry.attachNewNode(ModelNode('npcData'))
                    currTag = node.getTag('npcData')
                    if currTag:
                        data = eval(currTag)
                    else:
                        data = {}
                    data.setdefault(uid, {}).update({'rolOffset': rolOffset})
                    node.setTag('npcData', str(data))
                    newObj = node
        elif objType == 'Building Exterior':
            gameArea.builder.registerMinimapObject(levelObj)
        peopleWithIcons = ('Shipwright', 'Stowaway', 'Gypsy', 'CatalogRep')
        if self.allowFishingGame:
            peopleWithIcons = peopleWithIcons + ('Fishmaster', )
        if self.allowCannonGame:
            peopleWithIcons = peopleWithIcons + ('Cannonmaster', )
        if objType == 'Townsperson' and levelObj.data['Category'] in peopleWithIcons:
            gameArea.builder.registerMinimapObject(levelObj)
        if objType == 'Invasion Barricade':
            gameArea.builder.registerMinimapObject(levelObj)
        return newObj

    @report(types=['args'], dConfigParam='dteleport')
    def getBuilder(self, master, areaType):
        if areaType == 'Section':
            return SectionAreaBuilder.SectionAreaBuilder(master)
        elif areaType == 'Modular':
            return ModularAreaBuilder.ModularAreaBuilder(master)
        else:
            return GridAreaBuilder.GridAreaBuilder(master)

    def isPvpIslandByUid(self, islandUid):
        if not base.cr.config.GetBool('want-privateering', 1):
            return False
        objData = self.getObjectDataByUid(islandUid)
        if not objData:
            base.cr.centralLogger.writeClientEvent('DevWarning: unknown islandUid (%s)' % (islandUid,))
            return False
        else:
            return 'PVPTeam' in objData

    def getPvpIslandTeam(self, islandUid):
        return int(self.getObjectDataByUid(islandUid).get('PVPTeam', 0))

    def isMysteriousIslandByUid(self, islandUid):
        objData = self.getObjectDataByUid(islandUid)
        if not objData:
            base.cr.centralLogger.writeClientEvent('DevWarning: unknown islandUid (%s)' % (islandUid,))
            return False
        else:
            objects = objData.get('Objects')
            if objects:
                return False
            else:
                return True