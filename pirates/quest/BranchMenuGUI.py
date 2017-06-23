from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.distributed import InteractGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.quest import QuestConstants
from pirates.quest import QuestLadderDB
from pirates.quest import QuestOffer
import QuestDetailGUI
import QuestDB

class BranchMenuGUI(DirectFrame):

    def __init__(self, offer, callback=None, descriptionCallback=None):
        DirectFrame.__init__(self, relief=None, pos=(0.8, 0, -0.65))
        self.initialiseoptions(BranchMenuGUI)
        self.questButtons = []
        self.callback = callback
        self.descriptionCallback = descriptionCallback
        self.setOffers(offer)
        return

    def destroy(self):
        self.destroyQuestButtons()
        DirectFrame.destroy(self)

    def destroyQuestButtons(self):
        for questButton in self.questButtons:
            questButton.destroy()

        self.questButtons = []

    def setOffers(self, offer):
        offers = offer.getQuestDNA().getContainers()
        z = 1.0
        self.destroyQuestButtons()
        self.title = DirectLabel(parent=self, relief=None, text=PLocalizer.InteractChooseBranch, text_align=TextNode.ACenter, text_scale=0.07, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0, 0, z - 0.08), text_font=PiratesGlobals.getPirateOutlineFont())
        gui = loader.loadModel('models/gui/avatar_chooser_rope')
        topPanel = gui.find('**/avatar_c_A_top')
        topPanelOver = gui.find('**/avatar_c_A_top_over')
        middlePanel = gui.find('**/avatar_c_A_middle')
        middlePanelOver = gui.find('**/avatar_c_A_middle_over')
        bottomPanel = gui.find('**/avatar_c_A_bottom')
        bottomPanelOver = gui.find('**/avatar_c_A_bottom_over')
        for i, offer in zip(range(len(offers)), offers):
            if i == 0:
                image = (
                 topPanel, topPanel, topPanelOver, topPanel)
                textPos = (0, -0.02)
                z -= 0.19
            else:
                image = (
                 middlePanel, middlePanel, middlePanelOver, middlePanel)
                textPos = (0, -0.015)
                if i == 1:
                    z -= 0.11
                else:
                    z -= 0.105
            offerName = offer.getName()
            if PLocalizer.QuestStrings.has_key(offerName) and 'title' in PLocalizer.QuestStrings[offerName].keys():
                questTitle = PLocalizer.QuestStrings[offerName]['title']
            elif PLocalizer.QuestStrings.has_key(offer.questId) and 'title' in PLocalizer.QuestStrings[offer.questId].keys():
                questTitle = PLocalizer.QuestStrings[offer.questId]['title']
            else:
                questTitle = offer.getTitle()
            questButton = DirectButton(parent=self, relief=None, pressEffect=0, text=questTitle, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=textPos, textMayChange=0, image=image, image_scale=0.4, pos=(0, 0, z), command=self.seeQuestDetails, extraArgs=[offer])
            self.questButtons.append(questButton)

        z -= 0.155
        if self.callback:
            questButton = DirectButton(parent=self, relief=None, pressEffect=0, text=PLocalizer.lBack, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0,
                                                                                                                                                                                                                                                                        0.033), textMayChange=0, image=(bottomPanel, bottomPanel, bottomPanelOver, bottomPanel), image_scale=0.4, pos=(0, 0, z), command=self.callback, extraArgs=[QuestConstants.CANCEL_QUEST])
            self.questButtons.append(questButton)
        gui.removeNode()
        return

    def seeQuestDetails(self, offer):
        offer = QuestOffer.QuestOffer.create(offer.getName(), localAvatar)
        self.descriptionCallback(offer)

    def questDetailCallback(self, offer, acceptedQuest):
        self.detailGUI.destroy()
        del self.detailGUI
        self.show()
        if acceptedQuest:
            self.callback(offer)