from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import Task
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.battle import WeaponGlobals
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.battle import CannonGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.uberdog import UberDogGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.reputation import ReputationGlobals
from pirates.piratesgui import CombatTray
from pirates.piratesgui.ReputationMeter import ReputationMeter
from pirates.inventory import ItemGlobals

class WeaponPanel(DirectFrame):
    width = PiratesGuiGlobals.InventoryInfoWidth
    height = PiratesGuiGlobals.InventoryInfoHeight
    guiLoaded = False
    topGui = None
    genericButton = None
    weaponIcons = None
    skillIcons = None
    kbButton = None
    MeterFrame = None

    def __init__(self, data, key, **kw):
        self.data = data
        self.key = key
        self.loadGui()
        DirectFrame.__init__(self, parent=NodePath())
        self.initialiseoptions(WeaponPanel)
        self.createGui()

    def destroyGui(self):
        pass

    def loadGui(self):
        if WeaponPanel.guiLoaded:
            return
        WeaponPanel.topGui = loader.loadModel('models/gui/toplevel_gui')
        WeaponPanel.genericButton = (WeaponPanel.topGui.find('**/generic_button'), WeaponPanel.topGui.find('**/generic_button_down'), WeaponPanel.topGui.find('**/generic_button_over'), WeaponPanel.topGui.find('**/generic_button_disabled'))
        WeaponPanel.weaponIcons = loader.loadModel('models/gui/gui_icons_weapon')
        WeaponPanel.skillIcons = loader.loadModel('models/textureCards/skillIcons')
        WeaponPanel.kbButton = WeaponPanel.topGui.find('**/keyboard_button')
        WeaponPanel.MeterFrame = loader.loadModel('models/gui/ship_battle')
        WeaponPanel.guiLoaded = True

    def createGui(self):
        itemId = self.data[0]
        item, quantity = self.data
        name = ItemGlobals.getName(item)
        itemType = ItemGlobals.getType(item)
        itemTypeName = name
        repCategory = ItemGlobals.getItemRepId(itemId)
        if quantity:
            repValue = localAvatar.getInventory().getReputation(repCategory)
            self.repMeter = ReputationMeter(repCategory, width=0.66)
            self.repMeter.setPos(0.62, 0, 0.041)
            self.repMeter.update(repValue)
            self.repMeter.reparentTo(self)
            self.repMeter.flattenLight()
            hotkeyLabel = ''
            hotkeys = ()
            desc = PLocalizer.WeaponDescriptions.get(itemId)
            helpText = PLocalizer.InventoryTypeNames[repCategory]
            self.weaponButton = CombatTray.WeaponButton(hotkeys=hotkeys, hotkeyLabel=hotkeyLabel, helpOpaque=True, helpText=helpText, parent=self, showQuant=0, pos=(0.1, 0, -0.02), scale=1.1)
            self.weaponButton.ignoreHotkeys()
            self.weaponButton.setWeaponId(itemId)
            self.weaponButton['extraArgs'] = [itemId]
            self.weaponButton.helpDelay = 0
            self.weaponButton.helpPos = (0.12, 0, -0.04)
            self.desc = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=PLocalizer.WeaponAlreadyUnlocked, text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.29, 0, -0.005), text_font=PiratesGlobals.getInterfaceFont())
        else:
            self.repMeter = None
            name = PLocalizer.makeHeadingString(PLocalizer.InventoryTypeNames[repCategory], 2)
            self.categoryLabel = DirectLabel(parent=self, relief=None, text=name, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.29,
                                                                                                                                                                                                         0,
                                                                                                                                                                                                         0.06), textMayChange=0)
            self.weaponButton = CombatTray.WeaponButton(parent=self, state=DGG.DISABLED, showQuant=0, scale=1.1)
            self.weaponButton.setPos(0.1, 0, -0.02)
            self.weaponButton.setWeaponId(itemId)
            self.weaponButton.helpDelay = 0
            self.weaponButton.helpPos = (0.12, 0, -0.04)
            unlockDesc = PLocalizer.WeaponUnlockText[repCategory]
            self.desc = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=unlockDesc, text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.29,
                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                             0.025), text_font=PiratesGlobals.getInterfaceFont())
            self.setColorScale(0.4, 0.4, 0.4, 1, 1)
        return

    def destroy(self):
        taskMgr.remove('helpInfoTask')
        taskMgr.remove(self.taskName('dragTask'))
        DirectFrame.destroy(self)

    def getData(self):
        return self.data

    def bringToFront(self):
        self.reparentTo(self.getParent())