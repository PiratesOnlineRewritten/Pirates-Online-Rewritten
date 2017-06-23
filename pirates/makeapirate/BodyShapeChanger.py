from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui import GuiButton
from pirates.pirate import BodyDefs
from pirates.piratesgui import PDialog
from otp.otpgui import OTPDialog

class BodyShapeChanger(BorderFrame):

    def __init__(self, **kw):
        self.sizeX = 0.8
        self.sizeZ = 0.9
        textScale = PiratesGuiGlobals.TextScaleTitleSmall
        optiondefs = (('state', DGG.DISABLED, None), ('frameSize', (-0.0 * self.sizeX, 1.0 * self.sizeX, -0.0 * self.sizeZ, 1.0 * self.sizeZ), None), ('text', PLocalizer.BodyShapeUpdate, None), ('text_align', TextNode.ACenter, None), ('text_font', PiratesGlobals.getPirateBoldOutlineFont(), None), ('text_fg', (1, 1, 1, 1), None), ('text_shadow', PiratesGuiGlobals.TextShadow, None), ('textMayChange', 1, None), ('text_scale', textScale, None), ('text_pos', (self.sizeX * 0.5, self.sizeZ * 0.95 - textScale), None))
        self.defineoptions(kw, optiondefs)
        BorderFrame.__init__(self)
        self.initialiseoptions(BodyShapeChanger)
        self.setPos(base.a2dRight - self.sizeX, 0, 0)
        self.confirmDialog = None
        self.isSetup = 0
        self.doingRegen = 0
        self.acceptOnce('localAV-enterHalt', self.setup)
        localAvatar.gameFSM.request('Halt')
        if not self.isSetup:
            self.destroy()
        return

    def destroy(self):
        base.localAvatar.guiMgr.setIgnoreMainMenuHotKey(True)
        base.localAvatar.guiMgr.setIgnoreAllKeys(False)
        base.localAvatar.guiMgr.hideSeaChest()
        base.localAvatar.guiMgr.setIgnoreMainMenuHotKey(False)
        self.ignoreAll()
        BorderFrame.destroy(self)
        if self.confirmDialog:
            self.confirmDialog.destroy()
        localAvatar.gameFSM.request('LandRoam')

    def setup(self):
        self.isSetup = 1
        self.setBin('gui-fixed', 0)
        self.messageLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.BodyChangeText, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=18, text_shadow=PiratesGuiGlobals.TextShadow, pos=(self.sizeX * 0.05, 0.0, self.sizeZ * 0.8))
        Gui = loader.loadModel('models/gui/toplevel_gui')
        buttonImage = (Gui.find('**/generic_button'), Gui.find('**/generic_button_down'), Gui.find('**/generic_button_over'), Gui.find('**/generic_button_disabled'))
        self.confirmButton = DirectButton(parent=self, relief=None, image=buttonImage, image_scale=(0.42,
                                                                                                    1.0,
                                                                                                    0.22), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=PLocalizer.BodyTypeCommit, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(self.sizeX * 0.5, 0, 0.17), command=self.confirmBody)
        self.cancelButton = DirectButton(parent=self, relief=None, image=buttonImage, image_scale=(0.42,
                                                                                                   1.0,
                                                                                                   0.22), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=PLocalizer.BodyTypeLater, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(self.sizeX * 0.5, 0, 0.07), command=self.cancelBody)
        self.confirmButton['state'] = DGG.DISABLED
        main_gui = loader.loadModel('models/gui/gui_main')
        generic_x = main_gui.find('**/x2')
        generic_box = main_gui.find('**/exit_button')
        generic_box_over = main_gui.find('**/exit_button_over')
        main_gui.removeNode()
        closeButton = GuiButton.GuiButton(parent=self, relief=None, pos=(1.0, 0, 0.06), image=(generic_box, generic_box, generic_box_over, generic_box), image_scale=0.4, command=self.cancelBody)
        xButton = OnscreenImage(parent=closeButton, image=generic_x, scale=0.2, pos=(-0.256, 0, 0.766))
        choices = None
        self.originalBody = localAvatar.getStyle().getBodyShape()
        self.bodyChoice = None
        gender = localAvatar.getStyle().gender
        if gender == 'f':
            choices = BodyDefs.BodyChoicesFemale
        elif gender == 'm':
            choices = BodyDefs.BodyChoicesMale
        xCount = 0
        for choice in choices:
            choiceButton = DirectButton(parent=self, relief=None, image=buttonImage, image_scale=(0.12,
                                                                                                  1.0,
                                                                                                  0.22), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text='%s' % (xCount + 1), text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.1 + 0.14 * xCount, 0, 0.27), command=self.chooseType, extraArgs=[choice])
            xCount += 1

        self.accept('localAV-exitHalt', self.cancelBody)
        self.accept('localAv-regenerate', self.cancelBody)
        return

    def chooseType(self, choice):
        self.confirmButton['state'] = DGG.NORMAL
        self.bodyChoice = choice
        localAvatar.setBodyShape(choice)
        self.doingRegen = 1
        localAvatar.doRegeneration()
        self.doingRegen = 0

    def cancelBody(self):
        if self.doingRegen:
            return
        if localAvatar.getGameState() not in 'Halt':
            self.destroy()
            return
        localAvatar.setBodyShape(self.originalBody)
        self.doingRegen = 1
        localAvatar.doRegeneration()
        self.doingRegen = 0
        self.destroy()

    def confirmBody(self):
        self.hide()
        self.confirmDialog = PDialog.PDialog(text=PLocalizer.BodyTypeConfirm, style=OTPDialog.YesNo, command=self.doConfirmBody)

    def doConfirmBody(self, choice):
        print 'doConfirmBody %s' % choice
        if localAvatar.getGameState() not in 'Halt':
            self.destroy()
            return
        if choice == 1:
            localAvatar.sendUpdate('requestBodyShapeTranslation', [self.bodyChoice])
            localAvatar.guiMgr.bodySelectGui.remove()
            self.destroy()
        else:
            self.confirmDialog.remove()
            self.confirmDialog = None
            self.show()
            self.cancelBody()
        return