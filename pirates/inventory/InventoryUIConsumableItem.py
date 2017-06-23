from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import Freebooter
from otp.otpbase import OTPLocalizer
from pirates.inventory.InventoryUIGlobals import *
from pirates.battle import WeaponGlobals
from pirates.inventory import ItemGlobals
from pirates.minigame import PotionGlobals
from pirates.inventory import InventoryUIStackItem

class InventoryUIConsumableItem(InventoryUIStackItem.InventoryUIStackItem):

    def __init__(self, manager, itemTuple, imageScaleFactor=1.0, showMax=1):
        InventoryUIStackItem.InventoryUIStackItem.__init__(self, manager, itemTuple, imageScaleFactor=imageScaleFactor, showMax=showMax, update=False)
        self.initialiseoptions(InventoryUIConsumableItem)
        skillIcons = loader.loadModel('models/textureCards/skillIcons')
        self['image'] = skillIcons.find('**/%s' % ItemGlobals.getIcon(self.itemTuple[1]))
        self['image_scale'] = 0.1 * imageScaleFactor
        self.helpFrame = None
        self.hasDrunk = False
        self.cm = CardMaker('itemCard')
        self.cm.setFrame(-0.3, 0.3, -0.09, 0.09)
        self.buffer = None
        self.lens = PerspectiveLens()
        self.lens.setNear(0.1)
        self.lens.setAspectRatio(0.6 / 0.18)
        self.realItem = None
        self.iconLabel = None
        self.itemCard = None
        self.portraitSceneGraph = NodePath('PortraitSceneGraph')
        detailGui = loader.loadModel('models/gui/gui_card_detail')
        self.bg = detailGui.find('**/color')
        self.bg.setScale(4)
        self.bg.setPos(0, 17, -6.3)
        self.glow = detailGui.find('**/glow')
        self.glow.setScale(3)
        self.glow.setPos(0, 17, -6.3)
        self.glow.setColor(1, 1, 1, 0.8)
        self.setBin('gui-fixed', 1)
        self.accept('open_main_window', self.createBuffer)
        self.accept('aspectRatioChanged', self.createBuffer)
        self.accept('close_main_window', self.destroyBuffer)
        return

    def destroy(self):
        if self.helpFrame:
            self.helpFrame.destroy()
            self.helpFrame = None
        self.destroyBuffer()
        if self.itemCard:
            self.itemCard.removeNode()
            del self.itemCard
            self.itemCard = None
        if self.realItem:
            self.realItem.removeNode()
            del self.realItem
            self.realItem = None
        if self.iconLabel:
            self.iconLabel.destroy()
            self.realItem = None
        if self.portraitSceneGraph:
            self.portraitSceneGraph.removeNode()
            del self.portraitSceneGraph
            self.portraitSceneGraph = None
        InventoryUIStackItem.InventoryUIStackItem.destroy(self)
        return

    def getName(self):
        return PLocalizer.getItemName(self.getId())

    def updateAmount(self, caller=None):
        if not self.localStore:
            import pdb
            pdb.set_trace()
        amount = localAvatar.getInventory().getItemQuantity(self.getCategory(), self.getId())
        self.amount = amount
        self.updateAmountText()

    def getAmount(self):
        return localAvatar.getInventory().getItemQuantity(self.getCategory(), self.getId())

    def getLimit(self):
        return localAvatar.getInventory().getItemLimit(self.getCategory(), self.getId())

    def showDetails(self, cell, detailsPos, detailsHeight, event=None):
        self.notify.debug('Item showDetails')
        if self.manager.heldItem or self.manager.locked or cell.isEmpty() or self.isEmpty() or not self.itemTuple:
            self.notify.debug(' early exit')
            return
        itemId = self.getId()
        self.helpFrame = DirectFrame(parent=self.manager, relief=None, state=DGG.DISABLED, sortOrder=1)
        self.helpFrame.setBin('gui-popup', -5)
        detailGui = loader.loadModel('models/gui/gui_card_detail')
        topGui = loader.loadModel('models/gui/toplevel_gui')
        coinImage = topGui.find('**/treasure_w_coin*')
        self.SkillIcons = loader.loadModel('models/textureCards/skillIcons')
        self.BuffIcons = loader.loadModel('models/textureCards/buff_icons')
        border = self.SkillIcons.find('**/base')
        halfWidth = 0.3
        halfHeight = 0.2
        basePosX = cell.getX(aspect2d)
        basePosZ = cell.getZ(aspect2d)
        cellSizeX = 0.0
        cellSizeZ = 0.0
        if cell:
            cellSizeX = cell.cellSizeX
            cellSizeZ = cell.cellSizeZ
        textScale = PiratesGuiGlobals.TextScaleMed
        titleScale = PiratesGuiGlobals.TextScaleTitleSmall
        if len(self.getName()) >= 30:
            titleNameScale = PiratesGuiGlobals.TextScaleLarge
        else:
            titleNameScale = PiratesGuiGlobals.TextScaleExtraLarge
        subtitleScale = PiratesGuiGlobals.TextScaleMed
        iconScalar = 1.5
        borderScaler = 0.25
        splitHeight = 0.01
        vMargin = 0.03
        runningVertPosition = 0.3
        runningSize = 0.0
        labels = []
        titleColor = PiratesGuiGlobals.TextFG6
        rarity = ItemGlobals.getRarity(itemId)
        rarityText = PLocalizer.getItemRarityName(rarity)
        subtypeText = PLocalizer.getItemSubtypeName(ItemGlobals.getSubtype(itemId))
        if rarity == ItemGlobals.CRUDE:
            titleColor = PiratesGuiGlobals.TextFG24
        else:
            if rarity == ItemGlobals.COMMON:
                titleColor = PiratesGuiGlobals.TextFG13
            else:
                if rarity == ItemGlobals.RARE:
                    titleColor = PiratesGuiGlobals.TextFG4
                elif rarity == ItemGlobals.FAMED:
                    titleColor = PiratesGuiGlobals.TextFG5
                titleLabel = DirectLabel(parent=self, relief=None, text=self.getName(), text_scale=titleNameScale, text_fg=titleColor, text_shadow=PiratesGuiGlobals.TextShadow, text_align=TextNode.ACenter, pos=(0.0, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                self.bg.setColor(titleColor)
                tHeight = 0.07
                titleLabel.setZ(runningVertPosition)
                runningVertPosition -= tHeight
                runningSize += tHeight
                labels.append(titleLabel)
                subtitleLabel = DirectLabel(parent=self, relief=None, text='\x01slant\x01%s %s\x02' % (rarityText, subtypeText), text_scale=subtitleScale, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_align=TextNode.ACenter, pos=(0.0, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                subtHeight = 0.05
                subtitleLabel.setZ(subtHeight * 0.5 + runningVertPosition)
                runningVertPosition -= subtHeight
                runningSize += subtHeight
                labels.append(subtitleLabel)
                itemType = ItemGlobals.getType(itemId)
                itemSubtype = ItemGlobals.getSubtype(itemId)
                model = ItemGlobals.getModel(itemId)
                skillIcons = loader.loadModel('models/textureCards/skillIcons')
                if itemSubtype == ItemGlobals.POTION_BUFF:
                    self.iconLabel = DirectLabel(parent=self.portraitSceneGraph, relief=None, image=skillIcons.find('**/%s' % ItemGlobals.getIcon(itemId)), pos=(0.0,
                                                                                                                                                                 2.5,
                                                                                                                                                                 0.0))
                elif model:
                    self.realItem = loader.loadModel('models/inventory/' + model, okMissing=True)
                    if not self.realItem:
                        self.realItem = loader.loadModel('models/handheld/' + model)
                    if self.realItem:
                        posHpr = ItemGlobals.getModelPosHpr(model)
                        if posHpr:
                            self.realItem.setPos(posHpr[0], posHpr[1], posHpr[2])
                            self.realItem.setHpr(posHpr[3], posHpr[4], posHpr[5])
                        else:
                            self.realItem.setPos(0.0, 2.5, -0.4)
                            self.realItem.setHpr(45, 0, 0)
                        self.realItem.reparentTo(self.portraitSceneGraph)
                iHeight = 0.18
                self.createBuffer()
                self.itemCard.setZ(runningVertPosition - 0.06)
                runningVertPosition -= iHeight
                runningSize += iHeight
                labels.append(self.itemCard)
                itemCost = int(ItemGlobals.getGoldCost(itemId))
                if self.cell and self.cell.container:
                    itemCost = int(itemCost * self.cell.container.getItemPriceMult())
                goldLabel = DirectLabel(parent=self, relief=None, image=coinImage, image_scale=0.12, image_pos=Vec3(0.025, 0, -0.02), text=str(itemCost), text_scale=subtitleScale, text_align=TextNode.ARight, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, pos=(halfWidth - 0.05, 0.0, runningVertPosition + 0.08), text_pos=(0.0, -textScale))
                labels.append(goldLabel)
                if ItemGlobals.getSubtype(itemId) == 30:
                    duration = PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(ItemGlobals.getUseSkill(itemId)))
                    if duration >= 3600:
                        duration = duration / 3600
                        if duration == 1:
                            units = PLocalizer.Hour
                        else:
                            units = PLocalizer.Hours
                    elif duration >= 60:
                        duration = duration / 60
                        if duration == 1:
                            units = PLocalizer.Minute
                        else:
                            units = PLocalizer.Minutes
                    else:
                        units = PLocalizer.Seconds
                    potency = PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(ItemGlobals.getUseSkill(itemId)))
                    data = {'pot': int(potency * 100),'dur': int(duration),'unit': units}
                    description = PLocalizer.PotionDescs[ItemGlobals.getUseSkill(itemId)].safe_substitute(data)
                else:
                    description = PLocalizer.getItemFlavorText(itemId)
                if description != '':
                    descriptionLabel = DirectLabel(parent=self, relief=None, text=description, text_scale=textScale, text_wordwrap=halfWidth * 2.0 * (0.95 / textScale), text_align=TextNode.ALeft, pos=(-halfWidth + textScale * 0.5, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                    dHeight = descriptionLabel.getHeight() + 0.02
                    runningVertPosition -= dHeight
                    runningSize += dHeight
                    labels.append(descriptionLabel)
                if not Freebooter.getPaidStatus(localAvatar.getDoId()):
                    if rarity != ItemGlobals.CRUDE:
                        unlimitedLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.UnlimitedAccessRequirement, text_scale=textScale, text_wordwrap=halfWidth * 2.0 * (1.5 / titleScale), text_fg=PiratesGuiGlobals.TextFG6, text_shadow=PiratesGuiGlobals.TextShadow, text_align=TextNode.ACenter, pos=(0.0, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                        uHeight = unlimitedLabel.getHeight()
                        runningVertPosition -= uHeight
                        runningSize += uHeight
                        labels.append(unlimitedLabel)
                runningVertPosition -= 0.02
                runningSize += 0.02
                useLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.RightClickPotion, text_scale=textScale, text_wordwrap=halfWidth * 2.0 * (1.5 / titleScale), text_fg=PiratesGuiGlobals.TextFG6, text_shadow=PiratesGuiGlobals.TextShadow, text_align=TextNode.ACenter, pos=(0.0, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                uHeight = useLabel.getHeight()
                runningVertPosition -= uHeight
                runningSize += uHeight
                labels.append(useLabel)
                runningVertPosition -= 0.02
                runningSize += 0.02
                panels = self.helpFrame.attachNewNode('panels')
                topPanel = panels.attachNewNode('middlePanel')
                detailGui.find('**/top_panel').copyTo(topPanel)
                topPanel.setScale(0.08)
                topPanel.reparentTo(self.helpFrame)
                middlePanel = panels.attachNewNode('middlePanel')
                detailGui.find('**/middle_panel').copyTo(middlePanel)
                middlePanel.setScale(0.08)
                middlePanel.reparentTo(self.helpFrame)
                placement = 0
                i = 0
                heightMax = -0.08
                currentHeight = runningVertPosition
                if detailsHeight:
                    currentHeight = -detailsHeight
                while currentHeight < heightMax:
                    middlePanel = panels.attachNewNode('middlePanel%s' % 1)
                    detailGui.find('**/middle_panel').copyTo(middlePanel)
                    middlePanel.setScale(0.08)
                    middlePanel.reparentTo(self.helpFrame)
                    if currentHeight + 0.2 >= heightMax:
                        difference = heightMax - currentHeight
                        placement += 0.168 / 0.2 * difference
                        currentHeight += difference
                    else:
                        placement += 0.168
                        currentHeight += 0.2
                    middlePanel.setZ(-placement)
                    i += 1

                bottomPanel = panels.attachNewNode('bottomPanel')
                detailGui.find('**/bottom_panel').copyTo(bottomPanel)
                bottomPanel.setScale(0.08)
                bottomPanel.setZ(-placement)
                bottomPanel.reparentTo(self.helpFrame)
                colorPanel = panels.attachNewNode('colorPanel')
                detailGui.find('**/color').copyTo(colorPanel)
                colorPanel.setScale(0.08)
                colorPanel.setColor(titleColor)
                colorPanel.reparentTo(self.helpFrame)
                lineBreakTopPanel = panels.attachNewNode('lineBreakTopPanel')
                detailGui.find('**/line_break_top').copyTo(lineBreakTopPanel)
                lineBreakTopPanel.setScale(0.08, 0.08, 0.07)
                lineBreakTopPanel.setZ(0.008)
                lineBreakTopPanel.reparentTo(self.helpFrame)
                panels.flattenStrong()
                self.helpFrame['frameSize'] = (
                 -halfWidth, halfWidth, -(runningSize + vMargin), vMargin)
                totalHeight = self.helpFrame.getHeight() - 0.1
                for label in labels:
                    label.reparentTo(self.helpFrame)

                if basePosX > 0.0:
                    newPosX = basePosX - (halfWidth + cellSizeX * 0.45)
                else:
                    newPosX = basePosX + (halfWidth + cellSizeX * 0.45)
                if basePosZ > 0.0:
                    newPosZ = basePosZ + cellSizeZ * 0.45
                newPosZ = basePosZ + totalHeight - cellSizeZ * 0.75
            if detailsPos:
                newPosX, newPosZ = detailsPos
        self.helpFrame.setPos(newPosX, 0, newPosZ)
        return

    def hideDetails(self, event=None):
        if self.helpFrame:
            self.helpFrame.destroy()
            self.helpFrame = None
        self.destroyBuffer()
        if self.realItem:
            self.realItem.removeNode()
        if self.iconLabel:
            self.iconLabel.destroy()
        return

    def createBuffer(self):
        self.destroyBuffer()
        self.buffer = base.win.makeTextureBuffer('par', 256, 256)
        self.buffer.setOneShot(True)
        self.cam = base.makeCamera(win=self.buffer, scene=self.portraitSceneGraph, clearColor=Vec4(1), lens=self.lens)
        self.cam.node().getDisplayRegion(0).setIncompleteRender(False)
        self.cam.reparentTo(self.portraitSceneGraph)
        self.bg.reparentTo(self.cam)
        self.glow.reparentTo(self.cam)
        if self.itemCard:
            self.itemCard.removeNode()
        tex = self.buffer.getTexture()
        self.itemCard = NodePath(self.cm.generate())
        self.itemCard.setTexture(tex, 1)
        if self.helpFrame:
            self.itemCard.reparentTo(self.helpFrame)

    def destroyBuffer(self):
        if self.buffer:
            base.graphicsEngine.removeWindow(self.buffer)
            self.buffer = None
            self.bg.detachNode()
            self.glow.detachNode()
            self.cam.removeNode()
            self.cam = None
        return