from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals

class DistributedTeleportHandlerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportHandlerAI')

    def __init__(self, air, teleportMgr, teleportFsm, avatar):
        DistributedObjectAI.__init__(self, air)

        self.teleportMgr = teleportMgr
        self.avatar = avatar
        self.teleportFsm = teleportFsm

    def startTeleportProcess(self, parentId, zoneId, bandId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        self.sendUpdateToAvatarId(self.avatar.doId, 'waitInTZ', [[], 0])

    def teleportToInstanceReady(self, zoneId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        world = self.teleportFsm.world
        instance = self.teleportFsm.instance

        self.sendUpdateToAvatarId(self.avatar.doId, 'continueTeleportToInstance', [world.parentId, world.zoneId, world.doId, world.getFileName(),
            world.doId, instance.zoneId, instance.doId, world.getFileName(), world.oceanGrid.doId])

    def readyToFinishTeleport(self, instanceDoId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        world = self.teleportFsm.world
        instance = self.teleportFsm.instance
        xPos, yPos, zPos, h = self.teleportFsm.spawnPt

        world.d_setSpawnInfo(self.avatar.doId, xPos, yPos, zPos, h, 0, [instance.doId, instance.parentId, instance.zoneId])
        self.sendUpdateToAvatarId(self.avatar.doId, 'teleportToInstanceCleanup', [])

    def teleportToInstanceFinal(self, avatarId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        instance = self.teleportFsm.instance
        self.avatar.b_setLocation(instance.doId, PiratesGlobals.IslandLocalZone)
        self.teleportFsm.request('Stop')
