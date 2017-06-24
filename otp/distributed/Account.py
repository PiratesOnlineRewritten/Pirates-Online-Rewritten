from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify import DirectNotifyGlobal

class Account(DistributedObjectGlobal):
    notify = DirectNotifyGlobal.directNotify.newCategory('Account')

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
