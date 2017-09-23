from direct.directnotify import DirectNotifyGlobal
from otp.uberdog.SpeedchatRelayUD import SpeedchatRelayUD

class DistributedChatManagerUD(SpeedchatRelayUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedChatManagerUD')

    def __init__(self, air):
        SpeedchatRelayUD.__init__(self, air)
