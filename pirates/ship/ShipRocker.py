from direct.showbase.PythonUtil import reduceAngle, pivotScalar, rad90, rad270
import math

class ShipRockerOffState():

    def getRollAngle(self):
        return 0.0

    def getRollVelocity(self):
        return 0.0

    def getRollTarget(self):
        return 0.0


class ShipRockerImpactState():

    def set(self, timebase, duration, startRoll, targetRoll):
        self.timebase = timebase
        self.duration = duration
        self.startRoll = startRoll
        self.targetRoll = targetRoll

    def getT(self):
        return globalClock.getFrameTime() - self.timebase

    def isActive(self):
        return self.getT() < self.duration

    def getRollAngle(self):
        theta = rad90 * (self.getT() / self.duration)
        return self.startRoll + (self.targetRoll - self.startRoll) * math.sin(theta)

    def getRollVelocity(self):
        theta = rad90 * (self.getT() / self.duration)
        return math.cos(theta) * (rad90 / self.duration)

    def getRollTarget(self):
        return self.targetRoll


class ShipRockerRollState():

    def set(self, timebase, duration, timeScale, amplitude, thetaBase):
        self.timebase = timebase
        self.duration = duration
        self.timeScale = timeScale
        self.amplitude = amplitude
        self.thetaBase = thetaBase

    def getT(self):
        return globalClock.getFrameTime() - self.timebase

    def isActive(self):
        return self.getT() < self.duration

    def getRollAngle(self):
        t = self.getT()
        theta = self.thetaBase + self.timeScale * t
        return self.amplitude * math.sin(theta) * (1.0 - t / self.duration)

    def getRollVelocity(self):
        t = self.getT()
        theta = self.thetaBase + self.timeScale * t
        return self.amplitude * self.timeScale * math.cos(theta) * (1.0 - t / self.duration)

    def getRollTarget(self):
        target = self.amplitude * (1.0 - self.getT() / self.duration)
        if self.getRollVelocity() < 0.0:
            target = -target
        return target


class ShipRocker():
    DefMaxRoll = 15.0
    DefFakeMass = 1.0

    def __init__(self, maxRoll=None, fakeMass=None):
        self._maxRoll = notNone(maxRoll, ShipRocker.DefMaxRoll)
        self._fakeMass = notNone(fakeMass, ShipRocker.DefFakeMass)
        self._off = ShipRockerOffState()
        self._impact = ShipRockerImpactState()
        self._roll = ShipRockerRollState()
        self.reset()

    def reset(self):
        self._active = False

    def destroy(self):
        del self._off
        del self._impact
        del self._roll

    def getMaxRoll(self):
        return self._maxRoll

    def setMaxRoll(self, maxRoll):
        self._maxRoll = maxRoll

    def setFakeMass(self, fakeMass):
        self._fakeMass = fakeMass

    def _getState(self):
        if not self._active:
            state = self._off
        elif self._impact.isActive():
            state = self._impact
        elif self._roll.isActive():
            state = self._roll
        else:
            self._active = False
            state = self._off
        return state

    def getRollAngle(self):
        return self._getState().getRollAngle()

    def _getRollVelocity(self):
        return self._getState().getRollVelocity()

    def addRoll(self, roll):
        curTime = globalClock.getFrameTime()
        roll /= self._fakeMass
        state = self._getState()
        curRoll = state.getRollAngle()
        curRollTarget = state.getRollTarget()
        newRoll = 0.1 * curRollTarget + roll
        newRoll = clampScalar(newRoll, self._maxRoll, -self._maxRoll)
        impactDur = 0.05 * abs(newRoll - curRoll) * self._fakeMass
        self._impact.set(timebase=curTime, duration=impactDur, startRoll=curRoll, targetRoll=newRoll)
        amplitude = abs(newRoll)
        timeScale = 3.0 / self._fakeMass
        rollDur = amplitude / timeScale / ((self._fakeMass + 1.0) * 0.5)
        if newRoll > 0.0:
            thetaBase = rad90
        else:
            thetaBase = rad270
        self._roll.set(timebase=curTime + impactDur, duration=rollDur, timeScale=timeScale, amplitude=amplitude, thetaBase=thetaBase)
        self._active = True