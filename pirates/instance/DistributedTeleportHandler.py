from direct.task import Task
from direct.distributed.DistributedObject import DistributedObject
from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals
from pirates.world.DistributedGameArea import DistributedGameArea
from pirates.world.DistributedOceanGrid import DistributedOceanGrid
from pirates.instance.DistributedInstanceBase import DistributedInstanceBase
from pirates.instance.DistributedMainWorld import DistributedMainWorld
from pirates.distributed.PiratesDistrict import PiratesDistrict
from pirates.piratesbase import PLocalizer

class DistributedTeleportHandler(DistributedObject):
    notify = directNotify.newCategory('DistributedTeleportHandler')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.destWorldGrid = None
        self.destInstance = None
        self.numInterestsCleared = 0
        self.pendingWorld = None
        self.spawnWorldName = None
        self.instanceWorldName = None
        self.doneCallback = None
        self.miniLog = MiniLog('DistributedTeleportHandler')

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.doId)

    def generate(self):
        DistributedObject.generate(self)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def disable(self):
        if self.pendingWorld:
            self.cr.relatedObjectMgr.abortRequest(self.pendingWorld)
            self.pendingWorld = None
        self.ignoreAll()
        DistributedObject.disable(self)
        return

    def getRemoveInterestEventName(self):
        return self.uniqueName('teleportRemoveInterest')

    def getAddInterestEventName(self):
        return self.uniqueName('teleportAddInterest')

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def startTeleport(self):
        s = MiniLogSentry(self.miniLog, 'startTeleport')
        bandId = localAvatar.getBandId()
        if bandId == None:
            bandId = 0
        elif bandId != 0:
            bandId = bandId[1]
        self.sendUpdate('startTeleportProcess', [0, 0, bandId])
        return

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def waitInTZ(self, objIds, destParentId):
        s = MiniLogSentry(self.miniLog, 'waitInTZ', objIds, destParentId)
        self.otherTeleportingObjIds = objIds
        parent = localAvatar.getParentObj()
        if parent:
            parentsParent = parent.getParentObj()
            if isinstance(parentsParent, DistributedInstanceBase):
                parentsParent.removeWorldInterest()
        elif self.cr.activeWorld:
            self.notify.warning('***JCW*** localAvatar has no parentObj, but has activeWorld: %s,%s' % (self.cr.activeWorld.__class__.__name__, self.cr.activeWorld.doId))
            self.cr.activeWorld.removeWorldInterest()
        else:
            self.notify.warning('***JCW*** localAvatar has no parentObj, and has no activeWorld')

        self.waitInTZ2(0, 0)

    def waitInTZ2(self, destParentId, destZoneId):
        s = MiniLogSentry(self.miniLog, 'waitInTZ2', destParentId, destZoneId)
        destParentId, destZoneId = self.getLocation()[0], localAvatar.doId
        base.loadingScreen.endStep('beginTeleport')
        base.loadingScreen.beginStep('enterArea', 29, 80)
        localAvatar.b_setLocation(destParentId, destZoneId)
        self.teleportingObjAtDest(destParentId, destZoneId, self.teleportRemoveInterestCompleteTZ)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def teleportingObjAtDest(self, destParentId, destZoneId, callback, clearInterest=True):
        s = MiniLogSentry(self.miniLog, 'teleportingObjAtDest', destParentId, destZoneId, callback.__name__, clearInterest)
        if clearInterest:
            leaveEvent = self.getRemoveInterestEventName()
            numInterests = localAvatar.clearInterestNamed(leaveEvent, ['instanceInterest', 'worldInterest'])
            localAvatar.clearInterestNamed(leaveEvent + 'Door', ['instanceInterest-Door'])
            self.numInterestsCleared = 0
            if numInterests == 0:
                callback(destZoneId, numInterests)
            else:
                self.accept(leaveEvent, callback, extraArgs=[destZoneId, numInterests])
        else:
            callback()

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def teleportRemoveInterestCompleteTZ(self, zoneId, numInterests):
        s = MiniLogSentry(self.miniLog, 'teleportRemoveInterestCompleteTZ', zoneId, numInterests)
        self.numInterestsCleared += 1
        if self.numInterestsCleared < numInterests:
            return

        self.accept('shardSwitchComplete', self.shardSwitchComplete, [zoneId])
        district = self.getParentObj()
        self.cr.distributedDistrict = district
        self.cr.alterInterest(self.cr.uberZoneInterest, district.getDoId(), 2, event='shardSwitchComplete')

    def shardSwitchComplete(self, zoneId):
        s = MiniLogSentry(self.miniLog, 'shardSwitchComplete', zoneId)
        self.oldWorld = base.cr.activeWorld

        def clockSyncComplete():
            self.sendUpdate('teleportToInstanceReady', [zoneId])

        if base.cr.timeManager and base.cr.timeManager.gotInitialTimeSync():
            clockSyncComplete()
        else:
            self.acceptOnce('gotTimeSync', clockSyncComplete)

    @report(types=['args', 'deltaStamp', 'printInterests'], dConfigParam='teleport')
    def continueTeleportToInstance(self, instanceParent, instanceZone, instanceDoId, instanceFileName, spawnParent, spawnZone, spawnDoId, spawnFileName, spawnWorldGridDoId):
        s = MiniLogSentry(self.miniLog, 'continueTeleportToInstance', instanceParent, instanceZone, instanceDoId, instanceFileName, spawnParent, spawnZone, spawnDoId, spawnFileName, spawnWorldGridDoId)
        self.spawnWorldName = spawnFileName + '.py'
        base.worldCreator.fileDicts = {}
        base.worldCreator.registerFileObject(self.spawnWorldName)
        base.worldCreator.registerFileObject(instanceFileName + '.py')
        base.worldCreator.loadFileDataRecursive(instanceFileName + '.py')
        self.instanceWorldName = None
        if instanceFileName:
            self.instanceWorldName = instanceFileName + '.py'

        localAvatar.setInterest(instanceParent, instanceZone, ['worldInterest'])

        def worldArrived(worldObj):
            s = MiniLogSentry(self.miniLog, 'worldArrived', worldObj)
            self.destInstance = worldObj
            self.teleportAddInterestWorldComplete(worldObj, spawnParent, spawnZone, spawnDoId, spawnWorldGridDoId, self.spawnWorldName)

        if self.pendingWorld:
            self.cr.relatedObjectMgr.abortRequest(self.pendingWorld)

        self.pendingWorld = self.cr.relatedObjectMgr.requestObjects([instanceDoId], eachCallback=worldArrived)

    @report(types=['args', 'deltaStamp', 'printInterests'], dConfigParam='teleport')
    def teleportAddInterestWorldComplete(self, instance, spawnParent, spawnZone, spawnDoId, spawnWorldGridDoId, worldName):
        s = MiniLogSentry(self.miniLog, 'teleportAddInterestWorldComplete', instance, spawnParent, spawnZone, spawnDoId, spawnWorldGridDoId, worldName)
        addEvent = self.getAddInterestEventName()
        if instance.doId != spawnDoId:
            instance.removeWorldInterest()

        self.acceptOnce(addEvent, self.teleportAddInterestDestComplete, extraArgs=[spawnDoId, spawnWorldGridDoId, worldName])
        localAvatar.setInterest(spawnParent, spawnZone, ['instanceInterest'], addEvent)

    @report(types=['args', 'deltaStamp', 'printInterests'], dConfigParam='teleport')
    def teleportAddInterestDestComplete(self, spawnDoId, spawnWorldGridDoId, worldName):
        s = MiniLogSentry(self.miniLog, 'teleportAddInterestDestComplete', spawnDoId, spawnWorldGridDoId, worldName)
        base.cr.relatedObjectMgr.requestObjects([spawnDoId], eachCallback=lambda param1, param2=spawnWorldGridDoId, param3=spawnDoId, param4=worldName: self.teleportInstanceExists(param1, param2, param3, param4))

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def teleportInstanceExists(self, instanceObj, worldGridDoId, instanceDoId, worldName):
        s = MiniLogSentry(self.miniLog, 'teleportInstanceExists', instanceObj, worldGridDoId, instanceDoId, worldName)
        base.cr.relatedObjectMgr.requestObjects([worldGridDoId], eachCallback=lambda param1, param2=instanceDoId, param3=worldName: self.teleportWorldGridExists(param1, param2, param3))

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def teleportWorldGridExists(self, worldGridObj, instanceDoId, worldName):
        s = MiniLogSentry(self.miniLog, 'teleportWorldGridExists', worldGridObj, instanceDoId, worldName)
        oceanAreas = base.cr.distributedDistrict.worldCreator.getOceanData(worldName)
        if oceanAreas:
            for currArea in oceanAreas:
                worldGridObj.addOceanArea(*currArea[:4])

            worldGridObj.addOceanAreasToMap()

        self.teleportInstanceComplete(worldGridObj, instanceDoId)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def teleportInstanceComplete(self, worldGrid, instanceDoId):
        s = MiniLogSentry(self.miniLog, 'teleportInstanceComplete', worldGrid, instanceDoId)
        self.setDestWorldGrid(worldGrid)
        if base.cr.distributedDistrict.shardType == PiratesGlobals.SHARD_WELCOME:
            localAvatar.b_setTeleportFlag(PiratesGlobals.TFInWelcomeWorld)
        else:
            localAvatar.b_clearTeleportFlag(PiratesGlobals.TFInWelcomeWorld)

        self.sendUpdate('readyToFinishTeleport', [instanceDoId])

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def teleportToInstanceCleanup(self):
        s = MiniLogSentry(self.miniLog, 'teleportToInstanceCleanup')
        if self.destInstance == None or self.destInstance.spawnInfo == None:
            self.notify.warning('no local destInstance reference for %s %s %s %s %s' % (localAvatar.doId, self.doId, self.getLocation(), self.spawnWorldName, self.instanceWorldName))
            self.sendAvatarLeft()
            self.abortTeleport()
            return

        self.spawnPos, zoneId, parents = self.destInstance.spawnInfo
        self.cr.teleportMgr.miniLog = self.miniLog
        self.cr.teleportMgr.createSpawnInterests(parents, self.teleportToInstanceCleanup3, self.destWorldGrid, localAvatar)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def teleportToInstanceCleanup3(self, parentObj, teleportingObj):
        s = MiniLogSentry(self.miniLog, 'teleportToInstanceCleanup3', parentObj, teleportingObj)
        if isinstance(parentObj, DistributedOceanGrid):
            self.miniLog.appendLine('being placed on the ocean')
            logBlock(5, self.miniLog)

        self.cr.teleportMgr.localTeleportToId(parentObj.doId, teleportingObj, self.spawnPos)
        if isinstance(parentObj, DistributedGameArea):
            self.destInstance.addWorldInterest(parentObj)
        else:
            self.destInstance.addWorldInterest()

        messenger.send('localAvatarExitWater')
        currParentId, currZoneId = teleportingObj.getLocation()
        self.teleportingObjAtDest(currParentId, currZoneId, self.teleportCleanupComplete, False)
        self.oldWorld = None

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def teleportCleanupComplete(self):
        s = MiniLogSentry(self.miniLog, 'teleportCleanupComplete')
        self.cr.activeWorld.setWorldGrid(self.destWorldGrid)
        localAvatar.teleportCleanupComplete(self.instanceType)
        self.sendUpdate('teleportToInstanceFinal', [localAvatar.getDoId()])
        self.clearTZInterest()

    def clearTZInterest(self):
        s = MiniLogSentry(self.miniLog, 'clearTZInterest')
        localAvatar.clearInterestNamed(None, ['TZInterest'])
        if self.doneCallback:
            self.doneCallback(self.destInstance)
            self.doneCallback = None

        messenger.send('localAvTeleportFinished')
        base.cr.teleportMgr.clearAmInTeleport()
        if self.destInstance:
            self.destInstance.queryActiveQuests()

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def setDestWorldGrid(self, worldGrid):
        s = MiniLogSentry(self.miniLog, 'setDestWorldGrid', worldGrid)
        self.destWorldGrid = worldGrid

    def abortTeleport(self):
        s = MiniLogSentry(self.miniLog, 'abortTeleport')
        self.notify.debug('%s: abortTeleport called' % self.doId)
        self.clearTZInterest()
        base.cr.teleportMgr.failTeleport(message=PLocalizer.TeleportGenericFailMessage)

    def sendAvatarLeft(self):
        s = MiniLogSentry(self.miniLog, 'sendAvatarLeft')
        self.sendUpdate('avatarLeft')
