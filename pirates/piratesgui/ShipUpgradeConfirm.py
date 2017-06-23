from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.RequestButton import RequestButton

class PiratesConfirmButton(RequestButton):

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(PiratesConfirmButton)


class ShipUpgradeConfirm(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesConfirm')

    def __init__(self, title, message, commandOkay, commandCancel, titleScale=PiratesGuiGlobals.TextScaleExtraLarge):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief=None, pos=(-0.6, 0, 0.47), image=guiMain.find('**/general_frame_e'), image_pos=(0.25,
                                                                                                                          0,
                                                                                                                          0.275), image_scale=0.25)
        self.initialiseoptions(ShipUpgradeConfirm)
        self.setBin('gui-fixed', 0)
        self.commandOkay = commandOkay
        self.commandCancel = commandCancel
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
        return

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('Esc')
        DirectFrame.destroy(self)

    def __handleOk(self):
        if self.commandOkay:
            self.commandOkay()
        self.destroy()

    def __handleNo(self):
        if self.commandCancel:
            self.commandCancel()
        self.destroy()