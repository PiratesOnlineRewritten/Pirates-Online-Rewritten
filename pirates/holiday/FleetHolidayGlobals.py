from pirates.ai.HolidayDates import *
from pirates.ship import ShipGlobals

class Squadrons():
    Leader_Eitc = (
     1, [ShipGlobals.EITC_INTREPID, ShipGlobals.EITC_CONQUERER, ShipGlobals.EITC_LEVIATHAN])
    Leader_Navy = (1, [ShipGlobals.HMS_VICTORY, ShipGlobals.HMS_NEWCASTLE, ShipGlobals.HMS_INVINCIBLE])
    Quad_Eitc = (4, [ShipGlobals.EITC_TYRANT])
    Quad_Navy = (4, [ShipGlobals.NAVY_ELITE])
    Duo_Eitc_Hard = (2, [ShipGlobals.EITC_JUGGERNAUT])
    Duo_Navy_Hard = (2, [ShipGlobals.NAVY_DREADNOUGHT])
    Duo_Eitc_Med = (2, [ShipGlobals.EITC_WARLORD])
    Duo_Navy_Med = (2, [ShipGlobals.NAVY_MAN_O_WAR])
    Warships = (4, [ShipGlobals.WARSHIPL2, ShipGlobals.WARSHIPL3])


class Fleets():
    Lite_Eitc = [
     Squadrons.Leader_Eitc]
    Lite_Navy = [Squadrons.Leader_Navy]
    Med_Eitc = [Squadrons.Leader_Eitc, Squadrons.Quad_Eitc]
    Med_Navy = [Squadrons.Leader_Navy, Squadrons.Quad_Navy]
    Test_Kraken = [Squadrons.Warships]


class Paths():
    TestMidCApproachingPortRoyal = '1264196992.0kanpatel0'
    FromKingshead = '1264194816.0kanpatel'
    FromPadres = '1264195968.0kanpatel'
    FromTheEast = '1264196864.0kanpatel'
    FromTheSouthWest = '1264197376.0kanpatel'
    FromTheSouth = '1264198016.0kanpatel'
    FromTheWest = '1264198272.0kanpatel'


class Msgs():
    EF_EitcLaunch = 30
    EF_EitcEscaped = 31
    EF_EitcDefeated = 32
    EF_NavyLaunch = 33
    EF_NavyEscaped = 34
    EF_NavyDefeated = 35
    TF_EitcLaunch = 36
    TF_EitcEscaped = 37
    TF_EitcDefeated = 38
    TF_NavyLaunch = 39
    TF_NavyEscaped = 40
    TF_NavyDefeated = 41
    TF_EitcWarn10min = 42
    TF_EitcWarn5min = 43
    TF_EitcWarn0min = 44
    TF_NavyWarn10min = 45
    TF_NavyWarn5min = 46
    TF_NavyWarn0min = 47


class Configs():
    EF_EITC_RAND_KH_P_E = 7
    EF_EITC_RAND_SW_S_W = 8
    EF_EITC_RAND_KH_P_E_SW_S_W = 9
    EF_NAVY_RAND_KH_P_E = 27
    EF_NAVY_RAND_SW_S_W = 28
    EF_NAVY_RAND_KH_P_E_SW_S_W = 29
    TF_EITC_RAND_KH_P_E = 37
    TF_EITC_RAND_SW_S_W = 38
    TF_EITC_RAND_KH_P_E_SW_S_W = 39
    TF_NAVY_RAND_KH_P_E = 47
    TF_NAVY_RAND_SW_S_W = 48
    TF_NAVY_RAND_KH_P_E_SW_S_W = 49
    TEST_KRAKEN = 98
    TEST = 99


FleetHolidayConfigs = {
    Configs.EF_EITC_RAND_KH_P_E: {
            'id': Configs.EF_EITC_RAND_KH_P_E,
            'name': 'Expedition Fleet (EITC, KH/P/E)',
            'team': ShipGlobals.TRADING_CO_TEAM,
            'fleet': Fleets.Med_Eitc,
            'pathId': [Paths.FromKingshead, Paths.FromPadres, Paths.FromTheEast],
            'formation': ShipGlobals.FORMATION_ARROW,
            'launchMsg': Msgs.EF_EitcLaunch,
            'escapedMsg': Msgs.EF_EitcEscaped,
            'defeatedMsg': Msgs.EF_EitcDefeated,
            'dates': HolidayDates(HolidayDates.TYPE_CUSTOM, [
                (2010, Month.MARCH, 11, 12, 0, 0), 
                (2010, Month.MARCH, 11, 13, 45, 0),
                (2010, Month.MARCH, 11, 15, 0, 0), 
                (2010, Month.MARCH, 11, 16, 45, 0), 
                (2010, Month.MARCH, 11, 17, 0, 0), 
                (2010, Month.MARCH, 11, 18, 45, 0), 
                (2010, Month.MARCH, 11, 20, 0, 0), 
                (2010, Month.MARCH, 11, 21, 45, 0), 
                (2010, Month.MARCH, 12, 13, 0, 0), 
                (2010, Month.MARCH, 12, 14, 45, 0), 
                (2010, Month.MARCH, 12, 15, 0, 0), 
                (2010, Month.MARCH, 12, 16, 45, 0), 
                (2010, Month.MARCH, 12, 17, 0, 0), 
                (2010, Month.MARCH, 12, 18, 45, 0), 
                (2010, Month.MARCH, 12, 20, 0, 0), 
                (2010, Month.MARCH, 12, 21, 45, 0), 
                (2010, Month.MARCH, 12, 22, 0, 0), 
                (2010, Month.MARCH, 12, 23, 45, 0), 
                (2010, Month.MARCH, 13, 10, 0, 0), 
                (2010, Month.MARCH, 13, 11, 45, 0), 
                (2010, Month.MARCH, 13, 12, 0, 0), 
                (2010, Month.MARCH, 13, 13, 45, 0), 
                (2010, Month.MARCH, 13, 15, 0, 0), 
                (2010, Month.MARCH, 13, 16, 45, 0), 
                (2010, Month.MARCH, 13, 18, 0, 0), 
                (2010, Month.MARCH, 13, 19, 45, 0), 
                (2010, Month.MARCH, 13, 21, 0, 0), 
                (2010, Month.MARCH, 13, 22, 45, 0), 
                (2010, Month.MARCH, 14, 10, 0, 0), 
                (2010, Month.MARCH, 14, 11, 45, 0), 
                (2010, Month.MARCH, 14, 13, 0, 0), 
                (2010, Month.MARCH, 14, 14, 45, 0), 
                (2010, Month.MARCH, 14, 15, 0, 0), 
                (2010, Month.MARCH, 14, 16, 45, 0), 
                (2010, Month.MARCH, 14, 18, 0, 0), 
                (2010, Month.MARCH, 14, 19, 45, 0), 
                (2010, Month.MARCH, 14, 20, 0, 0), 
                (2010, Month.MARCH, 14, 21, 45, 0), 
                (2010, Month.MARCH, 15, 13, 0, 0), 
                (2010, Month.MARCH, 15, 14, 45, 0), 
                (2010, Month.MARCH, 15, 16, 0, 0), 
                (2010, Month.MARCH, 15, 17, 45, 0), 
                (2010, Month.MARCH, 15, 19, 0, 0), 
                (2010, Month.MARCH, 15, 20, 45, 0), 
                (2010, Month.MARCH, 15, 21, 0, 0), 
                (2010, Month.MARCH, 15, 22, 45, 0), 
                (2010, Month.MARCH, 19, 13, 0, 0), 
                (2010, Month.MARCH, 19, 14, 45, 0), 
                (2010, Month.MARCH, 19, 15, 0, 0), 
                (2010, Month.MARCH, 19, 16, 45, 0), 
                (2010, Month.MARCH, 19, 17, 0, 0), 
                (2010, Month.MARCH, 19, 18, 45, 0), 
                (2010, Month.MARCH, 19, 20, 0, 0), 
                (2010, Month.MARCH, 19, 21, 45, 0), 
                (2010, Month.MARCH, 19, 22, 0, 0),
                (2010, Month.MARCH, 19, 23, 45, 0), 
                (2010, Month.MARCH, 20, 10, 0, 0),
                (2010, Month.MARCH, 20, 11, 45, 0), 
                (2010, Month.MARCH, 20, 12, 0, 0),
                (2010, Month.MARCH, 20, 13, 45, 0), 
                (2010, Month.MARCH, 20, 15, 0, 0),
                (2010, Month.MARCH, 20, 16, 45, 0), 
                (2010, Month.MARCH, 20, 19, 0, 0),
                (2010, Month.MARCH, 20, 20, 45, 0), 
                (2010, Month.MARCH, 20, 22, 0, 0), 
                (2010, Month.MARCH, 20, 23, 45, 0),
                (2010, Month.MARCH, 21, 7, 0, 0), 
                (2010, Month.MARCH, 21, 8, 45, 0), 
                (2010, Month.MARCH, 21, 10, 0, 0), 
                (2010, Month.MARCH, 21, 11, 45, 0), 
                (2010, Month.MARCH, 21, 13, 0, 0), 
                (2010, Month.MARCH, 21, 14, 45, 0), 
                (2010, Month.MARCH, 21, 15, 0, 0), 
                (2010, Month.MARCH, 21, 16, 45, 0), 
                (2010, Month.MARCH, 21, 19, 0, 0), 
                (2010, Month.MARCH, 21, 20, 45, 0), 
                (2010, Month.MARCH, 21, 22, 0, 0), 
                (2010, Month.MARCH, 21, 23, 45, 0), 
                (2010, Month.MARCH, 22, 13, 0, 0), 
                (2010, Month.MARCH, 22, 14, 45, 0), 
                (2010, Month.MARCH, 22, 16, 0, 0), 
                (2010, Month.MARCH, 22, 17, 45, 0), 
                (2010, Month.MARCH, 22, 19, 0, 0), 
                (2010, Month.MARCH, 22, 20, 45, 0), 
                (2010, Month.MARCH, 22, 21, 0, 0), 
                (2010, Month.MARCH, 22, 22, 45, 0)
            ])
        },
        Configs.EF_EITC_RAND_SW_S_W: {
            'id': Configs.EF_EITC_RAND_SW_S_W,
            'name': 'Expedition Fleet (EITC, SW/S/W)',
            'team': ShipGlobals.TRADING_CO_TEAM,
            'fleet': Fleets.Med_Eitc,
            'pathId': [Paths.FromTheSouthWest, Paths.FromTheSouth, Paths.FromTheWest],
            'formation': ShipGlobals.FORMATION_ARROW,
            'launchMsg': Msgs.EF_EitcLaunch,
            'escapedMsg': Msgs.EF_EitcEscaped,
            'defeatedMsg': Msgs.EF_EitcDefeated
        }, Configs.EF_EITC_RAND_KH_P_E_SW_S_W: {
            'id': Configs.EF_EITC_RAND_KH_P_E_SW_S_W,
            'name': 'Expedition Fleet (EITC, KH/P/E/SW/S/W)',
            'team': ShipGlobals.TRADING_CO_TEAM,
            'fleet': Fleets.Med_Eitc,
            'pathId': [Paths.FromKingshead, Paths.FromPadres, Paths.FromTheEast, Paths.FromTheSouthWest, Paths.FromTheSouth, Paths.FromTheWest],
            'formation': ShipGlobals.FORMATION_ARROW,
            'launchMsg': Msgs.EF_EitcLaunch,
            'escapedMsg': Msgs.EF_EitcEscaped,
            'defeatedMsg': Msgs.EF_EitcDefeated
        }, Configs.EF_NAVY_RAND_KH_P_E: {
            'id': Configs.EF_NAVY_RAND_KH_P_E,
            'name': 'Expedition Fleet (Navy, KH/P/E)',
            'team': ShipGlobals.NAVY_TEAM,
            'fleet': Fleets.Med_Navy,
            'pathId': [Paths.FromKingshead, Paths.FromPadres, Paths.FromTheEast],
            'formation': ShipGlobals.FORMATION_ARROW,
            'launchMsg': Msgs.EF_NavyLaunch,
            'escapedMsg': Msgs.EF_NavyEscaped,
            'defeatedMsg': Msgs.EF_NavyDefeated
        }, Configs.EF_NAVY_RAND_SW_S_W: {
            'id': Configs.EF_NAVY_RAND_SW_S_W,
            'name': 'Expedition Fleet (Navy, SW/S/W)',
            'team': ShipGlobals.NAVY_TEAM,
            'fleet': Fleets.Med_Navy,
            'pathId': [Paths.FromTheSouthWest, Paths.FromTheSouth, Paths.FromTheWest],
            'formation': ShipGlobals.FORMATION_ARROW,
            'launchMsg': Msgs.EF_NavyLaunch,
            'escapedMsg': Msgs.EF_NavyEscaped,
            'defeatedMsg': Msgs.EF_NavyDefeated
        }, Configs.EF_NAVY_RAND_KH_P_E_SW_S_W: {
            'id': Configs.EF_NAVY_RAND_KH_P_E_SW_S_W,
            'name': 'Expedition Fleet (Navy, KH/P/E/SW/S/W)',
            'team': ShipGlobals.NAVY_TEAM,
            'fleet': Fleets.Med_Navy,
            'pathId': [Paths.FromKingshead, Paths.FromPadres, Paths.FromTheEast, Paths.FromTheSouthWest, Paths.FromTheSouth, Paths.FromTheWest],
            'formation': ShipGlobals.FORMATION_ARROW,
            'launchMsg': Msgs.EF_NavyLaunch,
            'escapedMsg': Msgs.EF_NavyEscaped,
            'defeatedMsg': Msgs.EF_NavyDefeated
        }, Configs.TF_EITC_RAND_KH_P_E: {
            'id': Configs.TF_EITC_RAND_KH_P_E,
            'name': 'Treasure Fleet (EITC, KH/P/E)',
            'team': ShipGlobals.TRADING_CO_TEAM,
            'fleet': Fleets.Med_Eitc,
            'pathId': [Paths.FromKingshead, Paths.FromPadres, Paths.FromTheEast],
            'formation': ShipGlobals.FORMATION_ARROW,
            'countdown': [(Msgs.TF_EitcWarn10min, 5), (Msgs.TF_EitcWarn5min, 5)],
            'launchMsg': Msgs.TF_EitcWarn0min,
            'escapedMsg': Msgs.TF_EitcEscaped,
            'defeatedMsg': Msgs.TF_EitcDefeated
        }, Configs.TF_EITC_RAND_SW_S_W: {
            'id': Configs.TF_EITC_RAND_SW_S_W,
            'name': 'Treasure Fleet (EITC, SW/S/W)',
            'team': ShipGlobals.TRADING_CO_TEAM,
            'fleet': Fleets.Med_Eitc,
            'pathId': [Paths.FromTheSouthWest, Paths.FromTheSouth, Paths.FromTheWest],
            'formation': ShipGlobals.FORMATION_ARROW,
            'countdown': [(Msgs.TF_EitcWarn10min, 5), (Msgs.TF_EitcWarn5min, 5)],
            'launchMsg': Msgs.TF_EitcWarn0min,
            'escapedMsg': Msgs.TF_EitcEscaped,
            'defeatedMsg': Msgs.TF_EitcDefeated
        }, Configs.TF_EITC_RAND_KH_P_E_SW_S_W: {
            'id': Configs.TF_EITC_RAND_KH_P_E_SW_S_W,
            'name': 'Treasure Fleet (EITC, KH/P/E/SW/S/W)',
            'team': ShipGlobals.TRADING_CO_TEAM,
            'fleet': Fleets.Med_Eitc,
            'pathId': [Paths.FromKingshead, Paths.FromPadres, Paths.FromTheEast, Paths.FromTheSouthWest, Paths.FromTheSouth, Paths.FromTheWest],
            'formation': ShipGlobals.FORMATION_ARROW,
            'countdown': [(Msgs.TF_EitcWarn10min, 5), (Msgs.TF_EitcWarn5min, 5)],
            'launchMsg': Msgs.TF_EitcWarn0min,
            'escapedMsg': Msgs.TF_EitcEscaped,
            'defeatedMsg': Msgs.TF_EitcDefeated
        }, Configs.TF_NAVY_RAND_KH_P_E: {
            'id': Configs.TF_NAVY_RAND_KH_P_E,
            'name': 'Treasure Fleet (Navy, KH/P/E)',
            'team': ShipGlobals.NAVY_TEAM,
            'fleet': Fleets.Med_Navy,
            'pathId': [Paths.FromKingshead, Paths.FromPadres, Paths.FromTheEast],
            'formation': ShipGlobals.FORMATION_ARROW,
            'countdown': [(Msgs.TF_NavyWarn10min, 5), (Msgs.TF_NavyWarn5min, 5)],
            'launchMsg': Msgs.TF_NavyWarn0min,
            'escapedMsg': Msgs.TF_NavyEscaped,
            'defeatedMsg': Msgs.TF_NavyDefeated
        }, Configs.TF_NAVY_RAND_SW_S_W: {
            'id': Configs.TF_NAVY_RAND_SW_S_W,
            'name': 'Treasure Fleet (Navy, SW/S/W)',
            'team': ShipGlobals.NAVY_TEAM,
            'fleet': Fleets.Med_Navy,
            'pathId': [Paths.FromTheSouthWest, Paths.FromTheSouth, Paths.FromTheWest],
            'formation': ShipGlobals.FORMATION_ARROW,
            'countdown': [(Msgs.TF_NavyWarn10min, 5), (Msgs.TF_NavyWarn5min, 5)],
            'launchMsg': Msgs.TF_NavyWarn0min,
            'escapedMsg': Msgs.TF_NavyEscaped,
            'defeatedMsg': Msgs.TF_NavyDefeated
        }, Configs.TF_NAVY_RAND_KH_P_E_SW_S_W: {
            'id': Configs.TF_NAVY_RAND_KH_P_E_SW_S_W,
            'name': 'Treasure Fleet (Navy, KH/P/E/SW/S/W)',
            'team': ShipGlobals.NAVY_TEAM,
            'fleet': Fleets.Med_Navy,
            'pathId': [Paths.FromKingshead, Paths.FromPadres, Paths.FromTheEast, Paths.FromTheSouthWest, Paths.FromTheSouth, Paths.FromTheWest],
            'formation': ShipGlobals.FORMATION_ARROW,
            'countdown': [(Msgs.TF_NavyWarn10min, 5), (Msgs.TF_NavyWarn5min, 5)],
            'launchMsg': Msgs.TF_NavyWarn0min,
            'escapedMsg': Msgs.TF_NavyEscaped,
            'defeatedMsg': Msgs.TF_NavyDefeated
        }, Configs.TEST_KRAKEN: {
            'id': Configs.TEST_KRAKEN,
            'name': '(TEST CONFIG) (Eitc, Passing Port Royal)',
            'team': ShipGlobals.TRADING_CO_TEAM,
            'fleet': Fleets.Test_Kraken,
            'pathId': Paths.TestMidCApproachingPortRoyal,
            'formation': ShipGlobals.FORMATION_ARROW,
            'launchMsg': Msgs.TF_EitcLaunch,
            'escapedMsg': Msgs.TF_EitcEscaped,
            'defeatedMsg': Msgs.TF_EitcDefeated
        }, Configs.TEST: {
            'id': Configs.TEST,
            'name': '(TEST CONFIG) (Eitc, Passing Port Royal)',
            'team': ShipGlobals.TRADING_CO_TEAM,
            'fleet': Fleets.Med_Eitc,
            'pathId': Paths.TestMidCApproachingPortRoyal,
            'formation': ShipGlobals.FORMATION_ARROW,
            'countdown': [(Msgs.TF_EitcWarn10min, 0.25), (Msgs.TF_EitcWarn5min, 0.25)],
            'launchMsg': Msgs.TF_EitcWarn0min,
            'escapedMsg': Msgs.TF_EitcEscaped,
            'defeatedMsg': Msgs.TF_EitcDefeated,
            'dates': HolidayDates(HolidayDates.TYPE_CUSTOM, [
                (
                    2010, Month.JANUARY, 29, 19, 2, 0), (2010, Month.JANUARY, 29, 20, 0, 0)
            ])
        }
}