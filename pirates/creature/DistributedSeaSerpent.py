from pirates.creature.DistributedCreature import DistributedCreature
from pirates.creature.SeaSerpent import SeaSerpent

class DistributedSeaSerpent(DistributedCreature):

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr, SeaSerpent())