from otp.otpbase import OTPGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.effects.Bonfire import Bonfire
from pirates.battle import DistributedIslandCannon

class DistributedFortCannon(DistributedIslandCannon.DistributedIslandCannon):
    notify = directNotify.newCategory('DistributedFortCannon')

    def __init__(self, cr):
        DistributedIslandCannon.DistributedIslandCannon.__init__(self, cr)

    def loadModel(self):
        DistributedIslandCannon.DistributedIslandCannon.loadModel(self)

    def announceGenerate(self):
        DistributedIslandCannon.DistributedIslandCannon.announceGenerate(self)
        self.notify.debug('doId=%s pos=%s renderPos=%s parent=%s' % (self.doId, self.getPos(), self.getPos(render), self.getParent()))
        self.prop.fortId = self.fortId

    def setFortId(self, fortId):
        self.fortId = fortId

    def setDestructState(self, state):
        if state != self.destructState:
            self.destructState = state
            if self.destructState == PiratesGlobals.CANNON_STATE_DESTRUCT:
                self.request('Off')
            else:
                self.request('Idle')
                if self.bf:
                    self.bf.removeNode()
                    self.bf = None
        return