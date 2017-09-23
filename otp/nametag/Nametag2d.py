from otp.nametag.Nametag import Nametag
from otp.nametag import NametagGlobals

class Nametag2d(Nametag):
    IS_3D = False

    def getSpeechBalloon(self):
        return NametagGlobals.speechBalloon2d

    def getThoughtBalloon(self):
        return NametagGlobals.thoughtBalloon2d
