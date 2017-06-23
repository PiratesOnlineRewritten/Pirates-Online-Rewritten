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
import random
damper = 0.5
sliderRange = (-0.5, 0.5)

class Eyes(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('Eyes')

    def __init__(self, main=None):
        self.main = main.main
        self.parent = main.parent
        self.avatar = main.avatar
        self.mode = None
        self.load()
        return

    def enter(self):
        self.notify.debug('enter')
        self.showEyesCollections()
        self.loadExtraArgs()
        if self.mode == None:
            self.mode = -1
        return

    def exit(self):
        self.hide()

    def load(self):
        self.notify.debug('loading eyes')
        self.setupButtons()
        self.loadGUI()
        self.loadExtraArgs()

    def loadGUI(self):
        customRrange = (-1.0, 1.0)
        self.pgs1 = CharGuiSlider(self.main, parent=self.browFrame, text=PLocalizer.EyeBrowProtruding, range=(0.0,
                                                                                                              1.0), command=self.updateControlShape)
        self.pgs1.setPos(-0.4, 0, -0.3)
        self.pgs6 = CharGuiSlider(self.main, parent=self.eyeFrame, text=PLocalizer.EyeCorner, command=self.updateControlShape, range=(-0.25, 0.25))
        self.pgs6.setPos(-0.4, 0, -0.3)
        self.pgs7 = CharGuiSlider(self.main, parent=self.eyeFrame, text=PLocalizer.EyeOpeningSize, range=(-1,
                                                                                                          1), command=self.updateControlShape)
        self.pgs7.setPos(-0.4, 0, -0.55)
        self.pgs8 = CharGuiSlider(self.main, parent=self.eyeFrame, text=PLocalizer.EyeSpacing, range=(-1,
                                                                                                      1), command=self.updateControlShape)
        self.pgs8.setPos(-0.4, 0, -0.8)
        self.pgs = [
         self.pgs1, self.pgs6, self.pgs7, self.pgs8]

    def unload(self):
        self.notify.debug('called eyes unload')
        del self.main
        del self.parent
        del self.avatar

    def loadExtraArgs(self):
        self.pgs1['extraArgs'] = [
         self.pgs1, 'browProtruding', 135]
        self.pgs6['extraArgs'] = [self.pgs6, 'eyeCorner']
        self.pgs7['extraArgs'] = [self.pgs7, 'eyeOpeningSize']
        self.pgs8['extraArgs'] = [self.pgs8, 'eyeSpacing']

    def showEyesCollections(self):
        self.browFrame.show()
        self.eyeFrame.show()
        self.colorPicker.show()

    def hideEyesCollections(self):
        self.browFrame.hide()
        self.eyeFrame.hide()
        self.colorPicker.hide()

    def hide(self):
        self.hideEyesCollections()
        self.saveDNA()

    def setupButtons(self):
        self.browFrame = DirectFrame(parent=self.parent, relief=None, text=PLocalizer.EyeBrowFrameTitle, text_fg=(1,
                                                                                                                  1,
                                                                                                                  1,
                                                                                                                  1), text_scale=0.18, text_pos=(0, -0.05), pos=(0, 0, -0.1), scale=0.7)
        self.browFrame.hide()
        self.eyeFrame = DirectFrame(parent=self.parent, relief=None, text=PLocalizer.EyeFrameTitle, text_fg=(1,
                                                                                                             1,
                                                                                                             1,
                                                                                                             1), text_scale=0.18, text_pos=(0, -0.05), pos=(0,
                                                                                                                                                            0,
                                                                                                                                                            -1.1), scale=0.7)
        self.eyeFrame.hide()
        self.colorPicker = CharGuiPicker(self.main, parent=self.parent, text=PLocalizer.EyesColorFrameTitle, nextCommand=self.handleNextColor, backCommand=self.handleLastColor)
        self.colorPicker.setPos(0, 0, 0.2)
        self.colorPicker.hide()
        return

    def saveDNA(self):
        self.avatar.pirate.setBrowProtruding(self.pgs1.node().getValue())
        self.avatar.pirate.setEyeCorner(self.pgs6.node().getValue())
        self.avatar.pirate.setEyeOpeningSize(self.pgs7.node().getValue())
        self.avatar.pirate.setEyeBulge(self.pgs8.node().getValue())

    def restore(self):
        self.pgs1.node().setValue(self.avatar.dna.getBrowProtruding())
        self.pgs6.node().setValue(self.avatar.dna.getEyeCorner())
        self.pgs7.node().setValue(self.avatar.dna.getEyeOpeningSize())
        self.pgs8.node().setValue(self.avatar.dna.getEyeBulge())

    def reset(self):
        for i in xrange(0, len(self.pgs)):
            self.resetSlider(self.pgs[i])

        self.avatar.eyesColorIdx = 0
        self.avatar.pirate.setEyesColor(self.avatar.eyesColorIdx)
        self.avatar.pirate.generateEyesTexture()
        self.saveDNA()

    def resetSlider(self, slider):
        slider.node().setValue(0.0)

    def randomPick(self):
        global damper
        damper = 1.0
        for i in xrange(0, len(self.pgs)):
            slider = self.pgs[i]
            self.resetSlider(slider)
            if self.avatar.pirate.gender == 'f':
                if slider == self.pgs6:
                    continue
            if random.choice([0, 1]):
                value = random.random() * damper
                toss = 0
                if slider['range'][0] < 0:
                    toss = random.choice([0, 1])
                if toss:
                    slider.node().setValue(-value)
                else:
                    slider.node().setValue(value)

        self.saveDNA()
        choice = random.choice(range(0, self.avatar.numEyeColors))
        self.avatar.eyesColorIdx = choice
        self.avatar.pirate.setEyesColor(self.avatar.eyesColorIdx)
        self.avatar.pirate.generateEyesTexture()

    def handleNextColor(self):
        self.avatar.eyesColorIdx = (self.avatar.eyesColorIdx + 1) % self.avatar.numEyeColors
        self.notify.debug('new color idx %s' % self.avatar.eyesColorIdx)
        self.avatar.pirate.setEyesColor(self.avatar.eyesColorIdx)
        self.avatar.pirate.generateEyesTexture()

    def handleLastColor(self):
        self.avatar.eyesColorIdx = (self.avatar.eyesColorIdx - 1) % self.avatar.numEyeColors
        self.notify.debug('new color idx %s' % self.avatar.eyesColorIdx)
        self.avatar.pirate.setEyesColor(self.avatar.eyesColorIdx)
        self.avatar.pirate.generateEyesTexture()

    def updateControlShape(self, pgs, extraArgs1=None, extraArgs2=None):
        if extraArgs1 != None:
            self.avatar.pirate.setControlValue(pgs.node().getValue(), extraArgs1)
        self.main.handleQuarterView(extraArgs2)
        return