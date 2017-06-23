from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.DialMeter import DialMeter
from pirates.piratesgui import PiratesGuiGlobals

class CannonDefenseTimeRemainingUI():

    def __init__(self):
        self.timeRemaining = None
        self.skillRing = None
        self._loadAssets()
        return

    def _loadAssets(self):
        timer = None
        try:
            timer = loader.loadModel('models/gui/pir_m_gui_can_timer')
            self.timeRemaining = base.a2dTopRight.attachNewNode('CannonDefenseTimeRemaining')
            self.timeRemaining.setDepthTest(True)
            self.timeRemaining.setDepthWrite(True)
            self.timeRemaining.setScale(0.75)
            model = self.timeRemaining.attachNewNode('model')
            foreGround = timer.find('**/timer')
            self.skillRing = DialMeter(model, wantCover=False, dangerRatio=0.0, meterColor=Vec4(0.11328125, 0.09375, 0.05078125, 1.0), baseColor=Vec4(1.0, 0.0, 0.0, 1.0))
            self.skillRing.setScale(0.5)
            self.skillRing.setR(180)
            self.skillRing.update(0.0, 1.0)
            foreGround.reparentTo(model)
            foreGround.setY(-0.1)
            self.__createWaveText(model)
            self.__createWaveLabel(model)
            min = Point3()
            max = Point3()
            model.calcTightBounds(min, max)
            size = max - min
            model.setPos(-size[0] / 2.0, 0, -size[2] / 2.0)
        finally:
            if timer:
                timer.removeNode()

        return

    def __createWaveText(self, parent):
        self.waveNumberTxt = TextNode('WaveNumber')
        self.waveNumberTxt.setFont(PiratesGlobals.getInterfaceFont())
        self.waveNumberTxt.setTextColor(PiratesGuiGlobals.TextFG1)
        self.waveNumberTxt.setShadow(0.05, 0.05)
        self.waveNumberTxt.setAlign(TextNode.ACenter)
        waveTxtNode = parent.attachNewNode(self.waveNumberTxt)
        waveTxtNode.setScale(0.12)
        waveTxtNode.setPos(0, -0.2, -0.08)
        waveTxtNode.setDepthTest(False)
        waveTxtNode.setDepthWrite(False)

    def __createWaveLabel(self, parent):
        self.waveLabelTxt = TextNode('WaveLabel')
        self.waveLabelTxt.setFont(PiratesGlobals.getInterfaceFont())
        self.waveLabelTxt.setTextColor(PiratesGuiGlobals.TextFG1)
        self.waveLabelTxt.setShadow(0.05, 0.05)
        self.waveLabelTxt.setAlign(TextNode.ACenter)
        self.waveLabelTxt.setText(PLocalizer.CannonDefense['WaveLabel'])
        waveLblNode = parent.attachNewNode(self.waveLabelTxt)
        waveLblNode.setScale(0.06)
        waveLblNode.setPos(0, -0.2, 0.015)
        waveLblNode.setDepthTest(False)
        waveLblNode.setDepthWrite(False)

    def destroy(self):
        self.timeRemaining.removeNode()

    def hide(self):
        self.timeRemaining.hide()

    def show(self):
        self.timeRemaining.show()

    def setPercent(self, percent):
        if percent < 0.0:
            percent = 0.0
        elif percent > 1.0:
            percent = 1.0
        self.skillRing.update(percent, 1.0)

    def setWaveNumber(self, num):
        self.waveNumberTxt.setText(str(num))