from direct.distributed.DistributedObject import DistributedObject
from pirates.band import BandConstance
from pirates.piratesbase import PLocalizer

class DistributedPirateBandManager(DistributedObject):
    notify = directNotify.newCategory('PirateBandManager')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

    def generate(self):
        DistributedObject.generate(self)
        base.cr.PirateBandManager = self

    def disable(self):
        DistributedObject.disable(self)
        base.cr.PirateBandManager = None
        return

    def d_requestInvite(self, avatarId):
        self.sendUpdate('requestInvite', [avatarId])

    def d_requestRejoin(self, avatarId, isManager):
        self.sendUpdate('requestRejoin', [avatarId, isManager])

    def d_requestCancel(self, avatarId):
        self.sendUpdate('requestCancel', [avatarId])

    def requestOutCome(self, avatarId, avatarName, responce):
        if responce == 0:
            if len(localAvatar.guiMgr.crewHUD.crew) <= 1 and localAvatar.getLookingForCrew() == 1:
                localAvatar.toggleLookingForCrewSign()
            messenger.send('BandAdded-%s' % (avatarId,), [avatarId])
        else:
            if responce != BandConstance.outcome_already_invited:
                localAvatar.guiMgr.crewHUD.removePotentialCrew(avatarId)
            messenger.send('BandRequestRejected-%s' % (avatarId,), [avatarId, responce])

    def invitationFrom(self, avatarId, avatarName):
        messenger.send(BandConstance.BandInvitationEvent, [avatarId, avatarName])

    def rejoinFrom(self, avatarId, isManager, version):
        messenger.send(BandConstance.BandRejoinEvent, [avatarId, isManager, version])

    def invitationCancel(self, avatarId):
        messenger.send('BandRequestCancel-%s' % (avatarId,), [])

    def rejoinCancel(self, avatarId):
        messenger.send('BandRejoinCancel-%s' % (avatarId,), [])

    def d_invitationResponce(self, avatarId, avatarName, responce):
        if responce == 0 and len(localAvatar.guiMgr.crewHUD.crew) == 0 and localAvatar.getLookingForCrew() == 1:
            localAvatar.toggleLookingForCrewSign()
        self.sendUpdate('invitationResponce', [avatarId, avatarName, responce])

    def d_rejoinResponce(self, avatarId, isManager, responce):
        if responce == 0 and len(localAvatar.guiMgr.crewHUD.crew) == 0 and localAvatar.getLookingForCrew() == 1:
            localAvatar.toggleLookingForCrewSign()
        self.sendUpdate('rejoinResponce', [avatarId, isManager, responce])

    def d_requestBoot(self, avatarId):
        self.sendUpdate('requestBoot', [avatarId])

    def d_requestRemove(self, avatarId):
        self.sendUpdate('requestRemove', [avatarId])

    def d_requestRejoinCheck(self, avatarId):
        self.sendUpdate('requestRejoinCheck', [avatarId])

    def d_requestCrewIconUpdate(self, iconKey):
        self.sendUpdate('requestCrewIconUpdate', [iconKey])

    def receiveUpdatedCrewIcon(self, iconKey):
        base.localAvatar.setCrewIcon(iconKey)

    def receiveBootTeleport(self, avId, avName):
        base.localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewBootTeleport, name=avName, avId=avId, icon=('ship',
                                                                                                                       ''))
        base.cr.teleportMgr.d_requestIslandTeleport(base.localAvatar.getReturnLocation(), skipConfirm=True)

    def receiveBootSuccess(self, avId, avName):
        base.localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewBootSuccess, name=avName, avId=avId, icon=('ship',
                                                                                                                      ''))