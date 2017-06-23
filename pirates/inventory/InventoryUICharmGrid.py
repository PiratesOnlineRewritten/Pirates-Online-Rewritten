from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pirates.inventory import InventoryUISlotDisplayGrid
from pirates.piratesbase import PLocalizer
GRID_POSITIONS = {0: {0: [(0.105, 0, 0.07), 1.0],1: [(0.22, 0, 0.0455), 0.65],2: [(0.31, 0, 0.0455), 0.65],3: [(0.4, 0, 0.0455), 0.65]}}

class InventoryUICharmGrid(InventoryUISlotDisplayGrid.InventoryUISlotDisplayGrid):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, countX=1, countZ=1, slotList=[]):
        InventoryUISlotDisplayGrid.InventoryUISlotDisplayGrid.__init__(self, manager, sizeX, sizeZ, countX, countZ, slotList)
        self.initialiseoptions(InventoryUICharmGrid)
        self['relief'] = None
        self.relabelCell()
        return

    def destroy(self):
        self.clearIvals()
        InventoryUISlotDisplayGrid.InventoryUISlotDisplayGrid.destroy(self)

    def relabelCell(self):
        for cell in self.cellList:
            cell.labelText = PLocalizer.InventoryPageItemSlot
            cell.label['text'] = cell.labelText

    def clearIvals(self):
        pass

    def setupCellImage(self):
        gui = loader.loadModel('models/gui/gui_icons_weapon')
        self.cellImage = (gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox'))
        self.imageScale = 1.0
        self.imagePos = (0.0, 0.0, 0.0)
        self.relief = DGG.FLAT

    def makeCellBacking(self, cellPos):
        pass

    def changeGrid(self, gridSquare):
        pass