from pirates.world.AreaBuilderBaseAI import AreaBuilderBaseAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.interact.DistributedSearchableContainerAI import DistributedSearchableContainerAI
from pirates.minigame.DistributedFishingSpotAI import DistributedFishingSpotAI
from pirates.minigame.DistributedPotionCraftingTableAI import DistributedPotionCraftingTableAI
from pirates.piratesbase import PiratesGlobals

class GridAreaBuilderAI(AreaBuilderBaseAI):
    notify = directNotify.newCategory('GridAreaBuilderAI')

    def __init__(self, air, parent):
        AreaBuilderBaseAI.__init__(self, air, parent)
        self.wantSearchables = config.GetBool('want-searchables', True)
        self.wantFishing = config.GetBool('want-fishing', True)
        self.wantPotionTable = config.GetBool('want-potion-table', True)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic):
        newObj = None

        if objType == 'Searchable Container' and self.wantSearchables:
            newObj = self.__generateSearchableContainer(parent, parentUid, objKey, objectData)
        elif objType == 'FishingSpot' and self.wantFishing:
            newObj = self.__generateFishingSpot(parent, parentUid, objKey, objectData)
        elif objType == 'PotionTable' and self.wantPotionTable:
            newObj = self.__generatePotionTable(parent, parentUid, objKey, objectData)
        elif objType in ['Animal', 'Townsperson', 'Spawn Node', 'Dormant NPC Spawn Node', 'Skeleton', 'NavySailor', 'Creature', 'Ghost']:
            newObj = self.air.spawner.createObject(objType, objectData, parent, parentUid, objKey, dynamic)

        return newObj

    def __generateSearchableContainer(self, parent, parentUid, objKey, objectData):
        container = DistributedSearchableContainerAI(self.air)

        container.setUniqueId(objKey)

        container.setPos(objectData['Pos'])
        container.setHpr(objectData['Hpr'])
        container.setScale(objectData['Scale'])
        container.setType(objectData.get('type', 'Crate'))
        container.setContainerColor(objectData['Visual'].get('Color', (0, 0, 0, 0)))
        container.setSearchTime(float(objectData.get('searchTime', '6.0')))
        container.setVisZone(objectData.get('VisZone', ''))
        container.setSphereScale(float(objectData.get('Aggro Radius', 1.0)))

        parent.generateChildWithRequired(container, PiratesGlobals.IslandLocalZone)
        self.addObject(container)

        locationName = parent.getLocalizerName()
        self.notify.debug('Generating Searchable %s (%s) under zone %d in %s at %s with doId %d' % (container.getType(), objKey, container.zoneId, locationName, container.getPos(), container.doId))

        return container

    def __generateFishingSpot(self, parent, parentUid, objKey, objectData):
        fishingSpot = DistributedFishingSpotAI(self.air)

        fishingSpot.setPos(objectData['Pos'])
        fishingSpot.setHpr(objectData['Hpr'])
        fishingSpot.setScale(objectData['Scale'])
        fishingSpot.setOceanOffset(float(objectData.get('Ocean Offset', 1)))

        parent.generateChildWithRequired(fishingSpot, PiratesGlobals.IslandLocalZone)
        self.addObject(fishingSpot)

        locationName = parent.getLocalizerName()
        self.notify.debug('Generating Fishing Spot (%s) under zone %d in %s at %s with doId %d' % (objKey, fishingSpot.zoneId, locationName, fishingSpot.getPos(), fishingSpot.doId))

        return fishingSpot

    def __generatePotionTable(self, parent, parentUid, objKey, objectData):
        table = DistributedPotionCraftingTableAI(self.air)

        table.setPos(objectData['Pos'])
        table.setHpr(objectData['Hpr'])
        table.setScale(objectData['Scale'])

        parent.generateChildWithRequired(table, PiratesGlobals.IslandLocalZone)
        self.addObject(table)

        locationName = parent.getLocalizerName()
        self.notify.debug('Generating Potion Crafting Table (%s) under zone %d in %s at %s with doId %d' % (objKey, table.zoneId, locationName, table.getPos(), table.doId))

        return table