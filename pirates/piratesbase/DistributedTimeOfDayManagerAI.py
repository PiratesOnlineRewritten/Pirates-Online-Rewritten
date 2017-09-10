from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase.TimeOfDayManagerBase import TimeOfDayManagerBase
from pirates.piratesbase import TODDefs
from direct.distributed.ClockDelta import globalClockDelta

class DistributedTimeOfDayManagerAI(DistributedObjectAI, TimeOfDayManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTimeOfDayManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        TimeOfDayManagerBase.__init__(self)

        self.cycleType = TODDefs.TOD_REGULAR_CYCLE
        self.cycleSpeed = 0
        self.startingNetTime = globalClockDelta.getRealNetworkTime(bits=32)
        self.timeOffset = 0
        self.isPaused = 0
        self.subList = []
        self.fromCurrent = 0
        self.startPhase = 0
        self.targetPhase = 0
        self.targetTime = 0
        self.isJolly = 0

    def syncTOD(self, cycleType, cycleSpeed, startingNetTime, timeOffset):
        self.cycleType = cycleType
        self.cycleSpeed = cycleSpeed
        self.startingNetTime = startingNetTime
        self.timeOffset = timeOffset

    def d_syncTOD(self, cycleType, cycleSpeed, startingNetTime, timeOffset):
        self.sendUpdate('syncTOD', [cycleType, cycleSpeed, startingNetTime, timeOffset])

    def b_syncTOD(self, cycleType, cycleSpeed, startingNetTime, timeOffset):
        self.syncTOD(cycleType, cycleSpeed, startingNetTime, timeOffset)
        self.d_syncTOD(cycleType, cycleSpeed, startingNetTime, timeOffset)

    def getSyncTOD(self):
        return [self.cycleType, self.cycleSpeed, self.startingNetTime, self.timeOffset]

    def setIsPaused(self, isPaused):
        self.isPaused = isPaused

    def d_setIsPaused(self, isPaused):
        self.sendUpdate('setIsPaused', [isPaused])

    def b_setIsPaused(self, isPaused):
        self.setIsPaused(isPaused)
        self.d_setIsPaused(isPaused)

    def getIsPaused(self):
        return self.isPaused

    def requestSync(self):
        pass

    def setEnvSubs(self, subList):
        self.subList = subList

    def d_setEnvSubs(self, subList):
        self.sendUpdate('setEnvSubs', [subList])

    def b_setEnvSubs(self, subList):
        self.setEnvSubs(subList)
        self.d_setEnvSubs(subList)

    def getEnvSubs(self):
        return self.subList

    def setMoonPhaseChange(self, fromCurrent, startPhase, targetPhase, targetTime):
        self.fromCurrent = fromCurrent
        self.startPhase = startPhase
        self.targetPhase = targetPhase
        self.targetTime = targetTime

    def d_setMoonPhaseChange(self, fromCurrent, startPhase, targetPhase, targetTime):
        self.sendUpdate('setMoonPhaseChange', [fromCurrent, startPhase, targetPhase, targetTime])

    def b_setMoonPhaseChange(self, fromCurrent, startPhase, targetPhase, targetTime):
        self.setMoonPhaseChange(fromCurrent, startPhase, targetPhase, targetTime)
        self.d_setMoonPhaseChange(fromCurrent, startPhase, targetPhase, targetTime)

    def getMoonPhaseChange(self):
        return [self.fromCurrent, self.startPhase, self.targetPhase, self.targetTime]

    def setMoonJolly(self, isJolly):
        self.isJolly = isJolly

    def d_setMoonJolly(self, isJolly):
        self.sendUpdate('setMoonJolly', [isJolly])

    def b_setMoonJolly(self, isJolly):
        self.setMoonJolly(isJolly)
        self.d_setMoonJolly(isJolly)

    def getMoonJolly(self):
        return self.isJolly
