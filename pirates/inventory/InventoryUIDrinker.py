from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUIContainer
from pirates.inventory.InventoryUIGlobals import *
from pirates.battle import WeaponGlobals
from pirates.inventory import ItemGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

class InventoryUIDrinker(InventoryUIContainer.InventoryUIContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0):
        InventoryUIContainer.InventoryUIContainer.__init__(self, manager, sizeX, sizeZ)
        self.containerType = CONTAINER_DRINKER
        self.initialiseoptions(InventoryUIDrinker)
        self.heldItemOldCell = None
        self.waitTime = None
        return

    def setup(self):
        gui = loader.loadModel('models/textureCards/skillIcons')
        cell = self.makeCell(self.cellImage)
        geomImage = (gui.find('**/pir_t_ico_pot_elixir'), gui.find('**/pir_t_ico_pot_elixir'), gui.find('**/pir_t_ico_pot_elixir'), gui.find('**/pir_t_ico_pot_elixir'))
        cell['geom'] = geomImage
        cell['geom_scale'] = 0.13
        cell['text'] = PLocalizer.DrinkPotion
        cell['text_pos'] = (0.0, -0.025)
        self.drinkCell = cell

    def destroy(self):
        self.ignoreAll()
        InventoryUIContainer.InventoryUIContainer.destroy(self)
        taskMgr.remove('WaitDrinkPotion')
        self.drinkCell = None
        return

    def canDrag(self):
        return 0

    def cellUsed(self, cell):
        if self.manager.heldFromCell:
            self.heldItemOldCell = self.manager.heldFromCell
            if self.manager.testCanUse(self.heldItemOldCell.inventoryItem.itemTuple):
                itemId = self.heldItemOldCell.inventoryItem.itemTuple.getType()
                skillId = WeaponGlobals.getSkillIdForAmmoSkillId(itemId)
                if WeaponGlobals.getSkillEffectFlag(skillId):
                    drunk = localAvatar.guiMgr.combatTray.trySkill(InventoryType.UsePotion, skillId, 0)
                else:
                    drunk = localAvatar.guiMgr.combatTray.trySkill(InventoryType.UseItem, skillId, 0)
                if self.waitTime == None and drunk:
                    if WeaponGlobals.getSkillEffectFlag(skillId):
                        self.waitTime = base.cr.battleMgr.getModifiedRechargeTime(localAvatar, InventoryType.UsePotion, skillId)
                    else:
                        self.waitTime = base.cr.battleMgr.getModifiedRechargeTime(localAvatar, InventoryType.UseItem, skillId)
                    if self.waitTime:
                        self.drinkCell['text'] = PLocalizer.WaitPotion % int(self.waitTime)
                        taskMgr.doMethodLater(1.0, self.handlePotionRecharge, 'WaitDrinkPotion')
        else:
            localAvatar.guiMgr.createWarning(PLocalizer.HowToDrinkPotion, PiratesGuiGlobals.TextFG6)
        return

    def handlePotionRecharge(self, task):
        self.waitTime -= 1
        self.drinkCell['text'] = PLocalizer.WaitPotion % int(self.waitTime)
        if self.waitTime < 0:
            self.drinkCell['state'] = DGG.NORMAL
            self.drinkCell['text'] = PLocalizer.DrinkPotion
            self.waitTime = None
            return task.done
        else:
            taskMgr.doMethodLater(1.0, self.handlePotionRecharge, 'WaitDrinkPotion')
            return task.done
        return

    def setupCellImage(self):
        gui = loader.loadModel('models/gui/gui_icons_weapon')
        self.gridBacking = gui.find('**/pir_t_gui_frm_inventoryBox')
        self.cellImage = (gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox'))
        self.workingCellImage = (
         gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox'))
        self.focusCellImage = (
         gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox_over'))
        self.imageScale = 1.0
        self.imagePos = (0.0, 0.0, 0.0)
        self.relief = DGG.FLAT