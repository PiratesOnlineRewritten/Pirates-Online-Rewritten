import time
import random
from panda3d.core import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.distributed.PiratesInternalRepository import PiratesInternalRepository
from otp.distributed.OtpDoGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.distributed.PiratesDistrictAI import PiratesDistrictAI
from pirates.world import WorldGlobals
from pirates.piratesbase.UniqueIdManager import UniqueIdManager
from pirates.distributed.DistributedPopulationTrackerAI import DistributedPopulationTrackerAI
from pirates.ai.PiratesTimeManagerAI import PiratesTimeManagerAI
from pirates.instance.DistributedTeleportMgrAI import DistributedTeleportMgrAI
from pirates.piratesbase.DistributedTimeOfDayManagerAI import DistributedTimeOfDayManagerAI
from pirates.distributed.TargetManagerAI import TargetManagerAI
from pirates.battle.DistributedEnemySpawnerAI import DistributedEnemySpawnerAI
from pirates.world.WorldCreatorAI import WorldCreatorAI

class PiratesAIRepository(PiratesInternalRepository):
    notify = directNotify.newCategory('PiratesAIRepository')
    notify.setInfo(True)

    def __init__(self, baseChannel, serverId, districtName):
        PiratesInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='AI')

        self.districtName = districtName
        self.zoneAllocator = UniqueIdAllocator(PiratesGlobals.DynamicZonesBegin, PiratesGlobals.DynamicZonesEnd)
        self.zoneId2owner = {}
        self.uidMgr = UniqueIdManager(self)

    def handleConnected(self):
        self.districtId = self.allocateChannel()
        self.distributedDistrict = PiratesDistrictAI(self)
        self.distributedDistrict.setName(self.districtName)
        self.distributedDistrict.setMainWorld(WorldGlobals.PiratesWorldSceneFile)
        self.distributedDistrict.generateWithRequiredAndId(self.districtId, self.getGameDoId(), 2)
        self.setAI(self.districtId, self.ourChannel)

        self.createGlobals()
        self.createZones()

        self.distributedDistrict.b_setAvailable(1)
        self.notify.info('District is now ready.')

    def incrementPopulation(self):
        pass

    def decrementPopulation(self):
        pass

    def allocateZone(self, owner=None):
        zoneId = self.zoneAllocator.allocate()
        if owner:
            self.zoneId2owner[zoneId] = owner

        return zoneId

    def deallocateZone(self, zone):
        if self.zoneId2owner.get(zone):
            del self.zoneId2owner[zone]

        self.zoneAllocator.free(zone)

    def getAvatarExitEvent(self, avId):
        return 'distObjDelete-%d' % avId

    def createGlobals(self):
        """
        Create "global" objects, e.g. TimeManager et al.
        """

        self.populationTracker = DistributedPopulationTrackerAI(self)
        self.populationTracker.setShardId(self.districtId)
        self.populationTracker.setPopLimits(config.GetInt('shard-pop-limit-low', 100), config.GetInt('shard-pop-limit-high', 300))
        self.populationTracker.generateWithRequiredAndId(self.allocateChannel(), self.getGameDoId(), OTP_ZONE_ID_DISTRICTS_STATS)

        self.timeManager = PiratesTimeManagerAI(self)
        self.timeManager.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.travelAgent = self.generateGlobalObject(OTP_DO_ID_PIRATES_TRAVEL_AGENT, 'DistributedTravelAgent')

        self.teleportMgr = DistributedTeleportMgrAI(self)
        self.teleportMgr.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.timeOfDayMgr = DistributedTimeOfDayManagerAI(self)
        self.timeOfDayMgr.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.targetMgr = TargetManagerAI(self)
        self.targetMgr.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.spawner = DistributedEnemySpawnerAI(self)
        self.spawner.generateWithRequired(OTP_ZONE_ID_MANAGEMENT)

        self.inventoryManager = self.generateGlobalObject(OTP_DO_ID_PIRATES_INVENTORY_MANAGER, 'DistributedInventoryManager')

    def createZones(self):
        """
        Create "zone" objects, e.g. DistributedOceanGrid et al.
        """

        self.worldCreator = WorldCreatorAI(self)
        self.worldCreator.loadObjectsFromFile(WorldGlobals.PiratesWorldSceneFile)
