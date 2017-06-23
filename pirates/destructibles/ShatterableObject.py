from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase.PiratesGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.effects.ProjectileArc import ProjectileArc
import random

class ShatterableObject(DirectObject):

    def __init__(self):
        self.resetPos = []
        self.resetHpr = []
        self.resetScale = []
        self.intervals = []
        self.prop = None
        self.numBreaks = 0
        self.debrisA = None
        self.debrisB = None
        self.hasDestructionSequence = 0
        return

    def disable(self):
        for i in self.intervals:
            i.pause()
            del i

    def delete(self):
        del self.resetPos
        del self.resetHpr
        del self.resetScale
        del self.debrisA
        del self.debrisB
        del self.intervals

    def initializeDebris(self, wantHidden=0, wantRotate=1, wantColl=0, bounce=0):
        self.wantHidden = wantHidden
        self.wantRotate = wantRotate
        self.wantColl = wantColl
        self.findDebris()
        self.debrisA = self.break1High
        self.debrisB = self.break2High
        self.numBreaks = len(self.debrisA)
        for i in range(len(self.break1High)):
            pos = self.break1High[i].getPos(self.getDebrisParent())
            self.resetPos.append(pos)
            hpr = self.break1High[i].getHpr(self.getDebrisParent())
            self.resetHpr.append(hpr)
            scale = self.break1High[i].getScale(self.getDebrisParent())
            self.resetScale.append(scale)

        for i in range(len(self.break2High)):
            pos = self.break2High[i].getPos(self.getDebrisParent())
            self.resetPos.append(pos)
            hpr = self.break2High[i].getHpr(self.getDebrisParent())
            self.resetHpr.append(hpr)
            scale = self.break2High[i].getScale(self.getDebrisParent())
            self.resetScale.append(scale)

        self.resetDebris()

    def resetDebris(self):
        self.findDebris()
        for i in range(len(self.debrisA)):
            self.debrisA[i].setPos(self.getDebrisParent(), self.resetPos[i])
            self.debrisA[i].setHpr(self.getDebrisParent(), self.resetHpr[i])
            self.debrisA[i].setScale(self.getDebrisParent(), self.resetScale[i])
            self.debrisA[i].show()

        for i in range(len(self.debrisB)):
            self.debrisB[i].setPos(self.getDebrisParent(), self.resetPos[i + len(self.debrisA)])
            self.debrisB[i].setHpr(self.getDebrisParent(), self.resetHpr[i + len(self.debrisA)])
            self.debrisB[i].setScale(self.getDebrisParent(), self.resetScale[i + len(self.debrisA)])
            self.debrisB[i].show()

        if self.wantHidden:
            for i in self.break1High:
                i.stash()

            for i in self.break2High:
                i.stash()

    def findDebris(self):
        self.break1High = self.prop.findAllMatches('**/debrisA*')
        self.break2High = self.prop.findAllMatches('**/debrisB*')
        self.break1Med = None
        self.break2Med = None
        self.break1Low = None
        self.break2Low = None
        return

    def getDebrisParent(self):
        return self.prop

    def getZOffsetParent(self):
        return render

    def breakMe(self, debrisNode):
        projDummy = ProjectileArc(self.wantRotate, self.wantColl)
        projDummy.reparentTo(self.prop)
        projDummy.startVel = Vec3(random.uniform(-60, 60), random.uniform(-60, 60), random.uniform(30, 100))
        projDummy.gravityMult = 4.0
        projDummy.rotateMin = 30
        projDummy.rotateMax = 200
        debrisParent = self.getDebrisParent()
        if self.wantHidden:
            debrisNode.unstash()
        projDummy.setPos(debrisNode.getPos(self.prop))
        projDummy.setScale(debrisNode.getScale(self.prop))
        debrisNode.reparentTo(projDummy.rotateNode)
        debrisNode.setPos(0, 0, 0)
        debrisNode.setHpr(0, 0, 0)
        projDummy.startPos = projDummy.transNode.getPos(self.prop)
        shatterSeq = Sequence(Func(projDummy.play), Wait(10.0), Func(debrisNode.reparentTo, debrisParent), Func(debrisNode.hide))
        self.intervals.append(shatterSeq)
        shatterSeq.start()

    def playBreak(self):
        if self.prop and self.isAlive:
            for i in range(len(self.break1High)):
                if self.break1High[i] != None:
                    self.breakMe(self.break1High[i])
                    if self.break1Med:
                        if len(self.break1Med) > i:
                            self.break1Med[i].hide()
                    if self.break1Low:
                        if len(self.break1Low) > i:
                            self.break1Low[i].hide()
                    self.break1High[i] = None
                    if self.break1Med:
                        if len(self.break1Med) > i:
                            self.break1Med[i] = None
                    if self.break1Low:
                        if len(self.break1Low) > i:
                            self.break1Low[i] = None
                    return

        return

    def playBreakAll(self):
        for i in range(len(self.break1High)):
            if self.break1High[i] != None:
                self.breakMe(self.break1High[i])
                if self.break1Med:
                    if len(self.break1Med) > i:
                        self.break1Med[i].hide()
                if self.break1Low:
                    if len(self.break1Low) > i:
                        self.break1Low[i].hide()
                self.break1High[i] = None
                if self.break1Med:
                    if len(self.break1Med) > i:
                        self.break1Med[i] = None
                if self.break1Low:
                    if len(self.break1Low) > i:
                        self.break1Low[i] = None

        for i in range(len(self.break2High)):
            self.breakMe(self.break2High[i])
            if self.break2Med:
                if len(self.break2Med) > i:
                    self.break2Med[i].hide()
            if self.break2Low:
                if len(self.break2Low) > i:
                    self.break2Low[i].hide()

        return

    def hideBreak(self):
        if self.prop and self.isAlive:
            for i in range(len(self.break1High)):
                if self.break1High[i] != None:
                    self.break1High[i].hide()
                    self.break1High[i] = None
                if self.break1Med[i] != None:
                    self.break1Med[i].hide()
                    self.break1Med[i] = None
                if self.break1Low[i] != None:
                    self.break1Low[i].hide()
                    self.break1Low[i] = None
                    return

        return

    def hideBreakAll(self):
        for i in range(len(self.break1High)):
            if self.break1High[i] != None:
                self.break1High[i].hide()
                self.break1High[i] = None
            if self.break1Med[i] != None:
                self.break1Med[i].hide()
                self.break1Med[i] = None
            if self.break1Low[i] != None:
                self.break1Low[i].hide()
                self.break1Low[i] = None

        for i in range(len(self.break2High)):
            self.break2High[i].hide()
            if self.break2Med[i] != None:
                self.break2Med[i].hide()
            if self.break2Low[i] != None:
                self.break2Low[i].hide()

        return