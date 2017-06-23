import sys
import random
from pandac.PandaModules import NodePath, Point3
from direct.showbase import DirectObject
from direct.interval.IntervalGlobal import Sequence, Func, Wait
from pirates.piratesbase import PiratesGlobals
from pirates.npc import Townfolk
from pirates.distributed import DistributedInteractive
from pirates.piratesbase import PLocalizer
from direct.directnotify import DirectNotifyGlobal
from pirates.pirate import HumanDNA
from pirates.piratesbase import PLocalizer
from pirates.world.LocationConstants import LocationIds
from pirates.world.DistributedIsland import DistributedIsland
from pirates.piratesgui.PDialog import PDialog
from pirates.inventory.Lootable import Lootable
from otp.otpgui import OTPDialog
from pirates.inventory import ItemGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesgui import PiratesGuiGlobals
from pirates.audio import SoundGlobals
from FishingGame import FishingGame
import FishingGlobals

class DistributedFishingSpot(DistributedInteractive.DistributedInteractive, Lootable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFishingSpot')

    def __init__(self, cr):
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        Lootable.__init__(self)
        self.index = -1
        self.onABoat = False
        self.fadeTime = 0.5
        self.loadingSequence = None
        self.fishingGame = None
        self.xpBonus = 0
        self.goldBonus = 0
        self.showTutorial = False
        self.__dialog = None
        self.prevBaseCamParent = None
        self.prevCamPos = None
        self.prevCamHpr = None
        self.oldAvatarPos = None
        return

    def generate(self):
        DistributedInteractive.DistributedInteractive.generate(self)
        NodePath.__init__(self, 'DistributedFishingSpot')
        self.setInteractOptions(proximityText=PLocalizer.InteractFishingSpot, sphereScale=8, diskRadius=8)
        self.setAllowInteract(True)

    def announceGenerate(self):
        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        if self.getOnABoat() and self.getParentObj():
            self.getParentObj().registerFishingSpot(self)

    def setXpBonus(self, xpBonusAmount):
        self.xpBonus = xpBonusAmount
        if self.fishingGame:
            self.fishingGame.updateResultsScreen()

    def getXpBonus(self):
        return self.xpBonus

    def setGoldBonus(self, goldBonusAmount):
        self.goldBonus = goldBonusAmount
        if self.fishingGame:
            self.fishingGame.updateResultsScreen()

    def getGoldBonus(self):
        return self.goldBonus

    def setOnABoat(self, onABoat):
        self.onABoat = onABoat

    def getOnABoat(self):
        return self.onABoat

    def setOceanOffset(self, offset):
        self.oceanOffset = offset

    def requestInteraction(self, avId, interactType=0):
        inv = localAvatar.getInventory()
        rodQty = inv.getStackQuantity(InventoryType.FishingRod)
        regLureQty = inv.getStackQuantity(InventoryType.RegularLure)
        legendaryLureQty = inv.getStackQuantity(InventoryType.LegendaryLure)
        if rodQty > 0:
            if regLureQty + legendaryLureQty <= 0:
                localAvatar.guiMgr.createWarning(PLocalizer.FishingNoLuresWarning, PiratesGuiGlobals.TextFG6)
            elif localAvatar.isUndead():
                localAvatar.guiMgr.createWarning(PLocalizer.NoFishingWhileUndeadWarning, PiratesGuiGlobals.TextFG6)
            else:
                localAvatar.motionFSM.off()
                DistributedInteractive.DistributedInteractive.requestInteraction(self, avId, interactType)
        else:
            localAvatar.guiMgr.createWarning(PLocalizer.FishingNoRodWarning, PiratesGuiGlobals.TextFG6)

    def rejectInteraction(self):
        localAvatar.motionFSM.on()
        localAvatar.gameFSM.request('LandRoam')
        self.refreshState()
        DistributedInteractive.DistributedInteractive.rejectInteraction(self)

    def requestExit(self):
        DistributedInteractive.DistributedInteractive.requestExit(self)
        taskMgr.remove('tryFishingSpotAgain')
        if self.onABoat and self.oldAvatarPos:
            localAvatar.setPos(self.oldAvatarPos)
            self.oldAvatarPos = None
        if not localAvatar.gameFSM.isInTransition():
            localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
        if self.loadingSequence:
            self.loadingSequence.pause()
            self.loadingSequence.clearToInitial()
        base.transitions.fadeIn(self.fadeTime)
        if self.fishingGame is not None:
            self.fishingGame.delete()
            self.fishingGame = None
        if self.prevBaseCamParent is not None:
            base.cam.reparentTo(self.prevBaseCamParent)
            base.cam.setPos(self.prevCamPos)
            base.cam.setHpr(self.prevCamHpr)
            self.prevBaseCamParent = None
            self.prevCamPos = None
            self.prevCamHpr = None
        taskMgr.remove(self.uniqueName('bootFromFishing'))
        localAvatar.motionFSM.on()
        self.setAllowInteract(True)
        base.localAvatar.guiMgr.setIgnoreEscapeHotKey(False)
        self.refreshState()
        return

    def checkAndLoadFishingGame(self):
        localAvatar.b_setGameState('Fishing')
        if self.fishingGame is None:
            self.fishingGame = FishingGame(self)
        if self.onABoat:
            self.oldAvatarPos = localAvatar.getPos()
            localAvatar.collisionGhost()
            localAvatar.setPos(*FishingGlobals.fishingSpotPosHprBoatInformation[self.index]['pos'])
            localAvatar.setHpr(*FishingGlobals.fishingSpotPosHprBoatInformation[self.index]['hpr'])
            self.setHpr(*FishingGlobals.fishingSpotPosHprBoatInformation[self.index]['fishingSpotHpr'])
            base.cam.reparentTo(self.fishingGame.fishingSpot)
            base.cam.setPos(13.0, -18.0, 7.0)
            base.cam.setHpr(0.0, 0.0, 0.0)
        else:
            par = localAvatar.getParentObj()
            uid = par.getUniqueId()
            if uid == LocationIds.DEL_FUEGO_ISLAND:
                localAvatar.setHpr(50.0, 0.0, 0.0)
            elif localAvatar.onWelcomeWorld:
                localAvatar.setHpr(self.getH(render) - 196.0, 0.0, 0.0)
            else:
                localAvatar.setHpr(self.getH(render) - 16.0, 0.0, 0.0)
            localAvatar.setPos(self, Point3(*FishingGlobals.fishingSpotPosOffset))
            base.cam.reparentTo(self.fishingGame.fishingSpot)
            base.cam.setHpr(0.0, 0.0, 0.0)
        localAvatar.sendCurrentPosition()
        return

    def requestPlayerIdleState(self, task=None):
        if base.localAvatar.find('**/fishingRod').isEmpty():
            taskMgr.doMethodLater(0.5, self.requestPlayerIdleState, name='tryFishingSpotAgain')
        else:
            self.fishingGame.fsm.request('PlayerIdle')
            self.fishingGame.checkLures()

    def enterUse(self):
        DistributedInteractive.DistributedInteractive.enterUse(self)
        self.prevBaseCamParent = base.cam.getParent()
        self.prevCamPos = base.cam.getPos()
        self.prevCamHpr = base.cam.getHpr()
        if not base.transitions.fadeOutActive():
            self.loadingSequence = Sequence(Func(self.fadeOut), Wait(self.fadeTime + 0.1), Func(self.checkAndLoadFishingGame), Wait(1.5), Func(self.requestPlayerIdleState), Func(self.fadeIn))
            self.loadingSequence.start()
        else:
            print '--------------------- DistributedFishingSpot : Trouble fading out!'
        taskMgr.doMethodLater(FishingGlobals.idleDuration, self.bootFromFishing, self.uniqueName('bootFromFishing'))
        self.accept('mouse1', self.resetBootCheck)
        self.accept('fishing-skill-used', self.resetBootCheck)
        self.accept('newItemHeld', self.resetBootCheck)
        self.accept('releaseHeld', self.resetBootCheck)
        self.accept('plunderClosed', self.requestPlayerIdle)

    def fadeOut(self):
        base.transitions.setFadeColor(0, 0, 0)
        if base.transitions.fadeOutActive():
            return
        base.transitions.fadeOut(self.fadeTime)
        base.localAvatar.guiMgr.inventoryUIManager.hidePlunder()
        base.loadingScreen.showTarget(fishing=True)
        base.cr.loadingScreen.show()

    def fadeIn(self):
        base.transitions.fadeIn(self.fadeTime)
        base.musicMgr.request(SoundGlobals.MUSIC_MINIGAME_FISHING, looping=True, priority=1)
        base.cr.loadingScreen.hide()
        base.localAvatar.guiMgr.inventoryUIManager.showPlunder()

    def exitUse(self):
        self.ignoreAll()
        DistributedInteractive.DistributedInteractive.exitUse(self)
        base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_MINIGAME_FISHING)

    def firstTimeFisher(self):
        self.showTutorial = True

    def spotFilledByAvId(self, avId):
        if avId == 0:
            self.setAllowInteract(True)
            self.showTutorial = False
            return
        if base.localAvatar.doId != avId:
            self.setAllowInteract(False)

    def delete(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('bootFromFishing'))
        if self.fishingGame is not None:
            self.fishingGame.delete()
            del self.fishingGame
        if self.prevBaseCamParent is not None:
            base.cam.reparentTo(self.prevBaseCamParent)
            base.cam.setPos(self.prevCamPos)
            base.cam.setHpr(self.prevCamHpr)
            self.prevBaseCamParent = None
            self.prevCamPos = None
            self.prevCamHpr = None
        DistributedInteractive.DistributedInteractive.delete(self)
        return

    def b_setIndex(self, index):
        self.index = index
        self.sendUpdate('setIndex', [index])

    def setIndex(self, index):
        self.index = index

    def getIndex(self):
        return self.index

    def d_caughtFish(self, fishId, weight):
        self.sendUpdate('caughtFish', [fishId, weight])

    def lostLure(self, lureId):
        pass

    def d_lostLure(self, lureId):
        self.sendUpdate('lostLure', [lureId])

    def handleEndInteractKey(self):
        if self.fishingGame and not self.fishingGame.gui.resultsScreen.isHidden() or localAvatar.guiMgr.inventoryUIManager.hasPlunder():
            return
        if not self.fishingGame:
            return
        if self.__dialog == None:
            self.__dialog = PDialog(text=PLocalizer.FishingGui['ExitText'], style=OTPDialog.YesNo, giveMouse=False, command=self.__onDialogItemSelected)
        else:
            self.__dialog.cleanup()
            self.__dialog = None
        return

    def __onDialogItemSelected(self, value):
        if value == 1:
            self.requestExit()
        self.__dialog.cleanup()
        self.__dialog = None
        return

    def bootFromFishing(self, task=None):
        self.requestExit()

    def resetBootCheck(self, arg1=None, arg2=None):
        taskMgr.remove(self.uniqueName('bootFromFishing'))
        taskMgr.doMethodLater(FishingGlobals.idleDuration, self.bootFromFishing, self.uniqueName('bootFromFishing'))

    def requestPlayerIdle(self, arg1=None):
        if self.fishingGame.fsm.getCurrentOrNextState() == 'Reward':
            self.fishingGame.fsm.request('PlayerIdle')

    def startLooting(self, plunderList, itemsToTake=0, timer=0, autoShow=False, customName=None):
        Lootable.startLooting(self, plunderList, itemsToTake, timer=timer, autoShow=autoShow, customName=PLocalizer.FoundFishing)
        if self.fishingGame and not self.fishingGame.gui.resultsScreen.isHidden():
            localAvatar.guiMgr.inventoryUIManager.hidePlunder()

    def handleArrivedOnShip(self, ship):
        pass

    def handleLeftShip(self, ship):
        pass