from pandac.PandaModules import *
import DistributedPostInvasionObject
from pirates.effects.Fire import Fire
from pirates.effects.MansionSmoke import MansionSmoke

class DistributedWreckedFaithfulBride(DistributedPostInvasionObject.DistributedPostInvasionObject):
    notify = directNotify.newCategory('DistributedWreckedFaithfulBride')

    def __init__(self, cr):
        DistributedPostInvasionObject.DistributedPostInvasionObject.__init__(self, cr)
        self.fire_one = None
        self.smoke_one = None
        return

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

    def startBurning(self):
        if not self.postInvasionObjs:
            return
        parent = self.postInvasionObjs[0].getParent()
        builder = self.getParentObj().builder
        uid = parent.getNetTag('uid')
        visZone = parent.getNetTag('visZone')
        effectList = []
        if not self.fire_one:
            self.fire_one = Fire.getEffect(1)
        if self.fire_one:
            self.fire_one.reparentTo(parent)
            self.fire_one.setPos(6, -4, 15)
            self.fire_one.setEffectScale(1.1)
            self.fire_one.setTag('uid', uid)
            self.fire_one.setTag('visZone', visZone)
            builder.registerEffect(self.fire_one)
            effectList.append(self.fire_one)
        if not self.smoke_one:
            self.smoke_one = MansionSmoke.getEffect(1)
        if self.smoke_one:
            self.smoke_one.reparentTo(parent)
            self.smoke_one.setPos(6, -6, 24)
            self.smoke_one.setEffectScale(0.5)
            self.smoke_one.setTag('uid', uid)
            self.smoke_one.setTag('visZone', visZone)
            builder.registerEffect(self.smoke_one)
            effectList.append(self.smoke_one)
        builder.validateEffectSet(set(effectList))

    def stopBurning(self):
        builder = self.getParentObj().builder
        if self.fire_one:
            builder.unregisterEffect(self.fire_one)
            self.fire_one = None
        if self.smoke_one:
            builder.unregisterEffect(self.smoke_one)
            self.smoke_one = None
        return