from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryPage

class ClothingPage(InventoryPage.InventoryPage):

    def __init__(self):
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(ClothingPage)