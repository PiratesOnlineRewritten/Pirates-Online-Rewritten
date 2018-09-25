from direct.interval.IntervalGlobal import LerpColorInterval, Sequence

from otp.nametag.ClickablePopup import *
from otp.nametag.NametagConstants import *


class Nametag(ClickablePopup):
    CName = 1
    CSpeech = 2
    CThought = 4

    def __init__(self, wordwrap):
        ClickablePopup.__init__(self)

        self.avatar = None
        self.ival = None
        self.popup_region = None
        self.seq = 0
        self.mouse_watcher = None
        self.draw_order = 0
        self.has_draw_order = False

        self.contents = CFSpeech | CFThought | CFQuicktalker
        self.active = True
        self.field_12 = 0
        self.group = None
        self.wordwrap = wordwrap
        self.has_region = False
        self.ival_name = 'flash-%d' % id(self)

    def clearAvatar(self):
        self.avatar = None

    def clearDrawOrder(self):
        self.has_draw_order = False
        self.updateContents()

    def click(self):
        if self.group:
            self.group.click()

    def deactivate(self):
        if self.has_region:
            if self.mouse_watcher:
                self.mouse_watcher.removeRegion(self.popup_region)
                self.mouse_watcher = None

            self.has_region = None

        self.seq = 0

    def determineContents(self):
        if self.group and self.group.isManaged():
            v3 = self.contents & self.group.getContents()
            v4 = self.group.chat_flags

            if v4 & CFSpeech:
                if v3 & Nametag.CSpeech:
                    return Nametag.CSpeech

            elif v4 & CFThought and v3 & Nametag.CThought:
                return Nametag.CThought

            if v3 & Nametag.CName and self.group.getName() and NametagGlobals._master_nametags_visible:
                return Nametag.CName

        return 0

    def displayAsActive(self):
        if not self.active:
            return 0

        if self.group:
            return self.group.displayAsActive()

        else:
            return NametagGlobals._master_nametags_active

    def setAvatar(self, avatar):
        self.avatar = avatar

    def getAvatar(self):
        return self.avatar

    def setChatWordwrap(self, wordwrap):
        self.wordwrap = wordwrap

    def getChatWordwrap(self):
        return self.wordwrap

    def getGroup(self):
        return self.group

    def getState(self):
        if self.group:
            if not (self.active and self.group.displayAsActive()):
                return PGButton.SInactive

        elif not (self.active and NametagGlobals._master_nametags_active):
            return PGButton.SInactive

        return self._state

    def hasGroup(self):
        return self.group is not None

    def setActive(self, active):
        self.active = active
        self.updateContents()

    def isActive(self):
        return self.active

    def isGroupManaged(self):
        return self.group and self.group.isManaged()

    def keepRegion(self):
        if self.popup_region:
            self.seq = self.group.getRegionSeq()

    def manage(self, manager):
        self.updateContents()

    def unmanage(self, manager):
        self.updateContents()
        self.deactivate()

    def setContents(self, contents):
        self.contents = contents
        self.updateContents()

    def setDrawOrder(self, draw_order):
        self.draw_order = draw_order
        self.has_draw_order = True
        self.updateContents()

    def setRegion(self, frame, sort):
        if self.popup_region:
            self.popup_region.setFrame(frame)

        else:
            self.popup_region = self._createRegion(frame)

        self.popup_region.setSort(int(sort))
        self.seq = self.group.getRegionSeq()

    def startFlash(self, np):
        if self.ival:
            self.ival.finish()
            self.ival = None

        self.ival = Sequence(LerpColorInterval(np, 0.5, (1, 1, 1, 0.5), (1, 1, 1, 1), blendType='easeOut'),
                               LerpColorInterval(np, 0.5, (1, 1, 1, 1), (1, 1, 1, 0.5), blendType='easeIn'))
        self.ival.loop()

    def stopFlash(self):
        if self.ival:
            self.ival.finish()
            self.ival = None

    def updateRegion(self, seq):
        if seq == self.seq:
            is_active = self.displayAsActive()

        else:
            is_active = False

        if self.has_region:
            if self.mouse_watcher != NametagGlobals._mouse_watcher:
                if self.mouse_watcher:
                    self.mouse_watcher.removeRegion(self.popup_region)

                self.has_region = False
                self.setState(PGButton.SReady)

        if is_active:
            if (not self.has_region) and self.popup_region:
                if self.mouse_watcher != NametagGlobals._mouse_watcher:
                    self.mouse_watcher = NametagGlobals._mouse_watcher

                if self.mouse_watcher:
                    self.mouse_watcher.addRegion(self.popup_region)

                self.has_region = True

        elif self.has_region:
            if self.mouse_watcher and self.popup_region:
                self.mouse_watcher.removeRegion(self.popup_region)

            self.has_region = False
            self.mouse_watcher = None
            self.setState(PGButton.SReady)

    def upcastToPandaNode(self):
        return self
