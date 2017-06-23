from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.RequestButton import RequestButton

class FriendInviteeButton(RequestButton):

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(FriendInviteeButton)


class FriendInvitee(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendInvitee')

    def __init__(self, avId, avName, isPlayerInvite):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief=None, pos=(-0.6, 0, 0.47), image=guiMain.find('**/general_frame_e'), image_pos=(0.25,
                                                                                                                          0,
                                                                                                                          0.275), image_scale=0.25)
        self.initialiseoptions(FriendInvitee)
        self.avId = avId
        self.avName = avName
        self.isPlayerInvite = isPlayerInvite
        if base.cr.avatarFriendsManager.checkIgnored(self.avId):
            self.__handleNo()
            return
        nameArray = (
         '\x01CPOrangeHEAD\x01' + self.avName + '\x02', '\x01CPOrangeHEAD\x01' + self.avName + '\x02', '\x01CPOrangeOVER\x01' + self.avName + '\x02', '\x01CPOrangeHEAD\x01' + self.avName + '\x02')
        nameButton = DirectButton(parent=NodePath(), relief=None, text=nameArray, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, command=self.handleAvatarPress, extraArgs=[avId, avName])
        left, right, bottom, top = nameButton.getBounds()
        nameGFX = TextGraphic(nameButton, left, right, 0, 1)
        buttonName = '\x05' + self.avName + '\x05'
        buttonText = PLocalizer.CrewInviteeInvitation % buttonName
        tpMgr = TextPropertiesManager.getGlobalPtr()
        tpMgr.setGraphic(self.avName, nameGFX)
        del tpMgr
        if self.isPlayerInvite:
            text = OTPLocalizer.FriendInviteeInvitationPlayer % self.avName
        else:
            text = OTPLocalizer.FriendInviteeInvitation % buttonName
        self.title = DirectLabel(parent=self, relief=None, text=PLocalizer.FriendInviteeTitle, text_scale=PiratesGuiGlobals.TextScaleExtraLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateOutlineFont(), text_pos=(0,
                                                                                                                                                                                                                                                                                                                      0), pos=(0.25,
                                                                                                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                                                                                                               0.42), image=None, image_scale=0.25)
        self.message = DirectLabel(parent=self, relief=None, text=text, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.25,
                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                      0.325), textMayChange=1)
        self.bOk = FriendInviteeButton(text=OTPLocalizer.FriendInviteeOK, command=self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.1, 0, 0.05)
        self.bNo = FriendInviteeButton(text=OTPLocalizer.FriendInviteeNo, command=self.__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.05)
        self.accept('cancelFriendInvitation', self.__handleCancelFromAbove)
        return

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('cancelFriendInvitation')
        DirectFrame.destroy(self)

    def __handleOk(self):
        if self.isPlayerInvite:
            base.cr.playerFriendsManager.sendRequestInvite(self.avId)
        else:
            base.cr.avatarFriendsManager.sendRequestInvite(self.avId)
        self.destroy()

    def __handleNo(self):
        if self.isPlayerInvite:
            base.cr.playerFriendsManager.sendRequestDecline(self.avId)
        else:
            base.cr.avatarFriendsManager.sendRequestRemove(self.avId)
        self.destroy()

    def __handleCancelFromAbove(self):
        self.destroy()

    def handleAvatarPress(self, avId, avName):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            base.localAvatar.guiMgr.handleAvatarDetails(avId, avName)