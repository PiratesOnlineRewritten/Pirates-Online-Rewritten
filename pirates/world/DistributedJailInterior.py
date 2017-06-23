from pandac.PandaModules import *
from pirates.world.DistributedGAInterior import DistributedGAInterior
from pirates.piratesbase import PiratesGlobals

class DistributedJailInterior(DistributedGAInterior):
    notify = directNotify.newCategory('DistributedJailInterior')

    def announceGenerate(self):
        DistributedGAInterior.announceGenerate(self)
        doorPlanes = self.geom.findAllMatches('**/door_collision_planar_*;+s')
        doorPlanes.stash()

    @report(types=['frameCount', 'args'], dConfigParam='jail')
    def handleChildArrive(self, childObj, zoneId):
        DistributedGAInterior.handleChildArrive(self, childObj, zoneId)
        if childObj.isLocal() and childObj.belongsInJail():
            localAvatar.b_setGameState('ThrownInJail')
            if not self.footstepSound:
                localAvatar.setAreaFootstep('Rock')

    @report(types=['frameCount', 'args'], dConfigParam='jail')
    def handleAvatarSetLocation(self, parentId, zoneId):
        if parentId != self.doId:
            logBlock(4, 'jailed avatar is leaving before ThrownInJail is complete.\nGoing to %s (%s,%s)' % (self.cr.doId2do.get(parentId), parentId, zoneId))