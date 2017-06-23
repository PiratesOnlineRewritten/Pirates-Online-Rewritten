from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from otp.uberdog.RejectCode import RejectCode
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.battle.DistributedBattleNPC import DistributedBattleNPC
from pirates.band import BandConstance
from pirates.band import DistributedBandMember
from pirates.piratesgui.RequestButton import RequestButton

class CrewInviterButton(RequestButton):

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewInviterButton)


class CrewInviter(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('CrewInviter')

    def __init__(self):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief=None, pos=(-0.6, 0, 0.47), image=guiMain.find('**/general_frame_e'), image_pos=(0.25,
                                                                                                                          0,
                                                                                                                          0.275), image_scale=0.25)
        self.initialiseoptions(CrewInviter)
        self.avDisableName = ''
        self.fsm = ClassicFSM.ClassicFSM('CrewInviter', [
         State.State('off', self.enterOff, self.exitOff),
         State.State('begin', self.enterBegin, self.exitBegin),
         State.State('tooMany', self.enterTooMany, self.exitTooMany),
         State.State('notYet', self.enterNotYet, self.exitNotYet),
         State.State('checkAvailability', self.enterCheckAvailability, self.exitCheckAvailability),
         State.State('notAvailable', self.enterNotAvailable, self.exitNotAvailable),
         State.State('notAcceptingCrews', self.enterNotAcceptingCrews, self.exitNotAcceptingCrews),
         State.State('wentAway', self.enterWentAway, self.exitWentAway),
         State.State('alreadyCrewed', self.enterAlreadyCrewed, self.exitAlreadyCrewed),
         State.State('alreadyInvited', self.enterAlreadyInvited, self.exitAlreadyInvited),
         State.State('recentlyInvited', self.enterRecentlyInvited, self.exitRecentlyInvited),
         State.State('askingNPC', self.enterAskingNPC, self.exitAskingNPC),
         State.State('endCrewship', self.enterEndCrewship, self.exitEndCrewship),
         State.State('crewedNoMore', self.enterCrewedNoMore, self.exitCrewedNoMore),
         State.State('leaveCrew', self.enterLeaveCrew, self.exitLeaveCrew),
         State.State('leftCrew', self.enterLeftCrew, self.exitLeftCrew),
         State.State('notCaption', self.enterNotCaption, self.exitNotCaption),
         State.State('inOtherCrew', self.enterInOtherCrew, self.exitInOtherCrew),
         State.State('self', self.enterSelf, self.exitSelf),
         State.State('ignored', self.enterIgnored, self.exitIgnored),
         State.State('asking', self.enterAsking, self.exitAsking),
         State.State('yes', self.enterYes, self.exitYes),
         State.State('no', self.enterNo, self.exitNo),
         State.State('otherTooMany', self.enterOtherTooMany, self.exitOtherTooMany),
         State.State('maybe', self.enterMaybe, self.exitMaybe),
         State.State('down', self.enterDown, self.exitDown),
         State.State('cancel', self.enterCancel, self.exitCancel)], 'off', 'off')
        self.title = DirectLabel(parent=self, relief=None, text=PLocalizer.CrewInviterTitle, text_scale=PiratesGuiGlobals.TextScaleExtraLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateOutlineFont(), pos=(0.25,
                                                                                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                                                                                               0.42), image=None, image_scale=0.25)
        self.message = DirectLabel(parent=self, relief=None, text='', text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.25,
                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                    0.325), textMayChange=1)
        self.context = None
        self.bOk = CrewInviterButton(text=PLocalizer.CrewInviterOK, command=self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.2, 0, 0.05)
        self.bOk.hide()
        self.bCancel = CrewInviterButton(text=PLocalizer.CrewInviterCancel, command=self.__handleCancel)
        self.bCancel.reparentTo(self)
        self.bCancel.setPos(0.2, 0, 0.05)
        self.bCancel.hide()
        self.bStop = CrewInviterButton(text=PLocalizer.CrewInviterStopBeingCrewed, command=self.__handleStop)
        self.bStop.reparentTo(self)
        self.bStop.setPos(0.2, 0, 0.15)
        self.bStop.hide()
        self.bYes = CrewInviterButton(text=PLocalizer.CrewInviterYes, command=self.__handleYes)
        self.bYes.reparentTo(self)
        self.bYes.setPos(0.1, 0, 0.05)
        self.bYes.hide()
        self.bNo = CrewInviterButton(text=PLocalizer.CrewInviterNo, command=self.__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.05)
        self.bNo.hide()
        return

    def inviteAvatar(self, avId, avName):
        self.avId = avId
        self.avName = avName
        handle = base.cr.identifyAvatar(avId)
        if handle:
            self.bandId = handle.getBandId()
            self.avDisableName = 'disable-%s' % avId
            self.accept(self.avDisableName, self.__handleDisableAvatar)
            self.fsm.enterInitialState()
            self.fsm.request('begin')
        else:
            self.fsm.request('wentAway')

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.fsm.request('off')
        del self.fsm
        if self.avDisableName:
            self.ignore(self.avDisableName)
        DirectFrame.destroy(self)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterBegin(self):
        if self.avId == localAvatar.doId:
            self.fsm.request('leaveCrew')
        elif self.bandId and self.bandId[0] != 0 and self.bandId[1] != 0 or DistributedBandMember.DistributedBandMember.getBandMember(self.avId):
            if DistributedBandMember.DistributedBandMember.areSameCrew(localAvatar.doId, self.avId):
                if DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand():
                    self.fsm.request('alreadyCrewed')
                else:
                    self.fsm.request('leaveCrew')
            else:
                self.fsm.request('inOtherCrew')
        else:
            localcrew = DistributedBandMember.DistributedBandMember.getBandSetLocalAvatar()
            if len(localcrew) >= BandConstance.MAX_BAND_MEMBERS:
                self.fsm.request('tooMany')
            elif len(localcrew) > 0 and DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand():
                self.fsm.request('checkAvailability')
            elif len(localcrew) > 0:
                self.fsm.request('notCaption')
            else:
                self.fsm.request('checkAvailability')

    def exitBegin(self):
        pass

    def enterTooMany(self):
        self.message['text'] = PLocalizer.CrewInviterTooMany % (self.avName,)
        self['text_pos'] = (0.0, 0.2)
        self.bCancel.show()

    def exitTooMany(self):
        self.bCancel.hide()

    def enterNotYet(self):
        self.message['text'] = PLocalizer.CrewInviterNotYet % self.avName
        self.bYes.show()
        self.bNo.show()

    def exitNotYet(self):
        self.bYes.hide()
        self.bNo.hide()

    def enterCheckAvailability(self):
        handle = base.cr.identifyAvatar(self.avId)
        if not handle:
            self.fsm.request('wentAway')
            return
        if handle and isinstance(handle, DistributedBattleNPC):
            self.fsm.request('askingNPC')
            return
        if base.cr.PirateBandManager == None:
            self.fsm.request('wentAway')
            return
        localAvatar.guiMgr.crewHUD.addPotentialCrew(self.avId, self.avName)
        base.cr.PirateBandManager.d_requestInvite(self.avId)
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterAsking, name=self.avName, avId=self.avId, icon=('crew',
                                                                                                                             ''))
        self.accept('BandAdded-%s' % (self.avId,), self.__crewAdded)
        self.accept('BandRequestRejected-%s' % (self.avId,), self.__crewRejectInvite)
        self.context = self.avId
        self.hide()
        return

    def __crewAdded(self, member):
        if member == self.avId:
            self.fsm.request('yes')

    def exitCheckAvailability(self):
        self.ignore('BandAdded-%s' % (self.avId,))
        self.ignore('BandRequestRejected-%s' % (self.avId,))
        self.bCancel.hide()

    def enterNotAvailable(self):
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterNotAvailable, name=self.avName, avId=self.avId, icon=('crew',
                                                                                                                                   ''))
        localAvatar.guiMgr.crewHUD.removePotentialCrew(self.avId)
        self.context = None
        self.destroy()
        return

    def exitNotAvailable(self):
        self.bOk.hide()

    def enterNotAcceptingCrews(self):
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterCrewSaidNoNewCrews, name=self.avName, avId=self.avId, icon=('crew',
                                                                                                                                         ''))
        localAvatar.guiMgr.crewHUD.removePotentialCrew(self.avId)
        self.context = None
        self.bOk.show()
        return

    def exitNotAcceptingCrews(self):
        self.bOk.hide()

    def enterWentAway(self):
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterWentAway, name=self.avName, avId=self.avId, icon=('crew',
                                                                                                                               ''))
        localAvatar.guiMgr.crewHUD.removePotentialCrew(self.avId)
        self.context = None
        self.destroy()
        return

    def exitWentAway(self):
        self.bOk.hide()

    def enterAlreadyCrewed(self):
        self.title['text'] = PLocalizer.CrewInviterRemove
        self.message['text'] = PLocalizer.CrewInviterAlready % self.avName
        self['text_pos'] = (0.0, 0.2)
        self.context = None
        self.bStop.show()
        self.bCancel.show()
        return

    def exitAlreadyCrewed(self):
        self.message['text'] = ''
        self['text_pos'] = (0.0, 0.13)
        self.bStop.hide()
        self.bCancel.hide()

    def enterAlreadyInvited(self):
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterAlreadyInvited, name=self.avName, avId=self.avId, icon=('crew',
                                                                                                                                     ''))
        self.accept('BandRequestRejected-%s' % (self.avId,), self.__crewRejectInvite)

    def exitAlreadyInvited(self):
        self.bOk.hide()

    def enterRecentlyInvited(self):
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterRecentlyInvited, name=self.avName, avId=self.avId, icon=('crew',
                                                                                                                                      ''))
        self.context = None
        self.destroy()
        return

    def exitRecentlyInvited(self):
        self.bOk.hide()

    def enterAskingNPC(self):
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterAskingNPC, name=self.avName, avId=self.avId, icon=('crew',
                                                                                                                                ''))
        taskMgr.doMethodLater(2.0, self.npcReplies, 'npcCrewship')
        self.hide()

    def exitAskingNPC(self):
        taskMgr.remove('npcCrewship')
        self.bCancel.hide()

    def npcReplies(self, task):
        self.fsm.request('no')
        return Task.done

    def enterEndCrewship(self):
        self.message['text'] = PLocalizer.CrewInviterEndCrewship % self.avName
        self.context = None
        self.bYes.show()
        self.bNo.show()
        return

    def exitEndCrewship(self):
        self.bYes.hide()
        self.bNo.hide()

    def enterLeaveCrew(self):
        self.message['text'] = PLocalizer.CrewInviterLeave
        self.context = None
        self.bYes.show()
        self.bNo.show()
        return

    def exitLeaveCrew(self):
        self.bYes.hide()
        self.bNo.hide()

    def enterCrewedNoMore(self):
        if base.cr.PirateBandManager:
            base.cr.PirateBandManager.d_requestRemove(self.avId)
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterCrewedNoMore, name=self.avName, avId=self.avId, icon=('crew',
                                                                                                                                   ''))
        self.context = None
        self.destroy()
        if not base.cr.identifyAvatar(self.avId) and self.avDisableName:
            messenger.send(self.avDisableName)
        return

    def exitCrewedNoMore(self):
        self.bOk.hide()

    def enterLeftCrew(self):
        if base.cr.PirateBandManager:
            base.cr.PirateBandManager.d_requestRemove(localAvatar.doId)
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterLeft, icon=('crew',
                                                                                         ''))
        self.context = None
        self.destroy()
        return

    def exitLeftCrew(self):
        self.bOk.hide()

    def enterSelf(self):
        self.message['text'] = PLocalizer.CrewInviterSelf
        self.context = None
        self.bOk.show()
        return

    def exitSelf(self):
        self.bOk.hide()

    def enterIgnored(self):
        self.message['text'] = PLocalizer.CrewInviterIgnored % self.avName
        self.context = None
        self.bOk.show()
        return

    def exitIgnored(self):
        self.bOk.hide()

    def enterAsking(self):
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterAsking, name=self.avName, avId=self.avId, icon=('crew',
                                                                                                                             None))
        self.accept('crewResponse', self.__crewResponse)
        self.accept(PiratesGlobals.CrewAddEvent, self.__crewAdded)
        self.hide()
        return None

    def exitAsking(self):
        self.ignore('crewResponse')
        self.ignore(PiratesGlobals.CrewAddEvent)
        self.bCancel.hide()

    def enterYes(self):
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterCrewSaidYes, name=self.avName, avId=self.avId, icon=('crew',
                                                                                                                                  None))
        messenger.send('AvatarChange')
        self.context = None
        self.destroy()
        return

    def exitYes(self):
        self.bOk.hide()

    def enterNo(self):
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterCrewSaidNo, name=self.avName, avId=self.avId, icon=('crew',
                                                                                                                                 None))
        localAvatar.guiMgr.crewHUD.removeCrew(self.avId)
        self.context = None
        self.destroy()
        return

    def exitNo(self):
        self.bOk.hide()

    def enterOtherTooMany(self):
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterOtherTooMany, name=self.avName, avId=self.avId, icon=('crew',
                                                                                                                                   None))
        localAvatar.guiMgr.crewHUD.removeCrew(self.avId)
        self.context = None
        self.destroy()
        return

    def exitOtherTooMany(self):
        self.bOk.hide()

    def enterInOtherCrew(self):
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterInOtherCrew, name=self.avName, avId=self.avId, icon=('crew',
                                                                                                                                  None))
        localAvatar.guiMgr.crewHUD.removeCrew(self.avId)
        self.context = None
        self.destroy()
        return

    def exitInOtherCrew(self):
        self.bOk.hide()

    def enterNotCaption(self):
        mName = DistributedBandMember.DistributedBandMember.getLeaderNameLocalAvatar()
        if not mName:
            localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterNotCaption, icon=('crew',
                                                                                                   None))
        else:
            localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterNotCaption1 % mName, icon=('crew',
                                                                                                            None))
        self.context = None
        self.destroy()
        return

    def exitNotCaption(self):
        self.bOk.hide()

    def enterMaybe(self):
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterMaybe, name=self.avName, avId=self.avId, icon=('crew',
                                                                                                                            None))
        localAvatar.guiMgr.crewHUD.removeCrew(self.avId)
        self.context = None
        self.destroy()
        return

    def exitMaybe(self):
        self.bOk.hide()

    def enterDown(self):
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.CrewInviterDown, icon=('crew',
                                                                                         None))
        self.context = None
        self.destroy()
        return

    def exitDown(self):
        self.bOk.hide()

    def enterCancel(self):
        if self.context != None:
            if base.cr.PirateBandManager:
                base.cr.PirateBandManager.d_requestCancel(self.avId)
            self.context = None
        self.fsm.request('off')
        return

    def exitCancel(self):
        pass

    def __handleOk(self):
        self.destroy()

    def __handleCancel(self):
        self.destroy()

    def __handleStop(self):
        self.fsm.request('endCrewship')

    def __handleYes(self):
        if self.fsm.getCurrentState().getName() == 'notYet':
            self.fsm.request('checkAvailability')
        elif self.fsm.getCurrentState().getName() == 'endCrewship':
            self.fsm.request('crewedNoMore')
        elif self.fsm.getCurrentState().getName() == 'leaveCrew':
            self.fsm.request('leftCrew')
        else:
            self.destroy()

    def __handleNo(self):
        self.destroy()

    def __handleList(self):
        messenger.send('openCrewList')

    def __crewConsidering(self, yesNoAlready, context):
        if yesNoAlready == 1:
            self.context = context
            self.fsm.request('asking')
        elif yesNoAlready == 0:
            self.fsm.request('notAvailable')
        elif yesNoAlready == 2:
            self.fsm.request('alreadyCrewed')
        elif yesNoAlready == 3:
            self.fsm.request('self')
        elif yesNoAlready == 4:
            self.fsm.request('ignored')
        elif yesNoAlready == 6:
            self.fsm.request('notAcceptingCrews')
        elif yesNoAlready == 10:
            self.fsm.request('no')
        elif yesNoAlready == 13:
            self.fsm.request('otherTooMany')
        else:
            self.notify.warning('Got unexpected response to crewConsidering: %s' % yesNoAlready)
            self.fsm.request('maybe')

    def __crewRejectInvite(self, avId, reason):
        if reason == BandConstance.outcome_not_online:
            self.fsm.request('notAvailable')
        elif reason == BandConstance.outcome_already_invited:
            self.fsm.request('alreadyInvited')
        elif reason == BandConstance.outcome_recently_invited:
            self.fsm.request('recentlyInvited')
        elif reason == BandConstance.outcome_already_in_Band:
            self.fsm.request('alreadyCrewed')
        elif reason == BandConstance.outcome_full:
            self.fsm.request('tooMany')
        elif reason == BandConstance.outcome_declined:
            self.fsm.request('no')
        else:
            self.notify.warning('crewRejectInvite: %s unknown reason: %s.' % (avId, reason))

    def __crewResponse(self, yesNoMaybe, context):
        if self.context != context:
            self.notify.warning('Unexpected change of context from %s to %s.' % (self.context, context))
            self.context = context
        if yesNoMaybe == 1:
            self.fsm.request('yes')
        elif yesNoMaybe == 0:
            self.fsm.request('no')
        elif yesNoMaybe == 3:
            self.fsm.request('otherTooMany')
        else:
            self.notify.warning('Got unexpected response to crewResponse: %s' % yesNoMaybe)
            self.fsm.request('maybe')

    def __handleDisableAvatar(self):
        self.fsm.request('wentAway')