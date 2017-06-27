from otp.ai.TimeManagerAI import TimeManagerAI
from direct.directnotify import DirectNotifyGlobal

class PiratesTimeManagerAI(TimeManagerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesTimeManagerAI')
