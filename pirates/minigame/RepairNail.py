from pandac.PandaModules import NodePath
from direct.gui.DirectGui import DirectLabel
from direct.fsm import FSM
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
import RepairGlobals
NAIL_COLLIDE_MASK = 8
HAMMERED_DEPTH = -0.17

class RepairNail(NodePath, FSM.FSM):

    def __init__(self, name, parent, nailModel):
        self.config = RepairGlobals.Hammering
        NodePath.__init__(self, name)
        FSM.FSM.__init__(self, 'Nail_%sFSM' % name)
        self.reparentTo(parent)
        self.nailModel = nailModel
        self._initVars()
        self._initVisuals()

    def _initVars(self):
        self.totalClicks = 0
        self.remainingPercent = 1.0

    def _initVisuals(self):
        self.visual = self.attachNewNode('RepairNail.visual')
        self.nailModel.find('**/nail_collision').setPos(0.0, -35.0, 0.0)
        self.nailModel.setScale(1.5)
        self.nailModel.find('**/nail_collision').setCollideMask(NAIL_COLLIDE_MASK)
        self.nailModel.find('**/nail_collision').setPythonTag('nail', self)
        self.nailModel.find('**/nail_collision').hide()
        self.nailModel.reparentTo(self.visual)
        self.nailModel.find('**/nail_model').setHpr(0.0, 20.0, 0.0)
        self.nailModel.setDepthTest(True)
        self.nailModel.setDepthWrite(True)
        self.shadow = self.nailModel.find('**/shadow')
        self.shadow.reparentTo(self)
        self.shadow.setPos(0.0, -0.04, 0.02)
        self.shadow.setDepthTest(True)
        self.shadow.setDepthWrite(True)
        self.shadow.setScale(2.0)
        self.shadow.setTransparency(1)
        self.shadow.setSa(0.6)
        self.resultLabel = DirectLabel(text='', relief=None, text_fg=(1.0, 1.0, 1.0,
                                                                      1.0), text_shadow=(0.0,
                                                                                         0.0,
                                                                                         0.0,
                                                                                         1.0), text_font=PiratesGlobals.getPirateFont(), scale=(0.05,
                                                                                                                                                0.05,
                                                                                                                                                0.05), pos=(0.0, 0.0, -0.09), parent=self)
        return

    def removeNode(self):
        self.visual.removeNode()
        del self.visual
        self.resultLabel.destroy()
        NodePath.removeNode(self)

    def setShadow(self, percent):
        self.shadow.setScale(percent * 1.0 + 1.4)
        self.shadow.setSa(1.0 - (percent * 0.2 + 0.2))

    def hitNail(self, percentage):
        self.remainingPercent = max(0.0, self.remainingPercent - percentage)
        self.totalClicks += 1
        self.setShadow(self.remainingPercent)
        newDepth = (1.0 - self.remainingPercent) * HAMMERED_DEPTH
        self.visual.setZ(newDepth)
        if self.remainingPercent <= 0.0:
            for i in range(len(self.config.rankingThresholds)):
                if self.totalClicks >= self.config.rankingThresholds[i]:
                    break

            self.request('Hammered', PLocalizer.Minigame_Repair_Hammering_Thresholds[i])
            return True
        return False

    def enterActive(self):
        self.visual.setZ(0.0)
        self.remainingPercent = 1.0
        self.totalClicks = 0
        self.setShadow(1.0)

    def exitActive(self):
        pass

    def enterHammered(self, successText):
        self.resultLabel['text'] = successText
        self.resultLabel.setText()

    def exitHammered(self):
        self.resultLabel['text'] = ''
        self.resultLabel.setText()

    def enterIdle(self):
        self.stash()

    def exitIdle(self):
        self.unstash()