import string
import sys
from direct.showbase import DirectObject
from otp.otpbase import OTPGlobals
from direct.fsm import ClassicFSM
from direct.fsm import State
from otp.login import SecretFriendsInfoPanel
from otp.login import PrivacyPolicyPanel
from otp.otpbase import OTPLocalizer
from direct.directnotify import DirectNotifyGlobal
from otp.login import LeaveToPayDialog
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm.FSM import FSM

class ChatManagerV2(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('ChatManagerV2')

    def __init__(self):
        self.openChatWarning = None
        self.unpaidChatWarning = None
        self.teaser = None
        self.paidNoParentPassword = None
        self.noSecretChatAtAll = None
        self.noSecretChatWarning = None
        self.chatMoreInfo = None
        self.chatPrivacyPolicy = None
        self.secretChatActivated = None
        self.problemActivatingChat = None
        self.leaveToPayDialog = None
        self.fsm = ClassicFSM.ClassicFSM('chatManager', [
         State.State('off', self.enterOff, self.exitOff),
         State.State('mainMenu', self.enterMainMenu, self.exitMainMenu),
         State.State('openChatWarning', self.enterOpenChatWarning, self.exitOpenChatWarning),
         State.State('leaveToPayDialog', self.enterLeaveToPayDialog, self.exitLeaveToPayDialog),
         State.State('unpaidChatWarning', self.enterUnpaidChatWarning, self.exitUnpaidChatWarning),
         State.State('noSecretChatAtAll', self.enterNoSecretChatAtAll, self.exitNoSecretChatAtAll),
         State.State('noSecretChatWarning', self.enterNoSecretChatWarning, self.exitNoSecretChatWarning),
         State.State('noFriendsWarning', self.enterNoFriendsWarning, self.exitNoFriendsWarning),
         State.State('otherDialog', self.enterOtherDialog, self.exitOtherDialog),
         State.State('activateChat', self.enterActivateChat, self.exitActivateChat),
         State.State('chatMoreInfo', self.enterChatMoreInfo, self.exitChatMoreInfo),
         State.State('chatPrivacyPolicy', self.enterChatPrivacyPolicy, self.exitChatPrivacyPolicy),
         State.State('secretChatActivated', self.enterSecretChatActivated, self.exitSecretChatActivated),
         State.State('problemActivatingChat', self.enterProblemActivatingChat, self.exitProblemActivatingChat)], 'off', 'off')
        self.fsm.enterInitialState()
        self.accept('Chat-Failed open typed chat test', self.__handleFailOpenTypedChat)
        self.accept('Chat-Failed player typed chat test', self.__handleFailPlayerTypedWhsiper)
        self.accept('Chat-Failed avatar typed chat test', self.__handleFailAvatarTypedWhsiper)
        return

    def delete(self):
        self.ignoreAll()
        del self.fsm

    def __handleFailOpenTypedChat(self, caller=None):
        self.fsm.request('openChatWarning')

    def __handleFailPlayerTypedWhsiper(self, caller=None):
        self.fsm.request('noSecretChatWarning')

    def __handleFailAvatarTypedWhsiper(self, caller=None):
        self.fsm.request('noSecretChatWarning')

    def __handleLeaveToPayCancel(self):
        self.fsm.request('mainMenu')

    def __secretFriendsInfoDone(self):
        self.fsm.request('activateChat')

    def __privacyPolicyDone(self):
        self.fsm.request('activateChat')

    def enterOff(self):
        self.ignoreAll()

    def exitOff(self):
        pass

    def enterOtherDialog(self):
        pass

    def exitOtherDialog(self):
        pass

    def enterUnpaidChatWarning(self):
        self.notify.error('called enterUnpaidChatWarning() on parent class')

    def exitUnpaidChatWarning(self):
        self.notify.error('called exitUnpaidChatWarning() on parent class')

    def enterNoFriendsWarning(self):
        self.notify.error('called enterNoFriendsWarning() on parent class')

    def exitNoFriendsWarning(self):
        self.notify.error('called exitNoFriendsWarning() on parent class')

    def enterSecretChatActivated(self):
        self.notify.error('called enterSecretChatActivated() on parent class')

    def exitSecretChatActivated(self):
        self.notify.error('called exitSecretChatActivated() on parent class')

    def enterProblemActivatingChat(self):
        self.notify.error('called enterProblemActivatingChat() on parent class')

    def exitProblemActivatingChat(self):
        self.notify.error('called exitProblemActivatingChat() on parent class')

    def enterChatPrivacyPolicy(self):
        self.notify.error('called enterChatPrivacyPolicy() on parent class')

    def exitChatPrivacyPolicy(self):
        self.notify.error('called exitChatPrivacyPolicy() on parent class')

    def enterChatMoreInfo(self):
        self.notify.error('called enterChatMoreInfo() on parent class')

    def exitChatMoreInfo(self):
        self.notify.error('called exitChatMoreInfo() on parent class')

    def enterNoSecretChatWarning(self):
        self.notify.error('called enterNoSecretChatWarning() on parent class')

    def exitNoSecretChatWarning(self):
        self.notify.error('called exitNoSecretChatWarning() on parent class')

    def enterLeaveToPayDialog(self):
        self.notify.error('called enterLeaveToPayDialog() on parent class')

    def exitLeaveToPayDialog(self):
        self.notify.error('called exitLeaveToPayDialog() on parent class')