import string
import os
import datetime
import time
import copy
from otp.otpbase import OTPGlobals
from pirates.uberdog.UberDogGlobals import *
from pirates.economy.EconomyGlobals import *
from pirates.battle.EnemySkills import *
from pirates.minigame import PotionGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.world import OceanZone
from pirates.world.LocationConstants import LocationIds
from pirates.quest.QuestConstants import NPCIds, PropIds, QuestItems
from otp.otpbase import OTPLocalizer as OL
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfxString
from pirates.ai import HolidayGlobals
from pirates.inventory import ItemGlobals
from pirates.piratesbase import EmoteGlobals
from pirates.audio import SoundGlobals
OL.SpeedChatStaticText = OL.SpeedChatStaticTextPirates.copy()
for key in OL.SpeedChatStaticTextCommon.iterkeys():
    OL.SpeedChatStaticText[key] = OL.SpeedChatStaticTextCommon[key]

InterfaceFont = 'models/fonts/BardiT.bam'
InterfaceOutlineFont = 'models/fonts/BardiT_outline.bam'
PirateChippedFont = 'models/fonts/BriosoPro_chipped.bam'
PirateChippedOutlineFont = 'models/fonts/BriosoPro_chipped_outline.bam'
PirateBoldOutlineFont = 'models/fonts/BriosoPro_bold_outline.bam'
SignFont = PirateChippedOutlineFont
NoRambleshack = 'You cannot go outside yet. Rambleshack is still loading.'
NoPortRoyal = 'You cannot skip the tutorial yet. Port Royal is still loading.'
NoMainWorld = 'You cannot use ships yet. The main world is still loading.'
DialogOK = 'OK'
DialogYes = 'Yes'
DialogNo = 'No'
DialogCancel = 'Cancel'
PortNames = {
    'PortRoyalPort': 'Port Royal',
    'Bilgewater': 'Bilgewater',
    'Art Prototype': 'Art Prototype',
    'TheRock': 'The Rock',
    'Tortuga': 'Tortuga',
    'MadreDelFuego': 'Padres Del Fuego',
    'ArtPrototypePort': 'Bilgewater',
    'VegasPort': 'Vegas',
    'HiddenIslandPort': 'Hidden Island',
    'CutthroatPort': 'Cutthroat Isle',
    'TormentaPort': 'Isla Tormenta'
}
lCancel = 'Cancel'
lSubmit = 'Submit'
lConfirm = 'Confirm'
lClose = 'Close'
lOk = 'OK'
lNext = 'Next'
lBack = 'Back'
lQuit = 'Quit'
lYes = 'Yes'
lNo = 'No'
lExit = 'Exit'
Someone = 'Someone'
PirateShip = 'Pirate Ship'
MoneyName = 'Gold'
CheatCardName = 'Cards'
LevelUp = 'LEVEL UP!'
Level = 'Level'
Rank = 'Rank'
Lv = 'lv'
EXP = 'Rep.'
EXP_Nerf = 'basic access'
CrewBonus = 'crew bonus'
DoubleRepBonus = 'double rep bonus'
HolidayBonus = 'holiday bonus'
PotionBonus = 'potion rep bonus'
LevelRequirement = 'Requires level %s'
TrainingRequirement = 'Requires training'
SkillRequirement = 'Needs %s'
LandInfamyRequirement = 'Requires PvP Rank %s'
SeaInfamyRequirement = 'Requires Privateering Rank %s'
Unknown = 'Unknown'
NotYet = 'This skill is not yet available.'
InventoryCurrent = '%d/%d'
InventoryFull = 'Inventory Full (%d)'
InventoryOwned = 'Already Owned'
InventoryLowLevel = 'Higher Level Owned'
Sticky = 'Attuned'
Hull = 'Hull'
Sail = 'Sail'
Cannon = 'Cannons'
Broadside = 'Broadside'
Broadsides = 'Broadsides'
Armor = 'Armor'
Cargo = 'Cargo'
Timer = 'Timer'
Crew = 'Shipmates'
HP = 'HP'
SP = 'SP'
Knots = '%d Knots'
Speed = 'Speed'
Sails = 'Sails'
Plunder = 'Plunder'
Limits = 'Limits'
Hull = 'Hull'
Wear = 'Wear'
Skills = 'Skills'
Weapons = 'Weapons'
WeaponAbility = 'Weapon'
Treasure = 'Treasure'
ShipProfile = 'Ship Profile'
ExcessGoldLost = 'Are you sure you want to sell this? You can only carry 200,000 Gold, so the extra gold will be lost!'
NotEnoughMoneyWarning = 'Not enough ' + MoneyName + ' !'
EmptyPurchaseWarning = 'Nothing to purchase!'
CannotHoldGoldWarning = 'Cannot hold anymore ' + MoneyName + '!'
CannotHoldShipWarning = 'Cannot hold anymore Ships!'
NothingEquippedWarning = 'No item equipped!'
NoTrainingWarning = 'Requires %s training to use this weapon!'
LevelReqWarning = 'Must be at least Level %s in %s to use this weapon!'
WaitYourTurnWarning = 'Already playing a request!'
Apostrophe = "'s"
ShipRepair = 'Ship Repair'
SellShip = 'Sell Ship'
ShipOverhaul = 'Ship Overhaul'
RepairSails = 'Repair\nSails'
HitCombo = 'Hit Combo!'
TeamCombo = 'Team Attack!'
Damage = 'Total Damage!'
PassiveSkill = 'Passive Skill'
ComboSkill = 'Combo Skill'
CombatSkill = 'Combat Attack'
Consumable = 'Consumable'
ShipRepairSkill = 'Ship Repair Skill'
AmmoSkill = 'Ammo Skill'
AttackSkill = 'Combat Skill'
ShipSkill = 'Ship Maneuver'
ThrowSkill = 'Throwing Skill'
ManaName = 'Voodoo'
HexSkill = 'Hex - %d ' + ManaName
OrderSkill = 'Battle Order'
DealsDamage = 'Deals %d to %d damage!'
HealsDamageRange = 'Heals %d health!'
HealsDamage = 'Heals %d voodoo and %d health!'
DealsMpDamage = 'Removes %d to %d ' + ManaName + ' from the victim!'
OpenPortNames = {
    '1160614528.73sdnaik': 'Cuba',
    '1156207188.95dzlu': 'Tortuga',
    '1271348547.01akelts': "Raven's Cove",
    '1164135492.81dzlu': "Devil's Anvil"
}
Nametag_BountyHunter = 'Hunter'
Nametag_Warship = 'Warship'
ThreatLevel_1_text_a = 'They know this be a Pirate Ship! Time to start plundering!'
ThreatLevel_1_text_b = "Captain, they know we are Pirates! Plundering will make 'em real mad."
ThreatLevel_2_text_a = 'They think they can out gun us?! Open fire and plunder all you can!'
ThreatLevel_2_text_b = "They're on Alert, trying to protect their Treasure! Sink those ships and claim what's ours!"
ThreatLevel_3_text_a = "We're stuffed to the gills with treasure Captain! Those greedy bounty hunters will surely be after us."
ThreatLevel_3_text_b = "The navy's put a bounty on us. Hunters will be coming to collect. Let's give 'em what for!"
ThreatLevel_4_text_a = "Watch out Captain! The navy's laying in wait at the ports and we've got warships after us!"
ThreatLevel_5_Scenerio_DJ_text_a = "The navy hunters have given up captain! That's a good sign- I hope!"
ThreatLevel_6_Scenerio_DJ_text_b = 'Level 6!'
PortClosed_Cuba = 'The navy has closed Cuba!'
PortClosed_Tortuga = 'The navy has closed Tortuga!'
PortClosed_RavensCove = "The navy has closed Raven's Cove!"
PortClosed_DevilsAnvil = "The navy has closed Devil's Anvil!"
PortOpen_Cuba = ' but Cuba is open.'
PortOpen_Tortuga = ' but Tortuga is open.'
PortOpen_RavensCove = " but Raven's Cove is open."
PortOpen_DevilsAnvil = " but Devil's Anvil is open."
OpenPortMessage = 'Port open : %s'
PortSwitch = "They've closed %s, but %s is now unguarded!"
WrongIslandNoPort = 'You cannot port at this island while the Navy is hunting you!'
PortClosed_Initial = 'The Navy has closed down all the ports!'
NoPortWild = "We're sinking ducks if we anchor here!"
CantPortNavy_a = 'This port is occupied by the Navy! '
CantPortNavy_b = 'Too many Navy in this port'
ShipInboundSimple_a = 'Another Ship Inbound, Captain!'
ShipInboundSimple_b = 'Here comes an inbound ship.'
ShipInboundSimple_c = 'Arghh, here comes an inbound ship.'
ShipInboundHelp_a = 'More ships inbound! They must have sent out a distress.'
ShipInboundHelp_b = "Another Ship Inbound, Captain! Seems like they're call'n for help."
ShipInboundHunter_a = 'Oh good bounty hunters! More ships for us to sink.'
ShipInboundHunter_b = "Bounty hunter! Close'n in."
ShipInboundHunter_c = 'Bounty hunter!!'
ShipSunkMessage_a = 'Take what you can, give nothing back!'
ShipSunkMessage_b = 'Keep at it! Thar be loot aboard those ships!'
ShipSunkMessage_c = "We've sunk her, Captain!"
ShipSunkMessage_d = "To Davy Jones' locker with you all!"
ShipSunkMessage_e = 'Plunder Those Ships!'
ShipSunkMessage_f = 'Turn them into fish food!'
UpgradeTypeHull = 'Hulls'
UpgradeTypeRigging = 'Rigging'
UpgradeTypePattern = 'Sail Color'
UpgradeTypeLogo = 'Emblem'
UpgradeTypeExit = 'Exit'
UpgradePurchaseConfirm = 'Purchase Upgrade'
UpgradeShowMore = 'More...'
UpgradeShowNext = 'Next >'
UpgradeShowPrev = '< Prev'
UpgradePurchaseDowngrade = 'Downgrade'
UpgradePurchaseSidegrade = 'Purchase Conversion'
UpgradePurchaseUnlimitedOnly = 'Unlimited Only'
UpgradePurchaseWait = 'Please Wait'
UpgradePurchaseCurrent = 'Viewing Current'
UpgradePurchasePoor = "Can't Afford"
CurrentUpgrade = '(Current)'
YourCurrent = 'Your Ship'
UpgradeTitle = 'Upgrades'
UpgradeLineTitle = 'Upgrades'
DowngradeLineTitle = 'Downgrades'
ShipUpgradeAttributeArmor = 'Armor'
ShipUpgradeAttributeSpeed = 'Speed'
ShipUpgradeAttributeTurning = 'Turning'
ShipUpgradeAttributeCargo = 'Cargo'
ShipUpgradeComplete = 'Ship Modified!'
ShipUpgradeFailed = 'Ship Modification Failed!'
ShipUpgradePoor = ' (%s short)'
ShipBroadsideInfo = '%s%% %s attack'
ShipUgradeCosts = 'Resources:'
ShipUgradeCostsRequired = 'Required'
ShipUgradeCostsOwned = 'You Have'
ShipUpgradeStats = 'Hull Benefits:'
ShipUpgradeSkillBoosts = 'Skill Boosts:'
ShipUpgradeSkillBoostAdd = 'boosted by'
ShipUpgradeConfirmAsk = 'This will upgrade your hull. Are you sure?'
ShipUpgradeConfirmYes = 'Yes'
ShipUpgradeConfirmNo = 'No'
ShipUpgradeConfirmTitle = 'Upgrade!'
ShipUpgradeConfirmTitleDown = 'Downgrade?'
ShipUpgradeConfirmAskDown = 'This will downgrade your hull. It will not refund money or materials. Are you sure?'
ShipUpgradeConfirmTitleSide = 'Convert Type?'
ShipUpgradeConfirmAskSide = 'This will convert your hull to a different type at the same level. Are you sure?'
HullDefault = 'Basic Hull'
HullReinforced1 = 'Level 1 Reinforced'
HullReinforced2 = 'Level 2 Reinforced'
HullReinforced3 = 'Level 3 Reinforced'
HullStreamlined1 = 'Level 1 Streamlined'
HullStreamlined2 = 'Level 2 Streamlined'
HullStreamlined3 = 'Level 3 Streamlined'
HullCargo1 = 'Level 1 Cargo'
HullCargo2 = 'Level 2 Cargo'
HullCargo3 = 'Level 3 Cargo'
HullStormChaser1 = 'Level 4 Storm Chaser'
HullStormChaser2 = 'Level 5 Storm Chaser'
HullStormChaser3 = 'Level 6 Storm Chaser'
HullFireStorm1 = 'Level 4 Firestorm'
HullFireStorm2 = 'Level 5 Firestorm'
HullFireStorm3 = 'Level 6 Firestorm'
HullCaptBlood1 = 'Level 4 Fortune Hunter'
HullCaptBlood2 = 'Level 5 Fortune Hunter'
HullCaptBlood3 = 'Level 6 Fortune Hunter'
HullSkullBones1 = 'Level 4 Skull & Bones'
HullSkullBones2 = 'Level 5 Skull & Bones'
HullSkullBones3 = 'Level 6 Skull & Bones'
HullIronclad1 = 'Level 4 Copperhead'
HullIronclad2 = 'Level 5 Copperhead'
HullIronclad3 = 'Level 6 Copperhead'
HullLabel = 'Hull'
RiggingLabel = 'Rigging'
DescriptionBase = "The standard wooden frame hull. It creaks a bit and won't impress anyone."
DescriptionReinforced = "With metal plates bolted to the hull, you won't move very fast, but you'll get there in one piece."
DescriptionStreamlined = 'This cuts through the water like a knife through... well... water. Turning and cargo suffer.'
DescriptionCargo = 'The crew quarters have been converted into another cargo hold. You can sleep on the crates!'
DescriptionStormChaser = "Ever try putting lightning rods in the masts? It'll run fast, though no one will man the crow's nest."
DescriptionFirestorm = 'It has flames painted on it, and it shoots firebrand, what else could you ask for?'
DescriptionCaptBlood = 'This clever and efficient design is good at thwarting the dirty navy. It has a bit of everything.'
DescriptionSkullBones = 'Are you a dark and moody pirate? Or maybe you just like skulls. Either way, this boat is for you!'
DescriptionIronClad = 'Watch wooden boats explode from the safety of a hull hardened by layers of iron and steel.'
RiggingBase = 'Basic Rigging'
RiggingOffense1 = 'Offense 1'
RiggingOffense2 = 'Offense 2'
RiggingDefense1 = 'Defense 1'
RiggingDefense2 = 'Defense 2'
RiggingSpeed1 = 'Speed 1'
RiggingSpeed2 = 'Speed 2'
SailPlain = 'Plain'
SailWhite = 'White'
SailBlack = 'Black'
SailGray = 'Gray'
SailBrown = 'Brown'
SailGold = 'Gold'
SailTan = 'Tan'
SailOlive = 'Olive'
SailRed = 'Red'
SailOrange = 'Orange'
SailYellow = 'Yellow'
SailGreen = 'Green'
SailCyan = 'Cyan'
SailBlue = 'Blue'
SailPurple = 'Purple'
SailPink = 'Pink'
SailRose = 'Rose'
SailLime = 'Lime'
SailMaroon = 'Maroon'
SailStripeGreen = 'Green Stripe'
SailStripeRed = 'Red Stripe'
SailStripeViolet = 'Violet Stripe'
SailPatches = 'Patchy'
SailLogoBase = 'Blank'
SailLogoBull = 'Bull Skull'
SailLogoDagger = 'Dagger'
SailLogoScorpion = 'Scorpion'
SailLogoClaw = 'Claw'
SailLogoWasp = 'Wasp'
SailLogoSpider = 'Spider'
SailLogoSnake = 'Snake'
SailLogoHawk = 'Hawk'
SailLogoRose = 'Rose'
SailLogoFlame = 'Flame'
SailLogoSpanishBull = 'Bull'
SailLogoWolf = 'Wolf'
SailLogoAngel = 'Wings'
SailLogoDragon = 'Dragon'
SailLogoShield = 'Shield'
SailLogoHeart = 'Heart'
SailLogoSkull = 'Skull'
SailLogoOctopus = 'Octopus'
SailLogoShark = 'Shark'
SailLogoMermaid = 'Mermaid'
SailLogoStormCloud = 'Storm'
LevelUpHeading = 'Level Up!\nPress K to spend skill point.'
LevelUpHPIncrease = '    %s point HP increase.\n'
LevelUpVoodooIncrease = '    %s point Voodoo increase.\n'
LevelUpSkillPoint = '    %s earned.\n'
LevelUpSkillUnlock = '    %s skill unlocked.\n'
LevelUpCannonDefense = '%s ammo unlocked\n'
LevelUpCannonDefenseAmmoSlot = 'Additional ammo slot unlocked\n'
LevelUpCannonDefenseRepeaterCannon = 'Repeater Cannon unlocked\n'
TradeCannotHoldWarning = 'Cannot hold those Items!'
TradeItemFullWarning = 'Cannot carry more of that Item!'
TradeTimeoutWarning = 'Trade timeout!'
TradeFailedWarning = 'Trade failed'
WeaponSlotWarning = 'Can only equip a weapon on this slot!'
ItemSlotWarning = 'Can only equip an item on this slot!'
AlreadyOwnWeaponWarning = 'Weapon already owned.'
InventoryFullWarning = "This Item won't fit into your inventory!"
NoInventorySpaceWarning = 'Not enough space in your inventory!'
PlunderItemsLeftWarning = 'Some Items could not fit into your inventory.'
CantTrashThat = "You can't trash something you don't have"
NoSwitchingItemsWarning = "You can't switch Items while attacking!"
NoDoubleDrinkingItemsWarning = "You can't drink two things at once!"
FreeWeaponInventoryMessage = 'Free a slot in your weapon inventory before accepting quest reward!'
FreeClothingInventoryMessage = 'Free a slot in your clothing inventory before accepting quest reward!'
FreeJewelryInventoryMessage = 'Free a slot in your jewelry inventory before accepting quest reward!'
FreeTattooInventoryMessage = 'Free a slot in your tattoo inventory before accepting quest reward!'
FailedLootTradeTryAgainMessage = 'The items you requested from the containers were not taken! Please try again!'
FailedLootTradeMessage = 'The items you requested from the container(s) were not taken!'
ItemRemoved = '%s Removed'
ItemDrank = '%s Drank'
FreeWeaponFromBlackSmith = 'Hint: Any blacksmith will\ngive you a free rusty cutlass'
InventoryNotLoaded = 'Your items could not be loaded because your inventory could not connect to the server.\n\nYour items are not gone they are just hiding, probably because they are scared of Jolly Roger. Either that or the server crashed.\n\nWe will continue to look for them.\n\n '
OverflowHint = 'You have more items then can be stored,\nremove some to recover lost items.'
DoNotOwnEnoughWarning = "You don't own more of that Item!"
DrinkPotion = 'Drink\nPotion'
WaitPotion = '%s\nWait'
HowToDrinkPotion = 'Drop a potion here to drink it.'
CannotRedeemYet = 'Please progress further into the game to redeem codes for this pirate.'
PurchaseConfirmation = 'Purchase Confirmed: %s x %s'
PurchaseTimeout = 'Purchase timed out, please try again. Yarrr!'
PurchaseCart = 'Purchase'
SellCart = 'Sell'
PurchaseCommit = 'Buy'
PurchasePending = 'Buying'
PurchaseCommitHelp = 'Finalize the Sale'
Cost = 'Cost: '
Gain = 'Gain: '
Total = 'Total: '
YourMoney = 'Your Gold: '
YourPVPMoney = 'Your Infamy: '
Vests = 'Vests'
Vest = 'Vest'
Shirts = 'Shirts'
Shirt = 'Shirt'
Pants = 'Pants'
Coats = 'Coats'
Coat = 'Coat'
Shoes = 'Shoes'
Shoe = 'Shoe'
Hats = 'Hats'
Hat = 'Hat'
Belts = 'Belts'
Belt = 'Belt'
BrowJewelry = 'Brow Jewelry'
EarJewelry = 'Ear Jewelry'
NoseJewelry = 'Nose Jewelry'
MouthJewelry = 'Mouth Jewelry'
HandJewelry = 'Hand Jewelry'
ChestTattoo = 'Chest Tattoo'
ArmTattoo = 'Arm Tattoo'
FaceTattoo = 'Face Tattoo'
SimpleStoreClickPreview = 'Click on the item to preview'
MerchantStore = 'Merchant Store'
StowawayMenuTitle = 'Stowaway Destinations'
TailorStore = 'Accessories Store'
TailorPurchase = 'Purchases'
TailorPurchased = 'Purchased'
TailorSelling = 'Selling'
TailorWardrobe = 'My Items'
TailorRemove = 'Remove'
TailorSell = 'Sell'
TailorAddToCart = 'Add'
TailorPreview = 'Click to preview'
TailorEmptyWardrobe = 'No items in category.'
TailorEquip = 'Wear'
TailorPage = 'Page'
TailorTakeOff = 'Take Off'
TattooShopOwned = 'Currently worn'
TattooConfirm = 'Do you wish to\npurchase a %s\n%s for\n%s gold?'
TattooPurchase = 'Purchase Tattoo'
TattooChest = 'Chest'
TattooLeftArm = 'Left Arm'
TattooRightArm = 'Right Arm'
TattooArm = 'Arm'
TattooFace = 'Face'
TattooGeneral = 'General'
TattooShop = 'Tattoo Shop'
TailorStartingItem = 'Starting Item'
BarberConfirm = 'Would you like to buy \n%s for %s gold?'
BarberNoMustache = 'Your current beard does not allow for mustaches.'
BarberPurchase = 'Purchase Style'
StoreNewItem = 'New Item!'
CatalogStore = 'Catalog'
SimpleStoreSell = 'Sell'
SimpleStoreRedeemCode = 'Redeem Code'
SimpleStoreQty = 'Quantity: '
SimpleStoreCost = 'Total Cost: '
SimpleStoreOwned = 'You Own: '
SimpleStoreFull = '(max)'
SimpleStoreFullNonStack = '(full)'
JewelryTypeNames = {
    ItemGlobals.BROW: BrowJewelry, ItemGlobals.EAR: EarJewelry, ItemGlobals.NOSE: NoseJewelry, ItemGlobals.MOUTH: MouthJewelry, ItemGlobals.HAND: HandJewelry
}
CATALOG_HOLIDAY_ID_2_NAME = {
    5: "St. Patrick's Day",
    7: "Mother's Day",
    9: "Father's Day",
    10: 'Summer Festival',
    13: 'Halloween',
    21: 'Winter Festival',
    22: "New Year's",
    23: "Valentine's Day",
    33: 'Mardi Gras',
    41: "April Fool's",
    3901: 'Royal Commodore',
    3902: 'Spanish Adventurer',
    3903: 'Emerald Duelist',
    3904: 'Admiral',
    3905: 'Scourge of the Seas',
    3906: 'Barbary Corsair',
    3907: 'Snapdragon',
    3908: 'French Assassin',
    3909: 'Capt. Black',
    3910: 'Rogue Privateer',
    3911: 'Bounty Hunter',
    3912: 'Barony',
    3913: 'Garb of the Undead',
    3914: 'French Fencer',
    3915: "Town Mayor's Outfit",
    3916: 'Spanish Conquistador',
    3917: 'Sea Serpent',
    3918: 'Merchant Voyager',
    3919: 'The Diplomat',
    3920: 'Crimson Captain',
    3921: 'China Seas Warrior',
    3922: "Raven's Cove Mercenary"
}

def getJewelryTypeName(typeId):
    return JewelryTypeNames.get(typeId, '')


TattooTypeNames = {
    ItemGlobals.CHEST: ChestTattoo, ItemGlobals.ARM: ArmTattoo, ItemGlobals.FACE: FaceTattoo
}

def getTattooTypeName(typeId):
    return TattooTypeNames.get(typeId, '')


TailorColorStrings = {
    0: 'Plain',
    1: 'Light Blue',
    2: 'Light Yellow',
    3: 'Light Green',
    4: 'Brown',
    5: 'Pink',
    6: 'Light Purple',
    7: 'Light Grey',
    8: 'Blue',
    9: 'Yellow',
    10: 'Light Green',
    11: 'Light Brown',
    12: 'Light Red',
    13: 'Light Purple',
    14: 'Grey',
    15: 'Dark Blue',
    16: 'Dark Yellow',
    17: 'Dark Green',
    18: 'Dark Brown',
    19: 'Red',
    20: 'Purple',
    21: 'Bright Orange',
    22: 'Bright Yellow',
    23: 'Bright Blue',
    24: 'Lavender',
    25: 'Forest Green',
    26: 'Magenta',
    27: 'Bright Green',
    28: 'Navy Blue',
    29: 'Bright Red',
    30: 'Dark Black',
    31: 'Light Green',
    32: 'Pink',
    33: 'Lavender',
    34: 'Light Blue',
    35: 'Brown',
    36: 'Forest Green',
    37: 'Pink',
    38: 'Lavender',
    39: 'Blue',
    40: 'Dark Pink',
    41: 'Dark Lavender',
    42: 'Gray',
    43: 'Dark Gray',
    44: 'Brown'
}
HAIR = 0
BEARD = 1
MUSTACHE = 2
barberNames = {
    HAIR: 'Hair',
    BEARD: 'Beards',
    MUSTACHE: 'Mustaches'
}
BarberShortStrings = {
    0: 'Shaved',
    1: 'Haircut',
    2: 'Ponytail',
    3: 'Balding',
    4: 'Mohawk',
    5: 'Beard',
    6: 'Mustache',
    7: 'Bun',
    8: 'Barrette'
}
BarberLongStrings = {
    0: 'Completely shaved',
    1: "Men's short haircut",
    2: "Men's haircut with short ponytail",
    3: "Men's haircut with short top ponytail",
    4: "Men's balding haircut",
    5: "Men's shaved head with top ponytail",
    6: "Men's long mullet",
    7: "Men's short Mohawk",
    8: 'Short beard with mustache',
    9: 'Long beard with mustache',
    10: 'Long sideburns with mustache',
    11: 'Medium goatee',
    12: 'Thin goatee',
    13: 'Long hanging goatee',
    14: 'Side chops',
    15: 'Short goatee with soul patch',
    16: 'Thin side burns',
    17: 'Long braided beard',
    18: 'Thick bushy mustache',
    19: 'Thin short mustache',
    20: 'Regular short mustache',
    21: 'Long hanging mustache',
    22: 'Waxed long mustache',
    23: 'Curly waxed long mustache',
    24: 'Small bun',
    25: 'Small bun with bangs',
    26: 'Small bun with long bangs',
    27: 'Long top ponytail',
    28: 'Long top ponytail with bangs',
    29: 'Long top ponytail with long bangs',
    30: 'Short barrette haircut',
    31: 'Short barrette haircut with bangs',
    32: 'Medium haircut with bun',
    33: 'Medium haircut with long top ponytail',
    34: 'Medium haircut with barrette',
    35: 'Barrette with long braided ponytail',
    36: 'Barrette with long braided ponytail and bangs',
    37: 'Barrette with long braided ponytail and long bangs',
    38: 'Short barrette haircut',
    39: 'Short barrette with bangs',
    40: 'Short barrette with long bangs',
    41: 'Long layered haircut',
    42: 'Short layered haircut'
}
JewelryStrings = {
    0: 'Golden eye brow spike',
    1: 'Silver eye brow spike',
    2: 'Golden eye brow ring',
    3: 'Silver eye brow ring',
    4: 'Golden ear stud',
    5: 'Silver ear stud',
    6: 'Golden small ear loop',
    7: 'Silver small ear loop',
    8: 'Golden ear spike',
    9: 'Silver ear spike',
    10: 'Golden ear double loop',
    11: 'Silver ear double loop',
    12: 'Gold and silver ear double loop',
    13: 'Golden small ear spike',
    14: 'Silver small ear spike',
    15: 'Golden large ear loop',
    16: 'Silver large ear loop',
    17: 'Golden small ear loop',
    18: 'Silver small ear loop',
    19: 'Golden large ear loop with double top ring',
    20: 'Silver large ear loop with double top ring',
    21: 'Golden double top ear ring',
    22: 'Silver double top ear ring',
    23: 'Golden spike and ring',
    24: 'Silver spike and ring',
    25: 'Golden large ear stud with double top ring',
    26: 'Silver large ear stud with double top ring',
    27: 'Golden nose loop',
    28: 'Silver nose loop',
    29: 'Golden nose spike',
    30: 'Silver nose spike',
    31: 'Golden nose double spike.',
    32: 'Silver nose double spike.',
    33: 'Golden nose spike with loop.',
    34: 'Silver nose spike with loop.',
    35: 'Golden lip ring',
    36: 'Silver lip ring',
    37: 'Golden mouth spike',
    38: 'Silver mouth spike',
    39: 'Golden double lip ring',
    40: 'Silver double lip ring',
    41: 'Golden band',
    42: 'Silver band',
    43: 'Golden ring with ruby',
    44: 'Silver ring with ruby',
    45: 'Golden ring with amethyst',
    46: 'Silver ring with amethyst',
    47: 'Golden ring with sapphire',
    48: 'Silver ring with sapphire',
    49: 'Golden ring with turquoise',
    50: 'Silver ring with turquoise',
    51: 'Golden ring with emerald',
    52: 'Silver ring with emerald',
    53: 'Golden ring with onyx',
    54: 'Silver ring with onyx',
    55: 'Golden double band',
    56: 'Silver double band',
    57: 'Ruby lip ring',
    58: 'Onyx large ear loop',
    59: 'Sapphire eye brow ring',
    60: 'Ruby and amethyst ear stud and rings',
    61: 'Emerald double nose spike',
    62: 'Torquoise eye brow spike'
}
ClothingStrings = {
    0: 'Small hat',
    1: "Large sailor's hat",
    2: 'Tied hat',
    3: 'Hat',
    4: 'Exclusive! Free skull bandana!',
    5: 'Sleeveless shirt',
    6: 'Striped sleeveless shirt',
    7: 'Sleeveless shirt with suspenders',
    8: 'Fancy sleeveless shirt',
    9: 'Fancy short sleeve shirt',
    10: 'Short sleeve shirt',
    11: 'Striped short sleeve shirt',
    12: 'Long sleeve shirt',
    13: 'Fancy long sleeve shirt',
    14: 'Long sleeve button down shirt',
    15: 'Long sleeve open button down shirt',
    16: 'Plain vest',
    17: 'Large vest',
    18: 'Large long coat',
    19: 'Short coat',
    20: 'Long pants',
    21: 'Striped long pants',
    22: 'Cloth belt',
    23: 'Fancy belt',
    24: 'Plain shoes',
    25: 'Large hat with feather',
    26: 'Puffy short sleeve shirt',
    27: 'Long sleeve fancy shirt',
    28: 'Low vest',
    29: 'Cut off vest',
    30: 'Long coat',
    31: 'Shorts',
    32: 'Long skirt',
    33: 'Striped belt',
    34: 'Boots',
    35: 'Tall boots',
    36: 'Tall knee high boots',
    37: 'Large hat with feather',
    38: 'Large leather hat',
    39: "Fancy Captain's hat",
    40: 'Fancy short sleeve open shirt',
    41: 'Fancy long sleeve open shirt',
    42: 'Fancy long sleeve shirt with bowtie',
    43: 'Fancy vest with buttons',
    44: 'Large closed leather vest',
    45: 'Large closed vest with pockets',
    46: 'Fancy long vest',
    47: 'Long vest',
    48: 'Long fancy coat',
    49: 'Short fancy coat',
    50: 'Fancy striped pants',
    51: 'Fancy long pants',
    52: 'Fancy long sleeve belly shirt',
    53: 'Fancy vest',
    54: 'Fancy low cut vest',
    55: 'Fancy cut off vest',
    56: 'Tall fancy boots',
    57: 'Truehound Bandana',
    58: 'Fine Callecutter Hat',
    59: "Barbossa's Feathered Hat",
    60: 'Truehound Shirt',
    61: 'Puffy Callecutter Shirt',
    62: "Barbossa's Sleeveless Shirt",
    63: 'Callecutter Vest',
    64: "Barbossa's Closed Vest",
    65: "Barbossa's Long Coat",
    66: 'Truehound Pants',
    67: 'Long Callecutter Slacks',
    68: "Barbossa's Long Pants",
    69: 'Truehound Belt',
    70: 'Leather Callecutter Belt',
    71: "Barbossa's Belt",
    72: 'Truehound Boots',
    73: 'Tall Callecutter Boots',
    74: "Barbossa's Tall Boots",
    75: 'Truehound Bandana',
    76: 'Fine Callecutter Hat',
    77: "Barbosssa's Feathered Hat",
    78: 'Truehound Shirt',
    79: 'Puffy Callecutter Shirt',
    80: "Barbossa's Long Sleeve Shirt",
    81: 'Callecutter Vest',
    82: "Barbossa's Closed Vest",
    83: "Barbossa's Long Coat",
    84: 'Truehound Pants',
    85: 'Long Callecutter Slacks',
    86: "Barbossa's Short Pants",
    87: 'Truehound Belt',
    88: 'Leather Callecutter Belt',
    89: "Barbossa's Belt",
    90: 'Truehound Boots',
    91: 'Tall Callecutter Boots',
    92: "Barbossa's Short Boots",
    93: 'Exclusive! Free golden skull bandana!',
    94: "Valentine's Day Shirt"
}
TattooStrings = {
    0: 'Tattoo Removal',
    1: 'Shark tattoo',
    2: 'Skull pirate tattoo',
    3: 'Skull shield tattoo',
    4: 'Skull stab tattoo',
    5: 'Snake and daggers tattoo',
    6: 'Fancy dagger tattoo',
    7: 'Skull flag tattoo',
    8: 'Fancy key tattoo',
    9: 'Skull iron cross tattoo',
    10: 'Sword and scroll tattoo',
    11: 'Dagger tattoo',
    12: 'Heart torch tattoo',
    13: 'Lock and key tattoo',
    14: 'Skull and dagger',
    15: 'Skull and crossbones tattoo',
    16: 'Anchor tattoo',
    17: 'Compass tattoo',
    18: 'Dagger and scroll tattoo',
    19: 'Ship and anchor tattoo',
    20: 'Skull and crossbones tattoo',
    21: 'Skull tattoo',
    22: 'Nautical star',
    23: 'Mayan face tattoo',
    24: 'Octopus tattoo',
    25: 'Tribal skull tattoo',
    26: 'Squid and ship tattoo',
    27: "Saint Patrick's Day tattoo",
    28: 'Native lizards tattoo',
    29: 'Tribal swirl tattoo',
    30: 'Tribal bird tattoo',
    31: 'Tribal jellyfish tattoo',
    32: 'Tribal jellyfish tattoo',
    33: 'African face tattoo',
    34: 'Maori face tattoo',
    35: 'Asian leaf tattoo',
    36: 'Ethnic tattoo',
    37: 'Maori man tattoo',
    38: 'Native leaf tattoo',
    39: 'Thai tattoo',
    40: 'Two clovers face tattoo',
    41: 'Horseshoe face tattoo',
    42: 'Celtic leaf tattoo',
    43: 'Ethnic eagle tattoo',
    44: 'Crossed flintlocks tattoo',
    45: 'Shamrock tattoo',
    46: 'Thai monkey face tattoo',
    47: 'Tribal face tattoo',
    48: 'Tribal face tattoo',
    49: 'Asian face tattoo',
    50: 'Maori face tattoo',
    51: 'Tribal design tattoo',
    52: 'Celtic knot tattoo',
    53: 'Chinese knot tattoo',
    54: 'Hawaiian tiki tattoo',
    55: 'Twin sharks tattoo',
    56: 'Tribal waves tattoo',
    57: 'Celtic deer tattoo',
    58: 'Hawaiian design tattoo',
    59: 'Petroglyph tattoo',
    60: 'Ravens tattoo',
    61: 'Wave fan tattoo',
    62: 'Hawaiian pectoral tattoo',
    63: 'Tribal yakuza tattoo',
    64: 'Jack Sparrow eye tattoo',
    65: 'Tribal cheek tattoo',
    66: 'Tribal chin tattoo',
    67: 'Tribal forehead tattoo',
    68: 'Maori chin tattoo',
    69: 'Maori nose tattoo',
    70: 'Native eye tattoo',
    71: 'Tribal goatee tattoo',
    92: "Mother's Day flower tattoo",
    95: "Mother's Day sparrow tattoo",
    96: "Classic Mother's Day tattoo",
    100: "Mother's Day face flower tattoo",
    102: "Mother's Day face hearts tattoo",
    104: 'Spanish Ship PVP Tattoo',
    105: 'French Ship PVP Tattoo',
    111: 'Octopus Tattoo',
    112: 'Healed Bullet Holes Tattoo',
    113: 'Pirate Brand Tattoo',
    114: 'Large Stitched Scar',
    115: 'Stitched Bullet Holes Tattoo',
    116: 'Large X Stitch Tattoo',
    117: 'Large Y Stitch Tattoo',
    106: 'Healed Bullet Holes Tattoo',
    107: 'Pirate Brand Tattoo',
    108: 'Large Stitched Scar',
    129: 'Stitched Bullet Holes Tattoo',
    130: 'Large X Stitch Tattoo',
    131: 'Large Y Stitch Tattoo'
}
ClothingFlavorText = {
    1: 'Fine Pirate gARRRb!, part of a perfect plundering ensemble',
    2: 'Townie clothes... cleaner than any respectable pirate should be',
    3: 'Fancy Frilly Finery for Frivolous Festivities',
    4: 'Dirty Navy clothes for easy slippage behind enemy lines',
    5: 'Landlubber Wear: 50% Lub, 50% Ber',
    6: 'Lovingly borrowed, Never returned',
    7: 'Stitched together from leftovers of hand-me-downs',
    8: "Captain's Finest... Hookwash only",
    9: 'Woodland clothing... Show your love of nature without wearing bark & pine cones',
    10: 'Holiday clothes for that special time of yaarrr!',
    11: 'Something fetching when you go fetching your gold',
    12: 'Clothes for the few, the proud, the presumed guilty',
    13: 'Show yer best backside running away from powerful enemies',
    14: 'The perfect piece for felling foul tree stumps',
    15: 'OMG this is like totally perfect for you!!  Show your BFF!',
    16: 'Will these make your bum look fat? Yes, yes they will.',
    17: "Mirror, mirror on the wall, who's the coolest pirate of all? Do you think he wants his shirt back?",
    18: "Mirror, mirror on the wall, who's the coolest pirate of all? Do you think she wants her shirt back?",
    19: 'So "stylish" this will make other pirates shoot grog out their nose then challenge you to PVP',
    20: 'Ideal piece to wear during an invasion - it will distract the Undead',
    21: 'Three words - fab-you-less!',
    22: 'There are no words to describe this piece so why even try?',
    23: 'What all the best dressed Pirates are wearing to walk the plank',
    24: 'This shirt is perfect to show off those bulky guns of yours, ey?',
    25: 'Puffy sleeves are always a good choice for a swashbuckler',
    26: 'Made of the finest cloth you can buy - or steal - which it was',
    27: 'Your mates and guild fellows will be GREEN with envy when they see this shirt',
    28: 'Red is the ideal color for a fighting Pirate - helps cover the blood stains',
    29: 'Brown is a sensible color - and always in fashion, savvy?',
    30: 'Vests of any shade or make are good for hiding daggers and other toys',
    31: 'A classic - something every Pirate should have in their clothing stash',
    32: "Expensive and worth every penny - you'll turn all the Undead heads with this piece",
    33: 'Three words - oh-la-la - turn those Pirate heads with this little number',
    34: 'The perfect short pantaloons for those humid Caribbean days',
    35: 'Skirt with some frilly fringe - ideal for sassing-off the Undead',
    36: 'Stick a feather in your cap with the fetching plumed hat',
    37: 'A sassy sash in a bold, red accent - perfect for wiping your cutlass clean',
    38: 'A sensible hat for all weather wear - plus, it keeps your head from sunburn',
    39: "This is no joke - okay it is because it's a Jester Hat for all you funny Pirates!",
    40: "Someone must have bet you couldn't find a hat bigger than your ship",
    41: 'Metal hats may protect against voodoo mind control... or not',
    42: 'This is NPC clothing, if you have it, it may decide to disappear! you were warned!',
    43: "If you see anyone wearing this, don't let them buy you a drink.",
    44: 'The Baron really should be more careful with his laundry.',
    45: 'The Baroness really should be more careful with her laundry.',
    46: 'Fit for a Prince! but it looks alright on you anyway.',
    47: "If you think about it, a Rogue Privateer is just a pirate. But don't tell them that.",
    48: 'The point of your sword made a very diplomatic arguement for him to give you his hat.',
    49: 'This almost always comes with an impressive scar.',
    50: 'A peacock is a male peafowl. Females are peahens and their young are called peachicks.',
    51: "Appropriate attire for the discriminating ne' er-do-well.",
    52: 'Just in case you want to ironically dress like a zombie.',
    53: 'In the great tradition of Ching Shih, the widow of Zheng.',
    54: "Wild fires aren't usually a problem on the open ocean, but you aim to change that.",
    55: 'Wear this, and the next bounty hunter will think twice before thinking twice.',
    56: 'Who were the Barbary Corsairs? Were they pirates? Were they barbers? Were they pirate barbers? perhaps!',
    57: 'The point of your sword made a very diplomatic arguement for him to give you his shirt.',
    58: 'The point of your sword made a very diplomatic arguement for her to give you her blouse.',
    59: 'The point of your sword made a very diplomatic arguement for him to give you his coat.',
    60: 'The point of your sword made a very diplomatic arguement for her to give you her coat.',
    61: 'The point of your sword made a very diplomatic arguement for him to give you his pants.',
    62: 'The point of your sword made a very diplomatic arguement for her to give you her pants.',
    63: 'Fit for a very particularly fierce Prince, but it looks alright on you anyway.',
    64: 'The point of your sword made a very diplomatic arguement for him to give you his shoes.',
    65: 'The point of your sword made a very diplomatic arguement for her to give you her shoes.'
}
TattooFlavorText = {
    1: "Be glad this isn't permanent",
    2: 'Lovely classic design',
    3: 'The artist must have learned this design from a local tribe',
    4: 'Ouch... that looks painful',
    5: 'The "in" tattoo from back in the day... it\'s SO last week',
    6: 'Something this stylish is going to hurt - a lot - so be prepared',
    7: "The lady Pirates will love this one, whether you're a lady or not!",
    8: 'Something every bad and bold Pirate should have on his chest',
    9: 'A hearty tattoo for a hearty Pirate like yourself',
    10: 'With this tattoo, who needs a shirt!',
    11: 'This little ditty is worth all the pain...and the festering infection...no worries!',
    12: 'A tattoo that even your mother would be proud of',
    13: 'Face it mate, this is the finest design our artist could conjure up',
    14: "Your face will look better with this one...I'm just saying",
    15: 'Known to all the native Carib population as a tattoo with strong mojo',
    16: 'This tattoo wards off evil spirits and likely suitors - use as your own risk',
    17: 'Caution - wearing this tattoo will drive some Undead vermin wild',
    18: 'Arm yourself with this excellent design that let\'s others know how "bad" you really are!',
    19: 'The finest tattoo craftsmanship in the island - ready for purchase',
    20: "Don't shrink away from this bold tattoo - wearing it takes courage, and a little gold"
}
JewelryFlavorText = {
    1: "Shiny... It's like a treasure for your face",
    2: 'Not all that glitters is gold, but this is',
    3: 'This looks a little painful, such is the price of beauty',
    4: 'An inscription has been filed away',
    5: "This leaves quite an impression, especially on someone's forehead",
    6: 'For the discerning pirate who likes a lot of cranial accessories',
    7: 'Everyone will know you are special when you wear this',
    8: 'The jewel on this looks like it was ripped out of a crown',
    9: 'Pretty, shiny things to distract your enemies while fighting',
    10: 'Reward yourself after a hard day of pillaging and plundering with this fine piece of jewelry',
    11: 'Something to prove to your mates that you have good taste, or just lots of  gold to waste!',
    12: 'Arrrrrr you man enough to wear this?',
    13: 'Tasteful - elegant - stolen from the fingers of a true English gentleman',
    14: 'Classic design - flawless craftsmanship - taken from an Undead Gypsy and might be cursed',
    15: "This lovely piece will help you sink more ships - not really but you'll look good doing it!",
    16: "Rumor has it that this was forged from the melted sword of Blackbeard himself - we know because we're the one's who started the rumor!",
    17: 'Made from pure gold - as pure as a Pirates reputation',
    18: 'This will make you look so good even the Undead will swoon!',
    19: 'A timeless design looks good on your neck - just before you lay it on the chopping block',
    20: "Why not add some sparkle your outfit next time you're in jail?"
}
JewelryStore = 'Jewelry Store'
Jewelry = 'Jewelry'
CannonAmmoStore = 'Cannon Ammo'
Shipyard = 'Shipyard'
Submit = lSubmit
SubmitNameHelp = 'Commit the Ship Name'
Random = 'Random'
Shuffle = 'Shuffle'
RandomNameHelp = 'Make a random name'
NamePanelTitle = 'Name Your Ship'
TypeAName = 'Type'
PickAName = 'Pick'
TypeANameHelp = 'Type a Custom Name'
PickANameHelp = 'Generate a Ship Name'
TypeANameInstructions = 'Type in a custom name and submit it to the Pirate Ship Council for approval.'
AdventureTimerCancelHelp = 'Cancel the Adventure'
Timer = 'Timer'
AtSea = 'Out at Sea'
InPort = 'Docked'
InBottle = 'In Bottle'
Chartered = 'Chartered'
ShoveOff = 'Leaving Port'
LootPlundered = 'Plunder!'
SkillReady = 'Skill Ready'
ShipDisabled = 'Disabled'
Sunk = 'Sunk!'
Captain = 'Captain'
Commodore = 'Commodore'
ShipPinnedWarning = 'Ship is pinned in place!'
NotCaptainWarning = 'Must be the Captain to start Adventure!'
NotShipTeamWarning = "Not part of the Ship's Crew!"
AlreadyInUseWarning = 'Already in use!'
NoBoardingPermissionWarning = 'Must be part of Crew to board Ship!'
NoHelmPermissionWarning = 'Must be the Captain to Shove Off!'
NoBoardingCaptainReserved = 'Cannot board! Remaining space is reserved for the Captain!'
CannotRepairRepairedShipWarning = 'Ship does not need repairs!'
CannotRepairWhileWheelOccupiedWarning = 'Cannot repair while steering wheel is in use!'
OnlyCaptainCanUseWarning = 'Must be the Captain to use the steering wheel!'
IslandPlayerBarrierWarning = 'Need a Ship to enter High Seas!'
NoManaWarning = 'Not enough ' + ManaName + '!'
NotAttunedWarning = 'Must Attune Doll to a Target first!'
NeedFriendlyTarget = 'This skill must be used on an Ally!'
NeedHostileTarget = 'This skill must be used on an Enemy!'
TooFarAttuneWarning = 'Must be closer to Attune Doll!'
OutOfRangeWarning = 'Out of range!'
TooCloseWarning = 'Too close to fire this gun!'
TooCloseToAttackWarning = 'Too close to use this attack!'
UnattuneAll = 'Unattune All'
OutOfAmmoWarning = 'Out of Ammo!'
AmmoChargingWarning = 'Cannot change skills while charging!'
OutOfItemWarning = 'Item is used up!'
SkillRechargingWarning = 'Skill is not finished recharging!'
TonicRechargingWarning = 'Tonic is not finished recharging!'
RepairKitRechargingWarning = 'Repair kit is not finished recharging!'
BuffPriorityWarning = 'Cannot use that skill right now!'
SpellFailedWarning = 'Spirit summoning interrupted!'
NotUsableInAirWarning = 'Skill not usable in air!'
OutOfSightWarning = 'Target is out of sight!'
NoBroadsidesWarning = 'No broadside cannons to fire!'
FullHealthWarning = 'You already have full Health!'
FullShipHealthWarning = 'Your ship does not need repairs!'
TonicHelp = 'Drink a Tonic to heal.'
UsingSkill = 'Using Skill'
FriendlyFireWarning = "Cannot damage other Player's Ships!"
CannotDockYet = 'Cannon dock under fire, try again in %s seconds!'
TeamFireWarning = 'Cannot damage your own team...'
StunWarning = 'You cannot attack while Stunned!'
SailsNotReadyWarning = 'Sails not ready yet!'
RamWhileBoardingWarning = 'Cannot ram while boarding!'
TonicChargingWarning = 'Cannot use tonic while charging!'
TonicCannonWarning = 'Cannot use tonic while on a cannon!'
TonicParlorGameWarning = 'Cannot use tonic while playing a parlor game!'
TonicPVPWarning = 'Cannot use tonic while in Pirate vs. Pirate!'
NotWhileFishingWarning = 'Ye cannot do that while fishing, matey!'
NotFishingWarning = 'Ye gotta be fishing to do that, matey!'
FishingLureInWaterWarning = 'Ye gotta get yer lure in the water first, matey!'
FishingAbilityWarning = 'Ye cannot use that skill right now!'
FishingFightAbilityWarning = "Ye can only do that when yer fightin' a fish!"
NotEnoughFishingLures = "Ye don't have any lures of that type!"
FishingNoRodWarning = 'Ye need to get a fishing rod from the fishmaster first!'
FishingNoLuresWarning = 'Ye need to go buy some fishing lures from the fishmaster first!'
FishingNoLureEquipped = 'Ye need to choose a new lure for your line!'
LaunchFishingBoat = 'Go Fish'
FishingBoatVelvetRope = 'You need to have Unlimited Access to launch a fishing boat.'
NoFishingWhileUndeadWarning = "The Undead can't fish!"
EquipReasonVelvet = 'Sign up for Unlimited Access to use this item.'
EquipReasonGenderMale = 'This item is for men.'
EquipReasonGenderFemale = 'This item is for women.'
EquipReasonLevel = 'You are too low level for this item.'
EquipReasonFull = 'You need to make room to do that.'
EquipReasonFullSlot = 'That spot is already full.'
EquipItemInFromOverflow = 'A %s has been moved into your\ninventory from overflow.'
EquipReasonInventory = 'Your inventory was not found. Please try again in a few seconds.'
TonicBuffActiveWarning = 'Cannot mix with %s!'
NotGroggyWarning = "You aren't groggy!"
NoTransformInWaterWarning = "You better not drink this while you're in water..."
KnockdownWarning = 'You cannot attack while you are knocked down!'
DefenseSkillWarning = 'Defense skills trigger automatically when you are attacked!'
WrongDirectionWarning = 'You cannot use this attack while the Enemy is facing you!'
ScoreboardTitle = 'High Seas Adventure:'
LootScoreboard = 'High Seas Adventure Results:'
AdventureResults = 'Voyage Results:'
DividingPlunder = 'Plunder & Loot:'
CargoPlunder = 'Cargo Plunder:'
ShipStatus = 'Ship Status:'
PlunderShare = 'Your Plunder Share:'
PlunderGold = 'Gold taken from Loot:'
LootShare = 'Loot Already Collected:'
LimitedShare = 'Basic Player (Navy Tax -50%)'
UnlimitedShare = 'Unlimited Player (Pirate Bonus +50%)'
RatingsTitle = 'Pirate Rating:'
PlunderedLootContainers = 'Loot Containers:'
UnknownGoldValue = '??? %s' % MoneyName
LootTimeoutWarning = 'You have 60 seconds left to take your loot!'
LootTimeoutSorry = 'Your Loot Expired!'
You = 'You'
LowerYou = 'you'
Team = 'Team'
TotalTime = 'Total Time'
CrewRemaining = 'Shipmates Remaining'
ShipsSunk = 'Ships Sunk'
UndeadDefeated = 'Undead Defeated'
PiratesDefeated = 'Pirates Defeated'
NavyDefeated = 'Navy Defeated'
CreaturesDefeated = 'Creatures Defeated'
SeamonstersDefeated = 'Sea Monsters Defeated'
TownfolkDefeated = 'Townfolk Killed'
GoldLooted = 'Gold Looted'
CargoLooted = 'Cargo Looted'
NoCargoLooted = 'No Cargo Looted'
NoLootContainersPlundered = 'No Loot Containers Plundered'
CaptainsBonus = "Captain's Bonus"
ShipDamage = 'Ship Damage'
ShipRepairCost = 'Repair Cost'
PayForRepairs = 'Pay for Repairs'
TotalGold = 'Total Gold Earned'
CrewRating = 'Shipmates Rating:'
Rating = 'Your Rating:'
__highSeasAdventureRating = {
    0: 'Stowaway',
    1: 'Cabinboy',
    3: 'Swabbie',
    6: 'Deckhand',
    10: 'Seaman',
    15: 'Mariner',
    20: 'Swashbuckler',
    30: 'First Mate',
    50: 'Robber Baron!'
}

def getHighSeasRating(value):
    probabilityTable = __highSeasAdventureRating.keys()
    probabilityTable.sort()
    for rating in probabilityTable:
        if value <= rating:
            return __highSeasAdventureRating[rating]

    return __highSeasAdventureRating[rating]


__crewAdventureRating = {
    -1: 'Landlubbers', 0: 'Sailors', 5: 'Sea Dogs', 10: 'Adventurers!', 20: 'Plunderers!', 30: 'Raiders!', 40: 'Buccaneers!', 50: 'Warmongers!', 75: 'Robber Villains!', 100: 'HighSea Terrors!'
}

def getCrewRating(value):
    probabilityTable = __crewAdventureRating.keys()
    probabilityTable.sort()
    for rating in probabilityTable:
        if value <= rating:
            return __crewAdventureRating[rating]

    return __crewAdventureRating[rating]


InvasionScoreboardTitle = '%s Invasion Results:'
InvasionWon = 'Victory! Jolly Roger Defeated!'
InvasionLost = 'Defeat! %s Destroyed!'
InvasionMainZoneSaved = '%s Saved:'
InvasionBarricadesSaved = '%s Surviving Barricades:'
InvasionEnemyKilled = '1 Enemy Defeated:'
InvasionEnemiesKilled = '%s Enemies Defeated:'
InvasionWavesCleared = '%s Enemy Wave(s) Cleared:'
InvasionTotalBonus = 'Total Notoriety Bonus:'
InvasionNotoriety = '%s Notoriety'
InvasionNotorietyBonus = '+%s%% Notoriety Bonus'
CRConnecting = 'Connecting...'
CRNoConnectTryAgain = 'Could not connect to %s:%s. Try again?'
CRNoConnectProxyNoPort = 'Could not connect to %s:%s.\n\nYou are communicating to the internet via a proxy, but your proxy does not permit connections on port %s.\n\nYou must open up this port, or disable your proxy, in order to play.  If your proxy has been provided by your ISP, you must contact your ISP to request them to open up this port.'
CRLostConnection = 'Your internet connection has been unexpectedly broken.'
CRBootedReasons = {
    1: 'An unexpected problem has occurred.  Your connection has been lost, but you should be able to connect again and go right back into the game.',
    100: 'You have been disconnected because someone else just logged in using your account on another computer.',
    120: 'You have been disconnected because of a problem with your authorization to use keyboard chat.',
    122: 'There has been an unexpected problem logging you in.  Please contact customer support.',
    125: 'Your installed files appear to be invalid.  Please use the Play button on the official website to run.',
    126: 'You are not authorized to use administrator privileges.',
    151: 'You have been logged out by an administrator working on the servers.',
    153: 'The world you were playing on has been reset.  Everyone who was playing on that world has been disconnected.  However, you should be able to connect again and go right back into the game.',
    288: 'Sorry, you have used up all of your available minutes this month.',
    349: 'Sorry, you have used up all of your available minutes this month.'
}
CRBootedReasonUnknownCode = 'An unexpected problem has occurred (error code %s).  Your connection has been lost, but you should be able to connect again and go right back into the game.'
CRTryConnectAgain = '\n\nTry to connect again?'
CRToontownUnavailable = 'Pirates appears to be temporarily unavailable, still trying...'
CRToontownUnavailableCancel = lCancel
CRNameCongratulations = 'CONGRATULATIONS!!'
CRNameAccepted = 'Your name has been\napproved by the Pirate Bretheren.\n\nFrom this day forth\nyou will be named\n"%s"'
CRServerConstantsProxyNoPort = 'Unable to contact %s.\n\nYou are communicating to the internet via a proxy, but your proxy does not permit connections on port %s.\n\nYou must open up this port, or disable your proxy, in order to play.  If your proxy has been provided by your ISP, you must contact your ISP to request them to open up this port.'
CRServerConstantsProxyNoCONNECT = 'Unable to contact %s.\n\nYou are communicating to the internet via a proxy, but your proxy does not support the CONNECT method.\n\nYou must enable this capability, or disable your proxy, in order to play.  If your proxy has been provided by your ISP, you must contact your ISP to request them to enable this capability.'
CRServerConstantsTryAgain = 'Unable to contact %s.\n\nThe account server might be temporarily down, or there might be some problem with your internet connection.\n\nTry again?'
CRServerDateTryAgain = 'Could not get server date from %s. Try again?'
AfkForceAcknowledgeMessage = 'Your pirate got groggy and passed out.'
PeriodTimerWarning = 'Your time limit this month is almost over!'
PeriodForceAcknowledgeMessage = 'You have used up all of your available minutes this month.  Come back and play some more next month!'
CREnteringToontown = 'Entering Pirates...'
CRAvatarListFailed = 'Failed to login and retrieve your pirates. Please restart and try again.'
FriendsListLabel = 'Friends'
AvatarFriendsListLabel = 'Pirates'
AccountsFriendsListLabel = 'Players'
FriendsPageNewFriend = 'New Friend'
FriendsPageSecrets = 'Secrets'
FriendsPageOnlineFriends = 'ONLINE\nFRIENDS'
FriendsPageAllFriends = 'ALL\nFRIENDS'
FriendsPageIgnoredFriends = 'IGNORED\nPIRATES'
FriendsPagePets = 'NEARBY\nPETS'
FriendsPageOffline = '\x01slant\x01Offline\x02'
FriendsPageOnline = '\x01slant\x01Online\x02'
FriendsPageNameText = '%(avName)s [%(playerName)s]'
FriendsPageFriendText = '%(nameText)s\n%(presenceText)s'
FriendsPagePlayerName = '[%(playerName)s]'
AvatarChooserTitle = 'Choose Yer Pirate'
AvatarChooserCreate = 'Create A Pirate'
AvatarChooserUnderConstruction = 'Under Construction'
AvatarChooserSlotUnavailable = 'Unlimited Access Only'
AvatarChooserQuit = 'Quit'
AvatarChooserUpgrade = 'Upgrade'
AvatarChooserOptions = 'Options'
AvatarChooserPlay = 'Play'
AvatarChooserLoading = 'Loading'
AvatarChooserInQueue = 'Searching'
AvatarChooserDelete = 'Delete'
AvatarChooserShared = 'Share'
AvatarChooserLocked = 'Lock'
AvatarChooserLockedByOwner = 'Locked by Owner'
AvatarChooserAlreadyOnline = 'Already Online'
AvatarChooserConfirmDelete = 'Are you sure you want to delete %s?'
AvatarChooserConfirmShare = 'Share %s with all family member accounts?'
AvatarChooserConfirmLock = 'Lock out %s from all other family member accounts?'
AvatarChooserRejectPlayAvatar = 'Your request to play this pirate failed. Please reconnect and try again.'
OptionsPageLogout = 'Log Out'
AvatarChooserNameAccepted = 'Congratulations! Your pirate name was accepted.'
AvatarChooserPleaseRename = "We're sorry, your pirate name was not approved. Please enter a new name."
AvatarChooserNotDownload = 'Download is not yet complete.  Please wait until download is finished.'
AvatarChooserQueued = 'Searching for a free ocean, please try again in a moment...'
FirstAddTitle = 'Your 7 Day Full-Screen\nPreview Has Ended'
PreviewTitle1 = '7 Day'
PreviewTitle2 = 'Full Screen Preview'
FirstAddDisplay = 'You can continue to play in the current framed mode with free Basic Access or you can become a member and enjoy expanded features, including full-screen game play.'
FirstAddBasic = 'Continue Playing'
FirstAddUpgrade = 'Become A Member'
VR_FirstAddBasic = 'Continue Playing'
VR_FirstAddUpgrade = 'Become A Member'
MakeAPirateDone = 'Done'
MakeAPirateCancel = lCancel
MakeAPirateNext = lNext
MakeAPirateNextAnim = '>>'
MakeAPirateLastAnim = '<<'
MakeAPirateAllAnims = 'All Anims'
MakeAPirateWait = 'Please wait...'
MakeAPirateConfirm = 'Are you sure you are done making your pirate?'
SkipTutorialTitle = 'Pirate Tutorial'
SkipTutorialOffer = 'Follow Jack into the Tutorial and learn how to be a Pirate? If not, you can leave for Port Royal.'
SkipTutorialNo = 'Tutorial'
SkipTutorialYes = 'Skip'
AnimateFrame = 'Motion'
LODFrame = 'LOD'
LODSuperLow = 'S.Low'
LODLow = 'Low'
LODMed = 'Med'
LODHi = 'Hi'
RandomButton = 'Random'
ShuffleButton = 'Random All'
ShuffleNextButton = 'Next'
ShufflePrevButton = 'Last'
ResetButton = 'Reset'
DoneButton = 'Finished'
BodyShapeTab = 'Shape'
BodyHeightTab = 'Height'
BodyColorTab = 'Color'
BodyShapeTabTitle = 'Pick Body Shapes'
BodyHeightTabTitle = 'Adjust Body Height'
BodyColorTabTitle = 'Pick Skin Color'
GeneratePictures = 'Take Pics'
ClothingShirtTab = 'Shirt'
ClothingPantTab = 'Pants'
ClothingShoeTab = 'Shoe'
ClothingShirtTabTitle = 'Pick Shirts'
ClothingPantTabTitle = 'Pick Pants'
ClothingSockTabTitle = 'Pick Socks'
ClothingShoeTabTitle = 'Pick Shoes'
ShapeTab = 'Shape'
MouthTab = 'Mouth'
EyesTab = 'Eyes'
NoseTab = 'Nose'
EarTab = 'Ear'
ShapeTabTitle = 'Pick Shape'
MouthTabTitle = 'Pick Mouth'
EyesTabTitle = 'Pick Eyes'
NoseTabTitle = 'Pick Nose'
EarTabTitle = 'Pick Ear'
HairTabTitle = 'Pick Hair'
ClothesFrameTitle = 'Apparel'
ShirtFrameTitle = 'Top'
PantFrameTitle = 'Bottom'
ShoeFrameTitle = 'Shoe'
BodyShortFat = '1'
BodyMediumSkinny = '2'
BodyMediumIdeal = '3'
BodyTallPear = '4'
BodyTallMuscular = '5'
CastButton = 'CastButton'
SkeletonDJ1 = 'Crash'
SkeletonDJ2 = 'Jimmyleg'
SkeletonDJ3 = 'Koleniko'
SkeletonDJ4 = 'Palifico'
SkeletonDJ5 = 'Twins'
SkeletonGP1 = 'gp1'
SkeletonGP2 = 'gp2'
SkeletonGP4 = 'gp4'
SkeletonGP8 = 'gp8'
SkeletonSP1 = 'sp1'
SkeletonSP2 = 'sp2'
SkeletonSP3 = 'sp3'
SkeletonSP4 = 'sp4'
SkeletonFR1 = 'fr1'
SkeletonFR2 = 'fr2'
SkeletonFR3 = 'fr3'
SkeletonFR4 = 'fr4'
NPCShapeTab = 'Shape'
NPCHeadTab = 'Head'
NPCColorTab = 'Color'
NPCClothesTab = 'Clothes'
NPCShapeTabTitle = 'Pick NPC Shapes'
NPCHeadTabTitle = 'Adjust NPC Height'
NPCColorTabTitle = 'Pick Skin Color'
NPCClothesTabTitle = 'Pick Clothes'
NPCShapeFrameTitle = 'NPC Shape'
NPCHeadFrameTitle = 'Pick A Head'
NPCHeadFrame = 'Head'
NPCHead = 'Head'
NPCHeadScale = 'Size'
NPCColorFrameTitle = 'Skin Color'
NPCColorFrame = 'Skin Color'
NPCClothesFrameTitle = 'Clothes'
NPCShirtFrame = 'Shirt'
NPCVestFrame = 'Vest'
NPCCoatFrame = 'Coat'
NPCPantFrame = 'Pants'
NPCShoeFrame = 'Shoe'
NPCAccFrame = 'Acc'
NPCNext = '>>'
NPCLast = '<<'
MakeAPirateClothingHatStyle = 'Hat'
MakeAPirateClothingHatTrend = 'Pattern'
MakeAPirateClothingShirtStyle = 'Shirt'
MakeAPirateClothingShirtTrend = 'Pattern'
MakeAPirateClothingVestStyle = 'Vest'
MakeAPirateClothingVestTrend = 'Pattern'
MakeAPirateClothingCoatStyle = 'Coat'
MakeAPirateClothingCoatTrend = 'Pattern'
ClothingTopColorFrameTitle = 'Shirt Color'
ClothingTopColorTitle = 'Color'
MakeAPirateClothingPantStyle = 'Pants'
MakeAPirateClothingPantTrend = 'Pattern'
MakeAPirateClothingBeltStyle = 'Belt'
MakeAPirateClothingBeltTrend = 'Pattern'
ClothingBotColorFrameTitle = 'Pants Color'
ClothingBotColorFrame = 'Color'
MakeAPirateClothingSockStyle = 'Sock'
MakeAPirateClothingSockTrend = 'Pattern'
MakeAPirateClothingShoeStyle = 'Shoe'
MakeAPirateClothingShoeTrend = 'Pattern'
MakeAPirateCoatOff = 'Coat Off'
MakeAPirateCoatOn = 'Coat On'
TempNameIssued = 'Until your name is approved, you will be given a temporary name.'
RotateSlider = 'Rotate'
ZoomSlider = 'Zoom'
AnimSpeedSlider = 'Speed'
AvHPosSlider = 'H-Pos'
AvVPosSlider = 'V-Pos'
HatFrameTitle = 'Hat'
HatColorFrameTitle = 'Hat Color'
HatColorFrame = 'Color'
HairFrameTitle = 'Hair'
HairColorFrameTitle = 'Hair Color'
HairHighLightColorFrameTitle = 'Highlight Color'
MakeAPirateHairHair = 'Hair'
MakeAPirateHairBeard = 'Beard'
MakeAPirateHairMustache = 'Mustache'
MakeAPirateHairEyeBrow = 'Eyebrow'
MakeAPirateHairColor = 'Color'
MakeAPirateMale = 'Male'
MakeAPirateFemale = 'Female'
NameFrameTitle = 'Choose Your Name'
GenderFrameTitle = 'Gender'
BodyShapeFrameTitle = 'Shape'
BodyHeightFrameTitle = 'Height'
BodyHeight = 'Height'
BodyHeadScale = 'Shape'
BodyColorFrameTitle = 'Skin Tone'
BodyColorFrame = 'Skin Color'
NoseFrameTitle = 'Nose'
NoseBridgeWidth = 'Bridge Width'
NoseNostrilWidth = 'Nostril Width'
NoseLength = 'Length'
NoseBump = 'Bump'
NoseNostrilHeight = 'Nostril Height'
NoseNostrilAngle = 'Nostril Angle'
NoseBridgeBroke = 'Bridge Deform'
NoseNostrilBroke = 'Nostril Deform'
EarFrameTitle = 'Ears'
EarScale = 'Size'
EarFlapAngle = 'Angle'
EarPosition = 'Position'
EarLobe = 'Lobe'
BodyHairFrameTitle = 'Skin'
ShapeScaleFrameTitle = 'Size'
ShapeHeadFrameTitle = 'Head Shape'
ShapeTextureFrameTitle = 'Face'
ShapeTextureFrame = 'Style'
ShapeHeadWidth = 'Width'
ShapeHeadHeight = 'Height'
ShapeHeadRoundness = 'Roundness'
ShapeJewelryLEarFrameTitle = 'Ear Left'
ShapeJewelryREarFrameTitle = 'Ear Right'
ShapeJewelryLBrowFrameTitle = 'Brow Left'
ShapeJewelryRBrowFrameTitle = 'Brow Right'
ShapeJewelryNoseFrameTitle = 'Nose'
ShapeJewelryMouthFrameTitle = 'Mouth'
ShapeJewelryLHandFrameTitle = 'Hand Left'
ShapeJewelryRHandFrameTitle = 'Hand Right'
MouthJawFrameTitle = 'Jaw'
MouthFrameTitle = 'Lips'
MouthCheekFrameTitle = 'Cheeks'
MouthTeethFrameTitle = 'Teeth'
MouthTeethFrame = 'Teeth'
MouthJawWidth = 'Width'
MouthJawRoundness = 'Roundness'
MouthJawChinAngle = 'Chin Angle'
MouthJawChinSize = 'Chin Size'
MouthJawLength = 'Length'
MouthWidth = 'Width'
MouthThickness = 'Thickness'
MouthFrown = 'Frown'
CheekBoneWidth = 'Width'
CheekBoneHeight = 'Height'
CheekFat = 'Fat'
Teeth = 'Teeth'
EyeFrameTitle = 'Eyes'
EyeBrowFrameTitle = 'Brow'
EyeBrowWidth = 'Width'
EyeBrowProtruding = 'Protruding'
EyeBrowAngle = 'Angle'
EyeBrowHeight = 'Height'
EyeCorner = 'Corner'
EyeOpeningSize = 'Opening'
EyeBulge = 'Bulge'
EyeSpacing = 'Spacing'
EyeIrisColor = 'Eye Iris Color'
EyeBloodShot = 'Eye Blood Shot'
EyesColorFrameTitle = 'Eye Color'
EyesColorFrame = 'Color'
CreateYourPirateTitle = 'Create Your Pirate'
CreateYourPirateHead = "Click the 'head' arrows to pick different animals."
PirateButton = 'Pirate'
NPCButton = 'NPC'
NavyButton = 'Navy'
CastButton = 'Cast'
PickGender = 'Click the arrows to pick gender!'
PickBody = 'Click the arrows to pick body!'
PickHead = 'Click the arrows to pick head!'
PickClothes = 'Click the arrows to pick clothes!'
PickName = 'Choose a name for your pirate!'
MakeAPiratePageNames = [
    'Body', 'Head', 'Mouth', 'Eyes', 'Nose', 'Ear', 'Hair', 'Clothes', 'Name', 'Tattoos', 'Jewelry'
]
PaintYourPirate = 'Click the arrows to paint your pirate!'
PaintYourPirateTitle = 'Paint Your Pirate'
MakeAPirateYouCanGoBack = 'You can go back to change your body too!'
LootContainerOpen = 'Press Shift to open the %s!'
LootContainerWarning = 'Another pirate has laid claim to this plunder!'
LootContainerItemSac = 'Loot Pouch'
LootContainerTreasureChest = 'Loot Chest'
LootContainerRareChest = 'Loot Skull Chest'
LootContainerUpgradeChest = 'Ship Materials'
LootContainerRareUpgradeChest = 'Rare Ship Materials'
InventoryPageTitle = 'Inventory'
InventoryPageWeapons = 'Weapon Belt'
InventoryPageClothing = 'Garb'
InventoryPageJewelry = 'Jewelry & Tattoos'
InventoryPageAmmo = 'Ammo Pouch'
InventoryPageMaterial = 'Materials Pouch'
InventoryPagePotions = 'Potions Pouch'
InventoryPageCards = 'Cheat Cards'
InventoryPageTreasure = 'Treasure'
InventoryPageItemSlot = 'Item'
InventorySplitterTitle = 'How many?'
InventorySplitterConfirm = 'Ready!'
InventorySplitterAll = 'All'
InventorySplitterNone = 'None'
InventoryRedeemCode = 'Redeem Code'
InventoryFaceCamera = 'Face Camera'
InventoryRemoveDropTitle = 'Trash?'
InventoryRemoveDrop = 'Trash'
InventoryRemoveCancel = 'Keep'
InventorySellTitle = 'Sell Items'
InventorySell = 'Sell'
InventorySellMessage = 'Please drag items you want to sell into the box.'
InventorySellGoldCost = '\x01gold\x01Total Gold Value:\x02 %s'
InventorySellAmount = 'of %s'
InventorySellWarning = 'Please enter a valid amount of items!'
InventoryBuyTitle = 'Buy Item'
InventoryBuy = 'Buy'
InventoryBuyMessage = 'Buy this Item?'
InventoryBuyGoldCost = '\x01gold\x01Gold Value:\x02 %s'
InventoryBuyAmount = 'of %s'
InventoryBuyWarning = 'Please enter a valid amount of items!'
InventoryWear = 'Put it on'
InventoryPlunderTitle = 'Plundered %s!'
InventoryPlunderTakeAll = 'Take It All!'
InventoryPlunderTakeAllSundries = 'Take Small Items'
InventoryPlunderRating = 'Loot Rating:'
InventoryPlunderGiveNothingBack = '... And Give Nothing Back!'
InventoryPlunderPickSingular = 'Please select an item'
InventoryPlunderPickPlural = 'Please select %d items'
GoldName = 'Gold'
GoldDescription = 'Yarrr Gold'
InventoryCategoryNames = {
    InventoryCategory.BAD_CATEGORY: 'bad', InventoryCategory.MONEY: 'Money', InventoryCategory.CATEGORY: 'Locatable Items', InventoryCategory.WEAPONS: 'Weapons', InventoryCategory.INGREDIENTS: 'Voodoo Ingredients', InventoryCategory.CONSUMABLES: 'Consumables', InventoryCategory.SHIP_CANNONS: 'Ship Cannons', InventoryCategory.MAX_PLAYER_ATTRIBUTES: 'Max Player Attributes', InventoryCategory.TELEPORT_ACCESS: 'Teleport Access', InventoryCategory.WEAPON_SKILL_MELEE: 'Brawl Skill', InventoryCategory.WEAPON_SKILL_CUTLASS: 'Sword Skill', InventoryCategory.WEAPON_SKILL_PISTOL: 'Shooting Skill', InventoryCategory.WEAPON_SKILL_MUSKET: 'Musket Skill', InventoryCategory.WEAPON_SKILL_DAGGER: 'Dagger Skill', InventoryCategory.WEAPON_SKILL_GRENADE: 'Grenade Skill', InventoryCategory.WEAPON_SKILL_DOLL: 'Doll Skill', InventoryCategory.WEAPON_SKILL_WAND: 'Staff Skill', InventoryCategory.WEAPON_SKILL_KETTLE: 'Kettle Skill', InventoryCategory.WEAPON_SKILL_CANNON: 'Cannon Skill', InventoryCategory.UNSPENT_SKILL_POINTS: 'Unspent Skill Points', InventoryCategory.WEAPON_SKILL_ITEM: 'Weapon Skill', InventoryCategory.SKILL_SAILING: 'Sailing Skill', InventoryCategory.VITAE_PENALTY: 'Vitae Penalty', InventoryCategory.PLAYER_RANKING: 'Player Ranking', InventoryCategory.KEY_ITEMS: 'Key Items', InventoryCategory.QUEST_SLOTS: 'Quest Slots', InventoryCategory.ACCUMULATORS: 'Accumulators', InventoryCategory.REPAIR_TOKENS: 'Repair Tokens', InventoryCategory.WEAPON_PISTOL_AMMO: 'Gun Ammo', InventoryCategory.WEAPON_MUSKET_AMMO: 'Musket Ammo', InventoryCategory.WEAPON_GRENADE_AMMO: 'Grenade Ammo', InventoryCategory.WEAPON_CANNON_AMMO: 'Cannon Ammo', InventoryCategory.WEAPON_DAGGER_AMMO: 'Dagger Ammo', InventoryCategory.CARDS: 'Cards', InventoryCategory.CLOTHING: 'Clothing', InventoryCategory.PETS: 'Pets', InventoryCategory.FURNITURE: 'Furniture', InventoryCategory.SHIPS: 'Ships', InventoryCategory.SHIP_ACCESSORIES: 'Ship Accessories', InventoryCategory.FLAGS: 'Flags', InventoryCategory.COLLECTIONS: 'Collections', InventoryCategory.TELEPORT_TOKENS: 'Teleport Tokens', InventoryCategory.FISH_CAUGHT: 'Fish Caught', InventoryCategory.QUESTS: 'Quests', InventoryCategory.WAGERS: 'Wagers', InventoryCategory.TREASURE_MAPS: 'Treasure Maps', InventoryCategory.TRASH: 'trash'
}
BuffCorruption = 'CORRUPTION \n Bane damage over time \n'
BuffAcid = 'ACID \n Acid damage over time \n'
BuffToxin = 'TOXIN \n Toxic damage over time \n'
BuffPoison = 'VENOM \n Poison damage over time \n'
BuffWound = 'WOUNDED \n Health decay over time \n'
BuffHold = 'SNARE \n Locks victim movement \n'
BuffOnFire = 'BURN \n Fire damage over time \n'
BuffStun = 'STUN \n Cannot move or attack \n'
BuffUnstun = 'STUN IMMUNE \n Immune to Stun \n'
BuffVoodooStunLock = 'ATTUNEMENT LOCK \n Attunements cannot be broken \n'
BuffSlow = 'SLOW \n Slowed movement \n'
BuffBlind = 'BLIND \n Hindered sight \n'
BuffCurse = 'CURSED \n Increases damage taken \n'
BuffHasten = 'HASTEN \n Increases speed %d%% \n'
BuffTaunt = 'PROVOKED \n Accuracy lowered \n'
BuffWeaken = 'WEAKEN \n Decreased attack power! \n'
BuffSpawn = 'SPAWNING \n Temporary spawning invulnerability! \n'
BuffRegen = 'REGENERATION \n Regain lost health over time \n'
BuffAttune = 'ATTUNED \n A Voodoo Doll is attuned to you! \n'
BuffFullSail = 'FULL SAIL \n Full Speed Ahead! \n'
BuffComeAbout = 'COME ABOUT \n Ship Tacking Maneuver \n'
BuffOpenFire = 'OPEN FIRE \n Increases Cannon Damage \n'
BuffRam = 'RAMMING SPEED \n Ramming Maneuver \n'
BuffTakeCover = 'TAKE COVER \n Decreases Damage Take by Shipmates \n'
BuffPowerRecharge = 'LEADERSHIP \n Increases the rate of recharge for sailing skills and cannons \n'
BuffUnknownEffect = 'UNKNOWN \n This skill has no Buff Icon \n'
BuffReputation = 'REPUTATION BONUS \n Increases reputation gained %d%% \n'
BuffGold = 'GOLD BONUS \n Increases gold gained from land battles %d%% \n'
BuffCannonDamage = 'CANNON DAMAGE BONUS \n Increases cannon damage %d%% \n'
BuffPistolDamage = 'SHOOTING DAMAGE BONUS \n Increases shooting damage %d%% \n'
BuffCutlassDamage = 'SWORD DAMAGE BONUS \n Increases sword damage %d%% \n'
BuffDollDamage = 'DOLL DAMAGE BONUS \n Increases doll damage %d%% \n'
BuffBurp = 'BURP \n You are burping! \n'
BuffFart = 'FART \n You are farting! \n'
BuffFartLvl2 = 'FART \n You are farting! \n'
BuffVomit = 'VOMIT \n You are throwing up! \n'
BuffAccuracy = 'ACCURACY BONUS \n Increases accuracy %d%% \n'
BuffPotionRegen = 'BATTLE REGENERATION \n Regain %d%% health continuously \n'
BuffHeadFire = 'MYSTICAL FIRE \n A mystical blue fire burns on your head! \n'
BuffInvisibility = 'INVISIBILITY \n You disappear from sight. \n'
BuffHeadGrow = 'HEAD GROW \n Your head looks strangely large. \n'
BuffCrazySkinColor = 'CRAZY SKIN COLOR \n Your skin has turned a strange color!. \n'
BuffSizeReduce = 'SHRINK \n Decreases pirate size. \n'
BuffSizeIncrease = 'GROW \n Increases pirate size. \n'
BuffScorpionTransform = 'SCORPION TRANSFORMATION \n You become a giant scorpion! \n'
BuffAlligatorTransform = 'ALLIGATOR TRANSFORMATION \n You become a giant alligator! \n'
BuffCrabTransform = 'CRAB TRANSFORMATION \n You become a giant crab! \n'
BuffSummonChicken = 'SUMMON CHICKEN \n You attract a confused chicken. \n'
BuffSummonMonkey = 'SUMMON MONKEY \n You release a pet monkey. \n'
BuffSummonWasp = 'SUMMON WASP \n You tame a pet wasp. \n'
BuffSummonDog = 'SUMMON DOG \n You befriend a pet dog. \n'
BuffDuration = ' Duration: %s seconds'
BuffWreckHull = 'WRECK THE HULL \n Increases Hull Damage \n'
BuffWreckMasts = 'WRECK THE MASTS \n Increases Sail & Mast Damage \n'
BuffSinkHer = 'SINK HER \n Increases Broken Hull Panel Damage \n'
BuffIncoming = 'INCOMING \n Decreases Ship Damage and lowers the power of broadsides \n'
BuffKnockdown = 'KNOCKDOWN \n Cannot move or attack \n'
BuffDarkCurse = 'DARK CURSE \n Increases Combat and Projectile Defense \n'
BuffGhostForm = 'GHOST FORM \n Increases Combat and Projectile Defense \n'
BuffMastersRiposte = "MASTER'S RIPOSTE \n Increases Parrying \n"
BuffNotInFace = 'NOT IN THE FACE \n Avoids Contact \n'
BuffFixItNow = 'FIX IT NOW \n Increases Ship Repair effect \n'
BuffMonkeyPanic = 'MONKEY PANIC \n Increases attack power \n'
BuffQuickload = 'QUICK LOAD \n Allows shooting without reloading \n'
BuffVoodooReflect = 'VOODOO REFLECT \n Reflects enemy voodoo attacks \n'
BuffFury = 'FURY \n Increases combat and ranged attack damage \n'
BuffMeleeShield = 'MELEE SHIELD \n Protects from all incoming melee attack damage \n'
BuffMissileShield = 'MISSILE SHIELD \n Protects from all incoming ranged attack damage \n'
BuffMagicShield = 'MAGIC SHIELD \n Protects from all incoming magic attack damage \n'
BuffWarding = 'WARDING AURA \n Boosts Defense \n'
BuffNature = 'NATURE AURA \n Slowly Heals HP \n'
BuffDark = 'DARK AURA \n Boosts Attack \n'
CrewBuffCaptainOrder = "Captain's Orders:"
CrewBuffTakeCover = 'Shipmates immune\nto damage! Ship takes \n%s%% less damage!'
CrewBuffOpenFire = '+%s%% Damage Bonus for\nCannons & Broadsides!'
CrewBuffTakeCoverString = 'Take Cover!'
CrewBuffOpenFireString = 'Open Fire!'
DiceText_Wait = 'Waiting for Players'
DiceText_isTurn = "'s Turn"
DiceText_Wins = ' Wins'
DiceText_Roll = ' is Rolling'
DiceText_LowBet = 'You Must Exceed Prior Claim'
DiceText_Caught = '%s Caught Cheating'
DiceText_FirstClaim = 'You Must Make the First Claim'
DiceText_Call = '%s Calls Bluff'
DiceText_Ante = 'ANTE: '
DiceText_DiceUp_Chat = ['Higher than that', 'Up ye vermin!', 'Perhaps some more', 'Up we go']
DiceText_DiceUp_Size = len(DiceText_DiceUp_Chat) - 1
DiceText_DiceDown_Chat = ['Whoa, too high', 'Maybe a wee bit less', 'Not so much then']
DiceText_DiceDown_Size = len(DiceText_DiceDown_Chat) - 1
DiceText_Roll_Chat = ['Gimme a winner!', 'No tricks now you scamps!', 'Something good', "C'mon, show me the gold.", "Don't you be making me mad now"]
DiceText_Roll_Size = len(DiceText_Roll_Chat) - 1
Minigame_Repair_GenericBenchWarning = "You can't use this repair bench right now."
Minigame_Repair_UndeadWarning = "The Undead can't repair ships!"
Minigame_Repair_KickedFromBenchWarning = 'You have been temporarily banned from this bench!'
Minigame_Repair_KickedFromRepairSpotWarning = 'You have been temporarily banned from repairing this ship!'
Minigame_Repair_Names = {
    'repair': 'Ship Repair',
    'careening': 'Hull Scrubbing',
    'pumping': 'Bilge Pumping',
    'sawing': 'Plank Sawing',
    'bracing': 'Hull Bracing',
    'hammering': 'Hammering',
    'pitching': 'Hull Patching'
}
Minigame_Repair_Table_Text_Easy = 'Apprentice'
Minigame_Repair_Table_Text_Medium = 'Journeyman'
Minigame_Repair_Table_Text_Hard = 'Master'
Minigame_Repair_Table_Interact_Text_Easy = 'Easy Difficulty'
Minigame_Repair_Table_Interact_Text_Medium = 'Normal Difficulty'
Minigame_Repair_Table_Interact_Text_Hard = 'Hard Difficulty'
Minigame_Repair_Speed_Thresholds = (
    '\x01Igreen\x01Lightning Fast!\x02', 'Quick Work!', '\x01Iyellow\x01Pick Up The Pace!\x02', '\x01Ired\x01Faster, Landlubber!\x02')
Minigame_Repair_Level = 'Level: %s'
Minigame_Repair_Leave_Game_Text = ('Exit', )
Minigame_Repair_Win = 'You Win!'
Minigame_Repair_Pick_New_Game = 'Choose Another Game'
Minigame_Repair_Waiting_For_Players = 'Waiting for other players...'
Minigame_Repair_Countdown_3 = '3'
Minigame_Repair_Countdown_2 = '2'
Minigame_Repair_Countdown_1 = '1'
Minigame_Repair_Countdown_Ready = 'Ready!'
Minigame_Repair_Default_Start = 'Go!'
Minigame_Repair_Careening_Start = 'Scrub!'
Minigame_Repair_Careening_Power = 'Power'
Minigame_Repair_Pumping_Start = 'Pump!'
Minigame_Repair_Sawing_Start = 'Saw!'
Minigame_Repair_Bracing_Start = 'Brace!'
Minigame_Repair_Hammering_Start = 'Hammer!'
Minigame_Repair_Pitching_Start = 'Patch!'
Minigame_Repair_Pumping_Fail = 'Miss!'
Minigame_Repair_Pumping_Great = 'Great!'
Minigame_Repair_Hammering_Thresholds = ('Terrible', 'OK', 'Good', 'Great', 'Perfect')
Minigame_Repair_Sawing_Thresholds = (
    'Terrible!', 'OK', 'Great', 'Perfect!')
Minigame_Repair_Sawing_Description = 'Your sawing is:'
Minigame_Repair_Sawing_Board_Destroyed = 'Board destroyed!'
Minigame_Tutorials = {
    'repair': '',
    'pumping': 'Click when the bar is \nin the green to pump!',
    'careening': 'Keep moving your mouse over\nthe barnacles to scrub!\nClick for power! Release to recharge.',
    'sawing': 'Pick up the saw and\ncut along the black line!',
    'bracing': ['Move the pieces to form\na straight line!', 'Move the pieces to form\ntwo straight lines!'],
    'hammering': 'Hit the nails when the circle\nis the smallest!',
    'pitching': 'Click to plug all of the leaks!'
}
Minigame_Repair_ShipIntro = 'Click on a game icon below\nto repair your ship!'
Minigame_Repair_BenchIntro = 'Click on a game icon below\nto start repairing ships.\n\nThe more ships you repair\nthe more gold you earn!'
Minigame_Repair_ShipOutro = 'Great job, ship repaired!'
Minigame_Repair_BenchOutro = 'You fixed a ship!\n\nCompletion time: %s\nYou earned: %s'
Minigame_Repair_Minutes = 'minutes'
Minigame_Repair_Seconds = 'seconds'
Minigame_Repair_Gold = '\x01gold\x01%s gold\x02'
Minigame_Repair_GoldBonus = '\x01gold\x01%s gold\x02 \x01CPGreen\x01(+%s Holiday Bonus)\x02'
Second = 'second'
Seconds = 'seconds'
Minute = 'minute'
Minutes = 'minutes'
Hour = 'hour'
Hours = 'Hours'
from pirates.ship.ShipGlobals import Logos as ShipLogos
ShipLogoNames = {
    ShipLogos.Navy: 'OLD: navy skull', ShipLogos.BlackPearl: 'OLD: BP logo', ShipLogos.EITC: 'OLD: EITC', ShipLogos.EITC_Emblem: 'OLD: logo_eitc_emblem', ShipLogos.PVP_French: 'OLD: logo_french_flag', ShipLogos.PVP_Spanish: 'OLD: logo_spanish_flag', ShipLogos.Bandit_Bull: 'BANDIT: BULL', ShipLogos.Bandit_Dagger: 'BANDIT: DAGGER', ShipLogos.Bandit_Scorpion: 'BANDIT: SCORPION', ShipLogos.Bandit_Claw: 'BANDIT: CLAW', ShipGlobals.Logos.Player_Hawk: 'PIRATE: HAWK', ShipGlobals.Logos.Player_Rose: 'PIRATE: ROSE', ShipGlobals.Logos.Player_Flame: 'PIRATE: FLAME', ShipGlobals.Logos.Player_SpanishBull: 'PIRATE: BULL', ShipGlobals.Logos.Player_Wolf: 'PIRATE: WOLF', ShipGlobals.Logos.Player_Angel: 'PIRATE: ANGEL', ShipGlobals.Logos.Player_Dragon: 'PIRATE: DRAGON', ShipGlobals.Logos.Player_Shield: 'PIRATE: SHIELD', ShipGlobals.Logos.Player_Heart: 'PIRATE: HEART', ShipLogos.Treasure_Navy: 'NAVY TREASURE', ShipLogos.Treasure_EITC: 'EITC TREASURE', ShipLogos.QueenAnnesRevenge: 'OLD: BP logo'
}
ShipStyleNames = {
    ShipGlobals.Styles.Player: 'PLAYER', ShipGlobals.Styles.Navy: 'NAVY', ShipGlobals.Styles.EITC: 'EITC', ShipGlobals.Styles.Undead: 'UNDEAD', ShipGlobals.Styles.BP: 'BLACK PEARL', ShipGlobals.Styles.Treasure_Navy: 'NAVY TREASURE', ShipGlobals.Styles.Treasure_EITC: 'EITC TREASURE', ShipGlobals.Styles.Bandit01: 'RED BANDIT', ShipGlobals.Styles.Bandit02: 'GREEN BANDIT', ShipGlobals.Styles.Bandit03: 'BLUE BANDIT', ShipGlobals.Styles.Bandit04: 'SUPER BANDIT', ShipGlobals.Styles.QueenAnnesRevenge: 'QUEEN ANNES REVENGE', ShipGlobals.Styles.BountyHunter_A: 'BOUNTY HUNTER A', ShipGlobals.Styles.BountyHunter_B: 'BOUNTY HUNTER B', ShipGlobals.Styles.BountyHunter_C: 'BOUNTY HUNTER C', ShipGlobals.Styles.BountyHunter_D: 'BOUNTY HUNTER D', ShipGlobals.Styles.BountyHunter_E: 'BOUNTY HUNTER E', ShipGlobals.Styles.BountyHunter_F: 'BOUNTY HUNTER F', ShipGlobals.Styles.BountyHunter_G: 'BOUNTY HUNTER G', ShipGlobals.Styles.NavyHunter: 'NAVY HUNTER'
}
Minigame_Fishing_Boat = 'Fishing Boat'
Minigame_Fishing_New_Rod = 'Upgraded!'
Minigame_Fishing_Lure_Alerts = {
    'snap': 'Lure Stolen!',
    'click': 'Click!',
    'perfect': 'Perfect!',
    'toolate': 'Too late...',
    'clickhold': 'Click and Hold!',
    'letgo': "Don't Click!",
    'scaredOff': 'Scared Off',
    'eaten': 'Lure eaten!'
}
Minigame_Fishing_Tutorials = {
    'rodReceived': 'Received Fishing Rod\nand Lures!',
    'rodReceivedChatMessage': 'You now have a fishing rod and lures!',
    'launchFishingBoat': 'Congratulations!\n  At fishing reputation level 10 you can launch a fishing boat and go deep see fishing!\n  Talk to the fishmaster.',
    'legendaryFishShow': 'You have encountered a Legendary Fish!',
    'legendaryFishReelingFish': 'Move the mouse in a clockwise circle to reel in the fish!',
    'legendaryFishStruggle': 'Click rapidly to win a struggle with the Legendary Fish!',
    'legendaryFishHandleBreak': 'Click on the handle to stop the Legendary Fish from fleeing'
}
Minigame_Fishing_Level_Unlocks = {
    2: 'You have improved your Reel speed!',
    3: 'You can now use the Stall ability to pause your lure in the water!',
    4: 'You can now use the Pull ability to give a burst of speed while fighting a fish!',
    5: 'You can now upgrade to a Journeyman rod at the fishmaster!',
    6: 'You can now use the Heal Line ability to restore lost health to your line!',
    7: 'You have improved your Reel speed!',
    8: 'You can now use the Stall II ability to pause your lure in the water longer!',
    9: 'You can now use the Pull II ability to give a bigger burst of speed while fighting a fish!',
    10: 'You can now use the Fishing Boat available at the fishmaster!',
    11: 'You have improved your Reel speed!',
    12: 'You can now use the Heal Line II ability to restore lost health to your line!',
    13: "You can now use the Tug ability to stop a fish while it's fighting!",
    14: 'You have improved your Reel speed!',
    15: 'You can now upgrade to a Master Rod at the fishmaster!',
    16: 'You can now use the Sink ability to make your lure fall faster in the water!',
    17: 'You can now use the Ocean Eye ability to see the entire ocean!',
    18: 'You have improved your Reel speed!',
    19: 'You can now use Heal III and Pull III abilities!',
    20: 'You have unlocked the Legendary Lure! Start the hunt for Legendary Fish!'
}
FishingGui = {
    'ExitButton': 'Exit',
    'ExitTitle': 'Exit Fishing',
    'ExitText': 'Do you want to stop fishing?',
    'WinTitle': 'Congratulations!',
    'WinText': 'You caught a',
    'GoldText': 'Gold',
    'XPLabel': 'Rep',
    'XPBonusLabel': '(+%s Holiday Bonus)',
    'GoldBonusLabel': '(+%s Holiday Bonus)',
    'PlayAgainButton': 'OK',
    'StopButton': 'Exit',
    'XPEarned': 'Reputation Earned',
    'LevelUp': 'Level Up!',
    'WeightLabel': 'lbs',
    'ChooseYourLure': 'Choose your lure.',
    'RegularLures': 'Regular Lures',
    'Lures': 'Lures',
    'LegendaryLures': 'Legendary Lures',
    'AreYouSure': 'Are you sure you want to exit?'
}
LegendSelectionGui = {
    'panelTitle': 'Legendary Fish',
    'legendIntro': "So you want to hear about some of the most mysterious beasts of the seas, eh? Just tell me which one of em'...I've seen them all, I swear it! Or...well, I thought I saw one once.\n\nYou may see one too, if you cast your line deep, as deep as you can...",
    'shortStory': {
        InventoryType.Collection_Set11_Part1: {
            LocationIds.PORT_ROYAL_ISLAND: "\n  Ya know that feelin' ya get when the fog gets thick and the world is a grey haze, somewhere between life and death, the ocean and the rocks that may be only a few feet away? That's where Fogbell dwells. Some call him a shark, I call him a devil. Somewhere off the coast, there's a predator so vicious, so diabolical, so evil that when the fog rolls in the mariners head home. \n  It's hard to get a description of a creature that lurks in the mist but I've heard tell of a beast with red eyes. Glowing red eyes that penetrate the fog and cut to a man's soul. Its jaws are so massive, they can tear a ship in two in one terrifying bite. His strength is unmatched - it would take a trick or two to bring in this devil. \n  Just remember, when you hear the fog bells, get to port quick, or ye'll be starin' into two glowing red eyes for what remains of your time on earth. \n", LocationIds.TORTUGA_ISLAND: "\n  Aye, I've heard o' Fogbell. I'll tell ye of a time when the night was comin' on and I may have had a bit too much grog in me gullet. Well, I took the rowboat out, the moon was bright and the fog came a rollin' in. Like a thick blanket, it was. Enough to make a fella wanna take a nap. So I did.\n  I woke well enough but noticed the boat was rockin back and forth. I steadied me little rowboat and looked over the side and was starin' straight into the red eyes of a fish so hideous, I thought me ugly ol' Aunt Mertyl looked an angel. It jumped from the water and came toward me. \n  Bein' the buccaneer I am, I drew me rapier and we had ourselves a sword duel, right there on the rowboat. We fought on through the night until it gave up in defeat. One thing I know for sure - once that beast sees you with its red eyes, you better be ready for a fight of yer life or for a long dive to the bottom o' the waves.\n", LocationIds.DEL_FUEGO_ISLAND: "\n  I've got a tale to spin that will make your heart race and your stomach turn. It was a foggy night, the clouds seemed to leave the heavens and visit the calm surface of our blessed ocean. The mist lingered there, like a thing alive, waiting to be disturbed. \n  Our boat, the San Marquis, was splitting the fog in search of the Black Pearl. Then, in the middle of the mist, our boat lost its wind, as though the world itself was holding its breath. As we waited, we watched as the mist was cut in half, it parted like a sword through silk and next thing we knew, our boat was splitting along with it. The only thing I seen was two red eyes, right before our boat shattered into a million pieces. I swam to shore and I swear, I could feel that monster right behind me the whole way. For two days I swam, I never would have made it but I knew what would happen if I stopped. \n  Good luck catching that beast. I wouldn't enter the fog again if you promised me the Black Pearl herself. \n"
        }, InventoryType.Collection_Set11_Part2: {
            LocationIds.PORT_ROYAL_ISLAND: "\n  There's a legend about the creation of the sea, when the earth was still dry and arid. The fire god was angry with the water, furious that it was infringing on much of the land. In revenge, he made volcanoes. The water goddess was angered that the fire god would create such a destructive force out of spite so in turn, she made sharks. The shark made people afraid to go into the water, which made the water goddess sad, and the volcanoes made people scared to stay on land, which made the fire god sad. So they made a pact. The water goddess gave the fire god small islands where he could put his volcanoes so no one would be hurt. The fire god, deceitful and dangerous as the element he claimed, put something in the water more terrifying than any shark could ever be. \n  The Fire Dragon is the big one all the fishermen talk about.\n", LocationIds.TORTUGA_ISLAND: "\n  All jokes aside, mate, this beast is not to be trifled with. Padres del Fuego spawns many a fiery menace from its mouth but legend has it that on one particularly violent eruption, it spewed forth a dragon from the depths of the world, spitting out a beast so dangerous, the sea had to swallow it to keep it from destroying the world. \n  Is there truth in any of it? I wouldn't know but I wouldn't chance it. Ships disappear off the coast of that island all the time, usually burned and charred. How does a fire dragon live in the water? Maybe it's just that powerful. Whatever the reason, it has a hunger and the means to fill it. If you're fishing out that way, stay away from the hot vents in the water. Word is it lurks in warm water and enjoys the feel of the molten rocks beneath its belly.  \n  He only comes out at the twilight hour - some call it the devil's hour. \n", LocationIds.DEL_FUEGO_ISLAND: "\n  No. No, I will not speak of it. Fuego del Diablo. That's all I can say. \n"
        }, InventoryType.Collection_Set11_Part3: {
            LocationIds.PORT_ROYAL_ISLAND: "\n  Nowhere is the power of voodoo more apparent than in the legend of Amelia Stonehallow, the Werefish. Sea dogs the Caribbean over have seen with their own eyes the transformation that takes place on night of a full moon. \n  A woman, dressed in a white flowing gown, approaches the beach, climbing her way through the rocks and stands in the surge of waves crashing against the shoreline. Then, all of a sudden, the woman is gone and the most beautiful and lovely fish ye ever did see swims off into the blue. \n  Some say she is looking for another of her kind, some kindred spirit she can connect with. How ol' Amelia got the way she is, no one knows, but I'll tell ye, once you see the Glittering Girl, all other beauty will pale in comparison. \n", LocationIds.TORTUGA_ISLAND: "\n  It's hard to say any fish is beautiful, especially after me guppy bit me on me nose when I was a wee lad. But, I'll tell ye, I seen the Glitterin' Girl and there is nothing in this world more beautiful.\n  She's a smart one too, oh yes, quick as a fox, she is. I was stranded one time, I was. A barren island with nought but sand to eat and the sea to drink. Then she appeared. She saved me, she did. Showed me the way back to shore. When I got back, I hugged me wife and child, but then the fish was gone. Next day, a woman in a white gown, pure as snow and precious as silver, was in front of me hut. I went out to see what she was about and when I opened me door, she was gone. \n  I'll tell ye mate, if you catch the Glitterin' Girl, make sure ye thank her for me.\n", LocationIds.DEL_FUEGO_ISLAND: "\n  There are some tales that can make a pirate cry, lost treasures, captured buckos, and this one. Amelia Stonehallow was born right here, on the Fiery Island. Her young love, he was a pale boy, but a nice lad all the same. One day, feeble as he was, he came down with a sickness the likes o' which we'd not seen here. Amelia sat next to him for weeks 'til she could take it no more. She vowed to find a cure and sailed off for the voodoo lady, Tia Dalma, in Cuba. \n  Legend says what Amelia found there was none to her liking. The voodoo magic there turned her into a fish at night, allowing her the opportunity to rescue lost sailors in exchange for her lover's life. \n  Some would say, though her lover is gone, she still tries to help sailors all over the sea. \n"
        }, InventoryType.Collection_Set11_Part4: {
            LocationIds.PORT_ROYAL_ISLAND: "\n  I don't know why everyone is on about Mossy Moses all the time. He's a right fella by me. Sleeps for months at a time, only wakes up to eat, I can appreciate a mentality like that! \n  Besides, the whale of a fish is darn handsome. I seen him once, yessir, I did. I thought he was an island at first. I checked me map and didn't see any land where he was, but there was some land, green moss, even a treasure chest right there on his back! I tried to dock, but every time I did, the island would move.\n  After a bit, he came all the way up outta the water and looked me in the eye. I was hollerin' and makin' a racket, tryin' to scare him off. After all, I was frightened. Then, he kinda smiled at me and swam away. I like that big ol' lug. He's just tryin' to make his way in the world and doin' a fine job of it by my book!\n", LocationIds.TORTUGA_ISLAND: "\n  I been tryin' to catch Mossy Moses me entire life! Not once have I seen 'em, not even once! That blubbering excuse for a whale is so lazy, it don't even have the common courtesy to come up and bite the line. I'm sick of it. Forty years I been at it. I been fishin' south, all the way south and not once have I ever seen 'em. Maybe I been fishin' in the wrong spot ... or maybe it's just too tired to get up and do somethin'!\n", LocationIds.DEL_FUEGO_ISLAND: "\n  Most pirates catch twenty winks if they can between the morning swab and the midnight round of rum. Mossy Moses is a different story, to be sure. This big lug lounges around all day at the bottom of the murky depths, snorin' loud enough to wake the dead in Davy Jones' locker. He only comes up on that rare occasion that calls for him to eat. \n  Legend has it that Mossy Moses has become one with the ocean's floor. He's covered in all kind of plants and reef bits. He sleeps for years, they say - only arousin' when he has a hankerin' for some plankton. It's easy to accumulate a number of ocean oddities on your back when you lie still for all seasons. \n  The hard part ain't catching this lumberin' hulk of a whale; it's getting him to stay awake long enough to have 'em bite the line.\n"
        }, InventoryType.Collection_Set11_Part5: {
            LocationIds.PORT_ROYAL_ISLAND: "\n  The way I remember the story, Limpin' Lou was a cripple, got in a bad cannon accident back when he was a lad and never walked again. He dreamed of runnin' as fast as the Interceptor, fastest ship on the sea, ya know.  Anyway, Limpin' Lou just hung around the docks, watchin' the Interceptor pull out to sea, knowin' he was never gonna get on it, then he saw it. A fish, faster than the Interceptor, it outran the waves themselves. Limpin' Lou knew what he had to do. \n  He waded out into the waves and called for the fish. It appeared and he made a deal with it. The deal was, if he could ride around in its belly, Lou would speak for the fish and together, they could setup the grandest race a pirate had ever seen. One fish against the fastest ship humans had to offer, the Interceptor. To this day, that race ain't happened, but I'm sure Speedy Lou is workin' on it, even as we speak.\n", LocationIds.TORTUGA_ISLAND: "\n  It's within man's nature to want to best Mother Nature at her own game. So when a pirate named Speedy Lou heard about a prehistoric fish so fast that no man could catch it, he went about the task of training his mind and body to beat it in a swimming race. For two years he trained and then waded out into the water near Tortuga and yelled for the fish. \n  The fish showed up, alright. It ate Speedy Lou and swam off without a second thought. In honor of his dedication to this race, we named the fish Speedy Lou and believe he's still in its gullet, slowing it down somewhat, Lou's revenge on Mother Nature. \n", LocationIds.DEL_FUEGO_ISLAND: "\n  We don't got many fast land creatures in the Caribbean, there ain't much space to run. It's in the ocean that the true speed happens. And the fastest there is, Speedy Lou, rules that domain. That fish is a happy fellow, I can tell you that much. He always loves a good race, known to keep pace with ships, challenging them to go faster. \n  There's something liberatin' about goin' fast, eh? Some kind of freedom, like not even the air could catch you if ye could just go fast enough. That's what bein' a pirate is all about, freedom. So in a way, Speedy Lou is the pirate of fish, the one sea creature who truly understands what it means to be free. Any pirate who don't feel a kindred spirit with Speedy Lou don't really know what it means to be aboard a vessel.\n"
        }
    },
    'wholeStory': {
        InventoryType.Collection_Set11_Part1: "\n  What makes the savage beast? Is it in the nature of the fish or the nature of the waves? Perhaps, a fish so horrifying is nothing more than a product of its environment. Maybe it serves a purpose no pirate will ever understand. Perhaps Fogbell is not a terror but a protector. After all, the sea is a dangerous place, peril below every wave, hazards at every shore. Keeping a pirate on his toes in the fog may have saved many a ship from sharp rocks hidden below the mist. Fogbell is just a fish ... but maybe it's a fish with a purpose.\n  You release Fogbell back into the sea and watch as it swims away - but you keep a scale to sell to the highest bidder. You are a pirate, after all.\n", InventoryType.Collection_Set11_Part2: "\n  There is little in the world that can match staring, eye to eye, with a creature so ancient, it still has dust on its skin from the creation of the world. Staring at the Fire Dragon feels like being a part of something grander than being a pirate, grander than the ocean upon which the pirate sails. Legends are never meant to be imprisoned, they are meant to be shared, experienced through song and tale, for everyone. \n  Where did The Fire Dragon come from? None can really say for sure ... but isn't that what makes it a legend? By seeing the Fire Dragon, you will keep it alive forever. \n  You release the beast into the sea and watch it leave, knowing that soon, you will tell this story to all your friends at the tavern. But before it goes, you take a scale to sell back on shore. You are a pirate, after all. \n", InventoryType.Collection_Set11_Part3: "\n  The ocean watches out for her own. Sometimes the way in which this happens is mysterious and odd. Pirates and sailors, swimmers and fishermen, they all must respect the sea and the perils they face. As you look into the eyes of the fish they call the Glittering Girl, you can see that she is just another one of the sea's many companions. All the stories about how she saves the stranded, the lost, and forsaken, you can see it in her eyes. Was she once a woman, searching for a cure for her lost love? There seems to be no indication here but stranger things have happened. \n  As you release her back into the sea, you wave a fond farewell and good luck. Who knows, maybe someday you'll see her again when you need the help of the ocean, when all hope seems lost. You run your hands across the scale you took from her before she went and smile, thinking about the price it will run up at the market. You are a pirate, after all.\n", InventoryType.Collection_Set11_Part4: "\n  The strain of holding Mossy Moses on the line is enough to make you fall overboard. Never have you seen a fish so large and yet so goofy. You get tickled just looking at the awkward smile and toothy grin on its face. It makes you realize that even a legend can relax and enjoy the sea. \n  So often, pirating can be all about the plunder, the treasures, the new ships and sharp weapons.  You can see all these things amassed on Mossy Moses's back and it doesn't even care. It has more treasure stuck to its back than any pirate will see in a lifetime and all it does is sleep and enjoy its life. That's a lesson, to be sure. \n  You have little choice but to let Mossy Moses fall back into the sea, your boat couldn't have handled his girth anyway. But you be sure to take a scale from the big guy, it will catch a hefty sum on the main land. You are a pirate, after all.\n", InventoryType.Collection_Set11_Part5: '\n  The freedom of the ocean is as legendary as the fish hanging at the end of your line. As any great pirate will tell you, being free to adventure and explore the world is what being a buccaneer is all about. As you stare into the eye of Speedy Lou, you can tell, he would agree. How can you keep such a majestic fish from keeping the spirit of freedom alive on the high seas? You can only hope you gave the fish the kind of adventure it lived for.\n  As you let Speedy Lou off the line and it swims off into the blue, you swear you hear a muffled voice yell "Thanks for the race!" But that couldn\'t be right, fish don\'t talk. You flip the scale from Speedy Lou in your hand and wonder how much it will go for back on the main land. Fish stories are great but gold is gold. You are a pirate, after all.\n'
    }
}
LegendaryFishingGui = {
    'Struggle': ['Struggle!', 'Click as fast as you can!'],
    'ReelingFish': ['Reel!', 'Move your mouse in a circle!'],
    'CatchIt': ['Catch It!', 'Click on the handle!']
}
ShipClassNames = {
    ShipGlobals.WARSHIPL1: 'Light Frigate', ShipGlobals.WARSHIPL2: 'Frigate', ShipGlobals.WARSHIPL3: 'War Frigate', ShipGlobals.MERCHANTL1: 'Light Galleon', ShipGlobals.MERCHANTL2: 'Galleon', ShipGlobals.MERCHANTL3: 'War Galleon', ShipGlobals.INTERCEPTORL1: 'Light Sloop', ShipGlobals.INTERCEPTORL2: 'Sloop', ShipGlobals.INTERCEPTORL3: 'War Sloop', ShipGlobals.BRIGL1: 'Light Brig', ShipGlobals.BRIGL2: 'Brig', ShipGlobals.BRIGL3: 'War Brig', ShipGlobals.SHIP_OF_THE_LINE: 'Ship of the Line', ShipGlobals.HMS_VICTORY: 'HMS Victory', ShipGlobals.HMS_NEWCASTLE: 'HMS Newcastle', ShipGlobals.HMS_INVINCIBLE: 'HMS Invincible', ShipGlobals.EITC_INTREPID: 'EITC Intrepid', ShipGlobals.EITC_CONQUERER: 'EITC Conqueror', ShipGlobals.EITC_LEVIATHAN: 'EITC Leviathan', ShipGlobals.GOLIATH: 'Goliath', ShipGlobals.HUNTER_VENGEANCE: 'Vengeance', ShipGlobals.HUNTER_CUTTER_SHARK: 'Cutter Shark', ShipGlobals.HUNTER_FLYING_STORM: 'Flying Storm', ShipGlobals.HUNTER_KILLYADED: 'Killyaded', ShipGlobals.HUNTER_RED_DERVISH: 'Red Dervish', ShipGlobals.HUNTER_CENTURY_HAWK: 'Century Hawk', ShipGlobals.HUNTER_SCORNED_SIREN: 'Scorned Siren', ShipGlobals.HUNTER_TALLYHO: 'Tally-ho', ShipGlobals.HUNTER_BATTLEROYALE: 'Battle-Royale', ShipGlobals.HUNTER_EN_GARDE: 'En-Garde', ShipGlobals.EL_PATRONS_SHIP: 'El Patrons Ship', ShipGlobals.P_SKEL_PHANTOM: 'Phantom', ShipGlobals.P_SKEL_REVENANT: 'Revenant', ShipGlobals.P_SKEL_CEREBUS: 'Cerberus', ShipGlobals.P_NAVY_KINGFISHER: 'Kingfisher', ShipGlobals.P_EITC_WARLORD: 'Warlord', ShipGlobals.NAVY_KRAKEN_HUNTER: 'Navy Kraken Hunter', 'AnyLargeShip': 'Galleon or Frigate', 'AnyWarShip': 'Frigate', 'AnyL7PlusShip': 'Level 7+ ship', 'AnyL7PlusNavyShip': 'Level 7+ Navy ship', 'AnyL9PlusShip': 'Level 9+ ship', 'AnyL9PlusNavyShip': 'Level 9+ Navy ship', 'AnyL13PlusShip': 'Level 13+ ship', 'AnyL13PlusNavyShip': 'Level 13+ Navy ship', 'AnyEITCSeaViper': 'Sea Viper', 'AnyEITCMarauder': 'Marauder', 'AnyEITCBarracuda': 'Barracuda', 'AnyEITCCorvette': 'Corvette', 'AnyFrenchShadowCrow': 'French Shadow Crow', 'AnyFrenchHellhound': 'French Cerberus', 'AnyFrenchBloodScourge': 'French Blood Scourge', 'AnySpanishShadowCrow': 'Spanish Shadow Crow', 'AnySpanishHellhound': 'Spanish Cerberus', 'AnySpanishBloodScourge': 'Spanish Blood Scourge', 'AnyCerberus': 'French or Spanish Cerberus', ShipGlobals.SKEL_WARSHIPL3: 'War Frigate', ShipGlobals.SKEL_INTERCEPTORL3: 'War Sloop', ShipGlobals.QUEEN_ANNES_REVENGE: 'Legendary Ship', ShipGlobals.BLACK_PEARL: 'Legendary Ship', ShipGlobals.FLYING_DUTCHMAN: 'Legendary Ship', ShipGlobals.STUMPY_SHIP: 'Light Sloop', ShipGlobals.GOLIATH: 'The Goliath', ShipGlobals.JOLLY_ROGER: 'Legendary Ship', ShipGlobals.NAVY_FERRET: 'Navy Ferret', ShipGlobals.NAVY_GREYHOUND: 'Navy Greyhound', ShipGlobals.NAVY_KINGFISHER: 'Navy Kingfisher', ShipGlobals.NAVY_PREDATOR: 'Navy Predator', ShipGlobals.NAVY_BULWARK: 'Navy Bulwark', ShipGlobals.NAVY_VANGUARD: 'Navy Vanguard', ShipGlobals.NAVY_MONARCH: 'Navy Monarch', ShipGlobals.NAVY_COLOSSUS: 'Navy Colossus', ShipGlobals.NAVY_PANTHER: 'Navy Panther', ShipGlobals.NAVY_CENTURION: 'Navy Centurion', ShipGlobals.NAVY_MAN_O_WAR: 'Navy Man-O-War', ShipGlobals.NAVY_DREADNOUGHT: 'Navy Dreadnought', ShipGlobals.NAVY_BASTION: 'Navy Bastion', ShipGlobals.NAVY_ELITE: 'Navy Elite', ShipGlobals.EITC_SEA_VIPER: 'EITC Sea Viper', ShipGlobals.EITC_BLOODHOUND: 'EITC Bloodhound', ShipGlobals.EITC_BARRACUDA: 'EITC Barracuda', ShipGlobals.EITC_CORSAIR: 'EITC Corsair', ShipGlobals.EITC_SENTINEL: 'EITC Sentinel', ShipGlobals.EITC_IRONWALL: 'EITC Ironwall', ShipGlobals.EITC_OGRE: 'EITC Ogre', ShipGlobals.EITC_BEHEMOTH: 'EITC Behemoth', ShipGlobals.EITC_CORVETTE: 'EITC Corvette', ShipGlobals.EITC_MARAUDER: 'EITC Marauder', ShipGlobals.EITC_WARLORD: 'EITC Warlord', ShipGlobals.EITC_JUGGERNAUT: 'EITC Juggernaut', ShipGlobals.EITC_TYRANT: 'EITC Tyrant', ShipGlobals.SKEL_PHANTOM: 'Phantom', ShipGlobals.SKEL_REVENANT: 'Revenant', ShipGlobals.SKEL_STORM_REAPER: 'Storm Reaper', ShipGlobals.SKEL_BLACK_HARBINGER: 'Black Harbinger', ShipGlobals.SKEL_DEATH_OMEN: 'Death Omen', ShipGlobals.SKEL_SHADOW_CROW_FR: 'French Shadow Crow', ShipGlobals.SKEL_HELLHOUND_FR: 'French Cerberus', ShipGlobals.SKEL_BLOOD_SCOURGE_FR: 'French Blood Scourge', ShipGlobals.SKEL_SHADOW_CROW_SP: 'Spanish Shadow Crow', ShipGlobals.SKEL_HELLHOUND_SP: 'Spanish Cerberus', ShipGlobals.SKEL_BLOOD_SCOURGE_SP: 'Spanish Blood Scourge'
}
WeaponTypeNames = {
    InventoryType.PistolRep: 'Gun'
}
InventoryTypeNames = {
    InventoryType.GoldInPocket: 'Gold in Pocket', InventoryType.GoldWagered: 'Gold Wagered', InventoryType.PineInPocket: 'Pine', InventoryType.OakInPocket: 'Oak', InventoryType.IronInPocket: 'Iron', InventoryType.SteelInPocket: 'Steel', InventoryType.SilkInPocket: 'Silk', InventoryType.CanvasInPocket: 'Canvas', InventoryType.GrogInPocket: 'Grog', InventoryType.NewPlayerToken: 'New Player Token', InventoryType.ItemTypeWeapon: 'Weapon', InventoryType.ItemTypeClothing: 'Clothing', InventoryType.ItemTypeTattoo: 'Tattoo', InventoryType.ItemTypeJewelry: 'Jewelry', InventoryType.ItemTypeMusic: 'Music', InventoryType.MeleeWeaponL1: 'Fists', InventoryType.MeleeWeaponL2: 'Brass Knuckle', InventoryType.MeleeWeaponL3: 'Spiked Knuckle', InventoryType.MeleeWeaponL4: 'Fists', InventoryType.MeleeWeaponL5: 'Brass Knuckle', InventoryType.MeleeWeaponL6: 'Spiked Knuckle', InventoryType.CutlassWeaponL1: 'Rusty Cutlass', InventoryType.CutlassWeaponL2: 'Iron Cutlass', InventoryType.CutlassWeaponL3: 'Steel Cutlass', InventoryType.CutlassWeaponL4: 'Fine Cutlass', InventoryType.CutlassWeaponL5: 'Pirate Blade', InventoryType.CutlassWeaponL6: 'Dark Cutlass', InventoryType.PistolWeaponL1: 'Flintlock Pistol', InventoryType.PistolWeaponL2: 'Double-Barrel', InventoryType.PistolWeaponL3: 'Tri-Barrel', InventoryType.PistolWeaponL4: 'Heavy Tri-Barrel', InventoryType.PistolWeaponL5: 'Grand Pistol', InventoryType.PistolWeaponL6: 'Quad-Barrel', InventoryType.BayonetWeaponL1: 'Rusty Bayonet', InventoryType.BayonetWeaponL2: 'Navy Bayonet', InventoryType.BayonetWeaponL3: 'War Bayonet', InventoryType.MusketWeaponL1: 'Rusty Musket', InventoryType.MusketWeaponL2: 'Brass Musket', InventoryType.MusketWeaponL3: 'Iron Musket', InventoryType.DaggerWeaponL1: 'Dagger', InventoryType.DaggerWeaponL2: 'Battle Dirk', InventoryType.DaggerWeaponL3: 'Main Gauche', InventoryType.DaggerWeaponL4: 'Coltello', InventoryType.DaggerWeaponL5: 'Bloodletter', InventoryType.DaggerWeaponL6: 'Slicer', InventoryType.GrenadeWeaponL1: 'Grenades', InventoryType.GrenadeWeaponL2: 'Grenades Lvl2', InventoryType.GrenadeWeaponL3: 'Grenades Lvl3', InventoryType.GrenadeWeaponL4: 'Grenades Lvl4', InventoryType.GrenadeWeaponL5: 'Grenades Lvl5', InventoryType.GrenadeWeaponL6: 'Grenades Lvl6', InventoryType.DollWeaponL1: 'Voodoo Doll', InventoryType.DollWeaponL2: 'Cloth Doll', InventoryType.DollWeaponL3: 'Witch Doll', InventoryType.DollWeaponL4: 'Pirate Doll', InventoryType.DollWeaponL5: 'Taboo Doll', InventoryType.DollWeaponL6: 'Mojo Doll', InventoryType.WandWeaponL1: 'Cursed Staff', InventoryType.WandWeaponL2: 'Warped Staff', InventoryType.WandWeaponL3: 'Rend Staff', InventoryType.WandWeaponL4: 'Harrow Staff', InventoryType.WandWeaponL5: 'Vile Staff', InventoryType.WandWeaponL6: 'Dire Staff', InventoryType.KettleWeaponL1: 'Kettle', InventoryType.KettleWeaponL2: 'Cauldron', InventoryType.KettleWeaponL3: 'Black Kettle', InventoryType.RegularLure: 'Regular Lure', InventoryType.LegendaryLure: 'Legendary Lure', InventoryType.AppleIngredient: 'Apples', InventoryType.Potion1: 'Tonic', InventoryType.Potion2: 'Remedy', InventoryType.Potion3: 'Holy Water', InventoryType.Potion4: 'Elixir', InventoryType.Potion5: 'Miracle Water', InventoryType.CannonDamageLvl1: 'Cannoneer Draft I', InventoryType.CannonDamageLvl2: 'Cannoneer Draft II', InventoryType.CannonDamageLvl3: 'Cannoneer Draft III', InventoryType.PistolDamageLvl1: 'Marksman Draught I', InventoryType.PistolDamageLvl2: 'Marksman Draught II', InventoryType.PistolDamageLvl3: 'Marksman Draught III', InventoryType.CutlassDamageLvl1: 'Swashbuckler Stew I', InventoryType.CutlassDamageLvl2: 'Swashbuckler Stew II', InventoryType.CutlassDamageLvl3: 'Swashbuckler Stew III', InventoryType.DollDamageLvl1: 'Mystic Mixture I', InventoryType.DollDamageLvl2: 'Mystic Mixture II', InventoryType.DollDamageLvl3: 'Mystic Mixture III', InventoryType.HastenLvl1: 'Swift Foot I', InventoryType.HastenLvl2: 'Swift Foot II', InventoryType.HastenLvl3: 'Swift Foot III', InventoryType.RepBonusLvl1: 'Hardy Matey I', InventoryType.RepBonusLvl2: 'Hardy Matey II', InventoryType.RepBonusLvl3: 'Reputation Booster', InventoryType.RepBonusLvlComp: "Jack's Brew", InventoryType.GoldBonusLvl1: 'Plunder Potion I', InventoryType.GoldBonusLvl2: 'Plunder Potion II', InventoryType.InvisibilityLvl1: 'Phantom Spirits I', InventoryType.InvisibilityLvl2: 'Phantom Spirits II', InventoryType.RegenLvl1: 'Lively Bucko Brew I', InventoryType.RegenLvl2: 'Lively Bucko Brew II', InventoryType.RegenLvl3: 'Lively Bucko Brew III', InventoryType.RegenLvl4: 'Lively Bucko Brew IV', InventoryType.Burp: "Belchin' Brew", InventoryType.Fart: 'Flatulent Fizz', InventoryType.FartLvl2: 'Super Flatulent Fizz', InventoryType.Vomit: 'Puke Potion', InventoryType.HeadGrow: 'Big Head Potion', InventoryType.FaceColor: 'Ghastly Visage', InventoryType.SizeReduce: "Shrinkin' Grog", InventoryType.SizeIncrease: "Growin' Grog", InventoryType.HeadFire: 'Addled Elixir', InventoryType.ScorpionTransform: 'Stinger Stew', InventoryType.AlligatorTransform: 'Gator Grog', InventoryType.CrabTransform: 'Pincer Potion', InventoryType.AccuracyBonusLvl1: 'Deadeye I', InventoryType.AccuracyBonusLvl2: 'Deadeye II', InventoryType.AccuracyBonusLvl3: 'Deadeye III', InventoryType.StaffEnchant1: 'Staff Enchant I', InventoryType.StaffEnchant2: 'Staff Enchant II', InventoryType.SummonChicken: 'Summon Chicken', InventoryType.SummonMonkey: 'Summon Monkey', InventoryType.SummonWasp: 'Summon Wasp', InventoryType.SummonDog: 'Summon Dog', InventoryType.RemoveGroggy: "Clap o'Thunder", InventoryType.ShipRepairKit: 'Ship Repair Kit', InventoryType.PorkChunk: 'Roast Pork', InventoryType.CannonL1: 'Rusty Cannon', InventoryType.CannonL2: 'Iron Cannon', InventoryType.CannonL3: 'Gatling Cannon', InventoryType.Hp: 'Max HP', InventoryType.Mojo: 'Max Voodoo', InventoryType.TeleportHome: 'TeleportHome', InventoryType.TeleportGuildIsland: 'TeleportGuildIsland', InventoryType.FishingRodStall: 'Stall Lure', InventoryType.FishingRodPull: 'Pull Fish', InventoryType.FishingRodHeal: 'Heal Line', InventoryType.FishingRodTug: 'Tug Line', InventoryType.FishingRodSink: 'Sink Lure', InventoryType.FishingRodOceanEye: 'Ocean Eye', InventoryType.MeleeJab: 'Jab', InventoryType.MeleePunch: 'Punch', InventoryType.MeleeKick: 'Kick', InventoryType.MeleeRoundhouse: 'Roundhouse', InventoryType.MeleeHeadbutt: 'Headbutt', InventoryType.MeleeHaymaker: 'Haymaker', InventoryType.MeleeThrowDirt: 'Throw Dirt', InventoryType.MeleeToughness: 'Toughness', InventoryType.MeleeIronSkin: 'Iron Skin', InventoryType.MeleeDetermination: 'Determination', InventoryType.CutlassHack: 'Hack', InventoryType.CutlassSlash: 'Slash', InventoryType.CutlassStab: 'Thrust', InventoryType.CutlassFlourish: 'Flourish', InventoryType.CutlassCleave: 'Cleave', InventoryType.CutlassParry: 'Parry', InventoryType.CutlassEndurance: 'Endurance', InventoryType.CutlassTaunt: 'Taunt', InventoryType.CutlassBrawl: 'Brawl', InventoryType.CutlassSweep: 'Sweep', InventoryType.CutlassBladestorm: 'Blade Storm', EnemySkills.CUTLASS_MIGHTYSLASH: 'Mighty Slash', EnemySkills.CUTLASS_SKEWER: 'Skewer', EnemySkills.CUTLASS_OVERHEAD: 'Overhead Slash', EnemySkills.CUTLASS_ROLLTHRUST: 'Rolling Attack', EnemySkills.CUTLASS_CURSED_FIRE: 'Cursed Fire', EnemySkills.CUTLASS_CURSED_ICE: 'Cursed Ice', EnemySkills.CUTLASS_CURSED_THUNDER: 'Cursed Thunder', EnemySkills.CUTLASS_FIRE_BREAK: 'Inferno Sweep', EnemySkills.CUTLASS_ICE_BREAK: 'Freeze Sweep', EnemySkills.CUTLASS_THUNDER_BREAK: 'Shock Sweep', EnemySkills.CUTLASS_BLOWBACK: 'Hurricane Slash', EnemySkills.CUTLASS_CAPTAINS_FURY: "Captain's Fury", EnemySkills.CUTLASS_MASTERS_RIPOSTE: "Master's Riposte", EnemySkills.CUTLASS_POWER_ATTACK: 'Power Slash', EnemySkills.BROADSWORD_HACK: 'Chop', EnemySkills.BROADSWORD_SLASH: 'Roundhouse', EnemySkills.BROADSWORD_CLEAVE: 'Spin Cut', EnemySkills.BROADSWORD_FLOURISH: 'Reverse Spin Cut', EnemySkills.BROADSWORD_STAB: 'Jumping Slash', EnemySkills.SABRE_HACK: 'High Cut', EnemySkills.SABRE_SLASH: 'Low Slash', EnemySkills.SABRE_CLEAVE: 'Rapid Strike', EnemySkills.SABRE_FLOURISH: 'Slice & Dice', EnemySkills.SABRE_STAB: 'Cyclone Cut', InventoryType.PistolShoot: 'Shoot', InventoryType.PistolTakeAim: 'Take Aim', EnemySkills.PISTOL_CHARGE: 'Take Aim', EnemySkills.PISTOL_RELOAD: 'Reload', EnemySkills.SERPENT_VENOM: 'Venom Spit', InventoryType.PistolEagleEye: 'Eagle Eye', InventoryType.PistolDodge: 'Dodge', InventoryType.PistolSharpShooter: 'Sharp Shooter', InventoryType.PistolLeadShot: 'Lead Shot', InventoryType.PistolBaneShot: 'Bane Shot', InventoryType.PistolSilverShot: 'Silver Shot', InventoryType.PistolHexEaterShot: 'Hex Eater Shot', InventoryType.PistolSteelShot: 'Steel Shot', InventoryType.PistolVenomShot: 'Venom Shot', EnemySkills.PISTOL_SCATTERSHOT: 'Scattershot', EnemySkills.PISTOL_SCATTERSHOT_AIM: 'Take Aim', EnemySkills.PISTOL_DEADEYE: 'Deadeye', EnemySkills.PISTOL_RAPIDFIRE: 'Rapid Fire', EnemySkills.PISTOL_QUICKLOAD: 'Quick Load', EnemySkills.PISTOL_STUNSHOT: 'Stun Shot', EnemySkills.PISTOL_BREAKSHOT: 'Shrapnel Shot', EnemySkills.PISTOL_POINT_BLANK: 'Point Blank', EnemySkills.PISTOL_HOTSHOT: 'Coalfire Shot', InventoryType.BayonetShoot: 'Shoot', InventoryType.BayonetStab: 'Bayonet Stab', InventoryType.BayonetRush: 'Bayonet Rush', InventoryType.BayonetBash: 'Bayonet Bash', EnemySkills.BAYONET_SHOOT: 'Shoot', EnemySkills.BAYONET_STAB: 'Bayonet Stab', EnemySkills.BAYONET_RUSH: 'Bayonet Rush', EnemySkills.BAYONET_BASH: 'Bayonet Bash', EnemySkills.BAYONET_PLAYER_RUSH: 'Bayonet Rush', EnemySkills.BAYONET_PLAYER_BASH: 'Bayonet Bash', EnemySkills.BAYONET_DISABLE: 'Bayonet Disable', EnemySkills.BAYONET_PLAYER_STAB: 'Bayonet Stab', InventoryType.MusketShoot: 'Shoot', InventoryType.MusketTakeAim: 'Take Aim', InventoryType.MusketDeadeye: 'Deadeye', InventoryType.MusketEagleEye: 'Eagle Eye', InventoryType.MusketCrackShot: 'Crack Shot', InventoryType.MusketMarksman: 'Marksman', InventoryType.MusketLeadShot: 'Lead Shot', InventoryType.MusketScatterShot: 'Scatter Shot', InventoryType.MusketCursedShot: 'Cursed Shot', InventoryType.MusketCoalfireShot: 'Coalfire Shot', InventoryType.MusketHeavySlug: 'Heavy Slug', InventoryType.MusketExploderShot: 'Exploder Shot', InventoryType.DaggerCut: 'Cut', InventoryType.DaggerGouge: 'Gouge', InventoryType.DaggerSwipe: 'Swipe', InventoryType.DaggerEviscerate: 'Eviscerate', InventoryType.DaggerFinesse: 'Finesse', InventoryType.DaggerBladeInstinct: 'Blade Instinct', InventoryType.DaggerAsp: 'Asp', InventoryType.DaggerAdder: 'Adder', InventoryType.DaggerThrowDirt: 'Throw Dirt', InventoryType.DaggerSidewinder: 'Sidewinder', InventoryType.DaggerViperNest: "Viper's Nest", EnemySkills.DAGGER_BACKSTAB: 'Backstab', EnemySkills.DAGGER_COUP: 'Coup', EnemySkills.DAGGER_DAGGERRAIN: 'Dagger Rain', EnemySkills.DAGGER_THROW_COMBO_1: 'Knife Throw', EnemySkills.DAGGER_THROW_COMBO_2: 'Left-Handed Throw', EnemySkills.DAGGER_THROW_COMBO_3: 'Double Throw', EnemySkills.DAGGER_THROW_COMBO_4: 'Twin Backhand', EnemySkills.DAGGER_BARRAGE: 'Dagger Whirlwind', EnemySkills.DAGGER_ICEBARRAGE: 'Silver Freeze', EnemySkills.DAGGER_VENOMSTAB: 'Venom Stab', EnemySkills.DAGGER_ACIDDAGGER: 'Acid Dagger', InventoryType.SailBroadsideLeft: 'Left Broadside', InventoryType.SailBroadsideRight: 'Right Broadside', InventoryType.SailFullSail: 'Full Sail', InventoryType.SailComeAbout: 'Come About', InventoryType.SailOpenFire: 'Open Fire!', InventoryType.SailRammingSpeed: 'Ramming Speed', InventoryType.SailTakeCover: 'Take Cover!', InventoryType.SailPowerRecharge: 'Leadership', InventoryType.SailWindcatcher: 'Windcatcher', InventoryType.SailTacking: 'Tacking', InventoryType.SailTreasureSense: 'Treasure Sense', InventoryType.SailTaskmaster: 'Taskmaster', EnemySkills.SAIL_WRECK_HULL: 'Wreck the Hull', EnemySkills.SAIL_WRECK_MASTS: 'Wreck the Masts', EnemySkills.SAIL_SINK_HER: 'Sink Her', EnemySkills.SAIL_INCOMING: 'Incoming', EnemySkills.SAIL_FIX_IT_NOW: 'Fix It Now!', InventoryType.GrenadeThrow: 'Throw', InventoryType.GrenadeExplosion: 'Explosive', InventoryType.GrenadeShockBomb: 'Stink Pot', InventoryType.GrenadeFireBomb: 'Fire Bomb', InventoryType.GrenadeSmokeCloud: 'Smoke Bomb', InventoryType.GrenadeSiege: 'Siege Charge', InventoryType.GrenadeDetermination: 'Determination', InventoryType.GrenadeLongVolley: 'Long Volley', InventoryType.GrenadeDemolitions: 'Demolitions', InventoryType.GrenadeToughness: 'Toughness', InventoryType.GrenadeIgnorePain: 'Ignore Pain', EnemySkills.GRENADE_RELOAD: 'Reload', EnemySkills.GRENADE_CHARGE: 'Long Volley', InventoryType.DollAttune: 'Attune Doll', EnemySkills.DOLL_UNATTUNE: 'Unattune Doll', EnemySkills.DOLL_POKE2: 'Poke', InventoryType.DollPoke: 'Poke', InventoryType.DollSwarm: 'Swarm', InventoryType.DollHeal: 'Heal', InventoryType.DollBurn: 'Scorch', InventoryType.DollShackles: 'Grave Shackles', InventoryType.DollCure: 'Cure', InventoryType.DollCurse: 'Curse', InventoryType.DollLifeDrain: 'Life Drain', InventoryType.DollFocus: 'Focus', InventoryType.DollSpiritWard: 'Spirit Ward', EnemySkills.DOLL_REGENERATION: 'Regeneration', EnemySkills.DOLL_SPIRIT_MEND: 'Spirit Mend', EnemySkills.DOLL_WIND_GUARD: 'Wind Guard', EnemySkills.DOLL_RED_FURY: 'Red Fury', EnemySkills.DOLL_SPIRIT_GUARD: 'Spirit Guard', EnemySkills.DOLL_HEX_GUARD: 'Hex Guard', EnemySkills.DOLL_EVIL_EYE: 'Evil Eye', EnemySkills.STAFF_WITHER_CHARGE: 'Casting', EnemySkills.STAFF_SOULFLAY_CHARGE: 'Casting', EnemySkills.STAFF_PESTILENCE_CHARGE: 'Casting', EnemySkills.STAFF_HELLFIRE_CHARGE: 'Casting', EnemySkills.STAFF_BANISH_CHARGE: 'Casting', EnemySkills.STAFF_DESOLATION_CHARGE: 'Casting', EnemySkills.STAFF_FIZZLE: 'Fizzled', InventoryType.StaffBlast: 'Blast', InventoryType.StaffWither: 'Wither', InventoryType.StaffSoulFlay: 'Soul Flay', InventoryType.StaffPestilence: 'Pestilence', InventoryType.StaffHellfire: 'Flaming Skull', InventoryType.StaffBanish: 'Banish', InventoryType.StaffDesolation: 'Desolation', InventoryType.StaffConcentration: 'Concentration', InventoryType.StaffSpiritLore: 'Spirit Lore', InventoryType.StaffConservation: 'Conservation', InventoryType.StaffSpiritMastery: 'Spirit Mastery', EnemySkills.STAFF_TOGGLE_AURA_OFF: 'Toggle Aura Off', EnemySkills.STAFF_TOGGLE_AURA_WARDING: 'Warding Aura', EnemySkills.STAFF_TOGGLE_AURA_NATURE: 'Nature Aura', EnemySkills.STAFF_TOGGLE_AURA_DARK: 'Dark Aura', InventoryType.CannonShoot: 'Shoot', InventoryType.CannonRoundShot: 'Round Shot', InventoryType.CannonChainShot: 'Chain Shot', InventoryType.CannonExplosive: 'Explosive', InventoryType.CannonBullet: 'Bullet', InventoryType.CannonGasCloud: 'Gas Cloud', InventoryType.CannonGrapeShot: 'Grape Shot', InventoryType.CannonSkull: 'Skull Ammo', InventoryType.CannonFirebrand: 'Firebrand', InventoryType.CannonFlameCloud: 'Flame Cloud', InventoryType.CannonFlamingSkull: 'Firebrand', InventoryType.CannonBarShot: 'Bar Shot', InventoryType.CannonKnives: 'Knives', InventoryType.CannonMine: 'Mine', InventoryType.CannonBarnacles: 'Barnacles', InventoryType.CannonThunderbolt: 'Thunderbolt', InventoryType.CannonFury: 'Fury', InventoryType.CannonComet: 'Comet', InventoryType.CannonGrappleHook: 'Grapple Hook', InventoryType.CannonRapidReload: 'Rapid Reload', InventoryType.CannonBarrage: 'Barrage', InventoryType.CannonShrapnel: 'Shrapnel', InventoryType.DefenseCannonRoundShot: 'Round Shot', InventoryType.DefenseCannonMine: 'Mine', InventoryType.DefenseCannonTargetedShot: 'Targeted Shot', InventoryType.DefenseCannonHotShot: 'Hot Shot', InventoryType.DefenseCannonScatterShot: 'Scatter Shot', InventoryType.DefenseCannonPowderKeg: 'Powder Keg', InventoryType.DefenseCannonSmokePowder: 'Smoke Powder', InventoryType.DefenseCannonBullet: 'Bullet', InventoryType.DefenseCannonColdShot: 'Cold Shot', InventoryType.DefenseCannonBomb: 'Bomb', InventoryType.DefenseCannonChumShot: 'Bait Shot', InventoryType.DefenseCannonFireStorm: 'Firestorm', InventoryType.DefenseCannonEmpty: 'Empty', InventoryType.UseItem: 'Use Item', InventoryType.UsePotion: 'Use Potion', EnemySkills.CLAW_RAKE: 'Claw Rake', EnemySkills.CLAW_STRIKE: 'Claw Strike', EnemySkills.DUAL_CLAW: 'Dual Claw', EnemySkills.POISON_VOMIT: 'Poison Vomit', EnemySkills.GROUND_SLAP: 'Ground Slap', EnemySkills.ENSNARE: 'Ensnare', EnemySkills.CONSTRICT: 'Constrict', EnemySkills.PILEDRIVER: 'Piledriver', EnemySkills.POUND: 'Pound', EnemySkills.SQUASH: 'Squash', EnemySkills.STUMP_KICK: 'Lunge Kick', EnemySkills.STUMP_KICK_RIGHT: 'Kick', EnemySkills.STUMP_SLAP_LEFT: 'Smash Left', EnemySkills.STUMP_SLAP_RIGHT: 'Smash Right', EnemySkills.STUMP_SWAT_LEFT: 'Swat Left', EnemySkills.STUMP_SWAT_RIGHT: 'Swat Right', EnemySkills.STUMP_STOMP: 'Earthquake', EnemySkills.FLYTRAP_ATTACK_A: 'Bite', EnemySkills.FLYTRAP_ATTACK_JAB: 'Jab', EnemySkills.FLYTRAP_LEFT_FAKE: 'Left Fake', EnemySkills.FLYTRAP_RIGHT_FAKE: 'Right Fake', EnemySkills.FLYTRAP_SPIT: 'Acid Spit', EnemySkills.FLYTRAP_WEAK_SPIT: 'Venom Spit', EnemySkills.SCORPION_ATTACK_LEFT: 'Left Pincer', EnemySkills.SCORPION_ATTACK_RIGHT: 'Right Pincer', EnemySkills.SCORPION_ATTACK_BOTH: 'Dual Pincer', EnemySkills.SCORPION_ATTACK_TAIL_STING: 'Tail Sting', EnemySkills.SCORPION_PICK_UP_HUMAN: 'Pickup', EnemySkills.SCORPION_REAR_UP: 'Rearup', EnemySkills.ALLIGATOR_ATTACK_LEFT: 'Bite', EnemySkills.ALLIGATOR_ATTACK_RIGHT: 'Bite', EnemySkills.ALLIGATOR_ATTACK_STRAIGHT: 'Bite', EnemySkills.ALLIGATOR_CRUSH: 'Crushing Bite', EnemySkills.ALLIGATOR_MAIM: 'Maim', EnemySkills.BAT_ATTACK_LEFT: 'Bite', EnemySkills.BAT_ATTACK_RIGHT: 'Talon Rake', EnemySkills.BAT_SHRIEK: 'Shriek', EnemySkills.BAT_FLURRY: 'Bat Flurry', EnemySkills.WASP_ATTACK: 'Sting', EnemySkills.WASP_ATTACK_LEAP: 'Sting', EnemySkills.WASP_POISON_STING: 'Poison Sting', EnemySkills.WASP_PAIN_BITE: 'Paralyzing Sting', EnemySkills.LEFT_BROADSIDE: 'Left Broadside', EnemySkills.RIGHT_BROADSIDE: 'Right Broadside', EnemySkills.CUTLASS_CHOP: 'Savage Blow', EnemySkills.CUTLASS_DOUBLESLASH: 'Double Cut', EnemySkills.CUTLASS_LUNGE: 'Lunge', EnemySkills.CUTLASS_STAB: 'Stab', EnemySkills.CUTLASS_COMBOA: 'Coupe de Grace', EnemySkills.CUTLASS_WILDSLASH: 'Wild Swing', EnemySkills.CUTLASS_FLURRY: 'Flurry', EnemySkills.CUTLASS_RIPOSTE: 'Riposte', EnemySkills.DAGGER_THROW_KNIFE: 'Throwing Blade', EnemySkills.DAGGER_THROW_VENOMBLADE: 'Venom Blade', EnemySkills.DAGGER_THROW_BARBED: 'Crippling Blade', EnemySkills.DAGGER_THROW_INTERRUPT: 'Stinging Blade', EnemySkills.FOIL_FLECHE: 'Foil Fleche', EnemySkills.FOIL_REPRISE: 'Foil Reprise', EnemySkills.FOIL_SWIPE: 'Foil Swipe', EnemySkills.FOIL_IMPALE: 'Foil Impale', EnemySkills.FOIL_REMISE: 'Foil Remise', EnemySkills.FOIL_BALESTRAKICK: 'Foil Balestra Kick', EnemySkills.FOIL_CADENCE: 'Foil Cadence', EnemySkills.DUALCUTLASS_COMBINATION: 'Dual Cutlass Combination', EnemySkills.DUALCUTLASS_SPIN: 'Dual Cutlass Spin', EnemySkills.DUALCUTLASS_BARRAGE: 'Dual Cutlass Barrage', EnemySkills.DUALCUTLASS_XSLASH: 'Dual Cutlass X-Slash', EnemySkills.DUALCUTLASS_GORE: 'Dual Cutlass Gore', EnemySkills.JR_DEATH_SLASH: 'Death Slash', EnemySkills.JR_VOODOO_SHOT: 'Voodoo Blast', EnemySkills.JR_GRAVEBIND: 'Grave Bind', EnemySkills.JR_SOUL_HARVEST: 'Soul Storm', EnemySkills.JR_ANIMATE_DEAD: 'Animate Dead', EnemySkills.JR_PULVERIZER: 'Pulzerizer', EnemySkills.JR_CORRUPTION: 'Corruption', EnemySkills.JR_EXECUTE: 'Execute', EnemySkills.JR_THUNDER: 'Dark Thunderbolt', EnemySkills.AXE_CHOP: 'Axe Chop', EnemySkills.GHOST_PHANTOM_TOUCH: 'Phantom Reach', EnemySkills.GHOST_KILL_TOUCH: 'Somber Demise', EnemySkills.GHOST_SUMMON_HELP: 'Summon Help', EnemySkills.MISC_CLEANSE: 'Cleanse', EnemySkills.MISC_DARK_CURSE: 'Dark Curse', EnemySkills.MISC_GHOST_FORM: 'Ghost Form', EnemySkills.MISC_FEINT: 'Feint', EnemySkills.MISC_HEX_WARD: 'Hex Ward', EnemySkills.MISC_CAPTAINS_RESOLVE: "Captain's Resolve", EnemySkills.MISC_NOT_IN_FACE: 'Not in the Face!', EnemySkills.MISC_ACTIVATE_VOODOO_REFLECT: 'Voodoo Reflect', EnemySkills.MISC_VOODOO_REFLECT: 'Voodoo Reflect', EnemySkills.MISC_MONKEY_PANIC: 'Monkey Panic', EnemySkills.MISC_FIRST_AID: 'Healing Boost', EnemySkills.TORCH_ATTACK: 'Torch Attack', InventoryType.Dinghy: 'Dinghy', InventoryType.NewShipToken: 'New Ship Token', InventoryType.NewWeaponToken: 'New Weapon Token', InventoryType.SmallBottle: 'Small Ship Bottle', InventoryType.MediumBottle: 'Medium Ship Bottle', InventoryType.LargeBottle: 'Large Ship Bottle', InventoryType.CutlassToken: 'Cutlass Token', InventoryType.PistolToken: 'Pistol Token', InventoryType.MusketToken: 'Musket Token', InventoryType.DaggerToken: 'Dagger Token', InventoryType.GrenadeToken: 'Grenade Token', InventoryType.WandToken: 'Wand Token', InventoryType.DollToken: 'Doll Token', InventoryType.KettleToken: 'Kettle Token', InventoryType.OpenQuestSlot: 'Open Quest Slot', InventoryType.OverallRep: 'Notoriety', InventoryType.GeneralRep: 'General', InventoryType.MeleeRep: 'Brawl', InventoryType.CutlassRep: 'Sword', InventoryType.PistolRep: 'Shooting', InventoryType.MusketRep: 'Musket', InventoryType.DaggerRep: 'Dagger', InventoryType.GrenadeRep: 'Grenade', InventoryType.DollRep: 'Doll', InventoryType.WandRep: 'Staff', InventoryType.KettleRep: 'Kettle', InventoryType.CannonRep: 'Cannon', InventoryType.DefenseCannonRep: 'Navy Cannon', InventoryType.LockpickRep: 'Lockpick', InventoryType.MonsterRep: 'Monster', InventoryType.SailingRep: 'Sailing', InventoryType.GamblingRep: 'Gambling', InventoryType.FishingRep: 'Fishing', InventoryType.PotionsRep: 'Potions', InventoryType.UnspentMelee: 'Melee Skill Point', InventoryType.UnspentCutlass: 'Sword Skill Point', InventoryType.UnspentPistol: 'Shooting Skill Point', InventoryType.UnspentMusket: 'Musket Skill Point', InventoryType.UnspentDagger: 'Dagger Skill Point', InventoryType.UnspentGrenade: 'Grenade Skill Point', InventoryType.UnspentWand: 'Wand Skill Point', InventoryType.UnspentDoll: 'Doll Skill Point', InventoryType.UnspentKettle: 'Kettle Skill Point', InventoryType.UnspentCannon: 'Cannon Skill Point', InventoryType.UnspentSailing: 'Sailing Skill Point', InventoryType.Vitae_Level: 'Vitae Level', InventoryType.Vitae_Cost: 'Vitae Cost', InventoryType.Vitae_Left: 'Vitae Left', InventoryType.ShipRepairToken: 'Ship Repair Token', InventoryType.PlayerHealToken: 'Player Heal Token', InventoryType.PlayerMojoHealToken: 'Player Mojo Heal Token', InventoryType.AmmoLeadShot: 'Lead Shot', InventoryType.AmmoBaneShot: 'Bane Shot', InventoryType.AmmoSilverShot: 'Silver Shot', InventoryType.AmmoHexEaterShot: 'Hex Eater Shot', InventoryType.AmmoSteelShot: 'Steel Shot', InventoryType.AmmoVenomShot: 'Venom Shot', InventoryType.AmmoAsp: 'Throwing Knife', InventoryType.AmmoAdder: 'Venom Dagger', InventoryType.AmmoSidewinder: 'Sidewinder', InventoryType.AmmoViperNest: 'Viper Brace', InventoryType.AmmoScatterShot: 'Scatter Shot', InventoryType.AmmoCursedShot: 'Cursed Shot', InventoryType.AmmoCoalfireShot: 'Coalfire Shot', InventoryType.AmmoHeavySlug: 'Heavy Slug', InventoryType.AmmoExploderShot: 'Exploder Shot', InventoryType.AmmoGrenadeExplosion: 'Explosive', InventoryType.AmmoGrenadeFlame: 'Flame Burst', InventoryType.AmmoGrenadeShockBomb: 'Stink Pot', InventoryType.AmmoGrenadeSmoke: 'Smoke Cloud', InventoryType.AmmoGrenadeLandMine: 'Land Mine', InventoryType.AmmoGrenadeSiege: 'Siege Charge', InventoryType.AmmoRoundShot: 'Round Shot', InventoryType.AmmoChainShot: 'Chain Shot', InventoryType.AmmoExplosive: 'Explosive', InventoryType.AmmoBullet: 'Bullet', InventoryType.AmmoGasCloud: 'Gas Cloud', InventoryType.AmmoGrapeShot: 'Grape Shot', InventoryType.AmmoSkull: 'Skull', InventoryType.AmmoFirebrand: 'Firebrand', InventoryType.AmmoFlameCloud: 'Flame Cloud', InventoryType.AmmoFlamingSkull: 'Flaming Skull', InventoryType.AmmoBarShot: 'Bar Shot', InventoryType.AmmoKnives: 'Knives', InventoryType.AmmoMine: 'Mines', InventoryType.AmmoBarnacles: 'Barnacles', InventoryType.AmmoThunderbolt: 'Thunderbolt', InventoryType.AmmoFury: 'Fury', InventoryType.AmmoComet: 'Comet', InventoryType.AmmoGrappleHook: 'Grappling Hook', InventoryType.PistolPouchL1: 'Small Pouch', InventoryType.PistolPouchL2: 'Medium Pouch', InventoryType.PistolPouchL3: 'Large Pouch', InventoryType.DaggerPouchL1: 'Small Belt', InventoryType.DaggerPouchL2: 'Medium Belt', InventoryType.DaggerPouchL3: 'Large Belt', InventoryType.GrenadePouchL1: 'Small Sack', InventoryType.GrenadePouchL2: 'Medium Sack', InventoryType.GrenadePouchL3: 'Large Sack', InventoryType.CannonPouchL1: 'Small Barrel', InventoryType.CannonPouchL2: 'Medium Barrel', InventoryType.CannonPouchL3: 'Large Barrel', InventoryType.CTFGame: 'CTFGame', InventoryType.CTLGame: 'CTLGame', InventoryType.PTRGame: 'PTRGame', InventoryType.BTLGame: 'BTLGame', InventoryType.TBTGame: 'TBTGame', InventoryType.SBTGame: 'SBTGame', InventoryType.ARMGame: 'ARMGame', InventoryType.TKPGame: 'TKPGame', InventoryType.BTBGame: 'BTBGame', InventoryType.PokerGame: 'PokerGame', InventoryType.BlackjackGame: 'BlackjackGame', InventoryType.ShipPVPRank: 'Ship PVP', ItemId.INTERCEPTOR_L1: ShipClassNames.get(ShipGlobals.INTERCEPTORL1), ItemId.INTERCEPTOR_L2: ShipClassNames.get(ShipGlobals.INTERCEPTORL2), ItemId.INTERCEPTOR_L3: ShipClassNames.get(ShipGlobals.INTERCEPTORL3), ItemId.MERCHANT_L1: ShipClassNames.get(ShipGlobals.MERCHANTL1), ItemId.MERCHANT_L2: ShipClassNames.get(ShipGlobals.MERCHANTL2), ItemId.MERCHANT_L3: ShipClassNames.get(ShipGlobals.MERCHANTL3), ItemId.WARSHIP_L1: ShipClassNames.get(ShipGlobals.WARSHIPL1), ItemId.WARSHIP_L2: ShipClassNames.get(ShipGlobals.WARSHIPL2), ItemId.WARSHIP_L3: ShipClassNames.get(ShipGlobals.WARSHIPL3), ItemId.BRIG_L1: ShipClassNames.get(ShipGlobals.BRIGL1), ItemId.BRIG_L2: ShipClassNames.get(ShipGlobals.BRIGL2), ItemId.BRIG_L3: ShipClassNames.get(ShipGlobals.BRIGL3), ItemId.QUEEN_ANNES_REVENGE: ShipClassNames.get(ShipGlobals.QUEEN_ANNES_REVENGE), ItemId.HUNTER_VENGEANCE: ShipClassNames.get(ShipGlobals.HUNTER_VENGEANCE), ItemId.HUNTER_TALLYHO: ShipClassNames.get(ShipGlobals.HUNTER_TALLYHO), ItemId.BLACK_PEARL: ShipClassNames.get(ShipGlobals.BLACK_PEARL), ItemId.GOLIATH: ShipClassNames.get(ShipGlobals.GOLIATH), ItemId.SHIP_OF_THE_LINE: ShipClassNames.get(ShipGlobals.SHIP_OF_THE_LINE), ItemId.EL_PATRONS_SHIP: ShipClassNames.get(ShipGlobals.EL_PATRONS_SHIP), ItemId.P_SKEL_PHANTOM: ShipClassNames.get(ShipGlobals.P_SKEL_PHANTOM), ItemId.P_SKEL_REVENANT: ShipClassNames.get(ShipGlobals.P_SKEL_REVENANT), ItemId.P_SKEL_CEREBUS: ShipClassNames.get(ShipGlobals.P_SKEL_CEREBUS), ItemId.P_NAVY_KINGFISHER: ShipClassNames.get(ShipGlobals.P_NAVY_KINGFISHER), ItemId.P_EITC_WARLORD: ShipClassNames.get(ShipGlobals.P_EITC_WARLORD), ItemId.HMS_VICTORY: ShipClassNames.get(ShipGlobals.HMS_VICTORY), ItemId.HMS_NEWCASTLE: ShipClassNames.get(ShipGlobals.HMS_NEWCASTLE), ItemId.HMS_INVINCIBLE: ShipClassNames.get(ShipGlobals.HMS_INVINCIBLE), ItemId.EITC_INTREPID: ShipClassNames.get(ShipGlobals.EITC_INTREPID), ItemId.EITC_CONQUERER: ShipClassNames.get(ShipGlobals.EITC_CONQUERER), ItemId.EITC_LEVIATHAN: ShipClassNames.get(ShipGlobals.EITC_LEVIATHAN), ItemId.NAVY_FERRET: ShipClassNames.get(ShipGlobals.NAVY_FERRET), ItemId.NAVY_BULWARK: ShipClassNames.get(ShipGlobals.NAVY_BULWARK), ItemId.NAVY_PANTHER: ShipClassNames.get(ShipGlobals.NAVY_PANTHER), ItemId.NAVY_GREYHOUND: ShipClassNames.get(ShipGlobals.NAVY_GREYHOUND), ItemId.NAVY_VANGUARD: ShipClassNames.get(ShipGlobals.NAVY_VANGUARD), ItemId.NAVY_CENTURION: ShipClassNames.get(ShipGlobals.NAVY_CENTURION), ItemId.NAVY_KINGFISHER: ShipClassNames.get(ShipGlobals.NAVY_KINGFISHER), ItemId.NAVY_MONARCH: ShipClassNames.get(ShipGlobals.NAVY_MONARCH), ItemId.NAVY_MAN_O_WAR: ShipClassNames.get(ShipGlobals.NAVY_MAN_O_WAR), ItemId.NAVY_PREDATOR: ShipClassNames.get(ShipGlobals.NAVY_PREDATOR), ItemId.NAVY_COLOSSUS: ShipClassNames.get(ShipGlobals.NAVY_COLOSSUS), ItemId.NAVY_DREADNOUGHT: ShipClassNames.get(ShipGlobals.NAVY_DREADNOUGHT), ItemId.NAVY_BASTION: ShipClassNames.get(ShipGlobals.NAVY_BASTION), ItemId.NAVY_ELITE: ShipClassNames.get(ShipGlobals.NAVY_ELITE), ItemId.EITC_SEA_VIPER: ShipClassNames.get(ShipGlobals.EITC_SEA_VIPER), ItemId.EITC_SENTINEL: ShipClassNames.get(ShipGlobals.EITC_SENTINEL), ItemId.EITC_CORVETTE: ShipClassNames.get(ShipGlobals.EITC_CORVETTE), ItemId.EITC_BLOODHOUND: ShipClassNames.get(ShipGlobals.EITC_BLOODHOUND), ItemId.EITC_IRONWALL: ShipClassNames.get(ShipGlobals.EITC_IRONWALL), ItemId.EITC_MARAUDER: ShipClassNames.get(ShipGlobals.EITC_MARAUDER), ItemId.EITC_BARRACUDA: ShipClassNames.get(ShipGlobals.EITC_BARRACUDA), ItemId.EITC_OGRE: ShipClassNames.get(ShipGlobals.EITC_OGRE), ItemId.EITC_WARLORD: ShipClassNames.get(ShipGlobals.EITC_WARLORD), ItemId.EITC_CORSAIR: ShipClassNames.get(ShipGlobals.EITC_CORSAIR), ItemId.EITC_BEHEMOTH: ShipClassNames.get(ShipGlobals.EITC_BEHEMOTH), ItemId.EITC_JUGGERNAUT: ShipClassNames.get(ShipGlobals.EITC_JUGGERNAUT), ItemId.EITC_TYRANT: ShipClassNames.get(ShipGlobals.EITC_TYRANT), ItemId.SKEL_PHANTOM: ShipClassNames.get(ShipGlobals.SKEL_PHANTOM), ItemId.SKEL_REVENANT: ShipClassNames.get(ShipGlobals.SKEL_REVENANT), ItemId.SKEL_STORM_REAPER: ShipClassNames.get(ShipGlobals.SKEL_STORM_REAPER), ItemId.SKEL_BLACK_HARBINGER: ShipClassNames.get(ShipGlobals.SKEL_BLACK_HARBINGER), ItemId.SKEL_DEATH_OMEN: ShipClassNames.get(ShipGlobals.SKEL_DEATH_OMEN), ItemId.SKEL_SHADOW_CROW_FR: ShipClassNames.get(ShipGlobals.SKEL_SHADOW_CROW_FR), ItemId.SKEL_HELLHOUND_FR: ShipClassNames.get(ShipGlobals.SKEL_HELLHOUND_FR), ItemId.SKEL_BLOOD_SCOURGE_FR: ShipClassNames.get(ShipGlobals.SKEL_BLOOD_SCOURGE_FR), ItemId.SKEL_SHADOW_CROW_SP: ShipClassNames.get(ShipGlobals.SKEL_SHADOW_CROW_SP), ItemId.SKEL_HELLHOUND_SP: ShipClassNames.get(ShipGlobals.SKEL_HELLHOUND_SP), ItemId.SKEL_BLOOD_SCOURGE_SP: ShipClassNames.get(ShipGlobals.SKEL_BLOOD_SCOURGE_SP), ItemId.WHEAT: 'Wheat', ItemId.COTTON: 'Cotton', ItemId.RUM: 'Medicine', ItemId.IRON_ORE: 'Iron Ore', ItemId.IVORY: 'Ivory', ItemId.SILK: 'Silk', ItemId.SPICES: 'Spices', ItemId.COPPER_BARS: 'Copper Bars', ItemId.SILVER_BARS: 'Silver Bars', ItemId.GOLD_BARS: 'Gold Bars', ItemId.EMERALDS: 'Emeralds', ItemId.RUBIES: 'Rubies', ItemId.DIAMONDS: 'Diamonds', ItemId.CURSED_COIN: 'Cursed Coin', ItemId.ARTIFACT: 'Artifact', ItemId.RELIC: 'Relic', ItemId.RARE_DIAMOND: 'Rare Diamond', ItemId.CROWN_JEWELS: 'Crown Jewels', ItemId.RAREITEM6: 'Rare Item 6', InventoryType.PVPTotalInfamySea: 'Privateering Infamy Rank', InventoryType.PVPTotalInfamyLand: 'PvP Infamy Rank', InventoryType.Song_1: '1. Driftwood Island', InventoryType.Song_2: '2. Isla Cangrejos', InventoryType.Song_3: '3. Outcast Isle', InventoryType.Song_4: '4. Scatter the Gulls', InventoryType.Song_5: '5. Married to the Sea', InventoryType.Song_6: '6. Song 6', InventoryType.Song_7: '7. Song 7', InventoryType.Song_8: '8. Song 8', InventoryType.Song_9: '9. Song 9', InventoryType.Song_10: '10. Song 10', InventoryType.Song_11: "11. Merchant's Folly", InventoryType.Song_12: '12. Prepare to Cast Off!', InventoryType.Song_13: '13. Cutthroat Isle', InventoryType.Song_14: '14. Kingshead', InventoryType.Song_15: "15. Rumrunner's Isle", InventoryType.Song_16: '16. Song 16', InventoryType.Song_17: '17. Song 17', InventoryType.Song_18: '18. Song 18', InventoryType.Song_19: '19. Song 19', InventoryType.Song_20: '20. Song 20', InventoryType.Song_21: '21. Ballad of a Buccaneer', InventoryType.Song_22: '22. Caribbean Holiday'
}

def getInventoryTypeName(itemId):
    name = InventoryTypeNames.get(itemId)
    if name:
        return name
    return ''


ItemNames = {
    ItemGlobals.RUSTY_CUTLASS: 'Rusty Cutlass', ItemGlobals.IRON_CUTLASS: 'Iron Cutlass', ItemGlobals.STEEL_CUTLASS: 'Steel Cutlass', ItemGlobals.FINE_CUTLASS: 'Fine Cutlass', ItemGlobals.PIRATE_BLADE: 'Pirate Blade', ItemGlobals.WORN_CUTLASS: 'Worn Cutlass', ItemGlobals.SWABBIE_CUTLASS: "Swabbie's Cutlass", ItemGlobals.DECKHAND_CUTLASS: "Deck-hand's Cutlass", ItemGlobals.CABIN_BOY_CUTLASS: "Cabin Boy's Cutlass", ItemGlobals.LIGHT_CUTLASS: 'Light Cutlass', ItemGlobals.HEAVY_CUTLASS: 'Heavy Cutlass', ItemGlobals.SAILOR_CUTLASS: "Sailor's Cutlass", ItemGlobals.BOARDING_CUTLASS: 'Boarding Cutlass', ItemGlobals.WAR_CUTLASS: 'War Cutlass', ItemGlobals.SHARP_CUTLASS: 'Sharp Cutlass', ItemGlobals.TEMPERED_CUTLASS: 'Tempered Cutlass', ItemGlobals.ENGRAVED_CUTLASS: 'Engraved Cutlass', ItemGlobals.BEJEWELED_CUTLASS: 'Bejeweled Cutlass', ItemGlobals.MASTERWORK_CUTLASS: 'Masterwork Cutlass', ItemGlobals.NAVY_SERGEANT_CUTLASS: "Navy Sergeant's Cutlass", ItemGlobals.EITC_MERVENARY_CUTLASS: "EITC Mercenary's Cutlass", ItemGlobals.BANDIT_CUTLASS: "Bandit's Cutlass", ItemGlobals.PIRATE_CUTLASS: "Pirate's Cutlass", ItemGlobals.SLASHER_CUTLASS: "Slasher's Cutlass", ItemGlobals.POISONED_CUTLASS: 'Poisoned Cutlass', ItemGlobals.VENOMED_CUTLASS: 'Venomed Cutlass', ItemGlobals.ASSASSIN_CUTLASS: "Assassin's Cutlass", ItemGlobals.MONKEY_CUTLASS: 'Monkey Cutlass', ItemGlobals.BABOON_CUTLASS: 'Baboon Cutlass', ItemGlobals.ORANGUTAN_CUTLASS: 'Orangutan Cutlass', ItemGlobals.GORILLA_CUTLASS: 'Gorilla Cutlass', ItemGlobals.VOODOO_HUNTER_CUTLASS: 'Voodoo Hunter Cutlass', ItemGlobals.WITCH_HUNTER_CUTLASS: 'Witch Hunter Cutlass', ItemGlobals.CUTLASS_OF_THE_INQUISITION: 'Cutlass of the Inquisition', ItemGlobals.SILVER_CUTLASS: 'Silver Cutlass', ItemGlobals.HOLY_CUTLASS: 'Holy Cutlass', ItemGlobals.SACRED_CUTLASS: 'Sacred Cutlass', ItemGlobals.DIVINE_CUTLASS: 'Divine Cutlass', ItemGlobals.BRUTE_CUTLASS: "Brute's Cutlass", ItemGlobals.BRAWLER_CUTLASS: "Brawler's Cutlass", ItemGlobals.BRUISER_CUTLASS: "Bruiser's Cutlass", ItemGlobals.DARK_CUTLASS: 'Dark Cutlass', ItemGlobals.SHADOW_CUTLASS: 'Shadow Cutlass', ItemGlobals.FORBIDDEN_CUTLASS: 'Forbidden Cutlass', ItemGlobals.MARINER_CUTLASS: "Mariner's Cutlass", ItemGlobals.QUARTER_MASTER_CUTLASS: "Quarter Master's Cutlass", ItemGlobals.FIRST_MATE_CUTLASS: "First Mate's Cutlass", ItemGlobals.LIEUTENANT_CUTLASS: "Lieutenant's Cutlass", ItemGlobals.COMMANDER_CUTLASS: "Commander's Cutlass", ItemGlobals.CAPTAIN_CUTLASS: "Captain's Cutlass", ItemGlobals.COMMODORE_CUTLASS: "Commodore's Cutlass", ItemGlobals.VICE_ADMIRAL_CUTLASS: "Vice Admiral's Cutlass", ItemGlobals.ADMIRAL_CUTLASS: "Admiral's Cutlass", ItemGlobals.SHARK_BLADE: 'Shark Blade', ItemGlobals.TIGER_SHARK_BLADE: 'Tiger Shark Blade', ItemGlobals.BLACK_SHARK_BLADE: 'Black Shark Blade', ItemGlobals.BANE_BLADE_CUTLASS: 'Bane Blade Cutlass', ItemGlobals.BANE_FIRE_CUTLASS: 'Bane Fire Cutlass', ItemGlobals.BANE_CURSE_CUTLASS: 'Bane Curse Cutlass', ItemGlobals.SEA_DOG_CUTLASS: "Sea Dog's Cutlass", ItemGlobals.SWASHBUCKLER_CUTLASS: "Swashbuckler's Cutlass", ItemGlobals.BUCCANEER_CUTLASS: "Buccaneer's Cutlass", ItemGlobals.PRIVATEER_CUTLASS: "Privateer's Cutlass", ItemGlobals.CORSAIR_CUTLASS: "Corsair's Cutlass", ItemGlobals.SEVEN_SEAS_CUTLASS: 'Seven Seas Cutlass', ItemGlobals.BLOODFIRE_CUTLASS: 'Bloodfire Cutlass', ItemGlobals.CRIMSONFIRE_CUTLASS: 'Crimsonfire Cutlass', ItemGlobals.EMBERFIRE_CUTLASS: 'Emberfire Cutlass', ItemGlobals.LIFE_STEALER_CUTLASS: 'Life Stealer Cutlass', ItemGlobals.SPIRIT_STEALER_CUTLASS: 'Spirit Stealer Cutlass', ItemGlobals.SOUL_STEALER_CUTLASS: 'Soul Stealer Cutlass', ItemGlobals.HEART_OF_PADRES_DEL_FUEGO: 'Heart of Padres del Fuego', ItemGlobals.LOST_SWORD_OF_EL_DORADO: 'Lost Sword of El Dorado', ItemGlobals.LOST_BLADE_OF_CALYPSO: 'Lost Blade of Calypso', ItemGlobals.JACK_SPARROW_BLADE: "Jack Sparrow's Blade", ItemGlobals.SWORD_OF_QUETZALCOATL: 'Sword of Quetzalcoatl', ItemGlobals.MONTEZUMA_BLADE: "Montezuma's Blade", ItemGlobals.SPECTRAL_CUTLASS: 'Spectral Cutlass', ItemGlobals.DARKFIRE_CUTLASS: 'Darkfire Cutlass', ItemGlobals.CONQUISTADOR_CUTLASS: "Conquistador's Cutlass", ItemGlobals.LOST_SWORD_OF_EL_PATRON: 'Lost Sword of El Patron', ItemGlobals.SHORT_CUTLASS: 'Short Cutlass', ItemGlobals.VOODOO_CUTLASS: 'Voodoo Cutlass', ItemGlobals.BATTLE_CUTLASS: 'Battle Cutlass', ItemGlobals.ORNATE_CUTLASS: 'Ornate Cutlass', ItemGlobals.GRAND_CUTLASS: 'Grand Cutlass', ItemGlobals.ROYAL_CUTLASS: 'Royal Cutlass', ItemGlobals.DUAL_RUSTY_CUTLASS: 'Dual Rusty Cutlasses', ItemGlobals.RUSTY_SABRE: 'Rusty Sabre', ItemGlobals.LIGHT_SABRE: 'Light Sabre', ItemGlobals.SHARP_SABRE: 'Sharp Sabre', ItemGlobals.TEMPERED_SABRE: 'Tempered Sabre', ItemGlobals.ENGRAVED_SABRE: 'Engraved Sabre', ItemGlobals.BEJEWELED_SABRE: 'Bejeweled Sabre', ItemGlobals.MASTERWORK_SABRE: 'Masterwork Sabre', ItemGlobals.NAVY_MARINE_SABRE: "Navy Marine's Sabre", ItemGlobals.NAVY_OFFICER_SABRE: "Navy Officer's Sabre", ItemGlobals.BOARDING_SABRE: 'Boarding Sabre', ItemGlobals.ORNATE_SABRE: 'Ornate Sabre', ItemGlobals.ROYAL_SABRE: 'Royal Sabre', ItemGlobals.FENCER_SABRE: "Fencer's Sabre", ItemGlobals.DUELIST_SABRE: "Duelist's Sabre", ItemGlobals.MUSKETEER_SABRE: "Musketeer's Sabre", ItemGlobals.MASTER_FENCER_SABRE: "Master Fencer's Sabre", ItemGlobals.SWORDSMAN_SABRE: "Swordsman's Sabre", ItemGlobals.SWORD_FIGHTER_SABRE: "Sword Fighter's Sabre", ItemGlobals.SWORD_MASTER_SABRE: "Sword Master's Sabre", ItemGlobals.VOODOO_HUNTER_SABRE: 'Voodoo Hunter Sabre', ItemGlobals.WITCH_HUNTER_SABRE: 'Witch Hunter Sabre', ItemGlobals.SABRE_OF_THE_INQUISITION: 'Sabre of the Inquisition', ItemGlobals.SILVER_SABRE: 'Silver Sabre', ItemGlobals.HOLY_SABRE: 'Holy Sabre', ItemGlobals.SACRED_SABRE: 'Sacred Sabre', ItemGlobals.DIVINE_SABRE: 'Divine Sabre', ItemGlobals.HAWK_SABRE: 'Hawk Sabre', ItemGlobals.FALCON_SABRE: 'Falcon Sabre', ItemGlobals.EAGLE_SABRE: 'Eagle Sabre', ItemGlobals.GREAT_HAWK_SABRE: 'Great Hawk Sabre', ItemGlobals.KINGFISHER_SABRE: 'Kingfisher Sabre', ItemGlobals.MARINER_SABRE: "Mariner's Sabre", ItemGlobals.QUARTER_MASTER_SABRE: "Quarter Master's Sabre", ItemGlobals.FIRST_MATE_SABRE: "First Mate's Sabre", ItemGlobals.LIEUTENANT_SABRE: "Lieutenant's Sabre", ItemGlobals.COMMANDER_SABRE: "Commander's Sabre", ItemGlobals.CAPTAIN_SABRE: "Captain's Sabre", ItemGlobals.COMMODORE_SABRE: "Commodore's Sabre", ItemGlobals.VICE_ADMIRAL_SABRE: "Vice Admiral's Sabre", ItemGlobals.ADMIRAL_SABRE: "Admiral's Sabre", ItemGlobals.BLOODFIRE_SABRE: 'Bloodfire Sabre', ItemGlobals.CRIMSONFIRE_SABRE: 'Crimsonfire Sabre', ItemGlobals.EMBERFIRE_SABRE: 'Emberfire Sabre', ItemGlobals.BANE_BLADE_SABRE: 'Bane Blade Sabre', ItemGlobals.BANE_FIRE_SABRE: 'Bane Fire Sabre', ItemGlobals.BANE_CURSE_SABRE: 'Bane Curse Sabre', ItemGlobals.LE_PORC_SABRE: "LePorc's Sabre", ItemGlobals.IRON_SABRE: 'Iron Sabre', ItemGlobals.STEEL_SABRE: 'Steel Sabre', ItemGlobals.FINE_SABRE: 'Fine Sabre', ItemGlobals.WAR_SABRE: 'War Sabre', ItemGlobals.MASTER_SABRE: 'Master Sabre', ItemGlobals.SCIMITAR_42: "Viper's Kiss", ItemGlobals.SCIMITAR_46: 'Desert Claw', ItemGlobals.SCIMITAR_47: 'Scimitar 47', ItemGlobals.SCIMITAR_48: 'Scimitar 48', ItemGlobals.WORN_BROADSWORD: 'Worn Broadsword', ItemGlobals.IRON_BROADSWORD: 'Iron Broadsword', ItemGlobals.LIGHT_BROADSWORD: 'Light Broadsword', ItemGlobals.HEAVY_BROADSWORD: 'Heavy Broadsword', ItemGlobals.WAR_BROADSWORD: 'War Broadsword', ItemGlobals.ROYAL_BROADSWORD: 'Royal Broadsword', ItemGlobals.BRUTE_BROADSWORD: "Brute's Broadsword", ItemGlobals.EITC_GRUNT_BROADSWORD: "EITC Grunt's Broadsword", ItemGlobals.EXECUTIONER_BROADSWORD: "Executioner's Broadsword", ItemGlobals.SHARP_BROADSWORD: 'Sharp Broadsword', ItemGlobals.TEMPERED_BROADSWORD: 'Tempered Broadsword', ItemGlobals.ENGRAVED_BROADSWORD: 'Engraved Broadsword', ItemGlobals.BEJEWELED_BROADSWORD: 'Bejeweled Broadsword', ItemGlobals.MASTERWORK_BROADSWORD: 'Masterwork Broadsword', ItemGlobals.MONKEY_BROADSWORD: 'Monkey Broadsword', ItemGlobals.BABOON_BROADSWORD: 'Baboon Broadsword', ItemGlobals.GORILLA_BROADSWORD: 'Gorilla Broadsword', ItemGlobals.VOODOO_HUNTER_BROADSWORD: 'Voodoo Hunter Broadsword', ItemGlobals.WITCH_HUNTER_BROADSWORD: 'Witch Hunter Broadsword', ItemGlobals.BROADSWORD_OF_THE_INQUISITION: 'Broadsword of the Inquisition', ItemGlobals.BANE_BLADE_BROADSWORD: 'Bane Blade Broadsword', ItemGlobals.BANE_FIRE_BROADSWORD: 'Bane Fire Broadsword', ItemGlobals.BANE_CURSE_BROADSWORD: 'Bane Curse Broadsword', ItemGlobals.MILITARY_BROADSWORD: 'Military Broadsword', ItemGlobals.SOLDIER_BROADSWORD: "Soldier's Broadsword", ItemGlobals.CAVALRY_BROADSWORD: 'Cavalry Broadsword', ItemGlobals.DRAGOON_BROADSWORD: "Dragoon's Broadsword", ItemGlobals.BRIGADIER_BROADSWORD: "Brigadier's Broadsword", ItemGlobals.GENERAL_BROADSWORD: "General's Broadsword", ItemGlobals.DARK_BROADSWORD: 'Dark Broadsword', ItemGlobals.SHADOW_BROADSWORD: 'Shadow Broadsword', ItemGlobals.FORBIDDEN_BROADSWORD: 'Forbidden Broadsword', ItemGlobals.FIGHTER_BROADSWORD: "Fighter's Broadsword", ItemGlobals.SAVAGE_BROADSWORD: 'Savage Broadsword', ItemGlobals.WARMONGER_BROADSWORD: "Warmonger's Broadsword", ItemGlobals.WARLORD_BROADSWORD: "Warlord's Broadsword", ItemGlobals.WAR_MASTER_BROADSWORD: "War Master's Broadsword", ItemGlobals.LIEUTENANT_BROADSWORD: "Lieutenant's Broadsword", ItemGlobals.COMMANDER_BROADSWORD: "Commander's Broadsword", ItemGlobals.CAPTAIN_BROADSWORD: "Captain's Broadsword", ItemGlobals.COMMODORE_BROADSWORD: "Vice Admiral's Broadsword", ItemGlobals.BLOODFIRE_BROADSWORD: 'Bloodfire Broadsword', ItemGlobals.CRIMSONFIRE_BROADSWORD: 'Crimsonfire Broadsword', ItemGlobals.EMBERFIRE_BROADSWORD: 'Emberfire Broadsword', ItemGlobals.BLACK_RAVEN_BROADSWORD: 'Black Raven Broadsword', ItemGlobals.VULTURE_CLAW_BROADSWORD: 'Vulture Claw Broadsword', ItemGlobals.IGNIS_MAXIMUS: 'Ignis Maximus', ItemGlobals.AVARICIA_BROADSWORD: "Avaricia's Broadsword", ItemGlobals.BARBOSSA_EDGE: "Barbossa's Edge", ItemGlobals.NEMESIS_BLADE: 'Nemesis Blade', ItemGlobals.SWORD_OF_TRITON: 'Sword of Triton', ItemGlobals.SMALL_BROADSWORD: 'Small Broadsword', ItemGlobals.STEEL_BROADSWORD: 'Steel Broadsword', ItemGlobals.MIGHTY_BROADSWORD: 'Mighty Broadsword', ItemGlobals.ORNATE_BROADSWORD: 'Ornate Broadsword', ItemGlobals.GREAT_BROADSWORD: 'Great Broadsword', ItemGlobals.SWORD_OF_DECAY: 'Sword of Decay', ItemGlobals.SPINESKULL_BLADE: 'Spineskull Blade', ItemGlobals.GRIM_HOUND_BLADE: 'Grim Hound Blade', ItemGlobals.SEA_STEEL_SWORD: 'Sea Steel Sword', ItemGlobals.BARNACLE_BREAKER: 'Barnacle Breaker', ItemGlobals.DEEPWATER_BLADE: 'Deepwater Blade', ItemGlobals.GRAVE_REAPER: 'Grave Reaper', ItemGlobals.PLAGUEFIRE_BLADE: 'Plaguefire Blade', ItemGlobals.VIPER_BLADE: 'Viper Blade', ItemGlobals.DOOM_RATTLER: 'Doom Rattler', ItemGlobals.NAUTILUS_BLADE: 'Nautilus Blade', ItemGlobals.WHALEBONE_BLADE: 'Whalebone Blade', ItemGlobals.THE_DARK_MUTINEER: 'The Dark Mutineer', ItemGlobals.RAZORTOOTH_SWORD: 'Razortooth Sword', ItemGlobals.SPINECREST_SWORD: 'Spinecrest Sword', ItemGlobals.RIPSAW_BLADE: 'Ripsaw Blade', ItemGlobals.SHARKFANG_BLADE: 'Sharkfang Blade', ItemGlobals.HULL_RIPPER: 'Hull Ripper', ItemGlobals.BARRACUDA_BLADE: 'Barracuda Blade', ItemGlobals.DREAD_SPIKE: 'Dread Spike', ItemGlobals.BITTER_END: 'Bitter End', ItemGlobals.DOOM_STINGER: 'Doom Stinger', ItemGlobals.TREACHERYS_EDGE: "Treachery's End", ItemGlobals.TYRANT_BLADE: 'Tyrant Blade', ItemGlobals.BLIGHTFANG_EDGE: 'Blightfang Edge', ItemGlobals.BEHEMOTH_BLADE: 'Behemoth Blade', ItemGlobals.THUNDERSPINE_SWORD: 'Thunderspine Sword', ItemGlobals.BLADE_OF_THE_ABYSS: 'Blade of the Abyss', ItemGlobals.WORLD_EATER_BLADE: 'World Eater Blade', ItemGlobals.THE_EMERALD_CURSE: 'The Emerald Curse', ItemGlobals.SEAFANG_BLADE: 'Cursed Seafang Blade', ItemGlobals.DARKFROST_BLADE: 'Dark Frost Blade', ItemGlobals.CURSED_BLADE_47: 'Lost Blade of Leviathan', ItemGlobals.FLINTLOCK_PISTOL: 'Flintlock Pistol', ItemGlobals.DOUBLE_BARREL: 'Double-Barrel', ItemGlobals.TRI_BARREL: 'Tri-Barrel', ItemGlobals.HEAVY_TRI_BARREL: 'Heavy Tri-Barrel', ItemGlobals.GRAND_PISTOL: 'Grand Pistol', ItemGlobals.WHEELLOCK_PISTOL: 'Wheellock Pistol', ItemGlobals.SNAPLOCK_PISTOL: 'Snaplock Pistol', ItemGlobals.SEA_DOG_PISTOL: 'Sea Dog Pistol', ItemGlobals.SWASHBUCKLER_PISTOL: "Swashbuckler's Pistol", ItemGlobals.BUCCANEER_PISTOL: "Buccaneer's Pistol", ItemGlobals.RATTLER_PISTOL: 'Rattler Pistol', ItemGlobals.COBRA_PISTOL: 'Cobra Pistol', ItemGlobals.BUSH_MASTER_PISTOL: 'Bush Master Pistol', ItemGlobals.SCALLYWAG_PISTOL: "Scallywag's Pistol", ItemGlobals.ROBBER_PISTOL: "Robber's Pistol", ItemGlobals.SCOUNDREL_PISTOL: "Scoundrel's Pistol", ItemGlobals.NIGHT_HUNTER_PISTOL: 'Night Hunter Pistol', ItemGlobals.SHADOW_STALKER_PISTOL: 'Shadow Stalker Pistol', ItemGlobals.FOUL_BANE_PISTOL: 'Foul Bane Pistol', ItemGlobals.FULLMOON_SPECIAL_PISTOL: 'Fullmoon Special Pistol', ItemGlobals.EITC_THUG_PISTOL: "EITC Thug's Pistol", ItemGlobals.NAVY_SERGEANT_PISTOL: "Navy Sergeant's Pistol", ItemGlobals.DUELIST_PISTOL: "Duelist's Pistol", ItemGlobals.EXECUTIONER_PISTOL: "Executioner's Pistol", ItemGlobals.SILVER_PISTOL: 'Silver Pistol', ItemGlobals.HOLY_PISTOL: 'Holy Pistol', ItemGlobals.SACRED_PISTOL: 'Sacred Pistol', ItemGlobals.RUNIC_PISTOL: 'Runic Pistol', ItemGlobals.WARDING_PISTOL: 'Warding Pistol', ItemGlobals.ARCANE_PISTOL: 'Arcane Pistol', ItemGlobals.BECKETTE_PISTOL: "Beckette's Pistol", ItemGlobals.MERCER_PISTOL: "Mercer's Pistol", ItemGlobals.JACK_SPARROW_REVENGE: "Jack Sparrow's Revenge", ItemGlobals.IRON_PISTOL: 'Iron Pistol', ItemGlobals.STEEL_PISTOL: 'Steel Pistol', ItemGlobals.ORNATE_PISTOL: 'Ornate Pistol', ItemGlobals.RUSTY_BAYONET: 'Rusty Bayonet', ItemGlobals.HAYMAKER_PISTOL: 'Haymaker Pistol', ItemGlobals.BARBOSSA_FURY: "Barbossa's Fury", ItemGlobals.FLINTLOCK_BAYONET: 'Flintlock Bayonet', ItemGlobals.WHEELLOCK_BAYONET: 'Wheellock Bayonet', ItemGlobals.SNAPLOCK_BAYONET: 'Snaplock Bayonet', ItemGlobals.COMBAT_BAYONET: 'Combat Bayonet', ItemGlobals.BATTLE_BAYONET: 'Battle Bayonet', ItemGlobals.WAR_BAYONET: 'War Bayonet', ItemGlobals.NAVY_CADET_BAYONET: "Navy Cadet's Bayonet", ItemGlobals.NAVY_GUARD_BAYONET: "Navy Guard's Bayonet", ItemGlobals.NAVY_MUSKETEER_BAYONET: "Navy Musketeer's Bayonet", ItemGlobals.NAVY_VETERAN_BAYONET: "Navy Veteran's Bayonet", ItemGlobals.NAVY_DRAGOON_BAYONET: "Navy Dragoon's Bayonet", ItemGlobals.CRAB_STICKER_BAYONET: 'Crab Sticker Bayonet', ItemGlobals.PIG_STICKER_BAYONET: 'Pig Sticker Bayonet', ItemGlobals.GATOR_STICKER_BAYONET: 'Gator Sticker Bayonet', ItemGlobals.SHARK_STICKER_BAYONET: 'Shark Sticker Bayonet', ItemGlobals.MILITIA_BAYONET: 'Militia Bayonet', ItemGlobals.MILITARY_BAYONET: 'Military Bayonet', ItemGlobals.SOLDIER_BAYONET: "Soldier's Bayonet", ItemGlobals.OFFICER_BAYONET: "Officer's Bayonet", ItemGlobals.BRIGADIER_BAYONET: "Brigadier's Bayonet", ItemGlobals.SEA_DOG_BAYONET: "Sea Dog's Bayonet", ItemGlobals.SWASHBUCKLER_BAYONET: "Swashbuckler's Bayonet", ItemGlobals.BUCCANEER_BAYONET: "Buccaneer's Bayonet", ItemGlobals.PRIVATEER_BAYONET: "Privateer's Bayonet", ItemGlobals.CORSAIR_BAYONET: "Corsair's Bayonet", ItemGlobals.IRON_BAYONET: 'Iron Bayonet', ItemGlobals.STEEL_BAYONET: 'Steel Bayonet', ItemGlobals.MASTER_BAYONET: 'Master Bayonet', ItemGlobals.ZOMBIE_KABAB_BAYONET: 'Zombie Kabab Bayonet', ItemGlobals.OLD_MUSKET: 'Old Musket', ItemGlobals.FLINTLOCK_MUSKET: 'Flintlock Musket', ItemGlobals.WHEELLOCK_MUSKET: 'Wheellock Musket', ItemGlobals.SEA_DOG_MUSKET: 'Sea Dog Musket', ItemGlobals.HOTSHOT_MUSKET: 'Hotshot Musket', ItemGlobals.BURNSHOT_MUSKET: 'Burnshot Musket', ItemGlobals.FLAMESHOT_MUSKET: 'Flameshot Musket', ItemGlobals.FIREBRAND_MUSKET: 'Firebrand Musket', ItemGlobals.SCALLYWAG_MUSKET: "Scallywag's Musket", ItemGlobals.ROBBER_MUSKET: "Robber's Musket", ItemGlobals.SCOUNDREL_MUSKET: "Scoundrel's Musket", ItemGlobals.GUNNER_MUSKET: "Gunner's Musket", ItemGlobals.RIFLEMAN_MUSKET: "Rifleman's Musket", ItemGlobals.MASTER_GUNNER_MUSKET: "Master Gunner's Musket", ItemGlobals.HUNTSMAN_MUSKET: "Huntsman's Musket", ItemGlobals.MARKSMAN_MUSKET: "Marksman's Musket", ItemGlobals.SNIPER_MUSKET: "Sniper's Musket", ItemGlobals.HEX_GUARD_MUSKET: 'Hex Guard Musket', ItemGlobals.HEX_STOPPER_MUSKET: 'Hex Stopper Musket', ItemGlobals.HEX_BREAKER_MUSKET: 'Hex Breaker Musket', ItemGlobals.SILVER_MUSKET: 'Silver Musket', ItemGlobals.HOLY_MUSKET: 'Holy Musket', ItemGlobals.SACRED_MUSKET: 'Sacred Musket', ItemGlobals.SAILOR_MUSKET: "Sailor's Musket", ItemGlobals.BOARDING_MUSKET: 'Boarding Musket', ItemGlobals.ROYAL_MUSKET: 'Royal Musket', ItemGlobals.CRACKED_BLUNDERBUSS: 'Cracked Blunderbuss', ItemGlobals.MATCHLOCK_BLUNDERBUSS: 'Matchlock Blunderbuss', ItemGlobals.FLINTLOCK_BLUNDERBUSS: 'Flintlock Blunderbuss', ItemGlobals.SCATTERGUN: 'Scattergun', ItemGlobals.HEAVY_SCATTERGUN: 'Heavy Scattergun', ItemGlobals.WAR_SCATTERGUN: 'War Scattergun', ItemGlobals.SEA_DOG_BLUNDERBUSS: 'Sea Dog Blunderbuss', ItemGlobals.SWASHBUCKLER_BLUNDERBUSS: "Swashbuckler's Blunderbuss", ItemGlobals.BUCCANEER_BLUNDERBUSS: "Buccaneer's Blunderbuss", ItemGlobals.MONKEY_BLUNDERBUSS: 'Monkey Blunderbuss', ItemGlobals.BABOON_BLUNDERBUSS: 'Baboon Blunderbuss', ItemGlobals.GORILLA_BLUNDERBUSS: 'Gorilla Blunderbuss', ItemGlobals.NAVY_BLUNDERBUSS: 'Navy Blunderbuss', ItemGlobals.EITC_BLUNDERBUSS: 'EITC Blunderbuss', ItemGlobals.PIRATE_BLUNDERBUSS: 'Pirate Blunderbuss', ItemGlobals.GRAND_BLUNDERBUSS: 'Grand Blunderbuss', ItemGlobals.HUNTER_BLUNDERBUSS: "Hunter's Blunderbuss", ItemGlobals.HIRED_GUN_BLUNDERBUSS: "Hired-gun's Blunderbuss", ItemGlobals.MERCENARY_BLUNDERBUSS: "Mercenary's Blunderbuss", ItemGlobals.BOUNTY_HUNTER_BLUNDERBUSS: "Bounty Hunter's Blunderbuss", ItemGlobals.NIGHT_HUNTER_BLUNDERBUSS: 'Night Hunter Blunderbuss', ItemGlobals.SHADOW_STALKER_BLUNDERBUSS: 'Shadow Stalker Blunderbuss', ItemGlobals.FOUL_BANE_BLUNDERBUSS: 'Foul Bane Blunderbuss', ItemGlobals.FULLMOON_SPECIAL_BLUNDERBUSS: 'Fullmoon Special Blunderbuss', ItemGlobals.RUNIC_BLUNDERBUSS: 'Runic Blunderbuss', ItemGlobals.WARDING_BLUNDERBUSS: 'Warding Blunderbuss', ItemGlobals.ARCANE_BLUNDERBUSS: 'Arcane Blunderbuss', ItemGlobals.SMALL_BLUNDERBUSS: 'Small Blunderbuss', ItemGlobals.FINE_BLUNDERBUSS: 'Fine Blunderbuss', ItemGlobals.ROYAL_BLUNDERBUSS: 'Royal Blunderbuss', ItemGlobals.EITC_GRUNT_REPEATER: "EITC Grunt's Repeater Pistol", ItemGlobals.EITC_HIRED_GUN_REPEATER: "EITC Hired-gun's Repeater Pistol", ItemGlobals.EITC_MERCENARY_REPEATER: "EITC Mercenary's Repeater Pistol", ItemGlobals.WICKED_REPEATER: 'Wicked Repeater', ItemGlobals.DREAD_REPEATER: 'Dread Repeater', ItemGlobals.BANEBLAST_REPEATER: 'Baneblast Repeater', ItemGlobals.SKULLBONE_REPEATER: 'Skullbone Repeater', ItemGlobals.NIGHT_HUNTER_REPEATER: 'Night Hunter Repeater', ItemGlobals.SHADOW_STALKER_REPEATER: 'Shadow Stalker Repeater', ItemGlobals.FOUL_BANE_REPEATER: 'Foul Bane Repeater', ItemGlobals.FULLMOON_SPECIAL_REPEATER: 'Fullmoon Special Repeater', ItemGlobals.MONKEY_REPEATER: 'Monkey Repeater', ItemGlobals.BABOON_REPEATER: 'Baboon Repeater', ItemGlobals.ORANGUTAN_REPEATER: 'Orangutan Repeater', ItemGlobals.GORILLA_REPEATER: 'Gorilla Repeater', ItemGlobals.SEA_DOG_REPEATER: 'Sea Dog Repeater', ItemGlobals.SWASHBUCKLER_REPEATER: "Swashbuckler's Repeater", ItemGlobals.BUCCANEER_REPEATER: "Buccaneer's Repeater", ItemGlobals.PRIVATEER_REPEATER: "Privateer's Repeater Pistol", ItemGlobals.CORSAIR_REPEATER: "Corsair's Repeater Pistol", ItemGlobals.SEVEN_SEAS_REPEATER: 'Seven Seas Repeater', ItemGlobals.RUNIC_REPEATER: 'Runic Repeater', ItemGlobals.WARDING_REPEATER: 'Warding Repeater', ItemGlobals.ARCANE_REPEATER: 'Arcane Repeater', ItemGlobals.CABAL_REPEATER: 'Cabal Repeater', ItemGlobals.ENHANCED_REPEATER: 'Enhanced Repeater Pistol', ItemGlobals.CLOCKWORK_REPEATER: 'Clockwork Repeater Pistol', ItemGlobals.GATLING_REPEATER: 'Gatling Repeater Pistol', ItemGlobals.MASTER_CRAFTED_REPEATER: 'Master Crafted Repeater Pistol', ItemGlobals.DARK_REPEATER_PISTOL: 'Dark Repeater Pistol', ItemGlobals.SHADOW_REPEATER_PISTOL: 'Shadow Repeater Pistol', ItemGlobals.FORBIDDEN_REPEATER_PISTOL: 'Forbidden Repeater Pistol', ItemGlobals.SILVER_REPEATER_PISTOL: 'Silver Repeater Pistol', ItemGlobals.HOLY_REPEATER_PISTOL: 'Holy Repeater Pistol', ItemGlobals.SACRED_REPEATER_PISTOL: 'Sacred Repeater Pistol', ItemGlobals.TWIN_BARREL_PISTOL: 'Twin Barrel Pistol', ItemGlobals.STEEL_REPEATER: 'Steel Repeater', ItemGlobals.ORNATE_REPEATER: 'Ornate Repeater', ItemGlobals.VOLLEY_PISTOL: 'Volley Pistol', ItemGlobals.VOODOO_DOLL: 'Voodoo Doll', ItemGlobals.CLOTH_DOLL: 'Cloth Doll', ItemGlobals.WITCH_DOLL: 'Witch Doll', ItemGlobals.PIRATE_DOLL: 'Pirate Doll', ItemGlobals.TABOO_DOLL: 'Taboo Doll', ItemGlobals.UGLY_DOLL: 'Ugly Voodoo Doll', ItemGlobals.ZOMBIE_DOLL: 'Zombie Doll', ItemGlobals.GHOUL_DOLL: 'Ghoul Doll', ItemGlobals.HYPNOTIC_DOLL: 'Hypnotic Doll', ItemGlobals.MANIPULATION_DOLL: 'Manipulation Doll', ItemGlobals.MIND_CONTROL_DOLL: 'Mind Control Doll', ItemGlobals.DOMINATION_DOLL: 'Domination Doll', ItemGlobals.EVIL_DOLL: 'Evil Doll', ItemGlobals.WICKED_DOLL: 'Wicked Doll', ItemGlobals.UNHOLY_DOLL: 'Unholy Doll', ItemGlobals.VILLAINY_DOLL: 'Villainy Doll', ItemGlobals.TYRANNY_DOLL: 'Tyranny Doll', ItemGlobals.SKELETON_DOLL: 'Skeleton Doll', ItemGlobals.CEMETERY_DOLL: 'Cemetery Doll', ItemGlobals.CRYPT_DOLL: 'Crypt Doll', ItemGlobals.CARRION_DOLL: 'Carrion Doll', ItemGlobals.REVENANT_DOLL: 'Revenant Doll', ItemGlobals.TOMB_KING_DOLL: 'Tomb King Doll', ItemGlobals.SWASHBUCKLER_DOLL: 'Swashbuckler Doll', ItemGlobals.BUCCANEER_DOLL: 'Buccaneer Doll', ItemGlobals.MUTINEER_DOLL: 'Mutineer Doll', ItemGlobals.PRIVATEER_DOLL: 'Privateer Doll', ItemGlobals.WARMONGER_DOLL: 'Warmonger Doll', ItemGlobals.BARBOSSA_DOLL: 'Barbossa Doll', ItemGlobals.DARK_DOLL: 'Dark Voodoo Doll', ItemGlobals.SHADOW_DOLL: 'Shadow Voodoo Doll', ItemGlobals.FORBIDDEN_DOLL: 'Forbidden Voodoo Doll', ItemGlobals.JOLLY_ROGER_DOLL: 'Jolly Roger Voodoo Doll', ItemGlobals.CURSED_DOLL: 'Cursed Doll', ItemGlobals.TORMENTED_DOLL: 'Tormented Voodoo Doll', ItemGlobals.OVERLORD_DOLL: 'Overlord Voodoo Doll', ItemGlobals.DAVY_JONES_DOLL: 'Davy Jones Voodoo Doll', ItemGlobals.FURY_DOLL: 'Fury Doll', ItemGlobals.RAGE_DOLL: 'Rage Doll', ItemGlobals.GRUDGER_DOLL: 'Grudger Doll', ItemGlobals.VENGEFUL_DOLL: 'Vengeful Doll', ItemGlobals.WRATH_DOLL: 'Wrath Doll', ItemGlobals.WAX_DOLL: 'Wax Doll', ItemGlobals.CLAY_DOLL: 'Clay Doll', ItemGlobals.SILK_DOLL: 'Silk Doll', ItemGlobals.ORIENTAL_DOLL: 'Oriental Doll', ItemGlobals.WARRIOR_DOLL: 'Warrior Doll', ItemGlobals.NOMAD_DOLL: 'Nomad Doll', ItemGlobals.WARLORD_DOLL: 'Warlord Doll', ItemGlobals.SHAO_FENG_DOLL: 'Shao Feng Doll', ItemGlobals.WITCH_DOCTOR_DOLL: 'Witch Doctor Doll', ItemGlobals.BEWITCHER_DOLL: 'Bewitcher Doll', ItemGlobals.SIREN_DOLL: 'Siren Doll', ItemGlobals.OCCULT_DOLL: 'Occult Doll', ItemGlobals.BANSHEE_DOLL: 'Banshee Doll', ItemGlobals.BLACK_MAGIC_DOLL: 'Black Magic Doll', ItemGlobals.MYSTIC_DOLL: 'Mystic Doll', ItemGlobals.PRIESTESS_DOLL: 'Priestess Doll', ItemGlobals.GYPSY_DOLL: 'Gypsy Doll', ItemGlobals.SHAMAN_DOLL: 'Shaman Doll', ItemGlobals.CABAL_DOLL: 'Cabal Doll', ItemGlobals.TIA_DALMA_DOLL: "Tia Dalma's Doll", ItemGlobals.STRAW_DOLL: 'Straw Doll', ItemGlobals.WARDING_DOLL: 'Warding Doll', ItemGlobals.HEX_WATCHER_DOLL: 'Hex Watcher Doll', ItemGlobals.SPELL_BINDER_DOLL: 'Spell Binder Doll', ItemGlobals.CURSE_BREAKER_DOLL: 'Curse Breaker Doll', ItemGlobals.JACK_SPARROW_DOLL: "Jack Sparrow's Voodoo Doll", ItemGlobals.HEX_REFLECTER_DOLL: 'Hex Reflecter Doll', ItemGlobals.HEX_REBOUND_DOLL: 'Hex Rebound Doll', ItemGlobals.HEX_GUARDIAN_DOLL: 'Hex Guardian Doll', ItemGlobals.CALYPSO_RADIANCE: "Calypso's Radiance", ItemGlobals.COTTON_SOLL: 'Cotton Doll', ItemGlobals.ORNATE_DOLL: 'Ornate Doll', ItemGlobals.ENCHANTED_DOLL: 'Enchanted Doll', ItemGlobals.MAGIC_DOLL: 'Magic Doll', ItemGlobals.MYSTERIOUS_DOLL: 'Mysterious Doll', ItemGlobals.RAG_DOLL: 'Rag Doll', ItemGlobals.CUPIE_DOLL: 'Cupie Doll', ItemGlobals.GAZE_BINDER_DOLL: 'Gaze Binder Doll', ItemGlobals.SIGHT_BINDER_DOLL: 'Sight Binder Doll', ItemGlobals.FAR_BINDER_DOLL: 'Far Binder Doll', ItemGlobals.SPIRIT_BINDER_DOLL: 'Spirit Binder Doll', ItemGlobals.SOUL_BINDER_DOLL: 'Soul Binder Doll', ItemGlobals.MONKEY_DOLL: 'Monkey Doll', ItemGlobals.CHIMPANZEE_DOLL: 'Chimpanzee Doll', ItemGlobals.BABOON_DOLL: 'Baboon Doll', ItemGlobals.ORANGUTAN_DOLL: 'Orangutan Doll', ItemGlobals.GORILLA_DOLL: 'Gorilla Doll', ItemGlobals.JACK_THE_MONKEY_DOLL: 'Jack the Monkey Doll', ItemGlobals.DOLL_OF_CLEANSING: 'Doll of Cleansing', ItemGlobals.DOLL_OF_PURIFICATION: 'Doll of Purification', ItemGlobals.DOLL_OF_SACRED_RITUALS: 'Doll of Sacred Rituals', ItemGlobals.SAILOR_DOLL: 'Sailor Doll', ItemGlobals.SEAFARER_DOLL: 'Seafarer Doll', ItemGlobals.TRAVELER_DOLL: 'Traveler Doll', ItemGlobals.VOYAGER_DOLL: 'Voyager Doll', ItemGlobals.EXPLORER_DOLL: 'Explorer Doll', ItemGlobals.ADVENTURER_DOLL: 'Adventurer Doll', ItemGlobals.ELIZABETH_SWAN_DOLL: 'Elizabeth Swan Doll', ItemGlobals.SOLDIER_DOLL: 'Soldier Doll', ItemGlobals.HERO_DOLL: 'Hero Doll', ItemGlobals.FENCER_DOLL: 'Fencer Doll', ItemGlobals.SWORDSMAN_DOLL: 'Swordsman Doll', ItemGlobals.CONQUISTADOR_DOLL: 'Conquistador Doll', ItemGlobals.TREASURE_HUNTER_DOLL: 'Treasure Hunter Doll', ItemGlobals.WILL_TURNER_DOLL: 'Will Turner Doll', ItemGlobals.HEALING_DOLL: 'Healing Doll', ItemGlobals.MENDING_DOLL: 'Mending Doll', ItemGlobals.RESTORATION_DOLL: 'Restoration Doll', ItemGlobals.RENEWAL_DOLL: 'Renewal Doll', ItemGlobals.LIFE_DOLL: 'Life Doll', ItemGlobals.BASIC_DAGGER: 'Dagger', ItemGlobals.BATTLE_DIRK: 'Battle Dirk', ItemGlobals.MAIN_GAUCHE: 'Main Gauche', ItemGlobals.COLTELLO: 'Coltello', ItemGlobals.BLOODLETTER: 'Bloodletter', ItemGlobals.GRAVEDIGGER_DAGGER: "Gravedigger's Dagger", ItemGlobals.MUTINEER_DAGGER: "Mutineer's Dagger", ItemGlobals.BRIGAND_DAGGER: "Brigand's Dagger", ItemGlobals.DUELIST_DAGGER: "Duelist's Dagger", ItemGlobals.EITC_THUG_DAGGER: "EITC Thug's Dagger", ItemGlobals.EITC_HIRED_GUN_DAGGER: "EITC Hiredgun's Dagger", ItemGlobals.EITC_ASSASSIN_DAGGER: "EITC Assassin's Dagger", ItemGlobals.SURVIVAL_DAGGER: 'Survival Dagger', ItemGlobals.WILDERNESS_DAGGER: 'Wilderness Dagger', ItemGlobals.JUNGLE_DAGGER: 'Jungle Dagger', ItemGlobals.SWAMP_DAGGER: 'Swamp Dagger', ItemGlobals.BAYOU_DAGGER: 'Bayou Dagger', ItemGlobals.BACKSTABBER_DAGGER: 'Backstabber Dagger', ItemGlobals.BACK_BITER_DAGGER: 'Back Biter Dagger', ItemGlobals.DEAL_BREAKER_DAGGER: 'Deal Breaker Dagger', ItemGlobals.DOUBLE_CROSS_DAGGER: 'Double Cross Dagger', ItemGlobals.TRAITOR_DAGGER: "Traitor's Dagger", ItemGlobals.CUTTHROAT_DAGGER: "Cutthroat's Dagger", ItemGlobals.SEA_DOG_DAGGER: "Sea Dog's Dagger", ItemGlobals.SWASHBUCKLER_DAGGER: "Swashbuckler's Dagger", ItemGlobals.BUCCANEER_DAGGER: "Buccaneer's Dagger", ItemGlobals.PRIVATEER_DAGGER: "Privateer's Dagger", ItemGlobals.CORSAIR_DAGGER: "Corsair's Dagger", ItemGlobals.SEVEN_SEAS_DAGGER: 'Seven Seas Dagger', ItemGlobals.DAGGER_OF_THE_SUN_IDOL: 'Dagger of the Sun Idol', ItemGlobals.DAGGER_OF_THE_MOON_IDOL: 'Dagger of the Moon Idol', ItemGlobals.DAGGER_OF_THE_HAWK_IDOL: 'Dagger of the Hawk Idol', ItemGlobals.DAGGER_OF_THE_BEAR_IDOL: 'Dagger of the Bear Idol', ItemGlobals.DAGGER_OF_THE_GOLDEN_IDOL: 'Dagger of the Golden Idol', ItemGlobals.DAGGER_OF_THE_DARK_IDOL: 'Dagger of the Dark Idol', ItemGlobals.SMALL_DAGGER: 'Small Dagger', ItemGlobals.STEEL_DAGGER: 'Steel Dagger', ItemGlobals.COMBAT_DAGGER: 'Combat Dagger', ItemGlobals.BATTLE_DAGGER: 'Battle Dagger', ItemGlobals.WAR_DAGGER: 'War Dagger', ItemGlobals.RUSTY_THROWING_KNIVES: 'Rusty Throwing Knives', ItemGlobals.BALANCED_THROWING_KNIVES: 'Balanced Throwing Knives', ItemGlobals.CUTLERY_SET: 'Cutlery Set', ItemGlobals.RAIDER_THROWING_KNIVES: "Raider's Throwing Knives", ItemGlobals.ASP_DEN_KNIVES: "Asp's Den Knives", ItemGlobals.ADDER_DEN_KNIVES: "Adder's Den Knives", ItemGlobals.SIDEWINDER_DEN_KNIVES: "Sidewinder's Den Knives", ItemGlobals.VIPER_DEN_KNIVES: "Viper's Den Knives", ItemGlobals.SCALLYWAG_KNIVES: "Scallywag's Knives", ItemGlobals.ROBBER_KNIVES: "Robber's Knives", ItemGlobals.SCOUNDREL_KNIVES: "Scoundrel's Knives", ItemGlobals.BLACK_FANG_KNIVES: 'Black Fang Knives', ItemGlobals.GRIM_FANG_KNIVES: 'Grim Fang Knives', ItemGlobals.RAVEN_FANG_KNIVES: 'Raven Fang Knives', ItemGlobals.SHARK_FANG_KNIVES: 'Shark Fang Knives', ItemGlobals.DEMON_FANG_KNIVES: 'Demon Fang Knives', ItemGlobals.KNIVES_OF_THE_SUN_IDOL: 'Knives of the Sun Idol', ItemGlobals.KNIVES_OF_THE_HAWK_IDOL: 'Knives of the Hawk Idol', ItemGlobals.KNIVES_OF_THE_GOLDEN_IDOL: 'Knives of the Golden Idol', ItemGlobals.SURVIVAL_THROWING_KNIVES: 'Survival Throwing Knives', ItemGlobals.WILDERNESS_THROWING_KNIVES: 'Wilderness Throwing Knives', ItemGlobals.JUNGLE_THROWING_KNIVES: 'Jungle Throwing Knives', ItemGlobals.SWAMP_THROWING_KNIVES: 'Swamp Throwing Knives', ItemGlobals.BAYOU_THROWING_KNIVES: 'Bayou Throwing Knives', ItemGlobals.HUNTER_THROWING_KNIVES: "Hunter's Throwing Knives", ItemGlobals.AZTEC_THROWING_KNIVES: 'Aztec Throwing Knives', ItemGlobals.MARKSMAN_THROWING_KNIVES: "Marksman's Throwing Knives", ItemGlobals.AMAZON_THROWING_KNIVES: 'Amazon Throwing Knives', ItemGlobals.ASSASSIN_THROWING_KNIVES: "Assassin's Throwing Knives", ItemGlobals.SILVER_FREEZE: 'Silver Freeze', ItemGlobals.SMALL_THROWING_KNIVES: 'Small Throwing Knives', ItemGlobals.IRON_THROWING_KNIVES: 'Iron Throwing Knives', ItemGlobals.TRIBAL_THROWING_KNIVES: 'Tribal Throwing Knives', ItemGlobals.FINE_THROWING_KNIVES: 'Fine Throwing Knives', ItemGlobals.MASTER_THROWING_KNIVES: 'Master Throwing Knives', ItemGlobals.CEREMONIAL_KNIVE: 'Ceremonial Knife', ItemGlobals.TRIBAL_KNIFE: 'Tribal Knife', ItemGlobals.RITUAL_KNIFE: 'Ritual Knife', ItemGlobals.KNIFE_OF_THE_BLOOD_IDOL: 'Knife of the Blood Idol', ItemGlobals.KNIFE_OF_THE_JACKAL_IDOL: 'Knife of the Jackal Idol', ItemGlobals.KNIFE_OF_THE_RAVEN_IDOL: 'Knife of the Raven Idol', ItemGlobals.KNIFE_OF_THE_WAR_IDOL: 'Knife of the War Idol', ItemGlobals.KNIFE_OF_THE_DEMON_IDOL: 'Knife of the Demon Idol', ItemGlobals.KNIFE_OF_THE_DEATH_IDOL: 'Knife of the Death Idol', ItemGlobals.GRIM_STRIKE_KNIFE: 'Grim Strike Knife', ItemGlobals.BLIGHT_STRIKE_KNIFE: 'Blight Strike Knife', ItemGlobals.DECAY_STRIKE_KNIFE: 'Decay Strike Knife', ItemGlobals.FATAL_STRIKE_KNIFE: 'Fatal Strike Knife', ItemGlobals.DEATH_STRIKE_KNIFE: 'Death Strike Knife', ItemGlobals.NIGHT_HUNTER_KNIFE: 'Night Hunter Knife', ItemGlobals.NIGHT_CHASER_KNIFE: 'Night Chaser Knife', ItemGlobals.NIGHT_STALKER_KNIFE: 'Night Stalker Knife', ItemGlobals.NIGHT_PREDATOR_KNIFE: 'Night Predator Knife', ItemGlobals.SNAKE_VENOM_KNIFE: 'Snake Venom Knife', ItemGlobals.VIPER_VENOM_KNIFE: 'Viper Venom Knife', ItemGlobals.COPPERHEAD_VENOM_KNIFE: 'Copperhead Venom Knife', ItemGlobals.MAMBA_VENOM_KNIFE: 'Mamba Venom Knife', ItemGlobals.COBRA_VENOM_KNIFE: 'Cobra Venom Knife', ItemGlobals.POISONED_KNIFE: 'Poisoned Knife', ItemGlobals.VENOM_KNIFE: 'Venomous Knife', ItemGlobals.TOXIC_KNIFE: 'Toxic Knife', ItemGlobals.PLAGUE_KNIFE: 'Plague Knife', ItemGlobals.DIRE_KNIFE: 'Dire Knife', ItemGlobals.CURSED_STAFF: 'Cursed Staff', ItemGlobals.WARPED_STAFF: 'Warped Staff', ItemGlobals.REND_STAFF: 'Rend Staff', ItemGlobals.HARROW_STAFF: 'Harrow Staff', ItemGlobals.VILE_STAFF: 'Vile Staff', ItemGlobals.DREAD_STAFF: 'Dread Staff', ItemGlobals.HAUNTED_STAFF: 'Haunted Staff', ItemGlobals.POSSESSED_STAFF: 'Possessed Staff', ItemGlobals.PHANTOM_STAFF: 'Phantom Staff', ItemGlobals.SKULL_STAFF: 'Skull Staff', ItemGlobals.DIRE_STAFF: 'Dire Staff', ItemGlobals.DIABOLIC_STAFF: 'Diabolic Staff', ItemGlobals.DEMON_SKULL_STAFF: 'Demon Skull Staff', ItemGlobals.SINGED_STAFF: 'Singed Staff', ItemGlobals.BURNT_STAFF: 'Burnt Staff', ItemGlobals.CHARRED_STAFF: 'Charred Staff', ItemGlobals.CAJUN_STAFF: 'Cajun Staff', ItemGlobals.SPIRIT_CALLER_STAFF: 'Spirit Caller Staff', ItemGlobals.SPIRIT_BINDER_STAFF: 'Spirit Burner Staff', ItemGlobals.SPIRIT_SHREDDER_STAFF: 'Spirit Shredder Staff', ItemGlobals.SOUL_HARVESTER_STAFF: 'Soul Harvester Staff', ItemGlobals.SOUL_REAPER_STAFF: 'Soul Reaper Staff', ItemGlobals.SOUL_EATER_STAFF: 'Soul Eater Staff', ItemGlobals.DARK_OMEN: 'Dark Omen', ItemGlobals.BONE_STAFF: 'Bone Staff', ItemGlobals.GRIM_STAFF: 'Grim Staff', ItemGlobals.SKELETAL_STAFF: 'Skeletal Staff', ItemGlobals.UNDEAD_STAFF: 'Undead Staff', ItemGlobals.DEATH_STAFF: 'Death Staff', ItemGlobals.ROTTEN_STAFF: 'Rotten Staff', ItemGlobals.JUJU_STAFF: 'Juju Staff', ItemGlobals.ANTIVENOM_STAFF: 'Anti-venom Staff', ItemGlobals.RESISTANCE_STAFF: 'Resistance Staff', ItemGlobals.REGROWTH_STAFF: 'Regrowth Staff', ItemGlobals.STAFF_OF_MISTS: 'Staff of Mists', ItemGlobals.STAFF_OF_RAIN: 'Staff of Rain', ItemGlobals.STAFF_OF_STORMS: 'Staff of Storms', ItemGlobals.BOA_STAFF: 'Boa Staff', ItemGlobals.PYTHON_STAFF: 'Python Staff', ItemGlobals.SERPENT_STAFF: 'Serpent Staff', ItemGlobals.MISSHAPEN_STAFF: 'Misshapen Staff', ItemGlobals.TWISTED_STAFF: 'Twisted Staff', ItemGlobals.GNARLED_STAFF: 'Gnarled Staff', ItemGlobals.ANCIENT_STAFF: 'Ancient Staff', ItemGlobals.STONE_GUARD_STAFF: 'Stone Guard Staff', ItemGlobals.GRANITE_GUARD_STAFF: 'Granite Guard Staff', ItemGlobals.EARTH_GUARD_STAFF: 'Earth Guard Staff', ItemGlobals.HEALING_STAFF: 'Healing Staff', ItemGlobals.MENDING_STAFF: 'Mending Staff', ItemGlobals.RESTORATION_STAFF: 'Restoration Staff', ItemGlobals.RENEWAL_STAFF: 'Renewal Staff', ItemGlobals.LIFE_STAFF: 'Life Staff', ItemGlobals.TRIBAL_STAFF: 'Tribal Staff', ItemGlobals.STAFF_OF_CLEANSING: 'Staff of Cleansing', ItemGlobals.STAFF_OF_PURIFICATION: 'Staff of Purification', ItemGlobals.STAFF_OF_SACRED_RITUALS: 'Staff of Sacred Rituals', ItemGlobals.STAFF_OF_PROTECTION: 'Staff of Protection', ItemGlobals.STAFF_OF_WARDING: 'Staff of Warding', ItemGlobals.STAFF_OF_SHIELDING: 'Staff of Shielding', ItemGlobals.STAFF_OF_DEFIANCE: 'Staff of Defiance', ItemGlobals.STAFF_OF_SANCTUARY: 'Staff of Sanctuary', ItemGlobals.SAGE_STAFF: 'Sage Staff', ItemGlobals.RITUAL_STAFF: 'Ritual Staff', ItemGlobals.BANISHING_STAFF: 'Banishing Staff', ItemGlobals.TABOO_STAFF: 'Taboo Staff', ItemGlobals.EXORCISM_STAFF: 'Exorcism Staff', ItemGlobals.STAFF_OF_THE_SACRED_OWL: 'Staff of the Sacred Owl', ItemGlobals.STAFF_OF_THE_SACRED_MOON: 'Staff of the Sacred Moon', ItemGlobals.STAFF_OF_THE_SACRED_STARS: 'Staff of the Sacred Stars', ItemGlobals.STAFF_OF_THE_SACRED_SUN: 'Staff of the Sacred Sun', ItemGlobals.DEFENDER_STAFF: 'Defender Staff', ItemGlobals.WARDEN_STAFF: 'Warden Staff', ItemGlobals.OVERSEER_STAFF: 'Overseer Staff', ItemGlobals.GUARDIAN_STAFF: 'Guardian Staff', ItemGlobals.TRIBAL_CHIEF_STAFF: 'Tribal Chief Staff', ItemGlobals.GRENADE_POUCH: 'Grenade Pouch', ItemGlobals.OLD_CANNON_RAM: 'Old Cannon Ram', ItemGlobals.HASTY_CANNON_RAM: 'Hasty Cannon Ram', ItemGlobals.GUNNERS_CANNON_RAM: "Gunner's Cannon Ram", ItemGlobals.MASTER_GUNNERS_CANNON_RAM: "Master Gunner's Cannon Ram", ItemGlobals.GREYHOUND_CANNON_RAM: 'Greyhound Cannon Ram', ItemGlobals.BLOODHOUND_CANNON_RAM: 'Bloodhound Cannon Ram', ItemGlobals.MAKESHIFT_CANNON_RAM: 'Makeshift Cannon Ram', ItemGlobals.MANOWAR_CANNON_RAM: 'Man-o-War Cannon Ram', ItemGlobals.JUGGERNAUT_CANNON_RAM: 'Juggernaut Cannon Ram', ItemGlobals.MARAUDER_CANNON_RAM: 'Marauder Cannon Ram', ItemGlobals.CERBERUS_CANNON_RAM: 'Cerberus Cannon Ram', ItemGlobals.PHANTOM_CANNON_RAM: 'Phantom Cannon Ram', ItemGlobals.STORMREAPER_CANNON_RAM: 'Storm Reaper Cannon Ram', ItemGlobals.REVENANT_CANNON_RAM: 'Revenant Cannon Ram', ItemGlobals.SHADOW_CROW_CANNON_RAM: 'Shadow Crow Cannon Ram', ItemGlobals.BRONZE_CANNON_RAM: 'Bronze Cannon Ram', ItemGlobals.IRON_CANNON_RAM: 'Iron Cannon Ram', ItemGlobals.STEEL_CANNON_RAM: 'Steel Cannon Ram', ItemGlobals.COTTON_CANNON_RAM: 'Cotton Cannon Ram', ItemGlobals.WOOL_CANNON_RAM: 'Wool Cannon Ram', ItemGlobals.SPONGE_CANNON_RAM: 'Sponge Cannon Ram', ItemGlobals.FLEECE_CANNON_RAM: 'Fleece Cannon Ram', ItemGlobals.FIERY_CANNON_RAM: 'Fiery Cannon Ram', ItemGlobals.SEARING_CANNON_RAM: 'Searing Cannon Ram', ItemGlobals.CAJUN_CANNON_RAM: 'Cajun Cannon Ram', ItemGlobals.HAUNTED_CANNON_RAM: 'Haunted Cannon Ram', ItemGlobals.SPECTRAL_CANNON_RAM: 'Spectral Cannon Ram', ItemGlobals.POSSESSED_CANNON_RAM: 'Possessed Cannon Ram', ItemGlobals.LADLE_CANNON_RAM: 'Ladle Cannon Ram', ItemGlobals.COPPER_LADLE_CANNON_RAM: 'Copper Ladle Cannon Ram', ItemGlobals.CLOTH_CANNON_RAM: 'Cloth Cannon Ram', ItemGlobals.PADDED_CANNON_RAM: 'Padded Cannon Ram', ItemGlobals.PRIMING_RAM: 'Priming Ram', ItemGlobals.IRON_PRIMING_RAM: 'Iron Priming Ram', ItemGlobals.BURNT_CANNON_RAM: 'Burnt Cannon Ram', ItemGlobals.CHARRED_CANNON_RAM: 'Charred Cannon Ram', ItemGlobals.ROTTEN_CANNON_RAM: 'Rotten Cannon Ram', ItemGlobals.WICKED_CANNON_RAM: 'Wicked Cannon Ram', ItemGlobals.ORIENTAL_SPYGLASS: 'Oriental Spyglass', ItemGlobals.GOLDEN_SPYGLASS: 'Golden Spyglass', ItemGlobals.SINGAPOREAN_SPYGLASS: 'Singaporean Spyglass', ItemGlobals.SEADOG_SPYGLASS: "Sea Dog's Spyglass", ItemGlobals.PIRATE_SPYGLASS: "Pirate's Spyglass", ItemGlobals.RAIDER_SPYGLASS: "Raider's Spyglass", ItemGlobals.MERCHANT_SPYGLASS: "Merchant's Spyglass", ItemGlobals.SMUGGLER_SPYGLASS: "Smuggler's Spyglass", ItemGlobals.RUMRUNNER_SPYGLASS: "Rumrunner's Spyglass", ItemGlobals.THIEVES_SPYGLASS: 'Thieves Spyglass', ItemGlobals.QUARTER_MASTER_SPYGLASS: "Quarter Master's Spyglass", ItemGlobals.FIRST_MATE_SPYGLASS: "First Mate's Spyglass", ItemGlobals.CAPTAIN_SPYGLASS: "Captain's Spyglass", ItemGlobals.COMMODORE_SPYGLASS: "Commodore's Spyglass", ItemGlobals.MARINER_SPYGLASS: "Mariner's Spyglass", ItemGlobals.LIEUTENANT_SPYGLASS: "Lieutenant's Spyglass", ItemGlobals.COMMANDER_SPYGLASS: "Commander's Spyglass", ItemGlobals.ADMIRAL_SPYGLASS: "Admiral's Spyglass", ItemGlobals.SWASHBUCKLER_SPYGLASS: "Swashbuckler's Spyglass", ItemGlobals.BUCCANEER_SPYGLASS: "Buccaneer's Spyglass", ItemGlobals.PRIVATEER_SPYGLASS: "Privateer's Spyglass", ItemGlobals.CORSAIR_SPYGLASS: "Corsair's Spyglass", ItemGlobals.CONQUISTADOR_SPYGLASS: "Conquistador's Spyglass", ItemGlobals.MERCENARY_SPYGLASS: "Mercenary's Spyglass", ItemGlobals.BOUNTY_HUNTER_SPYGLASS: "Bounty Hunter's Spyglass", ItemGlobals.WARMONGER_SPYGLASS: "Warmonger's Spyglass", ItemGlobals.NAVY_SPYGLASS: 'Navy Spyglass', ItemGlobals.TRADING_CO_SPYGLASS: 'Trading Company Spyglass', ItemGlobals.OFFICER_SPYGLASS: "Officer's Spyglass", ItemGlobals.BLACK_GUARD_SPYGLASS: "Black Guard's Spyglass", ItemGlobals.DAVY_JONES_SPYGLASS: "Davy Jones's Spyglass", ItemGlobals.BECKETTE_SPYGLASS: "Beckette's Spyglass", ItemGlobals.NORRINGTON_SPYGLASS: "Norrington's Spyglass", ItemGlobals.BARBOSSA_SPYGLASS: "Barbossa's Spyglass", ItemGlobals.JACK_SPARROW_SPYGLASS: "Jack Sparrow's Spyglass", ItemGlobals.FADED_SEA_CHART: 'Faded Sea Chart', ItemGlobals.MERCHANT_SEA_CHART: "Merchant's Sea Chart", ItemGlobals.SMUGGLER_SEA_CHART: "Smuggler's Sea Chart", ItemGlobals.RUMRUNNER_SEA_CHART: "Rumrunner's Sea Chart", ItemGlobals.LANDLUBBER_SEA_CHART: "Landlubber's Sea Chart", ItemGlobals.SAILOR_SEA_CHART: "Sailor's Sea Chart", ItemGlobals.FREEBOOTER_SEA_CHART: "Freebooter's Sea Chart", ItemGlobals.VOYAGER_SEA_CHART: "Voyager's Sea Chart", ItemGlobals.EXPLORER_SEA_CHART: "Explorer's Sea Chart", ItemGlobals.TREASURE_HUNTER_SEA_CHART: "Treasure Hunter's Sea Chart", ItemGlobals.OLD_WORLD_SEA_CHART: 'Old World Sea Chart', ItemGlobals.NEW_WORLD_SEA_CHART: 'New World Sea Chart', ItemGlobals.LOST_WORLD_SEA_CHART: 'Lost World Sea Chart', ItemGlobals.THIEVE_SEA_GLOBE: "Thieve's Sea Globe", ItemGlobals.BANDIT_SEA_GLOBE: "Bandit's Sea Globe", ItemGlobals.ROBBER_SEA_GLOBE: "Robber's Sea Globe", ItemGlobals.PRIVATEER_SEA_GLOBE: "Privateer's Sea Globe", ItemGlobals.CORSAIR_SEA_GLOBE: "Corsair's Sea Globe", ItemGlobals.SEVEN_SEAS_SEA_GLOBE: 'Seven Seas Sea Globe', ItemGlobals.WOODEN_CHARM: 'Wooden Charm', ItemGlobals.LUCKY_CHARM: 'Lucky Charm', ItemGlobals.GOLDEN_CHARM: 'Golden Charm', ItemGlobals.FORTUNE_CHARM: 'Fortune Charm', ItemGlobals.EL_DORODO_CHARM: "El Dorodo's Charm", ItemGlobals.MUTINEERS_CHARM: "Mutineer's Charm", ItemGlobals.TONIC: 'Tonic', ItemGlobals.REMEDY: 'Remedy', ItemGlobals.HOLY_WATER: 'Holy Water', ItemGlobals.ELIXIR: 'Elixir', ItemGlobals.MIRACLE_WATER: 'Miracle Water', ItemGlobals.SHIP_REPAIR_KIT: 'Ship Repair Kit', ItemGlobals.ROAST_PORK: 'Roast Pork', ItemGlobals.POTION_CUTLASS_1: 'Swashbuckler Stew I', ItemGlobals.POTION_CUTLASS_2: 'Swashbuckler Stew II', ItemGlobals.POTION_CUTLASS_3: 'Swashbuckler Stew III', ItemGlobals.POTION_PISTOL_1: 'Marksman Draught I', ItemGlobals.POTION_PISTOL_2: 'Marksman Draught II', ItemGlobals.POTION_PISTOL_3: 'Marksman Draught III', ItemGlobals.POTION_CANNON_1: 'Cannoneer Draft I', ItemGlobals.POTION_CANNON_2: 'Cannoneer Draft II', ItemGlobals.POTION_CANNON_3: 'Cannoneer Draft III', ItemGlobals.POTION_DOLL_1: 'Mystic Mixture I', ItemGlobals.POTION_DOLL_2: 'Mystic Mixture II', ItemGlobals.POTION_DOLL_3: 'Mystic Mixture III', ItemGlobals.POTION_SPEED_1: 'Swift Foot I', ItemGlobals.POTION_SPEED_2: 'Swift Foot II', ItemGlobals.POTION_SPEED_3: 'Swift Foot III', ItemGlobals.POTION_REP_1: 'Hardy Matey I', ItemGlobals.POTION_REP_2: 'Hardy Matey II', ItemGlobals.POTION_REP_3: 'Reputation Booster', ItemGlobals.POTION_REP_COMP: "Jack's Brew", ItemGlobals.POTION_GOLD_1: 'Plunder Potion I', ItemGlobals.POTION_GOLD_2: 'Plunder Potion II', ItemGlobals.POTION_INVIS_1: 'Phantom Spirits I', ItemGlobals.POTION_INVIS_2: 'Phantom Spirits II', ItemGlobals.POTION_REGEN_1: 'Lively Bucko Brew I', ItemGlobals.POTION_REGEN_2: 'Lively Bucko Brew II', ItemGlobals.POTION_REGEN_3: 'Lively Bucko Brew III', ItemGlobals.POTION_REGEN_4: 'Lively Bucko Brew IIII', ItemGlobals.POTION_BURP: "Belchin' Brew", ItemGlobals.POTION_FART: 'Flatulent Fizz', ItemGlobals.POTION_FART_2: 'Super Flatulent Fizz', ItemGlobals.POTION_VOMIT: 'Puke Potion', ItemGlobals.POTION_HEADGROW: 'Ginko Glug', ItemGlobals.POTION_FACECOLOR: 'Ghastly Visage', ItemGlobals.POTION_SHRINK: "Shrinkin' Grog", ItemGlobals.POTION_GROW: "Growin' Grog", ItemGlobals.POTION_HEADONFIRE: 'Addled Elixir', ItemGlobals.POTION_SCORPION: 'Stinger Stew', ItemGlobals.POTION_ALLIGATOR: 'Gator Grog', ItemGlobals.POTION_CRAB: 'Pincer Potion', ItemGlobals.POTION_ACC_1: 'Deadeye I', ItemGlobals.POTION_ACC_2: 'Deadeye II', ItemGlobals.POTION_ACC_3: 'Deadeye III', ItemGlobals.POTION_GROG: "Clap o'Thunder", ItemGlobals.STAFF_ENCHANT_1: 'Staff Enchant I', ItemGlobals.STAFF_ENCHANT_2: 'Staff Enchant II', ItemGlobals.POTION_SUMMON_CHICKEN: 'Summon Chicken', ItemGlobals.POTION_SUMMON_MONKEY: 'Summon Monkey', ItemGlobals.POTION_SUMMON_WASP: 'Summon Wasp', ItemGlobals.POTION_SUMMON_DOG: 'Summon Dog', ItemGlobals.HIGH_WING_HAT: 'High Wing Hat', ItemGlobals.ROUGH_TRICORNE: 'Rough Tricorne', ItemGlobals.ORANGE_TRICORNE: 'Orange Tricorne', ItemGlobals.SKULL_TRICORNE: 'Skull Tricorne', ItemGlobals.NAVY_TRIM_TRICORNE: 'Navy Trim Tricorne', ItemGlobals.EITC_HAT: 'EITC Hat', ItemGlobals.ADMIRAL_HAT: 'Admiral Hat', ItemGlobals.PATCHED_BANDANA: 'Patched Bandana', ItemGlobals.ZIGZAG_BANDANA: 'Zigzag Bandana', ItemGlobals.PATCHED_BAND: 'Patched Band', ItemGlobals.ZIGZAG_BAND: 'Zigzag Band', ItemGlobals.CAP: 'Cap', ItemGlobals.CROSSBONES_CAP: 'Crossbones Cap', ItemGlobals.CROSSBONE_BEANIE: 'Crossbone Beanie', ItemGlobals.DARK_OSTRICH_HAT: 'Dark Ostrich Hat', ItemGlobals.PURPLE_OSTRICH_HAT: 'Purple Ostrich Hat', ItemGlobals.BLUE_OSTRICH_HAT: 'Blue Ostrich Hat', ItemGlobals.RED_OSTRICH_HAT: 'Red Ostrich Hat', ItemGlobals.MAGENTA_OSTRICH_HAT: 'Magenta Ostrich Hat', ItemGlobals.ADVENTURE_OSTRICH_HAT: 'Adventure Ostrich Hat', ItemGlobals.TRAVELERS_OSTRICH_HAT: 'Travelers Ostrich Hat', ItemGlobals.GREEN_SILK_BEANIE: 'Green Silk Beanie', ItemGlobals.BARON_WING_HAT: "Baron's Hat", ItemGlobals.PRINCE_WING_HAT: "Prince's Hat", ItemGlobals.ROGUE_PRIVATEER_WING_HAT: 'Rogue Privateer Hat', ItemGlobals.PURPLE_BANDANA: 'Purple Bandana', ItemGlobals.BOHEMIAN_BANDANA: 'Bohemian Bandana', ItemGlobals.PURPLE_BAND: 'Purple Band', ItemGlobals.BOHEMIAN_BAND: 'Bohemian Band', ItemGlobals.BROWN_CAVALRY_HAT: 'Brown Cavalry Hat', ItemGlobals.BLUE_CAVALRY_HAT: 'Blue Cavalry Hat', ItemGlobals.GREEN_CAVALRY_HAT: 'Green Cavalry Hat', ItemGlobals.PURPLE_CAVALRY_HAT: 'Purple Cavalry Hat', ItemGlobals.BUTTERFLY_CAVALRY_HAT: 'Butterfly Cavalry Hat', ItemGlobals.ADVENTURE_CAVALRY_HAT: 'Adventure Cavalry Hat', ItemGlobals.TRAVELERS_CAVALRY_HAT: 'Travelers Cavalry Hat', ItemGlobals.DINGHY_HAT: 'Dinghy Hat', ItemGlobals.SIMPLE_BONNET: 'Simple Bonnet', ItemGlobals.RED_SILK_BANDANA: 'Red Silk Bandana', ItemGlobals.BARONESS_HAT: 'Baroness Hat', ItemGlobals.PRINCE_LADY_HAT: "Prince's Hat", ItemGlobals.ROGUE_PRIVATEER_CAVALRY_HAT: 'Rogue Privateer Hat', ItemGlobals.REDCOAT_HAT: 'Redcoat Hat', ItemGlobals.BANDANA: 'Bandana', ItemGlobals.BLUE_BANDANA: 'Blue Bandana', ItemGlobals.CROSSBONES_BANDANA: 'Crossbones Bandana', ItemGlobals.RECRUIT_BANDANA: 'Recruit Bandana', ItemGlobals.LOYALTY_BANDANA: 'Loyalty Bandana', ItemGlobals.HEAD_BAND: 'Head Band', ItemGlobals.BLUE_BAND: 'Blue Band', ItemGlobals.CROSSBONES_BAND: 'Crossbones Band', ItemGlobals.FRENCH_TRICORNE: 'French Tricorne', ItemGlobals.SPANISH_OSTRICH_HAT: 'Spanish Ostrich Hat', ItemGlobals.BLUE_FRENCH_HAT: 'Blue French Hat', ItemGlobals.GREEN_FRENCH_HAT: 'Green French Hat', ItemGlobals.VIOLET_FRENCH_HAT: 'Violet French Hat', ItemGlobals.BLACK_BICORNE: 'Black Bicorne', ItemGlobals.BROWN_BICORNE: 'Brown Bicorne', ItemGlobals.BLACK_CHAPEAU: 'Black Chapeau', ItemGlobals.NAVY_CHAPEAU: 'Navy Chapeau', ItemGlobals.BLACK_GAUCHO: 'Black Gaucho', ItemGlobals.BROWN_GAUCHO: 'Brown Gaucho', ItemGlobals.RED_GAUCHO: 'Red Gaucho', ItemGlobals.BRONZE_CABASET: 'Bronze Cabaset', ItemGlobals.STEEL_CABASET: 'Steel Cabaset', ItemGlobals.EMBOSSED_CABASET: 'Embossed Cabaset', ItemGlobals.RUSTED_CABASET: 'Rusted Cabaset', ItemGlobals.BLACK_CAVALIER: 'Black Cavalier', ItemGlobals.LEATHER_CAVALIER: 'Leather Cavalier', ItemGlobals.BURGUNDY_CAVALIER: 'Burgundy Cavalier', ItemGlobals.GRAY_CAVALIER: 'Gray Cavalier', ItemGlobals.BLACK_EXPLORER_HAT: 'Black Explorer Hat', ItemGlobals.LEATHER_EXPLORER_HAT: 'Leather Explorer Hat', ItemGlobals.STRAW_EXPLORER_HAT: 'Straw Explorer Hat', ItemGlobals.BLACK_PARADE_HAT: 'Black Parade Hat', ItemGlobals.RED_PARADE_HAT: 'Red Parade Hat', ItemGlobals.STEEL_CONQUISTADOR: 'Steel Conquistador', ItemGlobals.GOLD_CONQUISTADOR: 'Gold Conquistador', ItemGlobals.BLUE_STOCKING_CAP: 'Blue Stocking Cap', ItemGlobals.GREEN_STOCKING_CAP: 'Green Stocking Cap', ItemGlobals.GOLD_STOCKING_CAP: 'Gold Stocking Cap', ItemGlobals.RED_STOCKING_CAP: 'Red Stocking Cap', ItemGlobals.POLAR_STOCKING_CAP: 'Polar Stocking Cap', ItemGlobals.XMAS_CAP: 'Winter Festival Cap', ItemGlobals.MARDI_GRAS_TRICORNE: 'Mardi Gras Hat', ItemGlobals.SAINT_PATRICKS_STOVE_HAT: "St. Patrick's Hat", ItemGlobals.VALENTINES_TRICORNE: "Valentine's Hat", ItemGlobals.VIOLET_STOCKING_CAP: 'Violet Stocking Cap', ItemGlobals.COTTON_STOCKING_CAP: 'Cotton Stocking Cap', ItemGlobals.YELLOW_STOCKING_CAP: 'Yellow Stocking Cap', ItemGlobals.BLUE_RED_PARTY_HAT: 'Blue Red Party Hat', ItemGlobals.GREEN_ORANGE_PARTY_HAT: 'Green Orange Party Hat', ItemGlobals.PINK_PARTY_HAT: 'Pink Party Hat', ItemGlobals.ORANGE_GREEN_PARTY_HAT: 'Orange Green Party Hat', ItemGlobals.SKY_BLUE_PARTY_HAT: 'Sky Blue Party Hat', ItemGlobals.PURPLE_YELLOW_PARTY_HAT: 'Purple Yellow Party Hat', ItemGlobals.BLACK_STOVE_HAT: 'Black Stove Hat', ItemGlobals.BLUE_STOVE_HAT: 'Blue Stove Hat', ItemGlobals.BROWN_STOVE_HAT: 'Brown Stove Hat', ItemGlobals.GREEN_STOVE_HAT: 'Green Stove Hat', ItemGlobals.BLACK_BUCCANEER_HAT: 'Black Buccaneer Hat', ItemGlobals.GREEN_BUCCANEER_HAT: 'Green Buccaneer Hat', ItemGlobals.FANCY_BUCCANEER_HAT: 'Fancy Buccaneer Hat', ItemGlobals.CRIMSON_BUCCANEER_HAT: 'Scoundrel Hat', ItemGlobals.MOTTLED_BUCCANEER_HAT: 'Mottled Buccanner Hat', ItemGlobals.ROSE_BUCCANEER_HAT: 'Rose Buccaneer Hat', ItemGlobals.ROSE_BUCCANEER_HAT: 'Rose Buccaneer Hat', ItemGlobals.FRENCH_ASSASSIN_HAT: 'French Assassin Hat', ItemGlobals.DIPLOMAT_HAT: 'Diplomat Hat', ItemGlobals.SEA_SERPENT_HUNTER_HAT: 'Sea Serpent Hat', ItemGlobals.PEACOCK_TRICORN_HAT: 'Peacock Hat', ItemGlobals.SCOURGE_TRICORN_HAT: 'Scourge of the Seas Hat', ItemGlobals.ZOMBIE_PIRATE_HAT: 'Zombie Pirate Hat', ItemGlobals.ZOMBIES_PIRATE_HAT: "Zombie Pirate's Hat", ItemGlobals.SOUTH_CHINA_BAND: 'China Seas Warrior Bandana', ItemGlobals.WILDFIRE_BAND: 'Wildfire Bandana', ItemGlobals.BOUNTYHUNTER_BAND: 'Bounty Hunter Bandana', ItemGlobals.BARBARY_CORSAIR_BAND: 'Barbary Corsair Bandana', ItemGlobals.DINGY_LONG_COAT: 'Dingy Long Coat', ItemGlobals.EMBROIDERED_LONG_COAT: 'Embroidered Long Coat', ItemGlobals.TOURIST_LONG_COAT: 'Tourist Long Coat', ItemGlobals.TRADER_LONG_COAT: 'Trader Long Coat', ItemGlobals.FOREST_LONG_COAT: 'Forest Long Coat', ItemGlobals.WOOLEN_LONG_COAT: 'Woolen Long Coat', ItemGlobals.LEATHERCRAFT_LONG_COAT: 'Leathercraft Long Coat', ItemGlobals.DARKHEART_LONG_COAT: 'Darkheart Long Coat', ItemGlobals.WEATHERED_LONG_COAT: 'Weathered Long Coat', ItemGlobals.MERCHANT_LONG_COAT: 'Merchant Long Coat', ItemGlobals.FLEET_LONG_COAT: 'Fleet Long Coat', ItemGlobals.KEELHAUL_LONG_COAT: 'Keelhaul Long Coat', ItemGlobals.LUCKY_LONG_COAT: 'Lucky Long Coat', ItemGlobals.CLUB_COAT: 'Club Coat', ItemGlobals.ADVENTURE_LONG_COAT: 'Adventure Long Coat', ItemGlobals.SWABBIE_JACKET: "Swabby's Jacket", ItemGlobals.MONEY_JACKET: 'Money Jacket', ItemGlobals.COTTON_JACKET: 'Cotton Jacket', ItemGlobals.EVENING_JACKET: 'Evening Jacket', ItemGlobals.SHIPWRIGHT_JACKET: 'Shipwright Jacket', ItemGlobals.BOUNCER_JACKET: "Bouncer's Jacket", ItemGlobals.WHALING_JACKET: 'Whaling Jacket', ItemGlobals.MATEY_JACKET: "Matey's Jacket", ItemGlobals.ROYAL_LONG_COAT: 'Royal Long Coat', ItemGlobals.BLACK_GOLD_LONG_COAT: 'Black Gold Long Coat', ItemGlobals.FRENCH_ASSASSIN_LONG_COAT: 'French Assassin Long Coat', ItemGlobals.BARON_LONG_COAT: 'Baron Long Coat', ItemGlobals.PRINCE_LONG_COAT: 'Prince Long Coat', ItemGlobals.SCOURGE_LONG_COAT: 'Scourge of the Seas Coat', ItemGlobals.WILDIFRE_LONG_COAT: 'Wildfire Long Coat', ItemGlobals.ZOMBIE_PIRATE_LONG_COAT: 'Zombie Pirate Coat', ItemGlobals.ZOMBIES_PIRATE_LONG_COAT: "Zombie Pirate's Coat", ItemGlobals.ROGUE_PRIVATEER_LONG_COAT: 'Rogue Privateer Coat', ItemGlobals.SEA_SERPENT_JACKET: 'Sea Serpent Jacket', ItemGlobals.CHINA_WARRIOR_COAT: 'China Seas Warrior Coat', ItemGlobals.DIPLOMAT_COAT: 'Diplomat Long Coat', ItemGlobals.BROWN_STRIPE_JACKET: 'Brown Stripe Coat', ItemGlobals.BLACK_CHECKERBOARD_JACKET: 'Checker Coat', ItemGlobals.PATCHWORK_RIDING_COAT: 'Patchwork Riding Coat', ItemGlobals.LEATHER_RIDING_COAT: 'Leather Riding Coat', ItemGlobals.HIGHWAY_COAT: 'Highway Coat', ItemGlobals.MILITIA_RIDING_COAT: 'Militia Riding Coat', ItemGlobals.GOLD_THREAD_RIDING_COAT: 'Gold Thread Riding Coat', ItemGlobals.IMPROVISED_RIDING_COAT: 'Improvised Riding Coat', ItemGlobals.VALHALLA_RIDING_COAT: 'Valhalla Riding Coat', ItemGlobals.VICTORIAN_RIDING_COAT: 'Victorian Riding Coat', ItemGlobals.ROYALIST_RIDING_COAT: 'Royalist Riding Coat', ItemGlobals.ADVENTURE_RIDING_COAT: 'Adventure Riding Coat', ItemGlobals.CROCODILE_FROCK_COAT: 'Crocodile Frock Coat', ItemGlobals.WOOLEN_FROCK_COAT: 'Woolen Frock Coat', ItemGlobals.LEATHER_FROCK_COAT: 'Leather Frock Coat', ItemGlobals.SUEDE_FROCK_COAT: 'Suede Frock Coat', ItemGlobals.HARBOR_FROCK_COAT: 'Harbor Frock Coat', ItemGlobals.TOURIST_FROCK_COAT: 'Tourist Frock Coat', ItemGlobals.BORROWED_FROCK_COAT: '"Borrowed" Frock Coat', ItemGlobals.TAILORED_FROCK_COAT: 'Tailored Frock Coat', ItemGlobals.GOLD_FAD_FROCK_COAT: 'Gold Fad Frock Coat', ItemGlobals.FRENCH_ASSASSIN_FROCK_COAT: 'French Assassin Frock Coat', ItemGlobals.ROYAL_RIDING_COAT_TRIM: 'Royal Riding Coat with Trim', ItemGlobals.ADVENTURE_RIDING_COAT_TRIM: 'Adventure Riding Coat with Trim', ItemGlobals.VICTORIAN_RIDING_COAT_GOLD: 'Victorian Riding Coat with Gold', ItemGlobals.BARONESS_FROCK_COAT: 'Baroness Coat', ItemGlobals.DIPLOMAT_FROCK_COAT: 'Diplomat Coat', ItemGlobals.PRINCE_FROCK_COAT: 'Prince Coat', ItemGlobals.CHINA_WARROIR_CLOSED_LADY_COAT: 'China Seas Warrior Coat', ItemGlobals.ROGUE_PRIVATEER_FROCK_COAT: 'Rogue Privateer Coat', ItemGlobals.SCOURGE_FROCK_COAT: 'Scourge of the Seas Coat', ItemGlobals.SEA_SERPENT_FROCK_COAT: 'Sea Serpent Coat', ItemGlobals.ZOMBIE_PIRATE_FROCK_COAT: 'Zombie Pirate Coat', ItemGlobals.ZOMBIES_PIRATE_FROCK_COAT: "Zombie Pirate's Coat", ItemGlobals.NAVY_RED_COAT: 'Navy Red Coat', ItemGlobals.EITC_BLACK_COAT: 'EITC Black Coat', ItemGlobals.LEATHER_VEST: 'Leather Vest', ItemGlobals.PATCHWORK_VEST: 'Patchwork Vest', ItemGlobals.BELTED_VEST: 'Belted Vest', ItemGlobals.DRESSY_VEST: 'Dressy Vest', ItemGlobals.SUIT_VEST: 'Suit Vest', ItemGlobals.UNIFORM_VEST: 'Uniform Vest', ItemGlobals.MERCHANT_VEST: 'Merchant Vest', ItemGlobals.SCARF_VEST: 'Scarf Vest', ItemGlobals.PERFORMER_VEST: "Performer's Vest", ItemGlobals.HUNTING_VEST: 'Hunting Vest', ItemGlobals.SILK_VEST: 'Silk Vest', ItemGlobals.WOODLAND_VEST: 'Woodland Vest', ItemGlobals.CARPENTER_VEST: 'Carpenter Vest', ItemGlobals.NIGHT_VEST: 'Night Vest', ItemGlobals.OPEN_ADVENTURE_VEST: 'Open Adventure Vest', ItemGlobals.EMBELLISHED_VEST: 'Embellished Vest', ItemGlobals.SHOP_VEST: 'Shop Vest', ItemGlobals.LONGSHOREMAN_VEST: "Longshoreman's Vest", ItemGlobals.SACK_VEST: 'Sack Vest', ItemGlobals.BANK_VEST: 'Bank Vest', ItemGlobals.TRAVELERS_VEST: "Traveler's Vest", ItemGlobals.EMBELLISHED_BLACK_GOLD_VEST: 'Embellished Black Gold Vest', ItemGlobals.BOUNTYHUNTER_VEST: 'Bounty Hunter Vest', ItemGlobals.ROGUE_PRIVATEER_VEST: 'Rogue Privateer Vest', ItemGlobals.WILDFIRE_VEST: 'Wildfire Vest', ItemGlobals.BUTTONED_VEST: 'Buttoned Vest', ItemGlobals.COTTON_VEST: 'Cotton Vest', ItemGlobals.DECK_VEST: 'Deck Vest', ItemGlobals.LACED_VEST: 'Laced Vest', ItemGlobals.YEOMAN_VEST: 'Yeoman Vest', ItemGlobals.CORSETED_VEST: 'Corseted Vest', ItemGlobals.FOREST_VEST: 'Forest Vest', ItemGlobals.COUNTESS_VEST: 'Countess Vest', ItemGlobals.CITY_VEST: 'City Vest', ItemGlobals.COUNTRY_VEST: 'Country Vest', ItemGlobals.ADVENTURE_VEST: 'Adventure Vest', ItemGlobals.LOOSE_BUTTONED_VEST: 'Loose Buttoned Vest', ItemGlobals.LOOSE_LEATHER_VEST: 'Loose Leather Vest', ItemGlobals.ORCHARD_VEST: 'Orchard Vest', ItemGlobals.MESSENGER_VEST: 'Messenger Vest', ItemGlobals.COURT_VEST: 'Court Vest', ItemGlobals.BAND_VEST: 'Band Vest', ItemGlobals.CLOVER_VEST: 'Clover Vest', ItemGlobals.GARDEN_VEST: 'Garden Vest', ItemGlobals.PETAL_VEST: 'Petal Vest', ItemGlobals.DARKNESS_VEST: 'Darkness Vest', ItemGlobals.TRAVELERS_LOOSE_VEST: 'Travelers Loose Vest', ItemGlobals.ROYAL_CHEST_CORSET: 'Royal Chest Corset', ItemGlobals.ROSE_PETAL_CORSET: 'Rose Petal Corset', ItemGlobals.OLD_GROVE_CORSET: 'Old Grove Corset', ItemGlobals.GAS_LAMP_CORSET: 'Gas Lamp Corset', ItemGlobals.HIGH_TIDE_CORSET: 'High Tide Corset', ItemGlobals.MORNING_DEW_CORSET: 'Morning Dew Corset', ItemGlobals.RAWHIDE_CORSET: 'Rawhide Corset', ItemGlobals.EMBROIDERED_CORSET: 'Embroidered Corset', ItemGlobals.COTTON_CORSET: 'Cotton Corset', ItemGlobals.CHRISTENING_CORSET: 'Christening Corset', ItemGlobals.SEAFOAM_CORSET: 'Seafoam Corset', ItemGlobals.FAIRDAY_CORSET: 'Fairday Corset', ItemGlobals.BROWN_PILLOW_VEST: 'Brown Pillow Loose Vest', ItemGlobals.RED_BROWN_VEST: 'Red Brown Loose Vest', ItemGlobals.DARK_BLUE_GOLD_VEST: 'Dark Blue Gold Loose Vest', ItemGlobals.PEACOCK_CORSET: 'Peacock Corset', ItemGlobals.ZOMBIE_PIRATE_CORSET: 'Zombie Pirate Corset', ItemGlobals.ZOMBIES_PIRATE_CORSET: "Zombie Pirate's Corset", ItemGlobals.BOUNTYHUNTER_CORSET: 'Bounty Hunter Corset', ItemGlobals.ROGUE_PRIVATEER_CORSET: 'Rogue Privateer Corset', ItemGlobals.WILDFIRE_CORSET: 'Wildfire Corset', ItemGlobals.PRINCE_VEST: 'Prince Vest', ItemGlobals.OLD_TANK: 'Old Tank', ItemGlobals.STRIPED_TANK: 'Striped Tank', ItemGlobals.COTTON_TANK: 'Cotton Tank', ItemGlobals.TRIMMED_TANK: 'Trimmed Tank', ItemGlobals.SUSPENDER_TANK: 'Suspender Tank', ItemGlobals.CREW_TANK: 'Crew Tank', ItemGlobals.HOOKED_TANK: 'Hooked Tank', ItemGlobals.REINFORCED_TANK: 'Reinforced Tank', ItemGlobals.SEAMED_TANK: 'Seamed Tank', ItemGlobals.MARINER_TANK: 'Mariner Tank', ItemGlobals.IMPROVISED_TANK: 'Improvised Tank', ItemGlobals.MANLY_TANK: 'Manly Tank', ItemGlobals.INDENTURED_TANK: 'Indentured Tank', ItemGlobals.STITCHED_TANK: 'Stitched Tank', ItemGlobals.FRILLY_TANK: 'Frilly Tank', ItemGlobals.SHIELD_TANK: 'Shield Tank', ItemGlobals.CRESTED_TANK: 'Crested Tank', ItemGlobals.ADVANCED_TANK: 'Adventure Tank', ItemGlobals.LAYERD_SHIRTS: 'Layered Shirts', ItemGlobals.PUB_SHIRT: 'Pub Shirt', ItemGlobals.SWABBIE_SHIRT: 'Swabbie Shirt', ItemGlobals.PANELED_SHIRT: 'Paneled Shirt', ItemGlobals.GOVERNORS_EX_SHIRT: "Governor's Ex-Shirt", ItemGlobals.BIG_BUTTON_SHIRT: 'Big Button Shirt', ItemGlobals.MAYORS_SHIRT: "Mayor's Shirt", ItemGlobals.TRIMMED_JERKIN: 'Trimmed Jerkin', ItemGlobals.GREEN_GOLD_WHITE_COLLAR: 'Green Gold Shirt White Collar', ItemGlobals.TREASURE_SHORT_SLEEVE: 'Treasure Short Sleeve', ItemGlobals.COTTON_SHORT_SLEEVE: 'Cotton Short Sleeve', ItemGlobals.LINEN_SHORT_SLEEVE: 'Linen Short Sleeve', ItemGlobals.LACED_SHORT_SLEEVE: 'Laced Short Sleeve', ItemGlobals.TIED_SHORT_SLEEVE: 'Tied Short Sleeve', ItemGlobals.FLAP_SHORT_SLEEVE: 'Flap Short Sleeve', ItemGlobals.FLEET_SHORT_SLEEVE: 'Fleet Short Sleeve', ItemGlobals.OPEN_TREASURE_SHIRT: 'Open Treasure Shirt', ItemGlobals.OPEN_COTTON_SHIRT: 'Open Cotton Shirt', ItemGlobals.OPEN_LINEN_SHIRT: 'Open Linen Shirt', ItemGlobals.OPEN_LACED_SHIRT: 'Open Laced Shirt', ItemGlobals.OPEN_FLEET_SHIRT: 'Open Fleet Shirt', ItemGlobals.LACED_PUFFY_SHIRT: 'Laced Puffy Shirt', ItemGlobals.REINFORCED_PUFFY_SHIRT: 'Reinforced Puffy Shirt', ItemGlobals.COTTON_PUFFY_SHIRT: 'Cotton Puffy Shirt', ItemGlobals.LINEN_PUFFY_SHIRT: 'Linen Puffy Shirt', ItemGlobals.RENAISSANCE_SHIRT: 'Renaissance Shirt', ItemGlobals.PADDED_SHIRT: 'Padded Shirt', ItemGlobals.LEATHER_PUFFY_SHIRT: 'Leather Puffy Shirt', ItemGlobals.MERCHANT_SHIRT: 'Merchant Shirt', ItemGlobals.TRAVELERS_PUFFY_SHIRT: "Traveler's Shirt", ItemGlobals.LONG_TREASURE_SHIRT: 'Long Treasure Shirt', ItemGlobals.COTTON_LONG_SLEEVE: 'Cotton Long Sleeve', ItemGlobals.LINEN_LONG_SLEEVE: 'Linen Long Sleeve', ItemGlobals.LACED_LONG_SLEEVE: 'Laced Long Sleeve', ItemGlobals.TIED_LONG_SLEEVE: 'Tied Long Sleeve', ItemGlobals.FLAP_LONG_SLEEVE: 'Flap Long Sleeve', ItemGlobals.FLEET_LONG_SLEEVE: 'Fleet Long Sleeve', ItemGlobals.RECRUIT_LONG_SLEEVE: 'Recruit Long Sleeve', ItemGlobals.OPEN_TREASURE_LONG_SLEEVE: 'Open Treasure Long Sleeve', ItemGlobals.COTTON_OPEN_LONG_SLEEVE: 'Cotton Open Long Sleeve', ItemGlobals.LINEN_OPEN_LONG_SLEEVE: 'Linen Open Long Sleeve', ItemGlobals.DEALER_SHIRT: 'Dealer Shirt', ItemGlobals.CINCO_DE_MAYO_SHIRT: 'Cinco De Mayo Shirt', ItemGlobals.HALLOWEEN_SHIRT: 'Halloween Shirt', ItemGlobals.THANKSGIVING_SHIRT: 'Thanksgiving Shirt', ItemGlobals.GUY_FAWKES_SHIRT: 'Guy Fawkes Shirt', ItemGlobals.VALENTINES_SHIRT: "Valentine's Shirt", ItemGlobals.WINTER_HOLIDAY_SHIRT: 'Winter Holiday Shirt', ItemGlobals.CARIBBEAN_DAY_SHIRT: 'Caribbean Day Shirt', ItemGlobals.CARNIVAL_SHIRT: 'Carnival Shirt', ItemGlobals.CHINESE_NEWYEAR_SHIRT: 'Snapdragon Shirt', ItemGlobals.AUTUMN_SHIRT: 'Autumn Shirt', ItemGlobals.NEW_YEARS_EVE_SHIRT: 'Purple Emblem Shirt', ItemGlobals.SAINT_PATRICKS_SHIRT: "Saint Patrick's Shirt", ItemGlobals.SUMMER_SOLSTICE_SHIRT: 'Summer Solstice Shirt', ItemGlobals.WINTER_SOLSTICE_SHIRT: 'Winter Solstice Shirt', ItemGlobals.SPRING_SHIRT: 'Spring Shirt', ItemGlobals.GREEN_GOLD_WHITE_COLLAR: 'Green Gold White Collar', ItemGlobals.MERCHANT_SHIRT_GOLD_TRIM: 'Merchant Shirt Gold Trim', ItemGlobals.XMAS_SHIRT: 'Winter Festival Shirt', ItemGlobals.MARDI_GRAS_SHIRT: 'Mardi Gras Shirt', ItemGlobals.HIGHNECK_FRENCH_ASSASSIN_SHIRT: 'French Assassin Shirt', ItemGlobals.SCOURGE_TANK: 'Scourge of the Seas Tank', ItemGlobals.SEA_SERPENT_TANK: 'Sea Serpent Tank', ItemGlobals.ZOMBIE_LONG_SLEEVE: 'Zombie Shirt', ItemGlobals.ZOMBIES_LONG_SLEEVE: "Zombie's Shirt", ItemGlobals.HIGHNECK_BARON_SHIRT: 'Baron Shirt', ItemGlobals.HIGHNECK_PEACOCK_SHIRT: 'Peacock Shirt', ItemGlobals.HIGHNECK_PRINCE_SHIRT: 'Prince Shirt', ItemGlobals.BARBARY_CORSAIR_SHIRT: 'Barbary Corsair Shirt', ItemGlobals.STITCHED_BLOUSE: 'Stitched Blouse', ItemGlobals.BURLAP_BLOUSE: 'Burlap Blouse', ItemGlobals.TRIMMED_BLOUSE: 'Trimmed Blouse', ItemGlobals.DINGY_BLOUSE: 'Dingy Blouse', ItemGlobals.COURT_BLOUSE: 'Court Blouse', ItemGlobals.TAVERN_BLOUSE: 'Tavern Blouse', ItemGlobals.EMBROIDERED_BLOUSE: 'Embroidered Blouse', ItemGlobals.SCOURGE_BLOUSE: 'Scourge of the Seas Blouse', ItemGlobals.SEA_SERPENT_BLOUSE: 'Sea Serpent Blouse', ItemGlobals.DINGY_PUFF_BLOUSE: 'Dingy Puff Blouse', ItemGlobals.COTTON_PUFF_BLOUSE: 'Cotton Puff Blouse', ItemGlobals.FLAPPED_PUFF_BLOUSE: 'Flapped Puff Blouse', ItemGlobals.FRILLY_BLOUSE: ' Frilly Blouse', ItemGlobals.COLLAR_PUFF_BLOUSE: 'Collar Puff Blouse', ItemGlobals.SKY_BLOUSE: 'Sky Blouse', ItemGlobals.FESTIVAL_BLOUSE: ' Festival Blouse', ItemGlobals.DINGY_TOP: 'Dingy Top', ItemGlobals.SKULL_BROACH_TOP: 'Skull Broach Top', ItemGlobals.COTTON_TOP: 'Cotton Top', ItemGlobals.PANEL_TOP: 'Panel Top', ItemGlobals.CITY_TOP: 'City Top', ItemGlobals.WOODLAND_TOP: 'Woodland Top', ItemGlobals.VILLA_TOP: 'Villa Top', ItemGlobals.TAILORED_PUFFY_SHIRT: 'Tailored Puffy Shirt', ItemGlobals.SWASHBUCKLER_TOP: 'Swashbuckler Top', ItemGlobals.RUFFLE_SHIRT: 'Ruffle Shirt', ItemGlobals.FINE_PUFFY_SHIRT: 'Fine Puffy Shirt', ItemGlobals.MERCHANT_TOP: 'Merchant Top', ItemGlobals.FLORID_TOP: 'Florid Top', ItemGlobals.LACE_TRIM_TOP: 'Lace Trim Top', ItemGlobals.RECRUIT_TOP: 'Recruit Top', ItemGlobals.TRAVELERS_TOP: "Traveler's Top", ItemGlobals.ADVENTURE_TOP: 'Adventure Top', ItemGlobals.FRENCH_ASSASSIN_TOP: 'French Assassin Top', ItemGlobals.BARBARY_CORSAIR_TOP: 'Barbary Corsair Top', ItemGlobals.HIGH_SEAS_BLOUSE: 'High Seas Blouse', ItemGlobals.DARK_WATER_BLOUSE: 'Dark Water Blouse', ItemGlobals.BOARDING_BLOUSE: 'Boarding Blouse', ItemGlobals.DARK_CLOUD_BLOUSE: 'Dark Cloud Blouse', ItemGlobals.ROUGH_WATER_BLOUSE: 'Rough Water Blouse', ItemGlobals.OPERA_BLOUSE: 'Opera Blouse', ItemGlobals.MUSKETEER_BLOUSE: 'Musketeer Blouse', ItemGlobals.CARIBBEAN_DAY_BLOUSE: 'Caribbean Day Blouse', ItemGlobals.CINCO_DE_MAYO_BLOUSE: 'Cinco De Mayo Blouse', ItemGlobals.GUY_FAWKES_BLOUSE: 'Guy Fawkes Blouse', ItemGlobals.HALLOWEEN_BLOUSE: 'Halloween Blouse', ItemGlobals.SUMMER_SOLSTICE_BLOUSE: 'Summer Solstice Blouse', ItemGlobals.THANKSGIVING_BLOUSE: 'Thanksgiving Blouse', ItemGlobals.WINTER_HOLIDAY_BLOUSE: 'Winter Holiday Blouse', ItemGlobals.CARNIVAL_BLOUSE: 'Carnival Blouse', ItemGlobals.CHINESE_NEWYEAR_BLOUSE: 'Snapdragon Blouse', ItemGlobals.VALENTINES_BLOUSE: "Valentine's Day Blouse", ItemGlobals.AUTUMN_BLOUSE: 'Autumn Blouse', ItemGlobals.SPRING_BLOUSE: 'Spring Blouse', ItemGlobals.NEW_YEARS_EVE_BLOUSE: 'Purple Emblem Blouse', ItemGlobals.SAINT_PATRICKS_BLOUSE: "Saint Patrick's Blouse", ItemGlobals.WINTER_SOLSTICE_BLOUSE: 'Winter Solstice Blouse', ItemGlobals.FLEUR_BLOUSE: 'Fleur Blouse', ItemGlobals.TEACHERS_BLOUSE: "Teacher's Blouse", ItemGlobals.RIDING_BLOUSE: 'Riding Blouse', ItemGlobals.COTTON_BLOUSE: 'Cotton Blouse', ItemGlobals.GARDEN_BLOUSE: 'Garden Blouse', ItemGlobals.DAY_DREAM_BLOUSE: 'Day Dream Blouse', ItemGlobals.MORNING_BLOUSE: 'Morning Blouse', ItemGlobals.FESTIVAL_BLOUSE_GOLD_TRIM: 'Festival Blouse Gold Trim', ItemGlobals.BLUE_WHITE_BLOUSE: 'Blue Blouse White Ruff', ItemGlobals.XMAS_BLOUSE: 'Winter Festival Blouse', ItemGlobals.MARDI_GRAS_BLOUSE: 'Mardi Gras Blouse', ItemGlobals.DIPLOMAT_BLOUSE: 'Diplomat Blouse', ItemGlobals.PRINCE_BLOUSE: 'Prince Blouse', ItemGlobals.BARONESS_BLOUSE: 'Baroness Blouse', ItemGlobals.BROWN_APRON: 'Brown Apron', ItemGlobals.DIRTY_APRON: 'Dirty Apron', ItemGlobals.GYPSY_BLOUSE: 'Gypsy Blouse', ItemGlobals.BARTENDER_BLOUSE: 'Bartender Blouse', ItemGlobals.BARMAID_BLOUSE: 'Barmaid Blouse', ItemGlobals.SHOPKEEPER_BLOUSE: 'Shopkeeper Blouse', ItemGlobals.RECRUIT_SASH: 'Recruit Sash', ItemGlobals.BASIC_SASH: 'Basic Sash', ItemGlobals.BUCKLED_SASH: 'Buckled Sash', ItemGlobals.FIERCE_SASH: 'Fierce Sash', ItemGlobals.TRIMMED_SASH: 'Trimmed Sash', ItemGlobals.PINK_SASH: 'Pink Sash', ItemGlobals.BLOOD_SASH: 'Red Sash', ItemGlobals.GOLD_SKULL_BELT: 'Gold Skull Belt', ItemGlobals.JOLLY_BONES_BELT: 'Jolly Bones Belt', ItemGlobals.BOX_BELT: 'Box Belt', ItemGlobals.TOP_SKULL_BELT: 'Top Skull Belt', ItemGlobals.PROUD_BELT: 'Proud Belt', ItemGlobals.ROUND_BELT: 'Round Belt', ItemGlobals.KNOCKOFF_PROUD__BELT: 'Knockoff Proud Belt', ItemGlobals.TOP_SKULL_KNOCKOFF_BELT: 'Top Skull Knockoff Belt', ItemGlobals.ENGRAVED_BOX_BELT: 'Engraved Box Belt', ItemGlobals.INSPECTOR_BELT: "Inspector's Belt", ItemGlobals.SQUARE_ADVENTURE_BELT: 'Adventure Belt', ItemGlobals.SQUARE_TRAVELERS_BELT: "Traveler's Belt", ItemGlobals.PRINCE_SASH: 'Prince Sash', ItemGlobals.BUCKLE_SASH: 'Buckle Sash', ItemGlobals.PATTERNED_SASH: 'Patterned Sash', ItemGlobals.TASSLES_SASH: 'Tassles Sash', ItemGlobals.GOLD_BUCKLE_SASH: 'Gold Buckle Sash', ItemGlobals.BLUE_SASH: 'Blue Sash', ItemGlobals.RED_FUR_SASH: 'Red Fur Sash', ItemGlobals.BRASS_SQUARE_BELT: 'Brass Square Belt', ItemGlobals.GOLD_SQUARE_BELT: 'Gold Square Belt', ItemGlobals.WOODLAND_BELT: 'Woodland Belt', ItemGlobals.GOLD_BOX_BELT: 'Gold Box Belt', ItemGlobals.LACED_BELT: 'Laced Belt', ItemGlobals.SIDE_BELT: 'Side Belt', ItemGlobals.ADVENTURE_BELT: 'Adventure Belt', ItemGlobals.TRAVELERS_BELT: 'Travelers Belt', ItemGlobals.MARDI_GRAS_SASH: 'Mardi Gras Sash', ItemGlobals.FRENCH_ASSASSIN_SASH: 'French Assassin Sash', ItemGlobals.BOUNTYHUNTER_SASH: 'Bounty Hunter Sash', ItemGlobals.BARBARY_CORSAIR_SASH: 'Barbary Corsair Sash', ItemGlobals.PEACOCK_SASH_MALE: "Peacock Men's Sash", ItemGlobals.PEACOCK_SASH_FEMALE: "Peacock Lady's Sash", ItemGlobals.WILDFIRE_SASH_FEMALE: 'Wildfire Sash', ItemGlobals.ROGUE_PRIVATEER_BELT: 'Rogue Privateer Belt', ItemGlobals.SCOURGE_BELT: 'Scourge of the Seas Belt', ItemGlobals.SEA_SERPENT_BELT: 'Sea Serpent Belt', ItemGlobals.ZOMBIE_PIRATE_BELT: 'Zombie Pirate Belt', ItemGlobals.ZOMBIES_PIRATE_BELT: "Zombie Pirate's Belt", ItemGlobals.LEATHER_HIGHWATERS: 'Leather Highwaters', ItemGlobals.COTTON_HIGHWATERS: 'Cotton Highwaters', ItemGlobals.DENIM_HIGHWATERS: 'Denim Highwaters', ItemGlobals.LINEN_HIGHWATERS: 'Linen Highwaters', ItemGlobals.CIRCUS_BREECHES: 'Circus Breeches', ItemGlobals.BUTTONED_BREECHES: 'Buttoned Breeches', ItemGlobals.GOLD_TRIM_BREECHES: 'Gold Trim Breeches', ItemGlobals.BARD_BREECHES: 'Bard Breeches', ItemGlobals.F44_DUBLOON_BREECHES: '44 Dubloon Breeches', ItemGlobals.DEPUTYS_EX_BREECHES: "Deputy's Ex-Breeches", ItemGlobals.FESTIVAL_BREECHES: 'Festival Breeches', ItemGlobals.MATADOR_BREECHES: 'Matador Breeches', ItemGlobals.ADVENTURE_BREECHES: 'Adventure Breeches', ItemGlobals.COTTON_TROUSERS: 'Cotton Trousers', ItemGlobals.CELTIC_TROUSERS: 'Celtic Trousers', ItemGlobals.SAIL_TROUSERS: 'Sail Trousers', ItemGlobals.LINEN_TROUSERS: 'Linen Trousers', ItemGlobals.POTATO_SACK_TROUSERS: 'Potato Sack Trousers', ItemGlobals.KAKI_SKULL_SNAP_TROUSERS: 'Kaki Skullsnap Trousers', ItemGlobals.DENIM_SKULL_SNAP_TROUSERS: 'Denim Skullsnap Trousers', ItemGlobals.FADED_SKULL_SNAP_TROUSERS: 'Faded Skullsnap Trousers', ItemGlobals.STOWAWAY_TROUSERS: 'Stowaway Trousers', ItemGlobals.DENIM_TROUSERS: 'Denim Trousers', ItemGlobals.SWAB_THE_DECK_TROUSERS: 'Swab the Deck Trousers', ItemGlobals.ZOMBIE_TROUSERS: 'Zombie Trousers', ItemGlobals.ARABIAN_TROUSERS: 'Arabian Trousers', ItemGlobals.SMITHY_TROUSERS: 'Smithy Trousers', ItemGlobals.RECRUIT_TROUSERS: 'Recruit Trousers', ItemGlobals.TRAVELERS_TROUSERS: 'Travelers Trousers', ItemGlobals.DINGY_SHORTS: 'Dingy Shorts', ItemGlobals.BEACH_SHORTS: 'Beach Shorts', ItemGlobals.COTTON_SHORTS: 'Cotton Shorts', ItemGlobals.BUCKLED_SHORTS: 'Buckled Shorts', ItemGlobals.SACK_SHORTS: 'Sack Shorts', ItemGlobals.SWIM_SHORTS: 'Swim Shorts', ItemGlobals.EXPLORER_SHORTS: 'Explorer Shorts', ItemGlobals.CANVAS_SHORTS: 'Canvas Shorts', ItemGlobals.BEACH_COMBER_SHORTS: 'Beach Comber Shorts', ItemGlobals.OCEAN_SHORTS: 'Ocean Shorts', ItemGlobals.BAG_SHORTS: 'Bag Shorts', ItemGlobals.BOXERS: 'Boxers', ItemGlobals.SWAMP_SHORTS: 'Swamp Shorts', ItemGlobals.BUTTONED_SHORTS: 'Buttoned Shorts', ItemGlobals.VIOLET_YELLOW_BREECHES: 'Violet Yellow Breeches', ItemGlobals.GREY_GREEN_BREECHES: 'Side Stripe Breeches', ItemGlobals.GREEN_EMBROIDERED_TROUSERS: 'Green Embroidered Trousers', ItemGlobals.CHAPS_TROUSERS: 'Loose Chaps', ItemGlobals.BROWN_PATCHED_TROUSERS: 'Patched Trousers', ItemGlobals.GREEN_SILK_TROUSERS: 'Green Silk Trousers', ItemGlobals.BLACK_GOLD_TROUSERS: 'Black Gold Trousers', ItemGlobals.FANCY_LIGHT_BROWN_SHORTS: 'Fancy Light Brown Shorts', ItemGlobals.XMAS_TROUSERS: 'Winter Festival Trousers', ItemGlobals.MARDI_GRAS_TROUSERS: 'Mardi Gras Trousers', ItemGlobals.SAINT_PATRICKS_BREECHES: "St. Patrick's Breeches", ItemGlobals.VALENTINES_BREECHES: "Valentine's Breeches", ItemGlobals.FRENCH_ASSASSIN_BREECHES: 'French Assassin Breeches', ItemGlobals.BARON_BREECHES: 'Baron Breeches', ItemGlobals.BOUNTYHUNTER_BREECHES: 'Bounty Hunter Breeches', ItemGlobals.CHINA_WARRIOR_BREECHES: 'China Seas Warrior Breeches', ItemGlobals.DIPLOMAT_BREECHES: 'Diplomat Breeches', ItemGlobals.PEACOCK_BREECHES: 'Peacock Breeches', ItemGlobals.PRINCE_BREECHES: 'Prince Breeches', ItemGlobals.ROGUE_PRIVATEER_BREECHES: 'Rogue Breeches', ItemGlobals.SEA_SERPENT_BREECHES: 'Sea Serpent Breeches', ItemGlobals.ZOMBIE_PIRATE_BREECHES: 'Zombie Pirate Breeches', ItemGlobals.ZOMBIES_PIRATE_BREECHES: "Zombie Pirate's Breeches", ItemGlobals.BARBARY_CORSAIR_TROUSERS: 'Barbary Corsair Trousers', ItemGlobals.SCOURGE_TROUSERS: 'Scourge of the Seas Trousers', ItemGlobals.WILDFIRE_TROUSERS: 'Wildfire Trousers', ItemGlobals.PATCHWORK_CAPRIS: 'Patchwork Capris', ItemGlobals.TAILORED_CAPRIS: 'Tailored Capris', ItemGlobals.MISFITTED_CAPRIS: 'Misfitted Capris', ItemGlobals.SIDE_STRIPE_CAPRIS: 'Sidestripe Capris', ItemGlobals.IMPROVISED_CAPRIS: 'Improvised Capris', ItemGlobals.CANDYSTRIPE_CAPRIS: 'Candystripe Capris', ItemGlobals.PARADE_CAPRIS: 'Parade Capris', ItemGlobals.RUNNERS_CAPRIS: "Runner's Capris", ItemGlobals.RED_VELVET_CAPRIS: 'Red Velvet Capris', ItemGlobals.CASUAL_CAPRIS: 'Casual Capris', ItemGlobals.PATTYS_CAPRIS: "Patty's Capris", ItemGlobals.COURT_CAPRIS: 'Court Capris', ItemGlobals.PIN_CAPRIS: 'Pin Capris', ItemGlobals.RECRUIT_CAPRIS: 'Recruit Capris', ItemGlobals.ADVENTURE_CAPRIS: 'Adventure Capris', ItemGlobals.TRAVELERS_CAPRIS: "Traveler's Capris", ItemGlobals.PATCHWORK_SHORTS: 'Patchwork Shorts', ItemGlobals.TIE_SHORTS: 'Tie Shorts', ItemGlobals.LINEN_SHORTS: 'Linen Shorts', ItemGlobals.FOREST_SHORTS: 'Forest Shorts', ItemGlobals.SIDELACE_SHORTS: 'Sidelace Shorts', ItemGlobals.ZOMBIE_SHORTS: 'Zombie Shorts', ItemGlobals.JUNGLE_SHORTS: 'Jungle Shorts', ItemGlobals.LAGOON_SHORTS: 'Lagoon Shorts', ItemGlobals.CASUAL_SHORTS: 'Casual Shorts', ItemGlobals.OLD_ROYAL_SHORTS: 'Old Royal Shorts', ItemGlobals.EMPRESS_SHORTS: 'Empress Shorts', ItemGlobals.MIDNIGHT_SHORTS: 'Midnight Shorts', ItemGlobals.CHERRY_SHORTS: 'Cherry Shorts', ItemGlobals.LINEN_SKIRT: 'Linen Skirt', ItemGlobals.HAND_ME_DOWN_SKIRT: 'Hand me down Skirt', ItemGlobals.LAYERED_SKIRT: 'Layerd Skirt', ItemGlobals.POTATO_SACK_SKIRT: 'Potato Sack Skirt', ItemGlobals.SILK_SKIRT: 'Silk Skirt', ItemGlobals.DENIM_SKIRT: 'Denim Skirt', ItemGlobals.WOODLAND_SKIRT: 'Woodland Skirt', ItemGlobals.CANDYBOX_SKIRT: 'Candybox Skirt', ItemGlobals.OBLIQUE_SKIRT: 'Oblique Skirt', ItemGlobals.PEA_SOUP_SKIRT: 'Pea Soup Skirt', ItemGlobals.TROPIC_SKIRT: 'Tropic Skirt', ItemGlobals.PRINCESS_SKIRT: 'Princess Skirt', ItemGlobals.DECK_SKIRT: 'Deck Skirt', ItemGlobals.JEWELED_SKIRT: 'Jeweled Skirt', ItemGlobals.BROWN_SILVER_SHORTS: 'Brown Silver Shorts', ItemGlobals.GREEN_PURPLE_SHORTS: 'Green Purple Shorts', ItemGlobals.GREEN_EMBROIDERY_SHORTS: 'Green Embroidery Shorts', ItemGlobals.PINK_GOLD_TRIM_SHORTS: 'Gold Trim Shorts', ItemGlobals.BROWN_SILVER_BUTTON_SHORTS: 'Brown Silver Button Shorts', ItemGlobals.RED_SILK_SHORTS: 'Red Silk Shorts', ItemGlobals.GOLD_TRIM_CAPRIS: 'Gold Trim Capris', ItemGlobals.GREEN_PURPLE_SKIRT: 'Green Purple Skirt', ItemGlobals.GREEN_EMBROIDERY_SKIRT: 'Green Embroidery Skirt', ItemGlobals.XMAS_SKIRT: 'Winter Festival Skirt', ItemGlobals.MARDI_GRAS_SHORTS: 'Mardi Gras Shorts', ItemGlobals.SAINT_PATRICKS_SKIRT: "St. Patrick's Skirt", ItemGlobals.VALENTINES_SKIRT: "Valentine's Skirt", ItemGlobals.FRENCH_ASSASSIN_CAPRIS: 'French Assassin Capris', ItemGlobals.BOUNTYHUNTER_SHORTS: 'Bounty Hunter Short', ItemGlobals.BARBARY_CORSAIR_SHORTS: 'Barbary Corsair Shorts', ItemGlobals.PEACOCK_SKIRT: 'Peacock Skirt', ItemGlobals.PRINCE_SKIRT: 'Prince Skirt', ItemGlobals.WILDFIRE_SKIRT: 'Wildfire Skirt', ItemGlobals.BARONESS_CAPRIS: 'Baroness Capris', ItemGlobals.CHINA_WARRIOR_CAPRIS: 'China Seas Warrior Capris', ItemGlobals.DIPLOMAT_CAPRIS: 'Diplomat Capris', ItemGlobals.ROGUE_PRIVATEER_CAPRIS: 'Rogue Privateer Capris', ItemGlobals.SCOURGE_CAPRIS: 'Scourge of the Seas Capris', ItemGlobals.SEA_SERPENT_CAPRIS: 'Sea Serpent Capris', ItemGlobals.ZOMBIE_PIRATE_CAPRIS: 'Zombie Pirate Capris', ItemGlobals.ZOMBIES_PIRATE_CAPRIS: "Zombie Pirate's Capris", ItemGlobals.TAVERN_APRON: 'Tavern Apron', ItemGlobals.DARK_APRON: 'Dark Apron', ItemGlobals.NAVY_PANTS: 'Navy Pants', ItemGlobals.EITC_PANTS: 'EITC Pants', ItemGlobals.GYPSY_SKIRT: 'Gypsy Skirt', ItemGlobals.GYPSY_GRUNGE_SKIRT: 'Gypsy Grunge Skirt', ItemGlobals.BARTENDER_SKIRT: 'Bartender Skirt', ItemGlobals.SHOPKEEPER_SKIRT: 'Shopkeeper Skirt', ItemGlobals.COMFY_BOOTS: 'Comfy Boots', ItemGlobals.WALLOP_BOOTS: 'Wallop Boots', ItemGlobals.WORN_IN_BOOTS: 'Worn in Boots', ItemGlobals.HARD_LEATHER_BOOTS: 'Hard Leather', ItemGlobals.PURSUIT_BOOTS: 'Pursuit Boots', ItemGlobals.INDOOR_BOOTS: 'Indoor Boots', ItemGlobals.MOUNTAIN_BOOTS: 'Mountain Boots', ItemGlobals.SERIOUS_BOOTS: 'Serious Boots', ItemGlobals.ADVENTURE_BOOTS: 'Adventure Boots', ItemGlobals.TRAVELERS_BOOTS: 'Travelers Boots', ItemGlobals.BUCKET_BOOTS: 'Bucket Boots', ItemGlobals.BUCKLE_BOOTS: 'Buckle Boots', ItemGlobals.FISHING_TROPHY_BOOTS: 'Fishing Trophy Boots', ItemGlobals.OLD_BOOTS: 'Old Boots', ItemGlobals.SPIFFY_BOOTS: 'Spiffy Boots', ItemGlobals.HIKING_BOOTS: 'Hiking Boots', ItemGlobals.RAWHIDE_BOOTS: 'Rawhide Boots', ItemGlobals.RECRUIT_BOOTS: 'Recruit Boots', ItemGlobals.ROYAL_BOOTS: 'Royal Boots', ItemGlobals.EMERALD_BOOTS: 'Emerald Boots', ItemGlobals.BLUE_FUR_TOP_BOOTS: 'Blue Fur Top Boots', ItemGlobals.SPUR_BOOTS: 'Spur Boots', ItemGlobals.ROUND_BUCKLE_SHORT_BOOTS: 'Round Buckle Short Boots', ItemGlobals.XMAS_MED_BOOTS: 'Winter Festival Boots', ItemGlobals.MARDI_GRAS_MED_BOOTS: 'Mardi Gras Boots', ItemGlobals.SAINT_PATRICKS_TALL_BOOTS: "St. Patrick's Boots", ItemGlobals.VALENTINES_TALL_BOOTS: "Valentine's Boots", ItemGlobals.RAVEN_TALL_BOOTS: 'Raven Boots', ItemGlobals.FRENCH_ASSASSIN_BOOTS: 'French Assassin Boots', ItemGlobals.CHINA_WARRIOR_TALL_BOOTS: 'China Seas Warrior Boots', ItemGlobals.PEACOCK_TALL_BOOTS: 'Peacock Boots', ItemGlobals.SEA_SERPENT_TALL_BOOTS: 'Sea Serpent Boots', ItemGlobals.BOUNTYHUNTER_BOOTS: 'Bounty Hunter Boots', ItemGlobals.BARBARY_CORSAIR_BOOTS: 'Barbary Corsair Boots', ItemGlobals.ROGUE_PRIVATEER_BOOTS: 'Rogue Privateer Boots', ItemGlobals.SCOURGE_BOOTS: 'Scourge of the Seas Boots', ItemGlobals.WILDFIRE_BOOTS: 'Wildfire Boots', ItemGlobals.ZOMBIE_PIRATE_BOOTS: 'Zombie Pirate Boots', ItemGlobals.ZOMBIES_PIRATE_BOOTS: "Zombie Pirate's Boots", ItemGlobals.BARON_BOOTS: 'Baron Boots', ItemGlobals.DIPLOMAT_SHOES: 'Dipolmat Shoes', ItemGlobals.PRINCE_SHOES: 'Prince Shoes', ItemGlobals.VOYAGER_BOOTS: 'Voyager Boots', ItemGlobals.MAYOR_BOOTS: 'Mayor Boots', ItemGlobals.GOLD_TRIM_BOOTS: 'Gold Trim Boots', ItemGlobals.RED_TRIM_BOOTS: 'Red Trim Boots', ItemGlobals.DECK_SLAPPER_BOOTS: 'Deck Slapper Boots', ItemGlobals.DEER_SKIN_ANKLE_BOOTS: 'Deer Skin Ankle Boots', ItemGlobals.LEATHER_ANKLE_BOOTS: 'Leather Ankle Boots', ItemGlobals.CLOPPER_ANKLE_BOOTS: 'Clopper Ankle Boots', ItemGlobals.BOARDWALK_BOOTS: 'Boardwalk Boots', ItemGlobals.SHOP_BOOTS: 'Shop Boots', ItemGlobals.CORINTHIAN_ANKLE_BOOTS: 'Corinthian Ankle Boots', ItemGlobals.PEASANT_BOOTS: 'Peasant Boots', ItemGlobals.RECRUIT_SHORT_BOOTS: 'Recruit Short Boots', ItemGlobals.ADVENTURE_SHORT_BOOTS: 'Adventure Short Boots', ItemGlobals.BUCKLE_SHORT_BOOTS: 'Buckle Short Boots', ItemGlobals.RAMPART_BOOTS: 'Rampart Boots', ItemGlobals.GANGPLANK_BOOTS: 'Gangplank Boots', ItemGlobals.SIDEWALK_BOOTS: 'Sidewalk Boots', ItemGlobals.STITCH_BOOTS: 'Stitch Boots', ItemGlobals.FIELD_BOOTS: 'Field Boots', ItemGlobals.PLANTATION_BOOTS: 'Plantation Boots', ItemGlobals.TRYST_BOOTS: 'Tryst Boots', ItemGlobals.GREEN_PURPLE_BOOTS: 'Green Purple Boots', ItemGlobals.GOLD_BUTTONS_BOOTS: 'Gold Buttons Boots', ItemGlobals.VIOLET_SILVER_BOOTS: 'Violet Silver Boots', ItemGlobals.SILVER_TALL_BOOTS: 'Dusk Boots', ItemGlobals.XMAS_SHORT_BOOTS: 'Winter Festival Boots', ItemGlobals.MARDI_GRAS_SHORT_BOOTS: 'Mardi Gras Boots', ItemGlobals.SAINT_PATRICKS_KNEE_BOOTS: "St. Patrick's Boots", ItemGlobals.VALENTINES_SHORT_BOOTS: "Valentine's Boots", ItemGlobals.BARONESS_SHORT_BOOTS: 'Baroness Boots', ItemGlobals.ROGUE_PRIVATEER_SHORT_BOOTS: 'Rogue Privateer Boots', ItemGlobals.FRENCH_ASSASSIN_KNEE_BOOTS: 'French Assassin Boots', ItemGlobals.PEACOCK_KNEE_BOOTS: 'Peacock Boots', ItemGlobals.SCOURGE_KNEE_BOOTS: 'Scourge Boots', ItemGlobals.WILDFIRE_KNEE_BOOTS: 'Wildfire Boots', ItemGlobals.ZOMBIE_PIRATE_KNEE_BOOTS: 'Zombie Pirate Boots', ItemGlobals.ZOMBIES_PIRATE_KNEE_BOOTS: "Zombie Pirate's Boots", ItemGlobals.BOUNTYHUNTER_LADY_TALL_BOOTS: 'Bounty Hunter Boots', ItemGlobals.CHINA_WARRIOR__LADY_TALL_BOOTS: 'China Seas Warrior Boots', ItemGlobals.BARBARY_CORSAIR_LADY_TALL_BOOTS: 'Barbary Corsair Boots', ItemGlobals.SEA_SERPENT_LADY_TALL_BOOTS: 'Sea Serpent Boots', ItemGlobals.DIPLOMAT_SHORT_BOOTS: 'Diplomat Boots', ItemGlobals.PRINCE_SHORT_BOOTS: 'Prince Boots', ItemGlobals.RAVEN_SHORT_BOOTS: 'Raven Boots', ItemGlobals.VOYAGER_LADY_BOOTS: 'Voyager Boots', ItemGlobals.MAYOR_LADY_BOOTS: 'Mayor Boots', ItemGlobals.NAVY_SHOES: 'Navy Boots', ItemGlobals.EITC_SHOES: 'EITC Boots', ItemGlobals.LEATHER_KNEE_BOOTS: 'Leather Knee Boots', ItemGlobals.PLANKWALKER_BOOTS: 'Plank Walker Boots', ItemGlobals.CASTLE_BOOTS: 'Castle Boots', ItemGlobals.STROLL_BOOTS: 'Stroll Boots', ItemGlobals.STITCHED_KNEE_BOOTS: 'Stitched Knee Boots', ItemGlobals.CHILL_BOOTS: 'Chill Boots', ItemGlobals.RICH_KNEE_BOOTS: 'Rich Knee Boots', ItemGlobals.FOREST_KNEE_BOOTS: 'Forest Knee Boots', ItemGlobals.HARD_KNEE_BOOTS: 'Hard Knee Boots', ItemGlobals.CELTIC_TALL_BOOTS: 'Celtic Tall Boots', ItemGlobals.FENCER_BOOTS: "Fencer's Boots", ItemGlobals.DEER_SKIN_TALL_BOOTS: 'Deer Skin Tall Boots', ItemGlobals.SUEDE_TALL_BOOTS: 'Suede Tall Boots', ItemGlobals.BLUE_SILVER_BOOTS: 'Blue Silver Tall Boots', ItemGlobals.SUN_RIDER_TALL_BOOTS: 'Sun Rider Boots', ItemGlobals.TALL_COURT_BOOTS: 'Tall Court Boots', ItemGlobals.TRAVELERS_TALL_BOOTS: "Traveler's Tall Boots", ItemGlobals.GOLDEN_BROW_SPIKE: 'Golden Brow Spike', ItemGlobals.SILVER_BROW_SPIKE: 'Silver Brow Spike', ItemGlobals.GOLDEN_BROW_RING: 'Golden Brow Ring', ItemGlobals.SILVER_BROW_RING: 'Silver Brow Ring', ItemGlobals.GOLDEN_BROW_RING_SPIKE: 'Golden Brow Ring Spike', ItemGlobals.SILVER_BROW_RING_SPIKE: 'Silver Brow Ring Spike', ItemGlobals.TURQUOISE_BROW_SPIKE: 'Turquoise Brow Spike', ItemGlobals.SAPPHIRE_BROW_RING: 'Sapphire Brow Ring', ItemGlobals.GOLDEN_EAR_STUD: 'Golden Ear Stud', ItemGlobals.SILVER_EAR_STUD: 'Silver Ear Stud', ItemGlobals.GOLDEN_EAR_SMALL_LOOP: 'Golden Ear Small Loop', ItemGlobals.SILVER_EAR_SMALL_LOOP: 'Silver Ear Small Loop', ItemGlobals.GOLDEN_EAR_DOUBLE_LOOP: 'Golden Ear Double Loop', ItemGlobals.SILVER_EAR_DOUBLE_LOOP: 'Silver Ear Double Loop', ItemGlobals.GOLD_AND_SILVER_EAR_DOUBLE_LOOP: 'Gold and Silver Ear Double Loop', ItemGlobals.GOLDEN_SMALL_EAR_SPIKE: 'Golden Small Ear Spike', ItemGlobals.SILVER_SMALL_EAR_SPIKE: 'Silver Small Ear Spike', ItemGlobals.GOLDEN_LARGE_EAR_LOOP: 'Golden Large Ear Loop', ItemGlobals.SILVER_LARGE_EAR_LOOP: 'Silver Large Ear Loop', ItemGlobals.GOLDEN_LARGE_EAR_LOOP_WITH_DOUBLE: 'Golden Large Loop With Double Top Ring', ItemGlobals.SILVER_LARGE_EAR_LOOP_WITH_DOUBLE: 'Silver Large Loop With Double Top Ring', ItemGlobals.GOLDEN_EAR_CUFFS: 'Golden Ear Cuffs', ItemGlobals.SILVER_EAR_CUFFS: 'Silver Ear Cuffs', ItemGlobals.ONYX_LARGE_EAR_LOOP: 'Onyx Large Ear Loop', ItemGlobals.RUBY_AND_AMETHYST_EAR_STUD_AND_RING: 'Ruby and Amethyst Ear Stud and Ring', ItemGlobals.GOLDEN_NOSE_LOOP: 'Golden Nose Loop', ItemGlobals.SILVER_NOSE_LOOP: 'Silver Nose Loop', ItemGlobals.GOLDEN_NOSE_CENTER_LOOP: 'Golden Nose Center Loop', ItemGlobals.SILVER_NOSE_CENTER_LOOP: 'Silver Nose Center Loop', ItemGlobals.GOLDEN_NOSE_SPIKE: 'Golden Nose Spike', ItemGlobals.SILVER_NOSE_SPIKE: 'Silver Nose Spike', ItemGlobals.GOLDEN_DOUBLE_NOSE_SPIKE: 'Golden Double Nose Spike', ItemGlobals.SILVER_DOUBLE_NOSE_SPIKE: 'Silver Double Nose Spike', ItemGlobals.GOLDEN_NOSE_SPIKE_WITH_LOOP: 'Golden Nose Spike with Loop', ItemGlobals.SILVER_NOSE_SPIKE_WITH_LOOP: 'Silver Nose Spike with Loop', ItemGlobals.GOLDEN_DOUBLE_NOSE_SPIKE_WITH_LOOP: 'Golden Double Nose Spike with Loop', ItemGlobals.SILVER_DOUBLE_NOSE_SPIKE_WITH_LOOP: 'Silver Double Nose Spike with Loop', ItemGlobals.EMERALD_DOUBLE_NOSE_SPIKE: 'Emerald Double Nose Spike', ItemGlobals.GOLDEN_LIP_RING: 'Golden Lip Ring', ItemGlobals.SILVER_LIP_RING: 'Silver Lip Ring', ItemGlobals.GOLDEN_LIP_SPIKE: 'Golden Lip Spike', ItemGlobals.SILVER_LIP_SPIKE: 'Silver Lip Spike', ItemGlobals.GOLDEN_DOUBLE_LIP_RING: 'Golden Double Lip Ring', ItemGlobals.SILVER_DOUBLE_LIP_RING: 'Silver Double Lip Ring', ItemGlobals.RUBY_LIP_RING: 'Ruby Lip Ring', ItemGlobals.GOLDEN_BAND: 'Golden Band', ItemGlobals.SILVER_BAND: 'Silver Band', ItemGlobals.GOLDEN_RUBY_RING: 'Golden Ruby Ring', ItemGlobals.SILVER_RUBY_RING: 'Silver Ruby Ring', ItemGlobals.GOLDEN_AMETHIST_RING: 'Golden Amethist Ring', ItemGlobals.SILVER_AMETHIST_RING: 'Silver Amethist Ring', ItemGlobals.GOLDEN_SAPPHIRE_RING: 'Golden Sapphire Ring', ItemGlobals.SILVER_SAPPHIRE_RING: 'Silver Sapphire Ring', ItemGlobals.GOLDEN_TURQUOISE_RING: 'Golden Turquoise Ring', ItemGlobals.SILVER_TURQUOISE_RING: 'Silver Turquoise Ring', ItemGlobals.GOLDEN_EMERALD_RING: 'Golden Emerald Ring', ItemGlobals.SILVER_EMERALD_RING: 'Silver Emerald Ring', ItemGlobals.GOLDEN_ONYX_RING: 'Golden Onyx Ring', ItemGlobals.SILVER_ONYX_RING: 'Silver Onyx Ring', ItemGlobals.GOLDEN_DOUBLE_BAND: 'Golden Double Band', ItemGlobals.SILVER_DOUBLE_BAND: 'Silver Double Band', ItemGlobals.GOLDEN_KNUCKLES: 'Golden Knuckles', ItemGlobals.SILVER_KNUCKLES: 'Silver Knuckles', ItemGlobals.TATTOO_CHEST_DAGGER: 'Dagger Chest Tattoo', ItemGlobals.TATTOO_CHEST_HEART_TORCH: 'Heart Chest Tattoo', ItemGlobals.TATTOO_CHEST_LOCK_KEY: 'Lock and Key Chest Tattoo', ItemGlobals.TATTOO_CHEST_SKULL_DAGGER: 'Skull and Dagger Chest Tattoo', ItemGlobals.TATTOO_CHEST_SMALL_SKULL_CROSS: 'Small Skull and Cross Chest Tattoo', ItemGlobals.TATTOO_CHEST_ANCHOR: 'Anchor Chest Tattoo', ItemGlobals.TATTOO_CHEST_COMPASS: 'Compass Chest Tattoo', ItemGlobals.TATTOO_CHEST_DAGGER_SCROLL: 'Dagger Scroll Chest Tattoo', ItemGlobals.TATTOO_CHEST_SHIP_ANCHOR: 'Ship Anchor Chest Tattoo', ItemGlobals.TATTOO_CHEST_SMALL_SKULL_CROSSBONES: 'Skull and Crossbones Chest Tattoo', ItemGlobals.TATTOO_CHEST_SQUID_AND_SHIP: 'Squid and Ship Chest Tattoo', ItemGlobals.TATTOO_CHEST_SAINT_PATRICKS_DAY: "Saint Patrick's Day Chest Tattoo", ItemGlobals.TATTOO_CHEST_CELTIC_LEAF: 'Celtic Leaf Chest Tattoo', ItemGlobals.TATTOO_CHEST_SMALL_ETHNIC_EAGLE: 'Small Ethnic Eagle Chest Tattoo', ItemGlobals.TATTOO_CHEST_SMALL_CROSSED_FLINTLOCKS: 'Crossed Flintlocks Chest Tattoo', ItemGlobals.TATTOO_CHEST_SHAMROCK: 'Shamrock Chest Tattoo', ItemGlobals.TATTOO_CHEST_SMALL_THAI_MONKEY: 'Thai Monkey Small Chest Tattoo', ItemGlobals.TATTOO_CHEST_HAWAIIAN_PECTORAL: 'Hawaiin Pectoral Chest Tattoo', ItemGlobals.TATTOO_CHEST_SMALL_TRIBALYAKUZA: 'Tribal Yakuza Small Chest Tattoo', ItemGlobals.TATTOO_CHEST_SPANISH_SHIP_PVP: 'Spanish Chest Tattoo', ItemGlobals.TATTOO_CHEST_FRENCH_SHIP_PVP: 'French Chest Tattoo', ItemGlobals.TATTOO_CHEST_CLASSIC_MOTHERS_DAY: "Mother's Day Chest Tattoo", ItemGlobals.TATTOO_CHEST_HEALED_BULLET_HOLES: 'Bullet Chest Wound', ItemGlobals.TATTOO_CHEST_PIRATE_BRAND: 'Pirate Chest Brand', ItemGlobals.TATTOO_CHEST_LARGE_STITCHED_SCAR: 'Stitched Chest Scar', ItemGlobals.TATTOO_CHEST_STITCHED_BULLET_HOLES: 'Stitched Bullet Chest Wound', ItemGlobals.TATTOO_CHEST_LARGE_X_STITCH: 'X Chest Scar', ItemGlobals.TATTOO_CHEST_LARGE_Y_STITCH: 'Y Chest Scar', ItemGlobals.TATTOO_CHEST_FULL_CROSSED_FLINTLOCKS: 'Crossed Flintlocks Full Chest Tattoo', ItemGlobals.TATTOO_CHEST_FULL_TRIBAL_YAKUZA: 'Tribal Yakuza Full Chest Tattoo', ItemGlobals.TATTOO_CHEST_FULL_SKULL_CROSSBONES: 'Skull and Crossbones Full Chest Tattoo', ItemGlobals.TATTOO_CHEST_FULL_SKULL_CROSS: 'Skull Cross Full Chest Tattoo', ItemGlobals.TATTOO_CHEST_FULL_THAI_MONKEY: 'Thai Monkey Full Chest Tattoo', ItemGlobals.TATTOO_CHEST_FULL_ETHNIC_EAGLE: 'Ethnic Eagle Full Chest Tattoo', ItemGlobals.TATTOO_ARM_SHARK: 'Shark Arm Tattoo', ItemGlobals.TATTOO_ARM_SKULL_PIRATE: 'Pirate Skull Arm Tattoo', ItemGlobals.TATTOO_ARM_SKULL_SHIELD: 'Skull Shield Arm Tattoo', ItemGlobals.TATTOO_ARM_SKULL_STAB: 'Skull Dagger Arm Tattoo', ItemGlobals.TATTOO_ARM_SNAKES_DAGGER: 'Snakes and Dagger Arm Tattoo', ItemGlobals.TATTOO_ARM_FANCY_DAGGER: 'Fancy Dagger Arm Tattoo', ItemGlobals.TATTOO_ARM_SKULL_FLAG: 'Skull Flag Arm Tattoo', ItemGlobals.TATTOO_ARM_FANCY_KEY: 'Fancy Key Arm Tattoo', ItemGlobals.TATTOO_ARM_SKULL_IRON_CROSS: 'Iron Cross Arm Tattoo', ItemGlobals.TATTOO_ARM_SKULL_SCROLL: 'Skull Scroll Arm Tattoo', ItemGlobals.TATTOO_ARM_NAUTICAL_STAR: 'Nautical Star Arm Tattoo', ItemGlobals.TATTOO_ARM_MAYAN_FACE: 'Mayan Face Arm Tattoo', ItemGlobals.TATTOO_ARM_OCTOPUS: 'Octopus Arm Tattoo', ItemGlobals.TATTOO_ARM_TRIBAL_SKULL: 'Tribal Skull Arm Tattoo', ItemGlobals.TATTOO_ARM_SAINT_PATRICK: "Saint Patrick's Day Arm Tattoo", ItemGlobals.TATTOO_ARM_NATIVE_LIZARDS: 'Native Lizards Arm Tattoo', ItemGlobals.TATTOO_ARM_TRIBAL_SWIRL: 'Tribal Swirl Arm Tattoo', ItemGlobals.TATTOO_ARM_TRIBAL_BIRD: 'Tribal Bird Arm Tattoo', ItemGlobals.TATTOO_ARM_TRIBAL_JELLYFISH: 'Tribal Jellyfish Arm Tattoo', ItemGlobals.TATTOO_ARM_TRIBAL_JELLYFISHES: 'Tribal Jellyfish Arm Tattoo', ItemGlobals.TATTOO_ARM_ASIAN_LEAF: 'Asian Leaf Arm Tattoo', ItemGlobals.TATTOO_ARM_ETHNIC: 'Ethnic Arm Tattoo', ItemGlobals.TATTOO_ARM_MAORI_MAN: 'Maori Man Arm Tattoo', ItemGlobals.TATTOO_ARM_NATIVE_LEAF: 'Native Leaf Arm Tattoo', ItemGlobals.TATTOO_ARM_THAI: 'Thai Arm Tattoo', ItemGlobals.TATTOO_ARM_CELTIC_LEAF: 'Celtic Leaf Arm Tattoo', ItemGlobals.TATTOO_ARM_SHAMROCK: 'Shamrock Arm Tattoo', ItemGlobals.TATTOO_ARM_TIKI: 'Tiki Arm Tattoo', ItemGlobals.TATTOO_ARM_CELTIC_KNOT: 'Celtic Knot Arm Tattoo', ItemGlobals.TATTOO_ARM_TRIBAL_WAVES: 'Tribal Waves Arm Tattoo', ItemGlobals.TATTOO_ARM_SHARKS: 'Shark Arm Tattoo', ItemGlobals.TATTOO_ARM_CHINESE_KNOT: 'Chinese Knot Arm Tattoo', ItemGlobals.TATTOO_ARM_WAVE_FAN: 'Wave Fan Arm Tattoo', ItemGlobals.TATTOO_ARM_CELTIC_DEER: 'Celtic Deer Arm Tattoo', ItemGlobals.TATTOO_ARM_HAWAIIAN: 'Hawaiian Arm Tattoo', ItemGlobals.TATTOO_ARM_PETROGLYPH: 'Petroglyph Arm Tattoo', ItemGlobals.TATTOO_ARM_RAVENS: 'Ravens Arms Tattoo', ItemGlobals.TATTOO_ARM_SPANISH: 'Spanish Arm Tattoo', ItemGlobals.TATTOO_ARM_FRENCH: 'French Arm Tattoo', ItemGlobals.TATTOO_ARM_MOTHERS_DAY_FLOWERS_COLOR: "Mother's Day Flower Arm Tattoo", ItemGlobals.TATTOO_ARM_MOTHERS_DAY_SPARROWS: "Mother's Day Sparrows Arm Tattoo", ItemGlobals.TATTOO_ARM_OCTOPUS_SLEEVES: 'Octopus Arm Tattoo', ItemGlobals.TATTOO_ARM_HEALED_BULLET_HOLES: 'Bullet Arm Wound', ItemGlobals.TATTOO_ARM_PIRATE_BRAND: 'Pirate Arm Brand', ItemGlobals.TATTOO_ARM_STITCHED_SCAR: 'Stitched Arm Scar', ItemGlobals.TATTOO_ARM_STITCHED_BULLET_HOLES: 'Stitched Bullet Arm Wound', ItemGlobals.TATTOO_ARM_STITCHED_X: 'X Arm Scar', ItemGlobals.TATTOO_ARM_STITCHED_Y: 'Y Arm Scar', ItemGlobals.TATTOO_FACE_SKULL: 'Skull Face Paint', ItemGlobals.TATTOO_FACE_TWO_CLOVERS: 'Clover Face Paint', ItemGlobals.TATTOO_FACE_HORSE_SHOES: 'Horseshoe Face Paint', ItemGlobals.TATTOO_FACE_TRIBAL_FOREHEAD: 'Tribal Forehead Tattoo', ItemGlobals.TATTOO_FACE_TRIBAL_CHEEK: 'Tribal Cheek Tattoo', ItemGlobals.TATTOO_FACE_TRIBAL_CHIN: 'Tribal Chin Tattoo', ItemGlobals.TATTOO_FACE_JACK_EYES: "Jack's Eyes Face Paint", ItemGlobals.TATTOO_FACE_TRIBAL_GOATEE: 'Tribal Goatee Face Tattoo', ItemGlobals.TATTOO_FACE_MAORI_NOSE: 'Maori Nose Face Tattoo', ItemGlobals.TATTOO_FACE_MAORI_CHIN: 'Maori Nose Face Tattoo', ItemGlobals.TATTOO_FACE_NATIVE_EYE: 'Native Eye Face Tattoo', ItemGlobals.TATTOO_FACE_MOTHERS_DAY_FLOWER: "Mother's Day Flower Face Paint", ItemGlobals.TATTOO_FACE_MOTHERS_DAY_HEARTS: "Mother's Day Hearts Face Paint", ItemGlobals.TATTOO_FACE_PIRATE_BRAND: 'Pirate Face Brand', ItemGlobals.TATTOO_FACE_STITCHED_SCAR: 'Stiched Face Scar', ItemGlobals.TATTOO_FACE_STITCHED_X: 'X Face Scar', ItemGlobals.TATTOO_FACE_STITCHED_Y: 'Y Face Scar', ItemGlobals.TATTOO_FACE_COLOR_EYE_01: 'Eye Tattoo', ItemGlobals.TATTOO_FACE_COLOR_CHEEK: 'Cheek Tattoo', ItemGlobals.TATTOO_FACE_COLOR_TRIBAL_MOUTH: 'Tribal Mouth Tattoo', ItemGlobals.TATTOO_FACE_COLOR_VOODOO_01: 'Voodoo Goggles Tattoo', ItemGlobals.TATTOO_FACE_COLOR_VOODOO_02: 'Voodoo Circlet Tattoo', ItemGlobals.TATTOO_FACE_COLOR_VOODOO_03: 'Voodoo Thorns Tattoo', ItemGlobals.TATTOO_FACE_COLOR_VOODOO_04: 'Voodoo Forehead Tattoo', ItemGlobals.TATTOO_FACE_COLOR_VOODOO_05: 'Voodoo Mask Tattoo'
}

def getItemName(itemId):
    return ItemNames.get(itemId, 'Error, no name')


ItemFlavorText = {
    ItemGlobals.RUSTY_CUTLASS: "It's a bit crude, but it still has an edge.", ItemGlobals.IRON_CUTLASS: 'A well crafted iron blade. A good weapon!', ItemGlobals.STEEL_CUTLASS: 'An ornate steel cutlass. Well balanced and sharp!', ItemGlobals.FINE_CUTLASS: "A Fine Cutlass. It is crafted with pride by the Caribbean's best blacksmiths.", ItemGlobals.PIRATE_BLADE: 'A Pirate Blade, a clear warning sign to any EITC or Navy blokes.', ItemGlobals.SHORT_CUTLASS: 'A shorter cutlass meant for close quarters.', ItemGlobals.VOODOO_CUTLASS: 'Enchanted with a voodoo hex that heals the user.', ItemGlobals.BATTLE_CUTLASS: 'A powerful fighting weapon.', ItemGlobals.ORNATE_CUTLASS: 'A strong cutlass with a golden hilt.', ItemGlobals.GRAND_CUTLASS: 'A long cutlass with a mighty swing.', ItemGlobals.ROYAL_CUTLASS: 'A mighty cutlass used by the Royal Guard.', ItemGlobals.RUSTY_SABRE: 'A rusty sabre, able to make fast attacks!', ItemGlobals.LIGHT_SABRE: 'Sabres are quick swords able to deal rapid fast attacks.', ItemGlobals.IRON_SABRE: 'A plain sabre, able to deal fast rapid strikes!', ItemGlobals.STEEL_SABRE: 'A plain steel sabre.  Strong and fast.', ItemGlobals.FINE_SABRE: 'A well-balanced and swift blade.', ItemGlobals.WAR_SABRE: 'A powerful military sabre used in wars.', ItemGlobals.MASTER_SABRE: 'A masterful sabre used by the best fighters.', ItemGlobals.WORN_BROADSWORD: 'Broadswords can hit multiple enemies in one slash.', ItemGlobals.IRON_BROADSWORD: 'Broadswords are heavy swords that can cut through many enemies at once.', ItemGlobals.LIGHT_BROADSWORD: 'Broadswords can hit multiple enemies in one slash.', ItemGlobals.SMALL_BROADSWORD: 'Its powerful slashes can hit all nearby enemies!', ItemGlobals.STEEL_BROADSWORD: 'A heavy steel sword used by the military.', ItemGlobals.MIGHTY_BROADSWORD: 'A heavy sword able to hit many foes at once.', ItemGlobals.ORNATE_BROADSWORD: 'A hefty sword forged by a master blacksmith.', ItemGlobals.GREAT_BROADSWORD: 'A powerful heavy blade.', ItemGlobals.FLINTLOCK_PISTOL: 'A standard flintlock pistol. Fires one shot before it needs to be reloaded.', ItemGlobals.DOUBLE_BARREL: 'A flintlock pistol with two barrels. Each barrel can be fired separately before reloading.', ItemGlobals.TRI_BARREL: 'A multi-barreled pistol! This rare device can fire three times before reloading.', ItemGlobals.HEAVY_TRI_BARREL: 'A Heavy Tri-Barrel Pistol, a fine piece of weaponry.', ItemGlobals.GRAND_PISTOL: 'A Grand Pistol, equipped with three deadly barrels.', ItemGlobals.IRON_PISTOL: 'Fires one shot before it needs to be reloaded.', ItemGlobals.STEEL_PISTOL: 'A well-crafted steel pistol.  Fires one shot.', ItemGlobals.ORNATE_PISTOL: 'A fancy pistol created by a master Gunsmith.', ItemGlobals.IRON_BAYONET: 'Looks like it once belonged to a Navy Cadet.', ItemGlobals.STEEL_BAYONET: 'A powerful rifle that can fight up-close or from far away.', ItemGlobals.MASTER_BAYONET: 'A master-crafted weapon, made by the best rifle makers.', ItemGlobals.SAILOR_MUSKET: 'Has great range, but cannot fire if you are too close to the enemy.', ItemGlobals.BOARDING_MUSKET: 'Often used by pirates when boarding an enemy ship.', ItemGlobals.ROYAL_MUSKET: 'A gold musket used by the Royal Guard.', ItemGlobals.SMALL_BLUNDERBUSS: 'Fires a powerful spread-shot  Short range only.', ItemGlobals.FINE_BLUNDERBUSS: 'Short ranged attack, but can hit a group of enemies.', ItemGlobals.ROYAL_BLUNDERBUSS: 'A mighty hand-cannon decorated with gold.', ItemGlobals.TWIN_BARREL_PISTOL: 'A pistol with two barrels. Each barrel can be fired separately before reloading.', ItemGlobals.STEEL_REPEATER: 'A repeater pistol! This gun can fire three times before reloading.', ItemGlobals.ORNATE_REPEATER: 'An expert gun! This gun can fire three times before reloading.', ItemGlobals.VOLLEY_PISTOL: 'A three-barreled gun! This gun can fire three times before reloading.', ItemGlobals.VOODOO_DOLL: 'A mystical doll said to be able to bind to the spirit of anything it touches.', ItemGlobals.CLOTH_DOLL: 'A powerful doll able to bind to the spirits of the living and the dead.', ItemGlobals.WITCH_DOLL: 'An elaborate oriental doll able to strongly bind to the spirits of others.', ItemGlobals.PIRATE_DOLL: 'A Pirate Doll. Bind to the spirits of the Caribbean with this rare doll.', ItemGlobals.TABOO_DOLL: 'A Taboo Doll. Many pirates fear the power and unknowns of this legendary doll.', ItemGlobals.FURY_DOLL: 'This dark doll can give other pirates berserk power.', ItemGlobals.RAGE_DOLL: 'An evil voodoo doll filled with anger.', ItemGlobals.GRUDGER_DOLL: 'A dark doll shaped like a tough pirate.', ItemGlobals.VENGEFUL_DOLL: 'A grim doll that increases the battle fury in others.', ItemGlobals.WRATH_DOLL: 'A doll shaped like an infamous pirate.', ItemGlobals.COTTON_SOLL: 'A mystical doll able to protect others from evil voodoo.', ItemGlobals.ORNATE_DOLL: 'A fancy doll which protects others from harmful voodoo.', ItemGlobals.ENCHANTED_DOLL: 'Enchanted with strong hexes to ward off evil.', ItemGlobals.MAGIC_DOLL: 'A rare doll that pulses with voodoo magic.', ItemGlobals.MYSTERIOUS_DOLL: 'A mysterious voodoo doll with powerful protection spells on it.', ItemGlobals.HEALING_DOLL: 'Spirit Dolls increase the power of your Healing Voodoo skills.', ItemGlobals.MENDING_DOLL: 'Increases your ability to heal others.', ItemGlobals.RESTORATION_DOLL: 'A doll filled with good voodoo power.', ItemGlobals.RENEWAL_DOLL: 'A festive doll that glows with good voodoo magic.', ItemGlobals.LIFE_DOLL: 'A powerful voodoo doll with mighty healing powers.', ItemGlobals.BASIC_DAGGER: 'A sharp dagger. Small but deadly.', ItemGlobals.BATTLE_DIRK: 'A long knife. Well balanced for fighting.', ItemGlobals.MAIN_GAUCHE: 'A fancy blade that is useful for keeping your opponent off guard.', ItemGlobals.COLTELLO: "A Coltello dagger, it is a pirate's best friend in the right fight.", ItemGlobals.BLOODLETTER: 'A Bloodletter dagger. It is meticulously designed to fend off even the largest of foes.', ItemGlobals.SMALL_DAGGER: 'Daggers cause more damage when attacking enemies in the back.', ItemGlobals.STEEL_DAGGER: 'A sneaky blade.  Deals more damage when attacking enemies in the back.', ItemGlobals.COMBAT_DAGGER: 'A fighting knife.  Deals more damage when attacking enemies in the back.', ItemGlobals.BATTLE_DAGGER: 'Often used in duels.  Deals more damage when attacking enemies in the back.', ItemGlobals.WAR_DAGGER: 'Forged for combat.  Deals more damage when attacking enemies in the back.', ItemGlobals.SMALL_THROWING_KNIVES: 'Throwing Knives are great ranged weapons. Faster recharge on Throwing Skills.', ItemGlobals.IRON_THROWING_KNIVES: 'Sturdy throwing weapon. Faster recharge on Throwing Skills.', ItemGlobals.TRIBAL_THROWING_KNIVES: 'Tribal hunting weapon. Faster recharge on Throwing Skills.', ItemGlobals.FINE_THROWING_KNIVES: 'Golden throwing knives. Faster recharge on Throwing Skills.', ItemGlobals.MASTER_THROWING_KNIVES: 'Master crafted throwing knives. Faster recharge on Throwing Skills.', ItemGlobals.POISONED_KNIFE: 'Coated with poison. Increases the damage on all your Debuffs.', ItemGlobals.VENOM_KNIFE: 'Laced with venom. Increases the damage on all your Debuffs.', ItemGlobals.TOXIC_KNIFE: 'Covered in toxic venom. Increases the damage on all your Debuffs.', ItemGlobals.PLAGUE_KNIFE: 'A deadly knife. Increases the damage on all your Debuffs.', ItemGlobals.DIRE_KNIFE: 'Coated in strong poison. Increases the damage on all your Debuffs.', ItemGlobals.CURSED_STAFF: 'A tribal fetish used for summoning evil spirits.', ItemGlobals.WARPED_STAFF: 'A powerful fetish used for summoning and controlling spirits.', ItemGlobals.REND_STAFF: 'Sought after by many, this fetish allows the bearer to speak to the spirits of the dead.', ItemGlobals.HARROW_STAFF: 'Harrow Staff. Inflict the secrets of the dead upon your enemies with this rare staff.', ItemGlobals.VILE_STAFF: 'Vile Staff. Summon the plagues of the dead and unknown against your foes.', ItemGlobals.BONE_STAFF: 'Radiates a strong aura that increases the Attack Power of nearby friends.', ItemGlobals.GRIM_STAFF: 'A grim staff filled with dark power.', ItemGlobals.SKELETAL_STAFF: 'Made from the bones of animals.  Pulses with dark power.', ItemGlobals.UNDEAD_STAFF: 'A frightening staff that pulses with hostile energy.', ItemGlobals.DEATH_STAFF: 'A cursed staff used to channel dark energy.', ItemGlobals.HEALING_STAFF: 'Pulses with an aura that heals all friendly pirates slowly.', ItemGlobals.MENDING_STAFF: 'This wooden staff is filled with healing voodoo energy.', ItemGlobals.RESTORATION_STAFF: 'Glows with healing energy that can heal others nearby.', ItemGlobals.RENEWAL_STAFF: "Uses the earth's elements to heal others.", ItemGlobals.LIFE_STAFF: 'This staff glows with healing power.', ItemGlobals.DEFENDER_STAFF: 'Has a protective aura that increases defense for nearby pirates.', ItemGlobals.WARDEN_STAFF: 'Covered in defensive wards and trinkets.', ItemGlobals.OVERSEER_STAFF: 'A tribal voodoo staff with strong defensive magic.', ItemGlobals.GUARDIAN_STAFF: "Protects nearby friends when using it's aura.", ItemGlobals.TRIBAL_CHIEF_STAFF: 'Glows with protective voodoo energy.', ItemGlobals.GRENADE_POUCH: 'Grenades are highly lethal explosives. They are effective against large crowds of enemies!', ItemGlobals.TONIC: 'Eases pain. Smells kinda strong too.', ItemGlobals.REMEDY: 'An exotic remedy. Said to cure all maladies.', ItemGlobals.HOLY_WATER: 'Water blessed by the angels and gods.', ItemGlobals.ELIXIR: 'The one and only, legendary Elixir of Life!', ItemGlobals.MIRACLE_WATER: 'A miracle potion said to cure all sicknesses and regrow hair!', ItemGlobals.ROAST_PORK: 'A tasty chunk of pork.', ItemGlobals.POTION_CANNON_1: 'Increases cannon damage by 10% for 180 seconds', ItemGlobals.POTION_CANNON_2: 'Increases cannon damage by 15% for 240 seconds', ItemGlobals.POTION_CANNON_3: 'Increases cannon damage by 20% for 300 seconds', ItemGlobals.POTION_PISTOL_1: 'Increases pistol damage by 10% for 180 seconds', ItemGlobals.POTION_PISTOL_2: 'Increases pistol damage by 15% for 240 seconds', ItemGlobals.POTION_PISTOL_3: 'Increases pistol damage by 20% for 300 seconds', ItemGlobals.POTION_CUTLASS_1: 'Increases cutlass damage by 10% for 180 seconds', ItemGlobals.POTION_CUTLASS_2: 'Increases cutlass damage by 15% for 240 seconds', ItemGlobals.POTION_CUTLASS_3: 'Increases cutlass damage by 20% for 300 seconds', ItemGlobals.POTION_DOLL_1: 'Increases voodoo damage by 10% for 180 seconds', ItemGlobals.POTION_DOLL_2: 'Increases voodoo damage by 15% for 240 seconds', ItemGlobals.POTION_DOLL_3: 'Increases voodoo damage by 20% for 300 seconds', ItemGlobals.POTION_SPEED_1: 'Increases run speed by 30% for 60 seconds', ItemGlobals.POTION_SPEED_2: 'Increases run speed by 30% for 180 seconds', ItemGlobals.POTION_SPEED_3: 'Increases run speed by 30% for 360 seconds', ItemGlobals.POTION_REP_1: 'Increases reputation gained by 15% for 180 seconds', ItemGlobals.POTION_REP_2: 'Increases reputation gained by 30% for 180 seconds', ItemGlobals.POTION_REP_COMP: 'Increases reputation gained by 500% for an hour!', ItemGlobals.POTION_GOLD_1: 'Increases gold earned by 10% for 180 seconds', ItemGlobals.POTION_GOLD_2: 'Increases gold earned by 20% for 180 seconds', ItemGlobals.POTION_INVIS_1: 'Grants invisibility for 60 seconds', ItemGlobals.POTION_INVIS_2: 'Grants invisibility for 60 seconds', ItemGlobals.POTION_REGEN_1: 'Restores 3% of health every 2 seconds for 120 seconds', ItemGlobals.POTION_REGEN_2: 'Restores 3% of health every 2 seconds for 180 seconds', ItemGlobals.POTION_REGEN_3: 'Restores 3% of health every 2 seconds for 240 seconds', ItemGlobals.POTION_REGEN_4: 'Restores 3% of health every 2 seconds for 300 seconds', ItemGlobals.POTION_BURP: 'This fizzy drink will make you belch!', ItemGlobals.POTION_FART: 'A spicy concoction meant for pirate chili. Warning: drinking this straight may make you fart.', ItemGlobals.POTION_VOMIT: 'This potion will make you puke!', ItemGlobals.POTION_HEADGROW: 'This potion makes your head huge!', ItemGlobals.POTION_FACECOLOR: 'This potion changes your color!', ItemGlobals.POTION_SHRINK: "Either the world is getting bigger or you're shrinking!", ItemGlobals.POTION_GROW: 'Makes you huge! Careful not to step on any garrisons', ItemGlobals.POTION_HEADONFIRE: 'This potion lights your head on fire!', ItemGlobals.POTION_SCORPION: 'This potion transforms you into a scorpion!', ItemGlobals.POTION_ALLIGATOR: 'This potion transforms you into an alligator!', ItemGlobals.POTION_CRAB: 'This potion transforms you into a crab!', ItemGlobals.POTION_ACC_1: 'Increases weapon accuracy by 10% for 180 seconds', ItemGlobals.POTION_ACC_2: 'Increases weapon accuracy by 15% for 240 seconds', ItemGlobals.POTION_ACC_3: 'Increases weapon accuracy by 20% for 300 seconds', ItemGlobals.POTION_GROG: 'Grogg-away removes groggy effects in pirates and chickens.', ItemGlobals.POTION_REP_3: 'Increases reputation gained by 30% for 180 seconds', ItemGlobals.POTION_FART_2: 'This potion will make you fart, a lot!', ItemGlobals.STAFF_ENCHANT_1: 'Assists in staff creation', ItemGlobals.STAFF_ENCHANT_2: 'Assists in staff enchantment', ItemGlobals.POTION_SUMMON_CHICKEN: 'Summons a mighty chicken, scares off those deathly afraid of chickens!', ItemGlobals.POTION_SUMMON_WASP: 'Summons an intimidating wasp, let your foes cuddle it!', ItemGlobals.POTION_SUMMON_DOG: 'Summons a mostly scruffy, but slightly loyal dog!'
}

def getItemFlavorText(itemId):
    itemClass = ItemGlobals.getClass(itemId)
    flavorText = ItemGlobals.getFlavorText(itemId)
    if itemClass == InventoryType.ItemTypeClothing:
        return ClothingFlavorText.get(flavorText, 'Error, no flavor')
    elif itemClass == InventoryType.ItemTypeJewelry:
        return JewelryFlavorText.get(flavorText)
    elif itemClass == InventoryType.ItemTypeTattoo:
        return TattooFlavorText.get(flavorText)
    else :
        return ItemFlavorText.get(itemId, '')


ItemRarityNames = {
    ItemGlobals.CRUDE: 'Crude', ItemGlobals.COMMON: 'Common', ItemGlobals.RARE: 'Rare', ItemGlobals.FAMED: 'Famed', ItemGlobals.LEGENDARY: 'Legendary'
}

def getItemRarityName(itemId):
    name = ItemRarityNames.get(itemId)
    if name:
        return name
    return ''


ItemTypeNames = {
    ItemGlobals.SWORD: 'Sword', ItemGlobals.GUN: 'Gun', ItemGlobals.DOLL: 'Doll', ItemGlobals.DAGGER: 'Dagger', ItemGlobals.GRENADE: 'Grenade', ItemGlobals.STAFF: 'Staff', ItemGlobals.CANNON: 'Cannon', ItemGlobals.SAILING: 'Sailing', ItemGlobals.AXE: 'Axe', ItemGlobals.FENCING: 'Fencing', ItemGlobals.POTION: 'Potions', ItemGlobals.ODDS_AND_ENDS: 'Odds and Ends'
}

def getItemTypeName(itemId):
    name = ItemTypeNames.get(itemId)
    if name:
        return name
    return ''


ItemSubtypeNames = {
    ItemGlobals.CUTLASS: 'Cutlass', ItemGlobals.SABRE: 'Sabre', ItemGlobals.BROADSWORD: 'Broadsword', ItemGlobals.PISTOL: 'Pistol', ItemGlobals.REPEATER: 'Repeater Pistol', ItemGlobals.BLUNDERBUSS: 'Blunderbuss', ItemGlobals.MUSKET: 'Musket', ItemGlobals.BAYONET: 'Bayonet', ItemGlobals.BASIC_DOLL: 'Voodoo Doll', ItemGlobals.BASIC_STAFF: 'Voodoo Staff', ItemGlobals.BANE: 'Bane Doll', ItemGlobals.MOJO: 'Mojo Doll', ItemGlobals.SPIRIT: 'Spirit Doll', ItemGlobals.DAGGER_SUBTYPE: 'Dagger', ItemGlobals.DIRK: 'Throwing Knives', ItemGlobals.KRIS: 'Dark Blades', ItemGlobals.DARK: 'Dark Staff', ItemGlobals.NATURE: 'Nature Staff', ItemGlobals.WARDING: 'Warding Staff', ItemGlobals.RAM: 'Cannon Ram', ItemGlobals.BOARDING: 'Boarding', ItemGlobals.RAPIER: 'Rapier', ItemGlobals.EPEE: 'Epee', ItemGlobals.CARRONADE: 'Carronade', ItemGlobals.HEALING: 'Healing', ItemGlobals.SPYGLASS: 'Spyglass', ItemGlobals.NAVIGATION_TOOL: 'Navigation Tool', ItemGlobals.SEA_CHARM: 'Sea Charm', ItemGlobals.POTION_BUFF: 'Potion', ItemGlobals.CURSED_CUTLASS: 'Cursed Blade', ItemGlobals.CURSED_SABRE: 'Cursed Blade', ItemGlobals.CURSED_BROADSWORD: 'Cursed Blade', ItemGlobals.GRENADE_SUBTYPE: 'Grenades'
}

def getItemSubtypeName(itemId):
    return ItemSubtypeNames.get(itemId, '')


ItemSpeedNames = {
    ItemGlobals.SLOW: 'Slow', ItemGlobals.NORMAL: 'Normal', ItemGlobals.FAST: 'Fast'
}

def getItemSpeedName(itemId):
    return ItemSpeedNames.get(itemId, '')


ItemRangeNames = {
    ItemGlobals.SHORT: 'Short', ItemGlobals.MEDIUM: 'Medium', ItemGlobals.LONG: 'Long'
}

def getItemRangeName(itemId):
    return ItemRangeNames.get(itemId, '')


ItemAttributeNames = {
    ItemGlobals.CRITICAL: 'Critical Strike', ItemGlobals.VENOM: 'Venom Strike', ItemGlobals.POWERFUL: 'Powerful', ItemGlobals.PROTECT_COMBAT: 'Combat Protection', ItemGlobals.PROTECT_MISSILE: 'Projectile Protection', ItemGlobals.PROTECT_MAGIC: 'Magic Protection', ItemGlobals.PROTECT_GRENADE: 'Grenade Protection', ItemGlobals.DAMAGE_MANA: 'Voodoo Damage', ItemGlobals.SURE_FOOTED: 'Sure Footed', ItemGlobals.BLOOD_FIRE: 'Blood Fire', ItemGlobals.INFINITE_VENOM_SHOT: 'Infinite Venom Shot', ItemGlobals.INFINITE_BANE_SHOT: 'Infinite Bane Shot', ItemGlobals.INFINITE_HEX_EATER_SHOT: 'Infinite Hex Eater Shot', ItemGlobals.INFINITE_SILVER_SHOT: 'Infinite Silver Shot', ItemGlobals.INFINITE_STEEL_SHOT: 'Infinite Steel Shot', ItemGlobals.INFINITE_ASP: 'Infinite Asp', ItemGlobals.INFINITE_ADDER: 'Infinite Adder', ItemGlobals.INFINITE_SIDEWINDER: 'Infinite Sidewinder', ItemGlobals.INFINITE_VIPER_NEST: "Infinite Viper's Nest", ItemGlobals.INFINITE_CHAIN_SHOT: 'Infinite Chain Shot', ItemGlobals.INFINITE_EXPLOSIVE: 'Infinite Explosive', ItemGlobals.INFINITE_GRAPE_SHOT: 'Infinite Grape Shot', ItemGlobals.INFINITE_FIREBRAND: 'Infinite Firebrand', ItemGlobals.INFINITE_THUNDERBOLT: 'Infinite Thunderbolt', ItemGlobals.INFINITE_FURY: 'Infinite Fury', ItemGlobals.LEECH_HEALTH: 'Drain Health', ItemGlobals.LEECH_VOODOO: 'Drain Voodoo', ItemGlobals.CRITICAL_ROUND_SHOT: 'Critical Round Shot', ItemGlobals.CRITICAL_CHAIN_SHOT: 'Critical Chain Shot', ItemGlobals.CRITICAL_EXPLOSIVE: 'Critical Explosive', ItemGlobals.CRITICAL_GRAPE_SHOT: 'Critical Grape Shot', ItemGlobals.CRITICAL_FIREBRAND: 'Critical Firebrand', ItemGlobals.CRITICAL_FURY: 'Critical Fury', ItemGlobals.RANGE_ROUND_SHOT: 'Extra Round Shot Range', ItemGlobals.RANGE_CHAIN_SHOT: 'Extra Chain Shot Range', ItemGlobals.RANGE_EXPLOSIVE: 'Extra Explosive Range', ItemGlobals.RANGE_GRAPE_SHOT: 'Extra Grape Shot Range', ItemGlobals.RANGE_FIREBRAND: 'Extra Firebrand Range', ItemGlobals.RANGE_FURY: 'Extra Fury Range', ItemGlobals.IMMUNITY_POISON: 'Poison Immunity', ItemGlobals.IMMUNITY_ACID: 'Acid Immunity', ItemGlobals.IMMUNITY_BLIND: 'Blindness Immunity', ItemGlobals.IMMUNITY_FIRE: 'Fire Immunity', ItemGlobals.IMMUNITY_HOLD: 'Snare Immunity', ItemGlobals.IMMUNITY_STUN: 'Stun Immunity', ItemGlobals.IMMUNITY_PAIN: 'Pain Immunity', ItemGlobals.IMMUNITY_CURSE: 'Cursed Immunity', ItemGlobals.IMMUNITY_WEAKEN: 'Weaken Immunity', ItemGlobals.IMMUNITY_LIFEDRAIN: 'Life Drain Immunity', ItemGlobals.HALF_DURATION_POISON: 'Poison Resistance', ItemGlobals.HALF_DURATION_ACID: 'Acid Resistance', ItemGlobals.HALF_DURATION_BLIND: 'Blindness Resistance', ItemGlobals.HALF_DURATION_FIRE: 'Fire Resistance', ItemGlobals.HALF_DURATION_HOLD: 'Snare Resistance', ItemGlobals.HALF_DURATION_STUN: 'Stun Resistance', ItemGlobals.HALF_DURATION_CURSE: 'Cursed Resistance', ItemGlobals.HALF_DURATION_PAIN: 'Pain Resistance', ItemGlobals.HALF_DURATION_WOUND: 'Wounded Resistance', ItemGlobals.HALF_DAMAGE_LIFEDRAIN: 'Life Drain Resistance', ItemGlobals.HALF_DAMAGE_SOULTAP: 'Desolation Resistance', ItemGlobals.NAVIGATION: 'Navigation', ItemGlobals.ANTI_VOODOO_ZOMBIE: 'Bonus Damage vs. Jumbees'
}

def getItemAttributeName(itemId):
    name = ItemAttributeNames.get(itemId)
    if name:
        return name
    return ''


ItemAttributeDescriptions = {
    ItemGlobals.CRITICAL: 'High chance to deal Critical Damage!', ItemGlobals.VENOM: 'Poisons the target.', ItemGlobals.POWERFUL: 'Increases the damage of the weapon.', ItemGlobals.PROTECT_COMBAT: 'Combat Protection', ItemGlobals.PROTECT_MISSILE: 'Projectile Protection', ItemGlobals.PROTECT_MAGIC: 'Magic Protection', ItemGlobals.PROTECT_GRENADE: 'Grenade Protection', ItemGlobals.DAMAGE_MANA: "Damages the enemy's Voodoo Power.", ItemGlobals.SURE_FOOTED: 'You cannot be Knocked Down.', ItemGlobals.BLOOD_FIRE: 'Defeating enemies makes your sword burn and deal more damage!', ItemGlobals.INFINITE_VENOM_SHOT: 'Unlimited gun ammo', ItemGlobals.INFINITE_BANE_SHOT: 'Unlimited gun ammo', ItemGlobals.INFINITE_HEX_EATER_SHOT: 'Unlimited gun ammo', ItemGlobals.INFINITE_SILVER_SHOT: 'Unlimited gun ammo', ItemGlobals.INFINITE_STEEL_SHOT: 'Unlimited gun ammo', ItemGlobals.INFINITE_ASP: 'Unlimited dagger ammo', ItemGlobals.INFINITE_ADDER: 'Unlimited dagger ammo', ItemGlobals.INFINITE_SIDEWINDER: 'Unlimited dagger ammo', ItemGlobals.INFINITE_VIPER_NEST: 'Unlimited dagger ammo', ItemGlobals.INFINITE_CHAIN_SHOT: 'Unlimited cannon ammo', ItemGlobals.INFINITE_EXPLOSIVE: 'Unlimited cannon ammo', ItemGlobals.INFINITE_GRAPE_SHOT: 'Unlimited cannon ammo', ItemGlobals.INFINITE_FIREBRAND: 'Unlimited cannon ammo', ItemGlobals.INFINITE_THUNDERBOLT: 'Unlimited cannon ammo', ItemGlobals.INFINITE_FURY: 'Unlimited cannon ammo', ItemGlobals.LEECH_HEALTH: 'Steals health when damaging the enemy.', ItemGlobals.LEECH_VOODOO: 'Steals voodoo when damaging the enemy.', ItemGlobals.CRITICAL_ROUND_SHOT: 'Chance for Critical Damage with this ammo', ItemGlobals.CRITICAL_CHAIN_SHOT: 'Chance for Critical Damage with this ammo', ItemGlobals.CRITICAL_EXPLOSIVE: 'Chance for Critical Damage with this ammo', ItemGlobals.CRITICAL_GRAPE_SHOT: 'Chance for Critical Damage with this ammo', ItemGlobals.CRITICAL_FIREBRAND: 'Chance for Critical Damage with this ammo', ItemGlobals.CRITICAL_FURY: 'Chance for Critical Damage with this ammo', ItemGlobals.RANGE_ROUND_SHOT: 'Increased Range for this ammo', ItemGlobals.RANGE_CHAIN_SHOT: 'Increased Range for this ammo', ItemGlobals.RANGE_EXPLOSIVE: 'Increased Range for this ammo', ItemGlobals.RANGE_GRAPE_SHOT: 'Increased Range for this ammo', ItemGlobals.RANGE_FIREBRAND: 'Increased Range for this ammo', ItemGlobals.RANGE_FURY: 'Increased Range for this ammo', ItemGlobals.IMMUNITY_POISON: '', ItemGlobals.IMMUNITY_ACID: '', ItemGlobals.IMMUNITY_BLIND: '', ItemGlobals.IMMUNITY_FIRE: '', ItemGlobals.IMMUNITY_HOLD: '', ItemGlobals.IMMUNITY_STUN: '', ItemGlobals.IMMUNITY_PAIN: '', ItemGlobals.IMMUNITY_CURSE: '', ItemGlobals.IMMUNITY_WEAKEN: '', ItemGlobals.IMMUNITY_LIFEDRAIN: '', ItemGlobals.HALF_DURATION_POISON: 'Half duration from Poison', ItemGlobals.HALF_DURATION_ACID: 'Half duration from Acid', ItemGlobals.HALF_DURATION_BLIND: 'Half duration from Blindness', ItemGlobals.HALF_DURATION_FIRE: 'Half duration from Fire', ItemGlobals.HALF_DURATION_HOLD: 'Half duration from Snare', ItemGlobals.HALF_DURATION_STUN: 'Half duration from Stun', ItemGlobals.HALF_DURATION_CURSE: 'Half duration from Curse', ItemGlobals.HALF_DURATION_PAIN: 'Half duration from Pain', ItemGlobals.HALF_DURATION_WOUND: 'Half duration from Wound', ItemGlobals.HALF_DAMAGE_LIFEDRAIN: 'Half damage from Life Drain', ItemGlobals.HALF_DAMAGE_SOULTAP: 'Half damage from Desolation', ItemGlobals.NAVIGATION: 'Faster Recharge on Full Sail, Come About, and Ramming Speed'
}

def getItemAttributeDescription(itemId):
    name = ItemAttributeDescriptions.get(itemId)
    if name:
        return name
    return ''


ItemAttackStrength = 'Attack: %s'
ItemSpeedStrength = 'Speed: %s'
ItemRangeStrength = 'Range: %s'
ItemSpecialAttack = '(Special Attack)'
ItemRank = '\x01slant\x01Rank %s\x02'
ItemBoost = '%s Boost'
ItemBarrels = 'Barrels: %s'
ItemLevelRequirement = '\x01slant\x01Requires Level %s %s\x02'
ItemTrainingRequirement = '\x01slant\x01Requires %s Training\x02'
UnlimitedAccessRequirement = '\x01slant\x01Unlimited Access Only\x02'
RightClickPotion = 'Right click to use'
WeaponSkill = '\x01slant\x01(Weapon Skill)\x02'
BreakAttackSkill = '\x01slant\x01(Break Attack)\x02'
DefenseSkill = '\x01slant\x01(Defense Skill)\x02'
ClickToLearn = 'Click to learn Skill!'
ClickToLearnCombo = 'Click to learn a new Combo Skill and lengthen your Combo Chain!'
ClickToLearnAmmo = 'Click to learn how to use a new Ammunition Type!'
ClickToLearnManeuver = 'Click to learn a new Ship Maneuver!'
UpgradesDamage = 'Upgrade to improve damage'
UpgradesHealing = 'Upgrade to improve healing power'
UpgradesMpDamage = 'for Health and ' + ManaName
UpgradesDuration = 'Upgrade to increase the'
UnlocksAtLevel = 'Skill unlocks at Level %s'
And = 'and'
SkillDescriptions = {
    InventoryType.MeleeJab: ('', '', '', '', 0), InventoryType.MeleePunch: ('', '', '', '', 0), InventoryType.MeleeKick: ('', '', '', '', 0), InventoryType.MeleeRoundhouse: ('', '', '', '', 0), InventoryType.MeleeHeadbutt: ('', '', '', '', 0), InventoryType.MeleeHaymaker: ('', '', '', '', 0), InventoryType.MeleeThrowDirt: ('', '', '', '', 0), InventoryType.MeleeToughness: ('', '', '', '', 0), InventoryType.MeleeIronSkin: ('', '', '', '', 0), InventoryType.MeleeDetermination: ('', '', '', '', 0), InventoryType.CutlassHack: (ComboSkill, 'A quick opening attack!', '', ClickToLearnCombo, 0), InventoryType.CutlassSlash: (ComboSkill, 'A broad slash!', '', ClickToLearnCombo, 0), InventoryType.CutlassCleave: (ComboSkill, 'A mighty overhead cleave!', '', ClickToLearnCombo, 0), InventoryType.CutlassFlourish: (ComboSkill, 'A series of fast slashes!', '', ClickToLearnCombo, 0), InventoryType.CutlassStab: (ComboSkill, 'A fancy finishing thrust!', '', ClickToLearnCombo, 0), InventoryType.CutlassParry: (PassiveSkill, 'Parry enemy attacks! %d%% chance to block incoming Combat Attacks!', 'Upgrade to increase your chance to Parry!', '', 1), InventoryType.CutlassEndurance: (PassiveSkill, 'Increases your maximum Health by %d%%!', 'Upgrade to increase your maximum Health!', '', 1), InventoryType.CutlassTaunt: (CombatSkill, 'Pulls enemy Aggression!', '', '', 0), InventoryType.CutlassBrawl: (CombatSkill, 'Fight dirty!', '', '', 0), InventoryType.CutlassSweep: (CombatSkill, 'A wide circular slash! Hits all nearby enemies!', '', '', 0), InventoryType.CutlassBladestorm: (CombatSkill, 'Delivers a barrage of sword slashes!', '', '', 0), EnemySkills.CUTLASS_ROLLTHRUST: (CombatSkill, 'A quick rolling strike!', '', '', 0), EnemySkills.CUTLASS_CURSED_FIRE: (CombatSkill, 'Uses Voodoo to burn the enemy!', '', '', 0), EnemySkills.CUTLASS_CURSED_ICE: (CombatSkill, 'Uses Voodoo to freeze the enemy in their tracks!', '', '', 0), EnemySkills.CUTLASS_CURSED_THUNDER: (CombatSkill, 'Uses Voodoo to strike the enemy with lightning!', '', '', 0), EnemySkills.CUTLASS_BLOWBACK: (CombatSkill, 'Knocks down all nearby foes!', '', '', 0), EnemySkills.CUTLASS_CAPTAINS_FURY: (CombatSkill, 'Powerful spinning attack!', '', '', 0), EnemySkills.CUTLASS_MASTERS_RIPOSTE: (CombatSkill, 'Increased Parry rate for a short time.', '', '', 0), EnemySkills.CUTLASS_POWER_ATTACK: (CombatSkill, 'A strong jumping slice!', '', '', 0), EnemySkills.CUTLASS_SKEWER: (CombatSkill, 'Pierce through enemies in a row! Causes Wounding.', '', '', 0), EnemySkills.CUTLASS_FIRE_BREAK: (CombatSkill, 'Release a wave of cursed burning flames!', '', '', 0), EnemySkills.CUTLASS_ICE_BREAK: (CombatSkill, 'Freezes all nearby enemies in place!', '', '', 0), EnemySkills.CUTLASS_THUNDER_BREAK: (CombatSkill, 'Strikes all nearby enemies with lightning!', '', '', 0), EnemySkills.BROADSWORD_HACK: (ComboSkill, 'A broad opening swing!', '', ClickToLearnCombo, 0), EnemySkills.BROADSWORD_SLASH: (ComboSkill, 'A mighty slash that hits nearby enemies!', '', ClickToLearnCombo, 0), EnemySkills.BROADSWORD_CLEAVE: (ComboSkill, 'A spinning cut that hits all nearby enemies!', '', ClickToLearnCombo, 0), EnemySkills.BROADSWORD_FLOURISH: (ComboSkill, 'A reverse spinning slash that hits all nearby enemies!', '', ClickToLearnCombo, 0), EnemySkills.BROADSWORD_STAB: (ComboSkill, 'A powerful finishing move!', '', ClickToLearnCombo, 0), EnemySkills.SABRE_HACK: (ComboSkill, 'A fast guarded attack!', '', ClickToLearnCombo, 0), EnemySkills.SABRE_SLASH: (ComboSkill, 'A graceful low slash!', '', ClickToLearnCombo, 0), EnemySkills.SABRE_CLEAVE: (ComboSkill, 'Rapid fire sword thrusts!', '', ClickToLearnCombo, 0), EnemySkills.SABRE_FLOURISH: (ComboSkill, 'A barrage of sword blows!', '', ClickToLearnCombo, 0), EnemySkills.SABRE_STAB: (ComboSkill, 'An impressive finishing slash!', '', ClickToLearnCombo, 0), InventoryType.PistolShoot: (AttackSkill, 'Basic shooting skill.', '', '', 0), InventoryType.PistolTakeAim: (AttackSkill, 'Hold down the attack button for an Aimed Shot! Increases the accuracy, range, and damage of the shot!', '', '', 0), InventoryType.PistolEagleEye: (PassiveSkill, 'Increases the maximum range for Firearms and ranged Dagger attacks by %d%%!', 'Upgrade to increase Range bonus of this Skill!', '', 1), InventoryType.PistolDodge: (PassiveSkill, '%d%% chance to Dodge incoming Ranged Attacks.', 'Upgrade to increase your chance to Dodge!', '', 1), InventoryType.PistolSharpShooter: (PassiveSkill, 'Increases accuracy for Firearms and ranged Dagger attacks by %d%%!', 'Upgrade Accuracy boost for Firearms and ranged Dagger attacks!', '', 1), InventoryType.PistolLeadShot: (AmmoSkill, 'Standard Ammunition.', '', ClickToLearnAmmo, 0), InventoryType.PistolBaneShot: (AmmoSkill, 'A cursed bullet.', '', ClickToLearnAmmo, 0), InventoryType.PistolSilverShot: (AmmoSkill, 'Made from solid silver.', '', ClickToLearnAmmo, 0), InventoryType.PistolHexEaterShot: (AmmoSkill, 'Damages ' + ManaName + ' as well as Health.', '', ClickToLearnAmmo, 0), InventoryType.PistolSteelShot: (AmmoSkill, 'The strongest metal shot.', '', ClickToLearnAmmo, 0), InventoryType.PistolVenomShot: (AmmoSkill, 'Coated with deadly venom.', '', ClickToLearnAmmo, 0), EnemySkills.PISTOL_SCATTERSHOT: (AttackSkill, 'Standard Blunderbuss spread-shot!', '', '', 0), EnemySkills.PISTOL_SCATTERSHOT_AIM: (AttackSkill, 'Hold down the attack button for an Aimed Shot! Increases the accuracy, range, and damage of the shot!', '', '', 0), EnemySkills.PISTOL_DEADEYE: (AttackSkill, 'Snipe your enemies from afar!', '', '', 0), EnemySkills.PISTOL_QUICKLOAD: (AttackSkill, 'Fire without reloading for a short time!', '', '', 0), EnemySkills.PISTOL_STUNSHOT: (AttackSkill, 'One deafening gun blast!', '', '', 0), EnemySkills.PISTOL_BREAKSHOT: (AttackSkill, 'A devastating canister shot!', '', '', 0), EnemySkills.PISTOL_POINT_BLANK: (AttackSkill, 'Deals one powerful attack that is more powerful up close!', '', '', 0), EnemySkills.PISTOL_HOTSHOT: (AttackSkill, 'Heated fiery ammunition!', '', '', 0), EnemySkills.PISTOL_RAPIDFIRE: (AttackSkill, 'Fire a blaze of bullets at the enemy!', '', '', 0), EnemySkills.BAYONET_PLAYER_RUSH: (AttackSkill, 'A standard Navy combo!', '', '', 0), EnemySkills.BAYONET_PLAYER_BASH: (AttackSkill, 'A crippling attack!', '', '', 0), EnemySkills.BAYONET_RUSH: (AttackSkill, 'A standard Navy combo!', '', '', 0), EnemySkills.BAYONET_BASH: (AttackSkill, 'A crippling attack!', '', '', 0), EnemySkills.BAYONET_DISABLE: (AttackSkill, 'Knockdown and disables one enemy!', '', '', 0), InventoryType.MusketShoot: ('', '', '', '', 0), InventoryType.MusketTakeAim: ('', '', '', '', 0), InventoryType.MusketDeadeye: ('', '', '', '', 0), InventoryType.MusketEagleEye: ('', '', '', '', 0), InventoryType.MusketCrackShot: ('', '', '', '', 0), InventoryType.MusketMarksman: ('', '', '', '', 0), InventoryType.MusketLeadShot: ('', '', '', ClickToLearnAmmo, 0), InventoryType.MusketScatterShot: ('', '', '', ClickToLearnAmmo, 0), InventoryType.MusketCursedShot: ('', '', '', ClickToLearnAmmo, 0), InventoryType.MusketCoalfireShot: ('', '', '', ClickToLearnAmmo, 0), InventoryType.MusketHeavySlug: ('', '', '', ClickToLearnAmmo, 0), InventoryType.MusketExploderShot: ('', '', '', ClickToLearnAmmo, 0), InventoryType.SailBroadsideLeft: (ShipSkill, 'Fire left broadside.', 'Upgrade to increase Left Broadside Cannonball damage!', ClickToLearnManeuver, 1), InventoryType.SailBroadsideRight: (ShipSkill, 'Fire right broadside.', 'Upgrade to increase Right Broadside Cannonball damage!', ClickToLearnManeuver, 1), InventoryType.SailFullSail: (ShipSkill, "Coaxes a short burst of speed out of the ship. Interrupts the 'Come About' Maneuver.", 'Upgrade to increase Maneuver duration!', ClickToLearnManeuver, 0), InventoryType.SailComeAbout: (ShipSkill, "Allows your ship to make a hard sudden turn. Interrupts the 'Full Sail' Maneuver.", 'Upgrade to increase Maneuver duration!', ClickToLearnManeuver, 0), InventoryType.SailOpenFire: (OrderSkill, 'Call upon your shipmates to fire cannons for great effect!', 'Upgrade to increase Open Fire duration!', '', 0), InventoryType.SailRammingSpeed: (ShipSkill, 'Bear down upon an enemy vessel and ram it into splinters! Interrupts all other Sailing Maneuvers.', 'Upgrade to improve ship ramming damage!', ClickToLearnManeuver, 0), InventoryType.SailTakeCover: (OrderSkill, 'Protect your ship and shipmates from incoming fire.', 'Upgrade to increase Take Cover duration!', '', 0), InventoryType.SailPowerRecharge: (ShipSkill, 'Temporarily increases the rate of recharging sailing and cannon skills for the ship.', 'Unlocked after you recover the Black Pearl!', '', 0), InventoryType.SailWindcatcher: (PassiveSkill, 'A master of the sail, you know how to catch the wind in your sails for maximum speed. Increases ship speed by %d%%!', 'Upgrade to increase Speed bonus!', '', 1), InventoryType.SailTacking: (PassiveSkill, 'Superior knowledge of the rigging allows you to turn more rapidly. Improves ship turning radius by %d%%!', 'Upgrade to increase Maneuverability bonus!', '', 1), InventoryType.SailTreasureSense: (PassiveSkill, 'Your endeavours always seem to uncover more gold. Increases the quality of cargo drops by %d%%!', 'Upgrade to increase Cargo Drop bonus!', '', 1), InventoryType.SailTaskmaster: (PassiveSkill, 'A harsh taskmaster can get his shipmates to reload his cannons faster. Decreases cooldown time for Broadsides by %d%%!', 'Upgrade to decrease Broadside cooldown time!', '', 1), EnemySkills.SAIL_WRECK_HULL: (OrderSkill, 'Call upon your shipmates to fire cannons at hulls for great effect!', 'Upgrade to increase Wreck the Hull duration!', '', 0), EnemySkills.SAIL_WRECK_MASTS: (OrderSkill, 'Call upon your shipmates to fire cannons at sail and masts for great effect!', 'Upgrade to increase Wreck the Masts duration!', '', 0), EnemySkills.SAIL_SINK_HER: (OrderSkill, 'Call upon your shipmates to fire cannons at broken hull panels for great effect!', 'Upgrade to increase Sink Her duration!', '', 0), EnemySkills.SAIL_INCOMING: (OrderSkill, 'Protect your ship from incoming fire! Decreses ship damage but lowers broadside damage.', 'Upgrade to increase Incoming duration!', '', 0), EnemySkills.SAIL_FIX_IT_NOW: (OrderSkill, 'Call upon your shipmates to fix the ship! Increases ship repair effect.', 'Upgrade to increase Fix It Now duration!', '', 0), InventoryType.DaggerCut: (ComboSkill, 'An opening cut! Deals extra damage when striking a foe in the back!', '', ClickToLearnCombo, 0), InventoryType.DaggerSwipe: (ComboSkill, 'A whirling dagger attack! Deals extra damage when striking a foe in the back!', '', ClickToLearnCombo, 0), InventoryType.DaggerGouge: (ComboSkill, 'A powerful downward slice! Deals extra damage when striking a foe in the back!', '', ClickToLearnCombo, 0), InventoryType.DaggerEviscerate: (ComboSkill, 'Delivers three quick cuts! Deals extra damage when striking a foe in the back!', '', ClickToLearnCombo, 0), InventoryType.DaggerFinesse: (PassiveSkill, 'Decreases cooldown time for Dagger and Sword Skills by %d%%!', 'Upgrade to decrease Dagger and Sword Skill cooldown times!', '', 1), InventoryType.DaggerBladeInstinct: (PassiveSkill, 'Increases Sword and Dagger Combat damage by %d%%!', 'Upgrade to increase Sword and Dagger damage!', '', 1), InventoryType.DaggerAsp: (ThrowSkill, 'Basic dagger throw!', '', '', 0), InventoryType.DaggerAdder: (ThrowSkill, 'Poisoned dagger throw!', '', '', 0), InventoryType.DaggerThrowDirt: (CombatSkill, 'Fight dirty!', '', '', 0), InventoryType.DaggerSidewinder: (ThrowSkill, 'Sidearm dagger throw!', '', '', 0), InventoryType.DaggerViperNest: (ThrowSkill, 'Throw a brace of daggers!', '', '', 0), EnemySkills.DAGGER_COUP: (CombatSkill, 'A graceful finishing move!', '', '', 0), EnemySkills.DAGGER_DAGGERRAIN: (ThrowSkill, 'Throw a trio of daggers!', '', '', 0), EnemySkills.DAGGER_THROW_COMBO_1: (ComboSkill, 'Opening dagger toss.', '', '', 0), EnemySkills.DAGGER_THROW_COMBO_2: (ComboSkill, 'Left-hand dagger throw.', '', '', 0), EnemySkills.DAGGER_THROW_COMBO_3: (ComboSkill, 'Double dagger throw!', '', '', 0), EnemySkills.DAGGER_THROW_COMBO_4: (ComboSkill, 'Double backhanded dagger throw!', '', '', 0), EnemySkills.DAGGER_BARRAGE: (ThrowSkill, 'Strikes all nearby enemies with flying daggers!', '', '', 0), EnemySkills.DAGGER_ICEBARRAGE: (ThrowSkill, 'Freezes all nearby targets with icy daggers!', '', '', 0), EnemySkills.DAGGER_BACKSTAB: (CombatSkill, 'One powerful slash. Usable only when behind the enemy.', '', '', 0), EnemySkills.DAGGER_VENOMSTAB: (CombatSkill, 'A venomous dagger slash!', '', '', 0), EnemySkills.DAGGER_ACIDDAGGER: (ThrowSkill, 'A potent acidic throwing knife!', '', '', 0), InventoryType.GrenadeThrow: (AttackSkill, 'Fire in the hole! Basic grenade throwing skill.', '', '', 0), InventoryType.GrenadeExplosion: (AmmoSkill, 'A hefty grenade!', '', ClickToLearnAmmo, 0), InventoryType.GrenadeShockBomb: (AmmoSkill, 'A weak but stunning grenade!', '', ClickToLearnAmmo, 0), InventoryType.GrenadeFireBomb: (AmmoSkill, 'A flammable concoction!', '', ClickToLearnAmmo, 0), InventoryType.GrenadeSmokeCloud: (AmmoSkill, 'A smoke grenade that can used to obscure vision.', '', ClickToLearnAmmo, 0), InventoryType.GrenadeSiege: (AmmoSkill, 'A powerful siege bomb! Watch out, it is heavy!', '', ClickToLearnAmmo, 0), InventoryType.GrenadeLongVolley: (CombatSkill, 'Hold down the attack button to throw the grenade farther!  The longer you hold down the button, the further it will go!', '', '', 0), InventoryType.GrenadeDemolitions: (PassiveSkill, 'Increases the area of effect for your Grenade and Cannonball explosions!', 'Upgrade to increase Area of Effect bonus!', '', 0), InventoryType.GrenadeDetermination: (PassiveSkill, 'Increases your Health Recovery rate by %d%%!', 'Upgrade to increase your Health Recovery rate!', '', 1), InventoryType.GrenadeToughness: (PassiveSkill, 'Decreases damage suffered by incoming Grenades and Cannonballs by %d%%', 'Upgrade to increase your damage resistance to Grenades and Cannonballs!', '', 1), InventoryType.GrenadeIgnorePain: (PassiveSkill, 'Stun and Slow effect durations are reduced by %d%%!', 'Upgrade to increase Slow recovery speed!', '', 1), InventoryType.DollAttune: (AttackSkill, 'Attune the doll to a target in order to cast Hexes!', 'Upgrade to gain the ability to Attune the doll to 1 additional friend or enemy!', '', 0), InventoryType.DollPoke: (HexSkill, 'Poke attack!', '', '', 0), InventoryType.DollSwarm: (HexSkill, 'Summon insects to attack the enemy!', '', '', 0), InventoryType.DollHeal: (HexSkill, 'Heals a friendly pirate!', '', '', 0), InventoryType.DollBurn: (HexSkill, 'Sets enemies on fire!', '', '', 0), InventoryType.DollShackles: (HexSkill, 'Chains from the grave wrap around the enemy!', '', '', 0), InventoryType.DollCure: (HexSkill, 'Heals a friendly pirate and removes hostile effect Buffs from a friendly pirate!', '', '', 0), InventoryType.DollCurse: (HexSkill, 'Curses your opponent!', '', '', 0), InventoryType.DollLifeDrain: (HexSkill, 'Drain vitality from the victim.', '', '', 0), InventoryType.DollFocus: (PassiveSkill, 'Increases your maximum ' + ManaName + ' amount by %d%%!', 'Upgrade to increase your maximum ' + ManaName + '!', '', 1), InventoryType.DollSpiritWard: (PassiveSkill, '%d%% chance to Resist enemy Voodoo!', 'Upgrade to increase your chance to Resist enemy Voodoo!', '', 1), EnemySkills.DOLL_REGENERATION: (HexSkill, 'Heals health over time.', '', '', 0), EnemySkills.DOLL_SPIRIT_MEND: (HexSkill, 'Heals all targets without splitting the healing!', '', '', 0), EnemySkills.DOLL_WIND_GUARD: (HexSkill, 'Protects other pirates from ranged attacks!', '', '', 0), EnemySkills.DOLL_RED_FURY: (HexSkill, 'Increases the strength of friendly pirates!', '', '', 0), EnemySkills.DOLL_SPIRIT_GUARD: (HexSkill, 'Protects other pirates from combat attacks!', '', '', 0), EnemySkills.DOLL_HEX_GUARD: (HexSkill, 'Protects other pirates from voodoo attacks!', '', '', 0), EnemySkills.DOLL_EVIL_EYE: (AttackSkill, 'Attune targets from a distance!', '', '', 0), InventoryType.StaffBlast: (AttackSkill, '', '', '', 0), InventoryType.StaffWither: (HexSkill, '', '', '', 0), InventoryType.StaffSoulFlay: (HexSkill, '', '', '', 0), InventoryType.StaffPestilence: (HexSkill, '', '', '', 0), InventoryType.StaffHellfire: (HexSkill, '', '', '', 0), InventoryType.StaffBanish: (HexSkill, '', '', '', 0), InventoryType.StaffDesolation: (HexSkill, '', '', '', 0), InventoryType.StaffConcentration: (PassiveSkill, 'Increases your ' + ManaName + ' Recovery rate by %d%%!', 'Upgrade to increase your ' + ManaName + ' Recovery rate!', '', 1), InventoryType.StaffSpiritLore: (PassiveSkill, 'Increases Casting Speed for the Voodoo Staff by %d%%!', 'Upgrade to increase Casting Speed for the Voodoo Staff!', '', 1), InventoryType.StaffConservation: (PassiveSkill, 'Decreases ' + ManaName + ' used by Voodoo Staff and Voodoo Doll by %d%%!', 'Upgrade to decrease ' + ManaName + ' usage for Voodoo Staff and Voodoo Doll!', '', 1), InventoryType.StaffSpiritMastery: (PassiveSkill, 'Increases damage of Voodoo Doll and Staff Voodoo Hexes by %d%%!', 'Upgrade to increase Staff and Doll Voodoo Hex damage!', '', 1), EnemySkills.STAFF_TOGGLE_AURA_WARDING: (HexSkill, 'Boosts defense on all nearby Pirates.', '', '', 0), EnemySkills.STAFF_TOGGLE_AURA_NATURE: (HexSkill, 'Slowly heals all nearby Pirates.', '', '', 0), EnemySkills.STAFF_TOGGLE_AURA_DARK: (HexSkill, 'Boosts attack on all nearby Pirates.', '', '', 0), InventoryType.CannonShoot: (AttackSkill, 'Basic Cannoneering Skill!', 'Upgrade to increase Cannon firing rate!', '', 1), InventoryType.CannonRoundShot: (AmmoSkill, 'Medium ranged shot! Effective against ship hulls!', '', ClickToLearnAmmo, 0), InventoryType.CannonChainShot: (AmmoSkill, 'Short ranged shot! Effective against masts & sails!', '', ClickToLearnAmmo, 0), InventoryType.CannonExplosive: (AmmoSkill, 'Explodes and damages a large area!', '', ClickToLearnAmmo, 0), InventoryType.CannonBullet: (AmmoSkill, '', '', ClickToLearnAmmo, 0), InventoryType.CannonGasCloud: (AmmoSkill, '', '', ClickToLearnAmmo, 0), InventoryType.CannonGrapeShot: (AmmoSkill, 'Short ranged spread-shot! Slows enemy Ship Repair during PvP. Effective against Sea Monsters!', '', ClickToLearnAmmo, 0), InventoryType.CannonSkull: (AmmoSkill, '', '', ClickToLearnAmmo, 0), InventoryType.CannonFirebrand: (AmmoSkill, 'Flaming cannonballs set fire to enemy ships.', '', ClickToLearnAmmo, 0), InventoryType.CannonFlameCloud: (AmmoSkill, '', '', ClickToLearnAmmo, 0), InventoryType.CannonFlamingSkull: (AmmoSkill, 'Flaming cannonballs set fire to enemy ships.', '', ClickToLearnAmmo, 0), InventoryType.CannonBarShot: (AmmoSkill, '', '', ClickToLearnAmmo, 0), InventoryType.CannonKnives: (AmmoSkill, '', '', ClickToLearnAmmo, 0), InventoryType.CannonMine: (AmmoSkill, '', '', ClickToLearnAmmo, 0), InventoryType.CannonBarnacles: (AmmoSkill, '', '', ClickToLearnAmmo, 0), InventoryType.CannonThunderbolt: (AmmoSkill, 'Summons a thunderbolt to strike the enemy ship!', '', ClickToLearnAmmo, 0), InventoryType.CannonFury: (AmmoSkill, 'A spectral cannonball!', '', ClickToLearnAmmo, 0), InventoryType.CannonComet: (AmmoSkill, '', '', ClickToLearnAmmo, 0), InventoryType.CannonGrappleHook: (AmmoSkill, 'Used for grappling enemy ships for boarding actions!', '', ClickToLearnAmmo, 0), InventoryType.CannonRapidReload: (PassiveSkill, 'Increases Cannon reloading speed by %d%%!', 'Upgrade to increase Cannon reloading speed!', '', 1), InventoryType.CannonBarrage: (PassiveSkill, 'Increases damage for Cannon and Grenade attacks by %d%%!', 'Upgrade to increase Cannon and Grenade damage!', '', 1), InventoryType.CannonShrapnel: (PassiveSkill, 'Upgrade your Cannonballs and Grenades to explode in a cloud of shrapnel!', 'Upgrade to increase Shrapnel Wounding duration!', '', 0), InventoryType.Potion1: (Consumable, '', '', '', 0), InventoryType.Potion2: (Consumable, '', '', '', 0), InventoryType.Potion3: (Consumable, '', '', '', 0), InventoryType.Potion4: (Consumable, '', '', '', 0), InventoryType.Potion5: (Consumable, '', '', '', 0), InventoryType.CannonDamageLvl1: (Consumable, '', '', '', 0), InventoryType.CannonDamageLvl2: (Consumable, '', '', '', 0), InventoryType.CannonDamageLvl3: (Consumable, '', '', '', 0), InventoryType.PistolDamageLvl1: (Consumable, '', '', '', 0), InventoryType.PistolDamageLvl2: (Consumable, '', '', '', 0), InventoryType.PistolDamageLvl3: (Consumable, '', '', '', 0), InventoryType.CutlassDamageLvl1: (Consumable, '', '', '', 0), InventoryType.CutlassDamageLvl2: (Consumable, '', '', '', 0), InventoryType.CutlassDamageLvl3: (Consumable, '', '', '', 0), InventoryType.DollDamageLvl1: (Consumable, '', '', '', 0), InventoryType.DollDamageLvl2: (Consumable, '', '', '', 0), InventoryType.DollDamageLvl3: (Consumable, '', '', '', 0), InventoryType.HastenLvl1: (Consumable, '', '', '', 0), InventoryType.HastenLvl2: (Consumable, '', '', '', 0), InventoryType.HastenLvl3: (Consumable, '', '', '', 0), InventoryType.RepBonusLvl1: (Consumable, '', '', '', 0), InventoryType.RepBonusLvl2: (Consumable, '', '', '', 0), InventoryType.RepBonusLvl3: (Consumable, '', '', '', 0), InventoryType.RepBonusLvlComp: (Consumable, '', '', '', 0), InventoryType.GoldBonusLvl1: (Consumable, '', '', '', 0), InventoryType.GoldBonusLvl2: (Consumable, '', '', '', 0), InventoryType.InvisibilityLvl1: (Consumable, '', '', '', 0), InventoryType.InvisibilityLvl2: (Consumable, '', '', '', 0), InventoryType.RegenLvl1: (Consumable, '', '', '', 0), InventoryType.RegenLvl2: (Consumable, '', '', '', 0), InventoryType.RegenLvl3: (Consumable, '', '', '', 0), InventoryType.RegenLvl4: (Consumable, '', '', '', 0), InventoryType.Burp: (Consumable, '', '', '', 0), InventoryType.Fart: (Consumable, '', '', '', 0), InventoryType.FartLvl2: (Consumable, '', '', '', 0), InventoryType.Vomit: (Consumable, '', '', '', 0), InventoryType.HeadGrow: (Consumable, '', '', '', 0), InventoryType.FaceColor: (Consumable, '', '', '', 0), InventoryType.SizeReduce: (Consumable, '', '', '', 0), InventoryType.SizeIncrease: (Consumable, '', '', '', 0), InventoryType.HeadFire: (Consumable, '', '', '', 0), InventoryType.ScorpionTransform: (Consumable, '', '', '', 0), InventoryType.AlligatorTransform: (Consumable, '', '', '', 0), InventoryType.CrabTransform: (Consumable, '', '', '', 0), InventoryType.AccuracyBonusLvl1: (Consumable, '', '', '', 0), InventoryType.AccuracyBonusLvl2: (Consumable, '', '', '', 0), InventoryType.AccuracyBonusLvl3: (Consumable, '', '', '', 0), InventoryType.RemoveGroggy: (Consumable, '', '', '', 0), InventoryType.ShipRepairKit: (ShipRepairSkill, '', '', '', 0), InventoryType.PorkChunk: (Consumable, '', '', '', 0), EnemySkills.MISC_CLEANSE: (AttackSkill, 'Removes all negative status effects!', '', '', 0), EnemySkills.MISC_DARK_CURSE: (AttackSkill, 'Dark Form prevents half damage from ranged and combat attacks!', '', '', 0), EnemySkills.MISC_GHOST_FORM: (AttackSkill, 'Ghost Form prevents half damage from ranged and combat attacks!', '', '', 0), EnemySkills.MISC_FEINT: (AttackSkill, 'Auto-block one melee attack.', '', '', 0), EnemySkills.MISC_HEX_WARD: (AttackSkill, 'Auto-resists one voodoo attack.', '', '', 0), EnemySkills.MISC_CAPTAINS_RESOLVE: (AttackSkill, 'Heals all nearby pirates!', '', '', 0), EnemySkills.MISC_NOT_IN_FACE: (AttackSkill, 'This might make the enemy stop attacking you.', '', '', 0), EnemySkills.MISC_ACTIVATE_VOODOO_REFLECT: (AttackSkill, 'Reflects all voodoo magic back to the caster.', '', '', 0), EnemySkills.MISC_MONKEY_PANIC: (AttackSkill, 'Go bananas! Increases health and attack power!', '', '', 0), EnemySkills.MISC_FIRST_AID: (AttackSkill, 'Uses Voodoo Power to heal yourself!', '', '', 0)
}
PoisonDesc = 'Poisons an enemy for %d seconds!'
PoisonUpgrade = 'Poison duration'
ToxinDesc = 'Intoxicates an enemy for %d seconds!'
ToxinUpgrade = 'Toxin duration'
AcidDesc = 'Causes acid burns on an enemy for %d seconds!'
AcidUpgrade = 'Acid duration'
HoldDesc = 'Prevents enemy from moving for %d seconds!'
HoldUpgrade = 'movement lock duration'
WoundDesc = 'Wounds an enemy for %d seconds!'
WoundUpgrade = 'Wound duration'
OnFireDesc = 'Burns an enemy for %d seconds!'
OnFireUpgrade = 'Burning duration'
StunDesc = 'Disables an enemy for %d seconds!'
StunUpgrade = 'Stun duration'
UnstunDesc = 'Immune to Stun for %d seconds!'
UnstunUpgrade = 'Stun Immunity duration'
SlowDesc = 'Slows an enemy for %d seconds!'
SlowUpgrade = 'Slow duration'
BlindDesc = 'Blinds an enemy for %d seconds!'
BlindUpgrade = 'Blindness duration'
CurseDesc = 'Curses an enemy so that they suffer an additional %d%% damage from attacks! Lasts %d seconds!'
CurseUpgrade = 'Curse duration'
HastenDesc = 'Increases movement speed of a pirate by 50%%! Lasts %d seconds!'
HastenUpgrade = 'Hasten duration'
TauntDesc = 'Decreases enemy attack accuracy! Lasts %d seconds!'
TauntUpgrade = 'Taunt duration'
WeakenDesc = 'Decreases enemy attack power by %d%% for %d seconds!'
WeakenUpgrade = 'Weakness duration'
RegenDesc = 'Regain lost health for %d seconds!'
RegenUpgrade = 'Regeneration duration'
SoulTapDesc = "Injures the caster and expends most of the pirate's remaining Health!"
LifeDrainDesc = 'Drains Health from the victim!'
ManaDrainDesc = 'Drains ' + ManaName + ' from the victim!'
InterruptDesc = 'Interrupts weapon charging!'
UnattuneDesc = 'Breaks voodoo attunements!'
KnockdownDesc = 'Knocks down an enemy for %d seconds!'
FullSailDesc = 'Lasts %d seconds!'
ComeAboutDesc = 'Lasts %d seconds!'
OpenFireDesc = 'Lasts %d seconds!'
OpenFireUpgrade = 'Ram Maneuver duration!'
RamDesc = 'Lasts %d seconds!'
TakeCoverDesc = 'Lasts %d seconds!'
PowerRechargeDesc = 'Lasts %d seconds!'
AttuneDesc = 'Can attune up to %d friends or enemies!'
MonsterKillerDesc = 'Powerful against the Living, but weak against the Undead.'
UndeadKillerDesc = 'Powerful against the Undead, but weak against the Living.'
BuffBreakDesc = 'Has a chance to destroy a Voodoo Hex on the target!'
BuffBreakUpgrade = 'increase the chance to remove a Voodoo Hex from the target'
BroadsideDesc = 'Cannonball damage increased by %d%%!'
CannonShootDesc = 'Cannon firing rate increased by %d%%!'
MultiAttuneDesc = 'The more targets attuned, the weaker your Hexes will be!'
WreckHullDesc = 'Lasts %d seconds!'
WreckMastsDesc = 'Lasts %d seconds!'
SinkHerDesc = 'Lasts %d seconds!'
IncomingDesc = 'Lasts %d seconds!'
AttackBackstab = 'Backstrike!'
AttackUnattune = 'Attunements Shattered!'
AttackInterrupt = 'Interrupted!'
AttackBlocked = 'Blocked!'
AttackReflected = 'Reflected!'
ComboReqSwipe = 'Requires Swipe.'
ComboReqGouge = 'Requires Gouge'
ComboReqSlash = 'Requires Slash'
ComboReqCleave = 'Requires Cleave'
ComboReqFlourish = 'Requires Flourish'
SloopDescription = 'The fastest and most maneuverable ship class, the Sloop is ideal for scouting and hit-and-run attacks.  However, Sloops tend to have weak armor and little cargo room. \n \n The strongest armor of the hull is located near the middle of the ship.'
MerchantDescription = 'The Galleons have the toughest armor amongst the ship classes.  They also can carry the most cargo.  \n \n Their strongest armor is near the rear of the ship, with a weakness in the front.'
WarshipDescription = "The Frigate Class vessels pack the most firepower, sporting many cannons and strong below deck broadside capability.  \n \n The warship's strongest armor is near the front, with a weakness in the rear."
BrigDescription = 'Second best at everything the Brig is a jack of all trades, but a master of none. They are a good mix of firepower, speed, and cargo room. \n \n Their armor is the most evenly distributed without weak or strong areas.'
FishingRepDescription = 'Fishing Reputation'
PotionRepDescription = 'Potion Brewing Reputation'
WeaponDescriptions = {
    InventoryType.CutlassWeaponL1: "It's a bit crude, but it still has an edge.", InventoryType.CutlassWeaponL2: 'A well crafted iron blade. A good weapon! \n +2 damage per hit.', InventoryType.CutlassWeaponL3: 'An ornate steel cutlass. Well balanced and sharp! \n +4 damage per hit.', InventoryType.CutlassWeaponL4: "A Fine Cutlass. It is crafted with pride by the Caribbean's best blacksmiths.\n +6 damage per hit.", InventoryType.CutlassWeaponL5: 'A Pirate Blade, a clear warning sign to any EITC or Navy blokes.\n +8 damage per hit.', InventoryType.CutlassWeaponL6: 'A Dark Cutlass. \n +10 damage per hit.', InventoryType.PistolWeaponL1: 'A standard flintlock pistol. Fires one shot before it needs to be reloaded.', InventoryType.PistolWeaponL2: 'A flintlock pistol with two barrels. Each barrel can be fired separately before reloading.', InventoryType.PistolWeaponL3: 'A multi-barreled pistol! This rare device can fire three times before reloading.', InventoryType.PistolWeaponL4: 'A Heavy Tri-Barrel Pistol, a fine piece of weaponry. \n +1 damage per hit.', InventoryType.PistolWeaponL5: 'A Grand Pistol, equipped with three deadly barrels. \n +2 damage per hit.', InventoryType.PistolWeaponL6: 'A Quad-Barrel Pistol, four shiny barrels that will scare even the deadliest of pirates away. \n +3 damage per hit.', InventoryType.MusketWeaponL1: '', InventoryType.MusketWeaponL2: '', InventoryType.MusketWeaponL3: '', InventoryType.BayonetWeaponL1: '', InventoryType.BayonetWeaponL2: '', InventoryType.BayonetWeaponL3: '', InventoryType.DaggerWeaponL1: 'A sharp dagger. Small but deadly.', InventoryType.DaggerWeaponL2: 'A long knife. Well balanced for fighting. \n +2 damage per hit.', InventoryType.DaggerWeaponL3: 'A fancy blade that is useful for keeping your opponent off guard. \n +4 damage per hit.', InventoryType.DaggerWeaponL4: "A Coltello dagger, it is a pirate's best friend in the right fight. \n +6 damage per hit.", InventoryType.DaggerWeaponL5: 'A Bloodletter dagger. It is meticulously designed to fend off even the largest of foes. \n +8 damage per hit.', InventoryType.DaggerWeaponL6: 'A Slicer dagger. Tear through your enemies with ease with this deadly weapon. \n +10 damage per hit.', InventoryType.GrenadeWeaponL1: 'Grenades are highly lethal explosives. They are effective against large crowds of enemies!', InventoryType.GrenadeWeaponL2: '', InventoryType.GrenadeWeaponL3: '', InventoryType.GrenadeWeaponL4: '', InventoryType.GrenadeWeaponL5: '', InventoryType.GrenadeWeaponL6: '', InventoryType.DollWeaponL1: 'A mystical doll said to be able to bind to the spirit of anything it touches.', InventoryType.DollWeaponL2: 'A powerful doll able to bind to the spirits of the living and the dead. \n +2 damage per hit.', InventoryType.DollWeaponL3: 'An elaborate oriental doll able to strongly bind to the spirits of others. \n +4 damage per hit.', InventoryType.DollWeaponL4: 'A Pirate Doll. Bind to the spirits of the Caribbean with this rare doll. \n +6 damage per hit.', InventoryType.DollWeaponL5: 'A Taboo Doll. Many pirates fear the power and unknowns of this legendary doll. \n +8 damage per hit.', InventoryType.DollWeaponL6: 'A Mojo Doll. Out perform almost any pirate with deadly and unmatched precision. \n +10 damage per hit.', InventoryType.WandWeaponL1: 'A tribal fetish used for summoning evil spirits.', InventoryType.WandWeaponL2: 'A powerful fetish used for summoning and controlling spirits. \n +2 damage per hit.', InventoryType.WandWeaponL3: 'Sought after by many, this fetish allows the bearer to speak to the spirits of the dead. \n +4 damage per hit.', InventoryType.WandWeaponL4: 'Harrow Staff. Inflict the secrets of the dead upon your enemies with this rare staff. \n +6 damage per hit.', InventoryType.WandWeaponL5: 'Vile Staff. Summon the plagues of the dead and unknown against your foes. \n +8 damage per hit.', InventoryType.WandWeaponL6: 'Dire Staff. A myth to some pirates, this staff holds the power to demolish your enemies. \n +10 damage per hit.', InventoryType.KettleWeaponL1: '', InventoryType.KettleWeaponL2: '', InventoryType.KettleWeaponL3: '', InventoryType.Potion1: 'Eases pain. Smells kinda strong too.', InventoryType.Potion2: 'An exotic remedy. Said to cure all maladies.', InventoryType.Potion3: 'Water blessed by the angels and gods.', InventoryType.Potion4: 'The one and only, legendary Elixir of Life!', InventoryType.Potion5: 'A miracle potion said to cure all sicknesses and regrow hair!', InventoryType.PorkChunk: 'A tasty chunk of pork.', InventoryType.ShipRepairKit: 'Tools and supplies for repairing your ship in PvP.', InventoryType.PineInPocket: 'A common wood used in ship building.', InventoryType.OakInPocket: 'A sturdy wood used in ship building.', InventoryType.IronInPocket: 'A common metal used in ship building.', InventoryType.SteelInPocket: 'A strong metal alloy used in ship building.', InventoryType.CanvasInPocket: 'A common fabric used in sail contruction.', InventoryType.SilkInPocket: 'A rare, light-weight fabric used in sail construction.', InventoryType.GrogInPocket: 'Keep a weather eye out for this valuable commodity to surface soon...', InventoryType.AmmoLeadShot: 'A solid ball of lead. Crude but effective.', InventoryType.AmmoVenomShot: "Coated with snake venom. If the shot don't kill you, the venom will.", InventoryType.AmmoBaneShot: 'Cursed by Davy Jones himself! Weakens your opponents.', InventoryType.AmmoSilverShot: 'Useful against spooks and ghouls.', InventoryType.AmmoHexEaterShot: 'Disrupts Voodoo of witch doctors and the like.', InventoryType.AmmoSteelShot: 'The strongest shot. Great for hunting beasts and monsters.', InventoryType.AmmoAsp: 'A small set of throwing knives. \n Throwing ammunition for the Asp Skill.', InventoryType.AmmoAdder: 'A throwing knife coated with snake venom. \n Throwing ammunition for the Adder Skill.', InventoryType.AmmoSidewinder: 'A large curved throwing knife. \n Throwing ammunition for the Sidewinder Skill.', InventoryType.AmmoViperNest: 'A brace of special throwing knives meant to be thrown in a set. \n Throwing ammunition for the Viper Nest Skill.', InventoryType.AmmoGrenadeExplosion: 'A crude ceramic grenade.', InventoryType.AmmoGrenadeFlame: 'A flammable bomb that sets fire to its surroundings.', InventoryType.AmmoGrenadeShockBomb: 'A ceramic pot filled with noxious gas and foul smelling gunk.', InventoryType.AmmoGrenadeSmoke: 'A bomb filled with quick burning tar and rags. Creates a blinding cloud of smoke.', InventoryType.AmmoGrenadeSiege: 'A heavy iron grenade that packs a wallop!', InventoryType.AmmoRoundShot: 'Standard large round cannonball.', InventoryType.AmmoChainShot: 'Two iron balls connected by a chain. Useful for tearing down sails and masts.', InventoryType.AmmoExplosive: 'A mighty exploding cannonball. Highly volatile and extremely heavy.', InventoryType.AmmoGrapeShot: 'A canister of small metal balls that fires in a huge spread. It is deadly against enemy crewmen, but has a short range.', InventoryType.AmmoFirebrand: 'A flaming cannonball capable of setting fire to enemy ships.', InventoryType.AmmoFlamingSkull: 'A flaming skull capable of setting fire to enemy ships.', InventoryType.AmmoThunderbolt: 'A highly charged cannonball that causes a lightning bolt to strike where it lands.', InventoryType.AmmoFury: 'An ethereal ghostly fireball.', InventoryType.AmmoGrappleHook: 'Useful for boarding enemy ships. First, disable the ship. Then fire grapples and pull it in.', InventoryType.PistolPouchL1: 'A small ammo pouch for pistol bullets. Lets you hold more bullets of each type.', InventoryType.PistolPouchL2: 'A medium ammo pouch for pistol bullets. Lets you hold more bullets of each type.', InventoryType.PistolPouchL3: 'A large ammo pouch for pistol bullets. Lets you hold more bullets of each type.', InventoryType.DaggerPouchL1: 'A small belt for throwing daggers. Lets you hold more throwing daggers of each type.', InventoryType.DaggerPouchL2: 'A medium belt for throwing daggers. Lets you hold more throwing daggers of each type.', InventoryType.DaggerPouchL3: 'A large belt for throwing daggers. Lets you hold more throwing daggers of each type.', InventoryType.GrenadePouchL1: 'A small sack for grenades. Lets you hold more grenades of each type.', InventoryType.GrenadePouchL2: 'A medium sack for grenades. Lets you hold more grenades of each type.', InventoryType.GrenadePouchL3: 'A large sack for grenades. Lets you hold more grenades of each type.', InventoryType.CannonPouchL1: 'A small barrel for holding cannon ammo. Lets you hold more cannonballs of each type.', InventoryType.CannonPouchL2: 'A medium barrel for holding cannon ammo. Lets you hold more cannonballs of each type.', InventoryType.CannonPouchL3: 'A large barrel for holding cannon ammo. Lets you hold more cannonballs of each type.', InventoryType.RegularLure: 'Use it to catch everything from trout to tiger sharks', InventoryType.LegendaryLure: 'An ancient Mayan lure used to hunt the legends of the sea'
}
ShipDescriptions = {
    ItemId.INTERCEPTOR_L1: SloopDescription, ItemId.INTERCEPTOR_L2: SloopDescription, ItemId.INTERCEPTOR_L3: SloopDescription, ItemId.MERCHANT_L1: MerchantDescription, ItemId.MERCHANT_L2: MerchantDescription, ItemId.MERCHANT_L3: MerchantDescription, ItemId.WARSHIP_L1: WarshipDescription, ItemId.WARSHIP_L2: WarshipDescription, ItemId.WARSHIP_L3: WarshipDescription, ItemId.BRIG_L1: BrigDescription, ItemId.BRIG_L2: BrigDescription, ItemId.BRIG_L3: BrigDescription, ItemId.QUEEN_ANNES_REVENGE: WarshipDescription, ItemId.HUNTER_VENGEANCE: WarshipDescription, ItemId.HUNTER_TALLYHO: WarshipDescription, ItemId.BLACK_PEARL: WarshipDescription, ItemId.GOLIATH: WarshipDescription, ItemId.SHIP_OF_THE_LINE: WarshipDescription, ItemId.EL_PATRONS_SHIP: WarshipDescription, ItemId.P_SKEL_PHANTOM: WarshipDescription, ItemId.P_SKEL_REVENANT: WarshipDescription, ItemId.P_SKEL_CEREBUS: WarshipDescription, ItemId.P_NAVY_KINGFISHER: SloopDescription, ItemId.P_EITC_WARLORD: WarshipDescription, ItemId.HMS_VICTORY: WarshipDescription, ItemId.HMS_NEWCASTLE: WarshipDescription, ItemId.HMS_INVINCIBLE: WarshipDescription, ItemId.EITC_INTREPID: WarshipDescription, ItemId.EITC_CONQUERER: WarshipDescription, ItemId.EITC_LEVIATHAN: WarshipDescription, ItemId.NAVY_FERRET: SloopDescription, ItemId.NAVY_BULWARK: MerchantDescription, ItemId.NAVY_PANTHER: WarshipDescription, ItemId.NAVY_GREYHOUND: SloopDescription, ItemId.NAVY_VANGUARD: MerchantDescription, ItemId.NAVY_CENTURION: WarshipDescription, ItemId.NAVY_KINGFISHER: SloopDescription, ItemId.NAVY_MONARCH: MerchantDescription, ItemId.NAVY_MAN_O_WAR: WarshipDescription, ItemId.NAVY_PREDATOR: SloopDescription, ItemId.NAVY_COLOSSUS: MerchantDescription, ItemId.NAVY_DREADNOUGHT: WarshipDescription, ItemId.NAVY_BASTION: WarshipDescription, ItemId.NAVY_ELITE: WarshipDescription, ItemId.EITC_SEA_VIPER: SloopDescription, ItemId.EITC_SENTINEL: MerchantDescription, ItemId.EITC_CORVETTE: WarshipDescription, ItemId.EITC_BLOODHOUND: SloopDescription, ItemId.EITC_IRONWALL: MerchantDescription, ItemId.EITC_MARAUDER: WarshipDescription, ItemId.EITC_BARRACUDA: SloopDescription, ItemId.EITC_OGRE: MerchantDescription, ItemId.EITC_WARLORD: WarshipDescription, ItemId.EITC_CORSAIR: SloopDescription, ItemId.EITC_BEHEMOTH: MerchantDescription, ItemId.EITC_JUGGERNAUT: WarshipDescription, ItemId.EITC_TYRANT: WarshipDescription, ItemId.SKEL_PHANTOM: WarshipDescription, ItemId.SKEL_REVENANT: WarshipDescription, ItemId.SKEL_STORM_REAPER: WarshipDescription, ItemId.SKEL_BLACK_HARBINGER: WarshipDescription, ItemId.SKEL_DEATH_OMEN: WarshipDescription, ItemId.SKEL_SHADOW_CROW_FR: SloopDescription, ItemId.SKEL_HELLHOUND_FR: SloopDescription, ItemId.SKEL_BLOOD_SCOURGE_FR: SloopDescription, ItemId.SKEL_SHADOW_CROW_SP: SloopDescription, ItemId.SKEL_HELLHOUND_SP: SloopDescription, ItemId.SKEL_BLOOD_SCOURGE_SP: SloopDescription
}
GrenadeShort = 'Grenade'
ShipCannonShort = 'Cannon'
InventoryItemClassNames = {
    ItemType.MELEE: 'Brawl', ItemType.SWORD: 'Sword', ItemType.PISTOL: 'Gun', ItemType.MUSKET: 'Musket', ItemType.DAGGER: 'Dagger', ItemType.GRENADE: 'Grenade Weapon', ItemType.DOLL: 'Voodoo Doll', ItemType.WAND: 'Voodoo Staff', ItemType.KETTLE: 'Voodoo Kettle', ItemType.SHIP: 'Ship', ItemType.SHIPPART: 'Ship Part', ItemType.CONSUMABLE: 'Consumable', ItemType.POTION: 'Drink', ItemType.FOOD: 'Food', ItemType.FURNITURE: 'Furniture', ItemType.INGREDIENT: 'Voodoo Ingredient', ItemType.CANNON: 'Ship Cannon', ItemType.BOTTLE: 'Holds a Ship', ItemType.CANNONAMMO: 'Cannon Ammo', ItemType.DAGGERAMMO: 'Dagger Ammo', ItemType.PISTOLAMMO: 'Pistol Ammo', ItemType.GRENADEAMMO: 'Grenade Ammo', ItemType.POUCH: 'Ammo Pouch', ItemType.PISTOL_POUCH: 'Pistol Ammo Pouch', ItemType.DAGGER_POUCH: 'Throwing Dagger Belt', ItemType.GRENADE_POUCH: 'Grenade Sack', ItemType.CANNON_POUCH: 'Cannonball Barrel', ItemType.SHIP_REPAIR_KIT: 'Repairs Ship in PvP', ItemType.FISHING_ROD: 'Fishing', ItemType.FISHING_LURE: 'Fishing Lure', ItemType.MATERIAL: 'Material'
}
ItemGroupNames = {
    ItemTypeGroup.CUTLASS: 'Swords', ItemTypeGroup.DAGGER: 'Daggers', ItemTypeGroup.PISTOL: 'Guns', ItemTypeGroup.CANNON: 'Cannons', ItemTypeGroup.DOLL: 'Dolls', ItemTypeGroup.POTION: 'Tonics', ItemTypeGroup.GRENADE: 'Grenades', ItemTypeGroup.WAND: 'Staff', ItemTypeGroup.FISHING_GEAR: 'Fishing Gear'
}
VoodooNames = {
    0: 'Heartiness',
    1: 'Strength',
    2: 'Swiftness',
    3: 'Luck',
    4: 'Voodoo'
}
SkillResultNames = {
    0: 'Miss',
    1: 'Hit',
    2: 'Delayed',
    3: 'Out of Range',
    4: 'Not Available',
    5: 'Not Recharged',
    6: 'Against Pirate Code',
    7: 'Parry',
    8: 'Dodge',
    9: 'Resist',
    10: 'Mistimed Miss',
    11: 'Mistimed Hit',
    12: 'Blocked',
    13: 'Reflected',
    14: 'Protect'
}
Mistimed = 'Mistimed'
Disengage = 'Disengage'
Perfect = 'Perfect!'
InteractCancel = lExit
InteractTalk = 'Talk'
InteractTrade = 'Trade'
InteractDuel = 'Duel'
InteractQuest = 'Quest'
InteractBribe = 'Bribe'
InteractBribeAlt = 'Pay Gold'
InteractShips = 'Purchase'
InteractSellShips = 'Sell'
InteractStore = 'Store'
InteractSellItems = 'Sell Items'
InteractRepair = 'Repair'
InteractOverhaul = 'Overhaul'
InteractUpgrade = 'Upgrade'
InteractNoUpgrade = 'Unfit'
InteractHealHp = 'Healing'
InteractHealMojo = 'Recharge'
InteractTrain = 'Training'
InteractSail = 'Sail'
InteractSailTM = 'Treasure Map'
InteractRespec = 'Retrain Skills'
InteractRespecCutlass = 'Retrain Sword'
InteractRespecPistol = 'Retrain Shooting'
InteractRespecGrenade = 'Retrain Grenade'
InteractRespecDoll = 'Retrain Voodoo Doll'
InteractRespecDagger = 'Retrain Dagger'
InteractRespecStaff = 'Retrain Voodoo Staff'
InteractRespecSailing = 'Retrain Sailing'
InteractRespecCannon = 'Retrain Cannon'
InteractBack = 'Back'
InteractMusician = 'Request a Song'
InteractPvPTattoo = 'PvP Tattoos'
InteractPvPCoat = 'PvP Coats'
InteractPvPHat = 'PvP Hats'
InteractStowaway = 'Stowaway'
InteractCannonDefense = 'Play Cannon Defense'
InteractPotionTutorial = 'Potion Brewing'
InteractLaunchFishingBoat = 'Launch Fishing Boat'
InteractUpgradeRod = 'Upgrade Fishing Rod'
InteractLegendaryFishStory = 'Legendary Fish Story'
InteractChooseBranch = 'Choose Branch'
InteractCatalogStore = 'Catalog'
InteractScrimmage = 'Play Scrimmage'
InteractCancelHelp = 'Finish talking with this person'
InteractTalkHelp = 'Chat with this person'
InteractTradeHelp = 'Trade with this person'
InteractDuelHelp = 'Fight this person'
InteractQuestHelp = 'Ask for a new Quest'
InteractBribeHelp = 'Bribe this person'
InteractShipsHelp = 'Purchase new ships'
InteractSellShipsHelp = 'Sell your ships'
InteractStoreHelp = 'Purchase or sell equipment and items'
InteractSellItemsHelp = 'Sell  items from your inventory'
InteractRepairHelp = 'Repair damage to your ship'
InteractOverhaulHelp = 'Reconstruct severely wrecked ships'
InteractUpgradeHelp = 'Upgrade your ship'
InteractHealHpHelp = 'Heal your character'
InteractHealMojoHelp = 'Refills lost Voodoo'
InteractTrainHelp = 'Learn new skills and techniques'
InteractAmmoHelp = 'Purchase cannon ammo'
InteractSailHelp = 'Sail the high seas'
InteractSailTMHelp = 'Sail using a Treasure Map'
InteractRespecHelp = 'Redistribute skill points'
InteractBackHelp = 'Go back to previous menu'
InteractMusicianHelp = 'Request some music...for a fee'
InteractPvPTattooHelp = 'Spend PvP Infamy on unique tattoos'
InteractPvPCoatHelp = 'Spend PvP Infamy on unique coats'
InteractPvPHatHelp = 'Spend PvP Infamy on unique hats'
InteractStowawayHelp = 'Pay to sneak aboard a merchant ship'
InteractCannonDefenseHelp = 'Use a cannon to defend the island from bandits'
InteractPotionTutorialHelp = 'Learn how to brew potions'
InteractLaunchFishingBoatHelp = 'Launch a fishing boat and go deep sea fishing!'
InteractUpgradeRodHelp = 'Get a new rod'
InteractLegendaryFishStoryHelp = 'Legendary fish only appears once!'
InteractCatalogHelp = 'Purchase or sell catalog items'
InteractScrimmageHelp = 'Fight off enemies to prove yourself to the Navy'
RespecConfirmDialog = 'Pay %(gold)s gold to retrain your %(weapon)s? Retraining will refund all of your spent skill points so that you can redistribute them.'
RespecPriceIncreaseDialog = ' \n\nChoose carefully! The next time you Retrain, it will cost more Gold!'
UpgradeRodConfirmDialog = "It will cost you %(gold)s gold to upgrade to a %(rod)s. You'll be able to cast further and catch deeper fish!"
UpgradeRodFail = 'You need %(gold)s gold to upgrade to a %(rod)s'
LaunchFishingBoatFail = 'You need %(gold)s gold to launch a fishing boat (you only have %(have)s)'
LaunchFishingBoatConfirmDialog = 'It will cost you %(gold)s gold to launch a fishing boat, but you will be able find bigger fishes.  Are you ready to go?'
BribeConfirmDialog = 'Bribe %(name)s for %(gold)s gold?'
HealHpConfirmDialog = 'Pay %(gold)s gold for full healing?'
HealMojoConfirmDialog = 'Pay %(gold)s gold for full voodoo recharge?'
RepairConfirmDialog = 'Pay %(gold)s gold for full ship repairs?'
OverhaulConfirmDialog = 'Pay %(gold)s gold to reconstruct your wrecked ship?'
SellShipConfirmDialog = 'Sell this ship for %(gold)s gold?'
SellShipAreYouSureDialog = 'Are you sure you want to sell your ship? It will be permanently lost.'
BribeConfirmYourGold = 'Your Gold: %s'
BribeNotEnoughGold = 'You cannot afford %(gold)s gold for the bribe.'
CannonDefenseConfirmDialog = 'Play the Cannon Defense game?'
TellLegendaryFishStoryConfirmDialog = 'Do you really want to know the story of legendary fish?'
InteractKey = 'Shift'
TabKey = 'Tab'
CtrlKey = 'Ctrl'
ShiftKey = 'Shift'
EscapeKey = 'Esc'
OneKey = '1'
QuestPageKey = 'J'
WeaponPageKey = 'I'
SkillPageKey = 'K'
LookoutPageKey = 'L'
WeaponSlot1 = 'F1'
WeaponSlot2 = 'F2'
ForwardMoveKey = 'W'
LeftMoveKey = 'A'
RightMoveKey = 'D'
BackwardMoveKey = 'S'
InteractGeneral = 'Press %s to interact' % InteractKey
InteractCannon = 'Press %s to use cannon' % InteractKey
InteractWheel = 'Press %s to steer ship' % InteractKey
InteractWheelCaptain = 'Press %s to take over steering the ship' % InteractKey
InteractRepairSpot = 'Press %s to repair ship' % InteractKey
InteractRepairBench = 'Press %s to repair ships for gold' % InteractKey
InteractBuriedTreasure = 'Press %s to dig' % InteractKey
InteractFishingSpot = 'Press %s to start fishing' % InteractKey
InteractDigging = 'Digging...'
InteractSearchableContainer = 'Press %s to search' % InteractKey
InteractSearching = 'Searching...'
InteractFoundersFeastBonfire = 'Press %s to initiate the Brethren Victory Feast Bonfire' % InteractKey
InteractMardiGrasBonfire = 'Press %s to initiate the Mardi Gras Bonfire' % InteractKey
InteractFoundersFeastPig = 'Press %s to get some Brethren Victory Feast meat' % InteractKey
InteractMardiGrasPig = 'Press %s to enjoy a Mardi Gras feast - Roast Pork' % InteractKey
AlreadySearched = 'Nothing interesting here.'
DidNotFindQuestItem = 'Did not find any quest items.'
FoundQuestItem = 'Found quest item!'
InteractTownfolk = 'Press %s to talk to townsperson' % InteractKey
InteractNamedTownfolk = 'Press %s to talk to ' % InteractKey + '%s'
InteractNavySailor = 'Press %s to battle the Navy Soldier' % InteractKey
BoardShipInstructions = 'Press %s to board ship' % InteractKey
DeployShipInstructions = 'Press %s to row out to a ship' % InteractKey
ShipDepositInstructions = 'Press %s to load treasure onto ship' % InteractKey
ShipTransferInstructions = 'Press %s to transfer treasure to base' % InteractKey
CraftPotionInstructions = 'Press %s to brew potions' % InteractKey
UnableBoardShipInstructions = 'Not able to board ship'
DinghyNeedFirstShip = 'Use the map in your sea chest to return to %s to see about acquiring a ship of your own.'
DinghyNeedShip = 'You must have a ship before you can go sailing.'
DinghyNoFriendShip = "None of your friends' ships are available for sailing at the moment."
DinghyNoCrewShip = "None of your crew members' ships are available for sailing at the moment."
DinghyNoGuildShip = "None of your guild members' ships are available for sailing at the moment."
DinghyNoPublicShip = 'There are no public ships available for sailing at the moment.'
DinghyWrongSiegeShip = "You can't launch a ship from here while you are on the %s privateering team."
DinghyMyShip = 'Own'
DinghyFriendShip = 'Friend'
DinghyCrewShip = 'Crew'
DinghyGuildShip = 'Guild'
DinghyPublicShip = 'Public'
ExitShipInstructions = 'Press %s to exit ship' % InteractKey
ExitShipLockedInstructions = 'Must be Docked to exit ship'
ExitShipToEnemyShipInstructions = 'Press %s to board enemy ship' % InteractKey
ExitShipToOriginalShipInstructions = 'Press %s to return to your ship' % InteractKey
FlagshipWaitingForGrappleInstructions = 'Shoot grappling hooks at the flashing green targets to tow the flagship into boarding position.'
FlagshipGrappleLerpingInstructions = 'Grappling hook landed!  Land more grappling hooks to tow the flagship faster!'
FlagshipInPositionInstructionsCaptain = 'Flagship is in position, click button to board it with your shipmates!'
FlagshipInPositionInstructionsCrew = 'Flagship is in position, waiting for captain to initiate boarding...'
FlagshipStatusWaitingForGrapple = 'Crippled'
FlagshipStatusInPosition = 'Ready to be boarded'
FlagshipStatusBoarded = 'Boarded'
FlagshipClickToBoard = 'Click button to board'
FlagshipWaveCountdown = 'Next wave in '
FlagshipWaveCount = 'Wave %s of %s'
NoPigRoasting = 'No pig roasting. Try again later!'
FoundersFeastBonfireAlreadyStarted = 'Brethren Victory Feast Bonfire already started!'
MardiGrasBonfireAlreadyStarted = 'Mardi Gras Bonfire already started!'
FoundersFeastPorkChunkReceived = 'You took some Roast Pork from the Brethren Victory Feast Roast'
MardiGrasPorkChunkReceived = 'You took some Roast Pork from the Mardi Gras Roast'
ClickToBattleGeneral = 'Click on enemy to battle'
ClickToBattleSkeleton = 'Click on skeleton to battle'
KeyToBattleGeneral = 'Press %s to battle enemy' % InteractKey
InteractOpenDoor = 'Press %s to open door' % InteractKey
InteractEnterNamedBuilding = 'Press %s to enter ' % InteractKey + '%s'
InteractExitNamedBuilding = 'Press %s to exit ' % InteractKey + '%s'
InteractKickDoor = 'Press %s to kick door' % InteractKey
InteractKicking = 'Kicking...'
InteractLock = 'Press %s to pick lock' % InteractKey
LockMechanism = 'Mechanism'
LockpickFailed = 'Lockpick Failed'
UnlockedBy = 'Unlocked by'
InteractTable = 'Press %s to sit down' % InteractKey
InteractTableBlackjack = 'Press %s to sit down and play Blackjack' % InteractKey
InteractTablePoker = 'Press %s to sit down and play Poker' % InteractKey
InteractTableHoldemPoker = "Press %s to sit down and play Tortuga Hold'em Poker" % InteractKey
InteractTable7StudPoker = 'Press %s to sit down and play 7 Stud Poker' % InteractKey
ShipAlreadyDeployedWarning = 'Already have a ship launched!'
ShipAlreadyDeployingWarning = 'Already deploying a ship!'
ShipReturnAdventureWarning = 'Cannot return ships during an Adventure!'
PlayerNotInWaterWarning = 'Player must be in water'
PlayerInHighSeaWarning = 'Cannot launch ships in High Seas!'
CannotBoardShipWarning = 'Cannot board ship at this time!'
ShipNotInBottleWarning = 'Ship must be put away in bottle first!'
OtherPrivShipIsBeingDeployed = "%s's ship, the %s, has begun privateering at %s!"
OtherShipIsBeingDeployed = "%s's ship, the %s, is now being launched at %s!"
CoralReefWarning = 'You are sailing too close to shore!'
HeavyFogWarning = 'You cannot dock here!'
AnchorButtonInfo = 'Drop Anchor'
AnchorButtonHelp = 'Drop anchor and enter port'
FlagshipButtonInfo = 'Swing Over'
FlagshipButtonHelp = 'Board the enemy flagship'
JournalButtonInfo = 'New Quest!'
JournalButtonHelp = 'You have a New Quest! Open your Quest Journal and view it!'
SocialButtonHelp = 'Friends'
QuestButtonHelp = 'Quest Journal'
WeaponButtonHelp = 'Weapons'
SkillButtonHelp = 'Skills'
ClothingButtonHelp = 'Clothing'
TitlesButtonHelp = 'Titles'
TreasuresButtonHelp = 'Treasure'
ShipsButtonHelp = 'Ships'
RadarButtonHelp = 'Compass'
OptionsButtonHelp = 'Options'
MapButtonHelp = 'Map'
ShardActiveWorlds = 'Active Oceans'
ShardCurrentWorld = 'Current Server'
ShardPreferredWorld = 'Preferred Server'
ShardNone = 'Random (Click here to choose)'
Ocean = 'Ocean'
ShardPageLow = 'Quiet'
ShardPageMed = 'Ideal'
ShardPageHigh = 'Full'
PortOfCall = 'Port of Call'
LookoutButtonHelp = 'Lookout'
SeaChestButtonHelp = 'Sea Chest'
InventoryHelp = 'Sea Chest'
SkillHelp = 'Skills'
QuestHelp = 'Quests'
WeaponHelp = 'Click to Equip Weapon'
WeaponSwitchHelp = 'Click to Change Selected Weapon'
GameHelp = 'Display Game Menu'
SocialButtonHelp = 'Hearties'
FriendButtonHelp = 'Toggle Friend List'
CrewButtonHelp = 'Toggle Crew List'
GuildButtonHelp = 'Toggle Guild List'
PirateCodeWarning1 = 'Keep to the Code'
PirateCodeWarning2 = 'Choose Another Weapon'
UnattuneGui = 'Unattune a Target?'
EmptyBottle = 'Empty Bottle'
EmptyBottleDesc = 'Will hold one ship'
ScreenshotLocation = 'Screenshots located'
Screenshot = 'screenshot'
ScreenshotDir = 'screenshots'
ScreenshotCaptured = 'Screenshot captured'
SeaChestTitleMap = 'World Map'
SeaChestTitleWeapons = 'Notoriety'
SeaChestTitleSkills = 'Skills'
SeaChestTitleShips = 'Ships'
SeaChestTitleQuests = 'Quests'
SeaChestTitleLookout = 'Lookout'
SeaChestTitleBadges = 'Badges'
HighSeasAdventureStartTitle = 'High Seas Adventure'
HighSeasAdventureStartInfo = 'Return to your Ship before it leaves Port!'
HighSeasAdventureStartWaitInfo = 'Waiting for Shipmates to board Ship!'
HighSeasAdventureLimitTitle = 'Supplies'
HighSeasShipSelectionTitle = 'Ship Selection'
Accept = 'Accept'
Decline = 'Decline'
Cancel = lCancel
Back = lBack
Decline = 'Decline'
Bribe = 'Bribe'
DropQuest = 'Drop'
DropQuestHelp = 'Abandon this quest and remove it from your journal.'
ShareQuest = 'Share'
TrackQuest = 'Track'
TrackQuestHelp = 'Show visual indicator to help find your next step in this quest.'
QuestDescription = 'Quest Description'
BPCrew = 'Crew'
BPCrewTitle = 'The Black Pearl Crew'
Continue = 'Continue'
QuestPageStoryQuests = 'Fame'
QuestPageWorkQuests = 'Fortune'
QuestFull = 'You must complete one of your Fortune Quests before accepting another task.'
QuestMultiHeadingOr = 'Do ONE of the following:'
QuestMultiHeadingAnd = 'Do ALL of the following:'
QuestStrOneTask = '%(task)s'
QuestStrMultiTask = '%(heading)s%(tasks)s'
QuestDescTaskSingle = '%(task)s.'
QuestDescTaskSingleNoPeriod = '%(task)s'
QuestDescTaskMulti = '\n- %(task)s'
QuestStatusTaskSingle = '%(task)s \x01questObj\x01%(prog)s\x02'
QuestStatusTaskMulti = '\n- %(task)s \x01questObj\x01%(prog)s\x02'
QuestStatusTaskBonus = '\nBonus: '
QuestTaskProgress = '(%(prog)s/%(goal)s)'
QuestProgressComplete = '(COMPLETE)'
QuestTitleNew = 'NEW!'
QuestTitleComplete = 'COMPLETE!'
QuestCompleted = 'Quest Completed!'
DefeatProgress = '%d/%d %s Defeated'
DefeatProgressWeapon = '%d/%d %s Defeated Using A %s'
DefeatNPCProgress = '%s Defeated'
RecoverItemProgress = '%d/%d %s Found'
DeliverItemProgress = '%d/%d %s Delivered'
SmuggleItemProgress = '%d/%d %s Smuggled'
PokerProgress = '%d/%d Gold Won'
PokerBonusProgress = '%d/%d Bonus Gold Won'
BlackjackProgress = '%d/%d Gold Won'
TreasureItemProgress = '%d/%d %s Found'
DefeatShipProgress = '%d/%d Ships Sunk'
DefeatShipTypeProgress = '%d/%d %s Sunk'
DefeatShipFactionProgress = '%d/%d %s Sunk'
DefeatShipFactionTypeProgress = '%d/%d %s %ss Sunk'
CaptureShipNPCProgress = '%d/%d %s Found'
CaptureNPCProgress = '%s Has Been Captured!'
MaroonNPCProgress = '%s Has Been Marooned!'
PoisonContainerProgress = '%d/%d %s Poisoned!'
SailToProgress = 'You have reached %s!'
PotionsProgress = '%d/%d "%s" Potions Brewed'
PotionsProgressBonus = '%d/%d "%s" Bonus Potions Brewed'
FishingProgress = '%d/%d %s Fish Caught'
FishingProgressBonus = '%d/%d "%s" Bonus Fish Caught'
DowsingRodSuccessTaskProgress = '%s Has Been Found!'
DowsingRodFailTaskProgress = '%s Has Been Found. Keep Looking For %s'
DefeatAroundPropProgress = '%s Has Been Found!'
ScrimmageProgress = '%d/%d Rounds Completed'
QuestRewardDescS = '%s'
QuestRewardDescM = '%s'
QuestRewardDescItem = '%s%s\n'
QuestRewardDescItemBonus = 'Bonus: '
QuestButtonNext = 'Next'
QuestButtonLast = 'Okay'
QuestCompleteFrameWorkText = '\n\nReward:'
VisitTaskTitle = 'Visit %s'
BribeTaskTitle = 'Bribe %s'
MaroonTaskTitle = 'Maroon %s'
DefeatNPCTaskTitle = 'Defeat %s'
ViewCutsceneTaskTitle = 'Visit %s'
RecoverAvatarItemTaskTitle = 'Recover Enemy Item'
RecoverShipItemTaskTitle = 'Recover Ship Item'
CaptureShipNPCTaskTitle = 'Capture %s on Ship'
RecoverContainerItemTaskTitle = 'Recover Container Item'
PoisonContainerTaskTitle = 'Poison Container'
DeliverItemTaskTitle = 'Deliver Item'
SmuggleItemTaskTitle = 'Smuggle Item'
PokerTaskTitle = 'Win at Poker'
BlackjackTaskTitle = 'Win at Blackjack'
RecoverTreasureItemTaskTitle = 'Recover Treasure Item'
DefeatTaskTitle = 'Defeat %s'
DefeatWithWeaponTaskTitle = 'Defeat %s using a %s'
DefeatShipTaskTitle = 'Sink Ship'
CaptureNPCTaskTitle = 'Capture %s'
BossBattleName = 'Boss Battle'
BossBattleTaskTitle = BossBattleName + ': %s'
DeployShipTaskTitle = 'Launch Ship'
BurnPropTaskTitle = 'Burn %s'
DefendTaskTitle = 'Defend %s'
DefeatAroundPropTaskTitle = 'Defeat %s Around %s'
DowsingRodTaskTitle = 'Recover Item using a Dowsing Rod'
SailToTaskTitle = 'Sail to %s'
PotionTaskTitle = 'Brew Potions'
FishingTaskTitle = 'Catch fish'
LootPropTaskTitle = 'Loot Prop'
BribeTaskDesc = 'Bribe \x01questObj\x01%(toNpcName)s\x02 with \x01questObj\x01%(gold)s\x02 gold'
BribeTaskAltDesc = 'Pay \x01questObj\x01%(toNpcName)s\x02 with \x01questObj\x01%(gold)s\x02 gold'
ViewCutsceneTaskDesc = 'Visit \x01questObj\x01%(toNpcName)s\x02'
SmuggleItemTaskDescS = 'Smuggle \x01questObj\x01%(itemName)s\x02 to \x01questObj\x01%(location)s\x02'
SmuggleItemTaskDescP = 'Smuggle \x01questObj\x01%(num)s %(itemName)s\x02 to \x01questObj\x01%(location)s\x02'
PokerTaskDescS = 'Win \x01questObj\x01%(gold)s gold\x02 playing poker'
PokerTaskDescP = 'Win \x01questObj\x01%(gold)s gold\x02 playing poker'
PokerSkeletonTaskDescP = 'Win \x01questObj\x01%(gold)s gold\x02 playing Undead poker in one sitting'
PokerSkeletonTaskDescB = 'Win \x01questObj\x01%(gold)s gold\x02 playing Undead poker'
BlackjackTaskDescS = 'Win \x01questObj\x01%(gold)s gold\x02 playing blackjack'
BlackjackTaskDescP = 'Win \x01questObj\x01%(gold)s gold\x02 playing blackjack'
CaptureNPCTaskDesc = 'Capture \x01questObj\x01%(npcName)s\x02'
MaroonNPCTaskDesc = 'Maroon \x01questObj\x01%(npcName)s\x02 at \x01questObj\x01%(location)s\x02'
BossBattleTaskDesc = 'Complete ' + BossBattleName + ' : \x01questObj\x01%(treasureMapId)s\x02'
DeployShipTaskDesc = 'Launch Your Ship'
SailToTaskDesc = 'Sail to \x01questObj\x01%(location)s\x02'
PotionsTaskDescS = 'Brew a \x01questObj\x01%(potionName)s\x02 potion'
PotionsTaskDescP = 'Brew \x01questObj\x01%(num)s %(potionName)s\x02 potions'
FishingTaskDescS = 'Catch a \x01questObj\x01%(fishName)s\x02 fish'
FishingTaskDescP = 'Catch \x01questObj\x01%(num)s %(fishName)s\x02 fish'
FishingTaskDescLegendaryS = 'Catch a \x01questObj\x01%(fishName)s\x02'
FishingTaskDescLegendaryP = 'Catch \x01questObj\x01%(num)s %(fishName)s\x02'
SkeletonPokerTaskDescS = 'Win \x01questObj\x01%(gold)s gold\x02 playing skeleton poker'
QuestTaskNpc = ' \x01questObj\x01%(npcName)s\x02'
QuestTaskNum = ' \x01questObj\x01%(num)d\x02'
QuestTaskNumReg = ' %(num)d\x02'
QuestTaskLevel = ' \x01questObj\x01L%(level)d+\x02'
QuestTaskEnemy = ' \x01questObj\x01%(enemyName)s\x02'
QuestTaskLocation = ' in %(locationName)s'
QuestTaskIsland = ' on %(islandName)s'
QuestTaskWeapon = ' using a \x01questObj\x01%(weaponName)s\x02'
QuestTaskItem = ' \x01questObj\x01%(itemName)s\x02'
QuestTaskFaction = ' \x01questObj\x01%(factionName)s\x02'
QuestTaskContainer = ' %(containerName)s'
VisitTaskDesc = 'Visit%(npcName)s%(location)s'
DefeatTaskDesc = 'Defeat%(num)s%(level)s%(enemyName)s%(location)s%(weapon)s'
DefeatNPCTaskDesc = 'Defeat%(enemyName)s%(location)s'
RecoverAvatarItemTaskDesc = 'Recover%(num)s%(itemName)s from%(level)s%(enemyName)s%(location)s'
RecoverContainerItemTaskDesc = 'Recover%(num)s%(itemName)s from%(container)s%(location)s'
RecoverShipItemTaskDescS = 'Recover%(num)s%(itemName)s from a%(level)s%(faction)s%(shipName)s ship'
RecoverShipItemTaskDescSn = 'Recover%(num)s%(itemName)s from an%(level)s%(faction)s%(shipName)s ship'
RecoverShipItemTaskDescPL = 'Recover%(num)s%(itemName)s from%(level)s%(faction)s%(shipName)s ships'
CaptureShipNPCTaskDesc = 'Capture%(npcName)s from a%(level)s%(faction)s%(shipName)s ship'
CaptureShipNPCTaskDescN = 'Capture%(npcName)s from an%(level)s%(faction)s%(shipName)s ship'
DefeatShipTaskDescPL = 'Sink%(num)s%(level)s%(faction)s%(shipName)s ships'
DefeatShipTaskDescS = 'Sink%(num)s a%(level)s%(faction)s%(shipName)s ship'
DefeatShipTaskDescSn = 'Sink%(num)s an%(level)s%(faction)s%(shipName)s ship'
DeliverItemTaskDesc = 'Deliver%(num)s %(itemName)s to%(npcName)s%(location)s'
RecoverTreasureItemTaskDesc = 'Recover%(num)s%(itemName)s from a buried treasure chest%(location)s'
PoisonContainerTaskDesc = 'Poison%(num)s%(container)s%(location)s'
BurnPropTaskDesc = 'Burn%(num)s %(propName)s%(location)s'
DefeatNearPropTaskDesc = 'Defeat%(num)s%(level)s%(enemyName)s near %(propName)s%(location)s'
DefendNPCTaskDesc = 'Defend%(enemyName)s from enemies'
DefeatAroundPropTaskDesc = 'Defeat%(enemyName)s around %(propName)s to recover %(itemName)s'
DowsingRodTaskDesc = 'Recover%(itemName)s using a Dowsing Rod'
LootPropTaskDesc = 'Take treasure from %(propName)s%(location)s'
VisitPropTaskDesc = 'Visit %(propName)s%(location)s'
ScrimmageTaskDesc = 'Visit %(npcName)s%(location)s and complete %(num)s scrimmage rounds'
MultipleQuestReturnIds = 'Return to one of the following: \x01questObj\x01%(npcNames)s\x02'
MultipleChoiceQuestReturnIds = 'Return to one of the following after all parts completed: \x01questObj\x01%(npcNames)s\x02'
SingleQuestReturnId = 'Return to \x01questObj\x01%(npcName)s\x02.'
SingleQuestReturnIdCollect = 'Return to \x01questObj\x01%(npcName)s\x02 to collect the reward.'
SingleChoiceQuestReturnId = 'Return to \x01questObj\x01%(npcName)s\x02 after all parts completed.'
QuestRestartReturnId = 'Visit \x01questObj\x01%(npcName)s\x02 to restart the quest.'
DefaultTownfolkName = 'Unknown Townfolk'
ReturnVisitQuestTitle = 'Visit %s'
ReturnVisitQuestDesc = 'Return to \x01questObj\x01%s\x02.'
ReturnVisitQuestDialog = "Good, you're back. Let's start again."
QuestItemGuiTitle = '\x01questTitleMain\x01%(title)s\x02\n\n'
QuestItemGuiTask = '%(status)s\n\n'
QuestItemGuiReturnTo = '%(returnTo)s\n\n'
QuestItemGuiDescription = '\x01questTitle\x01Story\x02\n%(desc)s\n\n'
QuestItemGuiRewards = '\x01questTitle\x01Rewards\x02\n%(reward)s'
QuestItemGuiBonusRewards = '\x01questTitle\x01             Bonus Rewards\x02'
QuestItemGuiCompleteFormat = '\x01questTitleMain\x01%(title)s\x02\n\n%(status)s\n\n%(returnTo)s\n\n\x01questTitle\x01Reward\x02\n%(reward)s\n\n'
QuestItemGuiIncompleteFormat = '\x01questTitleMain\x01%(title)s\x02\n\n%(status)s\n\n\x01questTitle\x01Story\x02\n%(desc)s\n\n\x01questTitle\x01Reward\x02\n%(reward)s\n\n'
QuestItemGuiCompleteFormatNoReward = '\x01questTitleMain\x01%(title)s\x02\n\n%(status)s\n\n%(returnTo)s\n\n'
QuestItemGuiIncompleteFormatNoReward = '\x01questTitleMain\x01%(title)s\x02\n\n%(status)s\n\n\x01questTitle\x01Story\x02\n%(desc)s\n\n'
QuestItemGuiHeadingFormat = '\x01questTitleMain\x01%(title)s\x02\n\n\x01questTitle\x01Story\x02\n%(desc)s'
QuestItemGuiHeadingFormatWithReward = '\x01questTitleMain\x01%(title)s\x02\n\n\x01questTitle\x01Story\x02\n%(desc)s\n\n\x01questTitle\x01Reward\x02\n%(reward)s\n\n'
QuestItemGuiTimedFormat = '\x01questTitleMain\x01%(title)s\x02\n\n%(status)s\n\x01CPRedSlant\x01TIME LIMIT: %(timeLimit)s seconds\x02\n\n\x01questTitle\x01Story\x02\n%(desc)s\n\n\x01questTitle\x01Reward\x02\n%(reward)s\n\n'
QuestItemGuiTimedCompleteFormat = '\x01questTitleMain\x01%(title)s\x02\n\n%(status)s\n\x01CPRedSlant\x01TIME LIMIT: %(timeLimit)s seconds\x02\n\n%(returnTo)s\n\n\x01questTitle\x01Reward\x02\n%(reward)s\n\n'
QuestItemGuiTimedOutFormat = '\x01questTitleMain\x01%(title)s\x02    \x01CPRed\x01TIMED OUT\x02\n\n%(status)s\n\x01CPRedSlant\x01TIME LIMIT: %(timeLimit)s seconds\x02\n\n%(returnTo)s\n\n\x01questTitle\x01Reward\x02\n%(reward)s\n\n'
QuestItemGuiFormat = '\x01questTitleMain\x01%(title)s\x02\n\n\n\n\n\n\n\n\n'
QuestItemGuiAddRewards = '\x01questRewardTitle\x01Rewards\x02'
QuestItemGuiAddItems = '\x01questRewardTitle\x01                Items Received\x02'
QuestItemGuiAddGold = '\n%(gold)s \x05goldCoin\x05'
QuestItemGuiAddRep = '\n+ %(rep)s Rep'
TimerStatus = '\x01CPRedSlant\x01TIME LEFT: %(remainingTime)s sec.\x02'
TimedOutStatus = '\x01CPRed\x01TIMED OUT\x02'
Reputation = 'Rep'
Ship = (
    'a ship', 'ships')
QuestSCBribe = 'I need to  bribe %(npcName)s.'
QuestSCMaroonNPC = 'Maroon %(npcName)s at %(location)s.'
QuestSCFindNPC = 'I need to find %(npcName)s.'
QuestSCDefeatEnemy = 'I need to kill %(enemyName)s.'
QuestSCDefeatEnemyWeapon = 'I need to kill %(enemyName)s using a %(weaponType)s.'
QuestSCDefeatEnemyLvl = 'I need to kill %(enemyName)s L%(level)d+.'
QuestSCDefeatEnemyLvlWeapon = 'I need to kill %(enemyName)s L%(level)d+ using a %(weaponType)s.'
QuestSCDefeatEnemies = 'I need to kill %(num)s %(enemyName)s.'
QuestSCDefeatEnemiesWeapon = 'I need to kill %(num)s %(enemyName)s using a %(weaponType)s.'
QuestSCDefeatEnemiesLvl = 'I need to kill %(num)s L%(level)d+ %(enemyName)s.'
QuestSCDefeatEnemiesLvlWeapon = 'I need to kill %(num)s L%(level)d+ %(enemyName)s using a %(weaponType)s.'
QuestSCCapture = 'I need to capture a ship.'
QuestSCCaptureShip = 'I need to capture a %(shipType)s.'
QuestSCCaptureFaction = 'I need to capture a %(faction)s ship.'
QuestSCCaptureFactionShip = 'I need to capture a %(faction)s  %(shipType)s.'
QuestSCSink = 'I need to sink a ship.'
QuestSCSinkShip = 'I need to sink a %(shipType)s.'
QuestSCSinkNum = 'I need to sink %(num)s ships.'
QuestSCSinkShipNum = 'I need to sink %(num)s %(shipType)s ships.'
QuestSCSinkFaction = 'I need to sink %(faction)s ship.'
QuestSCSinkFactionShip = 'I need to sink %(faction)s %(shipType)s ships.'
QuestSCSinkFactionNum = 'I need to sink %(num)s %(faction)s ship.'
QuestSCSinkFactionNumShip = 'I need to sink %(num)s %(faction)s %(shipType)s.'
QuestSCCaptureNPC = 'I need to capture %(npcName)s.'
QuestSCCaptureNPCShip = 'I need to capture %(npcName)s from any %(shipType)s.'
QuestSCCaptureNPCFaction = 'I need to capture %(npcName)s from %(faction)s ship.'
QuestSCCaptureNPCFactionShip = 'I need to capture %(npcName)s from %(faction)s %(shipType)s.'
QuestSCRecoverItem = 'I need to recover %(itemName)s from %(enemyName)s.'
QuestSCRecoverItemNum = 'I need to recover %(num)s %(itemName)s from %(enemyName)s.'
QuestSCRecoverItemLvl = 'I need to recover %(itemName)s from %(enemyName)s L%(level)d+.'
QuestSCRecoverItemNumLvl = 'I need to recover %(num)s %(itemName)s from L%(level)d+ %(enemyName)s.'
QuestSCRecoverShipItem = 'I need to recover %(itemName)s from any ship.'
QuestSCRecoverShipItemShip = 'I need to recover %(itemName)s from any %(shipType)s.'
QuestSCRecoverShipItemNum = 'I need to recover %(num)s %(itemName)s from any ships.'
QuestSCRecoverShipItemNumShip = 'I need to recover %(num)s %(itemName)s from any %(shipType)s.'
QuestSCRecoverFactionShipItem = 'I need to recover %(itemName)s from %(faction)s ship.'
QuestSCRecoverFactionShipItemShip = 'I need to recover %(itemName)s from %(faction)s %(shipType)s.'
QuestSCRecoverFactionShipItemNum = 'I need to recover %(num)s %(itemName)s from %(faction)s ships.'
QuestSCRecoverFactionShipItemNumShip = 'I need to recover %(num)s %(itemName)s from %(faction)s %(shipType)s.'
QuestSCBossBattle = 'I need to complete the ' + BossBattleName + ': %s.'
QuestSCBossBattleMap = 'I need to complete the ' + BossBattleName + ': %(treasureMapId)s.'
QuestSCDeliverItem = 'I need to deliver %(itemName)s to %(location)s.'
QuestSCDeliverItemNum = 'I need to deliver %(num)s %(itemName)s to %(location)s.'
QuestSCSmuggleItem = 'I need to smuggle %(itemName)s to %(location)s.'
QuestSCSmuggleItemNum = 'I need to smuggle %(num)s %(itemName)s to %(location)s.'
QuestSCPokerWinGold = 'I need to win %(gold)s gold playing poker.'
QuestSCBlackjackWinGold = 'I need to win %(gold)s gold playing blackjack.'
QuestSCTreasureItem = 'I need to recover %(itemName)s from a buried treasure chest.'
QuestSCTreasureItemNum = 'I need to recover %(num)s %(itemName)s from a buried treasure chest.'
QuestSCContainerItem = 'I need to recover %(itemName)s from a storage container.'
QuestSCContainerItemNum = 'I need to recover %(num)s %(itemName)s from a storage container.'
QuestSCDeployShip = 'I need to launch my ship.'
QuestSCBurnProp = 'I need to burn %(num)s .'
QuestSCDefendNPC = 'I need to defend %(enemyName)s.'
QuestSCDefeatEnemiesAroundProp = 'I need to defeat %s.'
QuestSCSailTo = 'I need to sail to %(location)s.'
QuestSCSkeletonPokerWinGold = 'I need to win %(gold)s gold playing skeleton poker.'
QuestSCPotions = 'I need to brew a %(potionName)s potion.'
QuestSCFishing = 'I need to catch %(fishName)s fish.'
QuestSCWhereIsNPC = 'Where do I find %(npcName)s?'
QuestSCWhereIsEnemy = 'Where do I find %(enemyName)s?'
QuestSCWhereIsShip = 'Where do I find %(shipType)s ships?'
QuestSCWhereIsFaction = 'Where do I find  %(faction)s ships?'
QuestSCWhereIsFactionShip = 'Where do I find  %(faction)s %(shipType)s ships?'
QuestSCWhereIsLocation = 'Where is %(location)s?'
QuestSCWhereIsContainers = 'Where can I find containers to search?'
QuestSCWhereIsBrewingPotionTable = 'Where can I find a brewing potion table?'
QuestSCWhereIsFishingSpot = 'Where can I find a fishing spot?'
QuestSCFindTreasure = 'How do I find buried treasure?'
QuestSCFindHiddenContainer = 'How do I find hidden items?'
QuestSCHowToBribe = 'How do I bribe somebody?'
QuestSCWinPoker = 'How do I find a poker game?'
QuestSCWinBlackjack = 'How do I find a blackjack game?'
QuestSCHowToCaptureShip = 'How do I capture a ship?'
QuestSCHowToCaptureNPC = 'How do I capture an NPC?'
QuestSCHowDoIMaroon = 'How do I maroon someone?'
QuestSCHowDoIRecover = 'How do I recover %(itemName)s from %(enemyName)s?'
QuestSCHowDoIRecoverShipItem = 'How do I recover %(itemName)s from a ship?'
QuestSCWhereDoIDeployShip = 'Where do I launch my ship?'
QuestSCHowDoIDeployShip = 'How do I launch my ship?'
QuestSCWinSkeletonPoker = 'How do I find a skeleton poker game?'
QuestSCHowToBrewPotion = 'How can I brew a potion?'
QuestSCHowToCatchFish = 'How can I catch fish?'
QuestItemNotifications = {
    1: 'Enough %s have already been acquired.',
    2: '%s acquired. Quest Complete!',
    3: '%s acquired. Quest Updated.',
    4: 'Checking for %s... not found.',
    5: '%s are not found here. Look elsewhere.'
}
QuestNPCNotifications = {
    1: '%s has already been captured.',
    2: '%s captured. Quest Complete!',
    3: '%s captured. Quest Updated.',
    4: 'Checking for %s... not found.',
    5: '%s will not be found here. Look elsewhere.'
}
QuestItemNames = {
    0: ('a key', 'keys', 'Keys'),
    1: ('a sea chart', 'sea charts', 'Sea Charts'),
    2: ('an earring', 'earrings', 'Earrings'),
    3: ('a barrel of rum', 'barrels of rum', 'Barrels of Rum'),
    4: ('a crab claw', 'crab claws', 'Crab Claws'),
    5: ('a bag of coins', 'bags of coins', 'Bags of Coins'),
    6: ('a tattoo pattern', 'tattoo patterns', 'Tattoo Patterns'),
    7: ('a copper rod', 'copper rods', 'Copper Rods'),
    8: ('blood', 'blood', 'Blood'),
    9: ('a flag', 'flags', 'Flags'),
    10: ('a list', 'lists', 'Lists'),
    11: ('an arrest warrant', 'arrest warrants', 'Arrest Warrants'),
    12: ('a handkerchief', 'handkerchiefs', 'Handkerchiefs'),
    13: ('bat guano', 'bat guano', 'Bat Guano'),
    14: ('a remedy', 'remedies', 'Remedies'),
    15: ('personal effects', 'personal effects', 'Personal Effects'),
    16: ('an engraved pearl', 'engraved pearls', 'Engraved Pearls'),
    17: ('a severed arm', 'severed arms', 'Severed Arms'),
    18: ('alligator saliva', 'alligator saliva', 'Alligator Saliva'),
    19: ('venom', 'venom', 'Venom'),
    20: ('cursed wood', 'cursed wood', 'Cursed Wood'),
    21: ('a map', 'maps', 'Maps'),
    22: ('a necklace', 'necklaces', 'Necklaces'),
    23: ('a shipment of tin', 'shipments of tin', 'Shipments of Tin'),
    24: ('a shipment of sand', 'shipments of sand', 'Shipments of Sand'),
    25: ('a glass ring', 'glass rings', 'Glass Rings'),
    26: ('a wooden plate', 'wooden plates', 'Wooden Plates'),
    27: ('a chicken', 'chickens', 'Chickens'),
    28: ('a pig', 'pigs', 'Pigs'),
    29: ('an egg', 'eggs', 'Eggs'),
    30: ('a tooth', 'teeth', 'Teeth'),
    31: ('a wasp wing', 'wasp wings', 'Wasp Wings'),
    32: ('an alligator scale', 'alligator scales', 'Alligator Scales'),
    33: ('poison', 'poison', 'Poison'),
    34: ('a lump of mud', 'lumps of mud', 'Lumps of Mud'),
    35: ('a pint of grog', 'pints of grog', 'Pints of Grog'),
    36: ('a doll', 'dolls', 'Dolls'),
    37: ('a dinghy', 'dinghies', 'Dinghies'),
    38: ('release orders', 'release orders', 'Release Orders'),
    39: ('a barrel of honey', 'barrels of honey', 'Barrels of Honey'),
    40: ('a dress', 'dresses', 'Dresses'),
    41: ('a die', 'dice', 'Dice'),
    42: ('a wasp egg', 'wasp eggs', 'Wasp Eggs'),
    43: ('a container of bile', 'containers of bile', 'Containers of Bile'),
    44: ('a bottle of rum', 'bottles of rum', 'Bottles of Rum'),
    45: ('a bracelet', 'bracelets', 'Bracelets'),
    46: ('a needle', 'needles', 'Needles'),
    47: ('a kraken eye', 'kraken eyes', 'Kraken Eyes'),
    48: ('powder', 'powder', 'Powder'),
    49: ('gator water', 'gator water', 'Gator Water'),
    50: ('entrails', 'entrails', 'Entrails'),
    51: ('a splinter', 'splinters', 'Splinters'),
    52: ('dust', 'dust', 'Dust'),
    53: ('earth', 'earth', 'Earth'),
    54: ('a lichen', 'lichens', 'Lichens'),
    55: ('water', 'water', 'Water'),
    56: ('a scorpion egg', 'scorpion eggs', 'Scorpion Eggs'),
    57: ('bloody treasure', 'bloody treasure', 'Bloody Treasure'),
    58: ('nightshade', 'nightshade', 'Nightshade'),
    59: ('a whisker', 'whiskers', 'Whiskers'),
    60: ('a jar', 'jars', 'Jars'),
    61: ('a piece of paper', 'papers', 'Papers'),
    62: ('a bone', 'bones', 'Bones'),
    63: ('bone shavings', 'bone shavings', 'Bone Shavings'),
    64: ('a chest', 'chests', 'Chests'),
    65: ('a hook arm', 'hook arms', 'Hook Arms'),
    66: ('a diamond', 'diamonds', 'Diamonds'),
    67: ('a box of cigars', 'boxes of cigars', 'Boxes of Cigars'),
    68: ('a gold chain', 'gold chains', 'Gold Chains'),
    69: ('cargo', 'cargo', 'Cargo'),
    70: ('a ladle', 'ladles', 'Ladles'),
    71: ('sugar', 'sugar', 'Sugar'),
    72: ('a bottle', 'bottles', 'Bottles'),
    73: ('a barrel of molasses', 'barrels of molasses', 'Barrels of Molasses'),
    74: ('vanilla', 'vanilla', 'Vanilla'),
    75: ('bone dust', 'pinches of bone dust', 'Pinches Bone Dust'),
    76: ('swamp gas', 'swamp gas', 'Swamp Gas'),
    77: ('a stinger', 'stingers', 'Stingers'),
    78: ('a bladder', 'bladders', 'Bladders'),
    79: ('a pint', 'pints', 'Pints'),
    80: ('a pinch of cinnamon', 'pinches of cinnamon', 'Pinches of Cinnamon'),
    81: ('a coconut', 'coconuts', 'Coconuts'),
    82: ('a feather', 'feathers', 'Feathers'),
    83: ('a barrel of honey', 'barrels of honey', 'Barrels of Honey'),
    84: ('barnacles', 'barnacles', 'Barnacles'),
    85: ('a hairball', 'hairballs', 'Hairballs'),
    86: ('a flea', 'fleas', 'Fleas'),
    87: ('a drink', 'drinks', 'Drinks'),
    88: ('a schedule', 'schedules', 'Schedules'),
    89: ('a hair', 'hairs', 'Hairs'),
    90: ('honeysuckle', 'honeysuckle', 'Honeysuckle'),
    91: ('sap', 'sap', 'Sap'),
    92: ('a tear', 'tears', 'Tears'),
    93: ('a bottle of perfume', 'bottles of perfume', 'Bottles of Perfume'),
    94: ('oil', 'oils', 'Oils'),
    95: ('rum', 'rum', 'Rum'),
    96: ('orders', 'orders', 'Orders'),
    97: ('salve', 'salve', 'Salve'),
    98: ('wax', 'wax', 'Wax'),
    99: ('a chunk of meat', 'chunks of meat', 'Chunks of Meat'),
    100: ('a plank of wood', 'planks of wood', 'Planks of Wood'),
    101: ('a nail', 'nails', 'Nails'),
    102: ('a bucket of pitch', 'buckets of pitch', 'Buckets of Pitch'),
    103: ('a saw', 'saws', 'Saws'),
    104: ('a ship in a bottle', 'ships in bottles', 'Ships in Bottles'),
    105: ('a wood beam', 'wood beams', 'Wood Beams'),
    106: ('a bolt', 'bolts', 'Bolts'),
    107: ('a yard of sailcloth', 'yards of sailcloth', 'Yards of Sailcloth'),
    108: ('a rope', 'ropes', 'Ropes'),
    109: ('a cannon', 'cannons', 'Cannons'),
    110: ('a figurehead', 'figureheads', 'Figureheads'),
    111: ('a parrot', 'parrots', 'Parrots'),
    112: ('a document', 'documents', 'Documents'),
    113: ('an eye', 'eyes', 'Eyes'),
    114: ('a portrait', 'portraits', 'Portraits'),
    115: ('a treasure', 'treasures', 'Treasures'),
    116: ('a bundle of straw', 'bundles of straw', 'Bundles of Straw'),
    117: ('a bolt of silk', 'bolts of silk', 'Bolts of Silk'),
    118: ('a spool of wire', 'spools of wire', 'Spools of Wire'),
    119: ('a bag', 'bags', 'Bags'),
    120: ('dirt', 'dirt', 'Dirt'),
    121: ('a ring', 'rings', 'Rings'),
    122: ('a medal', 'medals', 'Medals'),
    123: ('a reagent', 'reagents', 'Reagents'),
    124: ('a chess piece', 'chess pieces', 'Chess Pieces'),
    125: ('a figurine', 'figurines', 'Figurines'),
    126: ('a steel rod', 'steel rods', 'Steel Rods'),
    127: ('a silver ingot', 'silver ingots', 'Silver Ingots'),
    128: ('tongs', 'tongs', 'Tongs'),
    129: ('a bucket of coal', 'buckets of coal', 'Buckets of Coal'),
    130: ('a message', 'messages', 'Messages'),
    131: ('knives', 'knives', 'Knives'),
    132: ('a grenade', 'grenades', 'Grenades'),
    133: ('a branch', 'branches', 'Branches'),
    134: ('a shrunken head', 'shrunken heads', 'Shrunken Heads'),
    135: ('a bucket of saltpeter', 'buckets of saltpeter', 'Buckets of Saltpeter'),
    136: ('a sack of charcoal', 'sacks of charcoal', 'Sacks of Charcoal'),
    137: ('a cup of sulfur', 'cups of sulfur', 'Cups of Sulfur'),
    138: ('a fuse', 'fuses', 'Fuses'),
    139: ('a flint', 'flints', 'Flints'),
    140: ('a casing', 'casings', 'Casings'),
    141: ('a bucket of tar', 'buckets of tar', 'Buckets of Tar'),
    142: ('a teleport totem', 'teleport totems', 'Teleport Totems'),
    143: ('a pair of bat wings', 'pairs of bat wings', 'Pairs of Bat Wings'),
    144: ('an alligator tooth', 'alligator teeth', 'Alligator Teeth'),
    145: ('a wasp essence', 'wasp essences', 'Wasp Essences'),
    146: ('a tortugan artifact', 'tortugan artifacts', 'Tortugan Artifacts'),
    147: ('a yard of cotton', 'yards of cotton', 'Yards of Cotton'),
    148: ('an iron bar', 'iron bars', 'Iron Bars'),
    149: ('an alligator tail', 'alligator tails', 'Alligator Tails'),
    150: ('a crab shell', 'crab shells', 'Crab Shells'),
    151: ('bat hair', 'bat hair', 'Bat Hair'),
    152: ('scorpion blood', 'scorpion blood', 'Scorpion Blood'),
    153: ('scorpion venom', 'scorpion venom', 'Scorpion Venom'),
    154: ('a barrel of whiskey', 'barrels of whiskey', 'Barrels of Whiskey'),
    155: ('a set of bar glasses', 'sets of bar glasses', 'Sets of Bar Glasses'),
    156: ('a bag of coal', 'bags of coal', 'Bags of Coal'),
    157: ('smithing tools', 'smithing tools', 'Smithing Tools'),
    158: ('the name of the attacker', 'the name of the attacker', 'the Name of the Attacker'),
    159: ('a fly trap leaf', 'fly trap leaves', 'Fly Trap Leaves'),
    160: ('a fly trap root', 'fly trap roots', 'Fly Trap Roots'),
    161: ('a Navy coat', 'Navy coats', 'Navy Coats'),
    162: ('The First Medal of Port Royal', '', 'The First Medal of Port Royal'),
    163: ('The Eye of Nabai', '', 'The Eye of Nabai'),
    164: ('a well-fashioned voodoo doll head', '', 'Well-Fashioned Voodoo Doll Heads'),
    165: ('a well-fashioned voodoo doll torso', '', 'Well-Fashioned Voodoo Doll Torsos'),
    166: ('a well-fashioned voodoo doll left arm', '', 'Well-Fashioned Voodoo Doll Left Arms'),
    167: ('a well-fashioned voodoo doll right arm', '', 'Well-Fashioned Voodoo Doll Right Arms'),
    168: ('a well-fashioned voodoo doll left leg', '', 'Well-Fashioned Voodoo Doll Left Legs'),
    169: ('a well-fashioned voodoo doll right leg', '', 'Well-Fashioned Voodoo Doll Right Legs'),
    170: ('a navy musket', 'navy muskets', 'Navy Muskets'),
    171: ('a pair of Navy pants', 'pairs of Navy pants', 'Pairs of Navy Pants'),
    172: ('a sergeant badge', 'sergeant badges', 'Sergeant Badges'),
    173: ('a prison key', 'prison keys', 'Prison Keys'),
    174: ('the hidden coins map for Fort Charles', '', ''),
    175: ('a sewing needle', 'sewing needles', 'Sewing Needles'),
    176: ('a guard schedule', 'guard schedules', 'Guard Schedules'),
    177: ('a navy ship schedule', 'navy ship schedules', 'Navy Ship Schedules'),
    178: ('a canteen of latrine water', 'canteens of latrine water', 'Canteens of Latrine Water'),
    179: ('a cup of moonlit water', 'cups of moonlit water', 'Cups of Moonlit Water'),
    180: ('a bottle of battle-touched water', 'bottles of battle-touched water', 'Bottles of Battle-Touched Water'),
    181: ('a pair of dice', 'pairs of dice', 'Pairs of Dice'),
    182: ('a water canteen', 'water canteens', 'Water Canteens'),
    183: ('a stash of rubies', 'a stash of rubies', 'Stash of Rubies'),
    184: ('a stash of amethysts', 'a stash of amethysts', 'Stash of Amethysts'),
    185: ('a stash of sapphires', 'a stash of sapphires', 'Stash of Sapphires'),
    186: ('a bottle of fine ink', 'fine inks', 'Fine Inks'),
    187: ('a deed', 'deeds', 'Deeds'),
    188: ('a EITC coat', 'EITC coats', 'EITC Coats'),
    189: ('a pair of EITC pants', 'pairs of EITC pants', 'Pairs of EITC Pants'),
    190: ('a shop application', 'shop applications', 'Shop Applications'),
    191: ('a hide', 'hides', 'Hides'),
    192: ('a contract', 'contracts', 'Contracts'),
    193: ('a blood sample', 'blood samples', 'Blood Samples'),
    194: ('a bandage', 'bandages', 'Bandages'),
    195: ('a medical tool', 'medical tools', 'Medical Tools'),
    196: ('a diary', 'diaries', 'Diary'),
    197: ('a ship log', 'ship logs', 'Ship Logs'),
    198: ('a family heirloom', 'family heirlooms', 'Family Heirlooms'),
    199: ('a gun', 'guns', 'Guns'),
    200: ('a gun order', 'gun orders', 'Gun Orders'),
    201: ('an antique pistol', 'antique pistols', 'Antique Pistols'),
    202: ('a ship plan', 'ship plans', 'Ship Plans'),
    203: ('a background check', 'background checks', 'Background Checks'),
    204: ('a bar of fine steel', 'bars of fine steel', 'Bars Of Fine Steel'),
    205: ('a strap of leather', 'leather straps', 'Leather Straps'),
    206: ('a blade sharpener', 'blade sharpeners', 'Blade Sharpeners'),
    207: ('a page from Pirate Lore', 'pages from Pirate Lore', 'Pages from Pirate Lore'),
    208: ('a chest of Pirate Lore', 'chests of Pirate Lore', 'Chests of Pirate Lore'),
    209: ('a book of Pirate Lore', 'books of Pirate Lore', 'Books of Pirate Lore'),
    210: ('an EITC manual', 'EITC manuals', 'EITC Manuals'),
    211: ('an unfinished book of Pirate Lore', 'unfinished books of Pirate Lore', 'Unfinished Books of Pirate Lore'),
    212: ('an alligator eye', 'alligator eyes', 'Alligator Eyes'),
    213: ('a wasp', 'wasps', 'Wasps'),
    214: ('a scorpion eye', 'scorpion eyes', 'Scorpion Eyes'),
    215: ('a bat eye', 'bat eyes', 'Bat Eyes'),
    216: ('a cloudy blue orb', 'cloudy blue orbs', 'Cloudy Blue Orbs'),
    217: ('a skeleton rib', 'skeleton ribs', 'Skeleton Ribs'),
    218: ('a badge', 'badges', 'Badges'),
    219: ('a writ of authority', 'writs of authority', 'Writs of Authority'),
    220: ('an alligator tooth', 'alligator teeth', 'Alligator Teeth'),
    221: ('a bat claw', 'bat claws', 'Bat Claws'),
    222: ('a skeleton bone', 'skeleton bones', 'Skeleton Bones'),
    223: ('a sunken ship mast', 'sunken ship masts', 'Sunken Ship Masts'),
    224: ('a bottle of battle-touched earth', 'bottles of battle-touched earth', 'Bottles of Battle-Touched Earth'),
    225: ('a relic piece', 'relic pieces', 'Relic Pieces'),
    226: ('Capt. Teague', 'Capt. Teague', 'Capt. Teague'),
    227: ('a spool of thread', 'spools of thread', 'Spools of Thread'),
    228: ('a rare feather', 'rare feathers', 'Rare Feathers'),
    229: ('a manifest', 'manifests', 'Manifests'),
    230: ("Bingham's diary", "Bingham's diary", "Bingham's Diary"),
    231: ('a bolt of cloth', 'bolts of cloth', 'Bolts of Cloth'),
    232: ('a pair of fine scissors', 'pairs of fine scissors', 'Pairs of Fine Scissors'),
    233: ('a spool of silk thread', 'spools of silk thread', 'Spools of Silk Thread'),
    234: ("Scarlet's pearl", "Scarlet's pearls", "Scarlet's Pearls"),
    235: ('a letter from Scarlet', 'letters from Scarlet', 'Letters From Scarlet'),
    236: ('a belt buckle', 'belt buckles', 'Belt Buckles'),
    237: ('a fine shoe design', 'fine shoe designs', 'Fine Shoe Designs'),
    238: ('a scorpion shell', 'scorpion shells', 'Scorpion Shells'),
    239: ('a piece of kraken cloth', 'kraken cloths', 'Kraken Cloths'),
    240: ('a cursed button', 'cursed buttons', 'Cursed Buttons'),
    241: ('a piece of cursed bark', 'cursed bark', 'Cursed Bark'),
    242: ('a piece of cursed cloth', 'cursed cloth', 'Cursed Cloth'),
    243: ('a piece of cursed thread', 'cursed threads', 'Cursed Thread'),
    244: ('a cursed needle', 'cursed needles', 'Cursed Needles'),
    245: ('a voodoo artifact', 'voodoo artifacts', 'Voodoo Artifacts'),
    246: ('a chunk of rotten meat', 'chunks of rotten meat', 'Chunks of Rotten Meat'),
    247: ('a compass', 'compasses', 'Compasses'),
    248: ("Lockgrim's letter", "Lockgrim's letters", "Lockgrim's Letters"),
    249: ('a tentacle', 'tentacles', 'Tentacles'),
    250: ('an Urchinfist eye', 'Urchinfist eyes', 'Urchinfist Eyes'),
    251: ('a cursed chest', 'cursed chests', 'Cursed Chests'),
    252: ('a bottle of fine rum', 'bottles of fine rum', 'Bottles of Fine Rum'),
    253: ("Turk's lucky deck", "Turk's lucky deck", "Turk's Lucky Deck"),
    254: ('a Navy shoestring', 'Navy shoestrings', 'Navy Shoestrings'),
    255: ('a Navy anchor', 'Navy anchors', 'Navy Anchors'),
    256: ('a EITC parchment', 'EITC parchments', 'EITC Parchments'),
    257: ('an empty flask', 'empty flasks', 'Empty Flasks'),
    258: ('a sail', 'sails', 'Sails'),
    259: ('a ship wheel', 'ship wheels', 'Ship Wheels'),
    260: ('a piece of Navy fabric', 'pieces of Navy fabric', 'Pieces of Navy Fabric'),
    261: ('a scrap of cursed sail cloth', 'scraps of cursed sail cloth', 'Scraps of Cursed Sail Cloth'),
    262: ('a suit of spanish armor', 'suits of spanish armor', 'Suits of Spanish Armor'),
    263: ('a spanish pistol component', 'spanish pistol components', 'Spanish Pistol Components'),
    264: ('a gun stock', 'gun stocks', 'Gun Stocks'),
    265: ('a bone handle', 'bone handles', 'Bone Handles'),
    266: ('a lock of hair', 'locks of hair', 'Locks of Hair'),
    267: ('a wooden statuette', 'wooden statuettes', 'Wooden Statuettes'),
    268: ('a barrel of gun powder', 'barrels of gun powder', 'Barrels of Gun Powder'),
    269: ('a spar', 'spars', 'Spars'),
    270: ('a stolen dagger', 'stolen daggers', 'Stolen Daggers'),
    271: ('a gem', 'gems', 'Gems'),
    272: ('a bar of navy steel', 'bars of navy steel', 'Bars of Navy Steel'),
    273: ('a gold-handle rapier', 'gold-handle rapiers', 'Gold Handle Rapiers'),
    274: ('an alligator skin', 'alligator skins', 'Alligator Skins'),
    275: ('a bat', 'bats', 'Bats'),
    276: ('a navy flag', 'navy flags', 'Navy Flags'),
    277: ('a brass button', 'brass buttons', 'Brass Buttons'),
    278: ('a crab', 'crabs', 'Crabs'),
    279: ('a skull', 'skulls', 'Skulls'),
    QuestItems.Ore: ('ore', 'ore', 'Ore'),
    QuestItems.Cure: ('a cure', 'cures', 'Cures'),
    QuestItems.LiverVial: ('a vial of liver oil', 'vials of liver oil', 'Vials of Liver Oil'),
    QuestItems.HairPatch: ('a patch of hair', 'patches of hair', 'Patches of Hair'),
    QuestItems.GourdShaker: ('a gourd shaker', 'gourd shakers', 'Gourd Shakers'),
    QuestItems.BileSack: ('a bile sack', 'bile sacks', 'Bile Sacks'),
    QuestItems.JunesItem: ("June's box item", "of June's box items", "June's Box Items"),
    QuestItems.LoveLetter: ('a love letter', 'love letters', 'Love Letters'),
    QuestItems.GallBladder: ('a gall bladder', 'gall bladders', 'Gall Bladders'),
    QuestItems.GunpowderPouch: ('a gunpowder pouch', 'gunpowder pouches', 'Gunpowder Pouches'),
    QuestItems.EmptyRumBottle: ('an empty rum bottle', 'empty rum bottles', 'Empty Rum Bottles'),
    QuestItems.SaltedRib: ('a salted rib', 'salted ribs', 'Salted Ribs'),
    QuestItems.PearlSack: ('a sack of pearls', 'sacks of pearls', 'Sacks of Pearls'),
    QuestItems.VenomSack: ('a venom sack', 'venom sacks', 'Venom Sacks'),
    QuestItems.EyeSocket: ('an eye socket', 'eye sockets', 'Eye Sockets'),
    QuestItems.Toenail: ('a toenail', 'toenails', 'Toenails'),
    QuestItems.GrogBottle: ('a bottle of grog', 'bottles of grog', 'Bottles of Grog'),
    QuestItems.LightRumBottle: ('a bottle of light rum', 'bottles of light rum', 'Bottles of Light Rum'),
    QuestItems.DarkRumBottle: ('a bottle of dark rum', 'bottles of dark rum', 'Bottles of Dark Rum'),
    QuestItems.FiveYearRum: ('a bottle of five year old rum', 'bottles five year old rum', 'Bottles of Five Year Old Rum'),
    QuestItems.TenYearRum: ('a bottle of ten year old rum', 'bottles of ten year old rum', 'Bottles of Ten Year Old Rum'),
    QuestItems.SkeletonRum: ('a bottle of skeleton rum', 'bottles of skeleton rum', 'Bottles of Skeleton Rum'),
    QuestItems.NavyRum: ('a bottle of Navy rum', 'bottles of Navy rum', 'Bottles of Navy Rum'),
    QuestItems.EITCRum: ('a bottle of EITC rum', 'bottles of EITC rum', 'Bottles of EITC Rum'),
    QuestItems.EmptyBottleBox: ('a box of empty bottles', 'boxes of empty bottles', 'Boxes of Empty Bottles'),
    QuestItems.WaterBarrel: ('a barrel of water', 'barrels of water', 'Barrels of Water'),
    QuestItems.MolassesCup: ('a cup of molasses', 'cups of molasses', 'Cups of Molasses'),
    QuestItems.Charm: ('a charm', 'charms', 'Charms'),
    QuestItems.MemoryCure: ('a memory cure', 'memory cures', 'Memory Cures'),
    QuestItems.ClothPiece: ('a piece of cloth', 'pieces of cloth', 'Pieces of Cloth'),
    QuestItems.CaneSugarBarrel: ('a barrel of cane sugar', 'barrels of cane sugar', 'Barrels of Cane Sugar'),
    QuestItems.NutmegCrate: ('a crate of nutmeg', 'crates of nutmeg', 'Crates of Nutmeg'),
    QuestItems.CursedDarkSugar: ('a barrel of cursed dark sugar', 'barrels of cursed dark sugar', 'Barrels of Cursed Dark Sugar'),
    QuestItems.DreadBitters: ('a barrel of dread bitters', 'barrels of dread bitters', 'Barrels of Dread Bitters'),
    QuestItems.CursedBarnacles: ('cursed barnacles', 'cursed barnacles', 'Cursed Barnacles'),
    QuestItems.Cutler100: ('a bottle of Cutler 100', 'bottles of Cutler 100', 'Bottles of Cutler 100'),
    QuestItems.SingaporeanRum: ('a bottle of singaporean rum', 'bottles of singaporean rum', 'Bottles of Singaporean Rum'),
    QuestItems.TwentyFiveYearRum: ('a bottle of 25 year old rum', 'bottles of 25 year old rum', 'Bottles of 25 Old Rum'),
    QuestItems.FishRumBottle: ('a bottle of fish rum', 'bottles of fish rum', 'Bottles of Fish Rum'),
    QuestItems.VoodooRumBottle: ('a bottle of voodoo rum', 'bottles of voodoo rum', 'Bottles of Voodoo Rum'),
    QuestItems.BoneRumBottle: ('a bottle of bone rum', 'bottles of bone rum', 'Bottles of Bone Rum'),
    QuestItems.GatorStomach: ('an alligator stomach', 'alligator stomachs', 'Alligator Stomachs'),
    QuestItems.BrassInstrument: ('a brass instrument', 'brass instruments', 'Brass Instruments'),
    QuestItems.ForgivenessLetter: ('a forgiveness letter', 'forgiveness letters', 'Forgiveness Letters'),
    QuestItems.Kneecap: ('a kneecap', 'kneecaps', 'Kneecaps'),
    QuestItems.PinkyRing: ('a pinky ring', 'pinky rings', 'Pinky Rings'),
    QuestItems.Money: ('money', 'money', 'Money'),
    QuestItems.Dagger: ('a dagger', 'daggers', 'Daggers'),
    QuestItems.Sword: ('a sword', 'swords', 'Swords'),
    QuestItems.Hay: ('a handful of hay', 'handfuls of hay', 'Handfuls of Hay'),
    QuestItems.MedicineKit: ('a medicine kit', 'medicine kits', 'Medicine Kits'),
    QuestItems.HerbSack: ('a herb sack', 'herb sacks', 'Herb Sacks'),
    QuestItems.Bowsprit: ('a bowsprit', 'bowsprits', 'Bowsprits'),
    QuestItems.Steelband: ('a steel band', 'steel bands', 'Steel Bands'),
    QuestItems.Rudder: ('a rudder', 'rudders', 'Rudders'),
    QuestItems.NailBox: ('a box of nails', 'boxes of nails', 'Boxes of Nails'),
    QuestItems.BoltPack: ('a pack of bolts', 'packs of bolts', 'Packs of Bolts'),
    QuestItems.WaterFlask: ('a flask of water', 'flasks of water', 'Flasks of Water'),
    QuestItems.EnlistmentOrder: ('an enlistment order', 'enlistment orders', 'Enlistment Orders'),
    QuestItems.DefensePlans: ('defense plans', 'defense plans', 'Defense Plans'),
    QuestItems.VoodooRelic: ('a voodoo relic', 'voodoo relics', 'Voodoo Relics'),
    QuestItems.SecretRecord: ('a secret record', 'secret records', 'Secret Records'),
    QuestItems.Intelligence: ('intelligence', 'intelligence', 'Intelligence'),
    QuestItems.ExcavationRecord: ('an excavation record', 'excavation records', 'Excavation Records'),
    QuestItems.LostMap: ('a lost map', 'lost maps', 'Lost Maps'),
    QuestItems.CodedOrder: ('a coded order', 'coded orders', 'Coded Orders'),
    QuestItems.Journal: ('a journal', 'journals', 'Journals'),
    QuestItems.Idol: ('an idol', 'idols', 'Idols'),
    QuestItems.DowsingRodPart: ('a dowsing rod part', 'dowsing rod parts', 'Dowsing Rod Parts'),
    QuestItems.TwistedRoot: ('a twisted root', 'twisted roots', 'Twisted Roots'),
    QuestItems.GiantBladder: ('a giant bladder', 'giant bladders', 'Giant Bladders'),
    QuestItems.FatChicken: ('a fat chicken', 'fat chickens', 'Fat Chickens'),
    QuestItems.RevivingPotion: ('a reviving potion', 'reviving potions', 'Reviving Potions'),
    QuestItems.TotemPiece: ('a totem piece', 'totem pieces', 'Totem Pieces'),
    QuestItems.CursedSail: ('a cursed sail', 'cursed sails', 'Cursed Sails'),
    QuestItems.TornSail: ('a torn sail', 'torn sails', 'Torn Sails'),
    QuestItems.UndeadSail: ('an undead sail', 'undead sails', 'Undead Sails'),
    QuestItems.TBD: ('TBD', 'TBD', 'TBD')
}
QuestDogHiddenItemNames = [
    'a hook hand', 'a rubber ducky', 'a peg leg', 'a wooden eye', "Jolly's other boot", 'an old necklace'
]
AnyAvType = (
    'Anyone', ('an enemy', 'enemies'))
FactionAvTypeNames = {
    0: ('Undead', ('a Skeleton', 'Skeletons')),
    1: ('Navy', ('a Navy Soldier', 'Navy Soldiers')),
    2: ('Creature', ('a Creature', 'Creatures')),
    3: ('Townsfolk', ('a Townsperson', 'Townsfolk')),
    4: ('Pirate', ('a Pirate', 'Pirates')),
    5: ('East India Trading Co', ('an EITC Soldier', 'EITC Soldiers')),
    6: ('Ghosts', ('a ghost', 'Ghosts')),
    7: ('Voodoo Zombies', ('a voodoo zombie', 'Voodoo Zombies')),
    8: ('Bounty Hunters', ('a bounty hunter', 'Bounty Hunters'))
}
FactionShipTypeNames = {
    0: ('Skeleton', ('a Skeleton', 'Skeleton')),
    1: ('Navy', ('a Navy', 'Navy')),
    2: ('Creature', ('a Creature', 'Creature')),
    3: ('Townsfolk', ('a Townsperson', 'Townsfolk')),
    4: ('Pirate', ('a Pirate', 'Pirate')),
    5: ('East India Trading Co', ('an East India Trading Co', 'East India Trading Co')),
    6: ('French Skeleton', ('a French Skeleton', 'French Skeleton')),
    7: ('Spanish Skeleton', ('a Spanish Skeleton', 'Spanish Skeleton'))
}
TrackAvTypeNames = {
    0: {
        0: ('Earth Undead', ('an Earth Skeleton', 'Earth Skeletons')),
        1: ('Air Undead', ('an Air Skeleton', 'Air Skeletons')),
        2: ('Fire Undead', ('a Fire Skeleton', 'Fire Skeletons')),
        3: ('Water Undead', ('a Water Skeleton', 'Water Skeletons')),
        4: ('Classic Undead', ('a Classic Skeleton', 'Classic Skeletons')),
        5: ('Boss Undead', ('a Boss Skeleton', 'Boss Skeletons')),
        6: ('French Undead', ('a French Skeleton', 'French Skeletons')),
        7: ('Spanish Undead', ('a Spanish Skeleton', 'Spanish Skeletons')),
        8: ('Earth Special Undead', ('an Earth Special Skeleton', 'Earth Special Skeletons'))
    },
    1: {
        0: ('Navy Soldiers', ('a Navy Soldier', 'Navy Soldiers')),
        1: ('Navy Marksmen', ('a Navy Marksman', 'Navy Marksmen')),
        2: ('Navy Officer', ('a Navy Officer', 'Navy Officers'))
    },
    2: {
        0: ('Land Creatures', ('a Land Creature', 'Land Creatures')),
        1: ('Sea Creatures', ('a Sea Creature', 'Sea Creatures')),
        2: ('Air Creatures', ('an Air Creature', 'Air Creatures')),
        3: ('Sea Monsters', ('a Sea Monster', 'Sea Monsters')),
        4: ('Animals', ('an Animal', 'Animals'))
    },
    3: {
        0: ('Commoners', ('a Commoner', 'Commoners')),
        1: ('Merchants', ('a Merchant', 'Merchants')),
        2: ('Cast', ('a Character', 'Characters'))
    },
    4: {
        0: ('Players', ('a Player', 'Players')),
        1: ('Pirate Brawler', ('a Pirate Brawler', 'Pirate Brawlers')),
        2: ('Pirate Gunner', ('a Pirate Gunner', 'Pirate Gunners'))
    },
    5: {
        0: ('Trading Co Mercenaries', ('a Trading Co Mercenary', 'Trading Co Mercenaries')),
        1: ('Trading Co Assassins', ('a Trading Co Assassin', 'Trading Co Assassins')),
        2: ('Trading Co Officials', ('a Trading Co Official', 'Trading Co Officials'))
    },
    6: {
        0: ('Ghosts', ('a Ghost', 'Ghosts')),
        1: ('KillerGhosts', ('a KillerGhost', 'KillerGhosts'))
    },
    7: {
        0: ('Voodoo Zombies', ('a Voodoo Zombie', 'Voodoo Zombies'))
    },
    8: {
        0: ('Bounty Hunters', ('a Bounty Hunter', 'Bounty Hunters'))
    }
}
BossNames = {
    0: {
        0: {
            0: {
                0: 'Will Burybones',
                1: 'Foul Crenshaw',
                2: 'Evan the Digger',
                3: 'Thad Ill-Fortune'
            },
            1: {
                0: 'Simon Butcher'
            },
            2: {
                0: 'Thaddeus Woodworm'
            },
            3: {
                0: 'Bonebreaker'
            },
            4: {
                0: 'Gideon Grog'
            },
            5: {
                0: 'Whit Widowmaker'
            },
            6: {
                0: 'Blackheart'
            },
            7: {
                0: 'Francis Faust'
            },
            8: {
                0: 'Jeremy Coldhand'
            },
            9: {
                0: 'Stench'
            }
        }
    },
    1: {
        1: {
            0: {
                0: 'Geoffrey Pain'
            },
            1: {
                0: 'Hugh Brandish'
            },
            2: {
                0: 'Nathaniel Grimm'
            },
            3: {
                0: 'Sid Shiver'
            },
            4: {
                0: 'Ian Ramjaw'
            }
        }
    },
    2: {
        0: {
            0: {
                0: 'Sand Stalker'
            },
            1: {
                0: 'Man Ripper'
            },
            2: {
                0: 'Claw Chief'
            },
            6: {
                0: 'Bowbreaker'
            },
            7: {
                0: 'Snap Dragon'
            },
            8: {
                0: 'Rip Tail'
            },
            9: {
                0: 'Silent Stinger'
            },
            10: {
                0: 'Bonecracker'
            },
            11: {
                0: 'Trapjaw'
            },
            12: {
                0: 'Swamp Terror'
            }
        },
        2: {
            1: {
                0: 'Frightfang'
            },
            2: {
                0: 'Bloodleach'
            },
            3: {
                0: 'Firesting'
            },
            4: {
                0: 'Devilwing'
            }
        }
    },
    5: {
        0: {
            0: {
                0: 'Carlos Cudgel'
            },
            1: {
                0: 'Zachariah Sharp'
            },
            2: {
                0: 'Henry Flint'
            },
            3: {
                0: 'Phineas Fowl'
            },
            4: {
                0: 'Edward Lohand'
            }
        }
    },
    7: {
        0: {
            7: {
                0: 'LaSchafe'
            }
        }
    }
}
BossNPCNames = {
    'dynamicBoss_1': 'Blood Blade',
    '1154059362.19Shochet': 'Crabby',
    '1154059366.69Shochet': 'Spike',
    '1169616489.03Shochet': 'Woody',
    '1218238592.59mtucker': 'Test Skeleton Boss',
    '1218760328.71mtucker': 'Venom Lash',
    '1218760329.71mtucker': 'Malicioso',
    '1219277508.79mtucker': 'Dreadtooth',
    '1219277509.79mtucker': 'Hardtack',
    '1244583168.0jloehrle0': 'Croquettes De Crabe',
    '1244833920.0jloehrle': 'Scatter Snap',
    '1244657664.0jloehrle1': 'Devil Root',
    '1244832512.0jloehrle': 'Hive Queen',
    '1219352693.09mtucker': 'Neban the Silent',
    '1219339266.79mtucker': 'Samuel',
    '1219367627.94mtucker': 'Remington the Vicious',
    '1247517440.0jloehrle': 'General Bloodless',
    '1220906480.53mtucker': 'General Hex',
    '1291327895.46jloehrle': 'Foulberto Smasho',
    '1302895055.78jloehrle': 'LaSchafe',
    '1303260680.08jloehrle': 'Tomas Blanco',
    '1303331892.2jloehrle': 'Jacques le Blanc',
    '1219434293.16mtucker': 'General Sandspine',
    NPCIds.GENERAL_DARKHART: 'General Darkhart',
    '1219426331.38mtucker': 'Bonerattler',
    NPCIds.UNDEAD_TIMOTHY_DARTAN: 'Undead Timothy Dartan',
    NPCIds.CLAUDE_DARCIS: "Claude D'Arcis",
    '1248740229.97robrusso': 'Jolly Roger',
    NPCIds.EL_PATRON: 'El Patron',
    NPCIds.KUDGEL: 'Kudgel'
}
AvatarNames = {
    0: {
        0: {
            0: ('Undead Gravedigger', ('an Undead Gravedigger', 'Undead Gravediggers')),
            1: ('Undead Bandit', ('an Undead Bandit', 'Undead Bandits')),
            2: ('Undead Pirate', ('an Undead Pirate', 'Undead Pirates')),
            3: ('Undead Mutineer', ('an Undead Mutineer', 'Undead Mutineers')),
            4: ('Undead Witchdoctor', ('an Undead Witchdoctor', 'Undead Witchdoctors')),
            5: ('Undead Brute', ('an Undead Brute', 'Undead Brutes')),
            6: ('Undead Brigand', ('an Undead Brigand', 'Undead Brigands')),
            7: ('Undead Duelist', ('an Undead Duelist', 'Undead Duelists')),
            8: ('Undead Grenadier', ('an Undead Grenadier', 'Undead Grenadiers')),
            9: ('Undead Slasher', ('an Undead Slasher', 'Undead Slashers')),
            10: ('Undead Gypsy', ('an Undead Gypsy', 'Undead Gypsies')),
            11: ('Undead Executioner', ('an Undead Executioner', 'Undead Executioners')),
            12: ('Undead Raider', ('an Undead Raider', 'Undead Raiders')),
            13: ('Undead Captain', ('an Undead Captain', 'Undead Captains')),
            14: ('Mossman', ('a Mossman', 'Mossmen'))
        },
        1: {
            0: ('Whiff', ('a Whiff', 'Whiffs')),
            1: ('Reek', ('a Reek', 'Reeks')),
            2: ('Billow', ('a Billow', 'Billows')),
            3: ('Stench', ('a Stench', 'Stenches')),
            4: ('Shade', ('a Shade', 'Shades')),
            5: ('Specter', ('a Specter', 'Specters')),
            6: ('Phantom', ('a Phantom', 'Phantoms')),
            7: ('Wraith', ('a Wraith', 'Wraiths')),
            8: ('Captain Zephyr Windshadow', ('Captain Zephyr Windshadow', 'Captain Zephyr Windshadow')),
            9: ('Squall', ('a Squall', 'Squalls'))
        },
        2: {
            0: ('Glint', ('a Glint', 'Glints')),
            1: ('Flicker', ('a Flicker', 'Flickers')),
            2: ('Smolder', ('a Smolder', 'Smolders')),
            3: ('Spark', ('a Spark', 'Sparks')),
            4: ('Imp', ('an Imp', 'Imps')),
            5: ('Brand', ('a Brand', 'Brands')),
            6: ('Lumen', ('a Lumen', 'Lumens')),
            7: ('Fiend', ('a Fiend', 'Fiends')),
            8: ('Captain Cinderbones', ('Captain Cinderbones', 'Captain Cinderbones')),
            9: ('Torch', ('a Torch', 'Torches'))
        },
        3: {
            0: ('Dregs', ('a Dregs', 'Dregs')),
            1: ('Flotsam', ('a Flotsam', 'Flotsams')),
            2: ('Spineskull', ('a Spineskull', 'Spineskull')),
            3: ('Kelpbrain', ('a Kelpbrain', 'Kelpbrains')),
            4: ('Brinescum', ('a Brinescum', 'Brinescums')),
            5: ('Seabeard', ('a Seabeard', 'Seabeards')),
            6: ('Molusk', ('a Molusk', 'Molusks')),
            7: ('Urchinfist', ('an Urchinfist', 'Urchinfists')),
            8: ('Thrall Captain', ('Thrall Captain', 'Thrall Captains')),
            9: ('Spout', ('a Spout', 'Spouts'))
        },
        4: {},
        5: {
            0: ('Jolly Roger', ('a Jolly Roger', 'Jolly Rogers'))
        },
        6: {
            0: ('French Undead Quarter Master', ('a French Undead Quarter Master', 'French Undead Quarter Masters'), 'Fr.Undead Qtr.Master'),
            1: ('French Undead Maitre', ('a French Undead Maitre', 'French Undead Maitres'), 'Fr.Undead Maitres'),
            2: ('French Undead Lieutenant', ('a French Undead Lieutenant', 'French Undead Lieutenants'), 'Fr.Undead Lieutenant'),
            3: ('French Undead Capitaine', ('a French Undead Captaine', 'French Undead Captaines'), 'Fr.Undead Capitaine'),
            4: ('French Undead Boss', ('a French Undead Boss', 'French Undead Bosses'), 'Fr.Undead Boss')
        },
        7: {
            0: ('Spanish Undead Conquistador', ('a Spanish Undead Conquistador', 'Spanish Undead Conquistadors'), 'Sp.Undead Conquistador'),
            1: ('Spanish Undead Bandido', ('a Spanish Undead Bandido', 'Spanish Undead Bandidos'), 'Sp.Undead Bandido'),
            2: ('Spanish Undead Pirata', ('a Spanish Undead Pirata', 'Spanish Undead Piratas'), 'Sp.Undead Pirata'),
            3: ('Spanish Undead Capitan', ('a Spanish Undead Capitan', 'Spanish Undead Capitans'), 'Sp.Undead Capitan'),
            4: ('Spanish Undead Boss', ('a Spanish Undead Boss', 'Spanish Undead Bosses'), 'Sp.Undead Boss')
        },
        8: {
            0: ('Powder Keg Runner', ('a Powder Keg Runner', 'Powder Keg Runner'))
        }
    },
    1: {
        0: {
            0: ('Axeman', ('a Navy Axeman', 'Navy Axemen')),
            1: ('Swordsman', ('a Navy Swordsman', 'Navy Swordsmen')),
            2: ('Royal Guard', ('a Navy Royal Guard', 'Navy Royal Guards')),
            3: ('Master Swordsman', ('a Navy Master Swordsman', 'Navy Master Swordsmen')),
            4: ('Weapons Master', ('a Navy Weapons Master', 'Navy Weapons Masters'))
        },
        1: {
            0: ('Cadet', ('a Navy Cadet', 'Navy Cadets')),
            1: ('Guard', ('a Navy Guard', 'Navy Guards')),
            2: ('Marine', ('a Navy Marine', 'Navy Marines')),
            3: ('Sergeant', ('a Navy Sergeant', 'Navy Sergeants')),
            4: ('Veteran', ('a Navy Veteran', 'Navy Veterans')),
            5: ('Officer', ('a Navy Officer', 'Navy Officers')),
            6: ('Dragoon', ('a Navy Dragoon', 'Navy Dragoons'))
        },
        2: {
            0: ('First Mate', ('a Navy First Mate', 'Navy First Mates')),
            1: ('Captain', ('a Navy Captain', 'Navy Captains')),
            2: ('Lieutenant', ('a Navy Lieutenant', 'Navy Lieutenants')),
            3: ('Admiral', ('a Navy Admiral', 'Navy Admirals')),
            4: ('Commodore', ('a Navy Commodore', 'Navy Commodores'))
        }
    },
    2: {
        0: {
            0: ('Sand Crab', ('a Sand Crab', 'Sand Crabs')),
            1: ('Stone Crab', ('a Stone Crab', 'Stone Crabs')),
            2: ('Rock Crab', ('a Rock Crab', 'Rock Crabs')),
            3: ('Giant Crab', ('a Giant Crab', 'Giant Crabs')),
            4: ('Devourer Crab', ('a Devourer Crab', 'Devourer Crabs')),
            5: ('Chicken', ('a Chicken', 'Chickens')),
            6: ('Rooster', ('a Rooster', 'Roosters')),
            7: ('Pig', ('a Pig', 'Pigs')),
            8: ('Corrupt Stump', ('a Corrupt Stump', 'Corrupt Stumps')),
            9: ('Twisted Stump', ('a Twisted Stump', 'Twisted Stumps')),
            10: ('Giant Fly Trap', ('a Giant Fly Trap', 'Giant Fly Traps')),
            11: ('Rancid Fly Trap', ('a Rancid Fly Trap', 'Rancid Fly Traps')),
            12: ('Ancient Fly Trap', ('an Ancient Fly Trap', 'Ancient Fly Traps')),
            13: ('Giant Scorpion', ('a Giant Scorpion', 'Giant Scorpions')),
            14: ('Dire Scorpion', ('a Dire Scorpion', 'Dire Scorpions')),
            15: ('Dread Scorpion', ('a Dread Scorpion', 'Dread Scorpions')),
            16: ('Swamp Alligator', ('a Swamp Alligator', 'Swamp Alligators')),
            17: ('Bayou Alligator', ('a Bayou Alligator', 'Bayou Alligators')),
            18: ('Big Alligator', ('a Big Alligator', 'Big Alligators')),
            19: ('Huge Alligator', ('a Huge Alligator', 'Huge Alligators')),
            20: ('Dog', ('a Dog', 'Dogs')),
            21: ('Seagull', ('a Seagull', 'Seagulls')),
            22: ('Raven', ('a Raven', 'Ravens')),
            23: ('Monkey', ('a Monkey', 'Monkies'))
        },
        1: {
            0: ('Fish', ('a Fish', 'Fish'))
        },
        2: {
            0: ('Seagull', ('a Seagull', 'Seagulls')),
            1: ('Raven', ('a Raven', 'Ravens')),
            2: ('Cave Bat', ('a Cave Bat', 'Cave Bats')),
            3: ('Rabid Bat', ('a Rabid Bat', 'Rabid Bats')),
            4: ('Vampire Bat', ('a Vampire Bat', 'Vampire Bats')),
            5: ('Fire Bat', ('a Fire Bat', 'Fire Bats')),
            6: ('Dire Wasp', ('a Dire Wasp', 'Dire Wasps')),
            7: ('Killer Wasp', ('a Killer Wasp', 'Killer Wasps')),
            8: ('Terror Wasp', ('a Terror Wasp', 'Terror Wasps')),
            9: ('Soldier Wasp', ('a Soldier Wasp', 'Soldier Wasps'))
        },
        3: {
            0: ('The Sea Kraken', ('a Sea Kraken', 'Sea Krakens')),
            1: ('The Kraken', ('a Kraken', 'Krakens')),
            2: ('Body', ('a body', 'bodies')),
            3: ('Head', ('a head', 'heads')),
            4: ('Tentacle', ('a tentacle', 'tentacles')),
            5: ('Wrapper Tentacle', ('a tentacle', 'tentacles')),
            6: ('Sea Serpent', ('a sea serpent', 'sea serpents'))
        },
        4: {
            0: ('Chicken', ('a Chicken', 'Chickens')),
            1: ('Rooster', ('a Rooster', 'Roosters')),
            2: ('Pig', ('a Pig', 'Pigs')),
            3: ('Dog', ('a Dog', 'Dogs')),
            4: ('Seagull', ('a Seagull', 'Seagulls')),
            5: ('Raven', ('a Raven', 'Ravens'))
        }
    },
    3: {
        0: {
            0: ('Peasant', ('a Peasant', 'Peasants'))
        },
        1: {
            0: ('Gypsy', ('a Gypsy', 'Gypsy')),
            1: ('Blacksmith', ('a Blacksmith', 'Blacksmith')),
            2: ('Shipwright', ('a Shipwright', 'Shipwright')),
            3: ('Cannoneer', ('a Cannoneer', 'Cannoneer')),
            4: ('Merchant', ('a Merchant', 'Merchant')),
            5: ('Bartender', ('a Bartender', 'Bartender')),
            6: ('Gunsmith', ('a Gunsmith', 'Gunsmith')),
            7: ('Grenadier', ('a Grenadier', 'Grenadier')),
            8: ('Medicine Man', ('a Medicine Man', 'Medicine Man')),
            9: ('Tailor', ('a Tailor', 'Tailor')),
            10: ('Tattoo', ('a Tattooist', 'Tattooist')),
            11: ('Jeweler', ('a Jeweler', 'Jeweler')),
            12: ('Barber', ('a Barber', 'Barber')),
            13: ('Musician', ('a Musician', 'Musician')),
            14: ('Trainer', ('a Trainer', 'Trainer')),
            15: ('PvP Master', ('a PvP Master', 'PvP Master')),
            16: ('Dockworker', ('a Dockworker', 'Dockworker')),
            17: ('Fishmaster', ('a Fishmaster', 'Fishmaster')),
            18: ('Cannonmaster', ('a Cannonmaster', 'Cannonmaster')),
            19: ('Catalog Rep', ('a Catalog Rep', 'Catalog Rep')),
            20: ('Scrimmage Master', ('a Scrimmage Master', 'Scrimmage Master'))
        },
        2: {
            0: ('Cast', ('a Character', 'Characters'))
        }
    },
    4: {
        0: {
            0: ('You', ('you', 'you')),
            1: ('Another Player', ('another player', 'other players'))
        },
        1: {
            0: ('Landlubber', ('a Landlubber', 'Landlubbers')),
            1: ('Scallywag', ('a Scallywag', 'Scallywags')),
            2: ('Buccaneer', ('a Buccaneer', 'Buccaneers')),
            3: ('Swashbuckler', ('a Swashbuckler', 'Swashbucklers')),
            4: ('Warmonger', ('a Warmonger', 'Warmongers'))
        },
        2: {
            0: ('Cadet', ('a Gypsy', 'Gypsy')),
            1: ('Blacksmith', ('a Blacksmith', 'Blacksmith')),
            2: ('Shipwright', ('a Shipwright', 'Shipwright')),
            3: ('Merchant', ('a Merchant', 'Merchant')),
            4: ('Bartender', ('a Bartender', 'Bartender'))
        }
    },
    5: {
        0: {
            0: ('Thug', ('an EITC Thug', 'EITC Thugs')),
            1: ('Grunt', ('an EITC Grunt', 'EITC Grunts')),
            2: ('Hired-gun', ('an EITC Hired-Gun', 'EITC Hired-Guns')),
            3: ('Mercenary', ('an EITC Mercenary', 'EITC Mercenaries')),
            4: ('Assassin', ('an EITC Assassin', 'EITC Assassins'))
        },
        1: {
            0: ('Cadet', ('an EITC Cadet', 'EITC Cadets')),
            1: ('Musketeer', ('an EITC Musketeer', 'EITC Musketeers')),
            2: ('Cannoneer', ('an EITC Cannoneer', 'EITC Cannoneers')),
            3: ('Grenadier', ('an EITC Grenadier', 'EITC Grenadiers')),
            4: ('Master Gunner', ('an EITC Master Gunner', 'EITC Master Gunners'))
        },
        2: {
            0: ('First Mate', ('an EITC First Mate', 'EITC First Mates')),
            1: ('Captain', ('an EITC Captain', 'EITC Captains')),
            2: ('Lieutenant', ('an EITC Lieutenant', 'EITC Lieutenants')),
            3: ('Admiral', ('an EITC Admiral', 'EITC Admirals')),
            4: ('Commodore', ('an EITC Commodore', 'EITC Commodores'))
        }
    },
    6: {
        0: {
            0: ('Revenant', ('a Revenant', 'Revenants')),
            1: ('Rage Ghost', ('a Rage Ghost', 'Rage Ghosts')),
            1: ('Mutineer Ghost', ('a Mutineer Ghost', 'Mutineer Ghosts')),
            2: ('Devious Ghost', ('a Devious Ghost', 'Devious Ghosts')),
            3: ('Traitor Ghost', ('a Traitor Ghost', 'Traitor Ghosts')),
            4: ('Crew Ghost', ('a Crew Ghost', 'Crew Ghosts')),
            5: ('Leader Ghost', ('a Leader Ghost', 'Leader Ghosts'))
        },
        1: {
            0: ('Rage Ghost', ('a Rage Ghost', 'Rage Ghosts'))
        }
    },
    7: {
        0: {
            0: ('Jumbee Thrall', ('a Jumbee Thrall', 'Jumbee Thralls')),
            1: ('Jumbee Cook', ('a Jumbee Cook', 'Jumbee Cooks')),
            2: ('Jumbee Swabbie', ('a Jumbee Swabbie', 'Jumbee Swabbies')),
            3: ('Jumbee Lookout', ('a Jumbee Lookout', 'Jumbee Lookouts')),
            4: ('Jumbee Thug', ('an Jumbee Thug', 'Jumbee Thug')),
            5: ('Jumbee Officer', ('a Jumbee Officer', 'Jumbee Officers')),
            6: ('Jumbee Thralldriver', ('a Jumbee Thralldriver', 'Jumbee Thralldrivers')),
            7: ('Jumbee Boss', ('a Jumbee Boss', 'Jumbee Bosses'))
        }
    },
    8: {
        0: {
            0: ('Petty Hunter', ('a Petty Hunter', 'Petty Hunters')),
            1: ('Bail Hunter', ('a Bail Hunter', 'Bail Hunters')),
            2: ('Scallywag Hunter', ('a Scallywag Hunter', 'Scallywag Hunters')),
            3: ('Bandit Hunter', ('a Bandit Hunter', 'Bandit Hunters')),
            4: ('Pirate Hunter', ('a Pirate Hunter', 'Pirate Hunters')),
            5: ('Witch Hunter', ('a Witch Hunter', 'Witch Hunters')),
            6: ('Master Hunter', ('a Master Hunter', 'Master Hunters'))
        }
    }
}
QuestPropNames = {
    'azt_idol_a_destr': ('Aztec Idol', ('an Aztec idol', 'Aztec idols')),
    'azt_idol_b_destr': ('Aztec Idol', ('an Aztec idol', 'Aztec idols')),
    'azt_skeleton_a_destr': ('Aztec skeleton', ('an Aztec skeleton', 'Aztec skeletons')),
    'azt_skeleton_b_destr': ('Aztec skeleton', ('an Aztec skeleton', 'Aztec skeletons')),
    'wpn_ammopile': ('Ammo Pile', ('an ammo pile', 'ammo piles')),
    'rok_rubble_digspot': ('Rubble', ('rubble', 'rubble')),
    'rok_rubble_tunnel': ('Rubble', ('rubble', 'rubble')),
    'wpn_weaponrack': ('Weapon Rack', ('a weapon rack', 'weapon racks')),
    'lit_torchstand': ('Torch Stand', ('a torch stand', 'torch stands')),
    'cem_tomb_inter': ('Tomb', ('a tomb', 'tombs')),
    'cav_webwall': ('Web', ('a web', 'webs')),
    'frt_tent_navy': ('Navy Tent', ('a Navy tent', 'Navy tents')),
    'bon_skullShrine': ('Shrine', ('a shrine', 'shrines')),
    'set_chair_destr': ('Chair', ('a chair', 'chairs')),
    'enm_hive_scorpion': ('Scorpion Hive', ('a Scorpion hive', 'Scorpion Hives')),
    'enm_hive_wasp': ('Wasp Hive', ('a Wasp hive', 'Wasp lives')),
    'frm_pen_livestock': ('Livestock Pen', ('a livestock pens', 'livestock pens')),
    'shp_wrk_galleon': ('Shipwreck', ('a shipwreck', 'shipwrecks')),
    'shp_wrk_mastA': ('Shipwreck', ('a shipwreck', 'shipwrecks')),
    'shp_wrk_mastB': ('Shipwreck', ('a shipwreck', 'shipwrecks')),
    'shp_wrk_mastC': ('Shipwreck', ('a shipwreck', 'shipwrecks')),
    'ocn_rock_a': ('Ocean Rock', ('an ocean rock', 'ocean rocks')),
    'ocn_rock_b': ('Ocean Rock', ('an ocean rock', 'ocean rocks')),
    'ocn_rock_c': ('Ocean Rock', ('an ocean rock', 'ocean rocks')),
    'ocn_rock_d': ('Ocean Rock', ('an ocean rock', 'ocean rocks')),
    'ocn_rock_e': ('Ocean Rock', ('an ocean rock', 'ocean rocks')),
    'ocn_rock_f': ('Ocean Rock', ('an ocean rock', 'ocean rocks')),
    'ocn_fortisland': ('Fort Island', ('a fort island', 'fort islands')),
    'cav_fortdoor': ('Fort Door', ('a fort door', 'fort doors')),
    'ocn_watchtower_eitc': ('EITC Watchtower', ('an EITC watchtower', 'EITC watchtowers')),
    'ocn_watchtower_navy': ('Navy Watchtower', ('a Navy watchtower', 'Navy watchtowers')),
    'frt_cage_inter': ('Cage', ('a cage', 'cages')),
    'cem_coffin_inter': ('Coffin', ('a coffin', 'coffins')),
    'tol_sledge': ('Sledgehammer', ('a sledgehammer', 'sledgehammers')),
    'voo_crystalball': ('Crystal Ball', ('a crystal ball', 'crystal balls')),
    'hsw_bottle_destr': ('Bottle', ('a bottle', 'bottles')),
    'set_bench_destr': ('Bench', ('a bench', 'benches')),
    'frm_sugarcane': ('Sugar Cane', ('a sugar cane', 'sugar canes')),
    'powder_keg': ('Powder Keg', ('a powder keg', 'powder kegs')),
    'dig_spot': ('Dig Spot', ('a dig spot', 'dig spots')),
    'mng_elevator_basket': ('Elevator Shaft', ('an elevator shaft', 'elevator shafts')),
    'trs_chest_02': ('Loot Skull Chest', ('a loot skull chest', 'loot skull chests'))
}
CustomQuestPropNames = {
    '1277252070.81robrusso': "El Patron's Cursed Blades"
}
QuestPropInteractStrings = {
    'bon_skullShrine': 'Press %s to summon a ghost' % InteractKey,
    'dig_spot': 'Press %s to dig' % InteractKey,
    'mng_elevator_basket': 'Press %s to use the elevator shaft' % InteractKey,
    'trs_chest_02': 'Press %s to open treasure chest' % InteractKey,
    'cav_door_elPatron': 'Press %s to open door' % InteractKey
}
CustomQuestPropInteractStrings = {
    '1274822529.65caoconno': 'Press %s to take the idol' % InteractKey
}
QuestPropWarningStrings = {
    'mng_elevator_basket': "You don't have the key to operate the elevator shaft yet!",
    'bon_skullShrine': "You can't summon a ghost right now!"
}
CustomQuestPropWarningStrings = {
    '1274822529.65caoconno': 'You cannot take the idol while any enemy ghosts are around!'
}
QuestPropUpdateTitles = {
    '1274825998.85caoconno': 'Defend the Traitor Ghost'
}
QuestPropUpdateMessages = {
    '1274825998.85caoconno': ['Quest Scenario Start!', 'Quest Scenario Complete!', 'Quest Scenario Failed!']
}
ClubheartsQuestWarning = 'The door is locked. Talk to the bouncer nearby to enter.'
PracticeDummy = 'Practice Dummy'
LandCrabStrings = ('land crab', ('a land crab', 'land crabs'))
Boss = 'Boss'
TownfolkMenuTitle = 'Townfolk'
CommonerMenuTitle = 'Commoner'
CastMenuTitle = 'Character'
PeasantMenuTitle = 'Peasant'
StoreOwnerMenuTitle = 'General Store'
GypsyMenuTitle = 'Gypsy Mystic'
BlacksmithMenuTitle = 'Blacksmith'
GunsmithMenuTitle = 'Gunsmith'
GrenadierMenuTitle = 'Grenadier'
ShipwrightMenuTitle = 'Shipwright'
MerchantMenuTitle = 'Merchant Trader'
BartenderMenuTitle = 'Bartender'
CannoneerMenuTitle = 'Cannoneer'
MedicineManMenuTitle = 'Medicine Man'
TrainerMenuTitle = 'Trainer'
FishmasterMenuTitle = 'Fishmaster'
CannonmasterMenuTitle = 'Cannonmaster'
ScrimmageMasterMenuTitle = 'Scrimmage Master'
GoldRewardDesc = '+%s Gold pieces'
MaxHpRewardDesc = '%s point HP boost'
MaxMojoRewardDesc = '%s point Voodoo boost'
LuckRewardDesc = '%s point luck boost'
SwiftnessRewardDesc = '%s point swiftness boost'
TreasureMapDesc = 'a treasure map'
ShipRewardDesc = 'a ship'
PistolRewardDesc = 'a pistol'
DollRewardDesc = 'a voodoo doll'
DaggerRewardDesc = 'a dagger'
CutlassRewardDesc = 'a cutlass'
GrenadeRewardDesc = 'a grenade'
StaffRewardDesc = 'a voodoo staff'
StaffRewardDescBurnt = 'a burnt staff'
CharmRewardDesc = 'a bandit sea globe'
TeleportTotemRewardDesc = 'a teleportation totem'
CubaTeleportRewardDesc = 'teleport access to Cuba'
PortRoyalTeleportRewardDesc = 'teleport access to Port Royal'
PadresDelFuegoTeleportRewardDesc = 'teleport access to Padres Del Fuego'
KingsHeadTeleportRewardDesc = 'teleport access to Kingshead'
RavensCoveTeleportRewardDesc = "teleport access to Raven's Cove"
ReputationRewardDesc = '+%s Notoriety Points'
SpecialQuestRewardDesc = 'a special quest unlock'
PlayingCardRewardDesc = '%s playing card'
PlayingCardRewardDescPlural = '%s playing cards'
Chapter3RewardDesc = 'a special naval ability'
JewelryQuestRewardDesc = 'a special piece of jewelry'
TattooQuestRewardDesc = 'a special tattoo'
ClothingQuestRewardDesc = 'a special piece of clothing'
Temp2xRepQuestRewardDesc = 'Temporary 2x Reputation Points'
QuestDefaultDialogBefore = (
    'Good luck to ye!', )
QuestDefaultDialogDuring = (
    "How's that task coming?", 'Have ye finished that task?')
QuestDefaultDialogAfter = (
    'Great job!', 'Excellent work!')
QuestDefaultDialogBrushoff = (
    'Got nothing for ye', 'Try someone else, mate')
VisitTaskDefaultDialogAfter = (
    'Ahoy there!', 'Hello there!')
BribeTaskDefaultDialogAfter = (
    'Pleasure doing business with ye!', 'Come back any time.')
FishSelectBait = 'Select bait to fish'
FishWaitForBite = 'Wait for fish to bite'
ReelGuiTension = 'Tension'
FishCaughtInfo = "You caught 'er!"
FishEscapedInfo = 'The fish escaped!'
LineSnappedInfo = 'Your line snapped!'
FishTensionWarning = 'Careful!!'
FishDistanceWarning = "She's gonna escape!"
FishEncouragement = "You almost got 'er"
FoundFishing = 'Found Fishing:'
FishPanelTitle = 'You Caught'
FishGenusNames = {
    0: 'Angelfish',
    2: 'Barracuda',
    4: 'Blenny',
    6: 'Boxfish',
    8: 'Cardinalfish',
    10: 'Damselfish',
    12: 'Eel',
    14: 'Flounder',
    16: 'Grouper',
    18: 'Grunt',
    20: 'Hamlet',
    22: 'Jack',
    24: 'Parrotfish',
    26: 'Porgy',
    28: 'Puffer',
    30: 'Razorfish',
    32: 'Seabass',
    34: 'Snapper',
    36: 'Squirrelfish',
    38: 'Triggerfish',
    40: 'Other',
    100: ['Seaweed', 'Old Boot', 'Empty bottle']
}
FishSpeciesNames = {
    0: ('Blue Angelfish', 'Cherubfish', 'French Angelfish', 'Queen Angelfish'),
    2: ('Great Barracuda', 'Southern Sennet'),
    4: ('Arrow Blenny', 'Diamond Blenny', 'Hairy Blenny', 'Seaweed Blenny', 'Spotcheek Bleeny'),
    6: ('Honeycomb Cowfish', 'Scrawled Cowfish', 'Smooth Trunkfish', 'Spotted Trunkfish'),
    8: ('Barred Cardinalfish', 'Dusky Cardinalfish', 'Flamefish', 'Twospot Cardinalfish', 'Whitestar Cardinalfish'),
    100: ('Seaweed', 'Old Boot', 'Empty Bottle')
}

def getFishName(genus, species):
    speciesList = FishSpeciesNames.get(genus)
    if speciesList:
        if species < len(speciesList):
            name = speciesList[species]
    return name


from pirates.ship import ShipGlobals
DeployShip = 'Launch'
Locked = 'Locked'
BoardShip = 'Board'
SelectShip = 'Select'
ParlayShip = 'Parley'
ReturnShip = 'Put Away'
SetCrewShip = 'Crew Ship'
ChooseShipTitle = 'Choose A Ship'
Return = 'Return'
WordTo = 'to'
CargoIconHelp = 'Click to show cargo'
CargoIconHelp2 = 'Amount of cargo the ship is carrying'
CrewIconHelp = 'Number of shipmates aboard ship'
KnownCrew = 'Recognized'
PermIconHelp = "Click to see captain's boarding permissions"
PermIconHelpOwn = 'Click to change boarding permissions'
BoardPermTitle = "Captain's\nBoarding Permissions"
YourShip = 'Your Ship'
CrewShip = 'Crew Ship'
GuildShip = 'Guild Ship'
FriendShip = 'Friend Ship'
PublicShip = 'Public Ship'
ShipAtSea = 'Click here to board this ship.'
ShipInBottle = 'Click here to start sailing on this ship.'
ShipSunk = 'You must repair this ship before sailing it again.'
OtherShipOut = 'One of your other ships is already at sea.'
ShipFull = 'This ship has no room left.'
Crate = 'Cargo Crate'
Chest = 'Treasure Chest'
SkChest = 'Royal Chest'
PirateShipPrefix = {
    'Sea': 0,
    'Renegade': 1,
    'Freebooter': 2,
    'Riptide': 3,
    'Skysail': 4,
    'Victory': 5,
    'Windjammer': 6,
    'Buccaneer': 7,
    'Storm': 8,
    'Storm-sail': 9,
    'Dark-sail': 10,
    'Dark-water': 11,
    'Fire-sail': 12,
    'Wave': 13,
    'Barnacle': 14,
    'Gunwale': 15,
    'Wind-racer': 16,
    'Star-chaser': 17,
    'Black': 18,
    'Headhunter': 19,
    'Scallywag': 20,
    'Bountyhunter': 21,
    'Savage': 22,
    'Scarlet': 23,
    'Fugitive': 24,
    'Crimson': 25,
    'Tide': 26,
    'Dark-wind': 27,
    'Fortune': 28,
    'Outlaw': 29,
    'Ravager': 30,
    'Vagrant': 31,
    'Moonraker': 32,
    'Red': 33,
    'Yellow': 34,
    'Silver': 35,
    'Blue': 36,
    'Green': 37,
    'White': 38,
    'Silver': 39,
    'Blade': 40,
    'Dark-blade': 41,
    'Dark': 42,
    'Shadow': 43,
    'Gun': 44,
    'Cutthroat': 45,
    'Bilge': 46,
    'Siren': 47,
    'Morning': 48,
    'Iron': 49,
    'Midnight': 50,
    'Wicked': 51,
    'Golden': 52,
    'Floundering': 53,
    'Mystical': 54,
    'Lightning': 55,
    'Sun': 56,
    'Fighting': 57,
    'Cursed': 58,
    'Ghostly': 59,
    'Intrepid': 60,
    'Laughing': 61,
    'Noble': 62,
    'Sapphire': 63,
    'Savvy': 64
}
PirateShipSuffix = {
    'Despoiler': 1,
    'Hunter': 2,
    'Cutter': 3,
    'Runner': 4,
    'Sultan': 8,
    'Defender': 9,
    'Reaver': 10,
    'Brig': 11,
    'Plunderer': 12,
    'Pillager': 13,
    'Raider': 16,
    'Brigand': 17,
    'Mercenary': 18,
    'Raptor': 19,
    'Rogue': 20,
    'Serpent': 24,
    'Seafarer': 26,
    'Forager': 27,
    'Voyager': 28,
    'Wolf': 29,
    'Shark': 30,
    'Raven': 31,
    'Stallion': 32,
    'Eagle': 33,
    'Executioner': 34,
    'Sabre': 35,
    'Dancer': 36,
    'General': 37,
    'Tiger': 38,
    'Lion': 39,
    'Hawk': 40,
    'King': 41,
    'Albatross': 42,
    'Cobra': 43,
    'Swan': 44,
    'Demon': 45,
    'Mongrel': 46,
    'Navigator': 47,
    'Fox': 48,
    'Explorer': 50,
    'Privateer': 51,
    'Bull': 52,
    'Warrior': 53,
    'Conqueror': 54,
    'Queen': 55,
    'Leopard': 56,
    'Destroyer': 57,
    'Eel': 59,
    'Dragon': 60,
    'Fish': 61,
    'Crest': 62,
    'Titan': 63,
    'Revenge': 64,
    'Trident': 66,
    'Avenger': 67,
    'Rose': 68,
    'Wrath': 69,
    'Maelstrom': 70,
    'Chariot': 71,
    'Griffin': 72,
    'Witch': 73,
    'Star': 74,
    'Dog': 75,
    'Ransom': 76,
    'Banshee': 77,
    'Mariner': 78,
    'Phoenix': 79,
    'Widow': 80,
    'Nemesis': 81,
    'Starlight': 82,
    'Thunder': 83,
    'Minnow': 84,
    'Rebel': 85,
    'Mermaid': 86,
    'Enchantress': 87,
    'Strider': 88,
    'Falcon': 89,
    'Viking': 90,
    'Guardian': 91,
    'Champion': 92,
    'Comet': 93,
    'Eclipse': 94,
    'Firelight': 95,
    'Fury': 96,
    'Legend': 97,
    'Moonracer': 98,
    'Odyssey': 99,
    'Phantom': 100,
    'Rapscallion': 101,
    'Rescuer': 102,
    'Starfire': 103,
    'Song': 104,
    'Tempest': 105,
    'Treasure': 106,
    'Vindicator': 107,
    'Wraith': 108
}

def getShipName(nameIndices):
    myName = ''
    for namePart in PirateShipPrefix:
        if PirateShipPrefix[namePart] == nameIndices[0]:
            myName += namePart

    myName += ' '
    for namePart in PirateShipSuffix:
        if PirateShipSuffix[namePart] == nameIndices[1]:
            myName += namePart

    return myName


defaultShipNames = {
    ItemId.INTERCEPTOR_L1: 'Pirate Sloop', ItemId.INTERCEPTOR_L2: 'Pirate Sloop', ItemId.INTERCEPTOR_L3: 'Pirate Sloop', ItemId.MERCHANT_L1: 'Pirate Galleon', ItemId.MERCHANT_L2: 'Pirate Galleon', ItemId.MERCHANT_L3: 'Pirate Galleon', ItemId.WARSHIP_L1: 'Pirate Frigate', ItemId.WARSHIP_L2: 'Pirate Frigate', ItemId.WARSHIP_L3: 'Pirate Frigate'
}

def getDefaultShipName(itemId):
    return defaultShipNames.get(itemId)


NavyShipTitle = 'HMS'
NavyShipPrefix = ['Bonny', 'Royal', 'Baron', 'Duke', 'Lord', 'Queen', 'Intrepid', 'Invincible', 'Fearless', 'Reliant', 'King', 'Loyal', 'Roaring', 'Defiant', 'Valiant', 'Noble', 'Impervious', 'Golden', 'Sturdy', 'Worthy', 'Fighting', 'Flying', 'Gallant', 'Brave', 'Resolute', 'Iron', 'Red', 'Vigilant', 'White']
NavyShipSuffix = [
    'Bulwark', 'Hunter', 'Virtue', 'Chastity', 'Victory', 'Dasher', 'Barricader', 'Bounty', 'Valor', 'Justice', 'Leopard', 'Tiger', 'Ferret', 'Beagle', 'Avenger', 'Boar', 'Hawk', 'Warrior', 'Conqueror', 'Rose', 'Abbot', 'Providence', 'Prudence', 'Courage', 'Fish', 'Blockader', 'Runner', 'Titan', 'Man-O-War', 'Navigator', 'Warlord', 'Hero', 'Soldier', 'Champion', 'Triumph'
]
TradingShipTitle = 'EI'
TradingShipPrefix = ['Glorious', 'Rich', 'Magnificent', 'Wondrous', 'Joyful', 'Shining', 'Triumphant', 'Golden', 'Silver', 'Platinum']
TradingShipSuffix = [
    'Plunder', 'Horde', 'Force', 'Host', 'Vanguard', 'Treasure', 'Journey'
]
SkeletonShipTitle = 'SK'
SkeletonShipPrefix = ['Dire', 'Phantom', 'Dark', 'Dread', 'Storm', 'Midnight', 'Black', 'Cursed', 'Crimson', 'Carrion', 'Rancid', 'Rotten', 'Bloody', 'Vile', 'Venomous', 'Corrupted']
SkeletonShipSuffix = [
    'Treachery', 'Wraith', 'Bane', 'Pestilence', 'Gloom', 'Rebellion', 'Massacre', 'Doom', 'Tyranny', 'Grudger', 'Reaper', 'Revenge', 'Anarchy', 'Despair', 'Raider', 'Pain', 'Terror', 'Betrayal', 'Mutiny', 'Nemesis', 'Villany', 'Destroyer', 'Slaughter', 'Nightmare', 'Vulture', 'Predator', 'Omen', 'Crow', 'Buzzard', 'Vulture', 'Malice', 'Blade', 'Death', 'Harbinger', 'Shadow', 'Torturer'
]
TheBlackPearl = 'The Black Pearl'
TheDauntless = 'The Dauntless'
TheFlyingDutchman = 'The Flying Dutchman'
TheJollyRoger = "The Tyrant's Blade"
TheQueenAnnesRevenge = "The Queen Anne's Revenge"

def enumerateShipNames():
    firstPirate = PirateShipPrefix.keys()
    firstNavy = NavyShipPrefix[: ]
    firstTrading = TradingShipPrefix[: ]
    firstSkeleton = SkeletonShipPrefix[: ]
    lastPirate = PirateShipSuffix.keys()
    lastNavy = NavyShipSuffix[: ]
    lastTrading = TradingShipSuffix[: ]
    lastSkeleton = SkeletonShipSuffix[: ]
    proper = [
        TheBlackPearl, TheDauntless, TheFlyingDutchman, TheJollyRoger, TheQueenAnnesRevenge
    ]
    return (
        firstPirate, lastPirate, firstNavy, lastNavy, firstTrading, lastTrading, firstSkeleton, lastSkeleton)


def enumerateShipNameTokens():
    import operator
    return reduce(operator.add, enumerateShipNames())


def printShipNameTokens():
    for name in sorted(enumerateShipNameTokens()):
        pass


BlackjackActionNames = {
    0: 'No Action',
    1: 'Bid %s',
    2: 'Stay',
    3: 'Hit',
    4: 'Split',
    5: 'Double Down',
    6: 'Would you like a card?',
    7: '',
    8: 'Would you like to bid?'
}
PlayingCardSuits = (
    'Hearts', 'Diamonds', 'Clubs', 'Spades')
PlayingCardRanks = (
    'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
PlayingCardRanksPlural = (
    'Twos', 'Threes', 'Fours', 'Fives', 'Sixes', 'Sevens', 'Eights', 'Nines', 'Tens', 'Jacks', 'Queens', 'Kings', 'Aces')
PlayingCardHands = {
    'Nothing': '',
    'NoPair': 'High Card',
    'OnePair': 'Pair',
    'TwoPair': 'Two Pair',
    'Trips': 'Three of a Kind',
    'Straight': 'Straight',
    'Flush': 'Flush',
    'FlHouse': 'Full House',
    'Quads': 'Four of a Kind',
    'StFlush': 'Straight Flush'
}

def getHandNameSimple(handCode, cards):
    return PlayingCardHands.get(handCode, 'Unknown')


def getHandNameFull(handCode, cards):

    def getRank(card):
        return card % 13

    cardNames = map(lambda card: PlayingCardRanks[getRank(card)], cards)
    cardNamesPlural = map(lambda card: PlayingCardRanksPlural[getRank(card)], cards)
    if handCode == 'Nothing':
        return ''
    elif handCode == 'NoPair':
        return '%s High' % cardNames[0]
    elif handCode == 'OnePair':
        return 'Pair of %s\n%s kicker' % (cardNamesPlural[0], cardNames[2])
    elif handCode == 'TwoPair':
        return 'Two Pair\n%s and %s' % (cardNamesPlural[0], cardNamesPlural[2])
    elif handCode == 'Trips':
        return 'Three of a Kind\n%s' % cardNamesPlural[0]
    elif handCode == 'Straight':
        return 'Straight to the %s' % cardNames[0]
    elif handCode == 'Flush':
        return 'Flush\n%s high' % cardNames[0]
    elif handCode == 'FlHouse':
        return 'Full House\n%s over %s' % (cardNamesPlural[0], cardNamesPlural[3])
    elif handCode == 'Quads':
        return 'Four of a Kind\n%s' % cardNamesPlural[0]
    elif handCode == 'StFlush':
        if getRank(cards[0]) == 12:
            return 'Royal Flush'
        else:
            return 'Straight Flush\n%s High' % cardNames[0]
    else:
        return 'Unknown'


PlayingCardTemplate = '%s of %s'
PlayingCardUnknown = 'Unknown'

def getPlayingCardName(suit, rank):
    suitName = PlayingCardSuits[suit]
    rankName = PlayingCardRanks[rank]
    return PlayingCardTemplate % (rankName, suitName)


NameGUI_CheckboxText = [
    'Show', 'Hide'
]
NameGUI_RandomButtonText = 'Random Name'
NameGUI_TypeANameButtonText = 'Type a Name'
NameGUI_PickANameButtonText = 'Pick a Name'
NameGUI_SubmitButtonText = lSubmit
NameGUI_NextListItemText = lNext
NameGUI_PrevListItemText = 'Prev'
NameGUI_EmptyNameText = ' \n '
NameGUI_NoNameWarnings = ["Don't you want to have any name at all?", 'You gotta have a first or a last name, mate!']
NameGUI_Guidelines = 'Your name will need to be approved.  Make sure it has: \n\n  - No foul language\n  - No personal information\n  - No brand names\n'
NameGUI_URLText = '\x01uline\x01Click here to see all naming guidelines\x02'
PirateNames_NickNamesGeneric = [
    'Crazy', 'Bloody'
]
PirateNames_NickNamesFemale = [
    'Angel', 'Blonde', 'Bonny', 'Lady', 'Little', 'Lovely', 'Madam', 'Miss', 'Pretty', 'Pirate'
]
PirateNames_NickNamesMale = [
    'Gentleman', 'Fat', 'Big', 'Long', 'Yellow', 'Calico', 'Red', 'Scurvy', 'Stinky', 'Smelly', 'Blind', 'Dread', 'Swabby', 'Shabby', 'Stumpy', 'Spanish', 'Dirty', 'Drunk', 'Drunken', 'Cutthroat', 'Cross-eyed', 'Short-stack', 'Stupid', 'Lazy', 'Iron', 'Coal', 'Old', 'Ugly', 'Gruesome'
]
PirateNames_FirstNamesMale = [
    'Antoine', 'Antonio', 'Bart', 'Bartholomew', 'Basil', 'Ben', 'Benjamin ', 'Bill', 'Billy', 'Blaze', 'Charles', 'Chris', 'Christopher', 'Danger', 'Dashing', 'David', 'Davy', 'Destiny', 'Dog', 'Edgar', 'Edward', 'Eric', 'Enrique', 'Fenris', 'Flynn', 'Fortune', 'Francis', 'Francois', 'Geoffrey', 'George', 'Gerard', 'Hector', 'Henry', 'Hikaru', 'Ichabod', 'Isaiah', 'Jack', 'James', 'Jamie', 'Jason', 'Jeffrey', 'Jeremiah', 'Jessie', 'Jim', 'John', 'Johnny', 'Joseph', 'Lawrence', 'Leon', 'Luis', 'Marc', 'Mark', 'Matthew', 'Maximus', 'Nate', 'Nathaniel', 'Ned', 'Nick', 'Pepper', 'Peregrine', 'Peter', 'Quinn', 'Raven', 'Richard', 'Ricardo', 'Robert', 'Roger', 'Sam', 'Samuel', 'Simon', 'Solomon', 'Sven', 'Thaddeus', 'Thomas', 'Tobias', 'Tom', 'Will', 'William', 'Willow', 'Wolf'
]
PirateNames_FirstNamesFemale = [
    'Amelia', 'Angel', 'Anne', 'Bess', 'Beth', 'Bettie', 'Blaze', 'Catherine', 'Charlotte', 'Cleo', 'Constance', 'Danger', 'Darling', 'Dashing', 'Destiny', 'Eliza', 'Elizabeth', 'Emily', 'Esmerelda', 'Fortune', 'Gabrielle', 'Gertrude', 'Grace', 'Helena', 'Hikaru', 'Isabella', 'Jade', 'Jane', 'Janet', 'Jeanne', 'Jessie', 'Joan', 'Kat', 'Kate', 'Kelly', 'Kenya', 'Li', 'Linda', 'Lisa', 'Liz', 'Lorelei', 'Maggie', 'Margaret', 'Marge', 'Maria', 'Mary', 'Meg', 'Meghan', 'Mercy', 'Molly', 'Nell', 'Nelly', 'Penny', 'Pepper', 'Peregrine', 'Quinn', 'Rachel', 'Raven', 'Rosa', 'Rose', 'Roxy', 'Sage', 'Samantha', 'Sarah', 'Violet', 'Willow'
]
PirateNames_FirstNamesGeneric = []
PirateNames_LastNamePrefixesGeneric = [
    'Bad', 'Barrel', 'Bilge', 'Blade', 'Blast', 'Blue', 'Brave', 'Brawl', 'Bridge', 'Burn', 'Cabin', 'Calico', 'Calle', 'Cannon', 'Chain', 'Chip', 'Coal', 'Crest', 'Dagger', 'Damp', 'Dark', 'Deck', 'Dock', 'Dread', 'Edge', 'Fair', 'Fire', 'Foul', 'Gold', 'Gun', 'Helm', 'Hex', 'Hook', 'Hull', 'Iron', 'Keel', 'Lock', 'Merry', 'Moon', 'Phantom', 'Pillage', 'Plank', 'Plunder', 'Pond', 'Prow', 'Pug', 'Raid', 'Red', 'Rig', 'Rope', 'Ruby', 'Savage', 'Sail', 'Scurvy', 'Sea', 'Shark', 'Ship', 'Shore', 'Singed', 'Squid', 'Stern', 'Storm', 'Sun', 'Sword', 'Tack', 'Tiger', 'Treasure', 'True', 'War', 'Wave', 'Witch', 'Yellow', 'Wild', 'Whale'
]
PirateNames_LastNamePrefixesCapped = [
    'Mac', 'Mc', "O'"
]
PirateNames_LastNamePrefixesMale = [
    'Grease'
]
PirateNames_LastNamePrefixesFemale = [
    'Heart'
]
PirateNames_LastNameSuffixesMale = [
    'beard', 'davis', 'dougal', 'roberts', 'wallace'
]
PirateNames_LastNameSuffixesFemale = [
    'bonnet', 'bonney', 'fellow', 'hara'
]
PirateNames_LastNameSuffixesGeneric = [
    'arrow', 'batten', 'bellows', 'bain', 'bane', 'bolt', 'bones', 'bowers', 'breaker', 'burn', 'butler', 'castle', 'cloud', 'crash', 'cutter', 'eagle', 'easton', 'falcon', 'feather', 'fitte', 'fish', 'flint', 'foote', 'fox', 'fury', 'gallows', 'ginty', 'grin', 'grim', 'gull', 'hawk', 'hayes', 'hazzard', 'hogge', 'hound', 'kidd', 'legend', 'loather', 'martin', 'malley', 'menace', 'might', 'monger', 'morgan', 'morrigan', 'morris', 'monk', 'paine', 'parr', 'phoenix', 'pigge', 'pratt', 'quick', 'rackham', 'rage', 'rat', 'ratte', 'rose', 'scarlett', 'sharp', 'shot', 'shout', 'silver', 'skull', 'slipper', 'spark', 'stack', 'steel', 'stone', 'smythe', 'spinner', 'stealer', 'swain', 'swine', 'timbers', 'thorn', 'vane', 'walker', 'ward', 'wash', 'waters', 'weather', 'whirl', 'winds', 'wraith', 'wrecker'
]

def getMaleNicknames():
    return PirateNames_NickNamesGeneric + PirateNames_NickNamesMale


def getMaleFirstnames():
    return PirateNames_FirstNamesGeneric + PirateNames_FirstNamesMale


def getMaleLastnamePrefixes():
    return PirateNames_LastNamePrefixesGeneric + PirateNames_LastNamePrefixesCapped + PirateNames_LastNamePrefixesMale


def getMaleLastnameSuffixes():
    return PirateNames_LastNameSuffixesGeneric + PirateNames_LastNameSuffixesMale


def getFemaleNicknames():
    return PirateNames_NickNamesGeneric + PirateNames_NickNamesFemale


def getFemaleFirstnames():
    return PirateNames_FirstNamesGeneric + PirateNames_FirstNamesFemale


def getFemaleLastnamePrefixes():
    return PirateNames_LastNamePrefixesGeneric + PirateNames_LastNamePrefixesCapped + PirateNames_LastNamePrefixesFemale


def getFemaleLastnameSuffixes():
    return PirateNames_LastNameSuffixesGeneric + PirateNames_LastNameSuffixesFemale


def enumeratePirateNames():
    firstGeneric = PirateNames_FirstNamesGeneric[: ]
    firstMale = PirateNames_FirstNamesMale[: ]
    firstFemale = PirateNames_FirstNamesFemale[: ]
    lastGeneric = []
    lastMale = []
    lastFemale = []
    for pre in PirateNames_LastNamePrefixesGeneric + PirateNames_LastNamePrefixesCapped:
        lastGeneric.extend((pre + suf for suf in PirateNames_LastNameSuffixesGeneric))

    for pre in PirateNames_LastNamePrefixesGeneric + PirateNames_LastNamePrefixesCapped:
        lastMale.extend((pre + suf for suf in PirateNames_LastNameSuffixesMale))

    for pre in PirateNames_LastNamePrefixesMale:
        lastMale.extend((pre + suf for suf in PirateNames_LastNameSuffixesGeneric))

    for pre in PirateNames_LastNamePrefixesMale:
        lastMale.extend((pre + suf for suf in PirateNames_LastNameSuffixesMale))

    for pre in PirateNames_LastNamePrefixesGeneric + PirateNames_LastNamePrefixesCapped:
        lastFemale.extend((pre + suf for suf in PirateNames_LastNameSuffixesFemale))

    for pre in PirateNames_LastNamePrefixesFemale:
        lastFemale.extend((pre + suf for suf in PirateNames_LastNameSuffixesGeneric))

    for pre in PirateNames_LastNamePrefixesFemale:
        lastFemale.extend((pre + suf for suf in PirateNames_LastNameSuffixesFemale))

    return (firstGeneric, lastGeneric, firstMale, lastMale, firstFemale, lastFemale)


def enumeratePirateNameTokens():
    import operator
    return reduce(operator.add, enumeratePirateNames())


def enumeratePirateNameTokensLower():
    nameTokens = enumeratePirateNameTokens
    return [token.lower() for token in enumeratePirateNameTokens()]


def printPirateNameTokens():
    for name in sorted(enumeratePirateNameTokens()):
        pass


QuestScriptTutorialJack_1 = "Aren't you a sight, You look like I feel."
QuestScriptTutorialJack_2 = 'Here, use this to pull yourself together, mate.'
QuestScriptTutorialJack_3 = 'Ah, a bonnie lass.'
QuestScriptTutorialJack_4 = "You're a big fella aren't ya?"
QuestScriptTutorialJack_5 = 'Some of these should fit you.'
QuestScriptTutorialJack_6 = "Much better! So now, I'm Captain Jack Sparrow, if you please. Who might you be? Forgot your name as well?"
QuestScriptTutorialJack_10 = 'Well I need something to call you by.'
QuestScriptTutorialJack_11 = 'An honor to meet you...truly.'
QuestScriptTutorialJack_12 = 'Now, time for us to make our exit.'
QuestScriptTutorialJack_14 = 'Works every time!'
QuestScriptTutorialJack_15 = 'You look a bit unsteady, are you sure you can walk?'
QuestScriptTutorialJack_16 = 'You might want to go see Doggerel Dan over at the Black Dog Inn.'
QuestScriptTutorialJack_17 = "He'll fix you up right straight. Tell him Captain Jack sent you."
QuestScriptTutorialDan_a_1 = ''
QuestScriptTutorialDan_1 = 'Ahoy mate! Welcome to Rambleshack! Capn Jack sent ye, did he?'
QuestScriptTutorialDan_2 = 'A finer scallywag never did stumble the halls of this here Inn than Ole Jack!'
QuestScriptTutorialDan_3 = 'Did he mention he still owes me? For that Thing?'
QuestScriptTutorialDan_4 = "Well then, I suppose I've been holding this sea chest for you."
QuestScriptTutorialDan_5 = "Come on, open 'er up."
QuestScriptTutorialDan_5b = "You might want to let it breath a little...that scrap of biscuit there is still crawlin'."
QuestScriptTutorialDan_6 = 'Look straight, a pirate keeps all manner of precious things in his sea chest.'
QuestScriptTutorialDan_7 = 'But the most important of all is the pirate journal.'
QuestScriptTutorialDan_8 = 'Ye see, pirates is forgetful folk, so they need to keep a reckoning.'
QuestScriptTutorialDan_9 = "Now reckon this mate: you best be leavin' this hairy little wart of an island."
QuestScriptTutorialDan_9b = "Winds' a changin' and that means there's trouble about"
QuestScriptTutorialDan_10 = 'Get yourself down to the docks and find Captain Bo Beck.'
QuestScriptTutorialDan_10b = "I'll put that in the journal for ya."
QuestScriptTutorialDan_11 = 'Lost already? Better get down to the dock - '
QuestScriptTutorialDan_12 = "Bo Beck's stinkbucket of a raft will be shipping out for Bilgewater on the tide."
QuestScriptTutorialStumpy_1 = 'Grab a cannon, and keep an eye peeled for trouble.'
QuestScriptTutorialStumpy_6 = "Avast! ye've winged her! Good shootin' matie."
QuestScriptTutorialStumpy_8 = "Look sharp! Wouldn't want them to catch us unawares."
QuestScriptTutorialJR_1 = 'What fools be pirating in my waters?'
QuestScriptTutorialJR_2 = "Mmm, I've not seen ye before... not much mojo to speak of - yet."
QuestScriptTutorialJR_3 = "I'll deal with ye later."
QuestScriptTutorialJR_4 = "Ahoy mates! Send their ship to Davy Jones' locker."
QuestScriptShipwrightWarningA_1 = 'Ahoy, landlubber! A word to the wise, matey...'
QuestScriptShipwrightWarningA_2 = "Ye shouldn't be without a Sword in these parts."
QuestScriptShipwrightWarningA_3 = "Go see me friend Will Turner at the Rowdy Rooster, he take good care o' ya!"
QuestScriptShipwrightIntro_1 = 'Ahoy, ye landlubber! This here be the Shipyard!'
QuestScriptShipwrightIntro_2 = 'Avast! Ye be a pirate and ye have no vessel!?'
QuestScriptShipwrightIntro_3 = "This dingy be all I can spare. She ain't much, but it'll keep ye afloatin!"
QuestScriptShipwrightIntro_4 = 'Come back here when yer ready to buy a real Ship!'
QuestScriptShipwrightIntro_5 = 'Yarrr, and bring a bit more %s too.' % MoneyName
QuestScriptCutlassTutorial_1 = 'I practice three hours a day, so in all likelihood I can help you brush up your skills with the blade...'
QuestScriptCutlassTutorial_2 = "There's no parley with Jolly Roger, so be careful."
QuestScriptCutlassTutorial_3 = 'Very well.  Draw your sword.'
QuestScriptCutlassTutorial_3_5 = "'T will be difficult to cut down a skeleton in your path, if you haven't yet drawn your sword..."
QuestScriptCutlassTutorial_3_6 = 'It seems you are bound by a spell of lethargy.'
QuestScriptCutlassTutorial_4 = "I didn't have time to fashion a proper spell, so this dummy will have to do..."
QuestScriptCutlassTutorial_5 = 'Not to worry, simply advance and strike the dummy'
QuestScriptCutlassTutorial_5_5 = "I assure you.  He won't feel a thing."
QuestScriptCutlassTutorial_6 = "Good effort, but you'll need to be accurate if you're to defeat an enemy"
QuestScriptCutlassTutorial_7 = 'Move close and face the dummy.'
QuestScriptCutlassTutorial_7_5 = 'The lesson is not over, you still have much to learn.'
QuestScriptCutlassTutorial_8 = "Very good.  Alright let's move on. A true swordsman knows that timing and finesse will accomplish more than just swinging the blade around."
QuestScriptCutlassTutorial_8_5 = "If you slow down, you'll inflict more damage by chaining attacks together."
QuestScriptCutlassTutorial_8_6 = 'Too late, try again.'
QuestScriptCutlassTutorial_8_7 = 'Slow down and try again.'
QuestScriptCutlassTutorial_9 = 'Nicely executed!'
QuestScriptCutlassTutorial_9_25 = "A true pirate is defined by his reputation.  The greater your reputation, the easier it will be to defeat your enemies.  Now, let's try another skill."
QuestScriptCutlassTutorial_9_5 = 'The greater your reputation, the easier it will be to best your enemies.'
QuestScriptCutlassTutorial_10 = "Please, try out the new skill I've taught you."
QuestScriptCutlassTutorial_11 = "You're swinging too fast.  Try to swing a second time, just as your first attack ends."
QuestScriptCutlassTutorial_12 = 'Better to practice your new move on the dummy before trying it on Jolly Roger himself... go ahead.'
QuestScriptCutlassTutorial_13 = 'Well done!'
QuestScriptBlacksmithIntro_1 = 'Who are you?'
QuestScriptBlacksmithIntro_2 = "A friend of Jack's, are you?"
QuestScriptBlacksmithIntro_3 = "No sword? That won't do in these parts."
QuestScriptBlacksmithIntro_4 = 'Here, take this Cutlass. Give it a try.'
QuestScriptBlacksmithIntro_5 = 'Unfamiliar with the blade?'
QuestScriptBlacksmithIntro_6 = "It's okay to cross swords with a friend on occasion."
QuestScriptBlacksmithIntro_7 = 'Come on, just so you get the feel of it.'
QuestScriptBlacksmithIntro_8 = 'Okay, that will do.'
QuestScriptBlacksmithIntro_9 = 'Certain circumstances require a bit more firepower.'
QuestScriptBlacksmithIntro_10 = 'Take this pistol to protect against the worst that Jolly Roger has to offer.'
QuestScriptBlacksmithIntro_11 = "But don't go shootin' that thing at human folk... us Pirates must maintain a bit o' decency."
QuestScriptBlacksmithIntro_12 = "It's the Pirate Code, mate."
QuestScriptBlacksmithIntro_13 = "The Code's all we have to separate us from the likes of Jolly Roger."
QuestScriptBlacksmithIntro_14 = 'Besides, blasting away at the Navy will land you in jail faster than a dog can lift his leg.'
QuestScriptBlacksmithIntro_15 = "As for all manner of beasties, both nautical and land-lubber'd... fire away mate!"
QuestScriptBlacksmithIntro_17 = 'Go now, practice your skills with your new weapons on some crabs. Visit me when done.'
QuestScriptBlacksmithIntro_18 = 'After that, Billy Plankbite will be expecting you. Look for him in the swamps.'
QuestScriptPistolTutorial_1 = 'Now, take aim at the cursed simian over there...prove your mettle with the hand cannon!'
QuestScriptPistolTutorial_2 = "Come on, he can't feel a thing."
QuestScriptPistolTutorial_3 = 'A fine shot!  The little wretch had it coming...'
QuestScriptShipIntro = "Okay mate, I'll give ye a ship... but ye'll need to rename her so as no one can trace her back to me."
QuestScriptShipFinal = "Take good care of her... you'll not get a deal like this again."
TiaShowVoodooDoll = 'I been watching you...\x07Greatness lies behind your eyes... still, you have much to learn.\x07I will show you the way of the dark arts...\x07... but you must prove your worth... if you are to succeed.\x07Do not question my methods, only do as I say.\x07We begin with a trifle... a trifle true enough, but in the right hands it can bring down an army...\x07Look upon \x01slant\x01The Doll\x02!\x07The learning of the doll be in the learning of its construction... each must make their own.\x07Now go! We have much work to do.'
QuestScriptGypsyIntro_1 = 'Greetings, stranger.'
QuestScriptGypsyIntro_2 = 'I am Madame Bernadette, a mystic and oracle of the Gypsy people.'
QuestScriptGypsyIntro_3 = 'Have you come to learn of the arcane art of Voodoo?'
QuestScriptTiaDalmaCh2Rung1_1 = 'The claws told me you held great promise.'
QuestScriptTiaDalmaCh2Rung1_2 = 'Help witty Jack when you can.  Seek me in if you want to learn more of the dark arts.'
QuestScriptGrahamMarsh_1b_1 = "Lookin' for some honest pirating, eh?"
QuestScriptGrahamMarsh_1b_2 = "Yellow Dan stole my bloody treasure...but he only got half! And now he's cursed!"
QuestScriptGrahamMarsh_1b_3 = "I buried mine in a proper chest -- find it and I'll share the prize."
QuestScriptGrahamMarsh_1b_4 = "Where?  In the cave by the beach.  Don't recollect precisely...dig around, you lazy scabs!"
QuestScriptGrahamMarsh_1a_1 = "Well done.  You'll make proper scalawags yet..."
QuestScriptGrahamMarsh_2b_1 = 'Find the other earring just like mine -- together they be the prize!'
QuestScriptGrahamMarsh_2b_2 = "A Navy contact told me Yellow Dan was captured by some of Jolly Roger's goons..."
QuestScriptGrahamMarsh_2b_3 = "So you'll have to sink Roger's ships until you find the other earring."
QuestScriptGrahamMarsh_2b_4 = 'When you have both, take them to Sophie on Volcano Island.'
QuestScriptGrahamMarsh_2b_5 = 'She knows what to do with them...and will reward you for your efforts.'
QuestScriptGrahamMarsh_2a_1 = "I was captured by the devils.  Can't stand the smell of 'em."
QuestScriptGrahamMarsh_2a_2 = "Made an appointment with Davy Jones just so my nose'd stop burnin'"
QuestScriptGrahamMarsh_2a_3 = "Didn't realize I was cursed me-self!"
QuestScriptGrahamMarsh_2a_4 = "So here I am back from the dead... and I'll be needin' my treasure back."
QuestScriptGrahamMarsh_3a_1 = 'Do you have the earrings?'
QuestScriptGrahamMarsh_3a_2 = "Voodoo earrings don't like being split up..."
QuestScriptGrahamMarsh_3a_3 = "That's how Yellow Dan found himself cursed."
QuestScriptGrahamMarsh_3a_4 = 'But Marsh knew I could undo it.'
QuestScriptGrahamMarsh_3a_5 = 'Thanks for your help.  This is for your troubles...'
CutEscCutscene = 'Press Esc to Skip'
CutSubtitle1_1_1__1 = "Aren't you a sight? Hmm, you look how I feel, mate.\nHere, pull yourself together."
CutSubtitle1_1_1__2 = ''
CutSubtitle1_1_1__3 = ''
CutSubtitle1_1_2__1 = 'An honor to meet you, truly!'
CutSubtitle1_1_2__2 = "And now it's time to make our sortie...\nas in exit... as in leave... as in... NOW!"
CutSubtitle1_1_2__3 = 'Works every time!'
CutSubtitle1_1_2__4 = "That's not thunder mate. If I were you, I'd fetch my personal effects\nand get out of the range of those cannons."
CutSubtitle1_1_2__5 = 'Doggerel Dan will help you out.'
CutSubtitle1_1_2__6 = "That is, if he's still on this scrap of an island."
CutSubtitle1_1_2__7 = "Tell 'em that Captain Jack Sparrow sent you!"
CutSubtitle1_1_5_a__1 = "Nah, nah, nah, nah, we are closed mate, out o' business!"
CutSubtitle1_1_5_a__2 = "Packin' up before those cannons get any closer\nand you'd do the same if you know what's good for ye."
CutSubtitle1_1_5_a__3 = "What's that? Captain Jack sent you?"
CutSubtitle1_1_5_a__4 = 'Did he mention that he still owes me... for that... thing?'
CutSubtitle1_1_5_a__5 = 'Ah, Doggerel!'
CutSubtitle1_1_5_a__6 = 'Let it go Dan, and hand over the chest so we can shove off!'
CutSubtitle1_1_5_a__7 = "Well then, I suppose that I've been holding this sea chest for you."
CutSubtitle1_1_5_b__1 = 'Come on open her up.'
CutSubtitle1_1_5_c__1 = 'Oohh, you might want to let her breathe a little.'
CutSubtitle1_1_5_c__2 = 'That scrap of biscuit there is still crawling.'
CutSubtitle1_1_5_c__3 = 'Look straight.\nA pirate keeps all manner of precious things in his sea chest.'
CutSubtitle1_1_5_c__4 = 'But the most important thing is the pirate journal.'
CutSubtitle1_1_5_c__5 = "See pirates is forgetful folk, so they need to keep a reckonin'."
CutSubtitle1_1_5_c__6 = "Now reckon this mate: Get yourself down to the dock\nand find Captain Bo Beck before it's too late."
CutSubtitle1_1_5_c__7 = "I'll put that in the journal for you!"
CutSubtitle1_1_5_c__8 = 'Oh and one more thing, when you see Jack Sparrow again,\ngive him this message...'
CutSubtitle1_1_5_c__9 = 'FROM THE BOTH OF US!!!'
CutSubtitle1_1_5_c__10 = 'Fair winds mate!'
CutSubtitle1_2_a__1 = 'You there, come aboard quickly!'
CutSubtitle1_2_a__2 = 'I was about to shove off without you.'
CutSubtitle1_2_a__3 = "Jolly Roger will be back in a hair's breadth or my name's not Bo Beck."
CutSubtitle1_2_b__1 = 'Risked my neck to fetch Captain Sparrow I did!'
CutSubtitle1_2_b__2 = 'But he most generously requested that\nI take you to Port Royal in his place!'
CutSubtitle1_2_b__3 = 'Now grab a cannon, and keep an eye peeled for trouble.'
CutSubtitle1_3_a__1 = "Hold your fire! It's Jolly Roger,\nand he's got us dead to rights!"
CutSubtitle1_3_a__2 = 'SPAAARROW!!!'
CutSubtitle1_3_a__3 = "Don't worry, I'll handle this."
CutSubtitle1_3_a__4 = "Where's that yellow coward Sparrow? Beck, we had a deal!"
CutSubtitle1_3_a__5 = "But Sparrow paid me double what you was payin'."
CutSubtitle1_3_a__6 = "A pretty piece of profit, too!\nSo, here's your gold back."
CutSubtitle1_3_a__7 = "'Course I was going to reimburse you... as it were."
CutSubtitle1_3_a__8 = 'ah, ha, ha, ha, ha! It looks like the price of loyalty just went up, eh?'
CutSubtitle1_3_a__9 = "What?  Can't take a joke?"
CutSubtitle1_3_a__10 = "Dead men tell no tales! So, I'm forced to let ye live."
CutSubtitle1_3_a__11 = "Just make sure Jack Sparrow knows I'm comin' for him."
CutSubtitle1_3_a__12 = "Said, I'll be lettin' you live\nbut the sharks may not be so charitable..."
CutSubtitle1_3_a__13 = 'What are you waiting for? Sink her!!!!! NOWWWW!!!!'
CutSubtitle2_1_a__1 = "On my word, do as I say or I'll run you through!"
CutSubtitle2_1_a__2 = "Hmmm, unarmed.  Wait, you're Jack's friend."
CutSubtitle2_1_a__3 = 'Please accept my apologies.'
CutSubtitle2_1_a__4 = "There's some gentleman from the\nEast India Trading Company looking for me."
CutSubtitle2_1_a__5 = "Can't be too cautious."
CutSubtitle2_1_a__6 = "Well, you aren't much use unarmed\nwith Jolly Roger's skeleton army on the move!"
CutSubtitle2_1_a__7 = "Here, the blade's a bit rusty... not well balanced,\nbut it should suffice for the present."
CutSubtitle2_1_a__8 = 'Not familiar with the blade?'
CutSubtitle2_1_a__9 = 'That practice dummy will do.'
CutSubtitle2_1_b__1 = "Keep the sword, you'll need it!"
CutSubtitle2_1_b__2 = "But you'll need more than just a cutlass\nif you're to challenge the likes of Jolly Roger."
CutSubtitle2_1_b__3 = 'Tia Dalma has something for you as well.'
CutSubtitle2_1_b__4 = "Go now, it's me they're after."
CutSubtitle2_1_b__5 = "You'll know her by the lantern she carries."
CutSubtitle2_1_b__6 = 'Good luck!'
CutSubtitle2_2__1 = "The claws lie true. There's a touch of destiny in you."
CutSubtitle2_2__2 = 'But know that the skeleton you destroyed\nwas nothing but a drop in the ocean!'
CutSubtitle2_2__3 = "Jolly Roger's servants are many and most be far more dangerous!"
CutSubtitle2_2__4 = 'Look now, from the darkness... comes the light.\nOn one horizon...'
CutSubtitle2_2__5 = "Lord Beckett's deadly assassins, the Black Guard!"
CutSubtitle2_2__6 = "On the other, Jolly Roger's skeleton army."
CutSubtitle2_2__7 = 'Their powers grow! Lord Beckett and Roger!\nNo more, this can be!'
CutSubtitle2_2__8 = 'You must play your part, just as witty Jack will play his part!'
CutSubtitle2_2__9 = 'Now take this, something for you.  Help to find the way, yes.'
CutSubtitle2_2__10 = 'I watch you, when destiny whispers, I will reveal more of the dark arts.'
CutSubtitle2_2__11 = 'But first you must help witty Jack recover his dear Black Pearl.'
CutSubtitle2_2__12 = 'For without the Pearl we all be lost. Go now, hurry!'
CutSubtitle2_3__1 = "Oh, so you're Jack Sparrow's newest prot\xc3\xa9g\xc3\xa9, hmmm?"
CutSubtitle2_3__2 = "Well, I'm afraid dear Jack is in more trouble than he realizes."
CutSubtitle2_3__3 = "Lord Beckett has recruited an army of assassins,\nand there's no parley with Jolly Roger."
CutSubtitle2_3__4 = 'Jack needs our help if he is to take back the Pearl.\nThe Navy has it heavily guarded.'
CutSubtitle2_3__5 = "What's this?  Release orders for the Pearl?"
CutSubtitle2_3__6 = 'I can see why Jack has taken a liking to you!'
CutSubtitle2_3__7 = "But these will do you no good without my father's seal!"
CutSubtitle2_3__8 = "Here, now if the Navy catches you with these orders, there'll be no trial."
CutSubtitle2_3__9 = 'You must leave Port Royal immediately.'
CutSubtitle2_3__10 = "You'll be much safer if you make for Tortuga."
CutSubtitle2_3__11 = "Find Jack, he'll know what to do."
CutSubtitle2_3__12 = "I'd go with you myself, but I am awaiting my father's return,\nand he's long overdue."
CutSubtitle2_3__13 = "I'll arrange a boat for you.  Good luck!"
CutSubtitle2_4_a__1 = "This here's a dark place."
CutSubtitle2_4_a__2 = "You'll need more than that cutlass\nif you're to get out of here with your skin."
CutSubtitle2_4_a__3 = 'Here, take this.\nNow, take aim at the cursed simian over there.'
CutSubtitle2_4_a__4 = 'Prove your mettle with the hand cannon.'
CutSubtitle2_4_b__1 = "Now before ye go blastin' every feckless ingrate in sight,\na word of warning about the code."
CutSubtitle2_4_b__2 = 'The code covers more than just parley.\nIt defines the guidelines of engagement for a pirate.'
CutSubtitle2_4_b__3 = 'I was getting to that, ye mongrel.  This be the part to remember.'
CutSubtitle2_4_b__4 = "There'll be no use of unnecessary force, no shooting other pirates,\nor even Navy swine for that matter."
CutSubtitle2_4_b__5 = "Cheat 'em, steal from 'em, plunder their ships, yes.  But no guns!"
CutSubtitle2_4_b__6 = 'That is, unless you be facing a cursed pirate.'
CutSubtitle2_4_b__7 = "You see, the code don't apply to dead pirates."
CutSubtitle2_4_b__8 = 'So if you want to have a go against your mates,\nbe sure you pick up one of these!'
CutSubtitle2_4_b__9 = 'Now you can blast away at each other all you like!'
CutSubtitle2_4_b__10 = "See, it doesn't hurt a bit!"
CutSubtitle2_5__1 = 'And the buttons popped clear off...'
CutSubtitle2_5__2 = 'and this being Singapore, by custom I had no choice but to-'
CutSubtitle2_5__3 = "You don't happen to have a lovely sister by the name of Ethel, do you?"
CutSubtitle2_5__4 = 'No?  Good, right then!'
CutSubtitle2_5__5 = 'Welcome to Tortuga!  Captain Jack Sparrow at your service.'
CutSubtitle2_5__6 = "And this gentleman who needs no introduction, is...\nWhat's your name again, mate?"
CutSubtitle2_5__7 = 'John! Oh well, uh, James, actually.'
CutSubtitle2_5__8 = 'Right! We were discussing the important matter of my next drink.'
CutSubtitle2_5__9 = 'Is... still there?'
CutSubtitle2_5__10 = "Now I remember!  You're that scrap of flotsam from the jail."
CutSubtitle2_5__11 = 'Come to square up with me for that free trip to Port Royal, eh?'
CutSubtitle2_5__12 = "We're going after the Black Pearl, mate.  Savvy?"
CutSubtitle2_5__13 = 'So go find Joshamee Gibbs and tell him I sent you!'
CutSubtitle2_5__14 = 'Leave a nice tip, mate! Jeremy here pours a spirited spirit.'
CutSubtitle3_1__1 = 'Halt! Who goes there?'
CutSubtitle3_1__2 = "What's this?  Some sort of letter?"
CutSubtitle3_1__3 = 'Looks official.  Let me see that.'
CutSubtitle3_1__4 = "Can't be too careful.  There's pirates about."
CutSubtitle3_1__5 = "Yeah, we're performing a very important duty."
CutSubtitle3_1__6 = 'Guarding the Black Pearl.'
CutSubtitle3_1__7 = "Not just us, really.  In the harbor there that's the Goliath."
CutSubtitle3_1__8 = 'No one gets in or out of this harbor without facing her eighteen guns.'
CutSubtitle3_1__9 = 'A nigh impossible proposition!'
CutSubtitle3_1__10 = "And, we're supposed to keep an eye out for Jack Sparrow."
CutSubtitle3_1__11 = "He won't make fools of us this time."
CutSubtitle3_1__12 = "Make a fool of you, perhaps.\nBut I don't recall a time where I was ever the fool."
CutSubtitle3_1__13 = 'Me a fool?  I was only being generous by including me self in the equation.'
CutSubtitle3_1__14 = "Oh, so you're the generous one now? I was the generous enough\n to not report you for sleeping on duty yesterday evening!"
CutSubtitle3_1__15 = 'I was just resting me eyelids.\nBesides, I was tired from covering your shift Tuesday!'
CutSubtitle3_1__16 = 'You call that covering? When I showed up you were nowhere in sight!'
CutSubtitle3_1__17 = "A man's got to take care of his business now and again..."
CutSubtitle3_2__1 = '...and proceeded to eat his own finger, to which I replied,'
CutSubtitle3_2__2 = "That's not right even if you did know where that finger has been!"
CutSubtitle3_2__3 = 'Ah yes, Master Gibbs tells me you have taken her.\nSo how is she, as beautiful as ever?'
CutSubtitle3_2__4 = "A word of warning mate, once you have had a taste, you'll only want more!"
CutSubtitle3_2__5 = 'Lest you start to covet the Black Pearl for your own, know this.'
CutSubtitle3_2__6 = 'The wind is her true master....'
CutSubtitle3_2__7 = 'Aye.  It is.'
CutSubtitle3_2__8 = 'To control the wind... is to control her destiny!'
CutSubtitle3_2__9 = 'Aye.  It is.'
CutSubtitle3_2__10 = 'And there is a way... to control the wind.'
CutSubtitle3_2__11 = 'Aye.  There is?'
CutSubtitle3_2__12 = "Don't take my word for it.\nIt's written in stone on a thing called the Headstone."
CutSubtitle3_2__13 = "The Headstone! We're not going back there again, are we?"
CutSubtitle3_2__14 = "You've done well so far.  And this is for your efforts..."
CutSubtitle3_2__15 = 'But, help me find the Headstone and I promise it will be worth your while!'
CutSubtitle3_2__16 = 'The catch is no map will lead you to it.'
CutSubtitle3_2__17 = 'But I happen to know where it is buried... Padres!'
CutSubtitle3_2__18 = 'Padres, del Fuego!  You know, the volcano.\nLava natives chanting. Headstone thrown in it.'
CutSubtitle3_2__19 = 'Rough place, Padres! Very shaky.'
CutSubtitle3_2__20 = 'Go there at once.'
CutSubtitle3_2__21 = "We wouldn't want to lose this prize to our dear friends in the Royal Navy."
CutSubtitle3_2__22 = 'I am told they are on the hunt already.'
CutSubtitle3_2__23 = 'When you get there, find Valentina.  She might know where to start looking.'
CutSubtitle3_2__24 = 'And I will meet up with you as soon as Master Gibbs here can ready the crew!'
CutSubtitle6_1__1 = 'I been watching you...'
CutSubtitle6_1__2 = '... still, you have much to learn.'
CutSubtitle6_1__3 = 'I will show you the way of the dark arts...'
CutSubtitle6_1__4 = 'We begin with a trifle...'
CutSubtitle6_1__5 = 'Look upon it!'
CutSubtitle6_1__6 = 'The learning of the doll be in the learning of its construction...'
CutSubtitle6_1__7 = 'each must make their own.'
CutSubtitle6_1__8 = 'We have much work to do.'
ProgressBlockPopupDialog = {
    'c3visitJoshamee': 'Congratulations! You have reached the start of the next Story Quest. Only players with full access may continue beyond this point. To become a full access member visit www.piratesonline.com and subscribe.',
    'c3r2.6visitCarver': 'Congratulations! You have recruited 5 crew members for the Black Pearl and have given Gibbs a clue as to where she is being held by the Navy. Only players with full access may continue beyond this point. To become a full access member visit www.piratesonline.com and subscribe.',
    'c4.1visitValentina': 'Story Quest Complete!'
}
__NavyAggro = [
    'Halt!', 'Halt!', 'Who goes there!?', 'This area is off limits!', 'Over there!', 'You are under arrest!', 'Surrender!', "It's that pirate again!", 'A pirate!', 'What are you doing here!?'
]
__NavyTaunt = [
    "It'll be the gallows for you, pirate!", 'You have a morning appointment with the gallows, pirate!', 'Drop your weapons!', "You're the one who escaped from our jail!", "You don't stand a chance!", 'Not so tough now, eh!?', "It's back to jail for you!"
]
__NavyTeamTalk = [
    'Hold your fire! We want that pirate alive!', "You're outnumbered! Surrender!", 'We have you surrounded!', 'Capture that pirate!', 'Take that pirate alive for questioning!'
]
__NavyBreakCombat = [
    "That is by far the worst pirate I've ever met.", 'Coward!', 'Running away again eh!?', 'Come back here and fight!', 'That coward ran away!', 'Bloody pirate!', 'Accursed pirate!', 'I better alert the watch.'
]

def getNavyAggroPhrase():
    dialogue = random.choice(__NavyAggro)
    return dialogue


def getNavyTauntPhrase():
    dialogue = random.choice(__NavyTaunt)
    return dialogue


def getNavyTeamTalkPhrase():
    dialogue = random.choice(__NavyTeamTalk)
    return dialogue


def getNavyBreakCombatPhrase():
    dialogue = random.choice(__NavyBreakCombat)
    return dialogue


__GhostAggro = [
    'You do not belong here!', 'So cold...', 'Are you a spirit?', 'I smell fear!'
]
__GhostTaunt = [
    'Join us!', 'You belong with us!', 'We will catch you!', 'I hunger'
]

def getGhostAggroPhrase():
    dialogue = random.choice(__GhostAggro)
    return dialogue


def getGhostTauntPhrase():
    dialogue = random.choice(__GhostTaunt)
    return dialogue


__UndeadAggro = [
    'An intruder!', 'Trespasser!', 'After that pirate!', 'Take no prisoners!', 'Leave no one alive!', 'Death cannot stop us!'
]
__UndeadTaunt = [
    'Jolly Roger will be pleased!', 'Death comes for ye, pirate!', 'Yer finished, pirate!', "See ye in Davy Jones's locker!", 'Ye fight like a dog!'
]
__UndeadTeamTalk = [
    'We outnumber ye, pirate!', 'Ye cannot defeat us all, pirate!', 'Fool! We outnumber ye!'
]
__UndeadBreakCombat = [
    'Weakling!', 'A waste of time!', 'Ye cannot escape us forever!', 'Ye cannot hide from us!', 'Wherever ye go, we will find ye!', 'Ye run like a dog!', 'Ye call yerself a pirate!'
]

def getUndeadAggroPhrase():
    dialogue = random.choice(__UndeadAggro)
    return dialogue


def getUndeadTauntPhrase():
    dialogue = random.choice(__UndeadTaunt)
    return dialogue


def getUndeadTeamTalkPhrase():
    dialogue = random.choice(__UndeadTeamTalk)
    return dialogue


def getUndeadBreakCombatPhrase():
    dialogue = random.choice(__UndeadBreakCombat)
    return dialogue


__EITCAggro = [
    'An intruder!', 'Halt!', "There's that pirate!", 'What have we here?', 'Surrender!', 'Mind your own business, pirate!', "Don't meddle in our affairs!", 'You will regret crossing swords with us, pirate!'
]
__EITCTaunt = [
    "You don't stand a chance! Surrender!", 'Lord Beckett will reward us well for this!', 'You are no match for us!', 'Any last words, pirate?', 'There is no escape!', "It's time to finish you off!", 'This is the last mistake you make with us, pirate!'
]
__EITCTeamTalk = [
    "You're outnumbered! Surrender!", 'We have you surrounded!', 'Give it up! We outnumber you!', "Don't let that pirate escape!", 'Take that pirate alive for questioning!'
]
__EITCBreakCombat = [
    'Bloody pirate!', 'That coward ran away.', 'I grow tired of this.', "Let's head him off.", 'Alert the watch!'
]
UndeadPokerCommentLose1 = "Luck of the living! But you'll be one of us eventually."
UndeadPokerCommentLose2 = "Blasted Mortal! You'll give those coins to the boatman!"
UndeadPokerCommentLose3 = 'Quit while you still have a head!'
UndeadPokerCommentLose4 = "You can't cheat death forever."
UndeadPokerCommentWin1 = 'This game will be your death.'
UndeadPokerCommentWin2 = 'Lose your gold... lose your life'
UndeadPokerCommentWin3 = 'Your life runs out with your luck!'
UndeadPokerCommentWin4 = 'Pay your debts in blood.'
UndeadPokerCommentLose = ['UndeadPokerCommentLose1', 'UndeadPokerCommentLose2', 'UndeadPokerCommentLose3', 'UndeadPokerCommentLose4']
UndeadPokerCommentWin = [
    'UndeadPokerCommentWin1', 'UndeadPokerCommentWin2', 'UndeadPokerCommentWin3', 'UndeadPokerCommentWin4'
]
UndeadPokerCommentExit = [
    'Run away and forfeit your winnings', 'There is a penalty for running away'
]
UndeadPokerCommentQuestComplete = [
    'The Clubhearts got their blasted gold back!'
]
UndeadPokerCommentQuestBonusComplete = [
    "You've cleaned us out. How can we live with the shame? Oh wait we're dead."
]
UndeadPokerNPCNames = [
    'Oldbones McGill', 'Jolly Robert', 'Paul T Geist', 'Doc Skull', 'Juan Esqueleto', 'Slim Pickins', 'Mortimer Late', 'Than Boatman', 'Justin Mortis', 'Rotten Rob'
]

def pickPokerUndeadName(choices = []):
    if not choices:
        choices = UndeadPokerNPCNames
    return (random.choice(choices), copy.copy(choices))


def getEITCAggroPhrase():
    dialogue = random.choice(__EITCAggro)
    return dialogue


def getEITCTauntPhrase():
    dialogue = random.choice(__EITCTaunt)
    return dialogue


def getEITCTeamTalkPhrase():
    dialogue = random.choice(__EITCTeamTalk)
    return dialogue


def getEITCBreakCombatPhrase():
    dialogue = random.choice(__EITCBreakCombat)
    return dialogue


__DavyJonesGuysAggro = [
    'Take no prisoners!', 'Leave no one alive!', "You don't belong here.", 'Part of the ship... Part of the crew...', 'We belong to the Flying Dutchman!', 'We serve Davy Jones!'
]
__DavyJonesGuysTaunt = [
    'Davy Jones will be pleased!', 'Do you fear death, pirate!', "See ye in Davy Jones's locker!"
]
__DavyJonesGuysTeamTalk = [
    'We outnumber ye, pirate!', 'Ye cannot stop Davy Jones, pirate!', 'Ye cannot defeat us all, pirate!'
]
__DavyJonesGuysBreakCombat = [
    'Ye cannot escape us forever!', 'Ye cannot hide from us!', 'No one can escape Davy Jones!'
]

def getDavyJonesGuysAggroPhrase():
    dialogue = random.choice(__DavyJonesGuysAggro)
    return dialogue


def getDavyJonesGuysTauntPhrase():
    dialogue = random.choice(__DavyJonesGuysTaunt)
    return dialogue


def getDavyJonesGuysTeamTalkPhrase():
    dialogue = random.choice(__DavyJonesGuysTeamTalk)
    return dialogue


def getDavyJonesGuysBreakCombatPhrase():
    dialogue = random.choice(__DavyJonesGuysBreakCombat)
    return dialogue


RammingSpeed = 'Ramming Speed!!!'
__LeftBroadside = [
    'Broadside port!!!'
]
__RightBroadside = [
    'Broadside starboard!!!'
]
__FullSail = [
    'Full speed ahead!', 'Full sail!'
]
__ComeAbout = [
    "Let's turn her around!", 'Prepare tacking maneuver!'
]
__OpenFire = [
    'Now! Open fire!!!', 'Shoot! Open fire!!!', "Let 'em have it! Open fire!!!"
]
__TakeCover = [
    "She's gonna broadside! Take cover!!!", 'Incoming! Take cover!!!', "We're being fired on! Take cover!!!"
]
__PowerRecharge = [
    'To the cannons!!!', "Let's rule the ocean!", "Sink 'em all!!"
]
__WreckHull = [
    'Wreck the hull!!!'
]
__WreckMasts = [
    'Wreck the masts!!!'
]
__SinkHer = [
    'Sink her!!!'
]
__Incoming = [
    'Incoming!!!'
]
__FixItNow = [
    'Fix it now!!!'
]
__Taunt = [
    'Hey! Over here!'
]
__NotInFace = [
    'Not in the face!'
]

def getLeftBroadsidePhrase():
    dialogue = random.choice(__LeftBroadside)
    return dialogue


def getRightBroadsidePhrase():
    dialogue = random.choice(__RightBroadside)
    return dialogue


def getFullSailPhrase():
    dialogue = random.choice(__FullSail)
    return dialogue


def getComeAboutPhrase():
    dialogue = random.choice(__ComeAbout)
    return dialogue


def getOpenFirePhrase():
    dialogue = random.choice(__OpenFire)
    return dialogue


def getTakeCoverPhrase():
    dialogue = random.choice(__TakeCover)
    return dialogue


def getPowerRechargePhrase():
    dialogue = random.choice(__PowerRecharge)
    return dialogue


def getWreckHullPhrase():
    dialogue = random.choice(__WreckHull)
    return dialogue


def getWreckMastsPhrase():
    dialogue = random.choice(__WreckMasts)
    return dialogue


def getSinkHerPhrase():
    dialogue = random.choice(__SinkHer)
    return dialogue


def getIncomingPhrase():
    dialogue = random.choice(__Incoming)
    return dialogue


def getFixItNowPhrase():
    dialogue = random.choice(__FixItNow)
    return dialogue


def getTauntPhrase():
    dialogue = random.choice(__Taunt)
    return dialogue


def getNotInFacePhrase():
    dialogue = random.choice(__NotInFace)
    return dialogue


FriendsPageTitle = 'Friends'
FriendInviterTitle = 'Invite Friend'
FriendInviterRemove = 'Remove Friend'
FriendInviteeTitle = 'Friend Invitation'
IgnoreConfirmTitle = 'Ignore Confirm'
FriendInviterTooMany = 'Your friends list is full.\n\nYou will need to remove some other friends if you want to invite \x01gold\x01%s\x02.'
FriendInviterAskingNPC = 'Asking %s to be your friend.'
FriendInviterTitle = 'Invite Friend'
FriendInviteIgnorePirate = 'Ingore Invites\n from this Pirate'
FriendInviteIgnorePlayer = 'Ingore Invites\n from this Player'
GuildPageTitle = 'Guild'
GuildPageCreateGuild = 'Create Guild'
GuildPageLeaveGuild = 'Leave Guild'
GuildPageRevertGui = 'Guild Options'
GuildPageNameGuild = 'Request Name'
GuildPageShowMembers = 'Show Members'
GuildCodeOptions = 'Invitation Options'
GuildDefaultName = 'Pirate Guild %d'
GuildNoGuild = 'No Guild'
GuildAskLeave = 'Leave Guild?'
GuildAskLeaveGM = 'You may not leave your guild without a Guildmaster.\n\nEither make someone else the Guildmaster or remove everyone else first.'
GuildAskCreate = 'Create New Guild?'
GuildInvite = 'Create Invitation'
GuildInviteeTitle = 'Guild Invitation'
GuildInviterTitle = 'Guild Invite'
GuildInviteeIgnore = 'Ignore all guild\ninvites until logout'
GuildInviterAskingNPC = 'Inviting %s to join your guild.'
GuildRedeemInvite = 'Redeem Invitation'
GuildAbout = 'About Guilds'
GuildNotifyTokenCreatorOfRedeem = '%s has redeemed a guild token, and is now a member of your guild.'
GuildEMailInvite = 'E-Mail'
GuildNameRequest = "Your guild name was submitted for approval. Please wait a few days for us to get back to you! In the meantime, fair winds and good plunderin'!"
GuildNameApprove = 'Your guild name:\n\n\x01guildName\x01\x01larger\x01%s\x02\x02\n\nwas approved!'
GuildNameApproveTitle = 'Congratulations!'
GuildNameReject = 'Your desired guild name:\n\n"\x01guildName\x01\x01larger\x01%s\x02\x02"\n\nwas rejected.\n\nPlease select another.'
GuildNameRejectTitle = 'Sorry!'
GuildNameDuplicate = 'Desired guild name is already in use.  Please select another.'
GuildKicksMaxed = 'Officers are only allowed to remove five guild members per day.'
GuildInviteResponse = 'Please make note of this code and select a code type'
GuildInviteJoinSucessful = "You're now a member of %s"
GuildInviteTooManyTokens = 'You have too many invite codes pending. Please have your friends redeem them, or wait until they expire.'
GuildInviteSingleButton = 'Single Use Invite'
GuildInviteLimitedButton = 'Multiple Use Invite'
GuildInviteUnlimitedButton = 'Unlimited Use Invite'
GuildManageInvite = 'Token Management'
GuildAboutTokenManagement = 'About Code Management'
GuildClearPerm = 'Clear Unlimited Invite'
GuildClearLimUse = 'Clear Limited Use Invites'
GuildSuspendPerm = 'Suspend Unlimited Invite'
GuildNotificationOptions = 'Notification Options'
GuildTokenAbout = 'About Guild Token Management'
GuildTokenMenuToMembers = 'Show Members'
GuildPermCodeLabel = 'Unlimited Invite Code'
GuildNoPermInviteCodeSet = 'None Set'
GuildMessageClearPermInvite = 'Delete your unlimited use invite code?'
GuildMessageClearLimInvite = 'Delete all active limited use invite codes?'
GuildTokenTut = ('If you have generated an unlimited use invite code, it will be displayed at the top of the panel.', 'Unlimited use invite codes can be deleted by clicking the Clear Unlimited Invite button. Limited use codes (single use and limited multi use) can be deleted by clicking the Clear Limited Use Invites button.')
GuildTut = ('Guilds are useful for grouping with other pirates and staying grouped with them even after you log out.', 'If you are a basic member, you may join a guild by invite.  If you are an unlimited member, you can start your own guild by pressing the Create Guild button.', 'To invite a pirate to your new guild, just click on them and select Guild from the menu. If they are not currently online, click the Create Invitation button to generate a code that can be redeemed for membership in your guild. Give the code to your friend, they can then join your guild via the Redeem Invitation button.', 'Three types of invite codes exist:\n\nSingle Use : Good for one redemption\n\nLimited Multi Use: Redeemable up to the number of times selected\n\nUnlimited Use: Unlimited Redemptions', 'As Guildmaster, you can promote other members to Officer and allow them to invite others into the guild.')
SocialPanelHelpTitle = 'Social Panel Help'
SocialPanelHelpContents = ('The social panel is where you can access and manage your Friends, Crew, and Guild.', 'Friends:\n\nTo make Friends, click on the Pirate you would like to make Friends with. Their Pirate Detail Panel will open. Click Friendship.\n\nYou will get a pop-up that says "Asking (Pirate Name) to be your friend. "Sometime later you get a "You are now friends with (Pirate Name)!" or "(Pirate Name) said no, thank you."', 'Friends:\n\nAll your Friends appear on your Friends Panel, along with a note telling you if they are currently online or not. You can have up to 300 Friends.', 'Crew:\n\nInviting someone to your Crew is very similar to making a Friend. Simply click on the Pirate you would like to invite to join your Crew. Their Pirate Detail Panel will open. Click Crew.\nYou will get a pop-up that says "Would you like to invite (Pirate Name) to join your crew? "Sometime later you get a "(Pirate Name) has joined your crew!" or "(Pirate Name) declined your crew invitation."', 'Crew:\n\nAll Crew members will appear on your Crew Panel. Unlike Friends and Guilds, Crews are not persistent between sessions. You can have up to 8 members in your Crew.', 'Guilds:\n\nGuilds are useful for grouping with other pirates and staying grouped with them even after you log out. If you are a basic member, you may join a guild by invite. If you are an unlimited member, you can start your own guild by pressing the Create Guild button.', 'Guilds:\n\nTo invite a pirate to your new guild, just click on them and select Guild from the menu. If they are not currently online, click the Create Invitation button to generate a code that can be redeemed for membership in your guild. Give the code to your friend, they can then join your guild via the Redeem Invitation button.', 'Guilds:\n\nThree types of invite codes exist:\n\nSingle Use : Good for one redemption\n\nLimited Multi Use: Redeemable up to the number of times selected\n\nUnlimited Use: Unlimited Redemptions', 'Guilds:\n\nAs Guildmaster, you can promote other members to Officer and allow them to invite others into the guild.')
TeleportConfirmTitle = 'Confirm Teleport'
TeleportConfirmMessage = 'Would you like to go to %s?'
TeleportConfirmOK = lOk
TeleportConfirmNo = lNo
TeleportToPlayerFailMessage = 'Could not successfully complete teleport because the pirate you were going to became unavailable.'
TeleportToGoneShipFailMessage = 'Could not successfully complete teleport because the ship you were going to became unavailable.'
TeleportToBoardingShipFailMessage = 'Could not successfully complete teleport because the ship you were going to is engaged in a flagship battle.'
TeleportGenericFailMessage = 'There was a problem with going to your destination.'
GenericConfirmOK = lOk
GenericConfirmNo = lNo
GenericConfirmNext = 'Next'
GenericConfirmDone = 'Done'
GenericConfirmCancel = 'Cancel'
CrewPageTitle = 'Crew'
CrewPageLeaveCrew = 'Leave Crew'
CrewOptions = 'Crew Options'
CrewList = 'Crew List'
CrewLookingForButton = 'Toggle Crew\nMatching'
CrewLookingForAd = 'Looking for Crew'
CrewLookingForOptionsButton = 'Crew Matching Options'
CrewIconButton = 'Toggle Crew Icon'
CrewIconTitle = 'Crew Icon Selection'
CrewClearIconButton = 'Clear Crew Icon'
CrewStartACrewButton = 'Start a Crew'
CrewBoardingAccessButton = 'Boarding Access'
CrewBoardingAccessAllowCrew = 'Allow Crew'
CrewBoardingAccessAllowFriends = 'Allow Friends'
CrewBoardingAccessAllowGuild = 'Allow Guild'
CrewBoardingAccessAllowPublic = 'Allow Public'
CrewBordingAccessBack = 'Back'
CrewBootTeleport = '\x01gold\x01%s\x02 has booted you from the ship. You are being transported back to your home island.'
CrewBootSuccess = '\x01gold\x01%s\x02 has been booted from your ship.'
CrewInviteeTitle = 'Crew Invitation'
CrewInviteeTooManyCrewed = '\x01gold\x01%s\x02 would like to be in your crew, but your crew is full!'
CrewInviteeInvitation = 'Would you like to join the crew of %s?'
CrewInviteeOK = lOk
CrewInviteeNo = lNo
CrewRejoinTitle = 'Rejoin Your Crew?'
CrewRejoinTooManyCrewed = '\x01gold\x01%s\x02 would like to be in your crew, but your crew is full!'
CrewRejoinInvitation = 'You seem to have been disconnected. Would you like to rejoin your crew?'
CrewRejoinPVPInvitation = 'Welcome back from Pirate vs. Pirate. Would you like to rejoin your crew?'
CrewRejoinParlorInvitation = 'Welcome back from Parlor Games. Would you like to rejoin your crew?'
CrewRejoinOK = lYes
CrewRejoinNo = lNo
CrewBootTitle = 'Boot Member?'
CrewBootMessage = 'Are you sure you want to boot \x01gold\x01%s\x02 from your ship?'
CrewBootOK = lYes
CrewBootNo = lNo
LeaveCrewWarningTitle = 'Leave Your Crew?'
LeaveCrewWarningMessage = 'Moving to a new server will cause you to leave your crew. Are you sure you want to continue?'
LeaveCrewWarningOK = lYes
LeaveCrewWarningNo = lNo
CrewInviterTitle = 'Invite Crew'
CrewInviterRemove = 'Remove Crew'
CrewInviterOK = lOk
CrewInviterCancel = lCancel
CrewInviterStopBeingCrewed = 'Remove'
CrewInviterYes = lYes
CrewInviterNo = lNo
CrewInviterTooMany = 'Your crew is full.\n\nYou will need to remove some crew members if you want to invite \x01gold\x01%s\x02.'
CrewInviterNotYet = 'Would you like to invite \x01gold\x01%s\x02 to join your crew?'
CrewInviterCheckAvailability = 'Seeing if %s is available.'
CrewInviterNotAvailable = '\x01gold\x01%s\x02 is busy right now; try again later.'
CrewInviterWentAway = '\x01gold\x01%s\x02 went away.'
CrewInviterAlready = '\x01gold\x01%s\x02 is already in your crew.'
CrewInviterAlreadyInvited = '\x01gold\x01%s\x02 has already been invited.'
CrewInviterRecentlyInvited = '\x01gold\x01%s\x02 has recently been invited to join your crew. Please wait a while before sending another invite.'
CrewInviterAskingNPC = 'Asking \x01gold\x01%s\x02 to join your crew.'
CrewInviterEndCrewship = 'Are you sure you want to kick \x01gold\x01%s\x02 out of your crew?'
CrewInviterCrewedNoMore = '\x01gold\x01%s\x02 is no longer in your crew.'
CrewInviterSelf = 'You are already in your own crew!'
CrewInviterLeave = 'Are you sure you want to leave your crew?'
CrewInviterLeft = 'You left the crew.'
CrewInviterIgnored = '\x01gold\x01%s\x02 is ignoring you.'
CrewInviterAsking = 'Asking %s to join your crew.'
CrewInviterCrewSaidYes = '%s has joined your crew!'
CrewInviterCrewSaidNo = '%s declined your crew invitation.'
CrewInviterCrewSaidNoNewCrews = '\x01gold\x01%s\x02 is not looking for a new crew right now.'
CrewInviterOtherTooMany = '\x01gold\x01%s\x02 has too many crew members already!'
CrewInviterMaybe = '\x01gold\x01%s\x02 was unable to answer.'
CrewInviterDown = 'Cannot join crews now.'
CrewInviterInOtherCrew = 'Sorry \x01gold\x01%s\x02 is in a different crew.'
CrewInviterNotCaption = 'Sorry you are not the caption of your crew.'
CrewInviterNotCaption1 = 'Sorry only \x01gold\x01%s\x02 can invite new crew members.'
CrewMatchInviteeInvitation = 'Would you like to join the crew of %s?\nThey are currently located in \x01gold\x01%s\x02.'
CrewMatchInviteeInvitationNoLocation = 'Would you like to join the crew of \x01gold\x01%s\x02?'
CrewMatchCrewFound = 'Crew Found'
CrewMatchCrewLookout = 'Crew Lookout'
CrewMatchNoCrewFound = 'Crew Matching is now active. Unfortunately, a crew could not be found. The search will continue.'
CrewMatchNoCrewFoundPVP = 'Privateering Crew Matching is now active. Unfortunately, a crew could not be found. The search will continue.'
CrewMatchRecruitButton = 'Recruit Crewmates'
CrewMatchJoinCrewButton = 'Find a Crew'
CrewMatchJoinPVPCrewButton = 'Find a Privateer Crew'
CrewMatchInviterText = 'Please select the notoriety range for the pirates you wish to recruit:'
CrewMatchCrewNowUnavailable = 'Sorry, the crew you just tried to join is now unavailable. Your crew search will continue.'
CrewMatchRemoveAvatarFromLookout = 'Crew Matching has been deactivated'
CrewMatchRemoveAvatarFromLookoutPVP = 'Privateering Crew Matching has been deactivated'
CrewMatchEnabledForCrew = 'Crew Matching has been activated for your crew. You will be notified of new recruits that want to join your crew.'
CrewMatchEnabledForCrewPVP = 'Privateering Crew Matching has been activated for your crew. You will be notified of new recruits that want to join your crew.'
CrewMatchAdvancedOptionsButton = 'Advanced Options'
CrewMatchCancelButton = 'Cancel'
CrewMatchAdvancedNotorietyRange = 'Notoriety Range:'
CrewMatchAdvancedMinSailSkillLevel = 'Minimum Sailing Level:'
CrewMatchAdvancedMinCannonSkillLevel = 'Minimum Cannon Level:'
CrewMatchAdvancedText = 'Advanced Options'
CrewMatchSimpleOptionsButton = 'Basic Options'
CrewMatchAvatarAddedToYourCrew = 'Crew Matching has added %s to your crew.'
CrewMatchRangeIndicator = 'Range +/- %s Levels'
CrewMatchLevelIndicator = 'Level %s'
CrewMatchEmptyName = 'Pirate'
CrewMatchAskingCrewLeader = 'Asking %s to join the crew.'
CrewMatchAccept = '%s has accepted you into the crew.'
CrewMatchDecline = '%s has decided not to let you into the crew.'
CrewMatchTeleport = "You are now being teleported to %s's ship."
CrewMatchTeleportShard = "You are now being teleported to %s's server."
CrewMatchStartCrewDeactivated = 'Crew Matching has been deactivated. You are no longer starting a crew.'
CrewMatchDeactivated = 'Crew Matching has been deactivated.'
CrewMatchCrewGone = 'Sorry, the crew you were invited to is now unavailable. Your crew search will continue.'
CrewMatchNewMemberRequestTitle = 'Crew Matching'
CrewMatchNewMemberRequestMessage = '%s would like to join your crew.'
CrewMatchNewMemberRequestYes = lYes
CrewMatchNewMemberRequestNo = lNo
PrivateerAllTeamsFull = 'Both Privateer teams are full!\n\nYou can join another server or an existing Privateer crew.\n\nDo you wish to join an existing Privateer crew?'
PrivateerSingleTeamFull = 'Sorry, this Privateer team is full!\n\nDo you wish to balance out the battle and join the opposition?'
CrewHUDNoCrew = 'No Crew Bonus'
CrewHUDCrewNearBy = 'Crew: \x01yellow\x01%s%%\x02 Bonus!'
CrewHUDCrewPanelButton = 'Toggle Crew HUD'
CrewHUDDisconnect = '\x01slant\x01Disconnected\x02'
CrewHUDRequest = '\x01slant\x01Crew Request\x02'
CrewHUDPVP = '\x01slant\x01In PVP Match\x02'
CrewHUDParlor = '\x01slant\x01In Parlor Game\x02'
CrewHUDAFK = 'AFK'
CrewHUDPrivFrench = 'Privateering\nFrench Team'
CrewHUDPrivSpanish = 'Privateering\nSpanish Team'
CrewHUDLeader = 'Crew Leader'
TradePanelTitle = 'Trade'
TradeInviterTitle = 'Invite Trade'
TradeInviterOK = lOk
TradeInviterCancel = lCancel
TradeInviterStopTrading = 'Stop'
TradeInviterYes = lYes
TradeInviterNo = lNo
TradeInviterClickToon = 'Click on the toon you would like to trade with.'
TradeInviterNotYet = 'Would you like to trade with %s?'
TradeInviterCheckAvailability = 'Seeing if %s is available.'
TradeInviterNotAvailable = '%s is busy right now; try again later.'
TradeInviterWentAway = '%s went away.'
TradeInviterAlready = '%s is already trading.'
TradeInviterAlreadyInvited = '%s has already been invited to trade.'
TradeInviterAskingNPC = 'Asking %s to trade.'
TradeInviterEndTrade = 'Are you sure you want to stop trading with %s?'
TradeInviterTradeNoMore = '%s is no longer trading.'
TradeInviterSelf = 'You cannot trade with yourself!'
TradeInviterIgnored = '%s is ignoring you.'
TradeInviterAsking = 'Asking %s to trade with you.'
TradeInviterTradeSaidYes = '%s said yes!'
TradeInviterTradeSaidNo = '%s said no, thank you.'
TradeInviterTradeSaidNoNewTrades = '%s is not interested in trades right now.'
TradeInviterMaybe = '%s was unable to answer.'
TradeInviterDown = 'Cannot trade now.'
PVPInviterTitle = 'Challenge to Skirmish'
PVPInviterBusy = '%s is busy'
PVPInviterNotYet = 'Would you like to issue a Challenge to %s and crew? Your crew members will also be invited.'
PVPInviterCheckAvailability = 'Checking if %s is available for the Challenge...'
PVPInviterEndChallenge = 'Cancel challenge with %s?'
PVPInviterNoMore = 'Removing Challenge with %s.'
PVPInviterNoMore = 'You cannot fight with yourself.'
PVPInviterAsking = 'Issuing Challenge to %s.'
PVPInviterAskingNPC = 'Challenging %s to a battle...'
PVPInviterSaidYes = '%s accepted your Challenge!'
PVPInviterSaidNo = '%s declined your Challenge!'
PVPInviterMaybe = "%s didn't bother to answer."
PVPInviterDown = 'Cannot Challenge right now.'
PVPInviterSelf = 'You cannot Challenge yourself to a fight.'
PVPInviteeTitle = 'Skirmish Invitation'
PVPInviteeInvitation = '%s is issuing you a Challenge!'
PVPRulesPanelPlay = 'PLAY'
PVPDefaultTitle = 'Skirmish'
PVPDefaultInstructions = 'Find treasure chests and bring them back to your fort. First crew to amass 200 gold wins.'
PVPPanelTitle = 'Game Score'
SiegePanelTitle = 'Ship PVP High Scores'
PVPPickUpTreasure = 'Press %s to pick up treasure' % InteractKey
PVPStealTreasure = 'Press %s to steal treasure' % InteractKey
PirateerDeckTreasure = 'Sail me to your base to unload me!'
PVPReplay = 'Replay Match'
PVPExit = 'Exit Match'
PVPStatDetail = 'View Details'
PVPStatSummary = 'View Summary'
PVPGoldAbbrev = 'g'
PVPUnknownValue = '??'
PVPTeam = 'Team %s: '
PVPYourTeam = 'Your Team: '
PVPOtherTeam = 'Other Team: '
PVPYourShip = 'Your Ship: '
PVPOtherShip = 'Other Ship: '
PVPYouCarry = 'You are carrying '
PVPYourScoreIs = 'Your score is '
PVPCompleteTitle = 'Game Complete'
PVPResult = 'Match Result: '
PVPTied = 'Tied...'
PVPWon = 'Won!'
PVPTeamWon = 'Team %s Wins!'
PVPPlayerWon = 'You Win!'
PVPPlayerLost = 'You Lost.'
PVPTeamName = 'Team %s'
PVPTeamScore = 'Team %s Score: %s'
PVPTeamTotal = 'Total'
PVPYourScore = "Your Team's Gold"
PVPOtherScore = "Other Team's Gold"
PVPLootStolen = 'Gold Stolen'
PVPLootDeposit = 'Gold Deposited'
PVPLootDropped = 'Gold Dropped'
PVPEnemiesDefeated = 'Enemies Defeated'
PVPTimesDefeated = 'Times Defeated'
PVPScore = 'Score'
PVPBounty = 'Bounty'
PVPTime = 'Total Time'
PVPRating = 'Rating'
PVPYourRank = 'You ranked #'
PVPYourTeamRank = 'Your team ranked #'
PVPPlayer = 'Player'
PVPShip = 'Ship Name'
PVPTeamFull = 'Sorry, you cannot launch your boat because this Privateer team has enough boats--for the moment. Please try again later.'
PVPSeaRankDecreaseMessage = 'Yarrr PVP Sea Rank has decreased from %s to %s, as the stories of your exploits faded.'
PVPLandRankDecreaseMessage = 'Yarrr PVP Land Rank has decreased from %s to %s, as the stories of your exploits faded.'
_pvpRating = {
    0: 'Landlubber',
    10: 'Swabbie',
    20: 'Deck Hand',
    30: 'Old Salt',
    40: 'Mate',
    50: 'Sea Dog',
    60: 'Swarthy',
    70: 'Leatherneck'
}
PVPTitleLandRanks = {
    0: 'No Rank',
    1: 'Rookie',
    2: 'Brawler',
    3: 'Duelist',
    4: 'Buccaneer',
    5: 'Swashbuckler',
    6: 'War Dog',
    7: 'War Master'
}
PVPTitleSeaRanks = {
    0: 'No Rank',
    1: 'Mariner',
    2: 'Lieutenant',
    3: 'Commander',
    4: 'Captain',
    5: 'Commodore',
    6: 'Vice Admiral',
    7: 'Admiral'
}
FounderTitleRanks = {
    0: None,
    1: 'Founder'
}
PVPTitleLandName = 'PvP Title'
PVPTitleSeaName = 'Privateering Title'
FounderTitleName = 'Founder Title'
PVPInfamy = 'Infamy'
PVPInfamySea = 'Infamy'
PVPInfamyLand = 'Infamy'
PVPSalvage = 'Salvage'
PVPInfamySpendable = 'Bounty'
PVPPrivateeringTitle = 'Privateering Infamy'
PVPLandTitle = 'PvP Infamy'
PVPMessageKill = 'You received %s infamy for landing the final blow on %s'
PVPMessageDamage = 'You received %s infamy for doing the most damage to %s'
PVPTitleSeaDesc = 'Ship Privateering Infamy'
PVPTitleLandDesc = 'Land Combat Infamy'
FounderTitleDesc = 'Founding Pirate for the Caribbean'
NoTitle = 'No Title'
TitlesTitle = 'Achievements'
DisplayTitle = 'Select the badges you want to display\n\nNote: Infamy decreases during days you do not play.'
DisplayTitleFree = 'Become a member to display your badges to other pirates!\n\nNote: Infamy decreases during days you do not play.'
DisplayTitleLand = 'Pirate\nNametag'
DisplayTitleSea = 'Ship\nNametag'
TitleOn = 'On'
TitleOff = 'Off'
import random

def getPVPRating(score):
    return random.choice(_pvpRating.values())


PirateerTitle = 'Dubloon Lagoon'
PirateerInstructions = 'Bring all the treasures to your base to win! But remember only merchant ships can haul treasure.'
PVPTeamBattleInstructions = 'Arrr matey, this be an all-out battle. The team that defeats the most opponents wins.'
PVPShipBattleInstructions = 'Arrr matey, this be an all-out battle at sea. The last team afloat wins.'
PVPBattleInstructions = 'Arrr matey, this be an all-out battle. Every man for himself! The pirate that defeats the most opponents wins.'
PVPDefeat = '%(defeater)s defeated %(defeated)s!'
PVPYouDefeated = 'You defeated %(defeated)s!'
PVPYouWereDefeated = 'You were defeated by %(defeater)s!'
PVPSuicide = '%(defeated)s was clumsy with his grenade!'
PVPYouSuicide = 'You were defeated by your own grenade!'
PVPSinkStreak1 = 'Sink Streak!'
PVPSinkStreak2 = 'Unstoppable!'
PVPSinkStreak3 = 'Sink Rampage!'
PVPTeam1name = 'French'
PVPTeam2name = 'Spanish'
PVPSinkAnnouncement = 'The %(shipName)s (%(teamName)s) sank the %(sunkShipName)s (%(sunkTeamName)s)!'
PVPSinkWithAssistAnnouncement = 'The %(shipName)s (%(teamName)s) and the %(assistShipName)s (%(assistTeamName)s) sank the %(sunkShipName)s (%(sunkTeamName)s)!'
PVPSinkStreakAnnouncement = 'The %(shipName)s (%(teamName)s) sank %(amount)s ships in a row!'
LookoutPanelTitle = 'Lookout'
LookoutPanelTitleDesc = 'Choose an activity:'
LookoutPanelTitleDescGame = 'Choose a game:'
LookoutPanelStatus = 'Lookout Status'
LookoutPanelStatusDesc = 'Currently searching for...'
LookoutPanelInvite = 'Lookout Invite'
LookoutPanelInviteDesc = 'Inviting crew members for...'
LookoutPanelJoin = 'Lookout Join'
LookoutPanelJoinDesc = 'Decide if you want to join this game...'
LookoutPanelJoined = 'Lookout Joined'
LookoutPanelJoinedDesc = 'Waiting for others to join the game'
LookoutSearchContinue = 'Continue search'
LookoutSearchCancel = 'Cancel search'
LookoutJoinCancel = 'Cancel join'
LookoutInviteSkip = 'Skip All'
LookoutJoinStatus = 'Waiting for other players...'
LookoutFailedMsg = 'Match failed to be created, continuing search...'
LookoutAbortedMsg = 'Match failed to be created, ending search...'
LookoutFoundTitle = 'Match Found!'
LookoutFoundStatusCat = 'Game Category: %s'
LookoutFoundStatusType = 'Game Type: %s'
LookoutFoundStatusChance = 'Chance to find a match: %s'
LookoutFoundStatusChanceLow = 'Low'
LookoutFoundStatusChanceModerate = 'Moderate'
LookoutFoundStatusChanceHigh = 'High'
LookoutChallengeTitle = 'Challenge!'
LookoutChallengeDesc = 'Pick a game type to accept:'
LookoutSkirmishTitle = 'Skirmish!'
LookoutSkirmishDesc = 'Inviting other players...'
LookoutFoundJoin = 'Join'
LookoutFoundSkip = 'Skip'
LookoutJoinMsg = 'You will be teleported when game is created...'
LookoutTypeTitle = 'Pick type...'
LookoutOptionsTitle = 'Options'
LookoutOptionsDesc = "Select game's options below:"
LookoutSubmit = lSubmit
LookoutCancel = lCancel
LookoutConfirm = lConfirm
LookoutNext = lNext
LookoutBack = lBack
LookoutTimer = 'Time left to join: %d seconds!'
Options = 'Options'
LookoutStartMsg = 'You will be notified when a match is found.'
LookoutFoundMsg = 'Game found, would you like to join?'
LookoutFoundCrewMsg = 'Game found, would you like to join? You will join up with a new crew and leave your old one.'
LookoutCancelMsg = 'Lookout canceled.'
LeaveInstance = 'Return to Main World'
LookoutInviteFromMsg = 'You are invited by %s to a %s, would you like to join?'
LookoutInviteFromCrewMsg = 'You are invited by %s to a %s, would you like to join? You will join up with a new crew and leave your old one.'
LookoutInviteMsg = 'You are invited to a %s, would you like to join?'
LookoutInviteCrewMsg = 'You are invited to a %s, would you like to join? You will join up with a new crew and leave your old one.'
LookoutInviteFail = 'Failed to invite %s crew member(s). They are not allowed to play the chosen game.'
LookoutInviteIgnore = 'Cannot invite your crew at this moment, an invite is already in progress.  You can try again in a minute.'
LookoutInviteNeedCrew = 'You need to join or create a crew to play that type of game.'
LookoutInviteNeedUnlimited = 'You are invited to a %s. Sorry, you must be an Unlimited Access Member to join.'
ParlorGame = 'Parlor Games'
PVPGame = 'Pirate vs Pirate'
TMGame = 'Treasure Maps'
CrewGame = 'Find a Crew'
PrivGame = 'Privateering'
QuestGame = 'Do a Quest'
HSAGame = HighSeasAdventureStartTitle
PokerGame = 'Poker Game'
BlackjackGame = 'Blackjack'
FindACrew = 'Find a Crew'
FindAPVPCrew = 'Find a Privateer Crew'
RecruitCrewMembers = 'Recruit Crew Members'
ParlorGameBrief = 'parlor game'
PVPGameBrief = 'Pirate vs Pirate game'
TMGameBrief = 'Treasure Map'
CrewGameBrief = 'crew'
PrivGameBrief = 'privateering'
QuestGameBrief = 'quest'
HSAGameBrief = HighSeasAdventureStartTitle
ParlorGameDesc = 'Play a card game or other parlor game with other pirates'
PVPGameDesc = 'Compete with other pirates in a variety of games'
TMGameDesc = 'Work with other pirates to recover some treasure'
CrewGameDesc = 'Look for a crew of other pirates to join'
PrivGameDesc = 'Look for a crew of privateers to join'
QuestGameDesc = 'Find other pirates working on a specific quest'
HSAGameDesc = 'Set sail with other pirates and battle enemies in the open waters'
GameStyleBattleDesc = 'Every pirate for him/her self'
GameStyleTeamBattleDesc = 'Pirate team vs. Pirate team'
GameStyleShipBattleDesc = "Sink the other team's ship"
GameStyleCTFDesc = "Capture the other team's pirate flag"
GameStyleCTLDesc = 'Most gold captured wins'
GameStylePirateer = 'Most gold captured with ships wins'
GameStylePoker = 'Standard poker rules'
GameStyleBlackjack = 'Hand closest to 21 wins'
CrewStyleFindACrewDesc = 'Search for a crew to join'
CrewStyleRecruitMembersDesc = 'Find members for your crew'
CrewStyleFindAPVPCrewDesc = 'Search for a privateering crew to join'
AnyGame = 'Any Game'
CTFGame = 'Capture The Flag'
CTLGame = 'Capture The Loot'
PTRGame = 'Pirateer'
BTLGame = 'Mayhem'
TBTGame = 'Team Battle'
SBTGame = 'Ship Battle'
ARMGame = 'Armada'
TKPGame = 'Treasure Keeper'
BTBGame = 'Borrow the Boat'
GameDuration = 'Duration'
GameDurationShort = 'Short'
GameDurationMed = 'Medium'
GameDurationLong = 'Long'
GameMatchCount = 'Match Count'
GamePassword = 'Game Password'
GameMinBet = 'Minimum Bet'
GameNPCPlayers = 'Include AI Players'
GameLocation = 'Game Location'
GameUseCrew = 'Use Current Crew'
GameMinPlayers = 'Min Num Players'
GameDesPlayers = 'Desired Num Players'
GameMaxPlayers = 'Max Num Players'
GameMaxCrew = 'Max Crew Size'
GameMaxShip = 'Max Crew Ship'
GameVIPPass = 'VIP Pass'
GameSoloPlay = 'Play Treasure Map Alone'
PlayTMNow = 'Play ' + BossBattleName + ' Now'
PlayTMNowHelp = 'Give it a shot alone'
PlayTMLookout = BossBattleName + ' With Crew'
PlayTMLookoutHelp = 'Find others to play with'
PlayTMBlackPearlNotReady = 'The Black Pearl boss battle is coming soon!'
PlayTMVelvetRope = '\x01smallCaps\x01Unlimited Access Members Only\x02'
Dowse = 'Use Dowsing Rod'
DowsingRodNotAvailable = 'You cannot use the Dowsing Rod here.'
DowsingRodWarmerFar = 'You are getting closer to the spot, but you are still very far away.'
DowsingRodWarmer = 'You are getting closer to the spot.'
DowsingRodWarmerClose = 'You are getting closer to the spot, and it is nearby.'
DowsingRodColder = 'You are getting further away from the spot.'
DowsingRodColderClose = 'You are getting further away from the spot, but it is still nearby.'
DowsingRodHot = 'You are right near the spot!'
DowsingRodSame = "You aren't any closer to the spot than you were before."
DowsingRodComplete = 'You have already found the item with your Dowsing Rod.'
DowsingRodFirstTime = 'The Dowsing Rod has determined where the item is.\nUse it when you are getting closer.'
CheckPortrait = 'Check Portrait'
RemovePortrait = 'Remove Portrait'
PortraitDisguiseMale = 'Disguise yourself with the hat, shirt, and pants that Mr. Clubheart wears.'
PortraitDisguiseFemale = 'Disguise yourself with the skirt, blouse, and boots that Mrs. Clubheart wears.'
ProfilePageLoading = 'Loading...'
ProfilePageCrew = 'Crew Invite'
ProfilePageRemoveCrew = 'Remove Crew'
ProfilePageLeaveCrew = 'Leave Crew'
ProfilePageFriend = 'Make Pirate Friendship'
ProfilePageRemoveFriend = 'Break Pirate Friendship'
ProfilePagePlayerFriend = 'Make Player Friendship'
ProfilePageRemovePlayerFriend = 'Break Player Friendship'
ProfilePageGuild = 'Guild Invite'
ProfilePageLeaveGuild = 'Leave Guild'
ProfilePageWhisper = 'Whisper'
ProfilePageTrade = 'Trade'
ProfilePageProblem = 'Take Action!'
ProfilePageBoot = 'Boot from\nShip'
ProfilePageIgnore = 'Ignore'
ProfilePageReport = 'Report'
ProfilePageUnignore = 'Unignore'
ProfilePageStopIgnore = 'Stop\nIgnoring'
ProfilePageChallenge = 'Crew\nBattle'
ProfilePageNotoriety = 'Level %s'
ProfilePageLevel = 'Level %s'
ProfilePageOcean = 'The High Seas'
ProfilePageHp = 'Health'
ProfilePageVoodoo = 'Voodoo'
ProfilePageSkillLevels = 'Skill Levels'
ProfilePageCannon = 'Cannon'
ProfilePageSailing = 'Sailing'
ProfilePageCutlass = 'Sword'
ProfilePagePistol = 'Shooting'
ProfilePageDoll = 'Doll'
ProfilePageDagger = 'Dagger'
ProfilePageGrenade = 'Grenade'
ProfilePageStaff = 'Staff'
ProfilePagePotions = 'Potions'
ProfilePageFishing = 'Fishing'
ProfilePageGoto = 'Go To'
ProfilePageLocation = 'Location:'
ProfilePageOffline = 'Offline'
ProfilePageToontown = 'Toontown Online'
ProfilePageFairies = 'Pixie Hollow'
ProfilePageCars = 'World of Cars'
ProfilePageUnknown = 'Unknown'
ProfilePageAccountName = 'DName: %s'
PlayerIgnoredWarning = '%s is currently ignored!'
PlayerOfflineWarning = '%s is not online!'
PlayerOtherGameWarning = '%s is playing %s!'
PlayerOtherShardWarning = '%s is on a different server!'
NoInteractPlayerWarning = 'Type in Local Chat to Interact with %s.'
PlayerNotInGuildWarning = 'You are not in a guild!'
PlayerNotPrivateeringWarning = 'You can not boot someone unless you are captain of a privateering ship!'
PlayerNotOnShipWarning = '%s is not on your ship!'
PlayerNotInCrewWarning = '%s is not in your crew!'
PlayerNotChallengeWarning = '%s is already playing Pirate vs. Pirate!'
PlayerSameCrewWarning = 'You should challenge people outside your crew since your crew will be on the same team!'
PlayerNotGuildOfficerWarning = "You can't invite people to a guild unless you are an officer or veteran of the guild!"
PlayerNotGuildRemoveWarning = "You can't remove people from a guild unless you are an officer of the guild!"
PlayerOpenChat = 'Open Chat'
PlayerSpeedChatPlus = 'SpeedChat Plus'
PlayerSpeedChat = 'SpeedChat'
FriendInviterAvatarNotYet = 'Make Pirate Friends with the pirate named %s?\n\nThis friendship will only exist within Pirates of the Caribbean Online and is only between these two pirates.'
FriendInviterPlayerNotYet = 'Make Player Friends with the player of %s named %s?\n\nThis type of friendship extends across other Disney online games and is not only between specific pirates.'
FriendInviterPlayerNotYetAvNameOnly = 'Make Player friends with the player of %s?\n\nThis type of friendship extends across this and other Disney Online games.  Your account name and online status for all characters will be displayed to this new friend.'
FriendInviterAvatarEndFriendShip = 'Stop being Pirate Friends with the pirate named %s?\n\nThis will not break a Player Friendship, but these two pirates will no longer be friends.'
FriendInviterPlayerEndFriendShip = 'Stop being Player Friends with the player named %s?\n\nThis will not break any friendships between your Pirate Friends'
MainMenuReturn = 'Return to Game'
MainMenuOptions = 'Game Options'
MainMenuFeedback = 'Send Feedback'
MainMenuLogout = 'Logout'
MainMenuQuit = 'Exit Game'
MainMenuLogoutConfirm = 'Are you sure you want to logout?'
MainMenuQuitConfirm = 'Are you sure you want to exit the game? This will return you to your desktop.'
ChatTabAll = 'Local'
ChatTabGuild = 'Guild'
ChatTabCrew = 'Crew'
ChatTabFrench = 'French'
ChatTabSpanish = 'Spanish'
ChatTabShipPVP = 'Privateer'
FriendSecretIntro = "If you are playing Disney's Pirates of the Caribbean Online with someone you know in the real world, you can become Player Friends.  You can chat using the keyboard with your Player Friends.  Other Pirates won't understand what you're saying.\n\nYou do this by getting a Player Friend Code.  Tell the Player Friend Code to your friend, but not to anyone else.  When your friend types in your Player Friend Code on his or her screen, you'll be Player Friends in Pirates!"
NoSecretChatAtAll = 'To chat with a friend, the Player Friends feature must first be enabled.  Player Friends allows one member to chat with another member only by means of a Player Friend Code that must be communicated outside of the game.\n\nTo activate this feature or to learn more about it, exit Pirates and then click on "Account Options" on the Pirates web page.'
RelationshipChooserTitle = '\nWhat Ye be wanting with %s?'
RelationshipChooserAvFriendsMake = 'Make Friends'
RelationshipChooserAvFriendsBreak = 'Break Friends'
RelationshipChooserPlFriendsMake = 'Make Player Friends'
RelationshipChooserPlFriendsBreak = 'Break Player Friends'
RelationshipChooserPlSecrets = 'Use Friend Codes'
ChatWarningClose = 'Understood'
ChatWarningTitle = 'System Message'
ChatWarningFirst = 'Final Warning \xe2\x80\x93 If you continue using inappropriate language you will be suspended. You said"%s"'
ChatWarningLast = 'Warning - Watch your language. Using inappropriate words will get you suspended. You said"%s"'
ChatWarningSuspend = 'Your account has been suspended for 24 hours for using inappropriate language. You said"%s"'
AFKFlag = '[AFK]'
IngoredFlag = 'IGNORED'
InjuredFlag = 'KNOCK OUT'
InjuredNeedTonic = 'Reviving Requires a Tonic'
InjuredHasTonic = 'Press Shift to Revive with Tonic'
InjuredReviving = 'Reviving'
InjuredGotoJail = 'Go to Jail'
InjuredDefeated = 'You have been Defeated!'
InjuredOrHelp = 'Wait for another Pirate to revive you or click this button to go to Jail.'
InjuredHelped = '%s has been revived by %s'
BodyChangeButton = 'Choose Shape'
BodyShapeUpdate = 'Read Carefully!'
BodyChangeText = "In order to improve animation we need to change the body shapes. Your pirate's body shape will soon be unsupported. We are sorry.\n\nYou may choose a new body shape by using this panel to do so at any time, however once you commit to a shape that choice will be final."
BodyTypeCommit = 'Commit to new Shape'
BodyTypeLater = 'Let me think about it'
BodyTypeConfirm = 'Are you sure you want this new body shape? This choice is final.'
from pandac.PandaModules import TextProperties
from pandac.PandaModules import TextPropertiesManager
tpMgr = TextPropertiesManager.getGlobalPtr()
gold = TextProperties()
gold.setTextColor( * PiratesGuiGlobals.TextFG1)
tpMgr.setProperties('gold', gold)
white = TextProperties()
white.setTextColor( * PiratesGuiGlobals.TextFG2)
tpMgr.setProperties('white', white)
slant = TextProperties()
slant.setSlant(0.2)
tpMgr.setProperties('slant', slant)
uline = TextProperties()
uline.setUnderscore(True)
uline.setUnderscoreHeight(-0.12)
tpMgr.setProperties('uline', uline)
smallCaps = TextProperties()
smallCaps.setSmallCaps(1)
tpMgr.setProperties('smallCaps', smallCaps)
questObj = TextProperties()
questObj.setTextColor( * PiratesGuiGlobals.TextFG27)
questObj.setShadowColor( * PiratesGuiGlobals.TextFG0)
tpMgr.setProperties('questObj', questObj)
interfaceRed = TextProperties()
interfaceRed.setTextColor(0.9, 0.4, 0.4, 1)
tpMgr.setProperties('Ired', interfaceRed)
darkRed = TextProperties()
darkRed.setTextColor(0.4, 0.0, 0.0, 1)
tpMgr.setProperties('Dred', darkRed)
brightRed = TextProperties()
brightRed.setTextColor(0.9, 0.1, 0.1, 1)
tpMgr.setProperties('Bred', brightRed)
interfaceBlue = TextProperties()
interfaceBlue.setTextColor(0.1, 0.5, 1.0, 1)
tpMgr.setProperties('Iblue', interfaceBlue)
interfaceGreen = TextProperties()
interfaceGreen.setTextColor(0.1, 1.0, 0.1, 1)
tpMgr.setProperties('Igreen', interfaceGreen)
interfaceYellow = TextProperties()
interfaceYellow.setTextColor(1.0, 1.0, 0.0, 1)
tpMgr.setProperties('Iyellow', interfaceYellow)
interfaceWhite = TextProperties()
interfaceWhite.setTextColor(1.0, 1.0, 1.0, 1)
tpMgr.setProperties('Iwhite', interfaceWhite)
lootDropBlack = TextProperties()
lootDropBlack.setTextColor( * PiratesGuiGlobals.TextFG0)
lootDropBlack.setShadowColor(0, 0, 0, 0)
tpMgr.setProperties('lootDropBlack', lootDropBlack)
guildName = TextProperties()
guildName.setGlyphScale(0.8)
guildName.setSmallCaps(1)
guildName.setTextColor(1.0, 1.0, 1.0, 1)
tpMgr.setProperties('guildName', guildName)
larger = TextProperties()
larger.setGlyphScale(1.5)
tpMgr.setProperties('larger', guildName)
copperGold = TextProperties()
copperGold.setTextColor( * PiratesGuiGlobals.TextFG25)
tpMgr.setProperties('CopperGold', copperGold)

def getHeadingScale(headingLevel):
    if headingLevel == 1:
        return 1.0
    else :
        return 1.2


def makeHeadingString(str, headingLevel):
    if headingLevel == 1:
        str = '\x01%s\x01%s\x02' % ('slant', str)
    elif headingLevel == 2:
        str = '\x01%s\x01\x01%s\x01%s\x02\x02' % ('gold', 'smallCaps', str)
    elif headingLevel == 3:
        str = str.upper()
    return str


TutorialPanelDialog = {
    'seachestOpen': '\nClick on the \x01Ired\x01Sea Chest Icon\x02 to open it.',
    'questPageOpen': '\nClick on the \x01Ired\x01Journal Icon\x02 to view your quests.',
    'questPageClose': '\nThe journal shows what to do next.\nClick on the \x01Ired\x01Sea Chest Icon\x02 to close it.',
    'boardShip': "\nPress \x05shiftButton\x05 to board Bo Beck's boat.",
    'useCannon': '\nPress \x05shiftButton\x05 to use the cannon.',
    'moveCannon': '\nHold down \x01Ired\x01Right Mouse Button\x02 then move the mouse to aim.',
    'fireCannon': '\nClick \x01Ired\x01Left Mouse Button\x02 to shoot.',
    'wreckInstruction': 'Hit the ship wreck 3 times. Hits so far \x01Ired\x01',
    'shipCombatInstruction': 'Shoot at the Ghost ship (hull) to sink it.',
    'exitCannon': '\nPress \x01Ired\x01Escape\x02 to stop using the cannon.',
    'leaveJail': '\nLeave the Jail. Press the \x01Ired\x01Arrow Keys\x02 or \x01Ired\x01WASD keys\x02 to move.',
    'showBlacksmith': 'Walk towards the light ray. Enter the Old Warehouse to get a sword.',
    'doCutlassTutorial': 'Would you like to learn how to use weapons?',
    'drawSword': '\nClick on the \x01Ired\x01Sword Icon\x02 to draw your weapon.',
    'attackSword': '\nClick with \x01Ired\x01Left Mouse Button\x02 to attack the dummy.',
    'comboSword': '\nTo perform a combo, \x01Ired\x01Click\x02 to swing then \x01Ired\x01Click\x02 again at the end of your swing.  Timing is key!',
    'cutlassLvl': '\nYou earned enough reputation to level up your cutlass.\nClick on the \x01Ired\x01Sea Chest Icon\x02 to open it.',
    'cutlassSkillOpen': '\nClick on the \x01Ired\x01Skill Icon\x02 to view your skills.',
    'cutlassSkillUnlock': '\nYou earned 1 Skill Point which can be used to unlock and improve skills. Click on the \x01Ired\x01Sweep Icon\x02 to unlock it.',
    'cutlassDoneLvl': '\nSweep Skill Unlocked. \nClick on the \x01Ired\x01Sea Chest Icon\x02 to continue.',
    'specialMenu': '\nClick the \x01\\Ired\x01Sweep Icon\x02.',
    'skillLearning': "As you level up you'll be able to unlock New Skills and gain more Weapons.",
    'sheatheSword': '\nPress \x01Ired\x01Escape\x02 to put away your weapon.',
    'showSkeleton': 'Defeat 3 \x01Ired\x01Undead Gravediggers\x02 in the \x01Ired\x01Graveyard\x02 before you visit Tia Dalma.',
    'showJungleTia': '\nWalk through the \x01Ired\x01Tree Tunnel\x02 to visit Tia Dalma.',
    'receiveCompass': 'Would you like to learn how to use the compass?',
    'compassActiveQuest': 'The \x01Iyellow\x01ARROW\x02 points to your quest goal.',
    'compassIconsBearing': 'You are the \x01Iwhite\x01Arrow\x02 in the center. \nExits are shown as \x01Iwhite\x01RECTANGLES\x02.',
    'compassIconsPeople': 'Enemies are shown in \x01Ired\x01RED\x02. Townfolk are shown in \x01Igreen\x01GREEN\x02. Other players are shown in \x01Iblue\x01BLUE\x02.',
    'showNavy': "Defeat \x01Ired\x01Navy Soldiers\x02 to find the Black Pearl release orders.\nFollow the arrow towards the Governor's Mansion.",
    'showGovMansion': "Enter the \x01Ired\x01Governor's Mansion\x02 to deliver release orders to Elizabeth Swann.",
    'showDarby': 'Walk towards the light ray. \nFind \x01Ired\x01Darby Drydock\x02 to get a ship.',
    'showDinghy': 'Use a \x01Ired\x01dinghy\x02 to launch your ship.',
    'showBarbossa': "Sail to \x01Ired\x01Devil's Anvil\x02 to visit Barbossa.",
    'pistolAim': '\nHold down \x01Ired\x01Right Mouse Button\x02 then move the mouse to aim at the monkey.',
    'pistolTarget': '\nThe aiming circle turns red over an enemy.',
    'pistolHit': '\nClick the \x01Ired\x01Left Mouse Button\x02 to shoot.',
    'pistolPractice': '\nPress \x01Ired\x01Escape\x02 to put away your weapon.',
    'lookoutChestOpen': '\nClick on the \x01Ired\x01Sea Chest Icon\x02 to open it.',
    'lookoutOpen': '\nClick on the \x01Ired\x01Lookout Icon\x02 to look for other players\nin Pirate vs. Pirate combat.',
    'lookoutClose': '\nClick on the \x01Ired\x01Sea Chest Icon\x02 to close it.',
    'showTortugaJack': '\nSail to \x01Ired\x01Tortuga\x02 and find \x01Ired\x01Jack Sparrow\x02.',
    'teleport_tut1': 'Now ....Press the \x05SmallMap\x05 to bring up the Map of the Islands.',
    'teleport_tut2': 'Continents that are available for transport to are highighted. As you unlock additional continents for transport, they will become highlighted ont his map. Double click the left mouse button \x05leftClick\x05 \x05leftClick\x05 on the highlighted continent (Tortuga) to be transported to there.',
    'teleport_tut3': 'You have safely arrived in Tortuga. Tortuga is never more than a double-click away. Click Ok to exit the tutorial.',
    'chat_tut1': 'Chatting with other pirates can be helpful for teaming up on the enemy. \nClick on the \x01Ired\x01Arrow\x02 or press ENTER to start chatting.',
    'chat_tut2': '\nSend a message by typing it at the prompt and pressing ENTER.',
    'chat_tut3': 'You can make friends or start a crew by clicking on another pirate.',
    'chat_tut4': 'This shows a profile card with a picture of the pirate as well as information about him.',
    'chat_tut5': 'To make friends or start a crew, click on the Friend Invite or Crew Invite buttons on the profile card.',
    'chat_tut6': 'You can also start a crew by clicking on the Start a Crew button in the upper left corner beneath your health bar.',
    'chat_tut7': 'To see a list of your friends, press F or click the mug icon in your Sea Chest.',
    'chat_tut8': 'A list of your crewmates will be shown on the left-hand side of the screen beneath your health bar.',
    'chat_tut_alt1': 'Chatting with other pirates can be helpful for teaming up on the enemy.',
    'chat_tut_alt2': '\nClick on the \x01Ired\x01Skull Icon\x02 in the lower left corner to bring up the SpeedChat menu.',
    'chat_tut_alt3': '\nSend a SpeedChat message by clicking on a menu item.',
    'chat_tut_alt4': 'You can make friends or start a crew by clicking on another pirate.',
    'chat_tut_alt5': 'This shows a profile card with a picture of the pirate as well as information about him.',
    'chat_tut_alt6': 'To make friends or start a crew, click on the Friend Invite or Crew Invite buttons on the profile card.',
    'chat_tut_alt7': 'To see a list of your friends, press F or click the mug icon in your Sea Chest.',
    'chat_tut_alt8': 'A list of your crewmates will be shown on the left-hand side of the screen beneath your health bar.'
}
TutorialPanelDialogEasyCombo = {
    'comboSword': '\nTo get a combo bonus, \x01Ired\x01Click\x02 to swing then \x01Ired\x01Click\x02 again at the end of your swing.  Timing is key!'
}
ContextPanelNoMoreHints = "Don't show %s hints."
ContextPanelTypes = {
    InventoryType.TutTypeBasic: 'Basic', InventoryType.TutTypeIntermediate: 'Intermediate', InventoryType.TutTypeAdvanced: 'Advanced'
}
ContextPanelTitles = {
    InventoryType.RepairShip: 'Repair Your Ship', InventoryType.SailCommands: {
        0: 'Camera Controls',
        1: 'Change Views',
        2: 'How to Exit Steering',
        3: 'Sailing with a Crew',
        4: 'Public Ships',
        6: 'Boarding Permissions',
        9: 'Travel Speed'
    }, InventoryType.FireBroadside: 'Fire a Broadside!', InventoryType.AimBroadsides: 'Aim Broadsides', InventoryType.DockToSellCargo: 'Dock to Sell Cargo', InventoryType.LostCargo: 'Lost Cargo', InventoryType.LowShipHealth: 'Low Ship Health!', InventoryType.BuyNewShip: 'Buy a New %s', InventoryType.AimForHull: 'Aim for the Hull!', InventoryType.ExitCannon: 'Exiting a Cannon', InventoryType.LowHealth: 'Low Health!', InventoryType.OutOfTonics: 'Out of Tonics', InventoryType.SwitchWeapons: 'Switch Weapons', InventoryType.AimPistol: 'Aim Your Pistol', InventoryType.NewSkillPoint: 'New %s Skill Point!', InventoryType.UpgradeSkills: 'Upgrading Skills', InventoryType.CutlassCombos: 'Sword Combos', InventoryType.NewComboMove: 'New Combo Move!', InventoryType.NewTakeAimSkill: 'New Take-Aim Skill!', InventoryType.AttuneVoodooDoll: 'Attune Voodoo Doll', InventoryType.FollowLight: 'Follow the Light', InventoryType.QuestJournal: 'Quest Journal', InventoryType.ChangeQuestTracking: 'Change Quest Tracking', InventoryType.NewWeaponQuest: 'New Weapon Quest!', InventoryType.MoreWeaponQuests: 'More Weapon Quests', InventoryType.IslandTeleport: 'Island Teleport', InventoryType.PlayerChat: 'Player Chat', InventoryType.PlayerProfiles: 'Player Profiles', InventoryType.PlayerInvites: 'Player Invites', InventoryType.NewCrew: 'New Crew!', InventoryType.CrewBonus: 'Crew Bonus', InventoryType.NewFriend: 'New Friend!', InventoryType.NewGuild: 'New Guild!', InventoryType.BrokenHull: 'Broken %s Hull', InventoryType.BrokenMast: 'Broken Mast', InventoryType.RearHullDamage: 'Rear Hull Damage!', InventoryType.AttuneFriend: 'Attune a Friend', InventoryType.RestAndHeal: 'Rest & Heal', InventoryType.GoToJail: 'Going to Jail', InventoryType.Disengage: 'Disengage', InventoryType.EarnMoreSkillPoints: 'Earn More Skill Points', InventoryType.NotorietyLevelUp: 'Notoriety Level Up!', InventoryType.MerchantStores: 'Merchant Stores', InventoryType.WeaponTraining: 'Weapon Training', InventoryType.NewAmmoSkill: 'New Ammo Skill!', InventoryType.OutOfAmmo: 'Out of Ammo', InventoryType.HardEnemies: 'Hard Enemies', InventoryType.IslandMap: 'Island Map', InventoryType.DockCommands: {
        3: 'Jump',
        5: 'Auto-Run',
        7: 'Parlor Games',
        9: 'Privateering',
        19: 'Pirate vs. Pirate'
    }, InventoryType.DockCrewCommands: {
        1: 'Leaving a Crew'
    }, InventoryType.TeleportToFriends: 'Teleporting to Friends', InventoryType.Flagships: 'Flagships', InventoryType.BackStrike: 'Back-strike', InventoryType.Interrupt: 'Interrupt', InventoryType.BossEnemy: 'Boss Enemy', InventoryType.TreasureCollection: 'Treasure Collection', InventoryType.SearchableContainers: '%s', InventoryType.UseEmotes: 'Use Emotes!', InventoryType.SpanishPrivateers: 'Spanish Privateers', InventoryType.FrenchPrivateers: 'French Privateers', InventoryType.Groggy: 'Groggy', InventoryType.ChatPreferences: 'Chat Preferences', InventoryType.SailShip: 'Sail the Ship', InventoryType.FishingTutorial: 'Fishing Tutorial', InventoryType.FishingEnterGame: 'Fishing', InventoryType.FishingAfterCast: 'Fishing', InventoryType.FishingAboutToBite: 'Fishing', InventoryType.FishingFishOnLine: 'Fishing', InventoryType.FishingLineHealth: 'Fishing', InventoryType.FishingLineBroken: 'Fishing', InventoryType.FishingNoMoreLures: 'Fishing', InventoryType.FishingCaughtFish: 'Fishing', InventoryType.FishingLevelGain: 'Fishing', InventoryType.FishingOceanEye: 'Ocean Eye', InventoryType.FishingSink: 'Sink', InventoryType.FishingStall: 'Stall', InventoryType.FishingPull: 'Pull', InventoryType.FishingHealLine: 'Heal Line', InventoryType.FishingLegendAppear: 'Legendary Fish', InventoryType.FishingLegendStruggle: 'Legendary Fish', InventoryType.FishingLegendReel: 'Legendary Fish', InventoryType.FishingLegendCaught: 'Legendary Fish', InventoryType.FishingLevel10: 'Fishing', InventoryType.FishingCaughtAllFish: 'Fishing', InventoryType.FishingLineBroken2: 'Fishing', InventoryType.FirstLootContainer: 'Loot Container', InventoryType.GunTrainingRequired: 'Gun Training', InventoryType.DollTrainingRequired: 'Voodoo Doll Training', InventoryType.DaggerTrainingRequired: 'Dagger Training', InventoryType.StaffTrainingRequired: 'Voodoo Staff Training', InventoryType.EquippingWeapons: 'Equipping Weapons', InventoryType.InventoryFull: 'Inventory Full', InventoryType.FirstSailingItem: 'Sailing Item', InventoryType.CursedBlades: 'Cursed Blades!'
}
ContextPanelMessages = {
    InventoryType.RepairShip: 'Repair your ship at the \x01Dred\x01Shipwright\x02 near the docks in town. Otherwise, you cannot sail it.', InventoryType.SailCommands: {
        0: 'Hold down the \x01Dred\x01Right Mouse Button\x02 to look around.',
        1: 'Use the \x01Dred\x01Mouse Wheel\x02 to move the Camera In or Out.',
        2: '\x01Dred\x01Press Escape (ESC)\x02 to stop using the Steering Wheel. This lets you use the deck Cannons.',
        3: "\x01Dred\x01Don't sail alone!\x02 Other players can fire Cannons on your Ship.",
        4: 'Want to find a large Pirate crew? Join a \x01Dred\x01Public Ship\x02 from the \x01Dred\x01Dinghy\x02.',
        6: "Want more players onboard? Set your \x01Dred\x01Boarding Permissions\x02 to \x01Dred\x01Public\x02. The button for this is above your ship's health meter.",
        9: 'Sailing in a straight line allows you to \x01Dred\x01travel long distances faster\x02.'
    }, InventoryType.FireBroadside: '\x01Dred\x01Press 1 or 2\x02 to fire a Broadside! You can also click on the Skill Icons.', InventoryType.AimBroadsides: '\x01Dred\x01Point the side of your ship at the enemy\x02 to aim your Broadsides! Then FIRE!', InventoryType.DockToSellCargo: 'Your Cargo Hold is full. \x01Dred\x01Dock at port\x02 to sell the plunder!', InventoryType.LostCargo: 'If your ship sinks, you lose all your Cargo from the voyage!', InventoryType.LowShipHealth: 'Your ship is damaged! You can \x01Dred\x01repair\x02 it at the \x01Dred\x01Shipwright\x02 in town.', InventoryType.BuyNewShip: 'You have earned enough gold to purchase a \x01Dred\x01%s\x02! You can purchase New Ships from the \x01Dred\x01Shipwright\x02 in town.', InventoryType.AimForHull: '\x01Dred\x01Aim for the Hull\x02 of a ship to sink it.', InventoryType.ExitCannon: '\x01Dred\x01Press Escape (ESC)\x02 to stop using the Cannon.', InventoryType.LowHealth: '\x01Dred\x01Press T\x02 to drink a Tonic! Tonics restore lost Health.', InventoryType.OutOfTonics: 'You have used up all your healing tonics! Purchase more from the \x01Dred\x01Gypsy Wagons\x02 in town.', InventoryType.SwitchWeapons: '\x01Dred\x01Press F1 or F2\x02 to switch between the Sword and the Pistol.', InventoryType.AimPistol: '\x01Dred\x01Hold down\x02 the \x01Dred\x01Right Mouse Button\x02 to aim your pistol.', InventoryType.NewSkillPoint: 'You got 1 new %s Skill Point! \x01Dred\x01Press K\x02 to see your Skill Page and \x01Dred\x01unlock\x02 new skills or \x01Dred\x01upgrade\x02 current skills.', InventoryType.UpgradeSkills: "You've upgraded a Skill! Upgrading a skill makes it more powerful, and its effect will last longer.", InventoryType.CutlassCombos: '\x01Dred\x01Time your Sword Attacks\x02 to form a Combo. Combos deal more damage over time than button-mashing.', InventoryType.NewComboMove: 'You unlocked a \x01Dred\x01new Combo Move\x02! You can now form longer Combo Chains for greater damage', InventoryType.NewTakeAimSkill: 'You unlocked the Take Aim Skill! \x01Dred\x01Hold down\x02 the \x01Dred\x01Left Mouse Button\x02 to Aim with your pistol.', InventoryType.AttuneVoodooDoll: 'Touch an enemy with the Voodoo Doll using your \x01Dred\x01Left Mouse Button\x02. Then you can cast Hexes on him from a distance!', InventoryType.FollowLight: 'Follow the Ray-of-Light. It leads you to your \x01Dred\x01Quest target\x02!', InventoryType.QuestJournal: 'You have a New Quest! \x01Dred\x01Press J\x02 to open your \x01Dred\x01Quest Journal\x02 and read it.', InventoryType.ChangeQuestTracking: 'You can change which Quest is being tracked by the Ray-of-Light in your \x01Dred\x01Quest Journal (J)\x02.', InventoryType.NewWeaponQuest: 'You received a New Weapon Quest! If you complete this Quest, you will unlock the \x01Dred\x01Voodoo Doll weapon\x02!', InventoryType.MoreWeaponQuests: 'As your Notoriety Level increases, you will unlock more Weapon Quests.', InventoryType.IslandTeleport: 'Use the \x01Dred\x01Map page (M)\x02 to Teleport from one island to another.', InventoryType.PlayerChat: '\x01Dred\x01Press ENTER\x02 to begin typing to nearby players.', InventoryType.PlayerProfiles: '\x01Dred\x01Click on other players\x02 to see their Player Profile. You must \x01Dred\x01put away your weapon first\x02 though.', InventoryType.PlayerInvites: 'You can invite another player to join your \x01Dred\x01Crew\x02 or \x01Dred\x01Guild\x02 from their \x01Dred\x01Player Profile\x02.', InventoryType.NewCrew: 'You have joined a Crew! Crews have their own private chat channel and you can teleport to any of your crewmates!', InventoryType.CrewBonus: 'When you fight near your Crewmates, you gain \x01Dred\x01bonus Reputation\x02 and level up faster!', InventoryType.NewFriend: "You made a new Friend! You can use your \x01Dred\x01Friend's List (F)\x02 to contact or teleport to your friend.", InventoryType.NewGuild: "You have joined a Guild! Guilds help you stay in contact with friends and meet other Pirates! View your Guild's status using the \x01Dred\x01Friend's List (F)\x02.", InventoryType.BrokenHull: 'You have lost all your Hull Points on your %s side. Further damage would be dangerous! You can \x01Dred\x01repair\x02 this at the \x01Dred\x01Shipwright\x02 in town.', InventoryType.BrokenMast: 'You have lost a Mast and move slower now. You can \x01Dred\x01repair\x02 this at the \x01Dred\x01Shipwright\x02 in town.', InventoryType.RearHullDamage: 'Attacking enemy ships in the \x01Dred\x01Rear Hull\x02 deals extra damage!', InventoryType.AttuneFriend: 'You can attune a friendly Pirate and \x01Dred\x01cast Healing Voodoo\x02 on him.', InventoryType.RestAndHeal: '\x01Dred\x01Wait in a safe place\x02 to heal after a battle. Over time, your Health will be restored.', InventoryType.GoToJail: 'When you are defeated, you are put in Jail by the Navy. Find a way to escape.', InventoryType.Disengage: 'Enemies disengage when they chase you too far from the area they are guarding.', InventoryType.EarnMoreSkillPoints: '\x01Dred\x01Level up your Weapons\x02 to earn more Skill Points for that weapon.', InventoryType.NotorietyLevelUp: 'You gained a new Notoriety Level! Notoriety Levels make you stronger and give you more Health and Voodoo Points.', InventoryType.WeaponTraining: 'You will \x01Dred\x01unlock new weapons\x02 like the Voodoo Doll, Dagger, Grenades, and Voodoo Staff when you reach \x01Dred\x01higher Notoriety Levels\x02.', InventoryType.MerchantStores: 'You can purchase new Weapons, Clothing, Tattoos, Jewelry, and Haircuts in town.', InventoryType.NewAmmoSkill: 'You unlocked a new Ammo Skill! Switching to this skill allows you to fire new ammo, but you must \x01Dred\x01purchase Ammo\x02 from the \x01Dred\x01Gunsmith\x02 in town.', InventoryType.OutOfAmmo: 'You ran out of ammo. \x01Dred\x01Purchase more\x02 from the \x01Dred\x01Gunsmith\x02 in town.', InventoryType.HardEnemies: 'Enemies with a \x01Dred\x01red Level tag\x02 are at a much \x01Dred\x01higher level\x02 than you! Be careful!', InventoryType.IslandMap: '\x01Dred\x01Press F8\x02 to show the Map for the island.', InventoryType.DockCommands: {
        3: 'Press the \x01Dred\x01Space Bar\x02 to Jump.',
        5: '\x01Dred\x01Press R\x02 to toggle Auto-Run.',
        7: 'You can play \x01Dred\x01Poker\x02 and \x01Dred\x01Blackjack\x02 at the \x01Dred\x01Taverns\x02 in town! Be careful not to lose all your gold though.',
        9: 'Want to battle other player ships at sea? Try Privateering in the \x01Dred\x01Lookout Panel (L)\x02.',
        19: 'Want to fight other players on land? Try Pirate vs. Pirate in the \x01Dred\x01Lookout Panel (L)\x02.'
    }, InventoryType.DockCrewCommands: {
        1: 'To leave a Crew, click on the Crew Button in the \x01Dred\x01Player Profile\x02.'
    }, InventoryType.TeleportToFriends: 'You can teleport to a Crewmate, Friend, or Guild Member by using the \x01Dred\x01Go To Button\x02 on their \x01Dred\x01Player Profiles\x02.', InventoryType.Flagships: 'Ships with a flag icon overhead are Flagships. They \x01Dred\x01must be boarded\x02 to be sunk!', InventoryType.BackStrike: 'Attacking enemies in the back with a Dagger deals extra damage!', InventoryType.Interrupt: "You can use the \x01Dred\x01new Asp Skill\x02 to interrupt a target's Voodoo Doll Attunement.", InventoryType.BossEnemy: 'This is a Boss Enemy! Boss Enemies are tough to defeat. You should find other Pirates to help you in this battle.', InventoryType.TreasureCollection: 'You unlocked a Treasure Collection Set! Complete the collection for a Reputation reward. \x01Dred\x01Press U\x02 to see your collections.', InventoryType.SearchableContainers: 'These searchable items are used for Quests later on.', InventoryType.UseEmotes: 'Ever wanted to express yourself to other players? Try typing \x01Dred\x01/wave\x02 or \x01Dred\x01/dance\x02 in chat!', InventoryType.SpanishPrivateers: 'Welcome to the Spanish Privateering Island! Deploy a ship or board an existing ship to hunt the French foe!', InventoryType.FrenchPrivateers: 'Welcome to the French Privateering Island! Deploy a ship or board an existing ship to hunt the Spanish foe!', InventoryType.Groggy: 'You are Groggy! While groggy, your \x01Dred\x01Maximum Health is reduced\x02 for a short time.', InventoryType.ChatPreferences: '%s', InventoryType.SailShip: 'Grab the \x01Dred\x01Steering Wheel\x02 to sail the ship around.', InventoryType.FishingEnterGame: 'Click to start the power bar, click again to cast!', InventoryType.FishingAfterCast: 'Click and hold to reel in, Space Bar quick reels!', InventoryType.FishingAboutToBite: 'Click as a fish bites to hook it!', InventoryType.FishingFishOnLine: 'Stop reeling when the fish fights or your line will lose health!', InventoryType.FishingLineHealth: 'If your line health reaches zero, you will lose your lure and the fish will get away!', InventoryType.FishingLineBroken: 'Your line broke! Choose a new lure from your tackle box.', InventoryType.FishingNoMoreLures: 'You can purchase more from the Fishing Master.', InventoryType.FishingCaughtFish: 'Congratulations! This fish has been added to your collection.', InventoryType.FishingLevelGain: 'Level up to gain new abilities and increase reel-in speed!', InventoryType.FishingOceanEye: 'Ocean Eye will give you a view of the entire ocean.', InventoryType.FishingSink: 'Sink will cause your lure to fall faster.', InventoryType.FishingStall: 'Stall will pause your lure in the water.', InventoryType.FishingPull: 'Pull will increase the speed of reeling in a fish.', InventoryType.FishingHealLine: 'Heal Line will restore health to your line.', InventoryType.FishingLegendAppear: 'You have encountered a Legendary Fish!', InventoryType.FishingLegendStruggle: 'Click rapidly to win a struggle with the Legendary Fish!', InventoryType.FishingLegendReel: 'Move the mouse in a circle to reel in the fish!', InventoryType.FishingLegendCaught: 'Click on the handle to stop the Legendary Fish from fleeing!', InventoryType.FishingLevel10: 'You can now use the Fishing Boat from the Fishing Master!', InventoryType.FishingCaughtAllFish: 'There are no more fish in this area.', InventoryType.FishingLineBroken2: 'Some fish are stronger than others and are worth more XP and Gold.', InventoryType.FirstLootContainer: 'Loot Containers sometimes drop from enemies as you defeat them. They contain all kinds of treasures and items!', InventoryType.GunTrainingRequired: "Before you can use this weapon, you must \x01Dred\x01visit Barbossa\x02 on Devil's Anvil to learn how to use Guns!", InventoryType.DollTrainingRequired: 'The Voodoo Doll Training Quest \x01Dred\x01unlocks at Notoriety Level 5.\x02 You must complete it before you can use Voodoo Doll weapons.', InventoryType.DaggerTrainingRequired: 'The Dagger Training Quest \x01Dred\x01unlocks at Notoriety Level 10.\x02 You must complete it before you can use Dagger weapons.', InventoryType.StaffTrainingRequired: 'The Voodoo Staff Training Quest \x01Dred\x01unlocks at Notoriety Level 30.\x02 You must complete it before you can use Voodoo Staff weapons.', InventoryType.EquippingWeapons: 'Open your Inventory (I) to equip weapons! Click on the Weapon Tab and \x01Dred\x01drag the Weapon to the equip slots\x02 marked F1, F2, F3, & F4.', InventoryType.InventoryFull: 'One of your Inventory bags is full! Open your Inventory (I) and drag items to the \x01Dred\x01Trash Bin\x02 to remove them. You can also \x01Dred\x01sell items\x02 to Shopkeepers in town for Gold.', InventoryType.FirstSailingItem: 'You just received a \x01Dred\x01Sailing Item!\x02 These are equipped into the Item Slot and give you bonuses while \x01Dred\x01Sailing\x02 or on a \x01Dred\x01Cannon\x02!', InventoryType.CursedBlades: "You can now find Cursed Blades by defeating enemies on Raven's Cove and Isla Tormenta!"
}
SpeedChatPlusPreferences = 'This Pirate is using \x01Dred\x01SpeedChat Plus\x02 and did not receive your full message. When you are typing, words marked in red will not be sent to this player.'
SpeedChatPreferences = 'This Pirate is using \x01Dred\x01SpeedChat\x02 and did not receive your message. Please use \x01Dred\x01SpeedChat\x02 to talk with this player.'
ContextTutSearchableContainers = 'Searchable Containers'
ContextTutBuriedTreasure = 'Buried Treasure'
Left = 'Left'
Right = 'Right'
from pirates.uberdog import UberDogGlobals
Reloading = 'Reloading'
CannonAmmoNames = {}
StatusTrayHp = 'Health'
StatusTrayVoodoo = 'Voodoo'
Vitae = 'Groggy'
VitaeDesc = 'You were knocked out. Your current maximum health and voodoo have been temporarily limited.'
WeaponPageInfo1 = 'Choose Slot Above to Equip Weapon'
WeaponPageInfo2 = 'Select Weapon from List Below'
WeaponPageInfo3 = 'Not skilled enough to use weapon'
WeaponPageInfo4 = 'Need Training to use weapon'
SkillPageUnspentPoints = 'Skill Points: %d'
LauncherPhaseNames = {
    0: 'Initialization',
    1: 'Game Engine',
    2: 'Make-A-Pirate',
    3: 'Tutorial',
    4: 'Starting Island',
    5: 'High Seas',
    6: 'Chat Dictionary'
}
LauncherProgress = '%(name)s (%(current)s of %(total)s)'
LauncherStartingMessage = 'Starting Pirates Online... '
LauncherDownloadFile = 'Downloading update for ' + LauncherProgress + '...'
LauncherDownloadFileBytes = 'Downloading update for ' + LauncherProgress + ': %(bytes)s'
LauncherDownloadFilePercent = 'Downloading update for ' + LauncherProgress + ': %(percent)s%%'
LauncherDecompressingFile = 'Decompressing update for ' + LauncherProgress + '...'
LauncherDecompressingPercent = 'Decompressing update for ' + LauncherProgress + ': %(percent)s%%'
LauncherExtractingFile = 'Extracting update for ' + LauncherProgress + '...'
LauncherExtractingPercent = 'Extracting update for ' + LauncherProgress + ': %(percent)s%%'
LauncherPatchingFile = 'Applying update for ' + LauncherProgress + '...'
LauncherPatchingPercent = 'Applying update for ' + LauncherProgress + ': %(percent)s%%'
LauncherConnectProxyAttempt = 'Connecting to Pirates: %s (proxy: %s) attempt: %s'
LauncherConnectAttempt = 'Connecting to Pirates: %s attempt %s'
LauncherDownloadServerFileList = 'Updating Pirates...'
LauncherCreatingDownloadDb = 'Updating Pirates...'
LauncherDownloadClientFileList = 'Updating Pirates...'
LauncherFinishedDownloadDb = 'Updating Pirates... '
LauncherStartingGame = 'Starting Pirates...'
LauncherRecoverFiles = 'Updating Pirates. Recovering files...'
LauncherCheckUpdates = 'Checking for updates for ' + LauncherProgress
LauncherVerifyPhase = 'Updating Pirates...'
DownloadBlockerPanelTitle = 'Incomplete Download'
DownloadBlockerMsgGeneric = 'Sorry, your download is incomplete.\nPlease try again later.'
DownloadBlockerMsgIsland = 'Sorry, you may not leave the island until your download is complete.\nPlease try again later.'
DownloadBlockerMsgBoat = 'Sorry, you may not launch a ship until your download is complete.\nPlease try again later.'
DownloadBlockerMsgTeleport = 'Sorry, you may not teleport until your download is complete.\nPlease try again later.'
DownloadBlockerMsgLookout = 'Sorry, you may not use the Lookout until your download is complete.\nPlease try again later.'
CannotBoardProximityText = 'Download is incomplete, cannot board ship yet'
TeleportBlockerPanelTitle = 'Teleport Unavailable'
TeleportBlockerMsgBattle = "Sorry, you can't teleport while in battle."
TeleportBlockerMsgOnShip = "Sorry, you can't teleport while on a ship."
TeleportBlockerMsgOnAdventure = "Sorry, you can't teleport while on a high seas adventure."
TeleportBlockerMsgInPVP = "Sorry, you can't teleport while in PVP."
TeleportNotAvailable = 'Sorry, teleport is not allowed from here.'
NoTeleportInBattle = "Sorry, you can't teleport while in battle."
NoTeleportIslandToken = "Sorry, you don't have teleport access to that island yet."
NoTeleportOnShip = "Sorry, you can't teleport while on a ship."
NoTeleportInWater = "Sorry, you can't teleport while swimming."
NoTeleportInPVP = "Sorry, you can't teleport while in PVP."
NoTeleportInTutorial = "Sorry, you can't teleport yet."
NoTeleportCompass = "Sorry, you can't teleport until you have both your Cutlass and Compass."
NoTeleportVelvetRope = "Sorry, you can't teleport yet."
NoTeleportInTunnel = "Sorry, you can't teleport from here."
NoTeleportInTeleport = 'Sorry, you are already teleporting.'
NoTeleportInjured = "Sorry, you can't teleport while injured."
NoTeleportInJail = "Sorry, you can't teleport from jail."
NoTeleportParlorGame = "Sorry, you can't teleport while playing a parlor game."
NoTeleportFlagshipBattle = "Sorry, you can't teleport while aboard an enemy flagship."
NoTeleportPhaseIncomplete = "Sorry, you can't teleport until your download is complete."
NoTeleportLookoutJoined = "Sorry, you can't teleport while waiting to enter a Lookout game."
NoTeleportSiegeCaptain = "Sorry, you can't teleport while captaining a privateer ship."
NoTeleportTreasureMap = TeleportNotAvailable
NoTeleportZombie = 'Cannot teleport while undead!'
NoTeleportSameArea = 'You are already there!'
NoTeleportFishing = "Sorry, you can't teleport while fishing."
NoTeleportPotionCrafting = "Sorry, you can't teleport while brewing potions."
NoTeleportInScrimmage = "Sorry, you can't teleport while in a scrimmage."
TeleportPlayerNotAvailable = '%s is not available, try again later.'
NoTeleportToUnavailable = 'Sorry, %s is not available at the moment.'
NoTeleportToInPVP = 'Sorry, %s is in PVP at the moment.'
NoTeleportToInTutorial = 'Sorry, %s is still in the tutorial.'
NoTeleportToInTunnel = 'Sorry, %s is temporarily unavailable.'
NoTeleportToInTeleport = 'Sorry, %s is temporarily unavailable.'
NoTeleportToInJail = 'Sorry, %s is in jail.'
NoTeleportToNoPermission = "Sorry, %s is on a ship that\nyou don't have permission to board yet."
NoTeleportToFlagshipBattle = 'Sorry, %s is battling a flagship!'
NoTeleportToIgnore = 'Sorry, %s\\ is ignoring you.'
NoTeleportToNoSpaceOnShip = "Sorry, %s's ship is full at the moment."
NoTeleportToTreasureMap = TeleportPlayerNotAvailable
NoTeleportToWelcomeWorld = NoTeleportToInTutorial
NoTeleportToZombie = 'Sorry, %s is undead!'
NoTeleportCannonDefense = 'Sorry, %s is in a cannon defense game at the moment.'
NoTeleportToInScrimmage = 'Sorry, %s is in a scrimmage at the moment.'
NoInteractInBattle = "Sorry, you can't interact while in battle."
CollectionRarities = {
    0: 'Common',
    1: 'Uncommon',
    2: 'Rare'
}
CollectionPopupDuplicateText = '%s\nRarity: %s\nValue: %s'
CollectionPopupNewText = '%s \x01CPGreen\x01NEW!\x02\nRarity: %s\nValue: %s Gold'
Collections = {
    InventoryType.Collection_Set1: 'Valuables', InventoryType.Collection_Set1_Part1: 'Sapphire', InventoryType.Collection_Set1_Part2: 'Ruby', InventoryType.Collection_Set1_Part3: 'Gold Nugget', InventoryType.Collection_Set1_Part4: 'Silver Coin', InventoryType.Collection_Set1_Part5: 'Brass Locket', InventoryType.Collection_Set1_Part6: 'Small Diamond', InventoryType.Collection_Set1_Part7: 'Emerald', InventoryType.Collection_Set1_Part8: 'Crystal Vase', InventoryType.Collection_Set1_Part9: 'Sparkling Necklace', InventoryType.Collection_Set1_Part10: 'Copper Bits', InventoryType.Collection_Set1_Part11: 'Fire Opal', InventoryType.Collection_Set1_Part12: 'Gilded Anklet', InventoryType.Collection_Set1_Part13: 'Gold Cuff Links', InventoryType.Collection_Set1_Part14: 'White Gold Earring', InventoryType.Collection_Set1_Part15: 'Pearl Strand', InventoryType.Collection_Set1_Part16: 'Jade Toe Ring', InventoryType.Collection_Set1_Part17: 'Onyx Pendant', InventoryType.Collection_Set1_Part18: 'Turquoise Bangle', InventoryType.Collection_Set1_Part19: 'Amethyst', InventoryType.Collection_Set1_Part20: 'Topaz', InventoryType.Collection_Set2: 'Odds and Ends', InventoryType.Collection_Set2_Part1: 'Wood Carving', InventoryType.Collection_Set2_Part2: 'Flute', InventoryType.Collection_Set2_Part3: 'Silk Napkin', InventoryType.Collection_Set2_Part4: 'Cursed Idol', InventoryType.Collection_Set2_Part5: 'Shiny Rock', InventoryType.Collection_Set2_Part6: 'Gypsy Cloth', InventoryType.Collection_Set2_Part7: 'Shrunken Head', InventoryType.Collection_Set2_Part8: 'Glass Eye', InventoryType.Collection_Set2_Part9: 'Mouse Carving', InventoryType.Collection_Set2_Part10: 'Tiny Cage', InventoryType.Collection_Set2_Part11: 'Peacock Feather', InventoryType.Collection_Set2_Part12: 'Cricket in Amber', InventoryType.Collection_Set2_Part13: 'Protection Charm', InventoryType.Collection_Set2_Part14: 'Spices', InventoryType.Collection_Set2_Part15: 'Letter Opener', InventoryType.Collection_Set2_Part16: 'Navy Manacles', InventoryType.Collection_Set2_Part17: 'Glass Trinket', InventoryType.Collection_Set2_Part18: 'Sextant', InventoryType.Collection_Set2_Part19: 'Compass', InventoryType.Collection_Set2_Part20: 'Eerie Statue', InventoryType.Collection_Set3: 'The Nine Rogues', InventoryType.Collection_Set3_Part1: 'Captain Chevalle', InventoryType.Collection_Set3_Part2: 'Captain Barbossa', InventoryType.Collection_Set3_Part3: 'Mistress Ching', InventoryType.Collection_Set3_Part4: 'Captain Jack Sparrow', InventoryType.Collection_Set3_Part5: 'Gentleman Jocard', InventoryType.Collection_Set3_Part6: 'Sao Feng', InventoryType.Collection_Set3_Part7: 'Sri Sumhajee', InventoryType.Collection_Set3_Part8: 'Captain Ammand', InventoryType.Collection_Set3_Part9: 'Vallenueva', InventoryType.Collection_Set4: 'Navy Decorations', InventoryType.Collection_Set4_Part1: 'Valiant Cross', InventoryType.Collection_Set4_Part2: 'Conspicuous Attendance', InventoryType.Collection_Set4_Part3: 'Good Conduct Award', InventoryType.Collection_Set4_Part4: 'Distinguished Obedience Pin', InventoryType.Collection_Set4_Part5: 'Obsequious Order Badge', InventoryType.Collection_Set4_Part6: 'Illustrious Baton', InventoryType.Collection_Set4_Part7: 'Companion of Honor Medal', InventoryType.Collection_Set4_Part8: 'Sash of Pleasantry', InventoryType.Collection_Set4_Part9: 'Effort Ribbon', InventoryType.Collection_Set4_Part10: 'Pirate Slayer Mark', InventoryType.Collection_Set4_Part11: 'Royal Favor', InventoryType.Collection_Set4_Part12: 'Veteran Insignia', InventoryType.Collection_Set4_Part13: "Survivor's Medallion", InventoryType.Collection_Set4_Part14: 'Noteworthy Bravery Pin', InventoryType.Collection_Set5: "Rudyard's Teeth", InventoryType.Collection_Set5_Part1: 'Lateral Incisor', InventoryType.Collection_Set5_Part2: 'Central Incisor', InventoryType.Collection_Set5_Part3: 'Canine', InventoryType.Collection_Set5_Part4: 'Bicuspid', InventoryType.Collection_Set5_Part5: 'First Molar', InventoryType.Collection_Set5_Part6: 'Second Molar', InventoryType.Collection_Set5_Part7: 'Wisdom Tooth', InventoryType.Collection_Set6: 'Rhineworth Rings', InventoryType.Collection_Set6_Part1: 'Left Pinkie', InventoryType.Collection_Set6_Part2: 'Left Ring Finger', InventoryType.Collection_Set6_Part3: 'Left Middle Finger', InventoryType.Collection_Set6_Part4: 'Left Index Finger', InventoryType.Collection_Set6_Part5: 'Left Thumb', InventoryType.Collection_Set6_Part6: 'Right Thumb', InventoryType.Collection_Set6_Part7: 'Right Index Finger', InventoryType.Collection_Set6_Part8: 'Right Middle Finger', InventoryType.Collection_Set6_Part9: 'Right Ring Finger', InventoryType.Collection_Set6_Part10: 'Right Pinkie', InventoryType.Collection_Set6_Part11: 'Extra Digit', InventoryType.Collection_Set7: 'Treasured Chess Set', InventoryType.Collection_Set7_Part1: 'Silver Pawn', InventoryType.Collection_Set7_Part2: 'Silver Knight', InventoryType.Collection_Set7_Part3: 'Silver Bishop', InventoryType.Collection_Set7_Part4: 'Silver Rook', InventoryType.Collection_Set7_Part5: 'Silver Queen', InventoryType.Collection_Set7_Part6: 'Silver King', InventoryType.Collection_Set7_Part7: 'Gold Pawn', InventoryType.Collection_Set7_Part8: 'Gold Knight', InventoryType.Collection_Set7_Part9: 'Gold Bishop', InventoryType.Collection_Set7_Part10: 'Gold Rook', InventoryType.Collection_Set7_Part11: 'Gold Queen', InventoryType.Collection_Set7_Part12: 'Gold King', InventoryType.Collection_Set8: "Tia Dalma's Menagerie", InventoryType.Collection_Set8_Part1: 'Alligator Figure', InventoryType.Collection_Set8_Part2: 'Wasp Figure', InventoryType.Collection_Set8_Part3: 'Stump Figure', InventoryType.Collection_Set8_Part4: 'Fly Trap Figure', InventoryType.Collection_Set8_Part5: 'Scorpion Figure', InventoryType.Collection_Set8_Part6: 'Vampire Bat Figure', InventoryType.Collection_Set8_Part7: 'Rock Crab Figure', InventoryType.Collection_Set8_Part8: 'Fly Figure', InventoryType.Collection_Set8_Part9: 'Jaguar Figure', InventoryType.Collection_Set8_Part10: 'Shark Figure', InventoryType.Collection_Set8_Part11: 'Snake Figure', InventoryType.Collection_Set8_Part12: 'Wolf Figure', InventoryType.Collection_Set8_Part13: 'Cockroach Figure', InventoryType.Collection_Set8_Part14: 'Monkey Figure', InventoryType.Collection_Set8_Part15: 'Crow Figure', InventoryType.Collection_Set9: 'Cannons of the Deep', InventoryType.Collection_Set9_Part1: 'Broken Ramrod', InventoryType.Collection_Set9_Part2: 'Cannon Flint', InventoryType.Collection_Set9_Part3: 'Cannon Ring', InventoryType.Collection_Set9_Part4: 'Cannon Wheel', InventoryType.Collection_Set9_Part5: 'Dented Cannonball', InventoryType.Collection_Set9_Part6: 'Gunpowder Flask', InventoryType.Collection_Set9_Part7: 'Ignitor', InventoryType.Collection_Set9_Part8: 'Quoin', InventoryType.Collection_Set9_Part9: 'Recoil Rope', InventoryType.Collection_Set9_Part10: 'Sighting Scope', InventoryType.Collection_Set9_Part11: 'Silk Swab', InventoryType.Collection_Set9_Part12: 'Silver Ramrod', InventoryType.Collection_Set10: 'Fish', InventoryType.Collection_Set10_Part1: 'Yellow Tang', InventoryType.Collection_Set10_Part2: 'Bermuda Chub', InventoryType.Collection_Set10_Part3: 'Blue Chromis', InventoryType.Collection_Set10_Part4: 'Anthias', InventoryType.Collection_Set10_Part5: 'Tuna', InventoryType.Collection_Set10_Part6: 'Parrot Fish', InventoryType.Collection_Set10_Part7: 'Barracuda', InventoryType.Collection_Set10_Part8: 'Marlin', InventoryType.Collection_Set10_Part9: 'Sand Tiger Shark', InventoryType.Collection_Set10_Part10: 'Grouper', InventoryType.Collection_Set10_Part11: 'Coelacanth', InventoryType.Collection_Set10_Part12: 'Hatchet Fish', InventoryType.Collection_Set10_Part13: 'Lion Fish', InventoryType.Collection_Set10_Part14: 'Atlantic Wolffish', InventoryType.Collection_Set10_Part15: 'Black Chimera', InventoryType.Collection_Set10_Part16: 'Dragon Fish', InventoryType.Collection_Set10_Part17: 'Goblin Shark', InventoryType.Collection_Set10_Part18: 'Angler', InventoryType.Collection_Set10_Part19: 'Lump Fish', InventoryType.Collection_Set10_Part20: 'Mega Mouth', InventoryType.Collection_Set11: 'Legendary Fish', InventoryType.Collection_Set11_Part1: 'Fogbell', InventoryType.Collection_Set11_Part2: 'Fire Dragon', InventoryType.Collection_Set11_Part3: 'Glittering Girl', InventoryType.Collection_Set11_Part4: 'Mossy Moses', InventoryType.Collection_Set11_Part5: 'Speedy Lou'
}
ChatPanelReputationMsg = 'Earned %s %s reputation point.'
ChatPanelReputationMsgPlural = 'Earned %s %s reputation points.'
ChatPanelRepFreeMsg = 'Earned %s %s reputation points. (reduced by %s)'
ChatPanelLevelUpMsg = 'Level Up! %s Level %s'
ChatPanelQuestCompletedMsg = 'Quest Completed'
ChatPanelQuestUpdatedMsg = 'Quest Updated'
ChatPanelQuestAddedMsg = 'New Quest Added'
Loading = 'Loading...'
GuildRankMember = '\x01slant\x01Member\x02'
GuildRankLeader = '\x01slant\x01Guildmaster\x02'
GuildRankSubLead = '\x01slant\x01Officer\x02'
GuildRankInviter = '\x01slant\x01Veteran\x02'
GuildRankNames = {
    1: 'Member',
    2: 'Officer',
    3: 'Guildmaster',
    4: 'Veteran'
}
GameOptionsTitle = 'Game Options'
GameOptionsCustom = 'Custom'
GameOptionsVolume = 'Volume'
GameOptionsTextureCompressed = 'Compressed Textures'
GameOptionsAggressiveMemory = 'Aggressive Memory Conservation'
GameOptionsRenderedShadows = 'Rendered Shadows'
GameOptionsHardwareGamma = 'Hardware Gamma'
GameOptionsIntensity = 'Intensity'
GameOptionsVideo = 'Video'
GameOptionsDefaultConfirm = 'Are you sure you want the default settings?'
GameOptionsRestoreConfirm = 'Are you sure you want to restore the last settings?'
GameOptionsDisplay = 'Display'
GameOptionsGraphics = 'Graphics'
GameOptionsGeometry = 'Geometry'
GameOptionsAudio = 'Audio'
GameOptionsInterface = 'Interface'
GameOptionsTutorial = 'Tutorial'
GameOptionsImage = 'Image'
GameOptionsKeys = 'Controls'
GameOptionsWebEmbeddedMode = 'Web Page'
GameOptionsWindowedMode = 'Window'
GameOptionsFullscreenMode = 'Fullscreen'
GameOptionsFullscreenOnOff = 'Fullscreen On/Off'
GameOptionsWindowedResolutions = 'Windowed Resolutions'
GameOptionsFullscreenResolutions = 'Fullscreen Resolutions'
GameOptions640x480 = '640x480'
GameOptions800x600 = '800x600'
GameOptions1024x768 = '1024x768'
GameOptions1280x1024 = '1280x1024'
GameOptions1600x1200 = '1600x1200'
GameOptions1280x720 = '1280x720'
GameOptions1920x1080 = '1920x1080'
GameOptionsWidescreen = 'Widescreen'
GameOptionsFullscreen = 'Fullscreen'
GameOptionsReflections = 'Reflections'
GameOptionsSkyOnly = 'Sky Only'
GameOptionsAll = 'All'
GameOptionsStereo = '3D Glasses'
GameOptionsShaderLevel = 'Shader Level'
GameOptionsRestartRequired = '* = Application restart is required for change to take effect.'
GameOptionsEmbeddedRestriction = 'Window/Fullscreen take effect when the game begins.'
GameOptionsNoShader = 'Shader (Minimum Required Shader Hardware Not Detected)'
GameOptionsSmoothEdges = 'Smooth Edges'
GameOptionsShadows = 'Shadows'
GameOptionsSimple = 'Simple'
GameOptionsRendered = 'Rendered'
GameOptionsSpecialEffectsLevel = 'Special Effects Level'
GameOptionsTextureDetailLevel = 'Texture Detail Level'
GameOptionsLow = 'Low'
GameOptionsMedium = 'Medium'
GameOptionsHigh = 'High'
GameOptionsMaximum = 'Maximum'
GameOptionsCompressed = 'Compressed'
GameOptionsAggressive = 'Aggressive'
GameOptionsCharacterDetailLevel = 'Character Detail Level'
GameOptionsTerrainDetailLevel = 'Scenery Detail Level'
GameOptionsMemory = 'Memory Conservation'
GameOptionsShipVis = 'Ship Visibility from Islands'
GameOptionsShipVisOff = 'Off'
GameOptionsShipVisLow = 'Low'
GameOptionsShipVisHigh = 'High'
GameOptionsSoundEffects = 'Sound Effects'
GameOptionsSoundEffectsVolume = 'Sound Effects Volume'
GameOptionsMusic = 'Music'
GameOptionsMusicVolume = 'Music Volume'
GameOptionsFirstMate = 'First Mate Voice'
GameOptionsBackgroundAudio = 'Background Audio'
GameOptionsRotateCompassOnLand = 'Rotate Compass with Camera on Land'
GameOptionsRotateCompassAtSea = 'Rotate Compass with Camera at Sea'
GameOptionsInvertMouseLook = 'Invert Mouse Look'
GameOptionsFrameRate = 'Frame Rate Counter'
GameOptionsFancyLoadingScreen = 'Fancy Loading Screen'
GameOptionsShipLook = 'Ship Look Ahead'
GameOptionsGUIScale = 'Interface Scale'
GameOptionsChatFontScale = 'Smaller Chat Text'
GameOptionsChatboxScale = 'Chatbox Scale'
GameOptionsChatStyle = 'Solid Chat Colors'
GameOptionsCpuFrequencyWarning = 'Cpu Frequency Warning'
GameOptionsEnableGamma = 'Enable Hardware Gamma'
GameOptionsGamma = 'Gamma'
GameOptionsHdr = 'High Dynamic Range (Requires Shader On) *'
GameOptionsHdrIntensity = 'High Dynamic Range Intensity'
GameOptionsLogout = 'Logout'
GameOptionsDefault = 'Default'
GameOptionsOptions = 'Options'
GameOptionsRestore = 'Restore'
GameOptionsSave = 'Save'
GameOptionsClose = 'Close'
GameOptionsOn = 'On'
GameOptionsOff = 'Off'
GameOptionsContextTutPanels = 'Tutorial Game Hint Panels'
GameOptionsBasic = 'Disable Basic Game Hints'
GameOptionsIntermediate = 'Disable Intermediate Game Hints'
GameOptionsAdvanced = 'Disable Advanced Game Hints'
GameOptionsLogoutConfirm = 'Are you sure you want to logout?'
GameOptionsApplicationRestartMessage = 'For this option to take effect you must save the game options and restart application.'
GameOptionsSaved = 'Game Options Saved'
GameOptionsFailedToSaveOptions = 'Failed to Save Game Options'
GameOptionsOnLowerFrameRate = 'Turning this option on may result in a lower frame rate.'
GameOptionsNoteOnChange = 'Note: raising the graphics settings may increase lag and make the game run less smoothly.'
GameOptionsStereoOption = "Note: 3D display mode enabled. You'll need some Red-Blue 3D glasses to enjoy this feature."
TableLeave = 'Leave'
TableCancel = 'Cancel'
TableIsFullMessage = "You can't sit at this table since it is full."
TableWinGold = 'You won %s gold!'
TableCardsHelp = 'Cards can be obtained from quests.  To swap a card, first select which card to swap.  Then select a card suit.  Lastly select a card rank.'
Card2 = '2'
Card3 = '3'
Card4 = '4'
Card5 = '5'
Card6 = '6'
Card7 = '7'
Card8 = '8'
Card9 = '9'
CardT = 'T'
CardJ = 'J'
CardQ = 'Q'
CardK = 'K'
CardA = 'A'
PokerBet = 'Bet'
PokerCall = 'Call'
PokerCheat1 = 'Swap 1st\nCard'
PokerCheat2 = 'Swap 2nd\nCard'
PokerCheck = 'Check'
PokerFold = 'Fold'
PokerRaise = 'Raise'
PokerAllIn = 'All-In'
PokerBetAmount = 'Bet %s'
PokerCallAmount = 'Call %s'
PokerRaiseAmount = 'Raise to %s'
PokerBigBlindAmount = 'Big Blind %s'
PokerSmallBlindAmount = 'Small Blind %s'
PokerAllInAmount = 'All-In %s'
PokerPotZero = 'Pot: 0'
PokerPotAmount = 'Pot: %s'
PokerWaitingForOtherPlayers = 'Waiting for other players ...'
PokerWaitingForNextGame = 'Waiting for next hand ...'
PokerOutOfChipsMessage = 'You have run out of gold.'
PokerCaughtCheatingMessage = 'The dealer inspects the cards and you have been caught cheating!  You have lost all of your winnings and been fined %s gold.'
PokerInsufficientChipsMessage = "You don't have enough gold to sit at this table.  The minimum gold required to sit at this table is %s."
PokerSwapConfirmMessage = 'Are you sure you want to swap the %s with the %s?'
PokerLeaveConfirmMessage = 'Are you sure you want to leave the table?  If you leave, then any hand in play will be automatically folded.'
PokerUndeadLeaveConfirmMessage = 'Are you sure you want to leave the table?  You will lose %s gold from your quest progress!  Also, any hand in play will be automatically folded.'
PokerSwapSuccessMessage = 'Card swap attempt succeeded!'
PokerSwapFailureMessage = 'Card swap attempt failed.'
PokerChatWinGoldMessage = '%s wins %s gold.'
PokerChatCaughtCheatingMessage = '%s has been caught cheating!'
PokerSitDownPoker = 'Poker'
PokerSitDownHoldEmPoker = "Tortuga Hold'em Poker"
PokerSitDown7StudPoker = '7 Stud Poker'
PokerYouLost = 'You Lost'
VR_Head_StayTuned1 = 'Stay tuned for the next Pirates of the Caribbean Online Expansion!'
VR_Head_StayTuned2 = 'Stay tuned for the next Pirates of the Caribbean Online Expansion!'
VR_UpgradeNow = '\x01smallCaps\x01Upgrade Now!\x02'
VR_UpgradeLater = '\x01smallCaps\x01Continue Playing\x02'
VR_DismissNow = 'Upgrade Later'
VR_Head_Combat = 'Upgrade your account to continue this quest!'
VR_Head_Quest = 'Upgrade your account to take part in this quest!'
VR_Head_Trial = 'Your 7-Day Full-Screen Preview Has Expired'
VR_Head_Guild = 'Upgrade your account to create your own Pirate Guild!'
VR_Head_Island = 'Upgrade your account to gain access to this high-level area!'
VR_Head_Ship = 'Upgrade your account to gain access to additional ships!'
VR_Head_Account = 'Upgrade your account to create more Pirates!'
VR_Head_Weapon = 'Upgrade your account to gain access to additional weapons and skills!'
VR_Head_PVP = 'Upgrade your account to gain access to additional PVP maps and game types!'
VR_Head_Parlor = 'Upgrade your account to gain access to additional parlor games!'
VR_Head_Treasure = 'Upgrade your account to complete this treasure collection!'
VR_Head_Customize = 'Upgrade your account to customize your Pirate with exclusive items!'
VR_StayTuned1 = '-  Coming soon: More fabulous places to explore\n-  More pirate adventures with Jack and friends\n-  Fiendish foes to test your mettle'
VR_StayTuned2 = '-  Coming soon: More fabulous places to explore\n-  More pirate adventures with Jack and friends\n-  Fiendish foes to test your mettle'
VR_Access = '\x01uline\x01Experience Unlimited Access - Click here for details\x02'
VRCustomizeBlurb = 'Customize your Pirates with exclusive clothing, jewelry, and tattoos'
VR_Combat = "You'll also gain access to these exclusive game features:\n   -  Unlock advanced weapons and skills\n   -  " + VRCustomizeBlurb + '\n   -  Captain bigger and better ships...and more!'
VR_Quest = "You'll also gain access to these exclusive game features:\n   -  " + VRCustomizeBlurb + '\n   -  Unlock advanced weapons and skills\n   -  Captain bigger and better ships... and more!'
VR_Trial = 'You can continue to play in windowed mode with free Basic Access or you can upgrade to Unlimited Access for expanded features including full-screen game play.'
VR_Guild = "You'll also gain access to these exclusive game features:\n   -  Unlock advanced weapons and skills\n   -  Captain bigger and better ships\n   -  " + VRCustomizeBlurb
VR_Island = "You'll also gain access to these exclusive game features:\n   -  Unlock advanced weapons and skills\n   -  Embark on expanded quests\n   -  " + VRCustomizeBlurb
VR_Ship = "You'll also gain access to these exclusive game features:\n   -  Unlock more powerful weapons and skills\n   -  Engage in expanded pirate-versus-pirate combat\n   -  " + VRCustomizeBlurb
VR_Account = "You'll also gain access to these exclusive game features:\n   -  " + VRCustomizeBlurb + '\n   -  Unlock advanced weapons and skills\n   -  Captain bigger and better ships....and more!'
VR_Weapon = "You'll also gain access to these exclusive game features:\n   -  Captain bigger and better ships\n   -  " + VRCustomizeBlurb + '\n   -  Engage in expanded pirate-versus-pirate combat... and more!'
VR_PVP = "You'll also gain access to these exclusive game features:\n   -  Unlock more powerful weapons and skills\n   -  Create and lead your own powerful Pirate guild\n   -  Captain bigger and better ships... and more!"
VR_Parlor = "You'll also gain access to these exclusive game features:\n   -  Unlock more powerful weapons and skills\n   -  Captain bigger and better ships\n   -  " + VRCustomizeBlurb
VR_Treasure = "You'll also gain access to these exclusive game features:\n   -  Embark on expanded quests\n   -  " + VRCustomizeBlurb + '\n   -  Captain bigger and better ships... and more!'
VR_Customize = "You'll also gain access to these exclusive game features:\n   -  Unlock advanced weapons and skills\n   -  Captain bigger and better ships\n   -  Create and lead your own Pirate Guild... and more!"
VR_Cap_StayTuned1 = 'Next Expansion in the Works'
VR_Cap_StayTuned2 = 'More Pirate Adventures'
VR_Cap_Parlor1 = 'Play a variety of games'
VR_Cap_Parlor2 = 'Enjoy members-only games'
VR_Cap_Combat1 = 'Retake the Pearl'
VR_Cap_Combat2 = 'Grab the Horizon'
VR_Cap_Trial1 = 'Live the adventure!'
VR_Cap_Trial2 = 'More pirate loot awaits!'
VR_Cap_Quest1 = 'Extend your adventure'
VR_Cap_Quest2 = 'Fully level up your character'
VR_Cap_Ship1 = 'Captain more powerful ships'
VR_Cap_Ship2 = 'Become a legend of the seas'
VR_Cap_Weapon1 = 'Master advanced weapons'
VR_Cap_Weapon2 = 'More powerful ammo and skills'
VR_Cap_Account1 = 'Unleash more characters'
VR_Cap_Account2 = 'Create a variety of Pirates'
VR_Cap_Treasure1 = 'Discover more treasure'
VR_Cap_Treasure2 = 'Complete your collection'
VR_Cap_Guild1 = 'Build a powerful Guild'
VR_Cap_Guild2 = 'Lead them into battle'
VR_Cap_Island1 = 'Explore the dangerous island of Kingshead'
VR_Cap_Island2 = 'Defeat high level Navy Officers'
VR_Cap_PVP1 = 'More PVP Maps'
VR_Cap_PVP2 = 'More PVP Games'
VR_Cap_Customize1 = 'More clothing & unique items'
VR_Cap_Customize2 = 'Stand out from the crowd'
VR_FeaturePopTitle = 'Sorry Mate...'
VR_FeaturePopLongText = 'This feature requires Unlimited Access Membership.\nJoin the crew of advanced players to experience\nall the Caribbean has to offer.'
VR_FeaturePopLongTextAvatars = 'Creating more Pirates requires Unlimited Access Membership.\nJoin the crew of advanced players to experience\nall the Caribbean has to offer.'
VR_AuthAccess = '\x01smallCaps\x01Unlimited Access Members Only\x02'
VR_StayTuned = 'Stay Tuned for More Adventures'
VR_MemberOnly = 'This feature is for Unlimited Access Members only!'
VR_LongText = "Unlock the full Pirate adventure waiting for you now!  See what additional help Jack and his friends need!  Can you survive Davy Jones' wrath?  Learn new skills and new weapons!  Gain full mastery of the skills you currently possess.  Open new PVP and Parlor gaming modes!"
TableIsFullMessage = "You can't sit at this table since it is full."
BlackjackHand = 'Blackjack'
BlackjackStay = 'Stay'
BlackjackHit = 'Hit'
BlackjackBid = 'Bid'
BlackjackDoubleDown = 'Double\nDown'
BlackjackSplit = 'Split'
BlackjackCardSwap = 'Swap\nCard'
BlackjackHandofHand = 'Hand %s of %s'
BlackjackBusted = 'Busted  %s'
BlackjackSitDownBlackjack = 'Blackjack'
BlackjackDealerWins = 'Dealer Wins'
ComboOrderWarn = 'Combo skills must be unlocked in order.'
TutorialSweepWarn = 'You must unlock Sweep on Cutlass upgrade.'
noFreebooterCap = 'Unlimited Access Only'
FreebooterSkillLock = '\x01Ired\x01Basic Members may spend only 6 skill points per category.\x02'
FreebooterSkillMax = '\x01Ired\x01Basic Members may raise skills to no more than rank 2.\x02'
FreebooterDisallow = '\x01Ired\x01Locked for Basic Members\x02'
Freebooter = 'Basic Member'
GuildPrefix = '(G):'
CrewPrefix = '(C):'
PVPPrefix = '(P):'
TalkGMLabel = 'GM'
TalkCrewLabel = 'Crew'
TalkCrewFull = 'Crew'
TalkGuildLabel = 'Guild'
TalkGuildFull = 'Guild'
TalkPrivateerLabel = ''
PVPSpanish = 'Spanish'
PVPFrench = 'French'
LocationUids = {
    'isla de la avaricia': LocationIds.ISLA_AVARICIA,
    'avaricia': LocationIds.ISLA_AVARICIA,
    'isla cangrejos': LocationIds.ISLA_CANGREJOS,
    'cangrejos': LocationIds.ISLA_CANGREJOS,
    'cuba': LocationIds.CUBA_ISLAND,
    'cutthroat': LocationIds.CUTTHROAT_ISLAND,
    'cutthroat isle': LocationIds.CUTTHROAT_ISLAND,
    'devils anvil': LocationIds.ANVIL_ISLAND,
    "devil's anvil": LocationIds.ANVIL_ISLAND,
    'driftwood': LocationIds.DRIFTWOOD_ISLAND,
    'driftwood island': LocationIds.DRIFTWOOD_ISLAND,
    "ile d'etable de porc": LocationIds.ISLA_DE_PORC,
    'kingshead': LocationIds.KINGSHEAD_ISLAND,
    'outcast': LocationIds.OUTCAST_ISLE,
    'outcast isle': LocationIds.OUTCAST_ISLE,
    'padres del fuego': LocationIds.DEL_FUEGO_ISLAND,
    'isla perdida': LocationIds.ISLA_PERDIDA,
    'perdida': LocationIds.ISLA_PERDIDA,
    'port royal': LocationIds.PORT_ROYAL_ISLAND,
    'rumrunner': LocationIds.RUMRUNNER_ISLE,
    'rumrunners': LocationIds.RUMRUNNER_ISLE,
    "rumrunner's": LocationIds.RUMRUNNER_ISLE,
    'rumrunners isle': LocationIds.RUMRUNNER_ISLE,
    "rumrunner's isle": LocationIds.RUMRUNNER_ISLE,
    'isla tormenta': LocationIds.ISLA_TORMENTA,
    'tormenta': LocationIds.ISLA_TORMENTA,
    'tortuga': LocationIds.TORTUGA_ISLAND,
    'antigua': LocationIds.ANTIGUA_ISLAND,
    'nassau': LocationIds.NASSAU_ISLAND 
}
LocationNames = {
    LocationIds.PORT_ROYAL_ISLAND: 'Port Royal',
    LocationIds.PORT_ROYAL_PORT: 'Port Royal Town', 
    LocationIds.PORT_ROYAL_CAVE_A: 'Royal Caverns', 
    LocationIds.PORT_ROYAL_CAVE_B: 'Murky Hollow', 
    LocationIds.PORT_ROYAL_JUNGLE_A: "Governor's Garden", 
    LocationIds.PORT_ROYAL_JUNGLE_B: "King's Run", 
    LocationIds.PORT_ROYAL_JUNGLE_C: 'Wicked Thicket', 
    LocationIds.FORT_CHARLES: 'Fort Charles', 
    LocationIds.FULLERS_BLACKSMITH: "Fuller's Blacksmithing", 
    LocationIds.JUNEGREER_RESIDENCE: 'June Greer Residence', 
    LocationIds.SMITTYS_JEWELRY: "Smitty's Jewelry Shoppe", 
    LocationIds.ROWDYROOSTER_TAVERN: 'Rowdy Rooster', 
    LocationIds.ROYALANCHOR_TAVERN: 'Royal Anchor', 
    LocationIds.GRAHAM_IMPORTS: 'Graham Marsh Imports', 
    LocationIds.EWANS_WEAPONS: "Ewan's Gunnery", 
    LocationIds.OLD_WAREHOUSE: 'Old Warehouse', 
    LocationIds.RSMITH_PEWTERER: 'R. Smith, Pewterer', 
    LocationIds.SOLOMONS_TATTOOS: "Solomon's Tattoo Parlor", 
    LocationIds.BASILS_BARBER: "Basil's Barbershop", 
    LocationIds.BLAKELEYS_RESIDENCE: "Blakeley's residence", 
    LocationIds.TURNBULLS_WEAPONS: "Turnbull's Weaponry", 
    LocationIds.WALLACE_BLACKSMITH: 'Wallace Blacksmith Shop', 
    LocationIds.TRUEHOUNDS_TAILOR: "Truehound's Tailor Shop", 
    LocationIds.MCCRAKENS_WEAPONS: "McCraken's Weaponry", 
    LocationIds.PORT_ROYAL_JAIL: 'Port Royal Jail', 
    LocationIds.GOVERNORS_MANSION: "Governor's Mansion", 
    LocationIds.TORTUGA_ISLAND: 'Tortuga', 
    LocationIds.TORTUGA_PORT: 'Tortuga Town', 
    LocationIds.TORTUGA_JUNGLE_A_GRAVEYARD: 'Tortuga Graveyard', 
    LocationIds.TORTUGA_CAVE: 'Thieves Den', 
    LocationIds.TORTUGA_JUNGLE_C: 'Wildwoods', 
    LocationIds.TORTUGA_SWAMP: 'Misty Mire', 
    LocationIds.TORTUGA_JUNGLE_B_SWAMPY: "Rat's Nest", 
    LocationIds.FAITHFULBRIDE_TAVERN: 'Faithful Bride', 
    LocationIds.KINGSARM_TAVERN: "King's Arm", 
    LocationIds.BOWDASH_MANSION: 'Bowdash Mansion', 
    LocationIds.WRIGHTS_BLACKSMITH: "Wright's Blacksmithing", 
    LocationIds.FLATTS_WEAPONS: 'Flatts & Flatts, Importers', 
    LocationIds.VALLANCE_WEAPONS: 'Daniel Vallance Weaponry', 
    LocationIds.SEAMSTRESS_TAILOR: "Seamstress Anne's Shop", 
    LocationIds.DOCTOR_GROGS: "Doc Grog's", 
    LocationIds.FLINTYS_BLACKSMITH: "Flinty's Smithery", 
    LocationIds.TRADING_COMPANY: 'Trading Co. Office', 
    LocationIds.ORINDAS_SHACK: "Orinda's Shack", 
    LocationIds.BOATSWAINS_HOUSE: "Boatswain's house", 
    LocationIds.THAYERS_WEAPONS: 'Thayers Weapons Shop', 
    LocationIds.MILLIES_COTTAGE: "Millie's Cottage", 
    LocationIds.CALLECUTTERS_TAILOR: "Callecutter's Tailor Shoppe",
    LocationIds.LOCKSPINNERS_BARBER: "Lockspinner's Barber and Beauty Shop", 
    LocationIds.MINGS_JEWELRY: "Ming's Jewelry Shop", 
    LocationIds.BONITAS_TATTOOS: "Bonita's Tattoo Parlor", 
    LocationIds.SHIPCRASH_WEAPONS: 'Edgar Shipcrash Weaponry', 
    LocationIds.TORTUGA_JAIL: 'Tortuga Jail', 
    LocationIds.EITC_OUTPOST: 'EITC Outpost', 
    LocationIds.DEL_FUEGO_ISLAND: 'Padres Del Fuego', 
    LocationIds.DEL_FUEGO_JUNGLE_B: 'El Sudoron', 
    LocationIds.DEL_FUEGO_CAVE_D: "Beckett's Quarry", 
    LocationIds.DEL_FUEGO_CAVE_E: 'The Catacombs', 
    LocationIds.DEL_FUEGO_CAVE_C: 'Lava Gorge', 
    LocationIds.DEL_FUEGO_FORT_DUNDEE: 'Fort Dundee', 
    LocationIds.SKULLSTHUNDER_TAVERN: "Skull's Thunder", 
    LocationIds.RATSKELLAR_TAVERN: 'Ratskellar', 
    LocationIds.FERRERAS_BLACKSMITH: "Ferrera's Blacksmith Shop", 
    LocationIds.GRIMSDITCH_WEAPONS: 'Grimsditch Gunsmithing', 
    LocationIds.DEAFGUNNYS_WEAPONS: "Deaf Gunny's Weapons shop", 
    LocationIds.PETES_WEAPONS: "Powder-Burnt Pete's Weaponry", 
    LocationIds.ANTONLEVY_BLACKSMITH: 'Anton Levy Smithery', 
    LocationIds.THORHAMMER_BLACKSMITH: 'Thorhammer Blacksmithing', 
    LocationIds.CORAZON_TATTOOS: 'Corazon Tattoos', 
    LocationIds.GUNNERS_SHACK: "Gunner's shack", 
    LocationIds.GARRETTS_HOUSE: "Garrett's Imports and Exports", 
    LocationIds.GOSLIN_TAVERN: "Goslin Prymme's", 
    LocationIds.DOLORES_TAILOR: 'Dolores Tailoring Shoppe', 
    LocationIds.PERLAS_JEWELRY: "Perla's Jewelry and Gems", 
    LocationIds.CESARS_BARBER: "Cesar's Barbershop", 
    LocationIds.FLAVIOS_BARBER: "Flavio's Barbershop", 
    LocationIds.BLANCAS_TAILOR: "Blanca's Tailor Shop", 
    LocationIds.FOUSTOS_JEWELRY: "Fousto's Jewelry Shop", 
    LocationIds.NINAS_TATTOOS: "Nina's Tattoo Parlor", 
    LocationIds.DEL_FUEGO_JAIL: 'Padres Del Fuego Jail', 
    '1156207578.91dzlu': 'Home of Bowdash', 
    LocationIds.ANVIL_ISLAND: "Devil's Anvil", 
    LocationIds.ANVIL_CAVE_BARBOSA: "Barbossa's Grotto", 
    LocationIds.DRIFTWOOD_ISLAND: 'Driftwood Island', 
    LocationIds.RUMRUNNER_ISLE: "Rumrunner's Isle", 
    LocationIds.RUMRUNNER_CELLAR: 'Rum Cellar', 
    LocationIds.ISLA_PERDIDA: 'Isla Perdida', 
    LocationIds.PERDIDA_JUNGLE_B: "Queen's Nest", 
    LocationIds.OUTCAST_ISLE: 'Outcast Isle', 
    LocationIds.CUBA_ISLAND: 'Cuba', 
    LocationIds.CUBA_SWAMP: 'Pantano River', 
    LocationIds.LA_BODEGUITA: 'La Bodeguita', 
    LocationIds.DAGGERFLINTS_TATTOOS: "Daggerflint's Tattoo Shop", 
    LocationIds.PUGPRATTS_TAILOR: "Pugpratt's Tailoring", 
    LocationIds.CUBA_JAIL: 'Cuba Jail', '1189479168.0sdnaik0': 'Kingshead', 
    LocationIds.KINGSHEAD_ISLAND: 'Kingshead', 
    '1190336896.0dxschafe': 'Kingshead Depot', 
    '1190397568.0dxschafe0': 'Kingshead Armory', 
    '1190397824.0dxschafe': 'Marching Grounds', 
    '1190397568.0dxschafe': 'Kingshead Barracks', 
    '1190397568.0dxschafe1': 'Kingshead Keep', 
    LocationIds.KINGSHEAD_JAIL: 'Kingshead Jail', 
    LocationIds.ISLA_CANGREJOS: 'Isla Cangrejos', 
    LocationIds.ISLA_TORMENTA: 'Isla Tormenta', 
    LocationIds.TORMENTA_CAVE_B: 'Cursed Caverns', 
    LocationIds.CUTTHROAT_ISLAND: 'Cutthroat Isle', 
    LocationIds.CUTTHROAT_JUNGLE: 'Cutthroat Jungle', 
    '1171761224.13sdnaik': 'Black Pearl Bay', 
    '1161805620.28Shochet': 'Parlor Games', 
    '1161805620.28Shochet0': 'Underground Parlor Games', 
    LocationIds.CANNON_DEFENSE: 'Cannon Defense', 
    LocationIds.RAVENS_COVE_ISLAND: "Raven's Cove", 
    LocationIds.RAVENS_COVE_MINE: "El Patron's Mine", 
    LocationIds.RAVENS_COVE_SHIP: "El Patron's Ship", 
    LocationIds.RAVENS_COVE_JAIL: "Raven's Cove Jail", 
    LocationIds.RAVENS_COVE_CAVE: 'Cave of Lost Souls', 
    LocationIds.PORT_ROYAL_ALL: 'Port Royal', 
    LocationIds.TORTUGA_ALL: 'Tortuga', 
    LocationIds.DEL_FUEGO_ALL: 'Padres Del Fuego', 
    LocationIds.ANVIL_ALL: "Devil's Anvil", 
    LocationIds.DRIFTWOOD_ALL: 'Driftwood Island', 
    LocationIds.RUMRUNNER_ALL: "Rumrunner's Isle", 
    LocationIds.PERDIDA_ALL: 'Isla Perdida', 
    LocationIds.OUTCAST_ALL: 'Outcast Isle', 
    LocationIds.CUBA_ALL: 'Cuba', 
    LocationIds.KINGSHEAD_ALL: 'Kingshead', 
    LocationIds.CANGREJOS_ALL: 'Isla Cangrejos', 
    LocationIds.CUTTHROAT_ALL: 'Cutthroat Isle', 
    LocationIds.TORMENTA_ALL: 'Isla Tormenta', 
    LocationIds.RAVENS_COVE_ALL: "Raven's Cove", 
    LocationIds.ANY_LARGE_ISLAND: 'Any Large Island', 
    LocationIds.ANY_LARGE_PORT: 'Any Large Island', 
    LocationIds.ANY_WILD_ISLAND: 'Any Wild Island', 
    LocationIds.ANY_WILD_PORT: 'Any Wild Island', 
    LocationIds.ANY_LOCATION: 'Anywhere', 
    LocationIds.ANY_PORT_ROYAL_JUNGLE: 'Any Port Royal Jungle', 
    LocationIds.ANY_PORT_ROYAL_CAVE: 'Any Port Royal Cave', 
    LocationIds.WINDWARD_PASSAGE: 'Windward Passage', 
    LocationIds.BRIGAND_BAY: 'Brigand Bay', 
    LocationIds.BLOODY_BAYOU: 'Bloody Bayou', 
    LocationIds.SCURVY_SHALLOWS: 'Scurvy Shallows', 
    LocationIds.BLACKHEART_STRAIT: 'Blackheart Strait', 
    LocationIds.SALTY_FLATS: 'Salty Flats', 
    LocationIds.MAR_DE_PLATA: 'Mar de Plata', 
    LocationIds.SMUGGLERS_RUN: 'Smugglers Run', 
    LocationIds.THE_HINTERSEAS: 'The Hinterseas', 
    LocationIds.DEAD_MANS_TROUGH: "Dead Man's Trough", 
    LocationIds.LEEWARD_PASSAGE: 'Leeward Passage', 
    LocationIds.BOILING_BAY: 'Boiling Bay', 
    LocationIds.MARINERS_REEF: 'Mariners Reef', 
    LocationIds.UNCHARTED_WATERS: 'Uncharted Waters', 
    LocationIds.THE_HIGH_SEAS: 'The High Seas', 
    LocationIds.MOLTEN_CAVERN: 'Molten Cavern', 
    LocationIds.BOULDER_HILL: 'Boulder Hill', 
    LocationIds.PILLAGERS_PASS: 'Pillagers Pass', 
    LocationIds.ISLA_AVARICIA: 'Isla de la Avaricia', 
    LocationIds.ISLA_DE_PORC: "Ile d'Etable de Porc", 
    LocationIds.PORCS_TAVERN: "Porc's Tavern", 
    LocationIds.AVARICIAS_TAVERN: "Avaricia's Tavern",
    LocationIds.ANTIGUA_ISLAND: 'Antigua',
    LocationIds.NASSAU_ISLAND : 'Nassau',
    LocationIds.MADRE_DEL_FUEGO_ISLAND: 'Madre Del Fuego'
}
LocationNamesNotIsland = {
    LocationIds.PORT_ROYAL_ISLAND: 'Port Royal Town', LocationIds.TORTUGA_ISLAND: 'Tortuga Town', LocationIds.DEL_FUEGO_ISLAND: 'Padres Del Fuego Town', LocationIds.ANVIL_ISLAND: 'Anvil Island Beach', LocationIds.CUBA_ISLAND: 'Cuba Beach'
}
PropTypeNames = {
    PropIds.ANY_PROP: ('a storage container', 'storage containers'), PropIds.ANY_BARREL: ('a barrel', 'barrels'), PropIds.ANY_CRATE: ('a crate', 'crates'), PropIds.ANY_DESK: ('a desk', 'desks'), PropIds.ANY_SHELF: ('a shelf', 'shelves'), PropIds.ANY_CABINET: ('a cabinet', 'cabinets'), PropIds.ANY_CLOCK: ('a clock', 'clocks'), PropIds.ANY_HAYSTACK: ('a haystack', 'haystacks'), PropIds.ANY_WELL: ('a well', 'wells'), PropIds.ANY_GRAVE: ('a grave', 'graves'), PropIds.WATER_GRAVE: ('a watery grave', 'watery graves'), PropIds.SOUTH_GRAVE: ('the southern grave', 'southern graves'), PropIds.ANY_CHEST: ('a treasure chest', 'treasure chests'), PropIds.ANY_MINE_SHAFT: ('a mine shaft', 'mine shafts')
}
UNDEAD_SPANISH_NAMES = (
    'Undead Spanish Soldier', 'Undead Spanish Soldiers')
UNDEAD_FRENCH_NAMES = ('Undead French Soldier', 'Undead French Soldiers')
LoadingScreen_PickAPirate = ''
LoadingScreen_Jail = 'Jail'
LoadingScreen_Ocean = 'The High Seas'
LoadingScreen_Hint = 'Hint'
GeneralTip1 = 'Plunder ships for Cargo in order to quickly get Gold!'
GeneralTip2 = 'Defeat skeletons to find rare Treasure Collection valuables.'
GeneralTip3 = 'Going to jail makes you groggy. While groggy, your Health and Voodoo Power will be temporarily reduced.'
GeneralTip4 = 'Use the Map Page (M) to change Servers!'
GeneralTip5 = 'Players cannot hurt each other except in PvP Matches!'
GeneralTip6 = "If you are alone, don't fight too many enemies at once!"
GeneralTip7 = "You can open an expanded map of the area you're in by pressing F8 or the map button on your compass."
ControlTip1 = 'You can use the WASD Keys to move.'
ControlTip2 = 'Press the Space Bar to jump.'
ControlTip3 = 'Use the Left Mouse Button or the CTRL Button to attack.'
ControlTip4 = 'Use the Right Mouse Button to move the Camera.'
ControlTip5 = 'Press R to enable Auto-run!'
ControlTip6 = 'While using Auto-run (R), you can run and chat at the same time!'
ControlTip9 = 'To steer a Ship, grab the Steering Wheel!'
ControlTip10 = "To fire a Ship's Broadsides, grab the Steering Wheel!"
ControlTip11 = 'Crew Members on a Ship should grab a cannon and fire!'
ControlTip12 = 'Sail near an Island and click on the Anchor Button to dock!'
OptimizeTip1 = 'If the game is running slowly, you can lower your graphics settings by pressing F7!'
TonicTip1 = 'You can buy health Tonics from the Gypsy!'
TonicTip2 = 'When you are low on health, Hit T to use a Tonic!'
TonicTip3 = 'Purchase the weaker healing Tonics until you are Level 10 or higher.'
QuestTip1 = 'Look for a Ray of Light if you get lost.'
QuestTip2 = 'Use the Journal (J) to find your next quest objective.'
QuestTip3 = "If you're not sure where to go for a Quest, search the skies for the Ray of Light."
QuestTip4 = 'If you get lost, teleport back to your Port of Call using the Map Page (M)!'
QuestTip5 = 'To navigate the map on the Map Page (M), click and drag it with the Left Mouse Button.'
QuestTip6 = 'Completing Story Quests rewards the most Notoriety!'
QuestTip7 = 'Complete the Teleport Quests as soon as possible. It will make other quests easier to complete.'
QuestTip8 = 'Complete your Weapon Quest to unlock the Voodoo Doll weapon!'
ShipTip0 = 'Maneuver your ship so that your broadside cannons line up with the enemy before firing!'
ShipTip1 = 'Repair a sunken ship at the Shipwright!'
ShipTip2 = 'While sailing, hold down the Right Mouse Button to move the Camera.'
ShipTip3 = 'Find a Crew to help man your ship before going sailing!'
ShipTip4 = "Don't sail alone! Other crewmates can fire cannons while you are steering!"
ShipTip5 = 'When sailing, use the Middle Mouse Wheel to move the Camera in and out!'
ShipTip6 = 'A ship cannot be reduced to zero Sail Points without destroying all the Masts!'
ShipTip7 = "Concentrate your cannon fire on the same section of a ship's Hull until it breaks!"
ShipTip8 = "Shooting a ship's sails will not sink it, but can slow it down!"
ShipTip9 = 'Sailing in a straight line allows your ship to move faster!'
ShipTip10 = 'Higher level ships carry better Cargo.'
ShipTip11 = 'Ships cost more to repair after they are sunk!'
ShipTip12 = 'Cannonballs that hit the Rear of a Ship gain a damage bonus!'
ShipTip13 = 'Sink ships with Cannons to become a better Cannoneer!'
ShipTip14 = 'Sink ships with Broadsides to gain Sailing Reputation!'
ShipTip15 = 'Level-up your Cannon Skill to unlock new Cannon Ammo types!'
ShipTip16 = 'Level-up your Sailing Skill to unlock new Ship Maneuvers and Battle Orders!'
ShipTip17 = 'Different cannonballs are effective against different parts of a ship!'
ShipTip18 = 'Break all the Masts on an enemy ship to stop it from moving!'
ShipTip19 = 'If a player exits the game and his ship has a Crew, the ship stays in use until the voyage ends!'
ShipTip20 = 'If your ship sinks at sea, all your cargo is lost!'
ShipTip21 = 'To sink a ship, aim for the Hull!'
ShipTip22 = 'Expensive ships cost more to repair!'
ShipTip23 = 'If you shoot the same part of a ship, the panel will break, catch fire, and give a damage bonus!'
ShipTip24 = "If one side of a ship's hull is broken, the ship will take extra damage on that side!"
ShipTip25 = "If one side of your ship's hull is broken, avoid taking more fire on that side!"
ShipTip26 = 'Be careful not to take too much damage on the same section of your hull!'
ShipTip27 = "Use the Boarding Access button on your Ship's Health Display to control who can board your ship!"
ShipTip28 = "Looking to join a ship's crew? Use a Dinghy and search for Public Ships!"
ShipTip29 = 'Looking for a crew for your ship? Set the Boarding Access for your ship to Public!'
FlagShipTip1 = 'Ships with a Flag Icon above them are Flagships. They need to be crippled and then boarded!'
FlagShipTip2 = 'Get a crew together before boarding a Flagship!'
FlagShipTip3 = 'Flagship boarding rights are given to the crew who dealt the most damage to it!'
FlagShipTip4 = 'Flagships give more cargo than regular ships!'
FriendTip1 = 'Click on other players to Crew up! Make sure you put away your weapon first!'
FriendTip2 = "You can board a Crew Member's ship from the Dinghy!"
FriendTip3 = 'Rule #1 of the pirate code: Befriend others wisely!'
FriendTip4 = 'Click on other players to make Friends! Make sure you put away your weapon first!'
FriendTip5 = 'Team up with other players against tough enemies!'
FriendTip6 = 'If a friend is in need, teleport to them using the Friends Page (F)!'
ChatTip1 = "If you type a '.' in the chat window before typing, the message will appear as a thought bubble and will stay longer."
TreadmillTip1 = 'Spend skill upgrades wisely. It will cost gold to change your choices later!'
TreadmillTip2 = 'Visit a Trainer at the local blacksmith to retrain your weapons. \n Retraining a weapon refunds all your spent skill points.'
TreadmillTip3 = 'Spending a Skill Point on an attack skill increases its damage 25%!'
TreadmillTip4 = 'Spending a Skill Point on an attack skill increases any Buff duration by 25%!'
TreadmillTip5 = 'Enemies who are lower level than you award less Reputation and Gold!'
TreadmillTip6 = 'Members of a Crew gain a Reputation Bonus for every enemy defeated.  Larger crews provide larger bonuses!'
TreadmillTip7 = 'The Captain of a ship receives a larger share of loot if he has a Crew onboard!'
TreadmillTip8 = 'The pirate steering the ship gains more Sailing Reputation if the ship has a Crew!'
TreadmillTip9 = 'As you Level-up your Cutlass, unlock new Combo Skills for a longer Combo Chain!'
TreadmillTip10 = 'As you Level-up your Pistol, unlock Take-Aim to pick-off enemies from long range!'
CombatTip1 = 'If you are not in battle, your Health will regenerate slowly. \n Avoid fighting until you are fully healed.'
CombatTip2 = 'A Cutlass Combo deals much more damage than just button-mashing!'
CombatTip3 = 'You can aim your attacks by holding down the Right Mouse Button!'
CombatTip4 = 'Watch your Cutlass attack timing to form Combos!'
CombatTip5 = "Don't attack enemies who are much higher level than you!"
CombatTip6 = "You're vulnerable to attack while you dig for buried treasure, so stay alert."
CombatTip7 = 'Switch Weapons using the F1 to F4 Keys!'
CombatTip8 = 'You can also use the Mouse Wheel to Switch Weapons!'
CombatTip9 = 'Clicking the Middle Mouse Button also draws your current Weapon!'
CombatTip10 = 'You can use the Number Keys to activate your Combat Skills or Switch Ammo!'
CombatTip11 = 'The Voodoo Doll will lose Attunement if you get too far away from your target!'
CombatTip12 = 'Voodoo Doll healers gain healing Reputation when their ally defeats their foe!'
CombatTip13 = 'You can Unattune a target with the Voodoo Doll by clicking on the Unattune Menu on the right!'
CombatTip14 = 'Upgrade the Attune Doll skill to be able to Attune the Voodoo Doll to multiple targets!'
CombatTip15 = 'Attacking an enemy in the back with a Dagger Combo will deal extra damage!'
CombatTip16 = "The Dagger's Asp skill can be used to break an enemy's Voodoo Doll Attunement!"
StoreTip1 = 'You can buy new weapons and ammunition from Stores!'
StoreTip2 = 'You can purchase Cannon and Pistol Ammo from the Gunsmith!'
StoreTip3 = 'You can purchase Throwing Knives from the Blacksmith!'
StoreTip4 = 'Blacksmiths sell stronger Cutlasses and Daggers!'
StoreTip5 = 'Gypsies sell stronger Voodoo Dolls and Voodoo Staves!'
StoreTip6 = 'Gunsmiths sell stronger Pistols!'
LevelupTip1 = 'Gaining a Cutlass Level gives you more Health!'
LevelupTip2 = 'Gaining a Grenade Level gives you more Health!'
LevelupTip3 = 'Gaining a Pistol Level gives you some Health and Voodoo Power!'
LevelupTip4 = 'Gaining a Dagger Level gives you some Health and Voodoo Power!'
LevelupTip5 = 'Gaining a Voodoo Doll Level gives you more Voodoo Power!'
LevelupTip6 = 'Gaining a Voodoo Staff Level gives you more Voodoo Power!'
DifficultyTip1 = 'Enemies with Red Level tags are very dangerous enemies! \n They still give standard Reputation rewards, though.'
DifficultyTip2 = 'Enemies with Green Level tags will be easy to defeat! They give reduced Reputation!'
DifficultyTip3 = 'Enemies with Yellow Level tags are a good match for you! \n They give standard Reputation rewards!'
DifficultyTip4 = 'Enemies with Grey Level tags are push-overs! They give very little Reputation rewards!'
DifficultyTip5 = "An enemy with a Skull Icon over its head is a boss! \n They are tough, so don't fight them alone!"
SkillTip1 = 'The Cutlass Sweep skill will hit all surrounding enemies!'
ParlorGameTip1 = 'You can play Poker or Blackjack at any Tavern. To find one, look for the sign with a Mug on it!'
ParlorGameTip2 = "Suits don't matter in Blackjack. All that matters is the total number value of the cards."
ParlorGameTip3 = "Play Poker to quickly earn Gold. But don't lose!"
FunnyTip1 = "Don't throw Grenades at your own feet!"
FunnyTip2 = "Don't feed the Alligators!"
FunnyTip3 = "Don't pet the Scorpions!"
FunnyTip4 = 'If you have been playing for more than 2 hours straight, you should take a break!'
FunnyTip5 = "Don't wear more than one eye-patch when playing this game!"
PortRoyalTip1 = 'Stay away from Fort Charles unless you are looking for trouble with the Navy!'
RavensCoveTip1 = "Raven's Cove Story Quest unlocks at Level 30."
RavensCoveTip2 = "When traveling Raven's Cove at night, beware the Red Ghosts."
RavensCoveTip3 = "Five friendly ghosts haunt Raven's Cove. Help them to access the mines."
RavensCoveTip4 = "Jolly Roger overran Raven's Cove destroying everything in sight."
RavensCoveTip5 = 'Watch where you step ... thar be ravens flying overhead.'
RavensCoveTip6 = 'There be rumors of Cursed Blades, El Patron, harmful ghosts and wicked phantoms abound...'
ShipPVPHint1 = 'Get a crew together! Unmanned cannons stack the odds against you.'
ShipPVPHint2 = "Stockpile cannonballs before sailing because it's a long way back to restock!"
ShipPVPHint3 = 'Shield the smaller, weaker ships on the team if your ship can withstand a pounding.'
ShipPVPHint4 = 'An Interceptor is best for the outskirts of a battle, and should stay away from War Frigates.'
ShipPVPHint5 = "If your team can't launch more ships, teleport to a friend's ship to balance the odds."
ShipPVPHint6 = "Make every cannonball count! Targeting broken panels or an enemy ship's rear earns a bonus. "
ShipPVPHint7 = 'Choose team ships carefully. Some are faster, some are stronger, and each has a vital role in battle.'
ShipPVPHint8 = "Stay clear of the enemy's island! Ships launching from there are temporarily invincible."
ShipPVPHint9 = 'Repair your vessel! Each repair spot on a ship can be manned by a different crew member to speed up repairs.'
ShipPVPHint10 = 'Be careful when doing repairs, leaving the wheel allows enemy ships to sneak up on you!'
ShipPVPHint11 = 'A Privateer ship receives a health boost for sinking enemy ships; a good pirate steals everything, including spare parts.'
ShipPVPHint12 = 'The health bonus that a Privateer ship receives for sinking an enemy ship depends on the amount of damage it did.'
ShipPVPHint13 = 'Privateer teams are automatically balanced. If the team you are trying to join is full, join the other!'
ShipPVPHint14 = 'If you want to check your score, press the ~ button.'
ShipPVPHint15 = 'Looking for a Privateer crew? Find one using the Lookout button or through the Crew section on your Hearties panel!'
ShipPVPHint16 = 'Looking to recruit pirates for your Privateer crew? Look for crewmates using the Lookout button or through the Crew section on your Hearties panel!'
Hints_General = [
    GeneralTip1, GeneralTip2, GeneralTip4, GeneralTip5, GeneralTip7, ControlTip1, ControlTip3, ControlTip4, ControlTip5, ControlTip6, TonicTip1, TonicTip2, TonicTip3, QuestTip1, QuestTip2, QuestTip3, QuestTip4, QuestTip5, QuestTip6, QuestTip7, ShipTip0, ShipTip1, ShipTip2, ShipTip3, ShipTip4, ShipTip5, ShipTip6, ShipTip7, ShipTip8, ShipTip9, ShipTip10, ShipTip11, ShipTip12, ShipTip13, ShipTip14, ShipTip15, ShipTip16, ShipTip17, ShipTip18, ShipTip19, ShipTip21, ShipTip22, ShipTip23, ShipTip24, ShipTip25, ShipTip26, ShipTip27, ShipTip28, ShipTip29, FriendTip1, FriendTip2, FriendTip3, FriendTip4, FriendTip5, FriendTip6, TreadmillTip1, TreadmillTip2, TreadmillTip3, TreadmillTip4, TreadmillTip5, TreadmillTip6, TreadmillTip7, ChatTip1, LevelupTip1, LevelupTip2, LevelupTip3, LevelupTip4, LevelupTip5, LevelupTip6, CombatTip1, CombatTip2, CombatTip3, CombatTip4, CombatTip5, CombatTip6, CombatTip7, CombatTip8, CombatTip9, CombatTip10, CombatTip11, CombatTip12, CombatTip13, CombatTip14, CombatTip15, CombatTip16, ParlorGameTip1, ParlorGameTip2, ParlorGameTip3, FunnyTip1, FunnyTip2, FunnyTip3, FunnyTip4, FunnyTip5, DifficultyTip1, DifficultyTip2, DifficultyTip3, DifficultyTip4, DifficultyTip5, FlagShipTip1, FlagShipTip2, FlagShipTip3, FlagShipTip4
]
Hints_Privateering = [
    ShipPVPHint1, ShipPVPHint2, ShipPVPHint3, ShipPVPHint4, ShipPVPHint5, ShipPVPHint6, ShipPVPHint7, ShipPVPHint8, ShipPVPHint9, ShipPVPHint10, ShipPVPHint11, ShipPVPHint12, ShipPVPHint13, ShipPVPHint14, ShipPVPHint15, ShipPVPHint16
]
HintMap_Levels = {
    1: (QuestTip1, QuestTip2, ControlTip1, ControlTip2, ControlTip4, PortRoyalTip1, GeneralTip7),
    2: (QuestTip1, QuestTip2, PortRoyalTip1, ControlTip1, ControlTip2, ControlTip3, ControlTip4, ControlTip9, ControlTip10, ControlTip12, ShipTip0, ShipTip1, ShipTip20, GeneralTip7),
    3: (ControlTip3, ControlTip4, ControlTip5, ControlTip11, CombatTip3, ShipTip1, ShipTip20, ShipTip21, OptimizeTip1, ShipTip0, SkillTip1, QuestTip3),
    4: (ControlTip4, ControlTip5, CombatTip3, TonicTip1, TonicTip2, ShipTip0, ShipTip1, ShipTip2, ShipTip20, ShipTip21, OptimizeTip1, SkillTip1, StoreTip1, QuestTip3),
    5: (ControlTip5, CombatTip7, CombatTip8, CombatTip9, TonicTip1, TonicTip2, GeneralTip6, StoreTip1, ShipTip0, ShipTip1, ShipTip2, TreadmillTip6, TreadmillTip8, TreadmillTip9, FriendTip2, QuestTip8),
    6: (ControlTip3, ControlTip5, StoreTip2, StoreTip3, TreadmillTip6, TreadmillTip8, TreadmillTip9, FriendTip2, GeneralTip6, QuestTip8, TonicTip3, ShipTip3, ShipTip5, CombatTip2, CombatTip4, CombatTip5, CombatTip7, CombatTip8, CombatTip9),
    7: (StoreTip2, StoreTip3, CombatTip1, CombatTip2, CombatTip3, CombatTip4, CombatTip5, CombatTip10, TreadmillTip6, FriendTip1, QuestTip5, GeneralTip1, ShipTip4, ShipTip5, ShipTip15, ShipTip16),
    8: (StoreTip4, StoreTip5, StoreTip6, CombatTip1, CombatTip3, QuestTip4, FriendTip4, FriendTip5, TreadmillTip1, TreadmillTip6, GeneralTip1, FlagShipTip1, FlagShipTip2, FlagShipTip3, FlagShipTip4),
    9: (LevelupTip1, LevelupTip2, LevelupTip3, LevelupTip4, LevelupTip5, LevelupTip6, CombatTip11, CombatTip12, CombatTip13, CombatTip14, ControlTip6, ShipTip8),
    10: (ShipTip4, ShipTip6, ShipTip22, FriendTip6, QuestTip7, TreadmillTip5, ControlTip6, CombatTip3, ParlorGameTip1, GeneralTip2, GeneralTip3, DifficultyTip1, DifficultyTip2, DifficultyTip3, DifficultyTip4),
    11: (TreadmillTip1, TreadmillTip2, TreadmillTip3, QuestTip6, ControlTip6, CombatTip3, ParlorGameTip2, GeneralTip4, GeneralTip3, ShipTip7),
    12: (ControlTip1, CombatTip10, CombatTip1, CombatTip3, ParlorGameTip3, GeneralTip2, GeneralTip5, GeneralTip3, ShipTip9, ShipTip10, ShipTip11, ShipTip17),
    13: (ShipTip12, ShipTip17, ShipTip18, ShipTip19, ShipTip22, ShipTip23, ShipTip24, ShipTip25, GeneralTip4, TreadmillTip5, TreadmillTip7),
    14: (),
    15: (),
    16: (),
    17: (),
    18: (),
    19: (),
    20: (),
    21: (),
    22: (),
    23: (),
    24: (),
    25: ('High level enemies can be found on Kingshead.', 'You can purchase Grenade Ammunition from the Gunsmith!'),
    26: (),
    27: ('High level enemies can be found on Padres Del Fuego.', ),
    28: (),
    29: (),
    30: ('High level enemies can be found on Isla Tormenta.', RavensCoveTip1),
    31: (),
    32: (),
    33: (),
    34: (),
    35: (),
    36: (),
    37: (),
    38: (),
    39: (),
    40: ()
}
HintMap_Locations = {
    LocationIds.PORT_ROYAL_ISLAND: (), LocationIds.PORT_ROYAL_PORT: (), LocationIds.PORT_ROYAL_JUNGLE_B: (), LocationIds.PORT_ROYAL_JUNGLE_C: (), LocationIds.PORT_ROYAL_CAVE_A: (), LocationIds.PORT_ROYAL_CAVE_B: (), LocationIds.PORT_ROYAL_JUNGLE_A: (), LocationIds.JUNEGREER_RESIDENCE: (), LocationIds.SMITTYS_JEWELRY: (), LocationIds.GOVERNORS_MANSION: (), LocationIds.ROWDYROOSTER_TAVERN: (), LocationIds.ROYALANCHOR_TAVERN: (), LocationIds.GRAHAM_IMPORTS: (), LocationIds.EWANS_WEAPONS: (), LocationIds.OLD_WAREHOUSE: (), LocationIds.RSMITH_PEWTERER: (), LocationIds.SOLOMONS_TATTOOS: (), LocationIds.TORTUGA_ISLAND: (), LocationIds.TORTUGA_PORT: (), LocationIds.TORTUGA_JUNGLE_A_GRAVEYARD: (), LocationIds.TORTUGA_CAVE: (), LocationIds.TORTUGA_JUNGLE_C: (), LocationIds.TORTUGA_SWAMP: (), LocationIds.TORTUGA_JUNGLE_B_SWAMPY: (), LocationIds.FAITHFULBRIDE_TAVERN: (), LocationIds.KINGSARM_TAVERN: (), LocationIds.BOWDASH_MANSION: (), LocationIds.ORINDAS_SHACK: (), LocationIds.FLATTS_WEAPONS: (), LocationIds.MILLIES_COTTAGE: (), LocationIds.SEAMSTRESS_TAILOR: (), LocationIds.DOCTOR_GROGS: (), LocationIds.FLINTYS_BLACKSMITH: (), LocationIds.DEL_FUEGO_ISLAND: (), LocationIds.ANVIL_ISLAND: (), LocationIds.ANVIL_CAVE_BARBOSA: (), LocationIds.DRIFTWOOD_ISLAND: ('Crabs have been known to infest Driftwood island.', ), LocationIds.RUMRUNNER_ISLE: (), LocationIds.ISLA_PERDIDA: (), LocationIds.PERDIDA_JUNGLE_B: (), LocationIds.OUTCAST_ISLE: (), LocationIds.CUBA_ISLAND: (), LocationIds.CUBA_SWAMP: (), LocationIds.KINGSHEAD_ISLAND: (), LocationIds.ISLA_CANGREJOS: (), LocationIds.ISLA_TORMENTA: (), LocationIds.TORMENTA_CAVE_B: (), LocationIds.CUTTHROAT_ISLAND: (), LocationIds.CUTTHROAT_JUNGLE: (), LocationIds.RAVENS_COVE_ISLAND: (RavensCoveTip1, RavensCoveTip2, RavensCoveTip3, RavensCoveTip4, RavensCoveTip5, RavensCoveTip6), LocationIds.RAVENS_COVE_MINE: (), LocationIds.WINDWARD_PASSAGE: (), LocationIds.BRIGAND_BAY: (), LocationIds.BLOODY_BAYOU: (), LocationIds.SCURVY_SHALLOWS: (), LocationIds.BLACKHEART_STRAIT: (), LocationIds.SALTY_FLATS: (), LocationIds.MAR_DE_PLATA: (), LocationIds.SMUGGLERS_RUN: (), LocationIds.THE_HINTERSEAS: (), LocationIds.DEAD_MANS_TROUGH: (), LocationIds.LEEWARD_PASSAGE: (), LocationIds.BOILING_BAY: (), LocationIds.MARINERS_REEF: (), LocationIds.PEARL_ISLAND: (), LocationIds.ANY_LARGE_ISLAND: (), LocationIds.ANY_LARGE_PORT: (), LocationIds.ANY_WILD_PORT: (), LocationIds.ANY_LOCATION: ()
}
Hints_VelvetRope = [
    'With Unlimited Access, you can use all 6 Weapons!', 'With Unlimited Access, you can purchase all 9 Ship types!', 'With Basic Member Access, a Skill cannot be upgraded past Rank 2!', 'With Unlimited Access, you can start your own Guild!', 'Grenades can be used to defeat large groups of enemies! \n Unlimited Access only!', 'Command dark powers using the Voodoo Staff! \n Unlimited Access only!', 'Fight enemies up close or from afar with the Dagger! \n Unlimited Access only!', 'With Unlimited Access, you can create up to 4 Pirate Characters!', 'With Unlimited Access, you can purchase stronger weapons \n like the Double-Barreled Pistol!', 'With Unlimited Access, you can unlock new ammo types, \n such as flaming cannonballs!'
]
RepCapText_Overall = 'Pirate Master\nLevel %s'
RepCapText_Skill = 'Mastered'
AnyTMName = 'Any Treasure Map'
AttackShipSunk = '1 Attack Ship Sunk!!'
AttackShipsSunk = '%s Attack Ships Sunk!!'
DrawbridgePassable = 'Bridge Destroyed!! '
BridgeNeedsToBeDestroyed = 'Bridge %d needs to be destroyed.'
AttackTheGoliath = 'Attack the Goliath!'
Goliath = 'Goliath'
SailTheBlackPearl = 'Sail the black pearl out of the harbor.'
DestroyTheBridges = ' Destroy the bridges blocking your way.'
BlackPearlTMName = 'Recover the Black Pearl'
BlackPearlTMDesc = "Escape with Jack's ship!"
BlackPearlStageZero = 'Stage One: Defeat the Navy Guards'
BlackPearlStageOne = 'Take the Wheel'
BlackPearlStageTwo = 'Stage Two:  Sink the Attack Ships'
BlackPearlStageThree = 'Stage Three:  Destroy the Drawbridges'
BlackPearlStageFour = 'Stage Four:  Sink the Goliath'
BlackPearlWarningLow = 'Danger!  The Black Pearl is almost sunk!'
BlackPearlLoser = 'The Black Pearl sank!'
BlackPearlWinner = 'You successfully rescued the Black Pearl! \nTake it back to Jack Sparrow to claim your booty'
BlackPearlWaitCutscene = 'Waiting for other players to finish cutscene.'
BlackPearlWaitCutscene2 = 'Other players waiting for you to finish cutscene.'
BlackPearlScoreboard = 'Black Pearl Quest:'
BlackPearlRewardSuccess = 'Congratulations!  You have earned a potion reward for liberating the Black Pearl!:\n\n\x01yellow\x01%s\x02\n\nComplete the Black Pearl treasure map again for the chance to earn rare items not available elsewhere!'
BlackPearlRewardFailure = 'You are unable to carry your potion reward!:\n\n\x01yellow\x01%s\x02\n\nMake sure you have room for new potions and liberate the Black Pearl again for the chance to earn rare potions!'
NavyFortName = 'Navy Fort'
EdgeOfWorldWarning = "You've sailed to the edge of the world. Turn your ship around to continue your adventure."
ShopBlacksmith = 'Blacksmith'
ShopGunsmith = 'Gunsmith'
ShopCannoneer = 'Cannoneer'
ShopShipwright = 'Shipwright'
ShopGypsy = 'Gypsy'
ShopMedicineMan = 'Medicine Man'
ShopGrenadier = 'Grenadier'
ShopMerchant = 'Merchant'
ShopBartender = 'Bartender'
ShopTailor = 'Tailor'
ShopTattoo = 'Tattoo Artist'
ShopBarber = 'Barber'
ShopJewelry = 'Jeweler'
ShopTavern = 'Tavern'
ShopFree = 'Free'
ShopQuestItem = 'Quest Item'
ShopMusician = 'Musician'
ShopTrainer = 'Trainer'
ShopPvP = 'PvP Infamy Rewards'
ShopSelectColor = 'Select Color'
ShopAddToCart = 'Add To Cart'
ShopEnterCode = 'Enter Code'
ShopCodeInst = 'Enter a specially obtained code below to redeem an item for your pirate.'
ShopCodeErr = 'Please enter a valid code for redemption.'
ShopCodeFull = 'Inventory is full. Free up an appropriate inventory spot and try again'
ShopCodeSuccess = 'Code has been redeemed.'
ShopRedeem = 'Code'
ShopStowaway = 'Dockworker'
ShopFishmaster = 'Fishmaster'
ShopCannonmaster = 'Cannonmaster'
ShopCatalogRep = 'Peddler'
ShopScrimmageMaster = 'Scrimmage Master'
SongPlayingAnnouncement = 'Now playing:\n%s'
RBROW = 0
LBROW = 1
LEAR = 2
REAR = 3
NOSE = 4
MOUTH = 5
LHAND = 6
RHAND = 7
JewelryNames = {
    RBROW: 'Right Brow',
    LBROW: 'Left Brow',
    LEAR: 'Left Ear',
    REAR: 'Right Ear',
    NOSE: 'Nose',
    MOUTH: 'Mouth',
    LHAND: 'Left Hand',
    RHAND: 'Right Hand'
}
ShopLimitTailor = 'You cannot hold this item.\n\nCurrently the limit for clothing is %s items per category.\n\nYou will not be able to purchase clothing of this type until you have a free spot open.'
ShopLimitJewelry = 'You cannot hold this item.\n\nCurrently the limit for jewelry is %s items per category.\n\nYou will not be able to purchase jewelry of this type until you have a free spot open.'
ShopLimitTattoo = 'You cannot hold this item.\n\nCurrently the limit for tattoos is %s items per category.\n\nYou will not be able to purchase tattoos of this type until you have a free spot open.'
ShopFemaleVestConflict = 'Your current vest selection does not allow for shirts.\n\nPlease change vests to properly see this item'
ShopOwnedBarber = 'You currently have this style.'
ChatManagerOpenChatWarning = 'Your current chat settings do not allow chat. You can change your settings in the Account Options area of the Pirates Online web site.'
ChatManagerUnpaidWarning = 'Your subscription level does not allow chat. You can change your settings in the Account Options area of the Pirates Online web site.'
ChatManagerWhisperWarning = "Whispering text messages is only allowed between two paid subscribers who are adults or have their parent's permission."
ChatManagerNoFriendsWarning = 'You need to exchange Player Friends Codes with your friends in order to use Player Friends chat. To learn more about Player Friends chat or to enable Open chat, visit www.PiratesOnline.com.'
ChatManagerNeedParentWarning = 'Your account must be validated by a parent or guardian in order to use Player Friends chat or Open chat. To learn more about chat, visit www.PiratesOnline.com'
EnterKingsheadMessage = 'Entering Unlimited Access area, Kingshead Island'
EnterKingsheadWarning = 'Sorry, you must be an Unlimited Access member to enter Kingshead Island'
AccessVelvetRope = 'Basic Member Access'
AccessFull = 'Unlimited Access'
AccessUnknown = 'Unknown Access'
VelvetRopeQuestBlock = '\x01Ired\x01This quest is available only to Unlimited Access.\x02'
AccessLevel = {
    OTPGlobals.AccessUnknown: AccessUnknown, OTPGlobals.AccessVelvetRope: AccessVelvetRope, OTPGlobals.AccessFull: AccessFull
}
for i in range(52):
    card = i
    suit = card / 13
    rank = card % 13
    iid = InventoryType.begin_Cards + i
    InventoryTypeNames[iid] = getPlayingCardName(suit, rank)

OceanZoneNames = {
    OceanZone.UNCHARTED_WATERS: 'Uncharted Waters', OceanZone.BRIGAND_BAY: 'Brigand Bay', OceanZone.BLOODY_BAYOU: 'Bloody Bayou', OceanZone.SCURVY_SHALLOWS: 'Scurvy Shallows', OceanZone.BLACKHEART_STRAIGHT: 'Blackheart Straight', OceanZone.WINDWARD_PASSAGE: 'Windward Passage', OceanZone.SALTY_FLATS: 'Salty Flats', OceanZone.MAR_DE_PLATA: 'Mar De Plata', OceanZone.SMUGGLERS_RUN: "Smuggler's Run", OceanZone.LEEWARD_PASSAGE: 'Leeward Passage', OceanZone.DEAD_MANS_TROUGH: "Dead Man's Trough", OceanZone.MARINERS_REEF: "Mariners' Reef", OceanZone.BOILING_BAY: 'Boiling Bay', OceanZone.THE_HINTER_SEAS: 'The Hinter Seas'
}
EnterOceanZone = 'Entering\n%s'
MapCurrentIsland = 'You are here.'
MapNeedsTeleportToken = 'You do not have the Teleport Totem for this island.'
MapCanTeleport = 'Click to teleport to this island.'
MapCanTeleportReturn = 'Click to return to this island.'
MapCanTeleportPortOfCall = 'Click to return to your Port of Call.'
MapCannotTeleport = 'You cannot teleport to this island.'
MapBasicAccess = 'With %s, you can get a special Voodoo Totem that allows you to teleport to this island!' % AccessFull
MinimapNotAvailable = 'Map is not available for this area.'
LootBounty = '%s Bounty'
LootGold = '%s Gold'
LootGoldDouble = '%s Gold (Holiday Bonus)'
LootGoldPotionBoost = '%s Gold (Potion Bonus)'
CargoCrate = '%s Cargo Crate'
CargoChest = '%s Treasure Chest'
CargoSkChest = '%s Royal Chest'
LootSac = '%s Loot Pouch'
LootChest = '%s Loot Chest'
LootSkChest = '%s Loot Skull Chest'
CargoCrateP = '%s Cargo Crates'
CargoChestP = '%s Treasure Chests'
CargoSkChestP = '%s Royal Chests'
LootSacP = '%s Loot Pouches'
LootChestP = '%s Loot Chests'
LootSkChestP = '%s Loot Skull Chests'
LootUpgradeChest = '%s Ship Materials'
LootRareUpgradeChest = '%s Rare Ship Materials'
LootUpgradeChestP = '%s Ship Materials'
LootRareUpgradeChestP = '%s Rare Ship Materials'
TempNameList = [
    'Pirate', 'Freebooter', 'Seadog'
]
WeaponUnlockText = {
    InventoryType.CutlassRep: 'Unlocked by Will Turner', InventoryType.PistolRep: 'Unlocked by Captain Barbossa', InventoryType.DollRep: 'Unlocked at Notoriety Level 5', InventoryType.DaggerRep: 'Unlocked at Notoriety Level 10', InventoryType.GrenadeRep: 'Unlocked at Notoriety Level 20', InventoryType.WandRep: 'Unlocked at Notoriety Level 30', InventoryType.FishingRep: 'Unlocked at Notoreity Level 10'
}
WeaponAlreadyUnlocked = 'Unlocked'
ReportPlayerTitle = 'Report A Player'
ReportPlayerCancel = 'Cancel'
ReportPlayerContinue = 'Continue'
ReportPlayerReport = 'Report'
ReportPlayerClose = 'Close'
ReportPlayerFoulLanguage = 'Foul Language'
ReportPlayerPersonalInfo = 'Sharing/Requesting Personal Info'
ReportPlayerRudeBehavior = 'Rude or Mean Behavior'
ReportPlayerBadName = 'Bad Name'
ReportPlayerAlreadyReported = '\x01Ired\x01%s\x02 has already been reported this session. Your report has already been sent to a Moderator for review.'
ReportPlayerTopMenu = 'This feature will send a complete report to a moderator.  Instead of sending a report, you might choose to do one of the following:\n\n  - Ignore this player for this session\n  - Switch to another server\n  - Remove friendship\n\n\n\nDo you want to report \x01Ired\x01%s\x02 to a Moderator?'
ReportPlayerChooseCategory = 'You are about to report \x01Ired\x01%s\x02. A Moderator will be alerted to your complaint and will take appropriate action for anyone breaking our rules. Please choose a reason for this report.'
ReportPlayerConfirmFoulLanguage = 'You are about to report that \x01Ired\x01%s\x02 has used obscene, bigoted or sexually explicit language.'
ReportPlayerConfirmPersonalInfo = 'You are about to report that \x01Ired\x01%s\x02 is being unsafe by giving out or requesting a phone number, address, last name, email address, password or account name.'
ReportPlayerConfirmRudeBehavior = 'You are about to report that \x01Ired\x01%s\x02 is bullying, harassing, or using extreme behavior to disrupt the game.'
ReportPlayerConfirmBadName = "You are about to report that \x01Ired\x01%s\x02 has created a name that does not follow Disney's House Rules."
ReportPlayerConfirmCategory = 'We take reporting very seriously. Your report will be viewed by a Moderator who will take appropriate action for anyone breaking our rules. If your account is found to have participated in breaking the rules, or if you make false reports or abuse the "Report a Player" system, a Moderator may take action against your account. Are you absolutely sure you want to report this player?'
ReportPlayerConfirmReport = 'Thank you! Your report has been sent to a Moderator for review. There is no need to contact us again about the issue. The moderation team will take appropriate action for a player found breaking our rules.'
ReportPlayerRemovedFriend = 'We have automatically removed \x01Ired\x01%s\x02 from your Friends List.'
ReportPlayerIgnored = '\x01Ired\x01%s\x02 has automatically been ignored for the remainder of this session.'
HOLIDAYIDS_TO_NAMES = {
    HolidayGlobals.MOTHERSDAY: "Mother's Day", HolidayGlobals.FATHERSDAY: "Father's Day", HolidayGlobals.SAINTPATRICKSDAY: "St. Patrick's Day", HolidayGlobals.FOURTHOFJULY: 'Fourth of July', HolidayGlobals.HALLOWEEN: 'Halloween', HolidayGlobals.WINTERFESTIVAL: 'Winter Festival', HolidayGlobals.NEWYEARS: "New Year's Day", HolidayGlobals.VALENTINESDAY: "Valentine's Day", HolidayGlobals.MARDIGRAS: 'Mardi Gras'
}
NO_CURRENT_HOLIDAYS = 'Sorry, there are no holiday events active right now.'
DoubleGoldStart = makeHeadingString('Double yer gold!', 2) + '\nEarn double gold for land and sea battles, Cannon Defense, Fishing and Ship Repair on land!'
DoubleGoldStartChat = 'Double yer gold!!\nEarn double gold for land and sea battles, Cannon Defense, Fishing and Ship Repair on land!'
DoubleGoldEnd = ''
DoubleGoldStatus = 'Double Gold Event (All Players):\nTime Remaining: %s Hours, %s Minutes'
DoubleGoldFullStart = makeHeadingString('Double Gold Event In Progress!', 2) + '\nAll Unlimited Access Members will receive double gold rewards for their quests and battles. %(hours)s Hours, %(minutes)s Minutes remain before the end of the event.'
DoubleGoldFullStartChat = 'Double Gold Event In Progress!\nAll Unlimited Access Members will receive double gold rewards for their quests and battles. %(hours)s Hours, %(minutes)s Minutes remain before the end of the event.'
DoubleGoldFullEnd = 'The double gold event for unlimited access members has just ended!'
DoubleGoldFullStatus = 'Double Gold Event (Unlimited Access Members):\nTime Remaining: %s Hours, %s Minutes'
DoubleLootStart = makeHeadingString('Double yer plunder!', 2) + '\nYer twice as likely to find loot, and earn double materials from sinking Warships and Bounty Hunters!'
DoubleLootStartChat = 'Double yer plunder!\nYer twice as likely to find loot, and earn double materials from sinking Warships and Bounty Hunters!'
DoubleLootEnd = ''
DoubleLootStatus = 'Double Loot Event (All Players):\nTime Remaining: %s Hours, %s Minutes'
DoubleGoldBonus = '2x Gold Bonus'
DoubleXPStart = makeHeadingString('Double Reputation Event In Progress!', 2) + '\nPlayers will earn double Reputation points for land and sea battles.'
DoubleXPStartChat = 'Double Reputation Event In Progress!\nPlayers will earn double reputation points for land and sea battles.'
DoubleXPEnd = 'The double reputation point event for all has just ended!'
DoubleXPStatus = 'Double Reputation Point Event (All Players):\nTime Remaining: %s Hours, %s Minutes'
DoubleXPFullStart = makeHeadingString('Double Reputation Event In Progress!', 2) + '\nAll Unlimited Access Members will receive double Reputation points for all land and sea battles.'
DoubleXPFullStartChat = 'Double Reputation Event In Progress!\nAll Unlimited Access Members will receive double Reputation points for all land and sea battles.'
DoubleXPFullEnd = 'The Double Reputation Event for Unlimited Access members has ended!'
DoubleXPFullStatus = 'Double Reputation Point Event (Unlimited Access Members):\nTime Remaining: %s Hours, %s Minutes'
BlackJackFridayStart = makeHeadingString('Blackjack Friday in progress!', 2) + "\nVisit the Rowdy Rooster in Port Royal or King's Arm in Tortuga to play"
BlackJackFridayStartChat = 'Blackjack Friday currently in progress.'
BlackJackFridayEnd = makeHeadingString('Blackjack Friday has ended!', 2) + "\nPlease attend next week's Blackjack Friday."
BlackJackFridayEndChat = 'Blackjack Friday has ended.'
BlackJackFridayStatus = 'BlackJack Friday:\nTime Remaining: %s Hours, %s Minutes'
FreeHatStartUnlimited = makeHeadingString('TO ALL PIRATES!', 2) + "\nDon't forget to pick up your exclusive skull bandana from any Tailor Shop."
FreeHatStartUnlimitedChat = "To all pirates! Don't forget to pick up your exclusive skull bandana from any Tailor Shop."
FreeHatStartBasic = makeHeadingString('Claim your exclusive in-game item!', 2) + '\nUpgrade to Unlimited Access and visit any Tailor shop to pick up an exclusive skull bandana.'
FreeHatStartBasicChat = 'Upgrade to Unlimited Access and visit any Tailor shop to pick up an exclusive skull bandana!'
FlirtEmoteStart = "To All Pirates... For Valentines Day, we are introducing a new emote, flirt. Flirt can be accessed through your emotes SpeedChat menu and by the emote command '/flirt'."
StPatricksStartAll = 'What mischief is this? The Caribbean seas have gone green!'
StPatricksStartUnlimited = makeHeadingString('To all Unlimited Access Members', 2) + "\nVisit the tattoo parlor for your exclusive St. Patty's Day tattoo & the Barber for some green hair."
StPatricksStartUnlimitedChat = "Don't forget to pick up your St. Patricks day tattoo and green hair before they disappear."
StPatricksStartBasic = makeHeadingString("Get your St. Patrick's day tattoos and hair!", 2) + '\nUpgrade to Unlimited Access and get your St. Patrick?s Day tattoo and green hair!'
StPatricksStartBasicChat = "Upgrade to Unlimited Access and pick up your St. Patrick's day tattoo and green hair before they disappear!"
StPatricksEndAll = 'The waters of the Caribbean have turned back to their usual balmy blue hue.'
StPatricksStatus = 'The Caribbean seas will remain green for the next %s Hours, %s Minutes'
MothersDayStartUnlimited = makeHeadingString('To all Unlimited Access Members', 2) + "\nVisit a Tattoo Parlor for exclusive Mother's Day tattoos."
MothersDayStartUnlimitedChat = "Visit a Tattoo Parlor for exclusive Mother's Day tattoos."
MothersDayStartBasic = makeHeadingString("Get your Mother's Day tattoos!", 2) + "\nUpgrade to Unlimited Access and get your Mother's Day tattoos."
MothersDayStartBasicChat = "Upgrade to Unlimited Access and pick up your Mother's Day tattoos before they disappear!"
MothersDayStatus = "Mother's Day Tattoo Event (Unlimited Access Members):\nTime Remaining: %s Hour(s), %s Minute(s)"
FathersDayStart = makeHeadingString("Father's Day Event", 2) + "\nVisit Jack Sparrow at the Rowdy Rooster in Port Royal, to take part in a limited time Father's Day Quest."
FathersDayStartChat = "Visit Jack Sparrow at the Rowdy Rooster in Port Royal, to take part in a limited time Father's Day quest."
FathersDayStatus = "Father's Day Quest Event:\nTime Remaining: %s Hours, %s Minutes"
FourthOfJulyStart = makeHeadingString('Fourth of July', 2) + '\nGo to the shores of Port Royal, Tortuga or Padres del Fuego to watch fireworks light up the night sky. Show occurs every hour during night time.'
FourthOfJulyStartChat = 'Go to the shores of Port Royal, Tortuga or Padres del Fuego to watch fireworks light up the night sky. Show occurs every hour during night time.'
FourthOfJulyStatus = 'Fourth Of July Holiday:\nTime Remaining: %s Hours, %s Minutes'
HalfOffCustomizationStart = 'Half off customization for Unlimited Access players: %s hours, and %s minutes'
HalfOffCustomizationEnd = 'The 50%% off all customization items event has ended.'
HalfOffCustomizationUnlimited = 'Unlimited Access Members Only!  Visit any of the shops for 50%% off all customization items such as Clothing, Tattoos and Jewelry. Now until noon (PDT), August 18. %s Hour(s), %s Minute(s) until the end of the event.'
HalfOffCustomizationBasic = 'Unlimited Access members receive 50%% off all Customization Items. (Note: Discounts for paid members only. Upgrade to a paid subscription to take advantage of the shop discounts.) %s Hour(s), %s Minute(s) until the end of the event.'
HalfOffCustomizationStatus = 'Half-Off Customization Event (Unlimited Access Players):\nTime Remaining: %s Hour(s), %s Minute(s)'
AllAccessHolidayStart = 'Free Preview Weekend for the next %s hours, and %s minutes'
UnlimitedAccessEventBasic = "Avast! It's a Free Preview Weekend! Your Basic Access account has been upgraded to Unlimited Access for FREE."
UnlimitedAccessEventUnlimited = "Avast! It's a Free Preview Weekend for Limited Access crew members. Please feel free to invite friends and family to signup for a free account. They will be able to experience being an Unlimited Access crew member from now until noon (PDT), August 18th."
UnlimitedAccessEventUnlimitedChat = "Avast! It's a Free Preview Weekend for Limited Access crew members. Please feel free to invite friends and family to signup for a free account. Now until noon (PDT), August 18th."
UnlimitedAccessEventBasicEnd = 'The Free Preview Weekend has ended. Your account has returned to Basic Access status, to use any Unlimited Access items you acquired during the Free Preview, please upgrade your account.'
HalloweenStart = makeHeadingString('A SUPERNATURAL CHILL SPREADS ACROSS THE ISLANDS!', 2) + "\nJolly Roger's ghastly magic casts an eerie atmosphere throughout the Caribbean."
HalloweenStartChat = "A supernatural chill spreads across the islands! \nJolly Roger's ghastly magic casts an eerie atmosphere throughout the Caribbean."
HalloweenEnd = 'The supernatural chill has faded... For now...'
HalloweenStatus = 'Eerie:\nTime Remaining: %s Hours, %s Minutes'
JollyRogerCurseStatus = 'Jolly Roger Curse Event:\nTime Remaining: %s Hours, %s Minutes'
CursedNightStart = 'Jolly Roger forced an evil atmosphere around the Caribbean once again. Beware! The curse is coming!'
CursedNightEnd = "Jolly Roger's powers have been weakened, evil atmosphere has lifted. At least for now..."
FullMoonWarning1 = 'The Moon will become full in about 5 minutes!'
FullMoonWarning2 = 'The Moon will become full in less than 1 minute!'
JollyRogerCurseComing = "Jolly Roger'sCurse is coming! \nTonight when the moon becomes full, everyone outdoors and on land will become Undead! Hide inside a building during the full moon to be safe from the curse!"
JollyRogerCurseActive = "Beware! Jolly Roger's Curse has turned the pirates outdoors into the Undead. Go defend the towns from the Cursed Pirates!"
JollyRogerCurseIndoors = "Jolly Roger's Curse is upon us! You are safe here, but the towns need your help!"
JollyRogerCurseOutdoors = "Jolly Roger's Curse is upon us! Jolly Roger commands you to attack other Undead and Humans!"
JollyRogerCurseJail = "You are restored from Jolly Roger's Curse! Now, go save the town from the other Undead!"
JollyRogerCurseEnd = "Jolly Roger's curse has been broken! The Caribbean is safe again for now..."
FoundersFeastStart = makeHeadingString('Brethren Victory Feast is in progress!', 2) + '\nCome to the shores of Tortuga to join the festivities.'
FoundersFeastStartChat = 'Brethren Victory Feast is in progress! \nCome to the shores of Tortuga to join the festivities.'
FoundersFeastEnd = 'Brethren Victory Feast has ended!'
FoundersFeastBegin = 'Let the Brethren Victory Feast begin!'
FoundersFeastStatus = 'Brethren Victory Feast:\nTime Remaining: %s Hours, %s Minutes'
FreeBandanaStartUnlimited = makeHeadingString('To all Unlimited Access Members', 2) + "\nDon't forget to pick up your exclusive golden skull bandana from any Tailor Shop."
FreeBandanaStartUnlimitedChat = "Don't forget to pick up your exclusive skull bandana from any Tailor Shop."
FreeBandanaStartBasic = makeHeadingString('Claim your exclusive in-game item!', 2) + '\nUpgrade to Unlimited Access and visit any Tailor shop to pick up an exclusive golden skull bandana.'
FreeBandanaStartBasicChat = 'Upgrade to Unlimited Access and visit any Tailor shop to pick up an exclusive golden skull bandana!'
WinterFestivalStart = makeHeadingString('WARM TIDES AND GLAD TIDINGS BRIGHTEN THE CARIBBEAN!', 2) + '\nPirates make merry with good cheer and jolly decorations around the streets and beaches of Port Royal, Tortuga, and Padres del Fuego.'
WinterFestivalStartChat = 'Warm tides and glad tidings brighten the caribbean!\nPirates make merry with good cheer and jolly decorations around the streets and beaches of Port Royal, Tortuga, and Padres del Fuego.'
WinterFestivalEnd = 'The unseasonal winter warmth has now set sail.'
WinterFestivalStatus = 'Winter Holiday:\nTime Remaining: %s Hours, %s Minutes'
NewYearsStart = makeHeadingString('All pirates celebrate with unlimited access to the caribbean!', 2) + '\nEnjoy the fireworks in the night sky, with more surprises each week!'
NewYearsStartChat = 'All pirates celebrate with unlimited access to the caribbean!\nEnjoy the fireworks in the night sky, with more surprises each week!'
NewYearsEnd = ''
NewYearsStatus = 'Fireworks:\nTime Remaining: %s Hours, %s Minutes'
ValentinesDayStartUnlimited = makeHeadingString("The Valentine's Holiday is in progress!", 2) + "\nVisit Erin Amorous in the Rowdy Rooster on Port Royal to pick up a special Valentine's Quest. Complete the Quest for a special reward!"
ValentinesDayStartUnlimitedChat = "The Valentine's Holiday is in progress!\nVisit Erin Amorous in the Rowdy Rooster on Port Royal to pick up a special Valentine's Quest. Complete the Quest for a special reward!"
ValentinesDayStartBasic = makeHeadingString("The Valentine's Holiday is in progress!", 2) + "\nBecome an Unlimited Access Member and receive a special reward when you complete the Valentine's Quest."
ValentinesDayStartBasicChat = "The Valentine's Holiday is in progress!\nBecome an Unlimited Access Member and receive a special reward when you complete the Valentine's Quest."
ValentinesDayEnd = "Valentine's Holiday has ended!"
ValentinesDayStatus = "Valentine's Holiday:\nTime Remaining: %s Hours, %s Minutes"
DoubleCrossStart = 'The Casa de Muertos Guild has a job for you and will pay good coin to see it done. Meet Captain Ezekiel Rott by the dock of Padres del Fuego to learn more. This quest can only be started by Pirates at Level 15 Notoriety or higher.'
DoubleCrossStartBasic = 'The Casa de Muertos Guild has a job for you and will pay good coin to see it done. Meet Captain Ezekiel Rott by the dock of Padres del Fuego to learn more. Available to Unlimited Access Members only.'
DoubleCrossStatus = 'The Casa de Muertos Guild\nTime Remaining: %s Hours, %s Minutes'
MardiGrasStart = 'Mardi Gras Carnival is in progress! Come to the shores of Tortuga to join the festivities.'
MardiGrasEnd = 'Mardi Gras Carnival has ended!'
MardiGrasStatus = 'Mardi Gras Carnival:\nTime Remaining: %s Hours, %s Minutes'
EITCMobilizationStart = 'EITC Sea Offensive:\nThe East India Trading Company has launched a Sea Offensive! Many EITC Ships now patrol the high seas, so get ready to face them when you set sail!'
EITCMobilizationStatus = 'EITC Sea Offensive:\nTime Remaining: %s Hours, %s Minutes'
NavyMobilizationStart = 'Navy Sea Offensive:\nThe Navy has launched a Sea Offensive! Many Navy Ships now patrol the high seas, so get ready to face them when you set sail!'
NavyMobilizationStatus = 'Navy Sea Offensive:\nTime Remaining: %s Hours, %s Minutes'
SkelMobilizationStart = 'Skeleton Sea Offensive:\nJolly Roger has launched a Sea Offensive! Many Skeleton Ships now roam the high seas, so get ready to face them when you set sail!'
SkelMobilizationStatus = 'Skeleton Sea Offensive:\nTime Remaining: %s Hours, %s Minutes'
InvasionPortRoyalStart = makeHeadingString('Port Royal Invasion', 2) + "\nGet ready to defend Port Royal from Jolly Roger's army! Undead will arrive from the shores and attack the town's barricades. As the barricades fall, the skeletons get closer to the Governor's Mansion. Protect the barricades and don't let the Governor's Mansion be destroyed, or Jolly Roger will be victorious."
InvasionTortugaStart = makeHeadingString('Tortuga Invasion', 2) + "\nGet ready to defend Tortuga from Jolly Roger's army! Undead will arrive from the shores and attack the town's barricades. As the barricades fall, the skeletons get closer to the Faithful Bride tavern. Protect the barricades and don't let Jolly Roger reach the Faithful Bride tavern, or Jolly Roger will find Jack Sparrow and have his revenge."
InvasionDelFuegoStart = makeHeadingString('Padres Del Fuego Invasion', 2) + "\nGet ready to defend Padres Del Fuego from Jolly Roger's army! Undead will arrive from the shores and attack the town's barricades. As the barricades fall, the skeletons get closer to the center of town. Protect the barricades and don't let the town be destroyed, or Jolly Roger will be victorious!"
InvasionPortRoyalStatus = 'Port Royal Invasion:\nTime Remaining: %s Hours, %s Minutes'
InvasionTortugaStatus = 'Tortuga Invasion:\nTime Remaining: %s Hours, %s Minutes'
InvasionDelFuegoStatus = 'Padres Del Fuego Invasion:\nTime Remaining: %s Hours, %s Minutes'
InvasionJollyRogerWarning = 'Invasion starts in %s minute(s). '
InvasionLocationPortRoyal = 'Port Royal'
InvasionLocationTortuga = 'Tortuga'
InvasionLocationDelFuego = 'Padres del Fuego'
InvasionWarn30min = ["Jolly Roger's Army is on the move towards %s and spies tell us they're 30 minutes away.", "Spies have seen Jolly's army on the move towards %s and they will arrive in 30 minutes.", 'The spirits report that the Undead army is about to invade %s in 30 minutes.']
InvasionWarn20min = [
    'The Undead hordes are sailing quickly towards %s and will make land in 20 minutes.', 'The Undead army of Jolly Roger will attack %s in 20 minutes', 'Prepare yourselves, mates!  The Undead invasion of %s begins in 20 minutes.'
]
InvasionWarn10min = [
    'Beware the invasions - they are coming to %s in only 10 minutes!', 'Look lively mates, reports suggest the %s invasion is only 10 minutes away!', 'Last chance to get your ammo and potions, the invasion of %s starts in 10 minutes!'
]
InvasionWarn5min = [
    'Sharpen your steel and steady your nerves, the %s invasion is 5 minutes away!', 'Tell all your friends and guild members join in - %s invasion in 5 minutes!', "Don't dilly dally - get ready to battle as the Undead will arrive in %s in 5 minutes!"
]
InvasionWarn1min = [
    'Time to fight or flee for the invading army is only 1 minute away from %s!', "Jolly's Undead army arrives in %s in only 1 minute!", 'Time to fight or flee, mates!  The %s invasion starts in 1 minute!'
]
InvasionJollyRogerNextBrigade = makeHeadingString('Brigade %s Arriving', 2) + '\nNew enemies are arriving on the beaches! Defeat them to advance to the next wave. %s brigade(s) remaining.'
InvasionJollyRogerBrigadeUpdate = 'Brigade %s is attacking!\n %s brigade(s) remaining.'
InvasionJollyRogerComing = 'Jolly Roger is coming to attack the %s!\nDefeat Jolly Roger to drive back the invasion!'
InvasionJollyRogerBoss1 = "I don't really have time for this... but if you insist."
InvasionJollyRogerBoss2 = "There'll be no mercy. Prepare yourself."
InvasionJollyRogerBoss3 = "Ye useless scabs! I shall show ye how it's done!"
InvasionJollyRogerBoss4 = 'Must I do everything meself? Fools!'
InvasionJollyRogerBoss5 = 'Dogs! Must I do the battle for ye? Follow me now!'
InvasionJollyRogerMainZone1 = "Ha ha ha ha! This will be the pirates' funeral fire!"
InvasionJollyRogerMainZone2 = 'Are you prepared for your destiny?'
InvasionJollyRogerEndPlayerWin1 = "You'll pay dearly for this!"
InvasionJollyRogerEndPlayerWin2 = "This can't be happening!"
InvasionJollyRogerEndPlayerWin3 = "You've not seen the last of me!"
InvasionJollyRogerEndPlayerWin4 = 'These pitiful pirates are foiling me plans! Fall back! Retreat!'
InvasionJollyRogerEndPlayerLose1 = 'Victory is mine! Me power grows!'
InvasionJollyRogerEndPlayerLose2 = "We've won the fray, ye mongrels! Now, set sail for our next conquest."
InvasionJollyRogerEndPlayerLose3 = "We've won the day, ye dogs! Now, onto our next target!"
InvasionJollyRogerEndPlayerLose4 = 'What? Sparrow escaped? Curse his vile soul!'
from pirates.holiday.FleetHolidayGlobals import Configs as FHConfigs
from pirates.holiday.FleetHolidayGlobals import Msgs as FHMsgs
FleetHolidayMsgs = {
    FHMsgs.EF_EitcLaunch: "The East India Trading Company has deployed an Expedition Fleet led by a mighty Ship of the Line to Raven Cove!  The Trading Company is after El Patron's Lost Weapons!  Sink the Expedition Fleet to prevent the weapons from falling into the hands of the EITC!", FHMsgs.EF_EitcEscaped: "The East India Trading Company's Expedition Fleet has left the Caribbean and is sailing towards the island of Raven Cove.  It is too late to stop this fleet now!", FHMsgs.EF_EitcDefeated: "The East India Trading Company's Expedition Fleet has been sunk by the Pirates.  El Patron's Lost Weapons are safe for now...", FHMsgs.EF_NavyLaunch: "The Navy has deployed an Expedition Fleet led by a mighty Ship of the Line to Raven Cove!  The Navy is after El Patron's Lost Weapons!  Sink the Expedition Fleet to prevent the weapons from falling into the hands of the Navy!", FHMsgs.EF_NavyEscaped: "The Navy's Expedition Fleet has left the Caribbean and is sailing towards the island of Raven Cove.  It is too late to stop this fleet now!", FHMsgs.EF_NavyDefeated: "The Navy's Expedition Fleet has been sunk by the Pirates.  El Patron's Lost Weapons are safe for now...", FHMsgs.TF_EitcLaunch: "An East India Trading Company Treasure Fleet has set sail! This heavily armed Fleet is transporting part of El Patron's Lost Weapons. Sink the Treasure Fleet and plunder the Lost Weapons!", FHMsgs.TF_EitcEscaped: 'The EITC Treasure Fleet has reached its destination. It is too late to plunder this treasure now!', FHMsgs.TF_EitcDefeated: 'The EITC Treasure Fleet has been sunk, and the Treasure has been looted by the Pirates!', FHMsgs.TF_NavyLaunch: "A Navy Treasure Fleet has set sail! This heavily armed Fleet is transporting part of El Patron's Lost Weapons. Sink the Treasure Fleet and plunder the Lost Weapons!", FHMsgs.TF_NavyEscaped: 'The Navy Treasure Fleet has reached its destination. It is too late to plunder this treasure now!', FHMsgs.TF_NavyDefeated: 'The Navy Treasure Fleet has been sunk, and the Treasure has been looted by the Pirates!', FHMsgs.TF_EitcWarn10min: ['The EITC Treasure Fleets will weigh anchor in 10 minutes.', 'Prepare the sail!  EITC Treasure fleets leave port in 10 minutes.', 'Arm your cannons, mates.  EITC Treasure fleets set sail in 10 minutes.'], FHMsgs.TF_EitcWarn5min: ['The EITC Treasure Fleets are filled with loot and leaving in 5 minutes.', '5 minutes until the EITC Treasure Fleets embark from port.', 'Ready your cannons and sails, EITC Treasure Fleets sail in 5 Minutes.'], FHMsgs.TF_EitcWarn0min: ['Scouts have seen EITC Treasure Fleets leaving port - sink them now!', 'Get on the water, mates!  EITC Treasure fleets are under full sail!', 'Prepare to do battle mates!  The EITC Treasure Fleets are sailing now!'], FHMsgs.TF_NavyWarn10min: ['The Navy Treasure Fleets will weigh anchor in 10 minutes.', 'Prepare the sail!  Navy Treasure fleets leave port in 10 minutes.', 'Arm your cannons, mates.  Navy Treasure fleets set sail in 10 minutes.'], FHMsgs.TF_NavyWarn5min: ['The Navy Treasure Fleets are filled with loot and leaving in 5 minutes.', '5 minutes until the Navy Treasure Fleets embark from port.', 'Ready your cannons and sails, Navy Treasure Fleets sail in 5 Minutes.'], FHMsgs.TF_NavyWarn0min: ['Scouts have seen Navy Treasure Fleets leaving port - sink them now!', 'Get on the water, mates!  Navy Treasure fleets are under full sail!', 'Prepare to do battle mates!  The Navy Treasure Fleets are sailing now!']
}
from pirates.holiday.KrakenHolidayGlobals import Msgs as KHMsgs
KrakenHolidayMsgs = {
    KHMsgs.Launch: ['Let no joyful voice be heard! Let no man look up to the sky with hope! And let this day be cursed by we who ready to wake... the Kraken!', 'RAWR! is Kraken for I love you...', 'Every day and in every way, Kraken is getting better and better...'], KHMsgs.Escaped: ["That's one slippery squid", 'Pesky jellyfish swam away!'], KHMsgs.Defeated: ['Why do I suddenly have the hankering for fried calamari???']
}
QueenAnnesHolidayMsgs = {
    60: ["The Queen Anne's Revenge has been seen in the Caribbean under the command of a vile and mutinous crew. Keep an ear open for rumors of her whereabouts."],
    61: ["The Queen Anne's Revenge has vanished mysteriously. Keep a sharp eye and an even sharper sword. Legend has it that she will strike again soon."],
    62: ["The Queen Anne's Revenge has gone down. Be warned! This reprieve is only temporary. The Queen Anne's Revenge will set sail again with her vicious crew in tow."],
    63: ["The Queen Anne's Revenge has been spotted circling Isla Tormenta! Disable, grapple and board the ship then prepare to battle Her undead crew!"],
    64: ["The Queen Anne's Revenge has been spotted circling Isla Perdida! Disable, grapple and board the ship then prepare to battle Her undead crew!"],
    65: ["The Queen Anne's Revenge has been spotted circling Isla Cangrejos! Disable, grapple and board the ship then prepare to battle Her undead crew!"]
}
from pirates.holiday.CatalogHolidayGlobals import ConfigIds as CHConfigIds
CatalogHolidayNames = {
    CHConfigIds.CAT1: {
        'displayName': 'JANUARY',
        'tabName': 'JAN'
    }, CHConfigIds.CAT2: {
        'displayName': 'FEBRUARY',
        'tabName': 'FEB'
    }, CHConfigIds.CAT3: {
        'displayName': 'MARCH',
        'tabName': 'MAR'
    }, CHConfigIds.CAT4: {
        'displayName': 'APRIL',
        'tabName': 'APR'
    }, CHConfigIds.CAT5: {
        'displayName': 'MAY',
        'tabName': 'MAY'
    }, CHConfigIds.CAT6: {
        'displayName': 'JUNE',
        'tabName': 'JUNE'
    }, CHConfigIds.CAT7: {
        'displayName': 'JULY',
        'tabName': 'JULY'
    }, CHConfigIds.CAT8: {
        'displayName': 'AUGUST',
        'tabName': 'AUG'
    }, CHConfigIds.CAT9: {
        'displayName': 'SEPTEMBER',
        'tabName': 'SEP'
    }, CHConfigIds.CAT10: {
        'displayName': 'OCTOBER',
        'tabName': 'OCT'
    }, CHConfigIds.CAT11: {
        'displayName': 'NOVEMBER',
        'tabName': 'NOV'
    }, CHConfigIds.CAT12: {
        'displayName': 'DECEMBER',
        'tabName': 'DEC'
    }, CHConfigIds.CAT13: {
        'displayName': 'ZOMBIE',
        'tabName': 'ZOM'
    }, CHConfigIds.CAT14: {
        'displayName': 'French Fencer',
        'tabName': 'FRC'
    }, CHConfigIds.CAT15: {
        'displayName': "Town Mayor's Outfit",
        'tabName': 'Mayor'
    }, CHConfigIds.CAT16: {
        'displayName': 'CONQUISTADOR',
        'tabName': 'CNQ'
    }, CHConfigIds.CAT17: {
        'displayName': 'SEA SERPENT',
        'tabName': 'Serpent'
    }, CHConfigIds.CAT18: {
        'displayName': 'Merchant Voyager',
        'tabName': 'Merchant'
    }, CHConfigIds.CAT19: {
        'displayName': 'The Diplomat',
        'tabName': 'Diplomat'
    }, CHConfigIds.CAT20: {
        'displayName': 'Crimson Captain',
        'tabName': 'Crimson'
    }, CHConfigIds.CAT21: {
        'displayName': 'Warrior',
        'tabName': 'Warrior'
    }, CHConfigIds.CAT22: {
        'displayName': "Raven's Cove Mercenary",
        'tabName': 'RCM'
    }, CHConfigIds.Outfit_3: {
        'displayName': 'July 2010',
        'tabName': 'Jul 2010'
    }, CHConfigIds.Outfit_2: {
        'displayName': 'August 2010',
        'tabName': 'Aug 2010'
    }, CHConfigIds.Outfit_1: {
        'displayName': 'September 2010',
        'tabName': 'Sep 2010'
    }
}
from pirates.holiday.MessageHolidayGlobals import ConfigIds as MHConfigIds
MHCrewDaysMsg = 'Join us for Crew Days! Every Friday and Saturday from 3pm-8pm PST, meet at the docks of Port Royal, Tortuga and Padres del Fuego to start or join a crew with other pirates!'
from pirates.ai.HolidayGlobals import MSG_START_ALL, MSG_START_UNLIMITED, MSG_START_BASIC, MSG_ICON, MSG_END_ALL, MSG_END_UNLIMITED, MSG_END_BASIC, MSG_CHAT_STATUS, MSG_CHAT_STATUS_UNLIMITED, MSG_CHAT_STATUS_BASIC, MSG_BONFIRE, MSG_PIG, MSG_BONFIRE_STARTED, MSG_PORK_RECEIVED
holidayMessages = {
    HolidayGlobals.DOUBLEGOLDHOLIDAY: {
        MSG_START_ALL: (DoubleGoldStart, DoubleGoldStartChat),
        MSG_END_ALL: (DoubleGoldEnd, DoubleGoldEnd),
        MSG_CHAT_STATUS: DoubleGoldStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.DOUBLEGOLDHOLIDAYPAID: {
        MSG_START_ALL: (DoubleGoldFullStart, DoubleGoldFullStartChat),
        MSG_END_ALL: (DoubleGoldFullEnd, DoubleGoldFullEnd),
        MSG_CHAT_STATUS: DoubleGoldFullStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.DOUBLEXPHOLIDAY: {
        MSG_START_ALL: (DoubleXPStart, DoubleXPStartChat),
        MSG_END_ALL: (DoubleXPEnd, DoubleXPEnd),
        MSG_CHAT_STATUS: DoubleXPStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.DOUBLEXPHOLIDAYPAID: {
        MSG_START_ALL: (DoubleXPFullStart, DoubleXPFullStartChat),
        MSG_END_ALL: (DoubleXPFullEnd, DoubleXPFullEnd),
        MSG_CHAT_STATUS: DoubleXPFullStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.DOUBLELOOTHOLIDAY: {
        MSG_START_ALL: (DoubleLootStart, DoubleLootStartChat),
        MSG_END_ALL: (DoubleLootEnd, DoubleLootEnd),
        MSG_CHAT_STATUS: DoubleLootStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.BLACKJACKFRIDAY: {
        MSG_START_ALL: (BlackJackFridayStart, BlackJackFridayStartChat),
        MSG_END_ALL: (BlackJackFridayEnd, BlackJackFridayEndChat),
        MSG_CHAT_STATUS: BlackJackFridayStatus,
        MSG_ICON: 'friends'
    }, HolidayGlobals.FREEHATWEEK: {
        MSG_START_UNLIMITED: (FreeHatStartUnlimited, FreeHatStartUnlimitedChat),
        MSG_START_BASIC: (FreeHatStartUnlimited, FreeHatStartUnlimitedChat),
        MSG_ICON: 'hat'
    }, HolidayGlobals.FLIRTEMOTE: {}, HolidayGlobals.ZOMBIEEMOTE: {}, HolidayGlobals.SAINTPATRICKSDAY: {
        MSG_START_ALL: (StPatricksStartAll, StPatricksStartAll),
        MSG_END_ALL: (StPatricksEndAll, StPatricksEndAll),
        MSG_CHAT_STATUS: StPatricksStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.MOTHERSDAY: {
        MSG_START_UNLIMITED: (MothersDayStartUnlimited, MothersDayStartUnlimitedChat),
        MSG_START_BASIC: (MothersDayStartBasic, MothersDayStartBasicChat),
        MSG_CHAT_STATUS: MothersDayStatus,
        MSG_ICON: 'tattoo'
    }, HolidayGlobals.FATHERSDAY: {
        MSG_START_ALL: (FathersDayStart, FathersDayStartChat),
        MSG_CHAT_STATUS: FathersDayStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.FOURTHOFJULY: {
        MSG_START_ALL: (FourthOfJulyStart, FourthOfJulyStartChat),
        MSG_CHAT_STATUS: FourthOfJulyStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.HALFOFFCUSTOMIZATION: {
        MSG_START_ALL: (HalfOffCustomizationUnlimited, HalfOffCustomizationUnlimited),
        MSG_END_ALL: (HalfOffCustomizationEnd, HalfOffCustomizationEnd),
        MSG_CHAT_STATUS: HalfOffCustomizationStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.ALLACCESSWEEKEND: {
        MSG_START_BASIC: (UnlimitedAccessEventBasic, UnlimitedAccessEventBasic),
        MSG_END_BASIC: (UnlimitedAccessEventBasicEnd, UnlimitedAccessEventBasicEnd),
        MSG_CHAT_STATUS_BASIC: AllAccessHolidayStart,
        MSG_ICON: 'admin'
    }, HolidayGlobals.HALLOWEEN: {
        MSG_START_ALL: (HalloweenStart, HalloweenStartChat),
        MSG_END_ALL: (HalloweenEnd, HalloweenEnd),
        MSG_CHAT_STATUS: HalloweenStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.JOLLYROGERCURSE: {
        MSG_CHAT_STATUS: JollyRogerCurseStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.CURSEDNIGHT: {
        MSG_START_ALL: (CursedNightStart, CursedNightStart),
        MSG_END_ALL: (CursedNightEnd, CursedNightEnd),
        MSG_ICON: 'admin'
    }, HolidayGlobals.JOLLYCURSEAUTO: {}, HolidayGlobals.FOUNDERSFEAST: {
        MSG_START_ALL: (FoundersFeastStart, FoundersFeastStartChat),
        MSG_END_ALL: (FoundersFeastEnd, FoundersFeastEnd),
        MSG_CHAT_STATUS: FoundersFeastStatus,
        MSG_ICON: 'admin',
        MSG_BONFIRE: InteractFoundersFeastBonfire,
        MSG_PIG: InteractFoundersFeastPig,
        MSG_BONFIRE_STARTED: FoundersFeastBonfireAlreadyStarted,
        MSG_PORK_RECEIVED: FoundersFeastPorkChunkReceived
    }, HolidayGlobals.FREEITEMTHANKSGIVING: {
        MSG_START_UNLIMITED: (FreeBandanaStartUnlimited, FreeBandanaStartUnlimitedChat),
        MSG_START_BASIC: (FreeBandanaStartBasic, FreeBandanaStartBasicChat),
        MSG_ICON: 'hat'
    }, HolidayGlobals.WINTERFESTIVAL: {
        MSG_START_ALL: (WinterFestivalStart, WinterFestivalStartChat),
        MSG_END_ALL: (WinterFestivalEnd, WinterFestivalEnd),
        MSG_CHAT_STATUS: WinterFestivalStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.NEWYEARS: {
        MSG_START_ALL: (NewYearsStart, NewYearsStartChat),
        MSG_END_ALL: (NewYearsEnd, NewYearsEnd),
        MSG_CHAT_STATUS: NewYearsStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.VALENTINESDAY: {
        MSG_START_UNLIMITED: (ValentinesDayStartUnlimited, ValentinesDayStartUnlimitedChat),
        MSG_START_BASIC: (ValentinesDayStartBasic, ValentinesDayStartBasicChat),
        MSG_END_ALL: (ValentinesDayEnd, ValentinesDayEnd),
        MSG_CHAT_STATUS: ValentinesDayStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.DOUBLECROSS: {
        MSG_START_UNLIMITED: (DoubleCrossStart, DoubleCrossStart),
        MSG_START_BASIC: (DoubleCrossStartBasic, DoubleCrossStartBasic),
        MSG_ICON: 'admin'
    }, HolidayGlobals.INVASIONPORTROYAL: {
        MSG_START_ALL: (InvasionPortRoyalStart, InvasionPortRoyalStart),
        MSG_CHAT_STATUS: InvasionPortRoyalStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.WRECKEDGOVERNORSMANSION: {}, HolidayGlobals.INVASIONTORTUGA: {
        MSG_START_ALL: (InvasionTortugaStart, InvasionTortugaStart),
        MSG_CHAT_STATUS: InvasionTortugaStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.WRECKEDFAITHFULBRIDE: {}, HolidayGlobals.INVASIONDELFUEGO: {
        MSG_START_ALL: (InvasionDelFuegoStart, InvasionDelFuegoStart),
        MSG_CHAT_STATUS: InvasionDelFuegoStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.MARDIGRAS: {
        MSG_START_ALL: (MardiGrasStart, MardiGrasStart),
        MSG_END_ALL: (MardiGrasEnd, MardiGrasEnd),
        MSG_CHAT_STATUS: MardiGrasStatus,
        MSG_ICON: 'admin',
        MSG_BONFIRE: InteractMardiGrasBonfire,
        MSG_PIG: InteractMardiGrasPig,
        MSG_BONFIRE_STARTED: MardiGrasBonfireAlreadyStarted,
        MSG_PORK_RECEIVED: MardiGrasPorkChunkReceived
    }, HolidayGlobals.FLEETHOLIDAY: {
        None: {
            MSG_ICON: 'ship'
        }
    }, HolidayGlobals.FEASTOFSTRENGTH: {}, HolidayGlobals.EITCMOBILIZATION: {
        MSG_START_ALL: (EITCMobilizationStart, EITCMobilizationStart),
        MSG_CHAT_STATUS: EITCMobilizationStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.NAVYMOBILIZATION: {
        MSG_START_ALL: (NavyMobilizationStart, NavyMobilizationStart),
        MSG_CHAT_STATUS: NavyMobilizationStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.SKELMOBILIZATION: {
        MSG_START_ALL: (SkelMobilizationStart, SkelMobilizationStart),
        MSG_CHAT_STATUS: SkelMobilizationStatus,
        MSG_ICON: 'admin'
    }, HolidayGlobals.KRAKENHOLIDAY: {
        None: {
            MSG_ICON: 'ship'
        }
    }, HolidayGlobals.CATALOGHOLIDAY: {
        None: {
            MSG_ICON: 'loot'
        }
    }, HolidayGlobals.MESSAGEHOLIDAY: {
        None: {
            MSG_ICON: 'admin'
        },
        MHConfigIds.CrewDays: {
            MSG_START_ALL: (MHCrewDaysMsg, MHCrewDaysMsg),
            MSG_ICON: 'admin'
        }
    }, HolidayGlobals.QUEENANNES: {
        MSG_START_ALL: (QueenAnnesHolidayMsgs[60][0], QueenAnnesHolidayMsgs[60][0]),
        MSG_CHAT_STATUS: QueenAnnesHolidayMsgs[60][0],
        MSG_ICON: 'admin'
    }
}
JollyRogerTaunts = [
    'I love the smell of fresh souls.', 'Ha ha ha! This really is a laugh!', 'You fear me now, eh?', 'Jack Sparrow will need to find someone else to do his dirty work.', "Why don't you just submit to my power?", "This is child's play!", 'Submit to me!', "I've not had so much fun in days!", 'Nothing beats a good fight before a meal.', 'Your weapons are but a nuisance to me.', 'Bring me a real opponent!', 'Being dead has its benefits. Care to try it out?', "Is that all you've got?", 'Ha ha ha!', 'Ready to meet your maker?', "Let me show ye how it's done!", "Out of me way! I've got some souls to devour!", "Now I'm angry! And everyone will pay!", 'A pox on your town!', 'Ahhhhhh!', 'Ha ha ha!', 'You call that fighting?', "I'm really enjoying this!", 'Is that the best ye can do?'
]

def getJollyRogerTaunt(number):
    return JollyRogerTaunts[number]


InvasionLv = '??'
JollySays = 'Jolly Roger: %s'
InvasionMainZoneNames = {
    HolidayGlobals.getHolidayName(HolidayGlobals.INVASIONPORTROYAL): "Governor's Mansion", HolidayGlobals.getHolidayName(HolidayGlobals.INVASIONTORTUGA): 'Faithful Bride Tavern', HolidayGlobals.getHolidayName(HolidayGlobals.INVASIONDELFUEGO): 'Padres Del Fuego Town'
}

def getInvasionMainZoneName(holiday):
    return InvasionMainZoneNames[holiday]


CapturePointNames = {
    HolidayGlobals.getHolidayName(HolidayGlobals.INVASIONPORTROYAL): {
        1: 'Wharf Barricade',
        2: 'Beach Barricade',
        3: 'Bridge Barricade',
        4: 'Old Town Barricade',
        5: 'Kings Way Barricade',
        6: "Farmer's Row Barricade",
        7: "The Governor's Mansion"
    }, HolidayGlobals.getHolidayName(HolidayGlobals.INVASIONTORTUGA): {
        1: 'Harbor Barricade',
        2: "Smuggler's Beach Barricade",
        3: 'Gypsy Way Barricade',
        4: 'Shanty Town Barricade',
        5: 'West Wall Barricade',
        6: 'East Wall Barricade',
        7: 'The Faithful Bride Tavern'
    }, HolidayGlobals.getHolidayName(HolidayGlobals.INVASIONDELFUEGO): {
        1: 'Magma Ridge Barricade',
        2: 'Dock Barricade',
        3: 'Burning Pass Barricade',
        4: 'South Wall Barricade',
        5: "Devil's Pass Barricade",
        6: "Outcast's Den Barricade",
        7: 'Padres Town Walls'
    }
}
CapturePointAttacked = '%s is under attack!'
CapturePointDestroyed = '%s is destroyed!'
CapturePointLowHealth = '%s is nearly destroyed!'
TEMP_DOUBLE_REP = 'You earned a x2 reputation reward.\nYou currently have %s hours(s) and %s minute(s), before the reward expires. Type /x2 at the chat prompt to check the time remaining.'
TEMP_DOUBLE_REP_CHAT = 'You earned a x2 reputation reward.\nYou currently have %s hours(s) and %s minute(s), before the reward expires.'
NO_TEMP_DOUBLE_REP = 'You currently do not have a double reputation award'
WhitelistScrubList = [
    'yarr', 'arrr', 'garr', 'arrrrr'
]
WhiteListWarning = 'Words typed in \x01WLEnter\x01red\x02 are shown in \x01WLDisplay\x01italics\x02 and may not be visible to some players.'
EmoteCommands = {
    'coin': (EmoteGlobals.EMOTE_COIN_HEADS, EmoteGlobals.EMOTE_COIN_TAILS),
    'dance': EmoteGlobals.EMOTE_DANCE,
    'jig': EmoteGlobals.EMOTE_DANCE_JIG,
    'flex': EmoteGlobals.EMOTE_FLEX,
    'crazy': EmoteGlobals.EMOTE_CRAZY,
    'search': EmoteGlobals.EMOTE_SEARCHING,
    'sweep': EmoteGlobals.EMOTE_SWEEP,
    'primp': EmoteGlobals.EMOTE_PRIMP,
    'agree': EmoteGlobals.EMOTE_AGREE,
    'amazed': EmoteGlobals.EMOTE_AMAZED,
    'angry': EmoteGlobals.EMOTE_ANGRY,
    'celebrate': EmoteGlobals.EMOTE_CELEBRATE,
    'sleep': EmoteGlobals.EMOTE_SLEEP,
    'arrr': EmoteGlobals.EMOTE_ARRR,
    'bark': EmoteGlobals.EMOTE_BARK,
    'blink': EmoteGlobals.EMOTE_BLINK,
    'bored': EmoteGlobals.EMOTE_BORED,
    'bow': EmoteGlobals.EMOTE_BOW,
    'cackle': EmoteGlobals.EMOTE_CACKLE,
    'cheer': EmoteGlobals.EMOTE_CHEER,
    'chuckle': EmoteGlobals.EMOTE_CHUCKLE,
    'clap': EmoteGlobals.EMOTE_CLAP,
    'confused': EmoteGlobals.EMOTE_CONFUSED,
    'congrats': EmoteGlobals.EMOTE_CONGRATS,
    'grats': EmoteGlobals.EMOTE_CONGRATS,
    'congratulate': EmoteGlobals.EMOTE_CONGRATS,
    'cry': EmoteGlobals.EMOTE_CRY,
    'curious': EmoteGlobals.EMOTE_CURIOUS,
    'drink': EmoteGlobals.EMOTE_DRINK,
    'eat': EmoteGlobals.EMOTE_EAT,
    'cower': EmoteGlobals.EMOTE_FEAR,
    'fear': EmoteGlobals.EMOTE_FEAR,
    'flee': EmoteGlobals.EMOTE_FLEE,
    'frown': EmoteGlobals.EMOTE_FROWN,
    'gasp': EmoteGlobals.EMOTE_GASP,
    'giggle': EmoteGlobals.EMOTE_GIGGLE,
    'glare': EmoteGlobals.EMOTE_GLARE,
    'bye': EmoteGlobals.EMOTE_GOODBYE,
    'goodbye': EmoteGlobals.EMOTE_GOODBYE,
    'greet': EmoteGlobals.EMOTE_GREET,
    'grin': EmoteGlobals.EMOTE_GRIN,
    'growl': EmoteGlobals.EMOTE_GROWL,
    'hail': EmoteGlobals.EMOTE_HAIL,
    'happy': EmoteGlobals.EMOTE_HAPPY,
    'hello': EmoteGlobals.EMOTE_HELLO,
    'help': EmoteGlobals.EMOTE_HELP,
    'hiss': EmoteGlobals.EMOTE_HISS,
    'hungry': EmoteGlobals.EMOTE_HUNGRY,
    'impatient': EmoteGlobals.EMOTE_IMPATIENT,
    'tap': EmoteGlobals.EMOTE_IMPATIENT,
    'jk': EmoteGlobals.EMOTE_JK,
    'kidding': EmoteGlobals.EMOTE_JK,
    'laugh': EmoteGlobals.EMOTE_LAUGH,
    'lol': EmoteGlobals.EMOTE_LAUGH,
    'meow': EmoteGlobals.EMOTE_MEOW,
    'moo': EmoteGlobals.EMOTE_MOO,
    'no': EmoteGlobals.EMOTE_NO,
    'nod': EmoteGlobals.EMOTE_NOD,
    '9000': EmoteGlobals.EMOTE_POWERFUL,
    'ready': EmoteGlobals.EMOTE_READY,
    'roar': EmoteGlobals.EMOTE_ROAR,
    'rofl': EmoteGlobals.EMOTE_ROFL,
    'sad': EmoteGlobals.EMOTE_SAD,
    'salute': EmoteGlobals.EMOTE_SALUTE,
    'scared': EmoteGlobals.EMOTE_SCARED,
    'shrug': EmoteGlobals.EMOTE_SHRUG,
    'sigh': EmoteGlobals.EMOTE_SIGH,
    'smile': EmoteGlobals.EMOTE_SMILE,
    'sorry': EmoteGlobals.EMOTE_SORRY,
    'sry': EmoteGlobals.EMOTE_SORRY,
    'thirsty': EmoteGlobals.EMOTE_THIRSTY,
    'tired': EmoteGlobals.EMOTE_TIRED,
    'flirt': EmoteGlobals.EMOTE_VALENTINES,
    'vittles': EmoteGlobals.EMOTE_VITTLES,
    'wait': EmoteGlobals.EMOTE_WAIT,
    'wave': EmoteGlobals.EMOTE_WAVE,
    'wink': EmoteGlobals.EMOTE_WINK,
    'yawn': EmoteGlobals.EMOTE_YAWN,
    'yes': EmoteGlobals.EMOTE_YES,
    'zombie': EmoteGlobals.EMOTE_HALLOWEEN,
    'noisemaker': EmoteGlobals.EMOTE_NOISEMAKER,
    'hand': EmoteGlobals.EMOTE_BLACKHAND
}
EmoteMessagesSelf = {
    EmoteGlobals.EMOTE_COIN_FLIP: 'You flip a coin.', EmoteGlobals.EMOTE_COIN_HEADS: 'You flip a coin... Heads', EmoteGlobals.EMOTE_COIN_TAILS: 'You flip a coin... Tails', EmoteGlobals.EMOTE_CHANT_A: 'You dance.', EmoteGlobals.EMOTE_CHANT_B: 'You dance.', EmoteGlobals.EMOTE_DANCE: 'You dance.', EmoteGlobals.EMOTE_DANCE_JIG: 'You dance a jig.', EmoteGlobals.EMOTE_FLEX: 'You flex mightily.', EmoteGlobals.EMOTE_CRAZY: "You're going crazy!", EmoteGlobals.EMOTE_SEARCHING: 'You look around, searching for something.', EmoteGlobals.EMOTE_SWEEP: 'You sweep the ground clean.', EmoteGlobals.EMOTE_PRIMP: 'You check your nails.', EmoteGlobals.EMOTE_AGREE: 'You agree.', EmoteGlobals.EMOTE_AMAZED: 'You are amazed!', EmoteGlobals.EMOTE_ANGRY: 'You look angry.', EmoteGlobals.EMOTE_CELEBRATE: 'You celebrate!', EmoteGlobals.EMOTE_SLEEP: 'You look sleepy.', EmoteGlobals.EMOTE_ARRR: 'Arrrrrrr!', EmoteGlobals.EMOTE_BARK: 'You bark like a wild dog!', EmoteGlobals.EMOTE_BLINK: 'You blink.', EmoteGlobals.EMOTE_BORED: 'You look bored.', EmoteGlobals.EMOTE_BOW: 'You bow politely.', EmoteGlobals.EMOTE_CACKLE: 'You cackle!', EmoteGlobals.EMOTE_CHEER: 'You cheer!', EmoteGlobals.EMOTE_CHUCKLE: 'You chuckle softly.', EmoteGlobals.EMOTE_CLAP: 'You clap!', EmoteGlobals.EMOTE_CONFUSED: 'You look confused.', EmoteGlobals.EMOTE_CONGRATS: 'You congratulate everyone.', EmoteGlobals.EMOTE_CRY: 'You cry.', EmoteGlobals.EMOTE_CURIOUS: 'You look curious.', EmoteGlobals.EMOTE_DRINK: 'You pour a drink.', EmoteGlobals.EMOTE_EAT: 'You munch on some food.', EmoteGlobals.EMOTE_FEAR: 'You cower in fear.', EmoteGlobals.EMOTE_FLEE: 'You flee in terror!', EmoteGlobals.EMOTE_FROWN: 'You frown.', EmoteGlobals.EMOTE_GASP: 'You gasp!', EmoteGlobals.EMOTE_GIGGLE: 'You giggle.', EmoteGlobals.EMOTE_GLARE: 'You glare angrily.', EmoteGlobals.EMOTE_GOODBYE: 'You wave goodbye.', EmoteGlobals.EMOTE_GREET: 'You greet everyone around you.', EmoteGlobals.EMOTE_GRIN: 'You grin.', EmoteGlobals.EMOTE_GROWL: 'You growl angrily.', EmoteGlobals.EMOTE_HAIL: 'You hail everyone around you.', EmoteGlobals.EMOTE_HALLOWEEN: "You're dancing like a zombie!", EmoteGlobals.EMOTE_HAPPY: 'You are happy!', EmoteGlobals.EMOTE_HELLO: 'You say hello!', EmoteGlobals.EMOTE_HELP: 'You call out for help!', EmoteGlobals.EMOTE_HISS: 'You hiss menacingly.', EmoteGlobals.EMOTE_HUNGRY: 'You look hungry.', EmoteGlobals.EMOTE_IMPATIENT: 'You tap your foot impatiently.', EmoteGlobals.EMOTE_JK: "You let everyone know you're just kidding!", EmoteGlobals.EMOTE_LAUGH: 'You laugh!', EmoteGlobals.EMOTE_MEOW: 'You meow like a cat.', EmoteGlobals.EMOTE_MOO: 'You moo.  Moooooooo!', EmoteGlobals.EMOTE_NO: 'You say, NO.', EmoteGlobals.EMOTE_NOD: 'You nod.', EmoteGlobals.EMOTE_POWERFUL: 'You are far too mighty for these weaklings!', EmoteGlobals.EMOTE_READY: 'You are ready!', EmoteGlobals.EMOTE_ROAR: 'You roar loudly!', EmoteGlobals.EMOTE_ROFL: 'You roll on the floor laughing.', EmoteGlobals.EMOTE_SAD: 'You look sad.', EmoteGlobals.EMOTE_SALUTE: 'You salute.', EmoteGlobals.EMOTE_SCARED: 'You are scared!', EmoteGlobals.EMOTE_SHRUG: 'You shrug.', EmoteGlobals.EMOTE_SIGH: 'You sigh softly.', EmoteGlobals.EMOTE_SMILE: 'You smile.', EmoteGlobals.EMOTE_SORRY: 'You apologize.  Sorry!', EmoteGlobals.EMOTE_THIRSTY: 'You look thirsty.', EmoteGlobals.EMOTE_TIRED: 'You look tired.', EmoteGlobals.EMOTE_VALENTINES: 'You wink.', EmoteGlobals.EMOTE_VALENTINES_A: 'You wink A!', EmoteGlobals.EMOTE_VALENTINES_B: 'You wink B!', EmoteGlobals.EMOTE_VALENTINES_C: 'You wink C!', EmoteGlobals.EMOTE_VALENTINES_D: 'You wink D!', EmoteGlobals.EMOTE_VALENTINES_E: 'You wink E!', EmoteGlobals.EMOTE_VITTLES: 'You ask around for something to eat.', EmoteGlobals.EMOTE_WAIT: 'You ask everyone to wait.', EmoteGlobals.EMOTE_WAVE: 'You wave.', EmoteGlobals.EMOTE_WINK: 'You wink.', EmoteGlobals.EMOTE_YAWN: 'You yawn.', EmoteGlobals.EMOTE_YES: 'You say, Yes!', EmoteGlobals.EMOTE_NOISEMAKER: 'You make some noise!', EmoteGlobals.EMOTE_BLACKHAND: "Your hand doesn't look like it contains an Evil Curse of Doom..."
}
EmoteMessagesThirdPerson = {
    EmoteGlobals.EMOTE_COIN_FLIP: '%s flips a coin.', EmoteGlobals.EMOTE_COIN_HEADS: '%s flips a coin... Heads', EmoteGlobals.EMOTE_COIN_TAILS: '%s flips a coin... Tails', EmoteGlobals.EMOTE_CHANT_A: '%s dances.', EmoteGlobals.EMOTE_CHANT_B: '%s dances.', EmoteGlobals.EMOTE_DANCE: '%s dances.', EmoteGlobals.EMOTE_DANCE_JIG: '%s dances a jig.', EmoteGlobals.EMOTE_FLEX: '%s flexes mightily.', EmoteGlobals.EMOTE_LUTE: '%s pulls out a lute and begins to play.', EmoteGlobals.EMOTE_FLUTE: '%s pulls out a flute and begins to play.', EmoteGlobals.EMOTE_CRAZY: '%s is going crazy!', EmoteGlobals.EMOTE_SEARCHING: '%s looks around, searching for something.', EmoteGlobals.EMOTE_SWEEP: '%s sweeps the ground clean.', EmoteGlobals.EMOTE_PRIMP: '%s checks her nails.', EmoteGlobals.EMOTE_AGREE: '%s agrees.', EmoteGlobals.EMOTE_AMAZED: '%s is amazed!', EmoteGlobals.EMOTE_ANGRY: '%s looks angry.', EmoteGlobals.EMOTE_CELEBRATE: '%s celebrates.', EmoteGlobals.EMOTE_SLEEP: '%s looks sleepy.', EmoteGlobals.EMOTE_ARRR: '%s says, "Arrrrrrr!"', EmoteGlobals.EMOTE_BARK: '%s barks like a wild dog!', EmoteGlobals.EMOTE_BLINK: '%s blinks.', EmoteGlobals.EMOTE_BORED: '%s looks bored.', EmoteGlobals.EMOTE_BOW: '%s bows politely.', EmoteGlobals.EMOTE_CACKLE: '%s cackles!', EmoteGlobals.EMOTE_CHEER: '%s cheers!', EmoteGlobals.EMOTE_CHUCKLE: '%s chuckles softly.', EmoteGlobals.EMOTE_CLAP: '%s claps!', EmoteGlobals.EMOTE_CONFUSED: '%s looks confused.', EmoteGlobals.EMOTE_CONGRATS: '%s congratulates everyone.', EmoteGlobals.EMOTE_CRY: '%s cries.', EmoteGlobals.EMOTE_CURIOUS: '%s looks curious.', EmoteGlobals.EMOTE_DRINK: '%s pours a drink.', EmoteGlobals.EMOTE_EAT: '%s munches on some food.', EmoteGlobals.EMOTE_FEAR: '%s cowers in fear.', EmoteGlobals.EMOTE_FLEE: '%s flees in terror!', EmoteGlobals.EMOTE_FROWN: '%s frowns.', EmoteGlobals.EMOTE_GASP: '%s gasps!', EmoteGlobals.EMOTE_GIGGLE: '%s giggles.', EmoteGlobals.EMOTE_GLARE: '%s glares angrily.', EmoteGlobals.EMOTE_GOODBYE: '%s waves goodbye.', EmoteGlobals.EMOTE_GREET: '%s greets everyone nearby.', EmoteGlobals.EMOTE_GRIN: '%s grins.', EmoteGlobals.EMOTE_GROWL: '%s growls angrily.', EmoteGlobals.EMOTE_HAIL: '%s hails everyone nearby.', EmoteGlobals.EMOTE_HALLOWEEN: '%s is dancing like a zombie!', EmoteGlobals.EMOTE_HAPPY: '%s is happy!', EmoteGlobals.EMOTE_HELLO: '%s says hello!', EmoteGlobals.EMOTE_HELP: '%s calls out for help!', EmoteGlobals.EMOTE_HISS: '%s hisses menacingly.', EmoteGlobals.EMOTE_HUNGRY: '%s looks hungry.', EmoteGlobals.EMOTE_IMPATIENT: '%s waits impatiently.', EmoteGlobals.EMOTE_JK: '%s is just kidding!', EmoteGlobals.EMOTE_LAUGH: '%s laughs!', EmoteGlobals.EMOTE_MEOW: '%s meows like a cat.', EmoteGlobals.EMOTE_MOO: '%s moos.  Moooooooo!', EmoteGlobals.EMOTE_NO: '%s says, NO.', EmoteGlobals.EMOTE_NOD: '%s nods.', EmoteGlobals.EMOTE_POWERFUL: '%s is far too mighty for these weaklings!', EmoteGlobals.EMOTE_READY: '%s is ready!', EmoteGlobals.EMOTE_ROAR: '%s roars loudly!', EmoteGlobals.EMOTE_ROFL: '%s rolls on the floor laughing.', EmoteGlobals.EMOTE_SAD: '%s looks sad.', EmoteGlobals.EMOTE_SALUTE: '%s salutes.', EmoteGlobals.EMOTE_SCARED: '%s is scared!', EmoteGlobals.EMOTE_SHRUG: '%s shrugs.', EmoteGlobals.EMOTE_SIGH: '%s sighs softly.', EmoteGlobals.EMOTE_SMILE: '%s smiles.', EmoteGlobals.EMOTE_SORRY: '%s apologizes.  Sorry!', EmoteGlobals.EMOTE_THIRSTY: '%s looks thirsty.', EmoteGlobals.EMOTE_TIRED: '%s looks tired.', EmoteGlobals.EMOTE_VALENTINES: '%s winks.', EmoteGlobals.EMOTE_VALENTINES_A: '%s winks A!', EmoteGlobals.EMOTE_VALENTINES_B: '%s winks B!', EmoteGlobals.EMOTE_VALENTINES_C: '%s winks C!', EmoteGlobals.EMOTE_VALENTINES_D: '%s winks D!', EmoteGlobals.EMOTE_VALENTINES_E: '%s winks E!', EmoteGlobals.EMOTE_VITTLES: '%s asks around for something to eat.', EmoteGlobals.EMOTE_WAIT: '%s asks everyone to wait.', EmoteGlobals.EMOTE_WAVE: '%s waves.', EmoteGlobals.EMOTE_WINK: '%s winks.', EmoteGlobals.EMOTE_YAWN: '%s yawns.', EmoteGlobals.EMOTE_YES: '%s says, Yes!', EmoteGlobals.EMOTE_NOISEMAKER: '%s is making some noise!', EmoteGlobals.EMOTE_BLACKHAND: '%s looks almost completely Evil Curse of Doom free.'
}
CpuWarning = "Warning! \n\nYour CPU's frequency is currently running at %.4f GHz instead of the maximum %.4f GHz.  As a result, your gaming experience might be affected."
RewardCongratulations = 'Congratulations!'
RewardBlackPearlComplete = 'Black Pearl Story Quest Complete'
RewardBlackPearlReward = 'You have unlocked the Leadership sailing skill'
RewardBlackPearlDescription = 'This skill increases the rate of recharge for sailing and cannon\nskills.  Use it strategically to tip a battle against your foes!\n\nYou can replay the Black Pearl Quest anytime through\n Treasure Maps under the Lookout Panel.'
RewardNotorietyLessThanMax = 'Your Notoriety Level: %s\n Current Notoriety Level Cap: %s'
RewardNotorietyAtMax = 'You have reached the current Notoriety level cap of %s\n and mastered the following skills:'
RewardTodo = 'To become more notorious, continue to level your unmastered skills:'
RewardStayTuned = "The adventure of Raven's Cove unlocks at level 30."
RewardLevelOfMax = 'Level %s of %s'
RewardLevelLocked = 'Locked'
RewardVoodooDollComplete = 'Voodoo Doll Quest Complete'
RewardVoodooDollReward = 'You have received the voodoo doll weapon'
RewardVoodooDollDescription = 'This weapon allows you to battle foes and heal friends!'
RewardDaggerComplete = 'Dagger Quest Complete'
RewardDaggerReward = 'You have received the dagger weapon'
RewardDaggerDescription = 'This weapon is handy for both close and range attacks!'
RewardVoodooStaffComplete = 'Voodoo Staff Quest Complete'
RewardVoodooStaffReward = 'You have received the voodoo staff weapon'
RewardVoodooStaffDescription = 'This weapon does not need to attune to a target,\nbut make sure it is fully charged!'
RewardGrenadeComplete = 'Grenade Quest Complete'
RewardGrenadeReward = 'You have received the grenade weapon'
RewardGrenadeDescription = 'Toss it to kill foes but stand clear of the impact spot!'
RewardRavensCoveComplete = "Raven's Cove Story Quest Complete"
RewardRavensCoveRewardA = 'You have received a ' + ItemNames.get(ItemGlobals.BITTER_END)
RewardRavensCoveRewardB = 'You have received a ' + ItemNames.get(ItemGlobals.SPINECREST_SWORD)
RewardRavensCoveRewardC = 'You have received a ' + ItemNames.get(ItemGlobals.NAUTILUS_BLADE)
RewardRavensCoveDescription = "Maybe questing for a 'cursed' blade wasn't such a good idea?\nYou are left to wonder... what is the nature of this evil?\n\n You can now use the 'hand' emote"
CodeSubmitting = 'Redeeming Code %s'
CodeRedemptionGood = 'Code Redeemed'
CodeRedemptionTimeout = 'Code Redemption Failed. Did not get response from server, try again later'
CodeRedemptionBad = 'Code Redemption Failed. Perhaps the code was mistyped or already used'
CodeRedemptionFull = 'Code Redemption Failed. Free up an appropriate inventory spot and try again'
CodeRedemptionGold = MoneyName
CodeRedemptionFreeHat = 'Free Hat Week Hat'
CodeRedemptionKrakenTattoo = 'Octopus Tattoo - Call of the Kraken Exclusive'
CodeRedemptionDarkfireCutlass = 'Darkfire Cutlass'
CodeRedemptionFlatulentFizz = 'Flatulent Fizz'
CodeRedemptionBlackBuccaneerHat = 'Black Buccaneer Hat'
CodeRedemptionSeafangBlade = 'Seafang Blade'
CodeRedemptionSwordOfTriton = 'Sword of Triton'
CodeRedemptionHaymakerPistol = 'Haymaker Pistol'
CodeRedemptionZombieKababBayonet = 'Zombie Kabab Bayonet'
CodeRedemptionSpectralCutlass = 'Spectral Cutlass'
CodeRedemptionNemesisBlade = 'Nemesis Blade'
CodeRedemptionDarkfrostBlade = 'Darkfrost Blade'
CodeRedemptionSuperReputationPotion = 'Super Reputation Potion'
CodeRedemptionScoundrelHat = 'Scoundrel Hat'
CodeRedemptionGoldenKnuckles = ItemNames[ItemGlobals.GOLDEN_KNUCKLES]
CodeRedemptionNorringtonsSpyglass = ItemNames[ItemGlobals.NORRINGTON_SPYGLASS]
CodeRedemptionElixir = InventoryTypeNames[InventoryType.Potion4]
CodeRedemptionPotionHeadOnFire = InventoryTypeNames[InventoryType.HeadFire]
CodeRedemptionPotionInvis2 = InventoryTypeNames[InventoryType.InvisibilityLvl2]
CodeRedemptionJackSparrowBlade = ItemNames[ItemGlobals.JACK_SPARROW_BLADE]
CodeRedemptionJackSparrowRevenge = ItemNames[ItemGlobals.JACK_SPARROW_REVENGE]
CodeRedemptionHeartOfPadres = ItemNames[ItemGlobals.HEART_OF_PADRES_DEL_FUEGO]
CodeRedemptionAmmoFury = InventoryTypeNames[InventoryType.AmmoFury]
CodeRedemptionLostBladeOfLeviathan = ItemNames[ItemGlobals.CURSED_BLADE_47]
CodeRedemptionLostSwordOfElPatron = ItemNames[ItemGlobals.LOST_SWORD_OF_EL_PATRON]
CodeRedemptionBarbossaFury = ItemNames[ItemGlobals.BARBOSSA_FURY]
CodeRedemptionScimitar42 = ItemNames[ItemGlobals.SCIMITAR_42]
CodeRedemptionScimitar46 = ItemNames[ItemGlobals.SCIMITAR_46]
CodeRedemptionScimitar47 = ItemNames[ItemGlobals.SCIMITAR_47]
CodeRedemptionScimitar48 = ItemNames[ItemGlobals.SCIMITAR_48]
CodeRedemptionSummonChicken = ItemNames[ItemGlobals.POTION_SUMMON_CHICKEN]
CodeRedemptionSummonWasp = ItemNames[ItemGlobals.POTION_SUMMON_WASP]
CodeRedemptionSummonDog = ItemNames[ItemGlobals.POTION_SUMMON_DOG]
ShipPVPQuestFrench = 'French'
ShipPVPQuestSpanish = 'Spanish'
ShipPVPQuestKillShip = 'ship'
ShipPVPQuestKillShipCap = 'Ship'
ShipPVPQuestKillPirate = 'pirate'
ShipPVPQuestKillPirateCap = 'Pirate'
ShipPVPQuestUseShip = 'ship'
ShipPVPQuestUseCannon = 'cannon'
ShipPVPQuestUseCannonCap = 'Cannon'
ShipPVPQuestGameName = 'Ship PVP'
ShipPVPQuestSingleNumA = 'Sink a \x01questObj\x01%s\x02 ship in \x01questObj\x01%s\x02'
ShipPVPQuestSingleNumB = 'Defeat a \x01questObj\x01%s\x02 pirate in \x01questObj\x01%s\x02'
ShipPVPQuestSingleAnyNumA = 'Sink a \x01questObj\x01ship\x02 in \x01questObj\x01%s\x02'
ShipPVPQuestSingleAnyNumB = 'Defeat a \x01questObj\x01pirate\x02 in \x01questObj\x01%s\x02'
ShipPVPQuestUsingA = ' using a \x01questObj\x01%s\x02'
ShipPVPQuestUsingACap = ' Using A %s'
ShipPVPQuestWithoutSinking = ' without sinking'
ShipPVPQuestWithoutSinkingCap = ' Without Sinking'
ShipPVPQuestMultA = 'Sink \x01questObj\x01%s %s\x02 ships in \x01questObj\x01%s\x02'
ShipPVPQuestMultB = 'Defeat \x01questObj\x01%s %s\x02 pirates in \x01questObj\x01%s\x02'
ShipPVPQuestMultAnyA = 'Sink \x01questObj\x01%s ships\x02 in \x01questObj\x01%s\x02'
ShipPVPQuestMultAnyB = 'Defeat \x01questObj\x01%s pirates\x02 in \x01questObj\x01%s\x02'
ShipPVPQuestDamageA = 'Do \x01questObj\x01%s\x02 points damage to \x01questObj\x01%s\x02 ships in \x01questObj\x01%s\x02'
ShipPVPQuestDamageB = 'Do \x01questObj\x01%s\x02 points damage to \x01questObj\x01%s\x02 pirates in \x01questObj\x01%s\x02'
ShipPVPQuestDamageAnyA = 'Do \x01questObj\x01%s\x02 points of damage to \x01questObj\x01ships\x02 in \x01questObj\x01%s\x02'
ShipPVPQuestDamageAnyB = 'Do \x01questObj\x01%s\x02 points of damage to \x01questObj\x01pirates\x02 in \x01questObj\x01%s\x02'
ShipPVPQuestDamageAnyC = 'Do \x01questObj\x01%s\x02 points of damage in \x01questObj\x01%s\x02'
ShipPVPQuestProgNumA = 'A %s %s Defeated In %s'
ShipPVPQuestProgNumB = 'A %s Defeated In %s'
ShipPVPQuestProgNumC = '%d/%d %s %ss Defeated In %s'
ShipPVPQuestProgNumD = '%d/%d %ss Defeated In %s'
ShipPVPQuestProgDamA = '%d/%d Points Of Damage To %s %ss In %s'
ShipPVPQuestProgDamB = '%d/%d Points Of Damage Against The %s In %s'
ShipPVPQuestProgDamC = '%d/%d Points Of Damage To %ss In %s'
ShipPVPQuestProgDamD = '%d/%d Points Of Damage In %s'
FeedbackFormTitle = 'Feedback Form'
FeedbackFormMessage = 'Please select a category from the list on the right and provide your feedback below. Thank you for helping us to improve the game!'
FeedbackFormCatItems = ['Quests', 'Weapons', 'Tech', 'Ships', 'PVP', 'Social', 'General', 'Crews', 'Guilds', 'Potions', 'Ship Repair', 'Cannons', 'Fishing']
FeedbackButtonHelp = 'Send Feedback'
FeedbackFormSend = 'Send'
FeedbackManageButton = 'Manage Account'
townfolkHelpText = {
    1: ["Ready to fly the French colours on that ship of yers?\x07 Be aware that sailing from an island like this, ye must know a thing or two.\x07First, Pirates who choose to embark from this scrap of an island will be thrown into a battle... whether they be wantin' to or not.\x07Second, be wary of the sail colours around ye. That way a pirate knows who's friend and who's foe.\x07And if ye be needin' to check your score, press the ~ button. That gives a ship's score AND its bounty.\x07Pirates earn both for sinkin' enemy ships. The higher a bounty, the more it's worth.\x07Fair winds and good luck, mate... ye be needin' both!"],
    2: ["Ready to fly the Spanish colours on that ship of yers?\x07Be aware that sailing from an island like this, ye must know a thing or two.\x07First, Pirates who choose to embark from this scrap of an island will be thrown into a battle... whether they be wantin' to or not.\x07Second, be wary of the sail colours around ye. That way a pirate knows who's friend and who's foe.\x07And if ye be needin' to check your score, press the ~ button. That gives a ship's score AND its bounty.\x07Pirates earn both for sinkin' enemy ships. The higher a bounty, the more it's worth.\x07Fair winds and good luck, mate... ye be needin' both!"],
    3: ["Please excuse me master, Pierre le Porc, he's had a bit of stress lately and isn't feeling so grand.\x07In his... absence, I'll brief ye on the situation and specifics of how the French can use your skills.\x07See, Pirate Lord Le Porc has claimed this island and others as his own.\x07There's only one problem though, he's not the only Pirate Lord lookin' to lay claim on what ain't his, savvy?\x07A Spanish Pirate Lord name of Garcia de la Avaricia thinks he's running these islands too!\x07A pirate like yerself can make earn quite a reputation in this fight and Pierre would be most grateful.\x07So consider yerself a true Frenchmen when ye set sail from this island mate, 'cause the Spanish sure will..."],
    4: ["Please excuse me master, Garcia de la Avaricia, he's had a bit of stress lately and isn't feeling so grand.\x07In his... absence, I'll brief ye on the situation and specifics of how the Spanish can use your skills.\x07See, Pirate Lord Avaricia has claimed this island and others as his own.\x07There's only one problem though, he's not the only Pirate Lord looking to lay claim on what ain't his, savvy?\x07A French Pirate Lord name of Le Porc thinks he's running these islands too!\x07A pirate like yerself can make earn quite a reputation in this fight and Garcia would be most grateful.\x07So consider yerself a true Spaniard when ye set sail from this island mate, 'cause the French sure will..."]
}
MAGICWORD_GMNAMETAG = 'GM NameTag Options:\nenable, disable, setString <string>,\nsetColor <red|green|blue|gold|white>'
CrewMemberAcquired = '%s had joined the Black Pearl Crew!'
ShowBlackPearlCrew = 'Show Crew'
HideBlackPearlCrew = 'Hide Crew'
SongTitleUnknown = '???'
SongComingSoon = 'Coming Soon...'
SongUndiscovered = 'Undiscovered'
ZombieNoDoors = 'This door is barricaded from the inside!'
ZombieNoBoats = 'Jolly Roger commands you to attack the island!'
ZombieNoPeople = 'We will never serve Jolly Roger!'
ShipNeedCompass = 'You need to get the compass from Tia Dalma before you can board a ship'
ShipRepaired = 'Your ship has been repaired.'
TargetsInHere = '\n\x01questObj\x01Targets are in this area!'
TargetsCloseBy = '\n\x01questObj\x01Targets are close by!'
TargetsInThere = '\n\x01questObj\x01Closest targets are in %s'

def getServerTimeString(secondsSinceEpoch):
    return 'Server Time: %s' % datetime.datetime.fromtimestamp(secondsSinceEpoch).ctime()


def requiresAnIndefiniteArticle(stringList = []):
    vowels = [
        'A', 'a', 'E', 'e', 'I', 'i', 'O', 'o'
    ]
    for string in stringList:
        if string:
            for letter in string:
                if letter != ' ':
                    if letter in vowels:
                        return True
                    return False

    return False


GypsyPotionCraftingTitle = 'Potion Brewing'
GypsyPotionCraftingMessage = "I can see the power in you. I'd wager you could brew a potion or two. Visit a Potion table nearby to test your skill in the art of brewing potions. Maybe the fates will see you become a master. "
GypsyPotionCraftingClose = 'Close'
NoPotionsWhileUndeadWarning = "The Undead can't brew potions!"
CannonDefense = {
    'Help': 'Help',
    'ExitCannon': 'Do you wish to exit the Cannon Defense game?',
    'TreasureRemaining': 'Treasure Remaining',
    'Treasure': 'Treasure',
    'DizzyHit': "You're Dizzy!\nShake your mouse quickly!",
    'DizzyChatNotification': '%s got hit by a barrel!',
    'WaveLabel': 'Wave',
    'WaveComplete': 'Wave %s Complete!',
    'GameOver': 'All riches are stolen!',
    'NextWave': 'Next wave in %s seconds...',
    'ShipsSunkWave': 'Hits on ships:',
    'DamageDealtWave': 'Damage dealt:',
    'AccuracyWave': 'Accuracy:',
    'ShotsFiredWave': 'Shots fired:',
    'SlotEmpty': 'Empty',
    'NotApplicable': 'n/a',
    'WaveResults': 'Wave Results',
    'TreasureStolen': 'Attackers stole:',
    'TreasureRemaining': 'Wealth remaining:',
    'TreasureEarned': 'On shore wealth has increased by \x01CopperGold\x01%s treasure\x02',
    'PayShare': 'Your Pay Share: \x01CopperGold\x01%s Gold\x02',
    'PayShareBonus': 'Your Pay Share: \x01CopperGold\x01%s Gold\x02 \x01CPGreen\x01(+%s Holiday Bonus)\x02',
    'TimePlayed': 'Time Played:',
    'GoldEarned': 'Gold Earned:',
    'Report': 'Defender Report',
    'GameTotals': 'Game Totals:',
    'Gold': 'Gold',
    'Previous': 'Previous',
    'Next': 'Next',
    'Exit': 'Exit',
    'Continue': 'Ready?',
    'Minutes': 'Minutes',
    'Seconds': 'Seconds',
    'Waiting': "Waiting for all players to click 'Ready'!",
    'PlayerIdleKicked': 'was kicked for idle.',
    'PlayerJoined': 'joined the game.',
    'PlayerQuit': 'quit the game.'
}
DazedHelpText = 'Dazed!\nShake your mouse!'
CannonDefenseHelp = {
    'MineHeader': 'Mine Resources',
    'MineBody': 'If the bandits steal all the treasure, you lose!',
    'AmmoPanelHeader': 'Ammo Panel',
    'AmmoPanelBody': 'Buy new ammo here using Navy Bank Notes.\n\nYou must have a free ammo slot below to buy a new ammo type.',
    'WaveHeader': 'Wave Dial',
    'WaveBody': 'This shows the current wave number and how long the wave will last.',
    'AmmoHeader': 'Ammo Slots',
    'AmmoBody': 'Ammo you buy is kept here. Click to select which to fire.\n\nNew slots will unlock with higher Navy Cannon Experience.\n\nSell old ammo types to make room for new ones!',
    'ExitHeader': 'Exit Mini-Game',
    'BeginGame': 'Go!',
    'HelpHeader': 'Hide Help Overlay'
}
CannonDefenseLevelUp = '%s Level %d'
CannonDefenseAmmoUnlocked = 'Unlocked %s Ammo'
CannonDefenseAmmoDesc = '%s\nCost: %d\nAmount: %s\n\n%s'
CannonDefenseAmmoUnlockedAt = 'Unlocked at Level %d\n\n%s'
NoAmmoSlot = 'No empty ammo slot available'
NotEnoughBankNotes = 'More banknotes needed'
Unlimited = 'Unlimited'
SellButton = 'Sell Ammo'
BankNotes = 'Banknotes: \n%d'
CannonDefenseAmmoTypeDesc = {
    InventoryType.DefenseCannonRoundShot: 'Basic Navy ammo', InventoryType.DefenseCannonMine: 'They float and explode!', InventoryType.DefenseCannonTargetedShot: 'Guaranteed accurate!', InventoryType.DefenseCannonHotShot: 'Sets ships on fire!', InventoryType.DefenseCannonScatterShot: 'Fires a clustershot', InventoryType.DefenseCannonPowderKeg: 'Shoot it for massive damage!', InventoryType.DefenseCannonSmokePowder: 'Confuse ships to slow them!', InventoryType.DefenseCannonBullet: 'Flies straight, hits hard!', InventoryType.DefenseCannonColdShot: 'Freeze the sea, and ships!', InventoryType.DefenseCannonBomb: 'BOOM!!!', InventoryType.DefenseCannonChumShot: 'Sharks love bait!', InventoryType.DefenseCannonFireStorm: 'Burn the ocean!', InventoryType.DefenseCannonEmpty: 'Empty'
}
PotionGui = {
    'ExitButton': 'Exit',
    'ExitTitle': 'Exit Potion Brewing',
    'AbortAndExitText': 'You will lose your progress on this recipe.  Do you want to stop brewing potions?',
    'ExitText': 'Do you want to stop brewing potions?',
    'SwitchTitle': 'Switch Recipe',
    'SwitchText': 'You will lose your progress on this recipe.  Do you want to brew a different potion?',
    'FailTitle': 'Game Over',
    'FailText': 'You ran out of space on the board.  This potion cannot be completed.',
    'WinTitle': 'Congratulations!',
    'WinText': 'You have made',
    'XPLabel': 'Rep.',
    'XPLabelBonus': '%s Rep. (+%s Holiday Bonus)',
    'PlayAgainButton': 'Continue',
    'StopButton': 'Exit',
    'AcceptButton': 'X',
    'HintTitle': 'How to brew potions :',
    'HintToggle': 'Show Potion Brewing Hints',
    'HintAccept': '>>>',
    'InfoText': 'Potion Ingredients',
    'UnknownRecipe': 'Drag ingredients into the spaces below to discover this recipe!',
    'UnknownRecipeName': '????',
    'UnknownIngredient': '????????',
    'IslandName': 'Any Island',
    'IslandName3': 'Padres Del Fuego',
    'IslandName4': 'Tortuga',
    'IslandName5': 'Cuba',
    'LevelLabel': 'Requires Potions Level : ',
    'NewLabel': 'New!',
    'QuestLabel': 'Quest!',
    'SwitchRecipe': 'switch recipe',
    'IngredientList': 'Show Ingredients',
    'ShowTutorial': 'Show Tutorial',
    'RecipeList': 'Potion Recipe List',
    'SurvivalName': 'Survival Mode',
    'SurvivalDesc': 'Combine as many ingredients as you can to increase your Reputation.',
    'IngredientCount': 'Ingredients Made',
    'TileCount': 'Base Ingredients Used',
    'SoulCount': 'Souls Cleared',
    'Efficiency': 'Efficiency Bonus',
    'XPEarned': 'Reputation Earned',
    'MaxedOutTitle': 'Potions Maxed Out',
    'MaxedOutText': 'You already have the maximum number of this potion. Continue anyway?'
}
PotionDescs = {
    InventoryType.CannonDamageLvl1: string.Template('Increases Cannon Damage by $pot% for $dur $unit'), InventoryType.CannonDamageLvl2: string.Template('Increases Cannon Damage by $pot% for $dur $unit'), InventoryType.CannonDamageLvl3: string.Template('Increases Cannon Damage by $pot% for $dur $unit'), InventoryType.PistolDamageLvl1: string.Template('Increases Pistol Damage by $pot% for $dur $unit'), InventoryType.PistolDamageLvl2: string.Template('Increases Pistol Damage by $pot% for $dur $unit'), InventoryType.PistolDamageLvl3: string.Template('Increases Pistol Damage by $pot% for $dur $unit'), InventoryType.CutlassDamageLvl1: string.Template('Increases Cutlass Damage by $pot% for $dur $unit'), InventoryType.CutlassDamageLvl2: string.Template('Increases Cutlass Damage by $pot% for $dur $unit'), InventoryType.CutlassDamageLvl3: string.Template('Increases Cutlass Damage by $pot% for $dur $unit'), InventoryType.DollDamageLvl1: string.Template('Increases Voodoo Damage by $pot% for $dur $unit'), InventoryType.DollDamageLvl2: string.Template('Increases Voodoo Damage by $pot% for $dur $unit'), InventoryType.DollDamageLvl3: string.Template('Increases Voodoo Damage by $pot% for $dur $unit'), InventoryType.HastenLvl1: string.Template('Increases run speed by $pot% for $dur $unit'), InventoryType.HastenLvl2: string.Template('Increases run speed by $pot% for $dur $unit'), InventoryType.HastenLvl3: string.Template('Increases run speed by $pot% for $dur $unit'), InventoryType.RepBonusLvl1: string.Template('Increases reputation gained by $pot% for $dur $unit'), InventoryType.RepBonusLvl2: string.Template('Increases reputation gained by $pot% for $dur $unit'), InventoryType.RepBonusLvl3: string.Template('Increases reputation gained by $pot% for $dur $unit'), InventoryType.RepBonusLvlComp: string.Template('Increases reputation gained by $pot% for $dur $unit'), InventoryType.GoldBonusLvl1: string.Template('Increases gold earned by $pot% for $dur $unit'), InventoryType.GoldBonusLvl2: string.Template('Increases gold earned by $pot% for $dur $unit'), InventoryType.InvisibilityLvl1: string.Template('Grants invisibility for $dur $unit'), InventoryType.InvisibilityLvl2: string.Template('Grants invisibility for $dur $unit'), InventoryType.RegenLvl1: string.Template('Restores $pot% of health every 2 seconds for $dur $unit'), InventoryType.RegenLvl2: string.Template('Restores $pot% of health every 2 seconds for $dur $unit'), InventoryType.RegenLvl3: string.Template('Restores $pot% of health every 2 seconds for $dur $unit'), InventoryType.RegenLvl4: string.Template('Restores $pot% of health every 2 seconds for $dur $unit'), InventoryType.Burp: string.Template('This potion will make you belch!'), InventoryType.Fart: string.Template('This potion will make you fart!'), InventoryType.FartLvl2: string.Template('This potion will make you fart A LOT!'), InventoryType.Vomit: string.Template('This potion will make you puke!'), InventoryType.HeadGrow: string.Template('This potion makes your head huge!'), InventoryType.FaceColor: string.Template('This potion changes your color!'), InventoryType.SizeReduce: string.Template('This potion makes you tiny!'), InventoryType.SizeIncrease: string.Template('This potion make you huge!'), InventoryType.HeadFire: string.Template('This potion lights your head on fire!'), InventoryType.ScorpionTransform: string.Template('This potion transforms you into a scorpion!'), InventoryType.AlligatorTransform: string.Template('This potion transforms you into an alligator!'), InventoryType.CrabTransform: string.Template('This potion transforms you into a crab!'), InventoryType.AccuracyBonusLvl1: string.Template('Increases weapon accuracy by $pot% for $dur $unit'), InventoryType.AccuracyBonusLvl2: string.Template('Increases weapon accuracy by $pot% for $dur $unit'), InventoryType.AccuracyBonusLvl3: string.Template('Increases weapon accuracy by $pot% for $dur $unit'), InventoryType.RemoveGroggy: string.Template('Removes the groggy effect'), InventoryType.StaffEnchant1: string.Template('Assists in staff creation'), InventoryType.StaffEnchant2: string.Template('Assists in staff enhancement')
}
PotionHints = {
    'RecipeList': ['Choose a recipe from the list on the right.'],
    'RecipeStart': ['Click on the board to drop ingredients.\nRight-Click or Space Bar swaps pieces.\nMatch 3 or more!'],
    'MatchMade': ['Groups of three or more will \nmake a new ingredient.'],
    'IngredientMatch': ['You made an ingredient you need.\nMake all the ingredients in the\nrecipe to complete the potion.'],
    'SoulMade': ['You just made a soul!\nMatch three of these to clear them\nand receive an xp bonus!']
}
PotionIngredients = [
    [
        'Scorpion Stinger', 'Scorpion Venom', 'Poison Extract', 'Essence of Scorpion', 'Venom Gem', 'Scorpion Soul'
    ],
    ['Crab Claw', 'Crab Jelly', 'Crab Extract', 'Essence of Crab', 'Crab Gem', 'Crab Soul'],
    ['Alligator Tooth', 'Fang Shard', 'Tooth Dust', 'Essence of Alligator', 'Alligator Gem', 'Alligator Soul'],
    ['Hot Magma', 'Magma Flakes', 'Lava Extract', 'Volcanic Essence', 'Volcano Gem', 'Volcano Soul'],
    ['Gold Coin', 'Crushed Gold', 'Gold Powder', 'Essence of Gold', 'Gold Gem', 'Pirate Soul'],
    ['Dried Bone', 'Bone Shards', 'Cursed Extract', 'Cursed Essence', 'Cursed Gem', 'Cursed Soul']
]
FishingRodNames = {
    0: 'Talk to a Fishmaster to get a Rod',
    1: 'Novice Fishing Rod',
    2: 'Journeyman Fishing Rod',
    3: 'Master Fishing Rod'
}
ScrimmageRoundComplete = 'Round %s Complete'
ScrimmageRoundContinue = 'Would you like to continue onto the next round?'