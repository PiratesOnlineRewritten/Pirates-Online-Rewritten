from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShowBaseGlobal import *
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.pirate import HumanDNA
import random

class GenderGUI(DirectFrame, StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('GenderGUI')

    def __init__(self, main=None):
        self.main = main
        self.parent = main.bookModel
        self.avatar = main.avatar
        self.mode = None
        self.maleDNA = HumanDNA.HumanDNA('m')
        self.maleDNA.makeMakeAPirate()
        self.femaleDNA = HumanDNA.HumanDNA('f')
        self.femaleDNA.makeMakeAPirate()
        self.navyDNA = HumanDNA.HumanDNA('n')
        self.navyDNA.makeMakeAPirate()
        return

    def setGenderGuiState(self, gender):
        if gender == 0:
            self.genderMaleButton.setColor(1, 1, 0.5, 1)
            self.genderFemaleButton.setColor(1, 1, 1, 1)
        else:
            self.genderMaleButton.setColor(1, 1, 1, 1)
            self.genderFemaleButton.setColor(1, 1, 0.5, 1)

    def enter(self):
        self.notify.debug('enter')
        if self.mode == None:
            self.load()
            self.mode = -1
            self.setGenderGuiState(0)
        self.show()
        return

    def exit(self):
        self.notify.debug('called genderGUI exit')
        self.hide()

    def save(self):
        if self.mode == -1:
            pass

    def assignAvatar(self, avatar):
        self.avatar = avatar

    def load(self):
        self.notify.debug('loading GenderGUI')
        self.setupButtons()

    def unload(self):
        self.notify.debug('called genderGUI unload')
        del self.main
        del self.parent
        del self.avatar

    def show(self):
        self.genderFrameTitle.show()
        self.genderMaleButton.show()
        self.genderFemaleButton.show()

    def hide(self):
        self.genderFrameTitle.hide()
        self.genderMaleButton.hide()
        self.genderFemaleButton.hide()

    def setupButtons(self):
        self.genderFrameTitle = DirectFrame(parent=self.parent, relief=None, text=PLocalizer.GenderFrameTitle, text_scale=0.18, text_pos=(0,
                                                                                                                                          0), text_fg=(1,
                                                                                                                                                       1,
                                                                                                                                                       1,
                                                                                                                                                       1), pos=(0,
                                                                                                                                                                0,
                                                                                                                                                                0.4), scale=0.7)
        self.genderFrameTitle.hide()
        self.genderMaleButton = DirectButton(parent=self.genderFrameTitle, relief=None, pos=(-0.3, 0, -0.25), image=(self.main.charGui.find('**/chargui_male'), self.main.charGui.find('**/chargui_male_down'), self.main.charGui.find('**/chargui_male_over')), image_scale=1.8, command=self.handleMale)
        self.genderMaleButton.hide()
        self.genderFemaleButton = DirectButton(parent=self.genderFrameTitle, relief=None, pos=(0.3, 0, -0.25), image=(self.main.charGui.find('**/chargui_female'), self.main.charGui.find('**/chargui_female_down'), self.main.charGui.find('**/chargui_female_over')), image_scale=1.8, command=self.handleFemale)
        self.genderFemaleButton.hide()
        return

    def reset(self, index):
        if index:
            self.handleFemale()
        else:
            self.handleMale()

    def randomPick(self):
        choice = random.choice([0, 1])
        if choice:
            self.handleFemale()
        else:
            self.handleMale()

    def handleMale(self):
        if self.main.pirate.style.gender == 'f':
            self.femaleDNA = self.main.pirate.style
        elif self.main.pirate.style.gender == 'n':
            self.navyDNA = self.main.pirate.style
        self.main.pirate.style = self.maleDNA
        self.setGenderGuiState(0)
        self.main.refresh(wantClothingChange=True)
        self.main.refreshShuffleButtons()
        self.main.nameGui.enter()
        self.main.nameGui.exit()

    def handleFemale(self):
        if self.main.pirate.style.gender == 'm':
            self.maleDNA = self.main.pirate.style
        elif self.main.pirate.style.gender == 'n':
            self.navyDNA = self.main.pirate.style
        self.main.pirate.setDNA(self.femaleDNA)
        self.setGenderGuiState(1)
        self.main.refresh(wantClothingChange=True)
        self.main.refreshShuffleButtons()
        self.main.nameGui.enter()
        self.main.nameGui.exit()

    def handleNavy(self):
        if self.main.pirate.style.gender == 'm':
            self.maleDNA = self.main.pirate.style
        elif self.main.pirate.style.gender == 'f':
            self.femaleDNA = self.main.pirate.style
        self.main.pirate.style = self.navyDNA
        self.setGenderGuiState(1)
        self.main.bodyGui.restore()
        self.main.headGui.restore()