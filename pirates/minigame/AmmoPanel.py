from pandac.PandaModules import *
import math
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import Sequence, PosInterval
from direct.gui.DirectGui import DirectButton, DirectFrame, DGG
from direct.interval.IntervalGlobal import *
from pirates.audio.SoundGlobals import loadSfx
from pirates.audio import SoundGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import Freebooter
from pirates.piratesgui import GuiPanel, GuiButton, RadialMenu
from pirates.minigame import AmmoPanelButton
from pirates.minigame.AmmoPanelMessageManager import AmmoPanelMessageManager
from pirates.minigame import CannonDefenseGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pandac.PandaModules import Point3
CLOSED = 0
OPENED = 1

class AmmoPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('AmmoPanel')

    def __init__(self, cannon):
        DirectFrame.__init__(self, parent=base.a2dLeftCenter, relief=None)
        self.msgMgr = AmmoPanelMessageManager()
        self.cannon = cannon
        self._bankNotes = 0
        self._initVars()
        self._initGUI()
        self._initSfx()
        self._createBankNoteText()
        self.currentLevel = 0
        self.levelUp(1)
        self.usedMagicWord = False
        self.flashIval = None
        for i in range(4):
            self.accept('%d' % (i + 1), self.triggerSkillWithHotkey, [i])

        return

    def _initVars(self):
        self.state = CLOSED
        self.buttons = {}
        self.ammoQuantities = {}
        self.accept('onSellClick', self.removeAmmoSkill)
        self.accept('defenseCannonLevelUp', self.levelUp)
        self.accept('incBankNotes', self.increaseBankNotes)
        self.accept('unlockAmmo', self.unlockAmmoFromAI)
        self.accept('cdUnlockAll', self.useMagicWord)
        self.accept('endOfWave', self.resetMin)
        self.accept('flashHandleStart', self.flashHandleStart)
        self.accept('flashHandleStop', self.flashHandleStop)

    def _initGUI(self):
        self.panel = loader.loadModel('models/gui/pir_m_gui_can_ammoShelf')
        self.panel.reparentTo(self)
        self.panel.setScale(3.0)
        self.panel.setPos(-0.26, 0.0, 0.0)
        self.tabHandle = GuiButton.GuiButton(parent=self.panel, command=self.onTabClick, image=None, geom=(self.panel.find('**/ammoButton/idle'), self.panel.find('**/ammoButton/idle'), self.panel.find('**/ammoButton/over')), hotkeys=['shift'], helpText='Help Text', helpDelay=0)
        self.tabHandle.reparentTo(self.panel)
        for i in range(12):
            skillId = 12931 + i
            button = AmmoPanelButton.AmmoPanelButton(self.onAmmoClick, skillId, 0)
            button.reparentTo(self.panel)
            button.setScale(button.getScale() / 3.0)
            button.setPos(0.0, 0.0, 0.125 - 0.05 * (i % 6))
            if i >= 6:
                button.setX(button.getX() + 0.05)
            self.buttons[skillId] = button
            if i == 0:
                button.disablePurchase()

        self.oldAmmoSkillId = self.cannon.getAmmoSkillId()
        self.setBin('gui-cannonDefense', 2)
        return

    def _initSfx(self):
        self.sfxAmmoBought = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_AMMO_BOUGHT)
        self.sfxAmmoDeny = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_AMMO_DENY)
        self.sfxAmmoOut = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_AMMO_RECHARGE)

    def _unloadSfx(self):
        if self.sfxAmmoBought:
            loader.unloadSfx(self.sfxAmmoBought)
            self.sfxAmmoBought = None
        if self.sfxAmmoDeny:
            loader.unloadSfx(self.sfxAmmoDeny)
            self.sfxAmmoDeny = None
        if self.sfxAmmoOut:
            loader.unloadSfx(self.sfxAmmoOut)
            self.sfxAmmoOut = None
        return

    def _createBankNoteText(self):
        textPlaceHolder = self.panel.find('**/text')
        self.bankNoteTxt = TextNode('BankNoteText')
        self.bankNoteTxt.setFont(PiratesGlobals.getInterfaceFont())
        self.bankNoteTxt.setTextColor(PiratesGuiGlobals.TextFG1)
        self.bankNoteTxt.setShadow(0.05, 0.05)
        self.bankNoteTxt.setAlign(TextNode.ALeft)
        bankNoteTxtNode = textPlaceHolder.attachNewNode(self.bankNoteTxt)
        bankNoteTxtNode.setScale(0.015)
        bankNoteTxtNode.setDepthTest(False)
        bankNoteTxtNode.setDepthWrite(False)
        bankNoteTxtNode.setPos(-0.02, 0, 0)
        self.updateBankNoteText()

    def onTabClick(self, event=None):
        if self.state == CLOSED:
            posInterval = self.panel.posInterval(0.25, Point3(0.1, 0.0, 0.0))
            self.flashHandleStop()
        else:
            posInterval = self.panel.posInterval(0.25, Point3(-0.26, 0.0, 0.0))
        self.state = 1 - self.state
        sequence = Sequence(posInterval)
        sequence.start()

    def onAmmoClick(self, skillId):
        button = self.buttons[skillId]
        if button.isLocked():
            if not Freebooter.getPaidStatus(base.localAvatar.doId) and skillId > CannonDefenseGlobals.FREEBOOTER_LAST_AMMO_AVAILABLE:
                localAvatar.guiMgr.showNonPayer()
            return
        if button.canPurchase(self._bankNotes):
            if self.addAmmoSkill(skillId):
                self._bankNotes -= button.cost
                self.updateBankNoteText()
                button.disablePurchase()
                if self.sfxAmmoBought:
                    base.playSfx(self.sfxAmmoBought)
            elif not self.hasSkill(skillId):
                button.flash()
                self.msgMgr.showNoAmmoSlot()
                if self.sfxAmmoDeny:
                    base.playSfx(self.sfxAmmoDeny)
        elif not self.hasSkill(skillId):
            button.flash()
            self.msgMgr.showNotEnoughBankNotes()
            if self.sfxAmmoDeny:
                base.playSfx(self.sfxAmmoDeny)
        if self.hasSkill(skillId):
            base.localAvatar.guiMgr.combatTray.skillTray.updateSkillTray(InventoryType.DefenseCannonRep, WeaponGlobals.DEFENSE_CANNON, hideFirst=False)
            base.localAvatar.guiMgr.combatTray.triggerSkillTraySkill(skillId)
            self.cannon.cgui.showCannonControls()
            self.updateQuantities()

    def hasAmmo(self):
        hasNotEmpty = False
        for i in range(len(PiratesGlobals.CANNON_DEFENSE_SKILLS)):
            if PiratesGlobals.CANNON_DEFENSE_SKILLS[i] != InventoryType.DefenseCannonEmpty:
                hasNotEmpty = True

        return hasNotEmpty

    def hasCurrentAmmo(self):
        return self.ammoQuantities.get(self.cannon.getAmmoSkillId(), 0) > 0 or self.ammoQuantities.get(self.cannon.getAmmoSkillId(), 0) == -1

    def hasSkill(self, skillId):
        for i in range(len(PiratesGlobals.CANNON_DEFENSE_SKILLS)):
            if PiratesGlobals.CANNON_DEFENSE_SKILLS[i] == skillId:
                return True

        return False

    def addAmmoSkill(self, skillId):
        index = -1
        for i in range(len(PiratesGlobals.CANNON_DEFENSE_SKILLS)):
            if PiratesGlobals.CANNON_DEFENSE_SKILLS[i] == InventoryType.DefenseCannonEmpty:
                index = i
                break

        if index < 0 or not Freebooter.getPaidStatus(base.localAvatar.doId) and index >= CannonDefenseGlobals.FREEBOOTER_MAX_AMMO_SLOTS:
            return False
        PiratesGlobals.CANNON_DEFENSE_SKILLS.remove(InventoryType.DefenseCannonEmpty)
        PiratesGlobals.CANNON_DEFENSE_SKILLS.insert(index, skillId)
        self.ammoQuantities[skillId] = CannonDefenseGlobals.getDefenseCannonAmmoAmount(skillId)
        return True

    def removeAmmoSkill(self, skillId, useDefaultAmmo=False):
        index = -1
        for i in range(len(PiratesGlobals.CANNON_DEFENSE_SKILLS)):
            if PiratesGlobals.CANNON_DEFENSE_SKILLS[i] == skillId:
                index = i
                break

        if index < 0:
            return False
        PiratesGlobals.CANNON_DEFENSE_SKILLS.remove(skillId)
        PiratesGlobals.CANNON_DEFENSE_SKILLS.insert(index, InventoryType.DefenseCannonEmpty)
        button = self.buttons[skillId]
        modifier = max(0, self.ammoQuantities[skillId] / float(CannonDefenseGlobals.getDefenseCannonAmmoAmount(skillId)))
        self._bankNotes += int(button.cost * modifier)
        self.updateBankNoteText()
        button.enablePurchase()
        base.localAvatar.guiMgr.combatTray.skillTray.updateSkillTray(InventoryType.DefenseCannonRep, WeaponGlobals.DEFENSE_CANNON, hideFirst=False)
        self.updateQuantities()
        if useDefaultAmmo and not self.hasAmmo():
            self.onAmmoClick(InventoryType.DefenseCannonRoundShot)
        elif skillId == base.localAvatar.guiMgr.combatTray.getLastAmmoSkillId():
            self.cannon.cgui.hideCannonControls()
            self.cannon.cgui.skillTray.show()
            if self.state == CLOSED and not self.hasAmmo():
                self.onTabClick()
        self.ammoQuantities[skillId] = 0
        return True

    def addDefaultAmmo(self):
        default = InventoryType.DefenseCannonRoundShot
        PiratesGlobals.CANNON_DEFENSE_SKILLS.append(default)
        self.ammoQuantities[default] = CannonDefenseGlobals.getDefenseCannonAmmoAmount(default)
        base.localAvatar.guiMgr.combatTray.triggerSkillTraySkill(default)

    def addAmmoSlot(self):
        if len(PiratesGlobals.CANNON_DEFENSE_SKILLS) == 0:
            self.addDefaultAmmo()
        else:
            PiratesGlobals.CANNON_DEFENSE_SKILLS.append(InventoryType.DefenseCannonEmpty)
        base.localAvatar.guiMgr.combatTray.skillTray.updateSkillTray(InventoryType.DefenseCannonRep, WeaponGlobals.DEFENSE_CANNON, hideFirst=False)
        self.updateQuantities()

    def levelUp(self, level):
        if level > 1:
            base.cr.activeWorld.d_sendMessage(base.localAvatar.doId, PLocalizer.CannonDefenseLevelUp % (PLocalizer.InventoryTypeNames[InventoryType.DefenseCannonRep], level))
        message = ''
        while self.currentLevel < level:
            if self.currentLevel < len(CannonDefenseGlobals.levelUpgrades):
                upgradeArray = CannonDefenseGlobals.levelUpgrades[self.currentLevel]
                for i in range(len(upgradeArray)):
                    upgrade = upgradeArray[i]
                    if upgrade == 'upgrade':
                        message += PLocalizer.LevelUpCannonDefenseRepeaterCannon
                        self.cannon.requestUpgradeToRepeater()
                    elif upgrade < 5:
                        message += PLocalizer.LevelUpCannonDefenseAmmoSlot
                        self.addAmmoSlot()
                    elif self.buttons[upgrade].isLocked():
                        message += PLocalizer.LevelUpCannonDefense % PLocalizer.InventoryTypeNames[upgrade]
                        base.cr.activeWorld.d_addUnlockedAmmo(upgrade)
                        if level > 1:
                            base.cr.activeWorld.d_sendMessage(base.localAvatar.doId, PLocalizer.CannonDefenseAmmoUnlocked % PLocalizer.InventoryTypeNames[upgrade])

            self.currentLevel += 1

        if self.currentLevel > 1:
            self.msgMgr.showDefenseCannonSkillsUnlocked(message)

    def updateBankNoteText(self):
        if self._bankNotes < 0:
            bnotes = 0
        else:
            bnotes = math.floor(self._bankNotes)
        self.bankNoteTxt.setText(PLocalizer.BankNotes % bnotes)

    def increaseBankNotes(self, increase, total):
        self._bankNotes = self._bankNotes + increase
        if self._bankNotes > total:
            if not self.usedMagicWord:
                self._bankNotes = total
        self.updateBankNoteText()

    def decreaseAmmoAmount(self, update=True):
        if self.ammoQuantities[self.cannon.getAmmoSkillId()] >= 0:
            if update:
                self.ammoQuantities[self.cannon.getAmmoSkillId()] -= 1
                if self.ammoQuantities[self.cannon.getAmmoSkillId()] <= 0:
                    self.ammoQuantities[self.cannon.getAmmoSkillId()] = 0
                    self.removeAmmoSkill(self.cannon.getAmmoSkillId(), True)
                    if self.sfxAmmoOut:
                        base.playSfx(self.sfxAmmoOut)
                    return
        self.updateQuantities()

    def updateQuantities(self):
        for button in base.localAvatar.guiMgr.combatTray.skillTray.tray.itervalues():
            if button.skillId != InventoryType.DefenseCannonEmpty:
                if button.skillId in self.ammoQuantities:
                    button.updateQuantity(self.ammoQuantities[button.skillId])

    def triggerSkillWithHotkey(self, hotkey):
        if hotkey < len(PiratesGlobals.CANNON_DEFENSE_SKILLS):
            skillId = PiratesGlobals.CANNON_DEFENSE_SKILLS[hotkey]
            if skillId != InventoryType.DefenseCannonEmpty:
                base.localAvatar.guiMgr.combatTray.triggerSkillTraySkill(skillId)

    def unlockAmmoFromAI(self, ammoSkillIds):
        for ammoSkillId in ammoSkillIds:
            if Freebooter.getPaidStatus(base.localAvatar.doId) or ammoSkillId <= CannonDefenseGlobals.FREEBOOTER_LAST_AMMO_AVAILABLE:
                self.buttons[ammoSkillId].unlock()

    def flashHandleStart(self):
        if self.flashIval or self.state == OPENED:
            return
        self.flashIval = Sequence(LerpColorInterval(self.tabHandle, 0.25, color=VBase4(0.2, 0.2, 0.2, 3.0), blendType='easeOut'), LerpColorInterval(self.tabHandle, 0.25, color=VBase4(1.0, 1.0, 1.0, 1.0), blendType='easeOut'))
        self.flashIval.loop()

    def flashHandleStop(self):
        if self.flashIval:
            self.flashIval.pause()
            self.flashIval = None
        self.tabHandle.setColor(1.0, 1.0, 1.0, 1.0)
        return

    def useMagicWord(self):
        self.levelUp(20)
        self.usedMagicWord = True
        self._bankNotes = 99999
        self.updateBankNoteText()

    def destroy(self):
        self._unloadSfx()
        self.panel.detachNode()
        self.tabHandle.destroy()
        self.msgMgr.destroy()
        self.cannon.setAmmoSkillId(self.oldAmmoSkillId)
        PiratesGlobals.CANNON_DEFENSE_SKILLS = []
        self.ignore('onSellClick')
        self.ignore('incBankNotes')
        self.ignore('defenseCannonLevelUp')
        self.ignore('unlockAmmo')
        self.ignore('cdUnlockAll')
        self.ignore('endOfWave')
        self.ignore('flashHandleStart')
        self.ignore('flashHandleStop')
        for i in range(4):
            self.ignore('%d' % (i + 1))

        DirectFrame.destroy(self)

    def resetMin(self):
        if self._bankNotes < 0:
            self._bankNotes = 0