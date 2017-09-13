from pirates.world.AreaBuilderBaseAI import AreaBuilderBaseAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.interact.DistributedSearchableContainerAI import DistributedSearchableContainerAI
from pirates.minigame.DistributedFishingSpotAI import DistributedFishingSpotAI
from pirates.piratesbase import PiratesGlobals

class GridAreaBuilderAI(AreaBuilderBaseAI):
    notify = directNotify.newCategory('GridAreaBuilderAI')

    def __init__(self, air, parent):
        AreaBuilderBaseAI.__init__(self, air, parent)
        self.wantSearchables = config.GetBool('want-searchables', True)
        self.wantFishing = config.GetBool('want-fishing', True)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic):
        newObj = None

        if objType == 'Searchable Container' and self.wantSearchables:
            newobj = self.__generateSearchableContainer(parent, parentUid, objKey, objectData)
        elif objType == 'FishingSpot' and self.wantFishing:
            newObj = self.__generateFishingSpot(parent, parentUid, objKey, objectData)

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