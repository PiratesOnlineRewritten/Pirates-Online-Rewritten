from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.ai import HolidayGlobals
from pirates.battle import WeaponGlobals
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import ItemType
from pirates.holiday import CatalogHoliday
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import GuiPanel, RedeemCodeGUI
from pirates.piratesgui import GuiButton, DialogButton
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiButton
from pirates.pirate import DynamicHuman
from pirates.pirate import Human
from pirates.pirate import HumanDNA
from pirates.piratesgui.TabBar import LeftTab, TabBar
from direct.interval.IntervalGlobal import *
from pirates.makeapirate import ClothingGlobals
from pirates.makeapirate import TattooGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
from pirates.piratesgui import PDialog
from direct.task import Task
import random
from pirates.piratesbase import Freebooter
from pirates.piratesgui.InventoryItemGui import InventoryItemGui
from pirates.inventory.InventoryGlobals import *
from pirates.uberdog.TradableInventoryBase import InvItem
from pirates.inventory import ItemGlobals, DropGlobals
from pirates.inventory import ItemConstants
from pirates.inventory import InventoryUIStoreContainer
from pirates.pirate import AvatarTypes
from math import sin
from math import cos
from math import pi
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import InventoryGlobals

class SimpleItem():

    def __init__(self, uid):
        self.uid = uid
        self.itemName = PLocalizer.getItemName(uid)
        self.shortDesc = PLocalizer.getItemName(uid)
        self.longDesc = PLocalizer.getItemFlavorText(uid)
        self.text = None
        self.modelId = None
        self.texId = None
        self.colorId = 0
        self.holidayId = None
        self.icon = None
        self.iconScale = 1.0
        self.iconHpr = (0, 0, 0)
        if self.checkStackable():
            self.quantity = EconomyGlobals.getItemQuantity(self.uid)
        else:
            self.quantity = 1
        return

    def checkStackable(self):
        return InventoryId.isStackable(self.uid)

    def configureForPirate(self, pirate):
        pass

    def canBeUsed(self, pirate):
        return True

    def apply(self, pirate):
        pass

    def unapply(self, pirate, sourceStyle):
        pass

    def purchase(self, npc):
        pass

    def getFlavorAnim(self):
        return ''

    def getCameraPos(self, pirate):
        return (0, 0, 0)

    def getCameraLookAtPos(self, pirate):
        return (0, 0, 0)


class SimpleLootItem(SimpleItem):
    Icons = None

    def __init__(self, uid):
        self.itemClass = ItemGlobals.getClass(uid)
        self.itemType = ItemGlobals.getType(uid)
        self.cost = ItemGlobals.getGoldCost(uid)
        SimpleItem.__init__(self, uid)
        self.holidayId = ItemGlobals.getHoliday(uid)
        if self.Icons:
            self.icon = self.Icons.find('**/%s' % ItemGlobals.getIcon(uid))

    def checkStackable(self):
        return InventoryGlobals.isStackableType(self.itemClass)

    def configureForPirate(self, pirate):
        gender = pirate.style.getGender()
        getModelId = choice(gender == 'm', ItemGlobals.getMaleModelId, ItemGlobals.getFemaleModelId)
        getTextureId = choice(gender == 'm', ItemGlobals.getMaleTextureId, ItemGlobals.getFemaleTextureId)
        self.modelId = getModelId(self.uid)
        self.texId = getTextureId(self.uid)

    def getQuantityInInventory(self):
        inventory = base.localAvatar.getInventory()
        quantity = inventory.getItemQuantity(self.itemClass, self.uid)
        return quantity


class SimpleClothingItem(SimpleLootItem):
    Icons = loader.loadModel('models/gui/gui_icons_clothing')

    def __init__(self, uid):
        SimpleLootItem.__init__(self, uid)
        self.clothingNumber = self.itemType
        self.clothingString = ClothingGlobals.CLOTHING_STRING[self.itemType]

    def canBeUsed(self, pirate):
        self.configureForPirate(pirate)
        return self.modelId >= 0 and self.texId >= 0

    def apply(self, pirate):
        if not self.canBeUsed(pirate):
            return
        self.configureForPirate(pirate)
        typeString = ClothingGlobals.CLOTHING_STRING[self.itemType]
        pirate.setClothesByType(typeString, self.modelId, self.texId, self.colorId)
        pirate.model.handleClothesHiding()
        pirate.model.handleHeadHiding()

    def unapply(self, pirate, sourceStyle):
        if not self.canBeUsed(pirate):
            return
        pirate.style.clothes.shirt = sourceStyle.clothes.shirt
        pirate.style.clothes.shirtTexture = sourceStyle.clothes.shirtTexture
        pirate.style.clothes.shirtColor = sourceStyle.clothes.shirtColor
        pirate.style.clothes.vest = sourceStyle.clothes.vest
        pirate.style.clothes.vestTexture = sourceStyle.clothes.vestTexture
        pirate.style.clothes.vestColor = sourceStyle.clothes.vestColor
        pirate.style.clothes.pant = sourceStyle.clothes.pant
        pirate.style.clothes.pantTexture = sourceStyle.clothes.pantTexture
        pirate.style.clothes.pantColor = sourceStyle.clothes.pantColor
        pirate.style.clothes.coat = sourceStyle.clothes.coat
        pirate.style.clothes.coatTexture = sourceStyle.clothes.coatTexture
        pirate.style.clothes.coatColor = sourceStyle.clothes.coatColor
        pirate.style.clothes.shoe = sourceStyle.clothes.shoe
        pirate.style.clothes.shoeTexture = sourceStyle.clothes.shoeTexture
        pirate.style.clothes.shoeColor = sourceStyle.clothes.shoeColor
        pirate.style.clothes.belt = sourceStyle.clothes.belt
        pirate.style.clothes.beltTexture = sourceStyle.clothes.beltTexture
        pirate.style.clothes.sashColor = sourceStyle.clothes.sashColor
        pirate.style.clothes.hat = sourceStyle.clothes.hat
        pirate.style.clothes.hatTexture = sourceStyle.clothes.hatTexture
        pirate.style.clothes.hatColor = sourceStyle.clothes.hatColor
        pirate.model.handleClothesHiding()
        pirate.model.handleHeadHiding()

    def purchase(self, npc):
        location = 0
        purchaseArgs = [self.uid, self.colorId, self.clothingNumber, location]
        npc.sendRequestAccessories([purchaseArgs], [])

    def getFlavorAnim(self):
        typeString = self.clothingString
        if typeString == 'SHIRT' or typeString == 'COAT':
            if random.randint(0, 1) == 0:
                return 'map_look_arm_left'
            else:
                return 'map_look_arm_right'
        if typeString == 'PANT' or typeString == 'BELT':
            return 'map_look_pant_right'
        if typeString == 'SHOE':
            return 'map_look_boot_left'
        return ''

    def getCameraPos(self, pirate):
        return (
         0, 10, pirate.headNode.getZ(pirate))

    def getCameraLookAtPos(self, pirate):
        return (
         pirate.headNode.getX(pirate), pirate.headNode.getY(pirate), pirate.headNode.getZ(pirate) * 0.9)


class SimpleJewelryItem(SimpleLootItem):
    Icons = loader.loadModel('models/gui/gui_icons_jewelry')

    def __init__(self, uid):
        SimpleLootItem.__init__(self, uid)
        self.jewelryType = SimpleJewelryItem.jewelryTypeFromItemType(self.itemType)

    @classmethod
    def jewelryTypeFromItemType(cls, itemType):
        if itemType == ItemGlobals.BROW:
            return JewelryGlobals.LBROW
        elif itemType == ItemGlobals.EAR:
            return JewelryGlobals.LEAR
        elif itemType == ItemGlobals.NOSE:
            return JewelryGlobals.NOSE
        elif itemType == ItemGlobals.MOUTH:
            return JewelryGlobals.MOUTH
        elif itemType == ItemGlobals.HAND:
            return JewelryGlobals.LHAND

    @classmethod
    def itemTypeFromJewelryType(cls, jewelryType):
        if jewelryType in (JewelryGlobals.LBROW, JewelryGlobals.RBROW):
            return ItemGlobals.BROW
        elif jewelryType in (JewelryGlobals.LEAR, JewelryGlobals.REAR):
            return ItemGlobals.EAR
        elif jewelryType == JewelryGlobals.NOSE:
            return ItemGlobals.NOSE
        elif jewelryType == JewelryGlobals.MOUTH:
            return ItemGlobals.MOUTH
        elif jewelryType in (JewelryGlobals.LHAND, JewelryGlobals.RHAND):
            return ItemGlobals.HAND

    def apply(self, pirate):
        gender = localAvatar.style.getGender()
        if gender == 'm':
            idx = ItemGlobals.getMaleModelId(self.uid)
        else:
            idx = ItemGlobals.getFemaleModelId(self.uid)
        primaryColor = ItemGlobals.getPrimaryColor(self.uid)
        secondaryColor = ItemGlobals.getSecondaryColor(self.uid)
        if self.jewelryType == JewelryGlobals.LBROW:
            pirate.setJewelryZone3(idx, primaryColor, secondaryColor)
        elif self.jewelryType == JewelryGlobals.RBROW:
            pirate.setJewelryZone4(idx, primaryColor, secondaryColor)
        elif self.jewelryType == JewelryGlobals.LEAR:
            pirate.setJewelryZone1(idx, primaryColor, secondaryColor)
        elif self.jewelryType == JewelryGlobals.REAR:
            pirate.setJewelryZone2(idx, primaryColor, secondaryColor)
        elif self.jewelryType == JewelryGlobals.NOSE:
            pirate.setJewelryZone5(idx, primaryColor, secondaryColor)
        elif self.jewelryType == JewelryGlobals.MOUTH:
            pirate.setJewelryZone6(idx, primaryColor, secondaryColor)
        elif self.jewelryType == JewelryGlobals.LHAND:
            pirate.setJewelryZone7(idx, primaryColor, secondaryColor)
        elif self.jewelryType == JewelryGlobals.RHAND:
            pirate.setJewelryZone8(idx, primaryColor, secondaryColor)
        pirate.model.handleJewelryHiding()

    def unapply(self, pirate, sourceStyle):
        jewelryZone4 = list(localAvatar.style.getJewelryZone4())
        jewelryZone3 = list(localAvatar.style.getJewelryZone3())
        jewelryZone1 = list(localAvatar.style.getJewelryZone1())
        jewelryZone2 = list(localAvatar.style.getJewelryZone2())
        jewelryZone5 = list(localAvatar.style.getJewelryZone5())
        jewelryZone6 = list(localAvatar.style.getJewelryZone6())
        jewelryZone7 = list(localAvatar.style.getJewelryZone7())
        jewelryZone8 = list(localAvatar.style.getJewelryZone8())
        if not hasattr(pirate, 'style'):
            return
        pirate.style.setJewelryZone1(jewelryZone1[0], jewelryZone1[1], jewelryZone1[2])
        pirate.style.setJewelryZone2(jewelryZone2[0], jewelryZone2[1], jewelryZone2[2])
        pirate.style.setJewelryZone3(jewelryZone3[0], jewelryZone3[1], jewelryZone3[2])
        pirate.style.setJewelryZone4(jewelryZone4[0], jewelryZone4[1], jewelryZone4[2])
        pirate.style.setJewelryZone5(jewelryZone5[0], jewelryZone5[1], jewelryZone5[2])
        pirate.style.setJewelryZone6(jewelryZone6[0], jewelryZone6[1], jewelryZone6[2])
        pirate.style.setJewelryZone7(jewelryZone7[0], jewelryZone7[1], jewelryZone7[2])
        pirate.style.setJewelryZone8(jewelryZone8[0], jewelryZone8[1], jewelryZone8[2])
        pirate.model.handleJewelryHiding()

    def purchase(self, npc):
        location = 0
        purchaseArgs = [self.uid, location]
        npc.sendRequestJewelry([purchaseArgs], [])

    def getCameraPos(self, pirate):
        pz = pirate.headNode.getZ(pirate)
        if self.jewelryType == JewelryGlobals.LBROW:
            return (-1, 2, pz + 0.5)
        elif self.jewelryType == JewelryGlobals.RBROW:
            return (1, 2, pz + 0.5)
        elif self.jewelryType == JewelryGlobals.LEAR:
            return (-2, 2, pz + 0.25)
        elif self.jewelryType == JewelryGlobals.REAR:
            return (2, 2, pz + 0.25)
        elif self.jewelryType == JewelryGlobals.NOSE:
            return (0, 2, pz + 0.25)
        elif self.jewelryType == JewelryGlobals.MOUTH:
            return (0, 2, pz)
        elif self.jewelryType == JewelryGlobals.LHAND:
            return (-2, 2.5, pirate.leftHandNode.getZ(pirate))
        elif self.jewelryType == JewelryGlobals.RHAND:
            return (2, 2.5, pirate.rightHandNode.getZ(pirate))
        return (0, 0, 0)

    def getCameraLookAtPos(self, pirate):
        px = pirate.headNode.getX(pirate)
        py = pirate.headNode.getY(pirate)
        pz = pirate.headNode.getZ(pirate)
        if self.jewelryType == JewelryGlobals.LBROW:
            return (px, py, pz * 1.1)
        elif self.jewelryType == JewelryGlobals.RBROW:
            return (px, py, pz * 1.1)
        elif self.jewelryType == JewelryGlobals.LEAR:
            return (px, py, pz * 1.1)
        elif self.jewelryType == JewelryGlobals.REAR:
            return (px, py, pz * 1.1)
        elif self.jewelryType == JewelryGlobals.NOSE:
            return (px, py, pz * 1.1)
        elif self.jewelryType == JewelryGlobals.MOUTH:
            return (px, py, pz * 1.075)
        elif self.jewelryType == JewelryGlobals.LHAND:
            return (pirate.leftHandNode.getX(pirate), pirate.leftHandNode.getY(pirate), pirate.leftHandNode.getZ(pirate) * 1.2)
        elif self.jewelryType == JewelryGlobals.RHAND:
            return (pirate.rightHandNode.getX(pirate), pirate.rightHandNode.getY(pirate), pirate.rightHandNode.getZ(pirate) * 1.2)
        return (0, 0, 0)


class SimpleTattooItem(SimpleLootItem):
    Icons = loader.loadModel('models/textureCards/tattooIcons')

    def __init__(self, uid):
        SimpleLootItem.__init__(self, uid)
        self.zone = SimpleTattooItem.tattooTypeFromItemType(self.itemType)
        self.icon = ItemGlobals.getItemTattooImage(uid)[0]
        self.iconScale = 0.4

    @classmethod
    def tattooTypeFromItemType(cls, itemType):
        if itemType == ItemGlobals.CHEST:
            return TattooGlobals.ZONE1
        elif itemType == ItemGlobals.ARM:
            return TattooGlobals.ZONE2
        elif itemType == ItemGlobals.FACE:
            return TattooGlobals.ZONE4

    @classmethod
    def itemTypeFromTattooType(cls, tattooType):
        if tattooType == TattooGlobals.ZONE1:
            return ItemGlobals.CHEST
        elif tattooType in (TattooGlobals.ZONE2, TattooGlobals.ZONE3):
            return ItemGlobals.ARM
        elif tattooType == TattooGlobals.ZONE4:
            return ItemGlobals.FACE

    def apply(self, pirate):
        pirate.style.setClothesShirt(0)
        pirate.style.setClothesCoat(0)
        pirate.style.setClothesVest(0)
        pirate.model.handleClothesHiding()
        gender = localAvatar.style.getGender()
        if gender == 'm':
            tattooId = ItemGlobals.getMaleModelId(self.uid)
            if self.zone == TattooGlobals.ZONE3:
                orientation = ItemGlobals.getMaleOrientation2(self.uid)
            else:
                orientation = ItemGlobals.getMaleOrientation(self.uid)
        else:
            tattooId = ItemGlobals.getFemaleModelId(self.uid)
            if self.zone == TattooGlobals.ZONE3:
                orientation = ItemGlobals.getFemaleOrientation2(self.uid)
            else:
                orientation = ItemGlobals.getFemaleOrientation(self.uid)
            offsetx, offsety, scale, rotate = ItemGlobals.getOrientation(orientation)
            if not hasattr(pirate, 'model'):
                return
        pirate.model.tattoos[self.zone][TattooGlobals.TYPE] = tattooId
        S = Vec2(1 / float(scale), 1 / float(scale))
        Iv = Vec2(offsetx, offsety)
        Vm = Vec2(sin(rotate * pi / 180.0), cos(rotate * pi / 180.0))
        Vms = Vec2(Vm[0] * S[0], Vm[1] * S[1])
        Vn = Vec2(Vm[1], -Vm[0])
        Vns = Vec2(Vn[0] * S[0], Vn[1] * S[1])
        F = Vec2(-Vns.dot(Iv) + 0.5, -Vms.dot(Iv) + 0.5)
        pirate.model.tattoos[self.zone][TattooGlobals.OFFSETX] = F[0]
        pirate.model.tattoos[self.zone][TattooGlobals.OFFSETY] = F[1]
        pirate.model.tattoos[self.zone][TattooGlobals.SCALE] = S[0]
        pirate.model.tattoos[self.zone][TattooGlobals.ROTATE] = rotate
        pirate.model.updateTattoo(self.zone)

    def unapply(self, pirate, sourceStyle):
        pirate.style.clothes.shirt = localAvatar.style.clothes.shirt
        pirate.style.clothes.shirtTexture = localAvatar.style.clothes.shirtTexture
        pirate.style.clothes.shirtColor = localAvatar.style.clothes.shirtColor
        pirate.style.clothes.vest = localAvatar.style.clothes.vest
        pirate.style.clothes.vestTexture = localAvatar.style.clothes.vestTexture
        pirate.style.clothes.vestColor = localAvatar.style.clothes.vestColor
        pirate.style.clothes.coat = localAvatar.style.clothes.coat
        pirate.style.clothes.coatTexture = localAvatar.style.clothes.coatTexture
        pirate.style.clothes.coatColor = localAvatar.style.clothes.coatColor
        pirate.model.handleClothesHiding()
        if self.zone == TattooGlobals.ZONE1:
            pirate.model.tattoos[self.zone] = list(localAvatar.style.getTattooChest())
        if self.zone == TattooGlobals.ZONE2:
            pirate.model.tattoos[self.zone] = list(localAvatar.style.getTattooZone2())
        if self.zone == TattooGlobals.ZONE3:
            pirate.model.tattoos[self.zone] = list(localAvatar.style.getTattooZone3())
        if self.zone == TattooGlobals.ZONE4:
            pirate.model.tattoos[self.zone] = list(localAvatar.style.getTattooZone4())
        pirate.model.updateTattoo(self.zone)

    def purchase(self, npc):
        location = 0
        purchaseArgs = [self.uid, location]
        npc.sendRequestTattoo([purchaseArgs], [])

    def getFlavorAnim(self):
        if self.zone == TattooGlobals.ZONE2:
            return 'map_look_arm_left'
        elif self.zone == TattooGlobals.ZONE3:
            return 'map_look_arm_right'
        return ''

    def getCameraPos(self, pirate):
        pz = pirate.headNode.getZ(pirate)
        if self.zone == TattooGlobals.ZONE1:
            return (0, 4, pz)
        elif self.zone == TattooGlobals.ZONE2:
            return (-5, 2, pz)
        elif self.zone == TattooGlobals.ZONE3:
            return (5, 2, pz)
        elif self.zone == TattooGlobals.ZONE4:
            return (0, 3, pz * 1.1)
        return (0, 0, 0)

    def getCameraLookAtPos(self, pirate):
        px = pirate.headNode.getX(pirate)
        py = pirate.headNode.getY(pirate)
        pz = pirate.headNode.getZ(pirate)
        if self.zone == TattooGlobals.ZONE1:
            return (px, py, pz)
        elif self.zone == TattooGlobals.ZONE2:
            return (px, py, pz * 0.9)
        elif self.zone == TattooGlobals.ZONE3:
            return (px, py, pz * 0.9)
        elif self.zone == TattooGlobals.ZONE4:
            return (px, py, pz * 1.1)
        return (0, 0, 0)


class SimpleWeaponItem(SimpleLootItem):
    Icons = loader.loadModel('models/gui/gui_icons_weapon')

    def __init__(self, uid):
        SimpleLootItem.__init__(self, uid)
        self.quantity = 1

    def purchase(self, npc):
        location = 0
        purchaseArgs = [self.uid, location]
        npc.sendRequestWeapon([purchaseArgs], [])


class SimpleConsumableItem(SimpleLootItem):
    Icons = loader.loadModel('models/textureCards/skillIcons')

    def __init__(self, uid):
        SimpleLootItem.__init__(self, uid)
        self.quantity = 1

    def purchase(self, npc):
        purchaseArgs = [
         self.uid, self.quantity]
        messenger.send('makeSale', [[purchaseArgs], []])

    def getQuantityInInventory(self):
        inventory = base.localAvatar.getInventory()
        quantity = inventory.getItemQuantity(self.itemClass, self.uid)
        return quantity


class SimpleEconomyItem(SimpleItem):

    def __init__(self, uid):
        SimpleItem.__init__(self, uid)
        self.itemClass = EconomyGlobals.getItemCategory(uid)
        self.itemType = EconomyGlobals.getItemType(uid)
        self.cost = EconomyGlobals.getItemCost(uid)
        if not self.cost:
            self.cost = ItemGlobals.getGoldCost(uid)

    def makeButton(self, parent, pos, cellSizeX, cellSizeZ):
        if InventoryId.isStackable(self.uid):
            data = [
             self.uid, 1]
        else:
            data = [
             InventoryId.getCategory(self.uid), self.uid]
        simpleItemGui = SimpleItemGUI([self.uid, 1], parent=parent, pos=pos)
        self.itemName = simpleItemGui.nameTag['text']
        self.shortDesc = self.itemName
        self.longDesc = self.itemName
        simpleItemGui.destroy()
        geomParams = InventoryItemGui.getGeomParams(self.uid)
        button = DirectButton(parent=parent, relief=None, rolloverSound=None, text='', text_scale=0.05, textMayChange=1, geom=geomParams['geom'], geom_pos=(0,
                                                                                                                                                            0,
                                                                                                                                                            0), geom_scale=geomParams['geom_scale'], pos=pos, extraArgs=[self])
        return button

    def purchase(self, npc):
        purchaseArgs = [
         self.uid, self.quantity]
        messenger.send('makeSale', [[purchaseArgs], []])

    def getCameraPos(self, pirate):
        pz = pirate.headNode.getZ(pirate)
        return (
         0, 0, pz)

    def getCameraLookAtPos(self, pirate):
        px = pirate.headNode.getX(pirate)
        py = pirate.headNode.getY(pirate)
        pz = pirate.headNode.getZ(pirate)
        return (
         px, py, pz)

    def getQuantityInInventory(self):
        inventory = base.localAvatar.getInventory()
        quantity = inventory.getStackQuantity(self.uid)
        return quantity


class SimpleAmmoItem(SimpleEconomyItem):
    Icons = loader.loadModel('models/textureCards/skillIcons')

    def __init__(self, uid):
        SimpleEconomyItem.__init__(self, uid)
        skillId = WeaponGlobals.getSkillIdForAmmoSkillId(uid)
        if skillId:
            asset = WeaponGlobals.getSkillIcon(skillId)
            if asset:
                self.icon = self.Icons.find('**/%s' % asset)
                self.iconScale = 1.1
                self.iconHpr = (0, 0, 45)

    def getQuantityInInventory(self):
        inventory = base.localAvatar.getInventory()
        quantity = inventory.getStackQuantity(self.uid)
        return quantity


class SimpleFishingLureItem(SimpleEconomyItem):
    Icons = loader.loadModel('models/textureCards/fishing_icons')
    FishingItemTable = {InventoryType.RegularLure: 'pir_t_gui_fsh_lureReg',InventoryType.LegendaryLure: 'pir_t_gui_fsh_lureLegend'}

    def __init__(self, uid):
        SimpleEconomyItem.__init__(self, uid)
        iconName = self.FishingItemTable.get(uid)
        asset = None
        if iconName:
            asset = self.Icons.find('**/%s' % iconName)
        if asset:
            self.icon = asset
            self.iconScale = 1.1
            self.iconHpr = (0, 0, 45)
        return

    def getQuantityInInventory(self):
        inventory = base.localAvatar.getInventory()
        quantity = inventory.getStackQuantity(self.uid)
        return quantity


class SimplePouchItem(SimpleEconomyItem):
    Icons = loader.loadModel('models/gui/gui_icons_weapon')

    def __init__(self, uid):
        SimpleEconomyItem.__init__(self, uid)
        self.icon = self.Icons.find('**/%s' % EconomyGlobals.getItemIcons(uid))
        if uid in range(InventoryType.begin_PistolPouches, InventoryType.end_PistolPouches):
            self.shortDesc = PLocalizer.makeHeadingString(PLocalizer.InventoryItemClassNames.get(ItemType.PISTOL), 1)
        elif uid in range(InventoryType.begin_DaggerPouches, InventoryType.end_DaggerPouches):
            self.shortDesc = PLocalizer.makeHeadingString(PLocalizer.InventoryItemClassNames.get(ItemType.DAGGER), 1)
        elif uid in range(InventoryType.begin_GrenadePouches, InventoryType.end_GrenadePouches):
            self.shortDesc = PLocalizer.makeHeadingString(PLocalizer.GrenadeShort, 1)
        elif uid in range(InventoryType.begin_CannonPouches, InventoryType.end_CannonPouches):
            self.shortDesc = PLocalizer.makeHeadingString(PLocalizer.ShipCannonShort, 1)
        else:
            self.shortDesc = PLocalizer.makeHeadingString(self.itemType, 1)
        self.itemName = self.shortDesc
        self.longDesc = self.shortDesc