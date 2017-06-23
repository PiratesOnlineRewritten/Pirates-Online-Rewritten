from otp.otpbase import OTPLocalizer as OL
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfxString
from pirates.uberdog.UberDogGlobals import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.inventory import ItemGlobals
from pirates.ai import HolidayGlobals
from pirates.quest.QuestPrereq import *
from pirates.effects.BlackhandCurseSword import BlackhandCurseSword
from pirates.effects.BlackhandCurse import BlackhandCurse
EMOTE_RECEIVE_DOLL = 60405
EMOTE_RECEIVE_STAFF = 60406
EMOTE_RECEIVE_DAGGER = 60407
EMOTE_RECEIVE_GRENADE = 60408
EMOTE_COIN_FLIP = 60505
EMOTE_COIN_HEADS = 60510
EMOTE_COIN_TAILS = 60506
EMOTE_CHANT_A = 60507
EMOTE_CHANT_B = 60508
EMOTE_DANCE_JIG = 60509
EMOTE_FLEX = 60511
EMOTE_LUTE = 60512
EMOTE_FLUTE = 60513
EMOTE_CRAZY = 60514
EMOTE_SEARCHING = 60515
EMOTE_SWEEP = 60518
EMOTE_PRIMP = 60519
EMOTE_AGREE = 60600
EMOTE_AMAZED = 60601
EMOTE_ANGRY = 60602
EMOTE_ARRR = 60603
EMOTE_BARK = 60605
EMOTE_BLINK = 60606
EMOTE_BORED = 60607
EMOTE_BOW = 60610
EMOTE_CACKLE = 60611
EMOTE_CHEER = 60612
EMOTE_CHUCKLE = 60613
EMOTE_CLAP = 60614
EMOTE_CONFUSED = 60615
EMOTE_CONGRATS = 60616
EMOTE_CRY = 60618
EMOTE_CURIOUS = 60619
EMOTE_DRINK = 60620
EMOTE_EAT = 60621
EMOTE_FEAR = 60622
EMOTE_FLEE = 60623
EMOTE_FROWN = 60624
EMOTE_GASP = 60625
EMOTE_GIGGLE = 60626
EMOTE_GLARE = 60627
EMOTE_GOODBYE = 60628
EMOTE_GREET = 60629
EMOTE_GRIN = 60630
EMOTE_GROWL = 60631
EMOTE_HAIL = 60632
EMOTE_HAPPY = 60633
EMOTE_HELLO = 60634
EMOTE_HELP = 60635
EMOTE_HISS = 60636
EMOTE_HUNGRY = 60637
EMOTE_IMPATIENT = 60638
EMOTE_JK = 60639
EMOTE_LAUGH = 60640
EMOTE_LOL = 60641
EMOTE_MEOW = 60642
EMOTE_MOO = 60643
EMOTE_NOD = 60645
EMOTE_POWERFUL = 60647
EMOTE_READY = 60649
EMOTE_ROAR = 60650
EMOTE_ROFL = 60651
EMOTE_SAD = 60652
EMOTE_SALUTE = 60653
EMOTE_SCARED = 60654
EMOTE_SHRUG = 60655
EMOTE_SIGH = 60656
EMOTE_SMILE = 60657
EMOTE_SORRY = 60658
EMOTE_TAP = 60659
EMOTE_THIRSTY = 60660
EMOTE_TIRED = 60661
EMOTE_VITTLES = 60662
EMOTE_WAIT = 60663
EMOTE_WAVE = 60664
EMOTE_WINK = 60665
EMOTE_YAWN = 60666
EMOTE_CELEBRATE = 60668
EMOTE_SLEEP = 60669
EMOTE_DANCE = 60670
EMOTE_VALENTINES_A = 60671
EMOTE_VALENTINES_B = 60672
EMOTE_VALENTINES_C = 60673
EMOTE_VALENTINES_D = 60674
EMOTE_VALENTINES_E = 60675
EMOTE_VALENTINES = 60676
EMOTE_HALLOWEEN = 60677
EMOTE_NOISEMAKER = 60678
EMOTE_DUHHH = 60700
EMOTE_BLOWKISS = 60701
EMOTE_FLIRT = 60702
EMOTE_SASSY = 60703
EMOTE_TALKTOHAND = 60704
EMOTE_INSANE = 60800
EMOTE_CUTTHROAT = 60801
EMOTE_EMBARRASSED = 60802
EMOTE_FACESMACK = 60803
EMOTE_HANDITOVER = 60804
EMOTE_HEADSCRATCH = 60805
EMOTE_NERVOUS = 60806
EMOTE_PETRIFIED = 60807
EMOTE_SHOWMEMONEY = 60808
EMOTE_SHRUG = 60809
EMOTE_SINCERETHANKS = 60810
EMOTE_SNARL = 60811
EMOTE_GUN_DRAW = 60900
EMOTE_GUN_AIM = 60901
EMOTE_GUN_PUTAWAY = 60902
EMOTE_FART = 60903
EMOTE_DRINKPOTION = 60904
EMOTE_NED_CRAZY = 60905
EMOTE_BLACKHAND_SWORD_A = 60906
EMOTE_BLACKHAND_SWORD_B = 60907
EMOTE_BLACKHAND_SWORD_C = 60908
EMOTE_BLACKHAND = 60909
EMOTE_YES = 65000
EMOTE_NO = 65001
emotes = {EMOTE_RECEIVE_DOLL: {'anim': 'doll_receive','prop': 'models/handheld/voodoo_doll_high'},EMOTE_RECEIVE_STAFF: {'anim': 'staff_receive','prop': 'models/handheld/voodoo_staff_high'},EMOTE_RECEIVE_DAGGER: {'anim': 'dagger_receive','prop': 'models/handheld/dagger_high'},EMOTE_RECEIVE_GRENADE: {'anim': 'bomb_receive','prop': 'models/ammunition/grenade'},EMOTE_DANCE_JIG: {'anim': 'emote_dance_jig_loop','loop': 1,'group': OL.Emotes_General},EMOTE_FLEX: {'anim': 'emote_flex','group': OL.Emotes_General},EMOTE_PRIMP: {'anim': 'primp_idle','loop': 1,'group': OL.Emotes_General,'gender': 'f'},EMOTE_ANGRY: {'anim': 'emote_anger','group': OL.Emotes_Expressions},EMOTE_CELEBRATE: {'anim': 'emote_celebrate','group': OL.Emotes_General},EMOTE_CLAP: {'anim': 'emote_clap','group': OL.Emotes_General,'sfx': loadSfxString(SoundGlobals.SFX_AVATAR_CLAP)},EMOTE_FEAR: {'anim': 'emote_fear','group': OL.Emotes_Expressions},EMOTE_LAUGH: {'anim': 'emote_laugh','group': OL.Emotes_Expressions},EMOTE_NO: {'anim': 'emote_no','group': OL.Emotes_General},EMOTE_SAD: {'anim': 'emote_sad','group': OL.Emotes_Expressions},EMOTE_SMILE: {'anim': 'emote_smile','group': OL.Emotes_Expressions},EMOTE_WAVE: {'anim': 'emote_wave','group': OL.Emotes_General},EMOTE_WINK: {'anim': 'emote_wink','group': OL.Emotes_General},EMOTE_YAWN: {'anim': 'emote_yawn','group': OL.Emotes_Expressions},EMOTE_YES: {'anim': 'emote_yes','group': OL.Emotes_General},EMOTE_SLEEP: {'anim': 'sleep_idle','loop': 1,'group': OL.Emotes_General},EMOTE_VALENTINES: {'prereqs': [IsHoliday(HolidayGlobals.VALENTINESDAY)],'anim': 'emote_wink','group': OL.Emotes_General},EMOTE_NOISEMAKER: {'prereqs': [IsHoliday(HolidayGlobals.WINTERFESTIVAL)],'anim': 'emote_newyears','prop': 'models/handheld/pir_m_hnd_hol_noisemaker08','group': OL.Emotes_General,'sfx': loadSfxString(SoundGlobals.SFX_AVATAR_NOISEMAKER)},EMOTE_HALLOWEEN: {'prereqs': [IsHoliday(HolidayGlobals.ZOMBIEEMOTE)],'anim': 'emote_thriller','group': OL.Emotes_General},EMOTE_CHEER: {'anim': 'emote_celebrate'},EMOTE_TIRED: {'anim': 'sleep_idle_loop','loop': 1},EMOTE_NOD: {'anim': 'emote_yes'},EMOTE_GREET: {'anim': 'emote_wave'},EMOTE_LOL: {'anim': 'emote_laugh'},EMOTE_SCARED: {'anim': 'emote_fear'},EMOTE_GRIN: {'anim': 'emote_smile'},EMOTE_HAPPY: {'anim': 'emote_smile'},EMOTE_DANCE: {'anim': 'emote_dance_jig','loop': 1},EMOTE_BORED: {'anim': 'idle_B_shiftWeight','loop': 1},EMOTE_CACKLE: {'anim': 'emote_laugh'},EMOTE_HAIL: {'anim': 'emote_wave'},EMOTE_SORRY: {'anim': 'sleep_idle','loop': 1},EMOTE_HISS: {'anim': 'emote_anger'},EMOTE_IMPATIENT: {'anim': 'idle_B_shiftWeight','loop': 1},EMOTE_CONFUSED: {'anim': 'idle_head_scratch'},EMOTE_WAIT: {'anim': 'emote_no'},EMOTE_GLARE: {'anim': 'idle_handhip','loop': 1},EMOTE_COIN_HEADS: {'anim': None},EMOTE_COIN_TAILS: {'anim': None},EMOTE_DUHHH: {'anim': 'emote_duhhh'},EMOTE_BLOWKISS: {'anim': 'emote_blow_kiss'},EMOTE_FLIRT: {'anim': 'emote_flirt'},EMOTE_SASSY: {'anim': 'emote_sassy'},EMOTE_TALKTOHAND: {'anim': 'emote_talk_to_the_hand'},EMOTE_INSANE: {'anim': 'emote_crazy'},EMOTE_CUTTHROAT: {'anim': 'emote_cut_throat'},EMOTE_EMBARRASSED: {'anim': 'emote_embarrassed'},EMOTE_FACESMACK: {'anim': 'emote_face_smack'},EMOTE_HANDITOVER: {'anim': 'emote_hand_it_over'},EMOTE_HEADSCRATCH: {'anim': 'emote_head_scratch'},EMOTE_NERVOUS: {'anim': 'emote_nervous'},EMOTE_PETRIFIED: {'anim': 'emote_scared'},EMOTE_SHOWMEMONEY: {'anim': 'emote_show_me_the_money'},EMOTE_SHRUG: {'anim': 'emote_shrug'},EMOTE_SINCERETHANKS: {'anim': 'emote_sincere_thanks'},EMOTE_SNARL: {'anim': 'emote_snarl'},EMOTE_GUN_DRAW: {'anim': 'gun_draw','prop': 'models/handheld/pir_m_hnd_gun_pistol_a'},EMOTE_GUN_AIM: {'anim': 'gun_aim_idle','loop': 1,'prop': 'models/handheld/pir_m_hnd_gun_pistol_a'},EMOTE_GUN_PUTAWAY: {'anim': 'gun_putaway','prop': 'models/handheld/pir_m_hnd_gun_pistol_a'},EMOTE_FART: {'anim': 'fart','sfx': loadSfxString(SoundGlobals.SFX_MINIGAME_POTION_FX_FART_1)},EMOTE_DRINKPOTION: {'anim': 'drink_potion','prop': 'models/handheld/bottle_high','sfx': loadSfxString(SoundGlobals.SFX_CONSUMABLE_DRINK)},EMOTE_NED_CRAZY: {'anim': 'crazy_ned_day_interact'},EMOTE_BLACKHAND_SWORD_A: {'anim': 'hand_curse_get_sword','prop': 'models/handheld/pir_m_hnd_swd_davyJones_g','waitProp': 0.5,'durProp': 17.0,'vfx': BlackhandCurseSword},EMOTE_BLACKHAND_SWORD_B: {'anim': 'hand_curse_get_sword','prop': 'models/handheld/pir_m_hnd_swd_davyJones_a','waitProp': 0.5,'durProp': 17.0,'vfx': BlackhandCurseSword},EMOTE_BLACKHAND_SWORD_C: {'anim': 'hand_curse_get_sword','prop': 'models/handheld/pir_m_hnd_swd_davyJones_e','waitProp': 0.5,'durProp': 17.0,'vfx': BlackhandCurseSword},EMOTE_BLACKHAND: {'prereqs': [DidQuest('rc.le.10lootTreasure')],'anim': 'hand_curse_check','group': OL.Emotes_General}}

def getEmotePrereqs(emoteId):
    if emotes.has_key(emoteId):
        return emotes[emoteId].get('prereqs', [])
    return []


def getEmoteAnim(emoteId):
    if emotes.has_key(emoteId):
        return emotes[emoteId].get('anim')
    return None


def getEmoteLoop(emoteId):
    if emotes.has_key(emoteId):
        return emotes[emoteId].get('loop', 0)
    return 0


def getEmoteProp(emoteId):
    if emotes.has_key(emoteId):
        return emotes[emoteId].get('prop', None)
    return None


def getEmoteGroup(emoteId):
    if emotes.has_key(emoteId):
        return emotes[emoteId].get('group', None)
    return None


def getEmoteGender(emoteId):
    if emotes.has_key(emoteId):
        return emotes[emoteId].get('gender', None)
    return None


def getEmoteSfx(emoteId):
    if emotes.has_key(emoteId):
        return emotes[emoteId].get('sfx', None)
    return None


def getWaitProp(emoteId):
    if emotes.has_key(emoteId):
        return emotes[emoteId].get('waitProp', 0)
    return 0


def getDurProp(emoteId):
    if emotes.has_key(emoteId):
        return emotes[emoteId].get('durProp', 0)
    return 0


def getEmoteVfx(emoteId):
    if emotes.has_key(emoteId) and emotes[emoteId].has_key('vfx'):
        effect = emotes[emoteId].get('vfx').getEffect(1)
        return effect
    return None


def getAllEmoteAnimations():
    animList = []
    for emoteId in emotes.keys():
        if getEmoteAnim(emoteId) not in animList:
            emoteAnim = getEmoteAnim(emoteId)
            if emoteAnim:
                animList.append(emoteAnim)

    return animList


RewardReceivedToEmoteCmds = {InventoryType.DollToken: (EMOTE_RECEIVE_DOLL, PiratesGuiGlobals.REWARD_PANEL_DOLL),InventoryType.WandToken: (EMOTE_RECEIVE_STAFF, PiratesGuiGlobals.REWARD_PANEL_STAFF),InventoryType.DaggerToken: (EMOTE_RECEIVE_DAGGER, PiratesGuiGlobals.REWARD_PANEL_DAGGER),InventoryType.GrenadeToken: (EMOTE_RECEIVE_GRENADE, PiratesGuiGlobals.REWARD_PANEL_GRENADE),InventoryType.SailPowerRecharge: (EMOTE_CELEBRATE, PiratesGuiGlobals.REWARD_PANEL_BLACK_PEARL),ItemGlobals.BITTER_END: (EMOTE_BLACKHAND_SWORD_A, PiratesGuiGlobals.REWARD_PANEL_RAVENS_COVE_A),ItemGlobals.SPINECREST_SWORD: (EMOTE_BLACKHAND_SWORD_B, PiratesGuiGlobals.REWARD_PANEL_RAVENS_COVE_B),ItemGlobals.NAUTILUS_BLADE: (EMOTE_BLACKHAND_SWORD_C, PiratesGuiGlobals.REWARD_PANEL_RAVENS_COVE_C)}