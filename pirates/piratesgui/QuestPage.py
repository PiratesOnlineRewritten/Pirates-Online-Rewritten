from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import InventoryPage
from pirates.piratesgui import QuestItemGui
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import QuestTitleList
from pirates.piratesgui.BlackPearlCrew import BlackPearlCrew
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import *
from pirates.piratesgui import BorderFrame
from pirates.uberdog import DistributedInventoryBase
import GuiButton
from pirates.quest.QuestDetailGUI import QuestDetailGUI
from pirates.piratesgui import PDialog
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
tpMgr = TextPropertiesManager.getGlobalPtr()
questTitleMain = TextProperties()
questTitleMain.setSmallCaps(1)
questTitleMain.setFont(PiratesGlobals.getPirateFont())
questTitleMain.setTextColor(*PiratesGuiGlobals.TextFG26)
questTitleMain.setShadowColor(*PiratesGuiGlobals.TextFG0)
questTitleMain.setGlyphScale(1.3)
tpMgr.setProperties('questTitleMain', questTitleMain)
questTitle = TextProperties()
questTitle.setSmallCaps(1)
questTitle.setFont(PiratesGlobals.getPirateFont())
questTitle.setTextColor(*PiratesGuiGlobals.TextFG26)
questTitle.setShadowColor(*PiratesGuiGlobals.TextFG0)
questTitle.setGlyphScale(1.2)
tpMgr.setProperties('questTitle', questTitle)
questTitle2 = TextProperties()
questTitle2.setSmallCaps(1)
questTitle2.setFont(PiratesGlobals.getPirateFont())
questTitle2.setTextColor(*PiratesGuiGlobals.TextFG2)
questTitle2.setShadowColor(*PiratesGuiGlobals.TextFG0)
questTitle2.setGlyphScale(1.2)
tpMgr.setProperties('questTitle2', questTitle2)
questPercent = TextProperties()
questPercent.setTextColor(*PiratesGuiGlobals.TextFG27)
questPercent.setGlyphScale(0.8)
tpMgr.setProperties('questPercent', questPercent)
questNew = TextProperties()
questNew.setTextColor(*PiratesGuiGlobals.TextFG4)
questNew.setGlyphScale(0.8)
tpMgr.setProperties('questNew', questNew)
questComplete = TextProperties()
questComplete.setTextColor(*PiratesGuiGlobals.TextFG4)
questComplete.setGlyphScale(0.8)
tpMgr.setProperties('questComplete', questComplete)
questObj = TextProperties()
questObj.setFont(PiratesGlobals.getPirateOutlineFont())
questObj.setTextColor(*PiratesGuiGlobals.TextFG27)
questObj.setShadowColor(*PiratesGuiGlobals.TextFG0)
tpMgr.setProperties('questObj', questObj)

class QuestPage(InventoryPage.InventoryPage):
    notify = directNotify.newCategory('QuestPage')
    specialInfoData = {'Chapter 3': {'class': BlackPearlCrew,'buttonOn': PLocalizer.ShowBlackPearlCrew,'buttonOff': PLocalizer.HideBlackPearlCrew}}

    def __init__(self):
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(QuestPage)
        self.detailId = None
        self.titleBorder = BorderFrame.BorderFrame(parent=self, frameSize=(-0.02, 0.97, -0.02, 0.56))
        self.titleBorder.setPos(0.065, 0, -0.01)
        self.titleBorder.background.setColor(0, 0, 0, 1)
        self.titleBorder.resetDecorations()
        self.titleList = QuestTitleList.QuestTitleList()
        self.titleList.reparentTo(self.titleBorder)
        self.titleList.setPos(0.005, 0, 0)
        self.detailFrame = QuestDetailGUI(parent=self, pos=(0.54, 0, 1.006))
        self.dropButton = GuiButton.GuiButton(parent=self, state=DGG.DISABLED, text=PLocalizer.DropQuest, textMayChange=0, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0, -0.014), pos=(0.91,
                                                                                                                                                                                                   0,
                                                                                                                                                                                                   0.605), image=GuiButton.GuiButton.redGenericButton, image_scale=0.6, command=self.dropQuest, helpText=PLocalizer.DropQuestHelp, helpDelay=PiratesGuiGlobals.HelpPopupTime, helpPos=(-0.335, 0, 0.125))
        gui = loader.loadModel('models/gui/compass_main')
        objectiveGrey = gui.find('**/icon_objective_grey')
        self.trackButton = GuiButton.GuiButton(parent=self, state=DGG.DISABLED, text=PLocalizer.TrackQuest, textMayChange=0, text_pos=(0.035, -0.014), text_scale=PiratesGuiGlobals.TextScaleLarge, pos=(0.66,
                                                                                                                                                                                                         0,
                                                                                                                                                                                                         0.605), command=self.trackQuest, helpText=PLocalizer.TrackQuestHelp, helpDelay=PiratesGuiGlobals.HelpPopupTime, helpPos=(-0.08, 0, 0.125), image=GuiButton.GuiButton.redGenericButton, image_scale=0.6, geom=objectiveGrey, geom_color=Vec4(1, 1, 0, 1), geom_scale=0.2, geom_pos=(-0.07, 0, -0.002))
        self.specialInfoPanel = {}
        self.specialButton = GuiButton.GuiButton(parent=self, state=DGG.NORMAL, text='', textMayChange=1, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0, -0.014), pos=(0.17,
                                                                                                                                                                                  0,
                                                                                                                                                                                  0.605), image=GuiButton.GuiButton.redGenericButton, image_scale=0.6, command=self.showSpecialInfo, helpText=PLocalizer.DropQuestHelp, helpDelay=PiratesGuiGlobals.HelpPopupTime, helpPos=(-0.335, 0, 0.125))
        self.specialButton.hide()
        self.accept('questGuiSelect', self.showQuestDetails)
        self.accept('localAvatarQuestComplete', self.updateQuestDetails)
        self.accept('localAvatarQuestUpdate', self.updateQuestDetails)
        self.accept('localAvatarQuestItemUpdate', self.updateQuestDetails)
        self.accept('inventoryAddDoId-%s-%s' % (localAvatar.getInventoryId(), InventoryCategory.QUESTS), self.updateQuestTitlesNewQuest)
        self.accept('inventoryRemoveDoId-%s-%s' % (localAvatar.getInventoryId(), InventoryCategory.QUESTS), self.updateQuestTitles)
        self.invRequest = None
        self.tmButtonQuick = None
        self.tmButtonSearch = None
        self.tmReadyDialog = None
        return

    def destroy(self):
        self.trackButton.command = None
        self.specialButton.command = None
        self.dropButton.command = None
        self.titleList.destroy()
        del self.titleList
        if self.tmReadyDialog:
            self.tmReadyDialog.destroy()
        InventoryPage.InventoryPage.destroy(self)
        self.ignoreAll()
        return

    def show(self):
        InventoryPage.InventoryPage.show(self)
        localAvatar.guiMgr.removeNewQuestIndicator()

    def dropQuest(self):
        if self.detailId:
            self.dropButton['state'] = DGG.DISABLED
            localAvatar.requestDropQuest(self.detailId)

    def trackQuest(self):
        questId = self.detailId
        if questId == localAvatar.activeQuestId or questId == None:
            localAvatar.b_requestActiveQuest('')
            self.titleList.showTracked('')
            localAvatar.guiMgr.hideTrackedQuestInfo()
            localAvatar.guiMgr.mapPage.worldMap.mapBall.removeDart()
        else:
            localAvatar.b_requestActiveQuest(questId, localSet=True)
            self.titleList.showTracked(questId)
            quest = localAvatar.getQuestById(questId)
            if quest is None:
                print 'Tracked quest not found on avatar!\n  Tracked quest: %s\n  Current quests: %s' % (questId,
                 map(lambda q: q.getQuestId(), localAvatar.getQuests()))
                localAvatar.guiMgr.hideTrackedQuestInfo()
            elif localAvatar.questStep:
                mapPage = localAvatar.guiMgr.mapPage
                doId = base.cr.uidMgr.uid2doId.get(localAvatar.questStep.getIsland())
                island = base.cr.doId2do.get(doId)
                if island:
                    pos = island.getPos()
                    if mapPage.worldMap.mapBall.questDartPlaced:
                        localAvatar.guiMgr.mapPage.worldMap.mapBall.updateDart('questStep', pos)
                    else:
                        localAvatar.guiMgr.mapPage.addQuestDart('questStep', pos)
                else:
                    localAvatar.guiMgr.mapPage.removeQuestDart('questStep')
        return

    def findNewActiveQuest(self, oldQuestId):
        localAvatar.d_findNewActiveQuest(oldQuestId)
        localAvatar.l_requestActiveQuest('')
        self.titleList.showTracked('')
        localAvatar.guiMgr.setQuestStatusText('')
        localAvatar.guiMgr.setQuestHintText('')
        localAvatar.guiMgr.hideTrackedQuestInfo()
        localAvatar.guiMgr.mapPage.worldMap.mapBall.removeDart()

    def updateQuestTitlesNewQuest(self, quest):
        self.updateQuestTitles(quest, newQuest=True)

    def updateQuestTitles(self, quest=None, newQuest=False, findNewTrackable=True):
        questIds = map(lambda q: q.getQuestId(), localAvatar.getQuests())
        self.titleList.update(questIds, quest, newQuest)
        if localAvatar.activeQuestId:
            self.titleList.showTracked(localAvatar.activeQuestId)
            localAvatar.guiMgr.showTrackedQuestInfo()
        if not self.detailId and localAvatar.activeQuestId:
            self.detailId = localAvatar.activeQuestId
        if self.detailId not in questIds:
            if questIds:
                self.detailId = None
                self.detailFrame.clearQuestDetails()
            else:
                self.showQuestDetails(None)
                self.dropButton['state'] = DGG.DISABLED
                self.trackButton['state'] = DGG.DISABLED
        elif not self.detailFrame.hasQuestDetails() or localAvatar.activeQuestId and self.detailId != localAvatar.activeQuestId:
            self.titleList.select(localAvatar.activeQuestId)
        localAvatar.chatMgr.emoteEntry.updateEmoteList()
        localAvatar.l_setActiveQuest(localAvatar.activeQuestId)
        return

    def showQuestDetails(self, questId):
        self.hideSpecialInfo()
        if questId in self.specialInfoData.keys():
            self.specialButton['text'] = self.specialInfoData[questId].get('buttonOn')
            self.specialButton['command'] = self.showSpecialInfo
            self.specialButton['extraArgs'] = [questId]
            self.specialButton.show()
        else:
            self.specialButton.hide()
        self.detailId = questId
        self.updateQuestIdDetails(questId)

    def updateQuestDetails(self, quest, item=None, note=None):
        questId = quest.getQuestId()
        self.updateQuestIdDetails(questId)
        self.updateQuestTitles(quest)
        messenger.send('localAvatarActiveQuestId', sentArgs=[localAvatar.activeQuestId])

    def updateQuestIdDetails(self, questId):
        self.removeTreasureMapButtons()
        if not questId:
            self.detailFrame.clearQuestDetails()
            return
        if self.detailId != questId:
            return
        quest = localAvatar.getQuestById(questId)
        if not quest:
            self.dropButton['state'] = DGG.DISABLED
            self.trackButton['state'] = DGG.DISABLED
            self.detailFrame.setQuestInfoFromQuestId(questId)
        else:
            self.detailFrame.setQuestInfoFromQuest(quest)
            self.checkButtonDisplay(quest)
            trackableQuestId = base.cr.questChoiceSibsMap.getTrackableQuest(localAvatar, quest.questId)
            if trackableQuestId == quest.questId or trackableQuestId == None:
                self.trackButton['state'] = DGG.NORMAL
            else:
                self.trackButton['state'] = DGG.DISABLED
                if self.detailId == localAvatar.activeQuestId:
                    self.findNewActiveQuest(quest.questId)
            if quest.isDroppable():
                self.dropButton['state'] = DGG.NORMAL
            else:
                self.dropButton['state'] = DGG.DISABLED
        return

    def checkButtonDisplay(self, quest):
        questDNA = quest.getQuestDNA()
        if questDNA == None:
            return
        questTasks = questDNA.getTasks()
        for currQuestTask in questTasks:
            if not hasattr(currQuestTask, 'getTreasureMapId'):
                continue
            tmId = currQuestTask.getTreasureMapId()
            if tmId != None:

                def inventoryReceived(inventory):
                    if inventory:
                        self.invRequest = None
                        tms = inventory.getTreasureMapsList()
                        for currTm in tms:
                            if currTm.mapId == tmId:
                                currTm.sendUpdate('requestIsEnabled')
                                self.addTreasureMapButtons(currTm, 0.602)
                                break

                    return

                self.invRequest = DistributedInventoryBase.DistributedInventoryBase.getInventory(localAvatar.getInventoryId(), inventoryReceived)

        return

    def addTreasureMapButtons(self, tm, buttonOffset):
        self.removeTreasureMapButtons()
        helpPos = (-0.26, 0, 0.095)
        if __debug__ and base.config.GetBool('enable-bp-solo', False):
            self.tmButtonQuick = GuiButton.GuiButton(parent=self, text=PLocalizer.PlayTMNow, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0, -0.01), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=40, image_scale=(0.45,
                                                                                                                                                                                                                                                                                                          1,
                                                                                                                                                                                                                                                                                                          0.24), command=self.startTreasureMap, extraArgs=[tm], pos=(0.3, 0, buttonOffset), helpText=PLocalizer.PlayTMNowHelp, helpPos=helpPos)
            searchPos = (
             0.775, 0, buttonOffset)
        else:
            searchPos = (
             0.55, 0, buttonOffset)
        self.tmButtonSearch = GuiButton.GuiButton(parent=self, text=PLocalizer.PlayTMLookout, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0, -0.01), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=40, image_scale=(0.45,
                                                                                                                                                                                                                                                                                                           1,
                                                                                                                                                                                                                                                                                                           0.24), command=self.startTreasureMap, extraArgs=[tm, False], pos=searchPos, helpText=PLocalizer.PlayTMLookoutHelp, helpPos=helpPos)
        if base.cr.teleportMgr.inInstanceType == PiratesGlobals.INSTANCE_TM:
            self.disableTreasureMapButtons()
        else:
            self.enableTreasureMapButtons()

    def removeTreasureMapButtons(self):
        self.trackButton.show()
        self.dropButton.show()
        if self.tmButtonQuick:
            self.tmButtonQuick.removeNode()
            self.tmButtonQuick = None
        if self.tmButtonSearch:
            self.tmButtonSearch.removeNode()
            self.tmButtonSearch = None
        return

    def enableTreasureMapButtons(self):
        if self.tmButtonQuick:
            self.tmButtonQuick['state'] = 'normal'
        if self.tmButtonSearch:
            self.tmButtonSearch['state'] = 'normal'
        self.trackButton.hide()
        self.dropButton.hide()

    def disableTreasureMapButtons(self):
        if self.tmButtonQuick:
            self.tmButtonQuick['state'] = 'disabled'
        if self.tmButtonSearch:
            self.tmButtonSearch['state'] = 'disabled'
        self.trackButton.hide()
        self.dropButton.hide()

    def startTreasureMap(self, tm, quick=True):
        if localAvatar.getAccess() != OTPGlobals.AccessFull:
            self.tmReadyDialog = PDialog.PDialog(text=PLocalizer.PlayTMVelvetRope, style=OTPDialog.Acknowledge, giveMouse=False, command=self.notReadyCallback)
            self.tmReadyDialog.show()
            return None
        if tm.getIsEnabled() or base.config.GetBool('black-pearl-ready', 0):
            from pirates.band.DistributedBandMember import DistributedBandMember
            if not DistributedBandMember.getBandMember(localAvatar.doId) and quick == False:
                localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.LookoutInviteNeedCrew, icon=('lookout',
                                                                                                       None))
                return None
            if localAvatar.testTeleportFlag(PiratesGlobals.TFNoTeleport) == False:
                if base.cr.teleportMgr.inInstanceType == PiratesGlobals.INSTANCE_MAIN:
                    tm.requestTreasureMapGo(quick)
                elif base.cr.teleportMgr.inInstanceType == PiratesGlobals.INSTANCE_TM:
                    tm.requestTreasureMapLeave()
        else:
            self.tmReadyDialog = PDialog.PDialog(text=PLocalizer.PlayTMBlackPearlNotReady, style=OTPDialog.Acknowledge, giveMouse=False, command=self.notReadyCallback)
            self.tmReadyDialog.show()
        return None

    def notReadyCallback(self, args):
        self.tmReadyDialog.hide()

    def showSpecialInfo(self, containerId=None):
        if not self.specialInfoPanel.has_key(containerId):
            panelClass = self.specialInfoData[containerId].get('class')
            self.specialInfoPanel[containerId] = panelClass()
            self.specialInfoPanel[containerId].reparentTo(self.detailFrame)
        self.specialButton['text'] = self.specialInfoData[containerId].get('buttonOff')
        self.specialButton['command'] = self.hideSpecialInfo
        self.specialInfoPanel[containerId].update()
        self.specialInfoPanel[containerId].show()
        self.detailFrame.setQuestTitleOnly(containerId)

    def hideSpecialInfo(self, containerId=None):
        for specialPanelId in self.specialInfoPanel.keys():
            self.specialInfoPanel[specialPanelId].hide()

        if containerId:
            self.showQuestDetails(containerId)