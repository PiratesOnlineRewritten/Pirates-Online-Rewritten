from pirates.instance import DistributedInstanceBase
from pandac.PandaModules import NodePath

class DistributedTeleportZone(DistributedInstanceBase.DistributedInstanceBase, NodePath):

    def __init__(self, cr):
        DistributedInstanceBase.DistributedInstanceBase.__init__(self, cr)

    def getInstanceNodePath(self):
        return self
