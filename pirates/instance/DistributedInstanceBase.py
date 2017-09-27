from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.StagedObject import StagedObject
from pirates.world.DistributedGameArea import DistributedGameArea
from pirates.world.DistributedOceanGrid import DistributedOceanGrid
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from direct.interval.IntervalGlobal import *
from pirates.uberdog import DistributedInventoryBase
from pirates.cutscene import Cutscene
from pirates.battle import EnemyGlobals
import random
from pirates.leveleditor import ObjectList

class DistributedInstanceBase(NodePath, DistributedObject, StagedObject):
    notify = directNotify.newCategory('DistributedInstanceBase')

    def __init__(self, cr):
        NodePath.__init__(self, 'InstanceBase')
        DistributedObject.__init__(self, cr)
        StagedObject.__init__(self, StagedObject.OFF)
        self.islands = {}
        self.playerSpawnPts = {}
        self.playerBootPts = {}
        self.cutsceneOriginNodes = {}
        self.type = PiratesGlobals.INSTANCE_GENERIC
        self.spawnInfo = None
        self.pendingJail = None
        self._onOffState = False
        if hasattr(localAvatar, 'gameFSM') and localAvatar.gameFSM:
            localAvatar.gameFSM.setDefaultGameState('LandRoam')

        self.worldGrid = None
        self.fireworkShowMgr = None

    def disable(self):
        DistributedObject.disable(self)
        self.detachNode()
        self.ignoreAll()

    def delete(self):
        if self.pendingJail:
            self.cr.relatedObjectMgr.abortRequest(self.pendingJail)
            self.pendingJail = None

        self.removeNode()
        self.cr.clearActiveWorld(self)
        DistributedObject.delete(self)

    def announceGenerate(self):
        self.reparentTo(render)
        DistributedObject.announceGenerate(self)
        base.worldCreator.loadFileDataRecursive(self.fileName + '.py')
        base.worldCreator.registerFileObject(self.fileName + '.py')
        self.stash()

    def setFileName(self, fileName):
        self.fileName = fileName

    def queryActiveQuests(self):

        def receiveActiveQuests(inventory):
            if inventory:
                for currQuest in inventory.getQuestList():
                    currQuest.setActive()

        DistributedInventoryBase.DistributedInventoryBase.getInventory(localAvatar.inventoryId, receiveActiveQuests)

    def getInstanceNodePath(self):
        return render

    def setWorldGrid(self, grid):
        self.worldGrid = grid

    def hasWater(self):
        if not self.isGenerated():
            self.notify.warning('Trying to get water for non-generated world')
            return None

        if not self.worldGrid:
            self.notify.warning('Trying to get water for world without worldGrid')
            return None

        return hasattr(self.worldGrid, 'water')

    def getWater(self):
        if not self.isGenerated():
            self.notify.warning('Trying to get water for non-generated world')
            return None

        if not self.worldGrid:
            self.notify.warning('Trying to get water for world without worldGrid')
            return None

        if not hasattr(self.worldGrid, 'water'):
            self.notify.warning('Trying to get water for worldGrid without water')
            return None

        return self.worldGrid.water

    def addCutsceneOriginNode(self, node, name):
        self.cutsceneOriginNodes[name] = node

    def addEntityObject(self, node):
        entityTypeName = node.getTag('EntityType')
        entityCatName = node.getTag('EntityCat')
        entity = None
        if entityTypeName and entityCatName:
            entityEntry = ObjectList.AVAIL_OBJ_LIST[entityCatName][entityTypeName]
            entityClassName = entityEntry.get('Entity')
            entityClass = ObjectList.ENTITY_DICT.get(entityClassName)
            if entityClass:
                entity = entityClass()
        if entity:
            for propertyKey in entityEntry['Properties']:
                tagData = node.getTag(propertyKey)
                if tagData:
                    entity.setProperty(propertyKey, tagData)

        entity.reparentTo(node)
        return entity

    def getCutsceneOriginNode(self, name):
        if name in self.cutsceneOriginNodes:
            return self.cutsceneOriginNodes.get(name)
        node = render.find('**/%s' % name)
        if not node.isEmpty():
            return node
        return None

    def addPlayerSpawnPt(self, parent, spawnPt, index=PiratesGlobals.ANY_LOCATION_SPAWN_INDEX):
        spawnPts = self.playerSpawnPts.setdefault(parent.getDoId(), {})
        spawnPts.setdefault(index, []).append(spawnPt)

    def getPlayerSpawnPt(self, parentDoId, index=PiratesGlobals.ANY_LOCATION_SPAWN_INDEX):
        spawnPts = self.playerSpawnPts.get(parentDoId, {})
        spawnPt = random.choice(spawnPts.get(index, [None]))
        if not spawnPt and index >= 0:
            return getPlayerSpawnPt(parentDoId, index=PiratesGlobals.ANY_LOCATION_SPAWN_INDEX)
        else:
            return spawnPt

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    @report(types=['deltaStamp', 'args'], dConfigParam=('jail', 'teleport'))
    def setSpawnInfo(self, xPos, yPos, zPos, h, spawnZone, parents):
        self.spawnInfo = [(xPos, yPos, zPos, h, 0, 0), spawnZone, parents]
        messenger.send(self.uniqueName('spawnInfoReceived'))

    def localAvEnterDeath(self, av):
        self.showDeathLoadingScreen(av)

    def localAvExitDeath(self, av):
        pass

    def showDeathLoadingScreen(self, av):
        base.cr.loadingScreen.showHint()
        base.cr.loadingScreen.showTarget(jail=True)
        base.cr.loadingScreen.show()

    def hideDeathLoadingScreen(self, av):
        base.cr.loadingScreen.hide()

    def updateShipProximityText(self, ship):
        pass

    def handleShipUse(self, ship):
        return False

    def updateTreasureProximityText(self, treasure):
        pass

    def handleTreasureUse(self, treasure):
        return False

    def handleDeposit(self, team, avId, bankId):
        pass

    def handleUseKey(self, interactiveObj):
        return False

    def setLocalAvatarDefaultGameState(self, loot):
        localAvatar.gameFSM.setDefaultGameState('LandRoam')

    def handleLocalAvatarEnterWater(self):
        localAvatar.b_setGameState('WaterRoam')

    def handleLocalAvatarExitWater(self):
        localAvatar.b_setGameState('LandRoam')

    def handleChildArrive(self, child, zoneId):
        DistributedObject.handleChildArrive(self, child, zoneId)
        if isinstance(child, DistributedOceanGrid):
            child.reparentTo(self)
            self.setWorldGrid(child)
            for key in self.islands:
                self.islands[key].addToOceanSeapatch()

    def handleChildLeave(self, child, zoneId):
        if isinstance(child, DistributedOceanGrid):
            if child == self.worldGrid:
                self.setWorldGrid(None)

        DistributedObject.handleChildLeave(self, child, zoneId)

    @report(types=['frameCount', 'args'], dConfigParam=['want-connector-report', 'want-jail-report'])
    def addWorldInterest(self, area=None):
        self.cr.setActiveWorld(self)
        self.turnOn(localAvatar)

    @report(types=['frameCount', 'args'], dConfigParam=['want-connector-report', 'want-jail-report'])
    def removeWorldInterest(self, area=None):
        if area:
            self.turnOff([area])
        else:
            self.turnOff()

    @report(types=['frameCount', 'args'], dConfigParam=['want-connector-report', 'want-jail-report'])
    def turnOff(self, cacheIslands=[]):
        self._turnOffIslands(cacheIslands)
        self.stash()
        self._onOffState = False
        if self.worldGrid:
            self.worldGrid.turnOff()

    @report(types=['frameCount', 'args'], dConfigParam=['want-connector-report', 'want-jail-report'])
    def turnOn(self, av=None):
        self.unstash()
        self._onOffState = True
        self.worldGrid.turnOn(av)

    def _turnOffIslands(self, cacheIslands=[]):
        for island in self.islands.values():
            cache = island in cacheIslands
            island.turnOff()

    def _turnOnIslands(self):
        for island in self.islands.values():
            island.turnOn()

    def isOn(self):
        return self._onOffState

    @report(types=['frameCount', 'args'], dConfigParam=['connector', 'jail'])
    def handleOffStage(self, cacheAreas=[]):
        if hasattr(self, 'islands'):
            self.stash()
            for area in self.islands.values():
                area.goOffStage(area in cacheAreas)

        StagedObject.handleOffStage(self)

    @report(types=['frameCount', 'args'], dConfigParam=['connector', 'jail'])
    def handleOnStage(self):
        StagedObject.handleOnStage(self)
        self.cr.setActiveWorld(self)
        self.unstash()
        if self.worldGrid:
            self.worldGrid.goOnStage()

        for island in self.islands.values():
            if island:
                island.goOnStage()

    def enteredSphere(self, params, collEntry):
        msgName = params[0]
        sphere = collEntry.getIntoNodePath()
        uniqueId = sphere.getTag('uid')
        if not uniqueId:
            uniqueId = params[1]
        objId = None
        if collEntry.getFromNodePath().hasNetTag('avId'):
            objId = int(collEntry.getFromNodePath().getNetTag('avId'))
            if objId:
                messenger.send(msgName + PiratesGlobals.SPHERE_ENTER_SUFFIX, [uniqueId, objId])
        if collEntry.getFromNodePath().hasNetTag('shipId'):
            objId = int(collEntry.getFromNodePath().getNetTag('shipId'))
            if objId:
                messenger.send(msgName + PiratesGlobals.SPHERE_ENTER_SUFFIX, [uniqueId, objId])
        if msgName == PiratesGlobals.LOCATION_SPHERE:
            displayName = PLocalizer.LocationNames.get(uniqueId, '')
            base.localAvatar.guiMgr.createTitle(displayName, PiratesGuiGlobals.TextFG2)
            parentUid = sphere.getTag('parentUid')
            parentDoId = base.cr.uidMgr.getDoId(parentUid)
            areaParent = base.cr.doId2do[parentDoId]
            locationInfo = areaParent.builder.getLocationInfo(uniqueId)
            if locationInfo:
                localAvatar.sendUpdate('enterAreaSphere', [uniqueId, parentUid])
        return

    def exitedSphere(self, params, collEntry):
        msgName = params[0]
        sphere = collEntry.getIntoNodePath()
        uniqueId = sphere.getTag('uid')
        if not uniqueId:
            uniqueId = params[1]
        objId = None
        if collEntry.getFromNodePath().hasNetTag('avId'):
            objId = int(collEntry.getFromNodePath().getNetTag('avId'))
            if objId:
                messenger.send(msgName + PiratesGlobals.SPHERE_EXIT_SUFFIX, [uniqueId, objId])
        if collEntry.getFromNodePath().hasNetTag('shipId'):
            objId = int(collEntry.getFromNodePath().getNetTag('shipId'))
            if objId:
                messenger.send(msgName + PiratesGlobals.SPHERE_EXIT_SUFFIX, [uniqueId, objId])
        if msgName == PiratesGlobals.LOCATION_SPHERE:
            parentUid = sphere.getTag('parentUid')
            parentDoId = base.cr.uidMgr.getDoId(parentUid)
            areaParent = base.cr.doId2do[parentDoId]
            locationInfo = areaParent.builder.getLocationInfo(uniqueId)
            if locationInfo:
                print 'left area %s' % locationInfo[2]
                localAvatar.sendUpdate('leaveAreaSphere', [uniqueId, parentUid])
        return

    def d_localAvatarDied(self):
        self.sendUpdate('avatarDied')

    def getWorldPos(self, node):
        return None

    def getAggroRadius(self):
        return EnemyGlobals.INTERIOR_MAX_SEARCH_RADIUS
