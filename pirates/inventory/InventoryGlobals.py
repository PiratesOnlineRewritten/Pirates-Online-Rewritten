from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.makeapirate import ClothingGlobals
from pirates.makeapirate import JewelryGlobals
from pirates.makeapirate import TattooGlobals
from pirates.inventory import ItemConstants
from pirates.inventory import ItemGlobals
GOLD_CAP = 200000

class Locations():
    INVALID_LOCATION = -1
    NON_LOCATION = 0
    FIRST_LOCATION = 1
    TOTAL_NUM_LOCATIONS = 255
    RANGE_EQUIP_WEAPONS = (
     FIRST_LOCATION, 4)
    RANGE_EQUIP_ITEMS = (49, )
    RANGE_WEAPONS = (13, 42)
    RANGE_EQUIP_HAT_CLOTHES = (50, )
    RANGE_EQUIP_COAT_CLOTHES = (51, )
    RANGE_EQUIP_VEST_CLOTHES = (52, )
    RANGE_EQUIP_SHIRT_CLOTHES = (53, )
    RANGE_EQUIP_BELT_CLOTHES = (54, )
    RANGE_EQUIP_PANTS_CLOTHES = (55, )
    RANGE_EQUIP_BOOTS_CLOTHES = (56, )
    RANGE_EQUIP_CLOTHES = (50, 56)
    RANGE_CLOTHES = (60, 94)
    CLOTHING_TYPE_TO_RANGE = {ClothingGlobals.HAT: RANGE_EQUIP_HAT_CLOTHES,ClothingGlobals.SHIRT: RANGE_EQUIP_SHIRT_CLOTHES,ClothingGlobals.VEST: RANGE_EQUIP_VEST_CLOTHES,ClothingGlobals.COAT: RANGE_EQUIP_COAT_CLOTHES,ClothingGlobals.BELT: RANGE_EQUIP_BELT_CLOTHES,ClothingGlobals.PANT: RANGE_EQUIP_PANTS_CLOTHES,ClothingGlobals.SHOE: RANGE_EQUIP_BOOTS_CLOTHES}
    RANGE_EQUIP_L_EYEBROW_JEWELRY = (100, )
    RANGE_EQUIP_R_EYEBROW_JEWELRY = (101, )
    RANGE_EQUIP_R_EAR_JEWELRY = (102, )
    RANGE_EQUIP_L_EAR_JEWELRY = (103, )
    RANGE_EQUIP_NOSE_JEWELRY = (104, )
    RANGE_EQUIP_LIP_JEWELRY = (105, )
    RANGE_EQUIP_R_FINGER_JEWELRY = (106, )
    RANGE_EQUIP_L_FINGER_JEWELRY = (107, )
    RANGE_EQUIP_BROW_JEWELRY = (100, 101)
    RANGE_EQUIP_EAR_JEWELRY = (102, 103)
    RANGE_EQUIP_HAND_JEWELRY = (106, 107)
    RANGE_EQUIP_JEWELRY = (100, 107)
    JEWELRY_RANGE_TO_LOCATION = {RANGE_EQUIP_R_EYEBROW_JEWELRY: JewelryGlobals.RBROW,RANGE_EQUIP_L_EYEBROW_JEWELRY: JewelryGlobals.LBROW,RANGE_EQUIP_R_EAR_JEWELRY: JewelryGlobals.REAR,RANGE_EQUIP_L_EAR_JEWELRY: JewelryGlobals.LEAR,RANGE_EQUIP_NOSE_JEWELRY: JewelryGlobals.NOSE,RANGE_EQUIP_LIP_JEWELRY: JewelryGlobals.MOUTH,RANGE_EQUIP_R_FINGER_JEWELRY: JewelryGlobals.RHAND,RANGE_EQUIP_L_FINGER_JEWELRY: JewelryGlobals.LHAND}
    RANGE_EQUIP_L_ARM_TATTOO = (110, )
    RANGE_EQUIP_R_ARM_TATTOO = (111, )
    RANGE_EQUIP_CHEST_TATTOO = (112, )
    RANGE_EQUIP_FACE_TATTOO = (113, )
    RANGE_EQUIP_ARM_TATTOO = (110, 111)
    RANGE_EQUIP_TATTOO = (110, 113)
    TATTOO_RANGE_TO_LOCATION = {RANGE_EQUIP_L_ARM_TATTOO: TattooGlobals.ZONE2,RANGE_EQUIP_R_ARM_TATTOO: TattooGlobals.ZONE3,RANGE_EQUIP_CHEST_TATTOO: TattooGlobals.ZONE1,RANGE_EQUIP_FACE_TATTOO: TattooGlobals.ZONE4}
    RANGE_JEWELERY_AND_TATTOO = (116, 143)
    JEWLERY_TYPE_TO_RANGE = {ItemGlobals.BROW: RANGE_EQUIP_BROW_JEWELRY,ItemGlobals.EAR: RANGE_EQUIP_EAR_JEWELRY,ItemGlobals.NOSE: RANGE_EQUIP_NOSE_JEWELRY,ItemGlobals.MOUTH: RANGE_EQUIP_LIP_JEWELRY,ItemGlobals.HAND: RANGE_EQUIP_HAND_JEWELRY}
    TATTOO_TYPE_TO_RANGE = {ItemGlobals.FACE: RANGE_EQUIP_FACE_TATTOO,ItemGlobals.ARM: RANGE_EQUIP_ARM_TATTOO,ItemGlobals.CHEST: RANGE_EQUIP_CHEST_TATTOO}
    RANGE_CONSUMABLE = (150, 191)
    RANGE_MISC = (190, 224)
    RANGE_GOLD = (225, )
    RANGE_GOLD_WAGERED = (226, )
    RANGE_OVERFLOW = (227, 255)
    RANGE_EQUIP_SLOTS = RANGE_EQUIP_WEAPONS + RANGE_EQUIP_ITEMS + RANGE_EQUIP_CLOTHES + RANGE_EQUIP_JEWELRY + RANGE_EQUIP_TATTOO
    LOCATION_RANGES = {InventoryType.ItemTypeWeapon: ((RANGE_WEAPONS[0], RANGE_WEAPONS[1]),),InventoryType.ItemTypeCharm: ((RANGE_WEAPONS[0], RANGE_WEAPONS[1]),),InventoryType.ItemTypeClothing: ((RANGE_CLOTHES[0], RANGE_CLOTHES[1]),),InventoryType.ItemTypeTattoo: (RANGE_JEWELERY_AND_TATTOO,),InventoryType.ItemTypeJewelry: (RANGE_JEWELERY_AND_TATTOO,),InventoryType.ItemTypeMusic: (RANGE_MISC,),InventoryType.ItemTypeConsumable: (RANGE_CONSUMABLE,),InventoryType.ItemTypeMoney: (RANGE_GOLD,),InventoryType.ItemTypeMoneyWagered: (RANGE_GOLD_WAGERED,)}
    LOCATION_EQUIP_RANGES_CLOTHING = {ClothingGlobals.HAT: (RANGE_EQUIP_HAT_CLOTHES,),ClothingGlobals.SHIRT: (RANGE_EQUIP_SHIRT_CLOTHES,),ClothingGlobals.VEST: (RANGE_EQUIP_VEST_CLOTHES,),ClothingGlobals.COAT: (RANGE_EQUIP_COAT_CLOTHES,),ClothingGlobals.BELT: (RANGE_EQUIP_BELT_CLOTHES,),ClothingGlobals.PANT: (RANGE_EQUIP_PANTS_CLOTHES,),ClothingGlobals.SHOE: (RANGE_EQUIP_BOOTS_CLOTHES,)}
    LOCATION_EQUIP_RANGES_JEWELRY = {ItemConstants.BROW: (RANGE_EQUIP_R_EYEBROW_JEWELRY, RANGE_EQUIP_L_EYEBROW_JEWELRY),ItemConstants.EAR: (RANGE_EQUIP_L_EAR_JEWELRY, RANGE_EQUIP_R_EAR_JEWELRY),ItemConstants.NOSE: (RANGE_EQUIP_NOSE_JEWELRY,),ItemConstants.MOUTH: (RANGE_EQUIP_LIP_JEWELRY,),ItemConstants.HAND: (RANGE_EQUIP_L_FINGER_JEWELRY, RANGE_EQUIP_R_FINGER_JEWELRY)}
    LOCATION_EQUIP_RANGES_TATTOO = {ItemConstants.CHEST: (RANGE_EQUIP_CHEST_TATTOO,),ItemConstants.ARM: (RANGE_EQUIP_L_ARM_TATTOO, RANGE_EQUIP_R_ARM_TATTOO),ItemConstants.FACE: (RANGE_EQUIP_FACE_TATTOO,)}


def getEquipRanges(itemCat, itemType, expanded=False):
    if itemCat == InventoryType.ItemTypeClothing:
        if itemType:
            equipType = ItemGlobals.getType(itemType)
            ranges = Locations.LOCATION_EQUIP_RANGES_CLOTHING.get(equipType)
        else:
            ranges = (
             Locations.RANGE_EQUIP_CLOTHES,)
    else:
        if itemCat == InventoryType.ItemTypeJewelry:
            if itemType:
                equipType = ItemGlobals.getType(itemType)
                ranges = Locations.LOCATION_EQUIP_RANGES_JEWELRY.get(equipType)
            else:
                ranges = (
                 Locations.RANGE_EQUIP_JEWELRY,)
        elif itemCat == InventoryType.ItemTypeTattoo:
            if itemType:
                equipType = ItemGlobals.getType(itemType)
                ranges = Locations.LOCATION_EQUIP_RANGES_TATTOO.get(equipType)
            else:
                ranges = (
                 Locations.RANGE_EQUIP_TATTOO,)
        elif itemCat == InventoryType.ItemTypeWeapon:
            ranges = (Locations.RANGE_EQUIP_WEAPONS,)
        elif itemCat == InventoryType.ItemTypeCharm:
            ranges = (
             Locations.RANGE_EQUIP_ITEMS,)
        else:
            return None
        if expanded:
            ranges = expandRanges(ranges)
    return ranges


def getClothingTypeBySlot(slot):
    for type in Locations.LOCATION_EQUIP_RANGES_CLOTHING:
        typeRanges = Locations.LOCATION_EQUIP_RANGES_CLOTHING[type]
        for typeRange in typeRanges:
            rangeStart = typeRange[0]
            if len(typeRange) == 1:
                rangeEnd = typeRange[0]
            else:
                rangeEnd = typeRange[1]
            if slot in range(rangeStart, rangeEnd + 1):
                return type

    return None


def getJewelryTypeBySlot(slot):
    for type in Locations.LOCATION_EQUIP_RANGES_JEWELRY:
        typeRanges = Locations.LOCATION_EQUIP_RANGES_JEWELRY[type]
        for typeRange in typeRanges:
            rangeStart = typeRange[0]
            if len(typeRange) == 1:
                rangeEnd = typeRange[0]
            else:
                rangeEnd = typeRange[1]
            if slot in range(rangeStart, rangeEnd + 1):
                return type

    return None


def getJewelryLocationBySlot(slot):
    for locationRange in Locations.JEWELRY_RANGE_TO_LOCATION:
        rangeStart = locationRange[0]
        if len(locationRange) == 1:
            rangeEnd = locationRange[0]
        else:
            rangeEnd = locationRange[1]
        if slot in range(rangeStart, rangeEnd + 1):
            return Locations.JEWELRY_RANGE_TO_LOCATION[locationRange]

    return None


def getTattooTypeBySlot(slot):
    for type in Locations.LOCATION_EQUIP_RANGES_TATTOO:
        typeRanges = Locations.LOCATION_EQUIP_RANGES_TATTOO[type]
        for typeRange in typeRanges:
            rangeStart = typeRange[0]
            if len(typeRange) == 1:
                rangeEnd = typeRange[0]
            else:
                rangeEnd = typeRange[1]
            if slot in range(rangeStart, rangeEnd + 1):
                return type

    return None


def getTattooLocationBySlot(slot):
    for locationRange in Locations.TATTOO_RANGE_TO_LOCATION:
        rangeStart = locationRange[0]
        if len(locationRange) == 1:
            rangeEnd = locationRange[0]
        else:
            rangeEnd = locationRange[1]
        if slot in range(rangeStart, rangeEnd + 1):
            return Locations.TATTOO_RANGE_TO_LOCATION[locationRange]

    return None


def isStackableType(category):
    return category in [InventoryType.ItemTypeConsumable, InventoryType.ItemTypeMoney, InventoryType.ItemTypeMoneyWagered]


def itemStoresLocation(category):
    return category > InventoryType.begin_Category and category < InventoryType.end_Category and category not in [InventoryType.ItemTypeMoney, InventoryType.ItemTypeMoneyWagered]


def getLocationChangeMsg(invId):
    return 'inventoryLocation-%s' % invId


def getOverflowChangeMsg(invId):
    return 'inventoryOverflow-%s' % invId


def getAnyChangeMsg(invId):
    return 'inventoryChanged-%s' % invId


def getCategoryChangeMsg(invId, category):
    return 'inventoryCategory-%s-%s' % (invId, category)


def getCategoryQuantChangeMsg(invId, category):
    return 'inventoryQuantity-%s-%s' % (invId, category)


def getLocationRanges(category, type, includeEquip=True, expanded=False):
    ranges = Locations.LOCATION_RANGES.get(category, ())
    if expanded:
        ranges = expandRanges(ranges)
    if includeEquip:
        equipRanges = getEquipRanges(category, type, expanded)
        if equipRanges:
            ranges = equipRanges + ranges
    return ranges


def expandRanges(ranges):
    expanded = []
    for currRange in ranges:
        min = currRange[0]
        if len(currRange) > 1:
            max = currRange[1]
        else:
            max = min
        expanded.extend(range(min, max + 1))

    return expanded


def inOverflow(location):
    return location >= Locations.RANGE_OVERFLOW[0] and location <= Locations.RANGE_OVERFLOW[1]


def getItemLimit(category, type=None):
    if category == InventoryType.ItemTypeMoney or category == InventoryType.ItemTypeMoneyWagered:
        return GOLD_CAP
    elif itemStoresLocation(category) and type:
        return ItemGlobals.getStackLimit(type)
    else:
        return None
    return None


AmmoInGUI = [
 InventoryType.AmmoVenomShot, InventoryType.AmmoBaneShot, InventoryType.AmmoHexEaterShot, InventoryType.AmmoSilverShot, InventoryType.AmmoSteelShot, InventoryType.AmmoChainShot, InventoryType.AmmoGrapeShot, InventoryType.AmmoFirebrand, InventoryType.AmmoThunderbolt, InventoryType.AmmoExplosive, InventoryType.AmmoFury, InventoryType.AmmoGrenadeShockBomb, InventoryType.AmmoGrenadeFlame, InventoryType.AmmoGrenadeSmoke, InventoryType.AmmoGrenadeSiege, InventoryType.AmmoAsp, InventoryType.AmmoAdder, InventoryType.AmmoSidewinder, InventoryType.AmmoViperNest, InventoryType.RegularLure, InventoryType.LegendaryLure]