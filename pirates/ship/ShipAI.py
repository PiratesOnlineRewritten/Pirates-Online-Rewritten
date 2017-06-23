from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.piratesbase import PiratesGlobals

class ShipAI(DirectObject.DirectObject):
    notify = directNotify.newCategory('ShipAI')

    def __init__(self, root, collisions, locators):
        self.modelRoot = root
        self.modelCollisions = collisions
        self.__targetableCollisions = []
        self.locators = locators
        self.center = None
        self.owner = None
        self.mastCollisions = dict([ (int(x.getTag('Mast Code')), x) for x in self.modelCollisions.findAllMatches('**/collision_masts') ])
        self._eventRadius = 600
        return

    def setupCollisions(self, ship):
        self.modelRoot.setTag('shipId', str(ship.doId))
        self.modelCollisions.setTag('objType', str(PiratesGlobals.COLL_NEWSHIP))
        self.floors = self.modelCollisions.find('**/collision_floors')
        self.deck = self.modelCollisions.find('**/collision_deck')
        self.planeBarriers = self.modelCollisions.find('**/collision_planes')
        self.planeBarriers.stash()
        self.walls = self.modelCollisions.find('**/collision_walls')
        self.shipCollWall = self.modelCollisions.find('**/collision_shiptoship')
        self.panels = self.modelCollisions.find('**/collision_panels')
        self.stashPlaneCollisions()
        self.__setupShipEventCollisions()

    def cleanup(self):
        self.owner = None
        return

    def stashPlaneCollisions(self):
        self.planeBarriers.stash()

    def unstashPlaneCollisions(self):
        self.planeBarriers.unstash()

    def computeDimensions(self):
        if not self.center:
            self.center = self.modelRoot.attachNewNode('center')
        tb = self.modelRoot.getTightBounds()
        self.center.setPos((tb[0] + tb[1]) / 2.0)
        self.dimensions = tb[1] - tb[0]
        self.hullDimensions = tb[1] - tb[0]

    def sinkingBegin(self):
        pass

    def sinkingEnd(self):
        pass

    def disableOnDeckInteractions(self):
        pass

    def removeWake(self):
        pass

    def uniqueName(self, name):
        return name + '-%s' % id(self)

    def isInCrew(self, avId):
        if self.owner:
            return self.owner.isInCrew(avId)
        return False

    def __setupShipEventCollisions(self):
        if self.owner == None:
            return
        self.shipCollideSphere = CollisionSphere(0, 0, 0, self._eventRadius)
        self.shipCollideSphere.setTangible(0)
        shipCollideSphereEvent = self.owner.uniqueName('ShipEventSphere')
        self.shipCollideSphereNode = CollisionNode(shipCollideSphereEvent)
        self.shipCollideSphereNode.setFromCollideMask(BitMask32.allOff())
        self.shipCollideSphereNode.setIntoCollideMask(PiratesGlobals.ShipCollideBitmask | PiratesGlobals.ShipAvoidBitmask)
        self.shipCollideSphereNode.addSolid(self.shipCollideSphere)
        self.shipCollideSphereNodePath = self.owner.attachNewNode(self.shipCollideSphereNode)
        self.shipCollideSphereNodePath.setTag('collId', str(self.owner.getDoId()))
        return

    def overrideEventRadius(self, radius):
        self._eventRadius = radius

    def dropMast(self, index):
        if self.mastCollisions.has_key(index):
            self.mastCollisions[index].stash()
            return True
        return False

    def restoreMast(self, index):
        if self.mastCollisions.has_key(index):
            self.mastCollisions[index].unstash()
            return True
        return False

    def getBoardingLocators(self):
        return self.locators.findAllMatches('**/boarding_spots/*')