from direct.fsm.FSM import FSM
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.CannonDefenseScorePanelBase import RoundCompleteFlags
from pirates.piratesgui.CannonDefenseEndOfWavePanel import CannonDefenseEndOfWavePanel
from pirates.piratesgui.CannonDefenseGameStatsPanel import CannonDefenseGameStatsPanel

class CannonDefenseScoreBoard(FSM, DirectFrame):

    def __init__(self, waveNumber, bonusRound, maxWaves, roundComplete):
        FSM.__init__(self, 'CannonDefenseScoreBoardFSM')
        DirectFrame.__init__(self, frameSize=(0, 2.406, 0, 1.5), pos=(-1.2, 0, -0.7), sortOrder=0)
        try:
            binOrder = 0
            if roundComplete:
                binOrder = 10
            self.setBin('gui-cannonDefense', binOrder)
            self.loadBackGround()
            actualWaveNumber = waveNumber + bonusRound * maxWaves
            self.panel1 = CannonDefenseEndOfWavePanel(actualWaveNumber, roundComplete, 1, 2, parent=self, frameColor=(0,
                                                                                                                      0,
                                                                                                                      0,
                                                                                                                      0), frameSize=(0,
                                                                                                                                     2.406,
                                                                                                                                     0,
                                                                                                                                     1.5))
            if roundComplete:
                self.panel1.nextButton['command'] = self.request
                self.panel1.nextButton['extraArgs'] = ['Panel3']
                self.panel3 = CannonDefenseGameStatsPanel(roundComplete, 2, 2, parent=self, frameColor=(0,
                                                                                                        0,
                                                                                                        0,
                                                                                                        0), frameSize=(0,
                                                                                                                       2.406,
                                                                                                                       0,
                                                                                                                       1.5))
                self.panel3.prevButton['command'] = self.request
                self.panel3.prevButton['extraArgs'] = ['Panel1']
            self.request('Panel1')
        except:
            self.destroy()
            raise

    def loadBackGround(self):
        self.backgroundModel = loader.loadModel('models/gui/pir_m_gui_can_reportPanel')
        self.backgroundModel.setPos(0, 0, 0)
        self.backgroundModel.wrtReparentTo(self)
        self.backgroundModel.setScale(0.4)
        self.backgroundModel.setDepthWrite(False)

    def enterPanel1(self):
        self.panel1.show()

    def exitPanel1(self):
        self.panel1.hide()

    def enterPanel3(self):
        self.panel3.show()

    def exitPanel3(self):
        self.panel3.hide()

    def destroy(self):
        DirectFrame.destroy(self)
        self.backgroundModel = None
        self.panel1 = None
        self.panel3 = None
        return

    def setupPanel1(self, endOfWaveData):
        self.panel1.setTreasureStats(endOfWaveData.treasureStolen, endOfWaveData.treasureRemaining)
        playerIndex = self.panel1.setNames(endOfWaveData.playerNames)
        self.panel1.setSunkShips(endOfWaveData.shipsSunkWave, playerIndex)
        self.panel1.setDamageDealt(endOfWaveData.damgeDealtWave, playerIndex)
        self.panel1.setAccuracy(endOfWaveData.accuracyWave, playerIndex)
        self.panel1.setShotsFired(endOfWaveData.shotsFiredWave, playerIndex)
        self.panel1.setGoldAwarded(endOfWaveData.myGoldEarned, endOfWaveData.myGoldBonus)
        self.panel1.setTreasureAwarded(endOfWaveData.treasureEarned)

    def setupPanel3(self, endOfWaveData):
        playerIndex = self.panel3.setNames(endOfWaveData.playerNames)
        self.panel3.setTimePlayed(endOfWaveData.timePlayed, playerIndex)
        self.panel3.setSunkShips(endOfWaveData.shipsSunkOverall, playerIndex)
        self.panel3.setDamageDealt(endOfWaveData.damgeDealtOverall, playerIndex)
        self.panel3.setAccuracy(endOfWaveData.accuracyOverall, playerIndex)
        self.panel3.setShotsFired(endOfWaveData.shotsFiredOverall, playerIndex)
        self.panel3.setGoldEarned(endOfWaveData.goldPaidOverall, playerIndex)