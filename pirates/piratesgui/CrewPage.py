from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm import StateData
from direct.task import Task
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import SocialPage
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import CrewStatus
from pirates.band import BandConstance
from pirates.band import DistributedBandMember
from pirates.piratesgui import PirateMemberList
from pirates.piratesgui import PirateButtonChain
from pirates.piratesgui import CrewIconSelector
from pirates.piratesgui import CrewMatchInviter
from pirates.piratesgui import CrewHUD

class CrewPage(SocialPage.SocialPage):
    notify = directNotify.newCategory('CrewPage')

    def __init__(self, crewHUD):
        SocialPage.SocialPage.__init__(self, PLocalizer.CrewPageTitle)
        self.initialiseoptions(CrewPage)
        self.crewHUD = crewHUD
        self.startACrewButton = 0
        self.addCrewLookout = 0
        self.changeCrewLookout = 0
        self.selectCrewIcon = 0
        self.crewHUDToggleButton = 0
        self.crewIconSelection = 1
        self.mainFrame = DirectFrame(relief=None, parent=self)
        self.chain = PirateButtonChain.PirateButtonChain(0.56, self.mainFrame, True)
        self.chain.setPos(-0.052, 0.0, 0.025)
        self.membersList = PirateMemberList.PirateMemberList(6, self.mainFrame, 'FOOLIO HC', height=0.547, memberHeight=0.08, memberWidth=0.48, memberOffset=0.04, bottom=0.074)
        self.membersList.setPos(0.001, 0.0, 0.123)
        self.membersList.hide()
        self.load()
        self.headingLabel = DirectLabel(parent=self, relief=None, state=DGG.NORMAL, text=PLocalizer.CrewPageTitle, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                       0.0), text_fg=PiratesGuiGlobals.TextFG1, pos=(0.23,
                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                     0.794))
        return

    def load(self):
        if not self.startACrewButton:
            self.startACrewButton = self.chain.premakeButton(PLocalizer.CrewStartACrewButton, self.crewHUD.toggleStartACrew)
        if not self.addCrewLookout:
            self.addCrewLookout = self.chain.premakeButton(PLocalizer.CrewMatchRecruitButton, self.crewHUD.toggleCrewLookout)
        if not self.changeCrewLookout:
            self.changeCrewLookout = self.chain.premakeButton(PLocalizer.CrewLookingForOptionsButton, self.crewHUD.toggleCrewOptions)
        if not self.crewHUDToggleButton:
            self.crewHUDToggleButton = self.chain.premakeButton(PLocalizer.CrewHUDCrewPanelButton, self.toggleCrewHUD)
        if not self.selectCrewIcon:
            self.selectCrewIcon = self.chain.premakeButton(PLocalizer.CrewIconButton, self.toggleCrewIcon)
        self.leaveButton = self.chain.premakeButton(PLocalizer.CrewPageLeaveCrew, self.crewHUD.leaveCrew)
        self.chain.makeButtons()
        self.determineOptionsButtonsState()

    def determineOptionsButtonsState(self):
        if self.startACrewButton:
            if self.crewHUD.crew or self.crewHUD.joinACrewStatus or self.crewHUD.joinACrewStatusPVP or self.crewHUD.inTM:
                self.startACrewButton['state'] = DGG.DISABLED
            else:
                self.startACrewButton['state'] = DGG.NORMAL
        if self.addCrewLookout:
            if self.crewHUD.crew and DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand() == 1 and not self.crewHUD.inTM:
                self.addCrewLookout['state'] = DGG.NORMAL
            else:
                self.addCrewLookout['state'] = DGG.DISABLED
        if self.changeCrewLookout:
            if (self.crewHUD.crew and DistributedBandMember.DistributedBandMember.IsLocalAvatarHeadOfBand() == 1 or self.crewHUD.startACrewState) and not self.crewHUD.inTM:
                self.changeCrewLookout['state'] = DGG.NORMAL
            else:
                self.changeCrewLookout['state'] = DGG.DISABLED
        if not self.crewHUD.crew and self.crewHUD.inTM:
            self.crewHUDToggleButton['state'] = DGG.DISABLED
        else:
            self.crewHUDToggleButton['state'] = DGG.NORMAL
        if self.crewHUD.crew:
            self.selectCrewIcon['state'] = DGG.NORMAL
            self.leaveButton['state'] = DGG.NORMAL
        else:
            self.selectCrewIcon['state'] = DGG.DISABLED
            self.leaveButton['state'] = DGG.DISABLED

    def destroy(self):
        self.ignoreAll()
        self.membersList.destroy()
        self.chain.destroy()
        self.mainFrame.destroy()
        SocialPage.SocialPage.destroy(self)

    def enableCrewIcon(self):
        base.localAvatar.setCrewIcon(0)
        base.localAvatar.setCrewIcon(1)
        self.crewIconSelection = 1

    def disableCrewIcon(self):
        base.localAvatar.setCrewIcon(0)
        self.crewIconSelection = 0

    def toggleCrewIcon(self):
        if self.crewIconSelection:
            self.disableCrewIcon()
        else:
            self.enableCrewIcon()

    def toggleCrewHUD(self):
        if base.localAvatar.guiMgr.crewHUDTurnedOff:
            self.crewHUD.setHUDOn()
            base.localAvatar.guiMgr.crewHUDTurnedOff = False
        else:
            self.crewHUD.setHUDOff()
            base.localAvatar.guiMgr.crewHUDTurnedOff = True