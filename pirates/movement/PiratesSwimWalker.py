from direct.showbase.InputStateGlobal import inputState
from direct.controls.SwimWalker import SwimWalker
from pandac.PandaModules import *
from direct.task.Task import Task

class PiratesSwimWalker(SwimWalker):

    def handleAvatarControls(self, task):
        if not self.lifter.hasContact():
            messenger.send('walkerIsOutOfWorld', [self.avatarNodePath])
        forward = inputState.isSet('forward')
        reverse = inputState.isSet('reverse')
        turnLeft = inputState.isSet('turnLeft') or inputState.isSet('slideLeft')
        turnRight = inputState.isSet('turnRight') or inputState.isSet('slideRight')
        slideLeft = inputState.isSet('slideLeft')
        slideRight = inputState.isSet('slideRight')
        if base.localAvatar.getAutoRun():
            forward = 1
            reverse = 0
        self.speed = forward and self.avatarControlForwardSpeed or reverse and -self.avatarControlReverseSpeed
        self.slideSpeed = reverse and slideLeft and -self.avatarControlReverseSpeed * 0.75 or reverse and slideRight and self.avatarControlReverseSpeed * 0.75 or slideLeft and -self.avatarControlForwardSpeed * 0.75 or slideRight and self.avatarControlForwardSpeed * 0.75
        self.rotationSpeed = not (slideLeft or slideRight) and (turnLeft and self.avatarControlRotateSpeed or turnRight and -self.avatarControlRotateSpeed)
        if self.wantDebugIndicator:
            self.displayDebugInfo()
        dt = ClockObject.getGlobalClock().getDt()
        self.moving = self.speed or self.slideSpeed or self.rotationSpeed
        if self.moving:
            if self.stopThisFrame:
                distance = 0.0
                slideDistance = 0.0
                rotation = 0.0
                self.stopThisFrame = 0
            else:
                distance = dt * self.speed
                slideDistance = dt * self.slideSpeed
                rotation = dt * self.rotationSpeed
            self.vel = Vec3(Vec3.forward() * distance + Vec3.right() * slideDistance)
            if self.vel != Vec3.zero():
                rotMat = Mat3.rotateMatNormaxis(self.avatarNodePath.getH(), Vec3.up())
                step = rotMat.xform(self.vel)
                self.avatarNodePath.setFluidPos(Point3(self.avatarNodePath.getPos() + step))
            self.avatarNodePath.setH(self.avatarNodePath.getH() + rotation)
            messenger.send('avatarMoving')
        else:
            self.vel.set(0.0, 0.0, 0.0)
        return task.cont