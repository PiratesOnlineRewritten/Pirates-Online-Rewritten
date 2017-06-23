from pandac.PandaModules import *
from direct.showbase.PythonUtil import clampScalar, lerp, report
from direct.interval.IntervalGlobal import Sequence, Parallel, LerpFunc, Func, Wait
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from pirates.map.SceneBuffer import SceneBuffer
from pirates.map.DecoratedMapBall import DecoratedMapBall
from pirates.map.MapConfig import MapConfig
import math

class WorldMap(DirectFrame):

    def __init__(self, parent, **kwargs):
        cm = CardMaker('Portrait')
        cm.setFrame(Vec4(-1, 1, -1, 1))
        b = SceneBuffer('worldmap-buffer', size=(512, 512), clearColor=Vec4(0.85))
        b.camLens.setNear(0.001)
        b.camLens.setFar(5.0)
        b.camera.node().getDisplayRegion(0).setIncompleteRender(False)
        self.buffer = b
        shot = NodePath(cm.generate())
        shot.setTexture(b.getTexture(), 1)
        optiondefs = (
         ('relief', None, None), ('geom', shot, None))
        self.defineoptions(kwargs, optiondefs)
        DirectFrame.__init__(self, parent, **kwargs)
        self.initialiseoptions(WorldMap)
        self.setTransparency(1)
        self.radius = 1.0
        self.camY = [
         -0.3, 0.25]
        self.tiltLimit = [ x * math.pi / 180 for x in (27, 33) ]
        self.mapBall = DecoratedMapBall('WorldMapArcBall', self, self.tiltLimit[1], mapSize=242000, radius=self.radius, scrollFactor=0.125, camera=b.camera, keepUpright=1, mouseDownEvent=self.getMouseDownEvent(), mouseUpEvent=self.getMouseUpEvent())
        self.render = b.getSceneRoot()
        self.worldRoot = self.render.attachNewNode('world')
        self.worldRoot.setTransparency(1)
        self.ballRoot = self.worldRoot.attachNewNode('ballRoot')
        self.ballRoot.setY(self.radius / 2.0)
        self.mapBall.reparentTo(self.ballRoot)
        self.mapBall.setInternalHpr(Vec3(0, 90, 0))
        self.mapBall.setNorth(Vec3(0, 1, 0))
        self.mapBall.setY(self.radius)
        self.setZoom(0)
        self.addLocalAvDart()
        self._hasLocalShip = False
        self._fleets = []
        self._enabled = False
        return

    def disable(self):
        self._enabled = False
        if self._hasLocalShip:
            self.stopLocalAvShipPosHprTask()
        for fleetDoId in self._fleets:
            self.stopFleetPosTask(fleetDoId)

        self.stopLocalAvPosTask()
        self.ignoreAll()
        self.mapBall.disable()
        self.buffer.disable()

    def destroy(self):
        self.disable()
        self.buffer.destroy()
        self.stopLocalAvShipPosHprTask()
        self.mapBall.removeNode()
        del self.mapBall
        self.worldRoot.removeNode()
        del self.render
        del self.worldRoot
        DirectFrame.destroy(self)

    def getMouseDownEvent(self):
        return self.getName() + '-worldMap-mouseDown'

    def getMouseUpEvent(self):
        return self.getName() + '-worldMap-mouseUp'

    @report(types=['frameCount', 'args'], dConfigParam='map')
    def enable(self):
        self.resetArcBall()
        self.accept('press-mouse1-%s' % self.guiId, self.mouseDown)
        self.accept('release-mouse1-%s' % self.guiId, self.mouseUp)
        self.accept('press-wheel_up-%s' % self.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.guiId, self.mouseWheelDown)
        self.accept('edge-dart-clicked', self.handleEdgeDartClicked)
        self.accept('enter-%s' % self.guiId, self.mapBall.startPickTask)
        self.accept('exit-%s' % self.guiId, self.mapBall.stopPickTask)
        self.buffer.enable()
        self.mapBall.enable()
        self.startLocalAvPosTask()
        if self._hasLocalShip:
            self.startLocalAvShipPosHprTask()
        for fleetDoId in self._fleets:
            self.startFleetPosTask(fleetDoId)

        self._enabled = True

    def rotateAvatarToCenter(self):
        self.mapBall.rotateAvatarToCenter()

    def mouseDown(self, *args, **kwargs):
        self.resetArcBall()
        messenger.send(self.getMouseDownEvent())

    def mouseUp(self, *args, **kwargs):
        messenger.send(self.getMouseUpEvent())

    def setScale(self, *args, **kwargs):
        DirectFrame.setScale(self, *args, **kwargs)
        self.resetArcBall()

    def setPos(self, *args, **kwargs):
        DirectFrame.setPos(self, *args, **kwargs)
        self.resetArcBall()

    def resetArcBall(self):
        if hasattr(self, 'mapBall'):
            frameSize = Vec4(-1, 1, -1, 1)
            scale = self.getScale(aspect2d)
            pos = self.getPos(aspect2d)
            ts = TransformState.makePosRotateScale2d(Point2(pos[0], pos[2]), 0, Vec2(scale[0], scale[2]))
            botLeft = Point3(frameSize[0], frameSize[2], 0)
            topRight = Point3(frameSize[1], frameSize[3], 0)
            botLeft = ts.getMat().xformPoint(botLeft)
            topRight = ts.getMat().xformPoint(topRight)
            self.mapBall.setFrame(Vec4(botLeft[0], topRight[0], botLeft[1], topRight[1]))

    def setZoom(self, zoom):
        self._zoom = clampScalar(0.0, 0.75, zoom)
        self.buffer.camera.setY(lerp(self.camY[0], self.camY[1], self._zoom))
        self.mapBall._setTiltLimit(lerp(self.tiltLimit[0], self.tiltLimit[1], self._zoom))
        self.mapBall.updateTextZoom(self._zoom)

    def mouseWheelUp(self, *args, **kwargs):
        self.setZoom(self._zoom + 0.05)

    def mouseWheelDown(self, *args, **kwargs):
        self.setZoom(self._zoom - 0.05)

    def handleEdgeDartClicked(self, dartPos):
        self.mapBall.rotatePtToCenter(dartPos, 1)

    def startLocalAvPosTask(self):
        self.stopLocalAvPosTask()
        taskMgr.add(self.localAvPosTask, 'localAvMapPos')

    def localAvPosTask(self, task):
        world = base.cr.getActiveWorld()
        if world:
            pos = world.getWorldPos(localAvatar)
            if pos:
                self.updateLocalAvDart(pos)
        return task.cont

    def stopLocalAvPosTask(self):
        taskMgr.removeTasksMatching('localAvMapPos')

    def startLocalAvShipPosHprTask(self):
        self.stopLocalAvShipPosHprTask()
        taskMgr.add(self.localAvShipPosHprTask, 'localAvMapShip')

    def localAvShipPosHprTask(self, task):
        world = base.cr.getActiveWorld()
        ship = localAvatar.getCrewShip()
        if ship and not ship.isEmpty() and world:
            pos = world.getWorldPos(ship)
            rotation = 180 + ship.getH(world)
            if pos:
                self.updateShip(ship.doId, pos, rotation)
        return task.cont

    def stopLocalAvShipPosHprTask(self):
        taskMgr.removeTasksMatching('localAvMapShip')

    def getFleetPosTaskName(self, fleetDoId):
        return 'fleet-%s-MapPos' % fleetDoId

    def startFleetPosTask(self, fleetDoId):
        self.stopFleetPosTask(fleetDoId)
        task = taskMgr.add(self.FleetPosTask, self.getFleetPosTaskName(fleetDoId))
        task.fleetDoId = fleetDoId

    def FleetPosTask(self, task):
        world = base.cr.getActiveWorld()
        fleet = base.cr.getDo(task.fleetDoId)
        if world and fleet:
            pos = world.getWorldPos(fleet)
            if pos:
                self.updateFleet(task.fleetDoId, pos)
        return task.cont

    def stopFleetPosTask(self, fleetDoId):
        taskMgr.removeTasksMatching(self.getFleetPosTaskName(fleetDoId))

    def showMapConfig(self):
        if hasattr(self, 'mapConfig'):
            self.mapConfig.show()
            return
        self.mapConfig = MapConfig(relief=DGG.FLAT, frameSize=(-0.02, 0.82, -1, 1), frameColor=(1,
                                                                                                1,
                                                                                                1,
                                                                                                1), pos=(0.7,
                                                                                                         0,
                                                                                                         0.0), scale=0.75)
        self.mapConfig.camSlider['command'] = self.buffer.camera.setY
        self.mapConfig.worldPSlider['command'] = self.ballRoot.setP
        self.mapConfig.worldDecorScaleSlider['command'] = self.mapBall.setDecorScale
        self.mapConfig.saveState0Button['command'] = self.saveState
        self.mapConfig.saveState0Button['extraArgs'] = [0]
        self.mapConfig.saveState1Button['command'] = self.saveState
        self.mapConfig.saveState1Button['extraArgs'] = [1]
        self.saveState()

    def saveState(self, pt=None):
        if pt == 0:
            self.camY[0] = self.buffer.camera.getY()
        elif pt == 1:
            self.camY[1] = self.buffer.camera.getY()
        if hasattr(self, 'mapConfig'):

            def zoom(t):
                self.mapConfig.camSlider['value'] = lerp(self.camY[0], self.camY[1], t)

            self.mapConfig.finalSlider['command'] = zoom
            if pt == 0:
                self.mapConfig.finalSlider['range'] = (
                 0, self.mapConfig.finalSlider['range'][1])
                self.mapConfig.finalSlider['value'] = 0.0
            elif pt == 1:
                self.mapConfig.finalSlider['range'] = (
                 self.mapConfig.finalSlider['range'][0], 1.0)
                self.mapConfig.finalSlider['value'] = 1.0

    def resetMapConfig(self):
        if hasattr(self, 'mapConfig'):
            self.mapConfig.camSlider['value'] = 0
            self.mapConfig.worldYSlider['value'] = self.worldRoot.getY()
            self.mapConfig.worldZSlider['value'] = self.worldRoot.getZ()
            self.mapConfig.worldPSlider['value'] = self.ballRoot.getP()
            self.mapConfig.worldDecorScaleSlider['value'] = self.mapBall.mapScale

    def hideMapConfig(self):
        if hasattr(self, 'mapConfig'):
            self.mapConfig.show()

    def showCollisionDebug(self):
        if hasattr(self, 'collisionBufferFrames') and self.collisionBufferFrames:
            for buffer, frame in self.collisionBufferFrames:
                frame.unstash()
                buffer.enable()

            return
        self.collisionBufferFrames = []
        cm = CardMaker('Side')
        cm.setFrame(Vec4(-1, 1, -1, 1))
        side = SceneBuffer('side-buffer', size=(512, 512), clearColor=Vec4(0, 0, 0, 1), sceneGraph=self.render)
        side.camera.setPos(4, 1, 0)
        side.camera.setH(90)
        shot = NodePath(cm.generate())
        shot.setTexture(side.getTexture(), 1)
        df = DirectFrame(geom=shot, relief=None, parent=aspect2d, scale=0.5, pos=(0.833, 0, -0.5), text='side', text_scale=0.1, text_pos=(-0.75, 0.75, 0), text_fg=(1,
                                                                                                                                                                    1,
                                                                                                                                                                    1,
                                                                                                                                                                    1))
        self.collisionBufferFrames.append((side, df))
        top = SceneBuffer('top-buffer', size=(512, 512), clearColor=Vec4(0, 0, 0, 1), sceneGraph=self.render)
        top.camera.setPos(0, 1, 4)
        top.camera.setP(-90)
        cm.setName('Top')
        shot = NodePath(cm.generate())
        shot.setTexture(top.getTexture(), 1)
        df = DirectFrame(geom=shot, relief=None, parent=aspect2d, scale=0.5, pos=(0.833,
                                                                                  0,
                                                                                  0.5), text='top', text_scale=0.1, text_pos=(-0.75, 0.75, 0), text_fg=(1,
                                                                                                                                                        1,
                                                                                                                                                        1,
                                                                                                                                                        1))
        self.collisionBufferFrames.append((top, df))
        self.mapBall.traverser.showCollisions(self.render)
        colNodes = self.render.findAllMatches('**/camRayNode')
        colNodes.show()
        colNodes = self.render.findAllMatches('**/mouseRayNode')
        colNodes.show()
        self.setPos(-0.5, 0, 0)
        self.setScale(0.825)
        return

    def hideCollisionDebug(self):
        if hasattr(self, 'collisionBufferFrames'):
            for buffer, frame in self.collisionBufferFrames:
                buffer.disable()
                frame.stash()

            self.mapBall.traverser.hideCollisions()
            colNodes = self.render.findAllMatches('**/+CollisionNode')
            colNodes.hide()

    def updateTeleportIsland(self, teleportTokenId):
        self.mapBall.updateTeleportIsland(teleportTokenId)

    def setReturnIsland(self, islandUid):
        self.mapBall.setReturnIsland(islandUid)

    def setPortOfCall(self, islandUid):
        self.mapBall.setPortOfCall(islandUid)

    def setCurrentIsland(self, islandUid):
        self.mapBall.setCurrentIsland(islandUid)

    def addQuestDart(self, questId, worldPos):
        self.mapBall.addDart(questId, worldPos, Vec4(0.7, 0.7, 0, 1))

    def updateQuestDart(self, questId, worldPos):
        self.mapBall.updateDart(questId, worldPos)

    def removeQuestDart(self, questId):
        self.mapBall.removeDart()

    def addLocalAvDart(self, worldPos=Vec3(0)):
        pass

    def updateLocalAvDart(self, worldPos):
        pass

    def addIsland(self, name, islandUid, modelPath, worldPos, rotation):
        return self.mapBall.addIsland(name, islandUid, modelPath, worldPos, rotation)

    def updateIsland(self, name, worldPos=None, rotation=None):
        self.mapBall.updateIsland(name, worldPos, rotation)

    def removeIsland(self, name):
        self.mapBall.removeIsland(name)

    def addOceanArea(self, name, areaUid, pos1, pos2):
        self.mapBall.addOceanArea(name, areaUid, pos1, pos2)

    def addShip(self, shipInfo, worldPos):
        self._hasLocalShip = True
        self.mapBall.addShip(shipInfo, worldPos)
        if self._enabled:
            self.startLocalAvShipPosHprTask()

    def updateShip(self, shipDoId, worldPos, rotation):
        self.mapBall.updateShip(shipDoId, worldPos, rotation)

    def removeShip(self, shipDoId):
        self._hasLocalShip = False
        if self._enabled:
            self.stopLocalAvShipPosHprTask()
        self.mapBall.removeShip(shipDoId)

    def addFleet(self, fleet):
        self.mapBall.addFleet(fleet)
        self._fleets.append(fleet.getDoId())
        if self._enabled:
            self.startFleetPosTask(fleet.getDoId())

    def updateFleet(self, fleetDoId, pos):
        self.mapBall.updateFleet(fleetDoId, pos)

    def removeFleet(self, fleet):
        if self._enabled:
            self.stopFleetPosTask(fleet.getDoId())
        self._fleets.remove(fleet.getDoId())
        self.mapBall.removeFleet(fleet.getDoId())

    def addPath(self, pathInfo):
        self.mapBall.addPath(pathInfo)

    def removePath(self, pathInfo):
        self.mapBall.removePath(pathInfo)