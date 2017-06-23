from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.actor import Actor
from pirates.distributed import DistributedInteractive
from pirates.piratesbase import PLocalizer
from pirates.interact import InteractiveBase
from pirates.inventory.Lootable import Lootable
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import GuiButton
from pirates.effects.LootSparks import LootSparks
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
containerCache = {}

class DistributedLootContainer(DistributedInteractive.DistributedInteractive, Lootable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLootContainer')
    ratingTable = {PiratesGlobals.ITEM_SAC: 1,PiratesGlobals.TREASURE_CHEST: 2,PiratesGlobals.RARE_CHEST: 3,PiratesGlobals.UPGRADE_CHEST: 3,PiratesGlobals.RARE_UPGRADE_CHEST: 3}

    def __init__(self, cr):
        NodePath.__init__(self, 'DistributedLootContainer')
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        Lootable.__init__(self)
        self.showLerp = None
        self.appearSound = None
        self.openSound = None
        self.chest = None
        self.type = 0
        self.typeName = ''
        self.creditLocks = []
        self.effect = None
        self.effectScale = 1.25
        return

    def generate(self):
        DistributedInteractive.DistributedInteractive.generate(self)
        self.setTransparency(1)
        self.setColorScale(1, 1, 1, 0)

    def setVisZone(self, zone):
        self.visZone = zone

    def getVisZone(self):
        return self.visZone

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def announceGenerate(self):
        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        self.loadContainer()
        if self.visZone != '':
            self.getParentObj().builder.addSectionObj(self.chest, self.visZone)

    def disable(self):
        DistributedInteractive.DistributedInteractive.disable(self)
        if self.visZone != '':
            self.getParentObj().builder.removeSectionObj(self.chest, self.visZone)
        if self.effect:
            self.effect.stopLoop()
            self.effect = None
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr and base.localAvatar.getPlundering() == self.getDoId():
            base.localAvatar.guiMgr.inventoryUIManager.closePlunder()
        if self.chest:
            self.chest.removeNode()
            self.chest = None
        if self.showLerp:
            self.showLerp.pause()
        if self.appearSound:
            self.appearSound.stop()
            loader.unloadSfx(self.appearSound)
        if self.openSound:
            self.openSound.stop()
            loader.unloadSfx(self.openSound)
        return

    def delete(self):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr and base.localAvatar.getPlundering() == self.getDoId():
            base.localAvatar.guiMgr.inventoryUIManager.closePlunder()
        if self.chest:
            self.chest.removeNode()
        del self.chest
        self.chest = None
        self.showLerp = None
        DistributedInteractive.DistributedInteractive.delete(self)
        return

    def loadContainer(self):
        if self.chest:
            return
        type = self.getType()
        if type == PiratesGlobals.ITEM_SAC:
            self.chest = self.getContainerModel('models/props/pir_m_prp_trs_sack')
            self.chest.setScale(0.75)
            self.effectScale = 1.25
            self.typeName = PLocalizer.LootContainerItemSac
            self.appearSound = loadSfx(SoundGlobals.SFX_FX_SACK_APPEAR_01)
            self.openSound = loadSfx(SoundGlobals.SFX_FX_OPEN_SACK_01)
        else:
            if type == PiratesGlobals.TREASURE_CHEST:
                self.chest = self.getContainerModel('models/props/pir_m_prp_trs_chest_01')
                self.chest.setScale(0.8)
                self.effectScale = 1.5
                self.typeName = PLocalizer.LootContainerTreasureChest
                self.appearSound = loadSfx(SoundGlobals.SFX_FX_CHEST_APPEAR_01)
                self.openSound = loadSfx(SoundGlobals.SFX_FX_OPEN_CHEST_01)
            elif type == PiratesGlobals.RARE_CHEST:
                self.chest = self.getContainerModel('models/props/pir_m_prp_trs_chest_02')
                self.typeName = PLocalizer.LootContainerRareChest
                self.effectScale = 2.0
                self.appearSound = loadSfx(SoundGlobals.SFX_FX_CHEST_APPEAR_02)
                self.openSound = loadSfx(SoundGlobals.SFX_FX_OPEN_CHEST_02)
            elif type == PiratesGlobals.UPGRADE_CHEST:
                self.chest = self.getContainerModel('models/props/pir_m_prp_trs_chest_01')
                self.chest.setScale(0.8)
                self.effectScale = 1.5
                self.typeName = PLocalizer.LootContainerUpgradeChest
                self.appearSound = loadSfx(SoundGlobals.SFX_FX_CHEST_APPEAR_01)
                self.openSound = loadSfx(SoundGlobals.SFX_FX_OPEN_CHEST_01)
            elif type == PiratesGlobals.RARE_UPGRADE_CHEST:
                self.chest = self.getContainerModel('models/props/pir_m_prp_trs_chest_02')
                self.typeName = PLocalizer.LootContainerRareUpgradeChest
                self.effectScale = 2.0
                self.appearSound = loadSfx(SoundGlobals.SFX_FX_CHEST_APPEAR_02)
                self.openSound = loadSfx(SoundGlobals.SFX_FX_OPEN_CHEST_02)
            if type != PiratesGlobals.ITEM_SAC:
                cb = self.chest.find('**/+Character').node().getBundle(0)
                ab = self.chest.find('**/+AnimBundleNode').node().getBundle()
                self.openAnim = cb.bindAnim(ab, -1)
                self.openAnim.pose(0)
        self.chest.setH(180)
        self.chest.reparentTo(self)
        self.appearSound.setVolume(0.8)
        self.openSound.setVolume(0.8)
        self.initInteractOpts()

    def getContainerModel(self, name):
        model = containerCache.get(name)
        if model:
            return model.copyTo(NodePath())
        else:
            model = loader.loadModel(name)
            model.flattenStrong()
            containerCache[name] = model
            return model.copyTo(NodePath())

    def getRating(self):
        return DistributedLootContainer.ratingTable[self.type]

    def requestInteraction(self, avId, interactType=0):
        base.localAvatar.motionFSM.off()
        DistributedInteractive.DistributedInteractive.requestInteraction(self, avId, interactType)

    def rejectInteraction(self):
        base.localAvatar.motionFSM.on()
        DistributedInteractive.DistributedInteractive.rejectInteraction(self)

    def initInteractOpts(self):
        self.setInteractOptions(sphereScale=10, diskRadius=10, proximityText=PLocalizer.LootContainerOpen % self.typeName, exclusive=0)
        self.setAllowInteract(False)

    def setCreditLocks(self, creditLocks):
        if hasattr(base, 'localAvatar') and base.localAvatar.getDoId() in creditLocks:
            self.setAllowInteract(True)
            self.effect = LootSparks.getEffect()
            if self.effect:
                self.effect.reparentTo(self)
                self.effect.setEffectScale(self.effectScale)
                self.effect.startLoop()
            if self.appearSound:
                base.playSfx(self.appearSound, node=self, cutoff=75)
        else:
            if self.effect:
                self.effect.stopLoop()
                self.effect = None
            self.setInteractOptions(sphereScale=0, diskRadius=0, proximityText=PLocalizer.LootContainerOpen % self.typeName, exclusive=0)
            self.setAllowInteract(False)
        return

    def startLooting(self, plunderList, itemsToTake=0, timer=0, autoShow=False, customName=None):
        self.acceptInteraction()
        if self.openSound:
            self.openSound.play()
        Lootable.startLooting(self, plunderList, itemsToTake, timer=timer, autoShow=autoShow, customName=customName)

    def stopLooting(self):
        Lootable.stopLooting(self)
        if self.type != PiratesGlobals.ITEM_SAC:
            self.openAnim.setPlayRate(-1.0)
            self.openAnim.play()

    def setEmpty(self, empty):
        if self.showLerp:
            self.showLerp.finish()
        if empty:
            self.showLerp = Sequence(Func(self.setTransparency, 1), LerpColorScaleInterval(self, 0.5, Vec4(1, 1, 1, 0)))
            self.showLerp.start()
            if self.effect:
                self.effect.stopLoop()
                self.effect = None
        else:
            self.showLerp = Sequence(LerpColorScaleInterval(self, 0.5, Vec4(1, 1, 1, 1)), Func(self.clearTransparency))
            self.showLerp.start()
        return

    def getTypeName(self):
        return self.typeName

    def doneTaking(self):
        Lootable.doneTaking(self)
        self.requestExit()
        localAvatar.motionFSM.on()
        self.cr.interactionMgr.start()