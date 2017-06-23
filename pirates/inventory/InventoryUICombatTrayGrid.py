from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pirates.inventory import InventoryUISlotDisplayGrid
from pirates.inventory.InventoryGlobals import Locations
weaponSlots = range(Locations.RANGE_EQUIP_WEAPONS[0] - 1, Locations.RANGE_EQUIP_WEAPONS[1])
NUMGRIDS = len(weaponSlots)
GRID_POSITIONS = {}
REG_WIDTH = 0.09
BIG_WIDTH = 0.115
REG_SCALE = 0.65
BIG_SCALE = 1.0
REG_Z = 0.0455
BIG_Z = 0.07
TOTALWIDTH = (NUMGRIDS - 1) * REG_WIDTH + BIG_WIDTH
START_X = 0.475 - TOTALWIDTH
for slotIdOuter in weaponSlots:
    runningX = START_X
    slotPostionDict = {}
    for slotId in weaponSlots:
        scale = REG_SCALE
        zPos = REG_Z
        width = REG_WIDTH
        if slotIdOuter == slotId:
            scale = BIG_SCALE
            zPos = BIG_Z
            width = BIG_WIDTH
            runningX += BIG_WIDTH - REG_WIDTH
        positionList = [
         (
          runningX, 0, zPos), scale]
        slotPostionDict[slotId] = positionList
        runningX += width

    GRID_POSITIONS[slotIdOuter] = slotPostionDict

class InventoryUICombatTrayGrid(InventoryUISlotDisplayGrid.InventoryUISlotDisplayGrid):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, countX=4, countZ=4, slotList=[]):
        InventoryUISlotDisplayGrid.InventoryUISlotDisplayGrid.__init__(self, manager, sizeX, sizeZ, countX, countZ, slotList)
        self.initialiseoptions(InventoryUICombatTrayGrid)
        self['relief'] = None
        self.lerpCellIvals = []
        self.changeGrid(0)
        return

    def destroy(self):
        self.clearIvals()
        InventoryUISlotDisplayGrid.InventoryUISlotDisplayGrid.destroy(self)

    def clearIvals(self):
        for lerpCellIval in self.lerpCellIvals:
            lerpCellIval.pause()
            lerpCellIval = None

        self.lerpCellIvals = []
        return

    def setupCellImage(self):
        gui = loader.loadModel('models/gui/gui_icons_weapon')
        self.cellImage = (gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox'))
        self.imageScale = 1.0
        self.imagePos = (0.0, 0.0, 0.0)
        self.relief = DGG.FLAT

    def makeCellBacking(self, cellPos):
        pass

    def changeGrid(self, gridSquare):
        self.clearIvals()
        if not GRID_POSITIONS.get(gridSquare):
            return
        for i in range(0, len(self.cellList)):
            cellPosIval = LerpPosInterval(self.cellList[i], 0.5, GRID_POSITIONS[gridSquare][i][0])
            cellPosIval.start()
            self.lerpCellIvals.append(cellPosIval)
            cellScaleIval = LerpScaleInterval(self.cellList[i], 0.5, GRID_POSITIONS[gridSquare][i][1])
            cellScaleIval.start()
            self.lerpCellIvals.append(cellScaleIval)