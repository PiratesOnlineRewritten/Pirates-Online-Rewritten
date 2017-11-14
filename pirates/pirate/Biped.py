from pandac.PandaModules import *
from direct.task import Task
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.gui.OnscreenText import OnscreenText
from otp.avatar.Avatar import Avatar
import AvatarTypes
from pirates.battle import WeaponGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.pirate.BipedAnimationMixer import BipedAnimationMixer
from pirates.effects.UsesEffectNode import UsesEffectNode
from pirates.movement.UsesAnimationMixer import UsesAnimationMixer
from pirates.audio import SoundGlobals
from otp.otpbase import OTPRender
import random
NA_INDEX = -1
STAND_INDEX = 0
WALK_INDEX = 1
ATTACK_INDEX = 2
OUCH_INDEX = 3
ACTION_INDEX = 4
msfCustomAnimList = [
 'idle', 'bayonet_drill', 'bayonet_run', 'bayonet_attack_idle', 'bayonet_attackA', 'bayonet_attackB', 'bayonet_attackC', 'bigbomb_draw', 'bigbomb_idle', 'bigbomb_throw', 'bigbomb_walk', 'cards_blackjack_hit', 'cards_blackjack_stay', 'emote_anger', 'emote_clap', 'emote_fear', 'emote_newyears', 'emote_sad', 'emote_wave', 'emote_yes', 'bomb_draw', 'bomb_idle', 'bomb_throw', 'cards_check', 'cards_hide', 'cards_hide_hit', 'cards_hide_idle', 'cards_pick_up', 'cards_pick_up_idle', 'cards_set_down', 'cards_set_down_win', 'cards_set_down_lose', 'cards_cheat', 'cards_good_tell', 'cards_bad_tell', 'dagger_combo', 'deal', 'deal_idle', 'idle_arm_scrach', 'idle_head_scratch_side', 'idle_head_scratch', 'idle_butt_scratchinto_deal', 'jail_dropinto', 'repairfloor_into', 'repairfloor_outof', 'rifle_fight_forward_diagonal_left', 'rifle_fight_forward_diagonal_right', 'rifle_fight_run_strafe_left', 'rifle_fight_run_strafe_right', 'rifle_fight_shoot_high', 'rifle_fight_walk', 'rifle_fight_walk_strafe_left', 'rifle_fight_walk_strafe_right', 'run', 'run_with_weapon', 'sit', 'sleep_idle', 'sweep', 'staff_receive', 'voodoo_doll_poke']
mmsCustomAnimList = [
 'idle']
mmiCustomAnimList = [
 'bayonet_drill', 'bayonet_attackA', 'bayonet_attack_idle', 'bayonet_run', 'bayonet_attack_idle', 'bayonet_attackB', 'bayonet_attackC', 'emote_clap', 'idle', 'idle_arm_scratch', 'rifle_fight_forward_diagonal_left', 'rifle_fight_forward_diagonal_right', 'rifle_fight_run_strafe_left', 'rifle_fight_run_strafe_right', 'rifle_fight_shoot_high', 'rifle_fight_shoot_hip', 'rifle_fight_walk_strafe_left', 'rifle_fight_walk_strafe_right', 'run', 'sweep']
mtpCustomAnimList = [
 'idle_butt_scratch', 'bayonet_drill', 'bigbomb_draw', 'bigbomb_idle', 'bigbomb_throw', 'bigbomb_walk', 'bomb_draw', 'bomb_idle', 'bomb_throw', 'cards_check', 'cards_hidecards_hide_idle', 'cards_pick_up', 'cards_pick_up_idle', 'cards_set_down', 'cards_set_down_win', 'cards_set_down_lose', 'cards_cheat', 'cards_good_tell', 'cards_bad_tell', 'dagger_combo', 'deal', 'deal_idle', 'idle', 'into_deal', 'rifle_fight_forward_diagonal_left', 'rifle_fight_forward_diagonal_right', 'rifle_fight_run_strafe_left', 'rifle_fight_run_strafe_right', 'rifle_fight_shoot_high', 'rifle_fight_shoot_hip', 'rifle_fight_walk_strafe_right', 'run', 'sit', 'voodoo_doll_poke']
mtmCustomAnimList = [
 'bayonet_drill', 'bayonet_attackA', 'bayonet_attack_idle', 'bayonet_run', 'bayonet_attack_idle', 'bayonet_attackB', 'bayonet_attackC', 'emote_clap', 'emote_fear', 'death4', 'idle_butt_scratch', 'idle_arm_scratch', 'sow_idle', 'sow_into_look', 'sow_outof_look', 'rifle_fight_forward_diagonal_left', 'rifle_fight_forward_diagonal_right', 'rifle_fight_run_strafe_left', 'rifle_fight_run_strafe_right', 'rifle_fight_shoot_high', 'rifle_fight_shoot_hip', 'rifle_fight_walk', 'rifle_fight_walk_strafe_left', 'rifle_fight_walk_strafe_right', 'run', 'sweep', 'idle']
fsfCustomAnimList = [
 'bayonet_attack_idle', 'bayonet_run', 'bayonet_attackB', 'bayonet_attackC', 'bigbomb_draw', 'bigbomb_idle', 'bigbomb_throw', 'bomb_draw', 'bomb_idle', 'bomb_throw', 'cards_bad_tell', 'cards_cheat', 'cards_good_tell', 'cards_hide', 'cards_hide_idle', 'cards_pick_up', 'cards_pick_up_idle', 'cards_set_down', 'cards_set_down_lose', 'cards_set_down_win', 'emote_anger', 'emote_clap', 'emote_fear', 'emote_newyears', 'emote_wave', 'cutlass_bladestorm', 'cutlass_combo', 'cutlass_headbutt', 'cutlass_kick', 'cutlass_multihit', 'cutlass_sweep', 'cutlass_taunt', 'dagger_asp', 'deal', 'deal_idle', 'drink_potion', 'emote_no', 'emote_sad', 'emote_yes', 'into_deal', 'kneel', 'kneel_dizzy', 'kneel_fromidle', 'emote_laugh', 'repair_bench', 'repairfloor_idle', 'repairfloor_into', 'repairfloor_outof', 'run', 'run_with_weapon', 'sit', 'sleep_idle', 'sleep_into_look', 'sleep_outof_look', 'emote_smile', 'sweep', 'sword_draw', 'sword_hit', 'sword_idle', 'tentacle_idle', 'tentacle_squeeze', 'voodoo_draw', 'voodoo_idle', 'voodoo_doll_poke', 'yawn']
fmsCustomAnimList = []
fmiCustomAnimList = []
ftpCustomAnimList = ['run']
ftmCustomAnimList = []
jsCustomAnimList = (('idle', 'js_idle'), ('emote_bow', 'js_emote_bow'), ('emote_hands_on_hips', 'js_emote_hands_on_hips'), ('emote_scared', 'js_emote_scared'), ('run', 'js_run'), ('run_diagonal_left', 'js_run_diagonal_left'), ('run_diagonal_right', 'js_run_diagonal_right'), ('run_with_weapon', 'js_run_with_weapon'), ('strafe_left', 'js_strafe_left'), ('strafe_right', 'js_strafe_right'), ('turn_left', 'js_turn_left'), ('turn_right', 'js_turn_right'), ('walk', 'js_walk'), ('walk_back_diagonal_left', 'js_walk_back_diagonal_left'), ('walk_back_diagonal_right', 'js_walk_back_diagonal_right'), ('sit_idle', 'js_playing_cards_idle'), ('into_sit_speak_idle', 'js_playing_cards_into_look'), ('sit_speak_idle', 'js_playing_cards_look_idle'), ('outof_sit_speak_idle', 'js_playing_cards_outof_look'), ('hands_on_hips', 'js_handsOnHips'), ('idle_to_bow', 'js_idleToBow'), ('special_bow', 'js_tv_bow'), ('walk_camera', 'js_walk_camera'), ('marketing_fight_jr', 'js_marketing_fight_jr'))
wtCustomAnimList = (('idle', 'wt_spar_idle'), ('outof_speak_idle', 'wt_spar_outof_look'), ('into_speak_idle', 'wt_spar_into_look'), ('speak_idle', 'wt_spar_look_idle'))
esCustomAnimList = (('sit_idle', 'es_sit_idle'), ('into_sit_speak_idle', 'es_sit_into_look'), ('sit_speak_idle', 'es_sit_look_idle'), ('outof_sit_speak_idle', 'es_sit_outof_look'))
tdCustomAnimList = (('sit_idle', 'td_pet_idle'), ('into_sit_speak_idle', 'td_pet_into_look'), ('sit_speak_idle', 'td_pet_look_idle'), ('outof_sit_speak_idle', 'td_pet_outof_look'), ('show_voodoo_doll', 'td_show_voodoo_doll'))
cbCustomAnimList = (('idle', 'cb_eat_apple_idle'), ('into_speak_idle', 'cb_eat_apple_into_look'), ('speak_idle', 'cb_eat_apple_look_idle'), ('outof_speak_idle', 'cb_eat_apple_outof_look'))
jgCustomAnimList = (('sit_idle', 'jg_playing_cards_idle'), ('into_sit_speak_idle', 'jg_playing_cards_into_look'), ('sit_speak_idle', 'jg_playing_cards_look_idle'), ('outof_sit_speak_idle', 'jg_playing_cards_outof_look'))
jrCustomAnimList = (('idle', 'jr_look_idle'), ('jr_look_idle', 'jr_look_idle'), ('jr_look_idle_2', 'jr_look_idle_2'), ('marketing_fight_js', 'jr_marketing_fight_js'), ('haunted_holiday', 'jr_haunted_holiday'))
plfCustomAnimList = (('drunk_idle', 'plf_drunk_idle'), ('drunk_into_look', 'plf_drunk_into_look'), ('drunk_look_idle', 'plf_drunk_look_idle'), ('drunk_outof_look', 'plf_drunk_outof_look'))
plsCustomAnimList = (('drunk_idle', 'pls_drunk_idle'), ('drunk_into_look', 'pls_drunk_into_look'), ('drunk_look_idle', 'pls_drunk_look_idle'), ('drunk_outof_look', 'pls_drunk_outof_look'))
djCustomAnimList = (('idle', 'dj_idle'))
stopLookaroundAnimList = ['walk', 'run']
DefaultAnimList = (
 ('idle', 'idle'), ('idle_centered', 'idle_centered'), ('idle_handhip', 'idle_handhip'), ('idle_flex', 'idle_flex'), ('idle_hit', 'idle_hit'), ('idle_handhip_from_idle', 'idle_handhip_from_idle'), ('idle_B_shiftWeight', 'idle_B_shiftWeight'), ('idle_sit', 'idle_sit'), ('idle_arm_scratch', 'idle_arm_scratch'), ('idle_butt_scratch', 'idle_butt_scratch'), ('idle_head_scratch', 'idle_head_scratch'), ('idle_head_scratch_side', 'idle_head_scratch_side'), ('idle_sit_alt', 'idle_sit_alt'), ('walk', 'walk'), ('run', 'run'), ('walk_back_diagonal_left', 'walk_back_diagonal_left'), ('walk_back_diagonal_right', 'walk_back_diagonal_right'), ('strafe_left', 'strafe_left'), ('strafe_right', 'strafe_right'), ('run_diagonal_left', 'run_diagonal_left'), ('run_diagonal_right', 'run_diagonal_right'), ('run_with_weapon', 'run_with_weapon'), ('cower_in_place', 'cower_idle'), ('cower_idle', 'cower_idle'), ('cower_into', 'cower_into'), ('cower_outof', 'cower_outof'), ('sit_cower_idle', 'sit_cower_idle'), ('sit_cower_into_sleep', 'sit_cower_into_sleep'), ('sit_sleep_into_cower', 'sit_sleep_into_cower'), ('jump', 'jump'), ('jump_idle', 'jump_idle'), ('fall_ground', 'fall_ground'), ('coin_flip_idle', 'coin_flip_idle'), ('coin_flip_old_idle', 'coin_flip_old_idle'), ('coin_flip_look_idle', 'coin_flip_look_idle'), ('chant_a_idle', 'chant_a_idle'), ('chant_b_idle', 'chant_b_idle'), ('summon_idle', 'summon_idle'), ('map_head_look_left_idle', 'map_head_look_left_idle'), ('map_head_into_look_left', 'map_head_into_look_left'), ('map_head_outof_look_left', 'map_head_outof_look_left'), ('map_look_arm_left', 'map_look_arm_left'), ('map_look_arm_right', 'map_look_arm_right'), ('map_look_pant_right', 'map_look_pant_right'), ('map_look_boot_left', 'map_look_boot_left'), ('map_look_boot_right', 'map_look_boot_right'), ('kneel', 'kneel'), ('kraken_struggle_idle', 'kraken_struggle_idle'), ('kraken_fight_idle', 'kraken_fight_idle'), ('wheel', 'wheel'), ('semi_conscious_loop', 'semi_conscious_loop'), ('semi_conscious_standup', 'semi_conscious_standup'), ('drink_potion', 'drink_potion'), ('emote_anger', 'emote_anger'), ('emote_blow_kiss', 'emote_blow_kiss'), ('emote_celebrate', 'emote_celebrate'), ('emote_clap', 'emote_clap'), ('emote_coin_flip', 'emote_coin_flip'), ('emote_coin_flip_loop', 'emote_coin_flip'), ('emote_crazy', 'emote_crazy'), ('emote_cut_throat', 'emote_cut_throat'), ('emote_dance_jig', 'emote_dance_jig'), ('emote_dance_jig_loop', 'emote_dance_jig'), ('emote_duhhh', 'emote_duhhh'), ('emote_embarrassed', 'emote_embarrassed'), ('emote_face_smack', 'emote_face_smack'), ('emote_fear', 'emote_fear'), ('emote_flex', 'emote_flex'), ('emote_flirt', 'emote_flirt'), ('emote_hand_it_over', 'emote_hand_it_over'), ('emote_head_scratch', 'emote_head_scratch'), ('emote_laugh', 'emote_laugh'), ('emote_navy_scared', 'emote_navy_scared'), ('emote_navy_wants_fight', 'emote_navy_wants_fight'), ('emote_nervous', 'emote_nervous'), ('emote_newyears', 'emote_newyears'), ('emote_no', 'emote_no'), ('emote_sad', 'emote_sad'), ('emote_sassy', 'emote_sassy'), ('emote_scared', 'emote_scared'), ('emote_show_me_the_money', 'emote_show_me_the_money'), ('emote_shrug', 'emote_shrug'), ('emote_sincere_thanks', 'emote_sincere_thanks'), ('emote_smile', 'emote_smile'), ('emote_snarl', 'emote_snarl'), ('emote_talk_to_the_hand', 'emote_talk_to_the_hand'), ('emote_thriller', 'emote_thriller'), ('emote_wave', 'emote_wave'), ('emote_wink', 'emote_wink'), ('emote_yawn', 'emote_yawn'), ('emote_yes', 'emote_yes'), ('injured_healing_into', 'injured_healing_into'), ('injured_healing_loop', 'injured_healing_loop'), ('injured_healing_outof', 'injured_healing_outof'), ('injured_idle', 'injured_idle'), ('injured_fall', 'injured_fall'), ('injured_idle_shakehead', 'injured_idle_shakehead'), ('injured_standup', 'injured_standup'), ('sweep', 'sweep'), ('sweep_idle', 'sweep_idle'), ('sweep_look_idle', 'sweep_look_idle'), ('sweep_into_look', 'sweep_into_look'), ('sweep_outof_look', 'sweep_outof_look'), ('stowaway_get_in_crate', 'stowaway_get_in_crate'), ('axe_chop_idle', 'axe_chop_idle'), ('axe_chop_look_idle', 'axe_chop_look_idle'), ('bar_wipe', 'bar_wipe'), ('bar_wipe_into_look', 'bar_wipe_into_look'), ('bar_wipe_look_idle', 'bar_wipe_look_idle'), ('bar_wipe_outof_look', 'bar_wipe_outof_look'), ('bar_talk01_idle', 'bar_talk01_idle'), ('bar_talk01_into_look', 'bar_talk01_into_look'), ('bar_talk01_look_idle', 'bar_talk01_look_idle'), ('bar_talk01_outof_look', 'bar_talk01_outof_look'), ('bar_talk02_idle', 'bar_talk02_idle'), ('bar_talk02_into_look', 'bar_talk02_into_look'), ('bar_talk02_look_idle', 'bar_talk02_look_idle'), ('bar_talk02_outof_look', 'bar_talk02_outof_look'), ('bar_talk03_idle', 'bar_talk03_idle'), ('bar_write_idle', 'bar_write_idle'), ('bar_write_into_look', 'bar_write_into_look'), ('bar_write_look_idle', 'bar_write_look_idle'), ('bar_write_outof_look', 'bar_write_outof_look'), ('barrel_hide_idle', 'barrel_hide_idle'), ('barrel_hide_into_look', 'barrel_hide_into_look'), ('barrel_hide_look_idle', 'barrel_hide_look_idle'), ('barrel_hide_outof_look', 'barrel_hide_outof_look'), ('lute_idle', 'lute_idle'), ('lute_into_look', 'lute_into_look'), ('lute_look_idle', 'lute_look_idle'), ('lute_outof_look', 'lute_outof_look'), ('loom_idle', 'loom_idle'), ('loom_into_look', 'loom_into_look'), ('loom_look_idle', 'loom_look_idle'), ('loom_outof_look', 'loom_outof_look'), ('primp_idle', 'primp_idle'), ('primp_into_look', 'primp_into_look'), ('primp_look_idle', 'primp_look_idle'), ('primp_outof_look', 'primp_outof_look'), ('sit_hanginglegs_outof_look', 'sit_hanginglegs_outof_look'), ('sit_hanginglegs_look_idle', 'sit_hanginglegs_look_idle'), ('sit_hanginglegs_into_look', 'sit_hanginglegs_into_look'), ('sit_hanginglegs_idle', 'sit_hanginglegs_idle'), ('sit_sleep_outof_look', 'sit_sleep_outof_look'), ('sit_sleep_look_idle', 'sit_sleep_look_idle'), ('sit_sleep_into_look', 'sit_sleep_into_look'), ('sit_sleep_idle', 'sit_sleep_idle'), ('sleep_outof_look', 'sleep_outof_look'), ('sleep_into_look', 'sleep_into_look'), ('sleep_idle_loop', 'sleep_idle'), ('sleep_idle', 'sleep_idle'), ('sleep_sick_idle', 'sleep_sick_idle'), ('sleep_sick_into_look', 'sleep_sick_into_look'), ('sleep_sick_look_idle', 'sleep_sick_look_idle'), ('sleep_sick_outof_look', 'sleep_sick_outof_look'), ('stir_idle', 'stir_idle'), ('stir_into_look', 'stir_into_look'), ('stir_outof_look', 'stir_outof_look'), ('stir_look_idle', 'stir_look_idle'), ('sow_idle', 'sow_idle'), ('sow_into_look', 'sow_into_look'), ('sow_look_idle', 'sow_look_idle'), ('sow_outof_look', 'sow_outof_look'), ('tatoo_idle', 'tatoo_idle'), ('tatoo_into_look', 'tatoo_into_look'), ('tatoo_look_idle', 'tatoo_look_idle'), ('tatoo_outof_look', 'tatoo_outof_look'), ('tatoo_receive_idle', 'tatoo_receive_idle'), ('tatoo_receive_into_look', 'tatoo_receive_into_look'), ('tatoo_receive_look_idle', 'tatoo_receive_look_idle'), ('tatoo_receive_outof_look', 'tatoo_receive_outof_look'), ('doctor_work_idle', 'doctor_work_idle'), ('doctor_work_into_look', 'doctor_work_into_look'), ('doctor_work_look_idle', 'doctor_work_look_idle'), ('doctor_work_outof_look', 'doctor_work_outof_look'), ('patient_work_idle', 'patient_work_idle'), ('crazy_idle', 'crazy_idle'), ('crazy_look_idle', 'crazy_look_idle'), ('flute_idle', 'flute_idle'), ('flute_look_idle', 'flute_look_idle'), ('handdig_idle', 'handdig_idle'), ('searching_idle', 'searching_idle'), ('moaning_idle', 'moaning_idle'), ('haunted_holiday', 'haunted_holiday'), ('bindPose', 'bindPose'), ('swim', 'swim'), ('swim_left', 'swim_left'), ('swim_right', 'swim_right'), ('swim_left_diagonal', 'swim_left_diagonal'), ('swim_right_diagonal', 'swim_right_diagonal'), ('swim_back', 'swim_back'), ('swim_back_diagonal_left', 'swim_back_diagonal_left'), ('swim_back_diagonal_right', 'swim_back_diagonal_right'), ('tread_water', 'tread_water'), ('tread_water_into_teleport', 'tread_water_into_teleport'), ('swim_into_tread_water', 'swim_into_tread_water'), ('repair_bench', 'repair_bench'), ('repairfloor_idle', 'repairfloor_idle'), ('repairfloor_into', 'repairfloor_into'), ('repairfloor_outof', 'repairfloor_outof'), ('search_med', 'search_med'), ('search_low', 'search_low'), ('bomb_throw', 'bomb_throw'), ('bomb_draw', 'bomb_draw'), ('bomb_hurt', 'bomb_hurt'), ('bomb_idle', 'bomb_idle'), ('bomb_charge', 'bomb_charge'), ('bomb_charge_loop', 'bomb_charge_loop'), ('bomb_charge_throw', 'bomb_charge_throw'), ('bigbomb_throw', 'bigbomb_throw'), ('bigbomb_idle', 'bigbomb_idle'), ('bigbomb_draw', 'bigbomb_draw'), ('bigbomb_walk', 'bigbomb_walk'), ('bigbomb_walk_back', 'bigbomb_walk_back'), ('bigbomb_walk_back_left', 'bigbomb_walk_back_left'), ('bigbomb_walk_back_right', 'bigbomb_walk_back_right'), ('bigbomb_walk_left', 'bigbomb_walk_left'), ('bigbomb_walk_left_diagonal', 'bigbomb_walk_left_diagonal'), ('bigbomb_walk_right', 'bigbomb_walk_right'), ('bigbomb_walk_right_diagonal', 'bigbomb_walk_right_diagonal'), ('bigbomb_charge', 'bigbomb_charge'), ('bigbomb_charge_loop', 'bigbomb_charge_loop'), ('bigbomb_charge_throw', 'bigbomb_charge_throw'), ('kneel_fromidle', 'kneel_fromidle'), ('wheel_idle', 'wheel_idle'), ('boxing_fromidle', 'boxing_fromidle'), ('boxing_hit_head_right', 'boxing_hit_head_right'), ('boxing_idle', 'boxing_idle'), ('boxing_idle_alt', 'boxing_idle_alt'), ('boxing_kick', 'boxing_kick'), ('boxing_punch', 'boxing_punch'), ('boxing_haymaker', 'boxing_haymaker'), ('fishing_idle', 'fishing_idle'), ('fishing_pole_idle', 'fishing_pole_idle'), ('fishing_pole_cast', 'fishing_pole_cast'), ('fishing_drawpole', 'fishing_drawpole'), ('gun_reload', 'gun_reload'), ('gun_draw', 'gun_draw'), ('gun_hurt', 'gun_hurt'), ('gun_fire', 'gun_fire'), ('gun_pointedup_idle', 'gun_pointedup_idle'), ('gun_putaway', 'gun_putaway'), ('gun_aim_idle', 'gun_aim_idle'), ('rifle_fight_forward_diagonal_left', 'rifle_fight_forward_diagonal_left'), ('rifle_fight_forward_diagonal_right', 'rifle_fight_forward_diagonal_right'), ('rifle_fight_walk_back_diagonal_left', 'rifle_fight_walk_back_diagonal_left'), ('rifle_fight_walk_back_diagonal_right', 'rifle_fight_walk_back_diagonal_right'), ('rifle_fight_run_strafe_right', 'rifle_fight_run_strafe_right'), ('rifle_fight_run_strafe_left', 'rifle_fight_run_strafe_left'), ('rifle_fight_shoot_hip', 'rifle_fight_shoot_hip'), ('rifle_fight_shoot_high_idle', 'rifle_fight_shoot_high_idle'), ('rifle_fight_shoot_high', 'rifle_fight_shoot_high'), ('rifle_fight_idle', 'rifle_fight_idle'), ('rifle_fight_walk', 'rifle_fight_walk'), ('rifle_fight_walk_strafe_left', 'rifle_fight_walk_strafe_left'), ('rifle_fight_walk_strafe_right', 'rifle_fight_walk_strafe_right'), ('rifle_reload_hip', 'rifle_reload_hip'), ('rifle_idle_to_fight_idle', 'rifle_idle_to_fight_idle'), ('blacksmith_work_idle', 'blacksmith_work_idle'), ('blacksmith_work_look_idle', 'blacksmith_work_look_idle'), ('blacksmith_work_outof_look', 'blacksmith_work_outof_look'), ('blacksmith_work_into_look', 'blacksmith_work_into_look'), ('cargomaster_work_idle', 'cargomaster_work_idle'), ('cargomaster_work_look_idle', 'cargomaster_work_look_idle'), ('cargomaster_work_outof_look', 'cargomaster_work_outof_look'), ('cargomaster_work_into_look', 'cargomaster_work_into_look'), ('shovel', 'shovel'), ('shovel_idle', 'shovel_idle'), ('shovel_idle_into_dig', 'shovel_idle_into_dig'), ('hand_curse_check', 'hand_curse_check'), ('hand_curse_get_sword', 'hand_curse_get_sword'), ('hand_curse_reaction', 'hand_curse_reaction'), ('chest_idle', 'chest_idle'), ('chest_strafe_left', 'chest_strafe_left'), ('chest_strafe_right', 'chest_strafe_right'), ('chest_walk', 'chest_walk'), ('chest_putdown', 'chest_putdown'), ('chest_kneel_to_steal', 'chest_kneel_to_steal'), ('chest_steal', 'chest_steal'), ('rigging_climb', 'rigging_climb'), ('board', 'board'), ('rope_grab', 'rope_grab'), ('rope_grab_from_idle', 'rope_grab_from_idle'), ('rope_board', 'rope_board'), ('rope_dismount', 'rope_dismount'), ('swing_aboard', 'swing_aboard'), ('intro', 'crawl_up_b'), ('crawl', 'crawl'), ('jail_dropinto', 'jail_dropinto'), ('jail_idle', 'jail_idle'), ('jail_standup', 'jail_standup'), ('sand_in_eyes', 'sand_in_eyes'), ('sand_in_eyes_holdweapon_noswing', 'sand_in_eyes_holdweapon_noswing'), ('sand_in_eyes_wWeapon', 'sand_in_eyes_wWeapon'), ('stock_idle', 'stock_idle'), ('stock_sleep', 'stock_sleep'), ('stock_sleep_to_idle', 'stock_sleep_to_idle'), ('death', 'death'), ('death2', 'death2'), ('death3', 'death3'), ('death4', 'death4'), ('bayonet_drill', 'bayonet_drill'), ('bayonet_attack_idle', 'bayonet_attack_idle'), ('bayonet_attack_walk', 'bayonet_attack_walk'), ('bayonet_attackA', 'bayonet_attackA'), ('bayonet_attackB', 'bayonet_attackB'), ('bayonet_attackC', 'bayonet_attackC'), ('bayonet_idle', 'bayonet_idle'), ('bayonet_jump', 'bayonet_jump'), ('bayonet_turn_left', 'bayonet_turn_left'), ('bayonet_turn_right', 'bayonet_turn_right'), ('bayonet_fall_ground', 'bayonet_fall_ground'), ('bayonet_run', 'bayonet_run'), ('bayonet_idle_to_fight_idle', 'bayonet_idle_to_fight_idle'), ('bayonet_walk', 'bayonet_walk'), ('bayonet_attack_idle', 'bayonet_attack_idle'), ('bayonet_jump', 'bayonet_jump'), ('bayonet_turn_left', 'bayonet_turn_left'), ('bayonet_turn_right', 'bayonet_turn_right'), ('bayonet_fall_ground', 'bayonet_fall_ground'), ('blunderbuss_reload', 'blunderbuss_reload'), ('broadsword_combo', 'broadsword_combo'), ('broadsword_combo_motion', 'broadsword_combo'), ('sabre_combo', 'sabre_combo'), ('sabre_combo_motion', 'sabre_combo'), ('sword_draw', 'sword_draw'), ('sword_idle', 'sword_idle'), ('sword_putaway', 'sword_putaway'), ('sword_slash', 'sword_slash'), ('sword_thrust', 'sword_thrust'), ('sword_hit', 'sword_hit'), ('sword_cleave', 'sword_cleave'), ('sword_lunge', 'sword_lunge'), ('sword_comboA', 'sword_comboA'), ('sword_roll_thrust', 'sword_roll_thrust'), ('cutlass_attention', 'cutlass_attention'), ('cutlass_combo', 'cutlass_combo'), ('cutlass_hurt', 'cutlass_hurt'), ('cutlass_taunt', 'cutlass_taunt'), ('cutlass_sweep', 'cutlass_sweep'), ('cutlass_bladestorm', 'cutlass_bladestorm'), ('cutlass_headbutt', 'cutlass_headbutt'), ('cutlass_walk_navy', 'cutlass_walk_navy'), ('dagger_backstab', 'dagger_backstab'), ('dagger_combo', 'dagger_combo'), ('dagger_coup', 'dagger_coup'), ('dagger_asp', 'dagger_asp'), ('dagger_hurt', 'dagger_hurt'), ('dagger_throw_combo', 'dagger_throw_combo'), ('dagger_throw_sand', 'dagger_throw_sand'), ('dagger_vipers_nest', 'dagger_vipers_nest'), ('bomb_receive', 'bomb_receive'), ('dagger_receive', 'dagger_receive'), ('doll_receive', 'doll_receive'), ('staff_receive', 'staff_receive'), ('knife_throw', 'knife_throw'), ('voodoo_draw', 'voodoo_draw'), ('voodoo_doll_hurt', 'voodoo_doll_hurt'), ('voodoo_idle', 'voodoo_idle'), ('voodoo_tune', 'voodoo_tune'), ('voodoo_strafe_left', 'voodoo_strafe_left'), ('voodoo_strafe_right', 'voodoo_strafe_right'), ('voodoo_swarm', 'voodoo_swarm'), ('voodoo_walk', 'voodoo_walk'), ('voodoo_doll_poke', 'voodoo_doll_poke'), ('wand_cast_fire', 'wand_cast_fire'), ('wand_cast_idle', 'wand_cast_idle'), ('wand_cast_start', 'wand_cast_start'), ('wand_hurt', 'wand_hurt'), ('wand_idle', 'wand_idle'), ('barf', 'barf'), ('burp', 'burp'), ('fart', 'fart'), ('fsh_idle', 'fsh_idle'), ('fsh_smallCast', 'fsh_smallCast'), ('fsh_bigCast', 'fsh_bigCast'), ('fsh_smallSuccess', 'fsh_smallSuccess'), ('fsh_bigSuccess', 'fsh_bigSuccess'), ('kneel_dizzy', 'kneel_dizzy'), ('mixing_idle', 'mixing_idle'), ('turn_left', 'turn_left'), ('turn_right', 'turn_right'), ('spin_left', 'spin_left'), ('spin_right', 'spin_right'), ('attention', 'attention'), ('march', 'march'), ('left_face', 'left_face'), ('0_tut_act_1_1_1_jail', '0_tut_act_1_1_1_jail'), ('0_tut_act_1_1_2_jail', '0_tut_act_1_1_2_jail'), ('tut_1_1_5_a_idle_dan', 'tut_1_1_5_a_idle_dan'), ('tut_1_1_5_b_dan', 'tut_1_1_5_b_dan'), ('1_tut_act_1_1_5_a_dan', '1_tut_act_1_1_5_a_dan'), ('1_tut_act_1_1_5_c_dan', '1_tut_act_1_1_5_c_dan'), ('0_tut_act_1_2_dock', '0_tut_act_1_2_dock'), ('1_tut_act_1_2_dock', '1_tut_act_1_2_dock'), ('0_tut_act_1_2_b_dock', '0_tut_act_1_2_b_dock'), ('1_tut_act_1_2_b_dock', '1_tut_act_1_2_b_dock'), ('0_tut_act_1_3_jr_a', '0_tut_act_1_3_jr_a'), ('0_tut_act_1_3_jr_b', '0_tut_act_1_3_jr_b'), ('1_tut_act_1_3_jr_a', '1_tut_act_1_3_jr_a'), ('1_tut_act_1_3_jr_b', '1_tut_act_1_3_jr_b'), ('2_tut_act_1_3_jr_a', '2_tut_act_1_3_jr_a'), ('2_tut_act_1_3_jr_b', '2_tut_act_1_3_jr_b'), ('3_tut_act_1_3_jr_a', '3_tut_act_1_3_jr_a'), ('3_tut_act_1_3_jr_b', '3_tut_act_1_3_jr_b'), ('0_tut_act_2_1_wt', '0_tut_act_2_1_wt'), ('0_tut_act_2_1_b_wt', '0_tut_act_2_1_b_wt'), ('2_tut_act_2_1_b_wt', '2_tut_act_2_1_b_wt'), ('3_tut_act_2_1_b_wt', '3_tut_act_2_1_b_wt'), ('0_tut_act_2_2_td', '0_tut_act_2_2_td'), ('1_tut_act_2_2_td', '1_tut_act_2_2_td'), ('2_tut_act_2_2_td', '2_tut_act_2_2_td'), ('3_tut_act_2_2_td', '3_tut_act_2_2_td'), ('4_tut_act_2_2_td', '4_tut_act_2_2_td'), ('5_tut_act_2_2_td', '5_tut_act_2_2_td'), ('0_tut_act_2_3_es', '0_tut_act_2_3_es'), ('0_tut_act_2_4_cb_a', '0_tut_act_2_4_cb_a'), ('0_tut_act_2_4_cb_b', '0_tut_act_2_4_cb_b'), ('0_tut_act_2_4_cb_c', '0_tut_act_2_4_cb_c'), ('0_tut_act_2_5_js', '0_tut_act_2_5_js'), ('1_tut_act_2_5_js', '1_tut_act_2_5_js'), ('1_tut_act_3_1_bp', '1_tut_act_3_1_bp'), ('2_tut_act_3_1_bp', '2_tut_act_3_1_bp'), ('3_tut_act_3_1_bp', '3_tut_act_3_1_bp'), ('4_tut_act_3_1_bp', '4_tut_act_3_1_bp'), ('0_tut_act_3_2_js', '0_tut_act_3_2_js'), ('1_tut_act_3_2_js', '1_tut_act_3_2_js'), ('sit', 'sit'), ('sit_idle', 'sit_idle'), ('deal_idle', 'deal_idle'), ('deal', 'deal'), ('deal_left', 'deal_left'), ('deal_right', 'deal_right'), ('into_deal', 'into_deal'), ('cards_bad_tell', 'cards_bad_tell'), ('cards_bet', 'cards_bet'), ('cards_cheat', 'cards_cheat'), ('cards_check', 'cards_check'), ('cards_good_tell', 'cards_good_tell'), ('cards_hide', 'cards_hide'), ('cards_hide_hit', 'cards_hide_hit'), ('cards_hide_idle', 'cards_hide_idle'), ('cards_pick_up', 'cards_pick_up'), ('cards_pick_up_idle', 'cards_pick_up_idle'), ('cards_set_down', 'cards_set_down'), ('cards_set_down_lose', 'cards_set_down_lose'), ('cards_set_down_win', 'cards_set_down_win'), ('cards_set_down_win_show', 'cards_set_down_win_show'), ('cards_blackjack_hit', 'cards_blackjack_hit'), ('cards_blackjack_stay', 'cards_blackjack_stay'), ('kick_door', 'kick_door'), ('kick_door_loop', 'kick_door_loop'), ('teleport', 'teleport'), ('tentacle_squeeze', 'tentacle_squeeze'), ('tentacle_idle', 'tentacle_idle'), ('screenshot_pose', 'screenshot_pose'), ('friend_pose', 'friend_pose'), ('rigTest', 'rigTest'), ('foil_coup', 'foil_coup'), ('foil_hack', 'foil_hack'), ('foil_idle', 'foil_idle'), ('foil_slash', 'foil_slash'), ('foil_thrust', 'foil_thrust'), ('foil_kick', 'foil_kick'), ('sword_advance', 'sword_advance'), ('dualcutlass_comboA', 'dualcutlass_comboA'), ('dualcutlass_comboB', 'dualcutlass_comboB'), ('dualcutlass_draw', 'dualcutlass_draw'), ('dualcutlass_idle', 'dualcutlass_idle'), ('dualcutlass_hurt', 'dualcutlass_hurt'), ('dualcutlass_walk', 'dualcutlass_walk'), ('emote_duhhh', 'emote_duhhh'), ('emote_blow_kiss', 'emote_blow_kiss'), ('emote_flirt', 'emote_flirt'), ('emote_sassy', 'emote_sassy'), ('emote_talk_to_the_hand', 'emote_talk_to_the_hand'), ('emote_crazy', 'emote_crazy'), ('emote_cut_throat', 'emote_cut_throat'), ('emote_embarrassed', 'emote_embarrassed'), ('emote_face_smack', 'emote_face_smack'), ('emote_hand_it_over', 'emote_hand_it_over'), ('emote_head_scratch', 'emote_head_scratch'), ('emote_nervous', 'emote_nervous'), ('emote_scared', 'emote_scared'), ('emote_show_me_the_money', 'emote_show_me_the_money'), ('emote_shrug', 'emote_shrug'), ('emote_sincere_thanks', 'emote_sincere_thanks'), ('emote_snarl', 'emote_snarl'), ('crazy_ned_day_idle', 'crazy_ned_day_idle'), ('crazy_ned_day_walk', 'crazy_ned_day_walk'), ('crazy_ned_day_interact', 'crazy_ned_day_interact'), ('crazy_ned_night_idle', 'crazy_ned_night_idle'), ('crazy_ned_night_interact', 'crazy_ned_night_interact'), ('crazy_ned_night_jump_in_box', 'crazy_ned_night_jump_in_box'), ('crazy_ned_night_jump_out_box', 'crazy_ned_night_jump_out_box'))

class Biped(UsesAnimationMixer, Avatar, UsesEffectNode):
    SfxNames = {'death': SoundGlobals.SFX_MONSTER_DEATH}
    sfx = {}
    FailsafeAnims = (
     ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0))
    animInfo = {}

    def __init__(self, other=None, animationMixerClass=BipedAnimationMixer):
        self.wantZombie = base.config.GetBool('want-zombie', 0)
        Avatar.__init__(self, other)
        UsesAnimationMixer.__init__(self, animationMixerClass)
        UsesEffectNode.__init__(self)
        Biped.initSfx()
        self.setPickable(0)
        self.height = 0.0
        self.nametagOffset = -5.0
        self.rootScale = 1.0
        self.nameText = None
        self.iconNodePath = None
        self.battleTubeHeight = 0.0
        self.battleTubeRadius = 0.0
        self.lerpHeadTrack = None
        self.loadAnimatedHead = None
        self.rightHandNode = NodePath(ModelNode('rightHand'))
        self.leftHandNode = NodePath(ModelNode('leftHand'))
        self.weaponJointInstances = []
        self.headFudgeHpr = Vec3(0, 0, 0)
        self.renderReflection = False
        self.nametag2dContents = 0
        self.nametag2dDist = 0
        self.nametag2dNormalContents = 0
        self.nametag.getNametag2d().setContents(0)
        self.nametag3d.setLightOff()
        self.fader = None
        return

    def setName(self, val):
        Avatar.setName(self, val)

    def deleteWeaponJoints(self):
        if not self.rightHandNode.isEmpty():
            self.rightHandNode.detachNode()
        if not self.leftHandNode.isEmpty():
            self.leftHandNode.detachNode()
        for node in self.weaponJointInstances:
            node.detachNode()

        self.weaponJointInstances = []

    def delete(self):
        self.loadAnimatedHead = None
        self.deleteWeaponJoints()
        Avatar.delete(self)
        UsesAnimationMixer.delete(self)
        UsesEffectNode.delete(self)
        return

    def actorInterval(self, *args, **kwargs):
        if hasattr(self, 'undead') and self.undead:
            return UsesAnimationMixer.actorInterval(self.skeleton, *args, **kwargs)
        else:
            bodyIval = UsesAnimationMixer.actorInterval(self, *args, **kwargs)
            return bodyIval

    def play(self, *args, **kwArgs):
        if hasattr(self, 'undead') and self.undead:
            UsesAnimationMixer.play(self.skeleton, *args, **kwArgs)
        else:
            UsesAnimationMixer.play(self, *args, **kwArgs)

    def loop(self, *args, **kwArgs):
        if hasattr(self, 'undead') and self.undead:
            UsesAnimationMixer.loop(self.skeleton, *args, **kwArgs)
        else:
            UsesAnimationMixer.loop(self, *args, **kwArgs)

    def stop(self, *args, **kwArgs):
        if hasattr(self, 'undead') and self.undead:
            UsesAnimationMixer.stop(self.skeleton, *args, **kwArgs)
        else:
            UsesAnimationMixer.stop(self, *args, **kwArgs)

    def pose(self, *args, **kwArgs):
        if hasattr(self, 'undead') and self.undead:
            UsesAnimationMixer.pose(self.skeleton, *args, **kwArgs)
        else:
            UsesAnimationMixer.pose(self, *args, **kwArgs)

    def pingpong(self, *args, **kwArgs):
        if hasattr(self, 'undead') and self.undead:
            UsesAnimationMixer.pingpong(self.skeleton, *args, **kwArgs)
        else:
            UsesAnimationMixer.pingpong(self, *args, **kwArgs)

    def getDuration(self, animName=None, partName=None, fromFrame=None, toFrame=None):
        return Avatar.getDuration(self, animName, partName, fromFrame, toFrame)

    def getFrameTime(self, animName, frame, partName=None):
        return Avatar.getFrameTime(self, animName, frame, partName)

    def getRadius(self):
        return self.battleTubeRadius

    def getWeaponJoints(self):
        self.deleteWeaponJoints()
        lods = list(self.getLODNames())
        lods.sort()
        for lodName in lods:
            handLocator = self.getLOD(lodName).find('**/*weapon_right')
            if not handLocator.isEmpty():
                if lodName == lods[0]:
                    self.rightHandNode.reparentTo(handLocator)
                else:
                    self.weaponJointInstances.append(self.rightHandNode.instanceTo(handLocator))
            handLocator = self.getLOD(lodName).find('**/*weapon_left')
            if not handLocator.isEmpty():
                if lodName == lods[0]:
                    self.leftHandNode.reparentTo(handLocator)
                else:
                    self.weaponJointInstances.append(self.leftHandNode.instanceTo(handLocator))

        self.postAsyncLoadFix()

    def postAsyncLoadFix(self):
        pass

    def startLookAroundTask(self):
        taskMgr.remove(self.lookAroundTaskName)
        if self.headNode:
            delayTime = 1.0 + random.random() * 1.0
            taskMgr.doMethodLater(delayTime, self.lookAroundTask, self.lookAroundTaskName)

    def stopLookAroundTask(self):
        taskMgr.remove(self.lookAroundTaskName)
        if self.lerpHeadTrack:
            self.lerpHeadTrack.pause()
            self.lerpHeadTrack = None
        if self.headNode:
            self.headNode.setHpr(self.headFudgeHpr)
        return

    def isInFov(self, target):
        k = 0.6658
        relPos = target.getPos(self)
        if relPos[1] > 0:
            tan = relPos[0] / relPos[1]
            if tan < k and tan > -k:
                return 1
        return 0

    def lookAroundTask(self, task):
        if self.isLocal():
            if self.gameFSM.state == 'Battle' and self.currentTarget and not self.currentTarget.isEmpty():
                task.delayTime = 5.0
                return Task.again
        if self.getCurrentAnim() in stopLookaroundAnimList:
            self.headNode.setHpr(self.headFudgeHpr)
            return Task.again
        hFov = 90
        vFov = 35
        if base.cr.targetMgr:
            allTargets = base.cr.targetMgr.objectDict.values()
        else:
            allTargets = []
        visibleTargets = []
        for target in allTargets:
            if not target.isEmpty():
                if self.isInFov(target):
                    visibleTargets.append(target)

        if len(visibleTargets) > 0:
            if random.choice((True, True, False)):
                dummyNode = self.attachNewNode('dummy')
                dummyNode.setZ(self.getHeight())
                dummyNode.lookAt(random.choice(visibleTargets))
                heading = max(-hFov * 0.5, min(hFov * 0.5, dummyNode.getH()))
                pitch = max(-vFov * 0.5, min(vFov * 0.5, dummyNode.getP()))
                newHpr = Vec3(0, heading, -pitch)
                dummyNode.removeNode()
            else:
                newHpr = self.headFudgeHpr
        else:
            if random.choice((True, True, False)):
                newHpr = Vec3(0, random.random() * hFov - hFov * 0.5, random.random() * vFov - vFov * 0.5)
            else:
                newHpr = self.headFudgeHpr
            if self.lerpHeadTrack:
                self.lerpHeadTrack.pause()
                self.lerpHeadTrac3dk = None
        t = 0.2 + random.random() * 0.8
        self.lerpHeadTrack = LerpHprInterval(self.headNode, t, newHpr, blendType='easeInOut')
        self.lerpHeadTrack.start()
        task.delayTime = 3.0 + random.random() * 4.0
        return Task.again

    def initializeNametag3d(self):
        Avatar.initializeNametag3d(self)
        self.nametag3d.setColorScaleOff(100)
        self.nametag3d.setLightOff()
        self.nametag3d.setFogOff()
        self.nametag3d.setZ(self.scale)
        self.nametag3d.setH(self.getGeomNode().getH())
        self.nametag.setFont(PiratesGlobals.getPirateFont())
        self.iconNodePath = self.nametag.getNameIcon()
        if self.iconNodePath.isEmpty():
            self.notify.warning('empty iconNodePath in initializeNametag3d')
            return 0
        if not self.nameText:
            self.nameText = OnscreenText(fg=Vec4(1, 1, 1, 1), bg=Vec4(0, 0, 0, 0), scale=1.1, align=TextNode.ACenter, mayChange=1, font=PiratesGlobals.getPirateBoldOutlineFont())
            self.nameText.reparentTo(self.iconNodePath)
            self.nameText.setTransparency(TransparencyAttrib.MDual, 2)
            self.nameText.setColorScaleOff(100)
            self.nameText.setLightOff()
            self.nameText.setFogOff()
            self.nameTag3dInitialized()

    def nameTag3dInitialized(self):
        pass

    def getNameText(self):
        return self.nameText

    def getDeathAnimName(self, animNum=None):
        animStrings = ['death', 'death2', 'death3', 'death4']
        if animNum not in range(len(animStrings)):
            animNum = random.choice(range(0, len(animStrings)))
        return animStrings[animNum]

    def setChatAbsolute(self, chatString, chatFlags, dialogue=None, interrupt=1):
        Avatar.setChatAbsolute(self, chatString, chatFlags, dialogue, interrupt)
        if chatString:
            avId = None
            if hasattr(self, 'doId'):
                avId = self.doId
            base.talkAssistant.receiveOpenTalk(avId, self.getName(), 0, None, chatString)
        return

    def fadeIn(self, time):
        if self.fader:
            self.fader.finish()
            self.fader = None
        self.setTransparency(1)
        self.setColorScale(1, 1, 1, 0)
        self.show()
        self.fader = self.colorScaleInterval(time, Vec4(1, 1, 1, 1), startColorScale=Vec4(1, 1, 1, 0))
        self.fader.start()
        return

    def fadeOut(self, time):
        if self.fader:
            self.fader.finish()
            self.fader = None
        self.setTransparency(1)
        self.setColorScale(1, 1, 1, 1)
        self.fader = Sequence(self.colorScaleInterval(time, Vec4(1, 1, 1, 0), startColorScale=Vec4(1, 1, 1, 1)), Func(self.hide))
        self.fader.start()
        return

    @classmethod
    def setupAnimInfoState(cls, state, info):
        if len(info) < len(cls.FailsafeAnims):
            info += cls.FailsafeAnims[len(info) - len(cls.FailsafeAnims):]
        cls.animInfo[state] = info

    def getAnimInfo(self, state):
        return self.animInfo.get(state, self.FailsafeAnims)

    def setRenderReflection(self):
        OTPRender.renderReflection(self.renderReflection, self, 'p_biped', None)
        return

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('strafe_left', 1), ('strafe_right', 1), ('run_diagonal_left', 1), ('run_diagonal_right', 1), ('walk_back_diagonal_left', 1), ('walk_back_diagonal_right', 1), ('fall_ground', 1), ('fall_ground', 1), ('spin_left', 1), ('spin_right', 1)))
        cls.setupAnimInfoState('WaterRoam', (('tread_water', 1.0), ('swim', 1.0), ('swim', 1.0), ('swim_back', 1.0), ('swim_left', 1.0), ('swim_right', 1.0), ('swim_left_diagonal', 1.0), ('swim_right_diagonal', 1.0), ('swim_back_diagonal_left', 1.0), ('swim_back_diagonal_right', 1.0), ('fall_ground', 1), ('fall_ground', 1), ('tread_water', 1), ('tread_water', 1)))
        cls.setupAnimInfoState('LandTreasureRoam', (('chest_idle', 1.0), ('chest_walk', 1.0), ('chest_walk', 1.0), ('chest_walk', -1.0), ('chest_strafe_left', 1.0), ('chest_strafe_right', 1.0), ('chest_strafe_left', 1), ('chest_strafe_right', 1), ('chest_strafe_right', -1), ('chest_strafe_left', -1), ('fall_ground', 1), ('fall_ground', 1), ('chest_walk', 1), ('chest_walk', 1)))
        cls.setupAnimInfoState('WaterTreasureRoam', (('tread_water', 1.0), ('swim', 1.0), ('swim', 1.0), ('swim_back', 1.0), ('swim_left', 1.0), ('swim_right', 1.0), ('swim_left_diagonal', 1.0), ('swim_right_diagonal', 1.0), ('swim_back_diagonal_left', 1.0), ('swim_back_diagonal_right', 1.0), ('fall_ground', 1), ('fall_ground', 1), ('walk', 1), ('walk', 1)))
        cls.setupAnimInfoState('BayonetLandRoam', (('bayonet_idle', 1.0), ('bayonet_walk', 1.0), ('bayonet_run', 1.0), ('bayonet_walk', -1.0), ('strafe_left', 1), ('strafe_right', 1), ('run_diagonal_left', 1), ('run_diagonal_right', 1), ('walk_back_diagonal_left', 1), ('walk_back_diagonal_right', 1), ('fall_ground', 1), ('fall_ground', 1), ('spin_left', 1.0), ('spin_right', 1.0)))

    @classmethod
    def initSfx(cls):
        for name, effect in cls.SfxNames.iteritems():
            if name not in cls.sfx:
                sound = SoundGlobals.loadSfx(effect)
                if sound and sound.getActive():
                    cls.sfx[name] = sound


Biped.setupAnimInfo()
Biped.initSfx()