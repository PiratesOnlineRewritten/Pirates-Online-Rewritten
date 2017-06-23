from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.makeapirate import TattooGlobals
from pirates.pirate import HumanDNA
from math import sin
from math import cos
from math import pi
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import ItemGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import Freebooter
from pirates.inventory import InventoryUIItem

class InventoryUITattooItem(InventoryUIItem.InventoryUIItem):

    def __init__(self, manager, itemTuple, imageScaleFactor=0.85):
        InventoryUIItem.InventoryUIItem.__init__(self, manager, itemTuple, imageScaleFactor=imageScaleFactor)
        self.initialiseoptions(InventoryUITattooItem)
        self['relief'] = None
        tattooGui = loader.loadModel('models/misc/tattoos')
        image = tattooGui.find('**/%s' % ItemGlobals.getIcon(itemTuple[1]))
        if image.isEmpty():
            image = tattooGui.find('**/tattoo_%s' % ItemGlobals.getIcon(itemTuple[1]))
        self['image'] = image
        self['image_scale'] = 0.1 * imageScaleFactor
        self.iconColor = (1.0, 1.0, 1.0, 1.0)
        self['image_color'] = (self.iconColor[0], self.iconColor[1], self.iconColor[2], self.iconColor[3])
        self.helpFrame = None
        self.cm = CardMaker('itemCard')
        self.cm.setFrame(-0.3, 0.3, -0.09, 0.09)
        self.buffer = None
        self.lens = PerspectiveLens()
        self.lens.setNear(0.1)
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
        self.displayHuman = self.manager.getDisplayHuman()
        self.masterHuman = self.manager.getMasterHuman()
        return

    def destroy(self):
        self.displayHuman = None
        self.masterHuman = None
        if self.helpFrame:
            self.helpFrame.destroy()
            self.helpFrame = None
        self.destroyBuffer()
        if self.itemCard:
            self.itemCard.removeNode()
        if self.realItem:
            self.realItem.removeNode()
        InventoryUIItem.InventoryUIItem.destroy(self)
        return

    def getName(self):
        return PLocalizer.getItemName(self.itemTuple[1])

    def showDetails(self, cell, detailsPos, detailsHeight, event=None):
        self.notify.debug('Item showDetails')
        if self.manager.heldItem or self.manager.locked or cell.isEmpty() or not self.itemTuple:
            self.notify.debug(' early exit')
            return
        itemId = self.getId()
        self.helpFrame = DirectFrame(parent=self.manager, relief=None, state=DGG.DISABLED, sortOrder=1)
        self.helpFrame.setBin('gui-popup', -5)
        detailGui = loader.loadModel('models/gui/gui_card_detail')
        topGui = loader.loadModel('models/gui/toplevel_gui')
        coinImage = topGui.find('**/treasure_w_coin*')
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
        typeText = PLocalizer.getTattooTypeName(ItemGlobals.getType(itemId))
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
                subtitleLabel = DirectLabel(parent=self, relief=None, text='\x01slant\x01%s %s\x02' % (rarityText, typeText), text_scale=subtitleScale, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_align=TextNode.ACenter, pos=(0.0, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
                subtHeight = 0.05
                subtitleLabel.setZ(subtHeight * 0.5 + runningVertPosition)
                runningVertPosition -= subtHeight
                runningSize += subtHeight
                labels.append(subtitleLabel)
                gender = localAvatar.style.gender
                dna = HumanDNA.HumanDNA(gender)
                dna.copy(localAvatar.style)
                bodyShape = localAvatar.style.getBodyShape()
                bodyHeight = localAvatar.style.getBodyHeight()
                bodyOffset = 0.5
                headOffset = 0
                armOffset = 0
                chestOffset = 0
                if bodyShape == 0:
                    bodyOffset = 0.5
                    if gender == 'm':
                        headOffset = 0.7
                        armOffset = 0.6
                        chestOffset = 0.5
                    elif gender == 'f':
                        headOffset = 0.55
                        armOffset = 0.5
                        chestOffset = 0.5
                else:
                    if bodyShape == 1:
                        bodyOffset = 0.5
                        if gender == 'm':
                            headOffset = 0.1
                            armOffset = 0.15
                        elif gender == 'f':
                            headOffset = 0.4
                            armOffset = 0.4
                            chestOffset = 0.3
                    else:
                        if bodyShape == 2:
                            bodyOffset = 0.5
                            if gender == 'f':
                                headOffset = -0.1
                        else:
                            if bodyShape == 3:
                                bodyOffset = 0.5
                                if gender == 'm':
                                    headOffset = 0.1
                                    armOffset = 0.15
                                elif gender == 'f':
                                    headOffset = -0.4
                                    armOffset = -0.2
                                    chestOffset = -0.3
                            else:
                                if bodyShape == 4:
                                    bodyOffset = 0.5
                                    if gender == 'm':
                                        headOffset = -0.25
                                        armOffset = -0.15
                                        chestOffset = -0.25
                                    elif gender == 'f':
                                        headOffset = 0.05
                                        armOffset = 0.1
                                else:
                                    if bodyShape == 5:
                                        bodyOffset = 0.5
                                        if gender == 'f':
                                            headOffset = -0.1
                                    elif bodyShape == 6:
                                        bodyOffset = 0.5
                                        if gender == 'f':
                                            headOffset = 0.3
                                            armOffset = 0.3
                                            chestOffset = 0.3
                                    elif bodyShape == 7:
                                        bodyOffset = 0.5
                                        if gender == 'f':
                                            headOffset = -0.1
                                    else:
                                        if bodyShape == 8:
                                            bodyOffset = 0.5
                                            if gender == 'm':
                                                headOffset = -0.15
                                                armOffset = -0.1
                                                chestOffset = -0.2
                                            elif gender == 'f':
                                                headOffset = -0.2
                                                armOffset = -0.1
                                                chestOffset = -0.2
                                        elif bodyShape == 9:
                                            bodyOffset = 0.5
                                            if gender == 'm':
                                                headOffset = -0.3
                                                armOffset = -0.2
                                                chestOffset = -0.3
                                            elif gender == 'f':
                                                headOffset = -0.4
                                                armOffset = -0.2
                                                chestOffset = -0.3
                                        m = Mat4(Mat4.identMat())
                                        itemType = ItemGlobals.getType(itemId)
                                        if itemType == ItemGlobals.CHEST:
                                            tattooType = TattooGlobals.ZONE1
                                        else:
                                            if itemType == ItemGlobals.ARM:
                                                tattooType = TattooGlobals.ZONE2
                                            elif itemType == ItemGlobals.FACE:
                                                tattooType = TattooGlobals.ZONE4
                                            if localAvatar.style.gender == 'm':
                                                maleModelId = ItemGlobals.getMaleModelId(itemId)
                                                if maleModelId:
                                                    tattooId = maleModelId
                                                    tattooOrientation = ItemGlobals.getOrientation(ItemGlobals.getMaleOrientation(itemId))
                                                    dna = HumanDNA.HumanDNA(localAvatar.style.gender)
                                                    dna.copy(localAvatar.style)
                                                    gender = 'm'
                                                else:
                                                    tattooId = ItemGlobals.getFemaleModelId(itemId)
                                                    tattooOrientation = ItemGlobals.getOrientation(ItemGlobals.getFemaleOrientation(itemId))
                                                    dna = HumanDNA.HumanDNA('f')
                                                    gender = 'f'
                                            else:
                                                femaleModelId = ItemGlobals.getFemaleModelId(itemId)
                                                if femaleModelId:
                                                    tattooId = femaleModelId
                                                    tattooOrientation = ItemGlobals.getOrientation(ItemGlobals.getFemaleOrientation(itemId))
                                                    dna = HumanDNA.HumanDNA(localAvatar.style.gender)
                                                    dna.copy(localAvatar.style)
                                                    gender = 'f'
                                                else:
                                                    tattooId = ItemGlobals.getMaleModelId(itemId)
                                                    tattooOrientation = ItemGlobals.getOrientation(ItemGlobals.getMaleOrientation(itemId))
                                                    dna = HumanDNA.HumanDNA('m')
                                                    gender = 'm'
                                                offsetx = tattooOrientation[0]
                                                offsety = tattooOrientation[1]
                                                scale = tattooOrientation[2]
                                                rotate = tattooOrientation[3]
                                                color = 0
                                                S = Vec2(1 / float(scale), 1 / float(scale))
                                                Iv = Vec2(offsetx, offsety)
                                                Vm = Vec2(sin(rotate * pi / 180.0), cos(rotate * pi / 180.0))
                                                Vms = Vec2(Vm[0] * S[0], Vm[1] * S[1])
                                                Vn = Vec2(Vm[1], -Vm[0])
                                                Vns = Vec2(Vn[0] * S[0], Vn[1] * S[1])
                                                F = Vec2(-Vns.dot(Iv) + 0.5, -Vms.dot(Iv) + 0.5)
                                                if tattooType == 0:
                                                    dna.setClothesShirt(0)
                                                    dna.setClothesVest(0)
                                                    dna.setClothesCoat(0)
                                                    dna.setTattooChest(tattooId, F[0], F[1], S[0], rotate, color)
                                                elif tattooType == 1:
                                                    dna.setClothesShirt(0)
                                                    dna.setClothesCoat(0)
                                                    dna.setTattooZone2(tattooId, F[0], F[1], S[0], rotate, color)
                                                elif tattooType == 2:
                                                    dna.setClothesShirt(0)
                                                    dna.setClothesCoat(0)
                                                    dna.setTattooZone3(tattooId, F[0], F[1], S[0], rotate, color)
                                                elif tattooType == 3:
                                                    dna.setTattooZone4(tattooId, F[0], F[1], S[0], rotate, color)
                                                elif tattooType == 4:
                                                    dna.setTattooZone5(tattooId, F[0], F[1], S[0], rotate, color)
                                                elif tattooType == 5:
                                                    dna.setTattooZone6(tattooId, F[0], F[1], S[0], rotate, color)
                                                else:
                                                    if tattooType == 6:
                                                        dna.setTattooZone7(tattooId, F[0], F[1], S[0], rotate, color)
                                                    if tattooType == 7:
                                                        dna.setTattooZone8(tattooId, F[0], F[1], S[0], rotate, color)
                                        self.displayHuman.setDNAString(dna)
                                        self.displayHuman.generateHuman(gender, self.masterHuman)
                                        self.displayHuman.stopBlink()
                                        self.displayHuman.pose('idle', 1)
                                        lodNode = self.displayHuman.find('**/+LODNode').node()
                                        lodNode.forceSwitch(lodNode.getHighestSwitch())
                                        self.displayHuman.reparentTo(self.portraitSceneGraph)
                                        if tattooType == TattooGlobals.ZONE1:
                                            self.displayHuman.getLOD('2000').getChild(0).node().findJoint('def_spine03').getNetTransform(m)
                                            spine3Height = TransformState.makeMat(m).getPos().getZ()
                                            offsetZ = -spine3Height + chestOffset - bodyHeight * 1.2
                                            offsetX = 0.0
                                            offsetY = 3.25 + bodyOffset
                                            offsetH = 180
                                        if tattooType == TattooGlobals.ZONE2:
                                            self.displayHuman.getLOD('2000').getChild(0).node().findJoint('def_left_shoulder').getNetTransform(m)
                                            leftShoulderHeight = TransformState.makeMat(m).getPos().getZ()
                                            if gender == 'f':
                                                offsetZ = -leftShoulderHeight + 1.2 + armOffset - bodyHeight * 0.8
                                                offsetX = 0.0
                                                offsetY = 2.0 + bodyOffset
                                            else:
                                                offsetZ = -leftShoulderHeight + 0.45 + armOffset - bodyHeight * 0.8
                                                if bodyShape == 4:
                                                    offsetY = 2.5 + bodyOffset
                                                else:
                                                    offsetY = 2.0 + bodyOffset
                                                offsetX = -0.2
                                            offsetH = 105
                                        if tattooType == TattooGlobals.ZONE4:
                                            self.displayHuman.getLOD('2000').getChild(0).node().findJoint('def_head01').getNetTransform(m)
                                            headHeight = TransformState.makeMat(m).getPos().getZ()
                                            offsetZ = -headHeight - 0.1 + headOffset - bodyHeight * 1.1
                                            offsetX = 0.0
                                            offsetY = 1.5 + bodyOffset
                                            offsetH = 180
                                        offsetZ = 0
                                        offsetY = 0
                                        offsetX = 0
                                        offsetH = 0
                                    self.displayHuman.setY(offsetY)
                                    self.displayHuman.setZ(offsetZ)
                                    self.displayHuman.setX(offsetX)
                                    self.displayHuman.setH(offsetH)
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
                                    descriptionLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.getItemFlavorText(itemId), text_scale=textScale, text_wordwrap=halfWidth * 2.0 * (0.95 / textScale), text_fg=PiratesGuiGlobals.TextFG0, text_align=TextNode.ALeft, pos=(-halfWidth + textScale * 0.5, 0.0, runningVertPosition), text_pos=(0.0, -textScale))
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
                        colorPanel = self.helpFrame.attachNewNode('colorPanel')
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
                    newPosX = basePosX + (halfWidth + cellSizeX * 0.45)
                if basePosZ > 0.0:
                    newPosZ = basePosZ + cellSizeZ * 0.45
                newPosZ = basePosZ + totalHeight - cellSizeZ * 0.75
            if detailsPos:
                newPosX, newPosZ = detailsPos
        self.helpFrame.setPos(newPosX, 0, newPosZ)
        return

    def hideDetails(self, event=None):
        InventoryUIItem.InventoryUIItem.hideDetails(self, event)
        if self.helpFrame:
            self.helpFrame.destroy()
            self.helpFrame = None
        self.destroyBuffer()
        if self.realItem:
            self.realItem.removeNode()
        if self.displayHuman:
            self.displayHuman.detachNode()
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