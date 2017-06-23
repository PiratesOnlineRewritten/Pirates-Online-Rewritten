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
from pirates.piratesgui.RequestButton import RequestButton
from pirates.piratesgui.CheckBox import CheckBox
from pirates.piratesgui import PiratesGuiGlobals
from pirates.battle.DistributedBattleNPC import DistributedBattleNPC
from otp.friends import FriendResponseCodes

class FriendInviterButton(RequestButton):

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(FriendInviterButton)


class FriendInviter(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendInviter')

    def __init__(self, avId, avName, isPlayerInvite, quickYesNo=True, playerId=None):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief=None, pos=(-0.25, 0, 0.64), image=guiMain.find('**/general_frame_e'), image_scale=0.35)
        self.initialiseoptions(FriendInviter)
        self.avId = avId
        self.avName = avName
        self.avDisableName = 'disable-%s' % avId
        self.isPlayerInvite = isPlayerInvite
        self.playerId = playerId
        self.playerName = None
        if isPlayerInvite:
            avatar = base.cr.doId2do.get(avId)
            if avatar:
                self.playerId = avatar.DISLid
                self.playerName = avatar.DISLname
            if not self.playerId or not self.playerName:
                aInfo = base.cr.avatarFriendsManager.getFriendInfo(avId)
                if aInfo:
                    if not self.playerId:
                        self.playerId = aInfo.playerId
                    if not self.playerName:
                        self.playerName = aInfo.playerName
            if not self.playerId or not self.playerName:
                pInfo = base.cr.playerFriendsManager.findPlayerInfoFromAvId(avId)
                if pInfo:
                    if not self.playerId:
                        self.playerId = base.cr.playerFriendsManager.findPlayerIdFromAvId(avId)
                    if not self.playerName:
                        self.playerName = pInfo.playerName
        self.skipYesNo = quickYesNo
        self.skipCongrats = False
        self.fsm = ClassicFSM.ClassicFSM('FriendInviter', [
         State.State('off', self.enterOff, self.exitOff),
         State.State('getNewFriend', self.enterGetNewFriend, self.exitGetNewFriend),
         State.State('begin', self.enterBegin, self.exitBegin),
         State.State('tooMany', self.enterTooMany, self.exitTooMany),
         State.State('notYet', self.enterNotYet, self.exitNotYet),
         State.State('checkAvailability', self.enterCheckAvailability, self.exitCheckAvailability),
         State.State('notAvailable', self.enterNotAvailable, self.exitNotAvailable),
         State.State('cantSee', self.enterCantSee, self.exitCantSee),
         State.State('notOnline', self.enterNotOnline, self.exitNotOnline),
         State.State('notOpen', self.enterNotOpen, self.exitNotOpen),
         State.State('notAcceptingFriends', self.enterNotAcceptingFriends, self.exitNotAcceptingFriends),
         State.State('wentAway', self.enterWentAway, self.exitWentAway),
         State.State('alreadyFriends', self.enterAlreadyFriends, self.exitAlreadyFriends),
         State.State('alreadyInvited', self.enterAlreadyInvited, self.exitAlreadyInvited),
         State.State('askingNPC', self.enterAskingNPC, self.exitAskingNPC),
         State.State('endFriendship', self.enterEndFriendship, self.exitEndFriendship),
         State.State('friendsNoMore', self.enterFriendsNoMore, self.exitFriendsNoMore),
         State.State('self', self.enterSelf, self.exitSelf),
         State.State('ignored', self.enterIgnored, self.exitIgnored),
         State.State('asking', self.enterAsking, self.exitAsking),
         State.State('yes', self.enterYes, self.exitYes),
         State.State('no', self.enterNo, self.exitNo),
         State.State('otherTooMany', self.enterOtherTooMany, self.exitOtherTooMany),
         State.State('maybe', self.enterMaybe, self.exitMaybe),
         State.State('down', self.enterDown, self.exitDown),
         State.State('cancel', self.enterCancel, self.exitCancel)], 'off', 'off')
        self.title = DirectLabel(parent=self, relief=None, text=PLocalizer.FriendInviterTitle, text_scale=PiratesGuiGlobals.TextScaleLarge * 1.8, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateOutlineFont(), pos=(0.0,
                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                  0.2), image=None, image_scale=1.0)
        self.message = DirectLabel(parent=self, relief=None, text='', text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=15, pos=(-0.3, 0, 0.085), textMayChange=1)
        self.context = None
        xOff = -0.025
        self.bOk = FriendInviterButton(text=OTPLocalizer.FriendInviterOK, command=self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.0 + xOff, 0, -0.29)
        self.bOk.hide()
        self.bCancel = FriendInviterButton(text=OTPLocalizer.FriendInviterCancel, command=self.__handleCancel)
        self.bCancel.reparentTo(self)
        self.bCancel.setPos(0.0 + xOff, 0, -0.29)
        self.bCancel.hide()
        self.bStop = FriendInviterButton(text=OTPLocalizer.FriendInviterConfirmRemove, command=self.__handleStop)
        self.bStop.reparentTo(self)
        self.bStop.setPos(0.0 + xOff, 0, -0.19)
        self.bStop.hide()
        self.bYes = FriendInviterButton(text=OTPLocalizer.FriendInviterYes, command=self.__handleYes)
        self.bYes.reparentTo(self)
        self.bYes.setPos(-0.1 + xOff, 0, -0.32)
        self.bYes.hide()
        self.bNo = FriendInviterButton(text=OTPLocalizer.FriendInviterNo, command=self.__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.1 + xOff, 0, -0.32)
        self.bNo.hide()
        self.fsm.enterInitialState()
        self.fsm.request('begin')
        return

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.fsm.request('cancel')
        del self.fsm
        DirectFrame.destroy(self)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterGetNewFriend(self):
        self.message['text'] = OTPLocalizer.FriendInviterClickToon
        self.bCancel.show()
        self.accept('clickedNametag', self.__handleClickedNametag)

    def exitGetNewFriend(self):
        self.bCancel.hide()
        self.ignore('clickedNametag')

    def __handleClickedNametag(self, avatar):
        self.avId = avatar.doId
        self.avName = avatar.getName()
        self.avDisableName = avatar.uniqueName('disable')
        self.fsm.request('begin')

    def enterBegin(self):
        myId = base.localAvatar.doId
        self.accept(self.avDisableName, self.__handleDisableAvatar)
        if self.avId == myId:
            self.fsm.request('self')
        elif self.isPlayerInvite:
            if base.cr.playerFriendsManager.isAvatarOwnerPlayerFriend(self.avId) or base.cr.playerFriendsManager.isPlayerFriend(self.playerId):
                self.fsm.request('alreadyFriends')
            elif len(base.cr.playerFriendsManager.playerFriendsList) >= OTPGlobals.MaxPlayerFriends:
                self.fsm.request('tooMany')
            elif not base.cr.identifyFriend(self.avId) and not self.playerId:
                self.fsm.request('cantSee')
            elif not base.cr.isFriendOnline(self.avId) and not base.cr.doId2do.get(self.avId):
                self.fsm.request('notOnline')
            elif self.skipYesNo == True:
                self.fsm.request('checkAvailability')
            else:
                self.fsm.request('notYet')
        elif base.cr.avatarFriendsManager.isFriend(self.avId):
            self.fsm.request('alreadyFriends')
        else:
            tooMany = len(base.cr.avatarFriendsManager.avatarFriendsList) >= PiratesGlobals.MaxPirateFriends
            if tooMany:
                self.fsm.request('tooMany')
            elif self.skipYesNo == True:
                self.fsm.request('checkAvailability')
            else:
                self.fsm.request('notYet')

    def exitBegin(self):
        self.ignore(self.avDisableName)

    def enterTooMany(self):
        localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterTooMany, name=self.avName, avId=self.avId, icon=('friends',
                                                                                                                                  None))
        self.context = None
        self.destroy()
        return

    def exitTooMany(self):
        self.bCancel.hide()

    def enterNotYet(self):
        self.accept(self.avDisableName, self.__handleDisableAvatar)
        if not self.isPlayerInvite:
            self.message['text'] = PLocalizer.FriendInviterAvatarNotYet % self.avName
        else:
            self.message['text'] = PLocalizer.FriendInviterPlayerNotYetAvNameOnly % self.avName
        self.bYes.show()
        self.bNo.show()

    def exitNotYet(self):
        self.ignore(self.avDisableName)
        self.bYes.hide()
        self.bNo.hide()

    def enterCheckAvailability(self):
        self.accept(self.avDisableName, self.__handleDisableAvatar)
        handle = base.cr.identifyAvatar(self.avId)
        if not handle:
            self.fsm.request('wentAway')
            return
        if isinstance(handle, DistributedBattleNPC):
            self.fsm.request('askingNPC')
            return
        if self.isPlayerInvite:
            self.playerId = None
            self.playerName = None
            avatarInfo = base.cr.avatarFriendsManager.getFriendInfo(self.avId)
            if avatarInfo and avatarInfo.playerId:
                self.playerId = avatarInfo.playerId
                self.playerName = avatarInfo.playerName
            elif base.cr.doId2do.get(self.avId):
                avatar = base.cr.doId2do.get(self.avId)
                self.playerName = avatar.DISLname
                self.playerId = avatar.DISLid
            if self.playerId:
                base.cr.playerFriendsManager.sendRequestInvite(self.playerId)
            else:
                self.fsm.request('cantSee')
                return
        else:
            base.cr.avatarFriendsManager.sendRequestInvite(self.avId)
        self.accept(OTPGlobals.AvatarFriendConsideringEvent, self.__friendConsidering)
        self.accept(OTPGlobals.AvatarFriendAddEvent, self.__friendAdded)
        self.accept(OTPGlobals.AvatarFriendRejectInviteEvent, self.__friendRejectInvite)
        self.accept(OTPGlobals.PlayerFriendUpdateEvent, self.__friendAdded)
        self.accept(OTPGlobals.PlayerFriendRejectInviteEvent, self.__friendRejectInvitePlayer)
        self.hide()
        return

    def __friendAdded(self, avId, info):
        if self.isPlayerInvite:
            if self.avId == info.avatarId:
                self.info = info
                self.fsm.request('yes')
        elif self.avId == avId:
            localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterFriendSaidYes, name=info.avatarName, avId=avId, icon=('friends',
                                                                                                                                           None))
            self.fsm.request('yes')
        return None

    def exitCheckAvailability(self):
        self.ignore(self.avDisableName)
        self.ignore('friendConsidering')
        self.ignore('friendResponse')
        self.ignore(OTPGlobals.AvatarFriendAddEvent)
        self.ignore(OTPGlobals.AvatarFriendRejectInviteEvent)
        self.ignore(OTPGlobals.PlayerFriendAddEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectInviteEvent)
        self.bCancel.hide()

    def enterNotAvailable(self):
        localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterNotAvailable, name=self.avName, avId=self.avId, icon=('friends',
                                                                                                                                       None))
        self.context = None
        self.destroy()
        return

    def exitNotAvailable(self):
        self.bOk.hide()

    def enterCantSee(self):
        localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterCantSee, name=self.avName, avId=self.avId, icon=('friends',
                                                                                                                                  None))
        self.context = None
        self.destroy()
        return

    def exitCantSee(self):
        self.bOk.hide()

    def enterNotOnline(self):
        localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterNotOnline, name=self.avName, avId=self.avId, icon=('friends',
                                                                                                                                    None))
        self.context = None
        self.destroy()
        return

    def exitNotOnline(self):
        self.bOk.hide()

    def enterNotOpen(self):
        localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterNotOpen, name=self.avName, avId=self.avId, icon=('friends',
                                                                                                                                  None))
        self.context = None
        self.destroy()
        return

    def exitNotOpen(self):
        self.bOk.hide()

    def enterNotAcceptingFriends(self):
        localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterFriendSaidNoNewFriends, name=self.avName, avId=self.avId, icon=('friends',
                                                                                                                                                 None))
        self.context = None
        self.destroy()
        return

    def exitNotAcceptingFriends(self):
        self.bOk.hide()

    def enterWentAway(self):
        localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterWentAway, name=self.avName, avId=self.avId, icon=('friends',
                                                                                                                                   None))
        if self.context != None:
            self.context = None
        self.destroy()
        return

    def exitWentAway(self):
        self.bOk.hide()

    def enterAlreadyFriends(self):
        self.title['text'] = PLocalizer.FriendInviterRemove
        self.message['text'] = OTPLocalizer.FriendInviterAlready % self.avName
        self['text_pos'] = (0.0, 0.2)
        self.context = None
        self.bStop.show()
        self.bCancel.show()
        return

    def exitAlreadyFriends(self):
        self.message['text'] = ''
        self['text_pos'] = (0.0, 0.13)
        self.bStop.hide()
        self.bCancel.hide()

    def enterAlreadyInvited(self):
        self.message['text'] = OTPLocalizer.FriendInviterAlreadyInvited % self.avName
        self['text_pos'] = (0.0, 0.2)
        self.context = None
        self.bStop.show()
        self.bCancel.show()
        return

    def exitAlreadyInvited(self):
        self.message['text'] = ''
        self['text_pos'] = (0.0, 0.13)
        self.bStop.hide()
        self.bCancel.hide()

    def enterAskingNPC(self):
        localAvatar.guiMgr.messageStack.addTextMessage(PPLocalizer.FriendInviterAskingNPC, name=self.avName, avId=self.avId, icon=('friends',
                                                                                                                                   ''))
        taskMgr.doMethodLater(2.0, self.npcReplies, 'npcFriendship')
        self.hide()

    def exitAskingNPC(self):
        taskMgr.remove('npcFriendship')
        self.bCancel.hide()

    def npcReplies(self, task):
        self.fsm.request('no')
        return Task.done

    def enterEndFriendship(self):
        if self.isPlayerInvite:
            self.message['text'] = PLocalizer.FriendInviterPlayerEndFriendShip % self.avName
        else:
            self.message['text'] = PLocalizer.FriendInviterAvatarEndFriendShip % self.avName
        self.context = None
        self.bYes.show()
        self.bNo.show()
        return

    def exitEndFriendship(self):
        self.bYes.hide()
        self.bNo.hide()

    def enterFriendsNoMore(self):
        if self.isPlayerInvite:
            if self.playerId:
                base.cr.playerFriendsManager.sendRequestRemove(self.playerId)
        else:
            base.cr.avatarFriendsManager.sendRequestRemove(self.avId)
        localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterFriendsNoMore, name=self.avName, avId=self.avId, icon=('friends',
                                                                                                                                        None))
        self.context = None
        self.destroy()
        if not self.isPlayerInvite and not base.cr.identifyAvatar(self.avId):
            messenger.send(self.avDisableName)
        return

    def exitFriendsNoMore(self):
        self.bOk.hide()

    def enterSelf(self):
        self.message['text'] = OTPLocalizer.FriendInviterSelf
        self.context = None
        self.bOk.show()
        return

    def exitSelf(self):
        self.bOk.hide()

    def enterIgnored(self):
        self.message['text'] = OTPLocalizer.FriendInviterIgnored % self.avName
        self.context = None
        self.bOk.show()
        return

    def exitIgnored(self):
        self.bOk.hide()

    def enterAsking(self):
        self.accept(self.avDisableName, self.__handleDisableAvatar)
        localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterAsking, name=self.avName, avId=self.avId, icon=('friends',
                                                                                                                                 None))
        self.accept(OTPGlobals.AvatarFriendConsideringEvent, self.__friendConsidering)
        self.accept(OTPGlobals.AvatarFriendAddEvent, self.__friendAdded)
        self.accept(OTPGlobals.AvatarFriendRejectInviteEvent, self.__friendRejectInvite)
        self.accept(OTPGlobals.PlayerFriendUpdateEvent, self.__friendAdded)
        self.accept(OTPGlobals.PlayerFriendRejectInviteEvent, self.__friendRejectInvitePlayer)
        self.hide()
        return None

    def exitAsking(self):
        self.ignore(self.avDisableName)
        self.ignore(OTPGlobals.AvatarFriendConsideringEvent)
        self.ignore(OTPGlobals.AvatarFriendAddEvent)
        self.ignore(OTPGlobals.AvatarFriendRejectInviteEvent)
        self.ignore(OTPGlobals.PlayerFriendAddEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectInviteEvent)
        self.bCancel.hide()

    def enterYes(self):
        self.context = None
        self.destroy()
        return

    def exitYes(self):
        self.bOk.hide()

    def enterNo(self):
        localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterFriendSaidNo, name=self.avName, avId=self.avId, icon=('friends',
                                                                                                                                       None))
        self.context = None
        self.destroy()
        return

    def exitNo(self):
        self.bOk.hide()

    def enterOtherTooMany(self):
        localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterOtherTooMany, name=self.avName, avId=self.avId, icon=('friends',
                                                                                                                                       None))
        self.context = None
        self.destroy()
        return

    def exitOtherTooMany(self):
        self.bOk.hide()

    def enterMaybe(self):
        localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterMaybe, name=self.avName, avId=self.avId, icon=('friends',
                                                                                                                                None))
        self.context = None
        self.destroy()
        return

    def exitMaybe(self):
        self.bOk.hide()

    def enterDown(self):
        localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterDown, icon=('friends',
                                                                                             None))
        self.message['text'] = OTPLocalizer.FriendInviterDown
        self.context = None
        self.destroy()
        return

    def exitDown(self):
        self.bOk.hide()

    def enterCancel(self):
        if self.context != None:
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
        self.fsm.request('endFriendship')

    def __handleYes(self):
        if self.fsm.getCurrentState().getName() == 'notYet':
            self.fsm.request('checkAvailability')
        elif self.fsm.getCurrentState().getName() == 'endFriendship':
            self.fsm.request('friendsNoMore')
        else:
            self.destroy()

    def __handleNo(self):
        self.destroy()

    def __handleList(self):
        messenger.send('openFriendsList')

    def __friendConsidering(self, yesNoAlready, context):
        if yesNoAlready == 1:
            self.context = context
            self.fsm.request('asking')
        elif yesNoAlready == 0:
            self.fsm.request('notAvailable')
        elif yesNoAlready == 2:
            self.fsm.request('alreadyFriends')
        elif yesNoAlready == 3:
            self.fsm.request('self')
        elif yesNoAlready == 4:
            self.fsm.request('ignored')
        elif yesNoAlready == 6:
            self.fsm.request('notAcceptingFriends')
        elif yesNoAlready == 10:
            self.fsm.request('no')
        elif yesNoAlready == 13:
            self.fsm.request('otherTooMany')
        else:
            self.notify.warning('Got unexpected response to friendConsidering: %s' % yesNoAlready)
            self.fsm.request('maybe')

    def __friendRejectInvite(self, avId, reason):
        if reason == RejectCode.NO_FRIENDS_LIST:
            pass
        elif reason == RejectCode.FRIENDS_LIST_NOT_HANDY:
            pass
        elif reason == RejectCode.INVITEE_NOT_ONLINE:
            self.fsm.request('notAvailable')
        elif reason == RejectCode.ALREADY_INVITED:
            self.fsm.request('alreadyInvited')
        elif reason == RejectCode.ALREADY_YOUR_FRIEND:
            self.fsm.request('alreadyFriends')
        elif reason == RejectCode.FRIENDS_LIST_FULL:
            self.fsm.request('tooMany')
        elif reason == RejectCode.OTHER_FRIENDS_LIST_FULL:
            self.fsm.request('otherTooMany')
        elif reason == RejectCode.INVITATION_DECLINED:
            self.fsm.request('no')
        elif reason == RejectCode.MAY_NOT_OPEN_INVITE:
            self.notify.warning('May Not Open Invite, switchboard confused %s.' % avId)
            self.fsm.request('notOpen')
        else:
            self.notify.warning('friendRejectInvite: %s unknown reason: %s.' % (avId, reason))

    def __friendRejectInvitePlayer(self, playerId, respCode):
        if respCode == FriendResponseCodes.INVITATION_RESP_DECLINE:
            self.fsm.request('no')

    def __friendResponse(self, yesNoMaybe, context):
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
            self.notify.warning('Got unexpected response to friendResponse: %s' % yesNoMaybe)
            self.fsm.request('maybe')

    def __handleDisableAvatar(self):
        self.fsm.request('wentAway')