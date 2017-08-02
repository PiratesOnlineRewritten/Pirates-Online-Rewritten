import time
import random
from panda3d.core import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.distributed.PiratesInternalRepository import PiratesInternalRepository
from otp.distributed.OtpDoGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.distributed.PiratesDistrictAI import PiratesDistrictAI
from pirates.world import WorldGlobals
from pirates.ai.PiratesTimeManagerAI import PiratesTimeManagerAI

class PiratesAIRepository(PiratesInternalRepository):
    notify = directNotify.newCategory('PiratesUberRepository')
    notify.setInfo(True)

    def __init__(self, baseChannel, serverId, districtName):
        PiratesInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='AI')

        self.districtName = districtName
        self.zoneAllocator = UniqueIdAllocator(PiratesGlobals.DynamicZonesBegin, PiratesGlobals.DynamicZonesEnd)
        self.zoneId2owner = {}

    def handleConnected(self):
        self.districtId = self.allocateChannel()
        self.distributedDistrict = PiratesDistrictAI(self)
        self.distributedDistrict.setName(self.districtName)
        self.distributedDistrict.setMainWorld(WorldGlobals.PiratesWorldSceneFile)
        self.distributedDistrict.generateWithRequiredAndId(self.districtId, self.getGameDoId(), 2)

        # Claim ownership of that district...
        self.setAI(self.districtId, self.ourChannel)

        self.createGlobals()

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

        self.timeManager = PiratesTimeManagerAI(self)
        self.timeManager.generateWithRequired(2)

        self.travelAgent = self.generateGlobalObject(OTP_DO_ID_PIRATES_TRAVEL_AGENT, 'DistributedTravelAgent')
