import random
import re
import imp
from pandac.PandaModules import *
from direct.actor import *
from direct.distributed.DistributedCartesianGrid import DistributedCartesianGrid
from direct.task import Task
from direct.showbase.PythonUtil import report
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DGG
from direct.distributed.StagedObject import StagedObject
from otp.nametag.Nametag import Nametag
from otp.nametag.NametagGroup import NametagGroup
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPRender
from pirates.ai import HolidayGlobals
from pirates.audio import SoundGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.effects.LanternGlow import LanternGlow
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.VolcanoEffect import VolcanoEffect
from pirates.effects.FeastFire import FeastFire
from pirates.effects import FireworkGlobals
from pirates.effects.FireworkShow import FireworkShow
from pirates.world.ZoneLOD import ZoneLOD
from pirates.world import WorldGlobals
from pirates.world.DistributedGameArea import DistributedGameArea
from pirates.world.LocationConstants import LocationIds
from pirates.distributed import DistributedInteractive
from pirates.piratesgui import PiratesGuiGlobals, RadarGui
from pirates.seapatch.Water import IslandWaterParameters
from pirates.swamp.Swamp import Swamp
from pirates.seapatch.Reflection import Reflection
from pirates.piratesbase import TODGlobals
from pirates.pvp import PVPGlobals
from pirates.map.Minimap import IslandMap
from pirates.map.Mappable import MappableGrid
from direct.gui import DirectGuiGlobals
from pirates.battle.Teamable import Teamable

class DistributedIsland(DistributedGameArea, DistributedCartesianGrid, ZoneLOD, Teamable, MappableGrid):
    SiegeIcon = None
    notify = directNotify.newCategory('DistributedIsland')

    def __init__(self, cr):
        DistributedGameArea.__init__(self, cr)
        DistributedCartesianGrid.__init__(self, cr)
        Teamable.__init__(self)
        MappableGrid.__init__(self)
        self.islandShoreWave = None
        self.islandObjectsLoaded = False
        self.animControls = None
        self.sphereRadii = [
         1000, 2000, 3000, 100000]
        self.sphereCenter = [0, 0]
        ZoneLOD.__init__(self, self.uniqueName, onStage=StagedObject.OFF)
        self.parentWorld = None
        self.gridSphere = None
        self.nameText = None
        self.geom = None
        self.dockingLOD = None
        self.dockingLodFog = None
        self.dockingChar = None
        self.playerBarrierNP = None
        self.islandLowLod = None
        self.islandLowLodFog = None
        self.fogTransitionIval = None
        self.gold = 0
        self.islandTunnel = []
        self.hasTunnelsOnRadar = False
        self.name = 'Island Name'
        self.nametag = None
        self.nametag3d = None
        self.volcanoEffect = None
        self.feastFireEnabled = False
        self.feastFireEffect = None
        self.fireworkShowEnabled = False
        self.fireworkShowLegal = False
        self.fireworkShowType = 0
        self.fireworkShow = None
        self.islandMapModelPath = None
        self.mapName = None
        self.objsCached = False
        self.oceanVisEnabled = base.config.GetBool('ocean-visibility', False)
        self.flatShipsOnIsland = base.config.GetBool('flat-ships-on-island', True)
        self.locationSphereName = ''
        self.SiegeIcons = []
        if not DistributedIsland.SiegeIcon and launcher.getPhaseComplete(3):
            logos = loader.loadModel('models/textureCards/sailLogo')
            if logos:
                DistributedIsland.SiegeIcon = [logos.find('**/logo_french_flag'), logos.find('**/logo_spanish_flag')]
        self.localInterest = None
        return

    def announceGenerate(self):
        DistributedGameArea.announceGenerate(self)
        DistributedCartesianGrid.announceGenerate(self)
        self.accept('docked', self.resetZoneLODs)
        self.accept('toggleIslandNametag', self.setNameVisible)
        self.loadDockingLOD()
        self.loadIslandLowLod()
        detailLevel = base.options.terrain_detail_level
        sailingLOD = FadeLODNode('sailingLOD')
        sailingLOD.setFadeTime(2)
        if detailLevel == 0:
            sailingLOD.addSwitch(5000, 0)
            sailingLOD.addSwitch(100000, 5000)
        else:
            if detailLevel == 1:
                sailingLOD.addSwitch(10000, 0)
                sailingLOD.addSwitch(100000, 10000)
            elif detailLevel == 2:
                sailingLOD.addSwitch(20000, 0)
                sailingLOD.addSwitch(100000, 20000)
            self.sailingLOD = self.attachNewNode(sailingLOD)
            if self.dockingLOD:
                self.dockingLOD.reparentTo(self.sailingLOD)
                self.islandLowLod.reparentTo(self.sailingLOD)
            self.islandLowLod.reparentTo(self.sailingLOD)
            self.islandLowLod.copyTo(self.sailingLOD)
        self.loadWaterRing()
        gridSphereName = self.uniqueName('GridSphere')
        self.gridSphereEnterEvent = 'enter' + gridSphereName
        self.gridSphereExitEvent = 'exit' + gridSphereName
        self.setLodCollideMask(self.getLodCollideMask() | PiratesGlobals.ShipCollideBitmask)
        self.setZoneRadii(self.sphereRadii, self.sphereCenter)
        islandLOD = FadeLODNode('islandLOD')
        islandLOD.addSwitch(10000, 0)
        islandLOD.addSwitch(20000, 10000)
        islandLOD.setFadeTime(0.5)
        lodnp = NodePath(islandLOD)
        lodnp.reparentTo(self.builder.areaGeometry)
        lodnp.showThrough(OTPRender.ReflectionCameraBitmask)
        self.geomLOD = lodnp
        self.highDetail = lodnp.attachNewNode('highDetail')
        self.lowDetail = lodnp.attachNewNode('lowDetail')
        self.parentWorld.islands[self.doId] = self
        self.initializeNametag3d()
        self.setName(self.name)
        self.addActive()
        self.understandable = 1
        self.setPlayerType(NametagGroup.CCNormal)
        self.placeOnMap()
        self.accept('timeOfDayChange', self.timeOfDayChanged)

    def disable(self):
        self.clearLocalInterest()
        self.unloadIslandLowLod()
        self.unloadDockingLOD()
        self.sailingLOD.detachNode()
        self.sailingLOD = None
        self.unloadWaterRing()
        self.removeFromMap()
        self.ignore('docked')
        self.ignore('toggleIslandNametag')
        self.ignore('timeOfDayChange')
        self.goOffStage()
        self.stopCustomEffects()
        if self.fogTransitionIval:
            self.fogTransitionIval.pause()
            self.fogTransitionIval = None
        ZoneLOD.cleanup(self)
        DistributedGameArea.disable(self)
        DistributedCartesianGrid.disable(self)
        self.deleteZoneCollisions()
        self.parentWorld.islands.pop(self.doId, None)
        self.parentWorld = None
        self.removeActive()
        self.deleteNametag3d()
        return

    def delete(self):
        DistributedGameArea.delete(self)
        DistributedCartesianGrid.delete(self)
        ZoneLOD.delete(self)
        self.unloadPlayerBarrier()
        self.removeNode()
        while len(self.SiegeIcons):
            icon = self.SiegeIcons.pop()
            icon.removeNode()
            icon = None

        return

    @report(types=['args'], dConfigParam=['connector', 'death-debug', 'dteleport'])
    def handleOffStage(self, cache=False):
        self.stopCustomEffects()
        if not cache:
            self.setZoneLevelOuter()
        localAvatar.clearInterestNamed(None, ['IslandLocal'])
        DistributedGameArea.handleOffStage(self)
        ZoneLOD.handleOffStage(self)
        return

    @report(types=['args'], dConfigParam=['connector', 'death-debug', 'dteleport'])
    def handleOnStage(self):
        DistributedGameArea.handleOnStage(self)
        ZoneLOD.handleOnStage(self)
        self.startCustomEffects()
        if self.lastZoneLevel == 0:
            self.loadConnectors()
            self.addLocalInterest()

    def isGrid(self):
        return DistributedCartesianGrid.isGrid(self)

    def setLocation(self, parentId, zoneId):
        DistributedGameArea.setLocation(self, parentId, zoneId)
        self.parentWorld = self.getParentObj()

    def setZoneSphereSize(self, rad0, rad1, rad2):
        self.sphereRadii = [
         rad0, rad1, rad2, 100000]

    def getZoneSphereSize(self):
        return self.sphereRadii

    def setZoneSphereCenter(self, x, y):
        self.sphereCenter = [
         x, y]

    def getZoneSphereCenter(self):
        return self.sphereCenter

    def getMusicName(self):
        islandName = self.getName()
        musicName = self.MusicNames.get(islandName, self.MusicDefault)
        return musicName

    def addLocalInterest(self):
        if not self.localInterest:
            self.localInterest = self.cr.addTaggedInterest(self.doId, PiratesGlobals.IslandLocalZone, self.cr.ITAG_GAME, 'IslandLocal')

    def clearLocalInterest(self):
        if self.localInterest:
            self.cr.removeTaggedInterest(self.localInterest)
            self.localInterest = None
        return

    @report(types=['args', 'deltaStamp'], dConfigParam=['connector', 'jail', 'island'])
    def loadZoneLevel(self, level):
        if level == 0:
            self.islandObjectsLoaded = True
            self.hideSailingLOD()
            base.loadingScreen.beginStep('island terrain')
            self.retrieveIslandTerrain()
            base.loadingScreen.endStep('island terrain')
            self.builder.loadObjects()
            base.loadingScreen.beginStep('rest', 1, 8)
            self.loadConnectors()
            self.listenForLocationSphere()
            self.startCustomEffects(island=True)
            messenger.send('toggleIslandNametag', [0])
            if self.isDockable():
                self.setupMinimap()
            if self.minimap and localAvatar.getMinimapObject():
                self.minimap.addObject(localAvatar.getMinimapObject())
                localAvatar.guiMgr.setMinimap(self.minimap)
            self.addLocalInterest()
            if base.config.GetBool('island-prepare-scene', 1) and base.win.getGsg():
                render.prepareScene(base.win.getGsg())
            self.initBlockers(self)
            self.builder.checkForHolidayObjects()
            base.loadingScreen.endStep('rest')
        elif level == 1:
            self.cr.addTaggedInterest(self.doId, PiratesGlobals.IslandShipDeployerZone, self.cr.ITAG_GAME, 'ShipDeployer', otherTags=['ShipDeployer'])
            messenger.send('toggleIslandNametag', [1])
            if not self.undockable:
                localAvatar.setPort(self.doId)
            else:
                localAvatar.guiMgr.createWarning(PLocalizer.HeavyFogWarning, PiratesGuiGlobals.TextFG6, duration=6.0)
        elif level == 2:
            if self.waterRing:
                self.setIslandWaterParameters(True)
            self.addToOceanSeapatch()
        elif level == 3:
            self.allEnabled = False
            self.showName()
        elif level == 4:
            pass
        self.updateCustomEffects(level)

    @report(types=['args', 'deltaStamp'], dConfigParam=['connector', 'jail', 'island'])
    def unloadZoneLevel(self, level):
        if level == 0:
            self.islandObjectsLoaded = False
            self.handleExitGameArea()
            self.unloadConnectors()
            self.cleanupIslandData()
            self.unloadIslandShoreWave()
            self.stopListenForLocationSphere()
            base.localAvatar.guiMgr.clearMinimap(self.minimap)
            self.destroyMinimap()
            base.musicMgr.requestCurMusicFadeOut(removeFromPlaylist=True)
            self.clearLocalInterest()
            self.showSailingLOD()
        elif level == 1:
            self.cr.removeInterestTag('ShipDeployer')
            localAvatar.clearPort(self.doId)
        elif level == 2:
            self.showName()
            self.removeFromOceanSeapatch()
        elif level == 3:
            self.hideName()
        elif level == 4:
            pass
        self.updateCustomEffects(level + 1)

    def handleChildArrive(self, child, zoneId):
        DistributedGameArea.handleChildArrive(self, child, zoneId)
        DistributedCartesianGrid.handleChildArrive(self, child, zoneId)
        if child.isLocal():
            self.childArrived(self.doId, self.getParentObj())
            self.updateAvReturnLocation(child)
            messenger.send('docked')
            self.accept('ship_vis_change', self.shipVisibilityChanged)
            if base.cr.config.GetBool('remove-island-barriers', False):
                self.setupPlayerBarrier()
            base.hideShipNametags = True
            messenger.send('hide-ship-nametags')
            if base.shipsVisibleFromIsland == 1:
                base.showShipFlats = True
                messenger.send('far-ships')
            else:
                base.showShipFlats = False
                messenger.send('normal-ships')
            self.setZoneLevel(0)

    def setChildGridCells(self, child, zoneId):
        DistributedCartesianGrid.setChildGridCells(self, child, zoneId)
        if base.shipsVisibleFromIsland:
            oceanGrid = self.cr.activeWorld.worldGrid
            zoneId = oceanGrid.getZoneFromXYZ(child.getPos(oceanGrid))
            child.updateGridInterest(oceanGrid, zoneId)

    def handleChildLeave(self, child, zoneId):
        if child.isLocal():
            self.childLeft(self.doId, self.getParentObj())
            self.ignore('ship_vis_change')
            self.unloadPlayerBarrier()
            messenger.send('normal-ships')
            base.showShipFlats = False
            base.hideShipNametags = False
            messenger.send('show-ship-nametags')
        DistributedGameArea.handleChildLeave(self, child, zoneId)
        DistributedCartesianGrid.handleChildLeave(self, child, zoneId)

    @report(types=['args', 'deltaStamp'], dConfigParam=['jail', 'teleport'])
    def handleEnterGameArea(self, collEntry=None):
        self.setZoneLevel(0)
        DistributedGameArea.handleEnterGameArea(self, collEntry)

    @report(types=['args', 'deltaStamp'], dConfigParam=['jail', 'teleport'])
    def setupPlayerBarrier(self):
        if not self.playerBarrierNP:
            playerBarrier = CollisionInvSphere(self.zoneCenter[0], self.zoneCenter[1], 0, self.zoneRadii[0] * 0.95)
            playerBarrier.setTangible(1)
            cName = self.uniqueName('PlayerBarrier')
            cSphereNode = CollisionNode(cName)
            cSphereNode.setIntoCollideMask(OTPGlobals.WallBitmask | OTPGlobals.GhostBitmask)
            cSphereNode.addSolid(playerBarrier)
            self.playerBarrierNP = self.attachNewNode(cSphereNode)
            self.accept('enter' + self.uniqueName('PlayerBarrier'), self.enteredPlayerBarrier)
            self.accept('islandPlayerBarrier', self.setPlayerBarrier)
        self.setPlayerBarrier(1)

    @report(types=['args', 'deltaStamp'], dConfigParam=['jail', 'teleport'])
    def enteredPlayerBarrier(self, *args):
        localAvatar.guiMgr.createWarning(PLocalizer.IslandPlayerBarrierWarning, PiratesGuiGlobals.TextFG6)

    @report(types=['args', 'deltaStamp'], dConfigParam=['jail', 'teleport'])
    def unloadPlayerBarrier(self):
        self.ignore('enter' + self.uniqueName('PlayerBarrier'))
        self.ignore('islandPlayerBarrier')
        if self.playerBarrierNP:
            self.playerBarrierNP.removeNode()
            self.playerBarrierNP = None
        return

    @report(types=['args', 'deltaStamp'], dConfigParam=['jail', 'teleport'])
    def setPlayerBarrier(self, isOn):
        if self.playerBarrierNP:
            if isOn:
                self.playerBarrierNP.unstash()
            else:
                self.playerBarrierNP.stash()

    def addIslandToOcean(self):
        if self.parentWorld.worldGrid:
            self.parentWorld.worldGrid.addIslandGrid(self)
        else:
            self.notify.error('worldGrid is none for %s %s' % (self.parentWorld, self))

    def removeIslandFromOcean(self):
        if self.parentWorld:
            self.parentWorld.worldGrid.removeIslandGrid(self)

    @report(types=['args', 'deltaStamp'], dConfigParam=['jail'])
    def setLinks(self, links):
        DistributedGameArea.setLinks(self, links)
        if self.lastZoneLevel == 0:
            self.loadConnectors()

    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def loadIslandLowLod(self):
        flatName = self.modelPath.split('_zero')[0]
        if not self.islandLowLod:
            self.islandLowLod = loader.loadModel('%s_low' % flatName, okMissing=False)
            self.islandLowLod.flattenStrong()
            self.islandLowLod.hide(OTPRender.MainCameraBitmask)
            self.islandLowLod.showThrough(OTPRender.EnviroCameraBitmask)
            self.islandLowLodFog = self.islandLowLod.find('**/fog')
            if self.islandLowLodFog:
                self.islandLowLodFog.setLightOff()
                self.islandLowLodFog.setDepthWrite(0)
                todMgr = base.cr.timeOfDayManager
                if todMgr:
                    self.islandLowLodFog.setColorScale(TODGlobals.getTodEnvSetting(todMgr.currentState, todMgr.environment, 'FogColor') / 3.0 + Vec4(0, 0, 0, 1))

    def unloadIslandLowLod(self):
        if self.islandLowLod:
            self.islandLowLod.removeNode()
        self.islandLowLod = None
        return

    def loadIslandMapModel(self):
        if not self.islandMapModelPath:
            mapModelName = self.modelPath.split('_zero')
            self.islandMapModelPath = mapModelName[0] + '_worldmap'

    @report(types=['args', 'deltaStamp'], dConfigParam='map')
    def placeOnMap(self):
        self.loadIslandMapModel()
        if not self.mapName and self.islandMapModelPath:
            mapPage = localAvatar.guiMgr.mapPage
            self.mapName = mapPage.addIsland(self.name, self.uniqueId, self.islandMapModelPath, self.getPos(), self.getH())

    @report(types=['args', 'deltaStamp'], dConfigParam='map')
    def removeFromMap(self):
        if self.mapName:
            mapPage = localAvatar.guiMgr.mapPage
            mapPage.removeIsland(self.mapName)
        self.mapName = None
        return

    def loadIslandShoreWave(self, parent):
        if self.islandShoreWave:
            return
        lowend = ''
        if base.options.getTerrainDetailSetting() == 0:
            lowend = '_lowend'
        islandBaseName = self.modelPath.split('_zero')[0]
        waveModel = loader.loadModel(islandBaseName + lowend + '_wave_none', okMissing=True)
        if lowend != '' and not waveModel:
            lowend = ''
            waveModel = loader.loadModel(islandBaseName + lowend + '_wave_none', okMissing=True)
        if waveModel:
            self.islandShoreWave = Actor.Actor(waveModel)
            self.islandShoreWave.loadAnims({'idle': islandBaseName + lowend + '_wave_idle'})
            self.islandShoreWave.reparentTo(parent)
            self.islandShoreWave.loop('idle')
            meshes = self.islandShoreWave.findAllMatches('**/mesh_tide1')
            if not meshes.isEmpty():
                mesh = meshes[0]
                joints = self.islandShoreWave.findAllMatches('**/uvj_WakeWhiteTide1')
                if joints.getNumPaths() and mesh.findTextureStage('default'):
                    mesh.setTexProjector(mesh.findTextureStage('default'), joints[0], parent)
            meshes = self.islandShoreWave.findAllMatches('**/mesh_tide2')
            if not meshes.isEmpty():
                mesh = meshes[0]
                joints = self.islandShoreWave.findAllMatches('**/uvj_WakeWhiteTide2')
                if joints.getNumPaths() and mesh.findTextureStage('default'):
                    mesh.setTexProjector(mesh.findTextureStage('default'), joints[0], parent)
            lavaCombo = self.islandShoreWave.findAllMatches('**/lava_combo_*')
            if lavaCombo.getNumPaths():
                lavaComboRoot = self.islandShoreWave.find('**/+Character').attachNewNode('lavaCombo')
                lavaComboRoot.setDepthWrite(1, 100)
                lavaCombo.reparentTo(lavaComboRoot)
                joint = self.islandShoreWave.find('**/uvj_LavaCombo1')
                lavaComboRoot.setTexProjector(lavaComboRoot.findTextureStage('default'), joint, parent)
            lavaHot = self.islandShoreWave.findAllMatches('**/lava_hot_*')
            if lavaHot.getNumPaths():
                lavaHotRoot = self.islandShoreWave.find('**/+Character').attachNewNode('lavaHot')
                lavaHotRoot.setDepthWrite(1, 100)
                lavaHot.reparentTo(lavaHotRoot)
                joint = self.islandShoreWave.find('**/uvj_LavaHot1')
                lavaHotRoot.setTexProjector(lavaHotRoot.findTextureStage('default'), joint, parent)
            lavaCool = self.islandShoreWave.findAllMatches('**/lava_cool_*')
            if lavaCool.getNumPaths():
                lavaCoolRoot = self.islandShoreWave.find('**/+Character').attachNewNode('lavaCool')
                lavaCoolRoot.setDepthWrite(1, 100)
                lavaCool.reparentTo(lavaCoolRoot)
                joint = self.islandShoreWave.find('**/uvj_LavaCool1')
                lavaCoolRoot.setTexProjector(lavaCoolRoot.findTextureStage('default'), joint, parent)
            self.islandShoreWave.setPlayRate(0.8, 'idle')
            OTPRender.renderReflection(False, self.islandShoreWave, 'p_island_shore', None)
            alpha_test_attrib = AlphaTestAttrib.make(RenderAttrib.MAlways, 0)
            self.islandShoreWave.setAttrib(alpha_test_attrib, 100)
            self.islandShoreWave.setTwoSided(1, 100)
            self.islandShoreWave.setDepthWrite(0, 100)
        return

    def unloadIslandShoreWave(self):
        if self.islandShoreWave:
            self.islandShoreWave.delete()
            self.islandShoreWave = None
        return

    def foo(self):
        collNodes = self.geom.findAllMatches('**/+CollisionNode')
        for collNode in collNodes:
            curMask = collNode.node().getIntoCollideMask()
            if curMask.hasBitsInCommon(OTPGlobals.FloorBitmask):
                self.setupCannonballLandColl(collNode, PiratesGlobals.TargetBitmask | curMask, 0)

    def loadDockingLOD(self):
        islandBaseName = self.modelPath.split('_zero')[0]
        if self.dockingLOD:
            self.dockingLOD.detachNode()
        self.dockingLOD = loader.loadModel(islandBaseName + '_dock_lod', okMissing=True)
        if self.dockingLOD:
            self.dockingLOD.hide(OTPRender.MainCameraBitmask)
            self.dockingLOD.showThrough(OTPRender.EnviroCameraBitmask)
            self.dockingLOD.findAllMatches('**/water_*').detach()
            self.dockingLOD.flattenStrong()
            self.dockingLodFog = self.dockingLOD.find('**/fog')
            if self.dockingLodFog:
                self.dockingLodFog.setLightOff()
                self.dockingLodFog.setDepthWrite(0)
                todMgr = base.cr.timeOfDayManager
                if todMgr:
                    self.dockingLodFog.setColorScale(TODGlobals.getTodEnvSetting(todMgr.currentState, todMgr.environment, 'FogColor') / 3.0 + Vec4(0, 0, 0, 1))

    def unloadDockingLOD(self):
        if self.dockingLOD:
            self.dockingLOD.removeNode()
            self.dockingLOD = None
        return

    def showSailingLOD(self):
        if self.sailingLOD:
            self.sailingLOD.show()

    def hideSailingLOD(self):
        self.sailingLOD.hide()

    def loadTerrain(self):
        islandBaseName = self.modelPath.split('_zero')[0]
        self.geom = self.loadWholeModel(islandBaseName)
        self.geom.findAllMatches('**/water_*').detach()

    def loadWholeModel(self, name):
        lowend = ''
        if base.options.getTerrainDetailSetting() == 0:
            lowend = '_lowend'
        zeroModel = loader.loadModel(name + lowend + '_zero', okMissing=True)
        if not zeroModel:
            zeroModel = loader.loadModel(name + lowend, okMissing=True)
        if lowend != '' and not zeroModel:
            zeroModel = loader.loadModel(name + '_zero', okMissing=True)
            if not zeroModel:
                zeroModel = loader.loadModel(name)
        geom = zeroModel
        collNode = geom.find('**/cannoncol*')
        if collNode != collNode.notFound():
            collNode.node().setIntoCollideMask(collNode.node().getIntoCollideMask() | PiratesGlobals.TargetBitmask | OTPGlobals.CameraBitmask)
            collNode.setTag('objType', str(PiratesGlobals.COLL_BLOCKER))
        return geom

    def addToOceanSeapatch(self):
        if self.parentWorld and self.parentWorld.getWater():
            self.parentWorld.getWater().patch.addFlatWell(self.uniqueName('flatWell'), self, self.zoneCenter[0], self.zoneCenter[1], self.zoneRadii[0], self.zoneRadii[0] + 100)

    def removeFromOceanSeapatch(self):
        if self.parentWorld.getWater():
            self.parentWorld.getWater().patch.removeFlatWell(self.uniqueName('flatWell'))

    def loadIslandStuff(self):
        self.largeObjects = self.geom.findAllMatches('**/*bldg*')
        for b in self.largeObjects:
            b.wrtReparentTo(self.largeObjectsHigh)
            wallGeom = b.find('**/wall*_n_window*')
            roofGeom = b.find('**/roof')
            for c in [wallGeom, roofGeom]:
                self.setupCannonballBldgColl(c, PiratesGlobals.TargetBitmask)

        details = [
         self.geom.find('**/barrels'), self.geom.find('**/crates'), self.geom.find('**/canopys'), self.geom.find('**/bushes')]
        for detail in details:
            if not detail.isEmpty():
                detail.wrtReparentTo(self.smallObjectsHigh)
                detail.flattenLight()

        self.smallObjects = details
        del details
        details = [self.geom.find('**/palmtrees'), self.geom.find('**/pier')]
        for detail in details:
            if not detail.isEmpty():
                detail.wrtReparentTo(self.medObjectsHigh)
                detail.flattenLight()

        self.mediumObjects = details

    def setName(self, name):
        self.name = name
        if not self.nametag:
            self.createNametag(self.name)
        else:
            self.nametag.setName(name)
        self.nametag.setDisplayName('        ')
        if self.nameText:
            self.nameText['text'] = name
            siegeTeam = self.getSiegeTeam()
            if siegeTeam and self.SiegeIcon:
                color = VBase4(PVPGlobals.getSiegeColor(siegeTeam))
                color.setW(0.7)
                icon = self.SiegeIcon[siegeTeam - 1].copyTo(NodePath('siegeIcons'))
                icon.reparentTo(self.nameText)
                self.SiegeIcons.append(icon)
                icon.setZ(1.5)
                icon.setScale(0.75)
            else:
                color = Vec4(0.6, 0.6, 1, 0.4)
            self.nameText['fg'] = color

    def setDisplayName(self, str):
        self.nametag.setDisplayName(str)

    def getName(self):
        return self.name

    def getNameVisible(self):
        return self.__nameVisible

    def setNameVisible(self, bool):
        self.__nameVisible = bool
        if bool:
            self.showName()
        if not bool:
            self.hideName()

    def hideName(self):
        self.nametag.getNametag3d().setContents(Nametag.CSpeech | Nametag.CThought)

    def showName(self):
        if self.__nameVisible:
            self.nametag.getNametag3d().setContents(Nametag.CName | Nametag.CSpeech | Nametag.CThought)

    def hideNametag2d(self):
        self.nametag2dContents = 0
        self.nametag.getNametag2d().setContents(self.nametag2dContents & self.nametag2dDist)

    def showNametag2d(self):
        self.nametag2dContents = self.nametag2dNormalContents
        self.nametag2dContents = Nametag.CSpeech
        self.nametag.getNametag2d().setContents(self.nametag2dContents & self.nametag2dDist)

    def hideNametag3d(self):
        self.nametag.getNametag3d().setContents(0)

    def showNametag3d(self):
        if self.__nameVisible:
            self.nametag.getNametag3d().setContents(Nametag.CName | Nametag.CSpeech | Nametag.CThought)
        else:
            self.nametag.getNametag3d().setContents(0)

    def setPickable(self, flag):
        self.nametag.setActive(flag)

    def clickedNametag(self):
        if self.nametag.isActive():
            messenger.send('clickedNametag', [self])

    def initializeNametag3d(self):
        self.deleteNametag3d()
        self.nametag.setFont(PiratesGlobals.getPirateFont())
        nametagNode = self.nametag.getNametag3d()
        self.nametag3d.attachNewNode(nametagNode)
        self.nametag3d.setFogOff()
        self.nametag3d.setLightOff()
        self.nametag3d.setColorScaleOff(100)
        self.nametag3d.setDepthWrite(0)
        self.iconNodePath = self.nametag.getNameIcon()
        if self.iconNodePath.isEmpty():
            self.notify.warning('empty iconNodePath in initializeNametag3d')
            return 0
        if not self.nameText:
            self.nameText = OnscreenText(fg=Vec4(1, 1, 1, 1), bg=Vec4(0, 0, 0, 0), scale=1.1, align=TextNode.ACenter, mayChange=1, font=PiratesGlobals.getPirateBoldOutlineFont())
            self.nameText.setDepthWrite(0)
            self.nameText.reparentTo(self.iconNodePath)
            self.nameText.setColorScaleOff(100)
            self.nameText.setLightOff()
            self.nameText.setFogOff()

    def deleteNametag3d(self):
        children = self.nametag3d.getChildren()
        for i in range(children.getNumPaths()):
            children[i].removeNode()

    def addActive(self):
        if base.wantNametags:
            self.nametag.manage(base.marginManager)
            self.accept(self.nametag.getUniqueId(), self.clickedNametag)

    def removeActive(self):
        if base.wantNametags and self.nametag:
            self.nametag.unmanage(base.marginManager)
            self.ignore(self.nametag.getUniqueId())

    def createNametag(self, name):
        self.__nameVisible = 1
        self.nametag = NametagGroup()
        self.nametag.setAvatar(self)
        self.nametag.setFont(PiratesGlobals.getPirateFont())
        self.nametag2dContents = Nametag.CName
        self.nametag2dDist = Nametag.CName
        self.nametag2dNormalContents = Nametag.CName
        self.nametag3d = self.attachNewNode('nametag3d')
        self.nametag3d.setTag('cam', 'nametag')
        self.nametag.setName(name)
        self.nametag.setNameWordwrap(PiratesGlobals.NAMETAG_WORDWRAP)
        OTPRender.renderReflection(False, self.nametag3d, 'p_island_nametag', None)
        self.nametag3d.setPos(0, 0, WorldGlobals.getNametagHeight(self.name))
        self.setNametagScale(WorldGlobals.getNametagScale(self.name))
        self.nametag3d.setFogOff()
        self.setPickable(0)
        self.nametag.setColorCode(1)
        return

    def getNametagScale(self):
        return self.nametagScale

    def setNametagScale(self, scale):
        self.nametagScale = scale
        self.nametag3d.setScale(scale)

    def setPlayerType(self, playerType):
        self.playerType = playerType
        self.nametag.setColorCode(self.playerType)

    def setIslandWaterParameters(self, use_alpha_map):
        if self.islandWaterParameters:
            if self.parentWorld:
                self.islandWaterParameters.setIslandWaterParameters(self.parentWorld.getWater(), use_alpha_map)

    def setX(self, *args, **kwargs):
        DistributedGameArea.setX(self, *args, **kwargs)
        mapPage = base.localAvatar.guiMgr.mapPage
        mapPage.updateIsland(self.mapName, worldPos=self.getPos())

    def setY(self, *args, **kwargs):
        DistributedGameArea.setY(self, *args, **kwargs)
        mapPage = base.localAvatar.guiMgr.mapPage
        mapPage.updateIsland(self.mapName, worldPos=self.getPos())

    def setH(self, *args, **kwargs):
        DistributedGameArea.setH(self, *args, **kwargs)
        mapPage = base.localAvatar.guiMgr.mapPage
        mapPage.updateIsland(self.mapName, rotation=self.getH())

    def getTeam(self):
        return PiratesGlobals.ISLAND_TEAM

    def updateAvReturnLocation(self, av):
        av.d_requestReturnLocation(self.doId)

    def updateAvIsland(self, av):
        av.d_requestCurrentIsland(self.doId)

    def startFloatables(self):
        world = base.cr.getActiveWorld()
        if world:
            water = world.getWater()
            if water:
                for uid, obj in self.floatables.iteritems():
                    water.addFloatable(uid, obj, mass=5)

    def stopFloatables(self):
        world = base.cr.getActiveWorld()
        if world:
            water = world.getWater()
            if water:
                for uid in self.floatables:
                    water.removeFloatable(uid)

    @report(types=['args', 'deltaStamp'], dConfigParam='connector')
    def setOceanVisEnabled(self, enabled):
        self.oceanVisEnabled = enabled
        if self.lastZoneLevel == 0:
            pass

    def setFlatShips(self, value):
        self.flatShipsOnIsland = value
        if self.lastZoneLevel == 0:
            if self.flatShipsOnIsland:
                messenger.send('far-ships')
                base.showShipFlats = True
            else:
                messenger.send('normal-ships')
                base.showShipFlats = False

    def listenForLocationSphere(self):
        self.locationSphereName = 'locSphere-%s' % self.uniqueId
        msgName = PiratesGlobals.LOCATION_SPHERE
        self.accept('enter' + self.locationSphereName, self.cr.getActiveWorld().enteredSphere, extraArgs=[[msgName]])
        self.accept('exit' + self.locationSphereName, self.cr.getActiveWorld().exitedSphere, extraArgs=[[msgName]])

    def stopListenForLocationSphere(self):
        if self.locationSphereName:
            self.ignore('enter' + self.locationSphereName)
            self.ignore('exit' + self.locationSphereName)

    def buildDockingLOD(self):
        dockingCache = self.getDockingCache()
        self.loadDockingLOD()
        for obj in self.dockingLOD.findAllMatches('**/=ignore-lighting'):
            obj.setLightOff(1000)

        dockingCache.setData(self.dockingLOD.node(), 0)
        base.bamCache.store(dockingCache)

    def retrieveDockingLOD(self):
        dockingCache = self.getDockingCache()
        if dockingCache.hasData() and base.config.GetBool('want-disk-cache', 0):
            data = dockingCache.getData()
            newData = data.copySubgraph()
            self.dockingLOD = NodePath(newData)
        else:
            self.buildDockingLOD()
        islandBaseName = self.modelPath.split('_zero')[0]
        dockingChar = loader.loadModel(islandBaseName + '_dock_lod_none', okMissing=True)
        if dockingChar:
            self.dockingChar = Actor.Actor(dockingChar)
            self.dockingChar.loadAnims({'idle': islandBaseName + '_dock_lod_idle'})
            self.dockingChar.reparentTo(self.dockingLOD)
            joint = self.dockingChar.find('**/uvj_LavaCombo1')
            self.dockingChar.loop('idle')
            self.dockingChar.setTexProjector(self.dockingChar.findTextureStage('default'), joint, self.dockingLOD)
        self.dockingLOD.reparentTo(self)
        self.dockingLOD.hide(OTPRender.MainCameraBitmask)
        self.dockingLOD.showThrough(OTPRender.EnviroCameraBitmask)

    def buildIslandTerrain(self):
        islandGeomCache = self.getIslandCache()
        self.loadTerrain()
        flat = self.geom.find('**/island_flat_lod')
        if not flat.isEmpty():
            flat.removeNode()
        for obj in self.geom.findAllMatches('**/=ignore-lighting'):
            obj.setLightOff(1000)

        islandGeomCache.setData(self.geom.node(), 0)
        base.bamCache.store(islandGeomCache)

    def retrieveIslandTerrain(self):
        islandGeomCache = self.getIslandCache()
        if islandGeomCache.hasData() and base.config.GetBool('want-disk-cache', 0):
            data = islandGeomCache.getData()
            newData = data.copySubgraph()
            self.geom = NodePath(newData)
        else:
            self.buildIslandTerrain()
        self.geom.reparentTo(self)
        self.geom.hide(OTPRender.MainCameraBitmask)
        self.geom.showThrough(OTPRender.EnviroCameraBitmask)
        self.hideMapNodes()
        self.loadIslandShoreWave(self.geom)

    def cleanupIslandData(self):
        self.builder.cleanupData()
        self.cleanupTerrain()

    def cleanupTerrain(self):
        self.geom.removeNode()
        self.geom = None
        return

    def cleanupDockingLOD(self):
        if self.dockingChar:
            self.dockingChar.cleanup()
        self.dockingChar = None
        self.dockingLOD.removeNode()
        self.dockingLOD = None
        return

    def getCoreCache(self):
        return base.bamCache.lookup(Filename('/%s_%s_core_%s_%s.bam' % (self.name, self.uniqueId, base.launcher.getServerVersion(), base.gridDetail)), 'bam')

    def getGridCache(self):
        return base.bamCache.lookup(Filename('/%s_%s_grid_%s.bam' % (self.name, self.uniqueId, base.gridDetail)), 'bam')

    def getAnimCache(self):
        return base.bamCache.lookup(Filename('/%s_%s_anims_%s.bam' % (self.name, self.uniqueId, base.gridDetail)), 'bam')

    def getLargeObjectsCache(self):
        return base.bamCache.lookup(Filename('/%s_%s_large_%s.bam' % (self.name, self.uniqueId, base.gridDetail)), 'bam')

    def getIslandCache(self):
        return base.bamCache.lookup(Filename('/%s_%s_island_%s_%s.bam' % (self.name, self.uniqueId, base.launcher.getServerVersion(), base.gridDetail)), 'bam')

    def getDockingCache(self):
        return base.bamCache.lookup(Filename('/%s_%s_island_docking_%s_%s.bam' % (self.name, self.uniqueId, base.launcher.getServerVersion(), base.gridDetail)), 'bam')

    def getSiegeTeam(self):
        return base.cr.distributedDistrict.worldCreator.getPvpIslandTeam(self.uniqueId)

    def isInInvasion(self):
        return False

    def getArmorScale(self):
        return 1.0

    def setUndockable(self, undockable):
        self.undockable = undockable

    def isDockable(self):
        return not self.undockable

    def shipVisibilityChanged(self, value):
        pass

    def setupMinimap(self):
        if not self.minimap and not self.getMapNode().isEmpty():
            self.minimap = IslandMap(self)

    def destroyMinimap(self):
        if self.minimap:
            self.minimap.destroy()
            self.minimap = None
        return

    def getGridParameters(self):
        return (
         self.cellWidth, self.viewingRadius)

    def getMapName(self):
        return 'map-' + self.getName()

    @report(types=['args', 'deltaStamp'], dConfigParam=['connector', 'jail', 'island'])
    def setZoneLevel(self, *args, **kw):
        ZoneLOD.setZoneLevel(self, *args, **kw)

    def getIslandTransform(self):
        return (
         self.getX(), self.getY(), self.getZ(), self.getH())

    def setIslandTransform(self, x, y, z, h):
        self.setXYZH(x, y, z, h)

    def startCustomEffects(self, interior=False, island=False):
        DistributedGameArea.startCustomEffects(self, interior=False, loadIslandMusic=island)
        if self.uniqueId == LocationIds.DEL_FUEGO_ISLAND or self.uniqueId == LocationIds.MADRE_DEL_FUEGO_ISLAND:
            self.startVolcanoEffects()
        if self.uniqueId == LocationIds.TORTUGA_ISLAND:
            if not self.feastFireEffect and self.getFeastFireEnabled():
                self.startFeastEffects()
        self.updateCustomEffects(self.lastZoneLevel)
        self.builder.resumeSFX()

    def updateCustomEffects(self, level):
        if self.uniqueId == LocationIds.DEL_FUEGO_ISLAND or self.uniqueId == LocationIds.MADRE_DEL_FUEGO_ISLAND:
            self.startVolcanoEffects()
        if self.uniqueId == LocationIds.TORTUGA_ISLAND:
            if not self.feastFireEffect and self.getFeastFireEnabled():
                self.startFeastEffects()
            if level == 0:
                if self.feastFireEffect:
                    self.feastFireEffect.startMainEffects()
                    self.feastFireEffect.stopFarEffects()
            if level == 1 or level == 2:
                if self.feastFireEffect:
                    self.feastFireEffect.stopMainEffects()
                    self.feastFireEffect.startFarEffects()
            if level == 3:
                if self.feastFireEffect:
                    self.feastFireEffect.stopMainEffects()
                    self.feastFireEffect.startFarEffects()
        if self.fireworkShowEnabled:
            if level in [0, 1, 2]:
                self.fireworkShowLegal = True
                self.fireWorksStartTime = 0.0
                if base.cr.timeOfDayManager and not base.cr.timeOfDayManager.checkTimeOfDayToggle(self.uniqueName('fireWorksShow')):
                    base.cr.timeOfDayManager.addTimeOfDayToggle(self.uniqueName('fireWorksShow'), self.fireWorksStartTime, self.fireWorksStartTime + 2.0, startMethod=self.beginDailyFireworkShow, endMethod=self.destroyFireworkShow)
            else:
                self.fireWorksStartTime = None
                self.fireworkShowLegal = False
                self.destroyFireworkShow()
                if base.cr.timeOfDayManager:
                    base.cr.timeOfDayManager.removeTimeOfDayToggle(self.uniqueName('fireWorksShow'))
        return

    def stopCustomEffects(self):
        DistributedGameArea.stopCustomEffects(self)
        if base.cr.timeOfDayManager:
            base.cr.timeOfDayManager.removeTimeOfDayToggle(self.uniqueName('fireWorksShow'))
        self.destroyFireworkShow()
        if self.volcanoEffect:
            self.volcanoEffect.destroy()
            self.volcanoEffect = None
        if self.feastFireEffect:
            self.feastFireEffect.stopMainEffects()
            self.feastFireEffect.stopFarEffects()
        if self.fireworkShow:
            self.destroyFireworkShow()
        if self.builder:
            self.builder.pauseSFX()
        return

    def startVolcanoEffects(self):
        if not self.volcanoEffect:
            self.volcanoEffect = VolcanoEffect()
            self.volcanoEffect.reparentTo(self)
            if self.uniqueId == LocationIds.DEL_FUEGO_ISLAND:
                self.volcanoEffect.setPos(Vec3(-286, 180, 865))
            elif self.uniqueId == LocationIds.MADRE_DEL_FUEGO_ISLAND:
                self.volcanoEffect.setPos(Vec3(-40, 75, 600))
            self.volcanoEffect.enable()

    def makeLavaErupt(self):
        if self.lastZoneLevel in [0, 1, 2]:
            if not self.volcanoEffect:
                self.startVolcanoEffects()
            self.volcanoEffect.startLavaEruption()

    def startLavaFlow(self):
        return
        self.stopLavaFlow()
        lavaGeom = self.geom.find('**/lava')
        if not lavaGeom.isEmpty():
            lavaGeom.setLightOff()
            if base.main_rtt:
                lavaGeom.setFogOff()
                lavaGeom.showThrough(OTPRender.GlowCameraBitmask)
            tex = None
            if not lavaGeom.findTextureStage('VertexColor'):
                ts = TextureStage('VertexColor')
                ts.setSort(30)
                tex = lavaGeom.findTexture('*')
                if tex:
                    lavaGeom.setTexture(ts, tex)
            tsSet = lavaGeom.findAllTextureStages()
            tsSet = [ tsSet[x] for x in range(tsSet.getNumTextureStages()) ]
            tsSet.sort(key=lambda x: x.getSort())
            if not tsSet:
                return
            TS = TextureStage
            tsSet[0].setCombineRgb(TS.CMReplace, TS.CSTexture, TS.COSrcColor)
            tsSet[1].setCombineRgb(TS.CMAdd, TS.CSTexture, TS.COSrcColor, TS.CSPrevious, TS.COSrcColor)
            tsSet[2].setCombineRgb(TS.CMInterpolate, TS.CSTexture, TS.COSrcColor, TS.CSPrevious, TS.COSrcColor, TS.CSPrimaryColor, TS.COSrcAlpha)
            lavaSpeed = {0: 0.04,1: 0.02,2: 0.01}
            if tex:
                tsSet[3].setCombineRgb(TS.CMModulate, TS.CSPrevious, TS.COSrcColor, TS.CSPrimaryColor, TS.COSrcColor)
                tsSet[3].setCombineAlpha(TS.CMReplace, TS.CSConstant, TS.COSrcAlpha)
                tsSet[3].setColor(Vec4(1))
                lavaSpeed[3] = 0.0

            def flowLava(task):
                dt = globalClock.getDt()
                for key in lavaSpeed.keys():
                    offset = lavaGeom.getTexOffset(tsSet[key])[0]
                    offset -= lavaSpeed[key] * dt
                    offset %= 1.0
                    lavaGeom.setTexOffset(tsSet[key], offset, 0)

                return Task.cont

            taskMgr.add(flowLava, self.uniqueName('flowLava'))
        return

    def stopLavaFlow(self):
        return
        if self.geom and not self.geom.isEmpty():
            lavaGeom = self.geom.find('**/lava_red*')
            if lavaGeom and not lavaGeom.isEmpty():
                lavaGeom.clearLight()
                lavaGeom.clearFog()
        taskMgr.remove(self.uniqueName('flowLava'))

    def setFeastFireEnabled(self, value):
        if self.feastFireEnabled == value:
            return
        self.feastFireEnabled = value
        if self.feastFireEnabled:
            self.startFeastEffects()
            self.updateCustomEffects(self.lastZoneLevel)
        else:
            self.stopFeastEffects()

    def getFeastFireEnabled(self):
        return self.feastFireEnabled

    def startFeastEffects(self):
        if not self.feastFireEffect and self.getFeastFireEnabled():
            self.feastFireEffect = FeastFire()
            self.feastFireEffect.setCustomSettings()
            self.feastFireEffect.reparentTo(self)
            self.feastFireEffect.setPos(278, -166, 4.5)

    def stopFeastEffects(self):
        if self.feastFireEffect:
            self.feastFireEffect.stopLoop()
            self.feastFireEffect = None
        return

    def setFireworkShowEnabled(self, isEnabled, showType):
        self.fireworkShowEnabled = isEnabled
        self.fireworkShowType = showType
        if self.fireworkShowEnabled:
            self.createFireworkShow()
            self.updateCustomEffects(self.lastZoneLevel)
        else:
            self.destroyFireworkShow()

    def getFireworkShowEnabled(self):
        return self.fireworkShowEnabled

    def createFireworkShow(self):
        if not self.fireworkShow:
            self.fireworkShow = FireworkShow(self.fireworkShowType)

    def destroyFireworkShow(self):
        if self.fireworkShow:
            self.fireworkShow.cleanupShow()
            self.fireworkShow = None
        return

    def tryToBeginFireworkShow(self):
        if self.fireworkShowLegal and base.cr.timeOfDayManager:
            timeUntilShow = base.cr.timeOfDayManager.getTimeUntil(PiratesGlobals.TOD_STARS)
            if timeUntilShow <= 0:
                self.beginFireworkShow(timeStamp=-1 * timeUntilShow)
            else:
                self.destroyFireworkShow()

    def beginFireworkShow(self, task=None, timeStamp=0.0):
        self.createFireworkShow()
        if self.fireworkShow and not self.fireworkShow.isPlaying():
            self.fireworkShow.begin(timeStamp)
            self.fireworkShow.reparentTo(self)
            self.fireworkShow.setPos(render, FireworkGlobals.getShowPosition(self.uniqueId))
            self.fireworkShow.setHpr(render, FireworkGlobals.getShowOrientation(self.uniqueId))

    def beginDailyFireworkShow(self, task=None):
        self.createFireworkShow()
        if self.fireworkShow and not self.fireworkShow.isPlaying():
            currentTime = base.cr.timeOfDayManager.getCurrentIngameTime()
            startTimeDiff = currentTime - self.fireWorksStartTime
            startTimeDifSeconds = base.cr.timeOfDayManager.gameHoursToRealSeconds(startTimeDiff)
            duration = self.fireworkShow.getDuration()
            if startTimeDifSeconds < duration:
                self.fireworkShow.begin(startTimeDiff)
                self.fireworkShow.reparentTo(self)
                self.fireworkShow.setPos(render, FireworkGlobals.getShowPosition(self.uniqueId))
                self.fireworkShow.setHpr(render, FireworkGlobals.getShowOrientation(self.uniqueId))

    def ensureLoaded(self):
        self.setZoneLevel(0)
        DistributedGameArea.ensureLoaded(self)

    def resetZoneLODs(self):
        if localAvatar.parentId != self.doId:
            self.setZoneLevel(3)

    def loadWaterRing(self):
        islandBaseName = self.modelPath.split('_zero')[0]
        self.waterRing = loader.loadModel(islandBaseName + '_ocean', okMissing=True)
        if self.waterRing:
            self.waterRing.hide(OTPRender.MainCameraBitmask)
            self.waterRing.show(OTPRender.EnviroCameraBitmask)
            self.waterRing.reparentTo(self)
            self.initializeIslandWaterParameters(self.waterRing)
        else:
            self.setIslandWaterParameters(False)

    def unloadWaterRing(self):
        self.setIslandWaterParameters(False)
        if self.waterRing:
            self.waterRing.detachNode()
            self.waterRing = None
        return

    def setFogColor(self, fogColor):
        if self.dockingLodFog:
            self.dockingLodFog.setColorScale(fogColor)
        if self.islandLowLodFog:
            self.islandLowLodFog.setColorScale(fogColor)

    def timeOfDayChanged(self, stateId=None, stateDuration=0.0, elapsedTime=0.0, transitionTime=0.0):
        if self.dockingLodFog:
            todMgr = base.cr.timeOfDayManager
            transitionTime = todMgr.cycleDuration * TODGlobals.getStateTransitionTime(todMgr.cycleType, todMgr.currentState)
            fromFogColor = TODGlobals.getTodEnvSetting(todMgr.lastState, todMgr.environment, 'FogColor') / 2.5 + Vec4(0, 0, 0, 1)
            toFogColor = TODGlobals.getTodEnvSetting(todMgr.currentState, todMgr.environment, 'FogColor') / 2.5 + Vec4(0, 0, 0, 1)
            if self.fogTransitionIval:
                self.fogTransitionIval.pause()
                self.fogTransitionIval = None
            self.fogTransitionIval = LerpFunctionInterval(self.setFogColor, duration=transitionTime, toData=toFogColor, fromData=fromFogColor)
            self.fogTransitionIval.start(elapsedTime)
        return
