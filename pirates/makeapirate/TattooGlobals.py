from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.ai import HolidayGlobals
from pandac.PandaModules import *
import random
from pirates.inventory import ItemGlobals
tattooNames = [
 'blank', 'arm_color_shark', 'arm_color_skull_pirate', 'arm_color_skull_shield', 'arm_color_skull_stab', 'arm_color_snake', 'arm_mono_dagger_fancy', 'arm_mono_flag_skull', 'arm_mono_key', 'arm_mono_skull_ironcross', 'arm_mono_sword_hook', 'chest_color_8dagger', 'chest_color_heart_screw', 'chest_color_key_lock', 'chest_color_skull_dagger', 'chest_color_skullcrossbones', 'chest_mono_anchor', 'chest_mono_compass', 'chest_mono_dagger', 'chest_mono_ship_anchor', 'chest_mono_skullcrossbones', 'skull_face', 'arm_color_nautical_star', 'arm_color_mayanface', 'arm_color_skull_octo', 'arm_mono_skull_tribal', 'chest_color_squid_ship', 'chest_color_saint_patricks', 'arm_mono_nativelizards', 'arm_mono_tribal_01', 'arm_mono_tribal_bird', 'arm_mono_tribal_jellyfish_01', 'arm_mono_tribal_jellyfish_02', 'chest_mono_dd_africanface_01', 'chest_mono_dd_maoriface_01', 'arm_color_asian_leaf', 'arm_color_ethnic_02', 'arm_color_maoriman', 'arm_color_nativeleaf', 'arm_color_thai_01', 'face_color_face_2clovers', 'face_color_face_horseshoeclovers', 'chest_color_celtic4leaf', 'chest_color_ethniceagle', 'chest_color_flintlocks', 'chest_color_shamrock', 'chest_color_thaimonkeyface', 'chest_color_tribalface_01', 'chest_color_tribalface_04', 'chest_mono_dd_asianface_01', 'chest_mono_dd_maoriface_02', 'chest_mono_tribal_01', 'arm_color_celtic_knot', 'arm_color_chinese_knot', 'arm_color_hawaiian_tiki', 'arm_color_sharks', 'arm_color_tribal_waves', 'arm_mono_celtic_deer', 'arm_mono_hawaiian', 'arm_mono_petroglyph', 'arm_mono_ravens', 'arm_mono_wave_fan', 'chest_color_hawaiian_pectoral', 'chest_mono_tribal_yakuza', 'face_color_jacksparrow', 'face_color_tribal_cheek', 'face_color_tribal_chin', 'face_color_tribal_forehead', 'face_mono_maori_chin', 'face_mono_maori_nose', 'face_mono_native_eye', 'face_mono_tribal_gotee', 'face_color_eye_01', 'face_color_cheek', 'face_color_forehead', 'face_color_greennose', 'face_color_tribal_mouth', 'face_mono_cheek', 'face_mono_eye_01', 'face_mono_eye_02', 'face_mono_nose_01', 'face_mono_tribal_beard', 'face_color_voodoo_01', 'face_color_voodoo_02', 'face_color_voodoo_03', 'face_color_voodoo_04', 'face_color_voodoo_05', 'face_mono_voodoo_01', 'face_mono_voodoo_02', 'face_mono_voodoo_03', 'face_mono_voodoo_04', 'face_mono_voodoo_05', 'arm_color_mothersday_flowers', 'arm_mono_mothersday_flowers', 'arm_mono_mothersday_sparrows', 'arm_color_mothersday_sparrows', 'chest_color_mothersday_classic', 'chest_mono_mothersday_classic', 'face_color_mothersday_flower_sm', 'face_mono_mothersday_flower_sm', 'face_color_mothersday_flower_lg', 'face_mono_mothersday_flower_lg', 'face_color_mothersday_hearts', 'face_mono_mothersday_hearts', 'pvp_icon_spanish', 'pvp_icon_french', 'scars_bulletholes_healed', 'scars_piratebrand', 'scars_traintrack01', 'sleeve_color_bluebirds', 'sleeve_color_koi', 'sleeve_color_octopus', 'sleeve_color_peacock', 'sleeve_color_pinkphoenix', 'sleeve_color_pinktribal', 'sleeve_color_seahorses', 'sleeve_color_tribal_orangegreen', 'sleeve_color_tribal_rainbow', 'sleeve_color_tribal_yellowblue', 'sleeve_mono_3butterflies', 'sleeve_mono_bflystars', 'sleeve_mono_butterfly', 'sleeve_mono_kitty', 'sleeve_mono_tribal01', 'sleeve_mono_tribal02', 'sleeve_mono_tribal03', 'sleeve_mono_tribal04', 'sleeve_mono_tribal05', 'sleeve_mono_tribalshell', 'stitches_bulletholes', 'stitches_x', 'stitches_y']
ZONE1 = 0
ZONE2 = 1
ZONE3 = 2
ZONE4 = 3
ZONE5 = 4
ZONE6 = 5
ZONE7 = 6
ZONE8 = 7
ZONE_LIST = [
 ZONE2, ZONE3, ZONE1, ZONE4]
TYPE = 0
OFFSETX = 1
OFFSETY = 2
SCALE = 3
ROTATE = 4
COLOR = 5
_tattoosInitialized = 0
TattooImages = []

def initTattooImages():
    global _tattoosInitialized
    tattoos = loader.loadModel('models/misc/tattoos')
    for i in range(len(tattooNames)):
        image = tattoos.find('**/tattoo_' + tattooNames[i]).findAllTextures().getTexture(0)
        if i == 0:
            image.setCompression(image.CMOff)
        scale = float(image.getXSize()) / float(image.getYSize())
        image.setWrapU(Texture.WMBorderColor)
        image.setWrapV(Texture.WMBorderColor)
        image.setBorderColor(Vec4(1, 1, 1, 1))
        TattooImages.append((image, scale))

    _tattoosInitialized = 1


def getTattooImage(tattooNum):
    if _tattoosInitialized == 0:
        initTattooImages()
    if tattooNum >= len(tattooNames):
        return TattooImages[0]
    else:
        return TattooImages[tattooNum]


def doesTattooExist(modelId):
    return modelId < len(tattooNames)


SOLOMON_ODOUGAL_QUEST_A = 0
LALA_LOVEL_QUEST_A = 1
MERCEDES_CORAZON_QUEST_A = 2
SOLOMON_ODOUGAL_QUEST_B = 3
LALA_LOVEL_QUEST_B = 4
MERCEDES_CORAZON_QUEST_B = 5
SHIP_PVP_FRENCH_QUEST_A = 6
SHIP_PVP_SPANISH_QUEST_A = 7
questDrops = {SOLOMON_ODOUGAL_QUEST_A: [ItemGlobals.TATTOO_ARM_CHINESE_KNOT, ItemGlobals.TATTOO_ARM_CHINESE_KNOT],SOLOMON_ODOUGAL_QUEST_B: [ItemGlobals.TATTOO_FACE_NATIVE_EYE],LALA_LOVEL_QUEST_A: [ItemGlobals.TATTOO_CHEST_HAWAIIAN_PECTORAL],LALA_LOVEL_QUEST_B: [ItemGlobals.TATTOO_ARM_PETROGLYPH, ItemGlobals.TATTOO_ARM_PETROGLYPH],MERCEDES_CORAZON_QUEST_A: [ItemGlobals.TATTOO_ARM_TIKI, ItemGlobals.TATTOO_ARM_TIKI],MERCEDES_CORAZON_QUEST_B: [ItemGlobals.TATTOO_FACE_TRIBAL_CHEEK],SHIP_PVP_FRENCH_QUEST_A: [ItemGlobals.TATTOO_CHEST_FRENCH_SHIP_PVP, ItemGlobals.TATTOO_ARM_FRENCH, ItemGlobals.TATTOO_ARM_FRENCH],SHIP_PVP_SPANISH_QUEST_A: [ItemGlobals.TATTOO_CHEST_SPANISH_SHIP_PVP, ItemGlobals.TATTOO_ARM_SPANISH, ItemGlobals.TATTOO_ARM_SPANISH]}
quest_items = [
 ItemGlobals.TATTOO_ARM_CHINESE_KNOT, ItemGlobals.TATTOO_FACE_NATIVE_EYE, ItemGlobals.TATTOO_CHEST_HAWAIIAN_PECTORAL, ItemGlobals.TATTOO_ARM_PETROGLYPH, ItemGlobals.TATTOO_ARM_TIKI, ItemGlobals.TATTOO_FACE_TRIBAL_CHEEK, ItemGlobals.TATTOO_CHEST_FRENCH_SHIP_PVP, ItemGlobals.TATTOO_ARM_FRENCH, ItemGlobals.TATTOO_CHEST_SPANISH_SHIP_PVP, ItemGlobals.TATTOO_ARM_SPANISH]

def isQuestDrop(id):
    if id in quest_items:
        return True
    else:
        return False