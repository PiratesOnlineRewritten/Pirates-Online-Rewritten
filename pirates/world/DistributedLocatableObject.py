from direct.distributed.DistributedObject import DistributedObject
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals

class DistributedLocatableObject(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

    def locationChange(self, locationName):
        displayName = PLocalizer.LocationNames.get(locationName)
        if displayName:
            self.guiMgr.createTitle(displayName, PiratesGuiGlobals.TextFG2)
            localAvatar.guiMgr.radarGui.showLocation(locationName)