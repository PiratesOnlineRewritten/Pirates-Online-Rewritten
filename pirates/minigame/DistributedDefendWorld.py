from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.battle import WeaponGlobals
from pirates.inventory.Lootable import Lootable
from pirates.minigame.DistributedMiniGameWorld import DistributedMiniGameWorld
from pirates.minigame.CannonDefenseFSM import CannonDefenseFSM
from pirates.minigame import CannonDefenseGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import TODGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
import random

class EndOfWaveData():

    def __init__(self):
        self.playerNames = []
        self.shipsSunkWave = []
        self.damgeDealtWave = []
        self.shotsFiredWave = []
        self.accuracyWave = []
        self.timePlayed = []
        self.shipsSunkOverall = []
        self.damgeDealtOverall = []
        self.shotsFiredOverall = []
        self.accuracyOverall = []
        self.goldPaidOverall = []
        self.treasureEarned = 0
        self.treasureStolen = 0
        self.treasureRemaining = 0
        self.myGoldEarned = 0
        self.myGoldBonus = 0


class DistributedDefendWorld(DistributedMiniGameWorld, Lootable):

    def __init__(self, cr):
        DistributedMiniGameWorld.__init__(self, cr)
        Lootable.__init__(self)
        self.fsm = CannonDefenseFSM(self)
        self._numWaves = len(CannonDefenseGlobals.waveData)
        self._waveNumber = 0
        self._bonusSet = 0
        self.timeRemaining = 0
        self.treasurePercent = 1.0
        self.__isGameFull = False
        self.sfxGoldAttack = None
        self.goldBonus = 0
        self.endOfWaveData = EndOfWaveData()
        self.startingState = None
        self.flamingBarrels = []
        self.initGoldPiles()
        base.shipsVisibleFromIsland = True
        return

    def initGoldPiles(self):
        self.goldPiles = []
        self.goldPilesIndex = [
         5, 3, 7, 6, 4, 1, 9, 2, 8, 0]
        for i in range(10):
            goldPile = loader.loadModel('models/minigames/pir_m_gam_can_goldPile')
            goldPile.setScale(3.0, 3.0, 9.0)
            goldPile.setPos(660.0 + i * 30.0 + i % 2 * 10, -465.0 - i % 2 * 30.0, 25.0 - i % 2 * 5.0)
            goldPile.setHpr(random.random() * 360, 0, 0)
            goldPile.reparentTo(self)
            goldPile.setLightOff()
            self.goldPiles.append(goldPile)

        base.dw = self

    def setGoldBonus(self, goldBonusAmount):
        self.endOfWaveData.myGoldBonus = goldBonusAmount

    def setGoldPileSizes(self):
        treasureRemaining = CannonDefenseGlobals.MINE_TREASURE_START * self.treasurePercent
        for i in range(10):
            goldPile = self.goldPiles[self.goldPilesIndex[i]]
            if treasureRemaining > (i + 1) * CannonDefenseGlobals.MINE_TREASURE_START / 10.0:
                goldPile.unstash()
                goldPile.setScale(3.0, 3.0, 3.0)
            elif treasureRemaining > i * CannonDefenseGlobals.MINE_TREASURE_START / 10.0:
                goldPile.unstash()
                goldMod = treasureRemaining - i * CannonDefenseGlobals.MINE_TREASURE_START / 10.0
                goldPile.setScale(1.0 + 20.0 * goldMod / CannonDefenseGlobals.MINE_TREASURE_START, 1.0 + goldMod * 20.0 / CannonDefenseGlobals.MINE_TREASURE_START, 0.5 + goldMod * 25.0 / CannonDefenseGlobals.MINE_TREASURE_START)
            else:
                goldPile.stash()

    def generate(self):
        DistributedMiniGameWorld.generate(self)

    def announceGenerate(self):
        DistributedMiniGameWorld.announceGenerate(self)
        CullBinManager.getGlobalPtr().addBin('gui-cannonDefense', CullBinManager.BTFixed, 40)
        self.setupLocalPlayer()

    def disable(self):
        DistributedMiniGameWorld.disable(self)
        base.shipsVisibleFromIsland = False

    def delete(self):
        DistributedMiniGameWorld.delete(self)
        self.fsm.demand('Off')

    def setupLocalPlayer(self):
        base.musicMgr.request(SoundGlobals.MUSIC_MINIGAME_CANNON, priority=1, looping=1)
        localAvatar.disableLootUI()
        localAvatar.disableTutorial()
        localAvatar.surpressRepFlag(InventoryType.CannonRep)
        localAvatar.b_setTeleportFlag(PiratesGlobals.TFCannonDefense)
        self.loadSfx()

    def loadSfx(self):
        self.sfxGoldAttack = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_GOLD_ATTACK)

    def unloadSfx(self):
        if self.sfxGoldAttack:
            loader.unloadSfx(self.sfxGoldAttack)
            self.sfxGoldAttack = None
        return

    def kickPlayer(self):
        self.exitMiniGame()

    def turnOn(self, av=None):
        DistributedMiniGameWorld.turnOn(self, av)

    def enterCannon(self, cannonDoId):

        def avatarHere():
            doIds = [
             cannonDoId]
            base.cr.relatedObjectMgr.requestObjects(doIds, self._doCannonInteraction)
            base.cr.timeOfDayManager.setEnvironment(TODGlobals.ENV_CANNONGAME)

        self.accept('localAvTeleportFinished', avatarHere)

    def requestState(self, stateName):
        if localAvatar.cannon:
            self.fsm.request(stateName)
            self.startingState = None
        else:
            self.startingState = stateName
        return

    def onPlayerJoin(self, doid, gameFull):
        self.__isGameFull = gameFull

    def onPlayerLeave(self, doid, gameFull):
        self.__isGameFull = gameFull

    def setCurrentWave(self, waveNumber, bonusSet):
        messenger.send('endOfWave')
        self._waveNumber = waveNumber
        self._bonusSet = bonusSet
        if localAvatar.cannon and hasattr(localAvatar.cannon.cgui, 'hud'):
            actualWaveNumber = self._waveNumber + self._bonusSet * self._numWaves
            localAvatar.cannon.cgui.hud.timeRemainingUI.setWaveNumber(actualWaveNumber + 1)
        self.setGoldPileSizes()

    def updateTimer(self, timeLeft):
        self.timeRemaining = float(timeLeft) / 100.0
        if localAvatar.cannon and hasattr(localAvatar.cannon.cgui, 'hud'):
            localAvatar.cannon.cgui.hud.timeRemainingUI.setPercent(self.timeRemaining)

    def setTreasureRemaining(self, percent):
        newValue = float(percent) / 100.0
        if newValue < self.treasurePercent:
            if self.sfxGoldAttack:
                if self.sfxGoldAttack.status() != AudioSound.PLAYING:
                    base.playSfx(self.sfxGoldAttack)
        self.treasurePercent = newValue
        if localAvatar.cannon and hasattr(localAvatar.cannon.cgui, 'hud'):
            localAvatar.cannon.cgui.hud.goldRemainingUI.setPercent(self.treasurePercent)
        self.setGoldPileSizes()

    def getWaveNumber(self):
        return self._waveNumber

    def getBonusSet(self):
        return self._bonusSet

    def getNumWaves(self):
        return self._numWaves

    def getWorldPos(self, node):
        if not node.isEmpty() and self.isOnStage():
            return node.getPos(self)

    def _doCannonInteraction(self, dos):
        cannon = dos[0]
        base.cr.activeWorld.handleUseKey(self)
        currentInteractive = base.cr.interactionMgr.getCurrentInteractive()
        if currentInteractive and currentInteractive.isExclusiveInteraction():
            currentInteractive.requestExit()
        cannon.requestInteraction(localAvatar, 1)
        cannon.setReadyEvent(self.cannonReady)
        cannon.setExitEvent(self.exitMiniGame)

    def cannonReady(self):
        if self.startingState:
            self.fsm.demand(self.startingState)
        self.setCurrentWave(self._waveNumber, self._bonusSet)
        self.updateTimer(self.timeRemaining * 100.0)
        self.setTreasureRemaining(self.treasurePercent * 100.0)

    def disableCannonInput(self):
        if localAvatar.cannon and hasattr(localAvatar.cannon, 'disableInput'):
            localAvatar.cannon.disableInput()
            localAvatar.cannon.cgui.fadeOutAmmoCounters()

    def enableCannonInput(self):
        if localAvatar.cannon and hasattr(localAvatar.cannon, 'enableInput'):
            localAvatar.cannon.enableInput()
            localAvatar.cannon.cgui.fadeInAmmoCounters()

    def disableCannonFire(self):
        if localAvatar.cannon and hasattr(localAvatar.cannon, 'disableCannonFireInput'):
            localAvatar.cannon.disableCannonFireInput()
            localAvatar.cannon.cgui.fadeOutAmmoCounters()

    def enableCannonFire(self):
        if localAvatar.cannon and hasattr(localAvatar.cannon, 'enableCannonFireInput'):
            localAvatar.cannon.enableCannonFireInput()
            localAvatar.cannon.cgui.fadeInAmmoCounters()

    def exitMiniGame(self):
        localAvatar.enableLootUI()
        localAvatar.enableTutorial()
        localAvatar.clearRepFlags()
        self.unloadSfx()
        localAvatar.b_clearTeleportFlag(PiratesGlobals.TFCannonDefense)
        self.__isGameFull = False
        self.stopLooting()
        base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_MINIGAME_CANNON)
        self.fsm.demand('Off')
        self.clearDefenseAmmo()
        self.sendUpdate('requestLeave', [])

    def requestStartBonusRound(self):
        if self.fsm.state == 'Victory':
            self.sendUpdate('requestStartBonusRound', [localAvatar.getDoId()])

    def setPlayerNames(self, names):
        self.endOfWaveData.playerNames = names

    def setShipsSunkWave(self, shipsSunk):
        self.endOfWaveData.shipsSunkWave = shipsSunk

    def setDamageDealtWave(self, damageDealt):
        self.endOfWaveData.damgeDealtWave = damageDealt

    def setShotsFiredWave(self, shots):
        self.endOfWaveData.shotsFiredWave = shots

    def setAccuracyWave(self, accuracy):
        self.endOfWaveData.accuracyWave = accuracy

    def setTimePlayed(self, time):
        self.endOfWaveData.timePlayed = time

    def setShipsSunkOverall(self, shipsSunk):
        self.endOfWaveData.shipsSunkOverall = shipsSunk

    def setDamageDealtOverall(self, damageDealt):
        self.endOfWaveData.damgeDealtOverall = damageDealt

    def setShotsFiredOverall(self, shots):
        self.endOfWaveData.shotsFiredOverall = shots

    def setAccuracyOverall(self, accuracy):
        self.endOfWaveData.accuracyOverall = accuracy

    def setGoldPaidOverall(self, gold):
        self.endOfWaveData.goldPaidOverall = gold

    def setTreasureStats(self, stolen, remaining, earned):
        self.endOfWaveData.treasureStolen = stolen
        self.endOfWaveData.treasureRemaining = remaining
        self.endOfWaveData.treasureEarned = earned

    def setAwardedGold(self, gold):
        self.endOfWaveData.myGoldEarned = gold

    def setBankNotes(self, bankNotes, totalBankNotes):
        messenger.send('incBankNotes', [bankNotes, totalBankNotes])

    def setExperience(self, experience, totalExperience):
        self.experiece = experience
        messenger.send('incDefenseCannonExp', [experience, totalExperience])

    def d_addUnlockedAmmo(self, ammoSkillId):
        self.sendUpdate('addUnlockedAmmo', [ammoSkillId])

    def setUnlockedAmmo(self, ammoSkillIds):
        messenger.send('unlockAmmo', [ammoSkillIds])

    def updateWaitTimer(self, timeLeft):
        self.fsm.updateCountDown(timeLeft)

    def d_sendMessage(self, senderId, message):
        self.sendUpdate('sendMessage', [senderId, message])

    def setMessage(self, senderId, senderName, message):
        base.talkAssistant.receiveCannonDefenseMessage(message, senderName)

    def getTypeName(self):
        return 'Defense Rewards'

    def clearDefenseAmmo(self):
        for cannonball in render.findAllMatches('**/=DefenseAmmo'):
            ammo = cannonball.getPythonTag('DefenseAmmo')
            if ammo:
                ammo.destroy()