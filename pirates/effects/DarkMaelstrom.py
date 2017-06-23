from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
import random

class DarkMaelstrom(DirectObject, NodePath):

    def __init__(self, newParent=None):
        NodePath.__init__(self, 'DarkMaelstromParent')
        self.newParent = newParent
        self.setColorScaleOff()
        self.setAttrib(ColorWriteAttrib.make(ColorWriteAttrib.CRed | ColorWriteAttrib.CGreen | ColorWriteAttrib.CBlue))
        self.glow = loader.loadModel('models/effects/GhostShipFX')
        self.glow.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.glow.setDepthWrite(0)
        self.glow.setFogOff()
        self.glow.setLightOff()
        self.glow.setBin('fixed', 120)
        self.glow.reparentTo(self)
        self.bolt1 = self.glow.find('**/lightning_1')
        self.bolt1.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.bolt1.setBillboardAxis()
        self.bolt1.setColorScaleOff()
        self.bolt1.setColor(Vec4(0))
        self.bolt2 = self.glow.find('**/lightning_2')
        self.bolt2.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.bolt2.setBillboardAxis()
        self.bolt2.setColorScaleOff()
        self.bolt2.setColor(Vec4(0))
        self.bolt3 = self.glow.find('**/lightning_3')
        self.bolt3.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.bolt3.setBillboardAxis()
        self.bolt3.setColorScaleOff()
        self.bolt3.setColor(Vec4(0))
        self.bolt4 = self.glow.find('**/lightning_4')
        self.bolt4.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.bolt4.setBillboardAxis()
        self.bolt4.setColorScaleOff()
        self.bolt4.setColor(Vec4(0))
        stormTops = self.glow.findAllMatches('**/Swirl_*')
        for top in stormTops:
            top.setBin('fixed', 125)

        stormTopTs = [ top.findAllTextureStages()[0] for top in stormTops ]
        duration = 20 + random.randint(1, 20)
        rotate = Parallel(stormTops[0].hprInterval(duration, Point3(360, 0, 0), startHpr=Point3(0, 0, 0)), stormTops[1].hprInterval(duration, Point3(0, 0, 0), startHpr=Point3(360, 0, 0)))
        uvScrollTop = Parallel(LerpFunctionInterval(self.setNewUVs, duration, toData=0, fromData=1, extraArgs=[stormTops[0], stormTopTs[0]]), LerpFunctionInterval(self.setNewUVs, duration, fromData=1, toData=0, extraArgs=[stormTops[1], stormTopTs[1]]))
        self.track = Parallel(rotate, uvScrollTop)
        texture = top.findAllTextures()[0]
        texture.setWrapU(Texture.WMRepeat)
        texture.setWrapV(Texture.WMRepeat)
        bolt1In = self.bolt1.colorInterval(0.1, Vec4(1, 1, 1, 1), startColor=Vec4(0, 0, 0, 0))
        bolt1Out = self.bolt1.colorInterval(0.1, Vec4(0, 0, 0, 0), startColor=Vec4(1, 1, 1, 1))
        bolt2In = self.bolt2.colorInterval(0.1, Vec4(1, 1, 1, 1), startColor=Vec4(0, 0, 0, 0))
        bolt2Out = self.bolt2.colorInterval(0.1, Vec4(0, 0, 0, 0), startColor=Vec4(1, 1, 1, 1))
        bolt3In = self.bolt3.colorInterval(0.1, Vec4(1, 1, 1, 1), startColor=Vec4(0, 0, 0, 0))
        bolt3Out = self.bolt3.colorInterval(0.1, Vec4(0, 0, 0, 0), startColor=Vec4(1, 1, 1, 1))
        bolt4In = self.bolt4.colorInterval(0.1, Vec4(1, 1, 1, 1), startColor=Vec4(0, 0, 0, 0))
        bolt4Out = self.bolt4.colorInterval(0.1, Vec4(0, 0, 0, 0), startColor=Vec4(1, 1, 1, 1))
        playBolt1 = Sequence(bolt1In, Wait(0.1), bolt1Out)
        playBolt2 = Sequence(bolt2In, Wait(0.1), bolt2Out)
        playBolt3 = Sequence(bolt3In, Wait(0.1), bolt3Out)
        playBolt4 = Sequence(bolt4In, Wait(0.1), bolt4Out)
        self.lightningTrack = Sequence(Wait(1.0), playBolt1, Wait(0.5), playBolt2, Wait(2.0), playBolt3, Wait(1.5), playBolt4, Wait(0.0))
        self.fadeTrack = None
        return

    def play(self, rate=1):
        self.setColorScaleOff()
        self.track.start()
        self.lightningTrack.start()
        self.reparentTo(self.newParent)

    def loop(self, rate=1):
        self.setColorScaleOff()
        self.track.loop()
        self.lightningTrack.loop()
        self.reparentTo(self.newParent)

    def fadeOutAndStop(self):
        if hasattr(self, 'lightningTrack'):
            self.lightningTrack.finish()
        self.fadeTrack = Sequence(LerpColorScaleInterval(self, 1.0, Vec4(1.0, 1.0, 1.0, 0.0)), Func(self.stop))
        self.fadeTrack.start()

    def stop(self):
        if hasattr(self, 'track'):
            if self.track:
                self.track.finish()
        if hasattr(self, 'lightningTrack'):
            if self.lightningTrack:
                self.lightningTrack.finish()
        if hasattr(self, 'fadeTrack'):
            if self.fadeTrack:
                self.fadeTrack.finish()

    def finish(self):
        self.stop()
        self.cleanUpEffect()

    def cleanUpEffect(self):
        self.detachNode()

    def destroy(self):
        self.stop()
        if hasattr(self, 'track'):
            del self.track
        if hasattr(self, 'lightningTrack'):
            del self.lightningTrack
        if hasattr(self, 'fadeTrack'):
            del self.fadeTrack
        if hasattr(self, 'glow'):
            del self.glow
        self.removeNode()

    def setNewUVs(self, offset, part, ts):
        part.setTexOffset(ts, offset, offset)