from pandac.PandaModules import TransformState
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import report
from pirates.pirate import AvatarType, AvatarTypes
from pirates.piratesbase import PiratesGlobals
from pirates.quest import QuestConstants
from pirates.piratesbase import TeamUtils
from pirates.world import LocationConstants
import types
import copy

class QuestGoal():
    Type_Uid = 0
    Type_Custom = 1
    LEVEL_IDX = 0
    TYPE_IDX = 1
    FACTION_IDX = 2
    HULL_IDX = 3
    FLAGSHIP_IDX = 4
    LOCATION_IDX = 5
    MAX_IDX = 6
    GOAL_TYPE_DINGHY = 'dinghy'
    GOAL_TYPE_SHIP = 'ship'
    GOAL_TYPES_OCEAN = [GOAL_TYPE_SHIP]

    def __init__(self, typeInfo):
        self.__goalDataStr = None
        if typeInfo == None:
            self.__goalType = types.ListType
            self.__goalData = []
            return
        if type(typeInfo) == types.StringType:
            typeInfo = [typeInfo]
        self.__goalData = typeInfo
        self.__goalType = type(self.__goalData)
        return

    def getType(self):
        if self.__goalType == types.DictType:
            return self.Type_Custom
        return self.Type_Uid

    def getTargetType(self):
        if self.__goalType == types.DictType:
            return self.__goalData.get(self.TYPE_IDX)
        return (0, 0, 0, 0)

    def getTargetTypeOnlyOnOcean(self):
        return self.getTargetType() in self.GOAL_TYPES_OCEAN

    def getLocation(self):
        if self.__goalType == types.DictType:
            return self.__goalData.get(self.LOCATION_IDX)
        return None

    def compareTo(self, object, goalOwner=None):
        if self.__goalType == types.DictType:
            goalLevel = self.__goalData.get(self.LEVEL_IDX, 0)
            if goalLevel > 0 and goalLevel > object.getLevel():
                return 1
            hasIsShip = hasattr(object, '_isShip')
            if game.process == 'ai' and not hasIsShip:
                return -1
            goalLocation = self.__goalData.get(self.LOCATION_IDX, None)
            objectLocation = object.getParentObj()
            if goalLocation and objectLocation and hasattr(objectLocation, 'getUniqueId') and not goalLocation == LocationConstants.LocationIds.ANY_LOCATION and not LocationConstants.isInArea(goalLocation, objectLocation.getUniqueId())[0]:
                return 1
            if hasIsShip and object._isShip():
                if self.getTargetTypeOnlyOnOcean():
                    goalFaction = self.__goalData.get(self.FACTION_IDX, None)
                    if goalFaction:
                        isEnemy = False
                        if goalOwner:
                            isEnemy = TeamUtils.friendOrFoe(goalOwner, object) == PiratesGlobals.ENEMY
                        objFaction = object.getFaction()
                        if goalFaction != None and objFaction != None and goalFaction.getFaction() != objFaction.getFaction() or not isEnemy:
                            return 1
                    goalHull = self.__goalData.get(self.HULL_IDX, None)
                    if goalHull != None:
                        shipClassList = QuestConstants.getShipList(goalHull)
                        if shipClassList == None:
                            shipClassList = [
                             goalHull]
                        if object.shipClass not in shipClassList:
                            return 1
                    goalFlagship = self.__goalData.get(self.FLAGSHIP_IDX, False)
                    if goalFlagship != object.isFlagship:
                        return 1
                    if object.getTeam() == PiratesGlobals.PLAYER_TEAM:
                        return 1
                    return 0
            elif not self.getTargetTypeOnlyOnOcean():
                if self.__goalData.get(self.TYPE_IDX) == AvatarTypes.AnyAvatar and goalOwner:
                    if TeamUtils.friendOrFoe(goalOwner, object) == PiratesGlobals.ENEMY:
                        return 0
                elif object.getAvatarType().isA(self.__goalData.get(self.TYPE_IDX)):
                    return 0
        elif self.__goalData and object.getUniqueId() in self.__goalData:
            return 0
        return 1

    def getGoalIds(self, uidMgr=None, all=True):
        if all:
            results = [
             (0, '')]
        else:
            results = ''
        if self.__goalType == types.ListType:
            if all:
                uidData = self.__goalData
            else:
                uidData = self.__goalData[:1]
            if uidMgr:
                results = zip(map(lambda x: uidMgr.getDoId(x, None), uidData), uidData)
            elif len(uidData) == 0:
                results = ''
            else:
                results = uidData[0]
        return results

    def _asString(self):
        if self.__goalDataStr != None:
            return self.__goalDataStr
        if self.__goalData == None:
            resultStr = ''
        if self.__goalType == types.ListType:
            resultStr = str(self.__goalData)
        else:
            strRep = ''
            for currField in range(self.MAX_IDX):
                strRep += str(self.__goalData.get(currField, None))
                strRep += '-'

            resultStr = strRep
        self.__goalDataStr = resultStr
        return resultStr

    def __repr__(self):
        return self._asString()

    def __str__(self):
        return self._asString()

    def __cmp__(self, other):
        strRep = self._asString()
        otherStrRep = other._asString()
        if strRep < otherStrRep:
            return -1
        elif strRep > otherStrRep:
            return 1
        return 0

    def __hash__(self):
        result = hash(self._asString())
        return result


class QuestStep():
    STNPC = 1
    STItem = 2
    STArea = 3
    STTunnel = 4
    STExteriorDoor = 5
    STInteriorDoor = 6
    STDinghy = 7
    STShip = 8
    STNPCArea = 9
    STQuestNode = 10
    STNPCEnemy = 11
    STQuestProp = 12
    NullStep = None
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestStep')

    def __init__(self, originDoId, stepDoId, stepType, posH=(0, 0, 0, 0), islandUid='', targetAreaUid='', targetAvatarType=None, nodeSizes=(0, 0), nearOffset=(0, 0, 0), nearVis=(0, 0, 0)):
        self.originDoId = originDoId
        self.stepDoId = stepDoId
        self.stepType = stepType
        self.posH = posH
        self.islandUid = islandUid
        self.targetAreaUid = targetAreaUid
        self.targetAvatarType = targetAvatarType
        self.nodeSizes = nodeSizes
        self.nearOffset = nearOffset
        self.nearVis = nearVis

    def __repr__(self):
        return 'QuestStep(%d, %d, %d, %s, %s, %s, %s, %s, %s, %s)' % (self.getOriginDoId(), self.getStepDoId(), self.getStepType(), `(self.getPosH())`, self.getIsland(), self.getTargetArea(), self.targetAvatarType, self.nodeSizes, self.nearOffset, self.nearVis)

    def __cmp__(self, other):
        return not isinstance(other, QuestStep) or cmp(self.originDoId, other.originDoId) or cmp(self.stepDoId, other.stepDoId) or cmp(self.stepType, other.stepType) or cmp(self.posH, other.posH) or cmp(self.islandUid, other.islandUid) or cmp(self.targetAreaUid, other.targetAreaUid) or cmp(self.targetAvatarType, other.targetAvatarType) or cmp(self.nodeSizes, other.nodeSizes) or cmp(self.nearOffset, other.nearOffset) or cmp(self.nearVis, other.nearVis)

    def compareTarget(self, other):
        try:
            return not isinstance(other, QuestStep) or cmp(self.originDoId, other.originDoId) or cmp(self.stepDoId, other.stepDoId) or cmp(self.stepType, other.stepType) or cmp(self.islandId, other.islandId) or cmp(self.targetAreaId, other.targetAreaId) or cmp(self.targetAvatarType, other.targetAvatarType) or cmp(self.nodeSizes, other.nodeSizes) or cmp(self.nearOffset, other.nearOffset) or cmp(self.nearVis, other.nearVis)
        except:
            self.notify.warning('error encountered when comparing queststeps %s and %s' % (self, other))
            return 0

    def getOriginDoId(self):
        return self.originDoId

    def getStepDoId(self):
        return self.stepDoId

    def getStepType(self):
        return self.stepType

    def getPosH(self):
        return self.posH

    def setIsland(self, islandUid=''):
        self.islandUid = islandUid

    def getIsland(self):
        return self.islandUid

    def setTargetArea(self, targetUid=''):
        self.targetAreaUid = targetUid

    def getTargetArea(self):
        return self.targetAreaUid

    def getNodeSizes(self):
        return self.nodeSizes

    def getNearOffset(self):
        return self.nearOffset

    def getNearVis(self):
        return self.nearVis

    @staticmethod
    def getNullStep():
        if QuestStep.NullStep:
            pass
        else:
            QuestStep.NullStep = QuestStep(0, 0, 0)
        return QuestStep.NullStep

    def showIndicator(self):
        targetLocation = self.getTargetArea()
        parentObj = localAvatar.getParentObj()
        if config.GetBool('dynamic-rayoflight-area-only', True) and parentObj and hasattr(parentObj, 'uniqueId') and parentObj.uniqueId == targetLocation:
            return False
        return True


class QuestPath():
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestPath')

    def __init__(self, air):
        self.world = None
        self.posH = (0, 0, 0, 0)
        self.questSteps = {}
        self.islandStep = None
        self.islandDoId = None
        self.preferredStepUids = set()
        if __dev__:
            pass
        return

    def delete(self):
        self.islandDoId = None
        self.islandStep = None
        self.questSteps = {}
        self.world = None
        return

    def setWorld(self, world):
        self.world = world

    def setQuestStepPosH(self, x, y, z, h):
        self.posH = (
         x, y, z, h)

    def getIslandDoId(self):
        if self.islandDoId:
            pass
        elif self._isIsland():
            self.islandDoId = self.doId
        return self.islandDoId

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def getQuestStepIsland(self):
        if self._isIsland():
            return QuestStep(0, self.getIslandDoId(), self._getQuestStepType())

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def getQuestStep(self, questDestUid, islandDoId, avId):
        if not self.getIslandDoId():
            self.getExitIslandStep()
        questIslandDoId = islandDoId
        questIsland = None
        isPrivate = False
        goalType = questDestUid.getType()
        if goalType != QuestGoal.Type_Custom:
            if islandDoId == None:
                questIslandDoId = self.world.getObjectIslandDoId(questDestUid)
            isPrivate = self.world.getObjectIsPrivate(questDestUid)
            if not questIslandDoId:
                return
            questIsland = self.air.doId2do.get(questIslandDoId)
            if not questIsland:
                return
        if questIslandDoId or goalType == QuestGoal.Type_Custom:
            if (self.getIslandDoId() == questIslandDoId or goalType == QuestGoal.Type_Custom) and not questDestUid.getTargetTypeOnlyOnOcean():
                islandObj = self.getIsland()
                if islandObj and goalType == QuestGoal.Type_Custom and islandObj.notHasQuestGoal(questDestUid):
                    return QuestStep.NullStep
                islandSearchResult = self.getIntoIslandStep(questDestUid, isPrivate, avId)
                if islandObj:
                    if islandSearchResult == None or islandSearchResult == QuestStep.NullStep:
                        islandObj.setNotHasQuestGoal(questDestUid)
                    else:
                        searchArea = self._checkNeedDinghyStep(avId, islandSearchResult.getOriginDoId())
                        if searchArea:
                            return self._getLocalDinghy(avId, questDestUid, searchArea=searchArea)
                return islandSearchResult
            else:
                step = self.getExitIslandStep()
                if step:
                    return step
                else:
                    dinghyStep = self._getLocalDinghy(avId, questDestUid)
                    if dinghyStep:
                        return dinghyStep
                    else:
                        destIsland = self.air.doId2do.get(questIslandDoId)
                        if destIsland:
                            return QuestStep(self.doId, questIslandDoId, questIsland._getQuestStepType())
        return

    def _checkNeedDinghyStep(self, avId, goalOriginId):
        avObj = self.air.doId2do.get(avId)
        if avObj:
            avParent = avObj.getParentObj()
            avIsland = avParent.getIsland()
            if avParent is avIsland:
                if goalOriginId != avParent.doId:
                    return avParent
        return None

    def _getLocalDinghy(self, avId, questDestUid, searchArea=None):
        avObj = self.air.doId2do.get(avId)
        if avObj:
            avZone = avObj.zoneId
            if searchArea == None:
                searchArea = self
            dinghyId = self.world.queryGoalByObjectType(QuestGoal.GOAL_TYPE_DINGHY, avObj, questDestUid, searchArea)
            dinghyObj = self.air.doId2do.get(dinghyId)
            if dinghyObj:
                dinghyPos = dinghyObj.getPos(searchArea)
                return QuestStep(searchArea.doId, dinghyId, dinghyObj._getQuestStepType(), posH=(dinghyPos[0], dinghyPos[1], dinghyPos[2], dinghyObj.getH()), islandUid=self.getUniqueId())
        return

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def getExitIslandStep(self):
        if self._isIsland() or self._isShip():
            return None
        if not self.islandStep:
            self._getIslandPath([], [], {})
        returnStep = copy.copy(self.islandStep)
        return returnStep

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def getIntoIslandStep(self, questDestUid, isPrivate, avId=None):
        questStep = self.questSteps.get(questDestUid)
        if not questStep or config.GetBool('cache-quest-step', 1) == 0:
            path = self._getQuestPath(questDestUid, isPrivate, [], [], {}, avId)
            if path:
                targetAreaUid = self.air.doId2do[path[len(path) - 1]].getParentObj().uniqueId
                questStep = self.questSteps.get(questDestUid)
                if questStep:
                    questStep.setTargetArea(targetAreaUid)
        if questDestUid.getType() == QuestGoal.Type_Custom:
            self.questSteps.pop(questDestUid, None)
        return questStep

    def getOntoOceanStep(self, questDestUid, avId):
        questIds = self.world.queryGoal(questDestUid, self, avId)
        for questDoId, questUid in questIds:
            questGoalObj = self.air.doId2do.get(questDoId)
            if questGoalObj:
                questDest = QuestStep(self.world.worldGrid.doId, questDoId, questGoalObj._getQuestStepType(), questGoalObj._getQuestStepPosH())
                avObj = self.air.doId2do.get(avId)
                if avObj:
                    avObj.setQuestGoalDoId(questGoalObj)
                return questDest

        return QuestStep.NullStep

    def _getExitLinkDoIds(self, questGoalUid):
        if __dev__:
            pass
        return []

    def _getQuestStepType(self):
        if __dev__:
            pass
        return 0

    def _isIsland(self):
        if __dev__:
            pass
        return False

    def _isShip(self):
        return False

    def _getQuestStepPosH(self):
        return self.posH

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def _getIslandPath(self, alreadyVisited, needToVisit, pathDict):
        islandPath = []
        needToStore = False
        if not islandPath:
            if self._isIsland():
                islandPath = alreadyVisited + [self.doId]
        if islandPath:
            finalPath = [
             islandPath[-1]]
            next = pathDict.get(finalPath[-1])
            while next:
                finalPath.append(next)
                next = pathDict.get(finalPath[-1])

            finalPath.reverse()
        else:
            exitLinks = [ linkDoId for linkDoId in self._getExitLinkDoIds(None) if linkDoId not in alreadyVisited if linkDoId not in needToVisit ]
            for link in exitLinks:
                pathDict[link] = self.doId

            needToVisit += exitLinks
            if needToVisit:
                nextDoId = needToVisit.pop(0)
                nextStep = self.air.doId2do[nextDoId]
                finalPath = nextStep._getIslandPath(alreadyVisited + [self.doId], needToVisit, pathDict)
                needToStore = True
            else:
                finalPath = []
        if needToStore and self.doId in finalPath:
            self._storeIslandStep(finalPath)
        return finalPath

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def _storeIslandStep(self, path):
        stepDoId = path[path.index(self.doId) + 1]
        step = self.air.doId2do[stepDoId]
        if __dev__:
            pass
        self.islandStep = QuestStep(self.doId, stepDoId, step._getQuestStepType(), step._getQuestStepPosH())
        self.islandDoId = step.islandDoId

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def _getQuestPath(self, questDestUid, isPrivate, alreadyVisited, needToVisit, pathDict, avId):
        questDest = None
        questPath = []
        needToStore = False
        if not isPrivate:
            if not questPath:
                questIds = self.world.queryGoal(questDestUid, self, avId)
                for questDoId, questUid in questIds:
                    questGoalObj = self.air.doId2do.get(questDoId)
                    if questGoalObj:
                        if questGoalObj.getParentObj() is self or questGoalObj is self:
                            if questDoId != self.doId:
                                pathDict.setdefault(questDoId, self.doId)
                                newIds = [self.doId, questDoId]
                            else:
                                newIds = [
                                 self.doId]
                            questPath = alreadyVisited + [self.doId, questDoId]
                            questDest = QuestStep(self.doId, questDoId, questGoalObj._getQuestStepType(), questGoalObj._getQuestStepPosH())
                            needToStore = True
                            avObj = self.air.doId2do.get(avId)
                            if avObj:
                                avObj.setQuestGoalDoId(questGoalObj)
                            break
                    elif questDoId != None:
                        pass
                    if questDestUid.getType() != QuestGoal.Type_Custom and questUid:
                        try:
                            objInfo = self.air.worldCreator.getObjectDataFromFileByUid(questUid, self.getFileName())
                            if objInfo:
                                if objInfo.get('Type') == 'Dinghy':
                                    pos = objInfo['Pos']
                                    hpr = objInfo['Hpr']
                                    questPath = alreadyVisited + [self.doId]
                                    questDest = QuestStep(self.doId, 0, QuestStep.STQuestNode, (
                                     pos[0], pos[1], pos[2], hpr[0]))
                                    needToStore = True
                                    break
                                elif objInfo.get('Type') == 'Quest Node':
                                    pos = objInfo['Pos']
                                    nodePos = None
                                    parentUid = self.air.worldCreator.getObjectDataFromFileByUid(questUid, self.getFileName(), getParentUid=True)
                                    if parentUid:
                                        parentObj = self.world.uidMgr.justGetMeMeObject(parentUid)
                                        if parentObj:
                                            tform = TransformState.makePosHpr(parentObj.getPos(self), parentObj.getHpr(self))
                                            nodePos = tform.getMat().xformPoint(pos)
                                    if nodePos == None:
                                        nodePos = pos
                                    hpr = objInfo['Hpr']
                                    at = int(float(objInfo['At']))
                                    near = int(float(objInfo['Near']))
                                    nearOffset = (int(objInfo['NearOffsetX']), int(objInfo['NearOffsetY']), int(objInfo['NearOffsetZ']))
                                    nearVis = (
                                     int(objInfo['NearVisX']), int(objInfo['NearVisY']), int(objInfo['NearVisZ']))
                                    questPath = alreadyVisited + [self.doId]
                                    questDest = QuestStep(self.doId, 0, QuestStep.STQuestNode, (
                                     nodePos[0], nodePos[1], nodePos[2], hpr[0]), nodeSizes=[at, near], nearOffset=nearOffset, nearVis=nearVis)
                                    needToStore = True
                                    break
                                elif objInfo.get('Type') == 'Object Spawn Node':
                                    pos = objInfo['Pos']
                                    hpr = objInfo['Hpr']
                                    questPath = alreadyVisited + [self.doId]
                                    questDest = QuestStep(self.doId, 0, QuestStep.STArea, (
                                     pos[0], pos[1], pos[2], hpr[0]))
                                    needToStore = True
                                    break
                        except AttributeError:
                            pass

        elif not questPath:
            if self.air.worldCreator.isObjectDefined(questDestUid.getGoalIds(all=False), self.world.getFileName() + '.py'):
                questPath = alreadyVisited + [self.doId]
                needToStore = False
        if questPath:
            finalPath = [
             questPath[-1]]
            next = pathDict.get(finalPath[-1])
            while next:
                finalPath.append(next)
                next = pathDict.get(finalPath[-1])

            finalPath.reverse()
        else:
            exitLinks = [ linkDoId for linkDoId in self._getExitLinkDoIds(questDestUid.getGoalIds(all=False)) if linkDoId not in alreadyVisited if linkDoId not in needToVisit ]
            for link in exitLinks:
                pathDict[link] = self.doId

            needToVisit += exitLinks
            if needToVisit:
                nextDoId = needToVisit.pop(0)
                nextStep = self.air.doId2do[nextDoId]
                finalPath = nextStep._getQuestPath(questDestUid, isPrivate, alreadyVisited + [self.doId], needToVisit, pathDict, avId)
                if questDestUid.getType() == QuestGoal.Type_Custom:
                    nextStep.questSteps.pop(questDestUid, None)
                needToStore = True
            else:
                finalPath = []
                needToStore = True
            if needToStore and self.doId in finalPath:
                self._storeQuestStep(finalPath, questDestUid, questDest)
            if not finalPath:
                self._storeQuestStep(finalPath, questDestUid, questStep=QuestStep.getNullStep())
        return finalPath

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def _storeQuestStep(self, path, questDestUid, questStep=None):
        if not questStep:
            stepDoId = path[path.index(self.doId) + 1]
            step = self.air.doId2do[stepDoId]
            if __dev__:
                pass
            questStep = QuestStep(self.doId, stepDoId, step._getQuestStepType(), step._getQuestStepPosH())
        self.questSteps[questDestUid] = questStep

    def setAsPreferredStepFor(self, questGoalUid):
        self.preferredStepUids.add(questGoalUid)

    def isPreferredStep(self, questGoalUid):
        return questGoalUid in self.preferredStepUids