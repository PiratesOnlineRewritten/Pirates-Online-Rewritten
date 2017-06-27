from panda3d.core import *
from otp.nametag import NametagGlobals
from otp.nametag.Nametag2d import Nametag2d
from otp.nametag.Nametag3d import Nametag3d

class NametagGroup(object):
    CCNormal = NametagGlobals.CCNormal
    CCNoChat = NametagGlobals.CCNoChat
    CCNonPlayer = NametagGlobals.CCNonPlayer
    CCSuit = NametagGlobals.CCSuit
    CCToonBuilding = NametagGlobals.CCToonBuilding
    CCSuitBuilding = NametagGlobals.CCSuitBuilding
    CCHouseBuilding = NametagGlobals.CCHouseBuilding
    CCSpeedChat = NametagGlobals.CCSpeedChat
    CCFreeChat = NametagGlobals.CCFreeChat

    def __init__(self):
        self.avatar = None
        self.font = None
        self.name = ''
        self.displayName = ''
        self.colorCode = 0
        self.active = False
        self.contents = 0
        self.nameIcon = NodePath('icon')
        self.nameWordwrap = 0

        self.nametag2d = Nametag2d()
        self.nametag3d = Nametag3d()
        self.nametags = []

    def getNametag2d(self):
        return self.nametag2d

    def getNametag3d(self):
        return self.nametag3d

    def hasNametag(self, nametag):
        return nametag in self.nametags

    def addNametag(self, nametag):
        if self.hasNametag(nametag):
            return

        self.nametags.append(nametag)

    def removeNametag(self, nametag):
        if not self.hasNametag(nametag):
            return

        self.nametags.remove(nametag)

    def manage(self, manager):
        pass

    def unmanage(self, manager):
        pass

    def getUniqueId(self):
        return 'NametagGroup-%s' % id(self)

    def setAvatar(self, avatar):
        self.avatar = avatar

    def getAvatar(self):
        return self.avatar

    def setFont(self, font):
        self.font = font

    def getFont(self):
        return self.font

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setDisplayName(self, displayName):
        self.displayName = displayName

    def getDisplayName(self):
        return self.displayName

    def setColorCode(self, colorCode):
        self.colorCode = colorCode

    def getColorCode(self):
        return self.colorCode

    def setActive(self, active):
        self.active = active

    def getActive(self):
        return self.active

    def setContents(self, contents):
        self.contents = contents

    def getContents(self):
        return self.contents

    def getNameIcon(self):
        return self.nameIcon

    def setNameWordwrap(self, nameWordwrap):
        self.nameWordwrap = nameWordwrap

    def getNameWordwrap(self):
        return self.nameWordwrap
