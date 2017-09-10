from direct.controls.GravityWalker import GravityWalker
from direct.showbase.InputStateGlobal import inputState
from pandac.PandaModules import *
from direct.task.Task import Task

class PiratesGravityWalker(GravityWalker):
    notify = directNotify.newCategory('PiratesGravityWalker')

    def __init__(self, *args, **kwargs):
        GravityWalker.__init__(self, *args, **kwargs)
        self.predicting = 0

    def handleAvatarControls(self, task):
        run = inputState.isSet('run')
        forward = inputState.isSet('forward')
        reverse = inputState.isSet('reverse')
        turnLeft = inputState.isSet('turnLeft')
        turnRight = inputState.isSet('turnRight')
        slideLeft = inputState.isSet('slideLeft')
        slideRight = inputState.isSet('slideRight')
        jump = inputState.isSet('jump')
        if base.localAvatar.getAutoRun():
            forward = 1
            reverse = 0
        self.speed = forward and self.avatarControlForwardSpeed or reverse and -self.avatarControlReverseSpeed
        self.slideSpeed = reverse and slideLeft and -self.avatarControlReverseSpeed * 0.75 or reverse and slideRight and self.avatarControlReverseSpeed * 0.75 or slideLeft and -self.avatarControlForwardSpeed * 0.75 or slideRight and self.avatarControlForwardSpeed * 0.75
        self.rotationSpeed = turnLeft and self.avatarControlRotateSpeed or turnRight and -self.avatarControlRotateSpeed
        if self.speed:
            if self.slideSpeed:
                self.speed *= GravityWalker.DiagonalFactor
                self.slideSpeed *= GravityWalker.DiagonalFactor

        debugRunning = inputState.isSet('debugRunning')
        if debugRunning:
            self.speed *= base.debugRunningMultiplier
            self.slideSpeed *= base.debugRunningMultiplier
            self.rotationSpeed *= 1.25
        if self.needToDeltaPos:
            self.setPriorParentVector()
            self.needToDeltaPos = 0
        if self.wantDebugIndicator:
            self.displayDebugInfo()

        def sendLandMessage(impact):
            if impact > -15.0:
                messenger.send('jumpEnd')
            elif -15.0 >= impact > -40.0:
                messenger.send('jumpLand')
                self.startJumpDelay(0.5)
            else:
                messenger.send('jumpLandHard')
                self.startJumpDelay(0.5)

        def predictHeightAndVelocity(aheadFrames):
            dt = globalClock.getDt()
            vel = self.lifter.getVelocity()
            height = self.getAirborneHeight()
            grav = self.lifter.getGravity()
            dtt = dt * aheadFrames
            futureHeight = height + vel * dtt + 0.5 * grav * dtt * dtt
            futureVel = vel - grav * dtt
            return (
             futureHeight, futureVel)

        if self.lifter.isOnGround():
            if self.isAirborne:
                self.isAirborne = 0
                self.predicting = 0
                impact = self.lifter.getImpactVelocity()
                sendLandMessage(impact)
            self.priorParent = Vec3.zero()
            if jump and self.mayJump:

                def doJump(task):
                    self.lifter.addVelocity(self.avatarControlJumpForce)
                    self.isAirborne = 1
                    self.predicting = 1

                taskMgr.hasTaskNamed('jumpWait') or taskMgr.doMethodLater(0.2, doJump, 'jumpWait')
                messenger.send('jumpStart')
        else:
            if self.isAirborne and self.predicting:
                futureHeight, futureVel = predictHeightAndVelocity(2)
                if futureHeight <= 0.0:
                    self.isAirborne = 0
                    self.predicting = 0
                    sendLandMessage(futureVel)
            elif self.getAirborneHeight() > 2.0:
                self.isAirborne = 1
                self.predicting = 1

        self.__oldPosDelta = self.avatarNodePath.getPosDelta(render)
        self.__oldDt = ClockObject.getGlobalClock().getDt()
        dt = self.__oldDt
        self.moving = self.speed or self.slideSpeed or self.rotationSpeed or self.priorParent != Vec3.zero()
        if self.moving:
            distance = dt * self.speed
            slideDistance = dt * self.slideSpeed
            rotation = dt * self.rotationSpeed
            if distance or slideDistance or self.priorParent != Vec3.zero():
                rotMat = Mat3.rotateMatNormaxis(self.avatarNodePath.getH(), Vec3.up())
                if self.isAirborne:
                    forward = Vec3.forward()
                else:
                    contact = self.lifter.getContactNormal()
                    forward = contact.cross(Vec3.right())
                    forward.normalize()
                self.vel = Vec3(forward * distance)
                if slideDistance:
                    if self.isAirborne:
                        right = Vec3.right()
                    else:
                        right = forward.cross(contact)
                        right.normalize()
                    self.vel = Vec3(self.vel + right * slideDistance)
                self.vel = Vec3(rotMat.xform(self.vel))
                step = self.vel + self.priorParent * dt
                self.avatarNodePath.setFluidPos(Point3(self.avatarNodePath.getPos() + step))
                self.vel /= dt
            self.avatarNodePath.setH(self.avatarNodePath.getH() + rotation)
        else:
            self.vel.set(0.0, 0.0, 0.0)

        if self.moving or jump:
            messenger.send('avatarMoving')

        return task.cont

    def disableJump(self):
        if base.localAvatar.controlManager.forceAvJumpToken is None:
            base.localAvatar.controlManager.disableAvatarJump()
        return

    def enableJump(self):
        if base.localAvatar.controlManager.forceAvJumpToken is not None:
            base.localAvatar.controlManager.enableAvatarJump()
        return

    def abortJump(self):
        taskMgr.remove('jumpWait')

    def reset(self):
        GravityWalker.reset(self)
        self.abortJump()

    def disableAvatarControls(self):
        GravityWalker.disableAvatarControls(self)
        self.abortJump()
