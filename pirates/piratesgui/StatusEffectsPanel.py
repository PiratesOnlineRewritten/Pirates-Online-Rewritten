from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.battle import WeaponGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import BuffIcon

class StatusEffectsPanel(DirectFrame):

    def __init__(self, parent, **kw):
        DirectFrame.__init__(self, parent, **kw)
        self.initialiseoptions(StatusEffectsPanel)
        self.buffIcons = []
        self.buffs = []
        self.iconScale = 1.0

    def destroy(self):
        for buffIcon in self.buffIcons:
            buffIcon.destroy()

        del self.buffIcons
        del self.buffs
        DirectFrame.destroy(self)

    def addStatusEffect(self, effectId, maxDuration, timeLeft, lastTimestamp, attackerId):
        id = '%s-%s' % (effectId, attackerId)
        myIcon = BuffIcon.BuffIcon(self, effectId, maxDuration, attackerId)
        myIcon.lastTimestamp = lastTimestamp
        myIcon.timeLeft = timeLeft
        myIcon.makeIcons()
        myIcon.setScale(self.iconScale)
        self.buffIcons.append(myIcon)
        self.buffs.append(id)
        for i in range(len(self.buffIcons)):
            self.buffIcons[i].setPos(i * 0.12, 0, 0)

    def removeStatusEffect(self, effectId, attackerId):
        id = '%s-%s' % (effectId, attackerId)
        if id not in self.buffs:
            return
        index = self.buffs.index(id)
        buff = self.buffIcons[index]
        buff.destroy()
        self.buffIcons.remove(buff)
        self.buffs.remove(id)
        for i in range(len(self.buffIcons)):
            self.buffIcons[i].setPos(i * 0.11, 0, 0)

    def updateStatusEffect(self, effectId, maxDuration, timeLeft, lastTimestamp, attackerId):
        id = '%s-%s' % (effectId, attackerId)
        if id in self.buffs:
            index = self.buffs.index(id)
            buff = self.buffIcons[index]
            if buff.effectId == effectId:
                buff.maxDuration = maxDuration
                buff.timeLeft = timeLeft
                buff.lastTimestamp = lastTimestamp

    def updateDurations(self):
        for i in self.buffIcons:
            i.updateIconInfo()