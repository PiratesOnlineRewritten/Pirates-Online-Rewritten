from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import SocialPage
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import CrewStatus
from pirates.band import BandConstance
from pirates.band import DistributedBandMember
from pirates.piratesgui import PirateMemberList
from pirates.piratesgui import PirateButtonChain
from pirates.piratesgui import CrewMatchInviter
from pirates.piratesgui import GuiButton
from pirates.piratesgui import BorderFrame
HUD_ICONS = {0: 'pir_t_gui_gen_land',1: 'pir_t_ico_swd_broadsword_b',2: 'pir_t_ico_gun_pistol_a',3: 'pir_t_ico_doll_spirit_a',4: 'pir_t_ico_knf_small',5: 'pir_t_ico_bom_grenade',6: 'pir_t_ico_stf_dark_a',7: 'pir_t_ico_can_single',8: 'sail_come_about',9: 'topgui_icon_ship',10: 'lookout_win_parlor_game_icon',11: 'lookout_win_pvp_game_icon',12: None,13: 'pir_t_gui_gen_medical'}
PVP_ISLAND_ONE = '1196970080.56sdnaik'
PVP_ISLAND_TWO = '1196970035.53sdnaik'
PVP_ISLAND_LIST = [PVP_ISLAND_ONE, PVP_ISLAND_TWO]

class XButton(GuiButton.GuiButton):

    def __init__(self, crewHUD, avId, frame, image, image_scale, button):
        self.avId = avId
        self.crewHUD = crewHUD
        self.button = button
        self.frame = frame
        self.topGui = loader.loadModel('models/gui/toplevel_gui')
        GuiButton.GuiButton.__init__(self, parent=frame, relief=None, image=image, image_scale=image_scale, command=self.handlePress)
        self.initialiseoptions(XButton)
        self.bind(DGG.ENTER, self.highlightOn)
        self.bind(DGG.EXIT, self.highlightOff)
        return

    def handlePress(self):
        if self.button.potentialMember:
            if base.cr.PirateBandManager:
                base.cr.PirateBandManager.d_requestCancel(self.avId)
            self.crewHUD.removePotentialCrew(self.avId)
        else:
            self.crewHUD.removeCrew(self.avId, 0)

    def highlightOn(self, event):
        self.frame['image'] = self.topGui.find('**/generic_box_over')

    def highlightOff(self, event):
        self.frame['image'] = self.topGui.find('**/generic_box')


class HoverFrame(DirectFrame):

    def __init__(self, parent=None, hoverText='', hoverPos=(0, 0, 0), **kw):
        self.helpBox = None
        optiondefs = (
         ('relief', None, None), ('pos', (0, 0, 0), None), ('image', None, None), ('image_scale', (0.24, 0.22, 0.22), None), ('image_pos', (0, 0, 0), None), ('hoverText', hoverText, self.hoverTextUpdated), ('hoverPos', hoverPos, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent=parent, **kw)
        self.initialiseoptions(HoverFrame)
        self.bind(DGG.ENTER, self.showHelp)
        self.bind(DGG.EXIT, self.hideHelp)
        return

    def createHelpBox(self):
        helpLabel = DirectLabel(relief=None, state=DGG.DISABLED, text=self['hoverText'], text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleMed, text_fg=PiratesGuiGlobals.TextFG1, text_wordwrap=12, text_shadow=(0,
                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                   1), textMayChange=0, sortOrder=91)
        height = helpLabel.getHeight()
        width = helpLabel.getWidth() + 0.05
        fs = [0.25 - width, 0.25, -height, 0.045]
        pos = [0.25 - width / 2.0, 0, -0.01]
        self.helpBox = BorderFrame.BorderFrame(parent=self, state=DGG.DISABLED, frameSize=(fs[0], fs[1], fs[2], fs[3]), modelName='general_frame_f', pos=self['hoverPos'], sortOrder=90)
        helpLabel.reparentTo(self.helpBox)
        helpLabel.setPos(pos[0], pos[1], pos[2])
        self.helpBox.hide()
        self.helpBox.setClipPlaneOff()
        pos = self.helpBox.getPos(aspect2d)
        x = min(pos[0], base.a2dRight - width)
        z = max(pos[2], base.a2dBottom - height)
        self.helpBox.setPos(aspect2d, x, 0, z)
        self.helpBox.flattenLight()
        self.helpBox.setBin('gui-popup', 0)
        return

    def hoverTextUpdated(self):
        if self.helpBox and self.helpBox['text'] != self['hoverText']:
            self.helpBox.destroy()
            self.createHelpBox()
        elif self['hoverText']:
            self.createHelpBox()

    def showHelp(self, event):
        self.helpBox.show()

    def hideHelp(self, event):
        self.helpBox.hide()


class CrewHUD(SocialPage.SocialPage):
    notify = directNotify.newCategory('CrewHUD')

    def __init__(self):
        SocialPage.SocialPage.__init__(self, 'Crew HUD')
        self.crew = {}
        self.mainFrame = DirectFrame(relief=None, parent=base.a2dTopLeft, frameSize=(0,
                                                                                     0.5,
                                                                                     0,
                                                                                     1.5), state=DGG.DISABLED, sortOrder=0)
        self.mainFrameSea = DirectFrame(relief=None, parent=base.a2dTopLeft, frameSize=(0,
                                                                                        0.5,
                                                                                        0,
                                                                                        1), state=DGG.DISABLED, sortOrder=0)
        self.mainFrame.setPos(-0.0566664, 0, -1.93)
        self.mainFrameSea.setPos(-0.0566664, 0, -1.72667)
        self.hudLabel = DirectLabel(relief=None, parent=self.mainFrame, text=PLocalizer.CrewHUDNoCrew, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_pos=(0.29,
                                                                                                                                                                                                                                   1.56,
                                                                                                                                                                                                                                   0), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, state=DGG.DISABLED)
        self.hudLabelSea = DirectLabel(relief=None, parent=self.mainFrameSea, text=PLocalizer.CrewHUDNoCrew, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_pos=(0.29,
                                                                                                                                                                                                                                         1.055,
                                                                                                                                                                                                                                         0), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, state=DGG.DISABLED)
        self.lookoutGui = loader.loadModel('models/gui/lookout_gui')
        self.topGui = loader.loadModel('models/gui/toplevel_gui')
        self.icons = loader.loadModel('models/textureCards/icons')
        self.clamp = self.topGui.find('**/groggy_clamp')
        self.flagLogos = loader.loadModel('models/textureCards/sailLogo')
        self.spanishFlag = self.flagLogos.find('**/logo_spanish_flag')
        self.frenchFlag = self.flagLogos.find('**/logo_french_flag')
        self.lookoutFrame = OnscreenImage(parent=self.mainFrame, image=self.topGui.find('**/telescope_button'), scale=(0.2, 0, -0.2), pos=(0.6,
                                                                                                                                           0,
                                                                                                                                           1.58))
        self.lookoutButton = GuiButton.GuiButton(parent=self.mainFrame, text='', image_scale=0.3, image_pos=(0.6,
                                                                                                             0,
                                                                                                             1.58), command=self.toggleCrewLookout, image=(self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash')), helpText=PLocalizer.CrewLookingForButton, helpPos=(0.7,
                                                                                                                                                                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                                                                                                                                                                1.53), helpOpaque=1)
        self.leaveCrewFrame = OnscreenImage(parent=self.mainFrame, image=self.icons.find('**/pir_t_gui_gen_crew_mug'), scale=0.06, pos=(0.7,
                                                                                                                                        0,
                                                                                                                                        1.58))
        self.leaveCrewButton = GuiButton.GuiButton(parent=self.mainFrame, command=self.leaveCrew, image=(self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash')), image_scale=0.3, image_pos=(0.7,
                                                                                                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                                                                                                       1.58), helpText=PLocalizer.CrewPageLeaveCrew, helpPos=(0.7,
                                                                                                                                                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                                                                                                                                                              1.53), helpOpaque=1)
        self.startCrewFrame = OnscreenImage(parent=base.a2dTopLeft, image=self.topGui.find('**/telescope_button'), scale=(0.2, 0, -0.2), pos=(0.05, 0, -0.35))
        self.startCrewButton = GuiButton.GuiButton(parent=base.a2dTopLeft, image_scale=0.3, image_pos=(0.05, 0, -0.35), command=self.toggleStartACrew, image=(self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash')), helpText=PLocalizer.CrewStartACrewButton, helpPos=(0.1, 0, -0.4), helpOpaque=1, helpBin=None)
        self.lookoutFrameSea = OnscreenImage(parent=self.mainFrameSea, image=self.topGui.find('**/telescope_button'), scale=(0.2, 0, -0.2), pos=(0.6,
                                                                                                                                                 0,
                                                                                                                                                 1.075))
        self.lookoutButtonSea = GuiButton.GuiButton(parent=self.mainFrameSea, text='', image_scale=0.3, image_pos=(0.6,
                                                                                                                   0,
                                                                                                                   1.075), command=self.toggleCrewLookout, image=(self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash')), helpText=PLocalizer.CrewLookingForButton, helpPos=(0.7,
                                                                                                                                                                                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                                                                                                                                                                                       1.025), helpOpaque=1)
        self.leaveCrewFrameSea = OnscreenImage(parent=self.mainFrameSea, image=self.icons.find('**/pir_t_gui_gen_crew_mug'), scale=0.06, pos=(0.7,
                                                                                                                                              0,
                                                                                                                                              1.075))
        self.leaveCrewButtonSea = GuiButton.GuiButton(parent=self.mainFrameSea, text='', image_scale=0.3, image_pos=(0.7,
                                                                                                                     0,
                                                                                                                     1.075), command=self.leaveCrew, image=(self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash')), helpText=PLocalizer.CrewPageLeaveCrew, helpPos=(0.7,
                                                                                                                                                                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                                                                                                                                                                              1.025), helpOpaque=1)
        self.startCrewFrameSea = OnscreenImage(parent=base.a2dTopLeft, image=self.topGui.find('**/telescope_button'), scale=(0.2, 0, -0.2), pos=(0.05, 0, -0.65))
        self.startCrewButtonSea = GuiButton.GuiButton(parent=base.a2dTopLeft, image_scale=0.3, image_pos=(0.05, 0, -0.65), command=self.toggleStartACrew, image=(self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash')), helpText=PLocalizer.CrewStartACrewButton, helpPos=(0.1, 0, -0.6), helpOpaque=1)
        self.membersList = PirateMemberList.PirateMemberList(12, self.mainFrame, 'FOOLIO HC', height=1.5475, memberHeight=0.08, memberWidth=0.8, memberOffset=0.2, bottom=0.074, width=1.0, hud=True)
        self.membersList.setPos(-0.38, 0, 0)
        self.membersListSea = PirateMemberList.PirateMemberList(12, self.mainFrameSea, 'FOOLIO HC', height=1.0475, memberHeight=0.065, memberWidth=0.8, memberOffset=0.2, bottom=0.074, width=1.0, hud=True)
        self.membersListSea.setPos(-0.38, 0, 0)
        self.weaponCard = loader.loadModel('models/gui/gui_icons_weapon')
        self.card = loader.loadModel('models/textureCards/skillIcons')
        self.scCard = loader.loadModel('models/textureCards/speedchatIcons')
        self.mainFrame.hide()
        self.mainFrameSea.hide()
        self.hudOn = False
        self.initialStateSwitch = False
        self.startACrewState = 0
        self.recruitCrewMatesStatus = 0
        self.joinACrewStatus = 0
        self.joinACrewStatusPVP = 0
        self.inTM = False
        self.advancedMatching = False
        self.notorietyMatchRange = 20
        self.sailingMatchRange = 0
        self.cannonMatchRange = 0
        self.debugAvId = False
        self.debugCount = 0
        self.accept('chatPanelMax', self.respondChatPanelMax)
        self.accept('chatPanelMin', self.respondChatPanelMin)
        self.toggledByChat = False
        self.accept('localAvatarToSea', self.adjustHUDToSea)
        self.accept('localAvatarToLand', self.adjustHUDToLand)
        self.atSea = False
        self.accept('chatPanelOpen', self.chatPanelOpen)
        self.accept('chatPanelClose', self.chatPanelClose)
        self.chatPanelOpen = False
        self.accept(BandConstance.BandMemberHpChange, self.updateCrewMemberHp)
        self.accept(BandConstance.BandMemberManagerChange, self.updateIsManager)
        self.accept(BandConstance.BandMemberNameChange, self.updateCrewMemberName)
        self.accept(BandConstance.BandMembershipChange, self.DoUpdateCrewData)
        self.accept(BandConstance.BandMemberOnlineChange, self.updateCrewMemberOnline)
        self.accept(BandConstance.BandMemberPVPChange, self.updateCrewMemberPVP)
        self.accept(BandConstance.BandMemberParlorChange, self.updateCrewMemberParlor)
        self.setHUDOff()
        return

    def destroy(self):
        self.ignoreAll()
        self.crew = None
        self.membersList.destroy()
        self.membersListSea.destroy()
        if self.hudLabelSea:
            self.hudLabelSea.destroy()
            self.hudLabelSea = None
        if self.hudLabel:
            self.hudLabel.destroy()
            self.hudLabel = None
        if self.mainFrameSea:
            self.mainFrameSea.destroy()
            self.mainFrameSea = None
        if self.mainFrame:
            self.mainFrame.destroy()
            self.mainFrame = None
        if self.startCrewButton:
            self.startCrewButton.destroy()
            self.startCrewButton = None
        if self.startCrewFrame:
            self.startCrewFrame.destroy()
            self.startCrewFrame = None
        if self.startCrewButtonSea:
            self.startCrewButtonSea.destroy()
            self.startCrewButtonSea = None
        if self.startCrewFrameSea:
            self.startCrewFrameSea.destroy()
            self.startCrewFrameSea = None
        self.leaveCrewButton.destroy()
        del self.leaveCrewButton
        self.lookoutButton.destroy()
        del self.lookoutButton
        self.leaveCrewButtonSea.destroy()
        del self.leaveCrewButtonSea
        self.lookoutButtonSea.destroy()
        del self.lookoutButtonSea
        SocialPage.SocialPage.destroy(self)
        return

    def addCrew(self, member):
        avId = member.avatarId
        isManager = member.isManager
        inPvp = member.inPvp
        inParlorGame = member.inParlorGame
        disconnect = member.disconnect
        localAvatar.leaving = False
        if avId == localAvatar.doId:
            self.enableCrewIcon()
            for id in self.crew:
                localAvatar.guiMgr.radarGui.refreshRadarObject(id)

            return
        if avId not in self.crew or self.debugAvId:
            button = self.membersList.addMember(avId + self.debugCount, None, PirateMemberList.MODE_CREW_HUD, member)
            button['image'] = None
            buttonSea = self.membersListSea.addMember(avId + self.debugCount, None, PirateMemberList.MODE_CREW_HUD_SEA, member)
            buttonSea['image'] = None
            reloadFrame = DirectFrame(parent=button, relief=None, state=DGG.DISABLED, image=self.topGui.find('**/pir_t_gui_frm_base_circle'), image_scale=0.3, image_pos=(0,
                                                                                                                                                                          0,
                                                                                                                                                                          0.02), pos=(0.09,
                                                                                                                                                                                      0,
                                                                                                                                                                                      0.01))
            button.reloadFrame = reloadFrame
            reloadFrameSea = GuiButton.GuiButton(parent=buttonSea, relief=None, state=DGG.DISABLED, image=self.topGui.find('**/pir_t_gui_frm_base_circle'), image_scale=0.25, image_pos=(0,
                                                                                                                                                                                         0,
                                                                                                                                                                                         0.02), pos=(0.11,
                                                                                                                                                                                                     0,
                                                                                                                                                                                                     0.01))
            buttonSea.reloadFrame = reloadFrameSea
            skillFrame = DirectFrame(parent=reloadFrame, relief=None, state=DGG.DISABLED, image=self.icons.find('**/pir_t_gui_gen_land'), image_scale=0.06, image_pos=(0,
                                                                                                                                                                       0,
                                                                                                                                                                       0.02), text='', text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_font=PiratesGlobals.getPirateOutlineFont(), text_pos=(0,
                                                                                                                                                                                                                                                                                                                                                               0.01,
                                                                                                                                                                                                                                                                                                                                                               0))
            skillFrameSea = DirectFrame(parent=reloadFrameSea, relief=None, state=DGG.DISABLED, image=self.icons.find('**/pir_t_gui_gen_land'), image_scale=0.05, image_pos=(0,
                                                                                                                                                                             0,
                                                                                                                                                                             0.02), text='', text_scale=PiratesGuiGlobals.TextScaleTiny, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_font=PiratesGlobals.getPirateOutlineFont(), text_pos=(0,
                                                                                                                                                                                                                                                                                                                                                                    0.01,
                                                                                                                                                                                                                                                                                                                                                                    0))
            leaderFrame = HoverFrame(parent=reloadFrame, relief=None, state=DGG.NORMAL, image=self.scCard.find('**/emotionIcon'), image_scale=0.04, image_pos=(0.03, 0, -0.01), hoverText=PLocalizer.CrewHUDLeader, hoverPos=(0.0, 0, -0.1))
            leaderFrameSea = HoverFrame(parent=reloadFrameSea, relief=None, state=DGG.NORMAL, image=self.scCard.find('**/emotionIcon'), image_scale=0.03, image_pos=(0.015, 0, -0.005), hoverText=PLocalizer.CrewHUDLeader, hoverPos=(0.0, 0, -0.1))
            siegeFrame = HoverFrame(parent=button, relief=None, state=DGG.NORMAL, image=self.spanishFlag, image_scale=0.02, image_pos=(0.16,
                                                                                                                                       0,
                                                                                                                                       0.001), hoverPos=(0.1, 0, -0.1))
            siegeFrameSea = HoverFrame(parent=buttonSea, relief=None, state=DGG.NORMAL, image=self.spanishFlag, image_scale=0.015, image_pos=(0.155,
                                                                                                                                              0,
                                                                                                                                              0.005), hoverPos=(0.1, 0, -0.1))
            xFrame = DirectFrame(parent=button, relief=None, state=DGG.DISABLED, image=self.topGui.find('**/generic_box'), image_scale=0.15, image_pos=(0,
                                                                                                                                                        0,
                                                                                                                                                        0), pos=(0.55,
                                                                                                                                                                 0,
                                                                                                                                                                 0.05))
            xButton = XButton(self, avId, xFrame, self.topGui.find('**/generic_x'), 0.25, button)
            xFrameSea = DirectFrame(parent=buttonSea, relief=None, state=DGG.DISABLED, image=self.topGui.find('**/generic_box'), image_scale=0.1, image_pos=(0,
                                                                                                                                                             0,
                                                                                                                                                             0), pos=(0.45,
                                                                                                                                                                      0,
                                                                                                                                                                      0.05))
            xButtonSea = XButton(self, avId, xFrameSea, self.topGui.find('**/generic_x'), 0.17, buttonSea)
            clampFrame = DirectFrame(parent=button, relief=None, state=DGG.NORMAL, image=self.clamp, image_scale=0.4, image_pos=(0.36,
                                                                                                                                 0,
                                                                                                                                 0.02))
            clampFrameSea = DirectFrame(parent=buttonSea, relief=None, state=DGG.NORMAL, image=self.clamp, image_scale=0.35, image_pos=(0.315,
                                                                                                                                        0,
                                                                                                                                        0.02))
            skillFrame.setTransparency(1)
            skillFrameSea.setTransparency(1)
            skillFrame.hide()
            skillFrameSea.hide()
            siegeFrame.hide()
            siegeFrameSea.hide()
            if not isManager:
                leaderFrame.hide()
                leaderFrameSea.hide()
            xFrame.hide()
            xFrameSea.hide()
            clampFrame.setBin('gui-fixed', -10)
            clampFrameSea.setBin('gui-fixed', -10)
            clampFrame.hide()
            clampFrameSea.hide()
            self.crew[avId + self.debugCount] = [button, reloadFrame, skillFrame, buttonSea, reloadFrameSea, skillFrameSea, leaderFrame, leaderFrameSea, siegeFrame, siegeFrameSea, xFrame, xFrameSea, clampFrame, clampFrameSea]
            if avId != localAvatar.getDoId():
                self.repackCrew()
                if inPvp:
                    self.updateCrewMemberPVP(member, inPvp, avId)
                elif inParlorGame:
                    self.updateCrewMemberParlor(member, inParlorGame, avId)
                elif disconnect:
                    self.updateCrewMemberOnline(member, disconnect, avId)
            base.localAvatar.guiMgr.radarGui.refreshRadarObject(avId)
            base.localAvatar.guiMgr.crewPage.determineOptionsButtonsState()
            return 1
        else:
            return 0
        if self.debugAvId and self.debugCount < 11:
            print 'In CrewHUD Debug mode, generating debug button %s' % self.debugCount
            self.debugCount += 1
            self.addCrew(member)
        return

    def addPotentialCrew(self, avId, avName):
        if avId not in self.crew:
            button = self.membersList.addPotentialMember(avId, avName, PirateMemberList.MODE_CREW_HUD)
            button['image'] = None
            buttonSea = self.membersListSea.addPotentialMember(avId, avName, PirateMemberList.MODE_CREW_HUD_SEA)
            buttonSea['image'] = None
            reloadFrame = DirectFrame(parent=button, relief=None, state=DGG.DISABLED, image=self.topGui.find('**/pir_t_gui_frm_base_circle'), image_scale=0.3, image_pos=(0,
                                                                                                                                                                          0,
                                                                                                                                                                          0.02), pos=(0.09,
                                                                                                                                                                                      0,
                                                                                                                                                                                      0.01))
            button.reloadFrame = reloadFrame
            reloadFrameSea = DirectFrame(parent=buttonSea, relief=None, state=DGG.DISABLED, image=self.topGui.find('**/pir_t_gui_frm_base_circle'), image_scale=0.25, image_pos=(0,
                                                                                                                                                                                 0,
                                                                                                                                                                                 0.02), pos=(0.11,
                                                                                                                                                                                             0,
                                                                                                                                                                                             0.01))
            buttonSea.reloadFrame = reloadFrameSea
            skillFrame = DirectFrame(parent=reloadFrame, relief=None, state=DGG.DISABLED, image=self.topGui.find('**/quest_pending_icon'), image_scale=0.2, image_pos=(0,
                                                                                                                                                                       0,
                                                                                                                                                                       0.02))
            skillFrameSea = DirectFrame(parent=reloadFrameSea, relief=None, state=DGG.DISABLED, image=self.topGui.find('**/quest_pending_icon'), image_scale=0.17, image_pos=(0,
                                                                                                                                                                              0,
                                                                                                                                                                              0.02))
            xFrame = DirectFrame(parent=button, relief=None, state=DGG.DISABLED, image=self.topGui.find('**/generic_box'), image_scale=0.15, image_pos=(0,
                                                                                                                                                        0,
                                                                                                                                                        0), pos=(0.55,
                                                                                                                                                                 0,
                                                                                                                                                                 0.05))
            xButton = XButton(self, avId, xFrame, self.topGui.find('**/generic_x'), 0.25, button)
            xFrameSea = DirectFrame(parent=buttonSea, relief=None, state=DGG.DISABLED, image=self.topGui.find('**/generic_box'), image_scale=0.1, image_pos=(0,
                                                                                                                                                             0,
                                                                                                                                                             0), pos=(0.45,
                                                                                                                                                                      0,
                                                                                                                                                                      0.05))
            xButtonSea = XButton(self, avId, xFrameSea, self.topGui.find('**/generic_x'), 0.17, buttonSea)
            skillFrame.setTransparency(1)
            skillFrameSea.setTransparency(1)
            self.crew[avId] = [
             button, reloadFrame, buttonSea, reloadFrameSea]
            if avId != localAvatar.getDoId():
                self.repackCrew()
            return 1
        else:
            return 0
        return

    def removeCrew(self, avId, fromAbove=0):
        if not fromAbove:
            if base.cr.PirateBandManager:
                base.cr.PirateBandManager.d_requestRemove(avId)
        if self.crew:
            self.crew.pop(avId, None)
        if self.membersList:
            self.membersList.removeMember(avId, None, PirateMemberList.MODE_CREW)
            self.membersList.removeMember(avId, None, PirateMemberList.MODE_CREW_HUD)
        if self.membersListSea:
            self.membersListSea.removeMember(avId, None, PirateMemberList.MODE_CREW_HUD_SEA)
        base.localAvatar.guiMgr.radarGui.refreshRadarObject(avId)
        base.localAvatar.guiMgr.crewPage.determineOptionsButtonsState()
        if avId != localAvatar.getDoId():
            self.repackCrew()
        else:
            self.b_deactivateCrewLookout()
            for avId, avButton in self.crew.iteritems():
                av = base.cr.doId2do.get(avId)
                if av:
                    av.refreshName()
                    crewMembersIconId = av.getCrewIcon()
                    if crewMembersIconId:
                        av.setCrewIconIndicator(0)
                        av.setCrewIconIndicator(2)

            if not self.crew:
                self.startCrewButton['image'] = (
                 self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash'))
                self.startCrewButtonSea['image'] = (
                 self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash'))
        return

    def removePotentialCrew(self, avId):
        self.crew.pop(avId, None)
        self.membersList.removeMember(avId, None, PirateMemberList.MODE_CREW)
        self.membersList.removeMember(avId, None, PirateMemberList.MODE_CREW_HUD)
        self.membersListSea.removeMember(avId, None, PirateMemberList.MODE_CREW_HUD_SEA)
        if avId != localAvatar.getDoId():
            self.repackCrew()
        return

    def repackCrew(self):
        if self.crew or self.startACrewState:
            if not self.initialStateSwitch:
                if DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand():
                    self.b_activateCrewLookout(self.notorietyMatchRange, self.sailingMatchRange, self.cannonMatchRange)
                elif localAvatar.guiMgr.crewInviter and not localAvatar.guiMgr.crewInviter.isEmpty():
                    localAvatar.guiMgr.crewInviter.fsm.request('cancel')
                self.initialStateSwitch = True
            self.setHUDOn()
        else:
            base.localAvatar.setCrewIcon(0)
            if base.cr.crewMatchManager:
                base.cr.crewMatchManager.deleteCrewFromLookoutList()
            self.initialStateSwitch = False
            self.setHUDOn()
        crewMembersIconId = 0
        for avId, avButton in self.crew.iteritems():
            av = base.cr.doId2do.get(avId)
            if not av:
                return
            av.refreshName()
            crewMembersIconId = av.getCrewIcon()
            if crewMembersIconId:
                av.setCrewIconIndicator(0)
                av.setCrewIconIndicator(1)

        if crewMembersIconId:
            localAvatar.setCrewIcon(0)
            localAvatar.setCrewIcon(1)

    def updateActionIcons(self, avId, action, siege, vitaeLevel):
        member = self.crew.get(avId)
        if member and member[0].hudOnline and not member[0].inPvp and not member[0].inParlorGame and not member[0].potentialMember:
            skillFrame = member[2]
            skillFrameSea = member[5]
            siegeFrame = member[8]
            siegeFrameSea = member[9]
            clampFrame = member[12]
            clampFrameSea = member[13]
            if siege:
                if siege == 2:
                    siegeFrame['image'] = self.spanishFlag
                    siegeFrameSea['image'] = self.spanishFlag
                    siegeFrame['hoverText'] = PLocalizer.CrewHUDPrivSpanish
                    siegeFrameSea['hoverText'] = PLocalizer.CrewHUDPrivSpanish
                else:
                    siegeFrame['image'] = self.frenchFlag
                    siegeFrameSea['image'] = self.frenchFlag
                    siegeFrame['hoverText'] = PLocalizer.CrewHUDPrivFrench
                    siegeFrameSea['hoverText'] = PLocalizer.CrewHUDPrivFrench
                siegeFrame.show()
                siegeFrameSea.show()
            else:
                siegeFrame.hide()
                siegeFrameSea.hide()
            if vitaeLevel:
                clampFrame.show()
                clampFrameSea.show()
            else:
                clampFrame.hide()
                clampFrameSea.hide()
            newIcon = HUD_ICONS[action]
            if newIcon == None:
                skillFrame['image'] = None
                skillFrameSea['image'] = None
                if action in [12]:
                    skillFrame['text'] = PLocalizer.CrewHUDAFK
                    skillFrameSea['text'] = PLocalizer.CrewHUDAFK
            else:
                skillFrame['text'] = ''
                skillFrameSea['text'] = ''
                if action in [0]:
                    skillFrame['image'] = self.icons.find('**/%s' % newIcon)
                    skillFrame['image_scale'] = 0.06
                elif action in [8]:
                    skillFrame['image'] = self.card.find('**/%s' % newIcon)
                    skillFrame['image_scale'] = 0.07
                else:
                    if action in [9, 10, 11, 13]:
                        skillFrame['image'] = self.topGui.find('**/%s' % newIcon)
                        if action == 9:
                            skillFrame['image_scale'] = 0.125
                        elif action == 10:
                            skillFrame['image_scale'] = 0.2
                        elif action == 11:
                            skillFrame['image_scale'] = 0.3
                        elif action == 13:
                            skillFrame['image_scale'] = 0.5
                    else:
                        skillFrame['image'] = self.weaponCard.find('**/%s' % newIcon)
                        skillFrame['image_scale'] = 0.06
                    skillFrame['image_pos'] = (0, 0, 0.02)
                    if action in [0]:
                        skillFrameSea['image'] = self.icons.find('**/%s' % newIcon)
                        skillFrameSea['image_scale'] = 0.05
                    else:
                        if action in [8]:
                            skillFrameSea['image'] = self.card.find('**/%s' % newIcon)
                            skillFrameSea['image_scale'] = 0.06
                        if action in [9, 10, 11, 13]:
                            skillFrameSea['image'] = self.topGui.find('**/%s' % newIcon)
                            if action == 9:
                                skillFrameSea['image_scale'] = 0.1
                            elif action == 10:
                                skillFrameSea['image_scale'] = 0.17
                            elif action == 11:
                                skillFrameSea['image_scale'] = 0.25
                            elif action == 13:
                                skillFrameSea['image_scale'] = 0.4
                        skillFrameSea['image'] = self.weaponCard.find('**/%s' % newIcon)
                        skillFrameSea['image_scale'] = 0.05
                skillFrameSea['image_pos'] = (0, 0, 0.02)
            skillFrame.show()
            skillFrameSea.show()
        return

    def updateCrewNearBy(self, crewNearBy):
        if crewNearBy > 0:
            self.hudLabel['text'] = PLocalizer.CrewHUDCrewNearBy % crewNearBy
            self.hudLabelSea['text'] = PLocalizer.CrewHUDCrewNearBy % crewNearBy
        else:
            self.hudLabel['text'] = PLocalizer.CrewHUDNoCrew
            self.hudLabelSea['text'] = PLocalizer.CrewHUDNoCrew

    def showSiegeTeam(self, avId, siege, event):
        member = self.crew.get(avId)
        if member:
            siegeFrame = member[8]
            siegeFrameSea = member[9]
            if siege == 2:
                siegeFrame['hoverText'] = PLocalizer.CrewHUDPrivSpanish
                siegeFrameSea['hoverText'] = PLocalizer.CrewHUDPrivSpanish
            else:
                siegeFrame['hoverText'] = PLocalizer.CrewHUDPrivFrench
                siegeFrameSea['hoverText'] = PLocalizer.CrewHUDPrivFrench
            siegeFrame.helpBox.show()
            siegeFrameSea.helpBox.show()

    def hideSiegeTeam(self, avId, siege, event):
        member = self.crew.get(avId)
        if member:
            siegeFrame = member[8]
            siegeFrameSea = member[9]
            if siegeFrame.helpBox:
                siegeFrame.helpBox.hide()
            if siegeFrameSea.helpBox:
                siegeFrameSea.helpBox.hide()

    def toggleHUD(self):
        if self.hudOn:
            self.mainFrameSea.hide()
            self.mainFrame.hide()
            self.hudOn = False
        elif self.canShowButtons():
            if self.atSea:
                self.mainFrameSea.show()
            else:
                self.mainFrame.show()
            self.hudOn = True

    def setHUDOff(self):
        self.hudOn = False
        self.mainFrame.hide()
        self.mainFrameSea.hide()
        self.startCrewButton.hide()
        self.startCrewFrame.hide()
        self.startCrewButtonSea.hide()
        self.startCrewFrameSea.hide()

    def setHUDOn(self):
        self.hudOn = True
        if not self.crew:
            self.mainFrame.hide()
            self.mainFrameSea.hide()
            if not self.joinACrewStatus and not self.joinACrewStatusPVP and self.canShowButtons():
                if self.atSea:
                    self.startCrewButtonSea.show()
                    self.startCrewFrameSea.show()
                else:
                    self.startCrewButton.show()
                    self.startCrewFrame.show()
            elif not self.canShowButtons():
                self.startCrewButton.hide()
                self.startCrewFrame.hide()
                self.startCrewButtonSea.hide()
                self.startCrewFrameSea.hide()
        self.startCrewButton.hide()
        self.startCrewFrame.hide()
        self.startCrewButtonSea.hide()
        self.startCrewFrameSea.hide()
        if DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand() == 0 or not self.canShowButtons():
            self.lookoutButton.hide()
            self.lookoutFrame.hide()
            self.lookoutButtonSea.hide()
            self.lookoutFrameSea.hide()
        else:
            if self.atSea:
                self.lookoutButtonSea.show()
                self.lookoutFrameSea.show()
            else:
                self.lookoutButton.show()
                self.lookoutFrame.show()
            if self.canShowButtons():
                if self.atSea:
                    self.mainFrameSea.show()
                else:
                    self.mainFrame.show()
            if not self.canShowButtons():
                self.leaveCrewButton.hide()
                self.leaveCrewFrame.hide()
                self.leaveCrewButtonSea.hide()
                self.leaveCrewFrameSea.hide()
            else:
                self.leaveCrewButton.show()
                self.leaveCrewFrame.show()
                self.leaveCrewButtonSea.show()
                self.leaveCrewFrameSea.show()

    def setTM(self, inTM):
        self.inTM = inTM

    def debugFullCrewList(self):
        self.debugAvId = True
        print 'DEBUG: Activating crew HUD display debug mode'

    def destroyFullCrewList(self):
        self.debugAvId = False
        print 'DEBUG: Deactivating crew HUD display debug mode'

    def respondChatPanelMax(self):
        if self.hudOn and self.chatPanelOpen and (self.atSea or len(self.crew) > 2):
            self.toggledByChat = True
            self.setHUDOff()

    def respondChatPanelMin(self):
        if self.toggledByChat:
            self.toggledByChat = False
            self.setHUDOn()

    def adjustHUDToSea(self):
        if self.hudOn:
            if self.crew:
                self.mainFrame.hide()
                self.mainFrameSea.show()
            else:
                self.startCrewButton.hide()
                self.startCrewFrame.hide()
                if not self.joinACrewStatus and not self.joinACrewStatusPVP and self.canShowButtons():
                    self.startCrewButtonSea.show()
                    self.startCrewFrameSea.show()
        self.atSea = True

    def adjustHUDToLand(self):
        if self.hudOn and self.canShowButtons():
            if self.crew:
                self.mainFrameSea.hide()
                self.mainFrame.show()
            else:
                self.startCrewButtonSea.hide()
                self.startCrewFrameSea.hide()
                if not self.joinACrewStatus and not self.joinACrewStatusPVP and self.canShowButtons():
                    self.startCrewButton.show()
                    self.startCrewFrame.show()
        self.atSea = False

    def chatPanelOpen(self):
        if self.hudOn:
            self.chatPanelOpen = True

    def chatPanelClose(self):
        if hasattr(base, 'localAvatar'):
            if base.localAvatar.guiMgr.crewHUDTurnedOff:
                pass
            elif self.chatPanelOpen:
                self.setHUDOn()
                self.chatPanelOpen = False

    def updateCrewMemberHp(self, member, hp, maxHp):
        hudButton = self.crew.get(member.avatarId)
        if hudButton:
            hudButton[0].updateHp(hp, maxHp)
            hudButton[3].updateHp(hp, maxHp)

    def updateCrewMemberName(self, member, name):
        hudButton = self.crew.get(member.avatarId)
        if hudButton:
            hudButton[0].updateName(name)
            hudButton[3].updateName(name)

    def updateIsManager(self, member, flag):
        if DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand() and flag:
            if self.canShowButtons():
                self.lookoutButton.show()
                self.lookoutFrame.show()
                self.lookoutButtonSea.show()
                self.lookoutFrameSea.show()
            if self.recruitCrewMatesStatus:
                self.lookoutButton['image'] = (
                 self.topGui.find('**/pir_t_gui_but_circle'), self.topGui.find('**/pir_t_gui_but_circle'), self.topGui.find('**/pir_t_gui_but_circle_over'), self.topGui.find('**/pir_t_gui_but_circle'))
                self.lookoutButtonSea['image'] = (
                 self.topGui.find('**/pir_t_gui_but_circle'), self.topGui.find('**/pir_t_gui_but_circle'), self.topGui.find('**/pir_t_gui_but_circle_over'), self.topGui.find('**/pir_t_gui_but_circle'))
            else:
                self.lookoutButton['image'] = (
                 self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash'))
                self.lookoutButtonSea['image'] = (
                 self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash'))
            self.lookoutButton['command'] = self.toggleCrewLookout
            self.lookoutButtonSea['command'] = self.toggleCrewLookout
            for avId, hudButton in self.crew.iteritems():
                if not hudButton[0].potentialMember and (not hudButton[0].hudOnline or hudButton[0].inPvp or hudButton[0].inParlorGame):
                    hudButton[10].show()
                    hudButton[11].show()

        elif not flag or not self.canShowButtons():
            self.lookoutButton.hide()
            self.lookoutFrame.hide()
            self.lookoutButtonSea.hide()
            self.lookoutFrameSea.hide()
            for avId, hudButton in self.crew.iteritems():
                if not hudButton[0].potentialMember:
                    hudButton[10].hide()
                    hudButton[11].hide()

        base.localAvatar.guiMgr.crewPage.determineOptionsButtonsState()
        hudButton = self.crew.get(member.avatarId)
        if hudButton:
            if flag:
                hudButton[6].show()
                hudButton[7].show()
            else:
                hudButton[6].hide()
                hudButton[7].hide()

    def toggleAvatarLookout(self):
        if self.joinACrewStatus:
            self.b_deactivateAvatarLookout()
        elif not self.joinACrewStatus:
            self.b_activateAvatarLookout()

    def b_activateAvatarLookout(self):
        base.cr.crewMatchManager.addAvatarToLookoutList(1)
        self.joinACrewStatus = 1
        self.startCrewFrame.hide()
        self.startCrewButton.hide()
        self.startCrewFrameSea.hide()
        self.startCrewButtonSea.hide()

    def b_deactivateAvatarLookout(self):
        base.cr.crewMatchManager.deleteAvatarFromLookoutList()
        self.joinACrewStatus = 0
        if self.canShowButtons():
            if not self.atSea:
                self.startCrewFrame.show()
                self.startCrewButton.show()
            else:
                self.startCrewFrameSea.show()
                self.startCrewButtonSea.show()

    def toggleAvatarLookoutPVP(self):
        if self.joinACrewStatusPVP:
            self.b_deactivateAvatarLookoutPVP()
        elif not self.joinACrewStatusPVP:
            self.b_activateAvatarLookoutPVP()

    def b_activateAvatarLookoutPVP(self):
        base.cr.crewMatchManager.addAvatarToLookoutList(2)
        self.joinACrewStatusPVP = 1
        self.startCrewFrame.hide()
        self.startCrewButton.hide()
        self.startCrewFrameSea.hide()
        self.startCrewButtonSea.hide()

    def b_deactivateAvatarLookoutPVP(self):
        base.cr.crewMatchManager.deleteAvatarFromLookoutList()
        self.joinACrewStatusPVP = 0
        if self.canShowButtons():
            if not self.atSea:
                self.startCrewFrame.show()
                self.startCrewButton.show()
            else:
                self.startCrewFrameSea.show()
                self.startCrewButtonSea.show()

    def toggleCrewLookout(self):
        if self.recruitCrewMatesStatus:
            self.b_deactivateCrewLookout()
            self.stackMessage(PLocalizer.CrewMatchDeactivated)
        elif not self.recruitCrewMatesStatus:
            if localAvatar.getCurrentIsland() in PVP_ISLAND_LIST or localAvatar.getSiegeTeam():
                self.stackMessage(PLocalizer.CrewMatchEnabledForCrewPVP)
            else:
                self.stackMessage(PLocalizer.CrewMatchEnabledForCrew)
            if DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand() or self.startACrewState:
                self.b_activateCrewLookout(self.notorietyMatchRange, self.sailingMatchRange, self.cannonMatchRange)
            self.setHUDOn()

    def toggleCrewOptions(self):
        CrewMatchInviter.CrewMatchInviter(localAvatar.getLevel(), self.advancedMatching)

    def b_activateCrewLookout(self, range, sailValue=0, cannonValue=0):
        if (self.crew or self.startACrewState) and self.canShowButtons():
            base.cr.crewMatchManager.addCrewToLookoutList(range, sailValue, cannonValue)
            self.lookoutButton['image'] = (self.topGui.find('**/pir_t_gui_but_circle'), self.topGui.find('**/pir_t_gui_but_circle'), self.topGui.find('**/pir_t_gui_but_circle_over'), self.topGui.find('**/pir_t_gui_but_circle'))
            self.lookoutButtonSea['image'] = (
             self.topGui.find('**/pir_t_gui_but_circle'), self.topGui.find('**/pir_t_gui_but_circle'), self.topGui.find('**/pir_t_gui_but_circle_over'), self.topGui.find('**/pir_t_gui_but_circle'))
            self.startCrewButton['image'] = (
             self.topGui.find('**/pir_t_gui_but_circle'), self.topGui.find('**/pir_t_gui_but_circle'), self.topGui.find('**/pir_t_gui_but_circle_over'), self.topGui.find('**/pir_t_gui_but_circle'))
            self.startCrewButtonSea['image'] = (
             self.topGui.find('**/pir_t_gui_but_circle'), self.topGui.find('**/pir_t_gui_but_circle'), self.topGui.find('**/pir_t_gui_but_circle_over'), self.topGui.find('**/pir_t_gui_but_circle'))
            self.recruitCrewMatesStatus = 1

    def b_deactivateCrewLookout(self):
        base.cr.crewMatchManager.deleteCrewFromLookoutList()
        self.joinACrewStatus = 0
        self.joinACrewStatusPVP = 0
        self.recruitCrewMatesStatus = 0
        if not self.crew:
            if self.startACrewState:
                base.cr.crewMatchManager.requestDeleteCrewOfOne()
            if self.canShowButtons():
                if self.atSea:
                    self.startCrewButtonSea.show()
                    self.startCrewFrameSea.show()
                else:
                    self.startCrewButton.show()
                    self.startCrewFrame.show()
        self.startCrewButton['image'] = (
         self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash'))
        self.startCrewButtonSea['image'] = (
         self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash'))
        self.startACrewState = 0
        self.lookoutButton['image'] = (self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash'))
        self.lookoutButtonSea['image'] = (
         self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash'))

    def leaveCrew(self):
        for avId, avButton in self.crew.iteritems():
            av = base.cr.doId2do.get(avId)
            if av:
                av.refreshName()
                crewMembersIconId = av.getCrewIcon()
                if crewMembersIconId:
                    av.setCrewIconIndicator(0)
                    av.setCrewIconIndicator(2)

        base.cr.crewMatchManager.deleteCrewFromLookoutList()
        if base.cr.PirateBandManager:
            base.cr.PirateBandManager.d_requestRemove(localAvatar.doId)
        self.joinACrewStatus = 0
        self.joinACrewStatusPVP = 0
        self.recruitCrewMatesStatus = 0
        base.localAvatar.guiMgr.crewPage.determineOptionsButtonsState()
        self.setHUDOn()

    def DoUpdateCrewData(self, member, remove):
        if remove:
            self.removeCrew(member.avatarId, 1)
        else:
            self.removePotentialCrew(member.avatarId)
            self.addCrew(member)

    def enableCrewIcon(self):
        if base.cr.PirateBandManager:
            base.cr.PirateBandManager.d_requestCrewIconUpdate(1)
        base.localAvatar.setCrewIcon(0)
        base.localAvatar.setCrewIcon(1)

    def toggleLookingForCrew(self):
        currentVal = localAvatar.getLookingForCrew()
        if currentVal == 1:
            localAvatar.setLookingForCrew(0)
        else:
            localAvatar.setLookingForCrew(1)

    def toggleStartACrew(self):
        self.joinACrewStatus = 0
        if self.startACrewState == 1:
            base.cr.crewMatchManager.requestDeleteCrewOfOne()
            localAvatar.setCrewIcon(0)
            self.startACrewState = 0
            self.recruitCrewMatesStatus = 0
            self.startCrewButton['image'] = (self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash'))
            self.startCrewButtonSea['image'] = (
             self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash'), self.topGui.find('**/pir_t_gui_but_circle_slash_over'), self.topGui.find('**/pir_t_gui_but_circle_slash'))
            self.stackMessage(PLocalizer.CrewMatchStartCrewDeactivated)
            base.localAvatar.guiMgr.crewPage.determineOptionsButtonsState()
            return
        if not self.canShowButtons():
            return
        base.cr.crewMatchManager.requestCrewOfOne()
        self.startACrewState = 1
        self.toggleCrewLookout()
        base.localAvatar.guiMgr.crewPage.determineOptionsButtonsState()
        if not self.recruitCrewMatesStatus:
            if localAvatar.getCurrentIsland() in PVP_ISLAND_LIST or localAvatar.getSiegeTeam():
                self.stackMessage(PLocalizer.CrewMatchEnabledForCrewPVP)
            else:
                self.stackMessage(PLocalizer.CrewMatchEnabledForCrew)

    def updateCrewMemberOnline(self, member, disconnect, avatarId):
        if localAvatar.getDoId() == avatarId:
            return
        hudButton = self.crew.get(avatarId)
        if not hudButton or hudButton[0].potentialMember:
            return
        if disconnect:
            if hudButton:
                hudButton[0].updateHUDOnline(0)
                hudButton[3].updateHUDOnline(0)
                hudButton[2]['image'] = self.lookoutGui.find('**/lookout_skip')
                hudButton[2]['image_scale'] = 0.2
                hudButton[2]['image_pos'] = (0, 0, 0.02)
                hudButton[2]['text'] = ''
                hudButton[2].show()
                hudButton[5]['image'] = self.lookoutGui.find('**/lookout_skip')
                hudButton[5]['image_scale'] = 0.2
                hudButton[5]['image_pos'] = (0, 0, 0.02)
                hudButton[5]['text'] = ''
                hudButton[6].hide()
                hudButton[7].hide()
                hudButton[8]['image'] = None
                hudButton[9]['image'] = None
                if DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand():
                    hudButton[10].show()
                    hudButton[11].show()
        elif hudButton:
            hudButton[0].updateHUDOnline(1)
            hudButton[3].updateHUDOnline(1)
            hudButton[10].hide()
            hudButton[11].hide()
        return

    def updateCrewMemberPVP(self, member, pvp, avatarId):
        if localAvatar.getDoId() == avatarId:
            return
        hudButton = self.crew.get(avatarId)
        if not hudButton or hudButton[0].potentialMember:
            return
        if pvp:
            if hudButton:
                hudButton[0].updatePVP(1)
                hudButton[3].updatePVP(1)
                hudButton[2]['image'] = self.topGui.find('**/%s' % HUD_ICONS[11])
                hudButton[2]['image_scale'] = 0.3
                hudButton[2]['image_pos'] = (0, 0, 0.02)
                hudButton[2]['text'] = ''
                hudButton[2].show()
                hudButton[5]['image'] = self.topGui.find('**/%s' % HUD_ICONS[11])
                hudButton[5]['image_scale'] = 0.15
                hudButton[5]['image_pos'] = (0, 0, 0.02)
                hudButton[5]['text'] = ''
                hudButton[6].hide()
                hudButton[7].hide()
                hudButton[8]['image'] = None
                hudButton[9]['image'] = None
                if DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand():
                    hudButton[10].show()
                    hudButton[11].show()
        elif hudButton:
            hudButton[0].updatePVP(0)
            hudButton[3].updatePVP(0)
        return

    def updateCrewMemberParlor(self, member, parlor, avatarId):
        if localAvatar.getDoId() == avatarId:
            return
        hudButton = self.crew.get(avatarId)
        if not hudButton or hudButton[0].potentialMember:
            return
        if parlor:
            if hudButton:
                hudButton[0].updateParlor(1)
                hudButton[3].updateParlor(1)
                hudButton[2]['image'] = self.topGui.find('**/%s' % HUD_ICONS[10])
                hudButton[2]['image_scale'] = 0.3
                hudButton[2]['image_pos'] = (0, 0, 0.02)
                hudButton[2]['text'] = ''
                hudButton[2].show()
                hudButton[5]['image'] = self.topGui.find('**/%s' % HUD_ICONS[10])
                hudButton[5]['image_scale'] = 0.15
                hudButton[5]['image_pos'] = (0, 0, 0.02)
                hudButton[5]['text'] = ''
                hudButton[6].hide()
                hudButton[7].hide()
                hudButton[8]['image'] = None
                hudButton[9]['image'] = None
                if DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand():
                    hudButton[10].show()
                    hudButton[11].show()
        elif hudButton:
            hudButton[0].updateParlor(0)
            hudButton[3].updateParlor(0)
        return

    def stackMessage(self, msg, name=None, avId=None):
        base.localAvatar.guiMgr.messageStack.addTextMessage(msg, seconds=15, priority=0, color=PiratesGuiGlobals.TextFG14, modelName='general_frame_f', icon=('crew',
                                                                                                                                                              ''), name=name, avId=avId)

    def setAdvancedMatching(self, advancedMatching):
        self.advancedMatching = advancedMatching

    def setNotorietyMatchRange(self, notorietyMatchRange):
        self.notorietyMatchRange = notorietyMatchRange

    def getNotorietyMatchRange(self):
        return self.notorietyMatchRange

    def setSailingMatchRange(self, sailingMatchRange):
        self.sailingMatchRange = sailingMatchRange

    def getSailingMatchRange(self):
        return self.sailingMatchRange

    def setCannonMatchRange(self, cannonMatchRange):
        self.cannonMatchRange = cannonMatchRange

    def getCannonMatchRange(self):
        return self.cannonMatchRange

    def canShowButtons(self):
        return not self.inTM and localAvatar.getGameState() != 'Fishing' and not localAvatar.inPvp