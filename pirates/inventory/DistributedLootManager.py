from direct.distributed import DistributedObject

class DistributedLootManager(DistributedObject.DistributedObject):

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        base.cr.lootMgr = self

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        base.cr.lootMgr = None
        return

    def delete(self):
        DistributedObject.DistributedObject.disable(self)

    def d_requestItemFromContainer(self, containerId, itemInfo):
        self.sendUpdate('requestItemFromContainer', [containerId, itemInfo])

    def d_requestItems(self, containers):
        self.sendUpdate('requestItems', [containers])

    def warnRemoveLootContainerFromScoreboard(self, containerId):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            scoreboard = base.localAvatar.guiMgr.scoreboard
            if scoreboard and hasattr(scoreboard, 'removeLootContainer'):
                messenger.send('Scoreboard-Loot-Timed-Out-Warning', [containerId])

    def removeLootContainerFromScoreboard(self, containerId):
        messenger.send('Scoreboard-Loot-Timed-Out', [containerId])
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            scoreboard = base.localAvatar.guiMgr.scoreboard
            if scoreboard and hasattr(scoreboard, 'removeLootContainer'):
                scoreboard.removeLootContainer(containerId)