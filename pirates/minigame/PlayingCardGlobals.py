from pandac.PandaModules import *
from direct.showbase.ShowBase import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PLocalizer
SecondsPerHand = 30.0
MaximumTimeouts = 2
MinimumChips = 0
CheatingFine = 100
Unknown = 0
Holdem = 1
SevenStud = 2
Omaha = 3
OmahaHiLo = 4
Razz = 5
StudHiLo = 6
Limit = 1
PotLimit = 2
NoLimit = 3
Up = 1
Down = 0
NoAction = 0
Fold = 1
CheckCall = 2
BetRaise = 3
SmallBlind = 4
BigBlind = 5
Ante = 6
Check = 7
AllIn = 8
Leave = -1
Cheat1 = -2
Cheat2 = -3
Cheat7 = -7
CheatHelp = -10
Nothing = 0
NoPair = 1
OnePair = 2
TwoPair = 3
Trips = 4
Straight = 5
Flush = 6
FlHouse = 7
Quads = 8
StFlush = 9
UnknownCheat = -1
PeekCheatLeft = 1
PeekCheatRight = 2
ReplaceHoleCardOneCheat = 3
ReplaceHoleCardTwoCheat = 4
ReplaceHoleCardSevenCheat = 5
PlayBadHandTell = 6
PlayGoodHandTell = 7
CaughtCheating = 10
PlayerLost = 0
PlayerInactive = -1
PlayerOutOfChips = -2
PlayerCaughtCheating = -3
PlayerStateUndefined = -100
NoTell = 0
GoodTell = 1
BadTell = 2
BaseTellChanceAI = 0.15
BaseTellChancePlayer = 0.15
NoAction = 0
Bid = 1
Stay = 2
Hit = 3
Split = 4
DoubleDown = 5
AskCard = 6
AskQuiet = 7
AskForBid = 8
CardSwap = 9
AutoStay = 10
BidTimeout = 13.0
AskCardTimeout = 20.0
DealDelay = 1.0
DealCompleteDelay = 1.0
PayOutDelay = 1.0

def getBlackjackActionText(action):
    if action[0] == Bid:
        return PLocalizer.BlackjackActionNames[action[0]] % action[1]
    else:
        return PLocalizer.BlackjackActionNames[action[0]]


DefaultBetAmount = 2
BlackjackBidAmount = 2
Hearts = 0
Diamonds = 1
Clubs = 2
Spades = 3
Suits = [
 Hearts, Diamonds, Clubs, Spades]
AceOfSpades = 51
Unknown = 255
UpColor = Vec4(1, 1, 1, 1)
RolloverColor = Vec4(1, 1, 0.5, 1)
DownColor = Vec4(1, 0.9, 0.9, 1)
DisabledColor = Vec4(1, 1, 1, 0.5)
CardColors = (
 UpColor, DownColor, RolloverColor, DisabledColor)
Styles = [
 'standard']
_modelPathBase = 'models/handheld/playing_cards_'
_prefix = 'PC_'
CardImages = {}
_cardImagesInitialized = 0

def getCardName(value):
    if value == Unknown:
        return PLocalizer.PlayingCardUnknown
    else:
        rank = value % 13
        suit = value / 13
        return PLocalizer.getPlayingCardName(suit, rank)


def getCardEncoding(suit, rank):
    encoding = InventoryType.begin_Cards
    if suit == 's':
        encoding = encoding + 39
    else:
        if suit == 'c':
            encoding = encoding + 26
        elif suit == 'd':
            encoding = encoding + 13
        if rank == '01':
            encoding = encoding + 12
        elif rank == '13':
            encoding = encoding + 11
        elif rank == '12':
            encoding = encoding + 10
        elif rank == '11':
            encoding = encoding + 9
        elif rank == '10':
            encoding = encoding + 8
        elif rank == '09':
            encoding = encoding + 7
        elif rank == '08':
            encoding = encoding + 6
        elif rank == '07':
            encoding = encoding + 5
        elif rank == '06':
            encoding = encoding + 4
        elif rank == '05':
            encoding = encoding + 3
        elif rank == '04':
            encoding = encoding + 2
        elif rank == '03':
            encoding = encoding + 1
    return encoding


def getSuit(value, fromOffset=1):
    if fromOffset:
        newValue = value - InventoryType.begin_Cards
    else:
        newValue = value
    if newValue < 13:
        return 0
    else:
        return newValue / 13


def getRank(value, fromOffset=1):
    if fromOffset:
        newValue = value - InventoryType.begin_Cards
    else:
        newValue = value
    return newValue % 13


def initCardImages():
    global _cardImagesInitialized
    suitCodes = ('h', 'd', 'c', 's')
    rankCodes = ('02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12',
                 '13', '01')
    for style in Styles:
        modelPath = _modelPathBase + style
        cardModel = loader.loadModel(modelPath)
        CardImages[style] = {}
        for suitIndex in range(len(suitCodes)):
            suitCode = suitCodes[suitIndex]
            CardImages[style][suitIndex] = {}
            for rankIndex in range(len(rankCodes)):
                rankCode = rankCodes[rankIndex]
                nodeName = _prefix + rankCode + suitCode
                cardNode = cardModel.find('**/' + nodeName)
                CardImages[style][suitIndex][rankIndex] = cardNode

        CardImages[style]['back'] = cardModel.find('**/' + _prefix + 'back')

    _cardImagesInitialized = 1


def getImage(style, suit, rank):
    if _cardImagesInitialized == 0:
        initCardImages()
    return CardImages[style][suit][rank]


def getBack(style):
    if _cardImagesInitialized == 0:
        initCardImages()
    return CardImages[style]['back']


def getBlackjackHandValue(hand):
    aceCount = 0
    handValue = 0
    for card in hand:
        val = int(card % 13) + 2
        if val >= 11 and val <= 13:
            val = 10
        elif val == 14:
            aceCount += 1
            val = 11
        handValue += val

    for i in xrange(0, aceCount):
        if handValue > 21:
            handValue -= 10

    return handValue