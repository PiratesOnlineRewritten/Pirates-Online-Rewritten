from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.showbase import DirectObject
from direct.task import Task
from pirates.piratesbase import PiratesGlobals
import InteractiveBase

class InteractionManager(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('InteractionManager')
    Forward = Vec3(0, 1, 0)

    def __init__(self):
        self.__interactives = []
        self.__nearest = None
        self.__mouseOver = None
        self.__currentInteractive = None
        self.__updateDelay = 0.2
        self.__updateTaskName = 'InteractionManagerUpdate'
        self.__locked = 0
        self.cTrav = None
        self.lifter = None
        self.cRayNode = None
        self.setupLifter()
        return

    def delete(self):
        self.cleanupLifter()
        self.stop()

    def __str__(self):
        if self.__nearest:
            nearest = self.__nearest.getName()
        else:
            nearest = None
        if self.__currentInteractive:
            current = '%s(%s)' % (self.__currentInteractive.getName(), self.__currentInteractive.doId)
        else:
            current = None
        return 'InteractionMgr: N-%s, C-%s' % (nearest, current)

    def start(self):
        if self.__locked:
            return
        taskMgr.remove(self.__updateTaskName)
        taskMgr.doMethodLater(self.__updateDelay, self.updateTextMessage, self.__updateTaskName)

    def stop(self, endCurrent=False):
        if self.__locked:
            return
        if endCurrent:
            self.requestExitCurrent()
        taskMgr.remove(self.__updateTaskName)
        if self.__nearest:
            self.__nearest.hideProximityInfo()
            self.__nearest = None
        if self.__mouseOver:
            self.__mouseOver.hideMouseOverInfo()
            self.__mouseOver = None
        return

    def lock(self):
        self.__locked = 1

    def unlock(self):
        self.__locked = 0

    def addInteractive(self, iObj, priority=InteractiveBase.PROXIMITY):
        if iObj.allowInteract:
            if (
             iObj, priority) in self.__interactives:
                raise HierarchyException(0, 'Redundant Interactive - %s(%d)' % (iObj.getName(), iObj.doId))
            self.__interactives.append((iObj, priority))

    def removeInteractive(self, iObj, priority=InteractiveBase.PROXIMITY):
        if (
         iObj, priority) in self.__interactives:
            self.__interactives.remove((iObj, priority))
        if iObj == self.__nearest:
            iObj.hideProximityInfo()
            self.__nearest = None
        if iObj == self.__mouseOver:
            iObj.hideMouseOverInfo()
            self.__mouseOver = None
        return

    def sortInteractives(self):
        maxObj = None
        maxPri = 0
        for iObj, pri in self.__interactives:
            if pri > maxPri:
                maxObj = iObj
                maxPri = pri
                return (
                 maxObj, maxPri)

        maxDot = -1
        maxPri = -1
        for iObj, pri in self.__interactives:
            if not iObj.isEmpty():
                vObj = iObj.getPosRelToAv()
                vObj.normalize()
                vDot = self.Forward.dot(vObj)
                if vDot > maxDot:
                    maxDot = vDot
                    maxObj = iObj
                    maxPri = pri

        return (
         maxObj, maxPri)

    def updateTextMessage(self, task):
        if not self.__interactives:
            return task.again
        newClosest = None
        newObj, newPri = self.sortInteractives()

        def popupInfo(newObj, newPri, self=self):
            if newObj:
                if newPri == InteractiveBase.PROXIMITY:
                    newObj.showProximityInfo()
                    self.__nearest = newObj
                elif newPri == InteractiveBase.MOUSE_OVER:
                    newObj.showMouseOverInfo()
                    self.__mouseOver = newObj

        if newObj is None:
            if self.__nearest:
                self.__nearest.hideProximityInfo()
                self.__nearest = None
            if self.__mouseOver:
                self.__mouseOver.hideMouseOverInfo()
                self.__mouseOver = None
            return task.again
        if newObj != self.__nearest and newObj != self.__mouseOver:
            if self.__nearest:
                self.__nearest.hideProximityInfo()
                self.__nearest = None
            if self.__mouseOver:
                self.__mouseOver.hideMouseOverInfo()
                self.__mouseOver = None
            popupInfo(newObj, newPri)
        return task.again

    def setCurrentInteractive(self, interactive):
        interactiveId = 0
        if interactive:
            interactiveId = interactive.doId
        self.__currentInteractive = interactive
        if self.__nearest:
            self.__nearest.hideProximityInfo()
            self.__nearest = None
        if self.__mouseOver:
            self.__mouseOver.hideMouseOverInfo()
            self.__mouseOver = None
        return

    def getCurrentInteractive(self):
        return self.__currentInteractive

    def getCurrent(self):
        return self.getCurrentInteractive()

    def getInteractives(self):
        return self.__interactives

    def getNearest(self):
        return self.__nearest

    def getMouseOver(self):
        return self.__mouseOver

    def requestExitCurrent(self):
        if self.__currentInteractive:
            self.__currentInteractive.requestExit()

    def setupLifter(self):
        if not self.cTrav:
            self.cTrav = CollisionTraverser('InteractionMgr')
            cRay = CollisionRay(0.0, 0.0, 4000.0, 0.0, 0.0, -1.0)
            cRayNode = CollisionNode('InteractionMgr-cRay')
            cRayNode.addSolid(cRay)
            cRayNode.setFromCollideMask(PiratesGlobals.FloorBitmask | PiratesGlobals.ShipFloorBitmask)
            cRayNode.setIntoCollideMask(BitMask32.allOff())
            cRayNode.setBounds(BoundingSphere())
            cRayNode.setFinal(1)
            self.cRayNodePath = NodePath(cRayNode)
            self.lifter = CollisionHandlerFloor()
            self.lifter.setReach(8.0)

    def cleanupLifter(self):
        if self.cTrav:
            self.lifter.clearColliders()
            self.cTrav.clearColliders()
            self.cRayNode.removeNode()
            self.cTrav = None
            self.lifter = None
            self.cRayNode = None
        return

    def useLifter(self, liftedNodePath, severity=2):
        self.cRayNodePath.reparentTo(liftedNodePath)
        self.lifter.addCollider(self.cRayNodePath, liftedNodePath)
        self.cTrav.addCollider(self.cRayNodePath, self.lifter)
        self.cTrav.traverse(render)
        self.cTrav.removeCollider(self.cRayNodePath)
        self.lifter.removeCollider(self.cRayNodePath)
        self.cRayNodePath
        self.cRayNodePath.detachNode()