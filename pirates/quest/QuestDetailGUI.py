from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.distributed import InteractGlobals
from pirates.quest import QuestDB, QuestLadderDB, QuestReward
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.inventory import InventoryUIRewardsContainer

class QuestDetailBase(DirectFrame):

    def __init__(self, parent=aspect2d, pos=(0, 0, 0), *args, **kw):
        topGui = loader.loadModel('models/gui/toplevel_gui')
        questScroll = topGui.find('**/main_gui_quest_scroll')
        self.titleUnderline = topGui.find('**/pir_t_gui_but_quest')
        topGui.removeNode()
        optiondefs = (
         ('relief', None, None), ('pos', pos, None), ('image', questScroll, None), ('image_scale', VBase3(0.48, 0.48, 0.66), None), ('image_color', VBase4(0.9, 0.9, 0.9, 1), None), ('text', '', None), ('text_align', TextNode.ALeft, None), ('text_fg', PiratesGuiGlobals.TextFG0, None), ('text_scale', PiratesGuiGlobals.TextScaleLarge, None), ('text_pos', (-0.45, 0.215), None), ('text_shadow', (1, 1, 1, 0.01), None), ('text_wordwrap', 23, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent=parent, *args, **kw)
        self.initialiseoptions(QuestDetailBase)
        return


class QuestDetailGUI(QuestDetailBase):

    def __init__(self, offer=None, callback=None, quest=None, parent=base.a2dBottomRight, pos=(0.6, 0, 0.52)):
        self.width = 1
        QuestDetailBase.__init__(self, parent=parent, pos=pos)
        self.callback = callback
        self.initialiseoptions(QuestDetailGUI)
        self.rewardsContainer = None
        self.setupTitleLabel()
        if offer:
            self.setQuestInfoFromOffer(offer)
        else:
            self.setQuestInfoFromQuest(quest)
        self.buildIvals()
        return

    def destroy(self):
        self.showIval.pause()
        self.showIval = None
        self.hideIval.pause()
        self.hideIval = None
        if self.rewardsContainer:
            self.rewardsContainer.destroy()
        self.rewardsContainer = None
        QuestDetailBase.destroy(self)
        return

    def setupTitleLabel(self):
        self.titleUnderline.setColorScale(0.8, 0.2, 0.05, 0.8)
        self.titleUnderline.setScale(1.5, 0.05, 0.05)
        self.titleUnderline.setPos(0, 0, 0.2)
        self.titleUnderline.reparentTo(self)
        self.titleLabel = DirectLabel(parent=self, pos=(0, 0, 0.218), text='', text_scale=0.041, text_shadow=(0,
                                                                                                              0,
                                                                                                              0,
                                                                                                              1), text_align=TextNode.ACenter, text_wordwrap=24.0, textMayChange=1)

    def buildIvals(self):
        self.showIval = LerpPosInterval(self, 0.3, pos=Point3(-0.47, 0, 0.52), blendType='easeOut')
        self.hideIval = LerpPosInterval(self, 0.3, pos=Point3(0.6, 0, 0.52), blendType='easeIn')

    def showPanel(self):
        self.showIval.start()

    def hidePanel(self):
        self.hideIval.start()

    def hidePanelAndDestroy(self):
        Sequence(self.hideIval, Wait(0.25), Func(self.destroy)).start()

    def setItemRewards(self, rewards):
        if self.rewardsContainer:
            self.rewardsContainer.destroy()
            self.rewardsContainer = None
        itemRewards = []
        for reward in rewards:
            if reward.getItemId():
                itemRewards.append(reward.getItemId())

        if itemRewards and hasattr(localAvatar, 'guiMgr'):
            scale = 0.1 * len(itemRewards)
            self.rewardsContainer = InventoryUIRewardsContainer.InventoryUIRewardsContainer(localAvatar.guiMgr.inventoryUIManager, sizeX=scale, sizeZ=scale, countX=len(itemRewards), countZ=1)
            self.rewardsContainer.setPos(0.05, 0, -0.25 - 0.06 * len(itemRewards))
            self.rewardsContainer.reparentTo(self)
            for itemId in itemRewards:
                self.rewardsContainer.addRewardIntoGrid(itemId, itemRewards.index(itemId), 0)

        return

    @exceptionLogged()
    def setQuestInfoFromOffer(self, offer):
        questId = offer.getQuestId()
        questStrings = PLocalizer.QuestStrings.get(questId, {})
        title = questStrings.get('title', '\n')
        story = questStrings.get('description', '\n')
        timeLimit = 0
        containerDNA = None
        if offer.isLadder():
            containerDNA = QuestLadderDB.getContainer(questId)
            if containerDNA:
                status = ''
                if containerDNA.isChoice():
                    for container in containerDNA.getContainers():
                        status += container.getDescriptionText() + '\n'

                    status = status[0:-1]
                else:
                    status = containerDNA.getDescriptionText()
        else:
            containerDNA = QuestDB.QuestDict[questId]
            status = containerDNA.getDescriptionText(offer.initialTaskStates)
            statusBonus = containerDNA.getDescriptionText(offer.initialTaskStates, bonus=True)
            if statusBonus:
                status += PLocalizer.QuestStatusTaskBonus + statusBonus
            timeLimit = containerDNA.getTimeLimit()
        reward = ''
        if containerDNA:
            reward = QuestReward.QuestReward.getDescriptionText(containerDNA.getRewards())
        self.titleUnderline.show()
        self.titleLabel['text'] = PLocalizer.QuestItemGuiTitle % {'title': title}
        questText = '\n\n'
        questText += PLocalizer.QuestItemGuiTask % {'status': status}
        questText += PLocalizer.QuestItemGuiDescription % {'desc': story}
        if len(reward):
            questText += PLocalizer.QuestItemGuiRewards % {'reward': reward}
        self.setItemRewards(containerDNA.getRewards())
        self['text'] = questText
        return

    def setQuestInfoFromQuest(self, quest):
        if not quest:
            return
        questId = quest.getQuestId()
        taskStates = getattr(quest, 'taskStates', None)
        if not taskStates:
            taskStates = QuestDB.QuestDict[questId].getInitialTaskStates(localAvatar)
        questStrings = PLocalizer.QuestStrings.get(questId, {})
        title = questStrings.get('title', '\n')
        story = questStrings.get('description', '\n')
        status = quest.getStatusText()
        returnTo = quest.getReturnText()
        timeLimit = quest.getTimeLimit()
        reward = quest.getRewardText()
        self.titleUnderline.show()
        self.titleLabel['text'] = PLocalizer.QuestItemGuiTitle % {'title': title}
        questText = '\n\n'
        questText += PLocalizer.QuestItemGuiTask % {'status': status}
        if quest.isComplete():
            questText += PLocalizer.QuestItemGuiReturnTo % {'returnTo': returnTo}
        else:
            questText += PLocalizer.QuestItemGuiDescription % {'desc': story}
        if len(reward):
            questText += PLocalizer.QuestItemGuiRewards % {'reward': reward}
        self.setItemRewards(quest.getRewards())
        self['text'] = questText
        return

    def setQuestInfoFromQuestId(self, questId):
        questStrings = PLocalizer.QuestStrings.get(questId, {})
        title = questStrings.get('title', '\n')
        story = questStrings.get('description', '\n')
        reward = questStrings.get('reward', '')
        self.titleUnderline.show()
        self.titleLabel['text'] = PLocalizer.QuestItemGuiTitle % {'title': title}
        questText = '\n\n'
        questText += PLocalizer.QuestItemGuiDescription % {'desc': story}
        if len(reward):
            questText += PLocalizer.QuestItemGuiRewards % {'reward': reward}
        self['text'] = questText
        self.setItemRewards([])

    def setQuestTitleOnly(self, questId):
        questStrings = PLocalizer.QuestStrings.get(questId, {})
        title = questStrings.get('title', '\n')
        self.titleUnderline.show()
        self.titleLabel['text'] = PLocalizer.QuestItemGuiTitle % {'title': title}
        self['text'] = '\n\n'
        self.setItemRewards([])

    def clearQuestDetails(self):
        self['text'] = ''
        self.titleLabel['text'] = ''
        self.titleUnderline.hide()

    def hasQuestDetails(self):
        return self['text'] != ''