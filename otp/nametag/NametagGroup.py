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
        self.icon = NodePath('icon')
        self.nameWordwrap = 0

        self.nametag2d = Nametag2d()
        self.nametag3d = Nametag3d()

        self.nametags = []
        self.nametags.extend([self.nametag2d, self.nametag3d])

        self.tickTask = taskMgr.add(self.__tick, self.getUniqueId(), sort=45)

    def getUniqueId(self):
        return 'NametagGroup-%s' % id(self)

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

    def setAvatar(self, avatar):
        self.avatar = avatar
        self.updateTags()

    def getAvatar(self):
        return self.avatar

    def setFont(self, font):
        self.font = font
        self.updateTags()

    def getFont(self):
        return self.font

    def setName(self, name):
        self.name = name
        self.updateTags()

    def getName(self):
        return self.name

    def setDisplayName(self, displayName):
        self.displayName = displayName
        self.updateTags()

    def getDisplayName(self):
        return self.displayName

    def setColorCode(self, colorCode):
        self.colorCode = colorCode
        self.updateTags()

    def getColorCode(self):
        return self.colorCode

    def setActive(self, active):
        self.active = active
        self.updateTags()

    def getActive(self):
        return self.active

    def setContents(self, contents):
        self.contents = contents
        self.updateTags()

    def getContents(self):
        return self.contents

    def getNameIcon(self):
        return self.icon

    def setNameWordwrap(self, nameWordwrap):
        self.nameWordwrap = nameWordwrap
        self.updateTags()

    def getNameWordwrap(self):
        return self.nameWordwrap

    def __tick(self, task):
        for nametag in self.nametags:
            nametag.tick()

        return task.cont

    def updateTags(self):
        for nametag in self.nametags:
            self.updateTag(nametag)

    def updateTag(self, nametag):
        nametag.avatar = self.avatar
        nametag.font = self.font
        nametag.name = self.name
        nametag.displayName = self.displayName
        nametag.icon = self.icon
        #nametag.contents = self.contents
        nametag.update()
