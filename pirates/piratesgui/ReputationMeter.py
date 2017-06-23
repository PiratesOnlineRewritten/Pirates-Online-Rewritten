from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.reputation import ReputationGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from direct.interval.IntervalGlobal import *
from pirates.uberdog.UberDogGlobals import InventoryType

class ReputationMeter(DirectFrame):

    def __init__(self, category, width=0.4):
        DirectFrame.__init__(self, parent=NodePath(), relief=None)
        self.initialiseoptions(ReputationMeter)
        self.category = category
        self.level = 0
        self.value = 0
        self.max = 0
        self.masteredIval = None
        name = PLocalizer.makeHeadingString(self.getCategoryName(), 2)
        self.categoryLabel = DirectLabel(parent=self, relief=None, text=name, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, pos=(-width * 0.5, 0, 0.02), textMayChange=1)
        self.levelLabel = DirectLabel(parent=self, relief=None, text='', text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ARight, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(width * 0.5, 0, 0.02), textMayChange=1)
        gui = loader.loadModel('models/gui/ship_battle')
        guiModel = loader.loadModel('models/gui/toplevel_gui')
        self.meter = DirectWaitBar(parent=self, relief=DGG.FLAT, state=DGG.DISABLED, range=self.max, value=self.value, frameSize=(-width * 0.5, width * 0.5, -0.01, 0.01), frameColor=(65 / 255.0, 40 / 255.0, 8 / 255.0, 1), barColor=(223 / 255.0, 137 / 255.0, 28 / 255.0, 1), pos=(0,
                                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                                       0.0))
        self.meterFrame = DirectFrame(parent=self.meter, relief=None, image=gui.find('**/ship_battle_speed_bar*'), image_scale=(width * 0.75, 1.0, 0.6), pos=(0,
                                                                                                                                                              0,
                                                                                                                                                              0.0))
        self.clamp1 = DirectFrame(parent=self.meter, relief=None, image=guiModel.find('**/groggy_clamp'), image_scale=(0.15,
                                                                                                                       1.0,
                                                                                                                       0.4), image_color=(0.8,
                                                                                                                                          0.8,
                                                                                                                                          0.8,
                                                                                                                                          1.0), pos=(-width * 0.333, 0, 0))
        self.clamp2 = DirectFrame(parent=self.meter, relief=None, image=guiModel.find('**/groggy_clamp'), image_scale=(0.15,
                                                                                                                       1.0,
                                                                                                                       0.4), image_color=(0.8,
                                                                                                                                          0.8,
                                                                                                                                          0.8,
                                                                                                                                          1.0), pos=(-width * 0.167, 0, 0))
        self.clamp3 = DirectFrame(parent=self.meter, relief=None, image=guiModel.find('**/groggy_clamp'), image_scale=(0.15,
                                                                                                                       1.0,
                                                                                                                       0.4), image_color=(0.8,
                                                                                                                                          0.8,
                                                                                                                                          0.8,
                                                                                                                                          1.0), pos=(0,
                                                                                                                                                     0,
                                                                                                                                                     0))
        self.clamp4 = DirectFrame(parent=self.meter, relief=None, image=guiModel.find('**/groggy_clamp'), image_scale=(0.15,
                                                                                                                       1.0,
                                                                                                                       0.4), image_color=(0.8,
                                                                                                                                          0.8,
                                                                                                                                          0.8,
                                                                                                                                          1.0), pos=(width * 0.167, 0, 0))
        self.clamp5 = DirectFrame(parent=self.meter, relief=None, image=guiModel.find('**/groggy_clamp'), image_scale=(0.15,
                                                                                                                       1.0,
                                                                                                                       0.4), image_color=(0.8,
                                                                                                                                          0.8,
                                                                                                                                          0.8,
                                                                                                                                          1.0), pos=(width * 0.333, 0, 0))
        self.valueLabel = DirectLabel(parent=self.meter, relief=None, text='', text_scale=PiratesGuiGlobals.TextScaleMed, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getInterfaceFont(), text_pos=(0,
                                                                                                                                                                                                                                                                                           0.032), pos=(0, 0, -0.01), textMayChange=1)
        logoModel = loader.loadModel('models/gui/potcLogo')
        self.levelCapScroll = DirectFrame(parent=self.meter, relief=None, image=guiModel.find('**/main_gui_quest_scroll'))
        self.levelCapScroll.setPos(0.0, 0.0, 0.01)
        self.levelCapScroll.setScale(0.115, 1.0, 0.05)
        self.levelCapScroll.hide()
        self.levelCapIcon = DirectFrame(parent=self.meter, relief=None, image=logoModel.find('**/skull'))
        self.levelCapIcon.setPos(0.0, 0.0, 0.025)
        self.levelCapIcon.setScale(0.4)
        self.levelCapIcon.setBin('gui-popup', 0)
        self.levelCapIcon.hide()
        self.masteredLabel = DirectLabel(parent=self.meter, relief=None, text=PLocalizer.RepCapText_Skill, text_scale=0.045, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getInterfaceFont())
        self.masteredLabel.setPos(0.0, 0.0, -0.01)
        self.masteredLabel.hide()
        self.levelCapScroll.setTransparency(1)
        self.levelCapIcon.setTransparency(1)
        self.masteredLabel.setTransparency(1)
        self.update(self.value)
        self.flattenStrong()
        return

    def hideMasterOrnament(self):
        self.levelCapScroll.hide()
        self.levelCapIcon.hide()
        self.masteredLabel.hide()

    def showMasterOrnament(self):
        self.levelCapScroll.show()
        self.levelCapIcon.show()
        self.masteredLabel.show()

    def destroy(self):
        DirectFrame.destroy(self)
        if self.masteredIval:
            self.masteredIval.pause()
            self.masteredIval = None
        return

    def masteredFX(self):
        if self.masteredIval:
            self.masteredIval.start()
            return
        startColor = Vec4(1.0, 1.0, 1.0, 0.0)
        endColor = Vec4(1.0, 1.0, 1.0, 1.0)
        duration = 1.5
        fade = Parallel(LerpColorScaleInterval(self.levelCapScroll, duration, endColor, startColor, blendType='easeInOut'), LerpColorScaleInterval(self.levelCapIcon, duration, endColor, startColor, blendType='easeInOut'), LerpColorScaleInterval(self.masteredLabel, duration, endColor, startColor, blendType='easeInOut'))
        self.masteredIval = fade
        self.masteredIval.start()

    def update(self, value, playFX=False):
        self.value = value
        level, leftoverValue = ReputationGlobals.getLevelFromTotalReputation(self.category, value)
        self.max = ReputationGlobals.getReputationNeededToLevel(self.category, level)
        self.levelLabel['text'] = PLocalizer.Level + ' %s' % level
        if self.category == InventoryType.OverallRep:
            levelcap = ReputationGlobals.GlobalLevelCap
        else:
            if self.category in [InventoryType.FishingRep, InventoryType.PotionsRep]:
                levelcap = ReputationGlobals.MinigameLevelCap
            else:
                levelcap = ReputationGlobals.LevelCap
            if level >= levelcap:
                self.levelLabel['text_fg'] = PiratesGuiGlobals.TextFG1
                self.meter['range'] = self.max
                self.meter['value'] = self.max
                self.meter['barColor'] = (180 / 255.0, 190 / 255.0, 140 / 255.0, 1)
                self.valueLabel.hide()
                self.showMasterOrnament()
                if playFX:
                    self.masteredFX()
            self.levelLabel['text_fg'] = PiratesGuiGlobals.TextFG2
            self.valueLabel.show()
            self.valueLabel['text'] = '%s / %s' % (leftoverValue, self.max)
            self.meter.show()
            self.meter['range'] = self.max
            self.meter['value'] = leftoverValue
            self.meter['barColor'] = (223 / 255.0, 137 / 255.0, 28 / 255.0, 1)
            self.hideMasterOrnament()

    def setCategory(self, category):
        self.category = category
        name = PLocalizer.makeHeadingString(self.getCategoryName(), 2)
        self.categoryLabel['text'] = name

    def getCategory(self):
        return self.category

    def getCategoryName(self):
        return PLocalizer.InventoryTypeNames[self.category]