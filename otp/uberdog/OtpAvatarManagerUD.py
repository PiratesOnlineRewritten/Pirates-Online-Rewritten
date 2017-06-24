from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class OtpAvatarManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('OtpAvatarManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)