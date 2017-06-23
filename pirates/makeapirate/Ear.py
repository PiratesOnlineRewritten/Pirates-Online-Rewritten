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

class Ear(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('Ear')

    def __init__(self, main=None):
        self.main = main.main
        self.parent = main.parent
        self.avatar = main.avatar
        self.mode = None
        self.load()
        return

    def enter(self):
        self.notify.debug('enter')
        self.showEarCollections()
        self.loadExtraArgs()
        if self.mode == None:
            self.mode = -1
        return

    def exit(self):
        self.hide()

    def load(self):
        self.notify.debug('loading ear')
        self.setupButtons()
        self.loadGUI()
        self.loadExtraArgs()

    def loadGUI(self):
        global sliderRange
        customRange = (-1.0, 1.0)
        if self.main.wantMarketingViewer:
            sliderRange = (-1.0, 1.0)
        self.pgs1 = CharGuiSlider(self.main, parent=self.earFrame, text=PLocalizer.EarScale, range=sliderRange, command=self.updateControlShape)
        self.pgs1.setPos(-0.4, 0, -0.3)
        self.pgs2 = CharGuiSlider(self.main, parent=self.earFrame, text=PLocalizer.EarFlapAngle, range=sliderRange, command=self.updateControlShape)
        self.pgs2.setPos(-0.4, 0, -0.55)
        self.pgs3 = CharGuiSlider(self.main, parent=self.earFrame, text=PLocalizer.EarPosition, range=sliderRange, command=self.updateControlShape)
        self.pgs3.setPos(-0.4, 0, -0.8)
        self.pgs = [
         self.pgs1, self.pgs2, self.pgs3]

    def unload(self):
        self.notify.debug('called ear unload')
        del self.main
        del self.parent
        del self.avatar

    def loadExtraArgs(self):
        self.pgs1['extraArgs'] = [
         self.pgs1, 'earScale']
        self.pgs2['extraArgs'] = [self.pgs2, 'earFlap']
        self.pgs3['extraArgs'] = [self.pgs3, 'earPosition']

    def showEarCollections(self):
        self.earFrame.show()

    def hideEarCollections(self):
        self.earFrame.hide()

    def hide(self):
        self.hideEarCollections()
        self.saveDNA()

    def setupButtons(self):
        self.earFrame = DirectFrame(parent=self.parent, relief=None, text=PLocalizer.EarFrameTitle, text_fg=(1,
                                                                                                             1,
                                                                                                             1,
                                                                                                             1), text_scale=0.18, text_pos=(0, -0.05), pos=(0,
                                                                                                                                                            0,
                                                                                                                                                            0), scale=0.7)
        self.earFrame.hide()
        return

    def saveDNA(self):
        self.avatar.pirate.setEarScale(self.pgs1.node().getValue())
        self.avatar.pirate.setEarFlapAngle(self.pgs2.node().getValue())
        self.avatar.pirate.setEarPosition(self.pgs3.node().getValue())

    def restore(self):
        self.pgs1.node().setValue(self.avatar.dna.getEarScale())
        self.pgs2.node().setValue(self.avatar.dna.getEarFlapAngle())
        self.pgs3.node().setValue(self.avatar.dna.getEarPosition())

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