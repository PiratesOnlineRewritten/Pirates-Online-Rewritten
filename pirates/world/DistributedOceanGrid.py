from direct.distributed.DistributedCartesianGrid import DistributedCartesianGrid
from direct.showbase.PythonUtil import report
from pirates.world import WorldGlobals
from pirates.seapatch.SeaPatch import SeaPatch
from pirates.seapatch.Reflection import Reflection
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pandac.PandaModules import *
from OceanGridBase import OceanGridBase
from pirates.map.Minimap import OceanMap
from pirates.map.Mappable import MappableGrid

class DistributedOceanGrid(DistributedCartesianGrid, OceanGridBase, MappableGrid):

    def __init__(self, cr):
        DistributedCartesianGrid.__init__(self, cr)
        OceanGridBase.__init__(self)
        self.islandGrids = {}
        self.minimap = None
        self.water = None

    def generate(self):
        DistributedCartesianGrid.generate(self)
        self.setupWater()
        self.setupShipBarrier()

    def announceGenerate(self):
        DistributedCartesianGrid.announceGenerate(self)
        self.setupMinimap()
        #self.stash()
        #self.water.disable()
        
    def setLocation(self, parentId, zoneId):
        DistributedCartesianGrid.setLocation(self, parentId, zoneId)

    def disable(self):
        DistributedCartesianGrid.disable(self)
        self.destroyMinimap()
        self.shipBarrierNP.removeNode()
        self.ignore('enter' + self.cName)

    def delete(self):
        self.cleanupWater()
        DistributedCartesianGrid.delete(self)

    def setupWater(self):
        r = Reflection.getGlobalReflection()
        water = SeaPatch(self, reflection=r)
        water.loadSeaPatchFile('out.spf')
        self.water = water

    def cleanupWater(self):
        self.water.delete()
        self.water = None
        return

    def setupShipBarrier(self):
        worldRadius = WorldGlobals.OCEAN_GRID_SIZE * WorldGlobals.OCEAN_CELL_SIZE / 2.0 - 50
        shipBarrier = CollisionInvSphere(0.0, 0.0, 0.0, worldRadius)
        shipBarrier.setTangible(1)
        self.cName = self.uniqueName('ShipBarrier')
        cSphereNode = CollisionNode(self.cName)
        cSphereNode.setIntoCollideMask(PiratesGlobals.ShipCollideBitmask)
        cSphereNode.addSolid(shipBarrier)
        self.shipBarrierNP = self.attachNewNode(cSphereNode)
        self.accept('enter' + self.cName, self.handleEdgeOfWorld)

    def handleEdgeOfWorld(self, event):
        localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.EdgeOfWorldWarning)

    def handleChildArrive(self, childObj, zoneId):
        DistributedCartesianGrid.handleChildArrive(self, childObj, zoneId)
        if self.minimap and hasattr(childObj, 'getMinimapObject'):
            if childObj.getMinimapObject():
                self.minimap.addObject(childObj.getMinimapObject())

    def handleChildLeave(self, childObj, zoneId):
        if self.minimap and hasattr(childObj, 'getMinimapObject'):
            if childObj.getMinimapObject():
                self.minimap.removeObject(childObj.getMinimapObject())
        DistributedCartesianGrid.handleChildLeave(self, childObj, zoneId)

    oceanAreas = {}

    def addOceanArea(self, pos1, pos2, name, uid):
        ul = Point3(min(pos2.getX(), pos1.getX()), max(pos2.getY(), pos1.getY()), 0)
        lr = Point3(max(pos2.getX(), pos1.getX()), min(pos2.getY(), pos1.getY()), 0)
        if name in self.oceanAreas:
            pos1, pos2 = self.oceanAreas[name][0:2]
            ul = Point3(min(ul.getX(), pos1.getX()), max(ul.getY(), pos1.getY()), 0)
            lr = Point3(max(lr.getX(), pos2.getX()), min(lr.getY(), pos2.getY()), 0)
        self.oceanAreas[name] = [
         ul, lr, uid]

    def addOceanAreasToMap(self):
        mapPage = base.localAvatar.guiMgr.mapPage
        areaNames = self.oceanAreas.keys()
        for name in areaNames:
            mapPage.addOceanArea(name, self.oceanAreas[name][2], self.oceanAreas[name][0], self.oceanAreas[name][1])

    def addIslandGrid(self, island):
        self.islandGrids[island.doId] = island

    def removeIslandGrid(self, island):
        islandId = island.doId
        if self.islandGrids.get(islandId):
            del self.islandGrids[islandId]

    @report(types=['args'], dConfigParam=['dteleport'])
    def handleOnStage(self):
        self.unstash()
        self.water.enable()

    @report(types=['args'], dConfigParam=['dteleport'])
    def handleOffStage(self):
        self.stash()
        self.water.disable()

    def getTeleportDestPosH(self, index=0):
        return (0, 0, 0, 0)

    def getFootprintNode(self):
        return NodePath('footprint-empty')

    def getShopData(self):
        return ()

    def getGridParameters(self):
        return (self.cellWidth, self.viewingRadius)

    def getZoomLevels(self):
        return ((3000, 5000, 7000, 10000), 1)

    def getMapNode(self):
        mapNode = self.find('minimap')
        if mapNode.isEmpty():
            cm = CardMaker('minimap-card')
            sideWidth = self.cellWidth * self.gridSize
            cm.setFrame(-sideWidth, sideWidth, -sideWidth, sideWidth)
            modelNode = ModelNode('minimap')
            modelNode.setPreserveTransform(1)
            mapNode = self.attachNewNode(modelNode)
            mapGeom = mapNode.attachNewNode(cm.generate())
            mapGeom.setP(-90)
            mapGeom.hide()
        return mapNode

    def getMinimap(self):
        if not self.minimap:
            self.setupMinimap()
        return self.minimap

    def setupMinimap(self):
        if not self.minimap and not self.getMapNode().isEmpty():
            self.minimap = OceanMap(self)

    def destroyMinimap(self):
        if self.minimap:
            self.minimap.destroy()
            self.minimap = None