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
from pirates.piratesgui.SongListItem import SongListItem

class SongItemGui(SongListItem):
    width = PiratesGuiGlobals.InventoryItemGuiWidth
    height = PiratesGuiGlobals.InventoryItemGuiHeight
    available = True

    def __init__(self, data, trade=0, buy=0, sell=0, use=0, weapon=0, isDisabled=0, **kw):
        if (trade or buy or sell or use or weapon) and not isDisabled:
            buttonRelief = DGG.RAISED
            buttonState = DGG.NORMAL
        else:
            buttonRelief = DGG.RIDGE
            buttonState = DGG.DISABLED
        self.loadGui()
        optiondefs = (
         ('relief', None, None), ('state', buttonState, None), ('frameSize', (0, self.width, 0, self.height), None), ('image', SongItemGui.genericButton, None), ('image_scale', (0.54, 1, 0.42), None), ('image_pos', (0.26, 0, 0.08), None), ('pressEffect', 0, None), ('command', self.sendEvents, None))
        self.defineoptions(kw, optiondefs)
        SongListItem.__init__(self, data, trade=trade, buy=buy, sell=sell, use=use, weapon=weapon, isDisabled=isDisabled, width=self.width, height=self.height)
        self.initialiseoptions(SongItemGui)
        self.createGui()
        self.helpBox = None
        return

    def loadGui(self):
        if SongItemGui.guiLoaded:
            return
        SongListItem.loadGui(self)
        SongItemGui.genericButton = (
         SongListItem.topGui.find('**/generic_button'), SongListItem.topGui.find('**/generic_button_down'), SongListItem.topGui.find('**/generic_button_over'), SongListItem.topGui.find('**/generic_button_disabled'))

    def createGui(self):
        itemId = self.data[0]
        self.picture = DirectFrame(parent=self, relief=None, state=DGG.DISABLED, pos=(0.01,
                                                                                      0,
                                                                                      0.01))
        self.nameTag = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=self.name, text_scale=PiratesGuiGlobals.TextScaleSmall * PLocalizer.getHeadingScale(2), text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.05,
                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                           0.105), text_font=PiratesGlobals.getInterfaceFont())
        itemTypeFormatted = ''
        self.itemTypeName = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=itemTypeFormatted, text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getInterfaceFont(), pos=(0.05,
                                                                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                                                                     0.065))
        self.miscText = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text='', text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.05,
                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                       0.025))
        if self.minLvl > 0:
            repId = WeaponGlobals.getRepId(itemId)
            if repId:
                self.checkLevel(repId, self.minLvl)
        trainingReq = EconomyGlobals.getItemTrainingReq(itemId)
        if trainingReq:
            self.checkTrainingReq(trainingReq)
        if EconomyGlobals.getItemCategory(itemId) == ItemType.AMMO:
            skillId = WeaponGlobals.getSkillIdForAmmoSkillId(itemId)
            self.checkSkillReq(skillId)
        if self.buy:
            self.checkPlayerInventory(itemId)
        self.costText = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, image=SongListItem.coinImage, image_scale=0.12, image_pos=Vec3(-0.01, 0, 0.01), text=str(self.price), text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ARight, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, text_pos=(-0.03, 0, 0), pos=(self.width - 0.035, 0, 0.105), text_font=PiratesGlobals.getInterfaceFont())
        if self.quantity and self.quantity > 1:
            self.quantityLabel = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=str(self.quantity), frameColor=(0,
                                                                                                                                0,
                                                                                                                                0,
                                                                                                                                1), frameSize=(-0.01, 0.02, -0.01, 0.025), text_scale=0.0275, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.02,
                                                                                                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                                                                                                               0.025), text_font=PiratesGlobals.getPirateBoldOutlineFont())
        itemClass = EconomyGlobals.getItemCategory(itemId)
        if itemClass == ItemType.WEAPON or itemClass == ItemType.POUCH:
            asset = EconomyGlobals.getItemIcons(itemId)
            if asset:
                self.picture['geom'] = SongItemGui.weaponIcons.find('**/%s*' % asset)
                self.picture['geom_scale'] = 0.11
                self.picture['geom_pos'] = (0.08, 0, 0.068)
        elif itemClass == ItemType.CONSUMABLE:
            asset = EconomyGlobals.getItemIcons(itemId)
            if asset:
                self.picture['geom'] = SongItemGui.skillIcons.find('**/%s*' % asset)
                self.picture['geom_scale'] = 0.11
                self.picture['geom_pos'] = (0.08, 0, 0.068)
        if InventoryType.begin_WeaponCannonAmmo <= itemId and itemId <= InventoryType.end_WeaponCannonAmmo or InventoryType.begin_WeaponPistolAmmo <= itemId and itemId <= InventoryType.end_WeaponGrenadeAmmo or InventoryType.begin_WeaponDaggerAmmo <= itemId and itemId <= InventoryType.end_WeaponDaggerAmmo:
            skillId = WeaponGlobals.getSkillIdForAmmoSkillId(itemId)
            if skillId:
                asset = WeaponGlobals.getSkillIcon(skillId)
                if asset:
                    self.picture['geom'] = SongListItem.skillIcons.find('**/%s' % asset)
                    self.picture['geom_scale'] = 0.15
                    self.picture['geom_pos'] = (0.069, 0, 0.069)
        elif InventoryType.SmallBottle <= itemId and itemId <= InventoryType.LargeBottle:
            self.picture['geom'] = SongListItem.topGui.find('**/main_gui_ship_bottle')
            self.picture['geom_scale'] = 0.1
            self.picture['geom_pos'] = (0.069, 0, 0.069)
        self.flattenStrong()
        return

    def checkLevel(self, repId, minLvl):
        inv = localAvatar.getInventory()
        if inv:
            repAmt = inv.getAccumulator(repId)
            if minLvl > ReputationGlobals.getLevelFromTotalReputation(repId, repAmt)[0]:
                self.highlightRed(PLocalizer.LevelRequirement % self.minLvl)

    def checkTrainingReq(self, trainingReq):
        inv = localAvatar.getInventory()
        if inv:
            amt = inv.getStackQuantity(trainingReq)
            if not amt:
                self.highlightRed(PLocalizer.TrainingRequirement)

    def checkSkillReq(self, skillId):
        if skillId:
            if base.localAvatar.getSkillQuantity(skillId) < 2:
                skillName = PLocalizer.getInventoryTypeName(skillId)
                self.highlightRed(PLocalizer.SkillRequirement % skillName)

    def checkPlayerInventory(self, itemId, extraQty=0):
        if self.available:
            inventory = base.localAvatar.getInventory()
            currStock = inventory.getStackQuantity(itemId)
            currStockLimit = inventory.getStackLimit(itemId)
            if currStock == 0 and not (base.cr.newsManager.getHoliday(21) and itemId in InventoryType.WinterHolidaySongs):
                self.name = PLocalizer.makeHeadingString(PLocalizer.SongTitleUnknown, 2)
                self.nameTag['text'] = PLocalizer.makeHeadingString(PLocalizer.SongTitleUnknown, 2)
                self.itemTypeName['text'] = PLocalizer.makeHeadingString(PLocalizer.SongComingSoon, 1)
                self.disable()

    def highlightRed(self, text=''):
        self['state'] = DGG.DISABLED
        self['image_color'] = Vec4(0.55, 0.55, 0.5, 1)
        self.available = False
        self.highlightBox(text, Vec4(0.75, 0.5, 0.5, 1), PiratesGuiGlobals.TextFG6)

    def highlightGreen(self, text=''):
        self.highlightBox(text, Vec4(0.5, 0.75, 0.5, 1), PiratesGuiGlobals.TextFG4)

    def highlightBox(self, text, image_color, text_fg):
        self.miscText['text_fg'] = text_fg
        if text != '':
            self.miscText['text'] = text

    def enable(self):
        if self.available:
            self['state'] = DGG.NORMAL

    def disable(self):
        if self.available:
            self['state'] = DGG.DISABLED

    def createHelpbox(self, args=None):
        if self.helpBox:
            return
        weaponInfo = PLocalizer.WeaponDescriptions.get(self.data[0])
        weaponDesc = weaponInfo
        self.helpText = DirectFrame(parent=self, relief=None, text=weaponDesc, state=DGG.DISABLED, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleSmall, text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=13, textMayChange=0, sortOrder=91)
        height = -self.helpText.getHeight()
        self.helpBox = BorderFrame(parent=aspect2d, state=DGG.DISABLED, frameSize=(-0.03, 0.43, height, 0.05), sortOrder=90, borderScale=0.2)
        self.helpText.reparentTo(self.helpBox)
        self.helpBox.setBin('gui-popup', 0)
        self.helpBox.setPos(self, 0.25, 0, -0.035)
        return

    def destroy(self):
        taskMgr.remove('helpInfoTask')
        taskMgr.remove(self.taskName('dragTask'))
        if self.helpBox:
            self.helpBox.destroy()
            self.helpBox = None
        del self.picture
        if self.weapon:
            taskMgr.remove(DGG.B1PRESS)
            taskMgr.remove(DGG.B2PRESS)
            taskMgr.remove(DGG.B3PRESS)
        SongListItem.destroy(self)
        return

    def setDraggable(self, d):
        self.draggable = d

    def dragStart(self, event):
        self.origionalPos = self.getPos(render2d)
        self.origionalParent = self.getParent()
        self.bringToFront()
        self.setColorScale(1, 1, 1, 0.5)
        if self.draggable:
            self.wrtReparentTo(aspect2d)
            taskMgr.remove(self.taskName('dragTask'))
            vWidget2render2d = self.getPos(render2d)
            vMouse2render2d = Point3(event.getMouse()[0], 0, event.getMouse()[1])
            editVec = Vec3(vWidget2render2d - vMouse2render2d)
            task = taskMgr.add(self.dragTask, self.taskName('dragTask'))
            task.editVec = editVec

    def dragTask(self, task):
        if task.time < PiratesGuiGlobals.DragStartDelayTime:
            return Task.cont
        else:
            mwn = base.mouseWatcherNode
            if mwn.hasMouse():
                vMouse2render2d = Point3(mwn.getMouse()[0], 0, mwn.getMouse()[1])
                newPos = vMouse2render2d + task.editVec
                self.setPos(render2d, newPos)
                newPos = self.getPos(aspect2d)
                x = newPos[0]
                z = newPos[2]
                x = x - x % 0.05
                z = z - z % 0.05
                x = min(1.3 - self.width, max(-1.3, x))
                z = min(1 - self.height, max(-1, z))
                self.setPos(aspect2d, x, 0.0, z)
            return Task.cont

    def dragStop(self, event):
        self.clearColorScale()
        self.wrtReparentTo(self.origionalParent)
        self.setPos(render2d, self.origionalPos)
        if self.draggable:
            taskMgr.remove(self.taskName('dragTask'))

    def showDetails(self, event):
        taskMgr.doMethodLater(PiratesGuiGlobals.HelpPopupTime, self.createHelpbox, 'helpInfoTask')
        self.createHelpbox()

    def hideDetails(self, event):
        taskMgr.remove('helpInfoTask')
        if self.helpBox:
            self.helpBox.destroy()
            self.helpBox = None
        return