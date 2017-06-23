from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.task import Task
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
from otp.otpbase import OTPGlobals
from pirates.pirate import AvatarTypes
from pirates.creature import Creature
from pirates.piratesbase import PiratesGlobals
import pickle
import random
import math
import os
TWO_PI = math.pi * 2.0
GrassProfiles = {'models/islands/bilgewater_zero': 'bilgewaterGrass.dat','models/props/bilgewater_gameArea_test': 'bilgewaterGrass.dat','models/jungles/jungle_b': 'jungle_b_grass.dat'}

def HasGrass(modelPath):
    return GrassProfiles.get(modelPath)


class Grass(DirectObject, NodePath):

    def __init__(self, parent):
        NodePath.__init__(self, 'grass')
        self.parent = parent
        self.__grassDataFile = GrassProfiles.get(self.parent.modelPath)
        self.numClumps = 40
        self.clumps = []
        self.lastAvCell = None
        self.nearbySamples = None
        self.setupClumps()
        self.readGrassSamples()
        try:
            todMgr = base.cr.timeOfDayManager
        except:
            todMgr = None

        if todMgr:
            self.setLightOff()
            self.setLight(todMgr.grassLight)
            self.setLight(todMgr.alight)
        return

    def destroy(self):
        print 'deleting grass'
        self.stop()
        self.detachNode()
        del self.clumps

    def createActor(self):
        models = [
         (
          loader.loadModel('models/vegetation/Grass_huge_zero'), 'models/vegetation/Grass_huge_idle', 1.0)]
        ga = Actor.Actor()
        model, anim, scale = random.choice(models)
        ga.loadModel(model)
        ga.setScale(1, 1, 1.0 + 0.75 * random.random())
        ga.loadAnims({'idle': anim})
        ga.reparentTo(self)
        ga.setPlayRate(random.random(), 'idle')
        ga.loop('idle')
        return ga

    def setupClumps(self, actor=1):
        grassPath = 'models/vegetation/Grass_zero'
        if actor:
            for i in xrange(self.numClumps):
                ga = self.createActor()
                self.clumps.append(ga)

        else:
            for i in xrange(self.numClumps):
                clump = loader.loadModel('models/misc/smiley')
                clump.setScale(1.0 + random.random())
                clump.reparentTo(self)
                clump.hide()
                self.clumps.append(clump)

        self.setTwoSided(1)

    def getAvailableClump(self):
        if len(self.clumps) > 0:
            clump = self.clumps.pop()
            clump.loop('idle')
            return clump
        return None

    def getNumClumpsAvailable(self):
        return len(self.clumps)

    def returnClumpToPool(self, clump):
        clump.stop()
        clump.hide()
        self.clumps.append(clump)

    def start(self):
        self.unstash()
        taskMgr.add(self.grassTask, 'grassSwayTask')

    def stop(self):
        taskMgr.remove('grassSwayTask')
        self.stash()

    def avatarMoving(self):
        self.avatarMoving = 1

    def readGrassSamples(self):
        filename = self.__grassDataFile
        spfSearchPath = DSearchPath()
        spfSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$PIRATES/src/effects')))
        spfSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('pirates/src/effects')))
        spfSearchPath.appendDirectory(Filename('.'))
        pfile = Filename(filename)
        if vfs:
            found = vfs.resolveFilename(pfile, spfSearchPath)
        else:
            found = pfile.resolveFilename(spfSearchPath)
        dataFile = open(pfile.toOsSpecific(), 'r')
        grassSamples = pickle.load(dataFile)
        dataFile.close()
        self._numDivX, self._numDivY, self._dx, self._dy, self._minX, self._minY, self._grassDensity, self.sampleDict = grassSamples
        print self._numDivX, self._numDivY, self._dx, self._dy, self._minX, self._minY
        self.radius = math.sqrt(self.numClumps / math.pi / self._grassDensity)
        print 'radius = %s' % self.radius

    def getAvatarCell(self):
        avPos = localAvatar.getPos(self.parent)
        row = int(avPos[0] - self._minX) / self._dx
        col = int(avPos[1] - self._minY) / self._dx
        index = int(col * self._numDivX + row)
        return (
         index, row, col)

    def placeAllClumps(self):
        for sampleIndex in self.sampleDict.keys()[0:20]:
            samples = self.sampleDict.get(sampleIndex, [])
            for sample in samples:
                samplePos = Vec3(sample[1], sample[2], sample[3])
                sampleNormal = Vec3(sample[4], sample[5], sample[6])
                clump = self.createActor()
                clump.setPos(samplePos)
                clump.headsUp(Point3(samplePos), sampleNormal)
                clump.reparentTo(self)
                clump.setColorScale(sample[7], sample[8], sample[9], 1)
                self.clumps.append(clump)

    def getNearbySamples(self, row, col):
        samples = []
        radius = 2
        gridOffsets = xrange(-radius, radius + 1)
        for di in gridOffsets:
            for dj in gridOffsets:
                i = row + di
                j = col + dj
                cellIndex = int(j * self._numDivX + i)
                if cellIndex >= 0 and cellIndex < self._numDivX * self._numDivY:
                    cellSamples = self.sampleDict.get(cellIndex)
                    if cellSamples:
                        samples.append(cellIndex)

        for index in self.sampleDict:
            if index not in samples:
                cellSamples = self.sampleDict.get(index, [])
                for sample in cellSamples:
                    if sample[0] != 0:
                        self.returnClumpToPool(sample[0])
                        sample[0] = 0

        return samples

    def placeClumpsInRadius(self):
        numSaved = 0
        avPos = localAvatar.getPos(self.parent)
        avCell, row, col = self.getAvatarCell()
        if avCell != self.lastAvCell:
            self.lastAvCell = avCell
            self.nearbySamples = self.getNearbySamples(row, col)
        for sampleIndex in self.nearbySamples:
            samples = self.sampleDict.get(sampleIndex, [])
            for sample in samples:
                samplePos = Vec3(sample[1], sample[2], sample[3])
                sampleNormal = Vec3(sample[4], sample[5], sample[6])
                dist = (samplePos - avPos).length()
                if dist < self.radius:
                    sp = camera.getRelativePoint(self.parent, samplePos)
                    if sp[0] + sp[1] > 0:
                        if sp[0] - sp[1] < 0:
                            if sample[0] == 0:
                                clump = self.getAvailableClump()
                                if clump:
                                    clump.setPos(samplePos)
                                    clump.headsUp(Point3(samplePos), sampleNormal)
                                    k = 1.5
                                    clump.setColorScale(k * sample[7], k * sample[8], k * sample[9], 1)
                                    clump.show()
                                    sample[0] = clump
                            else:
                                numSaved += 1
                        elif sample[0] != 0:
                            self.returnClumpToPool(sample[0])
                            sample[0] = 0
                    elif sample[0] != 0:
                        self.returnClumpToPool(sample[0])
                        sample[0] = 0

    def grassTask(self, task):
        avMoving = 0
        if hasattr(localAvatar.controlManager.currentControls, 'moving'):
            avMoving = localAvatar.controlManager.currentControls.moving
        if self.lastAvCell == None or avMoving:
            self.placeClumpsInRadius()
        return Task.cont

    def moveGrass(self):
        t = globalClock.getFrameTime()
        for i in xrange(self.numClumps):
            clump = self.clumps[i]
            hiFreq = 1.0 * math.sin(math.pi * i * t)
            lowFreq = 3.0 * math.sin(0.1 * math.pi * t) + 3.0
            p = hiFreq + lowFreq
            clump.setP(p)
