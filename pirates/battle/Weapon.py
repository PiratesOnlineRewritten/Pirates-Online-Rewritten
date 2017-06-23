from direct.showbase.DirectObject import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from pirates.effects.SmokeCloud import SmokeCloud
import WeaponGlobals
from pirates.inventory import ItemGlobals
from pirates.uberdog.UberDogGlobals import *

class Weapon(NodePath):
    notify = DirectNotifyGlobal.directNotify.newCategory('Weapon')
    models = {}
    icons = {}
    walkAnim = 'walk'
    runAnim = 'run'
    walkBackAnim = 'walk'
    neutralAnim = 'idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    strafeDiagLeftAnim = 'run_diagonal_left'
    strafeDiagRightAnim = 'run_diagonal_right'
    strafeRevDiagLeftAnim = 'walk_back_diagonal_left'
    strafeRevDiagRightAnim = 'walk_back_diagonal_right'
    fallGroundAnim = 'fall_ground'
    fallWaterAnim = 'fall_ground'
    spinLeftAnim = 'spin_left'
    spinRightAnim = 'spin_right'
    painAnim = 'boxing_hit_head_right'

    def __init__(self, itemId=None, name='weapon'):
        NodePath.__init__(self, name)
        self.itemId = itemId
        self.modelId = None
        if self.itemId:
            self.modelId = ItemGlobals.getModel(itemId)
        self.effect = None
        self.effect2 = None
        self.effectActor = None
        self.chargeSound = None
        self.chargeLoopSound = None
        self.chargeSoundSequence = None
        self.loadModel()
        self.motion_trail = None
        self.spinBlur = None
        self.ammoSkillId = 0
        return

    def delete(self):
        if self.effect:
            self.effect.stopLoop()
            self.effect = None
        if self.effect2:
            self.effect2.stopLoop()
            self.effect2 = None
        self.removeNode()
        return

    def loadModel(self):
        pass

    def getWalkForWeapon(self, av):
        return [
         self.walkAnim, self.runAnim, self.walkBackAnim, self.neutralAnim, self.strafeLeftAnim, self.strafeRightAnim, self.strafeDiagLeftAnim, self.strafeDiagRightAnim, self.strafeRevDiagLeftAnim, self.strafeRevDiagRightAnim, self.fallGroundAnim, self.fallWaterAnim, self.spinLeftAnim, self.spinRightAnim]

    def getAutoAttackIval(self, av, blendInT, blendOutT):
        return None

    def getAttackIval(self, av, blendInT, blendOutT):
        return None

    def getDrawIval(self, av, ammoSkillId, blendInT, blendOutT):
        return None

    def getReturnIval(self, av, blendInT, blendOutT):
        return None

    def getNeutralIval(self, av, blendInT, blendOutT):
        return None

    def getAmmoChangeIval(self, av, skillId, ammoSkillId, charge, target=None):
        return None

    def updateItemId(self, itemId):
        if self.itemId == itemId:
            return
        self.itemId = itemId
        self.modelId = ItemGlobals.getModel(itemId)
        if hasattr(self, 'prop'):
            self.prop.removeNode()
            self.loadModel()

    def attachTo(self, av):
        if not self.isEmpty():
            if av.rightHandNode:
                self.reparentTo(av.rightHandNode)
            else:
                self.notify.warning('av.rightHandNode is None, just reparenting to av')
                self.reparentTo(av)

    def detachFrom(self, av):
        if not self.isEmpty():
            self.detachNode()

    def hideWeapon(self):
        if not self.isEmpty():
            self.hide()

    def showWeapon(self):
        if not self.isEmpty():
            self.show()

    def beginAttack(self, av, wantTrail=1):
        if self.motion_trail:
            if wantTrail == 1:
                self.motion_trail.beginTrail()
            else:
                self.motion_trail.beginTrailSoft()

    def endAttack(self, av):
        if self.motion_trail:
            self.motion_trail.endTrail()

    def setTrailLength(self, time):
        if self.motion_trail:
            self.motion_trail.setTimeWindow(time)

    def showSpinBlur(self):
        if self.spinBlur:
            if not self.spinBlur.isEmpty():
                self.spinBlur.setColorScale(self.getBlurColor() / 2.0)
                self.spinBlur.show()

    def hideSpinBlur(self):
        if self.spinBlur:
            if not self.spinBlur.isEmpty():
                self.spinBlur.hide()

    def startSpecialEffect(self, skillId=None):
        pass

    def stopSpecialEffect(self, skillId=None):
        pass

    def stopAuraEffects(self):
        pass

    def hideMouse(self, av):
        pass

    def playSkillSfx(self, skillId, node, startTime=0, loud=1):
        vol = 0.5
        if loud:
            vol = 1.0
        if self.isEmpty():
            return
        if self.getName() not in ['sword', 'pistol', 'daggers', 'grenade', 'fishingRod', 'bayonet', 'gun', 'doll']:
            return
        sfxFunc = WeaponGlobals.getWeaponSfx(node.currentWeaponId, skillId)
        if not sfxFunc:
            sfx = self.skillSfxs.get(skillId)
        else:
            sfx = sfxFunc()
        if sfx:
            base.playSfx(sfx, node=node, cutoff=60, time=startTime, volume=vol)

    def getModel(self, itemId):
        if self.modelId:
            if ItemGlobals.getType(self.itemId) == ItemGlobals.GRENADE:
                itemId = 'models/ammunition/' + self.modelId
            elif ItemGlobals.getSubtype(self.itemId) == ItemGlobals.QUEST_PROP_TORCH:
                itemId = 'models/props/' + self.modelId
            elif ItemGlobals.getSubtype(self.itemId) == ItemGlobals.HEALING:
                itemId = 'models/inventory/' + self.modelId
            else:
                itemId = 'models/handheld/' + self.modelId
        model = self.models.get(itemId)
        if not model:
            self.notify.error('failed to load %s, phases complete 3:%s 4:%s 5:%s' % (itemId, launcher.getPhaseComplete(3), launcher.getPhaseComplete(4), launcher.getPhaseComplete(5)))
        lod = model.find('**/+LODNode')
        if lod:
            lastSwitch = lod.getNumChildren() - 1
            switchOut = lod.node().getOut(lastSwitch)
            lod.node().setSwitch(lastSwitch, 1000, switchOut)
        model = model.copyTo(NodePath())
        return model

    def getIcon(self, itemId):
        model = self.icons[itemId]
        model = model.copyTo(hidden)
        model.detachNode()
        return model

    @classmethod
    def loadAsset(cls, modelId):
        model = loader.loadModel(modelId)
        try:
            model.flattenLight()
        except AttributeError:
            cls.notify.error('Could not load %s model: %s' % (cls.__name__, model))

        lod = model.find('**/+LODNode')
        if lod:
            lastSwitch = lod.getNumChildren() - 1
            switchOut = lod.node().getOut(lastSwitch)
            lod.node().setSwitch(lastSwitch, 1000, switchOut)
        cls.models[modelId] = model
        return model

    @classmethod
    def setupAssets(cls):
        if cls.models:
            return
        cls.models = {}
        for item in cls.modelTypes:
            model = loader.loadModel(item)
            try:
                model.flattenLight()
            except AttributeError:
                cls.notify.error('Could not load %s model: %s' % (cls.__name__, model))

            lod = model.find('**/+LODNode')
            if lod:
                lastSwitch = lod.getNumChildren() - 1
                switchOut = lod.node().getOut(lastSwitch)
                lod.node().setSwitch(lastSwitch, 1000, switchOut)
            cls.models[item] = model

        cls.setupSounds()

    @classmethod
    def setupSounds(cls):
        pass

    def getAnimState(self, av, animState):
        return animState

    def getEffectColor(self, itemId=None):
        return Vec4(1, 1, 1, 1)

    def getBlurColor(self):
        return Vec4(1, 1, 1, 1)

    def getOffset(self, itemId=None):
        return Vec3(0, 0, 0)