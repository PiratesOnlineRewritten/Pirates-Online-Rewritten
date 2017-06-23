from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.band import BandConstance
from pirates.piratesgui.RequestButton import RequestButton

class PiratesConfirmButton(RequestButton):

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(PiratesConfirmButton)


class PiratesConfirm(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesConfirm')

    def __init__(self, title, message, command, avId=None, tattoo=None, barber=None, titleScale=PiratesGuiGlobals.TextScaleExtraLarge):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief=None, pos=(-0.6, 0, 0.47), image=guiMain.find('**/general_frame_e'), image_pos=(0.25,
                                                                                                                          0,
                                                                                                                          0.275), image_scale=0.25)
        self.initialiseoptions(PiratesConfirm)
        self.command = command
        self.avId = avId
        self.tattoo = tattoo
        self.barber = barber
        if avId is not None and base.cr.avatarFriendsManager.checkIgnored(self.avId):
            self.__handleNo()
            return
        self.title = DirectLabel(parent=self, relief=None, text=title, text_scale=titleScale, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateOutlineFont(), pos=(0.25,
                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                              0.42), image=None, image_scale=0.25)
        text = message
        self.message = DirectLabel(parent=self, relief=None, text=message, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.25,
                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                         0.325), textMayChange=1)
        self.bOk = PiratesConfirmButton(text=PLocalizer.GenericConfirmOK, command=self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.1, 0, 0.05)
        self.bNo = PiratesConfirmButton(text=PLocalizer.GenericConfirmNo, command=self.__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.05)
        self.accept('clientLogout', self.destroy)
        return

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('BandRequestCancel-%s' % (self.avId,))
        self.ignore('BandRejoinCancel-%s' % (self.avId,))
        self.ignore('Esc')
        DirectFrame.destroy(self)

    def __handleOk(self):
        if self.avId:
            self.command(self.avId)
        elif self.tattoo:
            self.command(self.tattoo[0], self.tattoo[1], self.tattoo[2])
        elif self.barber:
            self.command(self.barber[0], self.barber[1], self.barber[2])
        else:
            self.command()
        self.destroy()

    def __handleNo(self):
        self.destroy()

    def __handleCancelFromAbove(self):
        self.destroy()