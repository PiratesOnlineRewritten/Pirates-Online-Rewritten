from pirates.minigame import PlayingCardGlobals
from pirates.minigame import DistributedPokerTable
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import Point3, Vec3
from pirates.piratesbase import PLocalizer

class Distributed7StudTable(DistributedPokerTable.DistributedPokerTable):

    def __init__(self, cr):
        DistributedPokerTable.DistributedPokerTable.__init__(self, cr, '7stud', numRounds=6)
        self.maxCommunityCards = 0
        self.maxHandCards = 7
        self.gameType = 1

    def getGameType(self):
        return PlayingCardGlobals.SevenStud

    def getInteractText(self):
        return PLocalizer.InteractTable7StudPoker

    def getSitDownText(self):
        return PLocalizer.PokerSitDown7StudPoker

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
                deals.append(self.dealPlayerCards(numCards=3))
            if round in [2, 3, 4, 5]:
                deals.append(self.dealPlayerCards(numCards=1))
        return deals

    def checkForVisiblePair(self):
        return self.sevenStudCheckForVisiblePair(self.playerHands)