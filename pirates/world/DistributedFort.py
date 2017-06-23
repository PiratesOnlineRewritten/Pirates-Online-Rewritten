from pandac.PandaModules import NodePath, BillboardEffect, Vec3, Vec4, Point3
from direct.directnotify import DirectNotifyGlobal
from pirates.battle import DistributedBattleAvatar
from pirates.pirate import BattleAvatarGameFSM
from direct.distributed import DistributedSmoothNode
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import Freebooter
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals, HpMeter
from direct.gui.DirectGui import DirectWaitBar, DGG
from pandac.PandaModules import TextNode
from pirates.treasuremap import TreasureMapBlackPearlGlobals
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.ShipDebris import ShipDebris
from direct.interval.LerpInterval import LerpPosHprInterval
from direct.interval.LerpInterval import LerpHprInterval
from pirates.effects.SmokeExplosion import SmokeExplosion
from direct.interval.IntervalGlobal import *
from pirates.effects import TextEffect
from pirates.reputation.DistributedReputationAvatar import DistributedReputationAvatar
from otp.otpbase import OTPRender

class DistributedFort(DistributedBattleAvatar.DistributedBattleAvatar):
    notify = directNotify.newCategory('DistributedFort')
    endingR = 60
    zeroHpR = 90
    HpTextGenerator = TextNode('HpTextGenerator')
    HpTextEnabled = 1

    def __init__(self, cr):
        DistributedBattleAvatar.DistributedBattleAvatar.__init__(self, cr)
        self.island = None
        self.name = PLocalizer.NavyFortName
        self.level = 1
        self.meterHp = self.maxHp
        self.hpMeter = None
        self.meterMp = 0
        self.maxMojo = 0
        self.currentAttack = 0
        self.drawbridges = []
        self.smoke = None
        self.islandRequest = None
        self.islandDependedObjectsSetup = 0
        self.hpTextNodes = []
        self.hpTextIvals = []
        return

    def delete(self):
        DistributedBattleAvatar.DistributedBattleAvatar.delete(self)
        if self.smoke:
            self.smoke.destroy()
            self.smoke = None
        if self.hpMeter:
            self.hpMeter.destroy()
            self.hpMeter = None
        if self.islandRequest:
            self.cr.relatedObjectMgr.abortRequest(self.islandRequest)
        return

    def setIslandId(self, islandId):
        self.islandId = islandId

    def getNameText(self):
        return ''

    def setObjKey(self, objKey):
        self.objKey = objKey

    def loadModel(self):
        DistributedBattleAvatar.DistributedBattleAvatar.loadModel(self)

    def createGameFSM(self):
        self.gameFSM = BattleAvatarGameFSM.BattleAvatarGameFSM(self)

    def announceGenerate(self):
        self.notify.debug('announceGenerate')
        self.battleTubeRadius = 50.0
        self.battleTubeHeight = 100.0
        DistributedBattleAvatar.DistributedBattleAvatar.announceGenerate(self)
        self.cr.relatedObjectMgr.abortRequest(self.islandRequest)
        self.islandRequest = self.cr.relatedObjectMgr.requestObjects([self.islandId], eachCallback=self.__gotIsland)

    def disable(self):
        DistributedBattleAvatar.DistributedBattleAvatar.disable(self)
        self.island = None
        self.fortNode = None
        self.islandDependedObjectsSetup = 0
        return

    def __gotIsland(self, island):
        self.notify.debug('__gotIsland %s' % island)
        self.islandRequest = None
        if island.lastZoneLevel == 0:
            self.__setupIslandDependentObjects()
        else:
            self.cr.distributedDistrict.worldCreator.registerPostLoadCall(self.__setupIslandDependentObjects)
        return

    def __setupIslandDependentObjects(self):
        self.notify.debug('setupIslandDependentObjects')
        if not self.areDrawbridgesLoaded():
            self.cr.distributedDistrict.worldCreator.registerPostLoadCall(self.__setupIslandDependentObjects)
            self.notify.debug('no drawbridges yet, registering another post load call')
            return
        self.notify.debug('drawbridges are in render')
        self.setupCollisions()
        self.setupDrawbridges()
        self.islandDependedObjectsSetup = 1

    def readyToGo(self):
        return self.islandDependedObjectsSetup == 1 and self.isGenerated()

    def smoothPosition(self):
        DistributedReputationAvatar.smoothPosition(self)

    def setupCollisions(self):
        self.notify.debug('setupCollisions')
        self.island = base.cr.doId2do.get(self.islandId)
        if not self.island:
            self.notify.warning("Couldn't find island %d" % self.islandId)
            return
        self.fortNode = self.island.find('**/=uid=%s' % self.objKey)
        if self.fortNode == self.fortNode.notFound():
            self.notify.warning("Couldn't find fort uid %s" % self.objKey)
            return
        allColls = self.fortNode.findAllMatches('**/*collision*')
        if allColls.getNumPaths() == 0:
            allColls = self.fortNode.findAllMatches('**/*Col_*')
        oldBitMask = allColls.getCollideMask()
        newBitMask = oldBitMask | PiratesGlobals.TargetBitmask
        allColls.setCollideMask(newBitMask)
        for index in xrange(allColls.getNumPaths()):
            nodePath = allColls[index]
            nodePath.setTag('objType', str(PiratesGlobals.COLL_FORT))
            nodePath.setTag('fortId', str(self.doId))

    def getNameText(self):
        return None

    def gotHitByProjectile(self, hitObject, entry, skillId, ammoSkillId):
        fn = entry.getFromNodePath()
        fortId = fn.getNetTag('fortId')
        if fortId:
            fortId = int(fortId)
        if fortId == self.doId:
            return
        if fortId and fortId > 0:
            return
        self.sendHitByProjectile(skillId, ammoSkillId)

    def sendHitByProjectile(self, skillId, ammoSkillId):
        if self.hp > 0:
            self.sendUpdate('hitByProjectile', [skillId, ammoSkillId])

    def getLevel(self):
        return self.level

    def setupHpMeter(self):
        if self.hpMeter:
            return
        zAdj = 50
        self.smokeZAdj = zAdj
        self.fortPart = self.fortNode.find('**/top_interior_wall_collision')
        if self.fortPart.isEmpty():
            self.fortPart = self.fortNode.find('**/col_TopFloor1')
        if self.fortPart.isEmpty():
            self.fortPart = self.fortNode.find('**/pPlane4')
            zAdj = 150
            self.smokeZAdj = 100
        if self.fortPart.isEmpty():
            self.fortPart = self.fortNode.find('**/*tower*')
        if self.fortPart.isEmpty():
            self.fortPart = self.fortNode.find('**/*buttress*')
        if self.fortPart.isEmpty():
            self.fortPart = self.fortNode.find('**/*floor*')
        fortPartBounds = self.fortPart.getBounds()
        self.hpAnchor = NodePath('hpAnchor')
        self.hpAnchor.setPos(fortPartBounds.getApproxCenter())
        self.hpAnchor.setZ(self.hpAnchor.getZ() + zAdj)
        self.hpAnchor.reparentTo(self.fortNode)
        self.hpMeter = HpMeter.HpMeter(fadeOut=0, parent=self.hpAnchor, originAtMidPt=True)
        self.hpMeter.setScale(200)
        self.hpMeter.setBin('fixed', 130)
        self.hpMeter.setDepthWrite(False)
        myEffect = BillboardEffect.make(Vec3(0, 0, 1), True, False, 150, NodePath(), Point3(0, 0, 0))
        self.hpMeter.node().setEffect(myEffect)
        self.hpMeter.update(self.hp, self.maxHp)
        self.hideFortHpMeter()

    def setHp(self, hp, quietly=0):
        DistributedBattleAvatar.DistributedBattleAvatar.setHp(self, hp, quietly)
        if self.isGenerated():
            if not self.hpMeter:
                self.setupHpMeter()
            self.hpMeter.update(self.hp, self.maxHp)
            if self.drawbridges:
                self.updateDrawbridges()
            if self.hp < self.maxHp:
                self.updateSmoke()
            if self.hp <= 0:
                self.hpMeter.hide()

    def takeDamage(self, hpLost, pos, bonus=0):
        DistributedBattleAvatar.DistributedBattleAvatar.takeDamage(self, hpLost, pos, bonus)

    def died(self):
        if self.cr and self.cr.wantSpecialEffects != 0:
            shipDebrisEffect = ShipDebris.getEffect()
            if shipDebrisEffect and not self.hpAnchor.isEmpty():
                shipDebrisEffect.reparentTo(self.hpAnchor)
                shipDebrisEffect.setZ(shipDebrisEffect.getZ() - self.smokeZAdj)
                shipDebrisEffect.endPlaneZ = 0
                shipDebrisEffect.play()

    def hideFortHpMeter(self):
        if self.hpMeter:
            self.hpMeter.hide()

    def showFortHpMeter(self):
        if self.hpMeter:
            self.hpMeter.show()

    def getInventory(self):
        return None

    def setupDrawbridgeCollisions(self, dbName, drawbridge):
        curNodePath = drawbridge
        oldBitMask = curNodePath.getCollideMask()
        newBitMask = oldBitMask | PiratesGlobals.TargetBitmask
        newBitMask = newBitMask & ~PiratesGlobals.ShipCollideBitmask
        curNodePath.setCollideMask(newBitMask)
        curNodePath.setTag('objType', str(PiratesGlobals.COLL_FORT))
        curNodePath.setTag('fortId', str(self.doId))
        shipCollider = drawbridge.find('**/*shipcollide*;+s')
        if shipCollider.isEmpty():
            self.notify.warning('setupDrawbridgeCollisions could not find ship collider for %s' % dbName)
        tempStr = 'drawbridge_pier'
        lenTemp = len(tempStr)
        suffix = dbName[lenTemp:]
        otherParts = ('crane_island', 'crane1_island', 'drawbridge_fort', 'crane_fort',
                      'crane1_fort', 'drawbridge_fort')
        for otherPart in otherParts:
            nodeName = otherPart + suffix
            curNodePath = render.find('**/%s' % nodeName)
            if curNodePath.isEmpty():
                self.notify.warning("setupDrawbridgeCollisions() couldn't find nodepath %s" % nodeName)
            else:
                oldBitMask = curNodePath.getCollideMask()
                newBitMask = oldBitMask | PiratesGlobals.TargetBitmask
                curNodePath.setCollideMask(newBitMask)
                curNodePath.setTag('objType', str(PiratesGlobals.COLL_FORT))
                curNodePath.setTag('fortId', str(self.doId))

    def setupDrawbridges(self):
        if TreasureMapBlackPearlGlobals.DrawbridgeDict.has_key(self.objKey):
            dbTuple = TreasureMapBlackPearlGlobals.DrawbridgeDict[self.objKey]
            for dbName in dbTuple:
                drawbridge = render.find('**/%s' % dbName)
                if drawbridge.isEmpty():
                    self.notify.warning("couldn't find drawbridge %s" % dbName)
                else:
                    self.drawbridges.append(drawbridge)
                    self.setupDrawbridgeCollisions(dbName, drawbridge)

    def areDrawbridgesLoaded(self):
        retval = True
        if TreasureMapBlackPearlGlobals.DrawbridgeDict.has_key(self.objKey):
            dbTuple = TreasureMapBlackPearlGlobals.DrawbridgeDict[self.objKey]
            for dbName in dbTuple:
                drawbridge = render.find('**/%s' % dbName)
                if drawbridge.isEmpty():
                    retval = False

        return retval

    def updateDrawbridges(self):
        for drawbridge in self.drawbridges:
            if self.hp <= 0:
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    smokeEffect = SmokeExplosion.getEffect()
                    if smokeEffect:
                        smokeEffect.reparentTo(render)
                        smokeEffect.setPos(drawbridge, 0, 0, 0)
                        smokeEffect.spriteScale = 1.0
                        smokeEffect.play()
                posHprIval = LerpPosHprInterval(drawbridge, 1.0, Vec3(drawbridge.getX(), drawbridge.getY(), drawbridge.getZ() - 130.0), Vec3(drawbridge.getH(), drawbridge.getP() - 360.0, drawbridge.getR() + 15))
                posHprIval.start()

    def debugMissing(self):
        wi = render.find('**/whole_island')
        allChildren = wi.getChildren()
        for index in xrange(allChildren.getNumPaths()):
            np = allChildren.getPath(index)
            if not np.isHidden():
                print np
                np.hide()
                break

    def setDrawbridgesR(self, r):
        for drawbridge in self.drawbridges:
            drawbridge.setR(r)

    def setDrawbridgesLerpR(self, r):
        angle = 0
        if r == 1:
            angle = -70
        for drawbridge in self.drawbridges:
            if drawbridge.getR() == angle:
                return
            ival = LerpHprInterval(drawbridge, 4.0, Vec3(drawbridge.getH(), drawbridge.getP(), angle))
            ival.start()

    def hideDrawbridges(self):
        for drawbridge in self.drawbridges:
            drawbridge.hide()

    def updateSmoke(self):
        if self.hp < self.maxHp:
            self.startSmoke()
            if self.smoke:
                density = 1 - float(self.hp) / self.maxHp
                self.smoke.setDensity(density)

    def startSmoke(self):
        if not self.smoke:
            self.smoke = BlackSmoke.getEffect()
            if self.smoke:
                self.smoke.reparentTo(self.hpAnchor)
                self.smoke.setZ(-self.smokeZAdj)
                self.smoke.startLoop()

    def setupRadarGui(self):
        self.hpAnchor.setTag('avId', str(self.doId))
        self.setTeam(PiratesGlobals.NAVY_TEAM)

    def initializeBattleCollisions(self):
        pass

    def setLevel(self, level):
        self.level = level

    def printExpText(self, totalExp, colorSetting, basicPenalty, crewBonus, doubleXPBonus, holidayBonus, potionBonus):
        taskMgr.doMethodLater(0.5, self.showHpText, self.taskName('printExp'), [
         totalExp, 4, 6.0, 1.0, basicPenalty, crewBonus, doubleXPBonus, holidayBonus, potionBonus])

    def showHpText(self, number, bonus=0, duration=2.0, scale=1.0, basicPenalty=0, crewBonus=0, doubleXPBonus=0, holidayBonus=0, potionBonus=0):
        if self.isEmpty():
            return
        distance = camera.getDistance(self)
        scale *= max(1.0, distance / 50.0)
        height = self.hpAnchor.getZ() + 25.0
        startPos = Point3(0, 0, height / 4)
        destPos = Point3(0, 0, height / 2)
        newEffect = None

        def cleanup():
            if newEffect in self.textEffects:
                self.textEffects.remove(newEffect)

        mods = {}
        if basicPenalty > 0:
            mods[TextEffect.MOD_BASICPENALTY] = basicPenalty
        if crewBonus > 0:
            mods[TextEffect.MOD_CREWBONUS] = crewBonus
        if doubleXPBonus > 0:
            mods[TextEffect.MOD_2XPBONUS] = doubleXPBonus
        if holidayBonus > 0:
            mods[TextEffect.MOD_HOLIDAYBONUS] = holidayBonus
        newEffect = TextEffect.genTextEffect(self.hpAnchor, self.HpTextGenerator, number, bonus, self.isNpc, cleanup, startPos, destPos, scale, modifiers=mods)
        if newEffect:
            self.textEffects.append(newEffect)
        return