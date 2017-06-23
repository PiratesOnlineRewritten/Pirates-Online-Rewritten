import copy
import random
import math
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence, Wait, Func
from pandac.PandaModules import NodePath
from pandac.PandaModules import Fog, FogAttrib, Shader
from pandac.PandaModules import Texture
from pandac.PandaModules import Vec4
from direct.directnotify import DirectNotifyGlobal
import FishingGlobals
from Fish import Fish
from LegendaryFish import LegendaryFish

class FishManager():
    notify = DirectNotifyGlobal.directNotify.newCategory('FishManager')

    def __init__(self, gameObject=None):
        base.loadingScreen.beginStep('FishManager', 2, 20)
        self.gameObject = gameObject
        if self.gameObject.distributedFishingSpot.onABoat:
            self.location = 'ship'
        else:
            self.location = 'dock'
        self.uncaughtFish = []
        self.caughtFish = 0
        self.deadFish = []
        self.activeFish = None
        self.specialFishIndex = 0
        self.fishHistogram = {}
        for fish in FishingGlobals.allFishData:
            self.fishHistogram[fish['id']] = [0, fish['maxPossiblePerScene']]

        self.hiddenFish = []
        self.legendaryFishPool = []
        self.hideNormalFishSequence = Sequence()
        self.objectsWithCaustics = NodePath('objectsWithCaustics')
        self.objectsWithCaustics.reparentTo(self.gameObject.fishingSpot)
        self.causticsTexture = loader.loadTexture('maps/pir_t_gam_fsh_caustics.jpg')
        self.causticsShader = loader.loadShader('models/shaders/fishingCausticsShader.sha')
        if base.win and base.win.getGsg():
            intShaders = base.win.getGsg().getSupportsBasicShaders()
        else:
            intShaders = 0
        if intShaders > 0:
            self.doShaders()
        else:
            self.doFixedFunction()
        if base.win and base.win.getGsg():
            shaderModel = base.win.getGsg().getShaderModel()
        base.loadingScreen.tick()
        self.loadFish()
        base.loadingScreen.endStep('FishManager')
        return

    def loadFish(self):
        rodSize = self.gameObject.getAvatarsBestRod()
        for depth in range(len(FishingGlobals.fishCountRangePerRodPerLevel[rodSize])):
            numberOfFishForThisLevel = random.randint(FishingGlobals.fishCountRangePerRodPerLevel[rodSize][depth][0], FishingGlobals.fishCountRangePerRodPerLevel[rodSize][depth][1])
            for fishIndex in range(numberOfFishForThisLevel):
                fishData = FishingGlobals.giveMeAFish(self.location, depth, self.fishHistogram)
                f = Fish(self, fishData, len(self.uncaughtFish))
                self.fishHistogram[f.myData['id']][0] += 1
                f.fsm.request('Offscreen')
                self.uncaughtFish.append(f)

            self.legendaryFish = None

        return

    def doShaders(self):
        self.objectsWithCaustics.setShader(self.causticsShader)
        self.objectsWithCaustics.setShaderInput('caustics', self.causticsTexture)
        self.objectsWithCaustics.setShaderInput('causticsParams', Vec4(5.33, 0.0234325112498, 0.010589092533, 0.2))
        self.objectsWithCaustics.setShaderInput('causticsParams2', Vec4(2.879531, -0.03568613, 0.0275891, 0.2))
        self.objectsWithCaustics.setShaderInput('causticsParams3', Vec4(3.7854611, 0.03703703, 0.047619047619047616, 0.2))
        self.objectsWithCaustics.setShaderInput('fogInfo', Vec4(0.0, FishingGlobals.fogDarkness, 0.7, 0.0))
        self.objectsWithCaustics.setShaderInput('fogColor', FishingGlobals.waterFogColor)
        self.objectsWithCaustics.setShaderInput('causticsToWorldScale', Vec4(1.0 / 30.1, 1.0 / 30.1, 0.0, 0.0))
        self.objectsWithCaustics.setShaderInput('sunWorldLocation', Vec4(0.0, 0.0, 100.0, 1.0))

    def doFixedFunction(self):
        fishFog = Fog('fishFogNode')
        fishFog.setMode(Fog.MLinear)
        fishFog.setColor(FishingGlobals.waterFogColor)
        fishFog.setLinearRange(0.0, 200.0)
        fishFogAttrib = FogAttrib.make(fishFog)
        self.objectsWithCaustics.setAttrib(fishFogAttrib)

    def codeReload(self):
        for fish in self.uncaughtFish:
            print fish.codeReload()

    def scareAwayNormalFish(self):
        for fish in self.uncaughtFish:
            if fish.fsm.getCurrentOrNextState() != 'ScareAway':
                if fish.movingRight and fish.fsm.getCurrentOrNextState() != 'TurnAround':
                    fish.fsm.request('TurnAround', 'ScareAway', False)
                else:
                    fish.fsm.request('ScareAway')

    def startLegendaryFish(self, whichFish=None):
        self.notify.debug('start LegendaryFish %s' % str(whichFish))
        fishData = FishingGlobals.getALegendaryFish(whichFish)
        self.legendaryFish = LegendaryFish(self, fishData, 0)
        self.activeFish = self.legendaryFish
        self.legendaryFish.fsm.request('AboutToBiteLure')

    def replaceFish(self, fish):
        depth = fish.myData['depth']
        index = fish.index
        self.fishHistogram[fish.myData['id']][0] -= 1
        self.uncaughtFish.remove(fish)
        fish.destroy()
        fishData = FishingGlobals.giveMeAFish(self.location, depth, self.fishHistogram)
        f = Fish(self, fishData, index)
        f.fsm.request('Offscreen')
        self.fishHistogram[f.myData['id']][0] += 1
        f.pickPositionAndSwim()
        self.uncaughtFish.append(f)

    def destroy(self):
        for fish in self.uncaughtFish:
            fish.destroy()

        self.uncaughtFish = []
        if self.legendaryFish:
            self.legendaryFish.destroy()
        self.legendaryFish = None
        return

    def moveFish(self, direction):
        self.shutdown()
        self.specialFishIndex += direction
        self.specialFishIndex = max(min(len(FishingGlobals.allFishData) - 1, self.specialFishIndex), 0)
        self.startup()

    def startup(self):
        for fish in self.uncaughtFish:
            fish.pickPositionAndSwim()

    def shutdown(self):
        self.activeFish = None
        self.caughtFish = 0
        self.deadFish = []
        for fish in self.uncaughtFish:
            if fish.fsm.getCurrentOrNextState() != 'Offscreen':
                fish.fsm.request('Offscreen')

        return

    def reset(self):
        if self.activeFish and self.activeFish.fsm and self.activeFish.fsm.getCurrentOrNextState() != 'Offscreen':
            self.activeFish.fsm.request('Offscreen')
        self.activeFish = None
        self.deadFish = []
        self.loseInterest()
        return

    def update(self, dt):
        lurePos = self.gameObject.lure.getPos()
        for i in range(len(self.uncaughtFish)):
            self.uncaughtFish[i].update(dt, i, lurePos)

        for fish in self.deadFish:
            self.uncaughtFish.remove(fish)
            fish.destroy()

        self.deadFish = []

    def turnAllFish(self):
        for fish in self.uncaughtFish:
            if fish.fsm.getCurrentOrNextState() != 'TurnAround':
                fish.fsm.request('TurnAround', 'Swimming', not fish.movingRight)

    def enterReeling(self):
        pass

    def reloadCollisions(self):
        if FishingGlobals.wantDebugCollisionVisuals:
            for fish in self.uncaughtFish:
                for fishData in FishingGlobals.allFishData:
                    if fish.myData['model'] == fishData['model']:
                        fish.myData = fishData
                        fish.reloadCollisions()
                        continue

    def loseInterest(self):
        for fish in self.uncaughtFish:
            if fish.fsm.getCurrentOrNextState() == 'Biting':
                fish.fsm.request('Swimming')

    def showAvoidanceCollisionVisuals(self):
        if FishingGlobals.wantDebugCollisionVisuals:
            for fish in self.uncaughtFish:
                fish.showAvoidanceCollisionVisuals()

    def hideAvoidanceCollisionVisuals(self):
        if FishingGlobals.wantDebugCollisionVisuals:
            for fish in self.uncaughtFish:
                fish.hideAvoidanceCollisionVisuals()

    def showAttractionCollisionVisuals(self):
        if FishingGlobals.wantDebugCollisionVisuals:
            for fish in self.uncaughtFish:
                fish.showAttractionCollisionVisuals()

    def hideAttractionCollisionVisuals(self):
        if FishingGlobals.wantDebugCollisionVisuals:
            for fish in self.uncaughtFish:
                fish.hideAttractionCollisionVisuals()