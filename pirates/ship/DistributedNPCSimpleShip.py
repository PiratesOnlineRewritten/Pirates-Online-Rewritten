from pirates.ship import ShipGlobals
from pirates.ship.DistributedSimpleShip import DistributedSimpleShip
import random
from pirates.piratesbase import PLocalizer
from pirates.battle import EnemyGlobals
from pirates.ship import HighSeasGlobals
from pirates.piratesgui import MessageGlobals

class DistributedNPCSimpleShip(DistributedSimpleShip):

    def __init__(self, cr):
        DistributedSimpleShip.__init__(self, cr)
        self.isNpc = 1
        self.hunterLevel = 0

    def announceGenerate(self):
        self.setupAggroCollisions()
        DistributedSimpleShip.announceGenerate(self)
        if self.gameFSM.state in ['Docked', 'Pinned', 'Adrift']:
            self.model.instantDocked()
        else:
            self.model.instantSailing()

    def disable(self):
        self.cleanupAggroCollisions()
        DistributedSimpleShip.disable(self)

    def getNPCship(self):
        return True

    def setShipClass(self, shipClass):
        self.hpModifier, self.cargoModifier, self.expModifier = ShipGlobals.getModifiedShipStats(self.level)
        DistributedSimpleShip.setShipClass(self, shipClass)

    def d_suggestResync(self, avId, timestampA, timestampB, serverTime, uncertainty):
        self.cr.timeManager.synchronize('suggested by %d' % avId)

    def announceAttack(self, shipToAttackDoId, hunterLevel):
        if localAvatar.ship and localAvatar.ship.getDoId() == shipToAttackDoId:
            simple = random.choice([0, 1])
            attackMessage = None
            if hunterLevel == EnemyGlobals.SHIP_THREAT_BOUNTY_HUNTERS:
                attackMessage = HighSeasGlobals.getInboundHunterMessage()
            else:
                simple = random.choice([0, 1])
                if simple:
                    attackMessage = HighSeasGlobals.getInboundMessage()
                else:
                    attackMessage = HighSeasGlobals.getInboundHelpMessage()
            if attackMessage:
                base.localAvatar.guiMgr.queueInstructionMessage(attackMessage[0], attackMessage[1], None, 1.0, messageCategory=MessageGlobals.MSG_CAT_ANNOUNCE_ATTACK)
        return

    def getHunterLevel(self):
        return self.hunterLevel

    def setHunterLevel(self, hunterLevel):
        self.hunterLevel = hunterLevel
        self.updateNametag()