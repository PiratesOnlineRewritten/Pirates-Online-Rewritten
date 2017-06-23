from pandac.PandaModules import *
from direct.task import Task
from direct.gui.DirectGui import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiTray
from pirates.piratesgui.BorderFrame import BorderFrame
import PVPGlobals

class PVPRulesPanel(BorderFrame):

    def __init__(self, panelName, gameTitle, instructions):
        BorderFrame.__init__(self, parent=base.a2dBottomCenter, frameSize=(-1, 1, 0,
                                                                           0.3), pos=(0,
                                                                                      0,
                                                                                      0.5), modelName='pir_m_gui_frm_subframe', imageColorScale=VBase4(0.75, 0.75, 0.9, 0.75))
        self.initialiseoptions(PVPRulesPanel)
        self.secondLayer = BorderFrame(parent=self, frameSize=(-1, 1, 0, 0.3), modelName='pir_m_gui_frm_subframe', imageColorScale=VBase4(0.75, 0.75, 0.9, 0.75))
        self.gameTitle = gameTitle
        self.instructions = instructions
        self.gameTitleText = DirectLabel(parent=self, relief=None, text=self.gameTitle, text_scale=0.06, text_align=TextNode.ALeft, text_font=PiratesGlobals.getPirateFont(), text_fg=(1,
                                                                                                                                                                                       1,
                                                                                                                                                                                       1,
                                                                                                                                                                                       1), text_shadow=(0,
                                                                                                                                                                                                        0,
                                                                                                                                                                                                        0,
                                                                                                                                                                                                        1), pos=(-0.96, 0, 0.23))
        self.instructionsText = DirectLabel(parent=self, relief=None, text=self.instructions, text_scale=0.05, text_align=TextNode.ALeft, text_wordwrap=40, text_fg=(1,
                                                                                                                                                                     1,
                                                                                                                                                                     1,
                                                                                                                                                                     1), text_shadow=(0,
                                                                                                                                                                                      0,
                                                                                                                                                                                      0,
                                                                                                                                                                                      1), pos=(-0.96, 0, 0.14))
        return