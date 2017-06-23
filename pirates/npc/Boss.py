from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.battle import EnemyGlobals
from pirates.npc.BossBase import BossBase
from pirates.pirate import AvatarTypes
from pirates.effects.BossEffect import BossEffect
from pirates.effects.BossAura import BossAura
from direct.showbase.DirectObject import DirectObject

class Boss(BossBase):

    def __init__(self, cr):
        BossBase.__init__(self, cr)
        self.effectIval = None
        self.auraEffect = None
        self.bossEffect = None
        self.geometryNode = None
        self.instanceNode = None
        self.effectsNode = None
        return

    def setupBoss(self, isUndead=1, override=False):
        if not override:
            if self.instanceNode or base.options.getCharacterDetailSetting() == 0:
                return
        root = self
        if hasattr(self, 'creature'):
            root = self.creature
        if root.hasLOD():
            geom = root.getLOD('500')
            if not geom:
                geom = root.getLOD('low')
            geom = geom.getChild(0)
            while not geom.find('**/weapon*').isEmpty():
                geom = geom.getChild(0)

        else:
            geom = root.getGeomNode().find('**/*actorGeom*')
        parent = root.getGeomNode()
        self.geometryNode = parent.attachNewNode('GeometryNode')
        self.instanceNode = parent.attachNewNode('InstanceNode')
        self.effectsNode = parent.attachNewNode('EffectsNode')
        parent.getChild(0).reparentTo(self.geometryNode)
        geom.instanceTo(self.instanceNode)
        if base.useStencils:
            mask = 255
            ref = isUndead * 2 + 2
            stencil_A = StencilAttrib.make(1, StencilAttrib.SCFAlways, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOReplace, 6, mask, mask)
            stencil_B = StencilAttrib.make(1, StencilAttrib.SCFGreaterThan, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOReplace, ref, mask, mask)
            stencil_C = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, ref, mask, mask)
            self.geometryNode.setAttrib(stencil_A)
            self.instanceNode.setAttrib(stencil_B)
            self.effectsNode.setAttrib(stencil_C)
        else:
            self.instanceNode.hide()
            self.effectsNode.hide()
        self.instanceNode.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.instanceNode.setTransparency(1, 1)
        self.instanceNode.setDepthWrite(0)
        self.instanceNode.setTextureOff(10000)
        ts = TextureStage('ts')
        ts.setCombineRgb(ts.CMReplace, ts.CSConstant, ts.COSrcColor)
        ts.setCombineAlpha(ts.CMReplace, ts.CSConstant, ts.COSrcAlpha)
        ts.setColor(Vec4(1, 1, 1, 0.01))
        image = PNMImage.PNMImage(2, 2)
        t = Texture.Texture()
        t.load(image)
        self.instanceNode.setTexture(ts, t)
        self.instanceNode.getState().getAttrib(TextureAttrib.getClassType()).addOnStage(ts, t)

    def _getBossModelScale(self):
        return self.bossData['ModelScale']

    def getEnemyScale(self):
        return EnemyGlobals.getEnemyScale(self, self._getBossModelScale())

    def skipBossEffect(self):
        return False

    def addBossEffect(self, avType):
        if self.skipBossEffect():
            return
        isUndead = avType != AvatarTypes.Navy
        if not self.instanceNode:
            self.setupBoss(isUndead)
        color = Vec4(0.25, 0.8, 0.0, 1.0)
        if not isUndead:
            color = Vec4(1.0, 1.0, 0.0, 1.0)
        startScale = Vec3(1.025, 1.025, 1.01)
        endScale = Vec3(1.15, 1.1, 1.01)
        if base.options.getCharacterDetailSetting() > 0 or self.getName() == 'Jolly Roger':
            self.effectIval = Sequence(LerpScaleInterval(self.instanceNode, 0.5, endScale, startScale=startScale), LerpScaleInterval(self.instanceNode, 0.5, startScale, startScale=endScale))
            self.effectIval.loop()
            self.bossEffect = BossEffect.getEffect(unlimited=True)
            if self.bossEffect:
                self.bossEffect.reparentTo(self.effectsNode)
                self.bossEffect.setEffectScale(3.0)
                self.bossEffect.setEffectColor(color)
                self.bossEffect.setPos(0, 0, 10.0)
                self.bossEffect.startLoop()
            if hasattr(self, 'creature'):
                headNode = self.creature.headNode
            else:
                headNode = self.headNode
            self.auraEffect = BossAura.getEffect()
            if self.auraEffect and base.useStencils:
                scale = self.getEnemyScale()
                mult = EffectModifiers[avType][0]
                offset = EffectModifiers[avType][1]
                if not headNode.isEmpty():
                    self.auraEffect.reparentTo(headNode)
                    stencil = StencilAttrib.make(1, StencilAttrib.SCFAlways, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 4, 255, 255)
                    self.auraEffect.setAttrib(stencil, 1)
                    self.auraEffect.setScale(scale * mult)
                    self.auraEffect.setEffectColor(color)
                    self.auraEffect.setHpr(0, 0, -90)
                    self.auraEffect.setPos(offset)
                self.auraEffect.startLoop()

    def removeBossEffect(self):
        if self.effectIval:
            self.effectIval.pause()
            self.effectIval = None
        if self.bossEffect:
            self.bossEffect.stopLoop()
            self.bossEffect = None
        if self.auraEffect:
            self.auraEffect.stopLoop()
            self.auraEffect = None
        return

    def getShortName(self):
        return self._getBossName()


EffectModifiers = {AvatarTypes.Undead: [1.0, Point3(-1.3, 0, 0)],AvatarTypes.Navy: [1.0, Point3(-1.3, 0, 0)],AvatarTypes.Alligator: [0.75, Point3(0.75, 0, 0)],AvatarTypes.Bat: [0.6, Point3(0, 0, 0)],AvatarTypes.Crab: [1.0, Point3(0, 0, 0)],AvatarTypes.FlyTrap: [2.5, Point3(2.5, 0, 0)],AvatarTypes.Scorpion: [0.3, Point3(0, 0, 0)],AvatarTypes.Stump: [1.25, Point3(0, 0, 0)],AvatarTypes.Wasp: [0.25, Point3(-0.1, 0, 0)],AvatarTypes.Townfolk: [1.0, Point3(-1.3, 0, 0)]}