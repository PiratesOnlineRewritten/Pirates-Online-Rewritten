from pirates.world.AreaBuilderBaseAI import AreaBuilderBaseAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.piratesbase import PiratesGlobals
from pirates.leveleditor import ObjectList
from pirates.world.DistributedInteriorDoorAI import DistributedInteriorDoorAI
from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI
from pirates.minigame.DistributedHoldemTableAI import DistributedHoldemTableAI
from pirates.minigame.DistributedBlackjackTableAI import DistributedBlackjackTableAI

class InteriorAreaBuilderAI(AreaBuilderBaseAI):
    notify = directNotify.newCategory('InteriorAreaBuilderAI')

    def __init__(self, air, parent):
        AreaBuilderBaseAI.__init__(self, air, parent)

        self.wantParlorGames = config.GetBool('want-parlor-games', True)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic):
        newObj = None

        if objType == ObjectList.DOOR_LOCATOR_NODE:
            newObj = self.__createDoorLocatorNode(objectData, parent, parentUid, objKey)
        elif objType == 'Parlor Game' and self.wantParlorGames:
            newObj = self.__createParlorTable(objectData, parent, parentUid, objKey)
        elif objType in ['Animal', 'Townsperson', 'Spawn Node', 'Dormant NPC Spawn Node', 'Skeleton', 'NavySailor', 'Creature', 'Ghost']:
            newObj = self.air.spawner.createObject(objType, objectData, parent, parentUid, objKey, dynamic, PiratesGlobals.InteriorDoorZone)

        return newObj

    def __createDoorLocatorNode(self, objectData, parent, parentUid, objKey):
        exteriorDoor = self.parent.getExteriorDoor()

        if not exteriorDoor:
            self.notify.warning('Cannot create interior door for interior %d, with no exterior door!' % self.parent.doId)
            return

        interiorDoor = DistributedInteriorDoorAI(self.air)
        interiorDoor.setUniqueId(objKey)
        interiorDoor.setPos(objectData.get('Pos', (0, 0, 0)))
        interiorDoor.setHpr(objectData.get('Hpr', (0, 0, 0)))
        interiorDoor.setScale(objectData.get('Scale', 1))
        interiorDoor.setInteriorId(self.parent.doId, self.parent.parentId, self.parent.zoneId)
        interiorDoor.setExteriorId(exteriorDoor.parentId, exteriorDoor.getParentObj().parentId, exteriorDoor.zoneId)
        interiorDoor.setBuildingDoorId(exteriorDoor.doId)

        self.parent.setInteriorDoor(interiorDoor)
        self.parent.generateChildWithRequired(interiorDoor, PiratesGlobals.InteriorDoorZone)
        self.addObject(interiorDoor)

        return interiorDoor

    def __createParlorTable(self, objectData, parent, parentUid, objKey):

        tableCls = None
        gameType = objectData.get('Category', 'Unknown')

        if gameType == 'Holdem':
            tableCls = DistributedHoldemTableAI
        elif gameType == 'Blackjack':
            tableCls = DistributedBlackjackTableAI
        else:
            self.notify.warning('Failed to generate Parlor Table %s; %s is not a valid game type' % (objKey, gameType))
            return

        gameTable = tableCls(self.air)
        gameTable.setUniqueId(objKey)
        gameTable.setPos(objectData.get('Pos', (0, 0, 0)))
        gameTable.setHpr(objectData.get('Hpr', (0, 0, 0)))
        gameTable.setScale(objectData.get('Scale', 1))
        gameTable.setTableType(1)

        gameTable.generatePlayers(gameTable.AVAILABLE_SEATS, gameTable.TABLE_AI)

        if isinstance(gameTable, DistributedPokerTableAI):
            gameTable.setGameType(gameType)

        gameTable.setBetMultiplier(int(objectData.get('BetMultiplier', '1')))

        self.parent.generateChildWithRequired(gameTable, PiratesGlobals.InteriorDoorZone)
        self.addObject(gameTable)

        self.broadcastObjectPosition(gameTable)

        return gameTable


