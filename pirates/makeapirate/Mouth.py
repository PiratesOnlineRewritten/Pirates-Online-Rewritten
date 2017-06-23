from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShowBaseGlobal import *
from direct.showbase import DirectObject
from direct.fsm import StateData
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from CharGuiBase import CharGuiSlider, CharGuiPicker
import random
damper = 0.5
sliderRange = (-0.5, 0.5)

class Mouth(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('Mouth')

    def __init__(self, main=None):
        self.main = main.main
        self.parent = main.parent
        self.avatar = main.avatar
        self.mode = None
        self.load()
        return

    def enter(self):
        self.notify.debug('enter')
        self.showMouthCollections()
        self.loadExtraArgs()
        if self.mode == None:
            self.mode = -1
        return

    def exit(self):
        self.hide()

    def load(self):
        self.notify.debug('loading mouth')
        self.setupButtons()
        self.loadGUI()
        self.loadExtraArgs()

    def loadGUI(self):
        customRange = (-1.0, 1.0)
        self.pgs1 = CharGuiSlider(self.main, parent=self.jawFrame, text=PLocalizer.MouthJawWidth, command=self.updateControlShape, range=customRange)
        self.pgs1.setPos(-0.4, 0, -0.3)
        self.pgs2 = CharGuiSlider(self.main, parent=self.jawFrame, text=PLocalizer.MouthJawLength, command=self.updateControlShape, range=customRange)
        self.pgs2.setPos(-0.4, 0, -0.55)
        self.pgs3 = CharGuiSlider(self.main, parent=self.jawFrame, text=PLocalizer.MouthJawChinAngle, command=self.updateControlShape, range=customRange)
        self.pgs3.setPos(-0.4, 0, -0.8)
        self.pgs4 = CharGuiSlider(self.main, parent=self.jawFrame, text=PLocalizer.MouthJawChinSize, command=self.updateControlShape, range=customRange)
        self.pgs4.setPos(-0.4, 0, -1.05)
        self.pgs5 = CharGuiSlider(self.main, parent=self.lipFrame, text=PLocalizer.MouthWidth, command=self.updateControlShape, range=(-1.0,
                                                                                                                                       0.0))
        self.pgs5.setPos(-0.4, 0, -0.3)
        self.pgs6 = CharGuiSlider(self.main, parent=self.lipFrame, text=PLocalizer.MouthThickness, command=self.updateControlShape, range=customRange)
        self.pgs6.setPos(-0.4, 0, -0.55)
        self.pgs8 = CharGuiSlider(self.main, parent=self.cheekFrame, text=PLocalizer.CheekFat, command=self.updateControlShape, range=customRange)
        self.pgs8.setPos(-0.4, 0, -0.3)
        self.pgs = [
         self.pgs1, self.pgs2, self.pgs3, self.pgs4, self.pgs5, self.pgs6, self.pgs8]

    def unload(self):
        self.notify.debug('called Mouth unload')
        del self.main
        del self.parent
        del self.avatar

    def loadExtraArgs(self):
        self.pgs1['extraArgs'] = [
         self.pgs1, 'jawWidth']
        self.pgs2['extraArgs'] = [self.pgs2, 'jawLength']
        self.pgs3['extraArgs'] = [self.pgs3, 'jawChinAngle', 135]
        self.pgs4['extraArgs'] = [self.pgs4, 'jawChinSize']
        self.pgs5['extraArgs'] = [self.pgs5, 'mouthWidth']
        self.pgs6['extraArgs'] = [self.pgs6, 'mouthLipThickness']
        self.pgs8['extraArgs'] = [self.pgs8, 'cheekFat']

    def showMouthCollections(self):
        self.jawFrame.show()
        self.lipFrame.show()
        self.cheekFrame.show()

    def hideMouthCollections(self):
        self.jawFrame.hide()
        self.lipFrame.hide()
        self.cheekFrame.hide()
        self.teethPicker.hide()

    def hide(self):
        self.hideMouthCollections()
        self.saveDNA()

    def setupButtons(self):
        self.jawFrame = DirectFrame(parent=self.parent, relief=None, text=PLocalizer.MouthJawFrameTitle, text_fg=(1,
                                                                                                                  1,
                                                                                                                  1,
                                                                                                                  1), text_scale=0.18, text_pos=(0, -0.05), pos=(0,
                                                                                                                                                                 0,
                                                                                                                                                                 0.4), scale=0.7)
        self.jawFrame.hide()
        self.lipFrame = DirectFrame(parent=self.parent, relief=None, text=PLocalizer.MouthFrameTitle, text_fg=(1,
                                                                                                               1,
                                                                                                               1,
                                                                                                               1), text_scale=0.18, text_pos=(0, -0.05), pos=(0, 0, -0.55), scale=0.7)
        self.lipFrame.hide()
        self.cheekFrame = DirectFrame(parent=self.parent, relief=None, text=PLocalizer.MouthCheekFrameTitle, text_fg=(1,
                                                                                                                      1,
                                                                                                                      1,
                                                                                                                      1), text_scale=0.18, text_pos=(0, -0.05), pos=(0,
                                                                                                                                                                     0,
                                                                                                                                                                     -1.4), scale=0.7)
        self.cheekFrame.hide()
        self.teethPicker = CharGuiPicker(self.main, parent=self.parent, text=PLocalizer.MouthTeethFrame, nextCommand=self.handleNextTeeth, backCommand=self.handleLastTeeth)
        self.teethPicker.setPos(0, 0, -0.3)
        self.teethPicker.hide()
        return

    def saveDNA(self):
        self.avatar.pirate.setJawWidth(self.pgs1.node().getValue())
        self.avatar.pirate.setJawLength(self.pgs2.node().getValue())
        self.avatar.pirate.setJawAngle(self.pgs3.node().getValue())
        self.avatar.pirate.setJawRoundness(self.pgs4.node().getValue())
        self.avatar.pirate.setMouthWidth(self.pgs5.node().getValue())
        self.avatar.pirate.setMouthLipThickness(self.pgs6.node().getValue())
        self.avatar.pirate.setCheekFat(self.pgs8.node().getValue())

    def restore(self):
        self.pgs1.node().setValue(self.avatar.dna.getJawWidth())
        self.pgs2.node().setValue(self.avatar.dna.getJawLength())
        self.pgs3.node().setValue(self.avatar.dna.getJawAngle())
        self.pgs4.node().setValue(self.avatar.dna.getJawRoundness())
        self.pgs5.node().setValue(self.avatar.dna.getMouthWidth())
        self.pgs6.node().setValue(self.avatar.dna.getMouthLipThickness())
        self.pgs8.node().setValue(self.avatar.dna.getCheekFat())

    def reset(self):
        for i in xrange(0, len(self.pgs)):
            self.resetSlider(self.pgs[i])

        self.saveDNA()

    def resetSlider(self, slider):
        slider.node().setValue(0.0)

    def randomPick(self):
        global damper
        damper = 1.0
        for i in xrange(0, len(self.pgs)):
            slider = self.pgs[i]
            self.resetSlider(slider)
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

    def updateControlShape(self, pgs, extraArgs1=None, extraArgs2=None):
        if extraArgs1 != None:
            self.avatar.pirate.setControlValue(pgs.node().getValue(), extraArgs1)
        self.main.handleQuarterView(extraArgs2)
        return

    def handleNextTeeth(self):
        if not self.avatar.tooths[self.avatar.toothIdx].isEmpty():
            self.avatar.tooths[self.avatar.toothIdx][0].hide()
        self.avatar.toothIdx += 1
        if self.avatar.toothIdx >= len(self.avatar.tooths):
            self.avatar.toothIdx = 0
        if not self.avatar.tooths[self.avatar.toothIdx].isEmpty():
            self.avatar.tooths[self.avatar.toothIdx][0].show()

    def handleLastTeeth(self):
        if not self.avatar.tooths[self.avatar.toothIdx].isEmpty():
            self.avatar.tooths[self.avatar.toothIdx][0].hide()
        self.avatar.toothIdx -= 1
        if self.avatar.toothIdx < 0:
            self.avatar.toothIdx = len(self.avatar.tooths) - 1
        if not self.avatar.tooths[self.avatar.toothIdx].isEmpty():
            self.avatar.tooths[self.avatar.toothIdx][0].show()