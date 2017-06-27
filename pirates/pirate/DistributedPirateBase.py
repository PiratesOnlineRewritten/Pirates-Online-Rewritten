from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.pirate import Pirate
from pirates.piratesbase import PiratesGlobals
from pirates.pvp import Beacon
from pirates.pvp import PVPGlobals

class DistributedPirateBase(DistributedObject.DistributedObject, Pirate.Pirate):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPirateBase')

    def __init__(self, cr):
        self.notify.debug('__init__')
        self.masterHuman = base.cr.human
        DistributedObject.DistributedObject.__init__(self, cr)
        Pirate.Pirate.__init__(self)
        self.beacon = None
        self.dnaKey = None

    def delete(self):
        Pirate.Pirate.delete(self)
        DistributedObject.DistributedObject.delete(self)

    def disable(self):
        self.dnaKey = self.getDnaKey()
        DistributedObject.DistributedObject.disable(self)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        if not self.loaded or self.dnaKey != self.getDnaKey():
            self.generateHuman(self.style.gender, self.masterHuman)

    def showBeacon(self, team):
        if self.beacon:
            self.hideBeacon()

        if team > 0:
            self.beaconNodePath = self.nametag3d.attachNewNode('beacon')
            self.beacon = Beacon.getBeacon(self.beaconNodePath)
            self.beacon.setZ(2)
            self.beacon.setBillboardPointWorld()
            self.exposeJoint(self.beaconNodePath, 'modelRoot', 'name_tag', '500')
            self.beacon.setColor(PVPGlobals.getTeamColor(team))

    def hideBeacon(self):
        if self.beacon:
            self.beacon.remove()

        self.beacon = None

    def getDnaKey(self):
        myDna = self.getStyle()
        dnaKey = (myDna.getClothesBelt(), myDna.getClothesBotColor(), myDna.getClothesCoat(), myDna.getClothesHat(), myDna.getClothesPant(), myDna.getClothesShirt(), myDna.getClothesVest(), myDna.getClothesShirt(), myDna.getClothesTopColor(), myDna.getTattooChest(), myDna.getTattooZone2(), myDna.getTattooZone3(), myDna.getTattooZone4(), myDna.getTattooZone5(), myDna.getTattooZone6(), myDna.getTattooZone7(), myDna.getTattooZone8(), myDna.jewelryZone1, myDna.jewelryZone2, myDna.jewelryZone3, myDna.jewelryZone4, myDna.jewelryZone5, myDna.jewelryZone6, myDna.jewelryZone7, myDna.jewelryZone8, myDna.getHairBaseColor(), myDna.getHairBeard(), myDna.getHairColor(), myDna.getHairHair(), myDna.getHairMustache())
        return dnaKey
