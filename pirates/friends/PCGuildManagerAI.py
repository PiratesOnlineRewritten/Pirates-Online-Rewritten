from direct.directnotify import DirectNotifyGlobal
from otp.friends.GuildManagerAI import GuildManagerAI

class PCGuildManagerAI(GuildManagerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PCGuildManagerAI')

    def __init__(self, air):
        GuildManagerAI.__init__(self, air)

    def sendSCQuest(self, questInt, mesgType, taskNum):
        pass
