from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import POD, invertDict, makeTuple
from pirates.quest import QuestEvent, QuestTaskState
from pirates.piratesbase import PLocalizer
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
import string
import random
from pirates.battle import EnemyGlobals
from pirates.ship import ShipGlobals
from pirates.quest.QuestConstants import NPCIds, PropIds, getPropList, getPropType
from pirates.quest.QuestConstants import TreasureIds, getTreasureList
from pirates.quest.QuestConstants import ShipIds, getShipList
from pirates.quest import QuestReward
from pirates.quest.QuestPath import QuestGoal
from pirates.world.LocationConstants import LocationIds, getParentIsland, getLocationList, isInArea
from pirates.uberdog.UberDogGlobals import InventoryType

class QuestTaskDNA(POD):
    notify = directNotify.newCategory('QuestTaskDNA')
    DataSet = {'location': LocationIds.ANY_LOCATION,'autoTriggerInfo': tuple(),'goalLocation': None}

    def getNPCName(self, npcId):
        npcName = PLocalizer.NPCNames.get(npcId)
        if not npcName:
            npcName = PLocalizer.BossNPCNames.get(npcId, PLocalizer.DefaultTownfolkName)
        return npcName

    def getInitialTaskState(self, holder):
        return QuestTaskState.QuestTaskState(taskType=Class2DBId[self.__class__])

    def computeRewards(self, initialTaskState, holder):
        return []

    def locationMatches(self, questEvent):
        match, message = isInArea(self.getLocation(), questEvent.getLocation())
        if message:
            self.notify.warning(message)
        return match

    def getGoalUid(self, taskState=None):
        if self.getGoalLocation():
            goalUid = self.getGoalLocation()
        else:
            locationList = getLocationList(self.getLocation())
            if locationList:
                goalUid = list(locationList)
            else:
                goalUid = None
        return QuestGoal(goalUid)

    def getGoalNum(self):
        return 1

    def handleEnemyDefeat(self, questEvent, taskState):
        pass

    def handleNPCDefeat(self, questEvent, taskState):
        pass

    def handlePokerHandWon(self, questEvent, taskState):
        pass

    def handlePokerHandLost(self, questEvent, taskState):
        pass

    def handleBlackjackHandWon(self, questEvent, taskState):
        pass

    def handleTreasureOpened(self, questEvent, taskState):
        pass

    def handleContainerSearched(self, questEvent, taskState):
        pass

    def handleDockedAtPort(self, questEvent, taskState):
        pass

    def handleDeployedShip(self, questEvent, taskState):
        pass

    def handleShipDefeat(self, questEvent, taskState):
        pass

    def handleNPCVisit(self, questEvent, taskState):
        pass

    def handleNPCBribe(self, questEvent, taskState):
        pass

    def handleObjectVisit(self, questEvent, taskState):
        pass

    def handleShipPVPSpawn(self, questEvent, taskState):
        pass

    def handleShipPVPSink(self, questEvent, taskState):
        pass

    def handleShipPVPEnemyDefeat(self, questEvent, taskState):
        pass

    def handleShipPVPShipDamage(self, questEvent, taskState):
        pass

    def handleShipPVPPlayerDamage(self, questEvent, taskState):
        pass

    def handleCompletedQuestContainer(self, questEvent, taskState):
        pass

    def handlePropBurned(self, questEvent, taskState):
        pass

    def handleEnemyDefeatNearProp(self, questEvent, taskState):
        pass

    def handleNPCDefended(self, questEvent, taskState):
        pass

    def handleEnemiesDefeatedAroundProp(self, questEvent, taskState):
        pass

    def handlePotionBrewed(self, questEvent, taskState):
        pass

    def handleFishCaught(self, questEvent, taskState):
        pass

    def handlePropLooted(self, questEvent, taskState):
        pass

    def handleScrimmageRoundComplete(self, questEvent, taskState):
        pass

    def handleStart(self, avId):
        pass

    def complete(self, questEvent, taskState):
        taskState.handleProgress()

    def cutsceneWatched(self, questEvent, taskState):
        pass

    def getDescriptionText(self, state):
        raise 'derived must override'

    def getDescriptionTextBonus(self, state):
        return None

    def getTitle(self):
        raise 'derived must override'

    def getStringBefore(self):
        return random.choice(PLocalizer.QuestDefaultDialogBefore)

    def getStringDuring(self):
        return random.choice(PLocalizer.QuestDefaultDialogDuring)

    def getStringAfter(self):
        return random.choice(PLocalizer.QuestDefaultDialogAfter)

    def getSCSummaryText(self, state):
        return ''

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return ''

    def getReturnGiverIds(self):
        return None

    def getTargetInfo(self, world):
        return None

    def compileStats(self, questStatData):
        pass

    def getProgressMessage(self, taskState):
        PiratesGuiGlobals.ProgressMsgOffset = 0.3
        return (None, None)

    def getLocationStr(self):
        locationStr = ''
        location = self.getLocation()
        if location != LocationIds.ANY_LOCATION:
            locationName = PLocalizer.LocationNames.get(location)
            islandName = PLocalizer.LocationNames.get(getParentIsland(location))
            locationStr = PLocalizer.QuestTaskLocation % {'locationName': locationName}
            if islandName and locationName != islandName:
                locationStr += PLocalizer.QuestTaskIsland % {'islandName': islandName}
            elif islandName:
                locationStr = PLocalizer.QuestTaskIsland % {'islandName': islandName}
        return locationStr


class VisitTaskDNA(QuestTaskDNA):
    DataSet = {'npcId': None}

    def handleNPCVisit(self, questEvent, taskState):
        if questEvent.npcId == self.npcId:
            return True
        return False

    def handleObjectVisit(self, questEvent, taskState):
        if questEvent.objectId == self.npcId:
            return True
        return False

    def getDescriptionText(self, state):
        npcNameStr = PLocalizer.QuestTaskNpc % {'npcName': self.getNPCName(self.npcId)}
        locationStr = self.getLocationStr()
        return PLocalizer.VisitTaskDesc % {'npcName': npcNameStr,'location': locationStr}

    def getSCSummaryText(self, state):
        return PLocalizer.QuestSCFindNPC % {'npcName': self.getNPCName(self.npcId)}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsNPC % {'npcName': self.getNPCName(self.npcId)}

    def getSCHowToText(self, state):
        return ''

    def getTitle(self):
        return PLocalizer.VisitTaskTitle % self.getNPCName(self.npcId)

    def getStringAfter(self):
        return random.choice(PLocalizer.VisitTaskDefaultDialogAfter)

    def getReturnGiverIds(self):
        return makeTuple(self.npcId)

    def getTargetInfo(self, world):
        targetInfo = world.uid2doSearch(self.npcId)
        if targetInfo == None:
            return
        npcDoId = targetInfo[0]
        npcInstance = targetInfo[1]
        if npcDoId == None:
            return
        targetNpc = simbase.air.doId2do.get(npcDoId)
        if targetNpc == None:
            return
        location = targetNpc.getPos(npcInstance.worldGrid)
        object = targetNpc
        return (
         location, object.getUniqueId(), npcInstance)

    def getGoalUid(self, taskState=None):
        return QuestGoal(self.getGoalLocation() or self.getNpcId())

    def compileStats(self, questStatData):
        questStatData.incrementTasks('visitTasks')
        questStatData.incrementMisc('visits')


class GoToTaskDNA(VisitTaskDNA):
    DataSet = {'npcId': None,'containerId': None}

    def handleNPCVisit(self, questEvent, taskState):
        return False

    def handleObjectVisit(self, questEvent, taskState):
        if questEvent.objectId == self.containerId:
            return True
        return False

    def getGoalUid(self, taskState=None):
        if self.containerId:
            return QuestGoal(self.getGoalLocation() or self.containerId)
        else:
            return QuestGoal(self.getGoalLocation() or self.npcId)

    def getDescriptionText(self, state):
        locationStr = self.getLocationStr()
        if self.containerId:
            containerType = getPropType(self.containerId)
            containerName = PLocalizer.PropTypeNames[containerType][0]
            return PLocalizer.VisitPropTaskDesc % {'propName': containerName,'location': locationStr}
        else:
            npcNameStr = PLocalizer.QuestTaskNpc % {'npcName': self.getNPCName(self.npcId)}
            locationStr = self.getLocationStr()
            return PLocalizer.VisitTaskDesc % {'npcName': npcNameStr,'location': locationStr}


class RecoverAvatarItemTaskDNA(QuestTaskDNA):
    DataSet = {'item': None,'num': 1,'maxAttempts': 4,'probability': 1.0,'enemyType': AvatarTypes.AnyAvatar,'level': 0}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def handleEnemyDefeat(self, questEvent, taskState):
        if not questEvent.enemyType.isA(self.enemyType):
            return False
        if questEvent.level < self.level:
            return False
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        found = False
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        if attempts == self.maxAttempts:
            found = True
        elif attempts > self.maxAttempts:
            found = True
        elif questEvent.getRng(self.item).random() <= self.probability:
            found = True
        return found

    def complete(self, questEvent, taskState):
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        taskState.handleProgress()

    def getSCSummaryText(self, state):
        if state:
            itemsLeft = state.goal - state.progress
        else:
            itemsLeft = self.num
        if itemsLeft == 1:
            if self.level == 0:
                return PLocalizer.QuestSCRecoverItem % {'itemName': PLocalizer.QuestItemNames[self.item][0],'enemyName': self.enemyType.getStrings()[0]}
            else:
                return PLocalizer.QuestSCRecoverItemLvl % {'itemName': PLocalizer.QuestItemNames[self.item][0],'enemyName': self.enemyType.getStrings()[0],'level': self.level}
        elif self.level == 0:
            return PLocalizer.QuestSCRecoverItemNum % {'num': itemsLeft,'itemName': PLocalizer.QuestItemNames[self.item][1],'enemyName': self.enemyType.getStrings()[0]}
        else:
            return PLocalizer.QuestSCRecoverItemNumLvl % {'num': itemsLeft,'itemName': PLocalizer.QuestItemNames[self.item][1],'level': self.level,'enemyName': self.enemyType.getStrings()[0]}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsEnemy % {'enemyName': self.enemyType.getStrings()[0]}

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCHowDoIRecover % {'itemName': PLocalizer.QuestItemNames[self.item][0],'enemyName': self.enemyType.getStrings()[0]}

    def getDescriptionText(self, state):
        numStr = ''
        if self.num > 1:
            numStr = PLocalizer.QuestTaskNum % {'num': self.num}
            itemName = PLocalizer.QuestItemNames[self.item][1]
            enemyName = self.enemyType.getStrings()[1]
        else:
            itemName = PLocalizer.QuestItemNames[self.item][0]
            enemyName = self.enemyType.getStrings()[0]
        itemStr = PLocalizer.QuestTaskItem % {'itemName': itemName}
        enemyStr = PLocalizer.QuestTaskEnemy % {'enemyName': enemyName}
        levelStr = ''
        if self.level > 0:
            levelStr = PLocalizer.QuestTaskLevel % {'level': self.level}
        locationStr = self.getLocationStr()
        return PLocalizer.RecoverAvatarItemTaskDesc % {'num': numStr,'itemName': itemStr,'level': levelStr,'enemyName': enemyStr,'location': locationStr}

    def getTitle(self):
        return PLocalizer.RecoverAvatarItemTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('recoverAvatarItemTasks')
        count = self.num * int((1.0 - self.probability) * self.maxAttempts)
        if count < self.num:
            count = self.num
        questStatData.incrementEnemies(self.enemyType.getName(), count)
        questStatData.incrementMisc('totalEnemies', count)

    def getGoalNum(self):
        return self.num

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        itemName = PLocalizer.QuestItemNames[self.item][2]
        progressMsg = PLocalizer.RecoverItemProgress % (taskState.progress, taskState.goal, itemName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)

    def getGoalUid(self, taskState=None):
        result = self.getGoalLocation()
        if result:
            return QuestGoal(result)
        level = max(0, self.getLevel())
        typeInfo = {QuestGoal.LEVEL_IDX: level,QuestGoal.TYPE_IDX: self.getEnemyType(),QuestGoal.LOCATION_IDX: self.getLocation()}
        goal = QuestGoal(typeInfo)
        return goal


class RecoverNPCItemTaskDNA(QuestTaskDNA):
    DataSet = {'item': None,'npcId': None}

    def handleNPCDefeat(self, questEvent, taskState):
        if questEvent.npcId == self.npcId:
            return True
        return False

    def getSCSummaryText(self, state):
        return PLocalizer.QuestSCDefeatEnemy % {'enemyName': self.getNPCName(self.npcId)}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsEnemy % {'enemyName': self.getNPCName(self.npcId)}

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        itemName = PLocalizer.QuestItemNames[self.item][0]
        itemStr = PLocalizer.QuestTaskItem % {'itemName': itemName}
        npcName = PLocalizer.QuestTaskEnemy % {'enemyName': self.getNPCName(self.getNpcId())}
        locationStr = self.getLocationStr()
        return PLocalizer.RecoverAvatarItemTaskDesc % {'num': '','itemName': itemStr,'level': '','enemyName': npcName,'location': locationStr}

    def getTitle(self):
        return PLocalizer.RecoverNPCItemTaskTitle % (PLocalizer.QuestItemNames[self.item][0], self.getNPCName(self.npcId))

    def getGoalUid(self, taskState=None):
        return QuestGoal(self.getNpcId())

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        itemName = PLocalizer.QuestItemNames[self.item][2]
        npcName = self.getNPCName(self.npcId)
        progressMsg = PLocalizer.RecoverItemProgress % (taskState.progress, taskState.goal, itemName)
        color = PiratesGuiGlobals.TextFG10
        return (
         progressMsg, color)


class RecoverShipItemTaskDNA(QuestTaskDNA):
    DataSet = {'item': None,'num': 1,'maxAttempts': 4,'probability': 1.0,'faction': None,'hull': None,'level': 0,'isFlagship': False,'level': 0}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def handleShipDefeat(self, questEvent, taskState):
        if self.faction is not None:
            if not questEvent.faction.isA(self.faction):
                return False
        if self.hull is not None:
            shipClassList = getShipList(self.hull)
            if shipClassList == None:
                shipClassList = [
                 self.hull]
            if questEvent.hull not in shipClassList:
                return False
        if self.level > 0:
            if questEvent.level < self.level:
                return False
        if self.isFlagship == True and questEvent.isFlagship == False:
            return False
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        found = False
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        if attempts == self.maxAttempts:
            found = True
        elif attempts > self.maxAttempts:
            found = True
        elif questEvent.getRng(self.item).random() <= self.probability:
            found = True
        return found

    def complete(self, questEvent, taskState):
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        taskState.handleProgress()

    def getSCSummaryText(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if state:
            itemsLeft = state.goal - state.progress
        else:
            itemsLeft = self.num
        if itemsLeft == 1:
            if self.faction is None or self.faction == AvatarTypes.AnyShip:
                if shipType:
                    return PLocalizer.QuestSCRecoverShipItemShip % {'itemName': PLocalizer.QuestItemNames[self.item][0],'shipType': shipType}
                else:
                    return PLocalizer.QuestSCRecoverShipItem % {'itemName': PLocalizer.QuestItemNames[self.item][0]}
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
                if shipType:
                    return PLocalizer.QuestSCRecoverFactionShipItemShip % {'itemName': PLocalizer.QuestItemNames[self.item][0],'faction': faction,'shipType': shipType}
                else:
                    return PLocalizer.QuestSCRecoverFactionShipItem % {'itemName': PLocalizer.QuestItemNames[self.item][0],'faction': faction}
        elif self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                return PLocalizer.QuestSCRecoverShipItemNumShip % {'num': itemsLeft,'itemName': PLocalizer.QuestItemNames[self.item][1],'shipType': shipType}
            else:
                return PLocalizer.QuestSCRecoverShipItemNum % {'num': itemsLeft,'itemName': PLocalizer.QuestItemNames[self.item][1]}
        else:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
            if shipType:
                return PLocalizer.QuestSCRecoverFactionShipItemNumShip % {'num': itemsLeft,'itemName': PLocalizer.QuestItemNames[self.item][1],'faction': faction,'shipType': shipType}
            else:
                return PLocalizer.QuestSCRecoverFactionShipItemNum % {'num': itemsLeft,'itemName': PLocalizer.QuestItemNames[self.item][1],'faction': faction}
        return

    def getSCWhereIsText(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                return PLocalizer.QuestSCWhereIsShip % {'shipType': shipType}
            else:
                return ''
        elif shipType:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
            return PLocalizer.QuestSCWhereIsFactionShip % {'shipType': shipType,'faction': faction}
        else:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
            return PLocalizer.QuestSCWhereIsFaction % {'faction': faction}
        return

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCHowDoIRecoverShipItem % {'itemName': PLocalizer.QuestItemNames[self.item][0]}

    def getDescriptionText(self, state):
        numStr = ''
        if self.num > 1:
            numStr = PLocalizer.QuestTaskNum % {'num': self.num}
            itemName = PLocalizer.QuestItemNames[self.item][1]
        else:
            itemName = PLocalizer.QuestItemNames[self.item][0]
        itemStr = PLocalizer.QuestTaskItem % {'itemName': itemName}
        levelStr = ''
        if self.level > 0:
            levelStr = PLocalizer.QuestTaskLevel % {'level': self.level}
        factionStr = ''
        faction = ''
        if self.faction and self.faction != AvatarTypes.AnyShip:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][0]
            factionStr = PLocalizer.QuestTaskFaction % {'factionName': faction}
        shipStr = ''
        shipType = ''
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
            shipStr = PLocalizer.QuestTaskEnemy % {'enemyName': shipType}
        arguments = {'num': numStr,'itemName': itemStr,'level': levelStr,'faction': factionStr,'shipName': shipStr}
        if self.num > 1:
            return PLocalizer.RecoverShipItemTaskDescPL % arguments
        if PLocalizer.requiresAnIndefiniteArticle(stringList=[levelStr, faction, shipType]):
            return PLocalizer.RecoverShipItemTaskDescSn % arguments
        return PLocalizer.RecoverShipItemTaskDescS % arguments

    def getTitle(self):
        return PLocalizer.RecoverShipItemTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('recoverShipItemTasks')
        count = self.num * int((1.0 - self.probability) * self.maxAttempts)
        if count < self.num:
            count = self.num
        if self.faction:
            questStatData.incrementEnemies(self.faction.getName() + '-ship', count)
        questStatData.incrementMisc('totalShips', count)

    def getGoalNum(self):
        return self.num

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        itemName = PLocalizer.QuestItemNames[self.item][2]
        progressMsg = PLocalizer.RecoverItemProgress % (taskState.progress, taskState.goal, itemName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)

    def getGoalUid(self, taskState=None):
        result = self.getGoalLocation()
        if result:
            return QuestGoal(result)
        level = max(0, self.getLevel())
        typeInfo = {QuestGoal.LEVEL_IDX: level,QuestGoal.TYPE_IDX: 'ship',QuestGoal.FACTION_IDX: self.getFaction(),QuestGoal.HULL_IDX: self.getHull(),QuestGoal.FLAGSHIP_IDX: self.getIsFlagship(),QuestGoal.LOCATION_IDX: self.getLocation()}
        goal = QuestGoal(typeInfo)
        return goal


class RecoverContainerItemTaskDNA(QuestTaskDNA):
    DataSet = {'containerId': PropIds.ANY_PROP,'item': None,'num': 1,'maxAttempts': 4,'probability': 1.0}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def handleContainerSearched(self, questEvent, taskState):
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        allowedToSearch = taskState.searchedContainer(questEvent.containerId)
        if not allowedToSearch:
            return False
        containerMatches = False
        if self.containerId != PropIds.ANY_PROP:
            propList = getPropList(self.containerId)
            if propList:
                for prop in propList:
                    if prop == questEvent.containerId:
                        containerMatches = True

            elif self.containerId == questEvent.containerId:
                containerMatches = True
        else:
            containerMatches = True
        if not containerMatches:
            return False
        found = False
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        if attempts == self.maxAttempts:
            found = True
        elif attempts > self.maxAttempts:
            found = True
        elif questEvent.getRng(self.item).random() <= self.probability:
            found = True
        return found

    def complete(self, questEvent, taskState):
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        taskState.handleProgress()

    def getSCSummaryText(self, state):
        if state:
            itemsLeft = state.goal - state.progress
        else:
            itemsLeft = self.num
        if itemsLeft == 1:
            return PLocalizer.QuestSCContainerItem % {'itemName': PLocalizer.QuestItemNames[self.item][0]}
        else:
            return PLocalizer.QuestSCContainerItemNum % {'num': itemsLeft,'itemName': PLocalizer.QuestItemNames[self.item][1]}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsContainers

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCFindHiddenContainer

    def getDescriptionText(self, state):
        containerType = getPropType(self.containerId)
        numStr = ''
        if self.num > 1:
            numStr = PLocalizer.QuestTaskNum % {'num': self.num}
            itemName = PLocalizer.QuestItemNames[self.item][1]
            containerName = PLocalizer.PropTypeNames[containerType][1]
        else:
            itemName = PLocalizer.QuestItemNames[self.item][0]
            containerName = PLocalizer.PropTypeNames[containerType][0]
        itemNameStr = PLocalizer.QuestTaskItem % {'itemName': itemName}
        containerStr = PLocalizer.QuestTaskContainer % {'containerName': containerName}
        locationStr = self.getLocationStr()
        return PLocalizer.RecoverContainerItemTaskDesc % {'num': numStr,'itemName': itemNameStr,'container': containerStr,'location': locationStr}

    def getTitle(self):
        return PLocalizer.RecoverContainerItemTaskTitle

    def getGoalUid(self, taskState=None):
        if self.getGoalLocation():
            goalUid = self.getGoalLocation()
        else:
            locationList = getLocationList(self.getLocation())
            if locationList:
                goalUid = list(locationList)
            else:
                goalUid = self.getContainerId()
        return QuestGoal(goalUid)

    def compileStats(self, questStatData):
        questStatData.incrementTasks('recoverContainerItemTasks')
        count = self.num * int((1.0 - self.probability) * self.maxAttempts)
        if count < self.num:
            count = self.num
        questStatData.incrementMisc('treasures', count)

    def getGoalNum(self):
        return self.num

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        itemName = PLocalizer.QuestItemNames[self.item][2]
        progressMsg = PLocalizer.RecoverItemProgress % (taskState.progress, taskState.goal, itemName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)


class PoisonContainerTaskDNA(RecoverContainerItemTaskDNA):
    DataSet = {'containerId': PropIds.ANY_PROP,'item': None,'num': 1,'maxAttempts': 4,'probability': 1.0}

    def getTitle(self):
        return PLocalizer.PoisonContainerTaskTitle

    def getDescriptionText(self, state):
        containerType = getPropType(self.containerId)
        numStr = ''
        if self.num > 1:
            numStr = PLocalizer.QuestTaskNum % {'num': self.num}
            containerName = PLocalizer.PropTypeNames[containerType][1]
        else:
            containerName = PLocalizer.PropTypeNames[containerType][0]
        containerStr = PLocalizer.QuestTaskContainer % {'containerName': containerName}
        locationStr = self.getLocationStr()
        return PLocalizer.PoisonContainerTaskDesc % {'num': numStr,'container': containerStr,'location': locationStr}

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        containerType = getPropType(self.containerId)
        containerName = PLocalizer.PropTypeNames[containerType][1]
        progressMsg = PLocalizer.PoisonContainerProgress % (taskState.progress, taskState.goal, containerName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)


class DeliverItemTaskDNA(QuestTaskDNA):
    DataSet = {'item': None,'num': 1,'npcId': None}

    def handleNPCVisit(self, questEvent, taskState):
        if questEvent.npcId == self.npcId:
            if not taskState.progress == taskState.goal:
                return True
        return False

    def handleObjectVisit(self, questEvent, taskState):
        if questEvent.objectId == self.npcId:
            return True
        return False

    def handleDockedAtPort(self, questEvent, taskState):
        if not self.npcId and self.getLocation():
            if self.locationMatches(questEvent):
                return True
        return False

    def getSCSummaryText(self, state):
        if self.npcId:
            locationName = self.getNPCName(self.npcId)
        else:
            if self.location:
                locationName = PLocalizer.LocationNames.get(self.location)
                if locationName == None:
                    return ''
            else:
                locationName = 'ErrorLocation'
            if self.num == 1:
                return PLocalizer.QuestSCDeliverItem % {'itemName': PLocalizer.QuestItemNames[self.item][0],'location': locationName}
            return PLocalizer.QuestSCDeliverItemNum % {'num': self.num,'itemName': PLocalizer.QuestItemNames[self.item][1],'location': locationName}
        return

    def getSCWhereIsText(self, state):
        if self.npcId:
            locationName = self.getNPCName(self.npcId)
        elif self.location:
            locationName = PLocalizer.LocationNames.get(self.location)
            if locationName == None:
                locationName = 'Unknown Location'
        else:
            return ''
        return PLocalizer.QuestSCWhereIsNPC % {'npcName': locationName}

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        npcNameStr = PLocalizer.QuestTaskNpc % {'npcName': self.getNPCName(self.npcId)}
        locationStr = self.getLocationStr()
        numStr = ''
        if self.num > 1:
            numStr = PLocalizer.QuestTaskNumReg % {'num': self.num}
            itemName = PLocalizer.QuestItemNames[self.item][1]
        else:
            itemName = PLocalizer.QuestItemNames[self.item][0]
        return PLocalizer.DeliverItemTaskDesc % {'num': numStr,'itemName': itemName,'npcName': npcNameStr,'location': locationStr}

    def getTitle(self):
        return PLocalizer.DeliverItemTaskTitle

    def getGoalUid(self, taskState=None):
        return QuestGoal(self.getNpcId())

    def compileStats(self, questStatData):
        questStatData.incrementTasks('deliverItemTasks')
        questStatData.incrementMisc('visits')

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        itemName = PLocalizer.QuestItemNames[self.item][2]
        progressMsg = PLocalizer.DeliverItemProgress % (self.num, self.num, itemName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)


class SmuggleItemTaskDNA(DeliverItemTaskDNA):

    def handleDockedAtPort(self, questEvent, taskState):
        if not self.npcId and self.getLocation():
            if self.locationMatches(questEvent):
                if questEvent.getDeployLocation() and questEvent.getLocation() != questEvent.getDeployLocation():
                    return True
        return False

    def getSCSummaryText(self, state):
        if self.npcId:
            locationName = self.getNPCName(self.npcId)
        else:
            if self.location:
                locationName = PLocalizer.LocationNames.get(self.location)
                if locationName == None:
                    locationName = 'Unknown Location'
            else:
                return ''
            if self.num == 1:
                return PLocalizer.QuestSCSmuggleItem % {'itemName': PLocalizer.QuestItemNames[self.item][0],'location': locationName}
            return PLocalizer.QuestSCSmuggleItemNum % {'num': self.num,'itemName': PLocalizer.QuestItemNames[self.item][1],'location': locationName}
        return

    def getSCWhereIsText(self, state):
        if self.npcId:
            locationName = self.getNPCName(self.npcId)
        elif self.location:
            locationName = PLocalizer.LocationNames.get(self.location)
            if locationName == None:
                locationName = 'Unknown Location'
        else:
            return ''
        return PLocalizer.QuestSCWhereIsNPC % {'npcName': locationName}

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        if self.npcId:
            locationName = self.getNPCName(self.npcId)
        else:
            if self.location:
                locationName = PLocalizer.LocationNames.get(self.location)
                if locationName == None:
                    locationName = 'Unknown Location'
            else:
                locationName = 'ErrorLocation'
            if self.num == 1:
                return PLocalizer.SmuggleItemTaskDescS % {'itemName': PLocalizer.QuestItemNames[self.item][0],'location': locationName}
            return PLocalizer.SmuggleItemTaskDescP % {'num': self.num,'itemName': PLocalizer.QuestItemNames[self.item][1],'location': locationName}
        return

    def getTitle(self):
        return PLocalizer.SmuggleItemTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('smuggleItemTasks')

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        itemName = PLocalizer.QuestItemNames[self.item][2]
        progressMsg = PLocalizer.SmuggleItemProgress % (taskState.progress, taskState.goal, itemName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)


class SailToTaskDNA(QuestTaskDNA):

    def handleDockedAtPort(self, questEvent, taskState):
        if self.getLocation():
            if self.locationMatches(questEvent):
                return True
        return False

    def getSCSummaryText(self, state):
        locationName = PLocalizer.LocationNames.get(self.location)
        if locationName == None:
            locationName = 'Unknown Location'
        return PLocalizer.QuestSCSailTo % {'location': locationName}

    def getSCWhereIsText(self, state):
        locationName = PLocalizer.LocationNames.get(self.location)
        if locationName == None:
            locationName = 'Unknown Location'
        return PLocalizer.QuestSCWhereIsLocation % {'location': locationName}

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        locationName = PLocalizer.LocationNames.get(self.location)
        if locationName == None:
            locationName = 'Unknown Location'
        return PLocalizer.SailToTaskDesc % {'location': locationName}

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        locationName = PLocalizer.LocationNames.get(self.location)
        progressMsg = PLocalizer.SailToProgress % locationName
        return (
         progressMsg, PiratesGuiGlobals.TextFG10)

    def getTitle(self):
        locationName = PLocalizer.LocationNames.get(self.location)
        return PLocalizer.SailToTaskTitle % locationName

    def compileStats(self, questStatData):
        questStatData.incrementTasks('sailToTasks')

    def getGoalUid(self, taskState=None):
        return QuestGoal(self.location)


class MaroonNPCTaskDNA(QuestTaskDNA):
    DataSet = {'npcId': None}

    def handleDockedAtPort(self, questEvent, taskState):
        if self.getLocation():
            if self.locationMatches(questEvent):
                return True
        return False

    def getSCSummaryText(self, state):
        npcName = self.getNPCName(self.npcId)
        locationName = PLocalizer.LocationNames.get(self.location)
        if locationName == None:
            locationName = 'Unknown Location'
        return PLocalizer.QuestSCMaroonNPC % {'npcName': npcName,'location': locationName}

    def getSCWhereIsText(self, state):
        locationName = PLocalizer.LocationNames.get(self.location)
        if locationName == None:
            locationName = 'Unknown Location'
        return PLocalizer.QuestSCWhereIsLocation % {'location': locationName}

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCHowDoIMaroon

    def getDescriptionText(self, state):
        npcName = self.getNPCName(self.npcId)
        locationName = PLocalizer.LocationNames.get(self.location)
        if locationName == None:
            locationName = 'Unknown Location'
        return PLocalizer.MaroonNPCTaskDesc % {'npcName': npcName,'location': locationName}

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        npcName = self.getNPCName(self.npcId)
        progressMsg = PLocalizer.MaroonNPCProgress % npcName
        return (
         progressMsg, PiratesGuiGlobals.TextFG10)

    def getTitle(self):
        return PLocalizer.MaroonNPCTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('maroonNPCTasks')

    def getGoalUid(self, taskState=None):
        return QuestGoal(None)


class BribeNPCTaskDNA(QuestTaskDNA):
    DataSet = {'npcId': None,'gold': 1,'bribeType': 0}

    def handleNPCBribe(self, questEvent, taskState):
        if questEvent.npcId == self.npcId and questEvent.gold >= self.gold:
            return True
        return False

    def getSCSummaryText(self, state):
        return PLocalizer.QuestSCBribe % {'npcName': self.getNPCName(self.npcId)}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsNPC % {'npcName': self.getNPCName(self.npcId)}

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCHowToBribe

    def getDescriptionText(self, state):
        if self.bribeType == 1:
            return PLocalizer.BribeTaskAltDesc % {'toNpcName': self.getNPCName(self.npcId),'gold': self.gold}
        else:
            return PLocalizer.BribeTaskDesc % {'toNpcName': self.getNPCName(self.npcId),'gold': self.gold}

    def getTitle(self):
        return PLocalizer.BribeTaskTitle % self.getNPCName(self.npcId)

    def getStringAfter(self):
        return random.choice(PLocalizer.BribeTaskDefaultDialogAfter)

    def getReturnGiverIds(self):
        return makeTuple(self.npcId)

    def getTargetInfo(self, world):
        targetInfo = world.uid2doSearch(self.npcId)
        if targetInfo == None:
            return
        npcDoId = targetInfo[0]
        npcInstance = targetInfo[1]
        if npcDoId == None:
            return
        targetNpc = simbase.air.doId2do.get(npcDoId)
        if targetNpc == None:
            return
        location = targetNpc.getPos(npcInstance.worldGrid)
        object = targetNpc
        return (
         location, object.getUniqueId(), npcInstance)

    def getGoalUid(self, taskState=None):
        return QuestGoal(self.getNpcId())

    def compileStats(self, questStatData):
        questStatData.incrementTasks('bribeNPCTasks')
        questStatData.incrementMisc('gold', self.gold)


class PurchaseItemTaskDNA(QuestTaskDNA):
    pass


class SkeletonPokerTaskDNA(QuestTaskDNA):
    DataSet = {'gold': 1,'goldBonus': None,'containerId': PropIds.UNDEAD_POKER_TABLE}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getGold())
        state.setBonusGoal(self.getGoldBonus())
        return state

    def handlePokerHandWon(self, questEvent, taskState):
        return questEvent.gameType == PiratesGlobals.PARLORGAME_VARIATION_UNDEAD

    def handlePokerHandLost(self, questEvent, taskState):
        return questEvent.gameType == PiratesGlobals.PARLORGAME_VARIATION_UNDEAD

    def complete(self, questEvent, taskState):
        taskState.handleProgress(questEvent.gold)
        taskState.handleProgressBonus(questEvent.gold)

    def getSCSummaryText(self, state):
        return PLocalizer.QuestSCSkeletonPokerWinGold % {'gold': self.gold}

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCWinSkeletonPoker

    def getDescriptionText(self, state):
        return PLocalizer.PokerSkeletonTaskDescP % {'gold': self.gold}

    def getDescriptionTextBonus(self, state):
        if self.getGoldBonus() == None:
            return
        return PLocalizer.PokerSkeletonTaskDescB % {'gold': self.goldBonus}

    def getTitle(self):
        return PLocalizer.PokerTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('pokerTasks')
        questStatData.incrementMisc('poker-gold', self.gold)

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        progressMsg = PLocalizer.BlackjackProgress % (taskState.progress, taskState.goal)
        if self.getGoldBonus():
            progressMsg += '\n' + PLocalizer.PokerBonusProgress % (taskState.bonusProgress, taskState.bonusGoal)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)

    def getGoalUid(self, taskState=None):
        return QuestGoal(self.getContainerId())


class PokerTaskDNA(QuestTaskDNA):
    DataSet = {'gold': 1}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getGold())
        return state

    def handlePokerHandWon(self, questEvent, taskState):
        return True

    def complete(self, questEvent, taskState):
        taskState.handleProgress(questEvent.gold)

    def getSCSummaryText(self, state):
        if self.gold == 1:
            return PLocalizer.QuestSCPokerWinGold % {'gold': self.gold}
        else:
            return PLocalizer.QuestSCPokerWinGold % {'gold': self.gold}

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCWinPoker

    def getDescriptionText(self, state):
        if self.gold == 1:
            return PLocalizer.PokerTaskDescS % {'gold': self.gold}
        else:
            return PLocalizer.PokerTaskDescP % {'gold': self.gold}

    def getTitle(self):
        return PLocalizer.PokerTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('pokerTasks')
        questStatData.incrementMisc('poker-gold', self.gold)

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        progressMsg = PLocalizer.PokerProgress % (taskState.progress, taskState.goal)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)


class BlackjackTaskDNA(QuestTaskDNA):
    DataSet = {'gold': 1}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getGold())
        return state

    def handleBlackjackHandWon(self, questEvent, taskState):
        return True

    def complete(self, questEvent, taskState):
        taskState.handleProgress(questEvent.gold)

    def getSCSummaryText(self, state):
        if self.gold == 1:
            return PLocalizer.QuestSCBlackjackWinGold % {'gold': self.gold}
        else:
            return PLocalizer.QuestSCBlackjackWinGold % {'gold': self.gold}

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCWinBlackjack

    def getDescriptionText(self, state):
        if self.gold == 1:
            return PLocalizer.BlackjackTaskDescS % {'gold': self.gold}
        else:
            return PLocalizer.BlackjackTaskDescP % {'gold': self.gold}

    def getTitle(self):
        return PLocalizer.BlackjackTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('blackjackTasks')
        questStatData.incrementMisc('poker-gold', self.gold)

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        progressMsg = PLocalizer.BlackjackProgress % (taskState.progress, taskState.goal)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)


class RecoverTreasureItemTaskDNA(QuestTaskDNA):
    DataSet = {'treasureId': TreasureIds.ANY_TREASURE,'item': None,'num': 1,'maxAttempts': 4,'probability': 1.0}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def handleTreasureOpened(self, questEvent, taskState):
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False

        treasureMatches = False
        if self.treasureId != TreasureIds.ANY_TREASURE:
            treasureList = getTreasureList(self.treasureId)
            if treasureList:
                for treasure in treasureList:
                    if treasure == questEvent.treasureId:
                        treasureMatches = True
                        continue
            else:
                self.notify.warning('No treasure list for: %s' % self.treasureId)
                return False
        else:
            treasureMatches = True

        if not treasureMatches:
            return False

        found = False
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)

        if attempts == self.maxAttempts:
            found = True
        elif attempts > self.maxAttempts:
            found = True
        elif questEvent.getRng(self.item).random() <= self.probability:
            found = True

        return found

    def complete(self, questEvent, taskState):
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        taskState.handleProgress()

    def getSCSummaryText(self, state):
        if state:
            itemsLeft = state.goal - state.progress
        else:
            itemsLeft = self.num
        if itemsLeft == 1:
            return PLocalizer.QuestSCTreasureItem % {'itemName': PLocalizer.QuestItemNames[self.item][0]}
        else:
            return PLocalizer.QuestSCTreasureItemNum % {'num': itemsLeft,'itemName': PLocalizer.QuestItemNames[self.item][1]}

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCFindTreasure

    def getDescriptionText(self, state):
        numStr = ''
        if self.num > 1:
            numStr = PLocalizer.QuestTaskNum % {'num': self.num}
            itemName = PLocalizer.QuestItemNames[self.item][1]
        else:
            itemName = PLocalizer.QuestItemNames[self.item][0]
        itemStr = PLocalizer.QuestTaskItem % {'itemName': itemName}
        locationStr = self.getLocationStr()
        return PLocalizer.RecoverTreasureItemTaskDesc % {'num': numStr,'itemName': itemStr,'location': locationStr}

    def getTitle(self):
        return PLocalizer.RecoverTreasureItemTaskTitle

    def getGoalUid(self, taskState=None):
        if self.getGoalLocation():
            goalUid = self.getGoalLocation()
        else:
            locationList = getLocationList(self.getLocation())
            if locationList:
                goalUid = list(locationList)
            else:
                treasureId = self.getTreasureId()
                treasureIds = getTreasureList(treasureId)
                if treasureIds:
                    goalUid = treasureIds[0]
                else:
                    goalUid = None
        return QuestGoal(goalUid)

    def compileStats(self, questStatData):
        questStatData.incrementTasks('recoverTreasureItemTasks')
        count = self.num * int((1.0 - self.probability) * self.maxAttempts)
        if count < self.num:
            count = self.num
        questStatData.incrementMisc('treasures', count)

    def getGoalNum(self):
        return self.num

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        itemName = PLocalizer.QuestItemNames[self.item][2]
        progressMsg = PLocalizer.TreasureItemProgress % (taskState.progress, taskState.goal, itemName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)


class DefeatTaskDNA(QuestTaskDNA):
    DataSet = {'enemyType': AvatarTypes.AnyAvatar,'num': 1,'level': 0,'weaponType': None}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def _getEnemyType(self, taskState):
        return self.getEnemyType()

    def _getNum(self, taskState):
        return self.getNum()

    def _getLevel(self, taskState):
        return self.getLevel()

    def handleEnemyDefeat(self, questEvent, taskState):
        if not questEvent.enemyType.isA(self._getEnemyType(taskState)):
            return False
        if questEvent.level < self._getLevel(taskState):
            return False
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        desiredWeapon = self.weaponType
        if desiredWeapon is not None:
            if questEvent.weaponType == desiredWeapon:
                return True
            else:
                return False
        return True

    def getSCSummaryText(self, state):
        strings = self.enemyType.getStrings()
        weaponName = PLocalizer.InventoryTypeNames.get(self.weaponType)
        if state:
            enemiesLeft = state.goal - state.progress
        else:
            enemiesLeft = self.num
        if enemiesLeft == 1:
            if self.level == 0:
                if weaponName is not None:
                    return PLocalizer.QuestSCDefeatEnemyWeapon % {'enemyName': strings[0],'weaponType': weaponName}
                else:
                    return PLocalizer.QuestSCDefeatEnemy % {'enemyName': strings[0]}
            elif weaponName is not None:
                return PLocalizer.QuestSCDefeatEnemyLvlWeapon % {'enemyName': strings[0],'level': self.level,'weaponType': weaponName}
            else:
                return PLocalizer.QuestSCDefeatEnemyLvl % {'enemyName': strings[0],'level': self.level}
        elif self.level == 0:
            if weaponName is not None:
                return PLocalizer.QuestSCDefeatEnemiesWeapon % {'num': enemiesLeft,'enemyName': strings[1],'weaponType': weaponName}
            else:
                return PLocalizer.QuestSCDefeatEnemies % {'num': enemiesLeft,'enemyName': strings[1]}
        elif weaponName is not None:
            return PLocalizer.QuestSCDefeatEnemiesLvlWeapon % {'num': enemiesLeft,'level': self.level,'enemyName': strings[1],'weaponType': weaponName}
        else:
            return PLocalizer.QuestSCDefeatEnemiesLvl % {'num': enemiesLeft,'level': self.level,'enemyName': strings[1]}
        return

    def getSCWhereIsText(self, state):
        strings = self.enemyType.getStrings()
        return PLocalizer.QuestSCWhereIsEnemy % {'enemyName': strings[0]}

    def getSCSummaryText_Dynamic(self, state):
        strings = self._getEnemyType(state).getStrings()
        weaponName = PLocalizer.InventoryTypeNames.get(self.weaponType)
        if self._getNum(state) == 1:
            if self._getLevel(state) == 0:
                if weaponName is not None:
                    return PLocalizer.QuestSCDefeatEnemyWeapon % {'enemyName': strings[0],'weaponType': weaponName}
                else:
                    return PLocalizer.QuestSCDefeatEnemy % {'enemyName': strings[0]}
            elif weaponName is not None:
                return PLocalizer.QuestSCDefeatEnemyLvlWeapon % {'enemyName': strings[0],'level': self._getLevel(state),'weaponType': weaponName}
            else:
                return PLocalizer.QuestSCDefeatEnemyLvl % {'enemyName': strings[0],'level': self._getLevel(state)}
        elif self._getLevel(state) == 0:
            if weaponName is not None:
                return PLocalizer.QuestSCDefeatEnemiesWeapon % {'num': state.goal,'enemyName': strings[1],'weaponType': weaponName}
            else:
                return PLocalizer.QuestSCDefeatEnemies % {'num': state.goal,'enemyName': strings[1]}
        elif weaponName is not None:
            return PLocalizer.QuestSCDefeatEnemiesLvlWeapon % {'num': state.goal,'level': self._getLevel(state),'enemyName': strings[1],'weaponType': weaponName}
        else:
            return PLocalizer.QuestSCDefeatEnemiesLvl % {'num': state.goal,'level': self._getLevel(state),'enemyName': strings[1]}
        return

    def getSCWhereIsText_Dynamic(self, state):
        strings = self._getEnemyType(state).getStrings()
        return PLocalizer.QuestSCWhereIsEnemy % {'enemyName': strings[0]}

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        strings = self._getEnemyType(state).getStrings()
        numStr = ''
        num = self._getNum(state)
        if num > 1:
            numStr = PLocalizer.QuestTaskNum % {'num': num}
            enemyNameStr = PLocalizer.QuestTaskEnemy % {'enemyName': strings[1]}
        else:
            enemyNameStr = PLocalizer.QuestTaskEnemy % {'enemyName': strings[0]}
        levelStr = ''
        level = self._getLevel(state)
        if level > 0:
            levelStr = PLocalizer.QuestTaskLevel % {'level': level}
        locationStr = self.getLocationStr()
        weaponStr = ''
        weaponName = PLocalizer.WeaponTypeNames.get(self.weaponType)
        if not weaponName:
            weaponName = PLocalizer.InventoryTypeNames.get(self.weaponType)
        if weaponName is not None:
            weaponStr = PLocalizer.QuestTaskWeapon % {'weaponName': weaponName}
        return PLocalizer.DefeatTaskDesc % {'num': numStr,'level': levelStr,'enemyName': enemyNameStr,'location': locationStr,'weapon': weaponStr}

    def getTitle(self):
        if self.weaponType is not None:
            weaponName = PLocalizer.WeaponTypeNames.get(self.weaponType)
            if not weaponName:
                weaponName = PLocalizer.InventoryTypeNames.get(self.weaponType)
            if weaponName is not None:
                return PLocalizer.DefeatWithWeaponTaskTitle % (self.enemyType.getStrings()[1], weaponName)
        return PLocalizer.DefeatTaskTitle % self.enemyType.getStrings()[1]

    def compileStats(self, questStatData):
        questStatData.incrementTasks('recoverAvatarItemTasks')
        questStatData.incrementEnemies(self.enemyType.getName(), self.num)
        questStatData.incrementMisc('totalEnemies', self.num)

    def getGoalNum(self):
        return self.num

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        enemyTypeName = self.enemyType.getStrings()[1]
        weaponName = PLocalizer.WeaponTypeNames.get(self.weaponType)
        if not weaponName:
            weaponName = PLocalizer.InventoryTypeNames.get(self.weaponType)
        if weaponName is not None:
            progressMsg = PLocalizer.DefeatProgressWeapon % (taskState.progress, taskState.goal, enemyTypeName, weaponName)
        else:
            progressMsg = PLocalizer.DefeatProgress % (taskState.progress, taskState.goal, enemyTypeName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (
         progressMsg, color)

    def getGoalUid(self, taskState=None):
        result = self.getGoalLocation()
        if result:
            return QuestGoal(result)
        level = max(0, self.getLevel())
        typeInfo = {QuestGoal.LEVEL_IDX: level,QuestGoal.TYPE_IDX: self.getEnemyType(),QuestGoal.LOCATION_IDX: self.getLocation()}
        goal = QuestGoal(typeInfo)
        return goal


class ShipPVPDefeatTaskDNA(QuestTaskDNA):
    DataSet = {'enemyClass': None,'num': None,'damage': None,'gameType': None,'killType': None,'killWeapon': None,'damageWeapon': None,'withoutSink': False}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        if self.getNum() is not None:
            state.setGoal(self.getNum())
        else:
            state.setGoal(self.getDamage())
        return state

    def handleShipPVPPlayerDamage(self, questEvent, taskState):
        if self.getNum() is not None:
            return
        if self.enemyClass is not None:
            if self.enemyClass != questEvent.enemyClass:
                return False
        if self.gameType is not None:
            if self.gameType != questEvent.gameType:
                return False
        if self.killWeapon is not None:
            if self.killWeapon != questEvent.damageWeapon:
                return False
        if self.damageWeapon is not None:
            if self.damageWeapon != questEvent.damageWeapon:
                return False
        if self.killType is not None:
            if self.killType != PiratesGlobals.ShipPVPPirate:
                return False
        if questEvent.damage > 0:
            if questEvent.damage + taskState.progress > taskState.goal:
                taskState.progress = taskState.goal
            else:
                taskState.progress += questEvent.damage
            taskState.modified = True
        return

    def handleShipPVPShipDamage(self, questEvent, taskState):
        if self.getNum() is not None:
            return
        if self.enemyClass is not None:
            if self.enemyClass != questEvent.enemyClass:
                return False
        if self.gameType is not None:
            if self.gameType != questEvent.gameType:
                return False
        if self.killWeapon is not None:
            if self.killWeapon != questEvent.damageWeapon:
                return False
        if self.damageWeapon is not None:
            if self.damageWeapon != questEvent.damageWeapon:
                return False
        if self.killType is not None:
            if self.killType != PiratesGlobals.ShipPVPShip:
                return False
        if questEvent.damage > 0:
            if questEvent.damage + taskState.progress > taskState.goal:
                taskState.progress = taskState.goal
            else:
                taskState.progress += questEvent.damage
            taskState.modified = True
        return

    def handleShipPVPSpawn(self, questEvent, taskState):
        if self.withoutSink is True:
            taskState.progress = 0
            taskState.modified = True
        return False

    def handleShipPVPSink(self, questEvent, taskState):
        if self.withoutSink is True:
            taskState.progress = 0
            taskState.modified = True
        return False

    def handleShipPVPEnemyDefeat(self, questEvent, taskState):
        if self.enemyClass is not None:
            if self.enemyClass != questEvent.enemyClass:
                return False
        if self.gameType is not None:
            if self.gameType != questEvent.gameType:
                return False
        if self.killType is not None:
            if self.killType != questEvent.killType:
                return False
        if self.killWeapon is not None:
            if self.killWeapon != questEvent.killWeapon:
                return False
        if self.getDamage() is not None:
            return False
        return True

    def getSCSummaryText(self, state):
        return self.getDescriptionText(state)

    def getDescriptionText(self, state):
        enemyText = None
        weaponText = None
        gameTypeText = None
        killTypeText = None
        summaryText = None
        if self.enemyClass == PiratesGlobals.ShipPVPFrench:
            enemyText = PLocalizer.ShipPVPQuestFrench
        elif self.enemyClass == PiratesGlobals.ShipPVPSpanish:
            enemyText = PLocalizer.ShipPVPQuestSpanish
        if self.killType == PiratesGlobals.ShipPVPShip:
            killTypeText = PLocalizer.ShipPVPQuestKillShip
        elif self.killType == PiratesGlobals.ShipPVPPirate:
            killTypeText = PLocalizer.ShipPVPQuestKillPirate
        if self.killWeapon == PiratesGlobals.ShipPVPKillCannon:
            weaponText = PLocalizer.ShipPVPQuestUseCannon
        elif self.killWeapon == PiratesGlobals.ShipPVPKillShip:
            weaponText = PLocalizer.ShipPVPQuestUseShip
        if self.gameType == PiratesGlobals.ShipPVPSiege:
            gameTypeText = PLocalizer.ShipPVPQuestGameName
        if self.num is not None:
            if self.num == 1:
                if enemyText is not None:
                    if self.killType == PiratesGlobals.ShipPVPShip:
                        summaryText = PLocalizer.ShipPVPQuestSingleNumA % (enemyText, gameTypeText)
                    else:
                        summaryText = PLocalizer.ShipPVPQuestSingleNumB % (enemyText, gameTypeText)
                else:
                    if self.killType == PiratesGlobals.ShipPVPShip:
                        summaryText = PLocalizer.ShipPVPQuestSingleAnyNumA % gameTypeText
                    else:
                        summaryText = PLocalizer.ShipPVPQuestSingleAnyNumB % gameTypeText
                    if weaponText is not None:
                        summaryText += PLocalizer.ShipPVPQuestUsingA % weaponText
                if self.withoutSink is True:
                    summaryText += PLocalizer.ShipPVPQuestWithoutSinking
            else:
                numString = str(self.num)
                if enemyText is not None:
                    if self.killType == PiratesGlobals.ShipPVPShip:
                        summaryText = PLocalizer.ShipPVPQuestMultA % (numString, enemyText, gameTypeText)
                    else:
                        summaryText = PLocalizer.ShipPVPQuestMultB % (numString, enemyText, gameTypeText)
                else:
                    if self.killType == PiratesGlobals.ShipPVPShip:
                        summaryText = PLocalizer.ShipPVPQuestMultAnyA % (numString, gameTypeText)
                    else:
                        summaryText = PLocalizer.ShipPVPQuestMultAnyB % (numString, gameTypeText)
                    if weaponText is not None:
                        summaryText += PLocalizer.ShipPVPQuestUsingA % weaponText
                if self.withoutSink is True:
                    summaryText += PLocalizer.ShipPVPQuestWithoutSinking
        else:
            numString = str(self.damage)
            if enemyText is not None:
                if self.killType == PiratesGlobals.ShipPVPShip:
                    summaryText = PLocalizer.ShipPVPQuestDamageA % (numString, enemyText, gameTypeText)
                else:
                    summaryText = PLocalizer.ShipPVPQuestDamageB % (numString, enemyText, gameTypeText)
            else:
                if killTypeText is not None:
                    if self.killType == PiratesGlobals.ShipPVPShip:
                        summaryText = PLocalizer.ShipPVPQuestDamageAnyA % (numString, gameTypeText)
                    else:
                        summaryText = PLocalizer.ShipPVPQuestDamageAnyB % (numString, gameTypeText)
                else:
                    summaryText = PLocalizer.ShipPVPQuestDamageAnyC % (numString, gameTypeText)
                if weaponText is not None:
                    summaryText += PLocalizer.ShipPVPQuestUsingA % weaponText
                if self.withoutSink is True:
                    summaryText += PLocalizer.ShipPVPQuestWithoutSinking
        return summaryText

    def compileStats(self, questStatData):
        if self.getNum() is not None:
            questStatData.incrementEnemies(str(self.enemyClass), self.num)
            questStatData.incrementMisc('totalEnemies', self.num)
        else:
            questStatData.incrementMisc('totalDamage', self.damage)
        return

    def getGoalNum(self):
        if self.getNum() is not None:
            return self.num
        else:
            return self.damage
        return

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        enemyText = None
        gameTypeText = None
        killTypeText = None
        weaponText = None
        progressText = None
        if self.enemyClass == PiratesGlobals.ShipPVPFrench:
            enemyText = PLocalizer.ShipPVPQuestFrench
        elif self.enemyClass == PiratesGlobals.ShipPVPSpanish:
            enemyText = PLocalizer.ShipPVPQuestSpanish
        if self.gameType == PiratesGlobals.ShipPVPSiege:
            gameTypeText = PLocalizer.ShipPVPQuestGameName
        if self.killType == PiratesGlobals.ShipPVPShip:
            killTypeText = PLocalizer.ShipPVPQuestKillShipCap
        elif self.killType == PiratesGlobals.ShipPVPPirate:
            killTypeText = PLocalizer.ShipPVPQuestKillPirateCap
        if self.killWeapon == PiratesGlobals.ShipPVPKillCannon:
            weaponText = PLocalizer.ShipPVPQuestUseCannonCap
        elif self.killWeapon == PiratesGlobals.ShipPVPKillShip:
            weaponText = PLocalizer.ShipPVPQuestKillShipCap
        if self.num is not None:
            if self.num == 1:
                if enemyText is not None:
                    text = PLocalizer.ShipPVPQuestProgNumA % (enemyText, killTypeText, gameTypeText)
                else:
                    text = PLocalizer.ShipPVPQuestProgNumB % (killTypeText, gameTypeText)
            elif enemyText is not None:
                text = PLocalizer.ShipPVPQuestProgNumC % (taskState.progress, taskState.goal, enemyText, killTypeText, gameTypeText)
            else:
                text = PLocalizer.ShipPVPQuestProgNumD % (taskState.progress, taskState.goal, killTypeText, gameTypeText)
        else:
            if enemyText is not None:
                if killTypeText is not None:
                    text = PLocalizer.ShipPVPQuestProgDamA % (taskState.progress, taskState.goal, enemyText, killTypeText, gameTypeText)
                else:
                    text = PLocalizer.ShipPVPQuestProgDamB % (taskState.progress, taskState.goal, enemyText, gameTypeText)
            else:
                if killTypeText is not None:
                    text = PLocalizer.ShipPVPQuestProgDamC % (taskState.progress, taskState.goal, killTypeText, gameTypeText)
                else:
                    text = PLocalizer.ShipPVPQuestProgDamD % (taskState.progress, taskState.goal, gameTypeText)
                if weaponText is not None:
                    text += PLocalizer.ShipPVPQuestUsingACap % weaponText
            if self.withoutSink is True:
                text += PLocalizer.ShipPVPQuestWithoutSinkingCap
        return (text, PiratesGuiGlobals.TextFG10)


class DefeatNPCTaskDNA(QuestTaskDNA):
    DataSet = {'npcId': None}

    def handleNPCDefeat(self, questEvent, taskState):
        if questEvent.npcId == self.npcId:
            return True
        return False

    def getSCSummaryText(self, state):
        return PLocalizer.QuestSCDefeatEnemy % {'enemyName': self.getNPCName(self.npcId)}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsEnemy % {'enemyName': self.getNPCName(self.npcId)}

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        npcName = PLocalizer.QuestTaskEnemy % {'enemyName': self.getNPCName(self.getNpcId())}
        locationStr = self.getLocationStr()
        return PLocalizer.DefeatNPCTaskDesc % {'enemyName': npcName,'location': locationStr}

    def getTitle(self):
        return PLocalizer.DefeatNPCTaskTitle % self.getNPCName(self.npcId)

    def getGoalUid(self, taskState=None):
        return QuestGoal(self.getGoalLocation() or self.getNpcId())

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        npcName = self.getNPCName(self.npcId)
        progressMsg = PLocalizer.DefeatNPCProgress % npcName
        color = PiratesGuiGlobals.TextFG10
        return (
         progressMsg, color)


class DefeatShipTaskDNA(QuestTaskDNA):
    DataSet = {'faction': None,'hull': None,'level': 0,'isFlagship': False,'num': 1,'level': 0}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def _getFaction(self, taskState):
        return self.getFaction()

    def _getHull(self, taskState):
        return self.getHull()

    def _getIsFlagship(self, taskState):
        return self.getIsFlagship()

    def _getNum(self, taskState):
        return self.getNum()

    def handleShipDefeat(self, questEvent, taskState):
        if self._getFaction(taskState) is not None:
            if not questEvent.faction.isA(self._getFaction(taskState)):
                return False
        if self._getHull(taskState) is not None:
            tgtHull = self._getHull(taskState)
            shipClassList = getShipList(tgtHull)
            if shipClassList == None:
                shipClassList = [
                 tgtHull]
            if questEvent.hull not in shipClassList:
                return False
        if self.level > 0:
            if questEvent.level < self.level:
                return False
        if self._getIsFlagship(taskState) == True and questEvent.isFlagship == False:
            return False
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        return True

    def getSCSummaryText(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if state:
            shipsLeft = state.goal - state.progress
        else:
            shipsLeft = self.num
        if shipsLeft == 1:
            if self.faction is None or self.faction == AvatarTypes.AnyShip:
                if shipType:
                    return PLocalizer.QuestSCSinkShip % {'shipType': shipType}
                else:
                    return PLocalizer.QuestSCSink
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
                if shipType:
                    return PLocalizer.QuestSCSinkFactionShip % {'faction': faction,'shipType': shipType}
                else:
                    return PLocalizer.QuestSCSinkFaction % {'faction': faction}
        elif self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                return PLocalizer.QuestSCSinkShipNum % {'num': shipsLeft,'shipType': shipType}
            else:
                return PLocalizer.QuestSCSinkNum % {'num': shipsLeft}
        else:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
            if shipType:
                return PLocalizer.QuestSCSinkFactionNumShip % {'num': self.num,'faction': faction,'shipType': shipType}
            else:
                return PLocalizer.QuestSCSinkFactionNum % {'num': self.num,'faction': faction}
        return

    def getSCWhereIsText(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                return PLocalizer.QuestSCWhereIsShip % {'shipType': shipType}
            else:
                return ''
        elif shipType:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
            return PLocalizer.QuestSCWhereIsFactionShip % {'faction': faction,'shipType': shipType}
        else:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
            return PLocalizer.QuestSCWhereIsFaction % {'faction': faction}
        return

    def getSCSummaryText_Dynamic(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if state.goal == 1:
            if self.faction is None or self.faction == AvatarTypes.AnyShip:
                if shipType:
                    return PLocalizer.QuestSCSinkShip % {'shipType': shipType}
                else:
                    return PLocalizer.QuestSCSink
            else:
                faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
                if shipType:
                    return PLocalizer.QuestSCSinkFactionShip % {'faction': faction,'shipType': shipType}
                else:
                    return PLocalizer.QuestSCSinkFaction % {'faction': faction}
        elif self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                return PLocalizer.QuestSCSinkShipNum % {'num': state.goal,'shipType': shipType}
            else:
                return PLocalizer.QuestSCSinkNum % {'num': state.goal}
        else:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
            if shipType:
                return PLocalizer.QuestSCSinkFactionNumShip % {'num': state.goal,'faction': faction,'shipType': shipType}
            else:
                return PLocalizer.QuestSCSinkFactionNum % {'num': state.goal,'faction': faction}
        return

    def getSCWhereIsText_Dynamic(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                return PLocalizer.QuestSCWhereIsShip % {'shipType': shipType}
            else:
                return ''
        elif shipType:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
            return PLocalizer.QuestSCWhereIsFactionShip % {'faction': faction,'shipType': shipType}
        else:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
            return PLocalizer.QuestSCWhereIsFaction % {'faction': faction}
        return

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        numStr = ''
        if self.num > 1:
            numStr = PLocalizer.QuestTaskNum % {'num': self.num}
        levelStr = ''
        if self.level > 0:
            levelStr = PLocalizer.QuestTaskLevel % {'level': self.level}
        factionStr = ''
        faction = ''
        if self.faction and self.faction != AvatarTypes.AnyShip:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][0]
            factionStr = PLocalizer.QuestTaskFaction % {'factionName': faction}
        shipStr = ''
        shipType = ''
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
            shipStr = PLocalizer.QuestTaskEnemy % {'enemyName': shipType}
        arguments = {'num': numStr,'level': levelStr,'faction': factionStr,'shipName': shipStr}
        if self.num > 1:
            return PLocalizer.DefeatShipTaskDescPL % arguments
        if PLocalizer.requiresAnIndefiniteArticle(stringList=[levelStr, faction, shipType]):
            return PLocalizer.DefeatShipTaskDescSn % arguments
        return PLocalizer.DefeatShipTaskDescS % arguments

    def getTitle(self):
        return PLocalizer.DefeatShipTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('defeatShipTasks')
        if self.faction:
            questStatData.incrementEnemies(self.faction.getName() + '-ship', self.num)
        questStatData.incrementMisc('totalShips', self.num)

    def getGoalNum(self):
        return self.num

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                progressMsg = PLocalizer.DefeatShipTypeProgress % (taskState.progress, taskState.goal, shipType)
            else:
                progressMsg = PLocalizer.DefeatShipProgress % (taskState.progress, taskState.goal)
        else:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
            if shipType:
                progressMsg = PLocalizer.DefeatShipFactionTypeProgress % (taskState.progress, taskState.goal, faction, shipType)
            else:
                progressMsg = PLocalizer.DefeatShipFactionProgress % (taskState.progress, taskState.goal, faction)
            if taskState.progress == taskState.goal:
                color = PiratesGuiGlobals.TextFG10
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)

    def getGoalUid(self, taskState=None):
        result = self.getGoalLocation()
        if result:
            return QuestGoal(result)
        level = max(0, self.getLevel())
        typeInfo = {QuestGoal.LEVEL_IDX: level,QuestGoal.TYPE_IDX: 'ship',QuestGoal.FACTION_IDX: self.getFaction(),QuestGoal.HULL_IDX: self.getHull(),QuestGoal.FLAGSHIP_IDX: self.getIsFlagship(),QuestGoal.LOCATION_IDX: self.getLocation()}
        goal = QuestGoal(typeInfo)
        return goal


class RandomizedDefeatTaskDNA(DefeatTaskDNA):

    def getInitialTaskState(self, holder):
        state = DefeatTaskDNA.getInitialTaskState(self, holder)
        enemyType, num = EnemyGlobals.getRandomEncounter(holder.getLevel())
        state.setEnemyType(enemyType)
        state.setGoal(num)
        return state

    def _getEnemyType(self, taskState):
        return taskState.enemyType

    def _getNum(self, taskState):
        return taskState.goal

    def computeRewards(self, initialTaskState, holder):
        return QuestReward.GoldReward(holder.getLevel())

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        enemyTypeName = taskState.enemyType.getStrings()[1]
        progressMsg = PLocalizer.DefeatProgress % (taskState.progress, taskState.goal, enemyTypeName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (
         progressMsg, color)

    def getGoalUid(self, taskState=None):
        result = self.getGoalLocation()
        if result:
            return QuestGoal(result)
        level = max(0, self.getLevel())
        typeInfo = {QuestGoal.LEVEL_IDX: level,QuestGoal.TYPE_IDX: self._getEnemyType(taskState),QuestGoal.LOCATION_IDX: self.getLocation()}
        goal = QuestGoal(typeInfo)
        return goal


class RandomizedDefeatShipTaskDNA(DefeatShipTaskDNA):

    def getInitialTaskState(self, holder):
        state = DefeatShipTaskDNA.getInitialTaskState(self, holder)
        faction = random.choice([AvatarTypes.Navy])
        hull = random.choice([ShipGlobals.WARSHIPL1, ShipGlobals.WARSHIPL2])
        num = random.randint(2, 4)
        state.setFaction(faction)
        state.setHull(hull)
        state.setGoal(num)
        return state

    def _getFaction(self, taskState):
        return taskState.faction

    def _getHull(self, taskState):
        return taskState.hull

    def _getNum(self, taskState):
        return taskState.goal

    def computeRewards(self, initialTaskState, holder):
        return QuestReward.GoldReward(holder.getLevel())

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if taskState.faction is None or taskState.faction == AvatarTypes.AnyShip:
            if shipType:
                progressMsg = PLocalizer.DefeatShipTypeProgress % (taskState.progress, taskState.goal, shipType)
            else:
                progressMsg = PLocalizer.DefeatShipProgress % (taskState.progress, taskState.goal)
        else:
            faction = PLocalizer.FactionShipTypeNames[taskState.faction.getFaction()][1][1]
            if shipType:
                progressMsg = PLocalizer.DefeatShipFactionTypeProgress % (taskState.progress, taskState.goal, faction, shipType)
            else:
                progressMsg = PLocalizer.DefeatShipFactionProgress % (taskState.progress, taskState.goal, faction)
            if taskState.progress == taskState.goal:
                color = PiratesGuiGlobals.TextFG10
            color = PiratesGuiGlobals.TextFG8
        return (progressMsg, color)

    def getGoalUid(self, taskState=None):
        result = self.getGoalLocation()
        if result:
            return QuestGoal(result)
        level = max(0, self.getLevel())
        typeInfo = {QuestGoal.LEVEL_IDX: level,QuestGoal.TYPE_IDX: 'ship',QuestGoal.FACTION_IDX: self._getFaction(taskState),QuestGoal.HULL_IDX: self._getHull(taskState),QuestGoal.FLAGSHIP_IDX: self.getIsFlagship(),QuestGoal.LOCATION_IDX: self.getLocation()}
        goal = QuestGoal(typeInfo)
        return goal


class ViewCutsceneTaskDNA(QuestTaskDNA):
    DataSet = {'npcId': None,'cutsceneId': None,'dialogId': None,'waitEvent': None}

    def handleStart(self, avId):
        self.avId = avId
        if self.waitEvent:
            playerAv = simbase.air.doId2do[self.avId]
            self.acceptOnce(playerAv.uniqueName(self.waitEvent), self._playCutscene)
        else:
            self._playCutscene()

    def _playCutscene(self):
        playerAv = simbase.air.doId2do[self.avId]
        currWorld = playerAv.world
        npcId = currWorld.uidMgr.getDoId(self.npcId)
        npc = simbase.air.doId2do.get(npcId)
        if self.dialogId:
            npc.playDialogMovie(self.avId, self.dialogId)
        elif self.cutsceneId:
            pass

    def handleNPCVisit(self, questEvent, taskState):
        if questEvent.npcId == self.npcId:
            playerAv = simbase.air.doId2do[self.avId]
            currWorld = playerAv.world
            npcId = currWorld.uidMgr.getDoId(self.npcId)
            npc = simbase.air.doId2do.get(npcId)
            playerAv.b_setGameState('NPCInteract', localArgs=[npc, True, False])
            if self.dialogId:
                npc.playDialogMovie(questEvent.avId, self.dialogId)
            elif self.cutsceneId:
                pass
            return True
        return False

    def cutsceneWatched(self, questEvent, taskState):
        if questEvent.npcId == self.npcId:
            return True
        return False

    def getDescriptionText(self, state):
        return PLocalizer.ViewCutsceneTaskDesc % {'toNpcName': self.getNPCName(self.npcId)} + ' to view cutscene'

    def getTitle(self):
        return PLocalizer.ViewCutsceneTaskTitle % self.getNPCName(self.npcId)

    def getStringAfter(self):
        return random.choice(PLocalizer.QuestDefaultDialogBefore)

    def getReturnGiverIds(self):
        return makeTuple(self.npcId)

    def getTargetInfo(self, world):
        targetInfo = world.uid2doSearch(self.npcId)
        if targetInfo == None:
            return
        npcDoId = targetInfo[0]
        npcInstance = targetInfo[1]
        if npcDoId == None:
            return
        targetNpc = simbase.air.doId2do.get(npcDoId)
        if targetNpc == None:
            return
        location = targetNpc.getPos(npcInstance.worldGrid)
        object = targetNpc
        return (
         location, object.getUniqueId(), npcInstance)


class CaptureShipNPCTaskDNA(QuestTaskDNA):
    DataSet = {'npcId': None,'maxAttempts': 2,'probability': 1.0,'faction': None,'hull': None,'level': 0,'isFlagship': False,'level': 0}

    def handleShipDefeat(self, questEvent, taskState):
        if self.faction is not None:
            if not questEvent.faction.isA(self.faction):
                return False
        if self.hull is not None:
            shipClassList = getShipList(self.hull)
            if shipClassList == None:
                shipClassList = [
                 self.hull]
            if shipClassList:
                if questEvent.hull not in shipClassList:
                    return False
        if self.level > 0:
            if questEvent.level < self.level:
                return False
        if self.isFlagship == True and questEvent.isFlagship == False:
            return False
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        found = False
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        if attempts == self.maxAttempts:
            found = True
        elif attempts > self.maxAttempts:
            found = True
        elif questEvent.getRng(hash(self.npcId)).random() <= self.probability:
            found = True
        return found

    def complete(self, questEvent, taskState):
        attempts = taskState.getAttempts()
        if attempts < self.maxAttempts:
            attempts += 1
            taskState.setAttempts(attempts)
        taskState.handleProgress()

    def getSCSummaryText(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                return PLocalizer.QuestSCCaptureNPCShip % {'npcName': self.getNPCName(self.npcId),'shipType': shipType}
            else:
                return PLocalizer.QuestSCCaptureNPC % {'npcName': self.getNPCName(self.npcId)}
        else:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
            if shipType:
                return PLocalizer.QuestSCCaptureNPCFactionShip % {'npcName': self.getNPCName(self.npcId),'faction': faction,'shipType': shipType}
            else:
                return PLocalizer.QuestSCCaptureNPCFaction % {'npcName': self.getNPCName(self.npcId),'faction': faction}
        return

    def getSCWhereIsText(self, state):
        shipType = None
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
        if self.faction is None or self.faction == AvatarTypes.AnyShip:
            if shipType:
                return ''
            else:
                return ''
        elif shipType:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][0]
            return PLocalizer.QuestSCWhereIsFactionShip % {'faction': faction,'shipType': shipType}
        else:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][1][1]
            return PLocalizer.QuestSCWhereIsFaction % {'faction': faction}
        return

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCHowToCaptureShip

    def getDescriptionText(self, state):
        npcNameStr = PLocalizer.QuestTaskNpc % {'npcName': self.getNPCName(self.npcId)}
        levelStr = ''
        if self.level > 0:
            levelStr = PLocalizer.QuestTaskLevel % {'level': self.level}
        factionStr = ''
        faction = ''
        if self.faction and self.faction != AvatarTypes.AnyShip:
            faction = PLocalizer.FactionShipTypeNames[self.faction.getFaction()][0]
            factionStr = PLocalizer.QuestTaskFaction % {'factionName': faction}
        shipStr = ''
        shipType = ''
        if self.hull is not None:
            shipType = PLocalizer.ShipClassNames.get(self.hull)
            shipStr = PLocalizer.QuestTaskEnemy % {'enemyName': shipType}
        arguments = {'npcName': npcNameStr,'level': levelStr,'faction': factionStr,'shipName': shipStr}
        if PLocalizer.requiresAnIndefiniteArticle(stringList=[levelStr, faction, shipType]):
            return PLocalizer.CaptureShipNPCTaskDescN % arguments
        return PLocalizer.CaptureShipNPCTaskDesc % arguments

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        npcName = self.getNPCName(self.npcId)
        progressMsg = PLocalizer.CaptureNPCProgress % npcName
        return (
         progressMsg, PiratesGuiGlobals.TextFG10)

    def getTitle(self):
        return PLocalizer.CaptureShipNPCTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('captureShipNPCTasks')

    def getGoalUid(self, taskState=None):
        result = self.getGoalLocation()
        if result:
            return QuestGoal(result)
        level = max(0, self.getLevel())
        typeInfo = {QuestGoal.LEVEL_IDX: level,QuestGoal.TYPE_IDX: 'ship',QuestGoal.FACTION_IDX: self.getFaction(),QuestGoal.HULL_IDX: self.getHull(),QuestGoal.FLAGSHIP_IDX: self.getIsFlagship(),QuestGoal.LOCATION_IDX: self.getLocation()}
        goal = QuestGoal(typeInfo)
        return goal


class CaptureNPCTaskDNA(QuestTaskDNA):
    DataSet = {'npcId': None,'itemId': None}

    def getSCSummaryText(self, state):
        return PLocalizer.QuestSCCaptureNPC % {'npcName': self.getNPCName(self.npcId)}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsNPC % {'npcName': self.getNPCName(self.npcId)}

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        return PLocalizer.CaptureNPCTaskDesc % {'npcName': self.getNPCName(self.npcId)}

    def getTitle(self):
        return PLocalizer.CaptureNPCTaskTitle % self.getNPCName(self.npcId)


class BossBattleTaskDNA(QuestTaskDNA):
    DataSet = {'treasureMapId': None}

    def handleBossBattleCompleted(self, questEvent, taskState):
        if questEvent.treasureMapId == self.treasureMapId:
            return True
        return False

    def getSCSummaryText(self, state):
        tmName = PiratesGlobals.DYNAMIC_GAME_STYLE_PROPS[PiratesGlobals.GAME_TYPE_TM][self.treasureMapId]['Name']
        return PLocalizer.QuestSCBossBattleMap % {'treasureMapId': tmName}

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        tmName = PiratesGlobals.DYNAMIC_GAME_STYLE_PROPS[PiratesGlobals.GAME_TYPE_TM][self.treasureMapId]['Name']
        return PLocalizer.BossBattleTaskDesc % {'treasureMapId': tmName}

    def getTitle(self):
        tmName = PiratesGlobals.DYNAMIC_GAME_STYLE_PROPS[PiratesGlobals.GAME_TYPE_TM][self.treasureMapId]['Name']
        return PLocalizer.BossBattleTaskTitle % tmName


class DeployShipTaskDNA(QuestTaskDNA):
    DataSet = {'location': None}

    def handleDeployedShip(self, questEvent, taskState):
        if self.getLocation():
            if self.locationMatches(questEvent):
                return True
            else:
                return False
        return True

    def getSCSummaryText(self, state):
        return PLocalizer.QuestSCDeployShip

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereDoIDeployShip

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCHowDoIDeployShip

    def getDescriptionText(self, state):
        return PLocalizer.DeployShipTaskDesc

    def getTitle(self):
        return PLocalizer.DeployShipTaskTitle

    def compileStats(self, questStatData):
        questStatData.incrementTasks('deployShipTasks')


class CompleteQuestContainerTaskDNA(QuestTaskDNA):
    DataSet = {'containerIds': []}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(len(self.containerIds))
        return state

    def handleCompletedQuestContainer(self, questEvent, taskState):
        if questEvent.containerId not in self.containerIds:
            return False
        return True

    def getTitle(self):
        return ''

    def getDescriptionText(self, state):
        return ''


class BurnPropTaskDNA(QuestTaskDNA):
    DataSet = {'propType': PiratesGlobals.QUEST_PROP_AZT_IDOL_A_DESTR,'num': 1}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def _getNum(self, taskState):
        return self.getNum()

    def handlePropBurned(self, questEvent, taskState):
        if questEvent.propType == self.propType:
            return True
        return False

    def getSCSummaryText(self, state):
        return ''

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        numStr = ''
        num = self._getNum(state)
        if num > 1:
            numStr = PLocalizer.QuestTaskNum % {'num': num}
            propNameStr = PLocalizer.QuestPropNames[self.propType][1][1]
        else:
            propNameStr = PLocalizer.QuestPropNames[self.propType][1][0]
        locationStr = self.getLocationStr()
        return PLocalizer.BurnPropTaskDesc % {'num': numStr,'propName': propNameStr,'location': locationStr}

    def getTitle(self):
        return PLocalizer.BurnPropTaskTitle % PLocalizer.QuestPropNames[self.propType][1][1]


class DefeatNearPropTaskDNA(QuestTaskDNA):
    DataSet = {'enemyType': AvatarTypes.AnyAvatar,'containerId': PropIds.ANY_PROP,'num': 1,'level': 0}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def _getEnemyType(self, taskState):
        return self.getEnemyType()

    def _getNum(self, taskState):
        return self.getNum()

    def _getLevel(self, taskState):
        return self.getLevel()

    def handleEnemyDefeatNearProp(self, questEvent, taskState):
        if not questEvent.enemyType.isA(self._getEnemyType(taskState)):
            return False
        if questEvent.containerId != self.containerId:
            return False
        if questEvent.level < self._getLevel(taskState):
            return False
        if self.getLocation():
            if not self.locationMatches(questEvent):
                return False
        return True

    def getSCSummaryText(self, state):
        strings = self.enemyType.getStrings()
        if state:
            enemiesLeft = state.goal - state.progress
        else:
            enemiesLeft = self.num
        if enemiesLeft == 1:
            if self.level == 0:
                return PLocalizer.QuestSCDefeatEnemy % {'enemyName': strings[0]}
            else:
                return PLocalizer.QuestSCDefeatEnemyLvl % {'enemyName': strings[0],'level': self.level}
        elif self.level == 0:
            return PLocalizer.QuestSCDefeatEnemies % {'num': enemiesLeft,'enemyName': strings[1]}
        else:
            return PLocalizer.QuestSCDefeatEnemiesLvl % {'num': enemiesLeft,'level': self.level,'enemyName': strings[1]}

    def getSCWhereIsText(self, state):
        strings = self.enemyType.getStrings()
        return PLocalizer.QuestSCWhereIsEnemy % {'enemyName': strings[0]}

    def getSCSummaryText_Dynamic(self, state):
        strings = self._getEnemyType(state).getStrings()
        if self._getNum(state) == 1:
            if self._getLevel(state) == 0:
                return PLocalizer.QuestSCDefeatEnemy % {'enemyName': strings[0]}
            else:
                return PLocalizer.QuestSCDefeatEnemyLvl % {'enemyName': strings[0],'level': self._getLevel(state)}
        elif self._getLevel(state) == 0:
            return PLocalizer.QuestSCDefeatEnemies % {'num': state.goal,'enemyName': strings[1]}
        else:
            return PLocalizer.QuestSCDefeatEnemiesLvl % {'num': state.goal,'level': self._getLevel(state),'enemyName': strings[1]}

    def getSCWhereIsText_Dynamic(self, state):
        strings = self._getEnemyType(state).getStrings()
        return PLocalizer.QuestSCWhereIsEnemy % {'enemyName': strings[0]}

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        strings = self._getEnemyType(state).getStrings()
        numStr = ''
        num = self._getNum(state)
        if num > 1:
            numStr = PLocalizer.QuestTaskNum % {'num': num}
            enemyNameStr = PLocalizer.QuestTaskEnemy % {'enemyName': strings[1]}
        else:
            enemyNameStr = PLocalizer.QuestTaskEnemy % {'enemyName': strings[0]}
        levelStr = ''
        level = self._getLevel(state)
        if level > 0:
            levelStr = PLocalizer.QuestTaskLevel % {'level': level}
        locationStr = self.getLocationStr()
        containerType = getPropType(self.containerId)
        propNameStr = PLocalizer.PropTypeNames[containerType][0]
        return PLocalizer.DefeatNearPropTaskDesc % {'num': numStr,'level': levelStr,'enemyName': enemyNameStr,'propName': propNameStr,'location': locationStr}

    def getTitle(self):
        return PLocalizer.DefeatTaskTitle % self.enemyType.getStrings()[1]

    def compileStats(self, questStatData):
        questStatData.incrementTasks('recoverAvatarItemTasks')
        questStatData.incrementEnemies(self.enemyType.getName(), self.num)
        questStatData.incrementMisc('totalEnemies', self.num)

    def getGoalNum(self):
        return self.num

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        enemyTypeName = self.enemyType.getStrings()[1]
        progressMsg = PLocalizer.DefeatProgress % (taskState.progress, taskState.goal, enemyTypeName)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        return (
         progressMsg, color)

    def getGoalUid(self, taskState=None):
        return QuestGoal(self.containerId)


class DefendNPCTaskDNA(QuestTaskDNA):
    DataSet = {'enemyType': AvatarTypes.AnyAvatar,'containerId': PropIds.ANY_PROP}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        return state

    def _getEnemyType(self, taskState):
        return self.getEnemyType()

    def handleNPCDefended(self, questEvent, taskState):
        if questEvent.containerId == self.containerId:
            return True
        return False

    def getSCSummaryText(self, state):
        return ''

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        strings = self._getEnemyType(state).getStrings()
        enemyNameStr = PLocalizer.QuestTaskEnemy % {'enemyName': strings[0]}
        return PLocalizer.DefendNPCTaskDesc % {'enemyName': enemyNameStr}

    def getTitle(self):
        strings = self._getEnemyType(state).getStrings()
        return PLocalizer.DefendNPCTaskTitle % PLocalizer.QuestTaskEnemy % {'enemyName': strings[0]}

    def getGoalUid(self, taskState=None):
        return QuestGoal(self.containerId)


class DefeatAroundPropTaskDNA(QuestTaskDNA):
    DataSet = {'enemyType': AvatarTypes.AnyAvatar,'containerId': PropIds.ANY_PROP,'itemId': None}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        return state

    def _getEnemyType(self, taskState):
        return self.getEnemyType()

    def handleEnemiesDefeatedAroundProp(self, questEvent, taskState):
        if questEvent.containerId == self.containerId:
            return True
        return False

    def getSCSummaryText(self, state):
        return ''

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        strings = self._getEnemyType(state).getStrings()
        enemyNameStr = PLocalizer.QuestTaskEnemy % {'enemyName': strings[1]}
        containerType = getPropType(self.containerId)
        propNameStr = PLocalizer.PropTypeNames[containerType][0]
        itemName = PLocalizer.QuestItemNames[self.itemId][0]
        return PLocalizer.DefeatAroundPropTaskDesc % {'enemyName': enemyNameStr,'propName': propNameStr,'itemName': itemName}

    def getTitle(self):
        return PLocalizer.DefeatAroundPropTaskTitle % (self.enemyType.getStrings()[1], PLocalizer.PropTypeNames[getPropType(self.containerId)][0])

    def getGoalUid(self, taskState=None):
        return QuestGoal(self.containerId)

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        itemName = PLocalizer.QuestItemNames[self.itemId][0]
        progressMsg = PLocalizer.DefeatAroundPropProgress % string.capwords(itemName)
        return (
         progressMsg, PiratesGuiGlobals.TextFG10)


class FishingTaskDNA(QuestTaskDNA):
    DataSet = {'fishType': None,'fishTypeBonus': None,'num': 1,'numBonus': 1}

    def handleFishCaught(self, questEvent, taskState):
        return questEvent.fishType == self.fishType or questEvent.fishType > self.fishTypeBonus

    def complete(self, questEvent, taskState):
        if questEvent.fishType == self.fishType:
            QuestTaskDNA.complete(self, questEvent, taskState)
        else:
            taskState.handleProgressBonus()

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.num)
        state.setBonusGoal(self.numBonus)
        self.progress = 0
        return state

    def getSCSummaryText(self, state):
        fishName = PLocalizer.Collections.get(self.fishType)
        return PLocalizer.QuestSCFishing % {'fishName': fishName}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsFishingSpot

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCHowToCatchFish

    def getDescriptionText(self, state):
        fishName = PLocalizer.Collections.get(self.fishType)
        if self.fishType == InventoryType.Collection_Set11:
            if self.num == 1:
                return PLocalizer.FishingTaskDescLegendaryS % {'fishName': fishName}
            else:
                return PLocalizer.FishingTaskDescLegendaryP % {'num': self.num,'fishName': fishName}
        elif self.num == 1:
            return PLocalizer.FishingTaskDescS % {'fishName': fishName}
        else:
            return PLocalizer.FishingTaskDescP % {'num': self.num,'fishName': fishName}

    def getDescriptionTextBonus(self, state):
        if self.getFishTypeBonus() == None:
            return
        fishName = PLocalizer.Collections.get(self.fishTypeBonus)
        goalNum = self.numBonus
        if self.fishTypeBonus == InventoryType.Collection_Set11:
            if goalNum == 1:
                return PLocalizer.FishingTaskDescLegendaryS % {'fishName': fishName}
            else:
                return PLocalizer.FishingTaskDescLegendaryP % {'num': self.num,'fishName': fishName}
        elif goalNum == 1:
            return PLocalizer.FishingTaskDescS % {'fishName': fishName}
        else:
            return PLocalizer.FishingTaskDescP % {'num': goalNum,'fishName': fishName}
        return

    def getTitle(self):
        return PLocalizer.FishingTaskTitle

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        fishName = PLocalizer.Collections.get(self.fishType)
        if self.fishTypeBonus:
            fishNameBonus = PLocalizer.Collections.get(self.fishTypeBonus)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        progressMsg = PLocalizer.FishingProgress % (taskState.progress, taskState.goal, fishName)
        if self.fishTypeBonus:
            progressMsg += '\n' + PLocalizer.FishingProgressBonus % (taskState.bonusProgress, taskState.bonusGoal, fishNameBonus)
        return (progressMsg, color)


class PotionsTaskDNA(QuestTaskDNA):
    DataSet = {'potionType': None,'potionTypeBonus': None,'num': 1,'numBonus': 1}

    def handlePotionBrewed(self, questEvent, taskState):
        return questEvent.potionType in [self.potionType, self.potionTypeBonus]

    def complete(self, questEvent, taskState):
        if questEvent.potionType == self.potionType:
            QuestTaskDNA.complete(self, questEvent, taskState)
        else:
            taskState.handleProgressBonus()

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.num)
        state.setBonusGoal(self.numBonus)
        self.progress = 0
        return state

    def getSCSummaryText(self, state):
        potionName = PLocalizer.getItemName(self.potionType)
        return PLocalizer.QuestSCPotions % {'potionName': potionName}

    def getSCWhereIsText(self, state):
        return PLocalizer.QuestSCWhereIsBrewingPotionTable

    def getSCHowToText(self, state):
        return PLocalizer.QuestSCHowToBrewPotion

    def getDescriptionText(self, state):
        potionName = PLocalizer.getItemName(self.potionType)
        goalNum = self.num
        if goalNum == 1:
            return PLocalizer.PotionsTaskDescS % {'potionName': potionName}
        else:
            return PLocalizer.PotionsTaskDescP % {'num': goalNum,'potionName': potionName}

    def getDescriptionTextBonus(self, state):
        if self.getPotionTypeBonus() == None:
            return
        potionName = PLocalizer.getItemName(self.potionTypeBonus)
        goalNum = self.numBonus
        if goalNum == 1:
            return PLocalizer.PotionsTaskDescS % {'potionName': potionName}
        else:
            return PLocalizer.PotionsTaskDescP % {'num': goalNum,'potionName': potionName}
        return

    def getTitle(self):
        return PLocalizer.PotionTaskTitle

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        PiratesGuiGlobals.ProgressMsgOffset = 0.7
        potionName = PLocalizer.getItemName(self.potionType)
        if self.potionTypeBonus:
            potionNameBonus = PLocalizer.getItemName(self.potionTypeBonus)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        progressMsg = PLocalizer.PotionsProgress % (taskState.progress, taskState.goal, potionName)
        if self.potionTypeBonus:
            progressMsg += '\n' + PLocalizer.PotionsProgressBonus % (taskState.bonusProgress, taskState.bonusGoal, potionNameBonus)
        return (progressMsg, color)


class DowsingRodTaskDNA(QuestTaskDNA):
    DataSet = {'treasureId': TreasureIds.ANY_TREASURE,'item': None,'num': 1}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        holder.resetDowsingRodDistance()
        return state

    def _getNum(self, taskState):
        return self.getNum()

    def handleTreasureOpened(self, questEvent, taskState):
        treasureList = getTreasureList(self.treasureId)
        if treasureList and questEvent.treasureId == treasureList[taskState.progress]:
            return True
        return False

    def getSCSummaryText(self, state):
        return ''

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return ''

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        itemName = PLocalizer.QuestItemNames[self.item][0].title()
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
            progressMsg = PLocalizer.DowsingRodSuccessTaskProgress % itemName
        else:
            itemFound = PLocalizer.QuestDogHiddenItemNames[taskState.progress].title()
            color = PiratesGuiGlobals.TextFG8
            progressMsg = PLocalizer.DowsingRodFailTaskProgress % (itemFound, itemName)
        return (progressMsg, color)

    def getDescriptionText(self, state):
        itemName = PLocalizer.QuestItemNames[self.item][0]
        itemStr = PLocalizer.QuestTaskItem % {'itemName': itemName}
        return PLocalizer.DowsingRodTaskDesc % {'itemName': itemStr}

    def getTitle(self):
        return PLocalizer.DowsingRodTaskTitle


class LootPropTaskDNA(QuestTaskDNA):
    DataSet = {'containerId': PropIds.ANY_PROP}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        return state

    def handlePropLooted(self, questEvent, taskState):
        if questEvent.containerId == self.containerId:
            return True
        return False

    def getSCSummaryText(self, state):
        return ''

    def getSCWhereIsText(self, state):
        return ''

    def getSCHowToText(self, state):
        return ''

    def getDescriptionText(self, state):
        containerType = getPropType(self.containerId)
        propNameStr = PLocalizer.PropTypeNames[containerType][0]
        locationStr = self.getLocationStr()
        return PLocalizer.LootPropTaskDesc % {'propName': propNameStr,'location': locationStr}

    def getTitle(self):
        return PLocalizer.LootPropTaskTitle

    def getGoalUid(self, taskState=None):
        return QuestGoal(self.containerId)


class ScrimmageTaskDNA(QuestTaskDNA):
    DataSet = {'npcId': None,'num': None}

    def getInitialTaskState(self, holder):
        state = QuestTaskDNA.getInitialTaskState(self, holder)
        state.setGoal(self.getNum())
        return state

    def _getNum(self, taskState):
        return self.getNum()

    def handleScrimmageRoundComplete(self, questEvent, taskState):
        return True

    def getGoalUid(self, taskState=None):
        return QuestGoal(self.getNpcId())

    def getProgressMessage(self, taskState):
        QuestTaskDNA.getProgressMessage(self, taskState)
        if not taskState.progress:
            return (None, None)
        if taskState.progress == taskState.goal:
            color = PiratesGuiGlobals.TextFG10
        else:
            color = PiratesGuiGlobals.TextFG8
        progressMsg = PLocalizer.ScrimmageProgress % (taskState.progress, taskState.goal)
        return (
         progressMsg, color)

    def getDescriptionText(self, state):
        npcNameStr = PLocalizer.QuestTaskNpc % {'npcName': self.getNPCName(self.npcId)}
        locationStr = self.getLocationStr()
        return PLocalizer.ScrimmageTaskDesc % {'npcName': npcNameStr,'location': locationStr,'num': self.num}


DBId2Class = {0: VisitTaskDNA,1: RecoverAvatarItemTaskDNA,2: DefeatTaskDNA,3: DefeatShipTaskDNA,4: RecoverTreasureItemTaskDNA,5: ViewCutsceneTaskDNA,6: CaptureNPCTaskDNA,7: PokerTaskDNA,8: BlackjackTaskDNA,9: DeliverItemTaskDNA,10: RecoverShipItemTaskDNA,11: RecoverContainerItemTaskDNA,12: SmuggleItemTaskDNA,13: PurchaseItemTaskDNA,14: BribeNPCTaskDNA,15: DefeatNPCTaskDNA,16: MaroonNPCTaskDNA,17: CaptureShipNPCTaskDNA,18: BossBattleTaskDNA,19: RandomizedDefeatTaskDNA,20: RandomizedDefeatShipTaskDNA,21: DeployShipTaskDNA,22: ShipPVPDefeatTaskDNA,23: RecoverNPCItemTaskDNA,24: PoisonContainerTaskDNA,25: BurnPropTaskDNA,26: DefeatNearPropTaskDNA,27: DefendNPCTaskDNA,28: DefeatAroundPropTaskDNA,25: CompleteQuestContainerTaskDNA,26: BurnPropTaskDNA,27: DefeatNearPropTaskDNA,28: DefendNPCTaskDNA,29: DefeatAroundPropTaskDNA,30: DowsingRodTaskDNA,31: SailToTaskDNA,32: PotionsTaskDNA,33: FishingTaskDNA,34: SkeletonPokerTaskDNA,35: GoToTaskDNA,36: LootPropTaskDNA,37: ScrimmageTaskDNA}
Class2DBId = invertDict(DBId2Class)
RecoverItemClasses = (
 RecoverAvatarItemTaskDNA, RecoverTreasureItemTaskDNA, RecoverShipItemTaskDNA, RecoverContainerItemTaskDNA, RecoverNPCItemTaskDNA, DowsingRodTaskDNA)
