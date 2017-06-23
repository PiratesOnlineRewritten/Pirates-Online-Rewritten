from pandac.PandaModules import NodePath
from direct.interval.IntervalGlobal import Sequence
from direct.task import Task
from panda3d.core import TextNode
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectWaitBar, DGG
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib
import FishingGlobals
import MinigameUtils
from LegendaryFishFSM import LegendaryFishFSM
from BlendActor import BlendActor
from Fish import Fish
from pirates.piratesbase import CollectionMap

class LegendaryFish(Fish):

    def __init__(self, fishManager, myData, index):
        Fish.__init__(self, fishManager, myData, index)
        self.fsm = LegendaryFishFSM(self)
        self.actor.setScale(self.myData['scaleRange'][0])
        self.staminaValue = self.myData['stamina']
        self.aboutToBitingInterval = None
        self.fishChaseLureSequence = Sequence()
        self.lfStruggleSequence = Sequence()
        self.initFishStaminaBar()
        self.lurePosition = None
        return

    def initFishStaminaBar(self):
        self.legendaryGui = loader.loadModel('models/minigames/pir_m_gam_fsh_legendaryGui')
        self.iconBaseFrame = DirectFrame(relief=None, state=DGG.DISABLED, pos=(0, 0,
                                                                               0), sortOrder=30, image=self.legendaryGui.find('**/pir_t_gui_fsh_fishPortraitFrame'), image_scale=0.18, image_pos=(0,
                                                                                                                                                                                                  0,
                                                                                                                                                                                                  0))
        self.iconBaseFrame.setTransparency(TransparencyAttrib.MAlpha)
        self.fishUINodePath = NodePath(self.iconBaseFrame)
        self.fishUINodePath.setPos(-0.3, 0.0, 0.83)
        self.fishUINodePath.reparentTo(hidden)
        self.iconCard = loader.loadModel('models/gui/treasure_gui')
        self.iconBaseFrame.iconImage = OnscreenImage(parent=self.iconBaseFrame, image=self.iconCard.find('**/%s*' % CollectionMap.Assets[self.myData['id']]), scale=0.35, hpr=(0,
                                                                                                                                                                               0,
                                                                                                                                                                               0), pos=(0.0,
                                                                                                                                                                                        0,
                                                                                                                                                                                        0.0))
        self.fishNameLabel = TextNode('fishNameLabel')
        name = self.getName().split('_')
        self.fishNameLabel.setText(name[0])
        self.fishNameLabel.setTextColor(1.0, 1.0, 1.0, 1.0)
        self.fishNameLabelNodePath = NodePath(self.fishNameLabel)
        self.fishNameLabelNodePath.setPos(0.3, 0, 0.04)
        self.fishNameLabelNodePath.setScale(0.045)
        self.fishNameLabelNodePath.reparentTo(self.iconBaseFrame)
        self.fishStaminaBar = DirectWaitBar(parent=self.iconBaseFrame, relief=DGG.FLAT, state=DGG.DISABLED, range=100, value=0, sortOrder=20, frameColor=(0,
                                                                                                                                                          0,
                                                                                                                                                          0,
                                                                                                                                                          1.0), pos=(0.07, 0.0, -0.015), hpr=(0,
                                                                                                                                                                                              0,
                                                                                                                                                                                              0), frameSize=(0,
                                                                                                                                                                                                             0.72,
                                                                                                                                                                                                             0,
                                                                                                                                                                                                             0.028))
        self.fishStaminaBar['value'] = self.staminaValue
        self.fishStaminaBar['barColor'] = FishingGlobals.fishingStaminaBarColor[int(self.staminaValue / 100.0 * (len(FishingGlobals.fishingStaminaBarColor) - 1))]
        self.fishStaminaValueLabel = TextNode('fishStaminaValueLabel')
        self.fishStaminaValueLabel.setText(str(self.staminaValue) + '//' + str(self.staminaValue))
        self.fishStaminaValueLabel.setTextColor(1.0, 1.0, 1.0, 1.0)
        self.fishStaminaValueLabelNodePath = NodePath(self.fishStaminaValueLabel)
        self.fishStaminaValueLabelNodePath.setPos(0.66, 0, -0.06)
        self.fishStaminaValueLabelNodePath.setScale(0.045)
        self.fishStaminaValueLabelNodePath.reparentTo(self.iconBaseFrame)
        self.fishStaminaBarFrame = DirectLabel(parent=self.iconBaseFrame, relief=None, state=DGG.DISABLED, frameColor=(1,
                                                                                                                       1,
                                                                                                                       1,
                                                                                                                       0.1), pos=(0.44,
                                                                                                                                  0.0,
                                                                                                                                  0.0), hpr=(0,
                                                                                                                                             0,
                                                                                                                                             0), sortOrder=25, image=self.legendaryGui.find('**/pir_t_gui_fsh_staminaBarForeground'), image_scale=(1.0,
                                                                                                                                                                                                                                                   0.0,
                                                                                                                                                                                                                                                   0.05), image_pos=(0.0,
                                                                                                                                                                                                                                                                     0.0,
                                                                                                                                                                                                                                                                     0.0), image_hpr=(0.0,
                                                                                                                                                                                                                                                                                      0.0,
                                                                                                                                                                                                                                                                                      0.0))
        self.fishStaminaBarFrame.setTransparency(TransparencyAttrib.MAlpha)
        self.fishStaminaBarFrame.setDepthTest(True)
        self.fishStaminaBarFrame.setDepthWrite(True)
        return

    def cleanFishData(self):
        self.staminaValue = self.myData['stamina']
        self.fishStaminaBar['value'] = self.staminaValue
        self.fishStaminaValueLabel.setText(str(int(self.staminaValue)) + ' / ' + str(100))
        self.fishStaminaBar['barColor'] = FishingGlobals.fishingStaminaBarColor[int(self.staminaValue / 100.0 * (len(FishingGlobals.fishingStaminaBarColor) - 1))]
        self.hideStaminaBar()
        taskMgr.remove('updateFishStaminaTask')
        self.lurePosition = None
        self.fishChaseLureSequence.pause()
        self.fishChaseLureSequence.clearToInitial()
        self.lfStruggleSequence.pause()
        self.lfStruggleSequence.clearToInitial()
        if self.aboutToBitingInterval is None:
            return
        self.aboutToBitingInterval.pause()
        return

    def destroy(self):
        self.fishUINodePath.removeNode()
        Fish.destroy(self)

    def updateFishStaminaTask(self, task=None):
        if self.staminaValue <= 1:
            return Task.done
        self.staminaValue = max(1, self.staminaValue - FishingGlobals.staminaReduceValue)
        self.fishStaminaValueLabel.setText(str(int(self.staminaValue)) + ' / ' + str(100))
        self.fishStaminaBar['value'] = self.staminaValue
        self.fishStaminaBar['barColor'] = FishingGlobals.fishingStaminaBarColor[int(self.staminaValue / 100.0 * (len(FishingGlobals.fishingStaminaBarColor) - 1))]
        return Task.cont

    def updateFishStaminaBar(self):
        self.fishStaminaBar['value'] = self.staminaValue

    def fishStaminaConsume(self):
        taskMgr.add(self.updateFishStaminaTask, 'updateFishStaminaTask')

    def staminaPercentage(self):
        return self.staminaValue / self.myData['stamina']

    def showStaminaBar(self):
        self.fishUINodePath.reparentTo(aspect2d)

    def hideStaminaBar(self):
        self.fishUINodePath.reparentTo(hidden)

    def performStraightBehavior(self, lurePos, dt):
        newX = self.getX() + self.velocity[0] * dt + self.accel[0] * dt * dt
        newZ = self.getZ() + self.velocity[2] * dt + self.accel[2] * dt * dt
        return (
         newX, newZ)