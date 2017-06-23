import random
UNCHARTED_WATERS = 0
BRIGAND_BAY = 1
BLOODY_BAYOU = 2
SCURVY_SHALLOWS = 3
BLACKHEART_STRAIGHT = 4
WINDWARD_PASSAGE = 5
SALTY_FLATS = 6
MAR_DE_PLATA = 7
SMUGGLERS_RUN = 8
LEEWARD_PASSAGE = 9
DEAD_MANS_TROUGH = 10
MARINERS_REEF = 11
BOILING_BAY = 12
THE_HINTER_SEAS = 13
MAX_ZONE = THE_HINTER_SEAS + 1

def getOceanZone(xc, yc):
    xcoord = xc / 2000
    ycoord = yc / 2000
    if xcoord >= -15 and xcoord < -7 and ycoord >= 4 and ycoord < 11:
        return BRIGAND_BAY
    elif xcoord >= -7 and xcoord < -2 and ycoord >= 4 and ycoord < 11:
        return SCURVY_SHALLOWS
    elif xcoord >= 6 and xcoord < 13 and ycoord >= 8 and ycoord < 14:
        return SALTY_FLATS
    elif xcoord >= -2 and xcoord < 6 and ycoord >= 10 and ycoord < 14:
        return BLACKHEART_STRAIGHT
    elif xcoord >= -2 and xcoord < 2 and ycoord >= 8 and ycoord < 10:
        return BLACKHEART_STRAIGHT
    elif xcoord >= -2 and xcoord < 6 and ycoord >= -1 and ycoord < 10:
        return WINDWARD_PASSAGE
    elif xcoord >= -15 and xcoord < 1 and ycoord >= -3 and ycoord < 4:
        return BLOODY_BAYOU
    elif xcoord >= 6 and xcoord < 13 and ycoord >= -1 and ycoord < 8:
        return MAR_DE_PLATA
    elif xcoord >= 9 and xcoord < 13 and ycoord >= -4 and ycoord < -1:
        return MAR_DE_PLATA
    elif xcoord >= 11 and xcoord < 13 and ycoord >= -6 and ycoord < -4:
        return MAR_DE_PLATA
    elif xcoord >= 1 and xcoord < 11 and ycoord >= -8 and ycoord < -1:
        return SMUGGLERS_RUN
    elif xcoord >= 7 and xcoord < 13 and ycoord >= -15 and ycoord < -6:
        return THE_HINTER_SEAS
    elif xcoord >= -8 and xcoord < 7 and ycoord >= -15 and ycoord < -12:
        return MARINERS_REEF
    elif xcoord >= 1 and xcoord < 7 and ycoord >= -12 and ycoord < -8:
        return BOILING_BAY
    elif xcoord >= -15 and xcoord < -6 and ycoord >= -8 and ycoord < -3:
        return DEAD_MANS_TROUGH
    elif xcoord >= -8 and xcoord < 1 and ycoord >= -12 and ycoord < 0:
        return LEEWARD_PASSAGE
    else:
        return UNCHARTED_WATERS


def randomZoneCoord(ozone):
    if ozone == BRIGAND_BAY:
        xc = random.randint(-30000, -20001)
        yc = random.randint(8000, 21999)
        return (
         xc, yc)
    elif ozone == SCURVY_SHALLOWS:
        xc = random.randint(-14000, -4001)
        yc = random.randint(8000, 21999)
        return (
         xc, yc)
    elif ozone == SALTY_FLATS:
        xc = random.randint(12000, 25999)
        yc = random.randint(16000, 27999)
        return (
         xc, yc)
    elif ozone == BLACKHEART_STRAIGHT:
        if random.randint(1, 5) < 5:
            xc = random.randint(-4000, 11999)
            yc = random.randint(20000, 27999)
        else:
            xc = random.randint(-4000, 3999)
            yc = random.randint(16000, 19999)
        return (xc, yc)
    elif ozone == WINDWARD_PASSAGE:
        xc = random.randint(-4000, 11999)
        yc = random.randint(-2000, 15999)
        return (
         xc, yc)
    elif ozone == BLOODY_BAYOU:
        xc = random.randint(-30000, -4001)
        yc = random.randint(-6000, 7999)
        return (
         xc, yc)
    elif ozone == MAR_DE_PLATA:
        rval = random.randint(1, 7)
        if rval < 4:
            xc = random.randint(12000, 17999)
            yc = random.randint(-2000, 15999)
        elif rval < 6:
            xc = random.randint(18000, 21999)
            yc = random.randint(-8000, 15999)
        else:
            xc = random.randint(22000, 25999)
            yc = random.randint(-12000, 15999)
        return (xc, yc)
    elif ozone == SMUGGLERS_RUN:
        if random.randint(1, 7) < 5:
            xc = random.randint(2000, 17999)
            yc = random.randint(-8000, -2001)
        else:
            xc = random.randint(2000, 21999)
            yc = random.randint(-16000, -8001)
        return (xc, yc)
    elif ozone == LEEWARD_PASSAGE:
        if random.randint(1, 5) < 4:
            xc = random.randint(-12000, 1999)
            yc = random.randint(-16000, -1)
        else:
            xc = random.randint(-16000, 1999)
            yc = random.randint(-24000, -16001)
        return (xc, yc)
    elif ozone == DEAD_MANS_TROUGH:
        xc = random.randint(-30000, -12001)
        yc = random.randint(-16000, -6001)
        return (
         xc, yc)
    elif ozone == MARINERS_REEF:
        xc = random.randint(-16000, 13999)
        yc = random.randint(-30000, -24001)
        return (
         xc, yc)
    elif ozone == BOILING_BAY:
        xc = random.randint(2000, 13999)
        yc = random.randint(-24000, -16001)
        return (
         xc, yc)
    elif ozone == THE_HINTER_SEAS:
        if random.randint(1, 10) < 10:
            xc = random.randint(14000, 25999)
            yc = random.randint(-30000, -16001)
        else:
            xc = random.randint(22000, 25999)
            yc = random.randint(-16000, -12001)
        return (xc, yc)
    elif ozone == UNCHARTED_WATERS:
        direction = random.randint(1, 4)
        if direction == 1:
            xc = random.randint(-32000, 28000)
            yc = random.randint(26000, 30000)
        elif direction == 2:
            xc = random.randint(24000, 28000)
            yc = random.randint(-32000, 28000)
        elif direction == 3:
            xc = random.randint(-32000, 28000)
            yc = random.randint(-32000, -28000)
        else:
            xc = random.randint(-32000, -28000)
            yc = random.randint(-32000, 28000)
        return (xc, yc)
    else:
        return (0, 0)