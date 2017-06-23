from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.fsm import FSM
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from otp.distributed import CentralLogger
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import GuiButton

class ReportAPlayer(GuiPanel.GuiPanel, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('ReportAPlayer')

    def __init__(self, playerId, avId, avName):
        GuiPanel.GuiPanel.__init__(self, PLocalizer.ReportPlayerTitle, 0.7, 0.9, showClose=False, titleSize=1)
        FSM.FSM.__init__(self, 'ReportAPlayer')
        self.initialiseoptions(ReportAPlayer)
        self.titleLabel['text_scale'] = PiratesGuiGlobals.TextScaleTitleSmall
        self.titleLabel.setPos(0.03, 0, 0.81)
        self.setPos(-self.width * 0.5, 0, -self.height * 0.5)
        self.setScale(1.4)
        self.playerId = playerId
        self.avId = avId
        self.avName = avName
        self.category = None
        gui = loader.loadModel('models/gui/toplevel_gui')
        geomX = gui.find('**/generic_x')
        self.fieldText = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleSmall, text_wordwrap=20, text_fg=PiratesGuiGlobals.TextFG2, pos=(0.05,
                                                                                                                                                                                                          0,
                                                                                                                                                                                                          0.75), textMayChange=1)
        self.buttons = []
        for i in range(4):
            button = GuiButton.GuiButton(parent=self, text='', textMayChange=1, text_scale=PiratesGuiGlobals.TextScaleMed, text_pos=(0, -0.01), text_wordwrap=16, image_scale=(0.56,
                                                                                                                                                                               0.25,
                                                                                                                                                                               0.25))
            button.hide()
            button.setPos(self.width * 0.5, 0, 0.5 + i * -0.1)
            self.buttons.append(button)

        self.cancelButton = GuiButton.GuiButton(parent=self, text=PLocalizer.ReportPlayerCancel, textMayChange=1, text_scale=PiratesGuiGlobals.TextScaleMed, text_pos=(0.035, -0.01), image_scale=(0.3,
                                                                                                                                                                                                   0.22,
                                                                                                                                                                                                   0.22), geom=(geomX,) * 4, geom_pos=(-0.06, 0, 0), geom_scale=0.5, geom0_color=PiratesGuiGlobals.ButtonColor3[0], geom1_color=PiratesGuiGlobals.ButtonColor3[1], geom2_color=PiratesGuiGlobals.ButtonColor3[2], geom3_color=PiratesGuiGlobals.ButtonColor3[3], image3_color=(0.8,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                               0.8,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                               0.8,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                               1), pos=(self.width * 0.5, 0, 0.075), command=self.destroy)
        if base.cr.centralLogger.hasReportedPlayer(self.playerId, self.avId):
            self.request('AlreadyReported')
        else:
            self.request('TopMenu')
        return

    def chooseCategory(self, category):
        self.category = category
        self.request('ConfirmCategory')

    def enterAlreadyReported(self):
        self.fieldText['text'] = PLocalizer.ReportPlayerAlreadyReported % self.avName
        self.cancelButton['text'] = PLocalizer.ReportPlayerClose

    def exitAlreadyReported(self):
        for b in self.buttons:
            b.hide()

    def enterTopMenu(self):
        self.fieldText['text'] = PLocalizer.ReportPlayerTopMenu % self.avName
        self.buttons[3].configure(text=PLocalizer.ReportPlayerReport, command=self.request, extraArgs=['ChooseCategory'])
        self.buttons[3].show()

    def exitTopMenu(self):
        for b in self.buttons:
            b.hide()

    def enterChooseCategory(self):
        self.fieldText['text'] = PLocalizer.ReportPlayerChooseCategory % self.avName
        self.buttons[0].configure(text=PLocalizer.ReportPlayerFoulLanguage, command=self.chooseCategory, extraArgs=[CentralLogger.ReportFoulLanguage])
        self.buttons[0].show()
        self.buttons[1].configure(text=PLocalizer.ReportPlayerPersonalInfo, command=self.chooseCategory, extraArgs=[CentralLogger.ReportPersonalInfo])
        self.buttons[1].show()
        self.buttons[2].configure(text=PLocalizer.ReportPlayerRudeBehavior, command=self.chooseCategory, extraArgs=[CentralLogger.ReportRudeBehavior])
        self.buttons[2].show()
        self.buttons[3].configure(text=PLocalizer.ReportPlayerBadName, command=self.chooseCategory, extraArgs=[CentralLogger.ReportBadName])
        self.buttons[3].show()

    def exitChooseCategory(self):
        for b in self.buttons:
            b.hide()

    def enterConfirmCategory(self):
        if self.category == CentralLogger.ReportFoulLanguage:
            text = PLocalizer.ReportPlayerConfirmFoulLanguage % self.avName
        elif self.category == CentralLogger.ReportPersonalInfo:
            text = PLocalizer.ReportPlayerConfirmPersonalInfo % self.avName
        elif self.category == CentralLogger.ReportRudeBehavior:
            text = PLocalizer.ReportPlayerConfirmRudeBehavior % self.avName
        elif self.category == CentralLogger.ReportBadName:
            text = PLocalizer.ReportPlayerConfirmBadName % self.avName
        text += '\n\n' + PLocalizer.ReportPlayerConfirmCategory
        self.fieldText['text'] = text
        self.buttons[3].configure(text=PLocalizer.ReportPlayerReport, command=self.request, extraArgs=['ConfirmReport'])
        self.buttons[3].show()

    def exitConfirmCategory(self):
        for b in self.buttons:
            b.hide()

    def enterConfirmReport(self):
        self.sendReport()
        text = PLocalizer.ReportPlayerConfirmReport
        removedFriendship = False
        if base.cr.avatarFriendsManager.isFriend(self.avId):
            base.cr.avatarFriendsManager.sendRequestRemove(self.avId)
            removedFriendship = True
        if base.cr.playerFriendsManager.isFriend(self.playerId):
            base.cr.playerFriendsManager.sendRequestRemove(self.playerId)
            removedFriendship = True
        if removedFriendship:
            text += '\n\n' + PLocalizer.ReportPlayerRemovedFriend % self.avName
        if not base.cr.avatarFriendsManager.checkIgnored(self.avId):
            base.cr.avatarFriendsManager.addIgnore(self.avId)
            text += '\n\n' + PLocalizer.ReportPlayerIgnored % self.avName
        self.fieldText['text'] = text
        self.cancelButton['text'] = PLocalizer.ReportPlayerClose

    def exitConfirmReport(self):
        for b in self.buttons:
            b.hide()

    def sendReport(self):
        return base.cr.centralLogger.reportPlayer(self.category, self.playerId, self.avId)

    def destroy(self):
        self.request('Off')
        GuiPanel.GuiPanel.destroy(self)