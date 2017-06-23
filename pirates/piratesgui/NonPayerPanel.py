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

class NonPayerPanel(DirectFrame):

    def configurePanel(self):
        self.NUM_IMAGES = 10
        piccard = loader.loadModel('models/textureCards/velvetpics')
        self.gameImage = [
         (
          piccard.find('**/vr_island1'), piccard.find('**/vr_island2')), (piccard.find('**/vr_guild1'), piccard.find('**/vr_guild2')), (piccard.find('**/vr_account1'), piccard.find('**/vr_account2')), (piccard.find('**/vr_ship1'), piccard.find('**/vr_ship2')), (piccard.find('**/vr_pvp1'), piccard.find('**/vr_pvp2')), (piccard.find('**/vr_weapon1'), piccard.find('**/vr_weapon2')), (piccard.find('**/vr_parlor1'), piccard.find('**/vr_parlor2')), (piccard.find('**/vr_treasure2'), piccard.find('**/vr_treasure1')), (piccard.find('**/vr_combat1'), piccard.find('**/vr_combat2')), (piccard.find('**/vr_quest1'), piccard.find('**/vr_quest2')), (piccard.find('**/vr_customize1'), piccard.find('**/vr_customize2'))]
        self.gameCaption = [
         (
          PLocalizer.VR_Cap_Island1, PLocalizer.VR_Cap_Island2), (PLocalizer.VR_Cap_Guild1, PLocalizer.VR_Cap_Guild2), (PLocalizer.VR_Cap_Account1, PLocalizer.VR_Cap_Account2), (PLocalizer.VR_Cap_Ship1, PLocalizer.VR_Cap_Ship2), (PLocalizer.VR_Cap_PVP1, PLocalizer.VR_Cap_PVP2), (PLocalizer.VR_Cap_Weapon1, PLocalizer.VR_Cap_Weapon2), (PLocalizer.VR_Cap_Parlor1, PLocalizer.VR_Cap_Parlor2), (PLocalizer.VR_Cap_Treasure1, PLocalizer.VR_Cap_Treasure2), (PLocalizer.VR_Cap_Combat1, PLocalizer.VR_Cap_Combat2), (PLocalizer.VR_Cap_Quest1, PLocalizer.VR_Cap_Quest2), (PLocalizer.VR_Cap_Customize1, PLocalizer.VR_Cap_Customize2)]
        self.gameHeader = [
         PLocalizer.VR_Head_Island, PLocalizer.VR_Head_Guild, PLocalizer.VR_Head_Account, PLocalizer.VR_Head_Ship, PLocalizer.VR_Head_PVP, PLocalizer.VR_Head_Weapon, PLocalizer.VR_Head_Parlor, PLocalizer.VR_Head_Treasure, PLocalizer.VR_Head_Combat, PLocalizer.VR_Head_Quest, PLocalizer.VR_Head_Customize]
        self.gameDescript = [
         PLocalizer.VR_Island, PLocalizer.VR_Guild, PLocalizer.VR_Account, PLocalizer.VR_Ship, PLocalizer.VR_PVP, PLocalizer.VR_Weapon, PLocalizer.VR_Parlor, PLocalizer.VR_Treasure, PLocalizer.VR_Combat, PLocalizer.VR_Quest, PLocalizer.VR_Customize]

    def __init__(self, w=9.0, h=6.0, lock=True):
        self.width = w
        self.height = h
        self.imageFocus = 0
        self.hasEmbedded = hasEmbedded
        self.questIdReporting = 'None_Provided'
        self.__fader = None
        DirectFrame.__init__(self, relief=DGG.RIDGE, state=DGG.NORMAL, frameColor=Vec4(0.0, 0.0, 0.0, 0.7), borderWidth=PiratesGuiGlobals.BorderWidth, frameSize=(0, self.width, 0, self.height), pos=(-4.5,
                                                                                                                                                                                                       0,
                                                                                                                                                                                                       -3.0), sortOrder=999)
        self.initialiseoptions(NonPayerPanel)
        self.configurePanel()
        self.gamePic = [
         None, None]
        self.gamePic[0] = DirectFrame(parent=self, relief=None, image=self.gameImage[0][0], image_scale=(1.0,
                                                                                                         0.75,
                                                                                                         0.75), image_pos=(0,
                                                                                                                           0,
                                                                                                                           0), pos=(4.0,
                                                                                                                                    0,
                                                                                                                                    3.28), text=self.gameCaption[0][0], text_align=TextNode.ACenter, text_scale=0.055, text_pos=(0, -0.32, 0), text_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getPirateOutlineFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_shadowOffset=(0.1,
                                                                                                                                                                                                                                                                                                                                                                                                0.1), textMayChange=1)
        self.gamePic[1] = DirectFrame(parent=self, relief=None, image=self.gameImage[0][1], image_scale=(1.0,
                                                                                                         0.75,
                                                                                                         0.75), image_pos=(0,
                                                                                                                           0,
                                                                                                                           0), pos=(5.0,
                                                                                                                                    0,
                                                                                                                                    3.28), text=self.gameCaption[0][1], text_align=TextNode.ACenter, text_scale=0.055, text_pos=(0, -0.32, 0), text_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getPirateOutlineFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_shadowOffset=(0.1,
                                                                                                                                                                                                                                                                                                                                                                                                0.1), textMayChange=1)
        gui2 = loader.loadModel('models/gui/velvetrope')
        gui2.find('**/go_right').hide()
        gui2.find('**/go_left').hide()
        gui2.find('**/close_button').hide()
        gui2.find('**/upgrade_buttomn').hide()
        gui2.find('**/drop_shadow_buttons').hide()
        if not lock:
            gui2.find('**/lock').hide()
            gui2.find('**/lock_red_halo').hide()
            gui2.find('**/window_hoops').hide()
        root = gui2.find('**/velvetrope_top')
        titleBorder = gui2.find('**/title_bar_08')
        titleBorder.reparentTo(root)
        self.imageOne = DirectFrame(parent=self, relief=None, geom=gui2.find('**/velvetrope_top'), geom_scale=0.4, pos=(4.5,
                                                                                                                        0,
                                                                                                                        3.15))
        self.titleText = DirectLabel(parent=self, relief=None, text=PLocalizer.VR_AuthAccess, text_align=TextNode.ACenter, text_scale=0.075, text_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getPirateFont(), text_shadow=PiratesGuiGlobals.TextShadow, pos=(4.5,
                                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                                         3.8), textMayChange=1)
        self.underText = DirectLabel(parent=self, relief=None, text=self.gameHeader[0], text_align=TextNode.ACenter, text_scale=0.06, text_wordwrap=40, text_fg=PiratesGuiGlobals.TextFG15, text_font=PiratesGlobals.getInterfaceFont(), text_shadow=PiratesGuiGlobals.TextShadow, pos=(4.5,
                                                                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                                                                        2.8))
        self.fullText = DirectLabel(parent=self, relief=None, text=self.gameDescript[0], text_align=TextNode.ALeft, text_scale=0.045, text_wordwrap=30, text_fg=PiratesGuiGlobals.TextFG0, text_font=PiratesGlobals.getInterfaceFont(), pos=(4.05,
                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                             2.72))
        lookoutUI = loader.loadModel('models/gui/lookout_gui')
        basegeom = gui2.find('**/go_right')
        norm_geom = basegeom.find('**/normal')
        over_geom = basegeom.find('**/over')
        down_geom = basegeom.find('**/down')
        self.scrollRight = DirectButton(parent=self, relief=None, geom=(norm_geom, down_geom, over_geom), scale=0.4, pos=(4.5,
                                                                                                                          0,
                                                                                                                          3.15), command=self.scrollPicsRight)
        basegeom = gui2.find('**/go_left')
        norm_geom = basegeom.find('**/normal')
        over_geom = basegeom.find('**/over')
        down_geom = basegeom.find('**/down')
        self.scrollLeft = DirectButton(parent=self, relief=None, geom=(norm_geom, down_geom, over_geom), scale=0.4, pos=(4.5,
                                                                                                                         0,
                                                                                                                         3.15), command=self.scrollPicsLeft)
        basegeom = gui2.find('**/upgrade_buttomn')
        norm_geom = basegeom.find('**/normal')
        over_geom = basegeom.find('**/over')
        down_geom = basegeom.find('**/down')
        self.upgradeButton = DirectButton(parent=self, relief=None, geom=(norm_geom, down_geom, over_geom), geom0_color=(0.8,
                                                                                                                         0.8,
                                                                                                                         0.8,
                                                                                                                         1), geom1_color=(0.7,
                                                                                                                                          0.7,
                                                                                                                                          0.7,
                                                                                                                                          1), geom2_color=(1,
                                                                                                                                                           1,
                                                                                                                                                           1,
                                                                                                                                                           1), pos=(4.9,
                                                                                                                                                                    0,
                                                                                                                                                                    3.15), geom_scale=0.4, command=self.upgradeNow, text=PLocalizer.VR_UpgradeNow, text_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getPirateOutlineFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_scale=0.06, text_pos=(0, -0.76))
        self.passButton = DirectButton(parent=self, relief=None, geom=(norm_geom, down_geom, over_geom), geom0_color=(0.8,
                                                                                                                      0.8,
                                                                                                                      0.8,
                                                                                                                      1), geom1_color=(0.7,
                                                                                                                                       0.7,
                                                                                                                                       0.7,
                                                                                                                                       1), geom2_color=(1,
                                                                                                                                                        1,
                                                                                                                                                        1,
                                                                                                                                                        1), pos=(4.1,
                                                                                                                                                                 0,
                                                                                                                                                                 3.15), geom_scale=0.4, command=self.continuePlayingNow, text=PLocalizer.VR_UpgradeLater, text_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getPirateOutlineFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_scale=0.06, text_pos=(0, -0.76))
        basegeom = gui2.find('**/close_button')
        norm_geom = basegeom.find('**/normal')
        over_geom = basegeom.find('**/over')
        down_geom = basegeom.find('**/down')
        self.dismissButton = DirectButton(parent=self, relief=None, geom=(norm_geom, down_geom, over_geom), scale=0.4, pos=(4.5,
                                                                                                                            0,
                                                                                                                            3.115), command=self.dismissNow)
        self.clickHereButton = DirectButton(parent=self, relief=None, pos=(4.53, 0,
                                                                           3.15), command=self.moreInfo, text=PLocalizer.VR_Access, text0_fg=PiratesGuiGlobals.TextFG0, text1_fg=PiratesGuiGlobals.TextFG0, text2_fg=PiratesGuiGlobals.TextFG6, text_font=PiratesGlobals.getInterfaceFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_scale=0.045, text_pos=(0, -0.635))
        self.setBin('gui-popup', 0)
        return

    def focusWrap(self, num):
        if num == -1:
            return self.NUM_IMAGES
        elif num == -2:
            return self.NUM_IMAGES - 1
        elif num == self.NUM_IMAGES + 1:
            return 0
        elif num == self.NUM_IMAGES + 2:
            return 1
        else:
            return num

    def scrollPicsRight(self):
        self.imageFocus = self.focusWrap(self.imageFocus + 1)
        self.gamePic[0]['image'] = self.gameImage[self.imageFocus][0]
        self.gamePic[0]['text'] = self.gameCaption[self.imageFocus][0]
        self.underText['text'] = self.gameHeader[self.imageFocus]
        self.fullText['text'] = self.gameDescript[self.imageFocus]
        self.gamePic[1]['image'] = self.gameImage[self.imageFocus][1]
        self.gamePic[1]['text'] = self.gameCaption[self.imageFocus][1]

    def scrollPicsLeft(self):
        self.imageFocus = self.focusWrap(self.imageFocus - 1)
        self.gamePic[0]['image'] = self.gameImage[self.imageFocus][0]
        self.gamePic[0]['text'] = self.gameCaption[self.imageFocus][0]
        self.underText['text'] = self.gameHeader[self.imageFocus]
        self.fullText['text'] = self.gameDescript[self.imageFocus]
        self.gamePic[1]['image'] = self.gameImage[self.imageFocus][1]
        self.gamePic[1]['text'] = self.gameCaption[self.imageFocus][1]

    def setPicFocus(self, num):
        if num > self.NUM_IMAGES:
            num = 0
        self.imageFocus = num
        self.gamePic[0]['image'] = self.gameImage[self.imageFocus][0]
        self.gamePic[0]['text'] = self.gameCaption[self.imageFocus][0]
        self.underText['text'] = self.gameHeader[self.imageFocus]
        self.fullText['text'] = self.gameDescript[self.imageFocus]
        self.gamePic[1]['image'] = self.gameImage[self.imageFocus][1]
        self.gamePic[1]['text'] = self.gameCaption[self.imageFocus][1]

    def dismissNow(self):
        UserFunnel.logSubmit(0, 'DISMISS_' + str(self.questIdReporting))
        UserFunnel.logSubmit(2, 'DISMISS_' + str(self.questIdReporting))
        base.cr.centralLogger.writeClientEvent('DISMISS_' + str(self.questIdReporting))
        self.hide()

    def continuePlayingNow(self):
        UserFunnel.logSubmit(0, 'CONTINUE-PLAYING_' + str(self.questIdReporting))
        UserFunnel.logSubmit(2, 'CONTINUE-PLAYING_' + str(self.questIdReporting))
        base.cr.centralLogger.writeClientEvent('CONTINUE-PLAYING_' + str(self.questIdReporting))
        self.hide()

    def upgradeNow(self):
        UserFunnel.logSubmit(0, 'UPGRADE_' + str(self.questIdReporting))
        UserFunnel.logSubmit(2, 'UPGRADE_' + str(self.questIdReporting))
        base.cr.centralLogger.writeClientEvent('UPGRADE_' + str(self.questIdReporting))
        base.popupBrowser(launcher.getValue('GAME_INGAME_UPGRADE'), True)

    def moreInfo(self):
        UserFunnel.logSubmit(0, 'MOREINFO_' + str(self.questIdReporting))
        UserFunnel.logSubmit(2, 'MOREINFO_' + str(self.questIdReporting))
        base.cr.centralLogger.writeClientEvent('MOREINFO_' + str(self.questIdReporting))
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