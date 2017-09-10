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
            self.notify.warning('An unknown avatar requested teleport to instance %d %s' %
                instanceType, instanceName)

            self.d_confirmTeleport(avatar.doId, False, [], 0, 0)
            return

        instance = self.air.worldCreator.world
        area = instance.uidMgr.justGetMeMeObject('1150922126.8dzlu')

        self.teleporting[avatar.doId] = [instance.doId, area.doId]
        self.d_confirmTeleport(avatar.doId, True, [[instance.parentId, instance.zoneId]], instance.doId, area.doId)

    def teleportInterestShard(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        instanceDoId, areaDoId = self.teleporting.get(avatar.doId)
        instance = self.air.doId2do.get(instanceDoId)
        area = self.air.doId2do.get(areaDoId)

        if not area or not instance:
            self.notify.warning('Failed to add teleport shard interest unable to find instance and/or area objects %d %d!' %
                instance.doId, area.doId)

            self.d_confirmTeleport(avatar.doId, False, [], 0, 0)
            return

        self.d_confirmTeleport(avatar.doId, True, [[area.parentId, area.zoneId]], instance.doId, area.doId)

    def teleportComplete(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        instanceDoId, areaDoId = self.teleporting.pop(avatar.doId)
        area = self.air.doId2do.get(areaDoId)

        if not area:
            self.notify.warning('Failed to complete teleport for avatar %d with unknown area doId %d!' %
                avatar.doId, area.doId)

            return

        avatar.b_setLocation(area.doId, PiratesGlobals.IslandLocalZone)

    def d_confirmTeleport(self, avatarId, success, worldLocations, worldDoId, areaDoId):
        self.sendUpdateToAvatarId(avatarId, 'confirmTeleport', [success, worldLocations, worldDoId, areaDoId])
