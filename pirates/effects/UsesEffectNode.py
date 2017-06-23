from pandac.PandaModules import *

class UsesEffectNode(NodePath):

    def __init__(self, offset=3.0):
        self.billboardNode = self.attachNewNode('billboardNode')
        self.billboardNode.node().setEffect(BillboardEffect.make(Vec3(0, 0, 1), 0, 1, offset, NodePath(), Point3(0, 0, 0)))
        self.effectNode = self.billboardNode.attachNewNode('effectNode')

    def getEffectParent(self):
        return self.effectNode

    def resetEffectParent(self):
        self.billboardNode.reparentTo(self)

    def delete(self):
        self.effectNode.removeNode()
        self.billboardNode.removeNode()
        del self.effectNode
        del self.billboardNode