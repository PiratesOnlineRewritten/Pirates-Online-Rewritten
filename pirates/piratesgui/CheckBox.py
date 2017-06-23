from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import Task
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from direct.gui.DirectCheckBox import DirectCheckBox

class CheckBox(DirectCheckBox):

    def __init__(self, text, command):
        self.charGui = loader.loadModel('models/gui/toplevel_gui')
        uncheckedImage = (self.charGui.find('**/main_gui_checkbox_off'), self.charGui.find('**/main_gui_checkbox_halfcheck'), self.charGui.find('**/main_gui_checkbox_off_over'), self.charGui.find('**/main_gui_checkbox_off_disable'))
        checkedImage = (
         self.charGui.find('**/main_gui_checkbox_on'), self.charGui.find('**/main_gui_checkbox_halfcheck'), self.charGui.find('**/main_gui_checkbox_on_over'), self.charGui.find('**/main_gui_checkbox_on_disable'))
        DirectCheckBox.__init__(self, relief=None, pos=(0, 0, 0), text=text, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.08,
                                                                                                                                                                                                                                              0.025), image=uncheckedImage, image_scale=(0.07,
                                                                                                                                                                                                                                                                                         0.07,
                                                                                                                                                                                                                                                                                         0.07), image_pos=(-0.01, 0.0, 0.035), command=command, uncheckedImage=uncheckedImage, checkedImage=checkedImage)
        self.initialiseoptions(CheckBox)
        self.charGui.removeNode()
        return