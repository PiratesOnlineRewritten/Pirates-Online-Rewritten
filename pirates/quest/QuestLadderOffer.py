from direct.showbase.PythonUtil import POD, makeTuple
from pirates.quest import QuestReward, QuestLadderDB

class QuestLadderOffer(POD):
    DataSet = {'questId': None,'title': '','rewardStructs': tuple()}

    def __init__(self, questId=None, title=None, rewards=None):
        POD.__init__(self)
        if None not in (questId, title, rewards):
            self.setQuestId(questId)
            self.setTitle(title)
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
            rewardStructs.append(reward.getQuestRewardStruct())

        self.setRewardStructs(rewardStructs)

    def getQuestDNA(self):
        return QuestLadderDB.getContainer(self.questId)

    def isLadder(self):
        return True