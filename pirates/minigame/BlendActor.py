from direct.interval.MetaInterval import Sequence
from direct.interval.MetaInterval import Parallel
from direct.interval.IntervalGlobal import Func
from direct.interval.LerpInterval import LerpFunctionInterval
from direct.actor.Actor import Actor

class BlendActor(Actor):
    counter = 0

    def __init__(self, modelName, animDict, defaultBlendTime, blendTimeDict={}):
        Actor.__init__(self, modelName, animDict)
        self.enableBlend()
        self.uniqueCounter = BlendActor.counter
        BlendActor.counter += 1
        self.defaultBlendTime = defaultBlendTime
        self.blendTimeDict = blendTimeDict
        self.blendInterval = None
        self.currentAnimation = None
        self.skeletonAnimationNames = animDict.keys()
        return

    def changeAnimationTo(self, toAnim, loopAnim=True, blend=True):
        self.currentAnimation = toAnim
        if loopAnim:
            self.loop(toAnim)
        else:
            self.play(toAnim)
        mostImportantAnimation = self.getMostImportantAnimationPlayingNow()[0]
        if self.blendTimeDict.has_key('%sTo%s' % (mostImportantAnimation, toAnim)):
            transitionDuration = self.blendTimeDict[toAnim]
        else:
            transitionDuration = self.defaultBlendTime
        if blend:
            self.makeBlendIntervalForBlendingToThisAnimation(toAnim, transitionDuration)
            self.blendInterval.append(Func(self.setExclusive, toAnim))
            self.blendInterval.start()
        else:
            self.clearControlEffectWeights()
            self.adjustEffect(1.0, toAnim)

    def makeBlendIntervalForBlendingToThisAnimation(self, newTransitionAnimation, transitionDuration):
        currentlyPlayingAnimationsAndEffectsAndDesiredEffects = []
        for animationName in self.skeletonAnimationNames:
            if animationName == newTransitionAnimation:
                continue
            controlEffect = self.getControlEffect(animationName)
            if controlEffect > 0.0:
                currentlyPlayingAnimationsAndEffectsAndDesiredEffects.append((animationName, controlEffect, 0.0))

        currentlyPlayingAnimationsAndEffectsAndDesiredEffects.append((newTransitionAnimation, 0.0, 1.0))
        if self.blendInterval:
            self.blendInterval.pause()
            self.blendInterval.clearToInitial()
        self.blendInterval = Sequence(name='%s_%d.blendInterval' % (self.getName(), self.uniqueCounter))
        par = Parallel()
        for animationName, fromData, toData in currentlyPlayingAnimationsAndEffectsAndDesiredEffects:
            par.append(LerpFunctionInterval(self.adjustEffect, duration=transitionDuration, fromData=fromData, toData=toData, extraArgs=[animationName]))

        self.blendInterval.append(par)

    def adjustEffect(self, newEffect, animationName):
        newEffect = min(1.0, newEffect)
        for subPart in self.getPartNames():
            self.setControlEffect(animName=animationName, effect=newEffect, partName=subPart)

    def getControlEffect(self, animationName, partName='modelRoot'):
        part = self.getPart(partName)
        if part:
            bundle = part.node().getBundle(0)
            return bundle.getControlEffect(self.getAnimControl(animationName, partName=partName))
        else:
            return None
        return None

    def setExclusive(self, anim):
        self.clearControlEffectWeights()
        self.adjustEffect(1.0, anim)

    def clearControlEffectWeights(self):
        for animationName in self.skeletonAnimationNames:
            for subPart in self.getPartNames():
                self.setControlEffect(animName=animationName, effect=0.0, partName=subPart)

    def getMostImportantAnimationPlayingNow(self):
        highestEffect = 0.0
        mostImportant = None
        for animationName in self.skeletonAnimationNames:
            controlEffect = self.getControlEffect(animationName)
            if controlEffect is None:
                continue
            if controlEffect > highestEffect:
                highestEffect = controlEffect
                mostImportant = animationName

        return (
         mostImportant, highestEffect)

    def printEffectWeights(self, task=None):
        print '-----'
        print self.getName()
        for animationName in self.skeletonAnimationNames:
            for subPart in self.getPartNames():
                weight = self.getControlEffect(animationName, partName=subPart)
                if weight > 0.0:
                    print '%s\t-\t%s - %.2f ' % (animationName, subPart, weight)

        print '-----'

    def destroy(self):
        if self.blendInterval:
            self.blendInterval.pause()
            self.blendInterval = None
        self.cleanup()
        self.removeNode()
        return