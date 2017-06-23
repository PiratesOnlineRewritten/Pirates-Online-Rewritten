from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from direct.showbase.PythonUtil import *
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PiratesGlobals
from direct.distributed.StagedObject import StagedObject

class ZoneLOD(DirectObject, StagedObject):
    notify = directNotify.newCategory('ZoneLOD')

    def __init__(self, uniqueNameFunc, zoneRadii=[], onStage=StagedObject.ON):
        StagedObject.__init__(self, onStage)
        self.uniqueNameFunc = uniqueNameFunc
        self.zoneRadii = zoneRadii
        self.zoneSphere = []
        self.lastZoneLevel = None
        self.numSpheres = 0
        self.levelForced = False
        self.lodCollideMask = PiratesGlobals.ZoneLODBitmask
        self.allEnabled = False
        return

    def delete(self):
        self.deleteZoneCollisions()
        if self.zoneSphere:
            del self.zoneSphere
        self.ignoreAll()
        del self.uniqueNameFunc

    def cleanup(self):
        if hasattr(self, 'outerSphere') and self.numSpheres:
            self.setZoneLevel(self.outerSphere + 1)

    def setZoneRadii(self, zoneRadii, zoneCenter=[0, 0]):
        self.numSpheres = len(zoneRadii)
        self.zoneRadii = zoneRadii
        self.zoneCenter = zoneCenter
        self.innerSphere = 0
        self.outerSphere = self.numSpheres - 1
        self.deleteZoneCollisions()
        self.initZoneCollisions()
        if not self.isOnStage():
            for i in range(self.numSpheres):
                self.ignore(self.uniqueNameFunc('enterzoneLevel' + str(i)))
                self.ignore(self.uniqueNameFunc('exitzoneLevel' + str(i)))

            for sphere in self.zoneSphere:
                sphere.stash()

    def setLodCollideMask(self, mask):
        self.lodCollideMask = mask
        for currSphere in self.zoneSphere:
            currSphere.node().setIntoCollideMask(self.lodCollideMask)

    def getLodCollideMask(self):
        return self.lodCollideMask

    def initZoneCollisions(self):
        for i in range(len(self.zoneRadii)):
            cSphere = CollisionSphere(0.0, 0.0, 0.0, self.zoneRadii[i])
            cSphere.setTangible(0)
            cName = self.uniqueNameFunc('zoneLevel' + str(i))
            cSphereNode = CollisionNode(cName)
            cSphereNode.setIntoCollideMask(self.lodCollideMask)
            cSphereNode.addSolid(cSphere)
            cRoot = self.find('collisions')
            if not cRoot.isEmpty():
                cSphereNodePath = cRoot.attachNewNode(cSphereNode)
            else:
                cSphereNodePath = self.attachNewNode(cSphereNode)
            cSphereNodePath.setPos(self.zoneCenter[0], self.zoneCenter[1], 0)
            self.zoneSphere.append(cSphereNodePath)

        self.setZoneLevel(self.outerSphere + 1)

    def deleteZoneCollisions(self):
        for c in self.zoneSphere:
            c.removeNode()

        self.zoneSphere = []
        for i in range(self.numSpheres):
            self.ignore(self.uniqueNameFunc('enterzoneLevel' + str(i)))
            self.ignore(self.uniqueNameFunc('exitzoneLevel' + str(i)))

    def showZoneCollisions(self):
        for c in self.zoneSphere:
            c.show()

    def hideZoneCollisions(self):
        for c in self.zoneSphere:
            c.hide()

    def enableAllLODSpheres(self):
        for i in range(self.numSpheres):
            self.accept(self.uniqueNameFunc('exitzoneLevel' + str(i)), Functor(self.handleExitZoneLevel, i + 1))
            self.accept(self.uniqueNameFunc('enterzoneLevel' + str(i)), Functor(self.handleEnterZoneLevel, i))

        for sphere in self.zoneSphere:
            sphere.unstash()

        self.allEnabled = True

    def disableAllLODSpheres(self):
        for i in range(self.numSpheres):
            self.ignore(self.uniqueNameFunc('exitzoneLevel' + str(i)))
            self.ignore(self.uniqueNameFunc('enterzoneLevel' + str(i)))

        for sphere in self.zoneSphere:
            sphere.stash()

        self.allEnabled = False

    def clearAllEnabled(self, resetLastZoneLevel=False):
        self.allEnabled = False
        if resetLastZoneLevel:
            self.setCollLevel(self.lastZoneLevel)

    def setCollLevel(self, level):
        if self.allEnabled:
            return
        for i in range(self.numSpheres):
            self.ignore(self.uniqueNameFunc('enterzoneLevel' + str(i)))
            self.ignore(self.uniqueNameFunc('exitzoneLevel' + str(i)))

        for sphere in self.zoneSphere:
            sphere.stash()

        if level <= self.outerSphere:
            self.zoneSphere[level].unstash()
        if level > self.innerSphere:
            self.zoneSphere[level - 1].unstash()
        if level <= self.outerSphere:
            self.accept(self.uniqueNameFunc('exitzoneLevel' + str(level)), Functor(self.handleExitZoneLevel, level + 1))
        if level > self.innerSphere:
            self.accept(self.uniqueNameFunc('enterzoneLevel' + str(level - 1)), Functor(self.handleEnterZoneLevel, level - 1))

    def handleEnterZoneLevel(self, level, entry=None):
        if level >= self.lastZoneLevel:
            return
        self.setZoneLevel(level, entry)

    def handleExitZoneLevel(self, level, entry=None):
        if level < self.lastZoneLevel:
            return
        self.setZoneLevel(level, entry)

    def setZoneLevel(self, level, entry=None):
        self.notify.debug('Changing Zone %s:%s' % (self.name, level))
        if self.levelForced:
            return
        if self.lastZoneLevel == None:
            self.loadZoneLevel(level)
        elif self.lastZoneLevel > level:
            for i in range(self.lastZoneLevel - 1, level - 1, -1):
                self.loadZoneLevel(i)
                self.lastZoneLevel = i

        elif self.lastZoneLevel < level:
            for i in range(self.lastZoneLevel, level):
                self.unloadZoneLevel(i)
                if i == self.numSpheres:
                    self.allEnabled = False
                self.lastZoneLevel = i

        self.setCollLevel(level)
        self.lastZoneLevel = level
        return

    def setInitialZone(self, pos):
        avDist = pos.length()
        curLevel = self.outerSphere + 1
        for i in range(self.numSpheres):
            dist = self.zoneRadii[i]
            if avDist < dist:
                curLevel = i
                break

        self.setZoneLevel(curLevel)

    def setZoneLevelOuter(self):
        if self.outerSphere > self.lastZoneLevel:
            self.setZoneLevel(self.outerSphere)

    def handleOffStage(self):
        for i in range(self.numSpheres):
            self.ignore(self.uniqueNameFunc('enterzoneLevel' + str(i)))
            self.ignore(self.uniqueNameFunc('exitzoneLevel' + str(i)))

        for sphere in self.zoneSphere:
            sphere.stash()

        StagedObject.handleOffStage(self)

    def handleOnStage(self):
        StagedObject.handleOnStage(self)
        self.allEnabled = False
        if self.lastZoneLevel is not None:
            self.setCollLevel(self.lastZoneLevel)
        else:
            self.setCollLevel(self.outerSphere)
        return

    def loadZoneLevel(self, level):
        pass

    def unloadZoneLevel(self, level):
        pass

    def forceZoneLevel(self, level):
        self.setZoneLevel(level)
        self.levelForced = True

    def clearForceZoneLevel(self):
        self.levelForced = False
        self.setZoneLevel(self.outerSphere)

    def childLeft(self, myDoId, parentObj, isIsland=True):
        if isIsland:
            self.builder.left()
        for island in parentObj.islands.values():
            if island.doId != myDoId:
                if isIsland:
                    island.builder.areaGeometry.unstash()
                island.enableAllLODSpheres()
                if isIsland:
                    island.builder.collisions.unstash()

    def childArrived(self, myDoId, parentObj, isIsland=True):
        if isIsland:
            self.builder.arrived()
        for island in parentObj.islands.values():
            if island.doId != myDoId:
                if isIsland:
                    island.builder.areaGeometry.stash()
                    island.disableAllLODSpheres()
                    island.builder.collisions.stash()
                else:
                    island.clearAllEnabled(True)