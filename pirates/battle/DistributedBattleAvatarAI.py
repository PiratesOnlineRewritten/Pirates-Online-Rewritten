from direct.directnotify import DirectNotifyGlobal
from pirates.reputation. DistributedReputationAvatarAI import  DistributedReputationAvatarAI
from Teamable import Teamable
from direct.distributed.ClockDelta import globalClockDelta
from pirates.piratesbase import EmoteGlobals

class DistributedBattleAvatarAI(DistributedReputationAvatarAI, Teamable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleAvatarAI')

    def __init__(self, air):
        DistributedReputationAvatarAI.__init__(self, air)
        Teamable.__init__(self)
        self.currentWeaponId = 0
        self.isWeaponDrawn = False
        self.currentAmmo = 0
        self.currentCharm = 0
        self.isGhost = False
        self.ghostColor = 0
        self.ghostPowers = False
        self.shipId = 0
        self.maxHp = 0
        self.hp = 0
        self.quietly = False
        self.luck = 0
        self.maxLuck = 0
        self.mojo = 0
        self.maxMojo = 0
        self.swiftness = 0
        self.maxSwiftness = 0
        self.power = 0
        self.maxPower = 0
        self.luckMod = 0
        self.mojoMod = 0
        self.swiftnessMod = 0
        self.hasteMod = 0
        self.stunMod = 0
        self.powerMod = 0
        self.inInvasion = False
        self.attackerId = 0
        self.combo = 0
        self.teamCombo = 0
        self.comboDamage = 0
        self.skillEffects = []
        self.ensaredTargetId = 0
        self.level = 0

    def setAvatarType(self, avatarType):
        self.avatarType = avatarType

    def getAvatarType(self):
        return self.avatarType

    def d_setGameState(self, gameState):
        self.sendUpdate('setGameState', [gameState, globalClockDelta.getRealNetworkTime(bits=16)])

    def setIsGhost(self, isGhost):
        self.isGhost = isGhost

    def d_setIsGhost(self, isGhost):
        self.sendUpdate('setIsGhost', [isGhost])

    def b_setIsGhost(self, isGhost):
        self.setIsGhost(isGhost)
        self.d_setIsGhost(isGhost)

    def getIsGhost(self):
        return self.isGhost

    def setGhostColor(self, ghostColor):
        self.ghostColor = ghostColor

    def d_setGhostColor(self, ghostColor):
        self.sendUpdate("setGhostColor", [ghostColor])

    def b_setGhostColor(self, ghostColor):
        self.setGhostColor(ghostColor)
        self.d_setGhostColor(ghostColor)

    def getGhostColor(self):
        return self.ghostColor

    def setHasGhostPowers(self, ghostPowers):
        self.ghostPowers = ghostPowers

    def d_setHasGhostPowers(self, ghostPowers):
        self.sendUpdate('setHasGhostPowers', [ghostPowers])

    def b_setHasGhostPowers(self, ghostPowers):
        self.setHasGhostPowers(ghostPowers)
        self.d_setHasGhostPowers(ghostPowers)

    def getHasGhostPowers(self):
        return self.ghostPowers

    def setCurrentWeapon(self, currentWeapon, isWeaponDrawn):
        self.currentWeaponId = currentWeapon
        self.isWeaponDrawn = isWeaponDrawn

    def d_setCurrentWeapon(self, currentWeapon, isWeaponDrawn):
        self.sendUpdate('setCurrentWeapon', [currentWeapon, isWeaponDrawn])

    def b_setCurrentWeapon(self, currentWeapon, isWeaponDrawn):
        self.setCurrentWeapon(currentWeapon, isWeaponDrawn)
        self.d_setCurrentWeapon(currentWeapon, isWeaponDrawn)

    def getCurrentWeapon(self):
        return [self.currentWeaponId, self.isWeaponDrawn]

    def setCurrentAmmo(self, currentAmmo):
        self.currentAmmo = currentAmmo

    def d_setCurrentAmmo(self, currentAmmo):
        self.sendUpdate('setCurrentAmmo', [currentAmmo])

    def b_setCurrentAmmo(self, currentAmmo):
        self.setCurrentAmmo(currentAmmo)
        self.d_setCurrentAmmo(currentAmmo)

    def getCurrentAmmo(self):
        return self.currentAmmo

    def setCurrentCharm(self, currentCharm):
        self.currentCharm = currentCharm

    def d_setCurrentCharm(self, currentCharm):
        self.sendUpdate('setCurrentCharm', [currentCharm])

    def b_setCurrentCharm(self, currentCharm):
        self.setCurrentCharm(currentCharm)
        self.d_setCurrentCharm(currentCharm)

    def getCurrentCharm(self):
        return self.currentCharm

    def setShipId(self, shipId):
        self.shipId = shipId

    def d_setShipId(self, shipId):
        self.sendUpdate('setShipId', [shipId])

    def b_setShipId(self, shipId):
        self.setShipId(shipId)
        self.d_setShipId(shipId)

    def getShipId(self):
        return self.shipId

    def setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def d_setMaxHp(self, maxHp):
        self.sendUpdate('setMaxHp', [maxHp])

    def b_setMaxHp(self, maxHp):
        self.setMaxHp(maxHp)
        self.d_setMaxHp(maxHp)

    def getMaxHp(self):
        return self.maxHp

    def setHp(self, hp, quietly):
        self.hp = hp
        self.quietly = quietly

    def d_setHp(self, hp, quietly):
        self.sendUpdate('setHp', [hp, quietly])

    def b_setHp(self, hp, quietly = False):
        self.setHp(hp, quietly)
        self.d_setHp(hp, quietly)

    def getHp(self):
        return (self.hp, self.quietly)

    def setLuck(self, luck):
        self.luck = luck

    def d_setLuck(self, luck):
        self.sendUpdate('setLuck', [luck])

    def b_setLuck(self, luck):
        self.setLuck(luck)
        self.d_setLuck(luck)

    def getLuck(self):
        return self.luck

    def setMaxLuck(self, maxLuck):
        self.maxLuck = maxLuck

    def d_setMaxLuck(self, maxLuck):
        self.sendUpdate('setMaxLuck', [maxLuck])

    def b_setMaxLuck(self, maxLuck):
        self.setMaxLuck(maxLuck)
        self.d_setMaxLuck(maxLuck)

    def getMaxLuck(self):
        return self.maxLuck

    def setMaxMojo(self, maxMojo):
        self.maxMojo = maxMojo

    def d_setMaxMojo(self, maxMojo):
        self.sendUpdate('setMaxMojo', [maxMojo])

    def b_setMaxMojo(self, maxMojo):
        self.setMaxMojo(maxMojo)
        self.d_setMaxMojo(maxMojo)

    def getMaxMojo(self):
        return self.maxMojo

    def setMojo(self, mojo):
        self.mojo = mojo

    def d_setMojo(self, mojo):
        self.sendUpdate('setMojo', [mojo])

    def b_setMojo(self, mojo):
        self.setMojo(mojo)
        self.d_setMojo(self.mojo)

    def getMojo(self):
        return self.mojo

    def setSwiftness(self, swiftness):
        self.swiftness = swiftness

    def d_setSwiftness(self, swiftness):
        self.sendUpdate('setSwiftness', [swiftness])

    def b_setSwiftness(self, swiftness):
        self.setSwiftness(swiftness)
        self.d_setSwiftness(swiftness)

    def getSwiftness(self):
        return self.swiftness

    def setMaxSwiftness(self, maxSwiftness):
        self.maxSwiftness = maxSwiftness

    def d_setMaxSwiftness(self, maxSwiftness):
        self.sendUpdate('setMaxSwiftnes', [maxSwiftness])

    def b_setMaxSwiftness(self, maxSwiftness):
        self.setMaxSwiftnes(maxSwiftness)
        self.d_setMaxSwiftness(maxSwiftness)

    def getMaxSwiftness(self):
        return self.maxSwiftness

    def setPower(self, power):
        self.power = power

    def d_setPower(self, power):
        self.sendUpdate('setPower', [power])

    def b_setPower(self, power):
        self.setPower(power)
        self.d_setPower(power)

    def getPower(self):
        return self.power

    def setMaxPower(self, maxPower):
        self.maxPower = maxPower

    def d_setMaxPower(self, maxPower):
        self.sendUpdate('setMaxPower', [maxPower])

    def b_setMaxPower(self, maxPower):
        self.setMaxPower(maxPower)
        self.d_setMaxPower(maxPower)

    def getMaxPower(self):
        return self.maxPower

    def setLuckMod(self, luckMod):
        self.luckMod = luckMod

    def d_setLuckMod(self, luckMod):
        self.sendUpdate('setLuckMod', [luckMod])

    def b_setLuckMod(self, luckMod):
        self.setLuckMod(luckMod)
        self.d_setLuckMod(luckMod)

    def getLuckMod(self):
        return self.luckMod

    def setMojoMod(self, mojoMod):
        self.mojoMod = mojoMod

    def d_setMojoMod(self, mojoMod):
        self.sendUpdate('setMojoMod', [mojoMod])

    def b_setMojoMod(self, mojoMod):
        self.setMojoMod(mojoMod)
        self.d_setMojoMod(mojoMod)

    def getMojoMod(self):
        return self.mojoMod

    def getSwiftnessMod(self):
        return self.swiftnessMod

    def getHasteMod(self):
        return self.hasteMod

    def getStunMod(self):
        return self.stunMod

    def getPowerMod(self):
        return self.powerMod

    def setCombo(self, combo, teamCombo, comboDamage, attackerId):
        self.combo = combo
        self.teamCombo = teamCombo
        self.comboDamage = comboDamage
        self.attackerId = attackerId

    def d_setCombo(self, combo, teamCombo, comboDamage, attackerId):
        self.sendUpdate('setCombo', [combo, teamCombo, comboDamage, attackerId])

    def b_setCombo(self, combo, teamCombo, comboDamage, attackerId):
        self.setCombo(self, combo, teamCombo, comboDamage, attackerId)
        self.d_setCombo(self, combo, teamCombo, comboDamage, attackerId)

    def getCombo(self):
        return [self.combo, self.teamCombo, self.comboDamage, self.attackerId]

    def setSkillEffects(self, skillEffects):
        self.skillEffects = skillEffects

    def d_setSkillEffects(self, skillEffects):
        self.sendUpdate('setSkillEffects', [skillEffects])

    def b_setSkillEffects(self, skillEffects):
        self.setSkillEffects(skillEffects)
        self.d_setSkillEffects(skillEffects)

    def getSkillEffects(self):
        return self.skillEffects

    def setEnsaredTargetId(self, ensaredTargetId):
        self.ensaredTargetId = ensaredTargetId

    def d_setEnsaredTargetId(self, ensaredTargetId):
        self.sendUpdate('setEnsaredTargetId', [ensaredTargetId])

    def b_setEnsaredTargetId(self, ensaredTargetId):
        self.setEnsaredTargetId(ensaredTargetId)
        self.d_setEnsaredTargetId(ensaredTargetId)

    def getEnsnaredTargetId(self):
        return self.ensaredTargetId

    def setLevel(self, level):
        self.level = level

    def d_setLevel(self, level):
        self.sendUpdate('setLevel', [level])

    def b_setLevel(self, level):
        self.setLevel(level)
        self.d_setLevel(level)

    def getLevel(self):
        return self.level

    def setInInvasion(self, inInvasion):
        self.inInvasion = inInvasion

    def d_setInInvasion(self, inInvasion):
        self.sendUpdate('setInInvasion', [inInvasion])

    def b_setInInvasion(self, inInvasion):
        self.setInInvasion(inInvasion)
        self.d_setInInvasion(inInvasion)

    def getInInvasion(self):
        return self.inInvasion

    def setEmote(self, emoteId):
        if emoteId not in EmoteGlobals.emotes:

            # Log potential hacking
            self.air.logPotentialHacker(
                message='Avatar attempted to use invalid emote',
                accountId=self.air.getAccountIdFromSender(),
                emoteId=emoteId)

            return

        prereqs = EmoteGlobals.getEmotePrereqs(emoteId)
        if prereqs:

            fault = False
            for prereq in prereqs:
                if not prereq.avIsReadyAI(self):
                    fault = True
                    break

            if fault:

                # Log potential hacking
                self.air.logPotentialHacker(
                    message='Avatar attempted to use emote that does not meet requirements',
                    accountId=self.air.getAccountIdFromSender(),
                    emoteId=emoteId)

                return

        self.sendUpdate('playEmote', [emoteId])
