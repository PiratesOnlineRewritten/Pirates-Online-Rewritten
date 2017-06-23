from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from pirates.effects.FuseSparks import FuseSparks
from pirates.effects.SimpleSmokeCloud import SimpleSmokeCloud
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.DustRing import DustRing
from pirates.effects.ShockwaveRing import ShockwaveRing
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class ExplodingBarrel(NodePath):

    def __init__(self):
        NodePath.__init__(self, 'ExplodingBarrel')
        self.model = loader.loadModel('models/handheld/pir_m_hnd_bom_barrelDynamite')
        self.model.reparentTo(self)
        self.sparks = None
        self.smokeVfx = None
        self.explosionVfx = None
        self.dustRingVfx = None
        self.splintersVfx = None
        self.explosionSfx = loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_IMPACT)
        return

    def lightUp(self):
        self.sparks = FuseSparks.getEffect(unlimited=True)
        self.sparks.setPos(0.5, 0, 1.2)
        self.sparks.reparentTo(self)
        self.sparks.startLoop()

    def explode(self):
        base.playSfx(self.explosionSfx, node=self, cutoff=200)
        if self.sparks:
            self.sparks.stopLoop()
            self.sparks = None
        self.model.stash()
        self.explosionVfx = ExplosionFlip.getEffect(unlimited=True)
        if self.explosionVfx:
            self.explosionVfx.reparentTo(self)
            self.explosionVfx.setScale(1.5)
            self.explosionVfx.play()
        self.smokeVfx = SimpleSmokeCloud.getEffect(unlimited=True)
        if self.smokeVfx:
            self.smokeVfx.reparentTo(self)
            self.smokeVfx.setPos(0, 0, 1)
            self.smokeVfx.setEffectScale(1.0)
            self.smokeVfx.play()
        self.dustRingVfx = DustRing.getEffect(unlimited=True)
        if self.dustRingVfx:
            self.dustRingVfx.reparentTo(self)
            self.dustRingVfx.setPos(0, 0, -2)
            self.dustRingVfx.play()
        cameraShakerEffect = CameraShaker()
        cameraShakerEffect.reparentTo(self)
        cameraShakerEffect.shakeSpeed = 0.06
        cameraShakerEffect.shakePower = 4.0
        cameraShakerEffect.scalePower = True
        cameraShakerEffect.numShakes = 2
        cameraShakerEffect.scalePower = 1.0
        cameraShakerEffect.play(120.0)
        self.splintersVfx = ShipSplintersA.getEffect(unlimited=True)
        if self.splintersVfx:
            self.splintersVfx.reparentTo(self)
            self.splintersVfx.setPos(0, 0, -2)
            self.splintersVfx.play()
        shockwaveRingEffect = ShockwaveRing.getEffect(unlimited=True)
        if shockwaveRingEffect:
            shockwaveRingEffect.reparentTo(self)
            shockwaveRingEffect.setPos(0, 0, -2)
            shockwaveRingEffect.size = 80
            shockwaveRingEffect.play()
        return

    def cleanUp(self):
        if self.sparks:
            self.sparks.stopLoop()
            self.sparks = None
        self.model.removeNode()
        if self.smokeVfx:
            self.smokeVfx.cleanUpEffect()
            self.smokeVfx = None
        if self.explosionVfx:
            self.explosionVfx.cleanUpEffect()
            self.explosionVfx = None
        if self.dustRingVfx:
            self.dustRingVfx.cleanUpEffect()
            self.dustRingVfx = None
        if self.splintersVfx:
            self.splintersVfx.cleanUpEffect()
            self.splintersVfx = None
        return