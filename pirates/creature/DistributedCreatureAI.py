from direct.directnotify import DirectNotifyGlobal
from pirates.battle.DistributedBattleNPCAI import *
from pirates.pirate import AvatarTypes

class DistributedCreatureAI(DistributedBattleNPCAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCreatureAI')

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)

