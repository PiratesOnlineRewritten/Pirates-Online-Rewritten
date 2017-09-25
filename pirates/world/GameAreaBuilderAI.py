from pirates.world.AreaBuilderBaseAI import AreaBuilderBaseAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.piratesbase import PiratesGlobals
from pirates.leveleditor import ObjectList
from pirates.interact.DistributedSearchableContainerAI import DistributedSearchableContainerAI
from pirates.minigame.DistributedFishingSpotAI import DistributedFishingSpotAI
from pirates.minigame.DistributedPotionCraftingTableAI import DistributedPotionCraftingTableAI
from pirates.minigame.DistributedRepairBenchAI import DistributedRepairBenchAI
from pirates.world.DistributedBuildingDoorAI import DistributedBuildingDoorAI
from pirates.world.DistributedDinghyAI import DistributedDinghyAI
from pirates.treasuremap.DistributedBuriedTreasureAI import DistributedBuriedTreasureAI
from pirates.treasuremap.DistributedSurfaceTreasureAI import DistributedSurfaceTreasureAI

class GameAreaBuilderAI(AreaBuilderBaseAI):
    notify = directNotify.newCategory('GridAreaBuilderAI')
    AREAZONE = PiratesGlobals.IslandLocalZone

    def __init__(self, air, parent):
        AreaBuilderBaseAI.__init__(self, air, parent)

        self.wantSearchables = config.GetBool('want-searchables', True)
        self.wantFishing = config.GetBool('want-fishing-game', True)
        self.wantPotionTable = config.GetBool('want-potion-game', False)
        self.wantBuildingInteriors = config.GetBool('want-building-interiors', True)
        self.wantDinghys = config.GetBool('want-dignhys', True)
        self.wantSpawnNodes = config.GetBool('want-spawn-nodes', False)
        self.wantRepairBench = config.GetBool('want-repair-game', True)
        self.wantIslandAreas = config.GetBool('want-island-game-areas', True)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic):
        newObj = None

        if objType == 'Searchable Container' and self.wantSearchables:
            newObj = self.__createSearchableContainer(parent, parentUid, objKey, objectData)
        elif objType == 'FishingSpot' and self.wantFishing:
            newObj = self.__createFishingSpot(parent, parentUid, objKey, objectData)
        elif objType == 'PotionTable' and self.wantPotionTable:
            newObj = self.__createPotionTable(parent, parentUid, objKey, objectData)
        elif objType in ['Animal', 'Townsperson', 'Spawn Node', 'Dormant NPC Spawn Node', 'Skeleton', 'NavySailor', 'Creature', 'Ghost']:
            newObj = self.air.spawner.createObject(objType, objectData, parent, parentUid, objKey, dynamic)
        elif objType == 'Building Exterior' and self.wantBuildingInteriors:
            newObj = self.__createBuildingExterior(parent, parentUid, objKey, objectData)
        elif objType == ObjectList.DOOR_LOCATOR_NODE and self.wantBuildingInteriors:
            newObj = self.__createDoorLocatorNode(parent, parentUid, objKey, objectData)
        elif objType == 'Dinghy' and self.wantDinghys:
            newObj = self.__createDinghy(parent, parentUid, objKey, objectData)
        elif objType == 'Object Spawn Node' and self.wantSpawnNodes:
            newObj = self.__createObjectSpawnNode(parent, parentUid, objKey, objectData)
        elif objType == 'RepairBench' and self.wantRepairBench:
            newObj = self.__createRepairBench(parent, parentUid, objKey, objectData)
        elif objType == ObjectList.AREA_TYPE_ISLAND_REGION and self.wantIslandAreas:
            newObj = self.__createIslandArea(parent, parentUid, objKey, objectData)

        return newObj

    def __createSearchableContainer(self, parent, parentUid, objKey, objectData):
        container = DistributedSearchableContainerAI(self.air)
        container.setUniqueId(objKey)
        container.setPos(self.getObjectTruePos(objKey, parentUid, objectData))
        container.setHpr(objectData.get('Hpr', (0, 0, 0)))
        container.setScale(objectData.get('Scale', (1, 1, 1)))
        container.setType(objectData.get('type', 'Crate'))

        if 'Visual' in objectData and 'Color' in objectData['Visual']:
            container.setContainerColor(objectData['Visual'].get('Color', (1.0, 1.0, 1.0, 1.0)))

        container.setSearchTime(float(objectData.get('searchTime', '6.0')))
        container.setVisZone(objectData.get('VisZone', ''))
        container.setSphereScale(float(objectData.get('Aggro Radius', 1.0)))

        parent.generateChildWithRequired(container, PiratesGlobals.IslandLocalZone)
        self.addObject(container)
        self.broadcastObjectPosition(container)

        return container

    def __createFishingSpot(self, parent, parentUid, objKey, objectData):
        fishingSpot = DistributedFishingSpotAI(self.air)
        fishingSpot.setPos(self.getObjectTruePos(objKey, parentUid, objectData))
        fishingSpot.setHpr(objectData.get('Hpr', (0, 0, 0)))
        fishingSpot.setScale(objectData.get('Scale', (1, 1, 1)))
        fishingSpot.setOceanOffset(float(objectData.get('Ocean Offset', 1)))

        parent.generateChildWithRequired(fishingSpot, PiratesGlobals.IslandLocalZone)
        self.addObject(fishingSpot)
        self.broadcastObjectPosition(fishingSpot)

        return fishingSpot

    def __createPotionTable(self, parent, parentUid, objKey, objectData):
        table = DistributedPotionCraftingTableAI(self.air)
        table.setPos(self.getObjectTruePos(objKey, parentUid, objectData))
        table.setHpr(objectData.get('Hpr', (0, 0, 0)))
        table.setScale(objectData.get('Scale', (1, 1, 1)))

        table.setPotionZone(int(objectData.get('Potion Zone', 0)))

        parent.generateChildWithRequired(table, PiratesGlobals.IslandLocalZone)
        self.addObject(table)
        self.broadcastObjectPosition(table)

        return table

    def __createBuildingExterior(self, parent, parentUid, objKey, objectData):
        from pirates.world.DistributedJailInteriorAI import DistributedJailInteriorAI
        from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI

        interiorFile = objectData.get('File', None)
        exteriorUid = objectData.get('ExtUid', None)

        if not interiorFile:
            return None

        interiorModel = self.air.worldCreator.getModelPathFromFile(interiorFile)
        if not interiorModel:
            self.notify.warning('Failed to spawn interior: %s; No interior model found in %s.' % (objKey, interiorFile))
            return None

        interiorClass = DistributedJailInteriorAI if 'Jail' in interiorFile else DistributedGAInteriorAI
        interior = interiorClass(self.air)
        interior.setUniqueId(exteriorUid)
        interior.setHpr(objectData.get('Hpr', (0, 0, 0)))
        interior.setHpr(objectData.get('Hpr', (0, 0, 0)))
        interior.setScale(objectData.get('Scale', 1))
        interior.setModelPath(interiorModel)
        interior.setName(interior.getLocalizerName())

        self.parent.getParentObj().generateChildWithRequired(interior, self.air.allocateZone())
        self.parent.getParentObj().builder.addObject(interior, objKey)

        self.air.worldCreator.loadObjectDict(objectData.get('Objects', {}), self.parent, objKey, False)
        self.air.worldCreator.loadObjectsFromFile(interiorFile + '.py', interior)

        return interior

    def __createDoorLocatorNode(self, parent, parentUid, objKey, objectData):
        from pirates.world.DistributedGAInteriorAI import DistributedGAInteriorAI

        interior = self.parent.getParentObj().uidMgr.justGetMeMeObject(parentUid)

        if not interior or not isinstance(interior, DistributedGAInteriorAI):
            self.notify.warning('Cannot create door for a non-existant interior %s!' % parentUid)
            return

        buildingDoor = DistributedBuildingDoorAI(self.air)
        buildingDoor.setUniqueId(objKey)
        buildingDoor.setHpr(objectData.get('Hpr', (0, 0, 0)))
        buildingDoor.setHpr(objectData.get('Hpr', (0, 0, 0)))
        buildingDoor.setScale(objectData.get('Scale', 1))
        buildingDoor.setInteriorId(interior.doId, interior.getUniqueId(), interior.parentId, interior.zoneId)
        buildingDoor.setBuildingUid(parentUid)

        interior.setExteriorDoor(buildingDoor)
        self.parent.generateChildWithRequired(buildingDoor, PiratesGlobals.IslandLocalZone)
        self.addObject(buildingDoor)

        return buildingDoor

    def __createDinghy(self, parent, parentUid, objKey, objectData):
        dinghy = DistributedDinghyAI(self.air)
        dinghy.setPos(self.getObjectTruePos(objKey, parentUid, objectData))
        dinghy.setHpr(objectData.get('Hpr', (0, 0, 0)))
        dinghy.setInteractRadius(float(objectData.get('Aggro Radius', 25)))

        parent.generateChildWithRequired(dinghy, PiratesGlobals.IslandLocalZone)
        self.addObject(dinghy)
        self.broadcastObjectPosition(dinghy)

        return dinghy

    def __createObjectSpawnNode(self, parent, parentUid, objKey, objectData):
        spawnClass = DistributedSurfaceTreasureAI if objectData['Spawnables'] == 'Surface Treasure' else DistributedBuriedTreasureAI

        spawnNode = spawnClass(self.air)
        spawnNode.setPos(self.getObjectTruePos(objKey, parentUid, objectData))
        spawnNode.setHpr(objectData.get('Hpr', (0, 0, 0)))
        spawnNode.setScale(objectData.get('Scale', (1, 1, 1)))
        spawnNode.setStartingDepth(int(objectData.get('startingDepth', 10)))
        spawnNode.setCurrentDepth(spawnNode.getStartingDepth())
        spawnNode.setVisZone(objectData.get('VisZone', ''))

        parent.generateChildWithRequired(spawnNode, PiratesGlobals.IslandLocalZone)
        self.addObject(spawnNode)
        self.broadcastObjectPosition(spawnNode)

        return spawnNode

    def __createRepairBench(self, parent, parentUid, objKey, objectData):
        bench = DistributedRepairBenchAI(self.air)
        bench.setPos(self.getObjectTruePos(objKey, parentUid, objectData))
        bench.setHpr(objectData.get('Hpr', (0, 0, 0)))
        bench.setScale(objectData.get('Scale', (1, 1, 1)))
        bench.setDifficulty(int(objectData.get('difficulty', '0')))

        parent.generateChildWithRequired(bench, PiratesGlobals.IslandLocalZone)
        self.addObject(bench)
        self.broadcastObjectPosition(bench)

        return bench

    def __createIslandArea(self, parent, parentUid, objKey, objectData):
        from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI

        areaFile = objectData.get('File', None)
        if not areaFile:
            self.notify.warning('Failed to generate Island Game Area %s; No file defined' % objKey)
            return

        islandArea = DistributedGameAreaAI(self.air)
        islandArea.setUniqueId(objKey)
        islandArea.setName(islandArea.getLocalizerName())
        islandArea.setModelPath(objectData['Visual']['Model'])

        self.parent.generateChildWithRequired(islandArea, self.air.allocateZone())
        self.addObject(islandArea)
        self.broadcastObjectPosition(islandArea)
        self.air.worldCreator.loadObjectsFromFile(areaFile + '.py', islandArea)

        return islandArea
