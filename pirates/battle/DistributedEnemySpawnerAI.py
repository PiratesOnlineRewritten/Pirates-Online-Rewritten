from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.DistributedAnimalAI import DistributedAnimalAI
from pirates.npc.DistributedNPCTownfolkAI import DistributedNPCTownfolkAI
from pirates.piratesbase import PiratesGlobals
from pirates.pirate import AvatarTypes
from pirates.leveleditor import NPCList
from pirates.piratesbase import PLocalizer

class DistributedEnemySpawnerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedEnemySpawnerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.wantEnemies = config.GetBool('want-enemies', False)
        self.wantDormantSpawns = config.GetBool('want-dormant-spawns', False)
        self.wantTownfolk = config.GetBool('want-townfolk', True)
        self.wantAnimals = config.GetBool('want-animals', True)
        self.wantCreatures = config.GetBool('want-creatures', False)
        self.wantBosses = config.GetBool('want-bosses', False)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic):
        newObj = None

        if objType == 'Townsperson':
            if self.wantTownfolk:
                newObj = self.__generateTownsperon(objType, objectData, parent, parentUid, objKey, dynamic)
        elif objType == 'Spawn Node':
            if self.wantEnemies:
                newObj = self.__generateEnemy(objType, objectData, parent, parentUid, objKey, dynamic)
        elif objType == 'Dormant NPC Spawn Node':
            if self.wantEnemies and self.wantDormantSpawns:
                newObj = self.__generateEnemy(objType, objectData, parent, parentUid, objKey, dynamic)
        elif objType == 'Animal':
            if self.wantAnimals:
                newObj = self.__generateAnimal(objType, objectData, parent, parentUid, objKey, dynamic)
        elif objType == 'Creature':
            if self.wantCreatures and self.wantEnemies:
                pass
        elif objType == 'Skeleton':
            if self.wantEnemies and self.wantBosses:
                pass
        elif objType == 'NavySailor':
            if self.wantEnemies and self.wantBosses:
                pass
        else:
            self.notify.warning('Received unknown generate: %s' % objType)

        return newObj

    def __generateTownsperon(self, objType, objectData, parent, parentUid, objKey, dynamic):
        townfolk = DistributedNPCTownfolkAI(self.air)

        townfolk.setPos(objectData.get('Pos'))
        townfolk.setHpr(objectData.get('Hpr'))
        townfolk.setSpawnPos(*objectData.get('Pos'))
        townfolk.setScale(objectData.get('Scale'))
        townfolk.setUniqueId(objKey)

        animSet = objectData.get('AnimSet', 'default')
        noticeAnim1 = objectData.get('Notice Animation 1', '')
        noticeAnim2 = objectData.get('Notice Animation 2', '')
        greetingAnim = objectData.get('Greeting Animation', '')
        townfolk.setActorAnims(animSet, noticeAnim1, noticeAnim2, greetingAnim)

        townfolk.setIsGhost(int(objectData.get('GhostFX', 0)))
        if 'GhostColor' in objectData and objectData['GhostColor'].isdigit():
            townfolk.setGhostColor(int(objectData.get('GhostColor', 0)))

        townfolk.setLevel(int(objectData.get('Level', 0)))
        
        townfolk.setAggroRadius(float(objectData.get('Aggro Radius', 0)))

        name = PLocalizer.Unknown
        if objKey in NPCList.NPC_LIST:
            name = NPCList.NPC_LIST[objKey][NPCList.setName]
        townfolk.setName(name)

        if 'Start State' in objectData:
            townfolk.setStartState(objectData['Start State'])

        townfolk.setDNAId(objectData.get('DNA', ''))
        if objectData.get('CustomModel', '') != '':
            townfolk.setDNAId(objectData.get('CustomModel', ''))

        category = objectData.get('Category', '')
        if not hasattr(AvatarTypes, category):
            self.notify.warning('Failed to spawn Townfolk (%s); Unknown category %s' % (objKey, category))
            return
        townfolk.setAvatarType(getattr(AvatarTypes, category, AvatarTypes.Commoner))

        shopId = objectData.get('ShopID', 'PORT_ROYAL_DEFAULTS')
        if not hasattr(PiratesGlobals, shopId):
            self.notify.warning('Failed to spawn Townfolk (%s); Unknown shopId: %s' % (objKey, shopid))
        townfolk.setShopId(getattr(PiratesGlobals, shopId, 0))

        helpId = objectData.get('HelpID', 'NONE')
        if helpId and helpId.isdigit():
            townfolk.setHelpId(int(helpId))
           
        parent.generateChildWithRequired(townfolk, PiratesGlobals.IslandLocalZone)

        locationName = parent.getLocalizerName()
        townfolkName = townfolk.getName()
        self.notify.debug('Generating Townfolk "%s" (%s) under zone %d in %s at %s with doId %d' % (townfolkName, objKey, townfolk.zoneId, locationName, townfolk.getPos(), townfolk.doId))

        return townfolk

    def __generateEnemy(self, objType, objectData, parent, parentUid, objKey, dynamic):
        pass

    def __generateAnimal(self, objType, objectData, parent, parentUid, objKey, dynamic):

        species = objectData.get('Species', None)
        if not species:
            self.notify.warning('Failed to generate Animal %s; Species was not defined' % objKey)
            return

        if not hasattr(AvatarTypes, species):
            self.notify.warning('Failed to generate Animal %s; %s is not a valid species' % (objKey, species))
            return
        avatarType = getattr(AvatarTypes, species, AvatarTypes.Chicken)

        animalClass = DistributedAnimalAI
        if species == 'Raven':
            self.notify.warning('Attempted to spawn unsupported Animal: %s' % species)
            return

        animal = animalClass(self.air)

        animal.setPos(objectData.get('Pos'))
        animal.setHpr(objectData.get('Hpr'))
        animal.setSpawnPos(*objectData.get('Pos'))
        animal.setScale(objectData.get('Scale'))
        animal.setUniqueId(objKey)

        animal.setAvatarType(avatarType)

        parent.generateChildWithRequired(animal, PiratesGlobals.IslandLocalZone)

        locationName = parent.getLocalizerName()
        self.notify.debug('Generating %s (%s) under zone %d in %s at %s with doId %d' % (species, objKey, animal.zoneId, locationName, animal.getPos(), animal.doId))

        return animal