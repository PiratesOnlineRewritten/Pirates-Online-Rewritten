from pandac.PandaModules import *
from direct.task import Task
from pirates.piratesbase import PiratesGlobals
from pirates.effects.WaterRipple2 import WaterRipple2
from pirates.effects.TentacleWaterDrips import TentacleWaterDrips
from pirates.effects.TentacleFire import TentacleFire

class TentacleUtils():

    def __init__(self):
        self.statusTable = []
        self.effectsScale = 1.0
        self.isUndead = True
        self.undeadSmoke = None
        self.setNameVisible(0)
        return

    def initStatusTable(self):
        self.statusTable = []
        if self.hasLOD():
            root = self.find('**/+LODNode').getChild(0)
        else:
            root = self
        joints = root.findAllMatches('**/def_tent*')
        jointList = [ (x.getName(), x) for x in joints ]
        jointList.sort()
        for i in range(len(joints) - 1):
            self.statusTable.append([jointList[i][1], jointList[i + 1][1], 0, Vec3(0, 0, 0), [None, None, None, None]])

        return

    def setEffectsScale(self, scale):
        self.effectsScale = scale

    def updateStatusTable(self):
        return
        for i in range(len(self.statusTable)):
            tempWaterPos = self.getWaterPos(self.statusTable[i][0], self.statusTable[i][1])
            self.statusTable[i][3] = tempWaterPos
            joint1Z = self.statusTable[i][0].getZ(render)
            joint2Z = self.statusTable[i][1].getZ(render)
            if joint1Z > 0 and joint2Z > 0:
                if self.statusTable[i][2] != 1:
                    self.stopRippleEffect(i)
                    self.statusTable[i][2] = 1
            elif joint1Z > 0 and joint2Z <= 0 or joint1Z <= 0 and joint2Z > 0:
                if self.statusTable[i][2] != 0:
                    self.startRippleEffect(i)
                    if i % 2.0 == 0:
                        self.startWaterDripEffect(i)
                    self.statusTable[i][2] = 0
            elif self.statusTable[i][2] != -1:
                self.stopAllEffects(i)
                self.statusTable[i][2] = -1

    def getWaterPos(self, aboveJoint, belowJoint):
        avgPos = (aboveJoint.getPos(render) + belowJoint.getPos(render)) / 2.0
        return Vec3(avgPos[0], avgPos[1], 0)

    def startRippleEffect(self, section):
        if not self.statusTable[section][4][0]:
            self.statusTable[section][4][0] = WaterRipple2.getEffect()
            if self.statusTable[section][4][0]:
                self.statusTable[section][4][0].reparentTo(self)
                self.statusTable[section][4][0].setEffectScale(self.effectsScale)
                self.statusTable[section][4][0].startLoop()

    def stopRippleEffect(self, section):
        if self.statusTable[section][4][0]:
            self.statusTable[section][4][0].stopLoop()
            self.statusTable[section][4][0] = None
        return

    def startWaterDripEffect(self, section):
        if not self.statusTable[section][4][1]:
            self.statusTable[section][4][1] = TentacleWaterDrips.getEffect()
            if self.statusTable[section][4][1]:
                length = self.statusTable[section][0].getDistance(self.statusTable[section][1])
                self.statusTable[section][4][1].reparentTo(self.statusTable[section][1])
                self.statusTable[section][4][1].setEffectScale(self.effectsScale)
                self.statusTable[section][4][1].setEffectLength(length + 6 * self.effectsScale)
                self.statusTable[section][4][1].play()

    def stopWaterDripEffect(self, section):
        if self.statusTable[section][4][1]:
            self.statusTable[section][4][1].stop()
            self.statusTable[section][4][1] = None
        return

    def startFireEffect(self, section):
        if not self.statusTable[section][4][2]:
            self.statusTable[section][4][2] = TentacleFire.getEffect()
            if self.statusTable[section][4][2]:
                length = self.statusTable[section][0].getDistance(self.statusTable[section][1])
                self.statusTable[section][4][2].reparentTo(self.statusTable[section][1])
                self.statusTable[section][4][2].setEffectScale(self.effectsScale)
                self.statusTable[section][4][2].setEffectLength(length)
                self.statusTable[section][4][2].startLoop()

    def stopFireEffect(self, section):
        if self.statusTable[section][4][2]:
            self.statusTable[section][4][2].stopLoop()
            self.statusTable[section][4][2] = None
        return

    def startUndeadSmoke(self):
        if not self.undeadSmoke:
            self.undeadSmoke = UndeadSmoke.getEffect()
            if self.undeadSmoke:
                self.undeadSmoke.reparentTo(self)
                self.undeadSmoke.setEffectScale(self.effectsScale)
                self.undeadSmoke.startLoop()

    def stopUndeadSmoke(self):
        if self.undeadSmoke:
            self.undeadSmoke.stopLoop()
            self.undeadSmoke = None
        return

    def stopAllEffects(self, section):
        self.stopRippleEffect(section)
        self.stopWaterDripEffect(section)
        self.stopFireEffect(section)

    def removeEffects(self):
        self.stopUndeadSmoke()
        for i in range(len(self.statusTable)):
            self.stopAllEffects(i)

    def updateEffects(self):
        for i in range(len(self.statusTable)):
            if self.statusTable[i][4][0]:
                self.statusTable[i][4][0].setPos(render, self.statusTable[i][3])
                self.statusTable[i][4][0].particleDummy.setZ(render, self.statusTable[i][3][2] + 2.0)

        if self.undeadSmoke:
            self.undeadSmoke.setPos(render, self.statusTable[len(self.statusTable) - 1][3])
            self.undeadSmoke.particleDummy.setZ(render, self.statusTable[len(self.statusTable) - 1][3][2] + 2.0)

    def startUpdateTask(self):
        taskMgr.add(self.updateTask, self.uniqueName('updateTask'))

    def stopUpdateTask(self):
        taskMgr.remove(self.uniqueName('updateTask'))

    def updateTask(self, task):
        return task.cont

    def uniqueName(self, str):
        pass