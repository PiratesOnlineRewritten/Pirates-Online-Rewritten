from pandac.PandaModules import TextNode
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpgui import OTPDialog
from pirates.piratesbase import PLocalizer, PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import GuiButton
from pirates.piratesgui import CheckButton

class SkipTutorialFrame(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('SkipTutorialFrame')

    def __init__(self, callback):
        topGui = loader.loadModel('models/gui/toplevel_gui')
        lookoutGui = loader.loadModel('models/gui/lookout_gui')
        DirectFrame.__init__(self, relief=None, image=topGui.find('**/pir_t_gui_gen_parchment'), image_scale=(0.33,
                                                                                                              0,
                                                                                                              0.44))
        self.initialiseoptions(SkipTutorialFrame)
        self.title = DirectLabel(parent=self, relief=None, text=PLocalizer.SkipTutorialTitle, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_fg=(0.6,
                                                                                                                                                         0.0,
                                                                                                                                                         0.0,
                                                                                                                                                         1.0), text_font=PiratesGlobals.getPirateOutlineFont(), text_align=TextNode.ACenter, pos=(0.02,
                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                  0.13))
        self.message = DirectLabel(parent=self, relief=None, text=PLocalizer.SkipTutorialOffer, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG0, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=14, pos=(0.02,
                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                              0.05))
        self.callback = callback
        self.checkButton = GuiButton.GuiButton(parent=self, relief=None, text=PLocalizer.SkipTutorialNo, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.11, -0.01), text0_fg=PiratesGuiGlobals.TextFG0, text_shadow=PiratesGuiGlobals.TextShadow, image=(lookoutGui.find('**/lookout_submit'), lookoutGui.find('**/lookout_submit_down'), lookoutGui.find('**/lookout_submit_over'), lookoutGui.find('**/lookout_submit')), image_scale=0.17, image_color=(0.5,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     0.0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     0.0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     1.0), pos=(-0.17, 0, -0.1), command=self.__handleNo)
        self.cancelButton = GuiButton.GuiButton(parent=self, relief=None, text=PLocalizer.SkipTutorialYes, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.09, -0.01), text0_fg=PiratesGuiGlobals.TextFG0, text_shadow=PiratesGuiGlobals.TextShadow, image=(lookoutGui.find('**/lookout_close_window'), lookoutGui.find('**/lookout_close_window_down'), lookoutGui.find('**/lookout_close_window_over'), lookoutGui.find('**/lookout_close_window')), image_scale=0.17, image_color=(0.5,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               0.0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               0.0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               1.0), pos=(0.07, 0, -0.1), command=self.__handleYes)
        topGui.removeNode()
        lookoutGui.removeNode()
        return

    def destroy(self):
        DirectFrame.destroy(self)

    def __handleYes(self):
        self.callback(True)
        self.destroy()

    def __handleNo(self):
        self.callback(False)
        self.destroy()