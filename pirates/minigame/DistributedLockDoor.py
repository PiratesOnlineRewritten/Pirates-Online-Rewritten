from pirates.minigame import DistributedLock
from direct.interval.IntervalGlobal import *

class DistributedLockDoor(DistributedLock.DistributedLock):

    def __init__(self, cr):
        DistributedLock.DistributedLock.__init__(self, cr)
        self.isDoor = 1

    def loadModel(self):
        self.table = loader.loadModel('models/props/jail_door_03')
        self.table.setScale(1.0, 1.0, 1.0)
        self.table.reparentTo(self)

    def finalOpen(self):
        colNode = self.table.find('**/collisions')
        colNode.stash()
        self.hinge = self.table.find('**/jail_door')
        lidopener = LerpHprInterval(self.hinge, 1, Vec3(-140, 0, 0))
        lidopener.start()
        self.setAllowInteract(False)