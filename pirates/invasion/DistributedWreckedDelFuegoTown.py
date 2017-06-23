from pandac.PandaModules import *
import DistributedPostInvasionObject
from pirates.effects.Fire import Fire
from pirates.effects.MansionSmoke import MansionSmoke
OBJ_EFFECT_PARAMS = {0: ('1233963904.0akelts', Point3(8, -6, 2.5), 1.0, Point3(8, -6, 7.5), 0.6),1: ('1233964160.0akelts0', Point3(10, -7, 5), 0.75, Point3(10, -10, 6), 0.35),2: ('1234209408.0akelts', Point3(4, -8, 1), 1.1, Point3(4, -8, 4), 0.4),3: ('1233696000.0akelts0', Point3(4, 2, 13), 0.8, Point3(4, 2, 14), 0.4)}

class DistributedWreckedDelFuegoTown(DistributedPostInvasionObject.DistributedPostInvasionObject):
    notify = directNotify.newCategory('DistributedWreckedDelFuegoTown')

    def __init__(self, cr):
        DistributedPostInvasionObject.DistributedPostInvasionObject.__init__(self, cr)
        self.fireEffects = {}
        self.smokeEffects = {}

    def generate(self):
        DistributedPostInvasionObject.DistributedPostInvasionObject.generate(self)
        self.notify.debug('generate')

    def announceGenerate(self):
        DistributedPostInvasionObject.DistributedPostInvasionObject.announceGenerate(self)
        if not self.postInvasionObjs:
            self.postInvasionObjs = self.getParentObj().findAllMatches('**/=Switch Class=Mansion;+s')
            for postInvasionObj in self.postInvasionObjs:
                postInvasionObj.node().setVisibleChild(1)

    def disable(self):
        for postInvasionObj in self.postInvasionObjs:
            postInvasionObj.node().setVisibleChild(0)

        DistributedPostInvasionObject.DistributedPostInvasionObject.disable(self)

    def delete(self):
        DistributedPostInvasionObject.DistributedPostInvasionObject.delete(self)

    def getParentWithId(self, uId):
        for obj in self.postInvasionObjs:
            if obj.getParent().getNetTag('uid') == uId:
                return obj

        return None

    def startBurning(self):
        if not self.postInvasionObjs:
            return
        base.wdf = self
        builder = self.getParentObj().builder
        effectList = []
        for id in OBJ_EFFECT_PARAMS:
            parent = self.getParentWithId(OBJ_EFFECT_PARAMS[id][0])
            uid = parent.getNetTag('uid')
            visZone = parent.getNetTag('visZone')
            if not self.fireEffects.has_key(id):
                self.fireEffects[id] = Fire.getEffect(1)
            if self.fireEffects[id]:
                fireEffect = self.fireEffects[id]
                fireEffect.reparentTo(parent)
                fireEffect.setPos(OBJ_EFFECT_PARAMS[id][1])
                fireEffect.setEffectScale(OBJ_EFFECT_PARAMS[id][2])
                fireEffect.setTag('uid', uid)
                fireEffect.setTag('visZone', visZone)
                builder.registerEffect(fireEffect)
                effectList.append(fireEffect)
            if not self.smokeEffects.has_key(id):
                self.smokeEffects[id] = MansionSmoke.getEffect(1)
            if self.smokeEffects[id]:
                smokeEffect = self.smokeEffects[id]
                smokeEffect.reparentTo(parent)
                smokeEffect.setPos(OBJ_EFFECT_PARAMS[id][3])
                smokeEffect.setEffectScale(OBJ_EFFECT_PARAMS[id][4])
                smokeEffect.setTag('uid', uid)
                smokeEffect.setTag('visZone', visZone)
                builder.registerEffect(smokeEffect)
                effectList.append(smokeEffect)

        if self.fireEffects[2]:
            self.fireEffects[2].p0.emitter.setRadius(3.0)
        if self.fireEffects[3]:
            self.fireEffects[3].p0.emitter.setRadius(2.0)
        builder.validateEffectSet(set(effectList))

    def stopBurning(self):
        builder = self.getParentObj().builder
        for id in self.fireEffects:
            if self.fireEffects[id]:
                builder.unregisterEffect(self.fireEffects[id])

        self.fireEffects = {}
        for id in self.smokeEffects:
            if self.smokeEffects[id]:
                builder.unregisterEffect(self.smokeEffects[id])

        self.smokeEffects = {}