from pandac.PandaModules import *
from direct.distributed.DistributedNode import DistributedNode
from direct.distributed.StagedObject import StagedObject
from pirates.audio import SoundGlobals
from pirates.world import WorldGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.effects.EnvironmentEffects import EnvironmentEffects
from pirates.effects import SwampEffects
from pirates.effects import ForestEffects
from pirates.effects import CaveEffects
from pirates.piratesbase import TODGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import UserFunnel
from pirates.piratesgui.NewTutorialPanel import NewTutorialPanel
from pirates.uberdog.UberDogGlobals import InventoryType
from pandac.PandaModules import CollisionSphere
from pandac.PandaModules import CollisionNode
from pandac.PandaModules import CollisionHandlerEvent
from pirates.chat.PiratesChatManager import PiratesChatManager
from pirates.seapatch.SeaPatch import SeaPatch
from pirates.seapatch.Reflection import Reflection
from pirates.seapatch.Water import IslandWaterParameters
from pirates.swamp.Swamp import Swamp
from pirates.world.LocationConstants import LocationIds, getLocationList
from pirates.map.Mappable import MappableArea
import time

class DistributedGameArea(DistributedNode, MappableArea, StagedObject):
    notify = directNotify.newCategory('DistributedGameArea')

    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        NodePath.__init__(self, 'GameArea')
        MappableArea.__init__(self)
        StagedObject.__init__(self, StagedObject.OFF)
        self.uniqueId = ''
        self.geom = None
        self.funnelDisplayName = None
        self.previousDisplayName = None
        self.gameFSM = None
        self.links = []
        self.pendingSetupConnector = {}
        self.connectors = {}
        self.connectorInterests = set()
        self.envEffects = None
        self.spawnTriggers = []
        self.blockerColls = []
        self.islandWaterParameters = None
        self.swamp_water = None
        self.entryTime = [
         None, 0]
        self.timeCheck = 0
        self.minimap = None
        self.footprintNode = None
        self.popupDialog = None
        self.minimapArea = 0
        self.laMinimapObj = None
        self.footstepSound = None
        self.environment = None
        self.connectorsHereCallback = None
        return

    def __repr__(self):
        return '%s (%s)' % (DistributedNode.__repr__(self), self.getName() or self.uniqueId)

    def __str__(self):
        return '%s (%s)' % (DistributedNode.__repr__(self), self.getName() or self.uniqueId)

    def disable(self):
        taskMgr.remove('showEnterMessage')
        DistributedNode.disable(self)
        if self.geom:
            self.geom.removeNode()
        self.unloadConnectors()
        for request in self.pendingSetupConnector.itervalues():
            self.cr.relatedObjectMgr.abortRequest(request)

        self.pendingSetupConnector = {}
        self.builder.delete()
        self.builder = None
        return

    def delete(self):
        if base.zoneLODTarget == self:
            base.disableZoneLODs()
        for trigger in self.spawnTriggers:
            trigger.removeNode()

        del self.spawnTriggers
        del self.connectors
        del self.links
        if self.envEffects:
            self.envEffects.delete()
            self.envEffects = None
        DistributedNode.delete(self)
        if self.islandWaterParameters:
            del self.islandWaterParameters
        if self.swamp_water:
            self.swamp_water.delete()
            del self.swamp_water
        if self.popupDialog:
            self.popupDialog.destroy()
        del self.popupDialog
        self.connectorsHereCallback = None
        return

    def setLocation(self, parentId, zoneId):
        DistributedNode.setLocation(self, parentId, zoneId)
        if parentId:
            parent = self.getParentObj()
            self.reparentTo(parent)

    def setName(self, name):
        self.name = name

    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    @report(types=['frameCount', 'args'], dConfigParam='minimap')
    def handleChildArrive(self, childObj, zoneId):
        DistributedNode.handleChildArrive(self, childObj, zoneId)
        if childObj.isLocal():
            base.loadingScreen.endStep('enterArea')
            base.enableZoneLODs(self)
            childObj.refreshActiveQuestStep()
            localAvatar.guiMgr.setMinimap(self.minimap)
            localAvatar.setAreaFootstep(self.footstepSound)
            localAvatar.guiMgr.radarGui.showLocation(self.uniqueId)
            envName = base.worldCreator.environmentTable.get(self.uniqueId)
            if envName:
                environmentID = TODGlobals.ENVIRONMENT_NAMES_TO_ID.get(envName, TODGlobals.ENV_DEFAULT)
                envData = {}
                envSettings = base.worldCreator.uidEnvSettings.get(self.uniqueId)
                if envSettings != None:
                    envData = envSettings
                base.cr.timeOfDayManager.setEnvironment(environmentID, envData)
            else:
                envData = None
                envSettings = base.worldCreator.uidEnvSettings.get(self.uniqueId)
                if envSettings != None:
                    envData = envSettings
                base.cr.timeOfDayManager.setEnvironment(TODGlobals.ENV_INTERIOR, envData)
            self.builder.arrived()
        self.accept('transferMinimapObjects', self.transferMinimapObject)
        if self.minimap and hasattr(childObj, 'getMinimapObject'):
            if childObj.getMinimapObject():
                self.laMinimapObj = childObj.getMinimapObject()
                self.minimap.addObject(childObj.getMinimapObject())
        return

    def transferMinimapObject(self, guiMgr):
        if self.laMinimapObj:
            guiMgr.transferMinimapObject(self.laMinimapObj)

    @report(types=['frameCount', 'args'], dConfigParam='minimap')
    def handleChildLeave(self, childObj, zoneId):
        if childObj.isLocal():
            base.disableZoneLODs()
            localAvatar.guiMgr.clearMinimap(self.minimap)
            self.builder.localAvLeaving()
            self.builder.left()
        self.ignore('transferMinimapObjects')
        self.laMinimapObj = None
        if self.minimap and hasattr(childObj, 'getMinimapObject'):
            if childObj.getMinimapObject():
                self.minimap.removeObject(childObj.getMinimapObject())
        DistributedNode.handleChildLeave(self, childObj, zoneId)
        return

    def setUniqueId(self, uid):
        if self.uniqueId != '':
            self.cr.uidMgr.removeUid(self.uniqueId)
        self.uniqueId = uid
        self.cr.uidMgr.addUid(self.uniqueId, self.getDoId())

    def getUniqueId(self):
        return self.uniqueId

    def loadModel(self):
        pass

    @report(types=['args', 'deltaStamp'], dConfigParam=['jail'])
    def setLinks(self, links):
        for link in links:
            areaNode, connId, areaUid, connParent, connZone, connNode, connWorld, connWorldZone = link
            newLink = [connId, connParent, connZone, connWorld, connWorldZone]
            if newLink in self.links:
                continue
            self.links.append(newLink)

            def setupConnector(connector):
                self.connectors[connector.doId] = connector
                request = self.pendingSetupConnector.pop(connector.doId, None)
                if not request:
                    pass
                return

            connector = self.cr.doId2do.get(connId)
            if connector:
                self.pendingSetupConnector[connId] = None
                setupConnector(connector)
            elif connId:
                if connId in self.pendingSetupConnector:
                    request = self.pendingSetupConnector.pop(connId)
                    self.cr.relatedObjectMgr.abortRequest(request)
                request = self.cr.relatedObjectMgr.requestObjects([connId], eachCallback=setupConnector)
                self.pendingSetupConnector[connId] = request

        return

    @report(types=['args', 'deltaStamp'], dConfigParam=['jail', 'teleport'])
    def loadConnectors(self):
        for link in self.links:
            if link:
                connectorId = link[0]
                if connectorId not in self.connectorInterests or not self.cr.doId2do.has_key(connectorId):
                    if connectorId not in self.connectorInterests:
                        self.connectorInterests.add(connectorId)
                    parentId = link[1]
                    zoneId = link[2]
                    linkParentId = link[3]
                    linkParentZoneId = link[4]

                    def connectorParentHere(connectorId, parentId, zoneId):
                        connectorEvent = 'connector-%s' % connectorId
                        self.acceptOnce(connectorEvent, self.reparentConnector, extraArgs=[connectorId])
                        self.cr.addTaggedInterest(parentId, zoneId, self.cr.ITAG_GAME, 'Connectors-%s' % self.doId, event=connectorEvent, otherTags=['Connectors-%s' % self.doId])

                    connectorEvent = 'connector-%s' % connectorId
                    self.acceptOnce(connectorEvent, connectorParentHere, extraArgs=[connectorId, parentId, zoneId])
                    self.cr.addTaggedInterest(linkParentId, linkParentZoneId, self.cr.ITAG_GAME, 'ConnectorsParent-%s' % self.doId, event=connectorEvent, otherTags=['ConnectorsParent-%s' % self.doId])
                else:
                    self.reparentConnector(connectorId)

    @report(types=['args', 'deltaStamp'], dConfigParam=['jail', 'teleport'])
    def unloadConnectors(self):
        for connectorId, connector in self.connectors.iteritems():
            if connector:
                connector.setLoadedArea(None)
                connector.goOffStage()

        self.connectors = {}
        self.cr.removeInterestTag('Connectors-%s' % self.doId)
        self.cr.removeInterestTag('ConnectorsParent-%s' % self.doId)
        self.connectorInterests = set()
        return

    @report(types=['args', 'deltaStamp'], dConfigParam=['jail', 'teleport'])
    def reparentConnector(self, connectorId):
        connector = self.cr.doId2do.get(connectorId)
        if connector:
            self.connectors[connectorId] = connector
            connector.reparentConnectorToArea(self)
            if self.isOnStage():
                connector.goOnStage()
            else:
                connector.goOffStage()
            if self.connectorsHereCallback and len(self.connectors) == len(self.links):
                self.connectorsHereCallback()
                self.connectorsHereCallback = None
        return

    def setConnectorsHereCallback(self, callback):
        self.connectorsHereCallback = callback

    @report(types=['args', 'deltaStamp'], dConfigParam=['jail', 'teleport'])
    def handleEnterGameArea(self, collEntry=None):
        inventory = localAvatar.getInventory()
        if localAvatar.style.getTutorial() == PiratesGlobals.TUT_GOT_SEACHEST and self.uniqueId == LocationIds.RAMBLESHACK_ISLAND and len(inventory.getWeapons()) < 1 and base.localAvatar.showQuest:
            base.localAvatar.resetQuestShow()
            popupDialogText = [
             'showBlacksmith', 'closeShowBlacksmith']
            self.popupDialog = NewTutorialPanel(popupDialogText)

            def closeTutorialWindow():
                messenger.send(self.popupDialog.closeMessage)

            self.popupDialog.setYesCommand(closeTutorialWindow)
            self.acceptOnce('closeTutorialWindow', closeTutorialWindow)
            self.popupDialog.activate()
        taskMgr.doMethodLater(1, self.showEnterMessage, 'showEnterMessage')
        UserFunnel.logSubmit(0, 'ENTERING_' + str(self.funnelDisplayName))
        UserFunnel.logSubmit(1, 'ENTERING_' + str(self.funnelDisplayName))
        self.storeLocationTime(self.funnelDisplayName, time.time())
        displayName = PLocalizer.LocationNames.get(self.uniqueId)
        base.setLocationCode(displayName)
        self.builder.initEffects()

    def storeLocationTime(self, loc, time):
        if loc == self.entryTime[0]:
            if self.entryTime[1] == 0:
                self.entryTime[1] = time
            return
        else:
            self.entryTime = [
             loc, time]

    def readLocationTime(self):
        return self.entryTime[1]

    def showEnterMessage(self, task):
        displayName = PLocalizer.LocationNames.get(self.uniqueId)
        self.displayGameAreaName(displayName)

    @report(types=['args', 'deltaStamp'], dConfigParam=['jail', 'teleport'])
    def handleExitGameArea(self, collEntry=None):
        UserFunnel.logSubmit(0, 'EXITING_' + str(self.funnelDisplayName))
        UserFunnel.logSubmit(1, 'EXITING_' + str(self.funnelDisplayName))
        self.stopCustomEffects()
        self.previousDisplayName = None
        displayName = str(self.funnelDisplayName)
        timeSpent = int(time.time()) - int(self.readLocationTime())
        if int(self.timeCheck) + 1 == int(timeSpent) or int(self.timeCheck) - 1 == int(timeSpent) or int(self.timeCheck) == int(timeSpent):
            pass
        else:
            base.cr.centralLogger.writeClientEvent('EXITING_AREA|%s|%d' % (displayName, timeSpent))
            self.timeCheck = timeSpent
        return

    def displayGameAreaName(self, displayName):
        self.funnelDisplayName = displayName
        if self.previousDisplayName != displayName:
            self.previousDisplayName = displayName
            base.localAvatar.guiMgr.createTitle(displayName, PiratesGuiGlobals.TextFG2)

    def setPlayerBarrier(self, isOn):
        pass

    def setupCannonballLandColl(self, collNode, mask, index):
        if collNode and not collNode.isEmpty():
            collNode.node().setCollideMask(mask)
            collNode.setTag('objType', str(PiratesGlobals.COLL_LAND))
            collNode.setTag('groundCode', str(index))
            collNode.setTag('groundId', str(self.doId))

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker, itemEffects=[]):
        pass

    def startCustomEffects(self, interior=True, loadIslandMusic=False):
        if self.envEffects:
            self.envEffects.delete()
            self.envEffects = None
        if self.environment == 'Swamp':
            self.envEffects = SwampEffects.SwampEffects(self, self.modelPath)
            base.musicMgr.requestCurMusicFadeOut(removeFromPlaylist=False)
            base.musicMgr.request(SoundGlobals.MUSIC_SWAMP, priority=1, volume=0.6)
        else:
            if self.environment == 'Jungle':
                self.envEffects = ForestEffects.ForestEffects(self, self.modelPath)
                base.musicMgr.requestCurMusicFadeOut(removeFromPlaylist=False)
                base.musicMgr.request(SoundGlobals.MUSIC_JUNGLE, priority=1, volume=0.6)
            elif self.environment == 'Cave':
                self.envEffects = CaveEffects.CaveEffects(self, self.modelPath)
                base.musicMgr.requestCurMusicFadeOut(removeFromPlaylist=False)
                if self.uniqueId == LocationIds.RAVENS_COVE_MINE:
                    base.musicMgr.request(SoundGlobals.getMainMusic(self.uniqueId), priority=1, volume=0.6)
                else:
                    base.musicMgr.request(SoundGlobals.MUSIC_CAVE, priority=1, volume=0.6)
            elif self.uniqueId in ('1189479168.0sdnaik0', '1150922126.8akelts'):
                r = Reflection.getGlobalReflection()
                water = SeaPatch(self, reflection=r)
                water.loadSeaPatchFile('out.spf')
                self.water = water
                self.initializeIslandWaterParameters(self.geom)
            else:
                self.envEffects = EnvironmentEffects(self, self.modelPath)
                if interior:
                    pass
            if loadIslandMusic:
                if not base.localAvatar.isInInvasion():
                    base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_TORMENTA)
                    base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_TORMENTA_COMBAT)

                def getCurrentIslandMusic():
                    priZeros = []
                    for music in base.musicMgr.playlist:
                        if music.priority == 0:
                            priZeros.append(music)

                    return priZeros

                def changeMusic(music, pri):
                    for priZero in getCurrentIslandMusic():
                        base.musicMgr.requestFadeOut(priZero.name, removeFromPlaylist=True)

                    base.musicMgr.request(music, priority=0, volume=0.6)

                mainMusic = SoundGlobals.getMainMusic(self.uniqueId)
                altMusic = SoundGlobals.getAltMusic(self.uniqueId)
                if mainMusic and altMusic:
                    base.musicMgr.requestCurMusicFadeOut(removeFromPlaylist=True)
                    todMgr = base.cr.timeOfDayManager
                    todMgr.addTimeOfDayToggle('Day-Night Area Music', 6.0, 20.0, changeMusic, [mainMusic, 0], changeMusic, [altMusic, 0])
                elif mainMusic:
                    base.musicMgr.requestCurMusicFadeOut(removeFromPlaylist=True)
                    base.musicMgr.request(mainMusic, volume=0.6)
                elif altMusic:
                    base.musicMgr.requestCurMusicFadeOut(removeFromPlaylist=True)
                    base.musicMgr.request(altMusic, volume=0.6)
        self.builder.initEffects()
        return

    def stopCustomEffects(self):
        if self.envEffects:
            self.envEffects.delete()
            self.envEffects = None
        if 'swamp' in self.modelPath:
            base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_SWAMP, removeFromPlaylist=True)
        else:
            if 'jungle' in self.modelPath:
                base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_JUNGLE, removeFromPlaylist=True)
            elif self.uniqueId in getLocationList(LocationIds.ANY_CAVE):
                base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_CAVE, removeFromPlaylist=True)
                base.musicMgr.requestFadeOut(SoundGlobals.getMainMusic(self.uniqueId), removeFromPlaylist=True)
            elif self.uniqueId == '1189479168.0sdnaik0':
                self.water.delete()
                self.water = None
            if base.cr.timeOfDayManager:
                base.cr.timeOfDayManager.removeTimeOfDayToggle('Day-Night Area Music')
        return

    def updateAvReturnLocation(self, av, uniqueId):
        pass

    @report(types=['frameCount', 'args'], dConfigParam=['jail', 'teleport'])
    def quickLoadOtherSide(self):
        connector = self.connectors.get(localAvatar.lastConnectorId)
        if connector:
            connector.quickLoadOtherSide()

    def addSpawnTriggers(self, triggerSpheres):
        for x, y, z, triggerRadius, spawnPtId in triggerSpheres:
            objectSphere = CollisionSphere(x, y, z, triggerRadius)
            objectName = uniqueName('spawnTriggerSphere')
            objectSphere.setTangible(0)
            objectSphereNode = CollisionNode(objectName)
            objectSphereNode.addSolid(objectSphere)
            objectSphereNode.setIntoCollideMask(PiratesGlobals.WallBitmask)
            objectSphereNodePath = self.builder.collisions.attachNewNode(objectSphereNode)
            self.accept('enter' + objectName, self.handleEnterSphere, extraArgs=[spawnPtId])
            self.spawnTriggers.append(objectSphereNodePath)

    def handleEnterSphere(self, spawnPtId, entry):
        if base.localAvatar:
            if hasattr(base.localAvatar, 'getDoId'):
                doId = base.localAvatar.getDoId()
                self.sendUpdate('spawnNPC', [spawnPtId, doId])

    def initBlockers(self, geom):
        self.disableBlockers = False
        if base.config.GetBool('disable-blockers', 0):
            self.disableBlockers = True
        blockerColls = geom.findAllMatches('**/blocker_*;+s')
        interior = False
        if not blockerColls.isEmpty():
            if blockerColls[0].getName().find('_i') != -1:
                interior = True
            for i in range(0, blockerColls.getNumPaths()):
                self.blockerColls.append(blockerColls[i])
                if self.disableBlockers:
                    blockerColls[i].stash()

        if interior:
            self.accept('enterblocker_1_i', self.handleInteriorBlockerCollision)
        else:
            self.accept('enterblocker_1', self.handleBlockerCollision)
            self.accept('enterblocker_0', self.handleBlockerCollision)

    def stashSpecificBlocker(self, name):
        self.ignore('enter' + name)
        for blocker in self.blockerColls:
            if blocker.getName() == name:
                blocker.stash()

    def stashAllBlockers(self):
        self.ignore('enterblocker_1_i')
        self.ignore('enterblocker_1')
        self.ignore('enterblocker_0')
        for blocker in self.blockerColls:
            blocker.stash()

    def handleInteriorBlockerCollision(self, entry):
        questId = localAvatar.activeQuestId
        if base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_GOT_CUTLASS:
            questId = 'c2_visit_will_turner'
            localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.QuestStrings[questId]['blockerMessage'])
        else:
            self.stashAllBlockers()

    def handleBlockerCollision(self, entry):
        if base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_KILLED_1_SKELETON:
            questId = 'c2.2defeatSkeletons'
            localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.QuestStrings[questId]['blockerMessage'])
        elif base.localAvatar.style.getTutorial() < PiratesGlobals.TUT_GOT_COMPASS:
            questId = 'c2_visit_tia_dalma'
            self.stashSpecificBlocker('blocker_1')
            if entry.getIntoNodePath().getName() != 'blocker_1':
                localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.QuestStrings[questId]['blockerMessage'])
        else:
            self.stashAllBlockers()

    @report(types=['frameCount'], dConfigParam='connector')
    def handleOnStage(self):
        StagedObject.handleOnStage(self)
        for id, connector in self.connectors.iteritems():
            if connector:
                connector.goOnStage()

        self.builder.addCutsceneOriginNode()

    @report(types=['frameCount'], dConfigParam='connector')
    def handleOffStage(self):
        for id, connector in self.connectors.iteritems():
            if connector:
                connector.goOffStage()

        StagedObject.handleOffStage(self)

    def getTeleportDestPosH(self, index=0):
        pt = self._getTunnelSpawnPos(index)
        if not pt:
            self.notify.warning('could not find tunnel location %s' % self)
            return (0, 0, 0, 0)
        return (pt[0], pt[1], pt[2], 0)

    @report(types=['args'], dConfigParam='teleport')
    def _getTunnelSpawnPos(self, index=0):
        connectorNodes = self.findAllMatches('**/portal_exterior*') + self.findAllMatches('**/portal_interior*')
        if not connectorNodes:
            return None
        return self.getRelativePoint(connectorNodes[index % len(connectorNodes)], Point3(40, 0, 0))

    def initializeIslandWaterParameters(self, reference):
        debug = False
        island_water_parameters = IslandWaterParameters()
        world_position = self.getPos(render)
        world_x_offset = world_position[0]
        world_y_offset = world_position[1]
        world_z_offset = world_position[2]
        if debug:
            print self, '=', self.getName()
            print 'GAME AREA X OFF, Y OFF, Z OFF = ', world_x_offset, world_y_offset, world_z_offset
        self.swampAreaNode = reference.find('**/ocean')
        model = reference.find('**/water_color')
        if model:
            if debug:
                print 'WATER COLOR X OFF, Y OFF, Z OFF = ', world_x_offset, world_y_offset, world_z_offset
            model.hide()
            min_point = Point3(0)
            max_point = Point3(0)
            model.calcTightBounds(min_point, max_point)
            size = max_point - min_point
            if self.getH() == 180 or self.getH() == -180:
                x = -min_point[0] + world_x_offset
                y = -min_point[1] + world_y_offset
                x_size = -size[0]
                y_size = -size[1]
            else:
                x = min_point[0] + world_x_offset
                y = min_point[1] + world_y_offset
                x_size = size[0]
                y_size = size[1]
            island_water_parameters.map_x_origin = x
            island_water_parameters.map_y_origin = y
            island_water_parameters.map_x_scale = x_size
            island_water_parameters.map_y_scale = y_size
            if debug:
                print 'X, Y, X SIZE, Y SIZE = ', min_point[0], min_point[1], x_size, y_size
            texture = model.findTexture('*')
            if texture:
                island_water_parameters.water_color_texture = texture
                if debug:
                    print 'WATER COLOR TEXTURE', texture
        elif debug:
            print '*** water_color NODE NOT FOUND'
        model = reference.find('**/water_alpha')
        if model:
            if debug:
                print 'WATER ALPHA X OFF, Y OFF, Z OFF = ', world_x_offset, world_y_offset, world_z_offset
            model.hide()
            min_point = Point3(0)
            max_point = Point3(0)
            model.calcTightBounds(min_point, max_point)
            size = max_point - min_point
            if self.getH() == 180 or self.getH() == -180:
                x = -min_point[0] + world_x_offset
                y = -min_point[1] + world_y_offset
                x_size = -size[0]
                y_size = -size[1]
            else:
                x = min_point[0] + world_x_offset
                y = min_point[1] + world_y_offset
                x_size = size[0]
                y_size = size[1]
            island_water_parameters.alpha_map_x_origin = x
            island_water_parameters.alpha_map_y_origin = y
            island_water_parameters.alpha_map_x_scale = x_size
            island_water_parameters.alpha_map_y_scale = y_size
            if debug:
                print 'ALPHA X, Y, X SIZE, Y SIZE = ', min_point[0], min_point[1], x_size, y_size
            texture = model.findTexture('*')
            if texture:
                island_water_parameters.water_alpha_texture = texture
                if debug:
                    print 'WATER ALPHA TEXTURE', texture
        elif debug:
            print '*** water_alpha NODE NOT FOUND'
        use_shader = False
        if base.config.GetBool('want-shaders', 1) and base.win and base.win.getGsg() and base.win.getGsg().getShaderModel() >= GraphicsStateGuardian.SM20:
            use_shader = True
        model_ns = reference.find('**/water_swamp_ns')
        if model_ns:
            if use_shader:
                model_ns.hide()
            else:
                model_ns.show()
                model = model_ns
                model.setBin('water', 1)
                parent = model.getParent()
                model.detachNode()
                stencil_one_node_path = NodePath('stencil_one')
                stencil_one_node_path.reparentTo(parent)
                model.instanceTo(stencil_one_node_path)
                mask = 4294967295L
                stencil_one = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 1, mask, mask)
                stencil_one_node_path.setAttrib(stencil_one, 100)
                stencil_one_node_path.setDepthTest(0)
                if not base.useStencils:
                    stencil_one_node_path.hide()
        model_alpha_texture = None
        model_alpha = reference.find('**/water_alpha_swamp')
        if model_alpha:
            model_alpha_texture = model_alpha.findTexture('*')
            model_alpha.hide()
            if debug:
                print 'model_alpha_texture', model_alpha_texture
            if False:
                texture = model_alpha_texture
                card_x_size = 0.5
                card_y_size = 0.5
                card = CardMaker('test_texture_card')
                card.setFrame(-card_x_size, card_x_size, -card_y_size, card_y_size)
                card_node_path = NodePath(card.generate())
                card_node_path.setTexture(texture, 1)
                card_node_path.node().setBounds(OmniBoundingVolume())
                card_node_path.node().setFinal(1)
                card_node_path.reparentTo(render2d)
        else:
            model_alpha = None
        model = reference.find('**/water_color_swamp')
        if model:
            if use_shader:
                model.show()
                model_texture = model.findTexture('*')
                if debug:
                    print 'WATER COLOR SWAMP X OFF, Y OFF, Z OFF = ', world_x_offset, world_y_offset, world_z_offset
                parent = model.getParent()
                model.detachNode()
                stencil_one_node_path = NodePath('stencil_one')
                stencil_one_node_path.reparentTo(parent)
                model.instanceTo(stencil_one_node_path)
                mask = 4294967295L
                stencil_one = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 1, mask, mask)
                stencil_one_node_path.setAttrib(stencil_one, 100)
                stencil_one_node_path.setDepthTest(0)
                if not base.useStencils:
                    stencil_one_node_path.hide()
                min_point = Point3(0)
                max_point = Point3(0)
                model.calcTightBounds(min_point, max_point)
                size = max_point - min_point
                if self.getH() == 180 or self.getH() == -180:
                    x = -min_point[0] + world_x_offset
                    y = -min_point[1] + world_y_offset
                    x_size = -size[0]
                    y_size = -size[1]
                else:
                    x = min_point[0] + world_x_offset
                    y = min_point[1] + world_y_offset
                    x_size = size[0]
                    y_size = size[1]
                if debug:
                    print 'min_point', min_point
                    print 'max_point', max_point
                    print 'size', size
                    print 'x y', x, y
                island_water_parameters.swamp_map_x_origin = x
                island_water_parameters.swamp_map_y_origin = y
                island_water_parameters.swamp_map_x_scale = x_size
                island_water_parameters.swamp_map_y_scale = y_size
                if debug:
                    print 'X, Y, X SIZE, Y SIZE = ', min_point[0], min_point[1], x_size, y_size
                texture = model.findTexture('*')
                if texture:
                    island_water_parameters.swamp_water_color_texture = texture
                    if debug:
                        print 'SWAMP WATER COLOR TEXTURE', texture
                water_color_file_path = island_water_parameters.default_water_color_file_path
                alpha_texture_file_path = island_water_parameters.default_water_alpha_file_path
                opacity_texture_file_path = None
                shader_file_path = 'models/swamps/cuba_swamp001_2X.cg'
                reflection = Reflection.getGlobalReflection()
                self.swamp_water = Swamp(None, None, reflection, model, shader_file_path)
                island_water_parameters.swamp_water = self.swamp_water
                unload_previous_texture = True
                self.swamp_water.set_water_color_texture(water_color_file_path, unload_previous_texture, model_texture)
                self.swamp_water.set_water_alpha_texture(alpha_texture_file_path, unload_previous_texture, model_alpha_texture)
                self.swamp_water.set_wrap_or_clamp(True)
                r = 37.0
                g = 62.0
                b = 40.0
                self.swamp_water.water_r = r
                self.swamp_water.water_g = g
                self.swamp_water.water_b = b
                island_water_parameters.swamp_color_r = r
                island_water_parameters.swamp_color_g = g
                island_water_parameters.swamp_color_b = b
                x = 0.0
                y = 1.0
                speed = 3.2
                island_water_parameters.swamp_direction_x = x
                island_water_parameters.swamp_direction_y = y
                island_water_parameters.swamp_speed = speed
                self.swamp_water.update_water_direction_and_speed(x, y, speed)
            else:
                model.hide()
        elif debug:
            print '*** water_color_swamp NODE NOT FOUND'
        self.islandWaterParameters = island_water_parameters
        return

    def getLevel(self):
        return 1

    def announceGenerate(self):
        base.loadingScreen.tick()
        DistributedNode.announceGenerate(self)
        base.worldCreator.registerSpecialNodes(self, self.uniqueId)
        self.areaType = base.worldCreator.getFieldFromUid(self.uniqueId, 'Visibility')
        self.envSettings = base.worldCreator.getEnvSettingsByUid(self.uniqueId)
        self.builder = base.worldCreator.getBuilder(self, self.areaType)

    def retrieveFootprintNode(self):
        footprintCache = self.getFootprintCache()
        if footprintCache.hasData() and base.config.GetBool('want-disk-cache', 0):
            data = footprintCache.getData()
            newData = data.copySubgraph()
            footprintNode = NodePath(newData)
        else:
            footprintNode = self.buildFootprintNode()
        return footprintNode

    def getFootprintCache(self):
        return base.bamCache.lookup(Filename('/%s_footprint_%s.bam' % (self.uniqueId, base.gridDetail)), 'bam')

    def buildFootprintNode(self):
        footprintCache = self.getFootprintCache()
        footprintNode = self.builder.buildFootprintNode()
        footprintCache.setData(footprintNode.node(), 0)
        base.bamCache.store(footprintCache)
        return footprintNode

    @report(types=['frameCount', 'args'], dConfigParam='minimap')
    def hideMapNodes(self):
        mapNodes = self.geom.findAllMatches('**/minimap_*')
        mapNodes.hide()

    def setFootstepSound(self, footstepSound):
        self.footstepSound = footstepSound
        if self.footstepSound and base.localAvatar:
            base.localAvatar.setAreaFootstep(self.footstepSound)
            base.localAvatar.setSurfaceIndexFromLevelDefault()

    def setEnvironment(self, environment):
        self.environment = environment

    @report(types=['frameCount', 'args'], dConfigParam='minimap')
    def setMinimapPrefix(self, prefix):
        minimaps = self.geom.findAllMatches('**/minimap_*;+s')
        for map in minimaps:
            if prefix not in map.getName():
                map.detachNode()

        minimaps = sorted(self.geom.findAllMatches('**/minimap_*;+s'))
        for x, map in enumerate(minimaps):
            map.setName('minimap_%d' % x)

    @report(types=['frameCount', 'args'], dConfigParam='minimap')
    def getMapNode(self):
        mapNode = self.geom.find('**/minimap_%s' % (self.minimapArea,))
        if not mapNode:
            minSide = 1500.0
            a, b = self.geom.getTightBounds()
            diff = b - a
            sideScale = 1
            if diff[0] > diff[1]:
                if diff[0] < minSide:
                    sideScale = minSide / diff[0]
            elif diff[1] < minSide:
                sideScale = minSide / diff[1]
            cm = CardMaker('minimap-card')
            cm.setFrame(VBase4(a[0], b[0], a[1], b[1]) * sideScale)
            modelNode = ModelNode('minimap_0')
            modelNode.setPreserveTransform(1)
            mapNode = self.geom.attachNewNode(modelNode)
            mapGeom = mapNode.attachNewNode(cm.generate())
            mapGeom.setP(-90)
            mapGeom.hide()
        return mapNode

    def getMapName(self):
        return 'map-' + self.getUniqueId()

    def getFootprintNode(self):
        if not self.footprintNode:
            self.footprintNode = self.retrieveFootprintNode()
        return self.footprintNode.find('footprint_%s' % (self.minimapArea,)) or NodePath('footprint_%s' % (self.minimapArea,))

    def getShopNodes(self):
        shopNodes = self.builder.getMinimapShopNodes()
        mapNodes = NodePathCollection()
        for node in shopNodes:
            minimapArea = int(node.getTag('MinimapArea') or '0')
            if minimapArea == self.minimapArea:
                mapNodes.addPath(node)

        return mapNodes

    def getCapturePointNodes(self, holidayName):
        capturePoints = self.builder.getMinimapCapturePointNodes(holidayName)
        mapNodes = NodePathCollection()
        for node in capturePoints:
            minimapArea = int(node.getTag('MinimapArea') or '0')
            if minimapArea == self.minimapArea:
                mapNodes.addPath(node)

        return mapNodes

    def getZoomLevels(self):
        return ((150, 200, 300), 1)

    @report(types=['frameCount', 'args'], dConfigParam='minimap')
    def addMinimapObject(self, obj):
        if self.minimap:
            self.minimap.addObject(obj)

    @report(types=['frameCount', 'args'], dConfigParam='minimap')
    def removeMinimapObject(self, obj):
        if self.minimap:
            self.minimap.removeObject(obj)

    def ensureLoaded(self):
        pass

    @report(types=['args'], dConfigParam='minimap')
    def setMinimapArea(self, areaId):
        if areaId != self.minimapArea:
            self.minimapArea = areaId
            self.destroyMinimap()
            self.setupMinimap()
            self.minimap.addObject(localAvatar.getMinimapObject())
            self.loadConnectors()
            localAvatar.guiMgr.setMinimap(self.minimap)

    @report(types=['frameCount', 'args'], dConfigParam='minimap')
    def showTunnelOnMinimap(self, tunnelUid):
        return self.builder.getTunnelMinimap(tunnelUid) == self.minimapArea

    def getConnectorNodeNamed(self, name):
        return self.find('**/' + name + '*')

    @report(types=['args'], dConfigParam='minimap')
    def handleHolidayStarted(self, holiday):
        if self.minimap:
            self.minimap.handleHolidayStarted(self, holiday)

    @report(types=['args'], dConfigParam='minimap')
    def handleHolidayEnded(self, holiday):
        if self.minimap:
            self.minimap.handleHolidayEnded(self, holiday)