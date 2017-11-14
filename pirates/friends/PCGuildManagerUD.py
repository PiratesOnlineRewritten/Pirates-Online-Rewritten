from direct.directnotify import DirectNotifyGlobal
from otp.friends.GuildManagerUD import GuildManagerUD

class PCGuildManagerUD(GuildManagerUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PCGuildManagerUD')

    def __init__(self, air):
        GuildManagerUD.__init__(self, air)
