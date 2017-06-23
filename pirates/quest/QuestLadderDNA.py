from direct.directnotify import DirectNotifyGlobal
from direct.showbase.PythonUtil import POD
from pirates.quest.QuestLadder import QuestLadder, QuestChoice, QuestBranch
from pirates.quest.QuestDNA import QuestDNA
from pirates.quest.QuestTaskDNA import VisitTaskDNA
from pirates.quest import QuestDB
from pirates.piratesbase import PLocalizer
import random

class QuestContainerDNA(POD):
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestContainerDNA')
    Counter = 1102
    DataSet = {'name': None,'questInt': -1,'title': '','description': '','giverId': None,'firstQuestId': None,'containers': None,'rewards': tuple(),'completeCount': QuestChoice.CompleteAll,'stringBefore': '','stringDuring': '','stringAfter': '','dialogBrushoff': '','droppable': False,'hideButton': False,'questMod': None,'obsolete': False,'questLink': None}

    def hasQuest(self, questId):
        for container in self.getContainers():
            if container.getName() == questId or container.hasQuest(questId):
                return True

        return False

    def isContainer(self):
        return True

    def isChoice(self):
        return False

    def isBranch(self):
        return False

    def isLadder(self):
        return False

    def getQuestId(self):
        return self.name

    def getObject(self, id):
        if self.getQuestId() == id:
            return self
        else:
            for container in self.getContainers():
                container.getObject(id)

        return None

    def getContainer(self, name):
        if self.name == name:
            return self
        else:
            for container in self.getContainers():
                ctr = container.getContainer(name)
                if ctr:
                    return ctr

        return None

    def getParentContainer(self, ctr):
        if ctr in self.getContainers():
            return self
        else:
            for container in self.getContainers():
                parent = container.getParentContainer(ctr)
                if parent:
                    return parent

        return None

    def initialize(self, parentIsChoice=False):
        for container in self.getContainers():
            container.initialize(parentIsChoice)

    def initializeFortune(self, droppable):
        for container in self.getContainers():
            container.initializeFortune(droppable)

    def constructDynamicCopy(self, av, parent=None):
        dynCopy = self._makeDynamicCopy(self.getName(), self.getTitle(), av, self.getQuestInt(), parent, self.getGiverId(), self.getRewards(), self.getFirstQuestId(), self.getDescription(), self.getCompleteCount())
        goal = 0
        for container in self.getContainers():
            dynObj = container.constructDynamicCopy(av, parent=dynCopy)
            goal += dynObj.getGoal()
            dynCopy.addContainer(dynObj)

        dynCopy.setGoal(goal)
        return dynCopy

    def _getString(self, stringName):
        if self.name not in PLocalizer.QuestStrings:
            return
        string = PLocalizer.QuestStrings[self.name].get(stringName)
        if string is None or len(string) == 0:
            return
        return string

    def getStringBefore(self):
        dialog = self._getString('stringBefore')
        if dialog is not None:
            return dialog
        return random.choice(PLocalizer.QuestDefaultDialogBefore)

    def getStringDuring(self):
        dialog = self._getString('stringDuring')
        if dialog is not None:
            return dialog
        return random.choice(PLocalizer.QuestDefaultDialogDuring)

    def getStringAfter(self):
        dialog = self._getString('stringAfter')
        if dialog is not None:
            return dialog
        return random.choice(PLocalizer.QuestDefaultDialogAfter)

    def getDialogAfter(self):
        dialog = self._getString('dialogAfter')
        if dialog is not None:
            return dialog
        return ''

    def getDialogBrushoff(self):
        dialog = self._getString('dialogBrushoff')
        if dialog is not None:
            return dialog
        return random.choice(PLocalizer.QuestDefaultDialogBrushoff)

    def getAnimSetAfter(self):
        anims = self._getString('animSetAfter')
        return anims

    def getDescriptionText(self):
        dialog = self._getString('description')
        if dialog is not None:
            return dialog
        return 'Unknown'

    def compileStats(self, questStatData):
        if self.completeCount == QuestChoice.CompleteAll:
            containers = self.containers
        else:
            containers = self.containers[:self.completeCount]
        for container in containers:
            container.compileStats(questStatData)


class QuestChoiceDNA(QuestContainerDNA):

    def _makeDynamicCopy(self, name, title, av, questInt, parent, giverId, rewards, firstQuestId, description, completeCount):
        return QuestChoice(name, title, av, questInt, parent, giverId, rewards, description, completeCount)

    def isChoice(self):
        return True


class QuestLadderDNA(QuestContainerDNA):

    def _makeDynamicCopy(self, name, title, av, questInt, parent, giverId, rewards, firstQuestId, description, completeCount):
        return QuestLadder(name, title, av, questInt, parent, giverId, rewards, firstQuestId, description)

    def isLadder(self):
        return True


class QuestBranchDNA(QuestContainerDNA):

    def _makeDynamicCopy(self, name, title, av, questInt, parent, giverId, rewards, firstQuestId, description, completeCount):
        return QuestBranch(name, title, av, questInt, parent, giverId, rewards, firstQuestId, description, completeCount)

    def isBranch(self):
        return True