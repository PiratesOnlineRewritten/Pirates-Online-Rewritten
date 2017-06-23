import random
import math
from pandac.PandaModules import NodePath, Point3
from direct.interval.IntervalGlobal import Sequence, Parallel, Wait, Func
from direct.interval.LerpInterval import LerpFunc
from direct.task import Task
from panda3d.core import TextNode
import FishingGlobals
from FishFSM import FishFSM
from BlendActor import BlendActor
from pirates.effects.FishIdleBubbleEffect import FishIdleBubbleEffect
from pirates.effects.FishBitingBubbleEffect import FishBitingBubbleEffect
from pirates.effects.FishFightingHookedBubbleEffect import FishFightingHookedBubbleEffect
import MinigameUtils
from pirates.uberdog.UberDogGlobals import InventoryType

class Fish(NodePath):

    def __init__(self, fishManager, myData, index, trophy=0):
        NodePath.__init__(self, '%s_%d' % (myData['name'], index))
        self.trophy = trophy
        self.myData = myData
        if not self.trophy:
            self.fishManager = fishManager
            self.index = index
            self.fsm = FishFSM(self)
            self.weight = random.randint(self.myData['weightRange'][0], self.myData['weightRange'][1])
        else:
            self.weight = trophy
        self.adjustedScale = (self.myData['scaleRange'][1] - self.myData['scaleRange'][0]) * (self.weight - self.myData['weightRange'][0]) / (self.myData['weightRange'][1] - self.myData['weightRange'][0]) + self.myData['scaleRange'][0]
        self.initActor()
        if not self.trophy:
            self.initVariables()
            self.initFishStatusIcon()
            if FishingGlobals.wantDebugCollisionVisuals:
                self.initCollisions()
        self.avoidingFish = False
        self.biteBubbleEffect = None
        self.idleBubbleEffect = None
        self.fightBubbleEffect = None
        self.behaviorNameToFunction = {'straight': self.performStraightBehavior,'sineStraight': self.performSineStraightBehavior,'erratic': self.performErraticBehavior}
        self.sineDtAccumulator = 0.0
        self.erraticDtAccumulator = 0.0
        self.myZ = 0.0
        if not self.trophy:
            self.setLightOff()
        return

    def initActor(self):
        self.animDict = {}
        for anim in FishingGlobals.fishAnimations:
            self.animDict[anim] = 'models/char/pir_a_gam_fsh_%s_%s.bam' % (self.myData['model'], anim)

        self.actor = BlendActor('models/char/pir_r_gam_fsh_%s.bam' % self.myData['model'], self.animDict, FishingGlobals.defaultFishBlendTime, FishingGlobals.fishBlendTimeDict)
        self.actor.reparentTo(self)
        self.actor.setScale(self.adjustedScale)
        self.mouthJoint = self.actor.exposeJoint(None, 'modelRoot', 'hookAttach')
        self.attractionPoint = NodePath('AttractionPoint')
        self.attractionPoint.reparentTo(self.mouthJoint)
        self.attractionPoint.setPos(0.0, 0.0, 0.0)
        self.actor.setPlayRate(self.myData['speed'] * self.myData['swimAnimationMultiplier'], 'swimIdle')
        self.actor.setPlayRate(self.myData['speed'] * self.myData['swimAnimationMultiplier'], 'swimIdleOpposite')
        self.actor.setPlayRate(self.myData['speed'] * self.myData['turnAnimationMultiplier'], 'turn')
        self.actor.setPlayRate(self.myData['speed'] * self.myData['turnAnimationMultiplier'], 'turnOpposite')
        if not self.trophy:
            self.setBin('fishingGame', 10)
        return

    def codeReload(self):
        self.actor.setPlayRate(self.myData['speed'] * self.myData['swimAnimationMultiplier'], 'swimIdle')
        self.actor.setPlayRate(self.myData['speed'] * self.myData['swimAnimationMultiplier'], 'swimIdleOpposite')
        self.actor.setPlayRate(self.myData['speed'] * self.myData['turnAnimationMultiplier'], 'turn')
        self.actor.setPlayRate(self.myData['speed'] * self.myData['turnAnimationMultiplier'], 'turnOpposite')

    def initFishStatusIcon(self):
        self.fishStatusIconTextNode = TextNode('fishBitingIcon')
        self.fishStatusIconNodePath = NodePath(self.fishStatusIconTextNode)
        self.fishStatusIconNodePath.setPos(0.0, 0.0, self.myData['indicatorHeightOffset'])
        self.fishStatusIconTextNode.setText('?')
        self.fishStatusIconTextNode.setTextColor(1.0, 0.0, 0.0, 1.0)
        self.fishStatusIconNodePath.reparentTo(self.mouthJoint)
        self.fishStatusIconNodePath.setBillboardPointEye()
        self.fishStatusIconNodePath.hide()
        self.fishStatusIconNodePath.setShaderOff()

    def initVariables(self):
        self.attractionVisual = None
        self.collisionVisual = None
        self.movingRight = True
        self.turnSpeed = 160.0
        self.turnTowardLureInterval = None
        self.velocity = FishingGlobals.baseFishVelocity * self.myData['speed']
        self.accel = FishingGlobals.baseFishAccel * self.myData['speed']
        self.fishMoveSequence = None
        self.bubbleEffect = None
        return

    def initCollisions(self):
        self.collisionVisual = loader.loadModel('models/props/crate')
        self.collisionVisual.setTransparency(1)
        self.collisionVisual.setColor(1.0, 1.0, 1.0, 0.3)
        self.collisionVisual.setScale(*self.myData['collisionBoxSize'])
        self.collisionVisual.setPos(*self.myData['collisionBoxOffset'])
        self.collisionVisual.reparentTo(self)
        self.collisionVisual.hide()
        self.attractionVisual = loader.loadModel('models/ammunition/cannonball')
        self.attractionVisual.setTransparency(1)
        self.attractionVisual.setColor(0.0, 1.0, 0.0, 0.3)
        self.attractionVisual.setScale(self.myData['attractionRadius'])
        self.attractionVisual.reparentTo(self.attractionPoint)
        self.attractionVisual.hide()
        self.collisionVisualVisible = False

    def hide(self):
        NodePath.hide(self)
        if self.idleBubbleEffect:
            self.idleBubbleEffect.hide()

    def show(self):
        NodePath.show(self)
        if self.idleBubbleEffect:
            self.idleBubbleEffect.show()

    def reloadCollisions(self):
        if FishingGlobals.wantDebugCollisionVisuals:
            self.collisionVisual.removeNode()
            self.attractionVisual.removeNode()
            self.initCollisions()

    def cleanFishData(self):
        pass

    def destroy(self):
        self.closeFish = []
        self.actor.destroy()
        self.stopIdleBubbleEffect()
        self.stopFightBubbleEffect()
        if self.fishMoveSequence:
            self.fishMoveSequence.pause()
            self.fishMoveSequence = None
        if self.fsm:
            del self.fsm
            self.fsm = None
        self.behaviorNameToFunction = {}
        self.removeNode()
        return

    def pickPositionAndSwim(self):
        self.initVariables()
        self.actor.clearControlEffectWeights()
        if self.myData['depth'] == 0:
            depth = random.uniform(FishingGlobals.fishingLevelBoundaries[self.myData['depth']], self.fishManager.gameObject.waterLevel + FishingGlobals.fishSpawnBelowWaterLevelHeight)
        else:
            depth = random.uniform(FishingGlobals.fishingLevelBoundaries[self.myData['depth']], FishingGlobals.fishingLevelBoundaries[self.myData['depth'] - 1])
        startX = random.uniform(FishingGlobals.leftFishBarrier + 5.0, FishingGlobals.rightFishBarrier - 5.0)
        self.setPos(startX, 0.0, depth)
        if random.randint(0, 1):
            self.fsm.request('TurnAround', 'Swimming', False)
        else:
            self.fsm.request('Swimming')

    def turnAround(self, nextState, shouldMoveRight):
        if self.velocity[0] < 0 and shouldMoveRight:
            self.velocity[0] = -self.velocity[0]
        elif self.velocity[0] > 0 and not shouldMoveRight:
            self.velocity[0] = -self.velocity[0]
        self.movingRight = self.velocity[0] > 0
        if self.fishMoveSequence:
            self.fishMoveSequence.pause()
            self.fishMoveSequence.clearToInitial()
        animationToTurn = 'turn'
        if self.movingRight:
            animationToTurn = 'turnOpposite'
        durationOfFishTurn = self.myData['durationOfFishTurn']
        self.fishMoveSequence = Parallel(Sequence(Func(self.actor.changeAnimationTo, animationToTurn, False), Wait(durationOfFishTurn), Func(self.fsm.request, nextState)), Sequence(Wait(durationOfFishTurn * 0.33), Func(self.setXVelocity, 0.0), Wait(durationOfFishTurn * 0.66), Func(self.setXVelocity, self.velocity[0])), name='%s_turnAroundInterval' % self.getName())
        self.velocity[0] = -self.velocity[0]
        self.fishMoveSequence.start()

    def setXVelocity(self, newVel):
        self.velocity[0] = newVel

    def checkForBiting(self):
        if self.fishManager.activeFish is not None:
            return
        if self.fishManager.gameObject.fsm.getCurrentOrNextState() not in ['Fishing', 'Reeling', 'LureStall', 'LegdFishShow']:
            return
        inv = localAvatar.getInventory()
        rodLvl = inv.getItemQuantity(InventoryType.FishingRod)
        if self.myData['depth'] + 1 > rodLvl:
            return
        self.fsm.request('Biting')
        return

    def checkForBoxOverlap(self, otherFish):
        pos = self.getPos(self.fishManager.gameObject.fishingSpot)
        size = self.myData['collisionBoxSize']
        offset = list(self.myData['collisionBoxOffset'])
        otherPos = otherFish.getPos()
        otherSize = otherFish.myData['collisionBoxSize']
        otherOffset = list(otherFish.myData['collisionBoxOffset'])
        if pos[0] + size[0] / 2.0 + offset[0] > otherPos[0] - otherSize[0] / 2.0 + otherOffset[0] and pos[0] - size[0] / 2.0 + offset[0] < otherPos[0] + otherSize[0] / 2.0 + otherOffset[0] and pos[2] + size[2] / 2.0 + offset[2] > otherPos[2] - otherSize[2] / 2.0 + otherOffset[2] and pos[2] - size[2] / 2.0 + offset[2] < otherPos[2] + otherSize[2] / 2.0 + otherOffset[2]:
            return True
        return False

    def checkForCloseFish(self, index):
        if index < len(self.fishManager.uncaughtFish) - 1:
            for i in range(index + 1, len(self.fishManager.uncaughtFish)):
                if self.fishManager.uncaughtFish[i].index != self.index:
                    if self.checkForBoxOverlap(self.fishManager.uncaughtFish[i]):
                        self.closeFish.append(self.fishManager.uncaughtFish[i])
                        if FishingGlobals.wantDebugCollisionVisuals:
                            self.collisionVisual.setColor(1, 0, 0, 0.3)

        if len(self.closeFish) == 0:
            if FishingGlobals.wantDebugCollisionVisuals:
                self.collisionVisual.setColor(1, 1, 1, 0.3)

    def checkForLures(self, currentState, lurePos):
        if self.getX() + FishingGlobals.fishAttractionOffset < lurePos[0] and self.movingRight or self.getX() - FishingGlobals.fishAttractionOffset > lurePos[0] and not self.movingRight:
            if self.attractionPoint.getDistance(self.fishManager.gameObject.lure) < self.myData['attractionRadius'] + self.fishManager.gameObject.lure.lureAttractRadius:
                self.checkForBiting()

    def update(self, dt, index, lurePos):
        currentState = self.fsm.getCurrentOrNextState()
        self.closeFish = []
        if currentState in ['ScareAway', 'Swimming', 'Flee', 'TurnAround']:
            self.checkForCloseFish(index)
            if currentState in ['Swimming']:
                self.checkForLures(currentState, lurePos)
            self.updateBasedOnBehavior(dt, lurePos)
        elif currentState in ['Hooked', 'AboutToFight', 'HookedFighting']:
            self.checkForCloseFish(-1)
            for fish in self.closeFish:
                self.makeFishRunFromMe(fish)

    def makeFishRunFromMe(self, otherFish):
        if otherFish.fsm.getCurrentOrNextState() == 'Flee' or otherFish.fsm.getCurrentOrNextState() == 'TurnAround':
            return
        if otherFish.getX() < self.getX(self.fishManager.gameObject.fishingSpot) and otherFish.movingRight:
            otherFish.fsm.request('TurnAround', 'Flee', False)
        elif otherFish.getX() > self.getX(self.fishManager.gameObject.fishingSpot) and not otherFish.movingRight:
            otherFish.fsm.request('TurnAround', 'Flee', True)
        else:
            otherFish.fsm.request('Flee')

    def updateBasedOnBehavior(self, dt, lurePos):
        currentState = self.fsm.getCurrentOrNextState()
        newX = self.getX()
        newY = self.getY()
        newZ = self.getZ()
        for fish in self.closeFish:
            if self.myData['size'] == 'small' and fish.myData['size'] == 'large':
                if self.checkForEating(fish):
                    return
            self.avoidingFish = True
            if fish.velocity[1] > 0.0 and fish.avoidingFish:
                self.velocity[1] = -FishingGlobals.fishAvoidYVelocity
            else:
                self.velocity[1] = FishingGlobals.fishAvoidYVelocity
            if abs(fish.getY() - self.getY()) > self.myData['collisionBoxSize'][1] + fish.myData['collisionBoxSize'][1]:
                self.velocity[1] = 0.0

        if len(self.closeFish) == 0 and abs(self.getY()) > FishingGlobals.fishYTolerance:
            self.avoidingFish = False
            if self.getY() > 0:
                self.velocity[1] = -FishingGlobals.fishAvoidYVelocity
            else:
                self.velocity[1] = FishingGlobals.fishAvoidYVelocity
        elif len(self.closeFish) == 0 and abs(self.getY()) < FishingGlobals.fishYTolerance:
            self.avoidingFish = False
            self.velocity[1] = 0.0
            self.setY(0.0)
        newY = self.getY() + self.velocity[1] * dt + self.accel[1] * dt * dt
        if currentState in ['Swimming', 'TurnAround', 'Flee', 'ScareAway']:
            if currentState == 'ScareAway':
                newX, newZ = self.performScareAwayBehavior(dt, self.velocity, self.accel)
            else:
                if currentState == 'Flee':
                    newX, newZ = self.performFleeBehavior(dt, self.velocity, self.accel)
                else:
                    newX, newZ = self.behaviorNameToFunction[self.myData['behaviorDict']['name']](dt, self.velocity, self.accel)
                currentState = self.fsm.getCurrentOrNextState()
                if newX < FishingGlobals.leftFishBarrier:
                    if currentState == 'ScareAway':
                        if newX < FishingGlobals.leftFishBarrier - FishingGlobals.fullyOffscreenXOffset:
                            self.fsm.request('Offscreen')
                            return
                    elif currentState != 'TurnAround' and not self.movingRight:
                        self.fsm.request('TurnAround', 'Swimming', True)
                elif newX > FishingGlobals.rightFishBarrier:
                    if currentState != 'TurnAround' and self.movingRight:
                        self.fsm.request('TurnAround', 'Swimming', False)
            newZ = min(max(FishingGlobals.fishingLevelBoundaries[len(FishingGlobals.fishingLevelBoundaries) - 1], newZ), self.fishManager.gameObject.waterLevel + FishingGlobals.fishSpawnBelowWaterLevelHeight)
        self.setPos(newX, newY, newZ)

    def checkForEating(self, fishThatWillEat):
        if (self.getX() < fishThatWillEat.getX() and not fishThatWillEat.movingRight or self.getX() > fishThatWillEat.getX() and fishThatWillEat.movingRight) and self.fsm.getCurrentOrNextState() == 'Swimming' and fishThatWillEat.fsm.getCurrentOrNextState() == 'Swimming' and random.random() < 1.0:
            self.fsm.request('BeingEaten', fishThatWillEat)
            fishThatWillEat.fsm.request('Eating', self.weight)
            return True
        return False

    def startIdleBubbleEffect(self):
        self.idleBubbleEffect = FishIdleBubbleEffect.getEffect(unlimited=True)
        if self.idleBubbleEffect:
            self.idleBubbleEffect.reparentTo(self.mouthJoint)
            self.idleBubbleEffect.setScale(1.0)
            self.idleBubbleEffect.setHpr(0, 0, 0)
            self.idleBubbleEffect.setLifespanBasedOnDepth(self.getPos(render))
            self.idleBubbleEffect.setBubbleSizeBasedOnWeight(self.weight)
            self.idleBubbleEffect.particleDummy.setBin('fishingGame', 5)
            self.idleBubbleEffect.startLoop()

    def stopIdleBubbleEffect(self):
        if self.idleBubbleEffect:
            self.idleBubbleEffect.stopLoop()
        self.idleBubbleEffect = None
        return

    def startBiteBubbleEffect(self):
        self.biteBubbleEffect = FishBitingBubbleEffect.getEffect(unlimited=True)
        if self.biteBubbleEffect:
            self.biteBubbleEffect.reparentTo(self.mouthJoint)
            self.biteBubbleEffect.setScale(1.0)
            self.biteBubbleEffect.setHpr(0, 0, 0)
            self.biteBubbleEffect.setLifespanBasedOnDepth(self.getPos(render))
            self.biteBubbleEffect.setBubbleSizeBasedOnWeight(self.weight)
            self.biteBubbleEffect.particleDummy.setBin('fishingGame', 5)
            self.biteBubbleEffect.play()

    def stopBiteBubbleEffect(self):
        if self.biteBubbleEffect:
            self.biteBubbleEffect.stopLoop()
        self.biteBubbleEffect = None
        return

    def startFightBubbleEffect(self):
        self.fightBubbleEffect = FishFightingHookedBubbleEffect.getEffect(unlimited=True)
        if self.fightBubbleEffect:
            self.fightBubbleEffect.reparentTo(self.mouthJoint)
            self.fightBubbleEffect.setScale(1.0)
            self.fightBubbleEffect.setHpr(0, 0, 0)
            self.fightBubbleEffect.setLifespanBasedOnDepth(self.getPos(render))
            self.fightBubbleEffect.setBubbleSizeBasedOnWeight(self.weight)
            self.fightBubbleEffect.particleDummy.setBin('fishingGame', 5)
            self.fightBubbleEffect.startLoop()

    def stopFightBubbleEffect(self):
        if self.fightBubbleEffect:
            self.fightBubbleEffect.stopLoop()
        self.fightBubbleEffect = None
        return

    def performStraightBehavior(self, dt, velocity, accel):
        newX = self.getX() + velocity[0] * dt + accel[0] * dt * dt
        newZ = self.getZ() + velocity[2] * dt + accel[2] * dt * dt
        return (
         newX, newZ)

    def performSineStraightBehavior(self, dt, velocity, accel):
        self.sineDtAccumulator += dt
        newX = self.getX() + velocity[0] * dt + accel[0] * dt * dt
        newZ = self.myZ + math.sin(self.sineDtAccumulator) * self.myData['behaviorDict']['sineMultiplier']
        return (
         newX, newZ)

    def performScareAwayBehavior(self, dt, velocity, accel):
        newX = self.getX() + velocity[0] * FishingGlobals.scareAwayVelocityMultiplier * dt + accel[0] * dt * dt
        newZ = self.getZ() + velocity[2] * FishingGlobals.scareAwayVelocityMultiplier * dt + accel[2] * dt * dt
        return (
         newX, newZ)

    def performFleeBehavior(self, dt, velocity, accel):
        newX = self.getX() + velocity[0] * FishingGlobals.fleeVelocityMultiplier * dt + accel[0] * dt * dt
        newZ = self.getZ() + velocity[2] * FishingGlobals.fleeVelocityMultiplier * dt + accel[2] * dt * dt
        return (
         newX, newZ)

    def performErraticBehavior(self, dt, velocity, accel):
        self.erraticDtAccumulator += dt
        self.sineDtAccumulator += dt
        newX = self.getX() + velocity[0] * dt + accel[0] * dt * dt
        newZ = self.myZ + math.sin(self.sineDtAccumulator) * self.myData['behaviorDict']['sineMultiplier']
        if self.erraticDtAccumulator > self.myData['behaviorDict']['secondsBetweenChanges']:
            self.erraticDtAccumulator = 0
            if random.random() < self.myData['behaviorDict']['chanceOfTurning']:
                if self.fsm.getCurrentOrNextState() != 'TurnAround':
                    self.fsm.request('TurnAround', 'Swimming', not self.movingRight)
        return (
         newX, newZ)

    def showAttractionCollisionVisuals(self):
        if FishingGlobals.wantDebugCollisionVisuals:
            self.attractionVisual.show()

    def hideAttractionCollisionVisuals(self):
        if FishingGlobals.wantDebugCollisionVisuals:
            self.attractionVisual.hide()

    def showAvoidanceCollisionVisuals(self):
        if FishingGlobals.wantDebugCollisionVisuals:
            self.collisionVisual.show()

    def hideAvoidanceCollisionVisuals(self):
        if FishingGlobals.wantDebugCollisionVisuals:
            self.collisionVisual.hide()