from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.reputation import ReputationGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.DialMeter import DialMeter
from pirates.piratesgui.ChangeDialMeter import ChangeDialMeter
from pirates.uberdog.UberDogGlobals import InventoryType
from direct.interval.IntervalGlobal import *

class ReputationMeterDial(DirectFrame):

    def __init__(self, category, width=0.4):
        DirectFrame.__init__(self, state=DGG.DISABLED, relief=None)
        self.initialiseoptions(ReputationMeterDial)
        self.category = category
        self.level = 0
        self.value = 0
        self.max = 0
        self.masteredIval = None
        name = self.getCategoryName()
        self.changeMeter = ChangeDialMeter(parent=self, meterColor=VBase4(0.7, 0.0, 0.0, 1), meterColor2=VBase4(0.7, 0.7, 0.0, 1), baseColor=VBase4(0.1, 0.1, 0.1, 1), wantCover=0, scale=0.45)
        self.changeMeter.hide()
        self.meter = DialMeter(parent=self, meterColor=VBase4(0.7, 0.0, 0.0, 1), baseColor=VBase4(0.1, 0.1, 0.1, 1), wantCover=0, scale=0.45)
        self.meter.setBackwards()
        self.lastLevel = None
        self.lastExp = None
        self.mastered = False
        self.categoryLabel = DirectLabel(parent=self, state=DGG.DISABLED, relief=None, text=name, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getInterfaceFont(), pos=(0,
                                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                                           0), textMayChange=1)
        self.levelLabel = DirectLabel(parent=self, state=DGG.DISABLED, relief=None, text='', text_scale=0.08, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_font=PiratesGlobals.getPirateFont(), pos=(-0.015, 0, -0.08), textMayChange=1)
        logoModel = loader.loadModel('models/gui/potcLogo')
        guiModel = loader.loadModel('models/gui/toplevel_gui')
        self.valueLabel = DirectLabel(parent=self, state=DGG.DISABLED, relief=None, text='', text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getInterfaceFont(), pos=(0.0,
                                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                                      -0.2), textMayChange=1)
        self.levelCapScroll = DirectFrame(parent=self, relief=None, image=guiModel.find('**/main_gui_quest_scroll'), image_scale=(0.13,
                                                                                                                                  1.0,
                                                                                                                                  0.09), pos=(0.0, 0.0, -0.1625))
        self.levelCapScroll.hide()
        self.levelCapIcon = DirectFrame(parent=self, relief=None, image=logoModel.find('**/skull'), image_pos=(0.0,
                                                                                                               0.0,
                                                                                                               0.0), image_scale=0.9, pos=(-0.0275, 0.0, -0.105))
        self.levelCapIcon.hide()
        self.levelCapScroll.setTransparency(1)
        self.levelCapIcon.setTransparency(1)
        self.valueLabel.setTransparency(1)
        return

    def destroy(self):
        DirectFrame.destroy(self)
        if self.masteredIval:
            self.masteredIval.pause()
            self.masteredIval = None
        return

    def hideMasterOrnament(self):
        self.levelCapScroll.hide()
        self.levelCapIcon.hide()
        self.levelLabel.show()

    def showMasterOrnament(self):
        self.levelCapScroll.show()
        self.levelCapIcon.show()
        self.levelLabel.hide()
        self.mastered = True

    def masteredFX(self):
        if self.masteredIval:
            self.masteredIval.start()
            return
        startColor = Vec4(1.0, 1.0, 1.0, 0.0)
        endColor = Vec4(1.0, 1.0, 1.0, 1.0)
        duration = 1.5
        fade = Parallel(LerpColorScaleInterval(self.levelCapScroll, duration, endColor, startColor, blendType='easeInOut'), LerpColorScaleInterval(self.levelCapIcon, duration, endColor, startColor, blendType='easeInOut'), LerpColorScaleInterval(self.valueLabel, duration, endColor, startColor, blendType='easeInOut'))
        startScale = Vec3(0.75, 0.75, 0.75)
        endScale = Vec3(1.0, 1.0, 1.0)
        duration = 1.0
        scale = Parallel(LerpScaleInterval(self.levelCapScroll, duration, endScale, startScale, blendType='easeInOut'), LerpScaleInterval(self.levelCapIcon, duration, endScale, startScale * 0.1, blendType='easeInOut'), LerpScaleInterval(self.valueLabel, duration, endScale, startScale, blendType='easeInOut'))
        self.masteredIval = Parallel(fade, scale)
        self.masteredIval.start()

    def update(self, value, updateLocal=0):
        if self.mastered:
            return
        self.value = value
        level, leftoverValue = ReputationGlobals.getLevelFromTotalReputation(self.category, value)
        self.max = ReputationGlobals.getReputationNeededToLevel(self.category, level)
        self.levelLabel['text'] = '%s' % level
        if self.category == InventoryType.OverallRep:
            levelCap = ReputationGlobals.GlobalLevelCap
            if updateLocal and level != self.level:
                localAvatar.setLevel(level)
        else:
            levelCap = ReputationGlobals.LevelCap
        self.level = level
        if level == levelCap:
            self.levelLabel['text_fg'] = PiratesGuiGlobals.TextFG4
            self.valueLabel['text_fg'] = PiratesGuiGlobals.TextFG1
            self.valueLabel['text_scale'] = 0.043
            self.valueLabel['text'] = PLocalizer.RepCapText_Overall % level
            self.categoryLabel.hide()
            self.meter.meterFaceHalf1.hide()
            self.meter.meterFaceHalf2.hide()
            self.meter.meterFace.setColor(0.1, 0.4, 0.1, 1.0)
            self.valueLabel.setZ(0.03)
            self.showMasterOrnament()
            self.masteredFX()
        else:
            self.levelLabel['text_fg'] = PiratesGuiGlobals.TextFG1
            self.meter.show()
            self.categoryLabel.show()
            self.valueLabel['text'] = '%s / %s' % (leftoverValue, self.max)
            self.valueLabel['text_scale'] = PiratesGuiGlobals.TextScaleLarge
            self.valueLabel['text_fg'] = PiratesGuiGlobals.TextFG2
            self.valueLabel.setZ(0.0)
            self.meter.update(leftoverValue, self.max)
            self.hideMasterOrnament()
            if self.lastLevel == None:
                self.lastLevel = level
            if self.lastExp == None:
                if hasattr(base, 'localAvatar'):
                    self.lastExp = localAvatar.getInventory().getReputation(self.category)
            if self.lastExp:
                expChange = value - self.lastExp
                if expChange and localAvatar.getGameState() != 'Fishing':
                    localAvatar.guiMgr.gameGui.createExpAlert(expChange, 4.0, Vec3(-0.93, 0.0, 0.75), Vec3(0.0, 0.0, 0.25))
            if self.lastLevel != level:
                self.lastLevel = level
                glowFrameColor = Vec4(0.7, 0.0, 0.0, 1.0)
                glowLevelColor = Vec4(0.8, 0.0, 0.0, 1.0)
                startFrameColor = self.meter.meterFace.getColor()
                startLevelColor = Vec4(0.9, 0.8, 0.63, 1.0)
                startFrameScale = self.meter.meterFace.getScale()
                startLevelScale = self.levelLabel.getScale()
                scale = Vec3(1.2, 1.2, 1.2)
                objFrame = self.meter.meterFace
                objLevel = self.levelLabel
                levelUpIval = Sequence(Func(self.meter.meterFaceHalf1.hide), Func(self.meter.meterFaceHalf2.hide), Parallel(LerpColorInterval(objFrame, 3.0, startFrameColor, glowFrameColor, blendType='easeInOut'), LerpColorInterval(objLevel, 3.0, startLevelColor, glowLevelColor, blendType='easeInOut'), Sequence(LerpScaleInterval(objLevel, 0.25, scale, startFrameScale, blendType='easeInOut'), LerpScaleInterval(objLevel, 2.0, startFrameScale, blendType='easeInOut'))), Func(self.meter.meterFaceHalf1.show), Func(self.meter.meterFaceHalf2.show), Func(objLevel.clearColor))
                levelUpIval.start()
            else:
                if self.lastExp is not None:
                    if self.lastExp == value:
                        return
                self.lastExp = value
                glowFrameColor = Vec4(1.0, 0, 0, 1.0)
                startFrameColorA = self.meter.meterFaceHalf1.getColor()
                startFrameColorB = self.meter.meterFaceHalf2.getColor()
                objFrameA = self.meter.meterFaceHalf1
                objFrameB = self.meter.meterFaceHalf2
                objFrameC = self.meter.meterFace
                if leftoverValue and float(self.max) / float(leftoverValue) > 2.0:
                    expUpIval = Sequence(LerpColorScaleInterval(objFrameA, 0.2, glowFrameColor, blendType='easeInOut'), Wait(0.2), LerpColorScaleInterval(objFrameA, 0.5, startFrameColorA, blendType='easeInOut'), LerpColorScaleInterval(objFrameA, 0.1, glowFrameColor, blendType='easeInOut'), Wait(0.1), LerpColorScaleInterval(objFrameA, 0.3, startFrameColorA, blendType='easeInOut'))
                else:
                    expUpIval = Sequence(Parallel(LerpColorScaleInterval(objFrameA, 0.2, glowFrameColor, blendType='easeInOut'), LerpColorScaleInterval(objFrameB, 0.2, glowFrameColor, blendType='easeInOut')), Wait(0.2), Parallel(LerpColorScaleInterval(objFrameA, 0.5, startFrameColorA, blendType='easeInOut'), LerpColorScaleInterval(objFrameB, 0.5, startFrameColorA, blendType='easeInOut')), Parallel(LerpColorScaleInterval(objFrameA, 0.1, glowFrameColor, blendType='easeInOut'), LerpColorScaleInterval(objFrameB, 0.1, glowFrameColor, blendType='easeInOut')), Wait(0.1), Parallel(LerpColorScaleInterval(objFrameA, 0.3, startFrameColorA, blendType='easeInOut'), LerpColorScaleInterval(objFrameB, 0.3, startFrameColorA, blendType='easeInOut')))
                expUpIval.start()
        return

    def updateChange(self, value, newValue):
        self.value = value
        level, leftoverValue = ReputationGlobals.getLevelFromTotalReputation(self.category, value + newValue)
        self.max = ReputationGlobals.getReputationNeededToLevel(self.category, level)
        self.levelLabel['text'] = '%s' % level
        oldValue = leftoverValue - newValue
        if oldValue < 0:
            oldValue = 0
        if self.category == InventoryType.OverallRep:
            levelCap = ReputationGlobals.GlobalLevelCap
        else:
            levelCap = ReputationGlobals.LevelCap
        if level == levelCap:
            self.levelLabel['text_fg'] = PiratesGuiGlobals.TextFG4
            self.valueLabel['text_fg'] = PiratesGuiGlobals.TextFG1
            self.valueLabel['text_scale'] = 0.043
            self.valueLabel['text'] = PLocalizer.RepCapText_Overall % level
            self.categoryLabel.hide()
            self.meter.meterFaceHalf1.hide()
            self.meter.meterFaceHalf2.hide()
            self.meter.meterFace.setColor(0.1, 0.4, 0.1, 1.0)
            self.valueLabel.setZ(0.03)
            self.showMasterOrnament()
            self.masteredFX()
        else:
            self.levelLabel['text_fg'] = PiratesGuiGlobals.TextFG1
            self.categoryLabel.show()
            self.valueLabel.hide()
            self.changeMeter.update(oldValue, leftoverValue, self.max)
            self.changeMeter.show()
            self.meter.hide()
            self.hideMasterOrnament()

    def setCategory(self, category):
        self.category = category
        name = self.getCategoryName()
        self.categoryLabel['text'] = name

    def getCategory(self):
        return self.category

    def getCategoryName(self):
        return PLocalizer.InventoryTypeNames[self.category]