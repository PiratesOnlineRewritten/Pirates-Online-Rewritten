from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesbase import PLocalizer
from pirates.quest.QuestConstants import NPCIds
from pirates.quest import QuestLadderDB
from direct.directnotify import DirectNotifyGlobal

class BlackPearlCrew(DirectFrame):
    crewData = [{'uniqueId': NPCIds.HENDRY_CUTTS,'image': 'crew_3_HendryCutts','ladder': 'c3r2r3Cutts'}, {'uniqueId': NPCIds.CARVER,'image': 'crew_1_CarverPidgeley','ladder': 'c3r2r1Carver'}, {'uniqueId': NPCIds.LE_CERDO,'image': 'crew_5_LeCerdo','ladder': 'c3r2r5Grog'}, {'uniqueId': NPCIds.GUNNER,'image': 'crew_6_Gunner','ladder': 'c3r3r1Gunner'}, {'uniqueId': NPCIds.GORDON_GREER,'image': 'crew_2_GordenGreer','ladder': 'c3r2r2Greer'}, {'uniqueId': NPCIds.JOHN_SMITH,'image': 'crew_9_JohnSmith','ladder': 'c3r3r4Smith'}, {'uniqueId': NPCIds.NILL_OFFRILL,'image': 'crew_4_NillOffrill','ladder': 'c3r2r4Offrill'}, {'uniqueId': NPCIds.SCARY_MARY,'image': 'crew_7_ScaryMary','ladder': 'c3r3r2Mary'}, {'uniqueId': NPCIds.GILADOGA,'image': 'crew_8_Giladoga','ladder': 'c3r3r3Giladoga'}]

    def __init__(self):
        DirectFrame.__init__(self, relief=None)
        self.crewButtons = {}
        self.crewQuestInts = {}
        imagePos = (-0.45, 0.0, -0.3)
        self.images = loader.loadModel('models/gui/gui_bpcrew')
        for crewMember in self.crewData:
            uniqueId = crewMember.get('uniqueId')
            memberImage = self.images.find('**/' + crewMember.get('image'))
            containerName = crewMember.get('ladder')
            container = QuestLadderDB.getContainer(containerName)
            self.crewQuestInts[uniqueId] = QuestLadderDB.getAllParentQuestInts(container)
            self.crewButtons[uniqueId] = GuiButton(parent=self, pos=imagePos, state=DGG.DISABLED, image=memberImage, image_scale=0.18, geom_pos=imagePos)

        self.accept('clientLogout', self.destroy)
        return

    def destroy(self):
        DirectFrame.destroy(self)

    def update(self):
        for crewMemberId in self.crewButtons.keys():
            self.updateCrewMember(crewMemberId)

    def updateCrewMember(self, uniqueId):
        if self.hasCrewMember(uniqueId):
            self.crewButtons[uniqueId].setColorScale(1, 1, 1, 1)
        else:
            self.crewButtons[uniqueId].setColorScale(0, 0, 0, 1)

    def hasCrewMember(self, uniqueId):
        questLadderHistory = set(localAvatar.getQuestLadderHistory())
        questInts = set(self.crewQuestInts.get(uniqueId))
        return len(questInts.intersection(questLadderHistory))