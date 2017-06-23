

class QuestHolderBase():

    def __init__(self):
        self._rewardCollectors = {}

    def getQuests(self):
        raise 'derived must implement'

    def _addQuestRewardCollector(self, collector):
        cId = collector._serialNum
        self._rewardCollectors[cId] = collector

    def _removeQuestRewardCollector(self, collector):
        cId = collector._serialNum
        del self._rewardCollectors[cId]

    def _trackRewards(self, trade):
        for collector in self._rewardCollectors.itervalues():
            collector.collect(trade)