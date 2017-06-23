from pirates.ai.HolidayDates import *

class Msgs():
    Launch = 50
    Escaped = 51
    Defeated = 52


class ConfigIds():
    Test_Maw = 89
    Test_Crush = 92
    Test_Grab = 94
    Test_DDG = 99


KrakenHolidayConfigs = {ConfigIds.Test_Maw: {'id': ConfigIds.Test_Maw,'name': 'Kraken (Maw Test)','launchMsg': Msgs.Launch,'escapedMsg': Msgs.Escaped,'defeatedMsg': Msgs.Defeated},ConfigIds.Test_Crush: {'id': ConfigIds.Test_Crush,'name': 'Kraken (Crush Test)','launchMsg': Msgs.Launch,'escapedMsg': Msgs.Escaped,'defeatedMsg': Msgs.Defeated},ConfigIds.Test_Grab: {'id': ConfigIds.Test_Grab,'name': 'Kraken (Grab Test)','launchMsg': Msgs.Launch,'escapedMsg': Msgs.Escaped,'defeatedMsg': Msgs.Defeated},ConfigIds.Test_DDG: {'id': ConfigIds.Test_DDG,'name': 'Kraken (Duck Duck Goose Test)','launchMsg': Msgs.Launch,'escapedMsg': Msgs.Escaped,'defeatedMsg': Msgs.Defeated}}