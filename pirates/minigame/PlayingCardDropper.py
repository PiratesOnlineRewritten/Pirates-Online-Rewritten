import random
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task import Task
from pirates.piratesbase import PLocalizer
import PlayingCardGlobals
chanceOfHigherCard = 50

def dropTier0():
    chance100 = random.randrange(1, 100, 1)
    chance4 = random.randrange(1, 5, 1)
    if chance100 > chanceOfHigherCard:
        rank = '03'
    else:
        rank = '02'
    if chance4 == 4:
        suit = 's'
    elif chance4 == 3:
        suit = 'c'
    elif chance4 == 2:
        suit = 'd'
    else:
        suit = 'h'
    return PlayingCardGlobals.getCardEncoding(suit, rank)


def dropTier1():
    chance5 = random.randrange(1, 6, 1)
    chance4 = random.randrange(1, 5, 1)
    if chance5 == 5:
        rank = '08'
    elif chance5 == 4:
        rank = '07'
    elif chance5 == 3:
        rank = '06'
    else:
        if chance5 == 2:
            rank = '05'
        else:
            rank = '04'
        if chance4 == 4:
            suit = 's'
        if chance4 == 3:
            suit = 'c'
        if chance4 == 2:
            suit = 'd'
        suit = 'h'
    return PlayingCardGlobals.getCardEncoding(suit, rank)


def dropTier2():
    chanceSuit4 = random.randrange(1, 5, 1)
    chance4 = random.randrange(1, 5, 1)
    if chanceSuit4 == 4:
        rank = '12'
    elif chanceSuit4 == 3:
        rank = '11'
    else:
        if chanceSuit4 == 2:
            rank = '10'
        else:
            rank = '09'
        if chance4 == 4:
            suit = 's'
        else:
            if chance4 == 3:
                suit = 'c'
            if chance4 == 2:
                suit = 'd'
            suit = 'h'
    return PlayingCardGlobals.getCardEncoding(suit, rank)


def dropTier3():
    chance2 = random.randrange(1, 3, 1)
    chance4 = random.randrange(1, 5, 1)
    if chance2 == 2:
        rank = '01'
    else:
        rank = '13'
    if chance4 == 4:
        suit = 's'
    elif chance4 == 3:
        suit = 'c'
    elif chance4 == 2:
        suit = 'd'
    else:
        suit = 'h'
    return PlayingCardGlobals.getCardEncoding(suit, rank)