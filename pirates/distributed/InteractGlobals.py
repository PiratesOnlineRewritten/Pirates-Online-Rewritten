from pirates.pirate import AvatarTypes
from pirates.quest.QuestConstants import NPCIds
from pirates.piratesbase import PLocalizer
import random
CANCEL = 0
TALK = 1
TRADE = 2
DUEL = 3
QUEST = 4
SHIPS = 5
STORE = 6
REPAIR = 7
UPGRADE = 8
HEAL_HP = 9
HEAL_MOJO = 10
TRAIN = 11
SAIL = 12
SAILTM = 13
BRIBE = 14
OVERHAUL = 15
SELL_SHIPS = 16
ACCESSORIES_STORE = 17
TATTOO_STORE = 18
JEWELRY_STORE = 19
BARBER_STORE = 20
RESPEC = 21
RESPEC_CUTLASS = 22
RESPEC_PISTOL = 23
RESPEC_DAGGER = 24
RESPEC_DOLL = 25
RESPEC_GRENADE = 26
RESPEC_STAFF = 27
RESPEC_SAILING = 28
RESPEC_CANNON = 29
BACK = 30
MUSICIAN = 31
PVP_REWARDS_TATTOO = 32
PVP_REWARDS_COATS = 33
PVP_REWARDS_HATS = 34
SELL_ITEMS = 35
STOWAWAY = 36
PLAY_CANNON_DEFENSE = 37
POTION_TUTORIAL = 38
LAUNCH_FISHING_BOAT = 39
LEGENDARY_FISH_STORY = 40
UPGRADE_ROD = 41
CATALOG_STORE = 42
PLAY_SCRIMMAGE = 43
InteractOptionNames = {CANCEL: PLocalizer.InteractCancel,TALK: PLocalizer.InteractTalk,TRADE: PLocalizer.InteractTrade,DUEL: PLocalizer.InteractDuel,QUEST: PLocalizer.InteractQuest,SHIPS: PLocalizer.InteractShips,SELL_SHIPS: PLocalizer.InteractSellShips,STORE: PLocalizer.InteractStore,SELL_ITEMS: PLocalizer.InteractSellItems,REPAIR: PLocalizer.InteractRepair,OVERHAUL: PLocalizer.InteractOverhaul,UPGRADE: PLocalizer.InteractUpgrade,HEAL_HP: PLocalizer.InteractHealHp,HEAL_MOJO: PLocalizer.InteractHealMojo,TRAIN: PLocalizer.InteractTrain,SAIL: PLocalizer.InteractSail,SAILTM: PLocalizer.InteractSailTM,BRIBE: PLocalizer.InteractBribe,ACCESSORIES_STORE: PLocalizer.InteractStore,CATALOG_STORE: PLocalizer.InteractCatalogStore,TATTOO_STORE: PLocalizer.InteractStore,JEWELRY_STORE: PLocalizer.InteractStore,BARBER_STORE: PLocalizer.InteractStore,RESPEC: PLocalizer.InteractRespec,RESPEC_CUTLASS: PLocalizer.InteractRespecCutlass,RESPEC_PISTOL: PLocalizer.InteractRespecPistol,RESPEC_DAGGER: PLocalizer.InteractRespecDagger,RESPEC_DOLL: PLocalizer.InteractRespecDoll,RESPEC_GRENADE: PLocalizer.InteractRespecGrenade,RESPEC_STAFF: PLocalizer.InteractRespecStaff,RESPEC_SAILING: PLocalizer.InteractRespecSailing,RESPEC_CANNON: PLocalizer.InteractRespecCannon,BACK: PLocalizer.InteractBack,MUSICIAN: PLocalizer.InteractMusician,PVP_REWARDS_TATTOO: PLocalizer.InteractPvPTattoo,PVP_REWARDS_COATS: PLocalizer.InteractPvPCoat,PVP_REWARDS_HATS: PLocalizer.InteractPvPHat,STOWAWAY: PLocalizer.InteractStowaway,PLAY_CANNON_DEFENSE: PLocalizer.InteractCannonDefense,POTION_TUTORIAL: PLocalizer.InteractPotionTutorial,LAUNCH_FISHING_BOAT: PLocalizer.InteractLaunchFishingBoat,LEGENDARY_FISH_STORY: PLocalizer.InteractLegendaryFishStory,UPGRADE_ROD: PLocalizer.InteractUpgradeRod,PLAY_SCRIMMAGE: PLocalizer.InteractScrimmage}
InteractOptionHelpText = {CANCEL: PLocalizer.InteractCancelHelp,TALK: PLocalizer.InteractTalkHelp,TRADE: PLocalizer.InteractTradeHelp,DUEL: PLocalizer.InteractDuelHelp,QUEST: PLocalizer.InteractQuestHelp,SHIPS: PLocalizer.InteractShipsHelp,SELL_SHIPS: PLocalizer.InteractSellShipsHelp,STORE: PLocalizer.InteractStoreHelp,SELL_ITEMS: PLocalizer.InteractSellItemsHelp,REPAIR: PLocalizer.InteractRepairHelp,OVERHAUL: PLocalizer.InteractOverhaulHelp,UPGRADE: PLocalizer.InteractUpgradeHelp,HEAL_HP: PLocalizer.InteractHealHpHelp,HEAL_MOJO: PLocalizer.InteractHealMojoHelp,TRAIN: PLocalizer.InteractTrainHelp,SAIL: PLocalizer.InteractSailHelp,SAILTM: PLocalizer.InteractSailTMHelp,BRIBE: PLocalizer.InteractBribeHelp,ACCESSORIES_STORE: PLocalizer.InteractStoreHelp,CATALOG_STORE: PLocalizer.InteractStoreHelp,TATTOO_STORE: PLocalizer.InteractStoreHelp,JEWELRY_STORE: PLocalizer.InteractStoreHelp,BARBER_STORE: PLocalizer.InteractStoreHelp,RESPEC: PLocalizer.InteractRespecHelp,RESPEC_CUTLASS: PLocalizer.InteractRespecHelp,RESPEC_PISTOL: PLocalizer.InteractRespecHelp,RESPEC_DAGGER: PLocalizer.InteractRespecHelp,RESPEC_DOLL: PLocalizer.InteractRespecHelp,RESPEC_GRENADE: PLocalizer.InteractRespecHelp,RESPEC_STAFF: PLocalizer.InteractRespecHelp,RESPEC_SAILING: PLocalizer.InteractRespecHelp,RESPEC_CANNON: PLocalizer.InteractRespecHelp,BACK: PLocalizer.InteractBackHelp,MUSICIAN: PLocalizer.InteractMusicianHelp,PVP_REWARDS_TATTOO: PLocalizer.InteractPvPTattooHelp,PVP_REWARDS_COATS: PLocalizer.InteractPvPCoatHelp,PVP_REWARDS_HATS: PLocalizer.InteractPvPHatHelp,STOWAWAY: PLocalizer.InteractStowawayHelp,PLAY_CANNON_DEFENSE: PLocalizer.InteractCannonDefenseHelp,POTION_TUTORIAL: PLocalizer.InteractPotionTutorialHelp,LAUNCH_FISHING_BOAT: PLocalizer.InteractLaunchFishingBoatHelp,LEGENDARY_FISH_STORY: PLocalizer.InteractLegendaryFishStory,UPGRADE_ROD: PLocalizer.InteractUpgradeRodHelp,PLAY_SCRIMMAGE: PLocalizer.InteractScrimmageHelp}
wantPotionGame = getBase().config.GetBool('want-potion-game', 0)
__NPCInteractMenus = {AvatarTypes.Townfolk: (PLocalizer.TownfolkMenuTitle, [QUEST, BRIBE, HEAL_HP, CANCEL]),AvatarTypes.Cast: (PLocalizer.CastMenuTitle, [QUEST, BRIBE, CANCEL]),AvatarTypes.Commoner: (PLocalizer.CommonerMenuTitle, [QUEST, BRIBE, HEAL_HP, CANCEL]),AvatarTypes.Peasant: (PLocalizer.PeasantMenuTitle, [QUEST, BRIBE, HEAL_HP, CANCEL]),AvatarTypes.Kudgel: (PLocalizer.CommonerMenuTitle, [QUEST, BRIBE, HEAL_HP, CANCEL]),AvatarTypes.StoreOwner: (PLocalizer.StoreOwnerMenuTitle, [QUEST, STORE, SELL_ITEMS, BRIBE, CANCEL]),AvatarTypes.Gypsy: (PLocalizer.GypsyMenuTitle, [QUEST, STORE, BRIBE, SELL_ITEMS, HEAL_MOJO, CANCEL]),AvatarTypes.Fishmaster: (PLocalizer.FishmasterMenuTitle, [STORE, UPGRADE_ROD, LAUNCH_FISHING_BOAT, LEGENDARY_FISH_STORY, CANCEL]),AvatarTypes.Cannonmaster: (PLocalizer.CannonmasterMenuTitle, [PLAY_CANNON_DEFENSE, CANCEL]),AvatarTypes.Blacksmith: (PLocalizer.BlacksmithMenuTitle, [QUEST, STORE, BRIBE, SELL_ITEMS, CANCEL]),AvatarTypes.Shipwright: (PLocalizer.ShipwrightMenuTitle, [QUEST, SHIPS, REPAIR, UPGRADE, SELL_SHIPS, BRIBE, CANCEL]),AvatarTypes.Merchant: (PLocalizer.MerchantMenuTitle, [QUEST, STORE, SELL_ITEMS, BRIBE, CANCEL]),AvatarTypes.Cannoneer: (PLocalizer.CannoneerMenuTitle, [QUEST, STORE, SELL_ITEMS, BRIBE, CANCEL]),AvatarTypes.Bartender: (PLocalizer.BartenderMenuTitle, [QUEST, BRIBE, HEAL_HP, CANCEL]),AvatarTypes.Gunsmith: (PLocalizer.GunsmithMenuTitle, [QUEST, STORE, SELL_ITEMS, BRIBE, CANCEL]),AvatarTypes.Grenadier: (PLocalizer.GrenadierMenuTitle, [QUEST, STORE, SELL_ITEMS, BRIBE, CANCEL]),AvatarTypes.MedicineMan: (PLocalizer.MedicineManMenuTitle, [QUEST, STORE, SELL_ITEMS, BRIBE, CANCEL]),AvatarTypes.Tailor: (PLocalizer.ShopTailor, [QUEST, ACCESSORIES_STORE, CANCEL]),AvatarTypes.Tattoo: (PLocalizer.ShopTattoo, [QUEST, TATTOO_STORE, CANCEL]),AvatarTypes.Jeweler: (PLocalizer.ShopJewelry, [QUEST, JEWELRY_STORE, CANCEL]),AvatarTypes.Barber: (PLocalizer.ShopBarber, [QUEST, BARBER_STORE, CANCEL]),AvatarTypes.Trainer: (PLocalizer.TrainerMenuTitle, [QUEST, RESPEC, BRIBE, CANCEL]),AvatarTypes.Musician: (PLocalizer.ShopMusician, [MUSICIAN, CANCEL]),AvatarTypes.PvPRewards: (PLocalizer.ShopPvP, [QUEST, PVP_REWARDS_TATTOO, PVP_REWARDS_COATS, PVP_REWARDS_HATS, BRIBE, CANCEL]),AvatarTypes.Stowaway: (PLocalizer.ShopStowaway, [STOWAWAY, CANCEL]),AvatarTypes.CatalogRep: (PLocalizer.ShopCatalogRep, [CATALOG_STORE, SELL_ITEMS, CANCEL]),AvatarTypes.ScrimmageMaster: (PLocalizer.ScrimmageMasterMenuTitle, [PLAY_SCRIMMAGE, CANCEL])}
if wantPotionGame:
    __NPCInteractMenus[AvatarTypes.Gypsy] = (
     PLocalizer.GypsyMenuTitle, [QUEST, STORE, POTION_TUTORIAL, BRIBE, SELL_ITEMS, HEAL_MOJO, CANCEL])

def getNPCInteractMenu(avatarType):
    menuChoices = __NPCInteractMenus.get(avatarType)
    return menuChoices


ShipwrightNoSwordWarning = 0
ShipwrightTutorial1 = 1
BlacksmithTutorial1 = 11
BlacksmithTutorial2 = 12
GypsyTutorial1 = 21
FishmasterTutorial1 = 31
__NPCTutorialDict = {ShipwrightNoSwordWarning: 'quest_tut_shipwright_warning_100',ShipwrightTutorial1: 'quest_tut_shipwright_intro_100',BlacksmithTutorial1: 'quest_tut_blacksmith_intro_100',BlacksmithTutorial2: 'quest_tut_blacksmith_intro_101',GypsyTutorial1: 'quest_tut_gypsy_intro_100',FishmasterTutorial1: 'quest_tut_gypsy_intro_100'}

def getNPCTutorial(index):
    tutorial = __NPCTutorialDict.get(index)
    return tutorial


__NPCSalutations = {AvatarTypes.Townfolk: {'greetings': PLocalizer.TownfolkGreetings,'goodbyes': PLocalizer.TownfolkGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.Cast: {},AvatarTypes.Commoner: {},AvatarTypes.Peasant: {},AvatarTypes.Kudgel: {},AvatarTypes.StoreOwner: {'greetings': PLocalizer.FormalGreetings,'goodbyes': PLocalizer.FormalGoodbyes,'durings': PLocalizer.TownfolkEncourage},AvatarTypes.Gypsy: {'greetings': PLocalizer.GypsyGreetings,'goodbyes': PLocalizer.GypsyGoodbyes,'durings': PLocalizer.GypsyEncourage,'brushoffs': PLocalizer.GypsyBrushoff},AvatarTypes.Fishmaster: {'greetings': PLocalizer.FishmasterGreetings,'goodbyes': PLocalizer.FishmasterGoodbyes,'durings': PLocalizer.FishmasterEncourage,'brushoffs': PLocalizer.FishmasterBrushoff},AvatarTypes.Cannonmaster: {'greetings': PLocalizer.CannonmasterGreetings,'goodbyes': PLocalizer.CannonmasterGoodbyes,'durings': PLocalizer.CannonmasterEncourage,'brushoffs': PLocalizer.CannonmasterBrushoff},AvatarTypes.Blacksmith: {'greetings': PLocalizer.FormalGreetings,'goodbyes': PLocalizer.FormalGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.Shipwright: {'greetings': PLocalizer.PirateGreetings,'goodbyes': PLocalizer.PirateGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.Merchant: {'greetings': PLocalizer.FormalGreetings,'goodbyes': PLocalizer.FormalGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.Bartender: {'greetings': PLocalizer.PirateGreetings,'goodbyes': PLocalizer.PirateGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.Gunsmith: {'greetings': PLocalizer.PirateGreetings,'goodbyes': PLocalizer.PirateGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.Grenadier: {'greetings': PLocalizer.FormalGreetings,'goodbyes': PLocalizer.FormalGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.Cannoneer: {'greetings': PLocalizer.PirateGreetings,'goodbyes': PLocalizer.PirateGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.MedicineMan: {'greetings': PLocalizer.GypsyGreetings,'goodbyes': PLocalizer.GypsyGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.Tailor: {'greetings': PLocalizer.FormalGreetings,'goodbyes': PLocalizer.FormalGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.Tattoo: {'greetings': PLocalizer.FormalGreetings,'goodbyes': PLocalizer.FormalGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.Jeweler: {'greetings': PLocalizer.FormalGreetings,'goodbyes': PLocalizer.FormalGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.Barber: {'greetings': PLocalizer.FormalGreetings,'goodbyes': PLocalizer.FormalGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.Trainer: {'greetings': PLocalizer.FormalGreetings,'goodbyes': PLocalizer.FormalGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.Musician: {'greetings': PLocalizer.FormalGreetings,'goodbyes': PLocalizer.FormalGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.PvPRewards: {'greetings': PLocalizer.PirateGreetings,'goodbyes': PLocalizer.PirateGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.Stowaway: {'greetings': PLocalizer.StowawayGreetings,'goodbyes': PLocalizer.StowawayGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.StowawayBrushoff},AvatarTypes.CatalogRep: {'greetings': PLocalizer.FormalGreetings,'goodbyes': PLocalizer.FormalGoodbyes,'durings': PLocalizer.TownfolkEncourage,'brushoffs': PLocalizer.TownfolkBrushoff},AvatarTypes.ScrimmageMaster: {'greetings': PLocalizer.ScrimmageMasterGreetings,'goodbyes': PLocalizer.ScrimmageMasterGoodbyes,'durings': PLocalizer.ScrimmageMasterEncourage,'brushoffs': PLocalizer.ScrimmageMasterBrushoff},NPCIds.PIERRE_LE_PORC: {'brushoffs': PLocalizer.ShipPVPLordBrushoff},NPCIds.GARCIA_DE_AVARCIA: {'brushoffs': PLocalizer.ShipPVPLordBrushoff},NPCIds.SAM_SEABONES: {'goodbyes': PLocalizer.SamSeabonesGoodbye,'brushoffs': PLocalizer.SamSeabonesBrushoff},NPCIds.JOSIE_MCREEDY: {'greetings': PLocalizer.JosieMcReedyGreeting,'groodbyes': PLocalizer.JosieMcReedyGoodbye,'brushoffs': PLocalizer.JosieMcReedyBrushoff},NPCIds.PETER_CHIPPARR: {'greetings': PLocalizer.PeterChipparrGreeting,'groodbyes': PLocalizer.PeterChipparrGoodbye,'brushoffs': PLocalizer.PeterChipparrBrushoff},NPCIds.BARTHOLOMEW_WATKINS: {'greetings': PLocalizer.BWatkinsGreeting,'groodbyes': PLocalizer.BWatkinsGoodbye,'brushoffs': PLocalizer.BWatkinsBrushoff},NPCIds.SHANE_MCGREENY: {'greetings': PLocalizer.ShaneMcGreenyGreeting,'groodbyes': PLocalizer.ShaneMcGreenyGoodbye,'brushoffs': PLocalizer.ShaneMcGreenyBrushoff},NPCIds.TIA_DALMA: {'greetings': PLocalizer.TiaDalmaGreeting,'groodbyes': PLocalizer.TiaDalmaGoodbye,'durings': PLocalizer.TiaDalmaEncourage,'brushoffs': PLocalizer.TiaDalmaBrushoff},NPCIds.ROSETTA_ZIMM: {'brushoffs': PLocalizer.GetConnectedBrushoff},NPCIds.EDWARD_BRITTLE: {'brushoffs': PLocalizer.CrazyNedBrushoff},NPCIds.THOMAS_FISHMEISTER: {'brushoffs': PLocalizer.ThomasFishmeisterBrushoff},NPCIds.MADAM_ZIGANA: {'brushoffs': PLocalizer.MadamZiganaBrushoff},NPCIds.WIDOW_THREADBARREN: {'brushoffs': PLocalizer.ThreadbarrenBrushoff},NPCIds.BEN_CLUBHEART: {'brushoffs': PLocalizer.ClubheartsBrushoff},NPCIds.SANDIE_CLUBHEART: {'brushoffs': PLocalizer.ClubheartsBrushoff},NPCIds.SENOR_FANTIFICO: {'brushoffs': PLocalizer.FantificoBrushoff}}

def getStringsForLocalAvatar(npc, type):
    list = []
    if __NPCSalutations.has_key(npc.getUniqueId()):
        list = __NPCSalutations.get(npc.getUniqueId()).get(type)
    if not list and __NPCSalutations.has_key(npc.avatarType):
        list = __NPCSalutations.get(npc.avatarType).get(type)
    if not list:
        list = __NPCSalutations.get(AvatarTypes.Townfolk).get(type)
    for dict in list:
        if dict.has_key('prereqs'):
            passed = True
            for prereq in dict.get('prereqs'):
                if not prereq.avIsReady(localAvatar):
                    passed = False

            if passed:
                return dict.get('strings')
        else:
            return dict.get('strings')


def getNPCGreeting(npc):
    return random.choice(getStringsForLocalAvatar(npc, 'greetings'))


def getNPCGoodbye(npc):
    return random.choice(getStringsForLocalAvatar(npc, 'goodbyes'))


def getNPCDuring(npc):
    return random.choice(getStringsForLocalAvatar(npc, 'durings'))


def getNPCBrushoff(npc):
    return random.choice(getStringsForLocalAvatar(npc, 'brushoffs'))


DISABLED = 0
NORMAL = 1
HIGHLIGHT = 2