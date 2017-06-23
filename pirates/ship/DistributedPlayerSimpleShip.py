from pandac.PandaModules import Vec4, VBase4
import direct.interval.IntervalGlobal as IG
from direct.fsm.StatePush import StateVar
from direct.task import Task
from pirates.ship.DistributedSimpleShip import MinimapShip
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.ship.ShipRepairSpotMgr import ShipRepairSpotMgr
from pirates.piratesbase import PLocalizer
from pirates.pvp import PVPGlobals
from pirates.ship.DistributedSimpleShip import DistributedSimpleShip
from pirates.ship import ShipGlobals
from pirates.ship import ShipUpgradeGlobals
from pirates.battle import EnemyGlobals
from pirates.ship import HighSeasGlobals
from pirates.piratesgui import MessageGlobals
from pirates.piratesgui import ShipFrameBoard
import random

class DistributedPlayerSimpleShip(DistributedSimpleShip):
    RepairSpotFadeAfter = 2.0
    RepairSpotFadeDur = 3.0

    def __init__(self, cr):
        DistributedSimpleShip.__init__(self, cr)
        self._respawnLocation = None
        self.checkAnchor = None
        self.lastAttacked = None
        self.threatLevel = 0
        self.openPort = 0
        self.allowCrewState = True
        self.allowFriendState = True
        self.allowGuildState = False
        self.allowPublicState = False
        self._repairSpotMgr = ShipRepairSpotMgr(self.cr)
        self._team = PiratesGlobals.PLAYER_TEAM
        self.badInitTeam = None
        self.prevLocStack = None
        self.customHull = 0
        self.customRigging = 0
        self.customSailPattern = 0
        self.customSailLogo = 0
        self.customProw = 0
        self.customCannon = 0
        self.boardingPanel = None
        return

    def generate(self):
        DistributedSimpleShip.generate(self)
        self._repairSpotWoodPile = None
        self._repairSpotWoodPiles = {}
        self._repairSpotHole = None
        self._repairSpotHoleFixed = None
        self._repairSpotHoles = {}
        self._repairSpotIvals = {}
        self._wheelInUse = StateVar(False)
        return

    def announceGenerate(self):
        self._respawnLocation = None
        self._respawnResponseDelayedCall = None
        DistributedSimpleShip.announceGenerate(self)
        self._repairSpotMgr.setShipId(self.doId)
        if self.badInitTeam != None:
            self._verifyTeam(self.badInitTeam)
        return

    def disable(self):
        if self.boardingPanel:
            self.boardingPanel.destroy()
            self.boardingPanel = None
        self._wheelInUse.destroy()
        if self._respawnResponseDelayedCall:
            self._respawnResponseDelayedCall.destroy()
            self._respawnResponseDelayedCall = None
        if self.checkAnchor:
            self.checkAnchor.remove()
            self.checkAnchor = None
        self._repairSpotMgr.destroy()
        for ival in self._repairSpotIvals.itervalues():
            ival.pause()

        self._repairSpotIvals = None
        self.prevLocStack = None
        self.prevLocStack = None
        DistributedSimpleShip.disable(self)
        return

    def calculateLook(self):
        team = self.getTeam()
        if team == PiratesGlobals.PLAYER_TEAM:
            if self.getSiegeTeam() == 1:
                self.style = ShipGlobals.Styles.French
            elif self.getSiegeTeam() == 2:
                self.style = ShipGlobals.Styles.Spanish

    def loadStats(self):
        DistributedSimpleShip.loadStats(self)
        speedUpgrade = 1.0
        turningUpgrade = 1.0
        if self.customHull:
            speedUpgrade = ShipUpgradeGlobals.HULL_TYPES[self.customHull]['Speed']
            turningUpgrade = ShipUpgradeGlobals.HULL_TYPES[self.customHull]['Turning']
            self.setSpeedMods(baseMod=None, speedUpgradeMod=speedUpgrade, turnUpgradeMod=turningUpgrade)
        return

    def setShipUpfitList(self, dataList):
        counter = 0
        while dataList:
            newData = dataList[0]
            dataList = dataList[1:]
            if counter == 0:
                self.customHull = newData
            elif counter == 1:
                self.customRigging = newData
            elif counter == 2:
                self.customSailPattern = newData
            elif counter == 3:
                self.customSailLogo = newData
            counter += 1

        self.setupLocalStats()
        messenger.send('ShipChanged-%s' % self.doId)

    def getSkillBoost(self, skillId):
        if self.customRigging:
            riggingInfo = ShipUpgradeGlobals.RIGGING_TYPES.get(self.customRigging)
            boostLevel = ShipUpgradeGlobals.RIGGING_TYPES.get(self.customRigging, {}).get('SkillBoosts', {}).get(skillId, 0)
            return boostLevel
        return 0

    def buildShip(self):
        hullMaterial = None
        sailMaterial = None
        sailPattern = None
        invertLogo = False
        logo = ShipGlobals.Logos.Undefined
        if self.customHull:
            hullType = ShipUpgradeGlobals.HULL_TYPES.get(self.customHull)
            if hullType:
                hullMaterial = hullType['StyleIndex']
        if self.customRigging:
            riggingType = ShipUpgradeGlobals.RIGGING_TYPES.get(self.customRigging)
            if riggingType:
                sailMaterial = riggingType['StyleIndex']
        if self.customSailPattern:
            patternType = ShipUpgradeGlobals.SAILCOLOR_TYPES.get(self.customSailPattern)
            if patternType:
                sailPattern = patternType['StyleIndex']
        logo = self.getLogo()
        if self.customSailLogo:
            logoType = ShipUpgradeGlobals.LOGO_TYPES.get(self.customSailLogo)
            if logoType:
                logo = logoType['StyleIndex']
                invertLogo = logoType['Invert']
        team = self.getTeam()
        if team == PiratesGlobals.PLAYER_TEAM:
            if self.getSiegeTeam() == 1:
                sailPattern = ShipGlobals.Styles.French
            elif self.getSiegeTeam() == 2:
                sailPattern = ShipGlobals.Styles.Spanish
        self.model = base.shipFactory.getShip(self.shipClass, self.getStyle(), detailLevel=base.options.terrain_detail_level, hullMaterial=hullMaterial, sailMaterial=sailMaterial, sailPattern=sailPattern, logo=logo, invertLogo=invertLogo)
        return

    def getNPCship(self):
        return False

    def setShipClass(self, shipClass):
        DistributedSimpleShip.setShipClass(self, shipClass)
        self._repairSpotMgr.updateShipClass(self.shipClass)

    def setHealthState(self, health):
        DistributedSimpleShip.setHealthState(self, health)
        self._repairSpotMgr.updateHealth(self.healthState)

    def setMastStates(self, mainMast1, mainMast2, mainMast3, aftMast, foreMast):
        DistributedSimpleShip.setMastStates(self, mainMast1, mainMast2, mainMast3, aftMast, foreMast)
        self._repairSpotMgr.updateSpeed(100.0 * self.Sp / self.maxSp)

    def setArmorStates(self, rear, left, right):
        DistributedSimpleShip.setArmorStates(self, rear, left, right)
        self._repairSpotMgr.updateArmor((rear + left + right) / 3.0)

    def setWillFullyRepairShip(self, willFullyRepairShip):
        self._repairSpotMgr.updateWillBeFullHealth(willFullyRepairShip)

    def setupLocalStats(self):
        DistributedSimpleShip.setupLocalStats(self)
        if self.customHull:
            tempArmorState = [
             100.0 * self.armor[0] / self.maxArmor[0], 100.0 * self.armor[1] / self.maxArmor[1], 100.0 * self.armor[2] / self.maxArmor[2]]
            tempHealthState = 100.0 * self.Hp / self.maxHp
            tempMastState = []
            for mastIndex in range(len(self.maxMastHealth)):
                if self.maxMastHealth[mastIndex] > 0.0:
                    tempMastState.append(100.0 * self.mastHealth[mastIndex] / self.maxMastHealth[mastIndex])
                else:
                    tempMastState.append(0.0)

            armorUpgrade = ShipUpgradeGlobals.HULL_TYPES[self.customHull]['Armor']
            self.maxHp *= armorUpgrade
            self.Hp *= armorUpgrade
            newArmor = []
            for entry in self.maxArmor:
                newArmor.append(entry * armorUpgrade)

            self.maxArmor = newArmor
            newMastHealth = []
            for entry in self.maxMastHealth:
                newMastHealth.append(entry * armorUpgrade)

            self.maxMastHealth = newMastHealth
            self.maxSp *= armorUpgrade
            cargoUpgrade = ShipUpgradeGlobals.HULL_TYPES[self.customHull]['Cargo']
            self.setMaxCargo(int(cargoUpgrade * self.maxCargo))

    def setOpenPort(self, portId):
        oldPort = self.openPort
        self.openPort = portId
        if localAvatar.ship and localAvatar.ship.getDoId() == self.getDoId():
            messenger.send('LocalAvatar_Ship_OpenPort_Update', [portId, oldPort])

    def getOpenPort(self):
        return self.openPort

    def isAtOpenPort(self):
        portDoId = localAvatar.getPort()
        portObj = base.cr.doId2do.get(portDoId, None)
        if self.threatLevel < EnemyGlobals.SHIP_THREAT_NAVY_HUNTERS:
            return 1
        elif portObj and portObj.uniqueId == EnemyGlobals.OPEN_PORT_DICT.get(self.openPort):
            return 1
        else:
            return 0
        return

    def setThreatLevel(self, threatLevel):
        if threatLevel != self.threatLevel:
            self.threatLevel = threatLevel
            self.updateNametag()
            if localAvatar.ship and localAvatar.ship.getDoId() == self.getDoId():
                messenger.send('LocalAvatar_Ship_ThreatLevel_Update', [threatLevel])
            self.checkAbleDropAnchor()

    def getThreatLevel(self):
        if base.config.GetBool('want-ship-threat', 1):
            return self.threatLevel
        else:
            return EnemyGlobals.SHIP_THREAT_ATTACK_BACK

    def getOpenPort(self):
        return self.openPort

    def sunkAShipFanfare(self, shipToAttackDoId):
        if localAvatar.ship and localAvatar.ship == self:
            if localAvatar.ship.getSiegeTeam():
                return
            attackMessage = HighSeasGlobals.getShipSunkMessage()
            if attackMessage:
                base.localAvatar.guiMgr.queueInstructionMessage(attackMessage[0], attackMessage[1], None, 1.0, messageCategory=MessageGlobals.MSG_CAT_SUNK_SHIP)
        return

    @report(types=['args'], dConfigParam='shipdeploy')
    def setSiegeTeam(self, team):
        different = team != self.getSiegeTeam()
        DistributedSimpleShip.setSiegeTeam(self, team)
        if different:
            self._doSiegeAndPVPTeamColors()
            self._repairSpotMgr.updateSiegeTeam(team)
            minimapObj = self.getMinimapObject()
            if minimapObj:
                minimapObj.setSiegeTeam(team)

    def _doSiegeAndPVPTeamColors(self):
        if self.getPVPTeam():
            self._doPVPTeamColors()
        elif self.getSiegeTeam():
            pass

    def _doPVPTeamColors(self):
        pass

    def getWheelInUseSV(self):
        return self._wheelInUse

    def setWheelInUse(self, wheelInUse):
        DistributedSimpleShip.setWheelInUse(self, wheelInUse)
        self._wheelInUse.set(wheelInUse)

    def canTakeWheel(self, wheel, av):
        available = True
        if self.queryGameState() in ('Pinned', 'Sinking', 'Sunk', 'OtherShipBoarded'):
            base.localAvatar.guiMgr.createWarning(PLocalizer.ShipPinnedWarning, PiratesGuiGlobals.TextFG6)
            available = False
        elif self.isFishing and base.localAvatar.getDoId() != self.ownerId:
            base.localAvatar.guiMgr.createWarning(PLocalizer.OnlyCaptainCanUseWarning, PiratesGuiGlobals.TextFG6)
            available = False
        elif wheel.getUserId() and base.localAvatar.getDoId() != self.ownerId:
            base.localAvatar.guiMgr.createWarning(PLocalizer.AlreadyInUseWarning, PiratesGuiGlobals.TextFG6)
            available = False
        return available

    def setRespawnLocation(self, parentId, zoneId):
        self._respawnLocation = (
         parentId, zoneId)

    def setLocation(self, parentId, zoneId):
        DistributedSimpleShip.setLocation(self, parentId, zoneId)
        if self._respawnLocation is not None and self._respawnLocation == (parentId, zoneId):
            self.updateCurrentZone()
            self._respawnLocation = None
            if not self._respawnResponseDelayedCall:
                self._respawnResponseDelayedCall = FrameDelayedCall('PlayerShip-respawnLocation-gridInterestComplete', Functor(base.cr.setAllInterestsCompleteCallback, self._sendRespawnLocationResponse))
        return

    def _sendRespawnLocationResponse(self):
        self.sendUpdate('clientReachedRespawnLocation')
        self._respawnResponseDelayedCall = None
        return

    def recoverFromSunk(self):
        self.lastAttacked = None
        DistributedSimpleShip.recoverFromSunk(self)
        return

    def attacked(self):
        self.lastAttacked = globalClock.getFrameTime()
        if self.getSiegeTeam() and not self.checkAnchor:
            self.checkAbleDropAnchor()

    def attackTimerRemaining(self):
        timer = 0
        if self.lastAttacked:
            timer = int(30 - (globalClock.getFrameTime() - self.lastAttacked))
        return timer

    def __recheckAbleDropAnchor(self, task):
        self.checkAnchor = None
        self.checkAbleDropAnchor()
        return

    def checkAbleDropAnchor(self):
        from pirates.piratesgui import PiratesGuiGlobals
        if localAvatar.doId == self.steeringAvId:
            if self.shipStatusDisplay:
                if localAvatar.getPort():
                    remaining = self.attackTimerRemaining()
                    if self.getSiegeTeam() and remaining > 0:
                        self.shipStatusDisplay.disableAnchorButton()
                        localAvatar.guiMgr.createWarning(PLocalizer.CannotDockYet % remaining, PiratesGuiGlobals.TextFG6)
                        self.checkAnchor = taskMgr.doMethodLater(remaining, self.__recheckAbleDropAnchor, 'checkAnchor')
                    elif self.isAtOpenPort():
                        self.shipStatusDisplay.enableAnchorButton()
                    else:
                        self.shipStatusDisplay.disableAnchorButton()
                        self.shipStatusDisplay.tellWrongPort()
                else:
                    self.shipStatusDisplay.disableAnchorButton()
                    self.shipStatusDisplay.hideWrongPort()

    def _addRepairSpotModels(self):
        if not self._repairSpotWoodPile:
            self._repairSpotWoodPile = loader.loadModel('models/props/repair_spot_wood')
            collFloors = self._repairSpotWoodPile.find('**/collision_floor')
            if not collFloors.isEmpty():
                collideMask = collFloors.getCollideMask()
                collideMask ^= PiratesGlobals.FloorBitmask
                collideMask |= PiratesGlobals.ShipFloorBitmask
                collFloors.setCollideMask(collideMask)
        for locIndex in PVPGlobals.ShipClass2repairLocators[self.modelClass].getValue():
            locName = PVPGlobals.RepairSpotLocatorNames[locIndex]
            self._repairSpotWoodPiles[locName] = self.getModelRoot().attachNewNode('repairSpotWoodPile-%s' % locName)
            self._repairSpotWoodPile.instanceTo(self._repairSpotWoodPiles[locName])
            locator = self.getLocator(locName)
            self._repairSpotWoodPiles[locName].setPosHpr(locator.getPos(), locator.getHpr())

    def _removeRepairSpotModels(self):
        for woodPile in self._repairSpotWoodPiles.itervalues():
            woodPile.detachNode()

        self._repairSpotWoodPiles = {}

    def _placeRepairSpotModel(self, locIndex, model):
        locName = PVPGlobals.RepairSpotLocatorNames[locIndex]
        parentNode = self.getModelRoot().attachNewNode('repairSpotHole-%s' % locName)
        parentNode.setTransparency(1, 100)
        model.instanceTo(parentNode)
        locator = self.getLocator(locName)
        parentNode.setPosHpr(locator.getPos(), locator.getHpr())
        self._repairSpotHoles[locIndex] = parentNode

    def _removeRepairSpotModel(self, locIndex):
        if locIndex in self._repairSpotHoles:
            self._repairSpotHoles[locIndex].detachNode()
            del self._repairSpotHoles[locIndex]

    def _fadeOutRepairSpotModel(self, locIndex):
        if locIndex in self._repairSpotIvals:
            self._repairSpotIvals[locIndex].pause()
        self._repairSpotHoles[locIndex].setTransparency(1, 100)
        ival = IG.Sequence(IG.Wait(DistributedPlayerSimpleShip.RepairSpotFadeAfter), IG.LerpColorScaleInterval(self._repairSpotHoles[locIndex], DistributedPlayerSimpleShip.RepairSpotFadeDur, Vec4(1.0, 1.0, 1.0, 0.0), blendType='easeInOut'))
        ival.start()
        self._repairSpotIvals[locIndex] = ival

    def _addRepairSpotHoles(self):
        if not self._repairSpotHole:
            repairSpotHoleModels = loader.loadModel('models/props/repair_spot_hole')
            self._repairSpotHole = repairSpotHoleModels.find('**/floor_hole')
            self._repairSpotHoleFixed = repairSpotHoleModels.find('**/floor_hole_fixed')
        for locIndex in PVPGlobals.ShipClass2repairLocators[self.modelClass].getValue():
            self._removeRepairSpotModel(locIndex)
            self._placeRepairSpotModel(locIndex, self._repairSpotHole)

    def _removeRepairSpotHoles(self):
        for locIndex in PVPGlobals.ShipClass2repairLocators[self.modelClass].getValue():
            self._removeRepairSpotModel(locIndex)
            if self._repairSpotHoleFixed:
                self._placeRepairSpotModel(locIndex, self._repairSpotHoleFixed)
                self._fadeOutRepairSpotModel(locIndex)
                self._repairSpotIvals[locIndex] = IG.Sequence(self._repairSpotIvals[locIndex], IG.Func(self._removeRepairSpotModel, locIndex))

    def b_setAllowCrewState(self, state):
        self.d_setAllowCrewState(state)
        self.setAllowCrewState(state)

    def b_setAllowFriendState(self, state):
        self.d_setAllowFriendState(state)
        self.setAllowFriendState(state)

    def b_setAllowGuildState(self, state):
        self.d_setAllowGuildState(state)
        self.setAllowGuildState(state)

    def b_setAllowPublicState(self, state):
        self.d_setAllowPublicState(state)
        self.setAllowPublicState(state)

    def d_setAllowCrewState(self, state):
        self.sendUpdate('setAllowCrewState', [state])

    def d_setAllowFriendState(self, state):
        self.sendUpdate('setAllowFriendState', [state])

    def d_setAllowGuildState(self, state):
        self.sendUpdate('setAllowGuildState', [state])

    def d_setAllowPublicState(self, state):
        self.sendUpdate('setAllowPublicState', [state])

    def setAllowCrewState(self, state):
        self.allowCrewState = state
        if self.shipStatusDisplay:
            self.shipStatusDisplay.setAllowCrew(state)

    def setAllowFriendState(self, state):
        self.allowFriendState = state
        if self.shipStatusDisplay:
            self.shipStatusDisplay.setAllowFriends(state)

    def setAllowGuildState(self, state):
        self.allowGuildState = state
        if self.shipStatusDisplay:
            self.shipStatusDisplay.setAllowGuild(state)

    def setAllowPublicState(self, state):
        self.allowPublicState = state
        if self.shipStatusDisplay:
            self.shipStatusDisplay.setAllowPublic(state)

    def getAllowCrewState(self):
        return self.allowCrewState

    def getAllowFriendState(self):
        return self.allowFriendState

    def getAllowGuildState(self):
        return self.allowGuildState

    def getAllowPublicState(self):
        return self.allowPublicState

    def hasSpace(self, avId=0, bandMgrId=0, bandId=0, guildId=0):
        if avId == self.ownerId:
            return True
        if self.isInCrew(avId):
            return True
        if self.isInCrew(self.ownerId) and len(self.crew) >= self.maxCrew:
            return False
        if len(self.crew) >= self.maxCrew - 1:
            return False
        return True

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='shipboard')
    def confirmSameCrewTeleport(self, toFrom, incomingAvId=0, bandMgrId=0, bandId=0, guildId=0):
        if toFrom == 'from':
            return True
        else:
            if not self.isGenerated():
                self.notify.warning('confirmSameCrewTeleport(%s)' % localAvatar.getShipString())
                return False
            if incomingAvId == self.ownerId:
                return True
            if bandMgrId and bandId and self.getAllowCrewState() and (bandMgrId, bandId) == self.getBandId():
                return True
            if localAvatar.doId == self.ownerId and self.getAllowFriendState() and self.cr.identifyFriend(incomingAvId):
                return True
            if guildId and self.getAllowGuildState() and guildId == self.getGuildId():
                return True
            if self.getAllowPublicState():
                return True
            return False

    def localPirateArrived(self, av):
        DistributedSimpleShip.localPirateArrived(self, av)
        self.enableOnDeckInteractions()
        mapObj = self.getMinimapObject()
        if mapObj:
            mapObj.setAsLocalAvShip(av.getCrewShipId() == self.doId)

    def showBoardingChoice(self, shipToBoard):
        if not self.boardingPanel:
            shipInfo = shipToBoard.getShipInfo()
            from direct.distributed.ClockDelta import globalClockDelta
            dt = globalClockDelta.localElapsedTime(shipToBoard.sinkTimestamp)
            time = shipToBoard.sinkTime - dt
            self.boardingPanel = ShipFrameBoard.ShipFrameBoard(shipName=shipInfo[1], shipClass=shipInfo[2], mastInfo=shipInfo[3], parent=base.a2dTopCenter, pos=(-0.45, 0, -0.5), time=time, command=self.__handleBoardingChoice)
            self._boardingTimer = taskMgr.doMethodLater(time, self._boardingChoiceTimeout, 'boardingTimer')
        self.boardingPanel.show()

    def _boardingChoiceTimeout(self, task):
        self.removeBoardingChoice()

    def hideBoardingChoice(self):
        if self.boardingPanel:
            self.boardingPanel.hide()

    def removeBoardingChoice(self):
        if self.boardingPanel:
            self.boardingPanel.destroy()
            self.boardingPanel = None
        if self._boardingTimer:
            self._boardingTimer.remove()
            self._boardingTimer = None
        return

    def __handleBoardingChoice(self, wishToBoard):
        self.removeBoardingChoice()
        self.d_setBoardingChoice(int(wishToBoard))

    def d_setBoardingChoice(self, choice):
        self.sendUpdate('setBoardingChoice', [choice])

    def getMinimapObject(self):
        if not self.minimapObj and not self.isDisabled():
            self.minimapObj = MinimapPlayerShip(self)
        return self.minimapObj

    def setTeam(self, team):
        if not self._verifyTeam(team):
            return
        DistributedSimpleShip.setTeam(self, team)

    def _verifyTeam(self, team):
        if team == PiratesGlobals.INVALID_TEAM:
            doId = '<no doId>'
            if hasattr(self, 'doId'):
                doId = self.doId
            else:
                self.badInitTeam = team
            base.cr.centralLogger.writeClientEvent('bad ship team: %s' % doId)
            self.notify.warning('bad ship team: %s' % doId)
            return False
        return True

    def d_setLocation(self, parentId, zoneId):
        theStack = StackTrace(start=1)
        if self.prevLocStack and len(theStack.trace) == len(self.prevLocStack.trace) and map(lambda x: x[1], theStack.trace) == map(lambda x: x[1], self.prevLocStack.trace):
            base.cr.centralLogger.writeClientEvent('bad ship team: %s setLoc' % self.doId)
        else:
            base.cr.centralLogger.writeClientEvent('bad ship team: %s' % self.doId + theStack.compact()[1:len(theStack.compact())])
            self.prevLocStack = theStack
        DistributedSimpleShip.d_setLocation(self, parentId, zoneId)


class MinimapPlayerShip(MinimapShip):
    DEFAULT_COLOR = VBase4(0.1, 0.5, 1.0, 0.7)

    def updateOnMap(self, map):
        MinimapShip.updateOnMap(self, map)
        if self.isLocalAvShip:
            map.updateRadarTransform(self.worldNode)

    @report(types=['args'], dConfigParam='shipdeploy')
    def setSiegeTeam(self, team):
        self.siegeTeam = team
        self.refreshIconColor()