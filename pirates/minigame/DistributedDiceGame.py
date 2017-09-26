from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.minigame import DistributedGameTable
from pirates.minigame import PlayingCardGlobals
from pirates.minigame import DiceGlobals
from pirates.minigame import PlayingCard
from pirates.minigame import DiceGameGUI
from pirates.pirate import HumanDNA
from pirates.uberdog.UberDogGlobals import *
from direct.task import Task

class DistributedDiceGame(DistributedGameTable.DistributedGameTable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDiceGame')
    SeatInfo = (
     (
      Vec3(-4, 6.5, 0), Vec3(180, 0, 0)), (Vec3(-11, 0, 0), Vec3(-90, 0, 0)), (Vec3(-4, -6.5, 0), Vec3(0, 0, 0)), (Vec3(0, -6.5, 0), Vec3(0, 0, 0)), (Vec3(4, -6.5, 0), Vec3(0, 0, 0)), (Vec3(11, 0, 0), Vec3(90, 0, 0)), (Vec3(4, 6.5, 0), Vec3(180, 0, 0)))
    NumSeats = 7

    def __init__(self, cr, numdice=5, public=1, name='dice game'):
        DistributedGameTable.DistributedGameTable.__init__(self, cr)
        self.round = 0
        self.buttonSeat = 0
        self.gameState = DiceGlobals.DSTATE_GETREADY
        self.public = public
        self.numDice = numdice
        self.ante = 10
        self.lastSeat = -1
        self.gameName = name
        self.dicevals = {}
        #dna = HumanDNA.HumanDNA()
        #dna.setGender('f')
        #dna.setBodyShape(2)
        #dna.setBodyHeight(-0.376766204834)
        #dna.setHeadSize(0.0)
        #dna.setBodySkin(5)
        #dna.setClothesShirt(1, 13)
        #dna.setClothesVest(3, 0)
        #dna.setClothesCoat(0, 0)
        #dna.setClothesPant(2, 0)
        #dna.setClothesBelt(0, 0)
        #dna.setClothesSock(0)
        #dna.setClothesShoe(3)
        #dna.setHeadWidth(-0.104657292366)
        #dna.setHeadHeight(0.303506076336)
        #dna.setHeadRoundness(0.0741384625435)
        #dna.setJawWidth(0.0104657411575)
        #dna.setJawRoundness(-0.0732600092888)
        #dna.setJawAngle(0.189869761467)
        #dna.setJawLength(0.0209314227104)
        #self.dealer = self.createDealer('Dealer', dna, Vec3(0, 6.5, 0), Vec3(180, 0, 0))

    def generate(self):
        DistributedGameTable.DistributedGameTable.generate(self)
        self.setName(self.uniqueName('DistributedDiceGame'))
        self.reparentTo(render)

    def disable(self):
        DistributedGameTable.DistributedGameTable.disable(self)

    def delete(self):
        DistributedGameTable.DistributedGameTable.delete(self)
        self.dealer.delete()
        del self.dealer

    def getTableModel(self):
        table = loader.loadModel('models/props/Cardtable_Pill')
        table.setScale(2.5, 2.5, 1)
        return table

    def setTableState(self, round, buttonSeat):
        self.buttonSeat = buttonSeat
        if self.isLocalAvatarSeated():
            self.gui.setTableState(round, buttonSeat)

    def guiCallback(self, action):
        self.gui.disableAction()
        if action == 'roll':
            self.gui.rollDice()
        elif action == PlayingCardGlobals.Fold:
            self.d_clientAction(self.round, [action, 0])
        elif action == -1:
            self.requestExit()
        elif self.extraGuiCallback(action):
            pass
        else:
            self.notify.error('guiCallback: unknown action: %s' % action)

    def localAvatarSatDown(self, seatIndex):
        DistributedGameTable.DistributedGameTable.localAvatarSatDown(self, seatIndex)
        self.gui = DiceGameGUI.DiceGameGUI(self, self.numDice, self.public, self.gameName)
        self.extraGuiSetup()
        camera.setPosHpr(self, 0, -10, 20, 0, -65, 0)
        base.camLens.setMinFov(55)
        self.mySeat = seatIndex

    def localAvatarGotUp(self, seatIndex):
        print 'DistributedDiceGame:localAvatarGotUp'
        self.extraGuiDestroy()
        self.gui.destroy()
        del self.gui
        DistributedGameTable.DistributedGameTable.localAvatarGotUp(self, seatIndex)

    def playerIsReady(self):
        inv = base.localAvatar.getInventory()
        if inv:
            if inv.getStackQuantity(InventoryType.ItemTypeMoney) < self.ante:
                base.localAvatar.guiMgr.createWarning(PLocalizer.NotEnoughMoneyWarning, PiratesGuiGlobals.TextFG6)
            else:
                self.sendUpdate('playerIsReady', [])
                self.gui.mainButton['state'] = DGG.DISABLED
                self.gui.mainButton['frameColor'] = (0, 0.4, 0.05, 1)
                self.gameState = DiceGlobals.DSTATE_DOROLL

    def newRound(self):
        self.gui.mainButton.show()
        self.gui.resetGui()
        self.dicevals.clear()
        self.extraGuiReset()
        self.gui.mainButton['state'] = DGG.DISABLED
        self.gui.mainButton['frameColor'] = (0, 0.3, 0.4, 1)

    def yourTurn(self, activeSeat):
        print 'DistributedDiceGame:yourTurn - activeSeat %d' % activeSeat
        if activeSeat != self.mySeat:
            print 'DistributedDiceGame:yourTurn - not my seat (%d)' % self.mySeat
            return
        if self.gameState == DiceGlobals.DSTATE_DOROLL:
            if activeSeat == self.mySeat:
                self.gui.timeToRoll()
            else:
                self.gui.mainButton['state'] = DGG.DISABLED
        self.extraYourTurn()

    def rollResults(self, seat, dice):
        self.dicevals[seat] = dice

    def playerHasLost(self, avId):
        pass

    def extraGuiSetup(self):
        pass

    def extraGuiDestroy(self):
        pass

    def extraYourTurn(self):
        pass

    def extraGuiReset(self):
        pass

    def currentTurn(self, state, seat, name):
        if seat != self.mySeat:
            self.lastSeat = seat
        self.gameState = state
        if state == DiceGlobals.DSTATE_PLAY:
            self.gui.updateTurnStatus(name + PLocalizer.DiceText_isTurn)
        elif state == DiceGlobals.DSTATE_DOROLL:
            self.gui.updateTurnStatus(name + PLocalizer.DiceText_Roll)

    def youWin(self, winId, name):
        self.gui.updateTurnStatus(name + PLocalizer.DiceText_Wins)
        avId = base.localAvatar.getDoId()
        if avId == winId:
            pass
        self.gui.mainButton['state'] = DGG.NORMAL
        self.gui.mainButton['text'] = 'READY'
        self.gui.mainButton['command'] = self.playerIsReady
        self.gui.mainButton['frameColor'] = (0, 0.4, 0.1, 1)
        self.gui.mainButton.show()
        self.gui.resetGui()
        self.dicevals.clear()
        self.extraGuiReset()

    def sendChat(self, chatType):
        avId = base.localAvatar.getDoId()
        self.sendUpdate('sendChat', [chatType, avId])