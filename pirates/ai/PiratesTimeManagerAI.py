from otp.ai.TimeManagerAI import TimeManagerAI
from direct.directnotify import DirectNotifyGlobal

class PiratesTimeManagerAI(TimeManagerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesTimeManagerAI')

    def setFrameRate(self, fps, deviation, numAvs, numShips, locationCode, timeInLocation, timeInGame, gameOptionsCode, vendorId, deviceId, processMemory, pageFileUsage, physicalMemory, pageFaultCount, osInfo, cpuSpeed, numCpuCores, numLogicalCpus, apiName):
        pass
