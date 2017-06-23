from pirates.piratesbase.PiratesGlobals import *
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from pirates.piratesbase import PiratesGlobals
from direct.distributed import DistributedObject
from pirates.piratesbase import PLocalizer
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.distributed import DistributedNode
from pirates.battle import WeaponGlobals

class DistributedDestructibleObject(DistributedNode.DistributedNode):
    notify = directNotify.newCategory('DistributedDestructibleObject')

    def __init__(self, cr):
        DistributedNode.DistributedNode.__init__(self, cr)
        self.Hp = 0
        self.maxHp = 0
        self.prop = None
        self.isAlive = 1
        self.level = 0
        self.classType = 0
        return

    def generate(self):
        DistributedNode.DistributedNode.generate(self)

    def announceGenerate(self):
        DistributedNode.DistributedNode.announceGenerate(self)

    def disable(self):
        DistributedNode.DistributedNode.disable(self)

    def delete(self):
        if base.cr.config.GetBool('want-ship-hpdisplay', 0) is 1:
            self.destroyHpDisplay()
        self.removeNode()
        DistributedNode.DistributedNode.delete(self)

    def initHpDisplay(self):
        if self.maxHp <= 50:
            pass
        elif base.cr.config.GetBool('want-ship-hpdisplay', 0) is 1:
            self.displayHp()
        if base.cr.config.GetBool('want-ship-hpdisplay', 0) is 1:
            self.updateHpDisplay()

    def displayHp(self):
        self.hasHpMeter = 1
        self.damageDummy = self.attachNewNode('damageDummy')
        self.damageDummy.setBillboardPointEye()
        self.HpDisplay = DirectLabel(text='HP: ' + str(self.Hp) + '/' + str(self.maxHp), scale=2.5, relief=None, text_fg=(1,
                                                                                                                          1,
                                                                                                                          1,
                                                                                                                          1))
        self.HpDisplay.reparentTo(self.damageDummy)
        self.HpDisplay.setBin('fixed', 0)
        self.HpDisplay.setDepthTest(0)
        return

    def updateHpDisplay(self):
        if self.hasHpMeter:
            self.HpDisplay['text'] = 'Hp: ' + str(self.Hp) + '/' + str(self.maxHp)

    def destroyHpDisplay(self):
        if self.hasHpMeter:
            self.HpDisplay.removeNode()
            del self.HpDisplay
            self.damageDummy.removeNode()
            del self.damageDummy

    def setHp(self, newHp):
        deltaHp = int(newHp - self.Hp)
        self.Hp = int(newHp)
        if base.cr.config.GetBool('want-ship-hpdisplay', 0) is 1:
            self.updateHpDisplay()
        if deltaHp > 0:
            if self.Hp == self.maxHp:
                self.respawn()
            elif self.Hp > 0:
                self.restoreDamage()
        elif deltaHp < 0:
            if self.Hp <= 0 and self.Hp - deltaHp > 0:
                self.playDeath()

    def getHp(self):
        return self.Hp

    def setMaxHp(self, newMaxHp):
        self.maxHp = int(newMaxHp)

    def getMaxHp(self):
        return self.maxHp

    def setModelType(self, modelType):
        self.modelType = modelType

    def getModelType(self):
        return self.modelType

    def setPosIndex(self, posIndex):
        self.posIndex = posIndex

    def getPosIndex(self):
        return self.posIndex

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker, itemEffects=[]):
        pass

    def targetedWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, attacker, itemEffects=[]):
        pass

    def playDeath(self):
        pass

    def respawn(self):
        pass

    def restoreDamage(self):
        pass