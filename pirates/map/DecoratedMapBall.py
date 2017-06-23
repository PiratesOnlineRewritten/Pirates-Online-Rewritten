from pandac.PandaModules import *
from direct.showbase.PythonUtil import clampScalar, report
from direct.task.Task import Task
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.map.MapBall import MapBall
from pirates.map.MapDecor import DecorTypes, DecorClasses
from pirates.piratesgui.DownloadBlockerPanel import DownloadBlockerPanel
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PiratesGlobals
from pirates.world.LocationConstants import LocationIds
from pirates.world import WorldGlobals
import math
OceanAreaOffsets = {'Brigand_Bay': [0, -1],'Scurvy_Shallows': [0, 3],'Blackheart_Strait': [0, 2],'Salty_Flats': [0, -1],'Dead_Mans_Trough': [0, 1],'Smugglers_Run': [0, 0.5],'Bloody_Bayou': [0, -1.5]}

class DecoratedMapBall(MapBall):
    notify = directNotify.newCategory('DecoratedMapBall')
    defaultModelPath = 'models/islands/bilgewater_worldmap'

    def __init__(self, name, worldMap, maxTilt, *args, **kwargs):
        MapBall.__init__(self, name, worldMap, maxTilt, *args, **kwargs)
        self.itemCounter = 0
        self.placedItems = {}
        self.placedIslands = {}
        self.dartList = []
        self.billboardList = []
        self.boundIslandCount = 0
        self.dragging = False
        self.questDartPlaced = False
        self.questDartName = None
        self.setDecorInfo()
        self.resetDecor()
        self.initGlobalStencil()
        self.accept(PiratesGlobals.SeaChestHotkey, self.toggleQuestDartHelpText)
        return

    def removeNode(self):
        for item in self.placedItems.keys():
            self.removeDecorItem(item)

        del self.placedItems
        del self.dartList
        del self.billboardList
        del self.decorInfo
        MapBall.removeNode(self)

    def enable(self):
        super(DecoratedMapBall, self).enable()
        self.startBillboardTask()
        self.rotateAvatarToCenter()

    def disable(self):
        super(DecoratedMapBall, self).disable()
        self.stopBillboardTask()
        self.stopPickTask()

    def getFramePoint(self, mapBallPt):
        return self._transCamSpaceToHomogenousFramePt(self.cam.getRelativePoint(self, Point3(0)))

    def _mouseDown(self):
        self.startClickCheckTask()

    def _mouseUp(self):
        self.stopClickCheckTask()
        super(DecoratedMapBall, self)._mouseUp()

    def startClickCheckTask(self):
        taskMgr.add(self.clickCheckTask, self.getName() + '-clickCheck')
        self.dragging = False

    def clickCheckTask(self, task):
        if base.mouseWatcherNode.hasMouse():
            if not hasattr(task, 'mousePt'):
                task.mousePt = Point2(base.mouseWatcherNode.getMouse())
            mousePt = base.mouseWatcherNode.getMouse()
            if mousePt != task.mousePt:
                super(DecoratedMapBall, self)._mouseDown()
                self.dragging = True
                return task.done
        return task.cont

    def stopClickCheckTask(self):
        self.dragging = False
        if taskMgr.remove(self.getName() + '-clickCheck'):
            item = self.pick()
            if not item:
                return
            islandUid = item.getNetTag('islandUid')
            canTeleportTo = item.getNetTag('canTeleportTo') != 'False'
            if islandUid and canTeleportTo:
                base.cr.teleportMgr.d_requestIslandTeleport(islandUid)
            dartName = item.getNetTag('dart')
            dart = self.placedItems.get(dartName)
            if dartName and dart:
                dart.mouseLeft()
                localAvatar.guiMgr.showQuestPanel()

    def pick(self):
        self._mouseRayCollide(BitMask32.bit(17))
        numEntries = self.colHandlerQueue.getNumEntries()
        if numEntries:
            self.colHandlerQueue.sortEntries()
            entry = self.colHandlerQueue.getEntry(0)
            item = entry.getIntoNodePath()
            return item

    @report(types=['frameCount', 'args'], dConfigParam='map')
    def startPickTask(self, *args):
        self.stopPickTask()
        task = taskMgr.add(self.pickTask, self.getName() + '-pickTask')
        task.activeIsland = None
        task.activeDart = None
        return

    def pickTask(self, task):
        if base.mouseWatcherNode.hasMouse():
            item = self.pick()
            if item and not self.dragging:
                islandUid = item.getNetTag('islandUid')
                dartName = item.getNetTag('dart')
                island = self.placedIslands.get(islandUid)
                dart = self.placedItems.get(dartName)
            else:
                islandUid = ''
                dartName = ''
                island = None
                dart = None
            if task.activeIsland and task.activeIsland != island:
                self.leftIsland(task.activeIsland)
                task.activeIsland = None
            if not task.activeIsland and island:
                self.overIsland(island)
                task.activeIsland = island
            if task.activeDart and task.activeDart != dart:
                task.activeDart.mouseLeft()
                task.activeDart = None
            if not task.activeDart and dart:
                p = Point2()
                self.camLens.project(self.cam.getRelativePoint(dart, Point3(0, 0, 0)), p)
                pos = aspect2d.getRelativePoint(self.worldMap, Point3(p[0], 0, p[1]))
                dart.mouseOver(pos)
                task.activeDart = dart
        return task.cont

    @report(types=['frameCount', 'args'], dConfigParam='map')
    def stopPickTask(self, *args):
        tasks = taskMgr.getTasksNamed(self.getName() + '-pickTask')
        if tasks:
            task = tasks[0]
            if task.activeIsland:
                self.leftIsland(task.activeIsland)
        for task in tasks:
            taskMgr.remove(task)

    def overIsland(self, island):
        p = Point2()
        self.camLens.project(self.cam.getRelativePoint(island, Point3(0, 0, 0)), p)
        pos = aspect2d.getRelativePoint(self.worldMap, Point3(p[0], 0, p[1]))
        island.mouseOver(pos)

    def leftIsland(self, island):
        island.mouseLeft()

    def initGlobalStencil(self):
        globalStencilAttrib = StencilAttrib.make(1, StencilAttrib.SCFAlways, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOReplace, 255, 4294967295L, 4294967295L)

    def addAndPlaceItem(self, name, info):
        self.setItemInfo(name, info)
        item = self.createDecorItem(name)
        self.placeDecorItem(name, item)

    def setItemInfo(self, name, info):
        self.decorInfo[name] = info

    def createDecorItem(self, name):
        self.itemCounter += 1
        decorType, args, options = self.decorInfo[name]
        item = DecorClasses[decorType](*args)
        if options.get('coordinateSpace', 'map') == 'map':
            pos = options.get('pos', Point2(0))
            if pos:
                worldPos = self.mapPosToSpherePt(pos)
                height = options.get('height', 0.0)
                newPos = worldPos * (1.01 + height)
                item.setPosition(self._worldNorth, newPos)
        rot = options.get('rot')
        if rot is not None:
            item.setRotation(self._worldNorth, rot)
        return item

    def updateDecorItem(self, name):
        decorType, args, options = self.decorInfo[name]
        item = self.placedItems.get(name)
        if item:
            if options.get('coordinateSpace', 'map') == 'map':
                pos = options.get('pos', Point2(0))
                if pos:
                    worldPos = self.mapPosToSpherePt(pos)
                    height = options.get('height', 0.0)
                    newPos = worldPos * (1.01 + height)
                    item.setPosition(self._worldNorth, newPos)
            rot = options.get('rot')
            if rot is not None:
                item.setRotation(self._worldNorth, rot)
        return

    def placeDecorItem(self, name, item):
        newItem = self.placedItems.setdefault(name, item)
        if item is not newItem:
            pass
        if isinstance(newItem, DecorClasses[DecorTypes.Dart]):
            self.billboardList.append(newItem)
        self.attachForRotation(newItem)

    def getDecorItem(self, name):
        return self.placedItems.get(name)

    def resetDecor(self):
        for name in self.placedItems.keys():
            self.removeDecorItem(name)

        for name in self.decorInfo:
            item = self.createDecorItem(name)
            self.placeDecorItem(name, item)

    def removeDecorItem(self, name):
        item = self.placedItems.pop(name, None)
        if item:
            if isinstance(item, DecorClasses[DecorTypes.Dart]):
                self.billboardList.remove(item)
                if item.helpBox:
                    item.helpBox.destroy()
                if item.helpLabel:
                    item.helpLabel.destroy()
            item.destroy()
            item.removeNode()
        return

    def setDecorScale(self, scale):
        self._setTiltLimit(math.pi / 3 * scale)
        self.resetDecor()

    def startBillboardTask(self):
        taskName = self.getName() + '-billboardTask'
        taskMgr.remove(taskName)
        taskMgr.add(self.billboardTask, taskName)

    def billboardTask(self, task):
        for nodepath in self.billboardList:
            nodepath.doBillboardPointEye(self.cam, 0.0)

        return task.cont

    def stopBillboardTask(self):
        taskMgr.remove(self.getName() + '-billboardTask')

    def startDartTask(self):
        taskName = self.getName() + '-dartTask'
        taskMgr.remove(taskName)
        taskMgr.add(self.dartTask, taskName)

    def dartTask(self, task):
        for dart in self.dartList:
            desiredPos = dart.getDefaultPos()
            newPos, theta = self.clampSpherePtToHorizon(desiredPos)
            framePos = self._transSphereToFramePt(newPos)
            if -1.1 < framePos[0] < 1.1 and -1.1 < framePos[1] < 1.1:
                dart.setEdgeMode(False)
                dart.setPos(newPos)
                if theta:
                    theta = clampScalar(0, math.pi / 4, theta)
                    dart.setScale(-2 * theta / math.pi + 1)
                else:
                    dart.setScale(1)
            else:
                dart.setPos(newPos)
                angle = math.atan2(-framePos[0], -framePos[1])
                angle = angle * 180 / math.pi
                dart.setEdgeMode(True)
                dart.edgeModeNode.setR(angle)
                absFramePos = (
                 abs(framePos[0]), abs(framePos[1]))
                markerFramePos = framePos / max(absFramePos)
                dart.edgeModeNode.setPos(markerFramePos[0], 0, markerFramePos[1])

        return task.cont

    def stopDartTask(self):
        taskMgr.remove(self.getName() + '-dartTask')

    def updateTextZoom(self, zoom):
        for item in self.placedItems.values():
            if isinstance(item, DecorClasses[DecorTypes.TextIsland]) or isinstance(item, DecorClasses[DecorTypes.OceanAreaText]) or isinstance(item, DecorClasses[DecorTypes.Ship]):
                item.updateZoom(zoom)

    def updateTeleportIsland(self, teleportToken):
        inventory = localAvatar.getInventory()
        islandUid = InventoryType.getIslandUidFromTeleportToken(teleportToken)
        island = self.getIsland(islandUid)
        if island and teleportToken:
            island.setHasTeleportToken(localAvatar.hasIslandTeleportToken(islandUid))

    def setReturnIsland(self, islandUid):
        for item in self.placedItems.itervalues():
            if item.hasNetTag('islandUid'):
                if islandUid and islandUid == item.getNetTag('islandUid'):
                    item.setAsReturnIsland(1)
                else:
                    item.setAsReturnIsland(0)

    def setPortOfCall(self, islandUid):
        for item in self.placedItems.itervalues():
            if item.hasNetTag('islandUid'):
                if islandUid and islandUid == item.getNetTag('islandUid'):
                    item.setAsPortOfCall(1)
                else:
                    item.setAsPortOfCall(0)

    def setCurrentIsland(self, islandUid):
        for item in self.placedItems.itervalues():
            if item.hasNetTag('islandUid'):
                if islandUid and islandUid == item.getNetTag('islandUid'):
                    item.setAsCurrentIsland(1)
                else:
                    item.setAsCurrentIsland(0)

    def getCurrentIsland(self):
        for item in self.placedItems.itervalues():
            if item.hasNetTag('islandUid') and item.isCurrentIsland():
                return item

        return None

    def getIsland(self, islandUid):
        island = None
        for item in self.placedItems.itervalues():
            if item.hasNetTag('islandUid'):
                if islandUid and islandUid == item.getNetTag('islandUid'):
                    island = item
                    break

        return island

    def getCurrentShip(self):
        for item in self.placedItems.itervalues():
            if item.hasNetTag('shipName'):
                return item

        return None

    def rotateAvatarToCenter(self):
        island = self.getCurrentIsland()
        if island:
            self.rotateSpherePtToCenter(island.getPos())
        else:
            ship = self.getCurrentShip()
            if ship:
                self.rotateSpherePtToCenter(ship.getPos())

    def addOceanArea(self, name, areaUid, pos1, pos2):
        worldPos = (pos1 + pos2) / 2.0
        if OceanAreaOffsets.get(name):
            worldPos.setY(worldPos.getY() + OceanAreaOffsets[name][1] * WorldGlobals.OCEAN_CELL_SIZE)
        info = (
         DecorTypes.OceanAreaText, (name, areaUid), {'pos': worldPos,'rot': 0})
        self.addAndPlaceItem(name, info)

    def getShipId(self, shipDoId):
        return 'ship-%d' % shipDoId

    def addShip(self, shipInfo, worldPos):
        name = self.getShipId(shipInfo[0])
        info = (DecorTypes.Ship, (shipInfo,), {'pos': worldPos,'rot': 0})
        self.addAndPlaceItem(name, info)

    def updateShip(self, shipDoId, worldPos, rotation):
        name = self.getShipId(shipDoId)
        shipInfo = self.decorInfo.get(name)
        if shipInfo:
            options = shipInfo[2]
            if worldPos is not None:
                options['pos'] = worldPos
            if rotation is not None:
                options['rot'] = rotation
            self.updateDecorItem(name)
        return

    def removeShip(self, shipDoId):
        name = self.getShipId(shipDoId)
        ship = self.placedItems.pop(name, None)
        if ship:
            ship.removeNode()
            ship.remove()
        return

    def getFleetId(self, fleetDoId):
        return 'fleet-%d' % fleetDoId

    def addFleet(self, fleetObj, pos=(0, 0, 0)):
        name = self.getFleetId(fleetObj.getDoId())
        info = (
         DecorTypes.BillboardCard, (name, fleetObj.mapIconInfo[0], fleetObj.mapIconInfo[1], self.cam, 0.0, fleetObj.mapIconInfo[2]), {'pos': pos})
        self.addAndPlaceItem(name, info)

    def updateFleet(self, fleetDoId, pos):
        name = self.getFleetId(fleetDoId)
        fleetInfo = self.decorInfo.get(name)
        if fleetInfo:
            options = fleetInfo[2]
            options['pos'] = pos
            self.updateDecorItem(name)

    def removeFleet(self, fleetDoId):
        name = self.getFleetId(fleetDoId)
        fleet = self.placedItems.pop(name, None)
        if fleet:
            fleet.removeNode()
            fleet.remove()
        return

    def addPath(self, pathInfo):
        startWaypointId = pathInfo[0]
        progressIds = pathInfo[1]
        name = 'Path-%s' % startWaypointId
        verts = []
        color = (128 / 255.0, 37 / 255.0, 21 / 255.0, 1)
        waypointIds = [startWaypointId]
        usedWayPoints = []
        looped = 0
        isLoop = 0
        ended = 0
        lastWaypointId = None
        waypointId = startWaypointId
        while not isLoop and not ended:
            waypointIds = base.worldCreator.getWaypointLinks(waypointId)
            if not waypointIds:
                ended = 1
            else:
                nextWaypointId = waypointIds[0]
                if startWaypointId == nextWaypointId:
                    lastWaypointId = waypointId
                    color = (128 / 255.0, 37 / 255.0, 21 / 255.0, 0.25)
                    isLoop = 1
                waypointId = nextWaypointId

        looped = 0
        if lastWaypointId:
            pos = base.worldCreator.getWaypointPos(lastWaypointId)
            if pos:
                pos = (
                 pos[0], pos[1], pos[2])
                pos = self.mapPosToSpherePt(pos)
                color = (128 / 255.0, 37 / 255.0, 21 / 255.0, 0.0)
                verts.append({'node': None,'point': pos,'color': color})
                color = (128 / 255.0, 37 / 255.0, 21 / 255.0, 0.25)
        waypointIds = [
         startWaypointId]
        while waypointIds and not looped:
            waypointId = waypointIds[0]
            if waypointId in usedWayPoints:
                looped = 1
                color = (128 / 255.0, 37 / 255.0, 21 / 255.0, 0.0)
            usedWayPoints.append(waypointId)
            pos = base.worldCreator.getWaypointPos(waypointId)
            if pos:
                pos = (
                 pos[0], pos[1], pos[2])
                pos = self.mapPosToSpherePt(pos)
                verts.append({'node': None,'point': pos,'color': color})
            if waypointId in progressIds and not isLoop:
                color = (
                 color[0], color[1], color[2], color[3] * 0.125)
            waypointIds = base.worldCreator.getWaypointLinks(waypointId)

        if looped:
            pos = base.worldCreator.getWaypointPos(startWaypointId)
            if pos:
                pos = (
                 pos[0], pos[1], pos[2])
                pos = self.mapPosToSpherePt(pos)
                color = (128 / 255.0, 37 / 255.0, 21 / 255.0, 0.0)
                verts.append({'node': None,'point': pos,'color': color})
        info = (DecorTypes.Spline, (name, verts), {'coordinateSpace': 'sphere'})
        self.addAndPlaceItem(name, info)
        item = self.placedItems.get(name)
        return

    def removePath(self, pathInfo):
        startWaypointId = pathInfo[0]
        name = 'Path-%s' % startWaypointId
        path = self.placedItems.pop(name, None)
        if path:
            path.removeNode()
            path.remove()
        return

    def addIsland(self, name, islandUid, modelPath, worldPos, rotation):
        scale = 25.0
        if not name:
            name = 'island-' + `(self.itemCounter)`
            info = (DecorTypes.Island, (name, islandUid, modelPath, False, scale), {'pos': worldPos,'rot': rotation})
        else:
            isTeleportable = islandUid != LocationIds.KINGSHEAD_ISLAND and not base.cr.distributedDistrict.worldCreator.isMysteriousIslandByUid(islandUid) and (bool(InventoryType.getIslandTeleportToken(islandUid)) or base.cr.distributedDistrict.worldCreator.isPvpIslandByUid(islandUid))
            info = (
             DecorTypes.TextIsland, (name, islandUid, modelPath, isTeleportable, self.cam, 0.001, scale), {'pos': worldPos,'rot': rotation})
        self.addAndPlaceItem(name, info)
        self.placedIslands[islandUid] = self.placedItems[name]
        return name

    def updateIsland(self, name, worldPos=None, rotation=None):
        islandInfo = self.decorInfo.get(name)
        if islandInfo:
            options = islandInfo[2]
            if worldPos is not None:
                options['pos'] = worldPos
            if rotation is not None:
                options['rot'] = rotation
            self.updateDecorItem(name)
        return

    def removeIsland(self, name):
        island = self.placedItems.pop(name, None)
        if island:
            islandUid = island.getTag('islandUid')
            island.removeNode()
            island.remove()
        return

    def addDart(self, id, worldPos, color=Vec4(0.2, 1, 0.6, 1.0)):
        name = 'dart-' + str(id)
        info = (DecorTypes.Dart, (name, self, self.mapPosToSpherePt(worldPos), color, 0.001), {'pos': worldPos})
        self.addAndPlaceItem(name, info)
        self.questDartPlaced = True
        self.questDartName = name
        return name

    def removeDart(self):
        if self.questDartName is not None:
            self.removeDecorItem(self.questDartName)
            self.questDartName = None
            self.questDartPlaced = False
        return

    def updateDartText(self, name, questId):
        dart = self.placedItems.get(name)
        if dart and questId:
            qs = localAvatar.getQuestById(questId)
            if qs:
                title = qs.getStatusText()
                dart.setHelpLabel(title)

    def updateDart(self, id, worldPos=None):
        name = 'dart-' + str(id)
        dartInfo = self.decorInfo.get(name)
        dart = self.placedItems.get(name)
        if dartInfo:
            options = dartInfo[2]
            if worldPos is not None:
                options['pos'] = worldPos
            self.updateDecorItem(name)
        return

    def setDecorInfo(self):
        if __dev__ and 0:
            self.decorInfo = {'BilgeWater': (DecorTypes.TextIsland, ('BilgeWater', 'models/worldmap/world_map_island_3d', self.cam, 0.001, 1.0, 1), {'pos': Point2(-0.1, -0.1) * 20000}),'Tortuga': (DecorTypes.TextIsland, ('Tortuga', 'models/worldmap/world_map_island_3d', self.cam, 0.001, 1.0, 2), {'pos': Point2(0.2, 0.2) * 20000}),'swirl': (DecorTypes.Swirl, ('models/worldmap/swirl', 1.0, 2), {'pos': Point2(0.0, 0.0) * 20000}),'ship': (DecorTypes.BillboardModel, ('ship', 'models/worldmap/world_map_ship', self.cam, 0.0, 1.0 / 80), {'pos': Point2(0.2, 0.0) * 20000}),'monster': (DecorTypes.BillboardModel, ('monster', 'models/worldmap/world_map_monster01', self.cam, 0.001, 1.0 / 200), {'pos': Point2(0.0, 0.1) * 20000}),'BilgeWater2': (DecorTypes.TextIsland, ('BilgeWater2', 'models/worldmap/world_map_island_3d', self.cam, 0.001, 1.0, 1), {'pos': Point2(0.25, -0.15) * 20000}),'Tortuga2': (DecorTypes.TextIsland, ('Tortuga2', 'models/worldmap/world_map_island_3d', self.cam, 0.001, 1.0, 2), {'pos': Point2(-0.4, -0.4) * 20000}),'BilgeWater3': (DecorTypes.TextIsland, ('BilgeWater3', 'models/worldmap/world_map_island_3d', self.cam, 0.001, 1.0, 1), {'pos': Point2(0.15, -0.25) * 20000}),'Tortuga3': (DecorTypes.TextIsland, ('Tortuga3', 'models/worldmap/world_map_island_3d', self.cam, 0.001, 1.0, 2), {'pos': Point2(0.2, -0.15) * 20000}),'BilgeWater3': (DecorTypes.TextIsland, ('BilgeWater3', 'models/worldmap/world_map_island_3d', self.cam, 0.001, 1.0, 1), {'pos': Point2(-0.3, 0.1) * 20000}),'Tortuga3': (DecorTypes.TextIsland, ('Tortuga3', 'models/worldmap/world_map_island_3d', self.cam, 0.001, 1.0, 2), {'pos': Point2(0.3, 0.25) * 20000}),'BilgeWater4': (DecorTypes.TextIsland, ('BilgeWater4', 'models/worldmap/world_map_island_3d', self.cam, 0.001, 1.5, 1), {'pos': Point2(-0.1, 0.3) * 20000}),'Tortuga4': (DecorTypes.TextIsland, ('Tortuga4', 'models/worldmap/world_map_island_3d', self.cam, 0.001, 1.0, 2), {'pos': Point2(0.4, 0.4) * 20000}),'BilgeWater5': (DecorTypes.TextIsland, ('BilgeWater4', 'models/worldmap/world_map_island_3d', self.cam, 0.001, 1.0, 1), {'pos': Point2(0.4, -0.4) * 20000}),'Tortuga5': (DecorTypes.TextIsland, ('Tortuga4', 'models/worldmap/world_map_island_3d', self.cam, 0.001, 1.0, 2), {'pos': Point2(-0.4, 0.4) * 20000})}
            self.decorInfo = {'BilgeWater': (DecorTypes.TextIsland, ('BilgeWater', 'models/worldmap/world_map_island_3d', self.cam, 0.001, 1.0, 1), {'pos': Point2(-0.1, -0.1) * 20000}),'smiley': (DecorTypes.Model, ('smiley', 'models/misc/smiley', 0.005), {'pos': Point2(0)})}
        else:
            self.decorInfo = {}

    def toggleQuestDartHelpText(self, task=None):
        dart = self.placedItems.get(self.questDartName)
        if dart is not None:
            dart.toggleHelpText()
        return