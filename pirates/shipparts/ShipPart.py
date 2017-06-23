from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class ShipPart():
    woodBreakSfx = None
    distantBreakSfx = None

    def __init__(self):
        self.__targetableCollisions = []
        self.dna = None
        self.geomParent = None
        self.ship = None
        self.prop = None
        self.propCollisions = None
        self.collisions = None
        self.shipId = 0
        self.doId = 0
        self.highDetail = None
        self.medDetail = None
        self.lowDetail = None
        self.geom_High = None
        self.geom_Medium = None
        self.geom_Low = None
        self.zoneLevel = 99
        self.loaded = False
        if not self.woodBreakSfx:
            ShipPart.woodBreakSfx = (
             loadSfx(SoundGlobals.SFX_FX_WOOD_IMPACT_01), loadSfx(SoundGlobals.SFX_FX_WOOD_IMPACT_02), loadSfx(SoundGlobals.SFX_FX_WOOD_IMPACT_03), loadSfx(SoundGlobals.SFX_FX_WOOD_IMPACT_04))
        if not self.distantBreakSfx:
            ShipPart.distantBreakSfx = (
             loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_01), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_02), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_03), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_04), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_05), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_06), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_07), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_08), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_09), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_10))
        return

    def disable(self):
        pass

    def destroy(self):
        pass

    def unload(self):
        self.unloadHigh()
        self.unloadMedium()
        self.unloadLow()
        self.unloadCollisions()

    def setZoneLevel(self, level):
        if level > self.zoneLevel:
            for i in range(level):
                self.unloadZoneLevel(i)

        elif level < self.zoneLevel:
            for i in range(len(PiratesGlobals.ShipZones) - level):
                self.loadZoneLevel(i)

        self.zoneLevel = level

    def loadZoneLevel(self, level):
        if level == 0:
            self.loadHigh()
            self.unstashDetailCollisions()
        elif level == 1:
            self.loadMedium()
        elif level == 2:
            self.loadCollisions()
        elif level == 3:
            self.loadLow()

    def unloadZoneLevel(self, level):
        if level == 0:
            pass
        elif level == 1:
            self.unloadHigh()
            self.stashDetailCollisions()
        elif level == 2:
            self.unloadMedium()
        elif level == 3:
            self.unloadLow()
            self.unloadCollisions()

    def loadHigh(self):
        pass

    def unloadHigh(self):
        pass

    def loadMedium(self):
        pass

    def unloadMedium(self):
        pass

    def loadLow(self):
        pass

    def unloadLow(self):
        pass

    def loadCollisions(self):
        pass

    def unloadCollisions(self):
        pass

    def stashDetailCollisions(self):
        pass

    def unstashDetailCollisions(self):
        pass

    def addToShip(self):
        if self.geom_Low:
            self.geom_Low.reparentTo(self.ship.getLowDetail())
        if self.geom_Medium:
            self.geom_Medium.reparentTo(self.ship.getMediumDetail())
        if self.geom_High:
            self.geom_High.reparentTo(self.ship.getHighDetail())

    def cache(self):
        self.ship = None
        self.shipId = 0
        return

    def uncache(self, ship):
        self.ship = ship
        self.shipId = ship.doId