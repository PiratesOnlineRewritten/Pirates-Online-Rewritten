from pandac.PandaModules import *
from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.DistributedNode import DistributedNode
from direct.distributed.StagedObject import StagedObject
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import report
from otp.otpbase import OTPRender
from pirates.effects.EnvironmentEffects import EnvironmentEffects
from pirates.map.MinimapObject import MinimapObject
from pirates.audio import SoundGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.world import GridAreaBuilder

class DistributedTunnel(DistributedNode, StagedObject):
    L_WORLD_STACK = 0
    L_AREA_UID = 1
    L_AREA_NODE = 2
    L_LINK_NODE = 3
    notify = directNotify.newCategory('DistributedTunnel')

    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        NodePath.__init__(self, 'DistributedTunnel')
        StagedObject.__init__(self, StagedObject.OFF)
        self.uniqueId = ''
        self.fakeZoneId = PiratesGlobals.FakeZoneId
        self.GridLOD = {}
        self.visNodes = {}
        self.geom = None
        self.envEffects = None
        self._links = {}
        self.areaWorldZone = [
         None, None]
        self.areaNode = [None, None]
        self.__loadedArea = None
        self.areaIndexLoading = None
        self.pendingAreaUnload = False
        self.pendingArea = None
        self.minimapObj = None
        self.builder = GridAreaBuilder.GridAreaBuilder(self)
        self.connectorNodes = [
         'portal_connector_1', 'portal_connector_2']
        self.connectorNodePosHpr = []
        self.ambientNames = [None, None]
        self.avatarZoneContext = None
        self.floorIndex = -1
        self._inTransition = False
        self.ownHandles = []
        return

    def announceGenerate(self):
        DistributedNode.announceGenerate(self)
        if self.cr.activeWorld == None or self.cr.activeWorld.getType() != PiratesGlobals.INSTANCE_PVP:
            self.setupCollisions()
        self.geom.hide(OTPRender.MainCameraBitmask)
        self.geom.showThrough(OTPRender.EnviroCameraBitmask)
        return

    def delete(self):
        self.goOffStage()
        self.fadeoutAllAmbient()
        self.destroyMinimapObject()
        self.cr.relatedObjectMgr.abortRequest(self.pendingArea)
        self.pendingArea = None
        self.setLoadedArea(None)
        for node in self.visNodes.values():
            node.detachNode()

        self.visNodes = {}
        if self.fakeZoneId != None:
            for node in self.GridLOD.values():
                node.cleanup()

            del self.GridLOD
        del self.fakeZoneId
        self.removeNode()
        self.ignoreAll()
        self.builder.delete()
        DistributedNode.delete(self)
        return

    def setLoadedArea(self, area):
        if self.__loadedArea and self.__loadedArea.isGenerated():
            self.__loadedArea.builder.removeLargeObj(self.visNodes[self.__loadedArea.getUniqueId()], self.uniqueId)
        if area:
            self.__loadedArea = area
            self.__loadedArea.builder.addLargeObj(self.visNodes[self.__loadedArea.getUniqueId()], self.uniqueId)

    def getLoadedArea(self):
        return self.__loadedArea

    def setLinks(self, links):
        for link in links:
            sideIndex = self.connectorNodes.index(link[self.L_LINK_NODE])
            self._links[sideIndex] = link
            self.visNodes.setdefault(link[self.L_AREA_UID], NodePath('vis-%s-%s' % (self.uniqueId, link[self.L_AREA_UID])))

        self.calcAmbientNames()
        self.setupConnectorNodes()

    def calcAmbientNames(self):
        self.ambientNames = [ self.calcOneAmbientName(self._links[index][self.L_AREA_NODE]) for index in (0,
                                                                                                          1) ]

    @report(types=['deltaStamp', 'args'], dConfigParam='connector')
    def calcOneAmbientName(self, area):
        return SoundGlobals.getAmbientFromStr(area.split('_')[-1]) or SoundGlobals.getAmbientFromStr(self.modelPath.split('_')[1])

    def fadeInAmbient(self, index):
        if self.ambientNames[index]:
            base.ambientMgr.requestChangeVolume(self.ambientNames[index], duration=0.1, finalVolume=PiratesGlobals.DEFAULT_AMBIENT_VOLUME_NEAR)

    def fadeOutAmbient(self, index):
        if self.ambientNames[index]:
            base.ambientMgr.requestFadeOut(self.ambientNames[index], duration=0.01)
        if self.ambientNames[1 - index]:
            base.ambientMgr.requestChangeVolume(self.ambientNames[1 - index], duration=0, finalVolume=0)

    def fadeoutAllAmbient(self):
        for ambientName in self.ambientNames:
            if ambientName:
                base.ambientMgr.requestFadeOut(ambientName)

    @report(types=['args'], dConfigParam='connector')
    def setupConnectorNodes(self):
        locatorNodes = [ self.find('**/' + locator) for locator in self.connectorNodes ]
        self.connectorNodePosHpr = [ [self.getPos(node), self.getHpr(node)] for node in locatorNodes ]

    def setupCollisions(self):
        floorNames = [
         'collision_floor_1', 'collision_floor_2', 'collision_floor_middle']
        for x, floorName in enumerate(floorNames):
            floor = self.find('**/' + floorName)
            floor.setName(self.uniqueName(floorName))
            floorNames[x] = floor.getName()
            self.accept('enterFloor' + floor.getName(), self.__handleOnFloor, extraArgs=[x])

    @report(types=['deltaStamp', 'args'], dConfigParam='connector')
    def __handleOnFloor(self, areaIndex, collEntry):
        if not self._inTransition:
            self.floorIndex = 1 - areaIndex
            self._inTransition = True
            area = self.getLoadedArea()
            entranceNode = self.getEntranceNode(area)
            if collEntry:
                self.acceptOnce('EnterTunnelFinished', self.transitionToArea, extraArgs=[self.floorIndex])
                localAvatar.b_setGameState('EnterTunnel', [entranceNode])
            else:
                self.transitionToArea(self.floorIndex)

    @report(types=['deltaStamp', 'args'], dConfigParam='connector')
    def transitionToArea(self, areaIndex):
        areaUid = self._links[areaIndex][self.L_AREA_UID]
        self.cr.loadingScreen.showTarget(areaUid)
        self.cr.loadingScreen.showHint(areaUid)
        localAvatar.b_setLocation(self.cr.distributedDistrict.getDoId(), PiratesGlobals.QuietZone)
        localAvatar.detachNode()
        self.currTransParent, self.currTransZone = self.getLocation()

        def continueTransition():
            self.acceptOnce('activeTunnel-%s-complete' % self.getDoId(), continueTransition)
            currParentObj = self.cr.doId2do.get(self.currTransParent)
            if currParentObj:
                self.currTransParent, self.currTransZone = currParentObj.getLocation()
                self.ownHandles.append(self.cr.addTaggedInterest(self.currTransParent, self.currTransZone, self.cr.ITAG_GAME, 'activeTunnelParent-%s' % self.getDoId(), event='activeTunnel-%s-complete' % self.getDoId()))
            else:
                self.cr.activeWorld.goOffStage([self.getLoadedArea()])
                self.d_requestArea(areaIndex)
                localAvatar.refreshActiveQuestStep(forceClear=True)
                localAvatar.lastConnectorId = self.doId

        self.acceptOnce('activeTunnel-%s-complete' % self.getDoId(), continueTransition)
        self.ownHandles.append(self.cr.addTaggedInterest(self.currTransParent, self.currTransZone, self.cr.ITAG_GAME, 'activeTunnel-%s' % self.getDoId(), event='activeTunnel-%s-complete' % self.getDoId()))

    @report(types=['frameCount'], dConfigParam='connector')
    def handleOnStage(self):
        StagedObject.handleOnStage(self)
        self.startCustomEffects()

    @report(types=['frameCount'], dConfigParam='connector')
    def handleOffStage(self):
        self.stopCustomEffects()
        StagedObject.handleOffStage(self)

    def setUniqueId(self, uid):
        if self.uniqueId:
            self.cr.uidMgr.removeUid(self.uniqueId)
        self.uniqueId = uid
        self.cr.uidMgr.addUid(self.uniqueId, self.getDoId())

    def getUniqueId(self):
        return self.uniqueId

    @report(types=['frameCount', 'args'], dConfigParam='connector')
    def reparentConnectorToArea(self, area):
        self.notify.debug('%s reparentConnectorToArea %s' % (self.doId, area))
        entranceNode = self.getEntranceNode(area)
        entranceNode.setScale(1)
        entranceNode.setP(0)
        entranceNode.setR(0)
        rootNode = self.visNodes[area.uniqueId]
        rootNode.reparentTo(area)
        rootNode.setTransform(entranceNode.getTransform(area))
        self.reparentTo(entranceNode)
        pos, hpr = self.connectorNodePosHpr[self.getAreaIndex(area)]
        self.setPos(pos)
        self.setHpr(hpr[0], 0, 0)
        self.wrtReparentTo(rootNode)
        self.setLoadedArea(area)
        if area.showTunnelOnMinimap(self.getUniqueId()):
            obj = self.getMinimapObject(entranceNode)
            area.addMinimapObject(obj)
            obj.updateWorldNode(entranceNode)

    def setModelPath(self, modelPath):
        self.notify.debug('setModelPath %s' % modelPath)
        self.modelPath = modelPath
        self.loadModel()

    def loadModel(self):
        if not self.geom:
            self.loadWholeModel()
            self.geom.flattenStrong()
            self.geom.reparentTo(self)

    def loadWholeModel(self):
        modelBaseName = self.modelPath
        self.geom = loader.loadModel(modelBaseName)

    def getAreaIndex(self, area):
        areaUid = area.getUniqueId()
        for x in (0, 1):
            if areaUid == self._links[x][self.L_AREA_UID]:
                return x

        return None

    def getAreaObject(self, index):
        areaUid = self._links[index][self.L_AREA_UID]
        areaDoId = self.cr.uidMgr.getDoId(areaUid)
        return self.cr.doId2do.get(areaDoId)

    def getConnectorNodePosHpr(self, index):
        if index < len(self.connectorNodePosHpr):
            return self.connectorNodePosHpr[index]
        return (Point3(0), Vec3(0))

    def getAreaNodeNameFromAreaUid(self, areaUid):
        for link in self._links.itervalues():
            if areaUid == link[self.L_AREA_UID]:
                return link[self.L_AREA_NODE]

        return None

    def getEntranceNode(self, area):
        areaIndex = self.getAreaIndex(area)
        areaNode = self._links[areaIndex][self.L_AREA_NODE]
        return area.find('**/' + areaNode + '*')

    @report(types=['frameCount', 'args'], dConfigParam='connector')
    def d_requestArea(self, linkIndex):
        self.sendUpdate('requestArea', [self._links[linkIndex][self.L_LINK_NODE]])

    @report(types=['frameCount', 'args'], dConfigParam='connector')
    def setArea(self, worldStack, areaDoId, autoFadeIn=True):
        self.cr.setWorldStack(worldStack, event='WorldOpen')

        @report(types=['frameCount', 'args'], dConfigParam='connector')
        def areaFinishedCallback(area):
            self.pendingArea = None
            self.loadAreaFinished(area, autoFadeIn)
            return

        self.cr.relatedObjectMgr.abortRequest(self.pendingArea)
        self.pendingArea = self.cr.relatedObjectMgr.requestObjects([areaDoId], eachCallback=areaFinishedCallback)

    @report(types=['deltaStamp', 'args'], dConfigParam='connector')
    def loadAreaFinished(self, area, autoFadeIn=True):

        def handleFinished():
            for currHandle in self.ownHandles:
                self.cr.removeTaggedInterest(currHandle)

            self.ownHandles = []

        self.acceptOnce('EnterTunnelFinished', handleFinished)

        @report(types=['deltaStamp', 'args'], dConfigParam='connector')
        def leaveTunnel():
            if autoFadeIn:

                def leaveTunnelFinished():
                    self._inTransition = False
                    area.forceManagePass(localAvatar)
                    localAvatar.sendCurrentPosition()

                self.acceptOnce('LeaveTunnelFinished', leaveTunnelFinished)
                localAvatar.b_setGameState('LeaveTunnel', [self, area, not autoFadeIn])
            else:

                def leaveTunnelFinished():
                    self.sendUpdate('sendLeaveTunnelDone')
                    area.forceManagePass(localAvatar)
                    localAvatar.sendCurrentPosition()

                localAvatar.b_setGameState('LeaveTunnel', [self, area, not autoFadeIn])
                self.cr.setAllInterestsCompleteCallback(leaveTunnelFinished)
            area.handleEnterGameArea()
            self.fadeInAmbient(self.floorIndex)

        world = area.getParentObj()
        world.goOnStage()
        area.goOnStage()
        self.cr.setAllInterestsCompleteCallback(leaveTunnel)

    def startCustomEffects(self):
        self.stopCustomEffects()
        self.envEffects = EnvironmentEffects(self.geom, self.modelPath)

    def stopCustomEffects(self):
        if self.envEffects:
            self.envEffects.delete()
            self.envEffects = None
        return

    def getMinimapObject(self, worldNode):
        if not self.minimapObj and not self.isDisabled():
            self.minimapObj = MinimapTunnel(worldNode)
        return self.minimapObj

    def destroyMinimapObject(self):
        if self.minimapObj:
            self.minimapObj.removeFromMap()
            self.minimapObj = None
        return

    def quickLoadOtherSide(self):
        self.cr.loadingScreen.show(waitForLocation=True)
        if self.floorIndex != -1:
            self._inTransition = False
            self.__handleOnFloor(self.floorIndex, None)
        return


class MinimapTunnel(MinimapObject):
    ICON = None
    OUTOFRANGE_ICON = None

    def __init__(self, worldNode):
        if not MinimapTunnel.ICON:
            compass = loader.loadModel('models/gui/compass_main')
            MinimapTunnel.ICON = compass.find('**/icon_rectangle_hollow').getChild(0).copyTo(NodePath('tunnel'))
            MinimapTunnel.ICON.clearTransform()
            MinimapTunnel.ICON.setHpr(90, 90, 0)
            MinimapTunnel.ICON.setScale(300)
            MinimapTunnel.ICON.flattenStrong()
            MinimapTunnel.OUTOFRANGE_ICON = compass.find('**/icon_rectangle_hollow').getChild(0).copyTo(NodePath('tunnel-outofrange'))
            MinimapTunnel.OUTOFRANGE_ICON.clearTransform()
            MinimapTunnel.OUTOFRANGE_ICON.setPosHpr(1, 0, 0, 0, 0, 90)
            MinimapTunnel.OUTOFRANGE_ICON.flattenStrong()
        MinimapObject.__init__(self, 'tunnel', worldNode, self.ICON)
        self.outOfRangeGeom = NodePath('outOfRange')
        icon = MinimapTunnel.OUTOFRANGE_ICON.copyTo(self.outOfRangeGeom)

    def updateWorldNode(self, worldNode):
        self.worldNode = worldNode
        if self.map:
            self.map.addObject(self)

    def _updateOnMap(self, map):
        localAvatar.guiMgr.radarGui.updateOutOfRange(map, self, self.outOfRangeGeom)

    def _removedFromMap(self, map):
        self.outOfRangeGeom.detachNode()