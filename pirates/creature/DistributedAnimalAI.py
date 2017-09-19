from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.creature.DistributedCreatureAI import *

class DistributedAnimalAI(DistributedCreatureAI):
    notify = directNotify.newCategory('DistributedAnimalAI')
    avatarType = AvatarTypes.Animal
