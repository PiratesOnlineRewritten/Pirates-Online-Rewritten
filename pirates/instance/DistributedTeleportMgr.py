from pandac.PandaModules import *
from direct.task import Task
from direct.distributed import DistributedObject
from pirates.piratesbase import PiratesGlobals
from pirates.world import ZoneLOD
from direct.showbase.PythonUtil import report
from otp.otpbase import OTPLocalizer
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PDialog
from otp.otpgui import OTPDialog
from pirates.piratesgui.DownloadBlockerPanel import DownloadBlockerPanel
from pirates.quest import QuestDB, QuestLadderDB
from pirates.world import WorldGlobals
from pirates.ship.DistributedSimpleShip import DistributedSimpleShip

class DistributedTeleportMgr(DistributedObject.DistributedObject):
    notify = directNotify.newCategory('DistributedTeleportMgr')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.instanceType = None
        self.fromInstanceType = None
        self.lastLocalTeleportLoc = None
        self.teleportQueryId = None
        self.inInstanceType = PiratesGlobals.INSTANCE_MAIN
        self.instanceName = WorldGlobals.PiratesWorldSceneFileBase
        self.doneCallback = None
        self.startedCallback = None
        self.oldWorld = None
        self.requestData = None
        self.localTeleportId = None
        self.localTeleportingObj = None
        self.localTeleportCallback = None
        self.localTeleportDestPos = None
        self.popupDialog = None
        self.doEffect = False
        self.stowawayEffect = False
        self.miniLog = None
        self.teleportQueue = []
        self.teleportQueueProcess = None
        self.__teleportCallback = None

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        base.cr.teleportMgr = self

    def requestTeleportToFishingShip(self):
        self.cr.teleportMgr.sendUpdate('requestTeleportToFishingShip')

    def requestTeleportToFishingShip(self):
        self.cr.teleportMgr.sendUpdate('requestTeleportToFishingShip')

    @report(types=['args', 'deltaStamp'], dConfigParam=['teleport', 'shipboardreport'])
    def localTeleportToId(self, locationId, teleportingObj=None, destPos=None, callback=None, objectLocation=None, showLoadingScreen=True):
        if showLoadingScreen:
            self.cr.loadingScreen.show(waitForLocation=True)
        if locationId in base.cr.doId2do and base.cr.doId2do[locationId].dclass.getName() == 'DistributedOceanGrid':
            logBlock(1, 'localTeleportToId(%s,%s,%s,%s,%s,%s) to ocean grid\n\n' % (locationId, teleportingObj, destPos, callback, objectLocation, showLoadingScreen) + str(StackTrace()))
        self.localTeleportId = locationId
        self.localTeleportingObj = teleportingObj
        self.localTeleportCallback = callback
        self.localTeleportDestPos = destPos
        destObj = self.cr.doId2do.get(locationId)
        if destObj:
            self._localTeleportToIdInterestComplete()
            self.notify.debug('destination object %s found, teleporting to there now' % locationId)
        elif objectLocation:
            self._localTeleportToIdResponse(objectLocation[0], objectLocation[1])
            self.notify.debug('destination object %s not found, but location %s given' % (locationId, objectLocation))
        else:
            self.sendUpdate('requestTargetsLocation', [int(locationId)])
            self.notify.debug('destination object %s not found, querying AI for its location' % locationId)

    @report(types=['args', 'deltaStamp'], dConfigParam=['teleport', 'shipboardreport'])
    def _localTeleportToIdResponse(self, parentId, zoneId):
        if parentId != 0 and zoneId != 0:
            if self.cr.doId2do.get(parentId):
                localAvatar.setInterest(parentId, zoneId, ['localTeleportToId'], 'localTeleportToIdInterestAddComplete')
                self.acceptOnce('localTeleportToIdInterestAddComplete', self._localTeleportToIdInterestComplete)
                self.notify.debug('parent %s of destination object found, setting up interest' % parentId)
            else:
                self.notify.warning('parent %s of destination object not found, teleport failure' % parentId)
        else:
            self.failTeleport(parentId, zoneId)

    def failTeleport(self, parentId=None, zoneId=None, message=PLocalizer.TeleportToPlayerFailMessage):
        self.sendUpdate('requestClearPreventDamage')
        fallbackAreaId = localAvatar.getReturnLocation()
        if fallbackAreaId != '':
            areaDoId = base.cr.uidMgr.getDoId(fallbackAreaId)
            self.clearAmInTeleport()
            if areaDoId:
                destPos = base.cr.activeWorld.getPlayerSpawnPt(areaDoId)
                if destPos and self.localTeleportingObj:
                    self.localTeleportToId(areaDoId, self.localTeleportingObj, destPos)
                else:
                    self.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, WorldGlobals.PiratesWorldSceneFileBase, doEffect=False)
            else:
                self.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, WorldGlobals.PiratesWorldSceneFileBase, doEffect=False)
            self.__createDialog(message)
        else:
            self.notify.warning("  teleport to object (%s %s) AND 'return location' %s failed" % (parentId, zoneId, fallbackAreaId))

    def failTeleportRequest(self, reasonBit):
        if reasonBit >= 0:
            localAvatar.guiMgr.createWarning(PiratesGlobals.TFNoTeleportReasons.get(BitMask32.bit(reasonBit), PLocalizer.TeleportGenericFailMessage))
        else:
            self.__createDialog(PLocalizer.TeleportToPlayerFailMessage)

    def __cleanupDialog(self, value=None):
        if self.popupDialog:
            self.popupDialog.destroy()
            del self.popupDialog
            self.popupDialog = None

    def __createDialog(self, message):
        if message:
            popupDialogText = message
            if self.popupDialog:
                self.__cleanupDialog()
            self.popupDialog = PDialog.PDialog(text=popupDialogText, style=OTPDialog.Acknowledge, command=self.__cleanupDialog)

    @report(types=['deltaStamp'], prefix='------', dConfigParam=['want-teleport-report', 'want-shipboardreport'])
    def _localTeleportToIdInterestComplete(self):
        teleportToObj = self.cr.doId2do.get(self.localTeleportId)
        if not teleportToObj:
            self.sendUpdate('requestTargetsLocation', [self.localTeleportId])
            return
        curParent = localAvatar.getParentObj()
        parentIsZoneLOD = isinstance(curParent, ZoneLOD.ZoneLOD)
        if parentIsZoneLOD:
            localAvatar.leaveZoneLOD(curParent)
        if isinstance(teleportToObj, DistributedSimpleShip):
            if teleportToObj.gameFSM.getCurrentOrNextState() in ('PutAway', 'Sunk',
                                                                 'Sinking', 'Off'):
                self.failTeleport(0, 0, PLocalizer.TeleportToGoneShipFailMessage)
                return
            elif teleportToObj.gameFSM.getCurrentOrNextState() in ('InBoardingPosition',
                                                                   'OtherShipBoarded'):
                self.failTeleport(0, 0, PLocalizer.TeleportToBoardingShipFailMessage)
                return
            teleportToObj.setZoneLevel(3)
            teleportToObj.registerMainBuiltFunction(localAvatar.placeOnShip, [teleportToObj])
            teleportToObj.registerBuildCompleteFunction(teleportToObj.enableOnDeckInteractions)
            self.acceptOnce(teleportToObj.getParentObj().uniqueName('visibility'), self._localTeleportToIdDone)
            base.setLocationCode('Ship')
        else:
            self.notify.debug('teleporting obj position is %s' % self.localTeleportingObj.getPos())
            if not self.localTeleportDestPos or self.localTeleportDestPos == (0, 0,
                                                                              0,
                                                                              0,
                                                                              0,
                                                                              0):
                self.localTeleportDestPos = teleportToObj.getTeleportDestPosH()
            self.localTeleportingObj.setPosHpr(self.localTeleportDestPos[0], self.localTeleportDestPos[1], self.localTeleportDestPos[2], self.localTeleportDestPos[3], 0, 0)
            try:
                self.localTeleportingObj.reparentTo(teleportToObj)
            except TypeError, err:
                print 'teleportToObj:', teleportToObj
                raise err

            teleportToObj.addObjectToGrid(self.localTeleportingObj)
            self._localTeleportToIdDone()

    @report(types=['args', 'deltaStamp'], dConfigParam=['teleport', 'shipboardreport'])
    def _localTeleportToIdDone(self):
        self.cr.loadingScreen.scheduleHide(base.cr.getAllInterestsCompleteEvent())
        curParent = localAvatar.getParentObj()
        if isinstance(curParent, ZoneLOD.ZoneLOD):
            localAvatar.enterZoneLOD(curParent)

        if self.localTeleportCallback:
            self.localTeleportCallback()

        self.localTeleportId = None
        self.localTeleportingObj = None
        self.localTeleportCallback = None
        self.localTeleportDestPos = None
        localAvatar.guiMgr.socialPanel.updateAll()

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        messenger.send('destroyCrewMatchInvite')
        taskMgr.removeTasksMatching('teleportRemoveInterest')
        taskMgr.removeTasksMatching('teleportAddInterest')
        taskMgr.removeTasksMatching(self.uniqueName('localTeleportPos'))
        taskMgr.removeTasksMatching(self.uniqueName('fadeDone'))
        self.requestData = None
        self.ignoreAll()
        if base.cr.teleportMgr == self:
            base.cr.teleportMgr = None
        requestData = self.requestData
        self.requestData = None
        if self.teleportQueueProcess:
            taskMgr.remove(self.teleportQueueProcess)
        return

    @report(types=['args', 'deltaStamp'], dConfigParam=['teleport'])
    def requestTeleport(self, instanceType, instanceName, shardId=0, locationUid='', instanceDoId=0, doneCallback=None, startedCallback=None, gameType=-1, friendDoId=0, friendAreaDoId=0, doEffect=True):
        self.requestData = (
         (
          instanceType, instanceName), {'shardId': shardId,'locationUid': locationUid,'instanceDoId': instanceDoId,'doneCallback': doneCallback,'startedCallback': startedCallback,'gameType': gameType,'friendDoId': friendDoId,'friendAreaDoId': friendAreaDoId,'doEffect': doEffect})
        localAvatar.confirmTeleport(self.teleportConfirmation, feedback=True)

    def teleportConfirmation(self, confirmed):
        if confirmed:
            requestData = self.requestData
            self.initiateTeleport(*requestData[0], **requestData[1])
            locationUid = requestData[1]['locationUid']
            base.cr.loadingScreen.showTarget(locationUid)
            base.cr.loadingScreen.showHint(locationUid)
        self.requestData = None
        return

    @report(types=['args', 'deltaStamp'], dConfigParam=['teleport'])
    def requestTeleportToAvatar(self, shardId, instanceDoId, avatarId, avatarParentId):
        self.requestTeleport(PiratesGlobals.INSTANCE_MAIN, '', shardId, '', instanceDoId, friendDoId=avatarId, friendAreaDoId=avatarParentId)

    @report(types=['args', 'deltaStamp'], dConfigParam=['teleport'])
    def queryAvatarForTeleport(self, avId):
        self.setTeleportQueryId(avId)

        @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
        def teleportConfirmation(confirmed, avId=avId):
            if confirmed:
                handle = self.cr.identifyAvatar(avId)
                if handle:
                    shardId = self.cr.distributedDistrict.doId
                    bandMgr, bandId = localAvatar.getBandId() or (0, 0)
                    guildId = localAvatar.getGuildId()
                    handle.sendTeleportQuery(avId, bandMgr, bandId, guildId, shardId)

        localAvatar.confirmTeleport(teleportConfirmation, feedback=True)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def handleAvatarTeleportQuery(self, requesterId, requesterBandMgrId, requesterBandId, requesterGuildId, requesterShardId):
        handle = self.cr.identifyAvatar(requesterId)
        if not handle:
            return
        if self.cr.identifyFriend(requesterId) and (requesterId in localAvatar.ignoreList or self.cr.avatarFriendsManager.checkIgnored(requesterId)):
            handle.sendTeleportResponse(PiratesGlobals.encodeTeleportFlag(PiratesGlobals.TFIgnore), 0, 0, 0, sendToId=requesterId)
            return
        if localAvatar.ship and len(localAvatar.ship.crew) >= localAvatar.ship.getMaxCrew():
            handle.sendTeleportResponse(PiratesGlobals.encodeTeleportFlag(PiratesGlobals.TFOnShip), 0, 0, 0, sendToId=requesterId)
            return
        avName = handle.getName()

        @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
        def confirmed(canTeleportTo, avId, failedFlag, avName=avName):
            if canTeleportTo:
                if self.cr.getActiveWorld() and self.cr.distributedDistrict and localAvatar.getParentObj():
                    handle.sendTeleportResponse(PiratesGlobals.TAAvailable, self.cr.distributedDistrict.doId, self.cr.getActiveWorld().doId, localAvatar.getParentObj().doId, sendToId=requesterId)
                else:
                    handle.sendTeleportResponse(PiratesGlobals.encodeTeleportFlag(PiratesGlobals.TFUnavailable), 0, 0, 0, sendToId=requesterId)
            else:
                if localAvatar.failedTeleportMessageOk(requesterId):
                    localAvatar.setSystemMessage(requesterId, OTPLocalizer.WhisperFailedVisit % avName)
                handle.sendTeleportResponse(PiratesGlobals.encodeTeleportFlag(failedFlag), 0, 0, 0, sendToId=requesterId)

        localAvatar.confirmTeleportTo(confirmed, requesterId, avName, requesterBandMgrId, requesterBandId, requesterGuildId)

    @report(types=['args', 'deltaStamp'], dConfigParam=['teleport'])
    def handleAvatarTeleportResponse(self, avId, available, shardId, instanceDoId, areaDoId):
        if not avId == self.teleportQueryId:
            self.clearTeleportQueryId()
            return
        self.clearTeleportQueryId()
        handle = self.cr.identifyAvatar(avId)
        if handle:
            avName = handle.getName()
        else:
            return
        if available == PiratesGlobals.TAAvailable:
            self.requestTeleportToAvatar(shardId, instanceDoId, avatarId=avId, avatarParentId=areaDoId)
        else:
            flag = PiratesGlobals.decodeTeleportFlag(available)
            if flag == PiratesGlobals.TAIgnore:
                pass
            elif flag in PiratesGlobals.TFNoTeleportToReasons:
                localAvatar.guiMgr.createWarning(PiratesGlobals.TFNoTeleportToReasons[flag] % avName, duration=10)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def initiateTeleport(self, instanceType, instanceName, shardId=0, locationUid='', instanceDoId=0, doneCallback=None, startedCallback=None, gameType=-1, friendDoId=0, friendAreaDoId=0, doEffect=True, queue=False, stowawayEffect=False):
        if friendDoId:
            self.d_requestPlayerTeleport(friendDoId, shardId)
        else:
            self.d_requestInstanceTeleport(instanceType, instanceName)

        return
        currInteractive = base.cr.interactionMgr.getCurrentInteractive()
        if currInteractive:
            currInteractive.requestExit()
        if self.cr.activeWorld:
            fromInstanceType = self.cr.activeWorld.getType()
        else:
            fromInstanceType = PiratesGlobals.INSTANCE_NONE
        if instanceType not in [PiratesGlobals.INSTANCE_MAIN, PiratesGlobals.INSTANCE_WELCOME] and fromInstanceType not in [PiratesGlobals.INSTANCE_MAIN, PiratesGlobals.INSTANCE_GENERIC, PiratesGlobals.INSTANCE_NONE]:
            if not base.config.GetBool('can-break-teleport-rules', 0):
                import pdb
                pdb.set_trace()
                return
        if self.amInTeleport():
            if queue:
                self.queueInitiateTeleport(instanceType, instanceName, shardId, locationUid, instanceDoId, doneCallback, startedCallback, gameType, friendDoId, friendAreaDoId, doEffect, stowawayEffect)
                return
            return
        self.setAmInTeleport()
        if instanceType == PiratesGlobals.INSTANCE_MAIN and not locationUid:
            locationUid = localAvatar.getReturnLocation()
        localAvatar.teleportFriendDoId = friendDoId
        self.doEffect = doEffect
        self.stowawayEffect = stowawayEffect
        self.sendUpdate('initiateTeleport', [instanceType, fromInstanceType, shardId, locationUid, instanceDoId, instanceName, gameType, friendDoId, friendAreaDoId])
        self.doneCallback = doneCallback
        self.startedCallback = startedCallback
        self.teleportInit(instanceType, fromInstanceType, instanceName)

    def queueInitiateTeleport(self, instanceType, instanceName, shardId=0, locationUid='', instanceDoId=0, doneCallback=None, startedCallback=None, gameType=-1, friendDoId=0, friendAreaDoId=0, doEffect=True, stowawayEffect=False):
        teleInfo = [
         instanceType, instanceName, shardId, locationUid, instanceDoId, doneCallback, startedCallback, gameType, friendDoId, friendAreaDoId, doEffect, stowawayEffect]
        self.teleportQueue.append(teleInfo)

        def processTeleportQueue(task=None):
            if self.amInTeleport():
                return Task.again
            if not self.teleportQueue:
                return Task.done
            teleportInfo = self.teleportQueue.pop(0)
            self.initiateTeleport(*teleportInfo)
            if self.teleportQueue:
                return Task.again
            return Task.done

        self.teleportQueueProcess = taskMgr.doMethodLater(1, processTeleportQueue, 'processTeleportQueue')
        return

    def amInTeleport(self):
        return localAvatar.testTeleportFlag(PiratesGlobals.TFInTeleport)

    def setAmInTeleport(self):
        localAvatar.b_setTeleportFlag(PiratesGlobals.TFInTeleport)
        localAvatar.b_clearTeleportFlag(PiratesGlobals.TFLookoutJoined)

    def clearAmInTeleport(self):
        localAvatar.clearTeleportFlag(PiratesGlobals.TFInInitTeleport)
        localAvatar.b_clearTeleportFlag(PiratesGlobals.TFInTeleport)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def setTeleportQueryId(self, avId):
        self.teleportQueryId = avId

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def clearTeleportQueryId(self):
        self.teleportQueryId = 0

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def initiateTeleportAI(self, instanceType, instanceName):
        self.teleportInit(instanceType, instanceName)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def teleportInit(self, instanceType, fromInstanceType, instanceName, gameType=None):
        self.clearTeleportQueryId()
        self.oldWorld = base.cr.activeWorld
        self.instanceType = instanceType
        self.fromInstanceType = fromInstanceType
        self.instanceName = instanceName
        self.gameType = gameType
        self.miniLog = MiniLog('TeleportLog')
        MiniLogSentry(self.miniLog, 'teleportInit', instanceType, fromInstanceType, instanceName, gameType)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def teleportHasBegun(self, instanceType, fromInstanceType, instanceName, gameType):
        if not self.miniLog:
            self.miniLog = MiniLog('TeleportLog')
        s = MiniLogSentry(self.miniLog, 'teleportHasBegun', instanceType, fromInstanceType, instanceName, gameType)
        if self.startedCallback:
            self.startedCallback()
            self.startedCallback = None
        if self.oldWorld == None or self.oldWorld.isEmpty():
            self.teleportInit(instanceType, fromInstanceType, instanceName, gameType)
        return

    def getRemoveInterestEventName(self):
        return self.uniqueName('teleportRemoveInterest')

    def getAddInterestEventName(self):
        return self.uniqueName('teleportAddInterest')

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def forceTeleportStart(self, instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone):
        s = MiniLogSentry(self.miniLog, 'forceTeleportStart', instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone)
        self.setAmInTeleport()
        localAvatar.guiMgr.request('Cutscene')
        if not base.transitions.fadeOutActive():
            base.transitions.fadeOut()
        if self.fromInstanceType == PiratesGlobals.INSTANCE_MAIN:
            self.inInstanceType = PiratesGlobals.INSTANCE_MAIN
        else:
            self.inInstanceType = self.instanceType
        if self.fromInstanceType == PiratesGlobals.INSTANCE_PVP:
            localAvatar.clearTeleportFlag(PiratesGlobals.TFInPVP)
        elif self.fromInstanceType == PiratesGlobals.INSTANCE_TUTORIAL:
            localAvatar.clearTeleportFlag(PiratesGlobals.TFInTutorial)

        def fadeDone():
            base.cr.loadingScreen.show()
            s = MiniLogSentry(self.miniLog, 'fadeDone')
            curParent = localAvatar.getParentObj()
            parentIsZoneLOD = isinstance(curParent, ZoneLOD.ZoneLOD)
            if parentIsZoneLOD:
                localAvatar.leaveZoneLOD(curParent)
                curParent.turnOff()
            if self.cr.doId2do.get(tzParent) == None:
                self.failTeleport(None, None, PLocalizer.TeleportGenericFailMessage)
            else:
                self.teleportAddInterestTZ(instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone)
            return

        localAvatar.guiMgr.request('Interactive')
        taskMgr.removeTasksMatching(self.uniqueName('fadeDone'))
        taskMgr.doMethodLater(1, fadeDone, self.uniqueName('fadeDone'), extraArgs=[])

    def teleportAddInterestTZ(self, instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone):
        s = MiniLogSentry(self.miniLog, 'teleportAddInterestTZ', instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone)
        addEvent = self.getAddInterestEventName()
        self.accept(addEvent, self.teleportAddInterestCompleteTZ, extraArgs=[tzDoId, thDoId, worldGridDoId])
        localAvatar.setInterest(tzParent, tzZone, ['TZInterest'], addEvent)
        self.instanceName = instanceName

    def requestRespawn(self):
        self.sendUpdate('requestLocalTeleport')

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def teleportAddInterestCompleteTZ(self, tzDoId, thDoId, worldGridDoId):
        s = MiniLogSentry(self.miniLog, 'teleportAddInterestCompleteTZ', tzDoId, thDoId, worldGridDoId)
        base.cr.relatedObjectMgr.requestObjects([tzDoId], eachCallback=lambda param1, param2=thDoId: self.teleportZoneExists(param1, param2))

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def teleportZoneExists(self, teleportZone, thDoId):
        s = MiniLogSentry(self.miniLog, 'teleportZoneExists', teleportZone, thDoId)
        base.cr.relatedObjectMgr.requestObjects([thDoId], eachCallback=lambda param1, param2=teleportZone: self.teleportHandlerExists(param1, param2))

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def teleportHandlerExists(self, teleportHandler, teleportZone):
        s = MiniLogSentry(self.miniLog, 'teleportHandlerExists', teleportHandler, teleportZone)
        teleportHandler.instanceName = self.instanceName
        teleportHandler.instanceType = self.instanceType
        teleportHandler.doneCallback = self.doneCallback
        self.doneCallback = None
        teleportHandler.oldWorld = self.oldWorld
        self.oldWorld = None
        teleportHandler.miniLog = self.miniLog
        self.miniLog = None
        teleportHandler.startTeleport()
        return

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def createSpawnInterests(self, parents, callback, destGrid, teleportingObj):
        s = MiniLogSentry(self.miniLog, 'createSpawnInterests', parents, callback.__name__, destGrid, teleportingObj)
        parentsLen = len(parents)
        if self.miniLog:
            self.miniLog.appendLine('parents - %s' % (parents,))
            self.miniLog.appendLine('destGrid - %s' % (destGrid,))
        if parentsLen == 0:
            logBlock(2, self.miniLog)
            callback(destGrid, teleportingObj)
        else:
            parentObj = base.cr.doId2do.get(parents[0])
            if parentObj:
                callback(parentObj, teleportingObj)
            elif parentsLen > 2 and base.cr.doId2do.has_key(parents[2]):
                base.cr.relatedObjectMgr.requestObjects([parents[0]], eachCallback=lambda param1=None, param2=teleportingObj: callback(param1, param2))
                localAvatar.setInterest(parents[2], parents[1], ['instanceInterest'])
            else:
                if parentsLen > 2:
                    parentParentId = parents[2]
                    parentParentZone = parents[1]
                else:
                    parentParentId = '<None Given>'
                    parentParentZone = '<None Given>'

                parentId = parents[0]
                self.notify.warning(('createSpawnInterests: parent %s of parent %s in zone %s ' + 'does not exist locally, aborting teleport') % (parentParentId, parentId, parentParentZone))
                self.failTeleport(None, None, PLocalizer.TeleportGenericFailMessage)

    def initiateCrossShardDeploy(self, shardId=0, islandUid='', shipId=0, doneCallback=None, startedCallback=None, doEffect=True):
        if not islandUid or not shipId:
            return
        currInteractive = base.cr.interactionMgr.getCurrentInteractive()
        if currInteractive:
            currInteractive.requestExit()
        if self.cr.activeWorld:
            fromInstanceType = self.cr.activeWorld.getType()
        else:
            fromInstanceType = PiratesGlobals.INSTANCE_NONE
        if self.amInTeleport():
            return
        self.setAmInTeleport()
        self.doEffect = doEffect
        self.sendUpdate('requestCrossShardDeploy', [shardId, islandUid, shipId])
        self.doneCallback = doneCallback
        self.startedCallback = startedCallback
        self.teleportInit(PiratesGlobals.INSTANCE_MAIN, fromInstanceType, 'Main World')

    def d_requestShardTeleport(self, shardId, skipConfirm=False):

        def teleportConfirmation(confirmed):
            if confirmed:
                self.sendUpdate('requestShardTeleport', [shardId])

        if skipConfirm:
            teleportConfirmation(True)
        else:
            localAvatar.confirmTeleport(teleportConfirmation, feedback=True)

    def d_requestPlayerTeleport(self, targetAvId, shardId, skipConfirm=False):

        def teleportConfirmation(confirmed):
            if confirmed:
                self.sendUpdate('requestPlayerTeleport', [targetAvId, shardId])

        if skipConfirm:
            teleportConfirmation(True)
        else:
            localAvatar.confirmTeleport(teleportConfirmation, feedback=True)

    def d_requestIslandTeleport(self, islandUid, skipConfirm=False):

        def teleportConfirmation(confirmed):
            if confirmed:
                self.sendUpdate('requestIslandTeleport', [islandUid])

        if skipConfirm:
            teleportConfirmation(True)
        else:
            localAvatar.confirmTeleport(teleportConfirmation, feedback=True)

    def d_requestInstanceTeleport(self, instanceType, instanceName, skipConfirm=True):

        def teleportConfirmation(confirmed):
            if confirmed:
                self.sendUpdate('requestInstanceTeleport', [instanceType, instanceName])

        if skipConfirm:
            teleportConfirmation(True)
        else:
            localAvatar.confirmTeleport(teleportConfirmation, feedback=True)

    def notifyFriendVisit(self, avId):
        av = base.cr.identifyAvatar(avId)
        if av:
            avName = av.getName()
        else:
            avName = PLocalizer.Someone

        localAvatar.setSystemMessage(avId, OTPLocalizer.WhisperComingToVisit % avName)
        localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.WhisperComingToVisit % avName, icon=('friends', None))
