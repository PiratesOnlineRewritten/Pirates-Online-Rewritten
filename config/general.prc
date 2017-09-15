# Window:
window-title Pirates Online Rewritten
icon-filename phase_3/etc/Pirates_Adds.ico
win-size 800 600
win-origin -2 -2
fullscreen #f
color-bits 0
framebuffer-depth #f

# Text:
text-encoding utf8
direct-wtext #f
text-never-break-before 1
text-flatten 0
text-dynamic-merge 1
text-minfilter linear
text-magfilter linear
text-page-size 512 512
text-rwap-mode WM_border_clor

# Models:
model-path ../resources
model-path ../resources/phase_2
model-path ../resources/phase_3
model-path ../resources/phase_4
model-path ../resources/phase_5
default-model-extension .bam

# Display Pipeline:
load-display pandagl
aux-display pandagl
aux-display pandadx9
aux-display tinydisplay

# Audio:
audio-output-rate 44100
audio-preload-threshold 1024
audio-library-name p3fmod_audio

# Graphics:
allow-live-flatten 1
framebuffer-alpha 1
alpha-bits 8
prefer-parasite-buffer 1
force-parasite-buffer 1
retransform-sprites 1

# Stenciles:
stencil-bits 8

# SRGB:
framebuffer-srgb #f

# DClass (reverse order...):
dc-file astron/dclass/pirates.dc
dc-file astron/dclass/otp.dc

# Animations: 
even-animation #t
interpolate-frames #t
hardware-animated-vertices #t
restore-initial-pose #f

# Cache:
model-cache-max-kbytes 262144
want-disk-cache #t
state-cache #t
transform-cache #t
model-cache-textures #f

# Textures:
textures-power-2 none
#textures-power-2 down
texture-anisotropic-degree 16
texture-magfilter linear
texture-minfilter linear
texture-quality-level fastest

# Texture Scales:
exclude-texture-scale BardiT*
exclude-texture-scale BriosoPro*
exclude-texture-scale Buccaneer_outline_1*
exclude-texture-scale playingcards*
exclude-texture-scale gui_*
exclude-texture-scale loading_screen*
exclude-texture-scale loadingscreen_*
exclude-texture-scale loading_window_texture*
exclude-texture-scale vr_*
exclude-texture-scale minimap_*
exclude-texture-scale general_frame_*
exclude-texture-scale drop-shadow
exclude-texture-scale pir_t_gui_*
exclude-texture-scale 2xp*
exclude-texture-scale AztechGold2*
exclude-texture-scale Interceptor_Render*
exclude-texture-scale Merchant_Render*
exclude-texture-scale NameTumbler*
exclude-texture-scale SelectionCursor*
exclude-texture-scale Speed_Chat_*_Tex*
exclude-texture-scale Warship_Render*
exclude-texture-scale avatar_c_*
exclude-texture-scale bar_shot*
exclude-texture-scale barnacles*
exclude-texture-scale base*
exclude-texture-scale box_base*
exclude-texture-scale bp_crew_carver*
exclude-texture-scale bpcrew_*
exclude-texture-scale buff_*
exclude-texture-scale bullet*
exclude-texture-scale but_compass*
exclude-texture-scale but_*
exclude-texture-scale cannon*
exclude-texture-scale cannon_barrage*
exclude-texture-scale cannon_chain_shot*
exclude-texture-scale cannon_explosive*
exclude-texture-scale cannon_firebrand*
exclude-texture-scale cannon_flaming_skull*
exclude-texture-scale cannon_fury*
exclude-texture-scale cannon_grape_shot*
exclude-texture-scale cannon_grapple_hook*
exclude-texture-scale cannon_round_shot*
exclude-texture-scale cannon_scrounger*
exclude-texture-scale cannon_shoot*
exclude-texture-scale cannon_shrapnel*
exclude-texture-scale cannon_thunderbolt*
exclude-texture-scale cannon_toughness*
exclude-texture-scale chain_shot*
exclude-texture-scale chargui_*
exclude-texture-scale chatArrow*
exclude-texture-scale chat_*
exclude-texture-scale comet*
exclude-texture-scale compass_*
exclude-texture-scale crew_member*
exclude-texture-scale cutlass_*
exclude-texture-scale dagger*
exclude-texture-scale dialmeter_full*
exclude-texture-scale dialmeter_half*
exclude-texture-scale doll*
exclude-texture-scale emotionIcon*
exclude-texture-scale explosive*
exclude-texture-scale firebrand*
exclude-texture-scale fist*
exclude-texture-scale flag_*
exclude-texture-scale flagship_*
exclude-texture-scale flame_cloud*
exclude-texture-scale flaming_skull*
exclude-texture-scale founders_coin*
exclude-texture-scale founders_silver_coin*
exclude-texture-scale friend_button*
exclude-texture-scale fury*
exclude-texture-scale gas_cloud*
exclude-texture-scale generic_*
exclude-texture-scale gm_logo*
exclude-texture-scale gold*
exclude-texture-scale goldCoin*
exclude-texture-scale grape_shot*
exclude-texture-scale grapple_hook*
exclude-texture-scale grenade*
exclude-texture-scale groggy_clamp*
exclude-texture-scale icon_*
exclude-texture-scale iron*
exclude-texture-scale island_sketch_mark*
exclude-texture-scale keyboard_button*
exclude-texture-scale kingshead_lod*
exclude-texture-scale knives*
exclude-texture-scale lead*
exclude-texture-scale logo_french_flag*
exclude-texture-scale logo_spanish_flag*
exclude-texture-scale lookout_*
exclude-texture-scale madre_lod*
exclude-texture-scale main_gui_*
exclude-texture-scale mine*
exclude-texture-scale moderation*
exclude-texture-scale morale_skull*
exclude-texture-scale nonpayer_panel*
exclude-texture-scale offscreen_flash*
exclude-texture-scale open_chat_enabled_icon*
exclude-texture-scale parchment*
exclude-texture-scale pir_t_bld_eng_shingles_footprint*
exclude-texture-scale pir_t_bld_eng_wall_footprint*
exclude-texture-scale pir_t_bld_frt_floor_footprint*
exclude-texture-scale pir_t_bld_frt_roof_footprint*
exclude-texture-scale pir_t_bld_frt_wall_footprint*
exclude-texture-scale pir_t_bld_shn_boat_footprint*
exclude-texture-scale pir_t_bld_shn_gypsy_footprint*
exclude-texture-scale pir_t_bld_shn_shingles_footprint*
exclude-texture-scale pistol*
exclude-texture-scale port_royal_lod*
exclude-texture-scale pvp_arrow*
exclude-texture-scale pvp_island_a_lod*
exclude-texture-scale pvp_island_b_lod*
exclude-texture-scale pvp_rock_lod*
exclude-texture-scale quest_pending_icon*
exclude-texture-scale recharge_*
exclude-texture-scale redglow_skull*
exclude-texture-scale reward_waiting_icon*
exclude-texture-scale roundshot*
exclude-texture-scale rumrunner_lod*
exclude-texture-scale sail_*
exclude-texture-scale set1_*
exclude-texture-scale set2_*
exclude-texture-scale set3_*
exclude-texture-scale set4_*
exclude-texture-scale set5_*
exclude-texture-scale set6_*
exclude-texture-scale set7_*
exclude-texture-scale set8_*
exclude-texture-scale set9_*
exclude-texture-scale shadow_circular*
exclude-texture-scale ship_battle_dish02*
exclude-texture-scale ship_battle_enemy_fort_icon*
exclude-texture-scale ship_battle_ship_name_bar*
exclude-texture-scale ship_battle_speed_bar*
exclude-texture-scale ship_damage_background*
exclude-texture-scale ship_damage_hp*
exclude-texture-scale ship_pvp_icon_french*
exclude-texture-scale ship_pvp_icon_spanish*
exclude-texture-scale ship_window*
exclude-texture-scale shopCoin_*
exclude-texture-scale silver*
exclude-texture-scale skill_tree_level_dot*
exclude-texture-scale skill_tree_level_ring*
exclude-texture-scale skull_ammo*
exclude-texture-scale staff*
exclude-texture-scale steel*
exclude-texture-scale subscribers_lock*
exclude-texture-scale sword*
exclude-texture-scale telescope_button*
exclude-texture-scale thunderbolt*
exclude-texture-scale timer_back*
exclude-texture-scale timer_front*
exclude-texture-scale topgui_*
exclude-texture-scale tortuga_lod*
exclude-texture-scale treasure_chest_closed*
exclude-texture-scale treasure_chest_open*
exclude-texture-scale treasure_w*
exclude-texture-scale triangle*
exclude-texture-scale tutorial_sweep*
exclude-texture-scale venom*
exclude-texture-scale voodoo_*
exclude-texture-scale wild_island_a_lod*
exclude-texture-scale wild_island_b_lod*
exclude-texture-scale wild_island_c_lod*
exclude-texture-scale wild_island_d_lod*
exclude-texture-scale wild_island_e_lod*
exclude-texture-scale wild_island_f_lod*
exclude-texture-scale wm_cuba*
exclude-texture-scale wm_pearl_island*
exclude-texture-scale wm_rumble_shack*
exclude-texture-scale pir_t_gui_pot_*
exclude-texture-scale pir_t_gui_srp_*

# NOTIFIER
notify-level-tiff error
notify-level-dxgsg warning
notify-level-gobj warning
notify-level-loader warning
notify-level-chan fatal
notify-level-pgraph error
notify-level-collide error
notify-level-abs error
notify-level-Actor error
notify-level-DisplayOptions debug

# Graphics Library:
gl-finish #f
gl-force-no-error #t
gl-check-errors #f
gl-force-no-flush #t
gl-force-no-scissor #t

uniquify-matrix #t
uniquify-transforms #t
uniquify-states #t
uniquify-attribs #f

# Shaders:
gl-validate-shaders #f
gl-skip-shader-recompilation-warnings #t

# Font:
text-default-font models/fonts/BardiT_outline.bam

# Server:
server-version pirates-dev
game-server 127.0.0.1

# SSL:
want-ssl-scheme #f

# Loading Screen:
fancy-loading-screen #t

# Antialiasing:
framebuffer-multisample 1
multisamples 2

# LOD:
default-lod-type fade
make-grid-lod true
verify-lods false

# Sticky Keys:
disable-sticky-keys 1

# Other:
want-logout #f
skip-tutorial #f

# Clock:
clock-mode limited
clock-frame-rate 120

# Options Gui:
enable-pipe-selector #f
enable-stereo-display #t
want-gameoptions-hdr #t
enable-frame-rate-counter #t
allow-options-override #f # BROKEN WITH CERTAIN DRIVERS

# Screenshot Viewer:
want-screenshot-viewer #t
model-path ./screenshots

# V-Sync:
sync-video #f

# Tutorial:
skip-tutorial #t
force-tutorial #f

# World:
#default-world PortRoyalWorld

# Analytics:
analytics-game-key 28f391f68f5e07f7713d044ea81f92ca
analytics-secret-key 9de82d4da112aa45ac0ee63f570c45d4e340812f

# Developer:
want-dev #t
#dev-branch-flavor development