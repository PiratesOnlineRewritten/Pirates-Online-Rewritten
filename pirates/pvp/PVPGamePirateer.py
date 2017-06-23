from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.pvp.PVPGameBase import PVPGameBase
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.interact import InteractiveBase
from pirates.ship import DistributedSimpleShip
from pirates.pvp.MiniScoreItemGui import MiniScoreItemGui
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import random

class PVPGamePirateer(PVPGameBase):
    notify = directNotify.newCategory('PVPGamePirateer')

    def __init__(self, cr):
        PVPGameBase.__init__(self, cr)
        self.teamScore = 0
        self.wrecks = {}
        self.coinCarriers = []
        self.otherTeamScore = 0
        self.maxTeamScore = 1
        self.maxCarry = 0
        self.prevTeamScore = 0
        self.prevLoadScore = 0
        self.depositSound = loadSfx(SoundGlobals.SFX_PVP_TREASURE_DEPOSIT)
        self.pendingInstanceRequest = None
        return

    def generate(self):
        PVPGameBase.generate(self)
        self.accept(PiratesGlobals.EVENT_SPHERE_PORT + PiratesGlobals.SPHERE_ENTER_SUFFIX, self.handleEnterPort)
        self.accept(PiratesGlobals.EVENT_SPHERE_PORT + PiratesGlobals.SPHERE_EXIT_SUFFIX, self.handleExitPort)
        self.accept('enterwreckSphere', self.approachWreck)
        self.accept('exitwreckSphere', self.leaveWreck)

    def announceGenerate(self):
        PVPGameBase.announceGenerate(self)
        self.pendingInstanceRequest = base.cr.relatedObjectMgr.requestObjects([self.instanceId], eachCallback=self.instanceGenerated)

    def instanceGenerated(self, instanceObj):
        self.instance = instanceObj
        localAvatar.guiMgr.showPVPUI(self)

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

    def isObjInteractionAllowed(self, object, avatar):
        return 0

    def handleEnterPort(self, depositType, shipId):
        self.notify.debug('<PIRATEER> ------- handleEnterPort')
        self.sendUpdate('portEntered', [depositType, shipId])

    def handleExitPort(self, depositType, shipId):
        self.notify.debug('<PIRATEER> ------- handleEnterPort')
        self.sendUpdate('portExited', [depositType, shipId])

    def setMaxTeamScore(self, maxScore):
        self.maxTeamScore = maxScore

    def setMaxCarry(self, maxCarry):
        self.maxCarry = maxCarry

    def updateShipProximityText(self, ship):
        ship.b_setIsBoardable(ship.isBoardable)

    def handleShipUse(self, ship):
        pass

    def updateTreasureProximityText(self, treasure):
        treasure.proximityText = PLocalizer.PirateerDeckTreasure

    def handleUseKey(self, interactiveObj):
        if isinstance(interactiveObj, DistributedSimpleShip.DistributedSimpleShip):
            self.handleShipUse(interactiveObj)

    def getTitle(self):
        return PLocalizer.PirateerTitle

    def getInstructions(self):
        return PLocalizer.PirateerInstructions

    def displayCoins(self, shipIds):
        for i in shipIds:
            if i not in self.coinCarriers:
                self.displayCoin(i)

    def displayCoin(self, shipId):
        self.coinCarriers.append(shipId)
        ship = base.cr.doId2do.get(shipId)
        self.notify.debug('<PIRATEER> ------ we gots us a coin thief %s' % shipId)
        ship.stats['maxSpeed'] = ship.stats['maxSpeed'] * 3 / 4
        barUI = loader.loadModel('models/gui/treasure_loaded')
        self.titleFrameImage = OnscreenImage(image=barUI, pos=(0, -45, 210), scale=(45,
                                                                                    45,
                                                                                    45), parent=ship)
        self.titleFrameImage.setBillboardPointEye()
        self.titleFrameImage.setLightOff()

    def unDisplayCoin(self, shipId):
        self.coinCarriers.remove(shipId)
        ship = base.cr.doId2do.get(shipId)
        if ship:
            icon = ship.find('**/treasure*')
            if icon:
                icon.hide()
                icon.removeNode()

    def coinCaptured(self, shipId):
        ship = base.cr.doId2do.get(shipId)
        self.notify.debug('<PIRATEER> ------ a winner %s' % ship.getPVPTeam())

    def approachWreck(self, collEntry):
        wid = int(collEntry.getIntoNodePath().getNetTag('avId'))
        if collEntry.getFromNodePath().hasNetTag('shipId'):
            shipId = int(collEntry.getFromNodePath().getNetTag('shipId'))
            self.notify.debug('<PIRATEER> ------ %s approaches wreck %s' % (str(shipId), str(wid)))
            self.sendUpdate('lootWreck', [wid, shipId])

    def leaveWreck(self, collEntry):
        wid = int(collEntry.getIntoNodePath().getNetTag('avId'))
        if collEntry.getFromNodePath().hasNetTag('shipId'):
            shipId = int(collEntry.getFromNodePath().getNetTag('shipId'))
            self.notify.debug('<PIRATEER> ------ %s leaves wreck %s' % (str(shipId), str(wid)))
            self.sendUpdate('unLootWreck', [wid, shipId])

    def getScoreList(self):
        return self.scoreList

    def setScoreList(self, teams, scores):
        self.scoreList = []
        for currIdx in range(len(teams)):
            if teams[currIdx] > 10 and teams[currIdx] % 10 != localAvatar.getTeam():
                continue
            self.scoreList.append({'Team': teams[currIdx],'Score': scores[currIdx]})

        self.scoreList.sort(self.sortScores)
        print 'got new score list %s' % self.scoreList
        messenger.send(self.getItemChangeMsg())

    def sortScores(self, item1, item2):
        team1 = item1.get('Team')
        team2 = item2.get('Team')
        if team1 == 0:
            return 100
        else:
            return team1 - team2

    def createNewItem(self, item, parent, itemType=None, columnWidths=[], color=None):
        itemColorScale = None
        blink = False
        team = item.get('Team')
        score = item.get('Score')
        if team == localAvatar.getTeam():
            if score < self.prevTeamScore:
                blink = True
                self.prevTeamScore = score
        if team > 10 and team < 20 and score != self.prevLoadScore:
            blink = True
            self.prevLoadScore = score
        return MiniScoreItemGui(item, parent, self.instance, itemColorScale, self.instance.gameRules, blink)

    def getScoreText(self, scoreValue):
        team = scoreValue.get('Team')
        score = scoreValue.get('Score')
        maxTeamScore = str(self.maxTeamScore)
        maxCarry = str(self.maxCarry)
        if team > 20:
            return PLocalizer.PVPYourShip + str(score) + '/' + str(maxCarry)
        elif team > 10:
            if score > 4:
                return 'Loading [.....]'
            elif score > 3:
                return 'Loading [.... ]'
            elif score > 2:
                return 'Loading [...  ]'
            elif score > 1:
                return 'Loading [..   ]'
            elif score > 0:
                return 'Loading [.    ]'
            else:
                return 'Loading [     ]'
        else:
            return PLocalizer.PVPTeam % str(team) + str(score) + '/' + str(maxTeamScore)