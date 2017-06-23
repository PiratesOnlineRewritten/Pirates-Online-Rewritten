from pandac.PandaModules import Vec3, Vec4, Point3

class VariableContainer():

    def __init__(self):
        pass


AI = VariableContainer()
AI.goldRewardRange = (15, 35)
AI.goldRewardMultiplier = [
 (14.0, 3.0), (18.0, 2.5), (24.0, 2.0), (36.0, 1.6), (52.0, 1.3), (72.0, 1.15)]
AI.repairRewardRange = (5000, 1000)
AI.grapeshotEffectCooldown = 2.0
AI.grapeshotEffectProbability = 0.5
AI.kickedTimestampLife = 60.0 * 60.0
AI.inactiveClientKickTime = 60.0 * 2.0 + 2.0
AI.numTimesKickedBeforeBlacklisted = 3
AI.maxPlayersPerBench = 5
AI.baseRepairAmount = 0.5
AI.maxRepairCount = 30
AI.reductionAtFullRepair = 0.5
AI.maxCombatCount = 20
AI.reductionAtFullCombat = 0.5
AI.critGrapeshotCombatDebuff = 3
AI.grapeshotCombatDebuff = 3
AI.regularCombatDebuff = 1
AI.totalDifficulty = AI.maxRepairCount + AI.maxCombatCount
AI.difficultyIncreasePoint = AI.totalDifficulty / 10.0
AI.repairDebuffPerModelClass = {1: 1.0,2: 1.0,3: 1.0,11: 1.0,12: 1.0,13: 1.0,21: 1.0,22: 1.0,23: 1.0,24: 1.0,25: 1.0,26: 1.0,27: 1.0}
AI.sailRepairPercent = 0.15
AI.armorRepairPercent = 0.15
AI.hpRepairPercent = 0.4
AI.hpTertiaryDecay = 0.0
Common = VariableContainer()
Common.guiShakeCooldownTime = 2.0
Common.youWinPos = {'careening': (-0.12, 0.0, 0.22),'pumping': (0.0, 0.0, 0.15),'sawing': (0.0, 0.0, 0.15),'bracing': (0.0, 0.0, 0.22),'hammering': (0.0, 0.0, 0.38),'pitching': (0.0, 0.0, 0.22)}
Common.scorePos = {'careening': (-0.12, 0.0, 0.09),'pumping': (0.0, 0.0, 0.02),'sawing': (0.0, 0.0, 0.02),'bracing': (0.0, 0.0, 0.09),'hammering': (0.0, 0.0, 0.25),'pitching': (0.0, 0.0, 0.09)}
Common.speedThresholds = {'careening': [(5.0, 15.0), (10.0, 30.0), (20.0, 90.0)],'pumping': [(10.0, 13.0), (20.0, 40.0), (40.0, 90.0)],'sawing': [(6.0, 9.0), (12.0, 18.0), (30.0, 45.0)],'bracing': [(5.0, 15.0), (30.0, 45.0), (90.0, 180.0)],'hammering': [(5.0, 10.0), (10.0, 20.0), (20.0, 40.0)],'pitching': [(8.0, 16.0), (16.0, 32.0), (32.0, 64.0)]}
Careening = VariableContainer()
Careening.barnacleCountRange = (15, 30)
Careening.superScrubMultiplier = 4.0
Careening.superScrubDecreaseRate = 0.4
Careening.superScrubIncreaseRate = 0.8
Careening.barnacleHPRange = (30, 70)
Careening.barnacleHPScaleRange = (1.0, 3.0)
Careening.xRange = (
 -0.615, 0.375)
Careening.yRange = (-0.165, 0.515)
Careening.barnacleRadius = 0.04
Careening.mossPercentage = 0.75
Careening.mossPosVariance = 0.01
Careening.mossEdgeRestrictionAmount = 0.1
Careening.showBarnacleHP = False
Pumping = VariableContainer()
Pumping.pumpPowerRange = (0.06, 0.02)
Pumping.hitRange = (0.18, 0.18)
Pumping.barStartRange = (1.2, 1.0)
Pumping.barSpeedMin = 2.0
Pumping.barSpeedMax = 0.3
Pumping.barSpeedIncrease = 1.25
Pumping.barSpeedDecrease = 0.8
Pumping.chainMultiplier = 0.08
Sawing = VariableContainer()
Sawing.difficultySets = (
 (3, 3, 1, 1), (3, 1, 1, 2), (1, 2, 1, 2), (3, 1, 2, 2), (2, 2, 1, 2), (3, 2, 1, 4), (2, 4, 3, 2), (4, 2, 1, 2), (4, 1, 1, 5), (2, 2, 4, 5))
Sawing.waypointRange = (0.08, 0.08, 0.08, 0.11, 0.1)
Sawing.sawlineColor = Vec4(0.75, 0.75, 0.75, 0.7)
Sawing.sawlineLineThickness = 4.0
Sawing.sawlineLinespawnDist = 0.02
Sawing.testWaypointDelta = 0.04
Sawing.playSawingSoundDelta = 0.1
Sawing.totalPoints = 20.0
Sawing.pointsPerBoard = 7.0
Sawing.pointsLostForZone1 = 4.0
Sawing.pointsLostForZone2 = 1.0
Sawing.cutColor = (0.3, 0.3, 0.3, 1.0)
Sawing.zone1Color = (0.75, 0.75, 0.75, 1.0)
Sawing.zone2Color = (0.75, 0.75, 0.75, 1.0)
Sawing.sawTurnSpeed = 1000
Sawing.newBoardAnimTime = 0.25
Sawing.splitBoardAnimTime = 0.5
Sawing.activeBoardPosition = (0.0, 0.0, 0.1)
Sawing.boardYDist = 1.3
from RepairGridPiece import GOAL_HORIZ_1, GOAL_HORIZ_2, GOAL_VERT_1
Bracing = VariableContainer()
Bracing.difficultyLevels = (
 (
  8, (GOAL_HORIZ_1,)), (7, (GOAL_HORIZ_1,)), (6, (GOAL_HORIZ_1,)), (7, (GOAL_HORIZ_1, GOAL_VERT_1)), (6, (GOAL_HORIZ_1, GOAL_VERT_1)), (5, (GOAL_HORIZ_1, GOAL_VERT_1)), (4, (GOAL_HORIZ_1, GOAL_VERT_1)), (5, (GOAL_HORIZ_1, GOAL_HORIZ_2)), (4, (GOAL_HORIZ_1, GOAL_HORIZ_2)), (3, (GOAL_HORIZ_1, GOAL_HORIZ_2)))
Bracing.moveTime = 0.08
Bracing.fadeTime = 0.15
Bracing.movePieceThreshold = 0.08
Bracing.pushPieceThreshold = 0.01
Bracing.repairTimeframe = 20
Hammering = VariableContainer()
Hammering.reticleScaleRange = (0.2, 1.0)
Hammering.reticleScaleRate = 1.0
Hammering.recoveryTime = 4.0
Hammering.nailCountRange = (4, 8)
Hammering.rankingThresholds = (5, 4, 3, 2, 1)
Hammering.hitForgiveness = 0.1
Hammering.useReticleColor = True
Pitching = VariableContainer()
Pitching.leakScaleRange = (0.1, 0.275)
Pitching.spawnDelayRange = (0.5, 0.1, 2.0, 1.0)
Pitching.leakCountRange = (16, 32)
Pitching.maxLeaksRange = (2, 5)
Pitching.useReticle = True
Pitching.ratingGive = 0
REPAIR_AT_SEA_REWARD_RATING = [
 0, 1, 1, 1.5, 2.0]
REPAIR_AT_SEA_GAME_MULTIPLIER = [
 20, 60, 200, 40, 20]

def getAtSeaRepairRating(rating, gameType):
    if rating > 4 or rating < 0:
        rating = 0
    return REPAIR_AT_SEA_REWARD_RATING[rating] * REPAIR_AT_SEA_GAME_MULTIPLIER[gameType]