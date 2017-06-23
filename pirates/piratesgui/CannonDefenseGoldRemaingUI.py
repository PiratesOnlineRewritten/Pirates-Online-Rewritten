from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals

class CannonDefenseGoldRemaingUI():

    def __init__(self):
        self.mineCounter = None
        self._healthDepletion = None
        self._loadAssets()
        self.setPercent(1)
        return

    def _loadAssets(self):
        counter = None
        try:
            self.mineCounter = base.a2dTopLeft.attachNewNode('CannonDefenseMineCounter')
            self.mineCounter.setScale(1.5)
            self.mineCounter.setDepthTest(True)
            self.mineCounter.setDepthWrite(True)
            model = self.mineCounter.attachNewNode('model')
            self._healthDepletion = model.attachNewNode('HealthDepletionBar')
            self._healthDepletion.setX(0.16)
            counter = loader.loadModel('models/gui/pir_m_gui_can_mineCounter')
            foreground = counter.find('**/mineCounter')
            healthBar = counter.find('**/healthBar')
            background = counter.find('**/background')
            background.setSx(0.72)
            min = Point3()
            max = Point3()
            background.calcTightBounds(min, max)
            size = max - min
            background.reparentTo(self._healthDepletion)
            background.setX(-size[0] / 2.0)
            healthBar.reparentTo(model)
            foreground.reparentTo(model)
            self.__createTextLabel(model)
            model.calcTightBounds(min, max)
            size = max - min
            model.setPos(size[0] / 2.0, 0, -size[2] / 2.0)
        finally:
            if counter:
                counter.removeNode()

        return

    def __createTextLabel(self, parent):
        goldLabelTxt = TextNode('TreasureRemaining')
        goldLabelTxt.setFont(PiratesGlobals.getInterfaceFont())
        goldLabelTxt.setTextColor(PiratesGuiGlobals.TextFG1)
        goldLabelTxt.setAlign(TextNode.ACenter)
        goldLabelTxt.setText(PLocalizer.CannonDefense['TreasureRemaining'])
        goldTxtNode = parent.attachNewNode(goldLabelTxt)
        goldTxtNode.setScale(0.03)
        goldTxtNode.setX(0.035)
        goldTxtNode.setZ(0.005)
        goldTxtNode.setDepthTest(False)
        goldTxtNode.setDepthWrite(False)

    def destroy(self):
        self.mineCounter.removeNode()

    def hide(self):
        self.mineCounter.hide()

    def show(self):
        self.mineCounter.show()

    def setPercent(self, percent):
        if percent < 0.0:
            percent = 0.0
        elif percent > 1.0:
            percent = 1.0
        self._healthDepletion.setSx(1 - percent)