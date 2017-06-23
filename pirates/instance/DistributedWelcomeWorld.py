from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import report
from pirates.instance import DistributedInstanceBase
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import TODGlobals
from pirates.battle import EnemyGlobals
from pirates.pvp import PVPGlobals

class DistributedWelcomeWorld(DistributedInstanceBase.DistributedInstanceBase):
    notify = directNotify.newCategory('DistributedWelcomeWorld')

    @report(types=['args'], dConfigParam=['dteleport'])
    def handleOnStage(self):
        DistributedInstanceBase.DistributedInstanceBase.handleOnStage(self)
        base.cr.timeOfDayManager.setEnvironment(TODGlobals.ENV_DEFAULT)

    def getWorldPos(self, node):
        if not node.isEmpty() and self.isOnStage():
            return node.getPos(self)

    def getAggroRadius(self):
        return EnemyGlobals.MAX_SEARCH_RADIUS

    @report(types=['frameCount'], dConfigParam='jail')
    def localAvEnterDeath(self, av):
        DistributedInstanceBase.DistributedInstanceBase.localAvEnterDeath(self, av)
        self.d_localAvatarDied()