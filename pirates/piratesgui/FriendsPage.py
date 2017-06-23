from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm import StateData
from otp.friends import FriendSecret
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import SocialPage
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from otp.otpbase import OTPGlobals
from otp.friends.FriendInfo import FriendInfo
import GuiButton
from pirates.piratesgui import PirateMemberList
from direct.task import Task
from pirates.uberdog.UberDogGlobals import InventoryType

class FriendsPage(SocialPage.SocialPage):
    NumVisible = 6

    def __init__(self, showAvatar=1, showPlayer=1, showPlayerFriendAvatars=0):
        self.showAvatar = showAvatar
        self.showPlayer = showPlayer
        self.showPlayerFriendAvatars = showPlayerFriendAvatars
        if self.showAvatar and self.showPlayer:
            myTitle = PLocalizer.FriendsListLabel
        else:
            if self.showAvatar:
                myTitle = PLocalizer.AvatarFriendsListLabel
            elif self.showPlayer:
                myTitle = PLocalizer.AccountsFriendsListLabel
            SocialPage.SocialPage.__init__(self, myTitle)
            self.initialiseoptions(FriendsPage)
            charGui = loader.loadModel('models/gui/char_gui')
            self.membersList = PirateMemberList.PirateMemberList(10, self, 'FOOLIO HC', height=0.68, memberWidth=0.6, width=0.62, sort=1)
            self.membersList.setPos(-0.087, 0.0, 0.03)
            self.accept(self.membersList.onlineChangeEvent, self.updateCount)
            if self.showAvatar:
                self.accept(OTPGlobals.AvatarFriendAddEvent, self.addAvatarFriend)
                self.accept(OTPGlobals.AvatarFriendUpdateEvent, self.updateAvatarFriend)
                self.accept(OTPGlobals.AvatarFriendRemoveEvent, self.removeAvatarFriend)
            if showPlayerFriendAvatars:
                self.accept(OTPGlobals.PlayerFriendAddEvent, self.addPlayerFriendAvatar)
                self.accept(OTPGlobals.PlayerFriendUpdateEvent, self.updatePlayerFriendAvatar)
                self.accept(OTPGlobals.PlayerFriendRemoveEvent, self.removePlayerFriendAvatar)
            if self.showPlayer:
                self.accept(OTPGlobals.PlayerFriendAddEvent, self.addPlayerFriend)
                self.accept(OTPGlobals.PlayerFriendUpdateEvent, self.updatePlayerFriend)
                self.accept(OTPGlobals.PlayerFriendRemoveEvent, self.removePlayerFriend)
        charGui.removeNode()
        self.headingLabel = DirectLabel(parent=self, relief=None, state=DGG.NORMAL, text=myTitle, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                      0.0), text_fg=PiratesGuiGlobals.TextFG1, pos=(0.24,
                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                    0.794))
        self.maintainNormalButtonState()
        return

    def show(self):
        SocialPage.SocialPage.show(self)
        self.membersList.updateOnlineData()

    def destroy(self):
        self.stopMaintainNormalButtonState()
        self.ignoreAll()
        self.membersList.destroy()
        SocialPage.SocialPage.destroy(self)

    def addAvatarFriend(self, avId, info):
        self.membersList.updateOrAddMember(avId, None, PirateMemberList.MODE_FRIEND_AVATAR, info)
        self.startRecountMembers()
        if hasattr(base, 'localAvatar'):
            inv = base.localAvatar.getInventory()
            if inv and not inv.getStackQuantity(InventoryType.NewFriend):
                base.localAvatar.sendRequestContext(InventoryType.NewFriend)
        return

    def addPlayerFriend(self, playerId, info, isNewFriend):
        if localAvatar.style.getTutorial() >= PiratesGlobals.TUT_MET_JOLLY_ROGER and isNewFriend:
            localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterFriendSaidYes, playerName=info.playerName, avId=playerId, icon=('friends',
                                                                                                                                                     None))
        self.membersList.updateOrAddMember(info.avatarId, playerId, PirateMemberList.MODE_FRIEND_PLAYER, info)
        self.startRecountMembers()
        return None

    def addPlayerFriendAvatar(self, playerId, info, isNewFriend):
        if info.isOnline() and info.avatarId:
            if isNewFriend:
                localAvatar.guiMgr.messageStack.addTextMessage(OTPLocalizer.FriendInviterPlayerFriendSaidYes, name=info.avatarName, playerName=info.playerName, avId=info.avatarId, icon=('friends',
                                                                                                                                                                                          None))
            self.membersList.updateOrAddMember(info.avatarId, playerId, PirateMemberList.MODE_FRIEND_PLAYER_AVATAR, info)
        self.startRecountMembers()
        return None

    def addAvatarFriends(self, friendData):
        for friendDetail in friendData:
            avId = friendDetail[0]
            info = friendDetail[1]
            self.membersList.updateOrAddMember(avId, None, PirateMemberList.MODE_FRIEND_AVATAR, info)

        self.startRecountMembers()
        return

    def addPlayerFriends(self, friendData):
        for friendDetail in friendData:
            playerId = friendDetail[0]
            info = friendDetail[1]
            self.membersList.updateOrAddMember(info.avatarId, playerId, PirateMemberList.MODE_FRIEND_PLAYER, info)

        self.startRecountMembers()

    def updateAvatarFriend(self, avId, info):
        self.membersList.updateOrAddMember(avId, None, PirateMemberList.MODE_FRIEND_AVATAR, info)
        self.startRecountMembers()
        return

    def updatePlayerFriend(self, playerId, info):
        self.membersList.updateOrAddMember(None, playerId, PirateMemberList.MODE_FRIEND_PLAYER, info)
        self.startRecountMembers()
        return

    def updatePlayerFriendAvatar(self, playerId, info):
        if info.isOnline() and info.avatarId:
            self.membersList.updateOrAddMember(info.avatarId, playerId, PirateMemberList.MODE_FRIEND_PLAYER_AVATAR, info)
        else:
            self.removePlayerFriendAvatar(playerId)
        self.startRecountMembers()

    def removeAvatarFriend(self, avId):
        removeIdPair = self.membersList.removeMember(avId, None, PirateMemberList.MODE_FRIEND_AVATAR)
        avId = removeIdPair[0]
        playerId = base.cr.playerFriendsManager.findPlayerIdFromAvId(avId)
        if self.showPlayerFriendAvatars:
            self.membersList.refillMember(avId, playerId, PirateMemberList.MODE_FRIEND_AVATAR)
        self.membersList.arrangeMembers()
        self.startRecountMembers()
        return

    def removePlayerFriend(self, playerId):
        removeIdPair = self.membersList.removeMember(None, playerId, PirateMemberList.MODE_FRIEND_PLAYER)
        self.membersList.arrangeMembers()
        self.startRecountMembers()
        return

    def removePlayerFriendAvatar(self, playerId):
        removeIdPair = self.membersList.removeMember(None, playerId, PirateMemberList.MODE_FRIEND_PLAYER_AVATAR)
        if self.showAvatar:
            self.membersList.refillMember(removeIdPair[0], removeIdPair[1], PirateMemberList.MODE_FRIEND_PLAYER_AVATAR)
        self.membersList.arrangeMembers()
        self.startRecountMembers()
        return

    def maintainNormalButtonState(self):
        taskMgr.remove('friendsMaintainNormalButtonState')
        taskMgr.doMethodLater(15, self.friendsMaintainNormalButtonState, 'friendsMaintainNormalButtonState')

    def stopMaintainNormalButtonState(self):
        taskMgr.remove('friendsMaintainNormalButtonState')

    def friendsMaintainNormalButtonState(self, task):
        for friendButton in self.membersList.members:
            friendButton['state'] = DGG.NORMAL

        return Task.again

    def updateCount(self, task=None):
        self.count = self.membersList.getSize()
        self.headingLabel['text'] = '%s %s/%s' % (self.title, self.membersList.onlineCount, self.count)
        if task:
            return task.done