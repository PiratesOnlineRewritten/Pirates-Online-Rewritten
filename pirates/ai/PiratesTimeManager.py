from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from otp.avatar.Avatar import Avatar
from otp.ai.TimeManager import TimeManager
from pirates.ship.DistributedSimpleShip import DistributedSimpleShip
import time
import os

class PiratesTimeManager(TimeManager):

    def frameRateMonitor(self, task):
        from otp.avatar.Avatar import Avatar
        vendorId = 0
        deviceId = 0
        processMemory = 0
        pageFileUsage = 0
        physicalMemory = 0
        pageFaultCount = 0
        osInfo = (
         os.name, 0, 0, 0)
        cpuSpeed = (0, 0)
        numCpuCores = 0
        numLogicalCpus = 0
        apiName = 'None'
        if getattr(base, 'pipe', None):
            di = base.pipe.getDisplayInformation()
            if di.getDisplayState() == DisplayInformation.DSSuccess:
                vendorId = di.getVendorId()
                deviceId = di.getDeviceId()
            di.updateMemoryInformation()
            oomb = 1.0 / (1024.0 * 1024.0)
            processMemory = di.getProcessMemory() * oomb
            pageFileUsage = di.getPageFileUsage() * oomb
            physicalMemory = di.getPhysicalMemory() * oomb
            pageFaultCount = di.getPageFaultCount() / 1000.0
            osInfo = (os.name, di.getOsPlatformId(), di.getOsVersionMajor(), di.getOsVersionMinor())
            di.updateCpuFrequency(0)
            ooghz = 1e-09
            cpuSpeed = (di.getMaximumCpuFrequency() * ooghz, di.getCurrentCpuFrequency() * ooghz)
            if hasattr(di, 'getNumCpuCores'):
                numCpuCores = di.getNumCpuCores()
                numLogicalCpus = di.getNumLogicalCpus()
            apiName = base.pipe.getInterfaceName()
        self.d_setFrameRate(globalClock.getAverageFrameRate(), globalClock.calcFrameRateDeviation(), len(Avatar.ActiveAvatars), len(DistributedSimpleShip.ActiveShips), base.locationCode or '', time.time() - base.locationCodeChanged, globalClock.getRealTime(), base.gameOptionsCode, vendorId, deviceId, processMemory, pageFileUsage, physicalMemory, pageFaultCount, osInfo, cpuSpeed, numCpuCores, numLogicalCpus, apiName)
        return task.again

    def d_setFrameRate(self, fps, deviation, numAvs, numShips, locationCode, timeInLocation, timeInGame, gameOptionsCode, vendorId, deviceId, processMemory, pageFileUsage, physicalMemory, pageFaultCount, osInfo, cpuSpeed, numCpuCores, numLogicalCpus, apiName):
        info = '%0.1f fps|%0.3fd|%s avs|%s ships|%s|%d|%d|%s|0x%04x|0x%04x|%0.1fMB|%0.1fMB|%0.1fMB|%d|%s|%s|%s cpus|%s' % (fps, deviation, numAvs, numShips, locationCode, timeInLocation, timeInGame, gameOptionsCode, vendorId, deviceId, processMemory, pageFileUsage, physicalMemory, pageFaultCount, '%s.%d.%d.%d' % osInfo, '%0.03f,%0.03f' % cpuSpeed, '%d,%d' % (numCpuCores, numLogicalCpus), apiName)
        print 'frame rate: %s' % info
        self.sendUpdate('setFrameRate', [fps, deviation, numAvs, numShips, locationCode, timeInLocation, timeInGame, gameOptionsCode, vendorId, deviceId, processMemory, pageFileUsage, physicalMemory, pageFaultCount, osInfo, cpuSpeed, numCpuCores, numLogicalCpus, apiName])
