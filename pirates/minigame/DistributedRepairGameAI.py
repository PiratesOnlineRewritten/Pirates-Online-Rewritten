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

        self.avatar2game = {}
        self.avatar2timeout = {}
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
        if avatar.doId in self.avatar2game:
            return False

        if len(self.avatar2game) >= self.getGameCount():
            return False

        self.sendUpdateToAvatarId(avatar.doId, 'start', [self.location])

        for gameIndex in self.game2progress:
            self.d_setMincroGameProgress(avatar.doId, gameIndex, self.game2progress[gameIndex])

        self.sendUpdateToAvatarId(avatar.doId, 'setAvIds2CurrentGameList', [self.avatar2game.values(),
            self.avatar2game.keys()])

        self.addTimeout(avatar)
        return True

    def quitGame(self, avatar):
        if avatar.doId in self.avatar2game:
            del self.avatar2game[avatar.doId]

        self.removeTimeout(avatar)
        self.sendUpdateToAvatarId(avatar.doId, 'stop', [])
        return True

    def __quit(self, avatar, task):
        self.quitGame(avatar)
        return task.done

    def resetGame(self):
        for gameIndex in self.game2progress:
            self.game2progress[gameIndex] = GAME_OPEN

            # Update progress to all players
            for avatarId in self.avatar2game:
                self.d_setMincroGameProgress(avatarId, gameIndex, self.game2progress[gameIndex])

    def requestMincroGame(self, gameIndex):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.notify.warning('Failed to requestMincroGame for non-existant avatar!')
            return

        if avatar.doId in self.avatar2game:
            if self.avatar2game[avatar.doId] == gameIndex:
                self.d_requestMincroGameResponse(avatar.doId, False)
                return

        self.avatar2game[avatar.doId] = gameIndex
        self.addTimeout(avatar)

        self.d_requestMincroGameResponse(avatar.doId, True)

    def addTimeout(self, avatar):
        if avatar.doId in self.avatar2timeout:
            self.removeTimeout(avatar)

        self.avatar2timeout[avatar.doId] = taskMgr.doMethodLater(RepairGlobals.AI.inactiveClientKickTime, self.__quit,
            self.uniqueName('timeout-%d' % avatar.doId), extraArgs=[avatar], appendTask=True)

    def removeTimeout(self, avatar):
        if avatar.doId not in self.avatar2timeout:
            return

        taskMgr.remove(self.avatar2timeout.pop(avatar.doId))

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
        if avatar.doId not in self.avatar2game:
            self.air.logPotentialHacker(
                message='Received reportMincroGameProgress from an avatar not playing a repair minigame',
                accountId=self.air.getAccountIdFromSender(),
                targetAvId=avatar.doId,
                gameIndex=gameIndex,
                progress=progress,
                rating=rating)
            return

        # Perform gameIndex sanity check
        if gameIndex != self.avatar2game[avatar.doId]:
            self.air.logPotentialHacker(
                message='Received reportMincroGameProgress from avatar for a game they are not post to be playing',
                accountId=self.air.getAccountIdFromSender(),
                targetAvId=avatar.doId,
                progress=progress,
                rating=rating)
            return

        self.addTimeout(avatar)
        self.game2progress[gameIndex] = progress

        # Update progress to all players
        for avatarId in self.avatar2game:
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
