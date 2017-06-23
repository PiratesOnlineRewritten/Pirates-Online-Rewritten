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
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.battle.DistributedBattleNPC import DistributedBattleNPC
from pirates.friends import PirateFriendSecret
from pirates.piratesgui import PirateButtonChain

class RelationshipChooser(GuiPanel.GuiPanel):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendInviter')

    def __init__(self, avId, avName, pId=None):
        self.avId = avId
        self.avName = avName
        self.pId = pId
        self.avDisableName = 'disable-%s' % avId
        if not self.pId and self.avId:
            self.pId = base.cr.playerFriendsManager.findPlayerIdFromAvId(self.avId)
        if not self.avId and self.pId:
            self.avId = base.cr.playerFriendsManager.findAvIdFromPlayerId(self.pId)
        GuiPanel.GuiPanel.__init__(self, PLocalizer.RelationshipChooserTitle % avName, 0.5, 0.25, True, 1)
        self.initialiseoptions(RelationshipChooser)
        self.setPos(0.15, 0, 0.25)
        self.chain = PirateButtonChain.PirateButtonChain(self.width, self)
        self.chain.setPos(0, 0, -0.03)
        self.load()
        self.determineButtonState()

    def load(self):
        self.avFriendButton = self.chain.premakeButton(PLocalizer.RelationshipChooserAvFriendsMake, self.__handleAvatarFriend)
        self.plFriendButton = self.chain.premakeButton(PLocalizer.RelationshipChooserPlFriendsMake, self.__handlePlayerFriend)
        self.secretsButton = self.chain.premakeButton(PLocalizer.RelationshipChooserPlSecrets, self.__handleSecrets)
        self.chain.makeButtons()

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.chain.destroy()
        GuiPanel.GuiPanel.destroy(self)

    def __handleSecrets(self):
        PirateFriendSecret.showFriendSecret()
        self.destroy()

    def __handleAvatarFriend(self):
        base.localAvatar.guiMgr.handleAvatarFriendInvite(self.avId, self.avName)
        self.destroy()

    def __handlePlayerFriend(self):
        base.localAvatar.guiMgr.handlePlayerFriendInvite(self.avId, self.avName)
        self.destroy()

    def determineButtonState(self):
        isPlayerFriend = base.cr.playerFriendsManager.isPlayerFriend(self.pId)
        isAvatarFriend = base.cr.avatarFriendsManager.isAvatarFriend(self.avId)
        if isPlayerFriend:
            self.plFriendButton['text'] = PLocalizer.RelationshipChooserPlFriendsBreak
        else:
            self.plFriendButton['text'] = PLocalizer.RelationshipChooserPlFriendsMake
        if isAvatarFriend:
            self.avFriendButton['text'] = PLocalizer.RelationshipChooserAvFriendsBreak
        else:
            self.avFriendButton['text'] = PLocalizer.RelationshipChooserAvFriendsMake
        self.avFriendButton['state'] = DGG.DISABLED
        self.plFriendButton['state'] = DGG.DISABLED
        self.secretsButton['state'] = DGG.NORMAL
        if self.avId or self.pId:
            av = base.cr.doId2do.get(self.avId)
            print 'avId %s av %s' % (self.avId, av)
            if av:
                if av.commonChatFlags & base.localAvatar.commonChatFlags & OTPGlobals.CommonChat:
                    self.plFriendButton['state'] = DGG.NORMAL
                self.avFriendButton['state'] = DGG.NORMAL
            if base.cr.avatarFriendsManager.checkIgnored(self.avId):
                self.avFriendButton['state'] = DGG.DISABLED
                self.plFriendButton['state'] = DGG.DISABLED
                self.secretsButton['state'] = DGG.DISABLED
            if isPlayerFriend:
                self.plFriendButton['state'] = DGG.NORMAL
            if isAvatarFriend:
                self.avFriendButton['state'] = DGG.NORMAL