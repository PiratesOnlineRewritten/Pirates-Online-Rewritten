from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShowBaseGlobal import *
from direct.showbase.PythonUtil import Functor
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from direct.task import Task
from pandac.PandaModules import *
from pirates.makeapirate import ClothingGlobals
from pirates.piratesbase import PLocalizer
from pirates.pirate import HumanDNA
from CharGuiBase import CharGuiSlider, CharGuiPicker
from pirates.inventory import ItemGlobals
from pirates.inventory.ItemConstants import DYE_COLORS
import random
genderIdx = 0
TOPNUMCOLOR = 6
BOTNUMCOLOR = 6
MALE_HAT_COLOR_SELECTIONS = [
 0, 1, 2, 3, 4, 5, 6]
MALE_COAT_COLOR_SELECTIONS = [0, 1, 2, 3, 4, 5, 6]
MALE_VEST_COLOR_SELECTIONS = [0, 1, 2, 3, 4, 5, 6]
MALE_SHIRT_COLOR_SELECTIONS = [0, 1, 2, 3, 4, 5, 6]
MALE_BELT_COLOR_SELECTIONS = [0, 1, 2, 3, 4, 5, 6]
MALE_PANTS_COLOR_SELECTIONS = [0, 1, 2, 3, 4, 5, 6]
MALE_SHOE_COLOR_SELECTIONS = [0, 1, 2, 3, 4, 5, 6]
FEMALE_HAT_COLOR_SELECTIONS = [
 0, 1, 2, 3, 4, 5, 6]
FEMALE_COAT_COLOR_SELECTIONS = [0, 1, 2, 3, 4, 5, 6]
FEMALE_VEST_COLOR_SELECTIONS = [0, 1, 2, 3, 4, 5, 6]
FEMALE_SHIRT_COLOR_SELECTIONS = [0, 1, 2, 3, 4, 5, 6]
FEMALE_BELT_COLOR_SELECTIONS = [0, 1, 2, 3, 4, 5, 6]
FEMALE_PANTS_COLOR_SELECTIONS = [0, 1, 2, 3, 4, 5, 6]
FEMALE_SHOE_COLOR_SELECTIONS = [0, 1, 2, 3, 4, 5, 6]
NPC_COLOR_SELECTIONS = [
 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
HAT = 0
SHIRT = 1
VEST = 2
COAT = 3
PANT = 4
BELT = 5
SOCK = 6
SHOE = 7

class ClothesGUI(DirectFrame, StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('ClothesGUI')

    def __init__(self, main=None):
        self.main = main
        self._parent = main.bookModel
        self.avatar = main.avatar
        self.mode = None
        self.entered = False
        self.once = False
        self.load()
        self.texName = ''
        self.lastRun = 0
        return

    def enter(self):
        self.entered = True
        if self.mode == None:
            self.mode = -1
        self.handleClothingChanged()
        self.show()
        return

    def exit(self):
        self.entered = False
        self.hide()

    def save(self):
        if self.mode == -1:
            pass

    def assignAvatar(self, avatar, wantClothingChange):
        global genderIdx
        self.avatar = avatar
        genderIdx = 0
        if avatar.dna.getGender() == 'f':
            genderIdx = 1
        if wantClothingChange:
            if self.avatar.dna.getGender() == 'm':
                self.avatar.currentClothing = ItemGlobals.getDefaultMaleClothing()
            else:
                self.avatar.currentClothing = ItemGlobals.getDefaultFemaleClothing()
        self.handleClothingChanged()

    def load(self):
        self.loadShirtGUI()
        self.loadPantGUI()
        self.loadShoeGUI()
        if self.main.wantNPCViewer:
            self.loadHatGUI()

    def loadShirtGUI(self):
        self.clothesFrame = DirectFrame(parent=self._parent, relief=None, pos=(0, 0,
                                                                              0), scale=1)
        self.clothesFrame.hide()
        self.genPicsButtonsFrame = DirectFrame(parent=self.clothesFrame, relief=None, pos=(0,
                                                                                           0,
                                                                                           0), scale=1.0)
        if not base.config.GetBool('want-gen-pics-buttons', 0):
            self.genPicsButtonsFrame.hide()
        self.shirtPicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingShirtStyle, nextCommand=Functor(self.handleNextClothing, 'SHIRT'), backCommand=Functor(self.handleLastClothing, 'SHIRT'))
        self.shirtPicker.setPos(-0.3, 0, 0.1)
        self.shirtGenPics = DirectButton(parent=self.genPicsButtonsFrame, relief=DGG.RAISED, frameSize=(-0.17, 0.17, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                                0.008), text=PLocalizer.GeneratePictures, text_pos=(0, -0.015), text_scale=0.08, pos=(-1,
                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                      0.1), command=self.handleShirtGenPics)
        self.vestPicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingVestStyle, nextCommand=Functor(self.handleNextClothing, 'VEST'), backCommand=Functor(self.handleLastClothing, 'VEST'))
        self.vestPicker.setPos(-0.3, 0, -0.3)
        self.vestGenPics = DirectButton(parent=self.genPicsButtonsFrame, relief=DGG.RAISED, frameSize=(-0.17, 0.17, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                               0.008), text=PLocalizer.GeneratePictures, text_pos=(0, -0.015), text_scale=0.08, pos=(-1, 0, -0.3), command=self.handleVestGenPics)
        if self.main.wantNPCViewer:
            self.coatPicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingCoatStyle, nextCommand=Functor(self.handleNextClothing, 'COAT'), backCommand=Functor(self.handleLastClothing, 'COAT'))
            self.coatPicker.setPos(-0.3, 0, -0.7)
            self.coatGenPics = DirectButton(parent=self.genPicsButtonsFrame, relief=DGG.RAISED, frameSize=(-0.17, 0.17, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                                   0.008), text=PLocalizer.GeneratePictures, text_pos=(0, -0.015), text_scale=0.08, pos=(-1, 0, -0.7), command=self.handleCoatGenPics)
        self.loadTopColorGUI()
        if self.main.wantNPCViewer:
            self.loadTopTextureGUI()
        return

    def makeColorSelector(self, frame, colors, xOffset, yOffset, selectCommand):
        if self.main.wantNPCViewer:
            colors = NPC_COLOR_SELECTIONS
        colorButtons = []
        colorCount = 0
        for colorId in colors:
            if colorCount and colorCount % 7 == 0:
                xOffset = 0.0
                yOffset -= 0.1
            clothesColor = DYE_COLORS[colorId]
            clothesTone = (clothesColor[0], clothesColor[1], clothesColor[2], 1.0)
            newColorButton = DirectButton(parent=frame, relief=DGG.RAISED, pos=(xOffset, 0, yOffset), frameSize=(-0.1, 0.1, -0.1, 0.1), borderWidth=(0.008,
                                                                                                                                                     0.008), frameColor=clothesTone, scale=0.5, command=selectCommand, extraArgs=[colorId])
            newColorButton.colorIndex = colorCount
            newColorButton.colorId = colorId
            colorButtons.append(newColorButton)
            colorCount += 1
            xOffset += 0.1

        return colorButtons

    def loadHatGUI(self):
        self.maleHatColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame01'), image_scale=(0.9,
                                                                                                                                                          1,
                                                                                                                                                          1.0), image_pos=(0.3, 0, -0.0), scale=0.8, pos=(0.35,
                                                                                                                                                                                                          0,
                                                                                                                                                                                                          0.55))
        self.femaleHatColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame01'), image_scale=(0.9,
                                                                                                                                                            1,
                                                                                                                                                            1.0), image_pos=(0.3, 0, -0.0), scale=0.8, pos=(0.35,
                                                                                                                                                                                                            0,
                                                                                                                                                                                                            0.55))
        self.hatPicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingHatStyle, nextCommand=Functor(self.handleNextClothing, 'HAT'), backCommand=Functor(self.handleLastClothing, 'HAT'))
        self.hatPicker.setPos(-0.3, 0.0, 0.4)
        self.hatGenPics = DirectButton(parent=self.genPicsButtonsFrame, relief=DGG.RAISED, frameSize=(-0.17, 0.17, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                              0.008), text=PLocalizer.GeneratePictures, text_pos=(0, -0.015), text_scale=0.08, pos=(-1,
                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                    0.4), command=self.handleHatGenPics)
        self.maleHatColorButtons = self.makeColorSelector(self.maleHatColorFrameTitle, MALE_HAT_COLOR_SELECTIONS, 0.0, 0.0, self.handleSetHatColor)
        self.femaleHatColorButtons = self.makeColorSelector(self.femaleHatColorFrameTitle, FEMALE_HAT_COLOR_SELECTIONS, 0.0, 0.0, self.handleSetHatColor)
        return

    def loadPantGUI(self):
        self.pantPicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingPantStyle, nextCommand=Functor(self.handleNextClothing, 'PANT'), backCommand=Functor(self.handleLastClothing, 'PANT'))
        self.pantPicker.setPos(-0.3, 0.0, -1.1)
        self.pantGenPics = DirectButton(parent=self.genPicsButtonsFrame, relief=DGG.RAISED, frameSize=(-0.17, 0.17, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                               0.008), text=PLocalizer.GeneratePictures, text_pos=(0, -0.015), text_scale=0.08, pos=(-1,
                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                     -1.1), command=self.handlePantGenPics)
        self.maleBeltColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame01'), image_scale=(0.9,
                                                                                                                                                           1,
                                                                                                                                                           1.0), image_pos=(0.3, 0, -0.0), scale=0.8, pos=(0.35,
                                                                                                                                                                                                           0,
                                                                                                                                                                                                           -1.45))
        self.femaleBeltColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame01'), image_scale=(0.9,
                                                                                                                                                             1,
                                                                                                                                                             1.0), image_pos=(0.3, 0, -0.0), scale=0.8, pos=(0.35,
                                                                                                                                                                                                             0,
                                                                                                                                                                                                             -1.45))
        self.beltPicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingBeltStyle, nextCommand=Functor(self.handleNextClothing, 'BELT'), backCommand=Functor(self.handleLastClothing, 'BELT'))
        self.beltPicker.setPos(-0.3, 0.0, -1.5)
        self.beltGenPics = DirectButton(parent=self.genPicsButtonsFrame, relief=DGG.RAISED, frameSize=(-0.17, 0.17, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                               0.008), text=PLocalizer.GeneratePictures, text_pos=(0, -0.015), text_scale=0.08, pos=(-1,
                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                     -1.46), command=self.handleBeltGenPics)
        if not self.main.wantNPCViewer:
            self.beltGenPics.setPos(-1, 0.0, -1.36)
        self.maleBeltColorButtons = self.makeColorSelector(self.maleBeltColorFrameTitle, MALE_BELT_COLOR_SELECTIONS, 0.0, 0.0, self.handleSetBeltColor)
        self.femaleBeltColorButtons = self.makeColorSelector(self.femaleBeltColorFrameTitle, FEMALE_BELT_COLOR_SELECTIONS, 0.0, 0.0, self.handleSetBeltColor)
        self.loadBotColorGUI()
        if not self.main.wantNPCViewer:
            self.pantPicker.setPos(-0.3, 0, -1.25)
            self.pantGenPics.setPos(-1, 0, -1.2)
            self.beltPicker.setPos(-0.3, 0.0, -0.85)
            self.maleBeltColorFrameTitle.setPos(0.35, 0.0, -0.8)
            self.femaleBeltColorFrameTitle.setPos(0.35, 0.0, -0.8)
            self.maleBotColorFrameTitle.setPos(0.35, 0.0, -1.2)
            self.femaleBotColorFrameTitle.setPos(0.35, 0.0, -1.2)
            self.clothesFrame.setPos(0, 0, 0.1)
        return

    def loadShoeGUI(self):
        self.shoePicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingShoeStyle, nextCommand=Functor(self.handleNextClothing, 'SHOE'), backCommand=Functor(self.handleLastClothing, 'SHOE'))
        self.shoePicker.setPos(-0.3, 0.0, -1.75)
        self.shoeGenPics = DirectButton(parent=self.genPicsButtonsFrame, relief=DGG.RAISED, frameSize=(-0.17, 0.17, -0.05, 0.05), borderWidth=(0.008,
                                                                                                                                               0.008), text=PLocalizer.GeneratePictures, text_pos=(0, -0.015), text_scale=0.08, pos=(-1,
                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                     -1.75), command=self.handleShoeGenPics)
        self.sockPicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingSockStyle, nextCommand=Functor(self.handleNextClothing, 'SHOE'), backCommand=Functor(self.handleLastClothing, 'SHOE'))
        self.sockPicker.setPos(-0.3, 0.0, -2.15)
        wantSocks = base.config.GetBool('want-socks', 0)
        if not wantSocks:
            self.sockPicker.hide()
        self.loadBotColorGUI()
        if self.main.wantNPCViewer:
            self.loadBotTextureGUI()

    def loadTopColorGUI(self):
        xOffset = 0.0
        yOffset = 0.0
        self.maleShirtColorButtons = []
        self.maleShirtColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame01'), image_scale=(0.9,
                                                                                                                                                            1,
                                                                                                                                                            1.0), image_pos=(0.3, 0, -0.0), scale=0.8, pos=(0.35,
                                                                                                                                                                                                            0,
                                                                                                                                                                                                            0.15))
        self.maleShirtColorButtons = self.makeColorSelector(self.maleShirtColorFrameTitle, MALE_SHIRT_COLOR_SELECTIONS, 0.0, 0.0, self.handleSetShirtColor)
        self.maleShirtColorFrameTitle.hide()
        self.maleVestColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame01'), image_scale=(0.9,
                                                                                                                                                           1,
                                                                                                                                                           1.0), image_pos=(0.3, 0, -0.0), scale=0.8, pos=(0.35, 0, -0.25))
        self.maleVestColorButtons = self.makeColorSelector(self.maleVestColorFrameTitle, MALE_VEST_COLOR_SELECTIONS, 0.0, 0.0, self.handleSetVestColor)
        self.maleVestColorFrameTitle.hide()
        self.maleCoatColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame01'), image_scale=(0.9,
                                                                                                                                                           1,
                                                                                                                                                           1.0), image_pos=(0.3, 0, -0.0), scale=0.8, pos=(0.35, 0, -0.65))
        self.maleCoatColorButtons = self.makeColorSelector(self.maleCoatColorFrameTitle, MALE_COAT_COLOR_SELECTIONS, 0.0, 0.0, self.handleSetCoatColor)
        self.maleCoatColorFrameTitle.hide()
        self.femaleShirtColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame01'), image_scale=(0.9,
                                                                                                                                                              1,
                                                                                                                                                              1.0), image_pos=(0.3, 0, -0.0), scale=0.8, pos=(0.35,
                                                                                                                                                                                                              0,
                                                                                                                                                                                                              0.15))
        self.femaleShirtColorButtons = self.makeColorSelector(self.femaleShirtColorFrameTitle, FEMALE_SHIRT_COLOR_SELECTIONS, 0.0, 0.0, self.handleSetShirtColor)
        self.femaleShirtColorFrameTitle.hide()
        self.femaleVestColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame01'), image_scale=(0.9,
                                                                                                                                                             1,
                                                                                                                                                             1.0), image_pos=(0.3, 0, -0.0), scale=0.8, pos=(0.35, 0, -0.25))
        self.femaleVestColorButtons = self.makeColorSelector(self.femaleVestColorFrameTitle, FEMALE_VEST_COLOR_SELECTIONS, 0.0, 0.0, self.handleSetVestColor)
        self.femaleVestColorFrameTitle.hide()
        self.femaleCoatColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame01'), image_scale=(0.9,
                                                                                                                                                             1,
                                                                                                                                                             1.0), image_pos=(0.3, 0, -0.0), scale=0.8, pos=(0.35, 0, -0.65))
        self.femaleCoatColorButtons = self.makeColorSelector(self.femaleCoatColorFrameTitle, FEMALE_COAT_COLOR_SELECTIONS, 0.0, 0.0, self.handleSetCoatColor)
        self.femaleCoatColorFrameTitle.hide()
        return

    def loadTopTextureGUI(self):
        self.hatTexturePicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingHatTrend, nextCommand=Functor(self.handleNextTexture, 'HAT'), backCommand=Functor(self.handleLastTexture, 'HAT'))
        self.hatTexturePicker.setPos(-0.3, 0, 0.25)
        self.shirtTexturePicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingShirtTrend, nextCommand=Functor(self.handleNextTexture, 'SHIRT'), backCommand=Functor(self.handleLastTexture, 'SHIRT'))
        self.shirtTexturePicker.setPos(-0.3, 0, -0.05)
        self.vestTexturePicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingVestTrend, nextCommand=Functor(self.handleNextTexture, 'VEST'), backCommand=Functor(self.handleLastTexture, 'VEST'))
        self.vestTexturePicker.setPos(-0.3, 0, -0.45)
        self.coatTexturePicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingCoatTrend, nextCommand=Functor(self.handleNextTexture, 'COAT'), backCommand=Functor(self.handleLastTexture, 'COAT'))
        self.coatTexturePicker.setPos(-0.3, 0, -0.85)

    def loadBotTextureGUI(self):
        self.pantTexturePicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingPantTrend, nextCommand=Functor(self.handleNextTexture, 'PANT'), backCommand=Functor(self.handleLastTexture, 'PANT'))
        self.pantTexturePicker.setPos(-0.3, 0, -1.25)
        self.shoeTexturePicker = CharGuiPicker(self.main, parent=self.clothesFrame, text=PLocalizer.MakeAPirateClothingShoeTrend, nextCommand=Functor(self.handleNextTexture, 'SHOE'), backCommand=Functor(self.handleLastTexture, 'SHOE'))
        self.shoeTexturePicker.setPos(-0.3, 0, -1.9)

    def loadBotColorGUI(self):
        vertPlace = -1.05
        if not self.main.wantNPCViewer:
            vertPlace = -1.2
        idx = 0
        self.maleBotColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame01'), image_scale=(0.9,
                                                                                                                                                          1,
                                                                                                                                                          1.0), image_pos=(0.3, 0, -0.0), scale=0.8, pos=(0.35, 0, vertPlace))
        self.maleBotColorFrameTitle.hide()
        self.malePantColorButtons = self.makeColorSelector(self.maleBotColorFrameTitle, MALE_PANTS_COLOR_SELECTIONS, 0.0, 0.0, self.handleSetPantColor)
        idx = 1
        self.femaleBotColorFrameTitle = DirectFrame(parent=self.clothesFrame, relief=None, image=self.main.charGui.find('**/chargui_frame01'), image_scale=(0.9,
                                                                                                                                                            1,
                                                                                                                                                            1.0), image_pos=(0.3, 0, -0.0), scale=0.8, pos=(0.35, 0, vertPlace))
        self.femaleBotColorFrameTitle.hide()
        self.femalePantColorButtons = self.makeColorSelector(self.femaleBotColorFrameTitle, FEMALE_PANTS_COLOR_SELECTIONS, 0.0, 0.0, self.handleSetPantColor)
        return

    def unload(self):
        del self.main
        del self._parent
        del self.avatar

    def showApparelCollections(self):
        if self.entered:
            self.clothesFrame.show()
            self.showTopColorCollections()
            self.showBotColorCollections()
            if self.main.wantNPCViewer:
                self.showHatColorCollections()
            self.showBeltColorCollections()

    def showHatColorCollections(self):
        colorButtons = self.maleHatColorButtons
        if self.main.pirate.style.gender == 'f':
            colorButtons = self.femaleHatColorButtons
            self.maleHatColorFrameTitle.hide()
            self.femaleHatColorFrameTitle.show()
        else:
            self.maleHatColorFrameTitle.show()
            self.femaleHatColorFrameTitle.hide()
        hatColor = self.avatar.dna.getHatColor()
        for i in range(0, TOPNUMCOLOR):
            colorButtons[i]['relief'] = DGG.RAISED

        colorButtons[hatColor]['relief'] = DGG.SUNKEN

    def showBeltColorCollections(self):
        colorButtons = self.maleBeltColorButtons
        if self.main.pirate.style.gender == 'f':
            colorButtons = self.femaleBeltColorButtons
            self.maleBeltColorFrameTitle.hide()
            if self.avatar.currentClothing['BELT'][1]:
                self.femaleBeltColorFrameTitle.show()
        else:
            if self.avatar.currentClothing['BELT'][1]:
                self.maleBeltColorFrameTitle.show()
            self.femaleBeltColorFrameTitle.hide()
        beltColor = self.avatar.dna.getClothesBotColor()[1]
        for i in range(0, TOPNUMCOLOR):
            colorButtons[i]['relief'] = DGG.RAISED

        colorButtons[beltColor]['relief'] = DGG.SUNKEN

    def showTopColorCollections(self):
        shirtColorButtons = self.maleShirtColorButtons
        vestColorButtons = self.maleVestColorButtons
        coatColorButtons = self.maleCoatColorButtons
        if self.main.pirate.style.gender == 'f':
            shirtColorButtons = self.femaleShirtColorButtons
            vestColorButtons = self.femaleVestColorButtons
            coatColorButtons = self.femaleCoatColorButtons
        clothesTopColor = self.avatar.dna.getClothesTopColor()
        if self.main.pirate.style.gender == 'm':
            if self.avatar.currentClothing['SHIRT'][1]:
                self.maleShirtColorFrameTitle.show()
            if self.avatar.currentClothing['VEST'][1]:
                self.maleVestColorFrameTitle.show()
            if self.main.wantNPCViewer:
                self.maleCoatColorFrameTitle.show()
        else:
            if self.avatar.currentClothing['SHIRT'][1]:
                self.femaleShirtColorFrameTitle.show()
            if self.avatar.currentClothing['VEST'][1]:
                self.femaleVestColorFrameTitle.show()
            if self.main.wantNPCViewer:
                self.femaleCoatColorFrameTitle.show()
        for button in shirtColorButtons:
            button['relief'] = DGG.RAISED
            if button.colorId == clothesTopColor[0]:
                button['relief'] = DGG.SUNKEN

        for button in vestColorButtons:
            button['relief'] = DGG.RAISED
            if button.colorId == clothesTopColor[1]:
                button['relief'] = DGG.SUNKEN

        for button in coatColorButtons:
            button['relief'] = DGG.RAISED
            if button.colorId == clothesTopColor[2]:
                button['relief'] = DGG.SUNKEN

    def showBotColorCollections(self):
        if self.main.pirate.style.gender == 'f':
            pantColorButtons = self.femalePantColorButtons
            if self.avatar.currentClothing['PANT'][1]:
                self.femaleBotColorFrameTitle.show()
        else:
            pantColorButtons = self.malePantColorButtons
            if self.avatar.currentClothing['PANT'][1]:
                self.maleBotColorFrameTitle.show()
        clothesBotColor = self.avatar.dna.getClothesBotColor()
        for button in pantColorButtons:
            button['relief'] = DGG.RAISED
            if button.colorId == clothesBotColor[0]:
                button['relief'] = DGG.SUNKEN

    def hideApparelCollections(self):
        self.clothesFrame.hide()
        self.maleShirtColorFrameTitle.hide()
        self.maleVestColorFrameTitle.hide()
        if self.main.wantNPCViewer:
            self.maleCoatColorFrameTitle.hide()
        self.maleBotColorFrameTitle.hide()
        self.femaleShirtColorFrameTitle.hide()
        self.femaleVestColorFrameTitle.hide()
        if self.main.wantNPCViewer:
            self.femaleCoatColorFrameTitle.hide()
        self.femaleBotColorFrameTitle.hide()

    def show(self):
        self.showApparelCollections()
        if self.main.inRandomAll:
            return
        if self.once:
            idx = 0
            if self.main.pirate.gender == 'f':
                idx = 1
            optionsLeft = len(self.main.JSD_CLOTHING_INTRO[idx])
            if optionsLeft:
                choice = random.choice(range(0, optionsLeft))
                if self.main.lastDialog:
                    self.main.lastDialog.stop()
                dialog = self.main.JSD_CLOTHING_INTRO[idx][choice]
                base.playSfx(dialog, node=self.avatar.pirate)
                self.main.lastDialog = dialog
                self.main.JSD_CLOTHING_INTRO[idx].remove(dialog)
        else:
            self.once = True

    def hide(self):
        self.hideApparelCollections()

    def restore(self):
        self.hideApparelCollections()
        self.showApparelCollections()

    def reset(self):
        if self.avatar.dna.getGender() == 'm':
            self.avatar.currentClothing = ItemGlobals.getDefaultMaleClothing()
        else:
            self.avatar.currentClothing = ItemGlobals.getDefaultFemaleClothing()
        self.avatar.pirate.setClothesCoat(0, 0)
        if self.main.pirate.style.gender == 'f':
            self.avatar.pirate.setClothesPant(ItemGlobals.getFemaleModelId(self.avatar.currentClothing['PANT'][0]), ItemGlobals.getFemaleTextureId(self.avatar.currentClothing['PANT'][0]))
            self.avatar.pirate.setClothesBelt(ItemGlobals.getFemaleModelId(self.avatar.currentClothing['BELT'][0]), ItemGlobals.getFemaleTextureId(self.avatar.currentClothing['BELT'][0]))
            self.avatar.pirate.setClothesShirt(ItemGlobals.getFemaleModelId(self.avatar.currentClothing['SHIRT'][0]), ItemGlobals.getFemaleTextureId(self.avatar.currentClothing['SHIRT'][0]))
            self.avatar.pirate.setClothesVest(ItemGlobals.getFemaleModelId(self.avatar.currentClothing['VEST'][0]), ItemGlobals.getFemaleTextureId(self.avatar.currentClothing['VEST'][0]))
            self.avatar.pirate.setClothesShoe(ItemGlobals.getFemaleModelId(self.avatar.currentClothing['SHOE'][0]), ItemGlobals.getFemaleTextureId(self.avatar.currentClothing['SHOE'][0]))
        else:
            self.avatar.pirate.setClothesPant(ItemGlobals.getMaleModelId(self.avatar.currentClothing['PANT'][0]), ItemGlobals.getMaleTextureId(self.avatar.currentClothing['PANT'][0]))
            self.avatar.pirate.setClothesBelt(ItemGlobals.getMaleModelId(self.avatar.currentClothing['BELT'][0]), ItemGlobals.getMaleTextureId(self.avatar.currentClothing['BELT'][0]))
            self.avatar.pirate.setClothesShirt(ItemGlobals.getMaleModelId(self.avatar.currentClothing['SHIRT'][0]), ItemGlobals.getMaleTextureId(self.avatar.currentClothing['SHIRT'][0]))
            self.avatar.pirate.setClothesVest(ItemGlobals.getMaleModelId(self.avatar.currentClothing['VEST'][0]), ItemGlobals.getMaleTextureId(self.avatar.currentClothing['VEST'][0]))
            self.avatar.pirate.setClothesShoe(ItemGlobals.getMaleModelId(self.avatar.currentClothing['SHOE'][0]), ItemGlobals.getMaleTextureId(self.avatar.currentClothing['SHOE'][0]))
        self.handleSetShirtColor(0)
        self.handleSetVestColor(0)
        self.handleSetCoatColor(0)
        self.handleSetPantColor(0)
        self.handleClothingChanged()

    def randomPick(self):
        self.avatar.clothing.stash()
        for type in ['SHIRT', 'VEST', 'COAT', 'PANT', 'BELT', 'SHOE']:
            id = random.choice(self.avatar.choices[type].keys())
            itemId = self.avatar.choices[type][id][0]
            texId = self.avatar.choices[type][id][1]
            dyeItem = self.avatar.choices[type][id][2]
            self.avatar.currentClothing[type] = [id, dyeItem, 0]
            self.avatar.pirate.setClothesByType(type, itemId, texId, 0)

        if self.avatar.currentClothing['VEST'][0] != 0:
            self.avatar.currentClothing['COAT'] = [
             0, 0, 0]
            self.avatar.pirate.setClothesByType('COAT', 0, 0, 0)
        if self.main.pirate.style.gender == 'f':
            coatColors = FEMALE_COAT_COLOR_SELECTIONS
            vestColors = FEMALE_VEST_COLOR_SELECTIONS
            shirtColors = FEMALE_SHIRT_COLOR_SELECTIONS
            beltColors = FEMALE_BELT_COLOR_SELECTIONS
            pantsColors = FEMALE_PANTS_COLOR_SELECTIONS
        else:
            coatColors = MALE_COAT_COLOR_SELECTIONS
            vestColors = MALE_VEST_COLOR_SELECTIONS
            shirtColors = MALE_SHIRT_COLOR_SELECTIONS
            beltColors = MALE_BELT_COLOR_SELECTIONS
            pantsColors = MALE_PANTS_COLOR_SELECTIONS
        if self.avatar.currentClothing['SHIRT'][1]:
            choice = random.choice(shirtColors)
            self.avatar.currentClothing['SHIRT'][2] = choice
            self.handleSetShirtColor(choice)
        if self.avatar.currentClothing['VEST'][1]:
            choice = random.choice(vestColors)
            self.avatar.currentClothing['VEST'][2] = choice
            self.handleSetVestColor(choice)
        if self.avatar.currentClothing['COAT'][1]:
            choice = random.choice(coatColors)
            self.avatar.currentClothing['COAT'][2] = choice
            self.handleSetCoatColor(choice)
        if self.avatar.currentClothing['PANT'][1]:
            choice = random.choice(pantsColors)
            self.avatar.currentClothing['PANT'][2] = choice
            self.handleSetPantColor(choice)
        if self.avatar.currentClothing['BELT'][1]:
            choice = random.choice(beltColors)
            self.avatar.currentClothing['BELT'][2] = choice
            self.handleSetBeltColor(choice)
        self.handleClothingChanged()

    def handleNextClothing(self, type):
        if not self.main.wantNPCViewer:
            clothing = self.getNextClothingItem(type)
            self.main.playJackDialogOnClothes(type)
        else:
            if self.main.wantPicButtons:
                clothing = self.getNextClothingItem(type)
            else:
                clothing = self.getNextClothingModel(type)
            self.texName = self.avatar.getTextureName(type, clothing[1], clothing[2])[0]
            self.main.guiTextureInfo[type]['text'] = '%s %s %s %s' % (self.texName, type, clothing[1], clothing[2])
            self.main.guiTextureInfo[type]['text_fg'] = (1, 1, 1, 1)
        self.avatar.pirate.setClothesByType(type, clothing[1], clothing[2])
        self.avatar.currentClothing[type][0] = clothing[0]
        self.avatar.currentClothing[type][1] = ItemGlobals.canDyeItem(clothing[0])
        self.avatar.currentClothing[type][2] = 0
        if type == 'HAT':
            self.handleSetHatColor(0)
        else:
            if type == 'SHIRT':
                self.handleSetShirtColor(0)
            elif type == 'VEST':
                self.handleSetVestColor(0)
            elif type == 'COAT':
                self.handleSetCoatColor(0)
            elif type == 'PANT':
                self.handleSetPantColor(0)
            elif type == 'BELT':
                self.handleSetBeltColor(0)
            self.handleClothingChanged()
            if base.config.GetBool('want-map-flavor-anims', 0):
                currTime = globalClock.getFrameTime()
                if self.main.pirate.style.gender == 'f':
                    if currTime - self.lastRun > 10:
                        if type == 'SHOE':
                            if random.randint(0, 1) == 0:
                                self.avatar.pirate.play('map_look_boot_left')
                            else:
                                self.avatar.pirate.play('map_look_boot_right')
                        self.lastRun = currTime
                    currTime = globalClock.getFrameTime()
                elif currTime - self.lastRun > 10:
                    if type == 'SHIRT' or type == 'COAT':
                        if random.randint(0, 1) == 0:
                            self.avatar.pirate.play('map_look_arm_left')
                        else:
                            self.avatar.pirate.play('map_look_arm_right')
                    if type == 'PANT' or type == 'BELT':
                        self.avatar.pirate.play('map_look_pant_right')
                    if type == 'SHOE':
                        self.avatar.pirate.play('map_look_boot_left')
                    self.lastRun = currTime

    def handleLastClothingOld(self, type):
        if not self.main.wantNPCViewer:
            clothing = self.getLastClothingItem(type)
            self.main.playJackDialogOnClothes(type)
        else:
            if self.main.wantPicButtons:
                clothing = self.getLastClothingItem(type)
            else:
                clothing = self.getLastClothingModel(type)
            texName = self.avatar.getTextureName(type, clothing[1], clothing[2])[0]
            self.main.guiTextureInfo[type]['text'] = texName
            self.main.guiTextureInfo[type]['text_fg'] = (1, 1, 1, 1)
        self.avatar.pirate.setClothesByType(type, clothing[1], clothing[2])
        self.avatar.currentClothing[type][0] = clothing[0]
        self.avatar.currentClothing[type][1] = ItemGlobals.canDyeItem(clothing[0])
        self.avatar.currentClothing[type][2] = 0
        if self.main.wantNPCViewer:
            self.texName = self.avatar.getTextureName(SHIRT, self.avatar.clothingShirtIdx, self.avatar.clothingShirtTexture)
            self.main.guiTextureInfo[type]['text'] = '%s %s %s %s' % (self.texName, type, clothing[1], clothing[2])
            self.main.guiTextureInfo['text_fg'] = (1, 1, 1, 1)
        self.handleClothingChanged()
        if base.config.GetBool('want-map-flavor-anims', 0):
            currTime = globalClock.getFrameTime()
            if self.main.pirate.style.gender == 'f':
                if currTime - self.lastRun > 10:
                    if type == 'SHOE':
                        if random.randint(0, 1) == 0:
                            self.avatar.pirate.play('map_look_boot_left')
                        else:
                            self.avatar.pirate.play('map_look_boot_right')
                    self.lastRun = currTime
                currTime = globalClock.getFrameTime()
            else:
                currTime = globalClock.getFrameTime()
                if currTime - self.lastRun > 10:
                    if type == 'SHIRT' or type == 'COAT':
                        if random.randint(0, 1) == 0:
                            self.avatar.pirate.play('map_look_arm_left')
                        else:
                            self.avatar.pirate.play('map_look_arm_right')
                    if type == 'PANT' or type == 'BELT':
                        self.avatar.pirate.play('map_look_pant_right')
                    if type == 'SHOE':
                        self.avatar.pirate.play('map_look_boot_left')
                    self.lastRun = currTime

    def handleLastClothing(self, type):
        if not self.main.wantNPCViewer:
            clothing = self.getLastClothingItem(type)
            self.main.playJackDialogOnClothes(type)
        else:
            if self.main.wantPicButtons:
                clothing = self.getLastClothingItem(type)
            else:
                clothing = self.getLastClothingModel(type)
            self.texName = self.avatar.getTextureName(type, clothing[1], clothing[2])[0]
            self.main.guiTextureInfo[type]['text'] = '%s %s %s %s' % (self.texName, type, clothing[1], clothing[2])
            self.main.guiTextureInfo[type]['text_fg'] = (1, 1, 1, 1)
        self.avatar.pirate.setClothesByType(type, clothing[1], clothing[2])
        self.avatar.currentClothing[type][0] = clothing[0]
        self.avatar.currentClothing[type][1] = ItemGlobals.canDyeItem(clothing[0])
        self.avatar.currentClothing[type][2] = 0
        if type == 'HAT':
            self.handleSetHatColor(0)
        else:
            if type == 'SHIRT':
                self.handleSetShirtColor(0)
            elif type == 'VEST':
                self.handleSetVestColor(0)
            elif type == 'COAT':
                self.handleSetCoatColor(0)
            elif type == 'PANT':
                self.handleSetPantColor(0)
            elif type == 'BELT':
                self.handleSetBeltColor(0)
            self.handleClothingChanged()
            if base.config.GetBool('want-map-flavor-anims', 0):
                currTime = globalClock.getFrameTime()
                if self.main.pirate.style.gender == 'f':
                    if currTime - self.lastRun > 10:
                        if type == 'SHOE':
                            if random.randint(0, 1) == 0:
                                self.avatar.pirate.play('map_look_boot_left')
                            else:
                                self.avatar.pirate.play('map_look_boot_right')
                        self.lastRun = currTime
                    currTime = globalClock.getFrameTime()
                elif currTime - self.lastRun > 10:
                    if type == 'SHIRT' or type == 'COAT':
                        if random.randint(0, 1) == 0:
                            self.avatar.pirate.play('map_look_arm_left')
                        else:
                            self.avatar.pirate.play('map_look_arm_right')
                    if type == 'PANT' or type == 'BELT':
                        self.avatar.pirate.play('map_look_pant_right')
                    if type == 'SHOE':
                        self.avatar.pirate.play('map_look_boot_left')
                    self.lastRun = currTime

    def handleNextTexture(self, type):
        clothing = self.getNextClothingTexture(type)
        self.avatar.currentClothing[type][1] = clothing[1]
        self.avatar.currentClothing[type][2] = clothing[2]
        self.avatar.pirate.setClothesByType(type, clothing[1], clothing[2])
        if self.main.wantNPCViewer:
            self.texName = self.avatar.getTextureName(type, clothing[1], clothing[2])[0]
            self.main.guiTextureInfo[type]['text'] = '%s %s %s %s' % (self.texName, type, clothing[1], clothing[2])
            self.main.guiTextureInfo[type]['text_fg'] = (1, 1, 1, 1)
        self.avatar.pirate.setClothesByType(type, clothing[1], clothing[2])
        self.avatar.currentClothing[type][0] = clothing[0]
        self.avatar.currentClothing[type][1] = ItemGlobals.canDyeItem(clothing[0])
        self.avatar.currentClothing[type][2] = 0
        if type == 'HAT':
            self.handleSetHatColor(0)
        elif type == 'SHIRT':
            self.handleSetShirtColor(0)
        elif type == 'VEST':
            self.handleSetVestColor(0)
        elif type == 'COAT':
            self.handleSetCoatColor(0)
        elif type == 'PANT':
            self.handleSetPantColor(0)
        elif type == 'BELT':
            self.handleSetBeltColor(0)
        self.handleClothingChanged()

    def handleLastTexture(self, type):
        clothing = self.getLastClothingTexture(type)
        self.avatar.currentClothing[type][1] = clothing[1]
        self.avatar.currentClothing[type][2] = clothing[2]
        self.avatar.pirate.setClothesByType(type, clothing[1], clothing[2])
        if self.main.wantNPCViewer:
            self.texName = self.avatar.getTextureName(type, clothing[1], clothing[2])[0]
            self.main.guiTextureInfo[type]['text'] = '%s %s %s %s' % (self.texName, type, clothing[1], clothing[2])
            self.main.guiTextureInfo[type]['text_fg'] = (1, 1, 1, 1)
        self.avatar.pirate.setClothesByType(type, clothing[1], clothing[2])
        self.avatar.currentClothing[type][0] = clothing[0]
        self.avatar.currentClothing[type][1] = ItemGlobals.canDyeItem(clothing[0])
        self.avatar.currentClothing[type][2] = 0
        if type == 'HAT':
            self.handleSetHatColor(0)
        elif type == 'SHIRT':
            self.handleSetShirtColor(0)
        elif type == 'VEST':
            self.handleSetVestColor(0)
        elif type == 'COAT':
            self.handleSetCoatColor(0)
        elif type == 'PANT':
            self.handleSetPantColor(0)
        elif type == 'BELT':
            self.handleSetBeltColor(0)
        self.handleClothingChanged()

    def handleSetShirtColor(self, colorIndex):
        colorButtons = self.maleShirtColorButtons
        if self.main.pirate.style.gender == 'f':
            colorButtons = self.femaleShirtColorButtons
        clothesTopColor = self.avatar.dna.getClothesTopColor()
        clothesTopColor[0] = colorIndex
        self.avatar.currentClothing['SHIRT'][2] = colorIndex
        for colorButton in colorButtons:
            if colorButton.colorId == colorIndex:
                colorButton['relief'] = DGG.RAISED
            else:
                colorButton['relief'] = DGG.SUNKEN

        self.main.pirate.setClothesTopColor(clothesTopColor[0], clothesTopColor[1], clothesTopColor[2])
        self.main.pirate.model.handleClothesHiding()

    def handleSetVestColor(self, colorIndex):
        colorButtons = self.maleVestColorButtons
        if self.main.pirate.style.gender == 'f':
            colorButtons = self.femaleVestColorButtons
        clothesTopColor = self.avatar.dna.getClothesTopColor()
        clothesTopColor[1] = colorIndex
        self.avatar.currentClothing['VEST'][2] = colorIndex
        for colorButton in colorButtons:
            if colorButton.colorId == colorIndex:
                colorButton['relief'] = DGG.RAISED
            else:
                colorButton['relief'] = DGG.SUNKEN

        self.main.pirate.setClothesTopColor(clothesTopColor[0], clothesTopColor[1], clothesTopColor[2])
        self.main.pirate.model.handleClothesHiding()

    def handleSetCoatColor(self, colorIndex):
        colorButtons = self.maleCoatColorButtons
        if self.main.pirate.style.gender == 'f':
            colorButtons = self.femaleCoatColorButtons
        clothesTopColor = self.avatar.dna.getClothesTopColor()
        clothesTopColor[2] = colorIndex
        self.avatar.currentClothing['COAT'][2] = colorIndex
        for colorButton in colorButtons:
            if colorButton.colorId == colorIndex:
                colorButton['relief'] = DGG.RAISED
            else:
                colorButton['relief'] = DGG.SUNKEN

        self.main.pirate.setClothesTopColor(clothesTopColor[0], clothesTopColor[1], clothesTopColor[2])
        self.main.pirate.model.handleClothesHiding()

    def handleSetPantColor(self, colorIndex):
        colorButtons = self.malePantColorButtons
        if self.main.pirate.style.gender == 'f':
            colorButtons = self.femalePantColorButtons
        clothesBotColor = self.avatar.dna.getClothesBotColor()
        clothesBotColor[0] = colorIndex
        self.avatar.currentClothing['PANT'][2] = colorIndex
        for colorButton in colorButtons:
            if colorButton.colorId == colorIndex:
                colorButton['relief'] = DGG.RAISED
            else:
                colorButton['relief'] = DGG.SUNKEN

        self.main.pirate.setClothesBotColor(clothesBotColor[0], clothesBotColor[1], clothesBotColor[2])
        self.main.pirate.model.handleClothesHiding()

    def handleSetBeltColor(self, colorIndex):
        colorButtons = self.maleBeltColorButtons
        if self.main.pirate.style.gender == 'f':
            colorButtons = self.femaleBeltColorButtons
        clothesBotColor = self.avatar.dna.getClothesBotColor()
        clothesBotColor[1] = colorIndex
        self.avatar.currentClothing['BELT'][2] = colorIndex
        for colorButton in colorButtons:
            if colorButton.colorId == colorIndex:
                colorButton['relief'] = DGG.RAISED
            else:
                colorButton['relief'] = DGG.SUNKEN

        self.main.pirate.setClothesBotColor(clothesBotColor[0], clothesBotColor[1], clothesBotColor[2])
        self.main.pirate.model.handleClothesHiding()

    def handleSetShoeColor(self, colorIndex):
        colorButtons = self.maleShoeColorButtons
        if self.main.pirate.style.gender == 'f':
            colorButtons = self.femaleShoeColorButtons
        clothesBotColor = self.avatar.dna.getClothesBotColor()
        clothesBotColor[2] = colorIndex
        self.avatar.currentClothing['SHOE'][2] = colorIndex
        for colorButton in colorButtons:
            if colorButton.colorId == colorIndex:
                colorButton['relief'] = DGG.RAISED
            else:
                colorButton['relief'] = DGG.SUNKEN

        self.main.pirate.setClothesBotColor(clothesBotColor[0], clothesBotColor[1], clothesBotColor[2])
        self.main.pirate.model.handleClothesHiding()
        self.main.pirate.model.handleClothesHiding()

    def handleSetHatColor(self, colorIndex):
        colorButtons = self.maleHatColorButtons
        if self.main.pirate.style.gender == 'f':
            colorButtons = self.femaleHatColorButtons
        hatColor = self.avatar.dna.getHatColor()
        hatColor = colorIndex
        self.avatar.currentClothing['HAT'][2] = colorIndex
        for colorButton in colorButtons:
            if colorButton.colorId == colorIndex:
                colorButton['relief'] = DGG.RAISED
            else:
                colorButton['relief'] = DGG.SUNKEN

        self.main.pirate.setHatColor(hatColor)
        self.main.pirate.model.handleClothesHiding()

    def generatePics(self, type):
        render2d.hide()
        self.avatar.pirate.findAllMatches('**/drop*').getPath(1).hide()
        self.hidePirate()
        self.hideOtherClothes(type)
        clothingSize = self.getClothingSize(type)
        for i in range(0, clothingSize):
            if i == 0:
                self.texName = self.avatar.getTextureName(type, self.avatar.currentClothing[type][0], self.avatar.currentClothing[type][1])[0]
            if i < 10:
                prefix = '0'
            else:
                prefix = ''
            self.avatar.pirate.setHpr(180, 0, 0)
            self.notify.info('SCREENSHOT %d__%s__FRONT' % (i, self.texName))
            uFilename = type + '_' + prefix + str(i) + '__' + self.texName + '__FRONT.' + base.screenshotExtension
            base.graphicsEngine.renderFrame()
            base.screenshot(namePrefix=uFilename, defaultFilename=0)
            self.avatar.pirate.setHpr(0, 0, 0)
            self.notify.info('SCREENSHOT %d__%s__BACK' % (i, self.texName))
            uFilename = type + '_' + prefix + str(i) + '__' + self.texName + '__BACK.' + base.screenshotExtension
            base.graphicsEngine.renderFrame()
            base.screenshot(namePrefix=uFilename, defaultFilename=0)
            self.handleNextClothing(type)

        self.notify.info('done with shirt screencaps')
        render2d.show()
        self.avatar.pirate.findAllMatches('**/drop*').getPath(1).show()
        self.showPirate()
        self.avatar.pirate.setHpr(180, 0, 0)
        self.showOtherClothes(type)

    def handleShirtGenPics(self):
        taskMgr.remove('avCreate-ZoomTask')
        oldPos = base.camera.getPos()
        if self.main.pirate.gender == 'f':
            base.camera.setPos(-0.2, -5, 5.27)
        else:
            base.camera.setPos(-0.2, -5, 5.3)
        self.generatePics('SHIRT')
        base.camera.setPos(oldPos)
        taskMgr.add(self.main.zoomTask, 'avCreate-ZoomTask')

    def handleVestGenPics(self):
        taskMgr.remove('avCreate-ZoomTask')
        oldPos = base.camera.getPos()
        if self.main.pirate.gender == 'f':
            base.camera.setPos(-0.2, -4.1, 4.95)
        else:
            base.camera.setPos(-0.2, -5, 5.3)
        self.generatePics('VEST')
        base.camera.setPos(oldPos)
        taskMgr.add(self.main.zoomTask, 'avCreate-ZoomTask')

    def handleCoatGenPics(self):
        taskMgr.remove('avCreate-ZoomTask')
        oldPos = base.camera.getPos()
        if self.main.pirate.gender == 'f':
            base.camera.setPos(-0.2, -6.6, 5.3)
        else:
            base.camera.setPos(-0.2, -7.5, 5.4)
        self.generatePics('COAT')
        base.camera.setPos(oldPos)
        taskMgr.add(self.main.zoomTask, 'avCreate-ZoomTask')

    def handlePantGenPics(self):
        taskMgr.remove('avCreate-ZoomTask')
        oldPos = base.camera.getPos()
        if self.main.pirate.gender == 'f':
            base.camera.setPos(-0.1, -8, 4)
        else:
            base.camera.setPos(-0.2, -5.5, 3.7)
        self.generatePics('PANT')
        base.camera.setPos(oldPos)
        taskMgr.add(self.main.zoomTask, 'avCreate-ZoomTask')

    def handleBeltGenPics(self):
        taskMgr.remove('avCreate-ZoomTask')
        oldPos = base.camera.getPos()
        if self.main.pirate.gender == 'f':
            base.camera.setPos(-0.1, -4.1, 3.8)
        else:
            base.camera.setPos(-0.1, -3.9, 3.55)
        self.generatePics('BELT')
        base.camera.setPos(oldPos)
        taskMgr.add(self.main.zoomTask, 'avCreate-ZoomTask')

    def handleShoeGenPics(self):
        taskMgr.remove('avCreate-ZoomTask')
        oldPos = base.camera.getPos()
        if self.main.pirate.gender == 'f':
            base.camera.setPos(-0.1, -5, 2.4)
        else:
            base.camera.setPos(-0.1, -4, 1.5)
        self.generatePics('SHOE')
        base.camera.setPos(oldPos)
        taskMgr.add(self.main.zoomTask, 'avCreate-ZoomTask')

    def handleHatGenPics(self):
        taskMgr.remove('avCreate-ZoomTask')
        oldPos = base.camera.getPos()
        if self.main.pirate.gender == 'f':
            base.camera.setPos(-0.1, -3, 6.1)
        else:
            base.camera.setPos(0, -3, 6.5)
        self.generatePics('HAT')
        base.camera.setPos(oldPos)
        taskMgr.add(self.main.zoomTask, 'avCreate-ZoomTask')

    def getNextClothingItem(self, type):
        clothes = [
         'SHIRT', 'VEST', 'PANT', 'COAT', 'BELT', 'SHOE', 'HAT']
        if type in clothes:
            dataId, dyeItem, color = self.avatar.currentClothing[type]
            if dataId not in self.avatar.choices[type]:
                self.notify.error('rrusso: how did it get here? dataId = %s' % dataId)
            dataIds = self.avatar.choices[type].keys()
            currIdx = dataIds.index(dataId)
            if currIdx + 1 < len(dataIds):
                dataId = dataIds[currIdx + 1]
            else:
                dataId = dataIds[0]
            if self.main.pirate.gender == 'f':
                itemId = ItemGlobals.getFemaleModelId(dataId)
                textureId = ItemGlobals.getFemaleTextureId(dataId)
            else:
                itemId = ItemGlobals.getMaleModelId(dataId)
                textureId = ItemGlobals.getMaleTextureId(dataId)
        else:
            dataId = 0
            itemId, textureId, color = self.avatar.currentClothing[type]
            if itemId not in self.avatar.choices[type]:
                self.notify.error('masad: how did it get here? itemId = %s' % itemId)
            itemTextures = self.avatar.choices[type][itemId]
            currentTexIdx = itemTextures.index(textureId)
            texIdx = currentTexIdx + 1
            if texIdx >= len(itemTextures):
                itemIds = self.avatar.choices[type].keys()
                itemIds.sort()
                currIdx = itemIds.index(itemId)
                if currIdx + 1 < len(itemIds):
                    newIdx = itemIds[currIdx + 1]
                else:
                    newIdx = itemIds[0]
                itemId = newIdx
                textureId = self.avatar.choices[type][newIdx][0]
            else:
                textureId = self.avatar.choices[type][itemId][texIdx]
        return (
         dataId, itemId, textureId)

    def getLastClothingItem(self, type):
        clothes = [
         'SHIRT', 'VEST', 'PANT', 'COAT', 'BELT', 'SHOE', 'HAT']
        if type in clothes:
            dataId, dyeItem, color = self.avatar.currentClothing[type]
            if dataId not in self.avatar.choices[type]:
                self.notify.error('rrusso: how did it get here? dataId = %s' % dataId)
            dataIds = self.avatar.choices[type].keys()
            currIdx = dataIds.index(dataId)
            if currIdx - 1 >= 0:
                dataId = dataIds[currIdx - 1]
            else:
                maxIdx = len(dataIds) - 1
                dataId = dataIds[maxIdx]
            if self.main.pirate.gender == 'f':
                itemId = ItemGlobals.getFemaleModelId(dataId)
                textureId = ItemGlobals.getFemaleTextureId(dataId)
            else:
                itemId = ItemGlobals.getMaleModelId(dataId)
                textureId = ItemGlobals.getMaleTextureId(dataId)
        else:
            dataId = 0
            itemId, textureId, color = self.avatar.currentClothing[type]
            if itemId not in self.avatar.choices[type]:
                self.notify.error('masad: how did it get here? itemId = %s' % itemId)
            itemTextures = self.avatar.choices[type][itemId]
            currentTexIdx = itemTextures.index(textureId)
            texIdx = currentTexIdx - 1
            if texIdx < 0:
                itemIds = self.avatar.choices[type].keys()
                itemIds.sort()
                currIdx = itemIds.index(itemId)
                itemId = itemIds[currIdx - 1]
                textureId = self.avatar.choices[type][itemId][-1]
            else:
                textureId = self.avatar.choices[type][itemId][texIdx]
        return (dataId, itemId, textureId)

    def checkCurrentClothing(self):
        for clothesType in ['HAT', 'SHIRT', 'VEST', 'COAT', 'PANT', 'BELT', 'SHOE']:
            dataId, dyeItem, color = self.avatar.currentClothing[clothesType]
            models = self.avatar.choices[clothesType].keys()
            if dataId not in models:
                nextItemId = models[0]
                if self.main.pirate.style.gender == 'f':
                    modelId = ItemGlobals.getFemaleModelId(nextItemId)
                    textureId = ItemGlobals.getFemaleTextureId(nextItemId)
                else:
                    modelId = ItemGlobals.getMaleModelId(nextItemId)
                    textureId = ItemGlobals.getMaleTextureId(nextItemId)
                self.avatar.pirate.setClothesByType(clothesType, modelId, textureId)
                self.avatar.currentClothing[clothesType][0] = nextItemId
                self.avatar.currentClothing[clothesType][1] = ItemGlobals.canDyeItem(nextItemId)
                self.avatar.currentClothing[clothesType][2] = 0
                if clothesType == 'HAT':
                    self.handleSetHatColor(0)
                elif clothesType == 'SHIRT':
                    self.handleSetShirtColor(0)
                elif clothesType == 'VEST':
                    self.handleSetVestColor(0)
                elif clothesType == 'COAT':
                    self.handleSetCoatColor(0)
                elif clothesType == 'PANT':
                    self.handleSetPantColor(0)
                elif clothesType == 'BELT':
                    self.handleSetBeltColor(0)

        self.handleClothingChanged()

    def getSortedKeysByModelId(self, dict):

        def modelId_compare(x, y):
            if dict[x][0] == dict[y][0]:
                return dict[x][1] - dict[y][1]
            else:
                return dict[x][0] - dict[y][0]

        return sorted(dict.keys(), cmp=modelId_compare)

    def getNextClothingModel(self, type):
        dataId, dyeItem, color = self.avatar.currentClothing[type]
        if self.main.pirate.style.gender == 'f':
            currModelId = ItemGlobals.getFemaleModelId(dataId)
            currTextureId = ItemGlobals.getFemaleTextureId(dataId)
        else:
            currModelId = ItemGlobals.getMaleModelId(dataId)
            currTextureId = ItemGlobals.getMaleTextureId(dataId)
        itemIds = self.getSortedKeysByModelId(self.avatar.choices[type])
        nextItemId = itemIds[0]
        nextModelId = self.avatar.choices[type][nextItemId][0]
        nextTextureId = self.avatar.choices[type][nextItemId][1]
        if dataId not in itemIds:
            currIdx = -1
            currModelId = nextModelId - 1
        else:
            currIdx = itemIds.index(dataId)
        for idx in range(currIdx + 1, len(itemIds)):
            itemId = itemIds[idx]
            if self.main.pirate.style.gender == 'f':
                modelId = ItemGlobals.getFemaleModelId(itemId)
                textureId = ItemGlobals.getFemaleTextureId(itemId)
            else:
                modelId = ItemGlobals.getMaleModelId(itemId)
                textureId = ItemGlobals.getMaleTextureId(itemId)
            if modelId > currModelId:
                nextItemId = itemId
                nextModelId = modelId
                nextTextureId = textureId
                break

        if nextItemId == itemIds[0]:
            currModelId = self.avatar.choices[type][nextItemId][0] - 1
            for itemId in itemIds:
                if self.main.pirate.style.gender == 'f':
                    modelId = ItemGlobals.getFemaleModelId(itemId)
                    textureId = ItemGlobals.getFemaleTextureId(itemId)
                else:
                    modelId = ItemGlobals.getMaleModelId(itemId)
                    textureId = ItemGlobals.getMaleTextureId(itemId)
                nextItemId = itemId
                nextModelId = modelId
                nextTextureId = textureId
                if modelId > currModelId:
                    break

        return (
         nextItemId, nextModelId, nextTextureId)

    def getLastClothingModel(self, type):
        dataId, dyeItem, color = self.avatar.currentClothing[type]
        if self.main.pirate.style.gender == 'f':
            currModelId = ItemGlobals.getFemaleModelId(dataId)
            currTextureId = ItemGlobals.getFemaleTextureId(dataId)
        else:
            currModelId = ItemGlobals.getMaleModelId(dataId)
            currTextureId = ItemGlobals.getMaleTextureId(dataId)
        itemIds = self.getSortedKeysByModelId(self.avatar.choices[type])
        lastItemId = itemIds[-1]
        lastModelId = self.avatar.choices[type][lastItemId][0]
        lastTextureId = self.avatar.choices[type][lastItemId][1]
        if dataId not in itemIds:
            currIdx = len(itemIds)
            currModelId = lastModelId + 1
        else:
            currIdx = itemIds.index(dataId)
        foundModelId = False
        for idx in range(currIdx, -1, -1):
            itemId = itemIds[idx]
            if self.main.pirate.style.gender == 'f':
                modelId = ItemGlobals.getFemaleModelId(itemId)
                textureId = ItemGlobals.getFemaleTextureId(itemId)
            else:
                modelId = ItemGlobals.getMaleModelId(itemId)
                textureId = ItemGlobals.getMaleTextureId(itemId)
            if not foundModelId and modelId < currModelId:
                foundModelId = True
                lastItemId = itemId
                lastModelId = modelId
                lastTextureId = textureId
            if foundModelId:
                if modelId < lastModelId:
                    break
                if textureId < lastTextureId:
                    lastItemId = itemId
                    lastModelId = modelId
                    lastTextureId = textureId

        if lastItemId == itemIds[-1]:
            currModelId = self.avatar.choices[type][lastItemId][0] + 1
            foundModelId = False
            for idx in range(len(itemIds) - 1, -1, -1):
                itemId = itemIds[idx]
                if self.main.pirate.style.gender == 'f':
                    modelId = ItemGlobals.getFemaleModelId(itemId)
                    textureId = ItemGlobals.getFemaleTextureId(itemId)
                else:
                    modelId = ItemGlobals.getMaleModelId(itemId)
                    textureId = ItemGlobals.getMaleTextureId(itemId)
                if not foundModelId and modelId < currModelId:
                    foundModelId = True
                    lastItemId = itemId
                    lastModelId = modelId
                    lastTextureId = textureId
                if foundModelId:
                    if modelId < lastModelId:
                        break
                    if textureId < lastTextureId:
                        lastItemId = itemId
                        lastModelId = modelId
                        lastTextureId = textureId

        return (
         lastItemId, lastModelId, lastTextureId)

    def getNextClothingTexture(self, type):
        dataId, dyeItem, color = self.avatar.currentClothing[type]
        if self.main.pirate.style.gender == 'f':
            currModelId = ItemGlobals.getFemaleModelId(dataId)
            currTextureId = ItemGlobals.getFemaleTextureId(dataId)
        else:
            currModelId = ItemGlobals.getMaleModelId(dataId)
            currTextureId = ItemGlobals.getMaleTextureId(dataId)
        itemIds = self.getSortedKeysByModelId(self.avatar.choices[type])
        nextItemId = itemIds[0]
        nextModelId = self.avatar.choices[type][nextItemId][0]
        nextTextureId = self.avatar.choices[type][nextItemId][1]
        if dataId not in itemIds:
            currIdx = -1
            currModelId = nextModelId
            currTextureId = -1
        else:
            currIdx = itemIds.index(dataId)
        for idx in range(currIdx + 1, len(itemIds)):
            itemId = itemIds[idx]
            if self.main.pirate.style.gender == 'f':
                modelId = ItemGlobals.getFemaleModelId(itemId)
                textureId = ItemGlobals.getFemaleTextureId(itemId)
            else:
                modelId = ItemGlobals.getMaleModelId(itemId)
                textureId = ItemGlobals.getMaleTextureId(itemId)
            if modelId == currModelId and textureId > currTextureId:
                nextItemId = itemId
                nextModelId = modelId
                nextTextureId = textureId
                break

        if nextItemId == itemIds[0]:
            currTextureId = -1
            for itemId in itemIds:
                if self.main.pirate.style.gender == 'f':
                    modelId = ItemGlobals.getFemaleModelId(itemId)
                    textureId = ItemGlobals.getFemaleTextureId(itemId)
                else:
                    modelId = ItemGlobals.getMaleModelId(itemId)
                    textureId = ItemGlobals.getMaleTextureId(itemId)
                nextItemId = itemId
                nextModelId = modelId
                nextTextureId = textureId
                if modelId == currModelId and textureId > currTextureId:
                    break

        return (
         nextItemId, nextModelId, nextTextureId)

    def getLastClothingTexture(self, type):
        dataId, dyeItem, color = self.avatar.currentClothing[type]
        if self.main.pirate.style.gender == 'f':
            currModelId = ItemGlobals.getFemaleModelId(dataId)
            currTextureId = ItemGlobals.getFemaleTextureId(dataId)
        else:
            currModelId = ItemGlobals.getMaleModelId(dataId)
            currTextureId = ItemGlobals.getMaleTextureId(dataId)
        itemIds = self.getSortedKeysByModelId(self.avatar.choices[type])
        lastItemId = itemIds[-1]
        lastModelId = self.avatar.choices[type][lastItemId][0]
        lastTextureId = self.avatar.choices[type][lastItemId][1]
        if dataId not in itemIds:
            currIdx = len(itemIds)
            currModelId = lastModelId
            currTextureId = lastTextureId + 1
        else:
            currIdx = itemIds.index(dataId)
        for idx in range(currIdx, -1, -1):
            itemId = itemIds[idx]
            if self.main.pirate.style.gender == 'f':
                modelId = ItemGlobals.getFemaleModelId(itemId)
                textureId = ItemGlobals.getFemaleTextureId(itemId)
            else:
                modelId = ItemGlobals.getMaleModelId(itemId)
                textureId = ItemGlobals.getMaleTextureId(itemId)
            if modelId == currModelId and textureId < currTextureId:
                lastItemId = itemId
                lastModelId = modelId
                lastTextureId = textureId
                break

        if lastItemId == itemIds[-1]:
            currTextureId = 99999
            for idx in range(len(itemIds) - 1, -1, -1):
                itemId = itemIds[idx]
                if self.main.pirate.style.gender == 'f':
                    modelId = ItemGlobals.getFemaleModelId(itemId)
                    textureId = ItemGlobals.getFemaleTextureId(itemId)
                else:
                    modelId = ItemGlobals.getMaleModelId(itemId)
                    textureId = ItemGlobals.getMaleTextureId(itemId)
                lastItemId = itemId
                lastModelId = modelId
                lastTextureId = textureId
                if modelId == currModelId and textureId < currTextureId:
                    break

        return (
         lastItemId, lastModelId, lastTextureId)

    def getClothingSize(self, type):
        size = 0
        return len(self.avatar.choices[type])

    def hidePirate(self):
        self.avatar.body.hide()
        self.avatar.hair.hide()
        self.avatar.teeth.hide()
        self.avatar.eyes.hide()

    def showPirate(self):
        self.avatar.body.show()
        self.avatar.hair.show()
        self.avatar.teeth.show()
        self.avatar.eyes.show()

    def hideOtherClothes(self, type):
        clothes = [
         'SHIRT', 'VEST', 'PANT', 'COAT', 'BELT', 'SHOE', 'HAT']
        clothes.remove(type)
        for i in clothes:
            for k in self.avatar.clothesByType[i]:
                k.hide()

    def showOtherClothes(self, type):
        clothes = ['SHIRT', 'VEST', 'PANT', 'COAT', 'BELT', 'SHOE', 'HAT']
        clothes.remove(type)
        for i in clothes:
            for k in self.avatar.clothesByType[i]:
                k.show()

    def handleClothingChanged(self):
        if self.avatar.currentClothing['SHIRT'][1]:
            if self.main.pirate.style.gender == 'm':
                self.maleShirtColorFrameTitle.show()
            else:
                self.femaleShirtColorFrameTitle.show()
        else:
            if self.main.pirate.style.gender == 'm':
                self.maleShirtColorFrameTitle.hide()
            else:
                self.femaleShirtColorFrameTitle.hide()
            if self.avatar.currentClothing['VEST'][1]:
                if self.main.pirate.style.gender == 'm':
                    self.maleVestColorFrameTitle.show()
                else:
                    self.femaleVestColorFrameTitle.show()
            else:
                if self.main.pirate.style.gender == 'm':
                    self.maleVestColorFrameTitle.hide()
                else:
                    self.femaleVestColorFrameTitle.hide()
                if self.avatar.currentClothing['PANT'][1]:
                    if self.main.pirate.style.gender == 'm':
                        self.maleBotColorFrameTitle.show()
                    else:
                        self.femaleBotColorFrameTitle.show()
                elif self.main.pirate.style.gender == 'm':
                    self.maleBotColorFrameTitle.hide()
                else:
                    self.femaleBotColorFrameTitle.hide()
                if self.avatar.currentClothing['BELT'][1]:
                    if self.main.pirate.style.gender == 'm':
                        self.maleBeltColorFrameTitle.show()
                    else:
                        self.femaleBeltColorFrameTitle.show()
                if self.main.pirate.style.gender == 'm':
                    self.maleBeltColorFrameTitle.hide()
                self.femaleBeltColorFrameTitle.hide()
        self.avatar.currentClothing['HAIR'] = [
         self.main.pirate.style.getHairHair(), self.main.pirate.style.getHairColor()]
        self.avatar.handleClothesHiding()
