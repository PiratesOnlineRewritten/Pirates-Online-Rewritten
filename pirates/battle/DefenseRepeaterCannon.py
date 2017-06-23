from pandac.PandaModules import *
from pirates.battle.DefenseCannon import DefenseCannon

class DefenseRepeaterCannon(DefenseCannon):

    def __init__(self, cr, shipCannon=False):
        DefenseCannon.__init__(self, cr, shipCannon)