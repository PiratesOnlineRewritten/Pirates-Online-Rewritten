from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.piratesgui.BorderFrame import BorderFrame

class ChatWarningBox(BorderFrame):

    def __init__(self, badText='Error'):
        self.sizeX = 0.8
        self.sizeZ = 0.6
        textScale = PiratesGuiGlobals.TextScaleTitleSmall
        optiondefs = (('state', DGG.DISABLED, None), ('frameSize', (-0.0 * self.sizeX, 1.0 * self.sizeX, -0.0 * self.sizeZ, 1.0 * self.sizeZ), None), ('text', PLocalizer.ChatWarningTitle, None), ('text_align', TextNode.ACenter, None), ('text_font', PiratesGlobals.getPirateBoldOutlineFont(), None), ('text_fg', (1, 1, 1, 1), None), ('text_shadow', PiratesGuiGlobals.TextShadow, None), ('textMayChange', 1, None), ('text_scale', textScale, None), ('text_pos', (self.sizeX * 0.5, self.sizeZ - textScale * 1.5), None))
        self.defineoptions({}, optiondefs)
        BorderFrame.__init__(self, parent=NodePath())
        self.initialiseoptions(ChatWarningBox)
        self.setX(self.sizeX * -0.5)
        self.badText = badText
        self.warningText = badText
        self.setup()
        return

    def setup(self):
        self.setBin('gui-popup', 100)
        Gui = loader.loadModel('models/gui/toplevel_gui')
        buttonImage = (Gui.find('**/generic_button'), Gui.find('**/generic_button_down'), Gui.find('**/generic_button_over'), Gui.find('**/generic_button_disabled'))
        textScale = PiratesGuiGlobals.TextScaleLarge
        self.messageLabel = DirectLabel(parent=self, relief=None, text=self.warningText, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ALeft, text_scale=textScale, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=self.sizeX * 0.9 / textScale, text_pos=(self.sizeX * -0.425, 0.066), pos=(self.sizeX * 0.5, 0.0, self.sizeZ * 0.5))
        generic_x = Gui.find('**/generic_x')
        generic_box = Gui.find('**/generic_box')
        generic_box_over = Gui.find('**/generic_box_over')
        self.cancelButton = DirectButton(parent=self, relief=None, image=buttonImage, image_scale=(0.28,
                                                                                                   1.0,
                                                                                                   0.22), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=PLocalizer.ChatWarningClose, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(self.sizeX * 0.5, 0, 0.1), command=self.requestClose)
        return

    def requestClose(self):
        self.close()
        localAvatar.guiMgr.closeSystemWarning()

    def close(self):
        self.destroy()