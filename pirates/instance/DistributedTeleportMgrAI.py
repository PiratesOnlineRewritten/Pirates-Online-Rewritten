from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals

class DistributedTeleportMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportMgrAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.teleporting = {}

    def requestInstanceTeleport(self, instanceType, instanceName):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.d_confirmTeleport(avatar.doId, False, [], 0, 0)
            return

        instance = self.air.worldCreator.world
        area = instance.uidMgr.justGetMeMeObject('1150922126.828659a2')

        self.teleporting[avatar.doId] = [instance.doId, area.doId]
        self.d_confirmTeleport(avatar.doId, True, [[instance.parentId, instance.zoneId]], instance.doId, area.doId)

    def teleportInitiated(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar or avatar.doId not in self.teleporting:
            self.d_confirmTeleport(avatar.doId, False, [], 0, 0)
            return

        instance = self.air.doId2do.get(self.teleporting[avatar.doId][0])
        area = self.air.doId2do.get(self.teleporting[avatar.doId][1])

        if not instance or not area:
            self.d_confirmTeleport(avatar.doId, False, [], 0, 0)
            return

        self.d_confirmTeleport(avatar.doId, True, [[area.parentId, area.zoneId]], instance.doId, area.doId)

    def teleportComplete(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar or avatar.doId not in self.teleporting:
            self.d_confirmTeleport(avatar.doId, False, [], 0, 0)
            return

        area = self.air.doId2do.get(self.teleporting[avatar.doId][1])

        if not area:
            self.d_confirmTeleport(avatar.doId, False, [], 0, 0)
            return

        avatar.b_setLocation(area.doId, PiratesGlobals.IslandLocalZone)

        del self.teleporting[avatar.doId]
        self.sendUpdateToAvatarId(avatar.doId, 'teleportCleanup', [])

    def d_confirmTeleport(self, avatarId, success, worldLocations, worldDoId, areaDoId):
        self.sendUpdateToAvatarId(avatarId, 'confirmTeleport', [success, worldLocations, worldDoId, areaDoId])
