from pirates.uberdog.UberDogGlobals import InventoryType
__levelUpStats = {InventoryType.OverallRep: (25, 3),InventoryType.CutlassRep: (8, 0),InventoryType.GrenadeRep: (8, 0),InventoryType.DaggerRep: (7, 1),InventoryType.PistolRep: (7, 1),InventoryType.DollRep: (4, 6),InventoryType.WandRep: (4, 6),InventoryType.CannonRep: (5, 0),InventoryType.SailingRep: (5, 0)}

def getLevelUpQuest(rep, level):
    retQuests = []
    if rep == InventoryType.OverallRep:
        if level == 5:
            retQuests.append('wd.1visitTia')
        elif level == 7:
            retQuests.append('tpt.1visitTia')
        elif level == 10:
            retQuests.append('wk.1visitElizabeth')
        elif level == 12:
            retQuests.append('tptpr.1visitLucinda')
        elif level == 14:
            retQuests.append('tptc.1visitTiaDalma')
        elif level == 16:
            retQuests.append('tr.1visitElizabeth')
        elif level == 18:
            retQuests.append('tt.1visitJack')
        elif level == 20:
            retQuests.append('wg.1visitJack')
        elif level == 21:
            retQuests.append('tm.1visitWill')
        elif level == 23:
            retQuests.append('tptpdf.1visitRomany')
        elif level == 25:
            retQuests.append('trr.1visitBarbossa')
        elif level == 29:
            retQuests.append('tc.1visitJoshamee')
        elif level == 30:
            retQuests.append('ws.1visitTia')
            retQuests.append('rc.1visitJack')
        elif level == 33:
            retQuests.append('tf.1visitTia')
    return retQuests


def getWeaponLevelUpQuest(rep, level, baseOb):
    retQuests = []
    if rep == InventoryType.CutlassRep:
        if level == 15:
            retQuests.append('wt1.visitWillTurner')
        if level == 20:
            retQuests.append('cul5.1visitBalthasar')
    if rep == InventoryType.DaggerRep:
        if level == 15:
            retQuests.append('jw1.visitJohnWallace')
        if level == 20:
            retQuests.append('dul5.1visitFerrar')
    if rep == InventoryType.PistolRep:
        if level == 15:
            retQuests.append('at1.0visitThayer')
        if level == 20:
            retQuests.append('pul5.1visitErasmus')
    if rep == InventoryType.DollRep:
        if level == 15:
            retQuests.append('vdu4.0visitTiaDalma')
        if level == 20:
            retQuests.append('vdul5.1visitTia')
    if rep == InventoryType.WandRep:
        if level == 15:
            retQuests.append('vsu4.0visitTiaDalma')
        if level == 20:
            retQuests.append('vsul5.1visitRoland')
    return retQuests


def getLevelUpStats(rep):
    stats = __levelUpStats.get(rep)
    if stats:
        return stats
    else:
        return (0, 0)


def getHpGain(rep):
    stats = __levelUpStats.get(rep)
    if stats:
        return stats[0]
    else:
        return 0


def getManaGain(rep):
    stats = __levelUpStats.get(rep)
    if stats:
        return stats[1]
    else:
        return 0


__levelUpSkills = {InventoryType.MeleeRep: {0: ([], [InventoryType.MeleePunch]),3: ([], [InventoryType.MeleeJab]),6: ([], [InventoryType.MeleeKick]),10: ([], [InventoryType.MeleeRoundhouse]),15: ([], [InventoryType.MeleeHeadbutt])},InventoryType.CutlassRep: {0: ([], [InventoryType.CutlassHack, InventoryType.CutlassSlash]),2: ([InventoryType.UnspentCutlass], [InventoryType.CutlassSweep]),3: ([InventoryType.UnspentCutlass], []),4: ([InventoryType.UnspentCutlass], [InventoryType.CutlassCleave]),5: ([InventoryType.UnspentCutlass], []),6: ([InventoryType.UnspentCutlass], [InventoryType.CutlassParry]),7: ([InventoryType.UnspentCutlass], []),8: ([InventoryType.UnspentCutlass], [InventoryType.CutlassBrawl]),9: ([InventoryType.UnspentCutlass], []),10: ([InventoryType.UnspentCutlass], [InventoryType.CutlassFlourish]),11: ([InventoryType.UnspentCutlass], []),12: ([InventoryType.UnspentCutlass], [InventoryType.CutlassEndurance]),13: ([InventoryType.UnspentCutlass], []),14: ([InventoryType.UnspentCutlass], [InventoryType.CutlassTaunt]),15: ([InventoryType.UnspentCutlass], []),16: ([InventoryType.UnspentCutlass], []),17: ([InventoryType.UnspentCutlass], [InventoryType.CutlassStab]),18: ([InventoryType.UnspentCutlass], []),19: ([InventoryType.UnspentCutlass], []),20: ([InventoryType.UnspentCutlass], [InventoryType.CutlassBladestorm]),21: ([InventoryType.UnspentCutlass], []),22: ([InventoryType.UnspentCutlass], []),23: ([InventoryType.UnspentCutlass], []),24: ([InventoryType.UnspentCutlass], []),25: ([InventoryType.UnspentCutlass], []),26: ([InventoryType.UnspentCutlass], []),27: ([InventoryType.UnspentCutlass], []),28: ([InventoryType.UnspentCutlass], []),29: ([InventoryType.UnspentCutlass], []),30: ([InventoryType.UnspentCutlass], [])},InventoryType.DaggerRep: {0: ([], [InventoryType.DaggerCut, InventoryType.DaggerSwipe]),2: ([InventoryType.UnspentDagger], [InventoryType.DaggerAsp]),3: ([InventoryType.UnspentDagger], []),4: ([InventoryType.UnspentDagger], [InventoryType.DaggerAdder]),5: ([InventoryType.UnspentDagger], []),6: ([InventoryType.UnspentDagger], [InventoryType.DaggerThrowDirt]),7: ([InventoryType.UnspentDagger], []),8: ([InventoryType.UnspentDagger], [InventoryType.DaggerGouge]),9: ([InventoryType.UnspentDagger], []),10: ([InventoryType.UnspentDagger], [InventoryType.DaggerFinesse]),11: ([InventoryType.UnspentDagger], []),12: ([InventoryType.UnspentDagger], [InventoryType.DaggerSidewinder]),13: ([InventoryType.UnspentDagger], []),14: ([InventoryType.UnspentDagger], [InventoryType.DaggerEviscerate]),15: ([InventoryType.UnspentDagger], []),16: ([InventoryType.UnspentDagger], []),17: ([InventoryType.UnspentDagger], [InventoryType.DaggerViperNest]),18: ([InventoryType.UnspentDagger], []),19: ([InventoryType.UnspentDagger], []),20: ([InventoryType.UnspentDagger], [InventoryType.DaggerBladeInstinct]),21: ([InventoryType.UnspentDagger], []),22: ([InventoryType.UnspentDagger], []),23: ([InventoryType.UnspentDagger], []),24: ([InventoryType.UnspentDagger], []),25: ([InventoryType.UnspentDagger], []),26: ([InventoryType.UnspentDagger], []),27: ([InventoryType.UnspentDagger], []),28: ([InventoryType.UnspentDagger], []),29: ([InventoryType.UnspentDagger], []),30: ([InventoryType.UnspentDagger], [])},InventoryType.PistolRep: {0: ([], [InventoryType.PistolShoot, InventoryType.PistolLeadShot]),2: ([InventoryType.UnspentPistol], [InventoryType.PistolVenomShot]),3: ([InventoryType.UnspentPistol], []),4: ([InventoryType.UnspentPistol], [InventoryType.PistolTakeAim]),5: ([InventoryType.UnspentPistol], []),6: ([InventoryType.UnspentPistol], [InventoryType.PistolBaneShot]),7: ([InventoryType.UnspentPistol], []),8: ([InventoryType.UnspentPistol], [InventoryType.PistolSharpShooter]),9: ([InventoryType.UnspentPistol], []),10: ([InventoryType.UnspentPistol], [InventoryType.PistolHexEaterShot]),11: ([InventoryType.UnspentPistol], []),12: ([InventoryType.UnspentPistol], [InventoryType.PistolDodge]),13: ([InventoryType.UnspentPistol], []),14: ([InventoryType.UnspentPistol], [InventoryType.PistolEagleEye]),15: ([InventoryType.UnspentPistol], []),16: ([InventoryType.UnspentPistol], []),17: ([InventoryType.UnspentPistol], [InventoryType.PistolSilverShot]),18: ([InventoryType.UnspentPistol], []),19: ([InventoryType.UnspentPistol], []),20: ([InventoryType.UnspentPistol], [InventoryType.PistolSteelShot]),21: ([InventoryType.UnspentPistol], []),22: ([InventoryType.UnspentPistol], []),23: ([InventoryType.UnspentPistol], []),24: ([InventoryType.UnspentPistol], []),25: ([InventoryType.UnspentPistol], []),26: ([InventoryType.UnspentPistol], []),27: ([InventoryType.UnspentPistol], []),28: ([InventoryType.UnspentPistol], []),29: ([InventoryType.UnspentPistol], []),30: ([InventoryType.UnspentPistol], [])},InventoryType.GrenadeRep: {0: ([], [InventoryType.GrenadeThrow, InventoryType.GrenadeExplosion]),2: ([InventoryType.UnspentGrenade], [InventoryType.GrenadeShockBomb]),3: ([InventoryType.UnspentGrenade], []),4: ([InventoryType.UnspentGrenade], [InventoryType.GrenadeLongVolley]),5: ([InventoryType.UnspentGrenade], []),6: ([InventoryType.UnspentGrenade], [InventoryType.GrenadeDetermination]),7: ([InventoryType.UnspentGrenade], []),8: ([InventoryType.UnspentGrenade], [InventoryType.GrenadeFireBomb]),9: ([InventoryType.UnspentGrenade], []),10: ([InventoryType.UnspentGrenade], [InventoryType.GrenadeDemolitions]),11: ([InventoryType.UnspentGrenade], []),12: ([InventoryType.UnspentGrenade], [InventoryType.GrenadeSmokeCloud]),13: ([InventoryType.UnspentGrenade], []),14: ([InventoryType.UnspentGrenade], [InventoryType.GrenadeToughness]),15: ([InventoryType.UnspentGrenade], []),16: ([InventoryType.UnspentGrenade], []),17: ([InventoryType.UnspentGrenade], [InventoryType.GrenadeIgnorePain]),18: ([InventoryType.UnspentGrenade], []),19: ([InventoryType.UnspentGrenade], []),20: ([InventoryType.UnspentGrenade], [InventoryType.GrenadeSiege]),21: ([InventoryType.UnspentGrenade], []),22: ([InventoryType.UnspentGrenade], []),23: ([InventoryType.UnspentGrenade], []),24: ([InventoryType.UnspentGrenade], []),25: ([InventoryType.UnspentGrenade], []),26: ([InventoryType.UnspentGrenade], []),27: ([InventoryType.UnspentGrenade], []),28: ([InventoryType.UnspentGrenade], []),29: ([InventoryType.UnspentGrenade], []),30: ([InventoryType.UnspentGrenade], [])},InventoryType.DollRep: {0: ([], [InventoryType.DollAttune, InventoryType.DollPoke]),2: ([InventoryType.UnspentDoll], [InventoryType.DollSwarm]),3: ([InventoryType.UnspentDoll], []),4: ([InventoryType.UnspentDoll], [InventoryType.DollHeal]),5: ([InventoryType.UnspentDoll], []),6: ([InventoryType.UnspentDoll], [InventoryType.DollCurse]),7: ([InventoryType.UnspentDoll], []),8: ([InventoryType.UnspentDoll], [InventoryType.DollBurn]),9: ([InventoryType.UnspentDoll], []),10: ([InventoryType.UnspentDoll], [InventoryType.DollFocus]),11: ([InventoryType.UnspentDoll], []),12: ([InventoryType.UnspentDoll], [InventoryType.DollCure]),13: ([InventoryType.UnspentDoll], []),14: ([InventoryType.UnspentDoll], [InventoryType.DollSpiritWard]),15: ([InventoryType.UnspentDoll], []),16: ([InventoryType.UnspentDoll], []),17: ([InventoryType.UnspentDoll], [InventoryType.DollShackles]),18: ([InventoryType.UnspentDoll], []),19: ([InventoryType.UnspentDoll], []),20: ([InventoryType.UnspentDoll], [InventoryType.DollLifeDrain]),21: ([InventoryType.UnspentDoll], []),22: ([InventoryType.UnspentDoll], []),23: ([InventoryType.UnspentDoll], []),24: ([InventoryType.UnspentDoll], []),25: ([InventoryType.UnspentDoll], []),26: ([InventoryType.UnspentDoll], []),27: ([InventoryType.UnspentDoll], []),28: ([InventoryType.UnspentDoll], []),29: ([InventoryType.UnspentDoll], []),30: ([InventoryType.UnspentDoll], [])},InventoryType.WandRep: {0: ([], [InventoryType.StaffBlast, InventoryType.StaffSoulFlay]),2: ([InventoryType.UnspentWand], [InventoryType.StaffPestilence]),3: ([InventoryType.UnspentWand], []),4: ([InventoryType.UnspentWand], [InventoryType.StaffWither]),5: ([InventoryType.UnspentWand], []),6: ([InventoryType.UnspentWand], [InventoryType.StaffConcentration]),7: ([InventoryType.UnspentWand], []),8: ([InventoryType.UnspentWand], [InventoryType.StaffSpiritLore]),9: ([InventoryType.UnspentWand], []),10: ([InventoryType.UnspentWand], [InventoryType.StaffHellfire]),11: ([InventoryType.UnspentWand], []),12: ([InventoryType.UnspentWand], [InventoryType.StaffConservation]),13: ([InventoryType.UnspentWand], []),14: ([InventoryType.UnspentWand], [InventoryType.StaffBanish]),15: ([InventoryType.UnspentWand], []),16: ([InventoryType.UnspentWand], []),17: ([InventoryType.UnspentWand], [InventoryType.StaffSpiritMastery]),18: ([InventoryType.UnspentWand], []),19: ([InventoryType.UnspentWand], []),20: ([InventoryType.UnspentWand], [InventoryType.StaffDesolation]),21: ([InventoryType.UnspentWand], []),22: ([InventoryType.UnspentWand], []),23: ([InventoryType.UnspentWand], []),24: ([InventoryType.UnspentWand], []),25: ([InventoryType.UnspentWand], []),26: ([InventoryType.UnspentWand], []),27: ([InventoryType.UnspentWand], []),28: ([InventoryType.UnspentWand], []),29: ([InventoryType.UnspentWand], []),30: ([InventoryType.UnspentWand], [])},InventoryType.CannonRep: {0: ([], [InventoryType.CannonShoot, InventoryType.CannonRoundShot]),2: ([InventoryType.UnspentCannon], [InventoryType.CannonChainShot]),3: ([InventoryType.UnspentCannon], []),4: ([InventoryType.UnspentCannon], [InventoryType.CannonGrapeShot]),5: ([InventoryType.UnspentCannon], []),6: ([InventoryType.UnspentCannon], [InventoryType.CannonRapidReload]),7: ([InventoryType.UnspentCannon], []),8: ([InventoryType.UnspentCannon], [InventoryType.CannonFirebrand]),9: ([InventoryType.UnspentCannon], []),10: ([InventoryType.UnspentCannon], [InventoryType.CannonBarrage]),11: ([InventoryType.UnspentCannon], []),12: ([InventoryType.UnspentCannon], [InventoryType.CannonThunderbolt]),13: ([InventoryType.UnspentCannon], []),14: ([InventoryType.UnspentCannon], [InventoryType.CannonShrapnel]),15: ([InventoryType.UnspentCannon], []),16: ([InventoryType.UnspentCannon], []),17: ([InventoryType.UnspentCannon], [InventoryType.CannonExplosive]),18: ([InventoryType.UnspentCannon], []),19: ([InventoryType.UnspentCannon], []),20: ([InventoryType.UnspentCannon], [InventoryType.CannonFury]),21: ([InventoryType.UnspentCannon], []),22: ([InventoryType.UnspentCannon], []),23: ([InventoryType.UnspentCannon], []),24: ([InventoryType.UnspentCannon], []),25: ([InventoryType.UnspentCannon], []),26: ([InventoryType.UnspentCannon], []),27: ([InventoryType.UnspentCannon], []),28: ([InventoryType.UnspentCannon], []),29: ([InventoryType.UnspentCannon], []),30: ([InventoryType.UnspentCannon], [])},InventoryType.SailingRep: {0: ([], [InventoryType.SailBroadsideLeft, InventoryType.SailBroadsideRight]),2: ([InventoryType.UnspentSailing], [InventoryType.SailFullSail]),3: ([InventoryType.UnspentSailing], []),4: ([InventoryType.UnspentSailing], [InventoryType.SailComeAbout]),5: ([InventoryType.UnspentSailing], []),6: ([InventoryType.UnspentSailing], [InventoryType.SailWindcatcher]),7: ([InventoryType.UnspentSailing], []),8: ([InventoryType.UnspentSailing], [InventoryType.SailTacking]),9: ([InventoryType.UnspentSailing], []),10: ([InventoryType.UnspentSailing], [InventoryType.SailOpenFire]),11: ([InventoryType.UnspentSailing], []),12: ([InventoryType.UnspentSailing], [InventoryType.SailRammingSpeed]),13: ([InventoryType.UnspentSailing], []),14: ([InventoryType.UnspentSailing], [InventoryType.SailTreasureSense]),15: ([InventoryType.UnspentSailing], []),16: ([InventoryType.UnspentSailing], []),17: ([InventoryType.UnspentSailing], [InventoryType.SailTaskmaster]),18: ([InventoryType.UnspentSailing], []),19: ([InventoryType.UnspentSailing], []),20: ([InventoryType.UnspentSailing], [InventoryType.SailTakeCover]),21: ([InventoryType.UnspentSailing], []),22: ([InventoryType.UnspentSailing], []),23: ([InventoryType.UnspentSailing], []),24: ([InventoryType.UnspentSailing], []),25: ([InventoryType.UnspentSailing], []),26: ([InventoryType.UnspentSailing], []),27: ([InventoryType.UnspentSailing], []),28: ([InventoryType.UnspentSailing], []),29: ([InventoryType.UnspentSailing], []),30: ([InventoryType.UnspentSailing], [])}}

def getLevelUpSkills(rep, level):
    repChart = __levelUpSkills.get(rep)
    if repChart:
        skills = repChart.get(level)
        if skills:
            return skills
    return ([], [])


__skill2Level = {}
for repData in __levelUpSkills.values():
    for level, unlocks in repData.items():
        for skillList in unlocks:
            for skillId in skillList:
                if InventoryType.begin_Unspent <= skillId <= InventoryType.end_Unspent:
                    continue
                __skill2Level[skillId] = level

def getSkillUnlockLevel(skillId):
    return __skill2Level.get(skillId, -1)