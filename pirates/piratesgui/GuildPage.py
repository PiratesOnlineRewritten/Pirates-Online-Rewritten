from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm import StateData
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPLocalizer
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import SocialPage
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import Freebooter
from pirates.piratesgui import PirateMemberList
from pirates.piratesgui import PirateButtonChain
from pirates.piratesgui import PiratesConfirm
from pirates.piratesgui import PiratesInfo
from pirates.piratesgui import PiratesOffLineRequest
from pirates.uberdog.UberDogGlobals import InventoryType
GUILDRANK_VETERAN = 4
GUILDRANK_GM = 3
GUILDRANK_OFFICER = 2
GUILDRANK_MEMBER = 1

class GuildPage(SocialPage.SocialPage):
    memberHeight = 0.1

    def __init__(self):
        SocialPage.SocialPage.__init__(self, PLocalizer.GuildPageTitle)
        self.initialiseoptions(GuildPage)
        self.setupFlag = 0
        self.confirmBox = None
        self.crew = {}
        self.leaveButton = 0
        self.createButton = 0
        self.nameEntry = 0
        self.tokenEntry = 0
        self.nameLabel = 0
        self.rankLabel = 0
        self.memberButton = 0
        self.revertButton = 0
        self.renameButton = 0
        self.aboutButton = 0
        self.inviteButton = 0
        self.redeemInvite = 0
        self.manageInvite = 0
        self.codeInviteOptions = 0
        self.aboutTokenManagement = 0
        self.clearPermToken = 0
        self.clearLimitedUseToken = 0
        self.suspendPermToken = 0
        self.notifyPreferences = 0
        self.tokenManagementToMain = 0
        self.tokenManagementToMembers = 0
        self.permTokenLabel = 0
        self.permTokenLabelTitle = 0
        self.permTokenValue = 0
        self.nonPermTokenCount = 0
        self.recentlySentName = False
        self.notLoaded = 1
        self.mainFrame = DirectFrame(relief=None, parent=self)
        self.membersFrame = DirectFrame(relief=None, parent=self)
        self.tokenFrame = DirectFrame(relief=None, parent=self)
        self.setupMemberPage = 0
        self.membersList = PirateMemberList.PirateMemberList(5, self.membersFrame, 'FOOLIO HC', height=0.6, memberHeight=0.1, memberWidth=0.6, memberOffset=0.055, width=0.62, sort=1)
        self.membersList.setPos(-0.087, 0.0, 0.11)
        self.accept(self.membersList.onlineChangeEvent, self.updateCount)
        self.mainChain = PirateButtonChain.PirateButtonChain(0.56, self.mainFrame, True)
        self.mainChain.setPos(-0.052, 0.0, 0.025)
        self.memberChain = PirateButtonChain.PirateButtonChain(0.56, self.membersFrame, True)
        self.memberChain.setPos(-0.052, 0.0, 0.025)
        self.membersFrame.hide()
        self.tokenChain = PirateButtonChain.PirateButtonChain(0.56, self.tokenFrame, True)
        self.tokenChain.setPos(-0.052, 0.0, 0.025)
        self.tokenFrame.hide()
        self.accept('Guild Status Updated', self.revertGui)
        self.headingLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.GuildPageTitle, state=DGG.NORMAL, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                        0.0), text_fg=PiratesGuiGlobals.TextFG1, textMayChange=1, pos=(0.23,
                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                       0.794))
        return

    def show(self):
        SocialPage.SocialPage.show(self)
        self.determineButtonState()
        if self.nameEntry:
            self.nameEntry.hide()
            self.nameLabel.show()
        if self.permTokenLabel:
            pass
        if self.tokenEntry:
            self.tokenEntry.hide()
        self.membersList.updateOnlineData()

    def initGuildPage(self):
        self.load()
        self.guildRank = 0
        self.guildId = base.localAvatar.getGuildId()
        self.requestPermTokenValue()
        self.requestNonPermTokenCount()

    def setupButtons(self):
        if not self.nameLabel:
            self.nameLabel = DirectLabel(parent=self.mainFrame, relief=None, text='', text_fg=(0.95,
                                                                                               1,
                                                                                               1,
                                                                                               1), text_align=TextNode.ACenter, text_shadow=(0,
                                                                                                                                             0,
                                                                                                                                             0,
                                                                                                                                             1), text_scale=0.06)
            self.nameLabel.setPos(0.23, 0, 0.637)
        if not self.rankLabel:
            self.rankLabel = DirectLabel(parent=self.mainFrame, relief=None, text='', text_fg=(1,
                                                                                               1,
                                                                                               1,
                                                                                               1), text_align=TextNode.ACenter, text_shadow=(0,
                                                                                                                                             0.0,
                                                                                                                                             0,
                                                                                                                                             1), text_scale=0.04)
            self.rankLabel.setPos(0.23, 0, 0.585)
        if self.guildId:
            self.guildName = base.localAvatar.getGuildName()
            self.guildReal = self.guildName
            self.guildRank = base.localAvatar.getGuildRank()
            if self.guildName == '0' or self.guildName == '':
                self.guildName = PLocalizer.GuildDefaultName % self.guildId
        if not self.memberButton:
            self.memberButton = self.mainChain.premakeButton(PLocalizer.GuildPageShowMembers, self.showGuildMembers)
        if not self.renameButton:
            self.renameButton = self.mainChain.premakeButton(PLocalizer.GuildPageNameGuild, self.renameGuild)
        if not self.createButton:
            self.createButton = self.mainChain.premakeButton(PLocalizer.GuildPageCreateGuild, self.createGuild)
        if not self.leaveButton:
            self.leaveButton = self.mainChain.premakeButton(PLocalizer.GuildPageLeaveGuild, self.leaveGuild)
        if not self.inviteButton:
            self.inviteButton = self.mainChain.premakeButton(PLocalizer.GuildInvite, self.inviteGuild)
        if not self.redeemInvite:
            self.redeemInvite = self.mainChain.premakeButton(PLocalizer.GuildRedeemInvite, self.redeemInviteGuild)
        if not self.codeInviteOptions:
            self.codeInviteOptions = self.mainChain.premakeButton(PLocalizer.GuildCodeOptions, self.b_codeInviteOptions)
        self.mainChain.makeButtons()
        self.setupFlag = 1
        self.determineButtonState()
        return

    def determineButtonState(self):
        self.guildName = None
        self.guildReal = None
        self.guildRank = None
        self.guildId = base.localAvatar.guildId
        if not self.setupFlag:
            self.setupButtons()
        if self.guildId:
            self.guildName = base.localAvatar.getGuildName()
            self.guildReal = self.guildName
            self.guildRank = base.localAvatar.getGuildRank()
            if self.guildName == '0' or self.guildName == '':
                self.guildName = PLocalizer.GuildDefaultName % self.guildId
            if hasattr(base, 'localAvatar'):
                inv = base.localAvatar.getInventory()
                if inv and not inv.getStackQuantity(InventoryType.NewGuild):
                    base.localAvatar.sendRequestContext(InventoryType.NewGuild)
        if self.nameLabel and self.guildName and self.guildName != PLocalizer.GuildNoGuild and (self.guildName != '0' or self.guildName != ''):
            self.nameLabel.show()
            self.nameLabel['text'] = self.guildName
        elif self.nameLabel:
            self.nameLabel.hide()
        rank = base.localAvatar.getGuildRank()
        if rank == 1:
            ranktxt = PLocalizer.GuildRankMember
        else:
            if rank == 2:
                ranktxt = PLocalizer.GuildRankSubLead
            else:
                if rank == 3:
                    ranktxt = PLocalizer.GuildRankLeader
                else:
                    if rank == 4:
                        ranktxt = PLocalizer.GuildRankInviter
                    else:
                        ranktxt = None
                    if self.rankLabel and rank and ranktxt:
                        self.rankLabel['text'] = ranktxt
                        self.rankLabel.show()
                    elif self.rankLabel:
                        ranktxt = PLocalizer.Loading
                        self.rankLabel.hide()
                    if self.memberButton:
                        self.memberButton['state'] = DGG.DISABLED
                    self.renameButton['state'] = DGG.DISABLED
                    self.createButton['state'] = DGG.DISABLED
                    self.leaveButton['state'] = DGG.DISABLED
                    self.inviteButton['state'] = DGG.DISABLED
                    self.redeemInvite['state'] = DGG.NORMAL
                    self.codeInviteOptions['state'] = DGG.DISABLED
                    if self.guildRank > 2 and (self.guildReal == '0' or self.guildReal == '') and not self.recentlySentName:
                        self.renameButton['state'] = DGG.NORMAL
                        self.redeemInvite['state'] = DGG.DISABLED
                    if self.guildRank > 1:
                        self.inviteButton['state'] = DGG.NORMAL
                        self.redeemInvite['state'] = DGG.DISABLED
                        self.codeInviteOptions['state'] = DGG.NORMAL
                if self.guildRank > 0:
                    self.leaveButton['state'] = DGG.NORMAL
                    self.memberButton['state'] = DGG.NORMAL
                    self.redeemInvite['state'] = DGG.DISABLED
                self.createButton['state'] = DGG.NORMAL
            if Freebooter.FreeGuildRestrict:
                if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                    if self.createButton:
                        self.createButton['state'] = DGG.DISABLED
                    if self.renameButton:
                        self.renameButton['state'] = DGG.DISABLED
        return

    def destroy(self):
        self.ignoreAll()
        self.crew = None
        self.confirmBox = None
        self.membersList.destroy()
        self.mainChain.destroy()
        self.memberChain.destroy()
        self.tokenChain.destroy()
        SocialPage.SocialPage.destroy(self)
        return

    def aboutGuild(self):
        self.confirmBox = PiratesInfo.PiratesInfo(PLocalizer.GuildAbout, PLocalizer.GuildTut)
        if self.nameEntry:
            self.nameEntry.hide()
            self.nameLabel.show()
        if self.tokenEntry:
            self.tokenEntry.hide()

    def manageInviteGuild(self):
        self.displayTokenOptionsFrame()

    def b_clearPermToken(self):
        self.confirmBox = PiratesConfirm.PiratesConfirm(PLocalizer.GuildClearPerm, PLocalizer.GuildMessageClearPermInvite, self.executeClearPermToken, titleScale=PiratesGuiGlobals.TextScaleMed)

    def executeClearPermToken(self):
        try:
            self.permTokenLabel.hide()
        except AttributeError:
            pass

        base.cr.guildManager.requestClearTokens(1)
        self.permTokenValue = 0
        self.permTokenLabel = ''
        self.clearPermToken['state'] = DGG.DISABLED

    def b_suspendPermToken(self):
        pass

    def b_clearLimitedUseToken(self):
        self.confirmBox = PiratesConfirm.PiratesConfirm(PLocalizer.GuildClearLimUse, PLocalizer.GuildMessageClearLimInvite, self.executeClearLimitedUseToken, titleScale=PiratesGuiGlobals.TextScaleMed)

    def executeClearLimitedUseToken(self):
        base.cr.guildManager.requestClearTokens(0)
        self.clearLimitedUseToken['state'] = DGG.DISABLED

    def b_notifyOptionsToken(self):
        pass

    def b_aboutTokenManagement(self):
        self.confirmBox = PiratesInfo.PiratesInfo(PLocalizer.GuildTokenAbout, PLocalizer.GuildTokenTut)

    def redeemInviteGuild(self):
        self.inputTokenForGuild()

    def displayRedeemErrorMessage(self, msgString=OTPLocalizer.GuildRedeemErrorInvalidToken):
        self.confirmBox = PiratesOffLineRequest.PiratesOffLineRequest(PLocalizer.GuildInvite, msgString)

    def displayRedeemConfirmMessage(self, guildName):
        self.guildId = base.localAvatar.getGuildId()
        self.confirmBox = PiratesOffLineRequest.PiratesOffLineRequest(PLocalizer.GuildInvite, PLocalizer.GuildInviteJoinSucessful % guildName)
        if self.tokenEntry:
            self.tokenEntry.set('')

    def inviteGuild(self):
        base.cr.guildManager.sendTokenRequest()

    def displayInviteGuild(self, displayToken, preExistPerm):
        if displayToken == 'TOO_MANY_TOKENS':
            self.confirmBox = PiratesOffLineRequest.PiratesOffLineRequest(PLocalizer.GuildInvite, PLocalizer.GuildInviteTooManyTokens)
        elif displayToken == 'GUILD FULL':
            self.confirmBox = PiratesOffLineRequest.PiratesOffLineRequest(PLocalizer.GuildInvite, OTPLocalizer.GuildInviterTooFull)
        else:
            self.confirmBox = PiratesOffLineRequest.PiratesOffLineRequest(PLocalizer.GuildInvite, PLocalizer.GuildInviteResponse, displayToken, preExistPerm)

    def leaveGuild(self):
        if localAvatar.getGuildRank() == GUILDRANK_GM and len(base.cr.guildManager.id2Name.keys()) > 1:
            self.confirmBox = PiratesInfo.PiratesInfo(PLocalizer.GuildPageLeaveGuild, [PLocalizer.GuildAskLeaveGM])
        else:
            self.confirmBox = PiratesConfirm.PiratesConfirm(PLocalizer.GuildPageLeaveGuild, PLocalizer.GuildAskLeave, base.cr.guildManager.removeMember, base.localAvatar.getDoId())
            if self.nameEntry:
                self.nameEntry.hide()
                self.nameLabel.show()
            self.recentlySentName = False
            self.permTokenValue = 0
            self.clearLocalPermTokenValue()
            self.nonPermTokenCount = 0

    def createGuild(self):
        if self.tokenEntry:
            self.tokenEntry.hide()
        self.confirmBox = PiratesConfirm.PiratesConfirm(PLocalizer.GuildPageCreateGuild, PLocalizer.GuildAskCreate, base.cr.guildManager.createGuild)
        if self.clearPermToken:
            self.clearPermToken['state'] = DGG.DISABLED
        if self.clearLimitedUseToken:
            self.clearLimitedUseToken['state'] = DGG.DISABLED

    def renameGuild(self):
        buttonColor = (
         (0.33, 0.3, 0.26, 1.0), (0.26, 0.24, 0.21, 1.0), (0.49, 0.45, 0.39, 1.0), (0.16, 0.15, 0.13, 1.0))
        if self.nameEntry:
            self.nameLabel.hide()
            self.nameEntry.show()
            self.nameEntry['focus'] = 1
        else:
            self.nameLabel.hide()
            self.nameEntry = DirectEntry(parent=self.mainFrame, relief=DGG.RAISED, scale=0.051, pos=(0.24,
                                                                                                     0,
                                                                                                     0.637), borderWidth=PiratesGuiGlobals.BorderWidthSmall, frameColor=(1,
                                                                                                                                                                         1,
                                                                                                                                                                         1,
                                                                                                                                                                         0.1), text_align=TextNode.ACenter, width=8, numLines=1, focus=1, cursorKeys=1, text_fg=(1,
                                                                                                                                                                                                                                                                 1,
                                                                                                                                                                                                                                                                 1,
                                                                                                                                                                                                                                                                 1), command=self._typedAName, suppressKeys=1, suppressMouse=1, autoCapitalize=1)

    def inputTokenForGuild(self):
        buttonColor = (
         (0.33, 0.3, 0.26, 1.0), (0.26, 0.24, 0.21, 1.0), (0.49, 0.45, 0.39, 1.0), (0.16, 0.15, 0.13, 1.0))
        if self.tokenEntry:
            self.tokenEntry.show()
            self.tokenEntry['focus'] = 1
        else:
            self.tokenEntry = DirectEntry(parent=self.mainFrame, relief=DGG.RAISED, scale=0.051, pos=(0.24,
                                                                                                      0,
                                                                                                      0.637), borderWidth=PiratesGuiGlobals.BorderWidthSmall, frameColor=(1,
                                                                                                                                                                          1,
                                                                                                                                                                          1,
                                                                                                                                                                          0.1), text_align=TextNode.ACenter, width=8, numLines=1, focus=1, cursorKeys=1, text_fg=(1,
                                                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                                                  1,
                                                                                                                                                                                                                                                                  1), command=self._typedAToken, suppressKeys=1, suppressMouse=1)

    def _typedAName(self, *args):
        self.nameEntry['focus'] = 0
        name = self.nameEntry.get()
        name = TextEncoder().decodeText(name)
        name = name.strip()
        name = TextEncoder().encodeWtext(name)
        self.nameEntry.enterText(name)
        newName = name
        self.nameEntry.hide()
        self.nameLabel.show()
        base.cr.guildManager.setWantName(newName)
        base.localAvatar.guildNameRequest()
        self.renameButton['state'] = DGG.DISABLED
        self.recentlySentName = True

    def _typedAToken(self, *args):
        self.tokenEntry['focus'] = 0
        token = self.tokenEntry.get()
        newToken = self.tokenEntry.get().replace(' ', '')
        newToken = newToken.upper()
        self.tokenEntry.hide()
        base.cr.guildManager.sendTokenForJoinRequest(newToken)

    def showGuildMembers(self):
        base.cr.guildManager.memberList()
        self.mainFrame.hide()
        self.tokenFrame.hide()
        self.membersFrame.show()
        if not self.setupMemberPage:
            self.revertButton = self.memberChain.premakeButton(PLocalizer.GuildPageRevertGui, self.revertGui)
            self.memberChain.makeButtons()
            self.setupMemberPage = True
        else:
            self.membersFrame.show()
        if self.nameEntry:
            self.nameEntry.hide()

    def showGuildMembersFake(self):
        pass

    def revertGui(self):
        self.mainFrame.show()
        self.membersFrame.hide()
        self.tokenFrame.hide()
        if self.nameEntry:
            self.nameEntry.hide()
        self.determineButtonState()

    def displayTokenOptionsFrame(self):
        self.mainFrame.hide()
        self.membersFrame.hide()
        if not self.permTokenLabel:
            if self.permTokenValue:
                label = self.permTokenValue
            else:
                label = PLocalizer.GuildNoPermInviteCodeSet
            self.permTokenLabel = DirectLabel(parent=self.tokenFrame, relief=None, text=str(label), text_fg=(0.95,
                                                                                                             1,
                                                                                                             1,
                                                                                                             1), text_align=TextNode.ACenter, text_shadow=(0,
                                                                                                                                                           0,
                                                                                                                                                           0,
                                                                                                                                                           1), text_scale=0.06)
            self.permTokenLabel.setPos(0.23, 0, 0.57)
        if not self.permTokenLabelTitle:
            self.permTokenLabelTitle = DirectLabel(parent=self.tokenFrame, relief=None, text=PLocalizer.GuildPermCodeLabel, text_fg=(0.95,
                                                                                                                                     1,
                                                                                                                                     1,
                                                                                                                                     1), text_align=TextNode.ACenter, text_shadow=(0,
                                                                                                                                                                                   0,
                                                                                                                                                                                   0,
                                                                                                                                                                                   1), text_scale=0.04)
            self.permTokenLabelTitle.setPos(0.23, 0, 0.647)
        self.permTokenLabelTitle.hide()
        if self.permTokenValue and self.permTokenLabel:
            self.permTokenLabel['text'] = self.permTokenValue
            self.permTokenLabelTitle.show()
        if not self.clearPermToken:
            self.clearPermToken = self.tokenChain.premakeButton(PLocalizer.GuildClearPerm, self.b_clearPermToken)
        if not self.clearLimitedUseToken:
            self.clearLimitedUseToken = self.tokenChain.premakeButton(PLocalizer.GuildClearLimUse, self.b_clearLimitedUseToken)
        if not self.tokenManagementToMain:
            self.tokenManagementToMain = self.tokenChain.premakeButton(PLocalizer.GuildPageRevertGui, self.revertGui)
        self.tokenChain.makeButtons()
        self.tokenFrame.show()
        self.permTokenLabel.show()
        self.permTokenLabelTitle.show()
        self.determineTokenButtonState()
        return

    def determineTokenButtonState(self):
        if not self.permTokenValue:
            self.clearPermToken['state'] = DGG.DISABLED
        if not self.nonPermTokenCount:
            self.clearLimitedUseToken['state'] = DGG.DISABLED

    def receiveMembers(self, memlist):
        self.mainFrame.hide()
        self.tokenFrame.hide()
        self.membersFrame.show()
        if not self.setupMemberPage:
            self.revertButton = self.memberChain.premakeButton(PLocalizer.GuildPageRevertGui, self.revertGui)
            self.memberChain.makeButtons()
            self.setupMemberPage = True
        else:
            self.membersFrame.show()
        cullList = []
        timeBefore = globalClock.getRealTime()
        for info in memlist:
            cullList.append(info[0])
            self.membersList.updateOrAddMember(info[0], None, PirateMemberList.MODE_GUILD, list(info))

        self.membersList.removeNotOnAvList(cullList)
        self.startRecountMembers()
        timeAfter = globalClock.getRealTime()
        timeToCreate = timeAfter - timeBefore
        return

    def updateCount(self, task=None):
        self.count = self.membersList.getSize()
        self.headingLabel['text'] = '%s %s/%s' % (PLocalizer.GuildPageTitle, self.membersList.onlineCount, self.membersList.getSize())
        if task:
            return task.done

    def addMember(self, info):
        self.membersList.addMember(info[0], None, PirateMemberList.MODE_GUILD, list(info))
        self.startRecountMembers()
        return

    def removeMember(self, avatarId):
        self.membersList.removeMember(avatarId, None, PirateMemberList.MODE_GUILD)
        self.startRecountMembers()
        return

    def updateGuildMemberRank(self, avatarId, rank):
        self.membersList.updateGuildMemberRank(avatarId, rank)

    def load(self):
        pass

    def notifyTokenGeneratorOfRedeem(self, redeemerName):
        msg = PLocalizer.GuildNotifyTokenCreatorOfRedeem % redeemerName
        base.localAvatar.guiMgr.messageStack.addTextMessage(msg, seconds=15, priority=0, color=(0.5,
                                                                                                0.0,
                                                                                                0,
                                                                                                1), icon=('friends',
                                                                                                          ''))

    def requestPermTokenValue(self):
        base.cr.guildManager.requestPermToken()

    def requestNonPermTokenCount(self):
        base.cr.guildManager.requestNonPermTokenCount()

    def receivePermTokenValue(self, token):
        if not token:
            return
        self.permTokenValue = token
        if self.clearPermToken:
            self.clearPermToken['state'] = DGG.NORMAL

    def receiveNonPermTokenCount(self, count):
        self.nonPermTokenCount = count
        if not count:
            if self.clearLimitedUseToken:
                self.clearLimitedUseToken['state'] = DGG.DISABLED
            return
        if self.clearLimitedUseToken:
            self.clearLimitedUseToken['state'] = DGG.NORMAL
            self.nonPermTokenCount = count

    def getNonPermTokenCount(self):
        return self.nonPermTokenCount

    def clearLocalPermTokenValue(self):
        self.permTokenValue = PLocalizer.GuildNoPermInviteCodeSet
        if self.permTokenLabel:
            self.permTokenLabel['text'] = self.permTokenValue

    def b_codeInviteOptions(self):
        self.displayTokenOptionsFrame()

    def resetRenameButton(self):
        self.recentlySentName = False
        self.renameButton['state'] = DGG.NORMAL