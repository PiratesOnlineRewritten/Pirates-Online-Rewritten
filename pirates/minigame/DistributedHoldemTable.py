import random
from pirates.minigame import PlayingCardGlobals
from pirates.minigame import DistributedPokerTable
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import Point3, Vec3
from pirates.piratesbase import PLocalizer

class DistributedHoldemTable(DistributedPokerTable.DistributedPokerTable):

    def __init__(self, cr):
        DistributedPokerTable.DistributedPokerTable.__init__(self, cr, 'holdem', numRounds=5)
        self.maxCommunityCards = 5
        self.maxHandCards = 2
        self.gameType = 0

    def getGameType(self):
        return PlayingCardGlobals.Holdem

    def getInteractText(self):
        return PLocalizer.InteractTableHoldemPoker

    def getSitDownText(self):
        return PLocalizer.PokerSitDownHoldEmPoker

    def dealerAnim(self, round):
        deals = Sequence()
        if round == 0:
            if self.isLocalAvatarSeated():
                self.gui.disableAction()
                self.gui.clearTable()
            for card in self.PocketCards:
                card.hide()

        else:
            if round == 1:
                deals.append(self.dealPlayerCards(numCards=2))
            if round in [2, 3, 4]:
                if round == 2:
                    deals.append(self.dealCommunityCards(numCards=3))
                else:
                    deals.append(self.dealCommunityCards(numCards=1))
        return deals