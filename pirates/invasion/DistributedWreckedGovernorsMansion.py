from pandac.PandaModules import *
import DistributedPostInvasionObject
from pirates.effects.Fire import Fire
from pirates.effects.MansionSmoke import MansionSmoke

class DistributedWreckedGovernorsMansion(DistributedPostInvasionObject.DistributedPostInvasionObject):
    notify = directNotify.newCategory('DistributedWreckedGovernorsMansion')

    def __init__(self, cr):
        DistributedPostInvasionObject.DistributedPostInvasionObject.__init__(self, cr)
        self.fire_one = None
        self.fire_two = None
        self.fire_three = None
        self.smoke_one = None
        self.smoke_two = None
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
            self.fire_one.setPos(-62, -15, 28)
            self.fire_one.setEffectScale(0.75)
            self.fire_one.setTag('uid', uid)
            self.fire_one.setTag('visZone', visZone)
            builder.registerEffect(self.fire_one)
            effectList.append(self.fire_one)
        if not self.fire_two:
            self.fire_two = Fire.getEffect(1)
        if self.fire_two:
            self.fire_two.reparentTo(parent)
            self.fire_two.setPos(-40, -15, 28)
            self.fire_two.setEffectScale(0.75)
            self.fire_two.setTag('uid', uid)
            self.fire_two.setTag('visZone', visZone)
            builder.registerEffect(self.fire_two)
            effectList.append(self.fire_two)
        if not self.fire_three:
            self.fire_three = Fire.getEffect(1)
        if self.fire_three:
            self.fire_three.reparentTo(parent)
            self.fire_three.setPos(60, -6, 35)
            self.fire_three.setEffectScale(1.5)
            self.fire_three.setTag('uid', uid)
            self.fire_three.setTag('visZone', visZone)
            builder.registerEffect(self.fire_three)
            effectList.append(self.fire_three)
        if not self.smoke_one:
            self.smoke_one = MansionSmoke.getEffect(1)
        if self.smoke_one:
            self.smoke_one.reparentTo(parent)
            self.smoke_one.setPos(-51, -4, 30)
            self.smoke_one.setEffectScale(1.0)
            self.smoke_one.setTag('uid', uid)
            self.smoke_one.setTag('visZone', visZone)
            builder.registerEffect(self.smoke_one)
            effectList.append(self.smoke_one)
        if not self.smoke_two:
            self.smoke_two = MansionSmoke.getEffect(1)
        if self.smoke_one:
            self.smoke_two.reparentTo(parent)
            self.smoke_two.setPos(58, -4, 36)
            self.smoke_two.setEffectScale(1.0)
            self.smoke_two.setTag('uid', uid)
            self.smoke_two.setTag('visZone', visZone)
            builder.registerEffect(self.smoke_two)
            effectList.append(self.smoke_two)
        builder.validateEffectSet(set(effectList))

    def stopBurning(self):
        builder = self.getParentObj().builder
        if self.fire_one:
            builder.unregisterEffect(self.fire_one)
            self.fire_one = None
        if self.fire_two:
            builder.unregisterEffect(self.fire_two)
            self.fire_two = None
        if self.fire_three:
            builder.unregisterEffect(self.fire_three)
            self.fire_three = None
        if self.smoke_one:
            builder.unregisterEffect(self.smoke_one)
            self.smoke_one = None
        if self.smoke_two:
            builder.unregisterEffect(self.smoke_two)
            self.smoke_two = None
        return