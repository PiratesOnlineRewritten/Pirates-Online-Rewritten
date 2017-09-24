import random
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShowBaseGlobal import *
from direct.interval.IntervalGlobal import *
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.pirate import HumanDNA
from pirates.pirate import Human
from CharGuiBase import CharGuiSlider, CharGuiPicker
from pirates.pirate import BodyDefs
import MakeAPirateGlobals

class BodyGUI(DirectFrame, StateData.StateData):
    maleShapeButtonIcons = []
    maleShapeButtonIconsOver = []
    femaleShapeButtonIcons = []
    femaleShapeButtonIconsOver = []
    notify = DirectNotifyGlobal.directNotify.newCategory('BodyGUI')
    bodyHeights = {}
    bodyHeights['m'] = Human.BodyScales[0]
    bodyHeights['f'] = Human.BodyScales[1]
    bodyHeights['n'] = Human.BodyScales[0]

    def __init__(self, main=None):
        self.main = main
        self._parent = main.bookModel
        self.avatar = main.avatar
        self.mode = None
        self.entered = False
        return

    def enter(self):
        self.notify.debug('enter')
        self.entered = True
        if self.mode == None:
            self.load()
            self.mode = -1
        self.show()
        return

    def exit(self):
        self.entered = False
        self.notify.debug('called bodyGUI exit')
        self.hide()

    def save(self):
        if self.mode == -1:
            pass

    def assignAvatar(self, avatar):
        self.avatar = avatar
        self.heightSlider.setValue(self.avatar.pirate.getStyle().getBodyHeight())

    def load(self):
        self.notify.debug('loading BodyGUI')
        self.loadShapeGUI()
        self.loadHeightGUI()
        self.loadColorGUI()
        self.setupButtons()

    def loadShapeGUI(self):
        self.maleShapeButtonIcons = [
         self.main.charGui.find('**/chargui_male_a'), self.main.charGui.find('**/chargui_male_b'), self.main.charGui.find('**/chargui_male_c'), self.main.charGui.find('**/chargui_male_d'), self.main.charGui.find('**/chargui_male_e')]
        self.maleShapeButtonIconsOver = [
         self.main.charGui.find('**/chargui_male_a_over'), self.main.charGui.find('**/chargui_male_b_over'), self.main.charGui.find('**/chargui_male_c_over'), self.main.charGui.find('**/chargui_male_d_over'), self.main.charGui.find('**/chargui_male_e_over')]
        self.femaleShapeButtonIcons = [
         self.main.charGui.find('**/chargui_female_a'), self.main.charGui.find('**/chargui_female_b'), self.main.charGui.find('**/chargui_female_c'), self.main.charGui.find('**/chargui_female_d'), self.main.charGui.find('**/chargui_female_e')]
        self.femaleShapeButtonIconsOver = [
         self.main.charGui.find('**/chargui_female_a_over'), self.main.charGui.find('**/chargui_female_b_over'), self.main.charGui.find('**/chargui_female_c_over'), self.main.charGui.find('**/chargui_female_d_over'), self.main.charGui.find('**/chargui_female_e_over')]
        self.shapeFrameTitle = DirectFrame(parent=self._parent, relief=None, text=PLocalizer.BodyShapeFrameTitle, text_fg=(1,
                                                                                                                          1,
                                                                                                                          1,
                                                                                                                          1), text_scale=0.18, text_pos=(0,
                                                                                                                                                         0), pos=(0, 0, -0.1), scale=0.7)
        self.shapeFrameTitle.hide()
        return

    def loadHeightGUI(self):
        self.heightSlider = CharGuiSlider(self.main, parent=self._parent, text=PLocalizer.BodyHeightFrameTitle, command=self.updateHeightSlider, range=(-0.2,
                                                                                                                                                       0.2))
        self.heightSlider.setPos(-0.3, 0, -0.7)
        self.heightSlider.setScale(0.7)
        self.heightSlider['extraArgs'] = [self.heightSlider, 0, 0]
        self.pgs = [self.heightSlider]

    def loadColorGUI(self):
        idx = 0
        self.maleColorFrameTitle = DirectFrame(parent=self._parent, relief=None, image=self.main.charGui.find('**/chargui_frame05'), image_pos=(0, 0, -0.6), image_scale=(1.5,
                                                                                                                                                                         1,
                                                                                                                                                                         1.25), text=PLocalizer.BodyColorFrameTitle, text_fg=(1,
                                                                                                                                                                                                                              1,
                                                                                                                                                                                                                              1,
                                                                                                                                                                                                                              1), text_scale=0.18, text_pos=(0, -0.04), pos=(0,
                                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                                             -1.0), scale=0.7)
        self.maleColorFrameTitle.hide()
        self.maleColorButtons = []
        xOffset = -0.4
        yOffset = -0.3
        whiteSkinTone = (1.0, 1.0, 1.0)
        for i in range(0, len(HumanDNA.skinColors)):
            if i and i % 5 == 0:
                xOffset = -0.4
                yOffset -= 0.2
            skinColor = HumanDNA.skinColors[i]
            skinTone = (skinColor[0] * whiteSkinTone[0], skinColor[1] * whiteSkinTone[1], skinColor[2] * whiteSkinTone[2], 1.0)
            self.maleColorButtons.append(DirectButton(parent=self.maleColorFrameTitle, relief=DGG.RAISED, pos=(xOffset, 0, yOffset), frameSize=(-0.1, 0.1, -0.1, 0.1), borderWidth=(0.008,
                                                                                                                                                                                    0.008), frameColor=skinTone, command=self.handleSetColor, extraArgs=[i]))
            xOffset += 0.2

        idx = 1
        self.femaleColorFrameTitle = DirectFrame(parent=self._parent, relief=None, image=self.main.charGui.find('**/chargui_frame05'), image_pos=(0, 0, -0.6), image_scale=(1.5,
                                                                                                                                                                           1,
                                                                                                                                                                           1.25), text=PLocalizer.BodyColorFrameTitle, text_fg=(1,
                                                                                                                                                                                                                                1,
                                                                                                                                                                                                                                1,
                                                                                                                                                                                                                                1), text_scale=0.18, text_pos=(0, -0.04), pos=(0,
                                                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                                                               -1.0), scale=0.7)
        self.femaleColorFrameTitle.hide()
        self.femaleColorButtons = []
        xOffset = -0.4
        yOffset = -0.3
        whiteSkinTone = (1.0, 1.0, 1.0)
        for i in range(0, len(HumanDNA.skinColors)):
            if i and i % 5 == 0:
                xOffset = -0.4
                yOffset -= 0.2
            skinColor = HumanDNA.skinColors[i]
            skinTone = (skinColor[0] * whiteSkinTone[0], skinColor[1] * whiteSkinTone[1], skinColor[2] * whiteSkinTone[2], 1.0)
            self.femaleColorButtons.append(DirectButton(parent=self.femaleColorFrameTitle, relief=DGG.RAISED, pos=(xOffset, 0, yOffset), frameSize=(-0.1, 0.1, -0.1, 0.1), borderWidth=(0.008,
                                                                                                                                                                                        0.008), frameColor=skinTone, command=self.handleSetColor, extraArgs=[i]))
            xOffset += 0.2

        return

    def unload(self):
        self.notify.debug('called bodyGUI unload')
        del self.main
        del self._parent
        del self.avatar

    def showShapeCollections(self):
        if self.entered:
            self.shapeFrameTitle.show()
            if self.main.pirate.style.body.shape in BodyDefs.BodyChoiceGenderDict[self.main.pirate.style.gender]:
                shapebuttonIndex = BodyDefs.BodyChoiceGenderDict[self.main.pirate.style.gender].index(self.main.pirate.style.body.shape)
            else:
                shapebuttonIndex = 2
            self.shapeButtons[shapebuttonIndex].setColor(1, 1, 0, 1)

    def showHeightCollections(self):
        if self.entered:
            self.heightSlider.show()

    def showColorCollections(self):
        if self.entered:
            if self.main.pirate.style.gender == 'f':
                self.femaleColorFrameTitle.show()
                self.femaleColorButtons[self.main.pirate.style.body.color]['relief'] = DGG.SUNKEN
            else:
                self.maleColorFrameTitle.show()
                self.maleColorButtons[self.main.pirate.style.body.color]['relief'] = DGG.SUNKEN

    def hideShapeCollections(self):
        self.shapeFrameTitle.hide()

    def hideHeightCollections(self):
        self.heightSlider.hide()

    def hideColorCollections(self):
        self.maleColorFrameTitle.hide()
        self.femaleColorFrameTitle.hide()

    def show(self):
        self.showShapeCollections()
        self.showHeightCollections()
        self.showColorCollections()

    def hide(self):
        self.hideShapeCollections()
        self.hideHeightCollections()
        self.hideColorCollections()

    def setupButtons(self):
        self.texturePicker = CharGuiPicker(self.main, parent=self._parent, text=PLocalizer.BodyHairFrameTitle, nextCommand=self.handleNextTexture, backCommand=self.handleLastTexture)
        self.texturePicker.setPos(0, 0, -1)
        self.texturePicker.hide()
        shapeButtonTexts = [
         PLocalizer.BodyShortFat, PLocalizer.BodyMediumSkinny, PLocalizer.BodyMediumIdeal, PLocalizer.BodyTallPear, PLocalizer.BodyTallMuscular]
        self.shapeButtons = []
        xOffset = -1.1
        yOffset = -0.4
        for i in range(0, len(self.maleShapeButtonIcons)):
            self.shapeButtons.append(DirectButton(parent=self.shapeFrameTitle, relief=None, geom=(self.maleShapeButtonIcons[i], self.maleShapeButtonIconsOver[i], self.maleShapeButtonIconsOver[i]), geom_scale=2, pos=(xOffset, 0, yOffset), command=self.handleShape, extraArgs=[i]))
            xOffset += 0.55

        return

    def restore(self, needToRefresh=True):
        self.heightSlider.node().setValue(self.main.pirate.style.body.height)
        findShape = BodyDefs.BodyChoiceGenderDict[self.main.pirate.style.gender].index(self.main.pirate.style.body.shape)
        self.handleShape(findShape, needToRefresh)
        self.hideColorCollections()
        self.showColorCollections()
        self.handleSetColor(self.main.pirate.style.body.color)
        self.toggleBodyShapes(self.main.pirate.style.gender)

    def reset(self):
        for i in xrange(0, len(self.pgs)):
            self.resetSlider(self.pgs[i])

        self.handleShape(2)
        self.handleSetColor(0)

    def resetSlider(self, slider):
        slider.node().setValue(0.0)
        self.updateHeightSlider(slider)

    def randomPick(self):
        for i in xrange(0, len(self.pgs)):
            slider = self.pgs[i]
            self.resetSlider(slider)
            if random.choice([0, 1]):
                value = random.random() * 0.1
                toss = 0
                if slider['range'][0] < 0:
                    toss = random.choice([0, 1])
                if toss:
                    slider.node().setValue(-value)
                else:
                    slider.node().setValue(value)
                self.updateHeightSlider(slider, slider['extraArgs'][1])

        cList = range(0, 5)
        bodyShapeIndex = BodyDefs.BodyChoiceGenderDict[self.main.pirate.style.gender].index(self.main.pirate.style.body.shape)
        cList.remove(bodyShapeIndex)
        choice = random.choice(cList)
        self.handleShape(choice)
        idx = 0
        if self.main.pirate.style.gender == 'f':
            idx = 1
        choice = random.choice(range(1, len(HumanDNA.skinColors)))
        self.handleSetColor(choice)

    def weightedRandomPick(self):
        for i in xrange(0, len(self.pgs)):
            slider = self.pgs[i]
            self.resetSlider(slider)
            if random.choice([0, 1]):
                value = random.random() * 0.1
                toss = 0
                if slider['range'][0] < 0:
                    toss = random.choice([0, 1, 2])
                if toss == 1:
                    slider.node().setValue(-value)
                elif toss == 0:
                    slider.node().setValue(value)
                elif toss == 2:
                    slider.node().setValue(0)
                self.updateHeightSlider(slider, slider['extraArgs'][1])

        if self.main.pirate.style.gender == 'f':
            bodyChoiceList = MakeAPirateGlobals.FEMALE_BODYTYPE_SELECTIONS
        else:
            bodyChoiceList = MakeAPirateGlobals.MALE_BODYTYPE_SELECTIONS
        bodyShapeIndex = BodyDefs.BodyChoiceGenderDict[self.main.pirate.style.gender].index(self.main.pirate.style.body.shape)
        choice = random.choice(bodyChoiceList)
        if choice == bodyShapeIndex:
            choice = random.choice(bodyChoiceList)
        self.handleShape(choice)
        colorSetChoice = random.choice(MakeAPirateGlobals.COMPLECTIONTYPES.keys())
        choice = random.choice(MakeAPirateGlobals.COMPLECTIONTYPES[colorSetChoice][0])
        self.handleSetColor(choice)

    def handleShape(self, index, needToRefresh=True):
        for i in range(0, len(self.shapeButtons)):
            self.shapeButtons[i].setColor(0.6, 0.8, 1.0, 1.0)

        bodyShapeIndex = BodyDefs.BodyChoiceGenderDict[self.main.pirate.style.gender][index]
        self.shapeButtons[index].setColor(1.0, 1.0, 0, 1.0)
        self.main.pirate.style.setBodyShape(bodyShapeIndex)
        self.updateHeightSlider(self.heightSlider, 0, 0)
        self.main.pirate.refreshBody()
        self.main.pirate.generateSkinTexture()
        if not self.main.isNPCEditor and not self.main.wantNPCViewer:
            self.main.pirate.loop('idle')
            if base.config.GetBool('want-idle-centered', 0):
                self.main.pirate.loop('idle_centered')
        else:
            self.main.refreshAnim(needToRefresh)
        self.main.setupCamera(self.main.pirate)
        if self.main.inRandomAll:
            return
        if hasattr(self.main, 'JSD_BODY'):
            optionsLeft = len(self.main.JSD_BODY[index])
            if optionsLeft and not random.randint(0, 4):
                choice = random.choice(range(0, optionsLeft))
                if self.main.lastDialog:
                    if self.main.lastDialog.status() == AudioSound.PLAYING:
                        return
                dialog = self.main.JSD_BODY[index][choice]
                base.playSfx(dialog, node=self.avatar.pirate)
                self.main.lastDialog = dialog
                if self.main.pirate.style.gender == 'm' and dialog == self.main.jsd_body_ms_1:
                    dialog.stop()
                elif self.main.pirate.style.gender == 'f' and dialog == self.main.jsd_body_tm_1:
                    dialog.stop()
                else:
                    self.main.JSD_BODY[index].remove(dialog)

    def handleSetColor(self, colorIdx):
        colorButtons = self.maleColorButtons
        if self.main.pirate.style.gender == 'f':
            colorButtons = self.femaleColorButtons
        for i in range(0, len(colorButtons)):
            colorButtons[i]['relief'] = DGG.RAISED

        colorButtons[colorIdx]['relief'] = DGG.SUNKEN
        self.avatar.skinColorIdx = colorIdx
        self.avatar.pirate.setBodyColor(self.avatar.skinColorIdx)
        self.avatar.pirate.generateSkinColor()

    def updateHeightSlider(self, pgs, extraArgs1=None, extraArgs2=None):
        value = pgs.node().getValue()
        self.avatar.pirate.setBodyHeight(value)
        self.avatar.pirate.setGlobalScale(self.avatar.pirate.calcBodyScale())

    def handleNextTexture(self):
        self.avatar.bodyTextureIdx = (self.avatar.bodyTextureIdx + 1) % self.avatar.numBodys
        self.avatar.pirate.setBodySkin(self.avatar.bodyTextureIdx)
        self.avatar.pirate.generateSkinTexture()

    def handleLastTexture(self):
        self.avatar.bodyTextureIdx = (self.avatar.bodyTextureIdx - 1) % self.avatar.numBodys
        self.avatar.pirate.setBodySkin(self.avatar.bodyTextureIdx)
        self.avatar.pirate.generateSkinTexture()

    def toggleBodyShapes(self, gender):
        if gender == 'f':
            self.notify.debug('gender is female')
            for i in range(0, len(self.femaleShapeButtonIcons)):
                self.shapeButtons[i]['geom'] = (
                 self.femaleShapeButtonIcons[i], self.femaleShapeButtonIconsOver[i], self.femaleShapeButtonIconsOver[i])

        else:
            self.notify.debug('gender is male')
            for i in range(0, len(self.maleShapeButtonIcons)):
                self.shapeButtons[i]['geom'] = (
                 self.maleShapeButtonIcons[i], self.maleShapeButtonIconsOver[i], self.maleShapeButtonIconsOver[i])
