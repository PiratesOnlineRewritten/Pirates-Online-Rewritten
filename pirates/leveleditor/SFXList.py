from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfxString
SOUND_FX_LIST = {'Cannon Fire': [loadSfxString(SoundGlobals.SFX_WEAPON_CANNON_FIRE_01), loadSfxString(SoundGlobals.SFX_WEAPON_CANNON_FIRE_02), loadSfxString(SoundGlobals.SFX_WEAPON_CANNON_FIRE_03), loadSfxString(SoundGlobals.SFX_WEAPON_CANNON_FIRE_04), loadSfxString(SoundGlobals.SFX_WEAPON_CANNON_FIRE_05)],'Distant Cannon': [loadSfxString(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_01), loadSfxString(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_02), loadSfxString(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_03), loadSfxString(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_04), loadSfxString(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_05), loadSfxString(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_06), loadSfxString(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_07), loadSfxString(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_08), loadSfxString(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_09), loadSfxString(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_10)],'Ambient': [loadSfxString(SoundGlobals.SFX_AMBIENT_SHORE)],'Sword': [loadSfxString(SoundGlobals.SFX_WEAPON_CUTLASS_CLASHCLANG), loadSfxString(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_01), loadSfxString(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_02), loadSfxString(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_03)],'Explosion': [loadSfxString(SoundGlobals.SFX_FX_EXPLODE_WOOD_01), loadSfxString(SoundGlobals.SFX_FX_EXPLODE_WOOD_02), loadSfxString(SoundGlobals.SFX_FX_EXPLODE_WOOD_GLASS)]}

def getSFXList():
    resultDic = {}
    totalList = []
    for sfxGroup in SOUND_FX_LIST.keys():
        sfxList = [
         [
          sfxGroup], SOUND_FX_LIST[sfxGroup]]
        totalList.append(sfxList)

    resultDic['["SFX Group"]'] = totalList
    return resultDic