from pirates.shipparts.DistributedSteeringWheel import DistributedSteeringWheel

class DistributedCDSteeringWheel(DistributedSteeringWheel):
    notify = directNotify.newCategory('DistributedCDSteeringWheel')

    def __init__(self, cr):
        DistributedSteeringWheel.__init__(self, cr)