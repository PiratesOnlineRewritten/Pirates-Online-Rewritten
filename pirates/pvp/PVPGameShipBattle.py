from pirates.pvp.PVPGameBase import PVPGameBase
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.interact import InteractiveBase
from pirates.pvp.MiniScoreItemGui import MiniScoreItemGui
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class PVPGameShipBattle(PVPGameBase):
    notify = directNotify.newCategory('PVPGameShipBattle')

    def __init__(self, cr):
        PVPGameBase.__init__(self, cr)
        self.teamScore = 0
        self.carryingScore = 0
        self.otherTeamScore = 0
        self.shipsNearBase = {}
        self.maxTeamScore = 0
        self.prevTeamScore = None
        self.depositSound = loadSfx(SoundGlobals.SFX_PVP_TREASURE_DEPOSIT)
        self.maxCarry = None
        self.localShip = None
        self.pendingInstanceRequest = None
        return

    def announceGenerate(self):
        PVPGameBase.announceGenerate(self)
        self.pendingInstanceRequest = base.cr.relatedObjectMgr.requestObjects([self.instanceId], eachCallback=self.instanceGenerated)
        self.cr.loadingScreen.show()
        localAvatar.motionFSM.off()

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

    def getTitle(self):
        return PLocalizer.SBTGame

    def getInstructions(self):
        return PLocalizer.PVPShipBattleInstructions

    def handleUseKey(self, interactiveObj):
        pass

    def setMaxTeamScore(self, maxScore):
        self.maxTeamScore = maxScore

    def setShipDoId(self, shipId):
        self.shipRequest = base.cr.relatedObjectMgr.requestObjects([shipId], eachCallback=self._shipArrived)

    def _shipArrived(self, ship):
        self.localShip = ship
        ship.registerBuildCompleteFunction(Functor(self._boardShip, ship))

    def _boardShip(self, ship):
        self.acceptOnce(ship.uniqueName('localAvBoardedShip'), self._boardShipDone)
        ship.localAvatarInstantBoard()

    def _boardShipDone(self):
        self.sendUpdate('setBoarded', [])
        localAvatar.motionFSM.on()
        base.cr.loadingScreen.hide()

    def updateShipProximityText(self, ship):
        ship.b_setIsBoardable(ship.isBoardable)

    def handleShipUse(self, ship):
        pass

    def complete(self):
        PVPGameBase.complete(self)
        ship = base.localAvatar.ship
        if self.localShip:
            if self.localShip.sinkTrack:
                self.localShip.sinkTrack.pause()
                self.localShip.sinkTrack = None
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
        team = item.get('Team')
        score = item.get('Score')
        if team == localAvatar.getTeam():
            if self.prevTeamScore != None and score < self.prevTeamScore:
                itemColorScale = (1, 0, 0)
            self.prevTeamScore = score
        return MiniScoreItemGui(item, parent, self.instance, itemColorScale, self.instance.gameRules)

    def getScoreText(self, scoreValue):
        team = scoreValue.get('Team')
        score = scoreValue.get('Score')
        if team == localAvatar.getTeam():
            maxTeamScore = str(self.maxTeamScore)
            return PLocalizer.PVPYourTeam + str(score)
        elif team == localAvatar.getDoId():
            maxCarry = str(self.maxCarry)
            return '\n' + PLocalizer.PVPYourScoreIs + str(score)
        else:
            maxTeamScore = str(self.maxTeamScore)
            return PLocalizer.PVPOtherTeam + str(score)

    def respawn(self):
        posHpr = self.instance.cr.activeWorld.spawnInfo[0]
        localAvatar.setPos(posHpr[0], posHpr[1], posHpr[2])
        localAvatar.b_setGameState('Spawn')