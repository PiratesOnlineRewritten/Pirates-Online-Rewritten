from direct.directnotify import DirectNotifyGlobal
from pirates.creature import DistributedCreature
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals
from otp.otpbase import OTPRender

class DistributedAnimal(DistributedCreature.DistributedCreature):

    def __init__(self, cr):
        DistributedCreature.DistributedCreature.__init__(self, cr)
        self.battleCollisionBitmask = PiratesGlobals.WallBitmask | PiratesGlobals.TargetBitmask
        OTPRender.renderReflection(False, self, 'p_animal', None)
        return

    def setupCreature(self, avatarType):
        DistributedCreature.DistributedCreature.setupCreature(self, avatarType)
        self.motionFSM.motionAnimFSM.setupSplashAnimOverride(self.creature.getSplashOverride())
        self.motionFSM.motionAnimFSM.setupSplashAnimOverrideDelay(12)

    def customInteractOptions(self):
        self.setInteractOptions(proximityText=None, allowInteract=False)
        return

    def showHpMeter(self):
        pass

    def isBattleable(self):
        return 0

    def initializeBattleCollisions(self):
        pass

    def getMinimapObject(self):
        return None

    def canIdleSplashEver(self):
        return self.creature.getSplashOverride()

    def canIdleSplash(self):
        return self.creature.getCurrentAnim() == 'idle'