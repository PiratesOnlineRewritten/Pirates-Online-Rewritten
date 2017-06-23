from pandac.PandaModules import TransformState, Vec3
OCEAN_GRID_SIZE = 60
OCEAN_CELL_SIZE = 2000
OCEAN_GRID_RADIUS = 3
OCEAN_GRID_STARTING_ZONE = 500
LARGE_ISLAND_GRID_SIZE = 80
MED_ISLAND_GRID_SIZE = 40
ISLAND_GRID_SIZE = 20
ISLAND_CELL_SIZE = 75
ISLAND_PVP_CELL_SIZE = 32000
ISLAND_TM_CELL_SIZE = 3200
ISLAND_GRID_RADIUS = 2
ISLAND_PVP_GRID_RADIUS = 5
ISLAND_TM_GRID_RADIUS = 5
ISLAND_GRID_STARTING_ZONE = 500
GAME_AREA_INTERIOR_CELL_SIZE = 150
GAME_AREA_INTERIOR_GRID_SIZE = 20
GAME_AREA_INTERIOR_GRID_RADIUS = 2
GAME_AREA_INTERIOR_STARTING_ZONE = 2500
GAME_AREA_CELL_SIZE = 150
GAME_AREA_GRID_SIZE = 20
GAME_AREA_GRID_RADIUS = 2
GAME_AREA_STARTING_ZONE = 500
EXTERIOR_TUNNEL_ZONE = 200
GAME_AREA_PVP_CELL_SIZE = 2000
GAME_AREA_PVP_GRID_SIZE = 10
GAME_AREA_PVP_GRID_RADIUS = 2
PiratesWorldSceneFileBase = config.GetString('default-world', 'piratesWorld')
PiratesWorldSceneFile = PiratesWorldSceneFileBase + '.py'
PiratesTutorialSceneFileBase = config.GetString('tutorial-world', 'RambleshackWorld')
PiratesTutorialSceneFile = PiratesTutorialSceneFileBase + '.py'
IslandSceneFiles = {'Port Royale': 'PortRoyale.scene.py','Cuba': 'Cuba.scene.py'}
OCEAN = 1
ISLAND = 2
TOWN = 3
BUILDING = 4
PORT = 5
GAMEAREA = 6
SHIP = 7
SPOT = 8
CARIBBEAN_SEA = 1
SHIPWRECK_SOUND = 2
SIR_JOHNS_TRENCH = 3
SERPENT_TRIANGLE = 4
STRAIGHT_OF_GOLD = 5
BLADE_BAY = 6
GULF_OF_SUN = 7
GULF_OF_MOON = 8
GULF_OF_LIFE = 9
GULF_OF_DEATH = 10
RAMBLESHACK = 101
BILGEWATER = 102
TORTUGA = 103
PORT_ROYAL = 104
KINGSHEAD = 105
PADRE_DEL_FUEGO = 106
MADRE_DEL_FUEGO = 107
ESCARGOTS = 108
PUERTO_NUEVO = 109
THE_ROCK = 1001
RAMBLESHACK_T = 2001
BILGEWATER_T = 2002
TORTUGA_T = 2003
PORT_ROYAL_T = 2004
KINGSHEAD_T = 2005
PADRE_DEL_FUEGO_T = 2006
MADRE_DEL_FUEGO_T = 2007
ESCARGOTS_T = 2008
PUERTO_NUEVO_T = 2009
BLACKSMITH = 2001
HALL_OF_CARDS = 2002
HOLLOWED_WOODS = 3001
__locationNames = {'PortRoyal': PORT_ROYAL,'Bilgewater': BILGEWATER,'TheRock': THE_ROCK}
__islandNametagHeight = {'Padres Del Fuego': 1200,'Port Royal': 1300,'Tortuga': 800,'Isla Cangrejos': 400,'Kingshead': 500,'Cuba': 400,"Rumrunner's Isle": 200,"Devil's Anvil": 700,'Outcast Isle': 200,'Isla Perdida': 800,'Driftwood Island': 200,'Isla Tormenta': 200,'Cutthroat Isle': 500,"Raven's Cove": 700}

def getNametagHeight(name):
    return __islandNametagHeight.get(name, 200)


def getNametagScale(name):
    return 35.0


ObjectAnimRates = {'Default': [0.8, 1.0],'models/vegetation/tree_b_leaf_idle': [0.4, 0.7]}
ObjectAnimRates_new = {'Default': [0.8, 1.0],'tree_b': [0.4, 0.7]}

def getLocationValue(name):
    return __locationNames.get(name)


class OceanZone():
    UNCHARTED_WATERS = (0, )
    BRIGAND_BAY = (1, )
    BLOODY_BAYOU = (2, )
    SCURVY_SHALLOWS = (3, )
    BLACKHEART_STRAIGHT = (4, )
    WINDWARD_PASSAGE = (5, )
    SALTY_FLATS = (6, )
    MAR_DE_PLATA = (7, )
    SMUGGLERS_RUN = (8, )
    LEEWARD_PASSAGE = (9, )
    DEAD_MANS_TROUGH = (10, )
    MARINERS_REEF = (11, )
    BOILING_BAY = (12, )
    THE_HINTER_SEAS = (13, )


def getOceanZone(xc, yc):
    xcoord = xc / 2000
    ycoord = yc / 2000
    if xcoord >= -15 and xcoord < -7 and ycoord >= 4 and ycoord < 11:
        return OceanZone.BRIGAND_BAY
    elif xcoord >= -15 and xcoord < -7 and ycoord >= 0 and ycoord < 4:
        return OceanZone.BLOODY_BAYOU
    elif xcoord >= -7 and xcoord < -2 and ycoord >= 0 and ycoord < 11:
        return OceanZone.SCURVY_SHALLOWS
    elif xcoord >= 6 and xcoord < 13 and ycoord >= 8 and ycoord < 14:
        return OceanZone.SALTY_FLATS
    elif xcoord >= -2 and xcoord < 6 and ycoord >= 10 and ycoord < 14:
        return OceanZone.BLACKHEART_STRAIGHT
    elif xcoord >= -2 and xcoord < 2 and ycoord >= 8 and ycoord < 10:
        return OceanZone.BLACKHEART_STRAIGHT
    elif xcoord >= -2 and xcoord < 6 and ycoord >= -1 and ycoord < 10:
        return OceanZone.WINDWARD_PASSAGE
    elif xcoord >= 6 and xcoord < 13 and ycoord >= -1 and ycoord < 8:
        return OceanZone.MAR_DE_PLATA
    elif xcoord >= 9 and xcoord < 13 and ycoord >= -4 and ycoord < -1:
        return OceanZone.MAR_DE_PLATA
    elif xcoord >= 11 and xcoord < 13 and ycoord >= -6 and ycoord < -4:
        return OceanZone.MAR_DE_PLATA
    elif xcoord >= 1 and xcoord < 11 and ycoord >= -8 and ycoord < -1:
        return OceanZone.SMUGGLERS_RUN
    elif xcoord >= 7 and xcoord < 13 and ycoord >= -15 and ycoord < -6:
        return OceanZone.THE_HINTER_SEAS
    elif xcoord >= -8 and xcoord < 7 and ycoord >= -15 and ycoord < -12:
        return OceanZone.MARINERS_REEF
    elif xcoord >= 1 and xcoord < 7 and ycoord >= -12 and ycoord < -8:
        return OceanZone.BOILING_BAY
    elif xcoord >= -15 and xcoord < -6 and ycoord >= -8 and ycoord < 0:
        return OceanZone.DEAD_MANS_TROUGH
    elif xcoord >= -8 and xcoord < 1 and ycoord >= -12 and ycoord < 0:
        return OceanZone.LEEWARD_PASSAGE
    else:
        return OceanZone.UNCHARTED_WATERS


class LevelObject():

    def __init__(self, uniqueId, data):
        self.uniqueId = uniqueId
        self.data = data
        pos = data.get('Pos', Vec3(0, 0, 0))
        hpr = data.get('Hpr', Vec3(0, 0, 0))
        scale = data.get('Scale', Vec3(1, 1, 1))
        self.transform = TransformState.makePosHprScale(pos, hpr, scale)

    def __repr__(self):
        return '%s(%s): %s' % (self.data['Type'], self.uniqueId, self.data)

    def __getitem__(self, key):
        return self.data[key]

    def get(self, key, default=None):
        return self.data.get(key, default)