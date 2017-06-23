from direct.directnotify import DirectNotifyGlobal
from pirates.pirate.BipedAnimationMixer import BipedAnimationMixer

class HumanAnimationMixer(BipedAnimationMixer):
    notify = DirectNotifyGlobal.directNotify.newCategory('HumanAnimationMixer')