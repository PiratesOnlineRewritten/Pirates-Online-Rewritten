from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.directnotify import DirectNotifyGlobal
from pirates.world.WorldGlobals import *
from pirates.world.LocationConstants import LocationIds
from pirates.battle.Teamable import Teamable
from direct.task import Task

class DistributedIslandAI(DistributedGameAreaAI, DistributedCartesianGridAI, Teamable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedIslandAI')
    notify.setInfo(True)

    def __init__(self, air):
        DistributedCartesianGridAI.__init__(self, air, ISLAND_GRID_STARTING_ZONE, ISLAND_GRID_SIZE,
            ISLAND_GRID_RADIUS, ISLAND_CELL_SIZE)

        DistributedGameAreaAI.__init__(self, air)
        Teamable.__init__(self)

        self.sphereRadii = [0, 0, 0]
        self.sphereCenter = [0, 0]
        self.islandModel = ''
        self.undockable = False
        self.collisionSpheres = []
        self.feastFireEnabled = False
        self.fireworkShowEnabled = [False, 0]

        self.nextEvent = 0

    def generate(self):
        DistributedCartesianGridAI.generate(self)
        DistributedGameAreaAI.generate(self)

    def announceGenerate(self):
        DistributedCartesianGridAI.announceGenerate(self)
        DistributedGameAreaAI.announceGenerate(self)
        if config.GetBool('want-island-events', True):
            self.__runIslandEvents()
            self.runEvents = taskMgr.doMethodLater(15, self.__runIslandEvents, 'runEvents')

    def delete(self):
        DistributedCartesianGridAI.delete(self)
        DistributedGameAreaAI.delete(self)

    def __runIslandEvents(self, task=None):
        self.nextEvent -= 15
        if self.nextEvent <= 0:
            islandId = self.getUniqueId()
            if islandId == LocationIds.DEL_FUEGO_ISLAND or islandId == LocationIds.MADRE_DEL_FUEGO_ISLAND:
                self.d_makeLavaErupt()
                self.nextEvent = max(config.GetInt('eruption-delay', 60), 15) if config.GetBool('want-dev', False) else random.randint(5, 10) * 60
                self.notify.debug('%s has erupted! Next eruption is in %d seconds' % (self.getLocalizerName(), self.nextEvent))

        return Task.again

    def setIslandTransform(self, x, y, z, h):
        self.setXYZH(x, y, z, h)

    def d_setIslandTransform(self, x, y, z, h):
        self.sendUpdate('setIslandTransform', [x, y, z, h])

    def b_setIslandTransform(self, x, y, z, h):
        self.setIslandTransform(x, y, z, h)
        self.d_setIslandTransform(x, y, z, h)

    def getIslandTransform(self):
        return [self.getX(), self.getY(), self.getZ(), self.getH()]

    def setZoneSphereSize(self, rad0, rad1, rad2):
        self.sphereRadii = [rad0, rad1, rad2]

    def d_setZoneSphereSize(self, rad0, rad1, rad2):
        self.sendUpdate('setZoneSphereSize', [rad0, rad1, rad2])

    def b_setZoneSphereSize(self, rad0, rad1, rad2):
        self.setZoneSphereSize(rad0, rad1, rad2)
        self.d_setZoneSphereSize(rad0, rad1, rad2)

    def getZoneSphereSize(self):
        return self.sphereRadii

    def setZoneSphereCenter(self, x, y):
        self.sphereCenter = [x, y]

    def d_setZoneSphereCenter(self, x, y):
        self.sendUpdate('setZoneSphereCenter', [x, y])

    def b_setZoneSphereCenter(self, x, y):
        self.setZoneSphereCenter(x, y)
        self.d_setZoneSphereCenter(x, y)

    def getZoneSphereCenter(self):
        return self.sphereCenter

    def setIslandModel(self, islandModel):
        self.islandModel = islandModel

    def d_setIslandModel(self, islandModel):
        self.sendUpdate('setIslandModel', [islandModel])

    def b_setIslandModel(self, islandModel):
        self.setIslandModel(islandModel)
        self.d_setIslandModel(islandModel)

    def getIslandModel(self):
        return self.islandModel

    def setUndockable(self, undockable):
        self.undockable = undockable

    def d_setUndockable(self, undockable):
        self.sendUpdate('setUndockable', [undockable])

    def b_setUndockable(self, undockable):
        self.setUndockable(undockable)
        self.d_setUndockable(undockable)

    def getUndockable(self):
        return self.undockable

    def setPortCollisionSpheres(self, collisionSpheres):
        self.collisionSpheres = collisionSpheres

    def d_setPortCollisionSpheres(self, collisionSpheres):
        self.sendUpdate('setPortCollisionSpheres', [collisionSpheres])

    def b_setPortCollisionSpheres(self, collisionSpheres):
        self.setPortCollisionSpheres(collisionSpheres)
        self.d_setPortCollisionSpheres(collisionSpheres)

    def getPortCollisionSpheres(self):
        return self.collisionSpheres

    def d_makeLavaErupt(self):
        self.sendUpdate('makeLavaErupt', [])

    def setFeastFireEnabled(self, feastFireEnabled):
        self.feastFireEnabled = feastFireEnabled

    def d_setFeastFireEnabled(self, feastFireEnabled):
        self.sendUpdate('setFeastFireEnabled', [feastFireEnabled])

    def b_setFeastFireEnabled(self, feastFireEnabled):
        self.setFeastFireEnabled(feastFireEnabled)
        self.d_setFeastFireEnabled(feastFireEnabled)

    def getFeastFireEnabled(self):
        return self.feastFireEnabled

    def setFireworkShowEnabled(self, isEnabled, showType):
        self.fireworkShowEnabled = [isEnabled, showType]

    def d_setFireworkShowEnabled(self, isEnabled, showType):
        self.sendUpdate('setFireworkShowEnabled', [isEnabled, showType])

    def b_setFireworkShowEnabled(self, isEnabled, showType):
        self.setFireworkShowEnabled(isEnabled, showType)
        self.d_setFireworkShowEnabled(isEnabled, showType)

    def getFireworkShowEnabled(self):
        return self.fireworkShowEnabled

    def delete(self):
        DistributedCartesianGridAI.delete(self)
        DistributedGameAreaAI.delete(self)
