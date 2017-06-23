import os
import sys
from direct.gui.DirectGui import *
from direct.task.Task import Task
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import UserFunnel
from pirates.piratesbase import PiratesGlobals
try:
    import embedded
    hasEmbedded = 1
except ImportError:
    hasEmbedded = 0

class TrialNonPayerPanel(DirectFrame):

    def __init__(self, w=9.0, h=6.0, trial=False, lock=True):
        self.width = w
        self.height = h
        self.imageFocus = 0
        self.hasEmbedded = hasEmbedded
        self.trial = trial
        if not self.trial:
            self.questIdReporting = 'None_Provided'
        self.__fader = None
        DirectFrame.__init__(self, relief=DGG.RIDGE, state=DGG.NORMAL, frameColor=Vec4(0.0, 0.0, 0.0, 0.7), borderWidth=PiratesGuiGlobals.BorderWidth, frameSize=(0, self.width, 0, self.height), pos=(-4.5,
                                                                                                                                                                                                       0,
                                                                                                                                                                                                       -3.0), sortOrder=999)
        self.initialiseoptions(TrialNonPayerPanel)
        if not self.trial:
            gui2 = loader.loadModel('models/gui/gui_main').find('**/velvetrope_top')
            geom = gui2.find('**/background')
            self.imageOne = DirectFrame(parent=self, relief=None, image=geom, image_scale=(1,
                                                                                           1,
                                                                                           0.95), scale=0.4, pos=(4.45,
                                                                                                                  0,
                                                                                                                  3.1))
            geom = gui2.find('**/frame')
            geom.getChild(0).stash()
            self.imageTwo = DirectFrame(parent=self.imageOne, relief=None, image=geom, scale=1.0, pos=(0,
                                                                                                       0,
                                                                                                       0))
            self.titleText = DirectLabel(parent=self.imageOne, relief=None, text=PLocalizer.VR_FeaturePopTitle, text_align=TextNode.ACenter, text_scale=0.2, text_fg=PiratesGuiGlobals.TextFG16, text_font=PiratesGlobals.getPirateFont(), text_shadow=PiratesGuiGlobals.TextShadow, pos=(0,
                                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                                          0.2))
            self.fullText = DirectLabel(parent=self.imageOne, relief=None, text=PLocalizer.VR_FeaturePopLongText, text_align=TextNode.ACenter, text_scale=0.1, text_fg=PiratesGuiGlobals.TextFG16, text_font=PiratesGlobals.getInterfaceFont(), pos=(0, 0, -0.1))
            upgrade_button = gui2.find('**/upgrade_button')
            norm_geom = upgrade_button.find('**/normal')
            over_geom = upgrade_button.find('**/over')
            down_geom = upgrade_button.find('**/down')
            self.upgradeButton = DirectButton(parent=self.imageOne, relief=None, geom=(norm_geom, down_geom, over_geom), pos=(0,
                                                                                                                              0,
                                                                                                                              0.05), scale=1, command=self.upgradeNow, text=PLocalizer.VR_FirstAddUpgrade, text_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getInterfaceFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_scale=0.09, text_pos=(0, -0.64))
            norm_geom.getChild(0).stash()
            over_geom.getChild(0).stash()
            down_geom.getChild(0).stash()
            self.passButton = DirectButton(parent=self.imageOne, relief=None, geom=(norm_geom, down_geom, over_geom), scale=(0.8,
                                                                                                                             1,
                                                                                                                             0.1), text=PLocalizer.VR_FirstAddBasic, text_fg=PiratesGuiGlobals.TextFG15, text_font=PiratesGlobals.getInterfaceFont(), text_scale=(0.125,
                                                                                                                                                                                                                                                                  0.8), text_pos=(0, -0.45), pos=(0, 0, -0.75), command=self.dismissNow)
            basegeom = gui2.find('**/close_button')
            norm_geom = basegeom.find('**/normal')
            over_geom = basegeom.find('**/over')
            down_geom = basegeom.find('**/down')
            self.dismissButton = DirectButton(parent=self, relief=None, geom=(norm_geom, down_geom, over_geom), scale=0.4, pos=(4.45,
                                                                                                                                0,
                                                                                                                                3.1), command=self.dismissNow)
        else:
            gui2 = loader.loadModel('models/textureCards/basic_unlimited')
            self.imageOne = DirectFrame(parent=self, relief=None, image=gui2.find('**/but_message_panel_border'), image_scale=(1,
                                                                                                                               1,
                                                                                                                               0.95), scale=0.8, pos=(4.5,
                                                                                                                                                      0,
                                                                                                                                                      3.0))
            self.imageTwo = DirectFrame(parent=self.imageOne, relief=None, image=gui2.find('**/but_compass'), scale=1.0, pos=(-0.49, 0, 0.22))
            self.titleText = DirectLabel(parent=self.imageOne, relief=None, text=PLocalizer.FirstAddTitle, text_align=TextNode.ALeft, text_scale=0.1, text_wordwrap=10, text_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getPirateFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0, -0.05), pos=(-0.26, 0, 0.29))
            self.fullText = DirectLabel(parent=self.imageOne, relief=None, text=PLocalizer.FirstAddDisplay, text_align=TextNode.ALeft, text_scale=0.06, text_wordwrap=21, text_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getInterfaceFont(), pos=(-0.65, 0, -0.06))
            norm_geom = gui2.find('**/but_nav')
            over_geom = gui2.find('**/but_nav_over')
            down_geom = gui2.find('**/but_nav_down')
            dsbl_geom = gui2.find('**/but_nav_disabled')
            self.upgradeButton = DirectButton(parent=self.imageOne, relief=None, geom=(norm_geom, down_geom, over_geom), pos=(0.28, 0, -0.37), scale=0.8, command=self.upgradeNow, text=PLocalizer.FirstAddUpgrade, text_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getInterfaceFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_scale=0.05, text_wordwrap=9, text_pos=(0, -0.01))
            self.dismissButton = DirectButton(parent=self.imageOne, relief=None, geom=(norm_geom, down_geom, over_geom), scale=0.8, text=PLocalizer.FirstAddBasic, text_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getInterfaceFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_scale=0.05, text_pos=(0, -0.01), pos=(-0.28, 0, -0.37), text_wordwrap=9, command=self.dismissNow)
        self.setBin('gui-popup', 0)
        return

    def dismissNow(self):
        if not self.trial:
            UserFunnel.logSubmit(0, 'NON_PAYER_CONTINUE_' + str(self.questIdReporting))
            UserFunnel.logSubmit(2, 'NON_PAYER_CONTINUE_' + str(self.questIdReporting))
            base.cr.centralLogger.writeClientEvent('NON_PAYER_CONTINUE_' + str(self.questIdReporting))
        self.hide()

    def upgradeNow(self):
        UserFunnel.logSubmit(0, 'NON_PAYER_UPGRADE_' + str(self.questIdReporting))
        UserFunnel.logSubmit(2, 'NON_PAYER_UPGRADE_' + str(self.questIdReporting))
        base.cr.centralLogger.writeClientEvent('NON_PAYER_UPGRADE_' + str(self.questIdReporting))
        base.popupBrowser(launcher.getValue('GAME_INGAME_MOREINFO'))

    def destroy(self):
        if self.__fader:
            self.__fader.pause()
            self.__fader = None
        DirectFrame.destroy(self)
        return

    def bringToFront(self):
        self.reparentTo(self.getParent())

    def show(self, questId='None_Provided'):
        self.questIdReporting = questId
        if self.__fader:
            self.__fader.pause()
        self.setAlphaScale(1.0)
        DirectFrame.show(self)
        messenger.send('NonPayerPanelShown')

    def hide(self):
        if self.__fader:
            self.__fader.pause()
        self.setAlphaScale(1.0)
        DirectFrame.hide(self)
        messenger.send('NonPayerPanelHidden')

    def fadeOut(self, delay=0.0, duration=0.5):
        if self.__fader:
            self.__fader.pause()
        self.__fader = Sequence(Wait(delay), LerpFunctionInterval(self.setAlphaScale, fromData=self.getColorScale()[3], toData=0.0, duration=duration), Func(self.hide))
        self.__fader.start()