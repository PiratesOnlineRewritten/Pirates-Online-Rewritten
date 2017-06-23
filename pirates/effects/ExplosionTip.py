from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class ExplosionTip(PooledEffect, EffectController):
    NUM_PARTS = 10

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.size = 4.0
        self.speed = 0.8
        self.speedSpread = 0.4
        self.parts = []
        for i in range(self.NUM_PARTS):
            explosion = loader.loadModel('models/effects/dirt_trail')
            explosion.setDepthWrite(0)
            explosion.reparentTo(self)
            explosion.hide()
            self.parts.append(explosion)

    def createTrack(self):
        subTracks = Parallel()
        for i in range(len(self.parts)):
            self.parts[i].setScale(1.0)
            self.parts[i].setColorScale(1, 1, 1, 1)
            self.parts[i].setPos(0, 0, 0)
            self.parts[i].setHpr(i * (360 / self.NUM_PARTS), 15, 0)
            speed = self.speed + random.uniform(0.0, self.speedSpread)
            fadeBlast = self.parts[i].colorScaleInterval(speed * 0.5, Vec4(0, 0, 0, 0))
            waitFade = Sequence(Wait(speed), fadeBlast)
            scaleBlast = self.parts[i].scaleInterval(speed, self.size, blendType='easeIn')
            moveBlast = self.parts[i].posInterval(speed, Vec3(1, 0, 4), startPos=Vec3(0, 0, 0), blendType='easeOut', other=self.parts[i])
            subTracks.append(Parallel(scaleBlast, moveBlast, waitFade))

        self.track = Sequence(Func(self.showAll), subTracks, Func(self.hideAll), Func(self.cleanUpEffect))

    def hideAll(self):
        for part in self.parts:
            part.hide()

    def showAll(self):
        for part in self.parts:
            part.show()

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        if self.card:
            self.card.removeNode()
            self.card = None
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        return