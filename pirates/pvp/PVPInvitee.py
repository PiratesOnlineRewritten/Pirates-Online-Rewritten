from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PDialog
from pirates.piratesgui import SocialPage
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.RequestButton import RequestButton

class PVPInviteeButton(RequestButton):

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(PVPInviteeButton)


class PVPInvitee(SocialPage.SocialPage):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPInvitee')

    def __init__(self, avId, avName):
        SocialPage.SocialPage.__init__(self, 'PVPInvitee')
        self.initialiseoptions(PVPInvitee)
        self.setPos(-0.6, 0, 0.47)
        self.avId = avId
        self.avName = avName
        guiMain = loader.loadModel('models/gui/gui_main')
        self.box = OnscreenImage(parent=self, pos=(0.25, 0, 0.275), image=guiMain.find('**/general_frame_e'), scale=0.25)
        self.title = DirectLabel(parent=self, relief=None, text=PLocalizer.PVPInviteeTitle, text_scale=PiratesGuiGlobals.TextScaleExtraLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateOutlineFont(), pos=(0.25,
                                                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                                                              0.42), image=None, image_scale=0.25)
        text = PLocalizer.PVPInviteeInvitation % self.avName
        self.message = DirectLabel(parent=self, relief=None, text=text, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.25,
                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                      0.325), textMayChange=1)
        self.bOk = PVPInviteeButton(text=OTPLocalizer.DialogOK, command=self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.1, 0, 0.1)
        self.bNo = PVPInviteeButton(text=OTPLocalizer.DialogNo, command=self.__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.1)
        self.accept('cancelChallengeInvitation', self.__handleCancelFromAbove)
        return

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('cancelChallengeInvitation')
        GuiPanel.GuiPanel.destroy(self)

    def __handleOk(self):
        base.cr.pvpManager.sendAcceptChallenge(self.avId)
        self.destroy()

    def __handleNo(self):
        self.destroy()

    def __handleCancelFromAbove(self):
        self.destroy()