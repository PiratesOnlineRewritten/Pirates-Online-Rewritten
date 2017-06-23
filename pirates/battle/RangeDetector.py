from pandac.PandaModules import *
from pirates.battle import WeaponGlobals

class RangeDetector(NodePath):

    def __init__(self):
        NodePath.__init__(self, 'rangeDetector')
        self.spheres = []
        for radius in WeaponGlobals.Ranges:
            sphere = CollisionSphere(0, 0, 0, 1.0)
            sphere.setTangible(0)
            sphereNode = CollisionNode('rangeDetector-%s' % radius)
            sphereNode.addSolid(sphere)
            sphereNodePath = self.attachNewNode(sphereNode)
            self.spheres.append(sphereNodePath)