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

class Shape(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('Shape')

    def __init__(self, main=None):
        self.main = main.main
        self.parent = main.parent
        self.avatar = main.avatar
        self.mode = None
        self.once = False
        self.load()
        return

    def enter(self):
        self.notify.debug('enter')
        self.showShapeCollections()
        self.loadExtraArgs()
        if self.mode == None:
            self.mode = -1
        return

    def exit(self):
        self.hide()

    def load(self):
        self.notify.debug('loading shape')
        self.setupButtons()
        self.loadGUI()
        self.loadExtraArgs()

    def loadGUI(self):
        global sliderRange
        customRange = (
         -0.5, 0.5)
        if self.main.wantMarketingViewer:
            sliderRange = (-1.0, 1.0)
        self.pgsScale = CharGuiSlider(self.main, parent=self.headFrame, text=PLocalizer.BodyHeadScale, command=self.updateHeadSlider, range=sliderRange)
        self.pgsScale.setPos(-0.4, 0, -0.2)
        self.pgsScale['extraArgs'] = [self.pgsScale, 0, 0]
        self.pgs1 = CharGuiSlider(self.main, parent=self.headFrame, text=PLocalizer.ShapeHeadWidth, command=self.updateControlShape, range=sliderRange)
        self.pgs1.setPos(-0.4, 0, -0.45)
        self.pgs2 = CharGuiSlider(self.main, parent=self.headFrame, text=PLocalizer.ShapeHeadHeight, command=self.updateControlShape, range=sliderRange)
        self.pgs2.setPos(-0.4, 0, -0.7)
        customRange = (0.0, 1.0)
        self.pgs3 = CharGuiSlider(self.main, parent=self.headFrame, text=PLocalizer.ShapeHeadRoundness, command=self.updateControlShape, range=customRange)
        self.pgs3.setPos(-0.4, 0, -0.95)
        self.pgs = [
         self.pgs1, self.pgs2, self.pgs3, self.pgsScale]

    def unload(self):
        self.notify.debug('called Shape unload')
        del self.main
        del self.parent
        del self.avatar

    def loadExtraArgs(self):
        self.pgs1['extraArgs'] = [
         self.pgs1, 'headWidth']
        self.pgs2['extraArgs'] = [self.pgs2, 'headHeight']
        self.pgs3['extraArgs'] = [self.pgs3, 'headRoundness']

    def showShapeCollections(self):
        self.headFrame.show()
        self.texturePicker.show()

    def hideShapeCollections(self):
        self.headFrame.hide()
        self.texturePicker.hide()

    def hide(self):
        self.hideShapeCollections()
        self.saveDNA()
        if self.main.inRandomAll:
            return
        if self.once:
            idx = 0
            if self.main.pirate.gender == 'f':
                idx = 1
            optionsLeft = len(self.main.JSD_FACE[idx])
            if optionsLeft:
                choice = random.choice(range(0, optionsLeft))
                if self.main.lastDialog:
                    self.main.lastDialog.stop()
                dialog = self.main.JSD_FACE[idx][choice]
                base.playSfx(dialog, node=self.avatar.pirate)
                self.main.lastDialog = dialog
                self.main.JSD_FACE[idx].remove(dialog)
        else:
            self.once = True

    def setupButtons(self):
        self.texturePicker = CharGuiPicker(self.main, parent=self.parent, text=PLocalizer.ShapeTextureFrameTitle, nextCommand=self.handleNextTexture, backCommand=self.handleLastTexture)
        self.texturePicker.setPos(0, 0, 0)
        self.texturePicker.hide()
        self.headFrame = DirectFrame(parent=self.parent, relief=None, pos=(0, 0, -0.3), scale=0.7)
        self.headFrame.hide()
        return

    def saveDNA(self):
        self.avatar.pirate.setHeadWidth(self.pgs1.node().getValue())
        self.avatar.pirate.setHeadHeight(self.pgs2.node().getValue())
        self.avatar.pirate.setHeadRoundness(self.pgs3.node().getValue())
        self.avatar.pirate.setHeadTexture(self.avatar.faceTextureIdx)

    def restore(self):
        self.pgs1.node().setValue(self.avatar.dna.getHeadWidth())
        self.pgs2.node().setValue(self.avatar.dna.getHeadHeight())
        self.pgs3.node().setValue(self.avatar.dna.getHeadRoundness())
        self.pgsScale.node().setValue(self.avatar.dna.getHeadSize())

    def reset(self):
        for i in xrange(0, len(self.pgs)):
            self.resetSlider(self.pgs[i])

        self.avatar.faceTextureIdx = 0
        self.avatar.pirate.setHeadTexture(self.avatar.faceTextureIdx)
        self.avatar.pirate.generateFaceTexture()
        self.saveDNA()

    def resetSlider(self, slider):
        slider.node().setValue(0.0)
        if slider == self.pgsScale:
            self.updateHeadSlider(slider)

    def randomPick(self):
        global damper
        damper = 1.0
        for i in xrange(0, len(self.pgs)):
            slider = self.pgs[i]
            self.resetSlider(slider)
            if self.avatar.pirate.gender == 'f':
                if slider == self.pgs3:
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
                if slider == self.pgsScale:
                    self.updateHeadSlider(slider)

        self.avatar.faceTextureIdx = random.choice(self.avatar.choices['FACE'])
        self.saveDNA()
        self.avatar.pirate.generateFaceTexture()

    def updateControlShape(self, pgs, extraArgs1=None, extraArgs2=None):
        if extraArgs1 != None:
            self.avatar.pirate.setControlValue(pgs.node().getValue(), extraArgs1)
        self.main.handleQuarterView(extraArgs2)
        return

    def updateHeadSlider(self, pgs, extraArgs1=None, extraArgs2=None):
        value = pgs.node().getValue()
        mappedValue = 0.9 + (1 + value) * 0.1
        if extraArgs1 == 0:
            self.avatar.pirate.setHeadSize(value)
        self.notify.debug('head slider value %s' % value)
        self.notify.debug('mapped value %s' % mappedValue)
        cjExtra = self.avatar.pirate.findAllMatches('**/def_extra_jt')
        if not cjExtra.isEmpty():
            prevScale = cjExtra[0].getScale()
            if extraArgs1 == 0:
                cjExtra[0].setScale(2 - mappedValue, mappedValue, prevScale[2])

    def handleNextTexture(self):
        currIdx = self.avatar.choices['FACE'].index(self.avatar.faceTextureIdx)
        currIdx += 1
        if currIdx >= len(self.avatar.choices['FACE']):
            currIdx = 0
        self.avatar.faceTextureIdx = self.avatar.choices['FACE'][currIdx]
        self.avatar.pirate.setHeadTexture(self.avatar.faceTextureIdx)
        self.avatar.pirate.generateFaceTexture()

    def handleLastTexture(self):
        currIdx = self.avatar.choices['FACE'].index(self.avatar.faceTextureIdx)
        currIdx -= 1
        if currIdx < 0:
            currIdx = len(self.avatar.choices['FACE']) - 1
        self.avatar.faceTextureIdx = self.avatar.choices['FACE'][currIdx]
        self.avatar.pirate.setHeadTexture(self.avatar.faceTextureIdx)
        self.avatar.pirate.generateFaceTexture()