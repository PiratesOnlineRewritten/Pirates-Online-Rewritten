import copy
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import POD, makeTuple
from direct.task.Task import Task
from pirates.piratesbase import PLocalizer
from pirates.quest import QuestDB, QuestReward, QuestTaskDNA
from pirates.quest.QuestDNA import QuestDNA
from otp.otpbase import OTPGlobals
from pirates.piratesbase import Freebooter

class Quest(POD):
    notify = DirectNotifyGlobal.directNotify.newCategory('Quest')
    DataSet = {'questId': None,'giverId': None,'combineOp': None,'tasks': None,'rewards': None,'taskStates': []}
    SerialNum = 0

    def __init__(self, questId=None, giverId=None, initialTaskStates=None, rewards=None):
        self.questDNA = None
        self._serialNum = Quest.SerialNum
        Quest.SerialNum += 1
        POD.__init__(self)
        if questId is not None:
            self.setupQuest(questId, giverId, initialTaskStates, rewards)
        self.__finished = False
        self.__finalized = False
        self.__timedOut = False
        self.__timeRemaining = 0
        return

    def destroy(self):
        del self.questDNA
        del self.tasks
        del self.rewards
        for taskState in self.taskStates:
            taskState.release()

        del self.taskStates

    def setupQuest(self, questId, giverId, initialTaskStates, rewards):
        self.setQuestId(questId)
        self.setGiverId(giverId)
        self.setRewards(rewards)
        self.sendTaskStates(initialTaskStates)

    def setQuestId(self, questId):
        self.questId = questId
        if questId not in (None, ''):
            self.questDNA = QuestDB.QuestDict.get(self.questId)
            if self.questDNA:
                self.questDNA.makeCopy()
                self.setCombineOp(self.questDNA.getCombineOp())
                self.setTasks(self.questDNA.getTasks())
                if self.questDNA.getTimeLimit():
                    self.__timedOut = True
        else:
            self.questDNA = None
        return

    def getQuestDNA(self):
        return self.questDNA

    def getQuestGoalUid(self):
        for taskState, taskDNA in zip(self.taskStates, self.questDNA.getTasks()):
            return taskDNA.getGoalUid(taskState)

        return None

    def getChangeEvent(self):
        return 'Quest.questChange-%s' % self._serialNum

    def setTaskStates(self, taskStates):
        oldTaskStates = getattr(self, 'taskStates', None)
        self.taskStates = taskStates
        if self.taskStates:
            for taskState in self.taskStates:
                taskState.acquire()

        if oldTaskStates:
            for taskState in oldTaskStates:
                taskState.release()

        messenger.send(self.getChangeEvent())
        return

    def sendTaskStates(self, taskStates):
        self.setTaskStates(taskStates)

    def setRewardStructs(self, rewardStructs):
        rewards = []
        if self.questDNA != None:
            rewardDNAs = list(self.questDNA.rewards)
            for rewardStruct in rewardStructs:
                rewardObj = QuestReward.QuestReward.makeFromStruct(rewardStruct)
                for currRewardDNA in rewardDNAs:
                    if currRewardDNA.isSame(rewardObj):
                        rewardObj.setBonus(currRewardDNA.isBonus())
                        rewardDNAs.remove(currRewardDNA)
                        break

                rewards.append(rewardObj)

        self.setRewards(rewards)
        return

    def getRewardStructs(self):
        rewardStructs = []
        for reward in self.getRewards():
            rewardStructs.append(reward.getQuestRewardStruct())

        return rewardStructs

    def handleEvent(self, holder, questEvent):
        modified = 0
        for taskState, taskDNA in zip(self.taskStates, self.questDNA.getTasks()):
            if taskDNA.locationMatches(questEvent):
                taskState.resetModified()
                if questEvent.applyTo(taskState, taskDNA):
                    if holder.getAccess() != 2 and self.questDNA.getVelvetRoped():
                        holder.d_popupProgressBlocker(self.getQuestId())
                    else:
                        questEvent.complete(taskState, taskDNA)
                modified += taskState.isModified()

        if modified:
            self.sendTaskStates(self.taskStates)

    def isDroppable(self):
        return self.questDNA != None and self.questDNA.getDroppable()

    def isShareable(self):
        return True

    def completeRequiresVisit(self):
        return self.questDNA.getCompleteRequiresVisit()

    def playStinger(self):
        if not self.questDNA:
            return False
        return self.questDNA.getPlayStinger()

    def getBranchParent(self, av):

        def getBranchParentRecursive(container):
            if container and container.parent:
                if container.parent.isBranch():
                    return container.parent
                else:
                    return getBranchParentRecursive(container.parent)
            else:
                return None
            return None

        container = av.questStatus.getContainer(self.questId)
        return getBranchParentRecursive(container)

    def setFinished(self, finished):
        self.__finished = finished

    def isFinished(self):
        return self.__finished

    def isTimedOut(self):
        return self.__timedOut

    def setTimedOut(self, timedOut):
        self.__timedOut = timedOut

    def getTimeLimit(self):
        return self.questDNA.getTimeLimit()

    def getTimeRemaining(self):
        return self.__timeRemaining

    def setTimeRemaining(self, time):
        self.__timeRemaining = time

    def setFinalized(self, finalized):
        self.__finalized = finalized

    def isFinalized(self):
        return self.__finalized

    def isCompleteWithBonus(self, showComplete=False):
        return self.isComplete(showComplete=showComplete) and self.isComplete(showComplete=showComplete, bonus=True)

    def isComplete(self, showComplete=False, bonus=False):
        if self.__finished and not bonus:
            return True
        if hasattr(self, 'taskStates'):
            if len(self.taskStates) == 0:
                return True
        else:
            return False
        if self.combineOp is QuestDNA.OR:
            for task in self.taskStates:
                if task.isComplete(bonus):
                    if not bonus:
                        self.__finished = True
                    return True

            return False
        elif self.combineOp is QuestDNA.AND:
            for task in self.taskStates:
                if not task.isComplete(bonus):
                    return False

            if not bonus:
                self.__finished = True
            return True
        else:
            raise 'unknown task combineOp: %s' % self.combineOp

    def percentComplete(self):
        if self.__finished or self.isComplete() == True:
            return 1.0
        if hasattr(self, 'taskStates') and len(self.taskStates) == 0:
            return 1.0
        if self.combineOp is QuestDNA.OR:
            return 0.0
        elif self.combineOp is QuestDNA.AND:
            totalTasks = len(self.taskStates)
            completedTasks = 0
            for task in self.taskStates:
                if task.isComplete():
                    completedTasks += 1

            return completedTasks / totalTasks
        else:
            raise 'unknown task combineOp: %s' % self.combineOp

    def canBeReturnedTo(self, giverId):
        noGiversSpecified = True
        returnGiverIds = self.questDNA.getReturnGiverIds()
        if returnGiverIds is not None:
            noGiversSpecified = False
            if giverId in returnGiverIds:
                return True
        for task, taskState in zip(self.getTasks(), self.getTaskStates()):
            if taskState.isComplete() or self.isTimedOut():
                returnGiverIds = task.getReturnGiverIds()
                if returnGiverIds is not None:
                    noGiversSpecified = False
                    if giverId in returnGiverIds:
                        return True

        if noGiversSpecified:
            if giverId == self.getGiverId():
                return True
        return False

    def getSCSummaryText(self, taskNum):
        taskState = self.getTaskStates()[taskNum]
        return self.questDNA.getSCSummaryText(taskNum, taskState)

    def getSCWhereIsText(self, taskNum):
        return self.questDNA.getSCWhereIsText(taskNum)

    def getSCHowToText(self, taskNum):
        return self.questDNA.getSCHowToText(taskNum)

    def getDescriptionText(self, bonus=False):
        return self.questDNA.getDescriptionText(self.taskStates, bonus=bonus)

    def getRewardText(self):
        return QuestReward.QuestReward.getDescriptionText(self.getRewards())

    def getRestartText(self):
        if self.questDNA == None:
            return ''
        return

    def getReturnText(self):
        if self.questDNA == None:
            return ''
        choice = False
        choiceComplete = False
        container = localAvatar.questStatus.getContainer(self.questId)
        if container and container.parent and container.parent.isChoice():
            choice = True
            if container.parent.isComplete(showComplete=True):
                choiceComplete = True
        timeLimit = self.questDNA.getTimeLimit()
        timeRemaining = self.getTimeRemaining()
        returnGiverIds = self.questDNA.getReturnGiverIds()
        if returnGiverIds:
            npcNames = map(lambda id: PLocalizer.NPCNames.get(id, PLocalizer.DefaultTownfolkName), returnGiverIds)
            if len(returnGiverIds) == 1:
                if timeLimit and not timeRemaining:
                    return PLocalizer.QuestRestartReturnId % {'npcName': npcNames[0]}
                elif choice and not choiceComplete:
                    return PLocalizer.SingleChoiceQuestReturnId % {'npcName': npcNames[0]}
                elif filter(lambda x: isinstance(self.getTasks()[0], x), [QuestTaskDNA.VisitTaskDNA, QuestTaskDNA.DeliverItemTaskDNA]):
                    return PLocalizer.SingleQuestReturnIdCollect % {'npcName': npcNames[0]}
                else:
                    return PLocalizer.SingleQuestReturnId % {'npcName': npcNames[0]}
            elif choice and not choiceComplete:
                return PLocalizer.MultipleChoiceQuestReturnIds % {'npcNames': npcNames}
            else:
                return PLocalizer.MultipleQuestReturnIds % {'npcNames': npcNames}
        else:
            giverId = ''
            taskDNAs = self.questDNA.getTaskDNAs()
            for task in taskDNAs:
                if isinstance(task, QuestTaskDNA.VisitTaskDNA):
                    giverId = task.getReturnGiverIds()[0]
                    break

            if not giverId:
                giverId = self.getGiverId()
            npcName = PLocalizer.NPCNames.get(giverId, PLocalizer.DefaultTownfolkName)
            if timeLimit and not timeRemaining:
                return PLocalizer.QuestRestartReturnId % {'npcName': npcName}
            if choice and not choiceComplete:
                return PLocalizer.SingleChoiceQuestReturnId % {'npcName': npcName}
            else:
                return PLocalizer.SingleQuestReturnId % {'npcName': npcName}
        return

    def getTaskProgress(self):
        progressList = []
        taskStates = getattr(self, 'taskStates', None)
        if taskStates:
            for taskState in taskStates:
                goal = taskState.getGoal()
                progress = taskState.getProgress()
                progressList.append((progress, goal))

        return progressList

    def getStatusText(self):
        if self.questDNA == None:
            return ''
        if self.questDNA.getVelvetRoped() and base.localAvatar.getAccess() != OTPGlobals.AccessFull:
            if not Freebooter.AllAccessHoliday:
                return PLocalizer.VelvetRopeQuestBlock
        taskDNAs = self.questDNA.getTaskDNAs()
        taskStates = self.getTaskStates()

        def getTaskText(taskDNA, taskState, format, bonus=False):
            descText = self.getDescriptionText(bonus=bonus)
            if descText == None:
                return
            if bonus:
                goal = taskState.getBonusGoal()
                progress = taskState.getBonusProgress()
            else:
                goal = taskState.getGoal()
                progress = taskState.getProgress()
            progressStr = ''
            if progress < goal:
                if goal > 1 and not isinstance(taskDNA, QuestTaskDNA.DowsingRodTaskDNA):
                    progressStr = PLocalizer.QuestTaskProgress % {'prog': progress,'goal': goal}
            else:
                progressStr = PLocalizer.QuestProgressComplete
            return format % {'task': descText,'prog': progressStr}

        if len(taskDNAs) == 1:
            str = PLocalizer.QuestStrOneTask % {'task': getTaskText(taskDNAs[0], taskStates[0], PLocalizer.QuestStatusTaskSingle)
               }
            bonusDescText = getTaskText(taskDNAs[0], taskStates[0], PLocalizer.QuestStatusTaskSingle, bonus=True)
            if bonusDescText:
                str += PLocalizer.QuestStatusTaskBonus + PLocalizer.QuestStrOneTask % {'task': bonusDescText}
        else:
            headingStr = {QuestDNA.OR: PLocalizer.QuestMultiHeadingOr,QuestDNA.AND: PLocalizer.QuestMultiHeadingAnd}[self.getCombineOp()]
            tasksStr = ''
            for taskDNA, taskState in zip(taskDNAs, taskStates):
                tasksStr += getTaskText(taskDNA, taskState, PLocalizer.QuestStatusTaskMulti)

            str = PLocalizer.QuestStrMultiTask % {'heading': headingStr,'tasks': tasksStr}
        return str

    def __repr__(self):
        return '<Quest %s>' % self.getQuestId()

    def handleStart(self, avId):
        for currTask in self.tasks:
            currTask.handleStart(avId)

    def getValidRewards(self):
        if self.isComplete(bonus=True):
            return self.getRewards()
        else:
            normalRewards = []
            for currReward in self.getRewards():
                if not currReward.isBonus():
                    normalRewards.append(currReward)

            return normalRewards