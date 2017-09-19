from pirates.creature.DistributedAnimal import DistributedAnimal
from pirates.creature.Seagull import Seagull

class DistributedSeagull(DistributedAnimal):

    def __init__(self, cr):
        DistributedAnimal.__init__(self, cr, Seagull())