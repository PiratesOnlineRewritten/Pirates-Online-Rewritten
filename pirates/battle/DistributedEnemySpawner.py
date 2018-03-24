from direct.distributed import DistributedObject

class DistributedEnemySpawner(DistributedObject.DistributedObject):

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
