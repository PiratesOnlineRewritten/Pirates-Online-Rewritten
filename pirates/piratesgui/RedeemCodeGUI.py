from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesgui import GuiButton
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PDialog
from otp.otpgui import OTPDialog
from pirates.coderedemption import CodeRedemptionGlobals

class RedeemCodeGUI(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('RedeemCodeGUI')

    def __init__(self, parent, **kw):
        optiondefs = (('relief', None, None), )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        self.initialiseoptions(RedeemCodeGUI)
        gui_main = loader.loadModel('models/gui/gui_main')
        topImage = gui_main.find('**/game_options_panel/top')
        topImage.setPos(0.52, 0, -0.15)
        gui_main.removeNode()
        self.artFrame = DirectFrame(parent=aspect2dp, relief=None, image=topImage, image_scale=(0.24,
                                                                                                0.24,
                                                                                                0.24), pos=(0.1, 0.0, -0.2))
        self.artFrame.setBin('gui-fixed', 2)
        self.blackout = DirectFrame(parent=aspect2dp, state=DGG.NORMAL, frameSize=(-5,
                                                                                   5,
                                                                                   -5,
                                                                                   5), frameColor=(0.0,
                                                                                                   0.0,
                                                                                                   0.0,
                                                                                                   0.4), pos=(0.0,
                                                                                                              0.0,
                                                                                                              0.0))
        self.enterCode = GuiButton.GuiButton(parent=self.artFrame, text=PLocalizer.lConfirm, pos=(0.385, 0.0, -0.025), command=self.confirmCode)
        self.cancelCode = GuiButton.GuiButton(parent=self.artFrame, text=PLocalizer.lCancel, pos=(0.65, 0.0, -0.025), command=self.hideCode)
        DirectLabel(parent=self.artFrame, relief=None, text=PLocalizer.ShopEnterCode, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleTitleSmall * 0.9, text_pos=(0.51,
                                                                                                                                                                                     0.335), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getInterfaceOutlineFont(), textMayChange=0)
        DirectLabel(parent=self.artFrame, relief=None, text=PLocalizer.ShopCodeInst, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge * 1.1, text_pos=(0.51,
                                                                                                                                                                               0.25), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getInterfaceOutlineFont(), textMayChange=0, text_wordwrap=12)
        self.codeInput = DirectEntry(parent=self.artFrame, relief=DGG.GROOVE, scale=PiratesGuiGlobals.TextScaleExtraLarge, pos=(0.52,
                                                                                                                                0,
                                                                                                                                0.06), borderWidth=PiratesGuiGlobals.BorderWidth, frameColor=(0.0,
                                                                                                                                                                                              0.0,
                                                                                                                                                                                              0.0,
                                                                                                                                                                                              1.0), text_align=TextNode.ACenter, width=15, numLines=1, focus=1, cursorKeys=1, text_fg=(1,
                                                                                                                                                                                                                                                                                       1,
                                                                                                                                                                                                                                                                                       1,
                                                                                                                                                                                                                                                                                       1), suppressKeys=1, suppressMouse=1, autoCapitalize=0, command=self.confirmCode)
        self.alertDialog = None
        self.accept('codeRedeemed', self.__handleCodeRedeem)
        return

    def confirmCode(self, input=None):
        if input == None:
            input = self.codeInput.get()
        self.codeInput.enterText('')
        self.hideCode(1)
        if self.alertDialog:
            self.alertDialog.destroy()
            self.alertDialog = None
        if input == None or len(input) == 0:
            self.alertDialog = PDialog.PDialog(parent=aspect2dp, text=PLocalizer.ShopCodeErr, style=OTPDialog.CancelOnly, command=self.__handleAlert, destroyedCallback=self.__destroyedAlert)
            self.alertDialog.setPos(0.6, 0, 0.1)
            self.alertDialog.setBin('gui-fixed', 2)
        else:
            localAvatar.submitCodeToServer(input)
        return

    def __destroyedAlert(self):
        self.alertDialog = None
        return

    def __handleCodeRedeem(self, value):
        if self.alertDialog:
            self.alertDialog.destroy()
            self.alertDialog = None
        if value == CodeRedemptionGlobals.ERROR_ID_GOOD:
            self.alertDialog = PDialog.PDialog(parent=aspect2dp, text=PLocalizer.ShopCodeSuccess, style=OTPDialog.CancelOnly, command=self.__handleCodeSuccess, destroyedCallback=self.__destroyedAlert)
        elif value == CodeRedemptionGlobals.ERROR_ID_OVERFLOW:
            self.alertDialog = PDialog.PDialog(parent=aspect2dp, text=PLocalizer.ShopCodeFull, style=OTPDialog.CancelOnly, command=self.__handleCodeSuccess, destroyedCallback=self.__destroyedAlert)
        else:
            self.alertDialog = PDialog.PDialog(parent=aspect2dp, text=PLocalizer.ShopCodeErr, style=OTPDialog.CancelOnly, command=self.__handleAlert, destroyedCallback=self.__destroyedAlert)
        self.alertDialog.setPos(0.6, 0, 0.1)
        self.alertDialog.setBin('gui-fixed', 2)
        return

    def __handleCodeSuccess(self, value=None):
        self.hideCode()
        if self.alertDialog:
            self.alertDialog.destroy()
            self.alertDialog = None
        return

    def __handleAlert(self, value=None):
        if value == -1:
            if self.alertDialog:
                self.alertDialog.destroy()
                self.alertDialog = None
            self.showCode()
        return

    def hideCode(self, option=0):
        self.artFrame.hide()
        if option == 0:
            self.blackout.hide()
        self.codeInput.enterText('')
        self.codeInput.hide()

    def showCode(self):
        self.artFrame.show()
        self.blackout.show()
        self.codeInput.show()

    def destroy(self):
        DirectFrame.destroy(self)
        if self.artFrame:
            self.artFrame.destroy()
        if self.blackout:
            self.blackout.destroy()
        if self.codeInput:
            self.codeInput.destroy()
        if self.alertDialog:
            self.alertDialog.destroy()