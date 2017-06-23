from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.band import BandConstance
from pirates.piratesgui.RequestButton import RequestButton

class CrewBootButton(RequestButton):

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewBootButton)


class CrewBoot(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('CrewBoot')

    def __init__(self, avId, avName):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief=None, pos=(-0.6, 0, 0.47), image=guiMain.find('**/general_frame_e'), image_pos=(0.25,
                                                                                                                          0,
                                                                                                                          0.275), image_scale=0.25)
        self.initialiseoptions(CrewBoot)
        self.avId = avId
        self.avName = avName
        self.title = DirectLabel(parent=self, relief=None, text=PLocalizer.CrewBootTitle, text_scale=PiratesGuiGlobals.TextScaleExtraLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateOutlineFont(), pos=(0.25,
                                                                                                                                                                                                                                                                                                            0,
                                                                                                                                                                                                                                                                                                            0.42))
        text = PLocalizer.CrewBootMessage % self.avName
        self.message = DirectLabel(parent=self, relief=None, text=text, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.25,
                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                      0.325), textMayChange=1)
        self.bOk = CrewBootButton(text=PLocalizer.CrewBootOK, command=self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.1, 0, 0.05)
        self.bNo = CrewBootButton(text=PLocalizer.CrewBootNo, command=self.__handleNo)
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
        base.cr.PirateBandManager.d_requestBoot(self.avId)
        self.destroy()

    def __handleNo(self):
        self.destroy()

    def __handleCancelFromAbove(self):
        self.destroy()