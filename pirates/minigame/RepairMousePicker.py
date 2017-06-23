import math
from pandac.PandaModules import BitMask32
from pandac.PandaModules import NodePath, Point3
from pandac.PandaModules import CollisionNode, CollisionSphere, CollisionRay, GeomNode
from pandac.PandaModules import CollisionTraverser, CollisionHandlerQueue
from direct.interval.IntervalGlobal import Sequence, Parallel, LerpPosInterval, LerpFunc, Func
from direct.gui.DirectGui import DirectButton, DGG
from direct.task import Task
from RepairMincroGame import RepairMincroGame

class RepairMousePicker():

    def __init__(self):
        self.pickerNode = CollisionNode('RepairMousePicker.pickerNode')
        self.pickerNP = base.cam2d.attachNewNode(self.pickerNode)
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.collisionTraverser = CollisionTraverser()
        self.collisionHandler = CollisionHandlerQueue()
        self.collisionTraverser.addCollider(self.pickerNP, self.collisionHandler)
        self.clearCollisionMask()
        self.orthographic = True

    def destroy(self):
        del self.pickerNode
        self.pickerNP.removeNode()
        del self.pickerNP
        del self.pickerRay
        del self.collisionTraverser
        del self.collisionHandler

    def setOrthographic(self, ortho):
        self.orthographic = ortho

    def setCollisionMask(self, mask):
        self.pickerNode.setFromCollideMask(mask)

    def clearCollisionMask(self):
        self.pickerNode.setFromCollideMask(BitMask32.allOff())

    def getCollisions(self, traverseRoot, useIntoNodePaths=False):
        if not base.mouseWatcherNode.hasMouse():
            return []
        mpos = base.mouseWatcherNode.getMouse()
        if self.orthographic:
            self.pickerRay.setFromLens(base.cam2d.node(), 0, 0)
            self.pickerNP.setPos(mpos.getX(), 0.0, mpos.getY())
        else:
            self.pickerRay.setFromLens(base.cam2d.node(), mpos.getX(), mpos.getY())
            self.pickerNP.setPos(0.0, 0.0, 0.0)
        self.collisionTraverser.traverse(traverseRoot)
        pickedObjects = []
        if useIntoNodePaths:
            for i in range(self.collisionHandler.getNumEntries()):
                pickedObjects.append(self.collisionHandler.getEntry(i).getIntoNodePath())

        else:
            for i in range(self.collisionHandler.getNumEntries()):
                pickedObjects.append(self.collisionHandler.getEntry(i))

        return pickedObjects