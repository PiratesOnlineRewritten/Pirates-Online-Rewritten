from pirates.pvp.PVPGameBase import PVPGameBase
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.interact import InteractiveBase
from pirates.ship import DistributedSimpleShip
from pirates.pvp.MiniScoreItemGui import MiniScoreItemGui
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class PVPGameCTL(PVPGameBase):
    notify = directNotify.newCategory('PVPGameCTL')

    def __init__(self, cr):
        PVPGameBase.__init__(self, cr)
        self.dropDisabled = 0
        self.teamScore = 0
        self.carryingScore = 0
        self.otherTeamScore = 0
        self.shipsNearBase = {}
        self.maxTeamScore = 0
        self.prevTeamScore = None
        self.depositSound = loadSfx(SoundGlobals.SFX_PVP_TREASURE_DEPOSIT)
        self.maxCarry = None
        self.pendingInstanceRequest = None
        return

    def generate(self):
        PVPGameBase.generate(self)
        self.accept(PiratesGlobals.EVENT_SPHERE_PORT + PiratesGlobals.SPHERE_ENTER_SUFFIX, self.handleEnterPort)
        self.accept(PiratesGlobals.EVENT_SPHERE_PORT + PiratesGlobals.SPHERE_EXIT_SUFFIX, self.handleExitPort)
        self.accept('carryingTreasure', self.startTreasureCarry)
        self.accept('notCarryingTreasure', self.stopTreasureCarry)

    def announceGenerate(self):
        PVPGameBase.announceGenerate(self)
        self.pendingInstanceRequest = base.cr.relatedObjectMgr.requestObjects([self.instanceId], eachCallback=self.instanceGenerated)

    def instanceGenerated(self, instanceObj):
        self.instance = instanceObj

    def disable(self):
        PVPGameBase.disable(self)
        if self.pendingInstanceRequest:
            base.cr.relatedObjectMgr.abortRequest(self.pendingInstanceRequest)
            self.pendingInstanceRequest = None
        base.localAvatar.guiMgr.hidePVPUI()
        return

    def delete(self):
        self.ignoreAll()
        PVPGameBase.delete(self)

    def handleDeposit(self, eventType, avId, bankId):
        if localAvatar.getDoId() == avId:
            if eventType == 'Team ' + str(localAvatar.getTeam()) and localAvatar.lootCarried > 0:
                base.playSfx(self.depositSound)
                self.sendUpdate('treasureDeposited', [bankId])
                if localAvatar.gameFSM.getCurrentOrNextState() != localAvatar.gameFSM.defaultState:
                    localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)

    def handleEnterPort(self, depositType, shipId):
        self.notify.debug('<HCLAY> ------- handleEnterPort')
        currVal = self.shipsNearBase.get(shipId)
        self.sendUpdate('portEntered', [depositType, shipId])
        self.shipsNearBase[shipId] = depositType

    def handleExitPort(self, depositType, shipId):
        self.notify.debug('<HCLAY> ------- handleEnterPort')
        currVal = self.shipsNearBase.get(shipId)
        self.sendUpdate('portExited', [depositType, shipId])
        if self.shipsNearBase.get(shipId):
            del self.shipsNearBase[shipId]

    def setMaxCarry(self, maxCarry):
        self.maxCarry = maxCarry

    def setMaxTeamScore(self, maxScore):
        self.maxTeamScore = maxScore

    def updateShipProximityText(self, ship):
        if localAvatar.lootCarried > 0:
            ship.proximityText = PLocalizer.ShipDepositInstructions
        else:
            ship.b_setIsBoardable(ship.isBoardable)

    def handleShipUse(self, ship):
        amt = localAvatar.lootCarried
        self.notify.debug('<HCLAY> ----- loot carried %s' % amt)
        if amt > 0:
            self.sendUpdate('shipDeposit', [ship.getDoId()])
            if localAvatar.gameFSM.getCurrentOrNextState() != localAvatar.gameFSM.defaultState:
                localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
            return True
        return False

    def shipDeposited(self, shipDoId):
        self.notify.debug('<HCLAY> ------- deposited stuff on ship')
        ship = self.cr.doId2do.get(shipDoId)
        if ship:
            ship.b_setIsBoardable(ship.isBoardable)
            ship.refreshProximityText()

    def startTreasureCarry(self):
        print 'start treasure carry'
        if localAvatar.gameFSM.getCurrentOrNextState() != 'LandTreasureRoam' and localAvatar.gameFSM.getCurrentOrNextState() != 'WaterTreasureRoam':
            return
        self.dropDisabled = 0
        self.acceptOnce(InteractiveBase.USE_KEY_EVENT, self.dropTreasure)
        self.ignore('exitProximityOfInteractive')
        self.accept('enterProximityOfInteractive', self.temporarilyDisableDrop)

    def stopTreasureCarry(self):
        print 'stop treasure carry'
        self.ignore(InteractiveBase.USE_KEY_EVENT)
        if localAvatar.gameFSM.getCurrentOrNextState() != 'WaterTreasureRoam' and localAvatar.gameFSM.getCurrentOrNextState() != 'LandTreasureRoam' and self.dropDisabled == 0:
            print 'leaving state, drop treasure'
            self.requestDropTreasure()

    def temporarilyDisableDrop(self):
        print 'disableDrop'
        self.dropDisabled = 1
        self.ignore(InteractiveBase.USE_KEY_EVENT)
        self.accept('exitProximityOfInteractive', self.startTreasureCarry)

    def dropTreasure(self):
        if localAvatar.gameFSM.getCurrentOrNextState() != localAvatar.gameFSM.defaultState:
            localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)

    def requestDropTreasure(self):
        self.sendUpdate('requestDropTreasure')

    def updateTreasureProximityText(self, treasure):
        baseType = self.shipsNearBase.get(treasure.parentId)
        if baseType and baseType == 'Team ' + str(localAvatar.getTeam()):
            treasure.proximityText = PLocalizer.ShipTransferInstructions
        elif treasure.zoneId == PiratesGlobals.ShipZoneOnDeck:
            treasure.proximityText = PLocalizer.PirateerDeckTreasure
        else:
            treasure.initInteractOpts()

    def setShipsNearBase(self, shipIds, baseTeams):
        self.shipsNearBase = {}
        for currIdx in range(len(shipIds)):
            self.shipsNearBase[shipIds[currIdx]] = baseTeams[currIdx]

    def handleUseKey(self, interactiveObj):
        if localAvatar.lootCarried > 0 and interactiveObj.isExclusiveInteraction():
            print 'dropping treasure now...'
            self.requestDropTreasure()
        if isinstance(interactiveObj, DistributedSimpleShip.DistributedSimpleShip):
            self.handleShipUse(interactiveObj)

    def complete(self):
        PVPGameBase.complete(self)
        self.prevTeamScore = None
        return

    def getScoreList(self):
        return self.scoreList

    def setScoreList(self, teams, scores):
        self.scoreList = []
        for currIdx in range(len(teams)):
            if teams[currIdx] > 1000 and teams[currIdx] != localAvatar.getDoId():
                continue
            self.scoreList.append({'Team': teams[currIdx],'Score': scores[currIdx]})

        self.scoreList.sort(self.sortScores)
        print 'got new score list %s' % self.scoreList
        messenger.send(self.getItemChangeMsg())

    def sortScores(self, item1, item2):
        team1 = item1.get('Team')
        team2 = item2.get('Team')
        if team1 == localAvatar.getDoId():
            return 1000
        elif team1 == localAvatar.getTeam():
            return -1000
        else:
            return team1 - team2

    def createNewItem(self, item, parent, itemType=None, columnWidths=[], color=None):
        itemColorScale = None
        blink = False
        team = item.get('Team')
        score = item.get('Score')
        if team == localAvatar.getTeam():
            if self.prevTeamScore != None and score < self.prevTeamScore:
                blink = True
            self.prevTeamScore = score
        return MiniScoreItemGui(item, parent, self.instance, itemColorScale, self.instance.gameRules, blink)

    def getScoreText(self, scoreValue):
        team = scoreValue.get('Team')
        score = scoreValue.get('Score')
        if team == localAvatar.getTeam():
            maxTeamScore = str(self.maxTeamScore)
            return PLocalizer.PVPYourTeam + str(score) + '/' + str(maxTeamScore) + PLocalizer.PVPGoldAbbrev
        elif team == localAvatar.getDoId():
            maxCarry = str(self.maxCarry)
            return '\n' + PLocalizer.PVPYouCarry + str(score) + '/' + maxCarry + PLocalizer.PVPGoldAbbrev
        else:
            maxTeamScore = str(self.maxTeamScore)
            return PLocalizer.PVPOtherTeam + str(score) + '/' + str(maxTeamScore) + PLocalizer.PVPGoldAbbrev