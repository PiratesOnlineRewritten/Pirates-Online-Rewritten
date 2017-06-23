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
from pirates.piratesgui import SkillpageGuiButton
from pirates.piratesgui.SkillRing import SkillRing

class TonicsPanel(DirectFrame):
    width = PiratesGuiGlobals.InventoryInfoWidth
    height = PiratesGuiGlobals.InventoryInfoHeight
    guiLoaded = False
    topGui = None
    weaponIcons = None
    skillIcons = None

    def __init__(self, data, **kw):
        self.skillId, self.amt = data
        self.button = None
        self.loadGui()
        DirectFrame.__init__(self)
        self.initialiseoptions(TonicsPanel)
        self.skillRing = SkillRing(Vec4(1, 0.8, 0.5, 1), Vec4(0, 0, 0, 1.0))
        self.skillRing.reparentTo(self)
        self.skillRing.setPos(0, 0, 0)
        self.setSkillId(self.skillId)
        self.greyOut = 0
        return

    def loadGui(self):
        if TonicsPanel.guiLoaded:
            return
        TonicsPanel.topGui = loader.loadModel('models/gui/toplevel_gui')
        TonicsPanel.weaponIcons = loader.loadModel('models/gui/gui_icons_weapon')
        TonicsPanel.skillIcons = loader.loadModel('models/textureCards/skillIcons')
        TonicsPanel.guiLoaded = True

    def setSkillId(self, skillId):
        self.skillId = skillId
        if self.button:
            self.button.destroy()
        self.button = SkillpageGuiButton.SkillpageGuiButton(self.callback, self.skillId, 0)
        self.button['geom_scale'] = 0.09
        self.button.reparentTo(self)
        self.button.resetFrameSize()
        self.button.attachQuantity(self.amt)

    def destroy(self):
        DirectFrame.destroy(self)

    def callback(self, skillId):
        localAvatar.guiMgr.combatTray.trySkill(InventoryType.UseItem, skillId, 0)

    def updateQuantity(self, amt):
        self.amt = amt
        if self.button:
            self.button.attachQuantity(amt)

    def update(self, task=None):
        inv = localAvatar.getInventory()
        if not inv:
            return Task.cont
        greyOut = 0
        amt = inv.getStackQuantity(self.skillId)
        if amt <= 0:
            greyOut = 1
        if amt != self.amt:
            self.amt = amt
            self.button.attachQuantity(amt)
        range = localAvatar.cr.battleMgr.getModifiedRechargeTime(localAvatar, InventoryType.UseItem)
        value = localAvatar.skillDiary.getTimeSpentRecharging(InventoryType.UseItem)
        if not value:
            value = range
        self.skillRing.update(value, range)
        if value < range:
            greyOut = 3
        if self.greyOut != greyOut:
            self.greyOut = greyOut
            if greyOut == 2:
                self.button['geom_color'] = Vec4(0.5, 0.5, 0.5, 1.0)
            elif greyOut == 1:
                self.button['geom_color'] = Vec4(0.5, 0.5, 0.5, 1.0)
                self.skillRing.meterFaceHalf1.setColorScale(0.4, 0.4, 0.4, 1.0)
                self.skillRing.meterFaceHalf2.setColorScale(0.4, 0.4, 0.4, 1.0)
            elif greyOut == 3:
                self.button['geom_color'] = Vec4(0.5, 0.5, 0.5, 1.0)
            else:
                self.button['geom_color'] = Vec4(1, 1, 1, 1)
                self.skillRing.meterFaceHalf1.setColorScale(1, 1, 1, 1.0)
                self.skillRing.meterFaceHalf2.setColorScale(1, 1, 1, 1.0)
        return Task.cont