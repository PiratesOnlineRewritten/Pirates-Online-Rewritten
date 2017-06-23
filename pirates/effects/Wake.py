from pandac.PandaModules import *
from libpirates import SeaPatchNode
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from direct.task import Task
import random
from otp.otpbase import OTPRender
from pirates.ship import ShipGlobals
from pirates.effects.WaterShadow import WaterShadow
from pirates.piratesbase import PiratesGlobals
from otp.otpbase import OTPRender

class Wake(PooledEffect):
    MinWakeVelocity = 6.0
    FadeOutVelocity = 10.0
    WakeFactor = 0.025
    TurnFactor = -2.0
    AvgCount = 50
    TexStage = TextureStage.getDefault()

    def __init__(self):
        PooledEffect.__init__(self)
        self.taskName = None
        self.u = 0.0
        self.pastForwardVelocity = []
        self.pastRotationalVelocity = []
        self.wake = Actor.Actor('models/sea/wake_zero', {'still': 'models/sea/wake_still'})
        self.wake.hide(OTPRender.MainCameraBitmask)
        self.wake.showThrough(OTPRender.EnviroCameraBitmask)
        self.bend = self.wake.controlJoint(None, 'modelRoot', 'def_wake_2')
        self.wake.controlJoint(self.bend, 'modelRoot', 'def_wake_3')
        self.wake.controlJoint(self.bend, 'modelRoot', 'def_wake_4')
        self.wake.loop('still')
        self.bowWave = NodePath('bowWave')
        if hasattr(base, 'pe'):
            spn = SeaPatchNode('spn', base.pe.seaPatch.patch)
        else:
            spn = SeaPatchNode('spn', base.cr.activeWorld.getWater().patch)
        spn.setWantColor(0)
        spn.setWantUv(0)
        spn.setWantNormal(0)
        spn.setWantReflect(0)
        self.spNP = self.wake.getGeomNode().getChild(0).attachNewNode(spn)
        self.wake.find('**/wake1').reparentTo(self.spNP)
        self.wake.find('**/wake2').reparentTo(self.spNP)
        spn.collectGeometry()
        self.use_water_bin = True
        self.use_depth_offset = False
        if self.use_water_bin:
            self.spNP.setBin('water', 9)
            if self.use_depth_offset:
                depth_offset = DepthOffsetAttrib.make(5)
                self.spNP.setAttrib(depth_offset)
        else:
            self.wake.setBin('ground', -7)
            self.bowWave.setBin('fixed', 0)
            self.spNP.setBin('ground', -5)
        if self.use_depth_offset:
            pass
        else:
            self.spNP.setDepthTest(0)
        self.wake.setAttrib(ColorWriteAttrib.make(ColorWriteAttrib.CRed | ColorWriteAttrib.CGreen | ColorWriteAttrib.CBlue))
        if hasattr(base, 'pe'):
            spn.setEffect(CompassEffect.make(base.pe.seaPatch.patchNP, CompassEffect.PZ))
        else:
            spn.setEffect(CompassEffect.make(base.cr.activeWorld.getWater().patchNP, CompassEffect.PZ))
        if self.use_water_bin:
            mask = 4294967295L
            stencil = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 1, mask, mask)
            self.spNP.setAttrib(stencil)
            if not base.useStencils:
                self.spNP.hide()
        self.shadow = None
        return

    def attachToShip(self, ship):
        self.taskName = ship.taskName('wake')
        draw_shadow = True
        shadow_offset_x = 0.0
        shadow_offset_y = 0.0
        shadow_offset_z = 0.0
        scale_x = 1.0
        scale_y = 1.0
        scale_z = 1.0
        wake_offset_x = 0.0
        wake_offset_y = 125.0
        wake_offset_z = 0.0
        wake_scale = 0.6
        string = 'UNKNOWN'
        self.shadow_model = None
        model = ShipGlobals.getModelClass(ship.shipClass)
        if model == ShipGlobals.INTERCEPTORL1:
            scale_x = 0.7
            scale_y = 0.55
            if hasattr(base, 'pe'):
                shadow_offset_y = 10
            else:
                shadow_offset_y = -10.0
            self.shadow_model = loader.loadModel('models/sea/shadow_merchant')
            if hasattr(base, 'pe'):
                wake_offset_y = -16.5
            else:
                wake_offset_y = 22.5
            wake_scale = 0.18
            string = 'INTERCEPTORL1'
        if model == ShipGlobals.INTERCEPTORL2:
            scale_x = 0.7 / 0.75
            scale_y = 0.55 / 0.75
            self.shadow_model = loader.loadModel('models/sea/shadow_merchant')
            if hasattr(base, 'pe'):
                wake_offset_y = -26.5 / 0.75
            else:
                wake_offset_y = 22.5 / 0.75
            wake_scale = 0.18 / 0.75
            string = 'INTERCEPTORL2'
        if model == ShipGlobals.INTERCEPTORL3 or model == ShipGlobals.SKEL_INTERCEPTORL3:
            scale_x = 0.7 / 0.75 / 0.75
            scale_y = 0.55 / 0.75 / 0.75
            self.shadow_model = loader.loadModel('models/sea/shadow_merchant')
            if hasattr(base, 'pe'):
                wake_offset_y = -26.5 / 0.75 / 0.75
            else:
                wake_offset_y = 22.5 / 0.75 / 0.75
            wake_scale = 0.18 / 0.75 / 0.75
            string = 'INTERCEPTORL3'
        if model == ShipGlobals.QUEEN_ANNES_REVENGE:
            scale_x = 0.7 / 0.75 / 0.75
            scale_y = 0.55 / 0.75 / 0.75
            self.shadow_model = loader.loadModel('models/sea/shadow_merchant')
            if hasattr(base, 'pe'):
                wake_offset_y = -26.5 / 0.75 / 0.75
            else:
                wake_offset_y = 22.5 / 0.75 / 0.75
            wake_scale = 0.18 / 0.75 / 0.75
            string = 'QUEEN_ANNES_REVENGE'
        if model == ShipGlobals.MERCHANTL1:
            scale_x = 1.05
            scale_y = 1.05
            self.shadow_model = loader.loadModel('models/sea/shadow_merchant')
            if hasattr(base, 'pe'):
                wake_offset_y = -80.0 * 0.7
            else:
                wake_offset_y = 80.0 * 0.7
            wake_scale = 0.5 * 0.7
            string = 'MERCHANTL1'
        if model == ShipGlobals.MERCHANTL2:
            scale_x = 1.5
            scale_y = 1.5
            self.shadow_model = loader.loadModel('models/sea/shadow_merchant')
            if hasattr(base, 'pe'):
                wake_offset_y = -80.0
            else:
                wake_offset_y = 80.0
            wake_scale = 0.5
            string = 'MERCHANTL2'
        if model == ShipGlobals.MERCHANTL3:
            scale_x = 1.85
            scale_y = 1.85
            self.shadow_model = loader.loadModel('models/sea/shadow_merchant')
            if hasattr(base, 'pe'):
                wake_offset_y = -80.0 * 1.2333
            else:
                wake_offset_y = 80.0 * 1.2333
            wake_scale = 0.5 * 1.2333
            string = 'MERCHANTL3'
        if model == ShipGlobals.WARSHIPL1:
            scale_x = 1.08 * 0.75 * 0.75
            scale_y = 1.01 * 0.75 * 0.75
            self.shadow_model = loader.loadModel('models/sea/shadow_warship')
            wake_scale = 0.6 * 0.7 * 0.7
            if hasattr(base, 'pe'):
                wake_offset_y = -125.0 * 0.7 * 0.7
            else:
                wake_offset_y = 125.0 * 0.7 * 0.7
            string = 'WARSHIPL1'
        if model == ShipGlobals.WARSHIPL2:
            scale_x = 1.08 * 0.75
            scale_y = 1.01 * 0.75
            self.shadow_model = loader.loadModel('models/sea/shadow_warship')
            wake_scale = 0.6 * 0.7
            if hasattr(base, 'pe'):
                wake_offset_y = -125.0 * 0.7
            else:
                wake_offset_y = 125.0 * 0.7
            string = 'WARSHIPL2'
        if model == ShipGlobals.WARSHIPL3:
            scale_x = 1.08
            scale_y = 1.05
            self.shadow_model = loader.loadModel('models/sea/shadow_warship')
            wake_scale = 0.6
            if hasattr(base, 'pe'):
                wake_offset_y = -125.0
            else:
                wake_offset_y = 125.0
            string = 'WARSHIPL3'
        if model == ShipGlobals.BRIGL1:
            scale_x = 1.08 * 0.75 * 0.75
            scale_y = 1.01 * 0.75 * 0.8
            self.shadow_model = loader.loadModel('models/sea/shadow_warship')
            wake_scale = 0.6 * 0.7 * 0.7
            if hasattr(base, 'pe'):
                wake_offset_y = -125.0 * 0.7 * 0.7
            else:
                wake_offset_y = 125.0 * 0.7 * 0.7
            string = 'BRIGL1'
        if model == ShipGlobals.BRIGL2:
            scale_x = 1.08 * 0.75
            scale_y = 1.01 * 0.8
            self.shadow_model = loader.loadModel('models/sea/shadow_warship')
            wake_scale = 0.6 * 0.7
            if hasattr(base, 'pe'):
                wake_offset_y = -125.0 * 0.7
            else:
                wake_offset_y = 125.0 * 0.7
            string = 'BRIGL2'
        if model == ShipGlobals.BRIGL3:
            scale_x = 1.08 * 0.95
            scale_y = 1.05 * 1.1
            self.shadow_model = loader.loadModel('models/sea/shadow_warship')
            wake_scale = 0.6
            if hasattr(base, 'pe'):
                wake_offset_y = -125.0
            else:
                wake_offset_y = 125.0
            string = 'BRIGL3'
        if model == ShipGlobals.SKEL_WARSHIPL3:
            scale = 0.725
            scale_x = 1.08 * scale
            scale_y = 1.22 * scale
            if hasattr(base, 'pe'):
                shadow_offset_y = 10.0
            else:
                shadow_offset_y = -12.5
            self.shadow_model = loader.loadModel('models/sea/shadow_warship')
            wake_scale = 0.5 * scale
            if hasattr(base, 'pe'):
                wake_offset_y = -85.0 * scale
            else:
                wake_offset_y = 85.0 * scale
            string = 'SKEL_WARSHIPL3'
        if model == ShipGlobals.BLACK_PEARL:
            scale_x = 1.05
            scale_y = 1.08
            self.shadow_model = loader.loadModel('models/sea/shadow_warship')
            wake_scale = 0.6
            wake_offset_y = 100.0
            string = 'BLACK_PEARL'
        if model == ShipGlobals.SHIP_OF_THE_LINE:
            scale_x = 1.05
            scale_y = 1.08
            self.shadow_model = loader.loadModel('models/sea/shadow_warship')
            wake_scale = 0.6
            wake_offset_y = 100.0
            string = 'SHIP_OF_THE_LINE'
        if model == ShipGlobals.DAUNTLESS:
            string = 'DAUNTLESS'
        if model == ShipGlobals.FLYING_DUTCHMAN:
            string = 'FLYING_DUTCHMAN'
        if draw_shadow:
            if self.shadow_model:
                water_shadow = WaterShadow('p_ship_shadow', self.shadow_model, ship)
                water_shadow.setPos(shadow_offset_x, shadow_offset_y, shadow_offset_z)
                water_shadow.setScale(scale_x, scale_y, scale_z)
                if not hasattr(base, 'pe'):
                    water_shadow.setHpr(180, 0, 0)
                self.shadow = water_shadow
            else:
                print 'ERROR: -------------- shadow model not found for ship class', ship.shipClass
        self.wake.setScale(wake_scale)
        if not hasattr(base, 'pe'):
            self.wake.setHpr(180, 0, 0)
        self.wake.setPos(wake_offset_x, wake_offset_y, wake_offset_z)
        self.wake.reparentTo(ship)
        self.wake.hide()
        return

    def startAnimate(self, ship):
        self.stopAnimate()
        self.wake.show()
        taskMgr.add(self.__animate, self.taskName, extraArgs=[ship])

    def stopAnimate(self):
        if self.wake:
            if not self.wake.isEmpty():
                self.wake.hide()
        if self.taskName:
            taskMgr.remove(self.taskName)

    def __animate(self, ship):
        self.pastForwardVelocity.append(ship.getForwardVelocity())
        while len(self.pastForwardVelocity) > self.AvgCount:
            del self.pastForwardVelocity[0]

        self.pastRotationalVelocity.append(ship.getRotationalVelocity())
        while len(self.pastRotationalVelocity) > self.AvgCount:
            del self.pastRotationalVelocity[0]

        velocity = sum(self.pastForwardVelocity) / len(self.pastForwardVelocity)
        rotationalVelocity = sum(self.pastRotationalVelocity) / len(self.pastRotationalVelocity)
        if velocity < self.MinWakeVelocity:
            self.wake.hide()
            self.bowWave.hide()
        elif velocity < self.FadeOutVelocity:
            self.wake.show()
            self.bowWave.show()
            scale = (velocity - self.MinWakeVelocity) / (self.FadeOutVelocity - self.MinWakeVelocity)
            self.wake.setAlphaScale(scale)
            self.bowWave.setAlphaScale(scale)
        else:
            self.wake.show()
            self.bowWave.show()
            self.wake.clearColorScale()
            self.bowWave.clearColorScale()
        dt = globalClock.getDt()
        self.u = (self.u + -dt * velocity * self.WakeFactor) % 1.0
        self.wake.setTexOffset(self.TexStage, self.u, 0)
        self.bowWave.setTexOffset(self.TexStage, self.u, 0)
        self.bend.setH(rotationalVelocity * self.TurnFactor)
        return Task.cont

    def startFakeAnimate(self):
        self.wake.show()
        taskMgr.add(self.__fakeAnimate, self.taskName)

    def stopFakeAnimate(self):
        if self.wake:
            if not self.wake.isEmpty():
                self.wake.hide()
        if self.taskName:
            taskMgr.remove(self.taskName)

    def __fakeAnimate(self, task):
        velocity = 90.0
        if velocity < self.MinWakeVelocity:
            self.wake.hide()
            self.bowWave.hide()
        elif velocity < self.FadeOutVelocity:
            self.wake.show()
            self.bowWave.show()
            scale = (velocity - self.MinWakeVelocity) / (self.FadeOutVelocity - self.MinWakeVelocity)
            self.wake.setAlphaScale(scale)
            self.bowWave.setAlphaScale(scale)
        else:
            self.wake.show()
            self.bowWave.show()
            self.wake.clearColorScale()
            self.bowWave.clearColorScale()
        dt = globalClock.getDt()
        self.u = (self.u + -dt * velocity * self.WakeFactor) % 1.0
        self.wake.setTexOffset(self.TexStage, self.u, 0)
        self.bowWave.setTexOffset(self.TexStage, self.u, 0)
        return Task.cont

    def cleanUpEffect(self):
        self.stopAnimate()
        self.wake.detachNode()
        self.bowWave.detachNode()
        self.checkInEffect(self)
        if self.shadow != None:
            self.shadow.detachNode()
        return

    def destroy(self):
        self.stopAnimate()
        self.wake.removeNode()
        self.bowWave.removeNode()
        if self.shadow != None:
            self.shadow.removeNode()
        PooledEffect.destroy(self)
        return