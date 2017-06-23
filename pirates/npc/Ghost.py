from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.pirate import Human
from pirates.pirate import AvatarTypes

class Ghost(Human.Human):

    def __init__(self, avatarType=AvatarTypes.Ghost):
        Human.Human.__init__(self)
        self.avatarType = avatarType