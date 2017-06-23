from pirates.quest import QuestHolderBase

class QuestHolder(QuestHolderBase.QuestHolderBase):

    def getLinkedHolders(self):
        return []