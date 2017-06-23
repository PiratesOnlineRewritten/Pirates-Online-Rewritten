from direct.directnotify import DirectNotifyGlobal
from direct.showbase import DirectObject
from pirates.quest.QuestTaskDNA import RandomizedDefeatTaskDNA
from pirates.quest.QuestTaskDNA import RandomizedDefeatShipTaskDNA
from pirates.quest import QuestLinkDB
from pirates.quest import QuestEvent

class QuestContainer(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestContainer')

    def __init__(self, name, title, av, questInt, parent=None, giverId=None, rewards=(), firstQuestId=None, description=''):
        self.name = name
        self.questInt = questInt
        if giverId:
            self.giverId = giverId
        else:
            self.giverId = ''
        if title == '':
            self.title = name
        else:
            self.title = title
        self.rewards = rewards
        self.description = description
        self.av = av
        self.parent = parent
        if not parent:
            pass
        self.firstQuestId = firstQuestId
        self.containers = []
        self.completedQuests = []
        self.goal = 0
        self.complete = False
        self.viewedInGUI = True

    def destroy(self):
        self.ignoreAll()
        self.completedQuests = []
        for container in self.containers:
            container.destroy()

        self.parent = None
        self.av = None
        return

    def getName(self):
        return self.name

    def getQuestId(self):
        return self.getName()

    def getQuestInt(self):
        return self.questInt

    def getParent(self):
        return self.parent

    def getRewards(self):
        return self.rewards

    def getTitle(self):
        return self.title

    def getDescription(self):
        return self.description

    def getGiverId(self):
        return self.giverId

    def getRewards(self):
        return self.rewards

    def getContainers(self):
        return self.containers

    def getValidContainers(self):
        return self.containers

    def getGoal(self):
        return self.goal

    def setGoal(self, goal):
        self.goal = goal

    def getComplete(self):
        return self.complete

    def isChoice(self):
        return False

    def isBranch(self):
        return False

    def addContainer(self, container):
        self.containers.append(container)

    def hasQuest(self, questId):
        for container in self.containers:
            if container.getName() == questId or container.hasQuest(questId):
                return True

        return False

    def linkQuest(self, quest):
        for container in self.containers:
            if container.linkQuest(quest):
                return True

        return False

    def unlinkQuest(self, questId):
        if not self.hasQuest(questId):
            self.notify.warning("tried to unlink quest: %s I don't have" % questId)
            return False
        for container in self.containers:
            if container.unlinkQuest(questId):
                return True

        return False

    def getFilteredContainers(self):
        containerList = self.getContainers()
        filteredContainerList = []
        currIndex = 0
        firstQuestId = self.getFirstQuestId()
        for i in range(len(containerList)):
            if containerList[i].getName() == firstQuestId:
                currIndex = i
                break

        while currIndex < len(containerList):
            container = containerList[currIndex]
            filteredContainerList.append(container)
            currIndex += 1 + QuestLinkDB.getQuestLink(container.getName())

        return filteredContainerList

    def isComplete(self, showComplete=False):
        for container in self.getFilteredContainers():
            if not container.isComplete(showComplete):
                return False

        return True

    def getNextContainer(self, currentQuestId):
        for container in self.containers:
            if container.hasQuest(currentQuestId):
                nextContainerIndex = self.containers.index(container) + QuestLinkDB.getQuestLink(currentQuestId)
                if nextContainerIndex >= len(self.containers):
                    return None
                return self.containers[nextContainerIndex]

        return None

    def assignFirstQuest(self, completedQuests):
        self.notify.debug('QC.assignFirstQuest().name: %s' % self.name)
        self.notify.debug('QC.assignFirstQuest().completedQuests: %s' % completedQuests)
        containerIndex = 0
        firstQuestId = self.getFirstQuestId()
        if firstQuestId:
            while self.containers[containerIndex].getName() != firstQuestId:
                if containerIndex >= len(self.containers):
                    containerIndex = 0
                    break
                else:
                    containerIndex += 1

        self.containers[containerIndex].assignFirstQuest(completedQuests)

    def updateCompletedQuests(self, completedQuest, prevCompletedQuests=[]):
        self.notify.debug('QC.updateCompletedQuests().name: %s' % self.name)
        self.notify.debug('QC.updateCompletedQuests().completedQuest: %s' % completedQuest.getName())
        self.notify.debug('QC.updateCompletedQuests().completedQuests: %s' % self.completedQuests)
        self.notify.debug('QC.updateCompletedQuests().prevCompletedQuests: %s' % prevCompletedQuests)
        if len(self.completedQuests) == 0:
            if len(prevCompletedQuests) > 0:
                self.notify.warning('QContainer.updateCompletedQuests.completeQuests is set to: %s' % prevCompletedQuests)
                self.completedQuests = prevCompletedQuests
        if completedQuest in self.completedQuests:
            self.notify.warning('QC.updateCompletedQuest(): Quest %s already in completedQuests!' % completedQuest.getQuestId())
        else:
            self.notify.debug('QC.updateCompletedQuest(): completedQuests appended with: %s' % completedQuest)
            self.completedQuests.append(completedQuest)

    def handleQuestComplete(self, completedQuest, completedContainer, prevCompletedQuests=[]):
        simbase.air.writeServerEvent('questLadder', self.av.doId, 'handleQuestComplete(%s,%s,%s)' % (completedQuest, completedContainer, prevCompletedQuests))
        self.notify.debug('QC.handleQuestComplete().name: %s' % self.name)
        self.notify.debug('QC.handleQuestComplete().completedQuest: %s' % completedQuest.getName())
        self.notify.debug('QC.handleQuestComplete().completedQuests: %s' % self.completedQuests)
        self.notify.debug('QC.handleQuestComplete().completedContainer: %s' % completedContainer.getName())
        self.notify.debug('QC.handleQuestComplete().completedContainer.completedQuests %s' % completedContainer.completedQuests)
        self.notify.debug('QC.handleQuestComplete().prevCompletedQuests: %s' % prevCompletedQuests)
        self.notify.debug('QC.handleQuestComplete().isComplete?: %s' % self.isComplete())
        qId = completedContainer.getName()
        simbase.air.writeServerEvent('questLadder', self.av.doId, 'ComletedContainer: %s' % qId)
        skipIndex = 1 + QuestLinkDB.getQuestLink(qId)
        nextIndex = self.containers.index(completedContainer) + skipIndex
        if nextIndex >= len(self.containers) and not isinstance(self, QuestChoice):
            if not self.isComplete():
                simbase.air.writeServerEvent('questLadder', self.av.doId, 'Container forced to complete!')
            isComplete = True
        else:
            isComplete = self.isComplete()
        if isComplete:
            simbase.air.writeServerEvent('questLadder', self.av.doId, 'Container COMPLETE: %s' % self.getName())
            self.av.questStatus.updateHistory(self)
            qEvent = QuestEvent.QuestContainerCompleted(containerId=self.getName())
            simbase.air.questMgr.handleEvent([self.av], qEvent)
            if self.parent:
                simbase.air.writeServerEvent('questLadder', self.av.doId, 'Call handleComlete on parent: %s' % self.parent.getName())
                self.updateCompletedQuests(completedQuest, prevCompletedQuests)
                self.parent.handleQuestComplete(completedQuest, self, self.completedQuests)
                self.completedQuests = []
            else:
                self.notify.debug('QC.handleQuestComplete(): root ladder is completed %s' % self.isComplete())
                self.updateCompletedQuests(completedQuest)
                quests = completedContainer.completedQuests
                self.av._swapQuest(oldQuests=quests, giverId=None, questIds=None, rewards=None)
                self.av.questStatus.handleLadderComplete(self)
        else:
            simbase.air.writeServerEvent('questLadder', self.av.doId, 'Container NOT COMPLETE: %s' % self.getName())
            simbase.air.writeServerEvent('questLadder', self.av.doId, 'Container skipIndex: %s' % skipIndex)
            self.av.questStatus.updateHistory(completedContainer)
            self.updateCompletedQuests(completedQuest)
            self.advance(completedContainer, skipIndex)
        return

    def handleQuestDropped(self, droppedQuest):
        self.notify.debug('QC.handleQuestDropped().name: %s' % self.name)
        self.notify.debug('QC.handleQuestDropped().droppedQuest: %s' % droppedQuest.getName())
        if self.parent:
            self.parent.handleQuestDropped(droppedQuest)
        else:
            self.av._dropQuest(droppedQuest)
            self.av.handleQuestDropped(droppedQuest.getQuestId())

    def advance(self, completedContainer, skipIndex=1):
        simbase.air.writeServerEvent('questLadder', self.av.doId, 'Advance QuestLadder: %s by %s' % (completedContainer.name, skipIndex))
        self.notify.debug('QC.advance().name: %s' % self.name)
        self.notify.debug('QC.advance().completedContainer: %s' % completedContainer.name)
        self.notify.debug('QC.advance().completedContainer.completedQuests: %s' % completedContainer.completedQuests)
        nextIndex = self.containers.index(completedContainer) + skipIndex
        nextContainer = self.containers[nextIndex]
        nextContainer.assignFirstQuest(completedContainer.completedQuests)
        for questId in completedContainer.completedQuests:
            if self.completedQuests.count(questId):
                self.completedQuests.remove(questId)

        completedContainer.complete = False
        completedContainer.completedQuests = []

    def assignQuest(self, quests, giverId, nextQuestIds, rewards=[], callback=None):
        simbase.air.writeServerEvent('questLadder', self.av.doId, 'assignQuest(quests: %s, giverId: %s, nextQuestIds: %s, rewards: %s, callback: %s)' % (quests, giverId, nextQuestIds, rewards, callback))
        self.notify.debug('QC.assignQuest().name: %s' % self.name)
        self.notify.debug('QC.assignQuest().nextQuestIds: %s' % nextQuestIds)
        for quest in quests:
            if hasattr(quest, 'questDNA'):
                questDNA = quest.getQuestDNA()
                if questDNA:
                    if questDNA.getProgressBlock() and (questDNA.getFinalQuest() or self.av.getAccess() != 2):
                        nextQuestId = nextQuestIds[0]
                        self.av.d_popupProgressBlocker(nextQuestId)
                else:
                    break
            else:
                self.notify.warning('%s has no questDNA!' % quest.getQuestId())

        nextQuestId = nextQuestIds[0]
        if len(quests):
            simbase.air.writeServerEvent('questLadder', self.av.doId, 'SWAP Quests: quests: %s, nestQuests: %s, rewards: %s' % (quests, nextQuestIds, rewards))
            self.av._swapQuest(quests, giverId, nextQuestIds, rewards)
        else:
            if len(nextQuestIds) > 1:
                self.notify.warning('attempted to assign multiple quests: %s' % nextQuestIds)
            simbase.air.writeServerEvent('questLadder', self.av.doId, 'ACCEPT Quest: %s' % nextQuestId)
            self.av._acceptQuest(nextQuestId, giverId, rewards)

        def handleQuestsAvailable(callback, av, quests):
            goalDisplayed = False
            for quest in quests:
                av.questStatus.assignQuest(quest)
                if not goalDisplayed:
                    if quest.getQuestDNA().getDisplayGoal() == True:
                        av.requestActiveQuest(quest.getQuestId())
                        goalDisplayed = True

            if callback:
                callback(av.getDoId())

        self.acceptOnce('quest-available-%s-%d' % (nextQuestId, self.av.getDoId()), handleQuestsAvailable, extraArgs=[callback])

    def updateHistory(self, completedContainer):
        self.av.questStatus.updateHistory(completedContainer)

    def getDownstreamContainers(self, downstreamContainers):
        for container in self.containers:
            downstreamContainers.append(container)
            container.getDownstreamContainers(downstreamContainers)

    def getChoiceContainers(self, choiceContainers):
        for container in self.getContainers():
            container.getChoiceContainers(choiceContainers)

        if self.isChoice():
            choiceContainers.append(self)

    def getPathToRoot(self, rootPath):
        container = self
        while container != None:
            parent = container.getParent()
            if parent:
                rootPath.append(parent)
            container = parent

        rootPath.reverse()
        return

    def getQuestPath(self, questId, cpath):
        if self.name == questId:
            self.getPathToRoot(cpath)
            return True
        for container in self.containers:
            if container.getQuestPath(questId, cpath):
                return True

        return False

    def getQuestStub(self, questId):
        if self.name == questId:
            return self
        for container in self.containers:
            qs = container.getQuestStub(questId)
            if qs:
                return qs

        return None

    def getFirstQuestId(self):
        if self.firstQuestId:
            return self.firstQuestId
        return self.containers[0].getFirstQuestId()

    def getNextQuestId(self, currQuestId):
        questStub = self.getQuestStub(currQuestId)
        if questStub:
            parent = questStub.getParent()
            nextContainer = parent.getNextContainer(currQuestId)
            if nextContainer:
                return nextContainer.getFirstQuestId()
            container = parent
            while container != None:
                parent = container.getParent()
                if parent:
                    nextContainer = parent.getNextContainer(currQuestId)
                    if nextContainer:
                        return nextContainer.getFirstQuestId()
                container = parent

        return

    def getSiblingQuestIds(self, questId):
        siblings = []
        questStub = self.getQuestStub(questId)
        if questStub:
            parent = questStub.getParent()
            for container in parent.getContainers():
                firstQuestId = container.getFirstQuestId()
                if firstQuestId and firstQuestId != questId:
                    siblings.append(firstQuestId)

        return siblings

    def getContainer(self, name):
        if self.name == name:
            return self
        else:
            for container in self.containers:
                ctr = container.getContainer(name)
                if ctr:
                    return ctr

        return None

    def getContainerInt(self, containerInt):
        if self.questInt == containerInt:
            return self
        else:
            for container in self.containers:
                ctr = container.getContainerInt(containerInt)
                if ctr:
                    return ctr

        return None

    def completeChildContainers(self):
        for container in self.getContainers():
            container.completeChildContainers()

        self.av.questStatus.updateHistory(self)

    def completePreviousContainers(self, container=None):
        if self.parent:
            self.parent.completePreviousContainers(self)
        if not (self.isChoice() or self.isBranch()) and container:
            if self.containers.count(container):
                index = self.containers.index(container)
                for idx in range(0, index):
                    self.containers[idx].completeChildContainers()

            else:
                self.notify.warning("%s not in parent's container list!" % container.getName())

    def printLine(self, indent, text):
        for i in range(0, indent):
            text = ' ' + text

        print text

    def printAll(self, indent=0):
        self.printLine(indent, 'Name: %s Title: %s' % (self.name, self.title))
        self.printLine(indent, 'Giver: %s FirstQuestId: %s' % (self.giverId, self.firstQuestId))
        self.printLine(indent, 'Description: %s' % self.description)
        self.printLine(indent, '--------------------------------------------')
        for container in self.containers:
            container.printAll(indent + 1)


class QuestStub(QuestContainer):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestStub')

    def __init__(self, name, av, questInt, parent, giverId, rewards, complete=False, description='', goal=1):
        title = name
        QuestContainer.__init__(self, name, title, av, questInt, parent, giverId, rewards, firstQuestId=name, description=description)
        self.quest = None
        self.goal = goal
        self.complete = complete
        self.processed = False
        return

    def destroy(self):
        self.quest = None
        QuestContainer.destroy(self)
        return

    def linkQuest(self, quest):
        if quest.getQuestId() == self.name:
            self.quest = quest
            if quest.isDroppable():
                self.acceptOnce(quest.getDroppedEventString(), self.handleQuestDropped)
            self.processed = False
            self.complete = False
            return True
        else:
            return False

    def unlinkQuest(self, questId):
        if questId == self.name:
            if self.quest == None:
                self.notify.warning('Unlinking empty quest stub: %s' % self.name)
            self.ignore(self.quest.getDroppedEventString())
            self.quest = None
            return True
        else:
            return False
        return

    def hasQuest(self, questId):
        return self.name == questId

    def assignFirstQuest(self, completedQuests):
        self.notify.warning('QS.assignFirstQuest().name: %s' % self.name)
        self.notify.warning('QS.assignFirstQuest().completedQuests: %s' % completedQuests)
        if not self.name:
            self.notify.warning('QS.assignFirstQuest(): no quest to assign!')
            return
        self.assignQuest(completedQuests, self.giverId, [self.name], [self.rewards])

    def handleQuestComplete(self, quest, prevCompletedQuests=[]):
        self.notify.debug('QS.handleQuestComplete().name: %s' % self.name)
        self.notify.debug('QS.handleQuestComplete().quest: %s' % quest.getName())
        self.notify.debug('QS.handleQuestComplete().prevCompletedQuests: %s' % prevCompletedQuests)
        self.notify.debug('QS.handleQuestComplete().completedQuests: %s' % self.completedQuests)
        self.notify.debug('QS.handleQuestComplete().isComplete?: %s' % self.isComplete())
        self.notify.debug('QS.handleQuestComplete().av.queststatus.NPC_Interact_Mode: %s' % self.av.questStatus.getNPCInteractMode())
        if self.complete:
            return False
        if self.av.questStatus.getNPCInteractMode() == False:
            qEvent = QuestEvent.QuestContainerCompleted(containerId=self.getName())
            simbase.air.questMgr.handleEvent([self.av], qEvent)
            self.complete = True
            if len(self.completedQuests) > 0:
                self.notify.warning('QS.handleQuestComplete(): completedQuests is not empty after getNPCInteractMode is reset False (interaction with npc is done)')
            self.completedQuests = [
             quest]
            self.processed = True
            self.parent.handleQuestComplete(quest, self, self.completedQuests)
        return True

    def handleQuestDropped(self, quest):
        self.complete = False
        self.parent.handleQuestDropped(quest)

    def isComplete(self, showComplete=False):
        if showComplete:
            if self.quest:
                return self.quest.isComplete(showComplete)
            else:
                return self.getComplete()
        if self.quest and not self.quest.isDeleted():
            if self.processed:
                return self.quest.isComplete(showComplete)
        return False

    def getFirstQuestId(self):
        return self.name

    def getTaskProgress(self):
        if self.quest:
            return self.quest.getTaskProgress()
        return []


class QuestChoice(QuestContainer):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestChoice')
    CompleteAll = -1

    def __init__(self, name, title, av, questInt, parent, giverId, rewards, description='', completeCount=-1):
        firstQuestId = None
        QuestContainer.__init__(self, name, title, av, questInt, parent, giverId, rewards, firstQuestId, description)
        self.revisitQuestId = '%s-revisit' % self.name
        self.completeCount = completeCount
        self.completeCountVerified = False
        return

    def isChoice(self):
        return True

    def __verifyCompleteCount(self):
        if not self.completeCountVerified:
            if self.completeCount == self.CompleteAll:
                self.completeCount = len(self.getContainers())
            self.completeCountVerified = True

    def getProgress(self, showComplete=False):
        self.__verifyCompleteCount()
        compCont = 0
        history = []
        if self.av:
            history = self.av.getQuestLadderHistory()
        for container in self.getContainers():
            if container.isComplete(showComplete) or container.getQuestInt() in history:
                compCont += 1

        return (
         compCont, self.completeCount, len(self.getContainers()))

    def getValidContainers(self):
        quests = self.av.questStatus.getCurrentQuests()
        containers = self.getContainers()
        validContainers = []
        for container in containers:
            valid = True
            for quest in quests:
                if container.hasQuest(quest.getQuestId()):
                    valid = False
                    break

            if valid:
                validContainers.append(container)

        return validContainers

    def isComplete(self, showComplete=False):
        self.__verifyCompleteCount()
        compCont = 0
        for container in self.getContainers():
            if container.isComplete(showComplete):
                compCont += 1

        return compCont == self.completeCount

    def chooseQuest(self, nextQuestId, giverId, rewards, callback=None):
        if len(self.completedQuests):
            pass
        container = self.getContainer(nextQuestId)
        if container:
            nextQuestId = container.getFirstQuestId()
        self.assignQuest(self.completedQuests, self.giverId, [nextQuestId], rewards=rewards, callback=callback)
        self.completedQuests = []

    def assignFirstQuest(self, completedQuests):
        self.notify.debug('QChoice.assignFirstQuest().name: %s' % self.name)
        self.notify.debug('QChoice.assignFirstQuest().completedQuests: %s' % completedQuests)
        nextQuestIds = []
        rewards = []
        for container in self.getContainers():
            nextQuestIds.append(container.getQuestId())
            rewards.append(container.getRewards())

        self.assignQuest(completedQuests, self.giverId, nextQuestIds, rewards)

    def updateCompletedQuests(self, completedQuest, prevCompletedQuests=[]):
        self.notify.debug('QChoice.updateCompletedQuests().name: %s' % self.name)
        self.notify.debug('QChoice.updateCompletedQuests().completedQuest: %s' % completedQuest.getName())
        self.notify.debug('QChoice.updateCompletedQuests().completedQuests: %s' % self.completedQuests)
        self.notify.debug('QChoice.updateCompletedQuests().prevCompletedQuest: %s' % prevCompletedQuests)
        if completedQuest in self.completedQuests:
            self.notify.warning('QChoice.updateCompletedQuests(): Quest %s already in completedQuests!' % completedQuest.getQuestId())
        else:
            self.notify.debug('QChoice.updateCompletedQuest(): completedQuests appended with: %s' % completedQuest)
            self.completedQuests.append(completedQuest)

    def advance(self, completedContainer, skipIndex=1):
        pass

    def handleQuestDropped(self, droppedQuest):
        self.notify.debug('QChoice.handleQuestDropped().name: %s' % self.name)
        self.notify.debug('QChoice.handleQuestDropped().droppedQuest: %s' % droppedQuest.getName())
        quests = self.av.questStatus.getCurrentQuests()
        found = 0
        if quests:
            droppedQuestId = droppedQuest.getQuestId()
            for quest in quests:
                if quest.getQuestId() != droppedQuestId and self.hasQuest(quest.getQuestId()):
                    found = 1
                    break

        if not found:
            self.notify.warning('DroppedQuest %s not in current quests!' % droppedQuest.getQuestId())
        self.av._dropQuest(droppedQuest)
        self.av.handleQuestDropped(droppedQuest.getQuestId())


class QuestLadder(QuestContainer):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestLadder')

    def isComplete(self, showComplete=False):
        containers = self.getFilteredContainers()
        return containers[-1].isComplete(showComplete)


class QuestBranch(QuestContainer):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestBranch')

    def __init__(self, name, title, av, questInt, parent, giverId, rewards, firstQuestId, description='', completeCount=-1):
        QuestContainer.__init__(self, name, title, av, questInt, parent, giverId, rewards, firstQuestId, description)
        self.completeCount = completeCount

    def isComplete(self, showComplete=False):
        if self.getFirstQuestId():
            for container in self.getFilteredContainers():
                if container.getQuestId() == self.getFirstQuestId():
                    return container.isComplete(showComplete)

            return False
        completedContainers = 0
        for container in self.getFilteredContainers():
            if container.isComplete(showComplete):
                completedContainers += 1
                if completedContainers == self.completeCount:
                    return True

        return False

    def handleQuestComplete(self, completedQuest, completedContainer, prevCompletedQuests=[]):
        if not self.isComplete():
            self.updateCompletedQuests(completedQuest)
            quests = completedContainer.completedQuests
            self.av._swapQuest(oldQuests=quests, giverId=None, questIds=None, rewards=None)
        else:
            if self.parent:
                self.av.questStatus.updateHistory(self)
                self.updateCompletedQuests(completedQuest, prevCompletedQuests)
                self.parent.handleQuestComplete(completedQuest, self, self.completedQuests)
                self.completedQuests = []
            else:
                self.av.questStatus.updateHistory(self)
                self.av.questStatus.handleLadderComplete(self)
            if self.isComplete():
                qEvent = QuestEvent.QuestContainerCompleted(containerId=self.getName())
                simbase.air.questMgr.handleEvent([self.av], qEvent)
        return

    def isBranch(self):
        return True