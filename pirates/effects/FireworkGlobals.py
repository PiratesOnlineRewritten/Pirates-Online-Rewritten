from pandac.PandaModules import *
from pirates.world.LocationConstants import LocationIds
ShowPosHpr = {LocationIds.PORT_ROYAL_ISLAND: (Point3(-525, 1285, 150), Point3(-20, 0, 0)),LocationIds.TORTUGA_ISLAND: (Point3(10525, 19000, 245), Point3(0, 0, 0)),LocationIds.DEL_FUEGO_ISLAND: (Point3(7900, -25500, 325), Point3(55, 0, 0))}

def getShowPosition(locationId):
    return ShowPosHpr.get(locationId)[0]


def getShowOrientation(locationId):
    return ShowPosHpr.get(locationId)[1]


class FireworkTrailType():
    Default = 0
    Polygonal = 1
    Glow = 2
    Sparkle = 3
    GlowSparkle = 4
    LongSparkle = 5
    LongGlowSparkle = 6


class FireworkBurstType():
    Sparkles = 0
    PeonyShell = 1
    PeonyParticleShell = 2
    PeonyDiademShell = 3
    ChrysanthemumShell = 4
    ChrysanthemumDiademShell = 5
    RingShell = 6
    SaturnShell = 7
    BeeShell = 8
    SkullBlast = 9
    TrailExplosion = 10


class FireworkType():
    BasicPeony = 0
    AdvancedPeony = 1
    DiademPeony = 2
    Chrysanthemum = 3
    DiademChrysanthemum = 4
    Ring = 5
    Saturn = 6
    Bees = 7
    TrailBurst = 8
    GlowFlare = 9
    PalmTree = 10
    Mickey = 11
    PirateSkull = 12
    AmericanFlag = 13