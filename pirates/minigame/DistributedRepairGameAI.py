from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.directnotify import DirectNotifyGlobal
from DistributedRepairGameBase import *
import RepairGlobals
import random

class DistributedRepairGameAI(DistributedNodeAI, DistributedRepairGameBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedRepairGameAI')

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)
        DistributedRepairGameBase.__init__(self)

        self.avId2game = {}
        self.game2progress = {gameIndex: GAME_OPEN for gameIndex in xrange(self.getGameCount())}

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty

    def d_setDifficulty(self, difficulty):
        self.sendUpdate('setDifficulty', [difficulty])

    def b_setDifficulty(self, difficulty):
        self.setDifficulty(difficulty)
        self.d_setDifficulty(difficulty)

    def getDifficulty(self):
        return self.difficulty

    def setLocation(self, location):
        self.location = location

    def d_setLocation(self, location):
        self.sendUpdate('setLocation', [location])

    def b_setLocation(self, location):
        self.setLocation(location)
        self.d_setLocation(location)

    def getLocation(self):
        return self.location

    def isComplete(self):
        for gameIndex, gameProgress in self.game2progress.items():
            if gameProgress < GAME_COMPLETE:
                return False

        return True

    def setOnLand(self, land):
        self.setLocation(ON_LAND if land else AT_SEA)

    def joinGame(self, avatar):
        if avatar.doId in self.avId2game:
            return False

        if len(self.avId2game) >= self.getGameCount():
            return False

        self.sendUpdateToAvatarId(avatar.doId, 'start', [self.location])

        for gameIndex in self.game2progress:
            self.d_setMincroGameProgress(avatar.doId, gameIndex, self.game2progress[gameIndex])

        self.sendUpdateToAvatarId(avatar.doId, 'setAvIds2CurrentGameList', [self.avId2game.values(),
            self.avId2game.keys()])

        return True

    def quitGame(self, avatar):
        if avatar.doId in self.avId2game:
            del self.avId2game[avatar.doId]

        self.sendUpdateToAvatarId(avatar.doId, 'stop', [])
        return True

    def resetGame(self):
        for gameIndex in self.game2progress:
            self.game2progress[gameIndex] = GAME_OPEN

            # Update progress to all players
            for avatarId in self.avId2game:
                self.d_setMincroGameProgress(avatarId, gameIndex, self.game2progress[gameIndex])

    def requestMincroGame(self, gameIndex):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.notify.warning('Failed to requestMincroGame for non-existant avatar!')
            return

        if avatar.doId in self.avId2game:
            if self.avId2game[avatar.doId] == gameIndex:
                self.d_requestMincroGameResponse(avatar.doId, False)
                return

        self.avId2game[avatar.doId] = gameIndex
        self.d_requestMincroGameResponse(avatar.doId, True)

    def d_requestMincroGameResponse(self, avatarId, success):
        self.sendUpdateToAvatarId(avatarId, 'requestMincroGameResponse', [success, self.difficulty])

    def d_setMincroGameProgress(self, avatarId, gameIndex, progress):
        self.sendUpdateToAvatarId(avatarId, 'setMincroGameProgress', [gameIndex, progress])

    def reportMincroGameProgress(self, gameIndex, progress, rating):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.notify.warning('Failed to reportMincroGameProgress for non-existant avatar!')
            return

        # Check if this player is playing
        if avatar.doId not in self.avId2game:
            self.notify.warning('Received reportMincroGameProgress from an avatar not playing a minigame!')
            self.air.logPotentialHacker(
                message='Received reportMincroGameProgress from an avatar not playing a repair minigame',
                targetAvId=avatar.doId,
                gameIndex=gameIndex,
                progress=progress,
                rating=rating)
            return

        # Perform gameIndex sanity check
        if gameIndex != self.avId2game[avatar.doId]:
            self.notify.warning('Received reportMincroGameProgress from avatar for a game they are not post to be playing!')
            self.air.logPotentialHacker(
                message='Received reportMincroGameProgress from avatar for a game they are not post to be playing',
                targetAvId=avatar.doId,
                progress=progress,
                rating=rating)
            return

        self.game2progress[gameIndex] = progress

        # Update progress to all players
        for avatarId in self.avId2game:
            self.d_setMincroGameProgress(avatarId, gameIndex, self.game2progress[gameIndex])

        if not self.isComplete():
            return

        self.notify.debug('%s complete game %d with a rating of %s' % (avatar.doId, gameIndex, rating))

        # Reward the player with gold
        goldReward = random.randint(*RepairGlobals.AI.goldRewardRange)
        rewardMultiplier = 1

        if rating in RepairGlobals.AI.goldRewardMultiplier:
            rewardMultiplier = random.randint(*RepairGlobals.AI.goldRewardMultiplier[rating])

        goldReward * rewardMultiplier

        inventory = self.air.inventoryManager.getInventory(avatar.doId)
        if not inventory:
            self.notify.warning('Failed to get inventory for avatar %d!' % avatar.doId)
            return

        inventory.setGoldInPocket(inventory.getGoldInPocket() + goldReward)
        self.resetGame()
