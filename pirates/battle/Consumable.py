import Weapon
import WeaponGlobals
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import ItemGlobals
__modelTypes = [
 'models/handheld/bottle_high', 'models/handheld/pir_m_hnd_foo_porktonic']

def getImage(itemId):
    return None


def getModel(id):
    if True:
        model = loader.loadModel('models/handheld/bottle_high')
    else:
        modelData = __modelTypes.get(id)
        model = loader.loadModel(modelData[0])
        model.setColor(modelData[1])
        model.setScale(modelData[2])
    return model


hitSfxs = None
repairSfxs = None
missSfxs = None
eatSfxs = None

def getDrinkSfx():
    global hitSfxs
    if not hitSfxs:
        hitSfxs = (
         loadSfx(SoundGlobals.SFX_CONSUMABLE_DRINK),)
    return hitSfxs


def getShipRepairSfx():
    global repairSfxs
    if not repairSfxs:
        repairSfxs = (
         loadSfx(SoundGlobals.SFX_CONSUMABLE_SHIP_REPAIR),)
    return repairSfxs


def getMissSfx():
    global missSfxs
    if not missSfxs:
        missSfxs = (
         loadSfx(SoundGlobals.SFX_CONSUMABLE_MISS), loadSfx(SoundGlobals.SFX_CONSUMABLE_MISS_ALT))
    return missSfxs


def getEatSfx():
    global eatSfxs
    if not eatSfxs:
        eatSfxs = loadSfx(SoundGlobals.SFX_CONSUMABLE_EAT_MEAT)
    return eatSfxs


class Consumable(Weapon.Weapon):
    notify = DirectNotifyGlobal.directNotify.newCategory('Consumable')

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'consumable')
        if self.itemId:
            self.modelId = ItemGlobals.getModel(itemId)
        return None

    def updateItemId(self, itemId):
        if self.itemId == itemId:
            return
        self.itemId = itemId
        self.modelId = ItemGlobals.getModel(itemId)
        if hasattr(self, 'prop'):
            self.prop.removeNode()
            self.loadModel()

    def loadModel(self):
        self.prop = getModel(self.itemId)
        if self.itemId != InventoryType.PorkChunk:
            pass
        else:
            self.prop.setHpr(0, 0, 0)
            self.prop.setPos(0, 0, 0)
        self.prop.reparentTo(self)
        self.prop.flattenLight()
        coll = self.prop.find('**/Collision*')
        if not coll.isEmpty():
            coll.stash()
        else:
            self.notify.warning('Collision not found!')