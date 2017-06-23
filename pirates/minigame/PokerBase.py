from pirates.minigame import PlayingCardGlobals

class PokerBase():
    debug = False
    handCodeArray = [
     'Nothing', 'NoPair', 'OnePair', 'TwoPair', 'Trips', 'Straight', 'Flush', 'FlHouse', 'Quads', 'StFlush']

    def __init__(self):
        self.debug = PokerBase.debug

    def getMinimumBetAmount(self):
        bet = self.anteList[2]
        if bet:
            if self.round >= 3:
                bet = bet * 2
        else:
            bet = self.anteList[0]
            if bet:
                if self.getGameType() == PlayingCardGlobals.SevenStud:
                    if self.checkForVisiblePair():
                        bet = bet * 2
            else:
                bet = PlayingCardGlobals.DefaultBetAmount
        return bet

    def minimumChipsToSitDown(self):
        minimum_chips = 20
        minimum_bet_multiplier = 10
        if self.anteList[2] > 0:
            minimum_chips = minimum_bet_multiplier * self.anteList[2]
        elif self.anteList[0] > 0:
            minimum_chips = minimum_bet_multiplier * self.anteList[0]
        return minimum_chips

    def handCodeToHandId(self, handCode):
        handId = PlayingCardGlobals.Nothing
        if handCode:
            if handCode == 'Nothing':
                handId = PlayingCardGlobals.Nothing
            elif handCode == 'NoPair':
                handId = PlayingCardGlobals.NoPair
            elif handCode == 'OnePair':
                handId = PlayingCardGlobals.OnePair
            elif handCode == 'TwoPair':
                handId = PlayingCardGlobals.TwoPair
            elif handCode == 'Trips':
                handId = PlayingCardGlobals.Trips
            elif handCode == 'Straight':
                handId = PlayingCardGlobals.Straight
            elif handCode == 'Flush':
                handId = PlayingCardGlobals.Flush
            elif handCode == 'FlHouse':
                handId = PlayingCardGlobals.FlHouse
            elif handCode == 'Quads':
                handId = PlayingCardGlobals.Quads
            elif handCode == 'StFlush':
                handId = PlayingCardGlobals.StFlush
        return handId

    def handIdToHandCode(self, handId):
        return self.handCodeArray[handId]

    def checkCondition(self):
        check = False
        if self.maxBet == 0:
            check = True
        return check

    def checkForVisiblePair(self):
        return False

    def sevenStudCheckForVisiblePair(self, hands):
        pair = False
        if hands:
            for hand in hands:
                length = len(hand)
                if length >= 4:
                    rank_array = [
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                    if length >= 7:
                        length = 6
                    i = 2
                    while i < length:
                        rank = hand[i] % 13
                        total = rank_array[rank]
                        if total == 0:
                            rank_array[rank] = 1
                        else:
                            pair = True
                            break
                        i = i + 1

                if pair:
                    break

        return pair