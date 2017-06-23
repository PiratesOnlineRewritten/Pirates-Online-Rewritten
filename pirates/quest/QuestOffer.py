from direct.showbase.PythonUtil import POD, makeTuple
from pirates.quest import QuestReward, QuestDB, QuestLadderDB

class QuestOffer(POD):
    DataSet = {'questId': None,'title': '','initialTaskStates': tuple(),'rewardStructs': tuple()}

    @staticmethod
    def create(questId, holder, timerReset=False, branchReset=False):
        if QuestDB.QuestDict.has_key(questId):
            questDNA = QuestDB.QuestDict[questId]
            initialTaskStates = questDNA.getInitialTaskStates(holder)
            rewards = questDNA.getRewards()
            if len(rewards) == 0:
                rewards = questDNA.computeRewards(initialTaskStates, holder)
        else:
            questDNA = QuestLadderDB.getContainer(questId)
            initialTaskStates = []
            rewards = []
        if timerReset:
            return QuestTimerResetOffer(questId, questId, initialTaskStates, rewards)
        if branchReset:
            return QuestBranchResetOffer(questId, questId, initialTaskStates, rewards)
        return QuestOffer(questId, questId, initialTaskStates, rewards)

    def __init__(self, questId=None, title=None, initialTaskStates=None, rewards=None):
        POD.__init__(self)
        if questId is not None:
            self.setQuestId(questId)
            self.setTitle(title)
            self.setInitialTaskStates(initialTaskStates)
            self.setRewards(rewards)
        return

    def getRewards(self):
        rewards = []
        for rewardStruct in self.getRewardStructs():
            rewards.append(QuestReward.QuestReward.makeFromStruct(rewardStruct))

        return rewards

    def setRewards(self, rewards):
        rewardStructs = []
        for reward in makeTuple(rewards):
            if reward:
                rewardStructs.append(reward.getQuestRewardStruct())

        self.setRewardStructs(rewardStructs)

    def getQuestDNA(self):
        if QuestDB.QuestDict.has_key(self.questId):
            return QuestDB.QuestDict[self.questId]
        else:
            return QuestLadderDB.getContainer(self.questId)

    def isLadder(self):
        if not QuestDB.QuestDict.has_key(self.questId):
            return True
        return False


class QuestTimerResetOffer(QuestOffer):
    pass


class QuestBranchResetOffer(QuestOffer):
    pass