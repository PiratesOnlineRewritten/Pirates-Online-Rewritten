from direct.gui.DirectGui import *
from direct.task import Task
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryPage
from pirates.piratesgui import WeaponPanel
from pirates.piratesgui.SkillButton import SkillButton
from pirates.piratesgui import InventoryItemGui
from pirates.piratesgui import InventoryItemList
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.CombatTray import WeaponButton
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.battle import WeaponGlobals
from pirates.reputation import ReputationGlobals
from pirates.piratesgui.ReputationMeter import ReputationMeter
import copy
from pirates.inventory import ItemGlobals, InventoryGlobals
from GuiButton import GuiButton
TOKEN_LIST = [
 InventoryType.CutlassToken, InventoryType.PistolToken, InventoryType.DollToken, InventoryType.DaggerToken, InventoryType.GrenadeToken, InventoryType.WandToken]

class WeaponPage(InventoryPage.InventoryPage):

    def __init__(self):
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(WeaponPage)
        self.weaponPanels = {}
        self.tonicButtons = {}
        self.fishingIcon = None
        self.potionIcon = None
        self.fishingRepMeter = None
        self.potionRepMeter = None
        self.fishingPoleName = None
        self.fishingChangeMsg = None
        self.needRefresh = 1
        self.showing = 0
        return

    def show(self):
        self.showing = 1
        InventoryPage.InventoryPage.show(self)
        if self.needRefresh:
            self.refreshList()
            self.needRefresh = 0

    def hide(self):
        self.showing = 0
        self.equipStatus = 0
        InventoryPage.InventoryPage.hide(self)

    def tonicCallback(self, skillId):
        localAvatar.guiMgr.combatTray.trySkill(InventoryType.UseItem, skillId, 0)

    def rePanel(self, inventory):
        if not self.showing:
            self.needRefresh = 1
            return
        skillTokens = {InventoryType.CutlassToken: (ItemGlobals.RUSTY_CUTLASS,),InventoryType.PistolToken: (ItemGlobals.FLINTLOCK_PISTOL,),InventoryType.DollToken: (ItemGlobals.VOODOO_DOLL,),InventoryType.DaggerToken: (ItemGlobals.BASIC_DAGGER,),InventoryType.GrenadeToken: (ItemGlobals.GRENADE_POUCH,),InventoryType.WandToken: (ItemGlobals.CURSED_STAFF,)}
        zIndex = 1
        for skillTokenKey in TOKEN_LIST:
            quantity = 0
            if localAvatar.getInventory().stacks.get(skillTokenKey):
                quantity = 1
            skillData = skillTokens[skillTokenKey]
            weaponId = skillData[0]
            key = None
            panel = WeaponPanel.WeaponPanel((weaponId, quantity), key)
            panel.reparentTo(self)
            panel.setZ(PiratesGuiGlobals.InventoryPanelHeight - 0.18 - zIndex * panel.height)
            zIndex += 1
            repCat = WeaponGlobals.getRepId(weaponId)
            self.weaponPanels[repCat] = panel
            self.ignore('inventoryQuantity-%s' % inventory.getDoId())
            self.acceptOnce('inventoryQuantity-%s-%s' % (inventory.getDoId(), skillTokenKey), self.refreshList)

        repIcon_gui = loader.loadModel('models/textureCards/skillIcons')
        repIcon = repIcon_gui.find('**/box_base')
        if config.GetBool('want-fishing-game', 0):
            self.fishingIcon = GuiButton(pos=(0.166, 0, 0.045 + (PiratesGuiGlobals.InventoryPanelHeight - 0.18) - zIndex * panel.height), helpText=PLocalizer.FishingRepDescription, helpOpaque=True, image=(repIcon, repIcon, repIcon, repIcon), image_scale=(0.144,
                                                                                                                                                                                                                                                               0.144,
                                                                                                                                                                                                                                                               0.144))
            fishIconCard = loader.loadModel('models/textureCards/fishing_icons')
            inv = localAvatar.getInventory()
            fishingChangeMsg = InventoryGlobals.getCategoryQuantChangeMsg(inv.doId, InventoryType.FishingRod)
            if self.fishingChangeMsg:
                self.ignore(fishingChangeMsg)
            self.fishingChangeMsg = fishingChangeMsg
            self.acceptOnce(fishingChangeMsg, self.refreshList)
            rodIcons = [
             'pir_t_gui_fsh_smRodIcon', 'pir_t_gui_fsh_mdRodIcon', 'pir_t_gui_fsh_lgRodIcon']
            rodLvl = inv.getStackQuantity(InventoryType.FishingRod)
            rodIcon = rodIcons[rodLvl - 1]
            rodText = PLocalizer.FishingRodNames[rodLvl]
            if rodLvl >= 1:
                self.fishingIcon['geom'] = fishIconCard.find('**/' + rodIcon)
            self.fishingIcon['geom_scale'] = 0.1
            self.fishingIcon['geom_pos'] = (0, 0, 0)
            self.fishingIcon.reparentTo(self)
            fishingRepValue = localAvatar.getInventory().getReputation(InventoryType.FishingRep)
            self.fishingRepMeter = ReputationMeter(InventoryType.FishingRep, width=0.66)
            self.fishingRepMeter.setPos(0.62, 0, 0.041 + (PiratesGuiGlobals.InventoryPanelHeight - 0.18) - zIndex * panel.height)
            self.fishingRepMeter.update(fishingRepValue)
            self.fishingRepMeter.reparentTo(self)
            self.fishingRepMeter.flattenLight()
            self.fishingPoleName = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=rodText, text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.29, 0, -0.005 + (PiratesGuiGlobals.InventoryPanelHeight - 0.18) - 7 * panel.height), text_font=PiratesGlobals.getInterfaceFont())
            self.fishingPoleName.reparentTo(self)
            zIndex += 1
        iconCard = loader.loadModel('models/textureCards/skillIcons')
        if config.GetBool('want-potion-game', 0):
            self.potionIcon = GuiButton(pos=(0.166, 0, 0.045 + (PiratesGuiGlobals.InventoryPanelHeight - 0.18) - zIndex * panel.height), helpText=PLocalizer.PotionRepDescription, helpOpaque=True, image=(repIcon, repIcon, repIcon, repIcon), image_scale=(0.144,
                                                                                                                                                                                                                                                             0.144,
                                                                                                                                                                                                                                                             0.144))
            self.potionIcon['geom'] = iconCard.find('**/pir_t_gui_pot_base')
            self.potionIcon['geom_scale'] = 0.1
            self.potionIcon['geom_pos'] = (0, 0, 0)
            self.potionIcon.reparentTo(self)
            potionRepValue = localAvatar.getInventory().getReputation(InventoryType.PotionsRep)
            self.potionRepMeter = ReputationMeter(InventoryType.PotionsRep, width=0.66)
            self.potionRepMeter.setPos(0.62, 0, 0.041 + (PiratesGuiGlobals.InventoryPanelHeight - 0.18) - zIndex * panel.height)
            self.potionRepMeter.update(potionRepValue)
            self.potionRepMeter.reparentTo(self)
            self.potionRepMeter.flattenLight()
            zIndex += 1
        items = dict(map(lambda x: (x.getType(), x.getCount()), inventory.getConsumables().values()))
        possibleItems = ItemGlobals.getAllHealthIds()
        havePorky = items.get(ItemGlobals.ROAST_PORK)
        if not havePorky and ItemGlobals.ROAST_PORK in possibleItems:
            possibleItems.remove(ItemGlobals.ROAST_PORK)
        offset = 0
        if base.config.GetBool('want-potion-game', 0):
            items = inventory.getConsumables()
            listLength = len(InventoryType.PotionMinigamePotions)
            count = 0
            for i in range(listLength):
                tonicId = InventoryType.PotionMinigamePotions[i]
                if items.get(tonicId):
                    button = SkillButton(tonicId, self.tonicCallback, items.get(tonicId), showQuantity=True, showHelp=True, showRing=True)
                    button.skillButton['geom_scale'] = 0.08
                    x = 0.16 * (count % 6) + -1.2
                    z = 1.0 - int(count / 6) * 0.16
                    button.setPos(x, 0, z)
                    button.reparentTo(self)
                    self.tonicButtons[tonicId] = button
                    count += 1

        return

    def refreshList(self, newWeaponId=None):
        for panel in self.weaponPanels.values():
            panel.destroy()

        for panel in self.tonicButtons.values():
            panel.destroy()

        if self.fishingIcon is not None:
            self.fishingIcon.destroy()
        if self.potionIcon is not None:
            self.potionIcon.destroy()
        if self.fishingRepMeter is not None:
            self.fishingRepMeter.destroy()
        if self.potionRepMeter is not None:
            self.potionRepMeter.destroy()
        if self.fishingPoleName is not None:
            self.fishingPoleName.destroy()
        inventory = localAvatar.getInventory()
        if inventory:
            if inventory.isReady():
                self.rePanel(inventory)
            else:
                self.ignore('inventoryReady-%s' % inventory.getDoId())
                self.acceptOnce('inventoryReady-%s' % inventory.getDoId(), self.rePanel)
        return

    def destroy(self):
        if self.fishingChangeMsg:
            self.ignore(self.fishingChangeMsg)
        InventoryPage.InventoryPage.destroy(self)

    def updateTonics(self):
        if not hasattr(base, 'localAvatar'):
            return
        inv = localAvatar.getInventory()
        if not inv:
            return
        possibleTonics = ItemGlobals.getAllHealthIds()
        for tonicId in possibleTonics:
            tonicAmt = inv.getItemQuantity(InventoryType.ItemTypeConsumable, tonicId)
            if self.tonicButtons.has_key(tonicId):
                self.tonicButtons[tonicId].updateQuantity(tonicAmt)
                self.tonicButtons[tonicId].checkAmount()