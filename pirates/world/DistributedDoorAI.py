from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.piratesbase import PiratesGlobals
from direct.distributed.ClockDelta import globalClockDelta

class DistributedDoorAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDoorAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)

        self.doorIndex = 0
        self.buildingUid = ''
        self.locked = 0
        self.otherDoorId = 0
        self.questNeeded = ''

    def handleRequestInteraction(self, avatar, interactType, instant):
        self.d_setMovie(PiratesGlobals.DOOR_OPEN, avatar.doId, globalClockDelta.getRealNetworkTime(bits=16))

        return self.ACCEPT

    def handleRequestExit(self, avatar):
        self.d_setMovie(PiratesGlobals.DOOR_CLOSED, avatar.doId, globalClockDelta.getRealNetworkTime(bits=16))

        return self.ACCEPT

    def setDoorIndex(self, doorIndex):
        self.doorIndex = doorIndex

    def d_setDoorIndex(self, doorIndex):
        self.sendUpdate('setDoorIndex', [doorIndex])

    def b_setDoorIndex(self, doorIndex):
        self.setDoorIndex(doorIndex)
        self.d_setDoorIndex(doorIndex)

    def getDoorIndex(self):
        return self.doorIndex

    def setBuildingUid(self, buildingUid):
        self.buildingUid = buildingUid

    def d_setBuildingUid(self, buildingUid):
        self.sendUpdate('setBuildingUid', [buildingUid])

    def b_setBuildingUid(self, buildingUid):
        self.setBuildingUid(buildingUid)
        self.d_setBuildingUid(buildingUid)

    def getBuildingUid(self):
        return self.buildingUid

    def d_setMovie(self, mode, avId, timestamp):
        self.sendUpdate('setMovie', [mode, avId, timestamp])

    def setLocked(self, locked):
        self.locked = locked

    def d_setLocked(self, locked):
        self.sendUpdate('setLocked', [locked])

    def b_setLocked(self, locked):
        self.setLocked(locked)
        self.d_setLocked(locked)

    def getLocked(self):
        return self.locked

    def setOtherDoorId(self, otherDoorId):
        self.otherDoorId = otherDoorId

    def d_setOtherDoorId(self, otherDoorId):
        self.sendUpdate('setOtherDoorId', [otherDoorId])

    def b_setOtherDoorId(self, otherDoorId):
        self.setOtherDoorId(otherDoorId)
        self.d_setOtherDoorId(otherDoorId)

    def getOtherDoorId(self):
        return self.otherDoorId

    def setQuestNeeded(self, questNeeded):
        self.questNeeded = questNeeded

    def d_setQuestNeeded(self, questNeeded):
        self.sendUpdate('setQuestNeeded', [questNeeded])

    def b_setQuestNeeded(self, questNeeded):
        self.setQuestNeeded(questNeeded)
        self.d_setQuestNeeded(questNeeded)

    def getQuestNeeded(self):
        return self.questNeeded
