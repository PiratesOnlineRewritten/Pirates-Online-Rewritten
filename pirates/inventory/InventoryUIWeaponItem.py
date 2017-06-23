from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import Freebooter
from otp.otpbase import OTPLocalizer
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.inventory.InventoryUIGlobals import *
from pirates.inventory import ItemGlobals
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import *
from pirates.reputation import ReputationGlobals
from pirates.economy import EconomyGlobals
from pirates.inventory import InventoryUIItem
tpMgr = TextPropertiesManager.getGlobalPtr()
itemBrown = TextProperties()
itemBrown.setSmallCaps(1)
itemBrown.setTextColor(0.525, 0.3125, 0.0875, 1)
itemBrown.setShadowColor(PiratesGuiGlobals.TextShadow)
itemBrown.setShadow(0.06, 0.06)
tpMgr.setProperties('itemBrown', itemBrown)
itemYellow = TextProperties()
itemYellow.setSmallCaps(1)
itemYellow.setTextColor(0.5, 0.5, 0, 1)
itemYellow.setShadowColor(PiratesGuiGlobals.TextShadow)
itemYellow.setShadow(0.06, 0.06)
tpMgr.setProperties('itemYellow', itemYellow)
itemGreen = TextProperties()
itemGreen.setSmallCaps(1)
itemGreen.setTextColor(0, 0.4, 0, 1)
itemGreen.setShadowColor(PiratesGuiGlobals.TextShadow)
itemGreen.setShadow(0.06, 0.06)
tpMgr.setProperties('itemGreen', itemGreen)
itemBlue = TextProperties()
itemBlue.setSmallCaps(1)
itemBlue.setTextColor(0.24, 0.36, 0.6, 1)
itemBlue.setShadowColor(PiratesGuiGlobals.TextShadow)
itemBlue.setShadow(0.06, 0.06)
tpMgr.setProperties('itemBlue', itemBlue)
itemRed = TextProperties()
itemRed.setSmallCaps(1)
itemRed.setTextColor(0.4, 0, 0, 1)
itemRed.setShadowColor(PiratesGuiGlobals.TextShadow)
itemRed.setShadow(0.06, 0.06)
tpMgr.setProperties('itemRed', itemRed)

class InventoryUIWeaponItem(InventoryUIItem.InventoryUIItem):
    notify = directNotify.newCategory('InventoryUIWeaponItem')

    def __init__(self, manager, itemTuple, imageScaleFactor=1.0):
        InventoryUIItem.InventoryUIItem.__init__(self, manager, itemTuple, imageScaleFactor=imageScaleFactor)
        weaponIcons = loader.loadModel('models/gui/gui_icons_weapon')
        self['image'] = weaponIcons.find('**/%s' % ItemGlobals.getIcon(itemTuple[1]))
        self['image_scale'] = 0.1 * imageScaleFactor
        self.helpFrame = None
        self.cm = CardMaker('itemCard')
        self.cm.setFrame(-0.3, 0.3, -0.09, 0.09)
        self.buffer = None
        self.lens = PerspectiveLens()
        self.lens.setNear(0.5)
        self.lens.setAspectRatio(0.6 / 0.18)
        self.realItem = None
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
            self.itemCard = None
        if self.realItem:
            self.realItem.removeNode()
            self.realItem = None
        if self.portraitSceneGraph:
            self.portraitSceneGraph.removeNode()
            self.portraitSceneGraph = None
        if self.bg:
            self.bg.removeNode()
            self.bg = None
        if self.glow:
            self.glow.removeNode()
            self.glow = None
        InventoryUIItem.InventoryUIItem.destroy(self)
        return

    def getName(self):
        return PLocalizer.getItemName(self.getId())

    def getPlunderName(self):
        nameText = self.getName()
        titleColor = PiratesGuiGlobals.TextFG6
        rarity = ItemGlobals.getRarity(self.getId())
        if rarity == ItemGlobals.CRUDE:
            titleColor = PiratesGuiGlobals.TextFG24
        elif rarity == ItemGlobals.COMMON:
            titleColor = PiratesGuiGlobals.TextFG13
        elif rarity == ItemGlobals.RARE:
            titleColor = PiratesGuiGlobals.TextFG4
        elif rarity == ItemGlobals.FAMED:
            titleColor = PiratesGuiGlobals.TextFG5
        return (nameText, titleColor)

    def showDetails(self, cell, detailsPos, detailsHeight, event=None):
        self.notify.debug('Item showDetails')
        if self.manager.heldItem or self.manager.locked or cell.isEmpty() or self.isEmpty() or not self.itemTuple:
            self.notify.debug(' early exit')
            return
        inv = localAvatar.getInventory()
        if not inv:
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
        itemColor = 'itemRed'
        rarity = ItemGlobals.getRarity(itemId)
        rarityText = PLocalizer.getItemRarityName(rarity)
        subtypeText = PLocalizer.getItemSubtypeName(ItemGlobals.getSubtype(itemId))
        if rarity == ItemGlobals.CRUDE:
            titleColor = PiratesGuiGlobals.TextFG24
            itemColor = 'itemBrown'
        else:
            if rarity == ItemGlobals.COMMON:
                titleColor = PiratesGuiGlobals.TextFG13
                itemColor = 'itemYellow'
            else:
                if rarity == ItemGlobals.RARE:
                    titleColor = PiratesGuiGlobals.TextFG4
                    itemColor = 'itemGreen'
                elif rarity == ItemGlobals.FAMED:
                    titleColor = PiratesGuiGlobals.TextFG5
                    itemColor = 'itemBlue'
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
                if model:
                    if itemType == ItemGlobals.GRENADE:
                        self.realItem = loader.loadModel('models/ammunition/' + model)
                    else:
                        self.realItem = loader.loadModel('models/handheld/' + model)
                    if self.realItem:
                        spinBlur = self.realItem.find('**/motion_blur')
                        if spinBlur:
                            spinBlur.hide()
                        if itemSubtype == ItemGlobals.MUSKET:
                            bayonetPart = self.realItem.find('**/bayonet')
                            if bayonetPart:
                                bayonetPart.stash()
                        posHpr = ItemGlobals.getModelPosHpr(model)
                        if posHpr:
                            self.realItem.setPos(posHpr[0], posHpr[1], posHpr[2])
                            self.realItem.setHpr(posHpr[3], posHpr[4], posHpr[5])
                        elif itemType == ItemGlobals.SWORD:
                            self.realItem.setPos(-1.5, 3.0, -0.3)
                            self.realItem.setHpr(90, 170, -90)
                        elif itemSubtype in (ItemGlobals.MUSKET, ItemGlobals.BAYONET):
                            self.realItem.setPos(-1.2, 3.0, -0.1)
                            self.realItem.setHpr(0, 135, 10)
                        elif itemSubtype == ItemGlobals.BLUNDERBUSS:
                            self.realItem.setPos(-0.3, 2.0, 0.0)
                            self.realItem.setHpr(0, 90, 0)
                        elif itemType == ItemGlobals.GUN:
                            self.realItem.setPos(-0.5, 2.0, -0.2)
                            self.realItem.setHpr(0, 90, 0)
                        elif itemType == ItemGlobals.DOLL:
                            self.realItem.setPos(0.0, 1.9, -0.1)
                            self.realItem.setHpr(0, 90, 180)
                        elif itemType == ItemGlobals.DAGGER:
                            self.realItem.setPos(-1.0, 2.0, -0.3)
                            self.realItem.setHpr(90, 170, -90)
                        elif itemType == ItemGlobals.GRENADE:
                            self.realItem.setPos(0.0, 3.5, -0.2)
                            self.realItem.setHpr(0, 0, 0)
                        elif itemType == ItemGlobals.STAFF:
                            self.realItem.setPos(-0.4, 3.0, -0.3)
                            self.realItem.setHpr(-90, 15, -90)
                        self.realItem.reparentTo(self.portraitSceneGraph)
                iHeight = 0.175
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
                infoText = PLocalizer.ItemAttackStrength % ('\x01%s\x01%s\x02' % (itemColor, ItemGlobals.getPower(itemId)))
                if itemType == ItemGlobals.GUN:
                    infoText += '     %s' % (PLocalizer.ItemBarrels % ('\x01%s\x01%s\x02' % (itemColor, ItemGlobals.getBarrels(itemId))))
                    infoText += '     %s' % (PLocalizer.ItemRangeStrength % ('\x01%s\x01%s\x02' % (itemColor, PLocalizer.getItemRangeName(WeaponGlobals.getRange(itemId)))))
                infoLabel = DirectLabel(parent=self, relief=None, text=infoText, text_scale=textScale, text_align=TextNode.ACenter, pos=(0.0, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                iHeight = 0.08
                runningVertPosition -= iHeight
                runningSize += iHeight
                labels.append(infoLabel)
                specialAttack = ItemGlobals.getSpecialAttack(itemId)
                if specialAttack:
                    attackIcon = self.SkillIcons.find('**/%s' % WeaponGlobals.getSkillIcon(specialAttack))
                    specialAttackNameLabel = DirectLabel(parent=self, relief=None, image=border, image_scale=0.1, geom=attackIcon, geom_scale=0.1, image_pos=(-0.07, 0.0, -0.05), geom_pos=(-0.07, 0.0, -0.05), text=PLocalizer.getInventoryTypeName(specialAttack), text_scale=PiratesGuiGlobals.TextScaleLarge, text_wordwrap=halfWidth * 2.0 * (0.9 / titleScale), text_align=TextNode.ALeft, text_fg=titleColor, text_font=PiratesGlobals.getInterfaceOutlineFont(), text_shadow=PiratesGuiGlobals.TextShadow, pos=(-halfWidth + 0.12 + textScale * 0.5, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                    specialAttackRankLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.ItemRank % ItemGlobals.getSpecialAttackRank(itemId), text_scale=textScale, text_wordwrap=halfWidth * 2.0 * (0.9 / titleScale), text_align=TextNode.ARight, pos=(halfWidth - textScale * 0.5, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                    specialAttackType = WeaponGlobals.getSkillTrack(specialAttack)
                    if specialAttackType == WeaponGlobals.BREAK_ATTACK_SKILL_INDEX:
                        specialAttackTypeText = PLocalizer.BreakAttackSkill
                    elif specialAttackType == WeaponGlobals.DEFENSE_SKILL_INDEX:
                        specialAttackTypeText = PLocalizer.DefenseSkill
                    else:
                        specialAttackTypeText = PLocalizer.WeaponSkill
                    specialAttackTypeLabel = DirectLabel(parent=self, relief=None, text=specialAttackTypeText, text_scale=0.0335, text_wordwrap=halfWidth * 2.8 * (0.9 / titleScale), text_align=TextNode.ALeft, pos=(-halfWidth + 0.12 + textScale * 0.5, 0.0, runningVertPosition - PiratesGuiGlobals.TextScaleLarge), text_pos=(0.0, -textScale))
                    specialAttackInfo = PLocalizer.SkillDescriptions.get(specialAttack)
                    specialAttackDescriptionText = specialAttackInfo[1]
                    specialAttackDescriptionLabel = DirectLabel(parent=self, relief=None, text=specialAttackDescriptionText, text_scale=textScale, text_wordwrap=halfWidth * 2.8 * (0.9 / titleScale), text_align=TextNode.ALeft, pos=(-halfWidth + 0.12 + textScale * 0.5, 0.0, runningVertPosition - (specialAttackNameLabel.getHeight() + specialAttackTypeLabel.getHeight() - 0.06)), text_pos=(0.0, -textScale))
                    saHeight = specialAttackNameLabel.getHeight() + specialAttackTypeLabel.getHeight() + specialAttackDescriptionLabel.getHeight() - 0.04
                    runningVertPosition -= saHeight
                    runningSize += saHeight
                    labels.append(specialAttackNameLabel)
                    labels.append(specialAttackRankLabel)
                    labels.append(specialAttackTypeLabel)
                    labels.append(specialAttackDescriptionLabel)
                attributes = ItemGlobals.getAttributes(itemId)
                for i in range(0, len(attributes)):
                    attributeIcon = self.SkillIcons.find('**/%s' % ItemGlobals.getAttributeIcon(attributes[i][0]))
                    if not attributeIcon:
                        attributeIcon = self.BuffIcons.find('**/%s' % ItemGlobals.getAttributeIcon(attributes[i][0]))
                    attributeNameLabel = DirectLabel(parent=self, relief=None, image=border, image_scale=0.05, geom=attributeIcon, geom_scale=0.05, image_pos=(-0.07, 0.0, -0.03), geom_pos=(-0.07, 0.0, -0.03), text=PLocalizer.getItemAttributeName(attributes[i][0]), text_scale=PiratesGuiGlobals.TextScaleLarge, text_wordwrap=halfWidth * 2.0 * (0.9 / titleScale), text_align=TextNode.ALeft, text_fg=titleColor, text_font=PiratesGlobals.getInterfaceOutlineFont(), text_shadow=PiratesGuiGlobals.TextShadow, pos=(-halfWidth + 0.12 + textScale * 0.5, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                    attributeRankLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.ItemRank % attributes[i][1], text_scale=textScale, text_wordwrap=halfWidth * 2.0 * (0.9 / titleScale), text_align=TextNode.ARight, pos=(halfWidth - textScale * 0.5, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                    if attributeNameLabel.getHeight() > 0.075:
                        attributeNameSpace = 0.08
                    else:
                        attributeNameSpace = PiratesGuiGlobals.TextScaleLarge
                    attributeDescriptionLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.getItemAttributeDescription(attributes[i][0]), text_scale=textScale, text_wordwrap=halfWidth * 2.8 * (0.9 / titleScale), text_align=TextNode.ALeft, pos=(-halfWidth + 0.12 + textScale * 0.5, 0.0, runningVertPosition - attributeNameSpace), text_pos=(0.0, -textScale))
                    aHeight = attributeNameLabel.getHeight() + attributeDescriptionLabel.getHeight()
                    runningVertPosition -= aHeight + splitHeight
                    runningSize += aHeight + splitHeight
                    labels.append(attributeNameLabel)
                    labels.append(attributeRankLabel)
                    labels.append(attributeDescriptionLabel)

                skillBoosts = ItemGlobals.getSkillBoosts(itemId)
                for i in range(0, len(skillBoosts)):
                    skillId, skillBoost = skillBoosts[i]
                    linkedSkills = ItemGlobals.getLinkedSkills(itemId)
                    if linkedSkills:
                        for id in linkedSkills:
                            if skillId == WeaponGlobals.getLinkedSkillId(id):
                                skillId = id

                    boostIcon = self.SkillIcons.find('**/%s' % WeaponGlobals.getSkillIcon(skillId))
                    boostNameLabel = DirectLabel(parent=self, relief=None, image=border, image_scale=0.05, geom=boostIcon, geom_scale=0.05, image_pos=(-0.07, 0.0, -0.03), geom_pos=(-0.07, 0.0, -0.03), text=PLocalizer.ItemBoost % PLocalizer.getInventoryTypeName(skillId), text_scale=textScale, text_wordwrap=halfWidth * 2.0 * (0.9 / titleScale), text_align=TextNode.ALeft, pos=(-halfWidth + 0.12 + textScale * 0.5, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                    boostRankLabel = DirectLabel(parent=self, relief=None, text='+%s' % str(skillBoost), text_scale=textScale, text_wordwrap=halfWidth * 2.0 * (0.9 / titleScale), text_align=TextNode.ARight, pos=(halfWidth - textScale * 0.5, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                    bHeight = boostNameLabel.getHeight()
                    runningVertPosition -= bHeight + splitHeight
                    runningSize += bHeight + splitHeight
                    labels.append(boostNameLabel)
                    labels.append(boostRankLabel)

                description = PLocalizer.getItemFlavorText(itemId)
                if description != '':
                    descriptionLabel = DirectLabel(parent=self, relief=None, text=description, text_scale=textScale, text_wordwrap=halfWidth * 2.0 * (0.95 / textScale), text_align=TextNode.ALeft, pos=(-halfWidth + textScale * 0.5, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                    dHeight = descriptionLabel.getHeight() + 0.02
                    runningVertPosition -= dHeight
                    runningSize += dHeight
                    labels.append(descriptionLabel)
                weaponLevel = 0
                weaponRepId = WeaponGlobals.getRepId(itemId)
                weaponRep = inv.getReputation(weaponRepId)
                weaponReq = ItemGlobals.getWeaponRequirement(itemId)
                weaponText = None
                trainingToken = EconomyGlobals.getItemTrainingReq(itemId)
                trainingAmt = inv.getItemQuantity(trainingToken)
                if weaponReq:
                    weaponLevel = ReputationGlobals.getLevelFromTotalReputation(weaponRepId, weaponRep)[0]
                    if weaponLevel < weaponReq:
                        weaponColor = PiratesGuiGlobals.TextFG6
                    else:
                        weaponColor = (0.4, 0.4, 0.4, 1.0)
                    weaponText = PLocalizer.ItemLevelRequirement % (weaponReq, PLocalizer.getItemTypeName(itemType))
                elif trainingAmt == 0:
                    weaponColor = PiratesGuiGlobals.TextFG6
                    weaponText = PLocalizer.ItemTrainingRequirement % PLocalizer.getItemTypeName(itemType)
                if trainingAmt == 0:
                    if itemType == ItemGlobals.GUN:
                        base.localAvatar.sendRequestContext(InventoryType.GunTrainingRequired)
                    elif itemType == ItemGlobals.DOLL:
                        base.localAvatar.sendRequestContext(InventoryType.DollTrainingRequired)
                    elif itemType == ItemGlobals.DAGGER:
                        base.localAvatar.sendRequestContext(InventoryType.DaggerTrainingRequired)
                    elif itemType == ItemGlobals.STAFF:
                        base.localAvatar.sendRequestContext(InventoryType.StaffTrainingRequired)
                if weaponText:
                    weaponReqLabel = DirectLabel(parent=self, relief=None, text=weaponText, text_scale=textScale, text_wordwrap=halfWidth * 2.0 * (1.5 / titleScale), text_fg=weaponColor, text_shadow=PiratesGuiGlobals.TextShadow, text_align=TextNode.ACenter, pos=(0.0, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                    wHeight = weaponReqLabel.getHeight()
                    runningVertPosition -= wHeight
                    runningSize += wHeight
                    labels.append(weaponReqLabel)
                if not Freebooter.getPaidStatus(localAvatar.getDoId()):
                    if rarity != ItemGlobals.CRUDE:
                        unlimitedLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.UnlimitedAccessRequirement, text_scale=textScale, text_wordwrap=halfWidth * 2.0 * (1.5 / titleScale), text_fg=PiratesGuiGlobals.TextFG6, text_shadow=PiratesGuiGlobals.TextShadow, text_align=TextNode.ACenter, pos=(0.0, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                        uHeight = unlimitedLabel.getHeight()
                        runningVertPosition -= uHeight
                        runningSize += uHeight
                        labels.append(unlimitedLabel)
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
                lineBreakBottomPanel = panels.attachNewNode('lineBreakBottomPanel')
                detailGui.find('**/line_break_bottom').copyTo(lineBreakBottomPanel)
                lineBreakBottomPanel.setScale(0.08, 0.08, 0.07)
                lineBreakBottomPanel.setZ(-0.015)
                lineBreakBottomPanel.reparentTo(self.helpFrame)
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