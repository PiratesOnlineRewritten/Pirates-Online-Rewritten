from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer

class RoundCompleteFlags():
    WAVE_COMPLETE = 0
    GAME_VICTORY = 1
    GAME_DEFEAT = 2


class CannonDefenseScorePanelBase(DirectFrame):

    def __init__(self, panelNumber, numOfPanels, **kw):
        DirectFrame.__init__(self, **kw)
        self.hide()
        self.panelNumber = panelNumber
        self.numOfPanels = numOfPanels
        self.playerLbls = []
        self.shipsSunkTotalslbl = []
        self.damageTotalslbl = []
        self.accuracyTotalslbl = []
        self.shotsFiredTotalslbl = []
        self.headingfont = PiratesGlobals.getPirateOutlineFont()
        self.bodyfont = PiratesGlobals.getPirateFont()
        self.highlightPlayerColor = PiratesGuiGlobals.TextFG4

    def _createPlayerNames(self, myParent, playerLbls, startX, startY, widthX):
        for x in range(0, 4):
            playerLbls.append(DirectLabel(parent=myParent, relief=None, state=DGG.DISABLED, text=PLocalizer.CannonDefense['SlotEmpty'], text_scale=PiratesGuiGlobals.TextScaleLarge * 1.25, text_align=TextNode.ACenter, text_fg=(0.75,
                                                                                                                                                                                                                                  0.75,
                                                                                                                                                                                                                                  0.75,
                                                                                                                                                                                                                                  0.5), text_shadow=(0,
                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                     0.5), text_wordwrap=7, text_pos=(0,
                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                      0), text_font=self.headingfont, textMayChange=1, pos=(startX + widthX * x, 0, startY)))

        return

    def _createStatsLabels(self, myParent, descTxt, statsLabels, startX, startY, widthX):
        DirectLabel(parent=myParent, relief=None, state=DGG.DISABLED, text=descTxt, text_scale=PiratesGuiGlobals.TextScaleLarge * 1.5, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG0, text_pos=(0,
                                                                                                                                                                                                               0,
                                                                                                                                                                                                               0), text_font=self.bodyfont, textMayChange=1, pos=(0.22, 0, startY))
        for x in range(0, 4):
            statsLabels.append(DirectLabel(parent=myParent, relief=None, state=DGG.DISABLED, text='', text_scale=PiratesGuiGlobals.TextScaleLarge * 1.5, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG0, text_pos=(0,
                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                   0), text_font=self.bodyfont, textMayChange=1, pos=(startX + widthX * x, 0, startY)))

        return

    def setNames(self, names):
        localPlayerIndex = -1
        for index in range(0, len(names)):
            if names[index] == localAvatar.name:
                self.playerLbls[index]['text_fg'] = self.highlightPlayerColor
                localPlayerIndex = index
            self.playerLbls[index]['text'] = names[index]

        return localPlayerIndex

    def setSunkShips(self, sunkShipScores, playerIndex):
        for index in range(0, len(sunkShipScores)):
            self.shipsSunkTotalslbl[index]['text'] = str(sunkShipScores[index])
            if index == playerIndex:
                self.shipsSunkTotalslbl[index]['text_fg'] = self.highlightPlayerColor
                self.shipsSunkTotalslbl[index]['text_font'] = self.headingfont
                self.shipsSunkTotalslbl[index]['text_shadow'] = PiratesGuiGlobals.TextShadow

    def setDamageDealt(self, damageDealt, playerIndex):
        for index in range(0, len(damageDealt)):
            self.damageTotalslbl[index]['text'] = str(damageDealt[index])
            if index == playerIndex:
                self.damageTotalslbl[index]['text_fg'] = self.highlightPlayerColor
                self.damageTotalslbl[index]['text_font'] = self.headingfont
                self.damageTotalslbl[index]['text_shadow'] = PiratesGuiGlobals.TextShadow

    def setAccuracy(self, accuracy, playerIndex):
        for index in range(0, len(accuracy)):
            value = accuracy[index]
            if value >= 0:
                self.accuracyTotalslbl[index]['text'] = '%s%%' % accuracy[index]
            else:
                self.accuracyTotalslbl[index]['text'] = PLocalizer.CannonDefense['NotApplicable']
            if index == playerIndex:
                self.accuracyTotalslbl[index]['text_fg'] = self.highlightPlayerColor
                self.accuracyTotalslbl[index]['text_font'] = self.headingfont
                self.accuracyTotalslbl[index]['text_shadow'] = PiratesGuiGlobals.TextShadow

    def setShotsFired(self, shotsFired, playerIndex):
        for index in range(0, len(shotsFired)):
            self.shotsFiredTotalslbl[index]['text'] = str(shotsFired[index])
            if index == playerIndex:
                self.shotsFiredTotalslbl[index]['text_fg'] = self.highlightPlayerColor
                self.shotsFiredTotalslbl[index]['text_font'] = self.headingfont
                self.shotsFiredTotalslbl[index]['text_shadow'] = PiratesGuiGlobals.TextShadow