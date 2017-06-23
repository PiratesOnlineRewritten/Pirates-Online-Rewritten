from pandac.PandaModules import NodePath, VBase3
from direct.fsm.FSM import FSM
from pirates.map.Mappable import Mappable, MappableArea, MappableGrid
from pirates.map.MinimapObject import MinimapFootprint, MinimapShop, MinimapCapturePoint
from pirates.ai import HolidayGlobals
from pirates.piratesgui.GameOptions import Options
from pirates.invasion import InvasionGlobals
from pirates.world.LocationConstants import LocationIds

class MapSentry():

    def __init__(self, initFunc, delFunc):
        initFunc()
        self.delFunc = delFunc

    def __del__(self):
        delFunc = self.delFunc
        del self.delFunc
        delFunc()


class Map(FSM):

    def __init__(self, name):
        FSM.__init__(self, name + '-FSM')
        self.objects = set()
        self.observing = 0
        self.sentry = None
        self.radarAxis = base.options.getLandMapRadarAxis()
        self.myUpdateTask = None
        return

    def destroy(self):
        self.stopUpdateTask()
        taskMgr.remove('handleInvasionEnded')

    def startUpdateTask(self):
        self.stopUpdateTask()
        self.myUpdateTask = taskMgr.add(self.updateTask, 'Map-update', priority=47)

    def stopUpdateTask(self):
        if self.myUpdateTask:
            taskMgr.remove(self.myUpdateTask)
            self.myUpdateTask = None
        return

    def updateTask(self, task):
        return task.done

    def addObject(self, object):
        self.objects.add(object)

    def hasObject(self, object):
        return object in self.objects

    def removeObject(self, object):
        self.objects.discard(object)

    def updateRadarTransform(self, transform):
        pass

    def setRadarAxis(self, radarAxis):
        self.radarAxis = radarAxis

    def getRadarAxis(self):
        return self.radarAxis

    def allowOnScreen(self):
        return True

    def enterOpaque(self):
        messenger.send('minimapOpened')
        self.screenNode.show()
        self.screenNode.setAlphaScale(1)
        self.sentry = self.getSentry()

    def filterOpaque(self, request, *args):
        if request == 'next':
            if not base.config.GetBool('want-momentary-minimap', 1):
                return 'Transparent'
            else:
                return 'Off'
        return self.defaultFilter(request, *args)

    def enterTransparent(self):
        self.screenNode.show()
        self.screenNode.setAlphaScale(0.6)
        self.sentry = self.getSentry()

    def filterTransparent(self, request, *args):
        if request == 'next':
            return 'Off'
        return self.defaultFilter(request, *args)

    def enterOff(self):
        self.sentry = None
        if self.screenNode.getParent() == localAvatar.guiMgr.minimapRoot:
            self.screenNode.hide()
        return

    def filterOff(self, request, *args):
        if request == 'next':
            return 'Opaque'
        return self.defaultFilter(request, *args)

    def addObserver(self):
        self.observing += 1
        if self.observing:
            self.startUpdateTask()

    def removeObserver(self):
        self.observing -= 1
        if not self.observing:
            self.stopUpdateTask()

    def getSentry(self):
        return MapSentry(self.addObserver, self.removeObserver)


class AreaMap(Map):

    def __init__(self, area):
        Map.__init__(self, 'map-' + area.getName())
        self.capturePoints = {}
        mapNode = area.getMapNode()
        if mapNode and not mapNode.isEmpty():
            geom = mapNode.getChild(0)
            geom.setScale(mapNode.getScale())
            geom.flattenStrong()
            mapNode.setScale(1)
            self.worldNode = mapNode
            self.map = self.worldNode.copyTo(NodePath())
            a, b = self.map.getTightBounds()
            diff = b - a
            h, w = diff[1], diff[0]
        else:
            self.worldNode = area
            self.map = NodePath('no map found')
            a, b = self.worldNode.geom.getTightBounds()
            diff = b - a
            h, w = diff[1], diff[0]
        ratio = h / w
        if ratio < 0.99:
            normalScale = 2 / w
            screenScale = 1
        else:
            normalScale = 2 / h
            screenScale = 0.75
        self.map.clearTransform()
        self.map.show()
        self.screenNode = NodePath('Minimap-screenNode')
        self.screenNode.setP(90)
        self.screenNode.setScale(screenScale * normalScale)
        self.screenNode.hide()
        self.map.reparentTo(self.screenNode)
        self.mapOverlay = self.map.attachNewNode('mapOverlay')
        self.mapOverlay.wrtReparentTo(self.screenNode)
        self.radarTransformNode = NodePath('radarTransform')
        self.radarTransformNode.setScale(self.worldNode.getScale()[0])
        self.map.instanceTo(self.radarTransformNode)
        localAvatar.guiMgr.addMinimap(self)
        if self.allowOnScreen():
            self.addObject(MinimapFootprint(area))
        self.shops = set()
        if self.allowOnScreen():
            if area.getUniqueId() not in [LocationIds.RAVENS_COVE_ISLAND]:
                for shop in area.getShopNodes():
                    uid = shop.getTag('Uid')
                    shopType = shop.getTag('ShopType')
                    self.addObject(MinimapShop(uid, shop, shopType))

            self.map.findAllMatches('**/=Holiday').stash()
            if base.cr.newsManager:
                for holiday in base.cr.newsManager.getHolidayList():
                    self.handleHolidayStarted(area, HolidayGlobals.getHolidayName(holiday))

        self.zoomLevels = area.getZoomLevels()
        self.accept('landMapRadarAxisChanged', self.setRadarAxis)

    def destroy(self):
        self.ignore('landMapRadarAxisChanged')
        if hasattr(base, 'localAvatar'):
            localAvatar.guiMgr.removeMinimap(self)
        for shop in self.shops:
            self.removeObject(shop)

        self.shops = set()
        for holiday in self.capturePoints.keys():
            zones = self.capturePoints.pop(holiday, {})
            for object in zones.itervalues():
                self.removeObject(object)

        Map.destroy(self)

    def allowOnScreen(self):
        return self.map.find('minimap-card').isEmpty()

    def getZoomLevels(self):
        return self.zoomLevels

    def getWorldNode(self):
        return self.worldNode

    def getScreenNode(self):
        return self.screenNode

    def getOverlayNode(self):
        return self.mapOverlay

    def getCapturePoint(self, holidayId, zone):
        if self.capturePoints.has_key(holidayId):
            return self.capturePoints[holidayId][zone]
        return None

    def updateTask(self, task):
        self.update()
        return task.cont

    def update(self):
        for obj in self.objects:
            obj.updateOnMap(self)

    def addObject(self, object):
        Map.addObject(self, object)
        mapNode = object.getMapNode()
        mapNode.reparentTo(self.map, sort=object.SORT)
        object.getOverlayNode().reparentTo(self.mapOverlay, sort=object.SORT)
        object.addedToMap(self)

    def removeObject(self, object):
        Map.removeObject(self, object)
        object.getMapNode().detachNode()
        object.getOverlayNode().detachNode()
        object.removedFromMap(self)

    def updateRadarTransform(self, av):
        if self.radarAxis == Options.RadarAxisMap:
            self.radarTransformNode.setPosHprScale(-av.getPos(self.worldNode), VBase3(0), VBase3(1))
        else:
            holdHpr = av.getHpr()
            av.setH(camera.getH(render) - self.worldNode.getH(render))
            self.radarTransformNode.setTransform(self.worldNode.getTransform(av))
            av.setHpr(holdHpr)
        localAvatar.guiMgr.radarGui.updateDial(self)

    def getRadarNode(self):
        return self.radarTransformNode

    @report(types=['frameCount', 'args'], dConfigParam='minimap')
    def handleHolidayStarted(self, area, holiday):
        self.map.findAllMatches('**/=Holiday=%s;+s' % (holiday,)).unstash()
        for node in area.getCapturePointNodes(holiday):
            zones = self.capturePoints.setdefault(holiday, {})
            zone = int(node.getTag('Zone'))
            if zone not in zones:
                object = MinimapCapturePoint(node, holiday, zone)
                zones[zone] = object
                self.addObject(object)

    @report(types=['frameCount', 'args'], dConfigParam='minimap')
    def handleHolidayEnded(self, area, holiday, override=False):
        if holiday in InvasionGlobals.INVASION_IDS and not override:
            taskMgr.doMethodLater(10, self.handleInvasionEnded, 'handleInvasionEnded', extraArgs=[area, holiday])
        else:
            self.map.findAllMatches('**/=Holiday=%s;+s' % (holiday,)).stash()
            for object in self.capturePoints.pop(holiday, {}).itervalues():
                self.removeObject(object)

    def handleInvasionEnded(self, area, holiday):
        if not localAvatar.guiMgr.invasionScoreboard:
            self.map.findAllMatches('**/=Holiday=%s;+s' % (holiday,)).stash()
            for object in self.capturePoints.pop(holiday, {}).itervalues():
                self.removeObject(object)


class GridMap(AreaMap):

    def __init__(self, grid):
        AreaMap.__init__(self, grid)
        self.cellWidth, self.cellRadius = grid.getGridParameters()

    def getGridParameters(self):
        return (
         self.cellWidth, self.cellRadius)


class IslandMap(GridMap):

    def __init__(self, island):
        GridMap.__init__(self, island)


class InteriorMap(GridMap):

    def __init__(self, interior):
        GridMap.__init__(self, interior)


class OceanMap(GridMap):

    def __init__(self, name):
        GridMap.__init__(self, name)
        self.setRadarAxis(base.options.getOceanMapRadarAxis())
        self.ignore('landMapRadarAxisChanged')
        self.accept('oceanMapRadarAxisChanged', self.setRadarAxis)

    def destroy(self):
        self.ignore('oceanMapRadarAxisChanged')
        GridMap.destroy(self)

    def allowOnScreen(self):
        return False

    def addObject(self, obj):
        GridMap.addObject(self, obj)
        obj.doUpdateOnZoom(localAvatar.guiMgr.radarGui.radius)

    def removeObject(self, obj):
        obj.stopUpdateOnZoom()
        GridMap.removeObject(self, obj)