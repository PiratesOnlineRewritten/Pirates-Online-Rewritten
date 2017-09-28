from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals
from pirates.world.LocationConstants import LocationIds
from direct.fsm.FSM import FSM
from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from pirates.world.DistributedIslandAI import DistributedIslandAI
from pirates.instance.DistributedTeleportZoneAI import DistributedTeleportZoneAI
from pirates.instance.DistributedTeleportHandlerAI import DistributedTeleportHandlerAI

class TeleportFSM(FSM):

    def __init__(self, teleportMgr, avatar, world, instance, spawnPt):
        self.teleportMgr = teleportMgr
        self.avatar = avatar
        self.world = world
        self.instance = instance
        self.spawnPt = spawnPt

        FSM.__init__(self, self.__class__.__name__)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterStart(self):
        self.teleportZone = DistributedTeleportZoneAI(self.teleportMgr.air)
        self.teleportZone.generateWithRequired(self.teleportMgr.air.allocateZone())

        self.teleportHandler = DistributedTeleportHandlerAI(self.teleportMgr.air, self.teleportMgr, self, self.avatar)
        self.teleportHandler.generateWithRequired(self.teleportZone.zoneId)

        self.avatar.d_forceTeleportStart(self.world.getFileName(), self.teleportZone.doId, self.teleportHandler.doId, 0,
            self.teleportZone.parentId, self.teleportZone.zoneId)

    def exitStart(self):
        pass

    def enterStop(self):
        self.teleportZone.requestDelete()
        self.teleportHandler.requestDelete()

        del self.teleportMgr.avatar2fsm[self.avatar.doId]
        self.demand('Off')

    def exitStop(self):
        pass

class DistributedTeleportMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportMgrAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.avatar2fsm = {}

    def getWorld(self, instanceType, instanceName):
        for object in self.air.doId2do.values():
            if not object or not isinstance(object, DistributedInstanceBaseAI):
                continue

            if object.getType() == instanceType and object.getFileName() == instanceName:
                return object

        return None

    def requestInstanceTeleport(self, instanceType, instanceName):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.notify.warning('Cannot teleport non-existant avatar to instance %d %s!' % (instanceType, instanceName))
            return

        self.initiateTeleport(avatar, instanceType=instanceType, instanceName=instanceName)

    def requestIslandTeleport(self, islandUid):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.notify.warning('Cannot teleport non-existant avatar to island %s!' % islandUid)
            return

        self.initiateTeleport(avatar, islandUid=islandUid)

    def initiateTeleport(self, avatar, instanceType=None, instanceName=None, islandUid=LocationIds.PORT_ROYAL_ISLAND, spawnPt=None):
        if avatar.doId in self.avatar2fsm:
            self.notify.warning('Cannot initiate teleport for %d, already teleporting!' % avatar.doId)
            self.d_failTeleportRequest(avatar.doId, PiratesGlobals.TFInTeleport)
            return

        instance = avatar.getParentObj()

        if instance and instance.getUniqueId() == islandUid:
            self.notify.warning('Cannot initiate teleport for %d, already there!' % avatar.doId)
            self.d_failTeleportRequest(avatar.doId, PiratesGlobals.TFSameArea)
            return

        if instanceType is None and instanceName is None:
            world = instance.getParentObj() if instance else None
        else:
            world = self.getWorld(instanceType, instanceName)

        if not world or not isinstance(world, DistributedInstanceBaseAI):
            self.notify.warning('Cannot initiate teleport for %d unknown world %d %s!' % (avatar.doId,
                instanceType, instanceName))

            return

        instance = world.uidMgr.justGetMeMeObject(islandUid)

        if not instance or not isinstance(instance, DistributedIslandAI):
            self.notify.warning('Cannot initiate teleport for %d unknown instance!' % avatar.doId)
            return

        if not spawnPt:
            spawnPt = world.getSpawnPt(instance.getUniqueId())

        self.avatar2fsm[avatar.doId] = TeleportFSM(self, avatar, world, instance, spawnPt)
        self.avatar2fsm[avatar.doId].request('Start')

    def d_failTeleportRequest(self, avatarId, reasonBit):
        self.sendUpdateToAvatarId(avatarId, 'failTeleportRequest', [reasonBit.getHighestOnBit()])
