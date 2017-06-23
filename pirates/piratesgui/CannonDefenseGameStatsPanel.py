from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui.CannonDefenseScorePanelBase import CannonDefenseScorePanelBase
from pirates.piratesgui.CannonDefenseScorePanelBase import RoundCompleteFlags
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
import math

class CannonDefenseGameStatsPanel(CannonDefenseScorePanelBase):

    def __init__(self, roundComplete, panelNumber, numOfPanels, **kw):
        CannonDefenseScorePanelBase.__init__(self, panelNumber, numOfPanels, **kw)
        self.prevButton = None
        self.nextButton = None
        self.timePlayedTotalslbl = []
        self.goldEarnedTotalslbl = []
        self.roundComplete = roundComplete
        self._createPanel()
        return

    def _createPanel(self):
        startX = 0.77
        widthX = 0.39
        self._createHeader(self)
        self._createPlayerNames(self, self.playerLbls, startX, 0.97, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['TimePlayed'], self.timePlayedTotalslbl, startX, 0.82, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['ShipsSunkWave'], self.shipsSunkTotalslbl, startX, 0.72, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['DamageDealtWave'], self.damageTotalslbl, startX, 0.62, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['AccuracyWave'], self.accuracyTotalslbl, startX, 0.52, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['ShotsFiredWave'], self.shotsFiredTotalslbl, startX, 0.42, widthX)
        self._createStatsLabels(self, PLocalizer.CannonDefense['GoldEarned'], self.goldEarnedTotalslbl, startX, 0.32, widthX)
        self._createFooter(self)

    def _createHeader(self, myParent):
        headingTxtScale = PiratesGuiGlobals.TextScaleLarge * 3
        DirectLabel(parent=myParent, relief=None, state=DGG.DISABLED, text=PLocalizer.CannonDefense['Report'], text_scale=headingTxtScale, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0,
                                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                                               0), text_font=self.headingfont, textMayChange=0, pos=(1.2,
                                                                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                                                                     1.37))
        return

    def _createFooter(self, myParent):
        doWhatNextTxt = None
        txtScale = PiratesGuiGlobals.TextScaleLarge * 1.5
        DirectLabel(parent=myParent, relief=None, state=DGG.DISABLED, text='%s/%s' % (self.panelNumber, self.numOfPanels), text_scale=txtScale, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0,
                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                    0), text_font=self.bodyfont, textMayChange=0, pos=(2.1,
                                                                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                                                                       0.03))
        self.prevButton = GuiButton(parent=self, pos=(1.85, 0, -0.05), text=PLocalizer.CannonDefense['Previous'])
        if self.roundComplete == RoundCompleteFlags.GAME_DEFEAT:
            doWhatNextTxt = PLocalizer.CannonDefense['Exit']
        else:
            doWhatNextTxt = PLocalizer.CannonDefense['Continue']
        self.nextButton = GuiButton(parent=self, pos=(2.1, 0, -0.05), text=doWhatNextTxt)
        return

    def setTimePlayed(self, times, playerIndex):
        for index in range(0, len(times)):
            seconds = times[index]
            if seconds >= 60:
                minutes = int(math.ceil(float(seconds) / 60.0))
                text = '%s %s' % (minutes, PLocalizer.CannonDefense['Minutes'])
            else:
                text = '%s %s' % (seconds, PLocalizer.CannonDefense['Seconds'])
            self.timePlayedTotalslbl[index]['text'] = text
            if index == playerIndex:
                self.timePlayedTotalslbl[index]['text_fg'] = self.highlightPlayerColor
                self.timePlayedTotalslbl[index]['text_font'] = self.headingfont
                self.timePlayedTotalslbl[index]['text_shadow'] = PiratesGuiGlobals.TextShadow

    def setGoldEarned(self, goldEarned, playerIndex):
        for index in range(0, len(goldEarned)):
            self.goldEarnedTotalslbl[index]['text'] = str(goldEarned[index])
            if index == playerIndex:
                self.goldEarnedTotalslbl[index]['text_fg'] = self.highlightPlayerColor
                self.goldEarnedTotalslbl[index]['text_font'] = self.headingfont
                self.goldEarnedTotalslbl[index]['text_shadow'] = PiratesGuiGlobals.TextShadow