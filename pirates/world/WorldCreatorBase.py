from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals
from pirates.piratesbase import TODGlobals
import os
import re
import imp
import types
from pirates.world.WorldGlobals import LevelObject

class WorldCreatorBase():

    def __init__(self, repository, worldFile=None):
        self.parentWorlds = []
        self.creatingInstance = False
        self.creatingInstanceParams = None
        self.repository = repository
        self.fileDicts = {}
        self.fileObjs = {}
        self.uidVisTables = {}
        self.uidAdjTables = {}
        self.uidTodSettings = {}
        self.uidEnvSettings = {}
        self.uidVisZoneMinimaps = {}
        self.uidVisZoneTunnels = {}
        self.uidMinimapPrefix = {}
        self.footstepTable = {}
        self.environmentTable = {}
        return

    def makeMainWorld(self, worldFile):
        self.worldType = PiratesGlobals.INSTANCE_MAIN
        if worldFile is not None:
            self.loadObjectsFromFile(worldFile, self.repository)
        self.worldType = None
        return

    def loadObjectsFromFile(self, filename, parent, parentIsObj=False):
        fileDict = self.openFile(filename)
        self.fileDicts[filename] = fileDict
        objDict = fileDict.get('Objects')
        parentUid = None
        if hasattr(parent, 'getUniqueId'):
            parentUid = parent.getUniqueId()
        objects = self.loadObjectDict(objDict, parent, parentUid, dynamic=0, parentIsObj=parentIsObj, fileName=re.sub('.py', '', filename))
        return [
         fileDict, objects]

    def getFieldFromUid(self, uid, field):
        objectInfo = self.getObjectDataByUid(uid, None)
        return objectInfo.get(field, '')

    def getModelPathFromFile(self, file):
        fileDict = self.openFile(file + '.py')
        return fileDict['Objects'].values()[0]['Visual']['Model']

    @report(types=['args'], dConfigParam=['dteleport'])
    def loadFileDataRecursive(self, file):
        fileDict = self.openFile(file)
        objects = fileDict.get('Objects')
        if objects:
            self.rFindFile(objects)
        self.fileDicts[file] = fileDict

    def rFindFile(self, objSet):
        for obj in objSet.values():
            fileName = obj.get('File')
            if fileName:
                self.loadFileDataRecursive(fileName + '.py')
            objects = obj.get('Objects')
            if objects:
                self.rFindFile(objects)

    def getObjectsOfType(self, uid, objType):
        finalObjs = []
        data = self.getObjectDataByUid(uid, None)
        objRoot = LevelObject(uid, data)
        self.rGetObjects(objRoot, data.get('Objects', []), finalObjs, objType)
        fileName = data.get('File')
        if fileName:
            fileDict = self.openFile(fileName + '.py')
            self.rGetObjects(objRoot, fileDict.get('Objects', []), finalObjs, objType)
        return finalObjs

    def rGetObjects(self, parentObj, subObjs, finalObjs, objType):
        for i in subObjs:
            data = subObjs[i]
            levelObj = LevelObject(i, data)
            levelObj.transform = parentObj.transform.compose(levelObj.transform)
            objList = data.get('Objects')
            if objList:
                self.rGetObjects(levelObj, objList, finalObjs, objType)
            if objType == data.get('Type'):
                finalObjs.append(levelObj)

    def loadObjectDict(self, objDict, parent, parentUid, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        objects = []
        for objKey in objDict.keys():
            newObj = self.loadObject(objDict[objKey], parent, parentUid, objKey, dynamic, parentIsObj=parentIsObj, fileName=fileName, actualParentObj=actualParentObj)
            if newObj:
                objects.append(newObj)

        return objects

    def loadInstancedObject(self, object, parent, parentUid, objKey, instanceParams=[]):
        self.creatingInstance = True
        self.creatingInstanceParams = instanceParams
        newObj = self.loadObject(object, parent, parentUid, objKey, False)
        self.creatingInstance = False
        self.creatingInstanceParams = None
        return newObj

    def loadObject(self, object, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        if not self.isObjectInCurrentGamePhase(object):
            return
        prevWorld = self.world
        newObjInfo = self.createObject(object, parent, parentUid, objKey, dynamic, parentIsObj=parentIsObj, fileName=fileName, actualParentObj=actualParentObj)
        if newObjInfo:
            newObj, newActualParent = newObjInfo
        else:
            return
        instanced = object.get('Instanced')
        if instanced:
            self.world.setCanBePrivate(instanced)
        objDict = object.get('Objects')
        if objDict:
            if newObj == None:
                newObj = parent
                if hasattr(newObj, 'getUniqueId'):
                    objKey = newObj.getUniqueId()
            self.loadObjectDict(objDict, newObj, objKey, dynamic, fileName=fileName, actualParentObj=newActualParent)
        #self._restoreWorld(prevWorld)
        return newObj

    def _restoreWorld(self, prevWorld):
        parentWorld = None
        if self.parentWorlds:
            parentWorld = self.parentWorlds[-1]
        if parentWorld:
            if prevWorld is not self.world:
                self.world = self.parentWorlds.pop()
        else:
            self.world = prevWorld
        return

    def createObject(self, object, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        objType = object.get('Type')
        self.notify.debug('createObject: type = %s' % objType)
        if dynamic and object.get('ExtUid'):
            return objType
        childFilename = object.get('File')
        if childFilename and object['Type'] != 'Building Exterior' and object['Type'] != 'Island Game Area':
            self.loadObjectsFromFile(childFilename + '.py', parent)
            return None
        return objType

    def openFile(self, filename):
        objectStruct = None
        moduleName = filename[:-3]
        try:
            obj = __import__('pirates.leveleditor.worldData.' + moduleName)
        except ImportError:
            obj = None
        except ValueError, e:
            self.notify.error('%s when loading %s' % (e, filename))

        for symbol in ['leveleditor', 'worldData', moduleName, 'objectStruct']:
            if obj:
                obj = getattr(obj, symbol, None)

        if not obj:
            self.notify.warning('Loading old-style file %s' % filename)
            spfSearchPath = DSearchPath()
            spfSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$PIRATES/src/leveleditor/worldData')))
            spfSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('pirates/src/leveleditor/worldData')))
            spfSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('pirates/leveleditor/worldData')))
            spfSearchPath.appendDirectory(Filename('.'))
            pfile = Filename(filename)
            found = vfs.resolveFilename(pfile, spfSearchPath)
            data = vfs.readFile(pfile, 1)
            data = data.replace('\r', '')
            try:
                obj = eval(data)
            except SyntaxError:
                obj = None

        return obj

    def getObjectDataByUid(self, uid, fileDict=None):
        fileDict = fileDict or self.fileDicts
        objectInfo = None
        for fileData in fileDict.itervalues():
            if uid in fileData['ObjectIds']:
                getSyntax = 'objectInfo = fileData' + fileData['ObjectIds'][uid]
                exec getSyntax
                if not objectInfo.has_key('File') or objectInfo.get('File') == '':
                    break

        return objectInfo

    def getObjectDataFromFileByUid(self, uid, fileName, getParentUid=False):
        objectInfo = None
        if fileName:
            if '.py' not in fileName:
                fileName += '.py'
            if self.isObjectDefined(uid, fileName):
                fileData = self.fileDicts[fileName]
                if getParentUid:
                    notFollowedBy = '(?!.*\\[".*\\[".*\\[".*)'
                    isFollowedBy = '(?=.*\\[".*\\[".*)'
                    match = re.search('(\\[")' + notFollowedBy + isFollowedBy + '.*?[\\]]', fileData['ObjectIds'][uid])
                    if match and match.end() - match.start() > 4:
                        return fileData['ObjectIds'][uid][match.start() + 2:match.end() - 2]
                    self.notify.warning('getObjectDataFromFileByUid: could not extract parentId from %s' % fileData['ObjectIds'][uid])
                    getSyntax = 'objectInfo = None'
                else:
                    getSyntax = 'objectInfo = fileData' + fileData['ObjectIds'][uid]
                exec getSyntax
        return objectInfo

    def getFilelistByUid(self, uid, fileDict = None):
        objectInfo = None
        if not fileDict:
            fileDict = self.fileDicts

        fileList = set()
        for name in fileDict:
            fileData = fileDict[name]
            if not fileData['ObjectIds'].has_key(uid):
                continue

            getSyntax = 'objectInfo = fileData' + fileData['ObjectIds'][uid]
            exec getSyntax
            fileList.add(name)
            objects = objectInfo.get('Objects')
            if objects:
                for obj in objects.values():
                    visual = obj.get('Visual')
                    if visual:
                        model = visual.get('Model')
                        if model:
                            if type(model) is types.ListType:
                                for currModel in model:
                                    fileList.add(currModel + '.bam')

                            else:
                                fileList.add(model + '.bam')

            objects = fileData.get('Objects')
            if objects:
                for obj in objects.values():
                    visual = obj.get('Visual')
                    if visual:
                        model = visual.get('Model')
                        if model:
                            fileList.add(model + '.bam')

            if not objectInfo.has_key('File') or objectInfo.get('File') == '':
                break
                continue

        return list(fileList)

    def getObjectIslandUid(self, objUid, fileDict=None):
        if not fileDict:
            fileDict = self.fileDicts
        found = False
        curUid = objUid
        isPrivate = False
        while curUid:
            curFile = None
            for name in fileDict:
                fileData = fileDict[name]
                if not fileData['ObjectIds'].has_key(str(curUid)):
                    continue
                if fileData['Objects'].has_key(str(curUid)):
                    if fileData['Objects'][str(curUid)].get('Type') == 'Island':
                        return (str(curUid), isPrivate)
                    continue
                objData = fileData['Objects'].values()[0]['Objects']
                if objData.has_key(str(curUid)):
                    if curUid == objUid:
                        if objData[str(curUid)].get('Private Status') == 'Private Only':
                            isPrivate = True
                    if objData[str(curUid)].get('Type') == 'Island':
                        return (str(curUid), isPrivate)
                curFile = fileData
                break

            if not curFile:
                return
            else:
                curUid = curFile.get('Objects', {}).keys()[0]
                if curFile['Objects'][str(curUid)].get('Type') == 'Island':
                    return (curUid, isPrivate)

        return

    def isObjectDefined(self, objUid, fileName):
        return fileName in self.fileDicts and objUid in self.fileDicts[fileName]['ObjectIds']

    def getObject(self, parentObj, key):
        data = parentObj.data['Objects'].get(key)
        if data:
            return LevelObject(key, data)
        return None

    def loadTemplateObject(self, filename, gameArea, rootTransform):
        fileData = self.openFile(filename)
        fileObjUid = fileData['Objects'].keys()[0]
        fileObj = self.getObject(LevelObject(fileObjUid, fileData), fileObjUid)
        fileObj.transform = rootTransform.compose(fileObj.transform)
        for objKey in fileObj.data.get('Objects', []):
            obj = self.getObject(fileObj, objKey)
            obj.transform = fileObj.transform.compose(obj.transform)
            self.loadObj(obj, gameArea)

    def loadObj(self, levelObj, gameArea):
        newObj = self.createObj(levelObj, gameArea)
        for objKey in levelObj.data.get('Objects', []):
            obj = self.getObject(levelObj, objKey)
            obj.transform = levelObj.transform.compose(obj.transform)
            self.loadObj(obj, gameArea)

        templates = levelObj.data.get('AdditionalData', [])
        for file in templates:
            self.loadTemplateObject(file + '.py', gameArea, levelObj.transform)

        objFile = levelObj.data.get('File')
        if objFile:
            self.registerFileObject(objFile + '.py')

    def storeNecessaryAreaData(self, areaUid, areaData):
        visTable = areaData.get('Vis Table')
        if visTable:
            self.uidVisTables[areaUid] = visTable
        adjTable = areaData.get('Adj Table')
        if adjTable:
            self.uidAdjTables[areaUid] = adjTable
        self.uidVisZoneMinimaps[areaUid] = areaData.get('VisZone Minimaps', {})
        self.uidVisZoneTunnels[areaUid] = areaData.get('Tunnel Minimaps', {})
        if areaData.get('Minimap', False):
            self.uidMinimapPrefix[areaUid] = areaData.get('Minimap Prefix', '')
        environmentName = None
        footStepSound = None
        envSettings = None
        baseObject = None
        objectData = areaData.get('Objects')
        if objectData:
            baseObject = objectData.get(areaUid)
        if baseObject:
            environmentName = baseObject.get('Environment')
            if environmentName:
                self.environmentTable[areaUid] = environmentName
            footStepSound = baseObject.get('Footstep Sound')
            if footStepSound:
                self.footstepTable[areaUid] = footStepSound
        if envSettings == None:
            envSettings = areaData.get('LevelEnvironment')
            if envSettings:
                self.uidEnvSettings[areaUid] = envSettings
        return

    def registerFileObject(self, filename):
        fileData = self.openFile(filename)
        self.fileDicts[filename] = fileData
        fileObjUid = fileData['Objects'].keys()[0]
        self.storeNecessaryAreaData(fileObjUid, fileData)
        self.fileObjs[fileObjUid] = LevelObject(fileObjUid, fileData['Objects'][fileObjUid])
        self.registerSubObj(self.fileObjs[fileObjUid])

    def registerSubObj(self, levelObj):
        for objKey in levelObj.data.get('Objects', []):
            obj = self.getObject(levelObj, objKey)
            self.registerSubObj(obj)

        objFile = levelObj.data.get('File')
        if objFile:
            self.registerFileObject(objFile + '.py')

    def loadFileObjFromUid(self, uniqueId, gameArea, transformParent):
        levelObj = self.fileObjs[uniqueId]
        looseNum = len(levelObj.data.get('Objects', []))
        base.loadingScreen.beginStep('LoadingObjects', looseNum, 80)
        for objKey in levelObj.data.get('Objects', []):
            obj = self.getObject(levelObj, objKey)
            self.loadObj(obj, gameArea)
            base.loadingScreen.tick()

        base.loadingScreen.endStep('LoadingObjects')
        templates = levelObj.data.get('AdditionalData', [])
        for file in templates:
            self.loadTemplateObject(file + '.py', gameArea, levelObj.transform)

        self.storeNecessaryAreaData(uniqueId, levelObj.data)

    def getTodSettingsByUid(self, uniqueId):
        return self.uidTodSettings.get(uniqueId, None)

    def getEnvSettingsByUid(self, uniqueId):
        return self.uidEnvSettings.get(uniqueId, None)
