from pandac.PandaModules import NodePath, Point3
from panda3d.core import TextNode
from direct.gui.DirectGui import DGG
from pirates.piratesgui.GuiButton import GuiButton
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from pandac.PandaModules import TransparencyAttrib
from direct.interval.IntervalGlobal import Sequence, Parallel, Wait, Func
from direct.interval.LerpInterval import LerpHprInterval, LerpPosInterval, LerpColorScaleInterval, LerpScaleInterval
import FishingGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from BlendActor import BlendActor

class LegendaryFishingGameGUI():

    def __init__(self, gameObject=None):
        base.loadingScreen.beginStep('LegendaryGameGUI', 4, 20)
        self.gameObject = gameObject
        self.guiImage = loader.loadModel('models/minigames/pir_m_gam_fsh_legendaryGui')
        self.UICompoments = {}
        self.uiBaseNode = NodePath('baseNode')
        self.uiBaseNode.reparentTo(aspect2d)
        self.uiBaseNode.show()
        self.leftBaseNode = NodePath('leftBaseNode')
        self.leftBaseNode.reparentTo(base.a2dLeftCenter)
        self.leftBaseNode.show()
        self.fishActor = None
        self.actorAnim = {}
        self.scaleSize = {InventoryType.Collection_Set11_Part1: 0.06,InventoryType.Collection_Set11_Part2: 0.055,InventoryType.Collection_Set11_Part3: 0.12,InventoryType.Collection_Set11_Part4: 0.087,InventoryType.Collection_Set11_Part5: 0.08}
        self.meterFrame = DirectFrame(parent=self.leftBaseNode, frameSize=(-0.3, 0.3, -1.0, 0.0), frameColor=(1.0,
                                                                                                              1.0,
                                                                                                              1.0,
                                                                                                              0.0), relief=None, state=DGG.DISABLED, pos=(1.0, 0.0, -0.45), hpr=(0,
                                                                                                                                                                                 0,
                                                                                                                                                                                 0), scale=(1.3,
                                                                                                                                                                                            0.0,
                                                                                                                                                                                            1.3), image=self.guiImage.find('**/pir_t_gui_fsh_meter'), image_scale=(0.2,
                                                                                                                                                                                                                                                                   0.0,
                                                                                                                                                                                                                                                                   0.8), image_pos=(0,
                                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                                    0), text='', textMayChange=1, text_scale=PiratesGuiGlobals.TextScaleTitleLarge, text_pos=(-0.55, 0.1), text_shadow=PiratesGuiGlobals.TextShadow)
        self.UICompoments['meterFrame'] = self.meterFrame
        self.fishingRod = DirectFrame(parent=self.meterFrame, frameSize=(-0.3, 0.3, -1.0, 0.0), relief=None, state=DGG.DISABLED, pos=FishingGlobals.fishingRodScreenPosition, image=self.guiImage.find('**/pir_t_gui_fsh_fullRod'), image_scale=(1.0,
                                                                                                                                                                                                                                                 0.0,
                                                                                                                                                                                                                                                 0.125), image_pos=(0.2,
                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                    0))
        self.fishingRod.setR(FishingGlobals.fishingRodInitSlope)
        self.UICompoments['fishingRod'] = self.fishingRod
        base.loadingScreen.tick()
        self.fishingHandleBaseFrame = DirectFrame(parent=self.uiBaseNode, frameSize=(-0.3, 0.3, -1.5, 1.5), frameColor=(1.0,
                                                                                                                        1.0,
                                                                                                                        1.0,
                                                                                                                        0.0), relief=None, state=DGG.DISABLED, pos=(0.0,
                                                                                                                                                                    0.0,
                                                                                                                                                                    0.0), hpr=(0,
                                                                                                                                                                               0,
                                                                                                                                                                               0), scale=(0.72,
                                                                                                                                                                                          0.0,
                                                                                                                                                                                          0.72), image=self.guiImage.find('**/pir_t_gui_fsh_partialRod'), image_scale=(3.8,
                                                                                                                                                                                                                                                                       0.0,
                                                                                                                                                                                                                                                                       1.9), image_pos=(0,
                                                                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                                                                        0), image_hpr=(0.0,
                                                                                                                                                                                                                                                                                                       0.0,
                                                                                                                                                                                                                                                                                                       0))
        self.fishingHandleBaseFrame.hide()
        self.UICompoments['fishingHandleBaseFrame'] = self.fishingHandleBaseFrame
        self.fishingHandle = DirectFrame(parent=self.fishingHandleBaseFrame, frameSize=(-0.08, 0.08, -0.2, 0.2), relief=None, state=DGG.DISABLED, pos=(-0.1, 0.0, -0.05), hpr=(0,
                                                                                                                                                                               0,
                                                                                                                                                                               0), image=self.guiImage.find('**/pir_t_gui_fsh_handleArm'), image_scale=(1.0,
                                                                                                                                                                                                                                                        0.0,
                                                                                                                                                                                                                                                        1.0), image_pos=(-0.042, 0, -0.115), image_hpr=(0.0,
                                                                                                                                                                                                                                                                                                        0.0,
                                                                                                                                                                                                                                                                                                        0))
        self.UICompoments['fishingHandle'] = self.fishingHandle
        self.arrowImage = DirectFrame(parent=self.fishingHandleBaseFrame, frameSize=(-0.4, 0.4, -0.4, 0.4), relief=None, state=DGG.DISABLED, pos=(0.0,
                                                                                                                                                  0.0,
                                                                                                                                                  0.0), hpr=(0,
                                                                                                                                                             0,
                                                                                                                                                             0), scale=(1.2,
                                                                                                                                                                        0.0,
                                                                                                                                                                        1.2), image=self.guiImage.find('**/pir_t_gui_fsh_arrow'), image_scale=(1.0,
                                                                                                                                                                                                                                               0.0,
                                                                                                                                                                                                                                               1.0), image_pos=(0.0,
                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                0.0), image_hpr=(0.0,
                                                                                                                                                                                                                                                                                 0.0,
                                                                                                                                                                                                                                                                                 0.0))
        self.arrowImage.hide()
        self.UICompoments['arrowImage'] = self.arrowImage
        btnGeom = (
         self.guiImage.find('**/pir_t_gui_fsh_handle'), self.guiImage.find('**/pir_t_gui_fsh_handle'), self.guiImage.find('**/pir_t_gui_fsh_handleOn'))
        self.fishingHandleButton = GuiButton(pos=(-0.3, 0, -0.55), hpr=(0, 0, 0), scale=0.45, image=btnGeom, image_pos=(0,
                                                                                                                        0,
                                                                                                                        0), image_scale=1.0, sortOrder=2)
        self.fishingHandleButton.bind(DGG.B1PRESS, self.handleButtonClicked)
        self.fishingHandleButton.reparentTo(self.fishingHandle)
        self.UICompoments['fishingHandleButton'] = self.fishingHandleButton
        self.fishingHandleBaseFrame.setTransparency(TransparencyAttrib.MAlpha)
        self.meterFrame.setTransparency(TransparencyAttrib.MAlpha)
        self.lineOneTransitTextNode = TextNode('lineOneTransitText')
        self.lineOneTransitTextNode.setFont(PiratesGlobals.getPirateFont())
        self.lineOneTransitTextNode.setText('')
        self.lineOneTransitTextNode.setAlign(TextNode.ACenter)
        self.lineOneTransitTextNode.setTextColor(1.0, 1.0, 1.0, 0.5)
        self.lineOneTransitTextNodePath = NodePath(self.lineOneTransitTextNode)
        self.lineOneTransitTextNodePath.setPos(0.0, 0.0, -0.8)
        self.lineOneTransitTextNodePath.setScale(0.35, 0.35, 0.35)
        self.lineOneTransitTextNodePath.reparentTo(self.uiBaseNode)
        self.lineOneTransitTextNodePath.hide()
        self.UICompoments['lineOneTransitText'] = self.lineOneTransitTextNodePath
        self.lineTwoTransitTextNode = TextNode('lineTwoTransitText')
        self.lineTwoTransitTextNode.setFont(PiratesGlobals.getPirateFont())
        self.lineTwoTransitTextNode.setText('')
        self.lineTwoTransitTextNode.setAlign(TextNode.ACenter)
        self.lineTwoTransitTextNode.setTextColor(1.0, 1.0, 1.0, 0.5)
        self.lineTwoTransitTextNodePath = NodePath(self.lineTwoTransitTextNode)
        self.lineTwoTransitTextNodePath.setPos(-0.4, 0.0, -0.95)
        self.lineTwoTransitTextNodePath.setScale(0.12, 0.12, 0.12)
        self.lineTwoTransitTextNodePath.reparentTo(self.uiBaseNode)
        self.lineTwoTransitTextNodePath.hide()
        self.UICompoments['lineTwoTransitText'] = self.lineTwoTransitTextNodePath
        base.loadingScreen.tick()
        self.test_guiImage = loader.loadModel('models/gui/toplevel_gui')
        self.buttonIcon = (self.test_guiImage.find('**/treasure_chest_closed'), self.test_guiImage.find('**/treasure_chest_closed'), self.test_guiImage.find('**/treasure_chest_closed_over'))
        self.winImagePanel = GuiPanel.GuiPanel('', 2.6, 1.9, True)
        self.winImagePanel.setPos(-1.3, 0.0, -0.95)
        self.winImagePanel.reparentTo(self.uiBaseNode)
        self.winImagePanel.background = OnscreenImage(parent=self.winImagePanel, scale=(2.4,
                                                                                        0,
                                                                                        1.8), image=self.guiImage.find('**/pir_t_gui_fsh_posterBackground'), hpr=(0,
                                                                                                                                                                  0,
                                                                                                                                                                  0), pos=(1.3,
                                                                                                                                                                           0,
                                                                                                                                                                           0.95))
        self.winImagePanel.setBin('gui-popup', -4)
        self.winTitleTextNode = TextNode('winTitleTextNode')
        self.winTitleTextNode.setText('Congratulations!')
        self.winTitleTextNode.setAlign(TextNode.ACenter)
        self.winTitleTextNode.setFont(PiratesGlobals.getPirateFont())
        self.winTitleTextNode.setTextColor(0.23, 0.09, 0.03, 1.0)
        self.winTitleTextNodePath = NodePath(self.winTitleTextNode)
        self.winTitleTextNodePath.setPos(1.35, 0.0, 1.67)
        self.winTitleTextNodePath.setScale(0.18)
        self.winTitleTextNodePath.reparentTo(self.winImagePanel)
        self.wholeStoryTextNode = TextNode('storyTextNode')
        self.wholeStoryTextNode.setText('')
        self.wholeStoryTextNode.setWordwrap(19.0)
        self.wholeStoryTextNode.setTextColor(0.23, 0.09, 0.03, 1.0)
        self.wholeStoryTextNodePath = NodePath(self.wholeStoryTextNode)
        self.wholeStoryTextNodePath.setPos(0.33, 0.0, 1.64)
        self.wholeStoryTextNodePath.setScale(0.05)
        self.wholeStoryTextNodePath.reparentTo(self.winImagePanel)
        self.winImagePanel.closeButton['command'] = self.closeDialogGotNextState
        self.winImagePanel.closeButton['extraArgs'] = ['winImagePanel', 'FarewellLegendaryFish', False]
        self.UICompoments['winImagePanel'] = self.winImagePanel
        self.winImagePanel.hide()
        self.luiCloseDialogSequence = Sequence()
        self.arrowImageRotationInterval = LerpHprInterval(self.arrowImage, 2.2, self.arrowImage.getHpr() + Point3(0.0, 0.0, 280.0), self.arrowImage.getHpr())
        self.luiArrowRotatingSequence = Sequence(Func(self.showGui, ['arrowImage']), Parallel(Func(self.arrowImageRotationInterval.start), Wait(2.2)), Func(self.hideGui, ['arrowImage']), Func(self.arrowImage.setHpr, self.arrowImage.getHpr() + Point3(0.0, 0.0, 5.0)), name=self.gameObject.distributedFishingSpot.uniqueName('luiArrowRotatingSequence'))
        self.lineOneColorChange = LerpColorScaleInterval(self.lineOneTransitTextNodePath, FishingGlobals.legendaryTransitionTextDuration, (1.0,
                                                                                                                                           1.0,
                                                                                                                                           1.0,
                                                                                                                                           0.0), (1.0,
                                                                                                                                                  1.0,
                                                                                                                                                  1.0,
                                                                                                                                                  1.0), blendType='easeOut')
        self.lineOnePosChange = LerpPosInterval(self.lineOneTransitTextNodePath, FishingGlobals.legendaryTransitionTextDuration, (0.0, 0.0, -0.2), (0.0, 0.0, -0.8), blendType='easeOut')
        self.lineTwoCholorChange = LerpColorScaleInterval(self.lineTwoTransitTextNodePath, FishingGlobals.legendaryTransitionTextDuration, (1.0,
                                                                                                                                            1.0,
                                                                                                                                            1.0,
                                                                                                                                            1.0), (1.0,
                                                                                                                                                   1.0,
                                                                                                                                                   1.0,
                                                                                                                                                   1.0), blendType='easeOut')
        self.lineTwoPosChange = LerpPosInterval(self.lineTwoTransitTextNodePath, FishingGlobals.legendaryTransitionTextDuration, (0.0, 0.0, -0.32), (0.0, 0.0, -0.95), blendType='easeOut')
        self.transitionTextMovingSequence = Sequence(Func(self.lineOneTransitTextNodePath.show), Func(self.lineTwoTransitTextNodePath.show), Parallel(self.lineOnePosChange, self.lineTwoPosChange, self.lineOneColorChange, self.lineTwoCholorChange), Func(self.lineOneTransitTextNodePath.hide), Func(self.lineTwoTransitTextNodePath.hide), name=self.gameObject.distributedFishingSpot.uniqueName('transitionTextMovingSequence'))
        self.meterFadeInInterval = Sequence(Func(self.meterFrame.show), LerpColorScaleInterval(self.meterFrame, FishingGlobals.legendaryTransitionTextDuration, colorScale=(1.0,
                                                                                                                                                                            1.0,
                                                                                                                                                                            1.0,
                                                                                                                                                                            1.0), startColorScale=(1.0,
                                                                                                                                                                                                   1.0,
                                                                                                                                                                                                   1.0,
                                                                                                                                                                                                   0.0), blendType='easeOut'), name='FadeInLegendaryMeter')
        self.meterFadeOutInterval = Sequence(LerpColorScaleInterval(self.meterFrame, FishingGlobals.legendaryTransitionTextDuration, colorScale=(1.0,
                                                                                                                                                 1.0,
                                                                                                                                                 1.0,
                                                                                                                                                 0.0), startColorScale=(1.0,
                                                                                                                                                                        1.0,
                                                                                                                                                                        1.0,
                                                                                                                                                                        1.0), blendType='easeOut'), Func(self.meterFrame.hide), name='FadeOutLegendaryMeter')
        self.rodFadeInInterval = Sequence(Func(self.fishingHandleBaseFrame.show), LerpColorScaleInterval(self.fishingHandleBaseFrame, FishingGlobals.legendaryTransitionTextDuration, colorScale=(1.0,
                                                                                                                                                                                                  1.0,
                                                                                                                                                                                                  1.0,
                                                                                                                                                                                                  1.0), startColorScale=(1.0,
                                                                                                                                                                                                                         1.0,
                                                                                                                                                                                                                         1.0,
                                                                                                                                                                                                                         0.0), blendType='easeOut'), name='FadeInLegendaryRodInterface')
        self.rodFadeOutInterval = Sequence(LerpColorScaleInterval(self.fishingHandleBaseFrame, FishingGlobals.legendaryTransitionTextDuration, colorScale=(1.0,
                                                                                                                                                           1.0,
                                                                                                                                                           1.0,
                                                                                                                                                           0.0), startColorScale=(1.0,
                                                                                                                                                                                  1.0,
                                                                                                                                                                                  1.0,
                                                                                                                                                                                  1.0), blendType='easeOut'), Func(self.fishingHandleBaseFrame.hide), name='FadeOutLegendaryRodInterface')
        base.loadingScreen.tick()
        smallScale = self.fishingHandleButton['scale']
        bigScale = self.fishingHandleButton['scale'] * 1.2
        self.buttonGrowUpInterval = LerpScaleInterval(self.fishingHandleButton, 1.0, bigScale, smallScale)
        self.luiFightTransitSequence = Sequence(Parallel(Func(self.fishingHandleBaseFrame.show), Func(self.meterFadeOutInterval.start), Func(self.rodFadeInInterval.start), Func(self.buttonGrowUpInterval.start)), Wait(1.0), Func(self.meterFrame.hide), name=self.gameObject.distributedFishingSpot.uniqueName('luiFightTransitSequence'))
        self.luiReelTransitSequence = Sequence(Parallel(Func(self.fishingHandleBaseFrame.show), Func(self.meterFadeOutInterval.start), Func(self.rodFadeInInterval.start)), Wait(1.0), Func(self.meterFrame.hide), name=self.gameObject.distributedFishingSpot.uniqueName('luiReelTransitSequence'))
        self.luiStruggleTransitSequence = Sequence(Parallel(Func(self.meterFrame.show), Func(self.resetFishingRod), self.meterFadeInInterval, self.rodFadeOutInterval), Wait(1.0), Func(self.fishingHandleBaseFrame.hide), name=self.gameObject.distributedFishingSpot.uniqueName('luiStruggleTransitSequence'))
        self.meterFadeOutInterval.start()
        self.rodFadeOutInterval.start()
        self.hideAllGUI()
        base.loadingScreen.endStep('LegendaryGameGUI')
        return

    def hideAllGUI(self):
        self.uiBaseNode.reparentTo(hidden)
        self.leftBaseNode.reparentTo(hidden)

    def showAllGUI(self):
        self.uiBaseNode.reparentTo(aspect2d)
        self.leftBaseNode.reparentTo(base.a2dLeftCenter)

    def hideGui(self, nameList):
        for ui in nameList:
            self.UICompoments[ui].hide()

    def showGui(self, nameList):
        for ui in nameList:
            self.UICompoments[ui].show()

    def destroy(self):
        self.arrowImageRotationInterval.pause()
        self.arrowImageRotationInterval.clearToInitial()
        self.luiArrowRotatingSequence.pause()
        self.luiArrowRotatingSequence.clearToInitial()
        self.luiCloseDialogSequence.pause()
        self.luiCloseDialogSequence.clearToInitial()
        totalKey = self.UICompoments.keys()
        for iKey in totalKey:
            del self.UICompoments[iKey]

        self.fishingHandle = None
        self.fishingHandleButton = None
        self.fishingRod.removeNode()
        self.leftBaseNode.removeNode()
        self.uiBaseNode.removeNode()
        if self.fishActor:
            self.fishActor.destroy()
            self.fishActor = None
        return

    def handleButtonClicked(self, mouseKey):
        if self.gameObject.lfgFsm.getCurrentOrNextState() in ['CatchIt']:
            self.gameObject.lfgFsm.request('Transition', 'Struggle')
            self.gameObject.sfx['legendaryGreen'].play()

    def setTransitionText(self, state):
        self.lineOneTransitTextNode.setText(PLocalizer.LegendaryFishingGui[state][0])
        self.lineTwoTransitTextNode.setText(PLocalizer.LegendaryFishingGui[state][1])

    def resetInterval(self):
        self.transitionTextMovingSequence.pause()
        self.transitionTextMovingSequence.clearToInitial()
        self.lineOneColorChange.pause()
        self.lineOneColorChange.clearToInitial()
        self.lineOnePosChange.pause()
        self.lineOnePosChange.clearToInitial()
        self.lineTwoCholorChange.pause()
        self.lineTwoCholorChange.clearToInitial()
        self.lineTwoPosChange.pause()
        self.lineTwoPosChange.clearToInitial()
        self.luiReelTransitSequence.pause()
        self.luiReelTransitSequence.clearToInitial()
        self.luiStruggleTransitSequence.pause()
        self.luiStruggleTransitSequence.clearToInitial()
        self.luiFightTransitSequence.pause()
        self.luiFightTransitSequence.clearToInitial()
        self.buttonGrowUpInterval.pause()
        self.buttonGrowUpInterval.clearToInitial()
        self.meterFadeOutInterval.pause()
        self.meterFadeOutInterval.clearToInitial()
        self.rodFadeInInterval.pause()
        self.rodFadeInInterval.clearToInitial()
        self.meterFadeInInterval.pause()
        self.meterFadeInInterval.clearToInitial()
        self.rodFadeOutInterval.pause()
        self.rodFadeOutInterval.clearToInitial()

    def fightingTransit(self):
        self.luiFightTransitSequence.start()

    def reelTransit(self):
        self.luiReelTransitSequence.start()

    def struggleTransit(self):
        self.luiStruggleTransitSequence.start()

    def resetFishingRod(self):
        self.fishingRod.setR(FishingGlobals.fishingRodInitSlope)

    def showWinImage(self, fish):
        self.hideGui(['meterFrame', 'fishingHandleBaseFrame'])
        result = fish.myData['name'].split(' ')
        fileName = str(result[0]).capitalize()
        imgName = 'pir_t_gui_fsh_render%s' % fileName
        self.actorAnim['swimIdleOpposite'] = 'models/char/pir_a_gam_fsh_%s_%s.bam' % (fish.myData['model'], 'swimIdleOpposite')
        self.fishActor = BlendActor('models/char/pir_r_gam_fsh_%s.bam' % fish.myData['model'], self.actorAnim, FishingGlobals.defaultFishBlendTime, FishingGlobals.fishBlendTimeDict)
        self.fishActor.setPlayRate(fish.myData['speed'] * fish.myData['swimAnimationMultiplier'], 'swimIdleOpposite')
        self.fishActor.changeAnimationTo('swimIdleOpposite')
        self.fishActor.reparentTo(self.winImagePanel)
        self.fishActor.setScale(self.scaleSize[fish.myData['id']])
        self.fishActor.setPos(1.7, 0, 1.0)
        self.fishActor.setHpr(0, 0, 35)
        self.fishActor.setDepthWrite(True)
        self.fishActor.setDepthTest(True)
        self.wholeStoryTextNode.setText(PLocalizer.LegendSelectionGui['wholeStory'][fish.myData['id']])
        self.winImagePanel.show()

    def closeDialogGotNextState(self, object, targetState, ifFadeInAgain):
        if self.fishActor:
            self.fishActor.destroy()
            self.fishActor = None
        self.luiCloseDialogSequence = Sequence(Func(self.gameObject.distributedFishingSpot.fadeOut), Wait(0.4), Func(self.UICompoments[object].hide), Func(self.gameObject.lfgFsm.request, targetState), name=self.gameObject.distributedFishingSpot.uniqueName('luiCloseDialogSequence'))
        self.luiCloseDialogSequence.start()
        return

    def updateStruggleTimerText(self, time, percent):
        self.meterFrame['text'] = str(time)
        self.meterFrame['text_fg'] = (1.0 - percent, percent, 0.0, 1.0)