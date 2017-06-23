from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.piratesgui import PiratesConfirm
from pirates.piratesgui import PiratesInfo
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import CrewMatchInvitee
from pirates.piratesgui import CrewMatchNewMemberRequest
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.band import CrewMatchHandle

class DistributedCrewMatchManager(DistributedObjectGlobal):
    notify = directNotify.newCategory('DistributedCrewMatchManager')

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
        self.offerRequestCache = []
        self.offerCurrentlyOnScreen = False
        self.crewType = 1
        self.confirmBox = None
        self.handleDict = {}
        return

    def generate(self):
        DistributedObjectGlobal.generate(self)

    def disable(self):
        DistributedObjectGlobal.disable(self)

    def addCrewToLookoutList(self, range, sailValue, cannonValue):
        if base.cr.distributedDistrict and base.localAvatar.getParentObj() and base.cr.getActiveWorld():
            self.sendUpdate('requestCrewAdd', [range, sailValue, cannonValue, base.cr.distributedDistrict.doId, localAvatar.getParentObj().doId, base.cr.getActiveWorld().doId])
        else:
            base.localAvatar.guiMgr.crewHUD.b_deactivateCrewLookout()

    def changeCrewLookoutOptions(self, range, sailValue, cannonValue):
        self.sendUpdate('requestCrewChangeOptions', [range, sailValue, cannonValue])

    def deleteCrewFromLookoutList(self):
        self.sendUpdate('requestCrewDelete', [])

    def responseCrewAdd(self, responseCode):
        self.notify.debug('responseCrewAdd(%s)' % responseCode)

    def responseCrewDelete(self, response):
        self.notify.debug('responseCrewDelete(%s)' % response)

    def addAvatarToLookoutList(self, crewType):
        self.crewType = crewType
        self.sendUpdate('requestInitialAvatarAdd', [crewType])

    def responseInitialAvatarAdd(self, response, submitterName, crewOwnAvId, location, crewType):
        self.notify.debug('responseInitialAvatarAdd(%s, %s, %s, %s)' % (response, submitterName, crewOwnAvId, location))
        self.availableCrewSubmitterName = submitterName
        if response:
            self.confirmBox = CrewMatchInvitee.CrewMatchInvitee(crewOwnAvId, submitterName, location, True, crewType)
        else:
            if crewType == 1:
                self.stackMessage(PLocalizer.CrewMatchNoCrewFound)
            elif crewType == 2:
                self.stackMessage(PLocalizer.CrewMatchNoCrewFoundPVP)
            self.putAvatarOnLookoutList(crewType)

    def acceptInitialInviteGUI(self):
        self.sendUpdate('requestInitialAvatarAddResponse', [1, self.crewType])

    def putAvatarOnLookoutList(self, crewType):
        self.sendUpdate('requestPutAvatarOnLookoutList', [crewType])

    def deleteAvatarFromLookoutList(self):
        if self.crewType == 1:
            self.stackMessage(PLocalizer.CrewMatchRemoveAvatarFromLookout)
        elif self.crewType == 2:
            self.stackMessage(PLocalizer.CrewMatchRemoveAvatarFromLookoutPVP)
        self.sendUpdate('requestDeleteAvatarFromLookoutList', [])

    def responseCrewFound(self, sponsorName, crewOwnAvId, location):
        if not self.offerCurrentlyOnScreen:
            self.offerCurrentlyOnScreen = True
            self.availableCrew = crewOwnAvId
            self.notify.debug('responseCrewFound(%s, %s, %s)' % (sponsorName, crewOwnAvId, location))
            self.confirmBox = CrewMatchInvitee.CrewMatchInvitee(crewOwnAvId, sponsorName, location, False)
        else:
            self.offerRequestCache.append([sponsorName, crewOwnAvId, location])

    def responseCrewGone(self):
        if self.confirmBox:
            self.confirmBox.destroy()
            self.confirmBox = None
        self.stackMessage(PLocalizer.CrewMatchCrewGone)
        return

    def acceptInvite(self):
        self.sendUpdate('requestAcceptInvite', [self.availableCrew])

    def initialAvatarAddResponse(self, response):
        self.sendUpdate('requestInitialAvatarAddResponse', [response, self.crewType])

    def responseInitialAvatarAddResponse(self, response):
        self.notify.debug('responseInitialAvatarAddResponse(%s)' % response)
        if response == 0:
            self.stackMessage(PLocalizer.CrewMatchCrewNowUnavailable)
            self.offerCurrentlyOnScreen = False
            self.checkOfferCache()

    def checkOfferCache(self):
        if self.offerRequestCache:
            sponsorName, crewOwnAvId, location = self.offerRequestCache.pop()
            self.responseCrewFound(sponsorName, crewOwnAvId, location)

    def stackMessage(self, msg, name=None, avId=None):
        base.localAvatar.guiMgr.messageStack.addTextMessage(msg, seconds=15, priority=0, color=PiratesGuiGlobals.TextFG14, modelName='general_frame_f', icon=('crew',
                                                                                                                                                              ''), name=name, avId=avId)

    def requestCrewOfOne(self):
        self.sendUpdate('requestCrewOfOneCreation', [])

    def requestDeleteCrewOfOne(self):
        self.sendUpdate('requestCrewOfOneDelete', [])

    def notifySponsorNewMember(self, avId, avName):
        self.stackMessage(PLocalizer.CrewMatchAvatarAddedToYourCrew, name=avName, avId=avId)

    def notifyNewMemberAskingCrewLeader(self, avId, avName):
        self.stackMessage(PLocalizer.CrewMatchAskingCrewLeader, name=avName, avId=avId)

    def notifyNewMemberAccept(self, avId, avName):
        self.stackMessage(PLocalizer.CrewMatchAccept, name=avName, avId=avId)

    def notifyNewMemberDecline(self, avId, avName):
        self.stackMessage(PLocalizer.CrewMatchDecline, name=avName, avId=avId)

    def notifyNewMemberTeleport(self, avId, avName):
        self.stackMessage(PLocalizer.CrewMatchTeleport, name=avName, avId=avId)
        base.localAvatar.guiMgr.handleGotoAvatar(avId, avName)

    def notifyNewMemberTeleportToNewShard(self, avId, avName, shardId, locationId, instanceId):
        base.cr.crewMatchManager.addHandle(avId, avName)
        self.stackMessage(PLocalizer.CrewMatchTeleportShard, name=avName, avId=avId)
        base.cr.teleportMgr.queryAvatarForTeleport(avId)

    def responseNewMemberRequest(self, avId, avName, crewType, openCrew):
        confirmBox = CrewMatchNewMemberRequest.CrewMatchNewMemberRequest(avId, avName, crewType, openCrew)

    def requestNewMember(self, avId, avName, response, crewType, openCrew):
        if response:
            base.cr.crewMatchManager.addHandle(avId, avName)
        self.sendUpdate('requestNewMember', [avId, response, crewType, openCrew])

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def d_requestTeleportQuery(self, sendToId, localBandMgrId, localBandId, localGuildId, localShardId):
        self.sendUpdate('requestTeleportQuery', [sendToId, localBandMgrId, localBandId, localGuildId, localShardId])

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def d_requestTeleportResponse(self, sendToId, available, shardId, instanceDoId, areaDoId):
        self.sendUpdate('requestTeleportResponse', [sendToId, available, shardId, instanceDoId, areaDoId])

    def teleportQuery(self, requesterId, requesterBandMgr, requesterBandId, requesterGuildId, requesterShardId):
        bandMgr, bandId = localAvatar.getBandId() or (0, 0)
        self.cr.teleportMgr.handleAvatarTeleportQuery(requesterId, requesterBandMgr, requesterBandId, requesterGuildId, requesterShardId)

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def teleportResponse(self, responderId, available, shardId, instanceDoId, areaDoId):
        self.cr.teleportMgr.handleAvatarTeleportResponse(responderId, available, shardId, instanceDoId, areaDoId)

    def getHandle(self, doId):
        return self.handleDict.get(doId)

    def addHandle(self, doId, name):
        if doId == localAvatar.doId:
            return
        handle = self.handleDict.get(doId)
        if not handle:
            handle = CrewMatchHandle.CrewMatchHandle(doId, name)
            self.handleDict[doId] = handle
            taskMgr.doMethodLater(300, self.removeHandle, 'removeCrewMatchHandle%s' % doId, extraArgs=[doId])

    def removeHandle(self, doId):
        self.handleDict.pop(doId, 0)

    def requestRemoveHandle(self, doId):
        taskMgr.remove('removeCrewMatchHandle%s' % doId)
        self.removeHandle(doId)