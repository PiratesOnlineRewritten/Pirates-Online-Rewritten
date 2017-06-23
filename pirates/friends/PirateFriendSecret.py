from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
import string
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer
globalFriendSecret = None
AccountSecret = 0
AvatarSecret = 1
BothSecrets = 2
offX = 0.8
offZ = 0.6

def showFriendSecret(secretType=AccountSecret):
    global globalFriendSecret
    if not Freebooter.getPaidStatus(localAvatar.getDoId()) and base.cr.productName == 'DisneyOnline-US':
        chatMgr = base.localAvatar.chatMgr
        chatMgr.fsm.request('unpaidChatWarning')
    elif not base.cr.allowSecretChat():
        chatMgr = base.localAvatar.chatMgr
        if base.cr.productName in ['DisneyOnline-AP', 'DisneyOnline-UK', 'ES', 'Wanadoo', 'T-Online', 'JP']:
            chatMgr = base.localAvatar.chatMgr
            if not Freebooter.getPaidStatus(localAvatar.getDoId()):
                chatMgr.fsm.request('unpaidChatWarning')
            else:
                chatMgr.paidNoParentPassword = 1
                chatMgr.fsm.request('unpaidChatWarning')
        else:
            chatMgr.fsm.request('noSecretChatAtAll')
    elif base.cr.needParentPasswordForSecretChat():
        unloadFriendSecret()
        globalFriendSecret = FriendSecretNeedsParentLogin(secretType)
        globalFriendSecret.enter()
    else:
        openFriendSecret(secretType)


def openFriendSecret(secretType):
    global globalFriendSecret
    if globalFriendSecret != None:
        globalFriendSecret.unload()
    globalFriendSecret = FriendSecret(secretType)
    globalFriendSecret.setPos(-0.75, 0, -0.45)
    globalFriendSecret.enter()
    return


def hideFriendSecret():
    if globalFriendSecret != None:
        globalFriendSecret.exit()
    return


def unloadFriendSecret():
    global globalFriendSecret
    if globalFriendSecret != None:
        globalFriendSecret.unload()
        globalFriendSecret = None
    return


class FriendSecretNeedsParentLogin(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendSecretNeedsParentLogin')

    def __init__(self, secretType):
        StateData.StateData.__init__(self, 'friend-secret-needs-parent-login-done')
        self.dialog = None
        self.secretType = secretType
        return

    def enter(self):
        StateData.StateData.enter(self)
        base.localAvatar.chatMgr.fsm.request('otherDialog')
        if self.dialog == None:
            charGui = loader.loadModel('models/gui/char_gui')
            buttonImage = (charGui.find('**/chargui_text_block_large'), charGui.find('**/chargui_text_block_large_down'), charGui.find('**/chargui_text_block_large_over'))
            self.dialog = GuiPanel.GuiPanel('Secret Codes!!! Arg!!', 1.6, 1.2, False)
            offX = -0.75
            offZ = -0.45
            self.dialog.setPos(offX, 0, offZ)
            okPos = (
             -0.22 - offX, 0.0, -0.3 - offZ)
            cancelPos = (0.2 - offX, 0.0, -0.3 - offZ)
            textPos = (0, 0.25)
            okCommand = self.__handleOK
            DirectButton(self.dialog, image=buttonImage, image_scale=(0.4, 1, 0.4), relief=None, text=OTPLocalizer.FriendSecretNeedsPasswordWarningOK, text_fg=PiratesGuiGlobals.TextFG2, text_scale=0.05, text_pos=(0.0, -0.01), textMayChange=0, pos=okPos, command=okCommand)
            DirectLabel(parent=self.dialog, relief=None, pos=(0 - offX, 0, 0.55 - offZ), text=OTPLocalizer.FriendSecretNeedsPasswordWarningTitle, text_fg=PiratesGuiGlobals.TextFG2, textMayChange=0, text_scale=0.08)
            if base.cr.productName != 'Terra-DMC':
                self.usernameLabel = DirectLabel(parent=self.dialog, relief=None, pos=(-0.07 - offX, 0.0, 0.1 - offZ), text=OTPLocalizer.ParentLogin, text_fg=PiratesGuiGlobals.TextFG2, text_scale=0.06, text_align=TextNode.ARight, textMayChange=0)
                self.usernameEntry = DirectEntry(parent=self.dialog, relief=None, text_fg=PiratesGuiGlobals.TextFG2, scale=0.064, pos=(0.0 - offX, 0.0, 0.1 - offZ), width=OTPGlobals.maxLoginWidth, numLines=1, focus=1, cursorKeys=1, obscured=1, suppressKeys=1, command=self.__handleUsername)
                self.passwordLabel = DirectLabel(parent=self.dialog, relief=None, pos=(-0.07 - offX, 0.0, -0.1 - offZ), text=OTPLocalizer.ParentPassword, text_fg=PiratesGuiGlobals.TextFG2, text_scale=0.06, text_align=TextNode.ARight, textMayChange=0)
                self.passwordEntry = DirectEntry(parent=self.dialog, relief=None, text_fg=PiratesGuiGlobals.TextFG2, scale=0.064, pos=(0.0 - offX, 0.0, -0.1 - offZ), width=OTPGlobals.maxLoginWidth, numLines=1, focus=1, cursorKeys=1, obscured=1, suppressKeys=1, command=self.__handleOK)
                DirectButton(self.dialog, image=buttonImage, image_scale=(0.4, 1, 0.4), relief=None, text=OTPLocalizer.FriendSecretNeedsPasswordWarningCancel, text_scale=0.05, text_pos=(0.0, -0.01), textMayChange=1, text_fg=PiratesGuiGlobals.TextFG2, pos=cancelPos, command=self.__handleCancel)
                self.usernameEntry['focus'] = 1
                self.usernameEntry.enterText('')
                charGui.removeNode()
        else:
            self.dialog['text'] = OTPLocalizer.FriendSecretNeedsParentLoginWarning
            if self.usernameEntry:
                self.usernameEntry['focus'] = 1
                self.usernameEntry.enterText('')
            elif self.passwordEntry:
                self.passwordEntry['focus'] = 1
                self.passwordEntry.enterText('')
        self.dialog.show()
        return

    def exit(self):
        print 'exit'
        self.ignoreAll()
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
        if self.isEntered:
            base.localAvatar.chatMgr.fsm.request('mainMenu')
            StateData.StateData.exit(self)
        return

    def __handleUsername(self, *args):
        if self.passwordEntry:
            self.passwordEntry['focus'] = 1
            self.passwordEntry.enterText('')

    def __oldHandleOK(self, *args):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        tt = base.cr.loginInterface
        okflag, message = tt.authenticateParentPassword(base.cr.userName, base.cr.password, password)
        if okflag:
            self.exit()
            openFriendSecret(self.secretType)
        elif message:
            base.localAvatar.chatMgr.fsm.request('problemActivatingChat')
            base.localAvatar.chatMgr.problemActivatingChat['text'] = OTPLocalizer.ProblemActivatingChat % message
        else:
            self.dialog['text'] = OTPLocalizer.FriendSecretNeedsPasswordWarningWrongPassword
            self.passwordEntry['focus'] = 1
            self.passwordEntry.enterText('')

    def __handleOK(self, *args):
        base.cr.parentUsername = self.usernameEntry.get()
        base.cr.parentPassword = self.passwordEntry.get()
        base.cr.playerFriendsManager.sendRequestUseLimitedSecret('', base.cr.parentUsername, base.cr.parentPassword)
        self.accept(OTPGlobals.PlayerFriendRejectUseSecretEvent, self.__handleParentLogin)
        self.__handleParentLogin(0)

    def __handleParentLogin(self, reason):
        if reason == 0:
            self.exit()
            openFriendSecret(self.secretType)
        elif reason == 1:
            self.dialog['text'] = OTPLocalizer.FriendSecretNeedsPasswordWarningWrongUsername
            self.usernameEntry['focus'] = 1
            self.usernameEntry.enterText('')
        elif reason == 2:
            self.dialog['text'] = OTPLocalizer.FriendSecretNeedsPasswordWarningWrongPassword
            self.passwordEntry['focus'] = 1
            self.passwordEntry.enterText('')
        else:
            base.localAvatar.chatMgr.fsm.request('problemActivatingChat')
            base.localAvatar.chatMgr.problemActivatingChat['text'] = OTPLocalizer.ProblemActivatingChat % message

    def __handleCancel(self):
        self.exit()


class FriendSecret(GuiPanel.GuiPanel, StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendSecret')

    def __init__(self, secretType):
        GuiPanel.GuiPanel.__init__(self, 'Secret Codes!!! Arg!!', 1.6, 1.2)
        StateData.StateData.__init__(self, 'friend-secret-done')
        self.initialiseoptions(FriendSecret)
        self.prefix = OTPGlobals.getDefaultProductPrefix()
        self.secretType = secretType
        self.notify.debug('### secretType = %s' % self.secretType)
        self.requestedSecretType = secretType
        self.notify.debug('### requestedSecretType = %s' % self.requestedSecretType)

    def unload(self):
        print 'unload'
        if self.isLoaded == 0:
            return None
        self.isLoaded = 0
        self.exit()
        del self.introText
        del self.getSecret
        del self.enterSecretText
        del self.enterSecret
        del self.ok1
        del self.ok2
        del self.cancel
        del self.secretText
        del self.avatarButton
        del self.accountButton
        GuiPanel.GuiPanel.destroy(self)
        return None

    def load(self):
        print 'load'
        if self.isLoaded == 1:
            return
        self.isLoaded = 1
        charGui = loader.loadModel('models/gui/char_gui')
        buttonImage = (charGui.find('**/chargui_text_block_large'), charGui.find('**/chargui_text_block_large_down'), charGui.find('**/chargui_text_block_large_over'))
        self.introText = DirectLabel(parent=self, relief=None, pos=(0 + offX, 0, 0.4 + offZ), scale=0.05, text=PLocalizer.FriendSecretIntro, text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=30)
        self.introText.hide()
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.getSecret = DirectButton(parent=self, relief=None, pos=(0 + offX, 0, -0.11 + offZ), image=buttonImage, image_scale=(0.85,
                                                                                                                                 1,
                                                                                                                                 0.4), text=OTPLocalizer.FriendSecretGetSecret, text_fg=PiratesGuiGlobals.TextFG2, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0, -0.02), command=self.__determineSecret)
        self.getSecret.hide()
        self.enterSecretText = DirectLabel(parent=self, relief=None, pos=(0 + offX, 0, -0.25 + offZ), text=OTPLocalizer.FriendSecretEnterSecret, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=30)
        self.enterSecretText.hide()
        self.enterSecret = DirectEntry(parent=self, relief=DGG.SUNKEN, scale=0.06, pos=(-0.6 + offX, 0, -0.38 + offZ), frameColor=(0.8,
                                                                                                                                   0.8,
                                                                                                                                   0.5,
                                                                                                                                   1), borderWidth=(0.1,
                                                                                                                                                    0.1), numLines=1, width=20, frameSize=(-0.4, 20.4, -0.4, 1.1), command=self.__enterSecret, suppressKeys=1)
        self.enterSecret.resetFrameSize()
        self.enterSecret.hide()
        self.ok1 = DirectButton(parent=self, relief=None, image=buttonImage, image_scale=(0.85,
                                                                                          1,
                                                                                          0.4), text=OTPLocalizer.FriendSecretEnter, text_fg=PiratesGuiGlobals.TextFG2, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0, -0.02), pos=(0 + offX, 0, -0.5 + offZ), command=self.__ok1)
        self.ok1.hide()
        self.ok2 = DirectButton(parent=self, relief=None, image=buttonImage, image_scale=(0.4,
                                                                                          1,
                                                                                          0.4), text=OTPLocalizer.FriendSecretOK, text_fg=PiratesGuiGlobals.TextFG2, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0, -0.02), pos=(0 + offX, 0, -0.5 + offZ), command=self.__ok2)
        self.ok2.hide()
        self.cancel = DirectButton(parent=self, relief=None, text=OTPLocalizer.FriendSecretCancel, image=buttonImage, image_scale=(0.4,
                                                                                                                                   1,
                                                                                                                                   0.4), text_fg=PiratesGuiGlobals.TextFG2, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0, -0.02), pos=(0 + offX, 0, -0.5 + offZ), command=self.__cancel)
        self.cancel.hide()
        self.nextText = DirectLabel(parent=self, relief=None, pos=(0 + offX, 0, 0.3 + offZ), scale=0.06, text='', text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=25.5)
        self.nextText.hide()
        self.secretText = DirectLabel(parent=self, relief=None, pos=(0 + offX, 0, -0.36 + offZ), scale=0.1, text='', text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=30)
        self.secretText.hide()
        charGui.removeNode()
        self.makeFriendTypeButtons()
        return

    def makeFriendTypeButtons(self):
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        self.avatarButton = DirectButton(self, relief=None, text=OTPLocalizer.FriendSecretDetermineSecretAvatar, text_scale=0.07, text_pos=(0.0, -0.1), pos=(-0.35 + offX, 0.0, -0.05 + offZ), command=self.__handleAvatar)
        avatarText = DirectLabel(parent=self, relief=None, pos=Vec3(0.35, 0, -0.3), text=OTPLocalizer.FriendSecretDetermineSecretAvatarRollover, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0,
                                                                                                                                                                                              0), text_scale=0.055, text_align=TextNode.ACenter)
        avatarText.reparentTo(self.avatarButton.stateNodePath[2])
        self.avatarButton.hide()
        self.accountButton = DirectButton(self, relief=None, text=OTPLocalizer.FriendSecretDetermineSecretAccount, text_scale=0.07, text_pos=(0.0, -0.1), pos=(0.35 + offX, 0.0, -0.05 + offZ), command=self.__handleAccount)
        accountText = DirectLabel(parent=self, relief=None, pos=Vec3(-0.35 + offX, 0, -0.3 + offZ), text=OTPLocalizer.FriendSecretDetermineSecretAccountRollover, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0,
                                                                                                                                                                                                               0), text_scale=0.055, text_align=TextNode.ACenter)
        accountText.reparentTo(self.accountButton.stateNodePath[2])
        self.accountButton.hide()
        return

    def enter(self):
        print 'enter'
        if self.isEntered == 1:
            return
        self.isEntered = 1
        if self.isLoaded == 0:
            self.load()
        self.show()
        self.introText.show()
        self.getSecret.show()
        self.enterSecretText.show()
        self.enterSecret.show()
        self.ok1.show()
        self.ok2.hide()
        self.cancel.hide()
        self.nextText.hide()
        self.secretText.hide()
        base.localAvatar.chatMgr.fsm.request('otherDialog')
        self.enterSecret['focus'] = 1
        NametagGlobals.setOnscreenChatForced(1)

    def closePanel(self):
        print 'closePanel'
        self.exit()

    def exit(self):
        print 'exit'
        if self.isEntered == 0:
            return
        self.isEntered = 0
        NametagGlobals.setOnscreenChatForced(0)
        self.__cleanupFirstPage()
        self.ignoreAll()
        self.hide()

    def __determineSecret(self):
        if self.secretType == BothSecrets:
            self.__cleanupFirstPage()
            self.ok1.hide()
            self.nextText['text'] = OTPLocalizer.FriendSecretDetermineSecret
            self.nextText.setPos(0, 0, 0.3)
            self.nextText.show()
            self.avatarButton.show()
            self.accountButton.show()
            self.cancel.show()
        else:
            self.__getSecret()

    def __handleAvatar(self):
        self.requestedSecretType = AvatarSecret
        self.__getSecret()

    def __handleAccount(self):
        self.requestedSecretType = AccountSecret
        self.__getSecret()

    def __handleCancel(self):
        self.exit()

    def __getSecret(self):
        self.__cleanupFirstPage()
        self.nextText['text'] = OTPLocalizer.FriendSecretGettingSecret
        self.nextText.setPos(0 + offX, 0, 0.3 + offZ)
        self.nextText.show()
        self.avatarButton.hide()
        self.accountButton.hide()
        self.ok1.hide()
        self.cancel.show()
        if self.requestedSecretType == AvatarSecret:
            if not base.cr.friendManager:
                self.notify.warning('No FriendManager available.')
                self.exit()
                return
            base.cr.friendManager.up_requestSecret()
            self.accept('requestSecretResponse', self.__gotAvatarSecret)
        else:
            if base.cr.needParentPasswordForSecretChat():
                base.cr.playerFriendsManager.sendRequestLimitedSecret(base.cr.parentUsername, base.cr.parentPassword)
            else:
                base.cr.playerFriendsManager.sendRequestUnlimitedSecret()
            self.accept(OTPGlobals.PlayerFriendNewSecretEvent, self.__gotAccountSecret)
            self.accept(OTPGlobals.PlayerFriendRejectNewSecretEvent, self.__rejectAccountSecret)

    def __gotAvatarSecret(self, result, secret):
        self.ignore('requestSecretResponse')
        if result == 1:
            self.nextText['text'] = OTPLocalizer.FriendSecretGotSecret
            self.nextText.setPos(0 + offX, 0, 0.47 + offZ)
            if self.prefix:
                self.secretText['text'] = self.prefix + ' ' + secret
            else:
                self.secretText['text'] = secret
        else:
            self.nextText['text'] = OTPLocalizer.FriendSecretTooMany
        self.nextText.show()
        self.secretText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    def __gotAccountSecret(self, secret):
        self.ignore(OTPGlobals.PlayerFriendNewSecretEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectNewSecretEvent)
        self.nextText['text'] = OTPLocalizer.FriendSecretGotSecret
        self.nextText.setPos(0 + offX, 0, 0.47 + offZ)
        self.secretText['text'] = secret
        self.nextText.show()
        self.secretText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    def __rejectAccountSecret(self, reason):
        self.ignore(OTPGlobals.PlayerFriendNewSecretEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectNewSecretEvent)
        self.nextText['text'] = OTPLocalizer.FriendSecretTooMany
        self.nextText.show()
        self.secretText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    def __enterSecret(self, secret):
        self.enterSecret.set('')
        secret = string.strip(secret)
        if not secret:
            self.exit()
            return
        if self.requestedSecretType == AvatarSecret:
            if not base.cr.friendManager:
                self.notify.warning('No FriendManager available.')
                self.exit()
                return
            self.__cleanupFirstPage()
            if self.prefix:
                if secret[0:2] == self.prefix:
                    secret = secret[3:]
                else:
                    self.__enteredSecret(4, 0)
                    return
            base.cr.friendManager.up_submitSecret(secret)
        else:
            self.__cleanupFirstPage()
            if base.cr.needParentPasswordForSecretChat():
                base.cr.playerFriendsManager.sendRequestUseLimitedSecret(secret, base.cr.parentUsername, base.cr.parentPassword)
            else:
                base.cr.playerFriendsManager.sendRequestUseUnlimitedSecret(secret)
        self.nextText['text'] = OTPLocalizer.FriendSecretTryingSecret
        self.nextText.setPos(0 + offX, 0, 0.3 + offZ)
        self.nextText.show()
        self.ok1.hide()
        self.cancel.show()
        self.accept(OTPGlobals.PlayerFriendAddEvent, self.__secretResponseOkay)
        self.accept(OTPGlobals.PlayerFriendRejectUseSecretEvent, self.__secretResponseReject)
        taskMgr.doMethodLater(10.0, self.__secretTimeout, 'timeoutSecretResponse')

    def __secretTimeout(self, caller=None):
        print '__secretTimeout'
        self.ignore(OTPGlobals.PlayerFriendAddEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectUseSecretEvent)
        self.nextText['text'] = OTPLocalizer.FriendSecretTimeOut
        return
        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    def __secretResponseOkay(self, avId, info):
        print '__secretResponseOkay'
        taskMgr.remove('timeoutSecretResponse')
        self.ignore(OTPGlobals.PlayerFriendAddEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectUseSecretEvent)
        self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretSuccess % info.playerName
        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    def __secretResponseReject(self, reason):
        print '__secretResponseReject'
        taskMgr.remove('timeoutSecretResponse')
        self.ignore(OTPGlobals.PlayerFriendAddEvent)
        self.ignore(OTPGlobals.PlayerFriendRejectUseSecretEvent)
        self.nextText['text'] = OTPLocalizer.FriendSecretEnteredSecretUnknown
        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()

    def __nowFriends(self, avId):
        self.ignore('friendsMapComplete')
        handle = base.cr.identifyAvatar(avId)
        if handle != None:
            self.nextText['text'] = OTPLocalizer.FriendSecretNowFriends % handle.getName()
        else:
            self.nextText['text'] = OTPLocalizer.FriendSecretNowFriendsNoName
        self.nextText.show()
        self.cancel.hide()
        self.ok1.hide()
        self.ok2.show()
        return

    def __ok1(self):
        secret = self.enterSecret.get()
        self.__enterSecret(secret)

    def __ok2(self):
        self.exit()

    def __cancel(self):
        self.exit()

    def __cleanupFirstPage(self):
        self.introText.hide()
        self.getSecret.hide()
        self.enterSecretText.hide()
        self.enterSecret.hide()
        base.localAvatar.chatMgr.fsm.request('mainMenu')