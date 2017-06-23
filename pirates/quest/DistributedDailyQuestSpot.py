from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedNode
from pirates.world import DistributedLocatableObject
from direct.showbase.PythonUtil import report

class DistributedDailyQuestSpot(DistributedNode.DistributedNode):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDailyQuestSpot')

    def __init__(self, cr):
        NodePath.NodePath.__init__(self, 'QuestSpot')
        DistributedNode.DistributedNode.__init__(self, cr)
        print 'New Daily Quest Spot'
        base.dqs = self

    def delete(self):
        DistributedNode.DistributedNode.delete(self)

    def generate(self):
        DistributedNode.DistributedNode.generate(self)

    def disable(self):
        DistributedNode.DistributedNode.disable(self)

    def announceGenerate(self):
        DistributedNode.DistributedNode.announceGenerate(self)

    def isBattleable(self):
        return 0

    def isInvisibleGhost(self):
        return 0