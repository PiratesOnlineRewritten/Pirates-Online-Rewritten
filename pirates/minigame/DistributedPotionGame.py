7
from direct.interval.IntervalGlobal import *
if __name__ == '__main__':
    from direct.directbase.DirectStart import *
    from direct.showbase.DirectObject import DirectObject as DistributedObject
else:
    from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.uberdog.UberDogGlobals import InventoryType
import PotionGlobals
import PotionRecipeData
from pirates.reputation import ReputationGlobals
from PotionGame import PotionGame
from pirates.world.LocationConstants import LocationIds

class DistributedPotionGame(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedRepairGame')
    IslandColorSets = {LocationIds.DEL_FUEGO_ISLAND: 1,LocationIds.TORTUGA_ISLAND: 2,LocationIds.CUBA_ISLAND: 3}

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.colorSet = 0
        self.fadeTime = 0.1
        self.fadeTask = None
        self.xpBonus = 0
        return

    def setColorSet(self, colorSet):
        self.colorSet = colorSet

    def setXpBonus(self, xpBonusAmt):
        self.xpBonus = xpBonusAmt
        self.potionGame.updateResultsScreen()

    def getXpBonus(self):
        return self.xpBonus

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.fadeTask = taskMgr.doMethodLater(1, self.fadeIn, 'potionfade', extraArgs=[])
        self.determineColorSet()

    def disable(self):
        if self.fadeTask:
            taskMgr.remove(self.fadeTask)
            self.fadeTask = None

        DistributedObject.disable(self)

    def determineColorSet(self):
        potionTable = self.getParentObj()
        if potionTable:
            island = potionTable.getParentObj()
            if island:
                colorSet = self.IslandColorSets.get(island.uniqueId, 0)
                self.setColorSet(colorSet)

    def fadeOut(self):
        base.transitions.setFadeColor(0, 0, 0)
        if not base.transitions.fadeOutActive():
            base.transitions.fadeOut(self.fadeTime)

    def fadeIn(self):
        self.potionGame = PotionGame(self)
        base.cr.loadingScreen.hide()
        base.transitions.fadeIn(self.fadeTime)

    def done(self):
        if base.transitions.fadeOutActive():
            self.loadingSequence = Sequence(Func(self.fadeOut), Wait(self.fadeTime), Func(self.d_finish))
            self.loadingSequence.start()
        else:
            self.d_finish()

    def d_completeRecipe(self, recipeID, clearNewFlag):
        self.sendUpdate('completeRecipe', [recipeID, clearNewFlag])

    def d_completeSurvival(self, ingredients, tiles):
        self.sendUpdate('completeSurvival', [ingredients, tiles])

    def d_claimXPBonus(self, bonusLevel):
        self.sendUpdate('claimXPBonus', [bonusLevel])

    def d_setHintsActive(self, active):
        self.sendUpdate('setHintsActive', [active])

    def d_finish(self):
        self.sendUpdate('finish')

    def d_reset(self):
        self.sendUpdate('reset')

    def checkExit(self):
        if self.potionGame.gameFSM.getCurrentOrNextState() in ['Input', 'Anim', 'Hint', 'Idle', 'Welcome']:
            self.potionGame.confirmQuit()
        elif self.potionGame.gameFSM.getCurrentOrNextState() in ['Results']:
            self.potionGame.resultsScreen.quit()

    def getPlayerNotNewFlags(self):
        madeList = []
        inv = localAvatar.getInventory()
        for madeID in InventoryType.HaveMadeList:
            if inv.getStackQuantity(madeID) > 0:
                potionID = PotionGlobals.getPotionForHaveMadeID(madeID)
                if potionID > 0:
                    madeList.append(potionID)

        return madeList

    def getPlayerPotionLevel(self):
        inv = localAvatar.getInventory()
        repAmt = inv.getAccumulator(InventoryType.PotionsRep)
        repLvl = ReputationGlobals.getLevelFromTotalReputation(InventoryType.PotionsRep, repAmt)
        return repLvl[0]

    def handleArrivedOnShip(self, ship):
        pass
