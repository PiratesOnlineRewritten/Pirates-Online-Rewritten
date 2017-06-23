from pirates.audio import SoundGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.ship import ShipGlobals
from pirates.ship.DistributedSimpleShip import DistributedSimpleShip

class DistributedTutorialSimpleShip(DistributedSimpleShip):

    def __init__(self, cr):
        DistributedSimpleShip.__init__(self, cr)
        self.interactTube = None
        return

    def announceGenerate(self):
        DistributedSimpleShip.announceGenerate(self)
        self.setupBoardingSphere(bitmask=PiratesGlobals.WallBitmask | PiratesGlobals.SelectBitmask | PiratesGlobals.RadarShipBitmask)
        self.addDeckInterest()

    def localPirateArrived(self, av):
        DistributedSimpleShip.localPirateArrived(self, av)
        if av.isLocal():
            self.gameFSM.stopCurrentMusic()
            self.gameFSM.startCurrentMusic(SoundGlobals.MUSIC_CUBA_COMBAT)

    def localPirateLeft(self, av):
        DistributedSimpleShip.localPirateLeft(self, av)