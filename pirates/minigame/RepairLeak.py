import math
from pandac.PandaModules import MouseButton
from pandac.PandaModules import ColorBlendAttrib
from direct.interval.IntervalGlobal import Sequence, Func, LerpScaleInterval
from direct.gui.DirectGui import DirectButton, DirectLabel, DGG
from direct.task import Task
from direct.fsm import FSM
from pandac.PandaModules import TransformState
from pandac.PandaModules import Texture
from pandac.PandaModules import TextureStage
from direct.interval.IntervalGlobal import *
from pirates.piratesgui.GuiPanel import *
import random
_activePosition = 0.5

class RepairLeak(DirectButton, FSM.FSM):

    def __init__(self, name, parent, leakscale, **kw):
        pitchingGui = loader.loadModel('models/gui/pir_m_gui_srp_pitching_main')
        self.hole = pitchingGui.find('**/hole')
        if random.random() > 0.5:
            self.holeFilled = pitchingGui.find('**/pitch1')
        else:
            self.holeFilled = pitchingGui.find('**/pitch2')
        optiondefs = (
         ('relief', None, None), ('geom', (self.hole, self.hole, self.hole, self.holeFilled), None), ('rolloverSound', None, None), ('clickSound', None, None))
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent=parent, **kw)
        self.initialiseoptions(RepairLeak)
        self.name = name
        FSM.FSM.__init__(self, 'leak_%sFSM' % self.name)
        self.onCleanup = None
        self.leakScale = leakscale
        self.pitchingGame = parent
        self._initVars()
        self._initVisuals()
        self._initIntervals()
        self.fadeSequence = None
        self.request('Idle')
        return

    def _initVars(self):
        self.timeActive = 0.0
        self.pulseScale = 0.6

    def _initVisuals(self):
        textureCard = loader.loadModel('models/minigames/pir_m_gam_srp_water')
        self.waterStream = textureCard.find('**/waterPlane')
        tex = textureCard.findTexture('pir_t_gui_srp_waterDrops')
        textureCard2 = loader.loadModel('models/minigames/pir_m_gam_srp_water')
        self.waterStream2 = textureCard2.find('**/waterPlane')
        tex2 = textureCard2.findTexture('pir_t_gui_srp_waterDrops')
        alphaCard = loader.loadModel('models/minigames/pir_m_gui_srp_waterDropsAlpha')
        self.alphaWaterStream = textureCard.find('**/pir_t_gui_srp_waterDropsAlpha')
        alphatex = alphaCard.find('**/pir_t_gui_srp_waterDropsAlpha').findTexture('*')
        self.alphaWaterStream2 = textureCard.find('**/pir_t_gui_srp_waterDropsAlpha2')
        alphatex2 = alphaCard.find('**/pir_t_gui_srp_waterDropsAlpha2').findTexture('*')
        alphaCard2 = loader.loadModel('models/minigames/pir_m_gui_srp_waterDropsAlpha')
        self.alphaWaterStream3 = textureCard.find('**/pir_t_gui_srp_waterDropsAlpha')
        alphatex3 = alphaCard2.findTexture('*')
        self.alphaWaterStream4 = textureCard.find('**/pir_t_gui_srp_waterDropsAlpha2')
        alphatex4 = alphaCard2.findTexture('*')
        tex.setWrapU(Texture.WMRepeat)
        tex.setWrapV(Texture.WMRepeat)
        alphatex.setWrapU(Texture.WMRepeat)
        alphatex.setWrapV(Texture.WMRepeat)
        tex2.setWrapU(Texture.WMRepeat)
        tex2.setWrapV(Texture.WMRepeat)
        alphatex3.setWrapU(Texture.WMRepeat)
        alphatex3.setWrapV(Texture.WMRepeat)
        self.setScale(2.5 * self.leakScale)
        self.waterStream.setScale(self.leakScale)
        self.waterStream.setPos(self.getX(), 0.0, -0.5 * self.leakScale + self.getZ())
        self.waterStream2.setScale(self.leakScale * 0.8, self.leakScale, self.leakScale * 1.2)
        self.waterStream2.setPos(self.getX(), 0.0, -0.6 * self.leakScale + self.getZ())
        self.waterStream.setColor(0.7, 0.85, 1.0, 1.0)
        self.waterStream2.setColor(0.5, 0.6, 0.9, 1.0)
        self.waterStream2.reparentTo(self.pitchingGame)
        self.waterStream.reparentTo(self.pitchingGame)
        self.waterStream2.setBin('fixed', 42)
        self.waterStream.setBin('fixed', 40)
        self.textureYOffset = random.random()
        self.textureYDelta = 0.25 + 0.025 / self.leakScale
        self.textureYOffset2 = random.random()
        self.textureYDelta2 = 0.25412354 + 0.058754645634 / self.leakScale
        self.textureYOffsetAlpha = 0.0
        self.textureYDeltaAlpha = 0.25 + 0.025 / self.leakScale
        self.textureYOffsetAlpha2 = 0.0
        self.textureYDeltaAlpha2 = 0.25412354 + 0.058754645634 / self.leakScale
        self.textureStage = self.waterStream.findTextureStage('*')
        self.textureStage2 = self.waterStream2.findTextureStage('*')
        self.textureStage3 = TextureStage('alphaLayer')
        self.textureStage3.setMode(TextureStage.MModulate)
        self.textureStage3.setSort(1)
        self.waterStream.setTexture(self.textureStage3, alphatex)
        self.textureStage4 = TextureStage('alphaLayer2')
        self.textureStage4.setMode(TextureStage.MModulate)
        self.textureStage4.setSort(2)
        self.waterStream.setTexture(self.textureStage4, alphatex2)
        trans = TransformState.makePos((0, 0.48, 0))
        self.waterStream.setTexTransform(self.textureStage4, trans)
        self.textureStage5 = TextureStage('alphaLayer3')
        self.textureStage5.setMode(TextureStage.MModulate)
        self.textureStage5.setSort(1)
        self.waterStream2.setTexture(self.textureStage5, alphatex3)
        self.textureStage6 = TextureStage('alphaLayer4')
        self.textureStage6.setMode(TextureStage.MModulate)
        self.textureStage6.setSort(2)
        self.waterStream2.setTexture(self.textureStage6, alphatex4)
        trans = TransformState.makePos((0, 0.48, 0))
        self.waterStream2.setTexTransform(self.textureStage6, trans)

    def repositionTo(self, newX, newZ):
        self.setPos(newX, 0.0, newZ)
        self.waterStream.setPos(self.getX(), 0.0, -0.5 * self.leakScale + self.getZ())
        self.waterStream2.setPos(self.getX(), 0.0, -0.6 * self.leakScale + self.getZ())

    def _initIntervals(self):
        pass

    def destroy(self):
        if self.fadeSequence is not None:
            self.fadeSequence.clearToInitial()
        self['extraArgs'] = None
        taskMgr.remove('RepairLeak_%s.update' % self.name)
        if self.onCleanup is not None:
            self.onCleanup(self)
        self.cleanup()
        self.waterStream.removeNode()
        self.waterStream2.removeNode()
        DirectButton.destroy(self)
        return

    def update(self, task):
        dt = globalClock.getDt()
        self.timeActive += dt
        self.textureYOffset += self.textureYDelta * dt
        trans = TransformState.makePos((0, self.textureYOffset, 0))
        self.waterStream.setTexTransform(self.textureStage, trans)
        done = False
        if self.getCurrentOrNextState() == 'Active' and self.textureYOffsetAlpha < _activePosition:
            self.textureYOffsetAlpha += self.textureYDeltaAlpha * dt
            if self.textureYOffsetAlpha > _activePosition:
                self.textureYOffsetAlpha = _activePosition
            trans2 = TransformState.makePos((0, self.textureYOffsetAlpha, 0))
            self.waterStream.setTexTransform(self.textureStage3, trans2)
        if self.getCurrentOrNextState() == 'Patched':
            if self.textureYOffsetAlpha < _activePosition:
                self.textureYOffsetAlpha = 0.75 - self.textureYOffsetAlpha / 2.0
                trans2 = TransformState.makePos((0, self.textureYOffsetAlpha, 0))
                self.waterStream.setTexTransform(self.textureStage3, trans2)
            elif self.textureYOffsetAlpha < 1.0:
                self.textureYOffsetAlpha += self.textureYDeltaAlpha * dt
                trans2 = TransformState.makePos((0, self.textureYOffsetAlpha, 0))
                self.waterStream.setTexTransform(self.textureStage3, trans2)
        self.textureYOffset2 += self.textureYDelta2 * dt
        trans = TransformState.makePos((0, self.textureYOffset2, 0))
        self.waterStream2.setTexTransform(self.textureStage2, trans)
        if self.getCurrentOrNextState() == 'Active' and self.textureYOffsetAlpha2 < _activePosition:
            self.textureYOffsetAlpha2 += self.textureYDeltaAlpha2 * dt
            if self.textureYOffsetAlpha2 > _activePosition:
                self.textureYOffsetAlpha2 = _activePosition
            trans2 = TransformState.makePos((0, self.textureYOffsetAlpha2, 0))
            self.waterStream2.setTexTransform(self.textureStage5, trans2)
        if self.getCurrentOrNextState() == 'Patched':
            if self.textureYOffsetAlpha2 < _activePosition:
                self.textureYOffsetAlpha2 = 0.75 - self.textureYOffsetAlpha2 / 2.0
                trans2 = TransformState.makePos((0, self.textureYOffsetAlpha2, 0))
                self.waterStream2.setTexTransform(self.textureStage5, trans2)
            if self.textureYOffsetAlpha2 < 1.0:
                self.textureYOffsetAlpha2 += self.textureYDeltaAlpha2 * dt
                trans2 = TransformState.makePos((0, self.textureYOffsetAlpha2, 0))
                self.waterStream2.setTexTransform(self.textureStage5, trans2)
            else:
                done = True
        if done:
            self.waterStream.stash()
            self.waterStream2.stash()
            self.fadeSequence = Sequence(LerpColorScaleInterval(self, duration=2.0, colorScale=(1.0,
                                                                                                1.0,
                                                                                                1.0,
                                                                                                0.0)), Func(self.destroy))
            self.fadeSequence.start()
            return Task.done
        else:
            return Task.cont

    def setCommandButtons(self):
        self.guiItem.addClickButton(MouseButton.one())
        self.bind(DGG.B1PRESS, self.commandFunc)

    def enterIdle(self):
        self.stash()
        self.waterStream.stash()
        self.waterStream2.stash()
        self['state'] = DGG.DISABLED

    def exitIdle(self):
        pass

    def enterPatched(self):
        self['state'] = DGG.DISABLED
        self.setScale(0.85)

    def exitPatched(self):
        self.stash()
        self.waterStream.stash()
        self.waterStream2.stash()

    def enterActive(self):
        taskMgr.add(self.update, 'RepairLeak_%s.update' % self.name)
        self.unstash()
        self.waterStream.unstash()
        self.waterStream2.unstash()
        self['state'] = DGG.NORMAL

    def exitActive(self):
        self['state'] = DGG.DISABLED