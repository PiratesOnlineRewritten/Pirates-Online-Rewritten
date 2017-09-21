from panda3d.core import BillboardEffect, Vec3, Point3, NodePath
from otp.nametag.Nametag import Nametag
from otp.nametag import NametagGlobals
import math

class Nametag3d(Nametag):
    SCALING_FACTOR = 0.07
    SCALING_MINDIST = 0.1
    SCALING_MAXDIST = 1000

    BILLBOARD_OFFSET = 3.0
    SHOULD_BILLBOARD = True

    def __init__(self):
        Nametag.__init__(self)

        self.contents = self.CName | self.CSpeech | self.CThought
        self.billboardOffset = self.BILLBOARD_OFFSET

        self._doBillboard()

    def _doBillboard(self):
        if self.SHOULD_BILLBOARD:
            self.innerNP.setEffect(BillboardEffect.make(
                Vec3(0, 0, 1),
                True,
                False,
                self.billboardOffset,
                NodePath(), # Empty; look at scene camera
                Point3(0, 0, 0)))
        else:
            self.billboardOffset = 0.0

    def setBillboardOffset(self, billboardOffset):
        self.billboardOffset = billboardOffset
        self._doBillboard()

    def getBillboardOffset(self):
        return self.billboardOffset

    def getSpeechBalloon(self):
        return NametagGlobals.speechBalloon3d

    def getThoughtBalloon(self):
        return NametagGlobals.thoughtBalloon3d

    def tick(self):
        distance = self.innerNP.getPos(NametagGlobals.camera).length()
        distance = max(min(distance, self.SCALING_MAXDIST), self.SCALING_MINDIST)
        scale = math.sqrt(distance) * self.SCALING_FACTOR

        self.innerNP.setScale(scale)
