from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.distributed import InteractGlobals
from pirates.quest import QuestDB, QuestLadderDB, QuestReward
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.reputation import ReputationGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.quest.QuestDetailGUI import QuestDetailBase
from pirates.piratesgui import GameGui
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.inventory import InventoryUIRewardsContainer
from pirates.inventory import ItemGlobals
tpMgr = TextPropertiesManager.getGlobalPtr()
questRewardComplete = TextProperties()
questRewardComplete.setTextColor(0.3, 0.7, 0.25, 1)
questRewardComplete.setGlyphScale(1.2)
tpMgr.setProperties('questRewardComplete', questRewardComplete)
questRewardTitle = TextProperties()
questRewardTitle.setSmallCaps(1)
questRewardTitle.setFont(PiratesGlobals.getPirateFont())
questRewardTitle.setTextColor(*PiratesGuiGlobals.TextFG26)
questRewardTitle.setShadowColor(*PiratesGuiGlobals.TextFG0)
tpMgr.setProperties('questRewardTitle', questRewardTitle)

class QuestRewardGUI(QuestDetailBase):

    def __init__(self, quest, rewards):
        self.width = 1
        self.rewards = rewards
        QuestDetailBase.__init__(self, parent=base.a2dBottomRight, pos=(0.6, 0, 0.52), text_fg=PiratesGuiGlobals.TextFG0)
        self.initialiseoptions(QuestRewardGUI)
        self.questComplete = DirectLabel(parent=self, relief=None, text=PLocalizer.QuestCompleted, text_fg=PiratesGuiGlobals.TextFG4, text_font=PiratesGlobals.getPirateOutlineFont(), text_shadow=(0,
                                                                                                                                                                                                    0,
                                                                                                                                                                                                    0,
                                                                                                                                                                                                    1), pos=(-1.32,
                                                                                                                                                                                                             0,
                                                                                                                                                                                                             0.13), scale=PiratesGuiGlobals.TextScaleTitleMed)
        gui = loader.loadModel('models/gui/toplevel_gui')
        gcButton = gui.find('**/treasure_w_coin*')
        goldCoin = gcButton.copyTo(gcButton)
        goldCoin.setScale(3)
        tpMgr.setGraphic('goldCoin', goldCoin)
        self.popupSfx = loadSfx(SoundGlobals.SFX_GUI_REWARD_POPUP)
        self.popupSfx.setVolume(0.4)
        self.reputation = self.rewards.get('reputation', 0)
        self.totalReputation = 0
        self.rewardsContainer = None
        self.items = self.rewards.get('items', [])
        if self.items:
            scale = 0.12 * len(self.items)
            self.rewardsContainer = InventoryUIRewardsContainer.InventoryUIRewardsContainer(localAvatar.guiMgr.inventoryUIManager, sizeX=scale, sizeZ=scale, countX=len(self.items), countZ=1)
            self.rewardsContainer.setPos(-0.1, 0, -0.225 - 0.06 * len(self.items))
            self.rewardsContainer.reparentTo(self)
            for itemId in self.items:
                self.rewardsContainer.addRewardIntoGrid(itemId, self.items.index(itemId), 0)

        inv = localAvatar.getInventory()
        if inv:
            self.totalReputation = localAvatar.getInventory().getReputation(InventoryType.OverallRep)
        oldLevel, leftoverValue = ReputationGlobals.getLevelFromTotalReputation(InventoryType.OverallRep, self.totalReputation)
        newLevel, leftoverValue = ReputationGlobals.getLevelFromTotalReputation(InventoryType.OverallRep, self.totalReputation + self.reputation)
        if oldLevel != newLevel:
            self.showLevelUp = True
        else:
            self.showLevelUp = False
        self.buildIvals()
        self.setQuestInfoFromQuest(quest)
        self.showPanel()
        return

    def destroy(self):
        self.showIval.pause()
        self.showIval = None
        self.hideIval.pause()
        self.hideIval = None
        self.questCompleteScaleSeq.pause()
        self.questCompleteScaleSeq = None
        self.colorChangeParallel.pause()
        self.colorChangeParallel = None
        self.gameGui.destroy()
        self.gameGui = None
        self.questComplete.destroy()
        self.questComplete = None
        self.rewards = None
        if self.rewardsContainer:
            self.rewardsContainer.destroy()
        loader.unloadSfx(self.popupSfx)
        del self.popupSfx
        QuestDetailBase.destroy(self)
        return

    def buildIvals(self):
        self.questCompleteScaleSeq = Sequence(LerpScaleInterval(self.questComplete, 1.0, scale=0.045), LerpScaleInterval(self.questComplete, 1.0, scale=PiratesGuiGlobals.TextScaleLarge))
        self.colorChangeParallel = Parallel()
        self.showIval = Sequence(Parallel(LerpPosInterval(self, 0.3, pos=Point3(-0.47, 0, 0.52), blendType='easeOut'), LerpPosInterval(self.questComplete, 0.3, pos=Point3(-0.25, 0, 0.13), blendType='easeOut')), LerpScaleInterval(self.questComplete, 0.5, scale=PiratesGuiGlobals.TextScaleLarge, blendType='easeOut'), Wait(1.0))
        if self.showLevelUp:
            self.showIval.append(Func(self.showLevelUpAlert))
            self.showIval.append(Wait(2.0))
        if self.reputation:
            self.showIval.append(Func(self.showPanelAnimations))
            self.showIval.append(Func(self.showExpAlert))
        self.hideIval = LerpPosInterval(self, 0.3, pos=Point3(0.6, 0, 0.52), blendType='easeIn')

    def showPanel(self):
        self.showIval.start()

    def hidePanel(self):
        self.hideIval.start()

    def hidePanelAndDestroy(self):
        Sequence(self.hideIval, Wait(0.25), Func(self.destroy)).start()

    def showPanelAnimations(self):
        self.questCompleteScaleSeq.loop()
        if self.reputation and not self.gameGui.repMeter.mastered:
            if self.gameGui.repMeter.changeMeter.meterFaceHalf2.getColor() == self.gameGui.repMeter.changeMeter['meterColor2']:
                self.colorChangeParallel.append(Sequence(LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf2, 0.1, color=Vec4(1, 1, 1, 1)), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf2, 0.1, color=self.gameGui.repMeter.changeMeter['meterColor2']), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf2, 0.1, color=Vec4(1, 1, 1, 1)), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf2, 0.1, color=self.gameGui.repMeter.changeMeter['meterColor2']), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf2, 0.1, color=Vec4(1, 1, 1, 1)), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf2, 0.1, color=self.gameGui.repMeter.changeMeter['meterColor2']), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf2, 0.1, color=Vec4(1, 1, 1, 1)), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf2, 0.1, color=self.gameGui.repMeter.changeMeter['meterColor2']), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf2, 0.1, color=Vec4(1, 1, 1, 1)), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf2, 0.4, color=self.gameGui.repMeter.changeMeter['meterColor'])))
            if self.gameGui.repMeter.changeMeter.meterFaceHalf3.getColor() == self.gameGui.repMeter.changeMeter['meterColor2']:
                self.colorChangeParallel.append(Sequence(LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf3, 0.1, color=Vec4(1, 1, 1, 1)), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf3, 0.1, color=self.gameGui.repMeter.changeMeter['meterColor2']), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf3, 0.1, color=Vec4(1, 1, 1, 1)), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf3, 0.1, color=self.gameGui.repMeter.changeMeter['meterColor2']), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf3, 0.1, color=Vec4(1, 1, 1, 1)), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf3, 0.1, color=self.gameGui.repMeter.changeMeter['meterColor2']), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf3, 0.1, color=Vec4(1, 1, 1, 1)), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf3, 0.1, color=self.gameGui.repMeter.changeMeter['meterColor2']), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf3, 0.1, color=Vec4(1, 1, 1, 1)), Wait(0.2), LerpColorInterval(self.gameGui.repMeter.changeMeter.meterFaceHalf3, 0.4, color=self.gameGui.repMeter.changeMeter['meterColor'])))
            self.colorChangeParallel.start()

    def showLevelUpAlert(self):
        self.popupSfx.play()
        self.gameGui.createLevelUpAlert(4.0, Vec3(0.69, 0.0, -0.5), Vec3(0.0, 0.0, 0.25))

    def showExpAlert(self):
        self.popupSfx.play()
        self.gameGui.createExpAlert(self.reputation, 8.0, Vec3(0.69, 0.0, -0.5), Vec3(0.0, 0.0, 0.25))

    def setQuestInfoFromQuest(self, quest):
        questId = quest.getQuestId()
        questStrings = PLocalizer.QuestStrings.get(questId)
        if questStrings:
            title = questStrings.get('title', '\n')
        else:
            title = '\n'
        gold = self.rewards.get('gold', 0)
        text = PLocalizer.QuestItemGuiFormat % {'title': title}
        if gold or self.reputation or self.items:
            text += PLocalizer.QuestItemGuiAddRewards
        if self.items:
            text += PLocalizer.QuestItemGuiAddItems
        if self.reputation:
            text += PLocalizer.QuestItemGuiAddRep % {'rep': self.reputation}
        if gold:
            text += PLocalizer.QuestItemGuiAddGold % {'gold': gold}
        self['text'] = text
        self.gameGui = GameGui.GameGui(self, relief=None, state=DGG.DISABLED, scale=0.6, pos=(-0.45, 0, -0.12))
        self.gameGui.vitaeMeter.hide()
        self.gameGui.statusTray.hpLabel.hide()
        self.gameGui.statusTray.hpMeter.component('text0').hide()
        self.gameGui.statusTray.voodooLabel.hide()
        self.gameGui.statusTray.voodooMeter.component('text0').hide()
        self.gameGui.statusTray.updateHp(localAvatar.hp, localAvatar.maxHp)
        self.gameGui.statusTray.updateVoodoo(localAvatar.getTotalMojo(), localAvatar.maxMojo)
        self.gameGui.repMeter.updateChange(self.totalReputation, self.reputation)
        return