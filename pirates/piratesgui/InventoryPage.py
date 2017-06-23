from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.uberdog import InventoryRequestBase

class InventoryPage(DirectFrame, InventoryRequestBase.InventoryRequestBase):

    def __init__(self):
        DirectFrame.__init__(self, parent=NodePath(), relief=None, state=DGG.DISABLED, frameColor=PiratesGuiGlobals.FrameColor, borderWidth=PiratesGuiGlobals.BorderWidth, frameSize=(0.0, PiratesGuiGlobals.InventoryPageWidth, 0.0, PiratesGuiGlobals.InventoryPageHeight), pos=(-0.54, 0, -0.72))
        InventoryRequestBase.InventoryRequestBase.__init__(self)
        self.initialiseoptions(InventoryPage)
        return

    def show(self):
        DirectFrame.show(self)

    def hide(self):
        DirectFrame.hide(self)

    def slideOpenCallback(self):
        pass

    def slideCloseCallback(self):
        pass

    def slideOpenPrecall(self):
        pass