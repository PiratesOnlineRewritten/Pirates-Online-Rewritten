from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShowBaseGlobal import *
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.pirate import HumanDNA
from CharGuiBase import CharGuiSlider, CharGuiPicker
import MakeAPirateGlobals
import random

class HairGUI(DirectFrame, StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('HairGUI')

    def __init__(self, main=None):
        self.main = main
        self._parent = main.bookModel
        self.avatar = main.avatar
        self.mode = None
        self.load()
        return

    def enter(self):
        self.notify.debug('enter')
        self.showHairCollections()
        self.showColorCollections()
        if self.mode == None:
            self.mode = -1
        return

    def exit(self):
        self.notify.debug('called HairGUI exit')
        self.hide()
        self.mode = None
        return

    def save(self):
        if self.mode == -1:
            pass

    def assignAvatar(self, avatar):
        self.avatar = avatar

    def load(self):
        self.notify.debug('loading HairGui')
        self.loadGUI()
        self.loadColorGUI()

    def loadGUI(self):
        self.hairPicker = CharGuiPicker(self.main, parent=self._parent, text=PLocalizer.MakeAPirateHairHair, nextCommand=self.handleNextHair, backCommand=self.handleLastHair)
        self.hairPicker.setPos(0, 0, 0.1)
        self.beardPicker = CharGuiPicker(self.main, parent=self._parent, text=PLocalizer.MakeAPirateHairBeard, nextCommand=self.handleNextBeard, backCommand=self.handleLastBeard)
        self.beardPicker.setPos(0, 0, -0.1)
        self.mustachePicker = CharGuiPicker(self.main, parent=self._parent, text=PLocalizer.MakeAPirateHairMustache, nextCommand=self.handleNextMustache, backCommand=self.handleLastMustache)
        self.mustachePicker.setPos(0, 0, -0.3)
        self.eyeBrowPicker = CharGuiPicker(self.main, parent=self._parent, text=PLocalizer.MakeAPirateHairEyeBrow, nextCommand=self.handleNextEyeBrow, backCommand=self.handleLastEyeBrow)
        self.eyeBrowPicker.setPos(0, 0, -0.5)
        self.hairPicker.hide()
        self.beardPicker.hide()
        self.mustachePicker.hide()
        self.eyeBrowPicker.hide()

    def loadColorGUI(self):
        self.baseColorFrameTitle = DirectFrame(parent=self._parent, relief=None, image=self.main.charGui.find('**/chargui_frame01'), image_pos=(0, 0, -0.3), image_scale=(2.13,
                                                                                                                                                                         1.6,
                                                                                                                                                                         1.6), text=PLocalizer.HairColorFrameTitle, text_fg=(1,
                                                                                                                                                                                                                             1,
                                                                                                                                                                                                                             1,
                                                                                                                                                                                                                             1), text_scale=0.18, text_pos=(0, -0.05), pos=(0, 0, -0.6), scale=0.7)
        self.baseColorFrameTitle.hide()
        self.baseColorButtons = []
        xOffset = -0.7
        yOffset = -0.3
        for i in HumanDNA.availableHairColors:
            if i and i % 8 == 0:
                xOffset = -0.5
                yOffset -= 0.3
            hairColor = HumanDNA.hairColors[i]
            hairTone = (hairColor[0], hairColor[1], hairColor[2], 1.0)
            self.baseColorButtons.append(DirectButton(parent=self.baseColorFrameTitle, relief=DGG.RAISED, pos=(xOffset, 0, yOffset), frameSize=(-0.1, 0.1, -0.1, 0.1), borderWidth=(0.008,
                                                                                                                                                                                    0.008), frameColor=hairTone, command=self.handleSetBaseColor, extraArgs=[i]))
            xOffset += 0.2

        return

    def unload(self):
        self.notify.debug('called HairGui unload')
        del self.main
        del self._parent
        del self.avatar

    def showHairCollections(self):
        self.hairPicker.show()
        if self.main.pirate.style.gender == 'f':
            self.beardPicker.hide()
            self.mustachePicker.hide()
        else:
            self.beardPicker.show()
            self.mustachePicker.show()

    def hideHairCollections(self):
        self.hairPicker.hide()
        self.beardPicker.hide()
        self.mustachePicker.hide()

    def showColorCollections(self):
        self.baseColorFrameTitle.show()
        self.baseColorButtons[self.main.pirate.style.head.hair.color]['relief'] = DGG.SUNKEN

    def hideColorCollections(self):
        self.baseColorFrameTitle.hide()

    def hide(self):
        self.hideHairCollections()
        self.hideColorCollections()

    def reset(self):
        self.avatar.hideHair()
        self.avatar.hairIdx = 0
        self.avatar.pirate.setHairHair(0)
        self.avatar.pirate.setHairColor(0)
        self.avatar.handleHeadHiding()
        if self.main.pirate.style.gender == 'm':
            self.avatar.beardIdx = 0
            self.avatar.pirate.setHairBeard(0)
            self.avatar.mustacheIdx = 0
            self.avatar.pirate.setHairMustache(0)
            self.avatar.showFacialHair()

    def randomPick(self):
        self.avatar.hairIdx = random.choice(self.avatar.choices['HAIR'])
        self.avatar.pirate.setHairHair(self.avatar.hairIdx)
        choice = random.choice(HumanDNA.availableHairColors)
        for i in range(0, len(self.baseColorButtons)):
            self.baseColorButtons[i]['relief'] = DGG.RAISED

        self.baseColorButtons[choice]['relief'] = DGG.SUNKEN
        self.avatar.hairColorIdx = choice
        self.avatar.pirate.setHairColor(choice)
        self.avatar.handleHeadHiding()
        if self.main.pirate.style.gender == 'm':
            roll = int(random.random() * 10.0)
            for i in range(roll):
                self.handleNextBeard()

            if choice == 0 or choice > 3:
                roll = int(random.random() * 10.0)
                for i in range(roll):
                    self.handleNextMustache()

            self.avatar.showFacialHair()

    def weightedRandomPick(self):
        if self.main.pirate.style.gender == 'm':
            self.avatar.hairIdx = random.choice(self.avatar.choices['HAIR'] + MakeAPirateGlobals.PREFERRED_MALE_HAIR_SELECTIONS)
        else:
            self.avatar.hairIdx = random.choice(self.avatar.choices['HAIR'] + MakeAPirateGlobals.PREFERRED_FEMALE_HAIR_SELECTIONS)
        self.avatar.pirate.setHairHair(self.avatar.hairIdx)
        colorSkew = []
        for key in MakeAPirateGlobals.COMPLECTIONTYPES:
            entrySkin = MakeAPirateGlobals.COMPLECTIONTYPES[key][0]
            if self.avatar.dna.getBodyColor() in entrySkin:
                colorSkew = MakeAPirateGlobals.COMPLECTIONTYPES[key][1]

        coinFlip = random.choice([0, 1])
        if coinFlip:
            choice = random.choice(colorSkew)
        else:
            choice = random.choice(HumanDNA.availableHairColors + colorSkew)
        for i in range(0, len(self.baseColorButtons)):
            self.baseColorButtons[i]['relief'] = DGG.RAISED

        self.baseColorButtons[choice]['relief'] = DGG.SUNKEN
        self.avatar.hairColorIdx = choice
        self.avatar.pirate.setHairColor(choice)
        self.avatar.handleHeadHiding()
        if self.main.pirate.style.gender == 'm':
            choice = random.choice(self.avatar.choices['BEARD'] + MakeAPirateGlobals.PREFERRED_MALE_BEARD_SELECTIONS)
            self.avatar.beardIdx = choice
            self.avatar.pirate.setHairBeard(choice)
            if choice == 0 or choice > 3:
                roll = int(random.random() * 10.0)
                for i in range(roll):
                    self.handleNextMustache()

            self.avatar.showFacialHair()

    def handleNextHair(self):
        self.notify.debug('--------------------------current hair---------------------')
        self.avatar.hideHair()
        currIdx = self.avatar.choices['HAIR'].index(self.avatar.hairIdx)
        currIdx += 1
        if currIdx >= len(self.avatar.choices['HAIR']):
            currIdx = 0
        self.avatar.hairIdx = self.avatar.choices['HAIR'][currIdx]
        self.avatar.pirate.setHairHair(self.avatar.hairIdx)
        self.avatar.handleHeadHiding()
        self.playJackDialog()

    def handleLastHair(self):
        self.notify.debug('--------------------------current hair---------------------')
        self.avatar.hideHair()
        currIdx = self.avatar.choices['HAIR'].index(self.avatar.hairIdx)
        currIdx -= 1
        if currIdx < 0:
            currIdx = len(self.avatar.choices['HAIR']) - 1
        self.avatar.hairIdx = self.avatar.choices['HAIR'][currIdx]
        self.avatar.pirate.setHairHair(self.avatar.hairIdx)
        self.avatar.handleHeadHiding()
        self.playJackDialog()

    def handleNextBeard(self):
        if self.main.wantNPCViewer:
            self.avatar.beardIdx += 1
            if self.avatar.beardIdx >= len(self.avatar.beards):
                self.avatar.beardIdx = 0
        else:
            currIdx = self.avatar.choices['BEARD'].index(self.avatar.beardIdx)
            currIdx += 1
            if currIdx >= len(self.avatar.choices['BEARD']):
                currIdx = 0
            self.avatar.beardIdx = self.avatar.choices['BEARD'][currIdx]
        self.avatar.showFacialHair()
        self.avatar.pirate.setHairBeard(self.avatar.beardIdx)

    def handleLastBeard(self):
        if self.main.wantNPCViewer:
            self.avatar.beardIdx -= 1
            if self.avatar.beardIdx < 0:
                self.avatar.beardIdx = len(self.avatar.beards) - 1
        else:
            currIdx = self.avatar.choices['BEARD'].index(self.avatar.beardIdx)
            currIdx -= 1
            if currIdx < 0:
                currIdx = len(self.avatar.choices['BEARD']) - 1
            self.avatar.beardIdx = self.avatar.choices['BEARD'][currIdx]
        self.avatar.showFacialHair()
        self.avatar.pirate.setHairBeard(self.avatar.beardIdx)

    def handleNextMustache(self):
        if self.main.wantNPCViewer:
            self.avatar.mustacheIdx += 1
            if self.avatar.mustacheIdx >= len(self.avatar.mustaches):
                self.avatar.mustacheIdx = 0
        else:
            currIdx = self.avatar.choices['MUSTACHE'].index(self.avatar.mustacheIdx)
            currIdx += 1
            if currIdx >= len(self.avatar.choices['MUSTACHE']):
                currIdx = 0
            self.avatar.mustacheIdx = self.avatar.choices['MUSTACHE'][currIdx]
        self.avatar.showFacialHair()
        self.avatar.pirate.setHairMustache(self.avatar.mustacheIdx)

    def handleLastMustache(self):
        if self.main.wantNPCViewer:
            self.avatar.mustacheIdx -= 1
            if self.avatar.mustacheIdx < 0:
                self.avatar.mustacheIdx = len(self.avatar.mustaches) - 1
        else:
            currIdx = self.avatar.choices['MUSTACHE'].index(self.avatar.mustacheIdx)
            currIdx -= 1
            if currIdx < 0:
                currIdx = len(self.avatar.choices['MUSTACHE']) - 1
            self.avatar.mustacheIdx = self.avatar.choices['MUSTACHE'][currIdx]
        self.avatar.showFacialHair()
        self.avatar.pirate.setHairMustache(self.avatar.mustacheIdx)

    def handleNextEyeBrow(self):
        if not self.avatar.eyeBrows[self.avatar.eyeBrowIdx].isEmpty():
            self.avatar.eyeBrows[self.avatar.eyeBrowIdx].hide()
        self.avatar.eyeBrowIdx += 1
        if self.avatar.eyeBrowIdx >= len(self.avatar.eyeBrows):
            self.avatar.eyeBrowIdx = 0
        if not self.avatar.eyeBrows[self.avatar.eyeBrowIdx].isEmpty():
            self.avatar.eyeBrows[self.avatar.eyeBrowIdx].show()

    def handleLastEyeBrow(self):
        if not self.avatar.eyeBrows[self.avatar.eyeBrowIdx].isEmpty():
            self.avatar.eyeBrows[self.avatar.eyeBrowIdx].hide()
        self.avatar.eyeBrowIdx -= 1
        if self.avatar.eyeBrowIdx < 0:
            self.avatar.eyeBrowIdx = len(self.avatar.eyeBrows) - 1
        if not self.avatar.eyeBrows[self.avatar.eyeBrowIdx].isEmpty():
            self.avatar.eyeBrows[self.avatar.eyeBrowIdx].show()

    def handleSetBaseColor(self, colorIdx):
        for i in range(0, len(self.baseColorButtons)):
            self.baseColorButtons[i]['relief'] = DGG.RAISED

        self.baseColorButtons[colorIdx]['relief'] = DGG.SUNKEN
        self.avatar.hairColorIdx = colorIdx
        self.avatar.pirate.setHairColor(self.avatar.hairColorIdx)
        self.avatar.setHairBaseColor()

    def playJackDialog(self):
        if self.main.inRandomAll:
            return
        choice = random.choice([0, 1, 2])
        if choice != 0:
            return
        idx = 0
        if self.main.pirate.gender == 'f':
            idx = 1
        optionsLeft = len(self.main.JSD_HAIR[idx])
        if optionsLeft:
            if self.main.lastDialog:
                self.main.lastDialog.stop()
            choice = random.choice(range(0, optionsLeft))
            dialog = self.main.JSD_HAIR[idx][choice]
            base.playSfx(dialog, node=self.avatar.pirate)
            self.main.lastDialog = dialog
            self.main.JSD_HAIR[idx].remove(dialog)
